import os
from dotenv import load_dotenv
load_dotenv()
access_token = os.getenv("PANDASCORE_API_KEY")
headers = {
    "accept": "application/json",
    "authorization": "Bearer " + access_token
}
