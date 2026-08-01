import streamlit as st

from app.components.empty_state import render as render_empty_state
from app.components.paper_card import render as render_paper_card
from app.components.search_bar import render as render_search_bar

from services.research.research_service import ResearchService


def render():
    """Render the Research Discovery page."""

    st.title("🔍 Research Discovery")
    st.caption("Discover research papers from arXiv.")

    query, search_clicked = render_search_bar()

    # Show empty state on initial page load
    if not search_clicked:
        render_empty_state()
        return

    # Validate user input
    if not query.strip():
        st.warning("Please enter a research topic.")
        return

    service = ResearchService()

    try:
        with st.spinner("Searching arXiv..."):
            papers = service.search(
                query=query,
                max_results=10,
            )

    except RuntimeError as e:
        st.error(str(e))
        return

    if not papers:
        st.info(
            "No research papers were found for your search. "
            "Try a different topic or broader keywords."
        )
        return

    st.success(f"Found {len(papers)} papers")

    for paper in papers:
        render_paper_card(paper)