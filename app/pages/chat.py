import streamlit as st
from pathlib import Path

from models.chat_message import ChatMessage
from models.chat_session import ChatSession
from services.chat.chat_service import ChatService


def render():
    """Render the Chat with Paper page."""

    st.title("💬 Chat with Paper")
    st.caption("Ask questions about your uploaded research papers.")

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
    # Initialize chat sessions
    # ---------------------------------------------------------

    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}

    if "active_chat_id" not in st.session_state:
        st.session_state.active_chat_id = None

    # ---------------------------------------------------------
    # No documents
    # ---------------------------------------------------------

    if not document_options:

        st.info(
            "📄 No research papers are available yet. "
            "Upload a paper in Paper Analysis first."
        )

        return

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

        st.divider()

        sessions = list(
            st.session_state.chat_sessions.values()
        )

        sessions.sort(
            key=lambda session: session.updated_at,
            reverse=True,
        )

        if not sessions:

            st.caption(
                "No conversations yet."
            )

        for session in sessions:

            is_active = (
                session.id
                == st.session_state.active_chat_id
            )

            button_label = (
                f"● {session.title}"
                if is_active
                else session.title
            )

            if st.button(
                button_label,
                key=f"chat_{session.id}",
                use_container_width=True,
            ):

                st.session_state.active_chat_id = (
                    session.id
                )

                st.session_state.show_new_chat = False

                st.rerun()

    # =========================================================
    # Current Chat
    # =========================================================

    with chat_col:

        # -----------------------------------------------------
        # New Chat
        # -----------------------------------------------------

        if st.session_state.get(
            "show_new_chat",
            False,
        ):

            st.subheader("＋ New Chat")

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

                session = ChatSession(
                    title=title,
                    document_id=selected_document_id,
                )

                st.session_state.chat_sessions[
                    session.id
                ] = session

                st.session_state.active_chat_id = (
                    session.id
                )

                st.session_state.show_new_chat = False

                st.rerun()

            return

        # -----------------------------------------------------
        # No Active Chat
        # -----------------------------------------------------

        active_chat_id = (
            st.session_state.active_chat_id
        )

        if not active_chat_id:

            st.info(
                "Create a new chat to start "
                "asking questions about a paper."
            )

            return

        # -----------------------------------------------------
        # Load Active Chat
        # -----------------------------------------------------

        session = st.session_state.chat_sessions.get(
            active_chat_id
        )

        if session is None:

            st.session_state.active_chat_id = None

            st.info(
                "The selected chat could not be found."
            )

            return

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

            user_message = ChatMessage(
                role="user",
                content=prompt,
            )

            session.messages.append(
                user_message
            )

            with st.chat_message("user"):

                st.markdown(prompt)

            chat_service = ChatService()

            with st.chat_message("assistant"):

                with st.spinner(
                    "ResearchPilot is thinking..."
                ):

                    result = chat_service.send_message(
                        message=prompt,
                        document_id=session.document_id,
                        history=session.messages,
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

            session.messages.append(
                assistant_message
            )

            # Update chat timestamp
            from datetime import datetime, timezone

            session.updated_at = (
                datetime.now(timezone.utc)
            )

            # Generate a better title after the first question
            if len(session.messages) == 2:
                session.title = prompt[:40]

            st.rerun()