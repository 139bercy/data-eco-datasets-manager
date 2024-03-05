import os
from dotenv import load_dotenv

from common import format_filename

load_dotenv()


HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
RAW_DATASETS_PATH = format_filename("datasets.json", "data")
FORMATTED_DATASETS_LIST = format_filename("datasets.csv", "data")
