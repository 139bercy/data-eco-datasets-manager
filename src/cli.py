import os.path

import click

from core.api import get_dataset_from_api, get_dataset_from_file
from core.db import create_table, import_quality_report
from quality import get_dataset_quality_score


@click.group()
def cli(args=None):
    """Application CLI"""


@cli.group("dataset")
def dataset():
    """Dataset management"""


@dataset.command("check-quality")
@click.option("-n", "--name", help="Dataset name")
@click.option("-o", "--output", help="File name if request needs to be exported to json")
@click.option("--no-dcat", is_flag=True, help="Take out DCAT from score calculation")
@click.option("-s", "--source", type=click.Choice(["api", "file"]), default="file", help="Source")
def check_dataset_quality(name, output, no_dcat, source):
    data = {}
    print(no_dcat)
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
