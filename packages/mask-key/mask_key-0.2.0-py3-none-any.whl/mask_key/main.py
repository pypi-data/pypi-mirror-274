# mask_key/main.py
import json
import os
from dotenv import load_dotenv, set_key
from .api import generate_keys
from .utils import check_env_exists

def ask_questions():
    user_data = {}
    user_data['name'] = input("What is your name? ")
    user_data['age'] = input("What is your age? ")
    user_data['color'] = input("What color do you like? ")
    user_data['email'] = input("What is your email address? ")
    return user_data

def save_to_json(data, filename='user_data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)

def main():
    if check_env_exists():
        print(".env file already exists.")
        return

    user_data = ask_questions()
    save_to_json(user_data)

    response = generate_keys(user_data)
    
    if response:
        app_key, company_key = response['application_key'], response['company_key']
    else:
        app_key, company_key = '', ''
        print("No response from server. Keys will be empty.")

    load_dotenv()
    set_key('.env', 'APPLICATION_KEY', app_key)
    set_key('.env', 'COMPANY_KEY', company_key)
    
    print("Keys have been saved to .env file.")
