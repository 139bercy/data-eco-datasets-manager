import csv
import json
from operator import itemgetter

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


def choose_headers(role, custom: list = None):
    headers = None
    match role:
        case "admin":
            headers = ADMIN_HEADERS
        case "user":
            headers = PUBLIC_HEADERS
    if custom:
        headers.extend(custom)
    return headers


def sort_by_field(data: list, field: str):
    if not field or data is None:
        return data
    reverse = True if field is not None and "-" in field else False
    try:
        null_fields_handler = [{k: (0 if v is None else v) for k, v in d.items()} for d in data]
        results = sorted(null_fields_handler, key=itemgetter(field.replace("-", "")), reverse=reverse)
    except TypeError:
        null_fields_handler = [{k: ("" if v is None else v) for k, v in d.items()} for d in data]
        results = sorted(null_fields_handler, key=itemgetter(field.replace("-", "")), reverse=reverse)
    return results


def to_csv(report: list, filename: str = FORMATTED_DATASETS_LIST, headers: list = None, quotes=False):
    opts = {"quotechar": '"', "quoting": csv.QUOTE_ALL} if quotes else {}
    with open(filename, "w") as output:
        writer = csv.DictWriter(f=output, fieldnames=headers, delimiter=";", extrasaction="ignore", **opts)
        writer.writeheader()
        writer.writerows(report)
    print(Fore.GREEN, f"File {filename} has been created.")


def output_results(results, detail):
    if not results:
        print(Fore.GREEN, "No results available for this keyword.")
        exit()
    for result in results:
        if detail:
            pprint(result)
    print(Fore.YELLOW, f"Resources : {len(results)}")
