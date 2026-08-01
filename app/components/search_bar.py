import streamlit as st


def render():
    """Reusable search bar component."""

    with st.form("research_search_form"):
        col1, col2 = st.columns([5, 1])

        with col1:
            query = st.text_input(
                "Research Topic",
                placeholder="e.g. GraphRAG for Question Answering",
                label_visibility="collapsed",
            )

        with col2:
            search_clicked = st.form_submit_button(
                "Search",
                use_container_width=True,
            )

    return query, search_clicked