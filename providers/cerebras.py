import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CerebrasProvider:
    def __init__(self):
        self.api_key = os.getenv("CEREBRAS_API_KEY")
        if not self.api_key:
            raise ValueError("CEREBRAS_API_KEY is not set in environment")
        self.url = "https://api.cerebras.ai/v1/chat/completions"

    async def generate(self, model: str, prompt: str, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(self.url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Cerebras API Error ({response.status_code}): {response.text}")
        
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        return {
            "text": text,
            "provider": "cerebras",
            "model": model
        }
