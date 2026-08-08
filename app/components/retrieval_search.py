import streamlit as st


def render():
    """Render the semantic search form."""

    st.divider()

    st.subheader("🔎 Semantic Search")

    with st.form("semantic_search_form"):

        query = st.text_input(
            "Ask a question about this paper",
            placeholder="e.g. What is LangGraph?",
        )

        search_clicked = st.form_submit_button(
            "Search Paper",
            use_container_width=True,
        )

    return query, search_clicked