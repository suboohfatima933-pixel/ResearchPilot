from models.chat_message import ChatMessage
from models.chat_session import ChatSession

from services.database.chat_repository import ChatRepository
from services.llm.llm_service import LLMService
from services.rag.rag_service import RAGService


class ChatService:
    """Manages conversational interactions with a research paper."""

    def __init__(self):
        self.rag_service = RAGService()
        self.llm_service = LLMService()
        self.chat_repository = ChatRepository()

    def create_chat(
        self,
        document_id: str,
        title: str = "New Chat",
    ) -> ChatSession:
        """Create and persist a new chat session."""

        if not document_id:
            raise ValueError("Document ID is required.")

        chat = ChatSession(
            title=title,
            document_id=document_id,
        )

        self.chat_repository.create_chat(chat)

        return chat

    def get_chat(
        self,
        chat_id: str,
    ) -> ChatSession | None:
        """Retrieve a chat from persistent storage."""

        return self.chat_repository.get_chat(
            chat_id
        )

    def get_all_chats(self) -> list[ChatSession]:
        """Retrieve all persisted chats."""

        return self.chat_repository.get_all_chats()

    def send_message(
        self,
        message: str,
        document_id: str,
        history: list[ChatMessage],
        chat_id: str,
    ) -> dict:
        """Send a message and generate a document-grounded response."""

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        if not document_id:
            raise ValueError("Document ID is required.")

        if not chat_id:
            raise ValueError("Chat ID is required.")

        # Convert recent conversation into text
        conversation = "\n".join(
            f"{item.role}: {item.content}"
            for item in history[-6:]
        )

        # Rewrite the current question using conversation context
        contextualized_query = self._contextualize_query(
            message,
            conversation,
        )

        # Generate document-grounded answer
        result = self.rag_service.answer(
            contextualized_query,
            document_id,
        )

        user_message = ChatMessage(
            role="user",
            content=message,
        )

        assistant_message = ChatMessage(
            role="assistant",
            content=result["answer"],
        )

        # Persist both messages
        self.chat_repository.add_message(
            chat_id,
            user_message,
        )

        self.chat_repository.add_message(
            chat_id,
            assistant_message,
        )

        return {
            "message": assistant_message,
            "sources": result["sources"],
        }

    def update_title(
        self,
        chat_id: str,
        title: str,
    ) -> None:
        """Update a chat title."""

        self.chat_repository.update_title(
            chat_id,
            title,
        )

    def delete_chat(
        self,
        chat_id: str,
    ) -> None:
        """Delete a chat and its messages."""

        self.chat_repository.delete_chat(
            chat_id
        )

    def _contextualize_query(
        self,
        message: str,
        conversation: str,
    ) -> str:
        """Rewrite a follow-up question into a standalone query."""

        if not conversation.strip():
            return message

        prompt = f"""
You are helping a research assistant understand a user's question.

Rewrite the user's latest question so that it can be understood
independently without the conversation history.

Resolve references such as:
- it
- its
- they
- them
- this
- that
- these
- those

Preserve the user's original intent.

Do not answer the question.
Only return the rewritten standalone question.

Conversation:
{conversation}

Latest User Question:
{message}

Standalone Question:
""".strip()

        return self.llm_service.generate(
            prompt
        ).strip()