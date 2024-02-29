import os
from dotenv import load_dotenv

load_dotenv()

HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}
DOMAIN_NAME = os.environ["DOMAIN_NAME"]
RAW_DATASETS_PATH = "data/datasets.json"
FORMATTED_DATASETS_LIST = "data/datasets.csv"
