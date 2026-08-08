import streamlit as st

from services.rag.embedding_service import EmbeddingService
from services.pdf.upload_service import UploadService
from services.pdf.parser_service import ParserService
from services.rag.chunk_service import ChunkService
from services.rag.vector_store_service import VectorStoreService


def render():
    """Render the Paper Analysis page."""

    st.title("📄 Paper Analysis")
    st.caption("Upload a research paper to prepare it for AI analysis.")

    uploaded_file = st.file_uploader(
        "Upload a Research Paper",
        type=["pdf"],
        accept_multiple_files=False,
    )

    if uploaded_file is None:
        st.info("Please upload a PDF research paper to continue.")
        return

    upload_service = UploadService()
    parser_service = ParserService()
    chunk_service = ChunkService()
    embedding_service = EmbeddingService()
    vector_store_service = VectorStoreService()

    try:
        with st.spinner("Uploading and analyzing PDF..."):

            file_info = upload_service.save(uploaded_file)

            document = parser_service.parse(file_info["filepath"])

            chunks = chunk_service.split(document)

            embeddings = embedding_service.embed(chunks)

            vector_store_service.create(embeddings)

            vector_store_service.save()

            vector_store_service.load()            

        st.success("PDF processed successfully!")

        # Document Metrics
     
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("File Name", file_info["original_filename"])

        with col2:
            st.metric("Pages", document.page_count)

        with col3:
            st.metric("Chunks", len(chunks))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Characters Extracted",
                f"{len(document.text):,}",
            )

        with col2:
            average_chunk_size = (
                sum(len(chunk.content) for chunk in chunks) // len(chunks)
                if chunks
                else 0
            )      

            st.metric(
                "Average Chunk Size",
                f"{average_chunk_size:,} chars",
            )

        with col3:
            st.metric(
                "Embeddings",
                len(embeddings),
            )

        # Document Metadata

        st.divider()

        st.subheader("📋 Document Metadata")

        if document.metadata:
            st.json(document.metadata)
        else:
            st.info("No metadata found in this PDF.")

        # Text Preview

        st.divider()

        st.subheader("📄 Text Preview")

        preview = document.text[:2000]

        st.text_area(
            "Extracted Text",
            preview,
            height=300,
        )

        if len(document.text) > 2000:
            st.caption("Showing the first 2,000 characters.")

        # Chunk Inspector

        st.divider()

        st.subheader("🔍 Chunk Inspector")

        for chunk in chunks:
            with st.expander(
                f"Chunk {chunk.chunk_id} • {len(chunk.content):,} characters"
            ):
                col1, col2 = st.columns(2)

                with col1:
                    st.caption(f"Start Index: {chunk.start_index:,}")

                with col2:
                    st.caption(f"End Index: {chunk.end_index:,}")

                st.text(chunk.content)

        # Chunk Statistics

        st.divider()

        st.subheader("📊 Chunk Statistics")

        chunk_sizes = [len(chunk.content) for chunk in chunks]

        if chunk_sizes:

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Smallest Chunk",
                    f"{min(chunk_sizes):,} chars",
                )

            with col2:
                st.metric(
                    "Largest Chunk",
                    f"{max(chunk_sizes):,} chars",
                )

            with col3:
                st.metric(
                    "Total Chunks",
                    len(chunks),
                )
        else:

            st.info("No chunks generated.")

        #Embedding Information

        st.divider()

        st.subheader("🧠 Embedding Information")

        if embeddings:

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Embedding Model",
                    embeddings[0].model_name,
                )

            with col2:
                st.metric(
                    "Vector Dimensions",
                    embeddings[0].dimensions,
                )         

        #Vector Store Information        

        st.divider()

        st.subheader("🗄️ Vector Store")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Backend",
                f"FAISS ({type(vector_store_service.index).__name__})",
            )

        with col2:
            st.metric(
                "Stored Vectors",
                vector_store_service.total_vectors,
            )
            

    except Exception as e:
        st.error(str(e))

