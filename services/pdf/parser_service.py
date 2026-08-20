import fitz  # PyMuPDF
from pathlib import Path

from models.document import Document


class ParserService:
    """Handles PDF parsing and text extraction."""

    def parse(
        self,
        pdf_path: str | Path,
        document_id: str,
        original_filename: str,
        file_size: int,
    ) -> Document:
        """Parse a PDF and return a Document object."""

        if not document_id:
            raise ValueError("Document ID is required.")

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        pdf = fitz.open(pdf_path)

        try:
            text = ""

            for page in pdf:
                text += page.get_text()

            metadata = pdf.metadata or {}

            document = Document(
                document_id=document_id,
                filename=pdf_path.name,
                original_filename=original_filename,
                filepath=pdf_path,
                file_size=file_size,
                page_count=len(pdf),
                text=text,
                metadata=metadata,
            )

            return document

        finally:
            pdf.close()