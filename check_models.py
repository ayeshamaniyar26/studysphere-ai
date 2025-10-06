import os
import requests

# Make sure your GEMINI_API_KEY is set in .env or environment variables
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found. Add GEMINI_API_KEY in your .env file.")

url = "https://generativelanguage.googleapis.com/v1beta/models"
headers = {"x-goog-api-key": api_key}

response = requests.get(url, headers=headers)
print(response.json())
