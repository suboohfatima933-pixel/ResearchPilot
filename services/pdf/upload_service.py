from pathlib import Path
from datetime import datetime
import re
import shutil


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

        # Generate a unique, human-readable filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        sanitized_filename = re.sub(
            r"[^a-zA-Z0-9._-]",
            "_",
            uploaded_file.name,
        )

        unique_filename = f"{timestamp}_{sanitized_filename}"

        destination = self.UPLOAD_DIR / unique_filename

        with open(destination, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)

        return {
            "filename": unique_filename,
            "original_filename": uploaded_file.name,
            "filepath": str(destination),
            "size": uploaded_file.size,
        }