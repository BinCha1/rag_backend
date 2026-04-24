from langchain_groq import ChatGroq
from app.providers.base import BaseLLMProvider
from app.api.core.config import GROQ_MODEL, GROQ_API_KEY


class GroqProvider(BaseLLMProvider):
    def __init__(self):
        self.model = ChatGroq(
            model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=1.0, max_tokens=2048
        )

    def generate(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response.content
