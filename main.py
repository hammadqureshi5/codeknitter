import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from openai import OpenAI


# Load environment variables
load_dotenv()

# Get API keys
gemini_api_key = os.getenv("GEMINI_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")
if not deepseek_api_key:
    raise ValueError("DEEPSEEK_API_KEY is not set")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")
if not mistral_api_key:
    raise ValueError("MISTRAL_API_KEY is not set")


# Create Clients
gemini_client = genai.Client(api_key=gemini_api_key)
deepseek_client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
openai_client = OpenAI(api_key=openai_api_key)
mistral_client = OpenAI(api_key=mistral_api_key, base_url="https://api.mistral.ai/v1")


# Price per token for input and output (based on $ per 1M tokens)
PRICING = {
    "gemini": {"input": 0.075 / 1_000_000, "output": 0.30 / 1_000_000},
    "deepseek": {"input": 0.14 / 1_000_000, "output": 0.28 / 1_000_000},
    "gpt": {"input": 0.150 / 1_000_000, "output": 0.600 / 1_000_000},
    "mistral": {"input": 0.20 / 1_000_000, "output": 0.60 / 1_000_000},
}


# Create FastAPI application
app = FastAPI(
    title="AI Gateway Prototype",
    version="0.1.0"
)


# Request model
class ChatRequest(BaseModel):
    prompt: str
    model: str


# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        input_tokens = 0
        output_tokens = 0
        provider = "unknown"

        if "gemini" in request.model.lower():
            provider = "google"
            response = gemini_client.models.generate_content(
                model=request.model,
                contents=request.prompt
            )
            response_text = response.text
            if response.usage_metadata:
                input_tokens = response.usage_metadata.prompt_token_count
                output_tokens = response.usage_metadata.candidates_token_count

        elif "deepseek" in request.model.lower():
            provider = "deepseek"
            response = deepseek_client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": request.prompt}]
            )
            response_text = response.choices[0].message.content
            if response.usage:
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens

        elif "gpt" in request.model.lower() or "o1" in request.model.lower():
            provider = "openai"
            response = openai_client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": request.prompt}]
            )
            response_text = response.choices[0].message.content
            if response.usage:
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens

        elif "mistral" in request.model.lower() or "pixtral" in request.model.lower():
            provider = "mistral"
            response = mistral_client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": request.prompt}]
            )
            response_text = response.choices[0].message.content
            if response.usage:
                input_tokens = response.usage.prompt_tokens
                output_tokens = response.usage.completion_tokens
        else:
            raise ValueError(f"Model '{request.model}' is not supported by this Gateway.")

        # Determine pricing key based on provider name
        pricing_key = provider
        if provider == "google":
            pricing_key = "gemini"
        elif provider == "openai":
            pricing_key = "gpt"

        pricing = PRICING.get(pricing_key, {"input": 0.0, "output": 0.0})
        cost = (input_tokens * pricing["input"]) + (output_tokens * pricing["output"])

        return {
            "id": f"req_{str(uuid.uuid4())[:8]}",
            "model": request.model,
            "provider": provider,
            "status": "completed",
            "output": response_text,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens
            },
            "cost": {
                "provider_cost": round(cost, 6)
            }
        }
    except Exception as e:
        # Catch errors from the client (like 404 NOT_FOUND for deepseek)
        raise HTTPException(status_code=400, detail=f"Model Error: {str(e)}")


# Mount the static directory to serve the frontend UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")