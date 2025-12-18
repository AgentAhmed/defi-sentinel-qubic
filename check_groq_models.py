import os
import requests
from dotenv import load_dotenv


# Load variables from .env into environment
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set")

url = "https://api.groq.com/openai/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}"
}

res = requests.get(url, headers=headers)
res.raise_for_status()

print("Available Groq models:\n")
for m in res.json()["data"]:
    print("-", m["id"])
