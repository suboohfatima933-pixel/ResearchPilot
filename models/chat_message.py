from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Represents a message in a research conversation."""

    role: str

    content: str