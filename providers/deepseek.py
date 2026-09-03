import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class DeepSeekProvider:

    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")

        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is not set")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    async def generate(self, model: str, prompt: str, **kwargs):

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "text": response.choices[0].message.content,
            "provider": "deepseek",
            "model": model
        }