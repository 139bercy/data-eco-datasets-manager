import json
import csv

from src.core.api import query_ods
from src.core.output import export

FETCH_FROM_API = False
FILENAME = "datasets"
if FETCH_FROM_API:
    response = query_ods(
        url="https://data.economie.gouv.fr/api/automation/v1.0/datasets/",
        params={"limit": 1000}
    )
    export(response=response, filename=f"../data/{FILENAME}.json")
else:
    with open(f"../data/{FILENAME}.json", "r") as file:
        report = []
        data = json.load(file)
        datasets = data["results"]
        for enum in enumerate(datasets):
            number, dataset = enum
            dataset_report = {
                "created": dataset["created_at"],
                "updated": dataset["updated_at"],
                "dataset_id": dataset["dataset_id"],
                "title": dataset.get("metadata", {}).get("default", {}).get("title", {}).get("value", None),
                "publisher": dataset.get("metadata", {}).get("default", {}).get("publisher", {}).get("value", None),
                "published": dataset["is_published"],
                "restricted": dataset["is_restricted"],
            }
            report.append(dataset_report)
        with open("../data/datasets.csv", "w") as output:
            headers = report[0].keys()
            writer = csv.DictWriter(f=output, fieldnames=headers)
            writer.writeheader()
            writer.writerows(report)
