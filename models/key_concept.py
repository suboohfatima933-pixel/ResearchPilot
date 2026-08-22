from pydantic import BaseModel


class KeyConcept(BaseModel):
    """Represents an important concept from a research paper."""

    concept: str
    explanation: str