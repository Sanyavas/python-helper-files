import json
from pathlib import Path

from utils.py_logger import get_logger

logger = get_logger(__name__)


class FileWriter:
    """Save data to different file formats."""

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def _create_directory(self):
        """Create parent directory if it does not exist."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save_json(self, data):
        """Save data to JSON file."""
        try:
            self._create_directory()
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logger.info(f"Saved to {self.file_path}")
        except Exception as e:
            logger.error(f"Error writing JSON file: {e}")

    def save_text(self, data: str):
        """Save data to text file."""
        try:
            self._create_directory()
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(data)
            logger.info(f"Saved to {self.file_path}")
        except Exception as e:
            logger.error(f"Error writing text file: {e}")

    def save_pdf(self, data: bytes):
        """Save data to PDF file."""
        try:
            self._create_directory()
            with open(self.file_path, "wb") as file:
                file.write(data)
            logger.info(f"Saved to {self.file_path}")
        except Exception as e:
            logger.error(f"Error writing PDF file: {e}")