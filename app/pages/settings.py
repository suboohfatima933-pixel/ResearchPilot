from pathlib import Path

import streamlit as st

from config.settings import OLLAMA_MODEL
from services.database.document_repository import (
    DocumentRepository,
)
from services.rag.embedding_service import (
    EmbeddingService,
)


def render():
    """Render the Settings page."""

    st.title("⚙️ Settings")

    st.caption(
        "View the current ResearchPilot configuration "
        "and application storage information."
    )

    st.divider()

    # Initialize services
    document_repository = DocumentRepository()
    embedding_service = EmbeddingService()

    # Load application data
    documents = document_repository.get_all()

    vector_store_dir = Path(
        "data/vector_stores"
    )

    presentation_dir = Path(
        "data/presentations"
    )

    vector_store_count = 0

    if vector_store_dir.exists():

        vector_store_count = len(
            [
                item
                for item in vector_store_dir.iterdir()
                if item.is_dir()
            ]
        )

    presentation_count = 0

    if presentation_dir.exists():

        presentation_count = len(
            [
                item
                for item in presentation_dir.iterdir()
                if (
                    item.is_file()
                    and item.suffix.lower() == ".pptx"
                )
            ]
        )

    st.subheader("🧠 AI Configuration")

    ai_col_1, ai_col_2 = st.columns(2)

    with ai_col_1:

        st.text_input(
            "LLM Provider",
            value="Ollama",
            disabled=True,
        )

        st.text_input(
            "Active LLM Model",
            value=OLLAMA_MODEL,
            disabled=True,
        )

    with ai_col_2:

        st.text_input(
            "Embedding Model",
            value=embedding_service.MODEL_NAME,
            disabled=True,
        )

        st.text_input(
            "Embedding Dimensions",
            value="384",
            disabled=True,
        )

    st.divider()

    st.subheader("📄 Document Processing")

    processing_col_1, processing_col_2 = (
        st.columns(2)
    )

    with processing_col_1:

        st.text_input(
            "Supported Document Format",
            value="PDF",
            disabled=True,
        )

        st.text_input(
            "Maximum Upload Size",
            value="25 MB",
            disabled=True,
        )

        st.text_input(
            "Vector Store",
            value="FAISS",
            disabled=True,
        )

    with processing_col_2:

        st.text_input(
            "Vector Similarity",
            value="Cosine Similarity",
            disabled=True,
        )

        st.text_input(
            "Presentation Export",
            value="PowerPoint (.pptx)",
            disabled=True,
        )

        st.text_input(
            "Vector Store Scope",
            value="Document-Scoped",
            disabled=True,
        )

    st.divider()

    st.subheader("💾 Storage Overview")

    storage_col_1, storage_col_2, storage_col_3 = (
        st.columns(3)
    )

    with storage_col_1:

        st.metric(
            "Research Papers",
            len(documents),
        )

    with storage_col_2:

        st.metric(
            "Vector Stores",
            vector_store_count,
        )

    with storage_col_3:

        st.metric(
            "Generated Presentations",
            presentation_count,
        )

    st.divider()

    st.subheader("ℹ️ System Information")

    st.info(
        "ResearchPilot uses document-scoped vector stores "
        "to keep research papers isolated during retrieval. "
        "AI-generated outputs are grounded using retrieved "
        "evidence from indexed research content."
    )