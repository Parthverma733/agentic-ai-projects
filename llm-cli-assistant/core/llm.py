from langchain_groq import ChatGroq

from core.config import MODEL_NAME


llm = ChatGroq(
    model=MODEL_NAME,
    reasoning_format="hidden",
    temperature=0.7,
)