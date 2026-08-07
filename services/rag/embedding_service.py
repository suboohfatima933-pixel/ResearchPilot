from sentence_transformers import SentenceTransformer

from models.chunk import Chunk
from models.embedding import Embedding


class EmbeddingService:
    """Generates embeddings for document chunks."""

    MODEL_NAME = "BAAI/bge-small-en-v1.5"

    def __init__(self):
        self.model = SentenceTransformer(self.MODEL_NAME)

    def embed(self, chunks: list[Chunk]) -> list[Embedding]:
        """Generate embeddings for a list of chunks."""

        if not chunks:
            return []

        texts = [chunk.content for chunk in chunks]

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        embeddings = []

        for chunk, vector in zip(chunks, vectors):

            embeddings.append(
                Embedding(
                    chunk_id=chunk.chunk_id,
                    document_name=chunk.document_name,
                    model_name=self.MODEL_NAME,
                    dimensions=len(vector),
                    vector=vector.tolist(),
                )
            )

        return embeddings