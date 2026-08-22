import streamlit as st

from services.database.document_repository import (
    DocumentRepository,
)
from services.insights.research_insights_service import (
    ResearchInsightsService,
)


def render():
    """Render the Research Insights page."""

    st.title("💡 Research Insights")

    st.caption(
        "Generate AI-powered insights from your "
        "processed research papers."
    )

    # Initialize services
    document_repository = DocumentRepository()
    insights_service = ResearchInsightsService()

    # Load documents
    documents = document_repository.get_all()

    if not documents:

        st.info(
            "📄 No research papers are available yet. "
            "Upload and process a paper first."
        )

        return

    document_options = {
        document.document_id: document.original_filename
        for document in documents
    }

    # Select paper
    selected_document_id = st.selectbox(
        "Select a research paper",
        options=list(document_options.keys()),
        format_func=lambda document_id:
            document_options[document_id],
    )

    selected_document_name = document_options[
        selected_document_id
    ]

    st.divider()

    # Generate insights
    if st.button(
        "✨ Generate Research Insights",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Analyzing research paper..."
            ):

                insights = insights_service.generate(
                    document_id=selected_document_id,
                    document_name=selected_document_name,
                )

        except (
            ValueError,
            FileNotFoundError,
        ) as error:

            st.error(str(error))

            return

        st.session_state.research_insights = insights

        st.session_state.insights_document_id = (
            selected_document_id
        )

        st.rerun()

    # Load generated insights
    insights = st.session_state.get(
        "research_insights"
    )

    insights_document_id = st.session_state.get(
        "insights_document_id"
    )

    if (
        insights is None
        or insights_document_id
        != selected_document_id
    ):
        return

    st.divider()

    st.subheader("📝 Executive Summary")

    st.write(
        insights.executive_summary
    )

    st.subheader("🎯 Research Problem")

    st.write(
        insights.research_problem
    )

    st.subheader("📌 Research Objectives")

    if insights.objectives:

        for objective in insights.objectives:
            st.markdown(
                f"- {objective}"
            )

    st.subheader("🔬 Methodology")

    st.write(
        insights.methodology
    )

    st.subheader("📈 Key Findings")

    if insights.key_findings:

        for finding in insights.key_findings:
            st.markdown(
                f"- {finding}"
            )

    st.subheader("⚠️ Limitations")

    if insights.limitations:

        for limitation in insights.limitations:
            st.markdown(
                f"- {limitation}"
            )

    st.subheader("🔎 Research Gaps")

    if insights.research_gaps:

        for gap in insights.research_gaps:
            st.markdown(
                f"- {gap}"
            )

    st.subheader("🌍 Practical Impact")

    st.write(
        insights.practical_impact
    )

    st.subheader("✨ Key Takeaways")

    if insights.key_takeaways:

        for takeaway in insights.key_takeaways:
            st.markdown(
                f"- {takeaway}"
            )