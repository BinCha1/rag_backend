from typing import List


class PromptBuilder:
    """Builds structured prompts for RAG with context and history."""

    def build(self, question: str, context: List[str], history: List[str]) -> str:
        """Create a structured prompt with clear instructions.

        Args:
            question: User's question
            context: List of relevant document chunks
            history: Conversation history

        Returns:
            Formatted prompt string for LLM
        """
        # Combine context chunks
        context_text: str = (
            "\n".join(context) if isinstance(context, list) else str(context)
        )

        # Format history
        history_text: str = "\n".join(history)

        prompt: str = f"""
You are a professional assistant providing accurate, structured information.

CRITICAL INSTRUCTIONS:
1. Answer ONLY based on the information provided to you.
2. Never mention "context," "document," or "provided information" in your response.
3. Format your answer clearly and professionally.
4. If information is not available, simply say: "I don't have that information."
5. Keep responses concise and natural.

RESPONSE FORMAT GUIDELINES:
- For questions about people/entities: Use bullet points for skills/attributes
- For questions about processes: Use step-by-step format
- For factual questions: Provide direct, clear answers
- Always maintain a professional, conversational tone
- Never expose internal system information

Conversation History:
{history_text}

Knowledge Base:
{context_text}

Question:
{question}

Response:
"""

        return prompt
