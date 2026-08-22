import streamlit as st

from services.comparison.paper_comparison_service import (
    PaperComparisonService,
)
from services.database.document_repository import (
    DocumentRepository,
)


def render():
    """Render the Compare Papers page."""

    st.title("⚖️ Compare Papers")
    st.caption(
        "Compare two research papers using AI-powered evidence."
    )

    # Initialize services
    comparison_service = PaperComparisonService()
    document_repository = DocumentRepository()

    # Load documents
    documents = document_repository.get_all()

    if len(documents) < 2:

        st.info(
            "Upload at least two research papers "
            "to compare them."
        )

        return

    document_options = {
        document.document_id: document.original_filename
        for document in documents
    }

    # Paper selection
    col1, col2 = st.columns(2)

    with col1:

        paper_a_id = st.selectbox(
            "📄 Paper A",
            options=list(document_options.keys()),
            format_func=lambda document_id:
                document_options[document_id],
            key="paper_a",
        )

    with col2:

        paper_b_options = [
            document_id
            for document_id in document_options
            if document_id != paper_a_id
        ]

        paper_b_id = st.selectbox(
            "📄 Paper B",
            options=paper_b_options,
            format_func=lambda document_id:
                document_options[document_id],
            key="paper_b",
        )

    st.divider()

    # Comparison type
    st.subheader("🔍 What would you like to compare?")

    comparison_type = st.radio(
        "Comparison focus",
        options=[
            "Overall Comparison",
            "Research Objectives",
            "Methodology",
            "Key Findings",
            "Strengths and Limitations",
            "Conclusions",
            "Custom Question",
        ],
        horizontal=True,
    )

    comparison_questions = {
        "Overall Comparison": (
            "Compare these two research papers overall, "
            "including their objectives, methodology, "
            "key findings, and conclusions."
        ),
        "Research Objectives": (
            "Compare the research objectives and "
            "main questions addressed by these two papers."
        ),
        "Methodology": (
            "Compare the research methodologies, "
            "data, approaches, and techniques used "
            "in these two papers."
        ),
        "Key Findings": (
            "Compare the key findings and results "
            "presented in these two research papers."
        ),
        "Strengths and Limitations": (
            "Compare the strengths and limitations "
            "of these two research papers."
        ),
        "Conclusions": (
            "Compare the conclusions and implications "
            "of these two research papers."
        ),
    }

    question = comparison_questions.get(
        comparison_type,
        "",
    )

    if comparison_type == "Custom Question":

        question = st.text_area(
            "Enter your comparison question",
            placeholder=(
                "e.g. Which paper provides stronger "
                "evidence for its conclusions?"
            ),
        )

    # Compare action
    if st.button(
        "⚖️ Compare Papers",
        type="primary",
        use_container_width=True,
    ):

        if not question.strip():

            st.warning(
                "Please enter a comparison question."
            )

            return

        paper_a_name = document_options[
            paper_a_id
        ]

        paper_b_name = document_options[
            paper_b_id
        ]

        try:

            with st.spinner(
                "Analyzing and comparing both papers..."
            ):

                comparison = comparison_service.compare(
                    question=question,
                    paper_a_id=paper_a_id,
                    paper_a_name=paper_a_name,
                    paper_b_id=paper_b_id,
                    paper_b_name=paper_b_name,
                )

            st.divider()

            # Comparison result
            st.subheader("🤖 AI Comparison")

            st.markdown(
                comparison.answer
            )

        except Exception as e:

            st.error(str(e))