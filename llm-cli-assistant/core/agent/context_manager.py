from langchain_core.messages import SystemMessage
from core.config import SYSTEM_PROMPT

MAX_RECENT_MESSAGES = 10


def get_context(messages):
    """Build a limited context window for the LLM."""

    if not messages:
        return [
            SystemMessage(content=SYSTEM_PROMPT)
        ]

    conversation_messages = messages[1:]

    recent_messages = conversation_messages[-MAX_RECENT_MESSAGES:]

    return [
        SystemMessage(content=SYSTEM_PROMPT),
        *recent_messages
    ]