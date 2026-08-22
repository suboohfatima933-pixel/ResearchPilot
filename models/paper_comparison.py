from pydantic import BaseModel

from models.search_result import SearchResult


class PaperComparison(BaseModel):
    """Represents a comparison between two research papers."""

    paper_a_name: str
    paper_b_name: str

    comparison_type: str
    answer: str

    paper_a_sources: list[SearchResult]
    paper_b_sources: list[SearchResult]