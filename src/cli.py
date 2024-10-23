import csv
import json
import time
from operator import itemgetter

import click

from core.api import (
    query_ods,
)
from datasets.api import (
    get_dataset_from_api,
    get_dataset_from_automation_api,
    get_dataset_from_file,
    get_attachments_files_extensions,
    automation_api_dataset_dto,
)
from datasets.usecases import create_dataset, search_resources
from common import format_filename, make_bytes_size_human_readable
from core.configuration import (
    RAW_DATASETS_PATH,
    DOMAIN_NAME,
    ADMIN_HEADERS,
    QUALITY_HEADERS,
    GROUP_PERMISSIONS,
    DATABASE,
)
from core.output import to_json, to_csv, pprint, choose_headers, sort_by_field
from datasets.repositories import TinyDbDatasetRepository
from services import security
from services.community import add_community_custom_view
from services.publications import unpublish, publish
from services.quality import get_dataset_quality_score
from services.stats import get_dataset_stats_report
from users.repositories import TinyDbUserRepository
from users.usecases import create_user
from users.api import get_all_users_from_api


@click.group()
def cli():
    """Application CLI"""


@cli.group("dataset")
def dataset():
    """Dataset management"""


@dataset.command("upsert")
@click.argument("dataset-id")
def upsert(dataset_id):
    """Create or update value in database"""
    repository = TinyDbDatasetRepository(DATABASE)
    data = repository.one(dataset_id=dataset_id)

    automation_response = get_dataset_from_automation_api(dataset_uid=data.uid, output=False)
    automation_dto = automation_api_dataset_dto(automation_response)

    explore_response = get_dataset_from_api(name=dataset_id, output=False)
    stats_report = get_dataset_stats_report(data=explore_response, pprint=False)
    ds_report = get_dataset_quality_score(data=explore_response, dcat=True, pprint=False)
    result = {**automation_dto, **stats_report, **ds_report}

    dataset = create_dataset(repository=repository, values=result)
    pprint(dataset.__dict__)


@dataset.command("export-csv")
@click.option("-d", "--input-file-date", help="Input dataset file filled date")
@click.option("--exclude-not-published", is_flag=True, help="Exclude not published datasets")
@click.option("--exclude-restricted", is_flag=True, help="Exclude restricted datasets")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def export_to_csv(input_file_date, exclude_not_published, exclude_restricted, quotes):
    """Export datasets list in csv file"""
    filename = format_filename(filename=f"datasets.json", directory="data", date=input_file_date)
    report = []
    with open(filename, "r") as file:
        data = json.load(file)
        datasets = data["results"]
    if exclude_not_published:
        datasets = [d for d in datasets if d["is_published"] is True]
    if exclude_restricted:
        datasets = [d for d in datasets if d["is_restricted"] is False]
    for dataset in datasets:
        dataset_report = automation_api_dataset_dto(dataset=dataset)
        report.append(dataset_report)
    output_opts = f"{'-published' if exclude_not_published else ''}{'-not-restricted' if exclude_restricted else ''}"
    output = format_filename(f"datasets{output_opts}.csv", "data")
    to_csv(report=report, filename=output, headers=ADMIN_HEADERS, quotes=quotes)


@dataset.group("api")
def dataset_api():
    """Retrieve intel from API"""


@dataset_api.command("download")
def download():
    """Retrieve datasets from ODS Automation API"""
    response = query_ods(url=f"{DOMAIN_NAME}/api/automation/v1.0/datasets/", params={"limit": 1000})
    to_json(response=response, filename=RAW_DATASETS_PATH)


@dataset_api.command("one")
@click.option("--metas", "-m", default=None, type=click.Choice(["default", "dcat", "explore"]))
@click.option("--attachments", "-a", is_flag=True, default=None)
@click.option("--output", "-o", is_flag=True, default=False)
@click.argument("name")
def get_details(name, metas, attachments, output):
    """Get dedicated dataset details. See options."""
    data = get_dataset_from_api(name=name, output=output)
    if metas:
        pprint(data["results"][0]["metas"][metas])
    if attachments:
        extensions = get_attachments_files_extensions(files=data["results"][0]["attachments"])
        pprint(extensions)
    else:
        print(data["results"][0].keys())


