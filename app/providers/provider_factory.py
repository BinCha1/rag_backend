from app.providers.openai_provider import OpenAIProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.groq_provider import GroqProvider


class ProviderFactory:
    """
    Returns provider based on config.
    """

    @staticmethod
    def get_provider(provider_name: str):

        if provider_name == "openai":
            return OpenAIProvider()

        elif provider_name == "gemini":
            return GeminiProvider()

        elif provider_name == "groq":
            return GroqProvider()

        else:
            raise ValueError("Unsupported provider")
