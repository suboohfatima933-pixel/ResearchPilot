from pydantic import BaseModel


class SearchResult(BaseModel):
    """Represents a semantic search result."""

    chunk_id: int

    document_name: str

    similarity_score: float

    start_index: int

    end_index: int

    content: str