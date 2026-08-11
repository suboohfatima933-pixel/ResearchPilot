from models.chat_message import ChatMessage
from services.llm.llm_service import LLMService
from services.rag.rag_service import RAGService


class ChatService:
    """Manages conversational interactions with a research paper."""

    def __init__(self):
        self.rag_service = RAGService()
        self.llm_service = LLMService()

    def send_message(
        self,
        message: str,
        document_id: str,
        history: list[ChatMessage],
    ) -> dict:
        """Send a message and generate a document-grounded response."""

        if not message.strip():
            raise ValueError("Message cannot be empty.")

        if not document_id:
            raise ValueError("Document ID is required.")

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

        # Retrieve and answer using the contextualized query
        result = self.rag_service.answer(
            contextualized_query,
            document_id,
        )

        return {
            "message": ChatMessage(
                role="assistant",
                content=result["answer"],
            ),
            "sources": result["sources"],
        }

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

        return self.llm_service.generate(prompt).strip()