from pydantic import BaseModel


class Embedding(BaseModel):
    """Domain model representing a vector embedding."""

    chunk_id: int

    document_name: str

    model_name: str

    dimensions: int

    vector: list[float]