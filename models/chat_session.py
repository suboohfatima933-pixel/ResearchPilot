from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field

from models.chat_message import ChatMessage


class ChatSession(BaseModel):
    """Represents a conversation linked to a research document."""

    id: str = Field(default_factory=lambda: str(uuid4()))

    title: str = "New Chat"

    document_id: str

    messages: list[ChatMessage] = Field(
        default_factory=list
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )