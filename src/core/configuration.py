import os
from dotenv import load_dotenv

from common import format_filename

load_dotenv()


HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
RAW_DATASETS_PATH = format_filename("datasets.json", "data")
FORMATTED_DATASETS_LIST = format_filename("datasets.csv", "data")
DATABASE = os.environ["DATABASE"]

DATASET_URL = f"{DOMAIN_NAME}/api/explore/v2.1/catalog/datasets/"

ADMIN_HEADERS = [
    "uid",
    "buid",
    "created",
    "updated",
    "publisher",
    "dataset_id",
    "title",
    "published",
    "restricted",
    "attachments",
    "records_size",
    "size",
    "records_count",
    "download_count",
    "link",
]

PUBLIC_HEADERS = [
    "created",
    "updated",
    "publisher",
    "dataset_id",
    "title",
    "published",
    "restricted",
    "attachments",
    "records_size",
    "size",
    "records_count",
    "download_count",
    "link",
]


QUALITY_HEADERS = ["description_score", "default_score", "dcat_score", "quality_score"]


AVAILABLE_PERMISSIONS = [
    "create_page",
    "manage_page",
    "create_dataset",
    "publish_dataset",
    "manage_dataset",
    "explore_monitoring",
    "edit_domain",
    "edit_page",
    "explore_restricted_page",
    "edit_dataset",
    "explore_restricted_dataset",
    "edit_reuse",
    "manage_subdomains",
    "edit_theme",
]

DEFAULT_GROUP_PERMISSIONS = [
    "create_page",
    "manage_page",
    "create_dataset",
    "publish_dataset",
    "manage_dataset",
]
