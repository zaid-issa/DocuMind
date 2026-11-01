"""Extract text from PDF files, page by page."""

from dataclasses import dataclass
from pathlib import Path

import pymupdf


@dataclass(frozen=True)
class PageText:
    """Text of a single PDF page. page_number starts at 1, like a PDF viewer."""

    page_number: int
    text: str


def extract_pages(pdf_path: str | Path) -> list[PageText]:
    """Return the text of every page in the PDF, in order."""
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    pages: list[PageText] = []
    with pymupdf.open(path) as doc:
        for index, page in enumerate(doc, start=1):
            pages.append(PageText(page_number=index, text=page.get_text()))
    return pages
