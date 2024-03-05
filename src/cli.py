import json
import os.path

import click

from core.configuration import RAW_DATASETS_PATH, DOMAIN_NAME
from core.output import export, format_dataset_report, csv_format_datasets_list

from adapters.api import get_dataset_from_api, get_dataset_from_file, query_ods
from adapters.secondaries import create_table, import_quality_report
from quality import get_dataset_quality_score


@click.group()
def cli():
    """Application CLI"""


@cli.group("api")
def api():
    """Fetch data from ODS API"""


@api.command("get-datasets")
def get_datasets():
    """Retrieve datasets"""
    response = query_ods(url=f"{DOMAIN_NAME}/api/automation/v1.0/datasets/", params={"limit": 1000})
    export(response=response, filename=RAW_DATASETS_PATH)


@cli.group("dataset")
def dataset():
    """Dataset management"""


@dataset.command("format-list")
def format_list():
    """Output datasets list in csv file"""
    with open(RAW_DATASETS_PATH, "r") as file:
        report = []
        data = json.load(file)
        datasets = data["results"]
    for dataset in datasets:
        dataset_report = format_dataset_report(dataset=dataset)
        report.append(dataset_report)
    csv_format_datasets_list(report)


@dataset.command("check-quality")
@click.option("-n", "--name", help="Dataset name")
@click.option("-o", "--output", is_flag=True, help="File name if request needs to be exported to json")
@click.option("--no-dcat", is_flag=True, help="Take out DCAT from score calculation")
@click.option("-s", "--source", type=click.Choice(["api", "file"]), default="file", help="Source")
def check_dataset_quality(name, output, no_dcat, source):
    """Check dedicated dataset quality"""
    data = {}
    if source == "api":
        data = get_dataset_from_api(name, output)
    elif source == "file":
        data = get_dataset_from_file()
    print(f'Dataset: {data["results"][0]["dataset_id"]}')
    get_dataset_quality_score(data=data, dcat=False if no_dcat else True, pprint=True)


@cli.group("database")
def database():
    """Manage sqlite3 database"""


@database.command("create")
def create_database():
    if os.path.exists("database.sqlite"):
        print("Database already exists")
        return
    create_table()


@database.command("import")
@click.option("-r", "--report", type=click.Choice(["quality"]), help="Report name")
def database_import(report):
    if report == "quality":
        import_quality_report()
        return
    print("ERROR: Fill report category name")
