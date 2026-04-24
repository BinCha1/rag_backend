from langchain_openai import ChatOpenAI
from app.providers.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI LLM provider implementation.
    """

    def __init__(self):
        self.client = ChatOpenAI(model="gpt-4o-mini", temperature=1.0, max_tokens=2048)

    def generate(self, prompt: str) -> str:
        response = self.client.invoke(prompt)
        return response.content
