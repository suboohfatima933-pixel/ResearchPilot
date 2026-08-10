from services.llm.llm_service import LLMService
from services.rag.embedding_service import EmbeddingService
from services.rag.vector_store_service import VectorStoreService


class RAGService:
    """Orchestrates retrieval and LLM generation."""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.llm_service = LLMService()

    def answer(self, query: str) -> dict:
        """Generate a grounded answer using retrieved document context."""

        if not query.strip():
            raise ValueError("Query cannot be empty.")

        # Generate query embedding
        query_embedding = self.embedding_service.embed_query(query)

        # Retrieve relevant chunks
        self.vector_store_service.load()

        results = self.vector_store_service.search(
            query_embedding,
            top_k=5,
            min_score=0.60,
        )

        if not results:
            return {
                "answer": (
                    "I couldn't find relevant information "
                    "in the uploaded document."
                ),
                "sources": [],
            }

        # Build context from retrieved chunks
        context = "\n\n".join(
            f"[Chunk {result.chunk_id}]\n{result.content}"
            for result in results
        )

        prompt = f"""
You are a research assistant answering questions about a research paper.

Answer the user's question using ONLY the provided document context.

If the answer cannot be found in the context, say that the information
is not available in the document.

Do not use outside knowledge.
Do not invent facts.

Document Context:
{context}

User Question:
{query}

Answer:
""".strip()

        answer = self.llm_service.generate(prompt)

        return {
            "answer": answer,
            "sources": results,
        }