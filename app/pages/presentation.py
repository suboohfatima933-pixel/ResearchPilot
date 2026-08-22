import streamlit as st

from services.database.document_repository import (
    DocumentRepository,
)
from services.presentation.presentation_service import (
    PresentationService,
)
from services.presentation.presentation_export_service import (
    PresentationExportService,
)


def render():
    """Render the Presentation Generator page."""

    st.title("📊 Presentation Generator")

    st.caption(
        "Turn research papers into structured, "
        "AI-generated presentations."
    )

    # Initialize services
    document_repository = DocumentRepository()
    presentation_service = PresentationService()
    presentation_export_service = (
        PresentationExportService()
    )

    # Load available documents
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

    # Presentation settings
    paper_col, type_col = st.columns(2)

    with paper_col:

        selected_document_id = st.selectbox(
            "Select a research paper",
            options=list(document_options.keys()),
            format_func=lambda document_id:
                document_options[document_id],
        )

    with type_col:

        presentation_type = st.selectbox(
            "Presentation type",
            options=[
                "Research Summary",
                "Academic Presentation",
                "Executive Summary",
                "Educational Presentation",
            ],
        )

    # Slide count
    slide_count = st.slider(
        "Number of slides",
        min_value=3,
        max_value=15,
        value=8,
    )

    st.divider()

    # Generate presentation
    if st.button(
        "✨ Generate Presentation",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Creating your presentation..."
            ):

                presentation_content = (
                    presentation_service.generate(
                        document_id=selected_document_id,
                        document_name=(
                            document_options[
                                selected_document_id
                            ]
                        ),
                        presentation_type=(
                            presentation_type
                        ),
                        slide_count=slide_count,
                    )
                )

        except (
            ValueError,
            FileNotFoundError,
        ) as error:

            st.error(str(error))

            return

        # Store generated presentation
        st.session_state.presentation_content = (
            presentation_content
        )

        st.session_state.presentation_document_id = (
            selected_document_id
        )

        st.session_state.presentation_type = (
            presentation_type
        )

        st.session_state.presentation_slide_count = (
            slide_count
        )

        st.rerun()

    # Load generated presentation
    presentation_content = st.session_state.get(
        "presentation_content"
    )

    presentation_document_id = st.session_state.get(
        "presentation_document_id"
    )

    stored_presentation_type = st.session_state.get(
        "presentation_type"
    )

    stored_slide_count = st.session_state.get(
        "presentation_slide_count"
    )

    # Prevent old presentation from appearing when
    # settings are changed
    if (
        presentation_content is None
        or presentation_document_id
        != selected_document_id
        or stored_presentation_type
        != presentation_type
        or stored_slide_count
        != slide_count
    ):
        return

    st.divider()

    # Presentation overview
    st.subheader(
        f"📊 {presentation_content.title}"
    )

    overview_col_1, overview_col_2 = st.columns(2)

    with overview_col_1:

        st.metric(
            "Slides",
            len(presentation_content.slides),
        )

    with overview_col_2:

        st.metric(
            "Presentation Type",
            presentation_type,
        )

    st.divider()

    # Slide preview
    st.subheader("🖥️ Slide Preview")

    for index, slide in enumerate(
        presentation_content.slides,
        start=1,
    ):

        with st.expander(
            f"Slide {index} — {slide.title}",
            expanded=index == 1,
        ):

            st.markdown(
                f"### {slide.title}"
            )

            for bullet in slide.content:

                st.markdown(
                    f"- {bullet}"
                )

            st.divider()

            st.markdown(
                "**🎤 Speaker Notes**"
            )

            st.write(
                slide.speaker_notes
            )

    st.divider()

    st.subheader("📥 Export Presentation")

    try:

        export_path = (
            presentation_export_service.export(
                presentation_content=
                presentation_content,
                document_name=(
                    document_options[
                        selected_document_id
                    ]
                ),
            )
        )

        with open(
            export_path,
            "rb",
        ) as file:

            st.download_button(
                label="⬇️ Download PowerPoint",
                data=file.read(),
                file_name=export_path.name,
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.presentationml."
                    "presentation"
                ),
                type="primary",
                use_container_width=True,
            )

    except ValueError as error:

        st.error(
            f"Unable to export presentation: {error}"
        )           