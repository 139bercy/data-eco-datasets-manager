import csv
import json
import time

import click

from common import format_filename
from core.configuration import (
    ADMIN_HEADERS,
    DATABASE,
)
from core.configuration import RAW_DATASETS_PATH
from core.output import to_csv, pprint, choose_headers
from core.output import to_json
from datasets.api import get_attachments_files_extensions
from datasets.api import (
    get_dataset_from_api,
    get_dataset_from_file,
    automation_api_dataset_dto,
    download_datasets,
)
from datasets.repositories import TinyDbDatasetRepository
from datasets.usecases import search_resources
from services.community import add_community_custom_view
from services.publications import unpublish, publish
from services.quality import get_dataset_quality_score


@click.group("datasets")
def dataset():
    """Manage datasets"""


@dataset.command("import")
def api_import_dataset():
    """Fetch datasets from domain API"""
    response = download_datasets(file=None)
    to_json(response=response, filename=RAW_DATASETS_PATH)


@dataset.command("one")
@click.option("--metas", "-m", default=None, type=click.Choice(["default", "dcat", "explore"]))
@click.option("--attachments", "-a", is_flag=True, default=None)
@click.option("--output", "-o", is_flag=True, default=False)
@click.argument("name")
def api_get_one_dataset(name, metas, attachments, output):
    """Get one dataset intel"""
    data = get_dataset_from_api(name=name, output=output)
    if metas:
        pprint(data["results"][0]["metas"][metas])
    if attachments:
        extensions = get_attachments_files_extensions(files=data["results"][0]["attachments"])
        pprint(extensions)
    else:
        print(data["results"][0].keys())


@dataset.command("republish")
@click.argument("name")
def api_republish_dataset(name):
    """Unpublish and republish dataset"""
    dataset = get_dataset_from_api(name=name, output=False)
    dataset_uid = dataset["results"][0]["dataset_uid"]
    unpublish(dataset_uid=dataset_uid)
    while publish(dataset_uid=dataset_uid) == 400:
        time.sleep(1)


@dataset.command("diff")
@click.option("--file", "-f", required=False, help="File path")
def display_new_datasets(file):
    """Spot new datasets"""
    repository = TinyDbDatasetRepository(DATABASE)
    data = {dataset["dataset_id"]: dataset for dataset in repository.all()}
    datasets = download_datasets(file)
    [
        pprint(automation_api_dataset_dto(dataset))
        for dataset in datasets
        if data.get(dataset["dataset_id"], None) is None
    ]


@dataset.command("quality-check")
@click.option("-n", "--name", help="Dataset name", required=False)
@click.option("-s", "--source", type=click.Choice(["api", "file"]), required=True, default="file", help="Source")
@click.option("-o", "--output", is_flag=True, help="File name if request needs to be exported to json")
@click.option("--no-dcat", is_flag=True, help="Take out DCAT from score calculation")
def check_dataset_quality(name, output, no_dcat, source):
    """Check dataset quality from id"""
    data = {}
    if source == "api" and name is None:
        print("Dataset name is required\nAdd -n <dataset-name> to the command options")
        return
    if source == "api" and name is not None:
        data = get_dataset_from_api(name, output)
    elif source == "file":
        print("TODO: Handle dataset file does not exist case.")
        data = get_dataset_from_file()
        return
    print(f'Source: \t{source}\nDataset: \t{data["results"][0]["dataset_id"]}')
    get_dataset_quality_score(data=data, dcat=False if no_dcat else True, pprint=True)


@dataset.command("export")
@click.option("-d", "--input-file-date", help="Input dataset file filled date")
@click.option("--exclude-not-published", is_flag=True, help="Exclude not published datasets")
@click.option("--exclude-restricted", is_flag=True, help="Exclude restricted datasets")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def export_to_csv(input_file_date, exclude_not_published, exclude_restricted, quotes):
    """Export datasets list in csv file"""
    filename = format_filename(filename=f"datasets.json", directory="data", date=input_file_date)
    report = []
    with open(filename, "r") as file:
        datasets = json.load(file)
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


@dataset.group("view")
def view():
    """Add community view and discussions tab"""


@view.command("from-id")
@click.argument("name")
def add_custom_view_from_id(name):
    """Use dataset id as input"""
    dataset = get_dataset_from_api(name=name, output=False)
    dataset_uid = dataset["results"][0]["dataset_uid"]
    add_community_custom_view(dataset_uid=dataset_uid)


@view.command("from-file")
@click.argument("file")
def add_custom_view_from_name(file):
    """Use csv file with uids"""
    with open(file, "r") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            uid = row["uid"]
            add_community_custom_view(dataset_uid=uid)


@dataset.command("search")
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
    for result in enumerate(results):
        print(f'{result[0]} - {result[1]["dataset_id"]}')
    if export:
        output = format_filename(f"datasets-{field}-{chain}.csv", "data")
        to_csv(report=results, filename=output, headers=headers, quotes=quotes)
