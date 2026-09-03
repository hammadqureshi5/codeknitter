from providers.gemini import GeminiProvider
from providers.openai_provider import OpenAIProvider
from providers.deepseek import DeepSeekProvider
from providers.mistral import MistralProvider
from providers.cerebras import CerebrasProvider
from providers.flux import FluxProvider


class ProviderRouter:

    def __init__(self):

        self.providers = {
            "google": GeminiProvider(),
            "openai": OpenAIProvider(),
            "deepseek": DeepSeekProvider(),
            "mistral": MistralProvider(),
            "cerebras": CerebrasProvider(),
            "flux": FluxProvider()
        }

    def get_provider(self, provider_name: str):

        provider = self.providers.get(provider_name)

        if not provider:
            raise ValueError(
                f"Provider '{provider_name}' is not available"
            )

        return provider