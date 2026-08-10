import streamlit as st

from services.rag.embedding_service import EmbeddingService
from services.pdf.upload_service import UploadService
from services.pdf.parser_service import ParserService
from services.rag.chunk_service import ChunkService
from services.rag.vector_store_service import VectorStoreService
from app.components.retrieval_search import render as render_retrieval_search
from services.rag.rag_service import RAGService


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
    rag_service = RAGService()

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


        query, search_clicked = render_retrieval_search()

        if search_clicked:

            if not query.strip():
                st.warning("Please enter a question.")
                return

            with st.spinner("Searching document..."):
                query_embedding = embedding_service.embed_query(query)

                results = vector_store_service.search(
                    query_embedding,
                    top_k=5,
                    min_score=0.60,
                )

            st.divider()

            st.subheader("📚 Search Results")

            if not results:
                st.info(
                    "No relevant content was found for your question. "
                    "Try rephrasing your query or ask about a topic covered in the uploaded paper."
                )
            else:

                for result in results:

                    with st.expander(
                        f"Chunk {result.chunk_id} • {result.similarity_score * 100:.1f}% Match"
                    ):                   

                        st.caption(result.document_name)

                        st.text(result.content)            

        #LLM

        st.divider()

        st.subheader("🧠 RAG Answer")

        with st.form("rag_answer_form"):

            question = st.text_input(
                "Ask the AI about this paper",
                placeholder="e.g. What is LangChain?",
            )

            answer_clicked = st.form_submit_button(
                "Ask AI",
                use_container_width=True,
            )

        if answer_clicked:

            if not question.strip():
                st.warning("Please enter a question.")
                return

            with st.spinner("Generating answer..."):

                result = rag_service.answer(question)

            st.markdown("### Answer")

            st.write(result["answer"])

            if result["sources"]:

                st.markdown("### Sources")

                for source in result["sources"]:

                    with st.expander(
                        f"Chunk {source.chunk_id} • "
                        f"{source.similarity_score * 100:.1f}% Match"
                    ):

                        st.caption(source.document_name)

                        st.text(source.content)                    

    except Exception as e:
        st.error(str(e))

