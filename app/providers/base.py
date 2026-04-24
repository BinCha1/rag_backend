from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate response from LLM.
        """
        pass