@dataset.command("get")
@click.argument("name")
def database_get_dataset(name):
    """Get intel on one dataset from database"""
    repository = TinyDbDatasetRepository(DATABASE)
    result = repository.one(dataset_id=name)
    formatted = json.dumps(result.__dict__, indent=2, ensure_ascii=False)
    click.echo(formatted)


@dataset_api.command("check-quality")
@click.option("-n", "--name", help="Dataset name", required=False)
@click.option("-o", "--output", is_flag=True, help="File name if request needs to be exported to json")
@click.option("--no-dcat", is_flag=True, help="Take out DCAT from score calculation")
@click.option("-s", "--source", type=click.Choice(["api", "file"]), required=True, default="file", help="Source")
def check_dataset_quality(name, output, no_dcat, source):
    """Check dataset quality from id"""
    data = {}
    if source == "api" and name is None:
        print("Dataset name is required\nAdd -n <dataset-name> to the command options")
        return
    if source == "api" and name is not None:
        data = get_dataset_from_api(name, output)
    elif source == "file":
        data = get_dataset_from_file()
    print(f'Source: \t{source}\nDataset: \t{data["results"][0]["dataset_id"]}')
    get_dataset_quality_score(data=data, dcat=False if no_dcat else True, pprint=True)


@dataset_api.command("republish")
@click.argument("name")
def republish(name):
    """Unpublish and republish dataset"""
    dataset = get_dataset_from_api(name=name, output=False)
    dataset_uid = dataset["results"][0]["dataset_uid"]
    unpublish(dataset_uid=dataset_uid)
    while publish(dataset_uid=dataset_uid) == 400:
        time.sleep(1)


@dataset_api.group("custom-view")
def custom_view():
    """Add community view and discussions tab"""


@custom_view.command("from-id")
@click.argument("name")
def add_custom_view(name):
    """Use dataset id as input"""
    dataset = get_dataset_from_api(name=name, output=False)
    dataset_uid = dataset["results"][0]["dataset_uid"]
    add_community_custom_view(dataset_uid=dataset_uid)


@custom_view.command("from-file")
@click.argument("file")
def add_custom_view(file):
    """Use csv file with uids"""
    with open(file, "r") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            uid = row["uid"]
            add_community_custom_view(dataset_uid=uid)


@cli.group("database")
def database():
    """Database management"""


@database.command("export")
@click.option("--exclude-not-published", is_flag=True, help="Exclude not published datasets")
@click.option("--exclude-restricted", is_flag=True, help="Exclude restricted datasets")
@click.option("--quality", "-q", is_flag=True, default=None, help="Add quality items")
@click.option("--role", "-r", default="user", help="Public for export", type=click.Choice(["admin", "user"]))
@click.option("--header", "-h", help="Custom headers for exports", multiple=True)
@click.option("--sort", "-s", help="Sort by (-)field")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def export_to_csv(exclude_not_published, exclude_restricted, quality, header, role, sort, quotes):
    """Append new datasets to database"""
    repository = TinyDbDatasetRepository(DATABASE)
    query_builder = repository.builder
    headers = (
        list(header) if len(header) != 0 else choose_headers(role=role, custom=QUALITY_HEADERS if quality else None)
    )
    if exclude_not_published:
        query_builder.add_filter("published", "==", "True")
    if exclude_restricted:
        query_builder.add_filter("restricted", "==", "False")
    datasets = repository.query()
    results = sort_by_field(data=datasets, field=sort)
    print(f"Datasets: {len(datasets)}")
    output_opts = (
        f"-catalog{'-published' if exclude_not_published else ''}{'-not-restricted' if exclude_restricted else ''}"
    )
    filename = format_filename(f"datasets{output_opts}.csv", "data")
    to_csv(report=results, filename=filename, headers=headers)


@cli.group("resources")
def resources():
    """Manage groups and publishers"""


