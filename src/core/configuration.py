import os
from dotenv import load_dotenv

from common import format_filename

load_dotenv()


HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
RAW_DATASETS_PATH = format_filename("datasets.json", "data")
FORMATTED_DATASETS_LIST = format_filename("datasets.csv", "data")

CUSTOM_HEADERS = [
    "buid",
    "created",
    "updated",
    "dataset_id",
    "title",
    "publisher",
    "published",
    "restricted",
    "records_size",
    "size",
    "records_count",
    "link",
]

GROUP_PERMISSIONS = [
    "create_page",
    "manage_page",
    "create_dataset",
    "publish_dataset",
    "manage_dataset",
    "explore_monitoring",
    # "edit_domain",
    # "edit_page",
    # "explore_restricted_page",
    # "edit_dataset",
    # "explore_restricted_dataset",
    # "edit_reuse",
    # "manage_subdomains",
    # "edit_theme",
]
