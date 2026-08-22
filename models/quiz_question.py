from pydantic import BaseModel


class QuizQuestion(BaseModel):
    """Represents a multiple-choice quiz question."""

    question: str
    options: list[str]
    correct_answer: str
    explanation: str