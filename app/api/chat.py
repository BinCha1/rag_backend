# app/api/chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat.chat_service import ChatService
from app.api.core.logger import get_logger

logger = get_logger("ChatAPI")

router = APIRouter()
service = ChatService()


class ChatRequest(BaseModel):
    user_id: str
    query: str


@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        result = await service.chat(request.query, [], request.user_id)
        return result
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise
