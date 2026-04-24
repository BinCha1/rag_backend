from app.providers.provider_factory import ProviderFactory


class LLMService:
    """
    Handles interaction with LLM providers.
    Acts as a thin abstraction layer.
    """

    def __init__(self, provider_name: str = "gemini"):
        self.provider = ProviderFactory.get_provider(provider_name)

    def generate(self, prompt: str) -> str:
        """
        Generate response from LLM.
        """
        return self.provider.generate(prompt)
