import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class OpenAIProvider:

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)

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
            "provider": "openai",
            "model": model
        }