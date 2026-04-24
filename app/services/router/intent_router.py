# app/services/router/intent_router.py

from typing import Dict, Any
from app.api.core.logger import get_logger

from app.services.router.prompts import get_intent_prompt
from app.services.router.tools import TOOLS

logger = get_logger("IntentRouter")


class IntentRouter:
    """
    Custom router that uses LLM for intent classification and manual routing logic.
    - LLM only classifies intent
    - Python executes tools manually
    """

    def __init__(self, llm):
        self.llm = llm
        self.prompt = get_intent_prompt()

    # Step 1: Intent Classification

    def classify_intent(self, message: str) -> str:
        """Classify user message as 'booking' or 'question'.

        Args:
            message: User message to classify

        Returns:
            Classification: 'booking' or 'question'
        """
        # Format prompt with user message
        prompt_value = self.prompt.format_prompt(input=message)

        # Convert to string and call LLM
        response: str = self.llm.generate(str(prompt_value))

        # Extract only the word
        clean_response: str = response.strip().lower()

        # Ensure response is only 'booking' or 'question'
        if "booking" in clean_response:
            return "booking"
        else:
            return "question"

    # Step 2: Routing

    async def route(
        self, message: str, session_id: str, history: list
    ) -> Dict[str, Any]:

        try:
            logger.info("User message received")

            # 1. Get intent from LLM
            intent = self.classify_intent(message)
            logger.info(f"Intent: {intent}")

            # 2. Route manually
            if "booking" in intent:
                tool = TOOLS["booking"]

                result = tool.invoke({"message": message, "session_id": session_id})

            else:
                tool = TOOLS["question"]

                result = tool.invoke({"question": message, "history": history})

            # 3. Return response
            return {"status": "success", "intent": intent, "response": result}

        except Exception as e:
            logger.error(f"Router error: {e}", exc_info=True)

            return {"status": "error", "message": str(e)}
