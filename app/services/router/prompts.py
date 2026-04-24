# app/services/router/prompts.py

from langchain_core.prompts import ChatPromptTemplate


def get_intent_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a strict intent classifier. Respond with EXACTLY ONE WORD only:

- If user wants to book/schedule/reserve an interview/appointment: respond with 'booking'
- If user is asking a question or wants information: respond with 'question'

Do NOT explain. Do NOT add anything else. Only one word.""",
            ),
            ("human", "{input}"),
        ]
    )
