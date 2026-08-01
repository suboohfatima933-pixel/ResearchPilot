import streamlit as st

from models.paper import Paper


def render(paper: Paper):
    """Render a research paper card."""

    with st.container(border=True):

        st.subheader(paper.title)

        st.caption(f"👤 {', '.join(paper.authors)}")

        st.caption(
            f"📅 Published: {paper.published.strftime('%d %b %Y')}"
        )

        st.caption(
            f"🏷 Categories: {', '.join(paper.categories)}"
        )

        st.markdown("### Abstract")

        st.write(paper.abstract)

        col1, col2 = st.columns(2)

        with col1:
            st.link_button(
                "📄 Open PDF",
                paper.pdf_url,
                use_container_width=True,
            )

        with col2:
            st.link_button(
                "🔗 View on arXiv",
                paper.arxiv_url,
                use_container_width=True,
            )