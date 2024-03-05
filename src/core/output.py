import csv
import json

from core.configuration import FORMATTED_DATASETS_LIST


def response_to_json(response):
    result = json.loads(response.text)
    return result


def pprint(response):
    result = json.dumps(response, indent=2, ensure_ascii=False)
    print(result)
    return result


def export(response, filename):
    with open(filename, "w") as file:
        json.dump(response, file, indent=2, ensure_ascii=False)
    print(f"File {filename} has been created!")


def csv_format_datasets_list(report: list, filename=FORMATTED_DATASETS_LIST):
    with open(filename, "w") as output:
        headers = report[0].keys()
        writer = csv.DictWriter(f=output, fieldnames=headers, delimiter=";")
        writer.writeheader()
        writer.writerows(report)
    print(f"{FORMATTED_DATASETS_LIST} has been upserted.")


def format_dataset_report(dataset: dict):
    dataset_report = {
        "created": dataset["created_at"],
        "updated": dataset["updated_at"],
        "dataset_id": dataset["dataset_id"],
        "title": dataset.get("metadata", {}).get("default", {}).get("title", {}).get("value", None),
        "publisher": dataset.get("metadata", {}).get("default", {}).get("publisher", {}).get("value", "Non renseigné"),
        "published": dataset["is_published"],
        "restricted": dataset["is_restricted"],
    }
    return dataset_report
