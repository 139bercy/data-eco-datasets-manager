from operator import itemgetter

import click

from common import format_filename
from core.configuration import DATABASE
from core.output import to_csv
from datasets.repositories import TinyDbDatasetRepository


@click.command("publishers")
@click.option("--output", "-o", is_flag=True, default=False, help="Export in csv")
@click.option("--quotes", "-q", is_flag=True, default=False, help="Output with quotes on CSV fields")
def get_publishers(output, quotes):
    """List publishers"""
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
