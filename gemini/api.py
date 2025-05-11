# gemini/api.py
import requests
import os

def call_gemini_api(user_query):
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
    
    data = {
        "contents": [ {
            "parts": [ { "text": user_query } ]
        }]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()
