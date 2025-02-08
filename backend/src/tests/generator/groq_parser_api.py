import requests
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv("API_KEY")

url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.json())