"""Split page text into overlapping chunks that remember their source."""

from dataclasses import dataclass

from app.services.pdf_extractor import PageText
from app.services.text_cleaner import clean_text


@dataclass(frozen=True)
class Chunk:
    """A piece of text with the document and page it came from."""

    document_name: str
    page_number: int
    text: str


def chunk_pages(
    pages: list[PageText],
    document_name: str,
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[Chunk]:
    """Split pages into overlapping chunks, keeping the page number."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    step = chunk_size - overlap
    chunks: list[Chunk] = []

    for page in pages:
        text = clean_text(page.text)
        start = 0
        while start < len(text):
            piece = text[start : start + chunk_size].strip()
            if piece:
                chunks.append(Chunk(document_name, page.page_number, piece))
            if start + chunk_size >= len(text):
                break
            start += step

    return chunks