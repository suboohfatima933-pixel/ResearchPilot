import fitz  # PyMuPDF
from pathlib import Path

from models.document import Document


class ParserService:
    """Handles PDF parsing and text extraction."""

    def parse(self, pdf_path: str | Path) -> Document:
        """Parse a PDF and return a Document object."""

        pdf_path = Path(pdf_path)

        pdf = fitz.open(pdf_path)

        text = ""

        for page in pdf:
            text += page.get_text()

        metadata = pdf.metadata or {}

        document = Document(
            filename=pdf_path.name,
            filepath=pdf_path,
            page_count=len(pdf),
            text=text,
            metadata=metadata,
        )

        pdf.close()

        return document