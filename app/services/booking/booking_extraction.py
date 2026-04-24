# app/services/booking/booking_extraction.py

import json
from typing import Dict, Any
from app.api.core.logger import get_logger

logger = get_logger(__name__)


class BookingExtractor:
    """Extracts booking fields (name, email, date, time) from user messages using LLM."""

    BOOKING_RULES: str = """CRITICAL RULES:
- Return ONLY raw JSON, absolutely NO markdown code blocks
- Do NOT wrap with ```json or ``` markers
- Only include fields that are present
- Do NOT ask questions or add explanations"""

    def __init__(self, llm: Any) -> None:
        """Initialize with LLM service.

        Args:
            llm: LLMService instance for field extraction
        """
        self.llm: Any = llm

    def _get_prompt(self, query: str, is_continuation: bool) -> str:
        """Build extraction prompt based on context.

        Args:
            query: User message to extract from
            is_continuation: Whether this is a continuation of existing booking

        Returns:
            Formatted prompt for LLM
        """
        if is_continuation:
            context = "The user is ALREADY in a booking flow. Extract ANY booking-related fields found (name, email, date, time). Add 'is_booking': true if any field found."
        else:
            context = "If user is booking/reserving/scheduling, extract: name, email, date, time (if found) and add 'is_booking': true. If NOT booking-related, return {}."

        return f"""Extract booking information.

{context}

{self.BOOKING_RULES}

User message: {query}

Return ONLY JSON object, nothing else:"""

    def extract(self, query: str, is_continuation: bool = False) -> Dict[str, Any]:
        """Extract booking fields from user message.

        Args:
            query: User message to extract from
            is_continuation: Whether continuing from previous turn

        Returns:
            Dict with extracted fields or empty dict if extraction fails
        """
        prompt: str = self._get_prompt(query, is_continuation)
        response: str = self.llm.generate(prompt)

        if not response or not response.strip():
            logger.debug(f"Empty response from LLM for query: {query}")
            return {}

        try:
            extracted: Dict[str, Any] = json.loads(response)
            logger.debug(f"Extracted booking data: {extracted}")
            return extracted
        except json.JSONDecodeError as e:
            logger.error(f"JSON extraction failed: {e}. Response: {response}")
            return {}
