import json

import click

from common import format_filename
from core.configuration import (
    QUALITY_HEADERS,
    DATABASE,
)
from core.output import to_csv, pprint, choose_headers, sort_by_field
from datasets.api import (
    get_dataset_from_api,
    get_dataset_from_automation_api,
    automation_api_dataset_dto,
)
from datasets.repositories import TinyDbDatasetRepository
from datasets.usecases import create_dataset
from services.quality import get_dataset_quality_score
from services.stats import get_dataset_stats_report
from users.api import get_all_users_from_api
from users.repositories import TinyDbUserRepository
from users.usecases import import_user


@click.group("db")
def database():
    """Manage database"""


@database.group("ds")
def database_datasets():
    """Manage datasets"""


@database_datasets.command("one")
@click.argument("name")
def database_get_dataset(name):
    """Get intel on one dataset from database"""
    repository = TinyDbDatasetRepository(DATABASE)
    result = repository.one(dataset_id=name)
    formatted = json.dumps(result.__dict__, indent=2, ensure_ascii=False)
    click.echo(formatted)


@database_datasets.command("upsert")
@click.argument("dataset-id")
@click.option("--uid", "-u", required=False, help="Dataset uid")
def upsert(dataset_id, uid):
    """Create or update dataset in database"""
    repository = TinyDbDatasetRepository(DATABASE)
    data = repository.one(dataset_id=dataset_id)

    automation_response = get_dataset_from_automation_api(dataset_uid=uid or data.uid, output=False)
    automation_dto = automation_api_dataset_dto(automation_response)

    explore_response = get_dataset_from_api(name=dataset_id, output=False)
    stats_report = get_dataset_stats_report(data=explore_response, pprint=False)
    ds_report = get_dataset_quality_score(data=explore_response, dcat=True, pprint=False)
    result = {**automation_dto, **stats_report, **ds_report}

    dataset = create_dataset(repository=repository, values=result)
    pprint(dataset.__dict__)


@database_datasets.command("export")
@click.option("--exclude-not-published", is_flag=True, help="Exclude not published datasets")
@click.option("--exclude-restricted", is_flag=True, help="Exclude restricted datasets")
@click.option("--quality", "-q", is_flag=True, default=None, help="Add quality items")
@click.option("--role", "-r", default="user", help="Public for export", type=click.Choice(["admin", "user"]))
@click.option("--header", "-h", help="Custom headers for exports", multiple=True)
@click.option("--sort", "-s", help="Sort by (-)field")
@click.option("--quotes", is_flag=True, default=False, help="Output with quotes on CSV fields")
def export_to_csv(exclude_not_published, exclude_restricted, quality, header, role, sort, quotes):
    """Export datasets to database"""
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


@database.group("users")
def database_users():
    """Manage users"""


@database_users.command("import")
def db_import_users():
    """Import users to database"""
    repository = TinyDbUserRepository(DATABASE)
    users = get_all_users_from_api()
    for user in users:
        import_user(repository=repository, user=user)
    click.echo(click.style(f"{len(users)} users have been imported to database {DATABASE}", fg="green"))
