import csv
import time

from adapters.api import query_ods
from common import format_filename
from core.configuration import FORMATTED_DATASETS_LIST, DOMAIN_NAME
from quality import get_dataset_quality_score


URL = f"{DOMAIN_NAME}/api/explore/v2.1/catalog/datasets/"
DCAT = False


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
        "created",
        "updated",
        "dataset_id",
        "title",
        "publisher",
        "published",
        "restricted",
        "description_score",
        "default_score",
        "dcat_score",
        "quality_score",
    ]
    writer = csv.DictWriter(report_file, fieldnames=headers, delimiter=";")
    writer.writeheader()
    for ds in datasets:
        ds_id = ds["dataset_id"]
        print(ds_id)
        params = {"where": f"dataset_id='{ds_id}'", "include_app_metas": True}

        data = query_ods(url=URL, params=params)
        ds_report = get_dataset_quality_score(data=data, dcat=DCAT, pprint=True)

        writer.writerow({**ds, **ds_report})
        time.sleep(0.5)
