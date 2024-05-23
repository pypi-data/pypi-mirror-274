# mask_key/api.py
import requests

API_URL = "http://127.0.0.1:8000/generate-mask-keys-for-user"

def generate_keys(user_data):
    try:
        response = requests.post(API_URL, json=user_data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
