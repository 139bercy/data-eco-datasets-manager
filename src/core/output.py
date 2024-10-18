import csv
import json

from colorama import Fore

from core.configuration import FORMATTED_DATASETS_LIST, ADMIN_HEADERS, PUBLIC_HEADERS


def response_to_json(response):
    result = json.loads(response.text)
    return result


def pprint(response):
    result = json.dumps(response, indent=2, ensure_ascii=False)
    print(result)
    return result


def to_json(response, filename: str):
    with open(filename, "w") as file:
        json.dump(response, file, indent=2, ensure_ascii=False)
    print(Fore.GREEN, f"File {filename} has been created!")


def choose_headers(role):
    match role:
        case "admin":
            return ADMIN_HEADERS
        case "user":
            return PUBLIC_HEADERS


def to_csv(report: list, filename: str = FORMATTED_DATASETS_LIST, headers: list = None):
    with open(filename, "w") as output:
        writer = csv.DictWriter(f=output, fieldnames=headers, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(report)
    print(Fore.GREEN, f"File {filename} has been created.")
