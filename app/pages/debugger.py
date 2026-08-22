import streamlit as st

from services.database.document_repository import (
    DocumentRepository,
)
from services.rag.retrieval_debugger_service import (
    RetrievalDebuggerService,
)


def render():
    """Render the Retrieval Debugger page."""

    st.title("🧠 Retrieval Debugger")

    st.caption(
        "Inspect how ResearchPilot retrieves "
        "evidence from your research papers."
    )

    # Initialize services
    document_repository = DocumentRepository()
    debugger_service = RetrievalDebuggerService()

    # Load documents
    documents = document_repository.get_all()

    if not documents:

        st.info(
            "📄 No research papers are available yet. "
            "Upload a paper first."
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

    st.caption(
        f"📄 Debugging: "
        f"{document_options[selected_document_id]}"
    )

    st.divider()

    # Query
    query = st.text_input(
        "Test retrieval query",
        placeholder=(
            "Example: What methodology was used "
            "in this research?"
        ),
    )

    # Retrieval settings
    settings_col, value_col = st.columns(2)

    with settings_col:

        top_k = st.slider(
            "Top K results",
            min_value=1,
            max_value=10,
            value=5,
        )

    with value_col:

        min_score = st.slider(
            "Minimum similarity score",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05,
        )

    # Run debugger
    if st.button(
        "🔍 Run Retrieval Debug",
        type="primary",
        use_container_width=True,
    ):

        if not query.strip():

            st.warning(
                "Enter a query to debug retrieval."
            )

            return

        try:

            with st.spinner(
                "Inspecting retrieval..."
            ):

                debug_result = (
                    debugger_service.debug(
                        query=query,
                        document_id=selected_document_id,
                        top_k=top_k,
                        min_score=min_score,
                    )
                )

        except (
            ValueError,
            FileNotFoundError,
        ) as error:

            st.error(str(error))

            return

        # Query details
        st.divider()

        st.subheader("📊 Retrieval Overview")

        metric_col_1, metric_col_2, metric_col_3, metric_col_4 = (
            st.columns(4)
        )

        with metric_col_1:

            st.metric(
                "Query Dimensions",
                debug_result[
                    "query_dimensions"
                ],
            )

        with metric_col_2:

            st.metric(
                "Total Vectors",
                debug_result[
                    "total_vectors"
                ],
            )

        with metric_col_3:

            st.metric(
                "Results Found",
                len(
                    debug_result["results"]
                ),
            )

        with metric_col_4:

            st.metric(
                "Min. Similarity",
                f"{min_score:.2f}",
            )

        st.divider()

        # Retrieved chunks
        st.subheader("📚 Retrieved Chunks")

        results = debug_result["results"]

        if not results:

            st.warning(
                "No chunks matched the selected "
                "similarity threshold."
            )

            return

        for position, result in enumerate(
            results,
            start=1,
        ):

            score_percent = (
                result.similarity_score * 100
            )

            with st.expander(
                f"#{position} — "
                f"{score_percent:.1f}% similarity",
                expanded=position == 1,
            ):

                st.caption(
                    f"Chunk ID: {result.chunk_id}"
                )

                st.caption(
                    f"Character range: "
                    f"{result.start_index} → "
                    f"{result.end_index}"
                )

                st.progress(
                    min(
                        max(
                            result.similarity_score,
                            0.0,
                        ),
                        1.0,
                    )
                )

                st.markdown(
                    result.content
                )