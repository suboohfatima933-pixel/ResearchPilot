from pathlib import Path
import json

import faiss
import numpy as np

from models.embedding import Embedding
from models.search_result import SearchResult


class VectorStoreService:
    """Manages document-scoped FAISS vector stores."""

    BASE_INDEX_DIR = Path("data/vector_stores")

    def __init__(self):
        self.BASE_INDEX_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.index = None
        self.metadata = []

    def _get_document_dir(self, document_id: str) -> Path:
        """Return the vector store directory for a document."""

        if not document_id:
            raise ValueError("Document ID is required.")

        document_dir = self.BASE_INDEX_DIR / document_id
        document_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return document_dir

    def create(
        self,
        embeddings: list[Embedding],
        document_id: str,
    ) -> None:
        """Create a FAISS index for a specific document."""

        if not embeddings:
            raise ValueError("No embeddings provided.")

        if not document_id:
            raise ValueError("Document ID is required.")

        dimensions = embeddings[0].dimensions

        self.index = faiss.IndexFlatIP(dimensions)

        vectors = np.array(
            [embedding.vector for embedding in embeddings],
            dtype="float32",
        )

        self.index.add(vectors)

        self.metadata = [
            {
                "chunk_id": embedding.chunk_id,
                "document_id": document_id,
                "document_name": embedding.document_name,
                "start_index": embedding.start_index,
                "end_index": embedding.end_index,
                "content": embedding.content,
            }
            for embedding in embeddings
        ]

    def save(self, document_id: str) -> None:
        """Save the FAISS index and metadata for a document."""

        if self.index is None:
            raise ValueError("No index has been created.")

        document_dir = self._get_document_dir(document_id)

        index_file = document_dir / "faiss.index"
        metadata_file = document_dir / "metadata.json"

        faiss.write_index(
            self.index,
            str(index_file),
        )

        with open(
            metadata_file,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.metadata,
                file,
                indent=4,
            )

    def load(self, document_id: str) -> None:
        """Load the FAISS index and metadata for a document."""

        document_dir = self._get_document_dir(document_id)

        index_file = document_dir / "faiss.index"
        metadata_file = document_dir / "metadata.json"

        if not index_file.exists():
            raise FileNotFoundError(
                f"Vector store not found for document: {document_id}"
            )

        if not metadata_file.exists():
            raise FileNotFoundError(
                f"Vector store metadata not found for document: {document_id}"
            )

        self.index = faiss.read_index(
            str(index_file)
        )

        with open(
            metadata_file,
            "r",
            encoding="utf-8",
        ) as file:
            self.metadata = json.load(file)

    def search(
        self,
        query_embedding: list[float],
        document_id: str,
        top_k: int = 5,
        min_score: float = 0.60,
    ) -> list[SearchResult]:
        """Search a specific document's vector store."""

        if self.index is None:
            raise ValueError("Vector store has not been loaded.")

        if not document_id:
            raise ValueError("Document ID is required.")

        query_vector = np.array(
            [query_embedding],
            dtype="float32",
        )

        scores, indices = self.index.search(
            query_vector,
            top_k,
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            if float(score) < min_score:
                continue

            metadata = self.metadata[index]

            results.append(
                SearchResult(
                    chunk_id=metadata["chunk_id"],
                    document_name=metadata["document_name"],
                    similarity_score=float(score),
                    start_index=metadata["start_index"],
                    end_index=metadata["end_index"],
                    content=metadata["content"],
                )
            )

        return results

    @property
    def total_vectors(self) -> int:
        """Return the total number of indexed vectors."""

        if self.index is None:
            return 0

        return self.index.ntotal