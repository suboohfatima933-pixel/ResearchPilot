from pydantic import BaseModel

from models.key_concept import KeyConcept
from models.flashcard import Flashcard
from models.quiz_question import QuizQuestion


class LearningContent(BaseModel):
    """Contains AI-generated learning material for a research paper."""

    simplified_explanation: str
    key_concepts: list[KeyConcept]
    flashcards: list[Flashcard]
    quiz_questions: list[QuizQuestion]