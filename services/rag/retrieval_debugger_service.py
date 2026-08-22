from services.rag.embedding_service import (
    EmbeddingService,
)
from services.rag.vector_store_service import (
    VectorStoreService,
)


class RetrievalDebuggerService:
    """Provides debugging information for document retrieval."""

    def __init__(self):
        self.embedding_service = (
            EmbeddingService()
        )

        self.vector_store_service = (
            VectorStoreService()
        )

    def debug(
        self,
        query: str,
        document_id: str,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> dict:
        """Run and inspect a document retrieval operation."""

        if not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        if not document_id:
            raise ValueError(
                "Document ID is required."
            )

        # Generate query embedding
        query_embedding = (
            self.embedding_service.embed_query(
                query
            )
        )

        # Load document vector store
        self.vector_store_service.load(
            document_id
        )

        # Retrieve results
        results = (
            self.vector_store_service.search(
                query_embedding=query_embedding,
                document_id=document_id,
                top_k=top_k,
                min_score=min_score,
            )
        )

        return {
            "query": query,
            "document_id": document_id,
            "query_dimensions": len(
                query_embedding
            ),
            "total_vectors": (
                self.vector_store_service.total_vectors
            ),
            "top_k": top_k,
            "min_score": min_score,
            "results": results,
        }