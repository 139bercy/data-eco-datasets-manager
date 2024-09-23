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


def csv_format_datasets_list(report: list, filename: str = FORMATTED_DATASETS_LIST, headers: list = None):
    with open(filename, "w") as output:
        writer = csv.DictWriter(f=output, fieldnames=headers, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(report)
    print(f"{filename} has been created.")
