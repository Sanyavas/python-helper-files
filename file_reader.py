import json
from pathlib import Path

import docx2txt
from PyPDF2 import PdfReader

from utils.py_logger import get_logger

logger = get_logger(__name__)


class FileReader:
    """Read content from different file formats."""

    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".json", ".docx"}

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.content = None

    def read(self):
        extension = self.file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            logger.warning(f"{self.file_path} | Unsupported file format")
            return None

        if extension == ".pdf":
            self._read_pdf()
        elif extension in {".txt", ".md"}:
            self._read_text_file()
        elif extension == ".json":
            self._read_json()
        elif extension == ".docx":
            self._read_docx()

        return self.content

    def _read_pdf(self):
        """Read text from PDF file."""
        try:
            with open(self.file_path, "rb") as pdf_file:
                reader = PdfReader(pdf_file)
                self.content = "".join(page.extract_text() or "" for page in reader.pages)
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
        except Exception as e:
            logger.error(f"Error reading PDF file: {e}")

    def _read_text_file(self):
        """Read content from TXT or MD file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.content = file.read()
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
        except Exception as e:
            logger.error(f"Error reading text file: {e}")

    def _read_json(self):
        """Read content from JSON file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.content = json.load(file)
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
        except Exception as e:
            logger.error(f"Error reading JSON file: {e}")

    def _read_docx(self):
        """Read text from DOCX file."""
        try:
            self.content = docx2txt.process(str(self.file_path))
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
        except Exception as e:
            logger.error(f"Error reading DOCX file: {e}")