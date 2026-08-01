from models.paper import Paper
from services.research.arxiv_provider import ArxivProvider


class ResearchService:
    """Business logic for research discovery."""

    def __init__(self):
        self.provider = ArxivProvider()

    def search(self, query: str, max_results: int = 10) -> list[Paper]:
        try:
            return self.provider.search(
                query=query,
                max_results=max_results,
            )

        except Exception as e:
            raise RuntimeError(
                f"Unable to retrieve papers from arXiv: {e}"
            ) from e