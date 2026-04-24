from app.services.router.intent_router import IntentRouter
from app.api.core.config import LLM_PROVIDER
from app.services.rag.llm import LLMService


class ChatService:
    """Orchestrates the entire chat flow, including intent routing."""

    def __init__(self):
        self.llm = LLMService(LLM_PROVIDER)
        self.router = IntentRouter(self.llm)

    async def chat(self, message: str, history: list[str], session_id: str):

        return await self.router.route(message, session_id, history)
