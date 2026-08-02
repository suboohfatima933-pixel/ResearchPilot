from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Domain model representing an uploaded research document."""

    filename: str
    filepath: Path

    page_count: int

    text: str

    metadata: dict = Field(default_factory=dict)

    uploaded_at: datetime = Field(default_factory=datetime.now)