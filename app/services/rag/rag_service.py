from typing import List
from app.services.rag.retriever import Retriever
from app.services.rag.prompt_builder import PromptBuilder
from app.services.rag.llm import LLMService
from app.api.core.config import LLM_PROVIDER
from app.api.core.logger import get_logger

logger = get_logger(__name__)


class RAGService:
    """Orchestrates complete RAG pipeline: Retrieve → Build Prompt → Generate Answer."""

    def __init__(self) -> None:
        self.retriever: Retriever = Retriever()
        self.prompt_builder: PromptBuilder = PromptBuilder()
        self.llm: LLMService = LLMService(LLM_PROVIDER)

    def answer(self, question: str, history: List[str] = None) -> str:
        """Generate answer using RAG pipeline.

        Args:
            question: User's question
            history: Conversation history (optional)

        Returns:
            Generated answer from LLM
        """
        if history is None:
            history = []

        logger.info("Processing question")

        # 1. Retrieve context from vector DB
        context: List[str] = self.retriever.get_relevant_chunks(question)
        logger.info(f"Retrieved {len(context)} chunks")

        # 2. Build prompt with context and history
        prompt: str = self.prompt_builder.build(
            question=question, context=context, history=history
        )
        logger.debug(f"Prompt built with {len(history)} history items")

        # 3. Generate response
        response: str = self.llm.generate(prompt)
        logger.info("Answer generated")

        return response
