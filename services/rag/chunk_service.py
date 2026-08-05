from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.chunk import Chunk
from models.document import Document


class ChunkService:
    """Handles document chunking for the RAG pipeline."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def split(self, document: Document) -> list[Chunk]:
        """Split a document into chunks."""

        texts = self.text_splitter.split_text(document.text)

        chunks = []

        current_position = 0

        for index, text in enumerate(texts):

            start = document.text.find(text, current_position)

            if start == -1:
                start = current_position

            end = start + len(text)

            chunks.append(
                Chunk(
                    chunk_id=index + 1,
                    document_name=document.filename,
                    source_path=document.filepath,
                    content=text,
                    start_index=start,
                    end_index=end,
                )
            )

            current_position = end

        return chunks