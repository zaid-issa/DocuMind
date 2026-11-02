import pymupdf
import pytest

from app.services.pdf_extractor import CorruptPdfError, NoTextError, extract_pages


def make_pdf(path, page_texts):
    """Create a small PDF where each string in page_texts is one page."""
    doc = pymupdf.open()
    for text in page_texts:
        page = doc.new_page()
        page.insert_text((72, 72), text)
    doc.save(str(path))
    doc.close()


def test_extract_pages_returns_one_entry_per_page(tmp_path):
    pdf_path = tmp_path / "two_pages.pdf"
    make_pdf(pdf_path, ["First page text", "Second page text"])

    pages = extract_pages(pdf_path)

    assert len(pages) == 2
    assert pages[0].page_number == 1
    assert "First page text" in pages[0].text
    assert pages[1].page_number == 2
    assert "Second page text" in pages[1].text


def test_extract_pages_raises_for_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        extract_pages(tmp_path / "does_not_exist.pdf")


def test_extract_pages_raises_for_corrupt_file(tmp_path):
    fake_pdf = tmp_path / "fake.pdf"
    fake_pdf.write_bytes(b"this is not a real pdf")

    with pytest.raises(CorruptPdfError):
        extract_pages(fake_pdf)


def test_extract_pages_raises_when_pdf_has_no_text(tmp_path):
    blank_pdf = tmp_path / "blank.pdf"
    doc = pymupdf.open()
    doc.new_page()
    doc.save(str(blank_pdf))
    doc.close()

    with pytest.raises(NoTextError):
        extract_pages(blank_pdf)