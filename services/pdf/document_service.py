from models.document import Document

from services.database.document_repository import DocumentRepository
from services.pdf.parser_service import ParserService
from services.pdf.upload_service import UploadService
from services.rag.chunk_service import ChunkService
from services.rag.embedding_service import EmbeddingService
from services.rag.vector_store_service import VectorStoreService


class DocumentService:
    """Orchestrates document upload, processing, and persistence."""

    def __init__(self):
        self.upload_service = UploadService()
        self.parser_service = ParserService()
        self.chunk_service = ChunkService()
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.document_repository = DocumentRepository()

    def process_upload(
        self,
        uploaded_file,
    ) -> Document:
        """Upload, process, and persist a research document."""

        # Save uploaded PDF
        file_info = self.upload_service.save(
            uploaded_file
        )

        # Parse PDF
        document = self.parser_service.parse(
            pdf_path=file_info["filepath"],
            document_id=file_info["document_id"],
            original_filename=file_info[
                "original_filename"
            ],
            file_size=file_info["size"],
        )

        # Create chunks
        chunks = self.chunk_service.split(
            document
        )

        # Create embeddings
        embeddings = self.embedding_service.embed(
            chunks
        )

        # Create and save vector store
        self.vector_store_service.create(
            embeddings,
            file_info["document_id"],
        )

        self.vector_store_service.save(
            file_info["document_id"]
        )

        # Persist document
        self.document_repository.create(
            document
        )

        return document

   
    def get(
        self,
        document_id: str,
    ) -> Document | None:
        """Retrieve a persisted document."""

        return self.document_repository.get(
            document_id
        )

    def get_all(self) -> list[Document]:
        """Retrieve all persisted documents."""

        return self.document_repository.get_all()

    def delete(
        self,
        document_id: str,
    ) -> None:
        """Delete a document record."""

        self.document_repository.delete(
            document_id
        )