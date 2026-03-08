from pathlib import Path

from pypdf import PdfReader


class Loader:
    def load_pdf(self, path: Path) -> str:
        reader = PdfReader(path)
        return "".join(
            page.extract_text() for page in reader.pages if page.extract_text()
        )

    def load_txt(self, path: Path) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
