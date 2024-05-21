# fridaylabs/fridaylabs.py

import requests

class FridayLabs:
    def __init__(self, api_key, api_url):
        self.api_key = api_key
        self.api_url = api_url

    def chat_completion(self, model, messages, temperature=1, max_tokens=256, top_p=1, frequency_penalty=0, presence_penalty=0):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        return response.json()
