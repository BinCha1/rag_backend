from langchain_google_genai import ChatGoogleGenerativeAI
from app.providers.base import BaseLLMProvider
from app.api.core.config import GEMINI_MODEL, GEMINI_API_KEY


class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL, api_key=GEMINI_API_KEY, temperature=1.0, max_tokens=2048
        )

    def generate(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response.content
