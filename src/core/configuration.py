import os
from dotenv import load_dotenv

load_dotenv()

HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}

RAW_DATASETS_PATH = "data/datasets.json"
FORMATTED_DATASETS_LIST = "data/datasets.csv"
