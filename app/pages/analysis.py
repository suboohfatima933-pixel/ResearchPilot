import streamlit as st

from services.pdf.upload_service import UploadService
from services.pdf.parser_service import ParserService


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

    try:
        with st.spinner("Uploading and parsing PDF..."):

            file_info = upload_service.save(uploaded_file)

            document = parser_service.parse(file_info["filepath"])

        st.success("PDF uploaded and parsed successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("File Name", file_info["original_filename"])

        with col2:
            st.metric("Pages", document.page_count)

        st.metric(
            "Characters Extracted",
            f"{len(document.text):,}",
        )

        if document.metadata:
            st.subheader("📋 Document Metadata")
            st.json(document.metadata)
        else:
            st.subheader("📋 Document Metadata")
            st.info("No metadata found in this PDF.")

        st.json(document.metadata)

        st.subheader("Text Preview")

        preview = document.text[:2000]

        st.text_area(
            "Extracted Text",
            preview,
            height=300,
        )

        if len(document.text) > 2000:
            st.caption("Showing the first 2,000 characters.")

    except Exception as e:
        st.error(str(e))