@resources.command("publishers")
@click.option("--output", "-o", is_flag=True, default=False, help="Export in csv")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def get_publishers(output, quotes):
    """Get publishers list"""
    repository = TinyDbDatasetRepository(DATABASE)
    data = repository.all()
    results = list([{"publisher": publisher} for publisher in set([dataset["publisher"] for dataset in data])])
    report = sorted(results, key=itemgetter("publisher"))
    if output:
        filename = format_filename(filename="publishers.csv", directory="data")
        to_csv(report=report, filename=filename, headers=["publisher"], quotes=quotes)
    else:
        for publisher in report:
            print(publisher["publisher"])


@cli.group("user")
def user_resources():
    """Users management"""


@user_resources.command("import")
def db_import_users():
    repository = TinyDbUserRepository(DATABASE)
    users = get_all_users_from_api()
    for user in users:
        create_user(repository=repository, user=user)
    click.echo(click.style(f"{len(users)} users have been imported to database {DATABASE}", fg="green"))


@user_resources.command("export")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def export_users_to_csv(quotes):
    """Export users and permissions to csv"""
    # /!\ Les ressources sont exportées directement en CSV par ODS
    data = security.get_users()
    headers = data[0].keys()
    filename = format_filename(f"users.csv", "data")
    to_csv(report=data, filename=filename, headers=headers, quotes=quotes)


@user_resources.command("search")
@click.argument("chain")
@click.option("--field", "-f", default="username", help="Field for research")
@click.option("--detail", "-d", is_flag=True, default=False, help="Print resources details")
@click.option("--export", "-e", is_flag=True, default=False, help="Export resources to csv")
@click.option("--header", "-h", help="Custom headers for exports", multiple=True)
@click.option("--sort", "-s", help="Sort by (-)field")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def search_users(chain, field, detail, export, header, sort, quotes):
    repository = TinyDbUserRepository(DATABASE)
    results = search_resources(chain=chain, detail=detail, field=field, repository=repository, sort=sort)
    headers = list(header) if len(header) != 0 else results[0].keys()
    if export:
        output = format_filename(f"users-{field}-{chain}.csv", "data")
        to_csv(report=results, filename=output, headers=headers, quotes=quotes)


@resources.group("groups")
def groups():
    """Groups management"""


@groups.command("get")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def export_groups_to_csv(quotes):
    """Export groups and permissions to csv"""
    data = security.get_groups()
    headers = [
        "uid",
        "created_at",
        "updated_at",
        "title",
        "description",
        "permissions",
        "management_limits",
        "explore_limits",
        "user_count",
    ]
    filename = format_filename(f"groups.csv", "data")
    to_csv(report=data, filename=filename, headers=headers, quotes=quotes)


@groups.command("permissions")
@click.argument("group_id")
@click.argument("title")
def update_group_permissions(group_id, title):
    security.update_one_group_permissions(group_id=group_id, title=title, permissions=GROUP_PERMISSIONS)


@cli.group("utils")
def utils():
    """Standalone helping tools"""


@utils.command("convert-size")
@click.argument("bytes")
def convert_size(bytes):
    result = make_bytes_size_human_readable(int(bytes))
    print(f"{bytes} octets => {result}")


@cli.command("search")
@click.argument("chain")
@click.option("--field", "-f", default="dataset_id", help="Field for research")
@click.option("--detail", "-d", is_flag=True, default=False, help="Print resources details")
@click.option("--export", "-e", is_flag=True, default=False, help="Export resources to csv")
@click.option("--role", "-r", default="user", help="Public for export", type=click.Choice(["admin", "user"]))
@click.option("--header", "-h", help="Custom headers for exports", multiple=True)
@click.option("--sort", "-s", help="Sort by (-)field")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def search(chain, field, detail, export, role, header, sort, quotes):
    """Retrieve datasets from database"""
    repository = TinyDbDatasetRepository(DATABASE)
    headers = list(header) if len(header) != 0 else choose_headers(role=role)
    results = search_resources(chain=chain, detail=detail, field=field, repository=repository, sort=sort)
    if export:
        output = format_filename(f"datasets-{field}-{chain}.csv", "data")
        to_csv(report=results, filename=output, headers=headers, quotes=quotes)
