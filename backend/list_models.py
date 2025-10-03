# list_models.py
import os
import requests

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not set. Please set it before running.")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(url)
data = response.json()

print("=== Available Models ===")
if "models" in data:
    for model in data["models"]:
        print(f"- {model['name']}")
else:
    print("❌ Error listing models:", data)
