from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field


class Document(BaseModel):
    """Domain model representing an uploaded research document."""

    document_id: str

    filename: str
    original_filename: str
    filepath: Path
    file_size: int

    page_count: int
    text: str = ""

    metadata: dict = Field(
        default_factory=dict
    )

    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )