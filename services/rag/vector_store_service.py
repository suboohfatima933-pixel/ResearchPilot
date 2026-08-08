from pathlib import Path
import json

import faiss
import numpy as np

from models.embedding import Embedding

from models.search_result import SearchResult


class VectorStoreService:
    """Manages the FAISS vector store."""

    INDEX_DIR = Path("data/vector_store")
    INDEX_FILE = INDEX_DIR / "faiss.index"
    METADATA_FILE = INDEX_DIR / "metadata.json"

    def __init__(self):
        self.INDEX_DIR.mkdir(parents=True, exist_ok=True)
        self.index = None

    def create(self, embeddings: list[Embedding]) -> None:
        """Create a FAISS index from embeddings."""

        if not embeddings:
            raise ValueError("No embeddings provided.")

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
                "document_name": embedding.document_name,
                "start_index": embedding.start_index,
                "end_index": embedding.end_index,
                "content": embedding.content,
            }
            for embedding in embeddings
        ]
       
    def save(self) -> None:
        """Save the FAISS index and metadata."""

        if self.index is None:
            raise ValueError("No index has been created.")

        faiss.write_index(
            self.index,
            str(self.INDEX_FILE),
        )

        with open(self.METADATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                self.metadata,
                file,
                indent=4,
            )    

    def load(self) -> None:
        """Load the FAISS index and metadata."""

        if not self.INDEX_FILE.exists():
            raise FileNotFoundError("Vector store not found.")

        self.index = faiss.read_index(
            str(self.INDEX_FILE)
        )

        with open(self.METADATA_FILE, "r", encoding="utf-8") as file:
            self.metadata = json.load(file)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        min_score: float = 0.60,
    ) -> list[SearchResult]:
        """Search the vector store for similar embeddings."""

        if self.index is None:
            raise ValueError("Vector store has not been loaded.")

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