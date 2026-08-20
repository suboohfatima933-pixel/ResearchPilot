from datetime import datetime, timezone

from models.chat_message import ChatMessage
from models.chat_session import ChatSession

from services.database.database_service import DatabaseService


class ChatRepository:
    """Handles persistent chat and message storage."""

    def __init__(self):
        self.database = DatabaseService()

    def create_chat(
        self,
        chat: ChatSession,
    ) -> ChatSession:
        """Persist a new chat session."""

        with self.database._get_connection() as connection:

            connection.execute(
                """
                INSERT INTO chats (
                    id,
                    title,
                    document_id,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    chat.id,
                    chat.title,
                    chat.document_id,
                    chat.created_at.isoformat(),
                    chat.updated_at.isoformat(),
                ),
            )

            connection.commit()

        return chat



    def get_chat(
        self,
        chat_id: str,
    ) -> ChatSession | None:
        """Retrieve a chat session by ID."""

        with self.database._get_connection() as connection:

            row = connection.execute(
                """
                SELECT
                    id,
                    title,
                    document_id,
                    created_at,
                    updated_at
                FROM chats
                WHERE id = ?
                """,
                (chat_id,),
            ).fetchone()

        if row is None:
            return None

        messages = self.get_messages(chat_id)

        return ChatSession(
            id=row["id"],
            title=row["title"],
            document_id=row["document_id"],
            messages=messages,
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                row["updated_at"]
            ),
        )

    def get_by_document_id(
        self,
        document_id: str,
    ) -> ChatSession | None:
        """Retrieve the most recent chat for a document."""

        with self.database._get_connection() as connection:

            row = connection.execute(
                """
                SELECT
                    id,
                    title,
                    document_id,
                    created_at,
                    updated_at
                FROM chats
                WHERE document_id = ?
                ORDER BY updated_at DESC
                LIMIT 1
                """,
                (document_id,),
            ).fetchone()

        if row is None:
            return None

        messages = self.get_messages(
            row["id"]
        )

        return ChatSession(
            id=row["id"],
            title=row["title"],
            document_id=row["document_id"],
            messages=messages,
            created_at=datetime.fromisoformat(
                row["created_at"]
            ),
            updated_at=datetime.fromisoformat(
                row["updated_at"]
            ),
        )


    def get_all_chats(self) -> list[ChatSession]:
        """Retrieve all chat sessions ordered by recent activity."""

        with self.database._get_connection() as connection:

            rows = connection.execute(
                """
                SELECT
                    id,
                    title,
                    document_id,
                    created_at,
                    updated_at
                FROM chats
                ORDER BY updated_at DESC
                """
            ).fetchall()

        chats = []

        for row in rows:

            messages = self.get_messages(
                row["id"]
            )

            chats.append(
                ChatSession(
                    id=row["id"],
                    title=row["title"],
                    document_id=row["document_id"],
                    messages=messages,
                    created_at=datetime.fromisoformat(
                        row["created_at"]
                    ),
                    updated_at=datetime.fromisoformat(
                        row["updated_at"]
                    ),
                )
            )

        return chats

    def add_message(
        self,
        chat_id: str,
        message: ChatMessage,
    ) -> None:
        """Persist a message and update the chat timestamp."""

        created_at = datetime.now(
            timezone.utc
        )

        with self.database._get_connection() as connection:

            connection.execute(
                """
                INSERT INTO chat_messages (
                    chat_id,
                    role,
                    content,
                    created_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    chat_id,
                    message.role,
                    message.content,
                    created_at.isoformat(),
                ),
            )

            connection.execute(
                """
                UPDATE chats
                SET updated_at = ?
                WHERE id = ?
                """,
                (
                    created_at.isoformat(),
                    chat_id,
                ),
            )

            connection.commit()

    def get_messages(
        self,
        chat_id: str,
    ) -> list[ChatMessage]:
        """Retrieve all messages for a chat."""

        with self.database._get_connection() as connection:

            rows = connection.execute(
                """
                SELECT
                    role,
                    content
                FROM chat_messages
                WHERE chat_id = ?
                ORDER BY id ASC
                """,
                (chat_id,),
            ).fetchall()

        return [
            ChatMessage(
                role=row["role"],
                content=row["content"],
            )
            for row in rows
        ]

    def update_title(
        self,
        chat_id: str,
        title: str,
    ) -> None:
        """Update a chat title."""

        with self.database._get_connection() as connection:

            connection.execute(
                """
                UPDATE chats
                SET
                    title = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    title,
                    datetime.now(
                        timezone.utc
                    ).isoformat(),
                    chat_id,
                ),
            )

            connection.commit()

    def delete_chat(
        self,
        chat_id: str,
    ) -> None:
        """Delete a chat and its messages."""

        # Delete chat
        with self.database._get_connection() as connection:

            connection.execute(
                """
                DELETE FROM chats
                WHERE id = ?
                """,
                (chat_id,),
            )

            connection.commit()   