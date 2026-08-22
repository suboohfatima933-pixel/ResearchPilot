from pydantic import BaseModel

from models.presentation_slide import PresentationSlide


class PresentationContent(BaseModel):
    """Represents a complete AI-generated presentation."""

    title: str
    slides: list[PresentationSlide]