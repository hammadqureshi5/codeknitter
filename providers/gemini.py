import os

from google import genai
from dotenv import load_dotenv


load_dotenv()


class GeminiProvider:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)

    async def generate(self, model: str, prompt: str, **kwargs):

        response = self.client.models.generate_content(
            model=model,
            contents=prompt
        )

        return {
            "text": response.text,
            "provider": "google",
            "model": model
        }