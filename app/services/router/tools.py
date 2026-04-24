# app/services/router/tools.py

from typing import List, Optional, Any
from langchain.tools import tool
from app.services.booking.booking_service import BookingService
from app.services.rag.rag_service import RAGService
from app.services.rag.llm import LLMService
from app.api.core.config import LLM_PROVIDER


@tool
def process_booking(message: str, session_id: str) -> str:
    """Handles booking flow (interview / appointment).

    Args:
        message: User message to process
        session_id: Session identifier for multi-turn context

    Returns:
        Result of booking processing
    """
    llm: LLMService = LLMService(LLM_PROVIDER)
    service: BookingService = BookingService(llm)
    result: Optional[Any] = service.process(message, session_id)
    return str(result)


@tool
def answer_question(question: str, history: Optional[List[str]] = None) -> str:
    """Handles RAG-based question answering.

    Args:
        question: User question
        history: Conversation history

    Returns:
        Answer from RAG service
    """
    rag: RAGService = RAGService()
    result: str = rag.answer(question, history or [])
    return str(result)


# Register tools
TOOLS: dict = {"booking": process_booking, "question": answer_question}
