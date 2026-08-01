import arxiv

from models.paper import Paper


class ArxivProvider:
    """Handles communication with the arXiv API."""

    def search(self, query: str, max_results: int = 10) -> list[Paper]:
        client = arxiv.Client()

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        papers: list[Paper] = []

        for result in client.results(search):
            papers.append(
                Paper(
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    abstract=result.summary,
                    published=result.published,
                    pdf_url=result.pdf_url,
                    arxiv_url=result.entry_id,
                    categories=result.categories,
                )
            )

        return papers