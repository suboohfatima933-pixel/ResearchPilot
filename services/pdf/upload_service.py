from pathlib import Path
from datetime import datetime
import re
import shutil
import uuid


class UploadService:
    """Handles PDF upload and storage."""

    UPLOAD_DIR = Path("data/uploads")
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

    def __init__(self):
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def save(self, uploaded_file):
        """Validate and save an uploaded PDF."""

        if uploaded_file is None:
            raise ValueError("No file uploaded.")

        if not uploaded_file.name.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported.")

        if uploaded_file.size > self.MAX_FILE_SIZE:
            raise ValueError("Maximum file size is 25 MB.")

        # Generate a unique document ID
        document_id = str(uuid.uuid4())

        # Create a dedicated directory for this document
        document_dir = self.UPLOAD_DIR / document_id
        document_dir.mkdir(parents=True, exist_ok=True)

        # Generate a unique, human-readable filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        sanitized_filename = re.sub(
            r"[^a-zA-Z0-9._-]",
            "_",
            uploaded_file.name,
        )

        unique_filename = f"{timestamp}_{sanitized_filename}"

        destination = document_dir / unique_filename

        with open(destination, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)

        return {
            "document_id": document_id,
            "filename": unique_filename,
            "original_filename": uploaded_file.name,
            "filepath": str(destination),
            "size": uploaded_file.size,
        }