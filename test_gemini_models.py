import requests

API_KEY = "AIzaSyAOm9cS1rvI_fu-Ni-lqp1gj4NHCeQHF70"  # Replace with your real key

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
response = requests.get(url)
models = response.json()

print("Available Gemini models:")
for model in models.get("models", []):
    print("-", model.get("name"))
