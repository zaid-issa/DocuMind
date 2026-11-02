"""Extract text from PDF files, page by page."""

from dataclasses import dataclass
from pathlib import Path

import pymupdf


class PdfExtractionError(Exception):
    """Base class for all PDF extraction problems."""


class CorruptPdfError(PdfExtractionError):
    """The file could not be read as a PDF."""


class NoTextError(PdfExtractionError):
    """The PDF has no extractable text (for example, a scanned document)."""


@dataclass(frozen=True)
class PageText:
    """Text of a single PDF page. page_number starts at 1."""

    page_number: int
    text: str


def extract_pages(pdf_path: str | Path) -> list[PageText]:
    """Return the text of every page in the PDF, in order."""
    path = Path(pdf_path)
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")

    try:
        doc = pymupdf.open(path)
    except pymupdf.FileDataError as exc:
        raise CorruptPdfError(f"Cannot read PDF: {path}") from exc

    pages: list[PageText] = []
    with doc:
        for index, page in enumerate(doc, start=1):
            pages.append(PageText(page_number=index, text=page.get_text()))

    if not any(page.text.strip() for page in pages):
        raise NoTextError(f"No extractable text in PDF (scanned?): {path}")
    return pages