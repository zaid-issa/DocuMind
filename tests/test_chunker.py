import pytest

from app.services.chunker import chunk_pages
from app.services.pdf_extractor import PageText


def test_short_page_gives_one_chunk_with_metadata():
    pages = [PageText(page_number=3, text="Short text.")]

    chunks = chunk_pages(pages, "report.pdf")

    assert len(chunks) == 1
    assert chunks[0].document_name == "report.pdf"
    assert chunks[0].page_number == 3
    assert chunks[0].text == "Short text."


def test_long_page_is_split_with_overlap():
    text = "abcdefghijklmnopqrstuvwxyz" * 10  # 260 characters
    pages = [PageText(page_number=1, text=text)]

    chunks = chunk_pages(pages, "doc.pdf", chunk_size=100, overlap=20)

    assert len(chunks) == 3
    assert all(len(chunk.text) <= 100 for chunk in chunks)
    assert chunks[0].text[-20:] == chunks[1].text[:20]


def test_chunks_keep_their_own_page_numbers():
    pages = [
        PageText(page_number=1, text="Text on page one."),
        PageText(page_number=2, text="Text on page two."),
    ]

    chunks = chunk_pages(pages, "doc.pdf")

    assert [chunk.page_number for chunk in chunks] == [1, 2]


def test_overlap_must_be_smaller_than_chunk_size():
    with pytest.raises(ValueError):
        chunk_pages([], "doc.pdf", chunk_size=100, overlap=100)