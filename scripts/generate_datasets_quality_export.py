import csv
import time

from adapters.api import query_ods
from adapters.usecases import create_dataset
from common import format_filename
from core.configuration import FORMATTED_DATASETS_LIST, DOMAIN_NAME
from infrastructure.repositories import TinyDbDatasetRepository
from quality import get_dataset_quality_score
from stats import get_dataset_stats_report

URL = f"{DOMAIN_NAME}/api/explore/v2.1/catalog/datasets/"
DCAT = True
REPOSITORY = TinyDbDatasetRepository(name="db.json")


def get_datasets():
    with open(FORMATTED_DATASETS_LIST, "r") as datasets_csv:
        reader = csv.DictReader(datasets_csv, delimiter=";")
        result = [row for row in reader]
        # result = [row for row in reader if row["published"] == "True" and row["restricted"] == "False"]
        return result


datasets = get_datasets()
filename = format_filename(filename="datasets-quality-report.csv")

with open(f"data/{filename}", "w") as report_file:
    headers = [
        "buid",
        "created",
        "updated",
        "dataset_id",
        "title",
        "publisher",
        "published",
        "restricted",
        "download_count",
        "records_size",
        "size",
        "records_count",
        "api_call_count",
        "popularity_score",
        "description_score",
        "default_score",
        "dcat_score",
        "quality_score",
    ]
    writer = csv.DictWriter(report_file, fieldnames=headers, delimiter=";")
    writer.writeheader()
    for ds in enumerate(datasets):
        ds_id = ds[1]["dataset_id"]
        print(f"{ds[0]}- {ds_id}")
        params = {"where": f"dataset_id='{ds_id}'", "include_app_metas": True}

        data = query_ods(url=URL, params=params)
        stats_report = get_dataset_stats_report(data=data, pprint=False)
        ds_report = get_dataset_quality_score(data=data, dcat=DCAT, pprint=False)
        dataset = {**ds[1], **stats_report, **ds_report}
        dataset = create_dataset(repository=REPOSITORY, values=dataset)
        writer.writerow(dataset.__dict__)
        time.sleep(0.1)
