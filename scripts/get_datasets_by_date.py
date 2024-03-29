import csv

import json
from datetime import datetime

from core.configuration import RAW_DATASETS_PATH, FORMATTED_DATASETS_LIST, DOMAIN_NAME

URL = f"{DOMAIN_NAME}/api/automation/v1.0/datasets/"

# URL = "{DOMAIN_NAME}/api/automation/v1.0/users/"
START_DATE = "2023-10-01T00:00:00Z"
END_DATE = "2023-11-30T00:00:00Z"


def decode_date(chain):
    result = datetime.utcnow().strptime(chain, "%Y-%m-%dT%H:%M:%SZ")
    return result


def handle_publisher(result):
    try:
        return result["metadata"]["default"].get("publisher", "Non renseigné")["value"]
    except TypeError:
        return "NC"


# response = requests.get(url=URL, headers=constants.HEADERS, params={"limit": 800, "offset": 0})
# export(response, "datasets.json")

with open(RAW_DATASETS_PATH, "r") as file:
    with open(FORMATTED_DATASETS_LIST, "w") as output:
        writer = csv.writer(output, delimiter=",")
        writer.writerow(
            [
                "created_at",
                "dataset_id",
                "title",
                "publisher",
                "is_published",
                "is_restricted",
            ]
        )
        data = json.load(file)
        results = data["results"]
        for result in results:
            date = decode_date(result["created_at"])
            if decode_date(START_DATE) <= date <= decode_date(END_DATE):
                try:
                    writer.writerow(
                        [
                            result["created_at"],
                            result["dataset_id"],
                            result["metadata"]["default"].get("title")["value"],
                            handle_publisher(result),
                            result["is_published"],
                            result["is_restricted"],
                        ]
                    )
                except Exception as e:
                    print(e, result, "\n")
