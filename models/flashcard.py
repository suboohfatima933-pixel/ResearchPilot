from pydantic import BaseModel


class Flashcard(BaseModel):
    """Represents a question and answer learning card."""

    question: str
    answer: str