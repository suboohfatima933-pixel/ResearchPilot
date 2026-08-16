import streamlit as st
from pathlib import Path

from services.chat.chat_service import ChatService


def render():
    """Render the Chat with Paper page."""

    st.title("💬 Chat with Paper")
    st.caption(
        "Ask questions about your uploaded research papers."
    )

    # ---------------------------------------------------------
    # Find available documents
    # ---------------------------------------------------------

    upload_dir = Path("data/uploads")

    document_options = {}

    if upload_dir.exists():

        for directory in upload_dir.iterdir():

            if not directory.is_dir():
                continue

            pdf_files = list(directory.glob("*.pdf"))

            if pdf_files:
                document_options[directory.name] = pdf_files[0].name

    # ---------------------------------------------------------
    # Initialize Chat Service
    # ---------------------------------------------------------

    chat_service = ChatService()

    # ---------------------------------------------------------
    # Load persisted chats
    # ---------------------------------------------------------

    chats = chat_service.get_all_chats()

    # ---------------------------------------------------------
    # Active Chat State
    # ---------------------------------------------------------

    if "active_chat_id" not in st.session_state:
        st.session_state.active_chat_id = None

    if "show_new_chat" not in st.session_state:
        st.session_state.show_new_chat = False

    # ---------------------------------------------------------
    # Main Chat Workspace
    # ---------------------------------------------------------

    history_col, chat_col = st.columns(
        [0.28, 0.72],
        gap="large",
    )

    # =========================================================
    # Chat History Panel
    # =========================================================

    with history_col:

        st.subheader("💬 Chats")

        if st.button(
            "＋ New Chat",
            use_container_width=True,
        ):
            st.session_state.show_new_chat = True
            st.session_state.active_chat_id = None
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

            if st.button(
                button_label,
                key=f"chat_{chat.id}",
                use_container_width=True,
            ):

                st.session_state.active_chat_id = chat.id
                st.session_state.show_new_chat = False

                st.rerun()

    # =========================================================
    # Current Chat
    # =========================================================

    with chat_col:

        # -----------------------------------------------------
        # New Chat
        # -----------------------------------------------------

        if st.session_state.show_new_chat:

            st.subheader("＋ New Chat")

            if not document_options:

                st.info(
                    "📄 No research papers are available yet. "
                    "Upload a paper in Paper Analysis first."
                )

                return

            selected_document_id = st.selectbox(
                "Select a research paper",
                options=list(
                    document_options.keys()
                ),
                format_func=lambda document_id:
                    document_options[document_id],
            )

            if st.button(
                "Create Chat",
                type="primary",
                use_container_width=True,
            ):

                document_name = document_options[
                    selected_document_id
                ]

                title = Path(
                    document_name
                ).stem

                chat = chat_service.create_chat(
                    document_id=selected_document_id,
                    title=title,
                )

                st.session_state.active_chat_id = chat.id
                st.session_state.show_new_chat = False

                st.rerun()

            return

        # -----------------------------------------------------
        # No Active Chat
        # -----------------------------------------------------

        if not st.session_state.active_chat_id:

            st.info(
                "Create a new chat to start "
                "asking questions about a paper."
            )

            return

        # -----------------------------------------------------
        # Load Active Chat
        # -----------------------------------------------------

        session = chat_service.get_chat(
            st.session_state.active_chat_id
        )

        if session is None:

            st.session_state.active_chat_id = None

            st.warning(
                "The selected chat could not be found."
            )

            return

        # -----------------------------------------------------
        # Document
        # -----------------------------------------------------

        document_name = document_options.get(
            session.document_id,
            "Research Paper",
        )

        st.subheader(
            f"💬 {session.title}"
        )

        st.caption(
            f"📄 {document_name}"
        )

        st.divider()

        # -----------------------------------------------------
        # Display Messages
        # -----------------------------------------------------

        for message in session.messages:

            with st.chat_message(
                message.role
            ):

                st.markdown(
                    message.content
                )

        # -----------------------------------------------------
        # Chat Input
        # -----------------------------------------------------

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