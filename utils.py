import requests
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

def get_available_models_groq():
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/models"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers).json()

    for item in response["data"]:
        print(item["id"], "\n")