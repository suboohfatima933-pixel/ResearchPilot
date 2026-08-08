from pydantic import BaseModel


class Embedding(BaseModel):
    """Domain model representing a vector embedding."""

    chunk_id: int

    document_name: str

    start_index: int

    end_index: int

    model_name: str

    dimensions: int

    vector: list[float]