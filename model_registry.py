MODEL_REGISTRY = {

    # Gemini
    "gemini-3.7-flash": {
        "provider": "google",
        "provider_model": "gemini-3.7-flash"
    },

    # OpenAI
    "gpt-4o-mini": {
        "provider": "openai",
        "provider_model": "gpt-4o-mini"
    },

    # DeepSeek
    "deepseek-chat": {
        "provider": "deepseek",
        "provider_model": "deepseek-chat"
    },

    # Mistral
    "mistral-large-latest": {
        "provider": "mistral",
        "provider_model": "mistral-large-latest"
    }
}


def get_model(model_name: str):

    model = MODEL_REGISTRY.get(model_name)

    if not model:
        raise ValueError(
            f"Model '{model_name}' is not registered"
        )

    return model