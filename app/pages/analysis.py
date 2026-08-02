import streamlit as st

from services.pdf.upload_service import UploadService


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

    service = UploadService()

    try:
        file_info = service.save(uploaded_file)

        st.success("PDF uploaded successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("File Name", file_info["original_filename"])

        with col2:
            st.metric(
                "File Size",
                f"{file_info['size'] / (1024 * 1024):.2f} MB",
            )

        st.info("✅ Ready for PDF parsing in Phase 5.")

    except ValueError as e:
        st.error(str(e))