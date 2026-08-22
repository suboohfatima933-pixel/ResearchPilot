from pydantic import BaseModel


class PresentationSlide(BaseModel):
    """Represents one slide in a generated presentation."""

    title: str
    content: list[str]
    speaker_notes: str