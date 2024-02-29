import os
from dotenv import load_dotenv

load_dotenv()

HEADERS = {"Authorization": f"Apikey {os.environ['KEY']}"}
