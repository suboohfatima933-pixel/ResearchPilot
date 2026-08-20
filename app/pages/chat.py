import streamlit as st
from pathlib import Path

from services.chat.chat_service import ChatService
from services.database.document_repository import DocumentRepository
from services.pdf.document_service import DocumentService


def render():
    """Render the Chat with Paper page."""

    st.title("💬 Chat with Paper")
    st.caption(
        "Ask questions about your uploaded research papers."
    )

    # Initialize services
    chat_service = ChatService()
    document_repository = DocumentRepository()
    document_service = DocumentService()

    # Load persisted documents
    documents = document_repository.get_all()

    document_options = {
        document.document_id: document.original_filename
        for document in documents
    }

    # Load persisted chats
    chats = chat_service.get_all_chats()

    # Active chat state
    if "active_chat_id" not in st.session_state:
        st.session_state.active_chat_id = None

    if "show_new_chat" not in st.session_state:
        st.session_state.show_new_chat = False

    if "show_rename_chat" not in st.session_state:
        st.session_state.show_rename_chat = False

    # Main chat workspace
    history_col, chat_col = st.columns(
        [0.28, 0.72],
        gap="large",
    )

    # Chat history
    with history_col:

        st.subheader("💬 Chats")

        if st.button(
            "＋ New Chat",
            use_container_width=True,
        ):
            st.session_state.show_new_chat = True
            st.session_state.active_chat_id = None
            st.session_state.show_rename_chat = False
            st.rerun()

        st.divider()

        if not chats:
            st.caption(
                "No conversations yet."
            )

        for chat in chats:

            is_active = (
                chat.id
                == st.session_state.active_chat_id
            )

            button_label = (
                f"● {chat.title}"
                if is_active
                else chat.title
            )

            chat_button_col, delete_button_col = st.columns(
                [0.85, 0.15]
            )

            with chat_button_col:

                if st.button(
                    button_label,
                    key=f"chat_{chat.id}",
                    use_container_width=True,
                ):
                    st.session_state.active_chat_id = chat.id
                    st.session_state.show_new_chat = False
                    st.session_state.show_rename_chat = False

                    st.rerun()

            with delete_button_col:

                if st.button(
                    "🗑️",
                    key=f"delete_chat_{chat.id}",
                    help="Delete chat",
                    use_container_width=True,
                ):
                    chat_service.delete_chat(
                        chat.id
                    )

                    if (
                        st.session_state.active_chat_id
                        == chat.id
                    ):
                        st.session_state.active_chat_id = None

                    st.session_state.show_rename_chat = False

                    st.rerun()

    # Current chat
    with chat_col:

        # New chat
        if st.session_state.show_new_chat:

            st.subheader("＋ New Chat")

            chat_source = st.radio(
                "How would you like to start?",
                [
                    "Choose Existing Paper",
                    "Upload New Paper",
                ],
                horizontal=True,
            )

            selected_document_id = None
            selected_document_name = None

            # Choose existing paper
            if chat_source == "Choose Existing Paper":

                if not document_options:

                    st.info(
                        "No existing research papers found. "
                        "Upload a new paper instead."
                    )

                else:

                    selected_document_id = st.selectbox(
                        "Select a research paper",
                        options=list(
                            document_options.keys()
                        ),
                        format_func=lambda document_id:
                            document_options[document_id],
                    )

                    selected_document_name = document_options[
                        selected_document_id
                    ]

            # Upload new paper
            else:

                uploaded_file = st.file_uploader(
                    "Upload a research paper",
                    type=["pdf"],
                    accept_multiple_files=False,
                )

                if uploaded_file:

                    selected_document_name = uploaded_file.name

            if st.button(
                "Create Chat",
                type="primary",
                use_container_width=True,
            ):

                if (
                    chat_source == "Choose Existing Paper"
                    and not selected_document_id
                ):

                    st.warning(
                        "Please select a research paper."
                    )

                    return

                if chat_source == "Upload New Paper":

                    if uploaded_file is None:

                        st.warning(
                            "Please upload a PDF research paper."
                        )

                        return

                    with st.spinner(
                        "Uploading and processing paper..."
                    ):

                        document = document_service.process_upload(
                            uploaded_file
                        )

                    selected_document_id = document.document_id
                    selected_document_name = (
                        document.original_filename
                    )

                title = Path(
                    selected_document_name
                ).stem

                chat = chat_service.create_chat(
                    document_id=selected_document_id,
                    title=title,
                )

                st.session_state.active_chat_id = chat.id
                st.session_state.show_new_chat = False
                st.session_state.show_rename_chat = False

                st.rerun()

            return

        # No active chat
        if not st.session_state.active_chat_id:

            st.info(
                "Create a new chat to start "
                "asking questions about a paper."
            )

            return

        # Load active chat
        session = chat_service.get_chat(
            st.session_state.active_chat_id
        )

        if session is None:

            st.session_state.active_chat_id = None
            st.session_state.show_rename_chat = False

            st.warning(
                "The selected chat could not be found."
            )

            return

        # Document
        document_name = document_options.get(
            session.document_id,
            "Research Paper",
        )

        # Chat header
        title_col, rename_col = st.columns(
            [0.9, 0.1]
        )

        with title_col:
            st.subheader(
                f"💬 {session.title}"
            )

        with rename_col:
            if st.button(
                "✏️",
                key=f"rename_chat_{session.id}",
                help="Rename chat",
            ):
                st.session_state.show_rename_chat = True
                st.rerun()

        st.caption(
            f"📄 {document_name}"
        )

        # Display rename form
        if st.session_state.show_rename_chat:

            with st.form(
                f"rename_form_{session.id}"
            ):

                new_title = st.text_input(
                    "Chat title",
                    value=session.title,
                    max_chars=100,
                )

                rename_col, cancel_col = st.columns(2)

                with rename_col:
                    rename_clicked = st.form_submit_button(
                        "Save",
                        type="primary",
                        use_container_width=True,
                    )

                with cancel_col:
                    cancel_clicked = st.form_submit_button(
                        "Cancel",
                        use_container_width=True,
                    )

            if rename_clicked:

                cleaned_title = new_title.strip()

                if not cleaned_title:

                    st.warning(
                        "Chat title cannot be empty."
                    )

                else:

                    chat_service.update_title(
                        session.id,
                        cleaned_title,
                    )

                    st.session_state.show_rename_chat = False

                    st.rerun()

            if cancel_clicked:

                st.session_state.show_rename_chat = False

                st.rerun()

        st.divider()

        # Display messages
        for message in session.messages:

            with st.chat_message(
                message.role
            ):
                st.markdown(
                    message.content
                )

        # Chat input
        prompt = st.chat_input(
            "Ask a question about this paper..."
        )

        if prompt:

            history = session.messages.copy()

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):

                with st.spinner(
                    "ResearchPilot is thinking..."
                ):

                    result = chat_service.send_message(
                        message=prompt,
                        document_id=session.document_id,
                        history=history,
                        chat_id=session.id,
                    )

                assistant_message = result[
                    "message"
                ]

                st.markdown(
                    assistant_message.content
                )

                sources = result["sources"]

                if sources:

                    with st.expander(
                        "📚 Sources"
                    ):

                        for source in sources:

                            st.markdown(
                                f"**Chunk "
                                f"{source.chunk_id}** "
                                f"— "
                                f"{source.similarity_score * 100:.1f}% match"
                            )

                            st.caption(
                                source.document_name
                            )

                            st.text(
                                source.content
                            )

            st.rerun()