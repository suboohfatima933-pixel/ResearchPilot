from pathlib import Path
import sqlite3


class DatabaseService:
    """Manages the ResearchPilot SQLite database."""

    DATABASE_DIR = Path("database")
    DATABASE_FILE = DATABASE_DIR / "research_pilot.db"

    def __init__(self):
        self.DATABASE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        """Create a database connection."""

        connection = sqlite3.connect(
            self.DATABASE_FILE
        )

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        return connection

    def _initialize_database(self) -> None:
        """Create database tables if they do not exist."""

        with self._get_connection() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chats (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    document_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (chat_id)
                        REFERENCES chats(id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.commit()