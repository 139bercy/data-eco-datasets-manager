import csv
import datetime
import json
import os
import time

import requests
from dotenv import load_dotenv

# Add .env file with api key as :
# KEY=azertyuiop
load_dotenv()


def get_date_range_from_week(year, week):
    start_date = datetime.datetime.strptime(
        f"{year}-W{int(week) - 1}-1", "%Y-W%W-%w"
    ).date()
    end_date = start_date + datetime.timedelta(days=6.9)
    return start_date, end_date


def format_url(dataset, start_date=None, end_date=None):
    params = {
        "select": "count(*)",
        "where": f"""
timestamp>='{start_date}' 
AND timestamp<='{end_date}' 
AND dataset_id='{dataset}'
AND domain_id='opendatamef'
AND (api='export_dataset' OR api='download_dataset' OR api='download_dataset_alternative_export')
""",
        "limit": "-1",
        "group_by": "dataset_id,date_format(timestamp,'YYYY-MM-dd')",
    }
    request = requests.Request(
        "GET",
        "https://data.economie.gouv.fr/api/v2/monitoring/datasets/ods-api-monitoring/records",
        params=params,
    )
    result = request.prepare().url
    return result


def pprint(response):
    pretty_json = json.loads(response.text)
    result = json.dumps(pretty_json, indent=2, ensure_ascii=False)
    print(result)
    return result


def count_downloads(response):
    records = json.loads(response.text)["records"]
    start_date = records[0]["record"]["fields"]["date_format(timestamp,'YYYY-MM-dd')"]
    end_date = records[-1]["record"]["fields"]["date_format(timestamp,'YYYY-MM-dd')"]
    count = sum([record["record"]["fields"]["count(*)"] for record in records])
    return [start_date, end_date, count]


HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}

dataset = "prix-des-carburants-en-france-flux-instantane-v2"
# dataset = "prix-carburants-fichier-instantane-test-ods-copie"

with open(f"{dataset}.csv", "w") as file:
    writer = csv.writer(file, delimiter=",")
    headers = ["start_date", "end_date", "downloads"]
    writer.writerow(headers)
    for week in range(1, 44):
        start_date, end_date = get_date_range_from_week(2023, week)
        url = format_url(dataset=dataset, start_date=start_date, end_date=end_date)
        response = requests.get(url, headers=HEADERS)
        try:
            row = count_downloads(response)
        except (IndexError, KeyError):
            row = f"{start_date};{end_date};0"
        print(row)
        writer.writerow(row)
        time.sleep(3)
