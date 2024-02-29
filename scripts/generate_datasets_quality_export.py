import csv
import time

from core.api import query_ods
from quality import get_dataset_quality_score


URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"


def get_datasets():
    with open("data/datasets.csv", "r") as datasets_csv:
        reader = csv.DictReader(datasets_csv)
        result = [row for row in reader if row["published"] == "True" and row["restricted"] == "False"]
        return result


datasets = get_datasets()

with open("datasets_quality_report.csv", "w") as report_file:
    headers = [
        "created",
        "updated",
        "dataset_id",
        "title",
        "publisher",
        "published",
        "restricted",
        "description_metadata_percent",
        "default_metadata_percent",
        "dcat_metadata_percent",
        "quality_score",
    ]
    writer = csv.DictWriter(report_file, fieldnames=headers)
    writer.writeheader()
    for ds in datasets:
        ds_id = ds["dataset_id"]
        print(ds_id)
        params = {"where": f"dataset_id='{ds_id}'", "include_app_metas": True}

        data = query_ods(url=URL, params=params)
        ds_report = get_dataset_quality_score(data=data, dcat=False, pprint=True)

        # writer.writerow({**ds, **ds_report})
        time.sleep(0.5)
