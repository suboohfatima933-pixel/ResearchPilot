from pydantic import BaseModel, Field

from models.paper import Paper


class SearchRequest(BaseModel):
    """Input model for research paper search."""

    query: str = Field(..., min_length=1)
    max_results: int = Field(default=10, ge=1, le=100)


class SearchResponse(BaseModel):
    """Output model returned by the research service."""

    success: bool
    papers: list[Paper] = Field(default_factory=list)
    total_results: int = 0
    source: str = "arXiv"
    error: str | None = None