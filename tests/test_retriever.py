import pymupdf
import pytest

from app.services.embedder import Embedder
from app.services.retriever import Retriever
from app.services.vector_store import VectorStore


@pytest.fixture(scope="module")
def embedder():
    return Embedder()


@pytest.fixture
def retriever(embedder, tmp_path):
    return Retriever(embedder, VectorStore(db_dir=tmp_path / "db"))


@pytest.fixture
def two_page_pdf(tmp_path):
    path = tmp_path / "notes.pdf"
    doc = pymupdf.open()
    for text in [
        "Python and Java are programming languages used for software development.",
        "Chocolate cake needs flour, sugar, eggs and cocoa to bake.",
    ]:
        doc.new_page().insert_text((72, 72), text)
    doc.save(str(path))
    doc.close()
    return path


def test_index_pdf_returns_number_of_chunks(retriever, two_page_pdf):
    assert retriever.index_pdf(two_page_pdf) == 2


def test_retrieve_finds_the_relevant_page(retriever, two_page_pdf):
    retriever.index_pdf(two_page_pdf)

    top = retriever.retrieve("Which programming languages are mentioned?", n_results=1)[0]

    assert top.document_name == "notes.pdf"
    assert top.page_number == 1


def test_indexing_the_same_pdf_twice_does_not_duplicate(retriever, two_page_pdf):
    retriever.index_pdf(two_page_pdf)
    retriever.index_pdf(two_page_pdf)

    assert len(retriever.retrieve("anything", n_results=10)) == 2