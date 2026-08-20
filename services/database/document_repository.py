import json
from datetime import datetime

from models.document import Document

from services.database.database_service import DatabaseService


class DocumentRepository:
    """Handles persistent research document storage."""

    def __init__(self):
        self.database = DatabaseService()

    def create(
        self,
        document: Document,
    ) -> Document:
        """Persist a new document."""

        with self.database._get_connection() as connection:

            connection.execute(
                """
                INSERT INTO documents (
                    document_id,
                    filename,
                    original_filename,
                    filepath,
                    file_size,
                    page_count,
                    metadata,
                    uploaded_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document.document_id,
                    document.filename,
                    document.original_filename,
                    str(document.filepath),
                    document.file_size,
                    document.page_count,
                    json.dumps(document.metadata),
                    document.uploaded_at.isoformat(),
                ),
            )

            connection.commit()

        return document

    def get(
        self,
        document_id: str,
    ) -> Document | None:
        """Retrieve a document by its ID."""

        with self.database._get_connection() as connection:

            row = connection.execute(
                """
                SELECT
                    document_id,
                    filename,
                    original_filename,
                    filepath,
                    file_size,
                    page_count,
                    metadata,
                    uploaded_at
                FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_document(row)

    def get_all(self) -> list[Document]:
        """Retrieve all documents ordered by upload date."""

        with self.database._get_connection() as connection:

            rows = connection.execute(
                """
                SELECT
                    document_id,
                    filename,
                    original_filename,
                    filepath,
                    file_size,
                    page_count,
                    metadata,
                    uploaded_at
                FROM documents
                ORDER BY uploaded_at DESC
                """
            ).fetchall()

        return [
            self._row_to_document(row)
            for row in rows
        ]

    def delete(
        self,
        document_id: str,
    ) -> None:
        """Delete a document record."""

        with self.database._get_connection() as connection:

            connection.execute(
                """
                DELETE FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            )

            connection.commit()

    @staticmethod
    def _row_to_document(
        row,
    ) -> Document:
        """Convert a database row into a Document model."""

        return Document(
            document_id=row["document_id"],
            filename=row["filename"],
            original_filename=row["original_filename"],
            filepath=row["filepath"],
            file_size=row["file_size"],
            page_count=row["page_count"],
            metadata=json.loads(row["metadata"]),
            uploaded_at=datetime.fromisoformat(
                row["uploaded_at"]
            ),
        )