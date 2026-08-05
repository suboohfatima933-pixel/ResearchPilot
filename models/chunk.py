from pathlib import Path

from pydantic import BaseModel


class Chunk(BaseModel):
    """Domain model representing a chunk of a document."""

    chunk_id: int

    document_name: str

    source_path: Path

    content: str

    start_index: int

    end_index: int