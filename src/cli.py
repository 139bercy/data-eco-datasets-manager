import json

import click

from adapters.api import (
    get_dataset_from_api,
    get_dataset_from_file,
    query_ods,
    automation_api_dataset_dto,
)
from common import format_filename, make_bytes_size_human_readable
from community import add_community_custom_view
from core.configuration import RAW_DATASETS_PATH, DOMAIN_NAME
from core.output import export, csv_format_datasets_list
from infrastructure.repositories import TinyDbDatasetRepository
from quality import get_dataset_quality_score


@click.group()
def cli():
    """Application CLI"""


@cli.group("dataset")
def dataset():
    """Dataset management"""


@dataset.command("download")
def download():
    """Retrieve datasets from ODS Automation API"""
    response = query_ods(url=f"{DOMAIN_NAME}/api/automation/v1.0/datasets/", params={"limit": 1000})
    export(response=response, filename=RAW_DATASETS_PATH)


@dataset.command("export-csv")
@click.option("-d", "--input-file-date", help="Input dataset file filled date")
@click.option("--exclude-not-published", is_flag=True, help="Exclude not published datasets")
@click.option("--exclude-restricted", is_flag=True, help="Exclude restricted datasets")
def export_to_csv(input_file_date, exclude_not_published, exclude_restricted):
    """Export datasets list in csv file"""
    filename = format_filename(filename=f"datasets.json", directory="data", date=input_file_date)
    with open(filename, "r") as file:
        report = []
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
    csv_format_datasets_list(report, output)


@dataset.command("check-quality")
@click.option("-n", "--name", help="Dataset name", required=False)
@click.option("-o", "--output", is_flag=True, help="File name if request needs to be exported to json")
@click.option("--no-dcat", is_flag=True, help="Take out DCAT from score calculation")
@click.option("-s", "--source", type=click.Choice(["api", "file"]), required=True, default="file", help="Source")
def check_dataset_quality(name, output, no_dcat, source):
    """Check dedicated dataset quality"""
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


@dataset.command("get-details")
@click.argument("name")
def get_details(name):
    """Export dedicated dataset details"""
    get_dataset_from_api(name=name, output=True)


@dataset.command("add-custom-view")
@click.argument("name")
def add_custom_view(name):
    dataset = get_dataset_from_api(name=name, output=False)
    dataset_uid = dataset["results"][0]["dataset_uid"]
    add_community_custom_view(dataset_uid=dataset_uid)


@cli.group("db")
def database():
    """Database management"""


@database.command("search")
@click.argument("chain")
def search(chain):
    repository = TinyDbDatasetRepository("data/db.json")
    results = repository.search(field="dataset_id", value=chain)
    for result in results:
        print(result["dataset_id"])


@database.command("get")
@click.argument("name")
def database_get_dataset(name):
    """Get intel on one dataset"""
    repository = TinyDbDatasetRepository("data/db.json")
    result = repository.get_one(dataset_id=name)
    formatted = json.dumps(result.__dict__, indent=2, ensure_ascii=False)
    click.echo(formatted)


@database.command("export")
@click.option("--exclude-not-published", is_flag=True, help="Exclude not published datasets")
@click.option("--exclude-restricted", is_flag=True, help="Exclude restricted datasets")
def export_to_csv(exclude_not_published, exclude_restricted):
    """Append new datasets to database"""
    repository = TinyDbDatasetRepository("data/db.json")
    query_builder = repository.builder
    if exclude_not_published:
        query_builder.add_filter("published", "==", "True")
    if exclude_restricted:
        query_builder.add_filter("restricted", "==", "False")
    datasets = repository.query()
    print(f"Datasets: {len(datasets)}")
    output_opts = f"{'-published' if exclude_not_published else ''}{'-not-restricted' if exclude_restricted else ''}"
    output = format_filename(f"datasets{output_opts}.csv", "data")
    csv_format_datasets_list(datasets, output)


@cli.group("utils")
def utils():
    """Standalone helping tools"""


@utils.command("convert-size")
@click.argument("bytes")
def convert_size(bytes):
    result = make_bytes_size_human_readable(int(bytes))
    print(f"{bytes} octets => {result}")
