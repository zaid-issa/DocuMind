import pytest

from app.services.chunker import Chunk
from app.services.vector_store import VectorStore

SAMPLE_VECTORS = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.9, 0.1, 0.0]]


@pytest.fixture
def store(tmp_path):
    return VectorStore(db_dir=tmp_path / "db")


def sample_chunks():
    return [
        Chunk("a.pdf", 1, "alpha"),
        Chunk("a.pdf", 2, "beta"),
        Chunk("a.pdf", 3, "gamma"),
    ]


def test_search_returns_nearest_chunks_first(store):
    store.add_chunks(sample_chunks(), SAMPLE_VECTORS)

    results = store.search([1.0, 0.0, 0.0], n_results=2)

    assert [r.text for r in results] == ["alpha", "gamma"]


def test_search_results_carry_citation_info(store):
    store.add_chunks(sample_chunks(), SAMPLE_VECTORS)

    top = store.search([0.0, 1.0, 0.0], n_results=1)[0]

    assert top.text == "beta"
    assert top.document_name == "a.pdf"
    assert top.page_number == 2


def test_search_on_empty_store_returns_nothing(store):
    assert store.search([1.0, 0.0, 0.0]) == []


def test_asking_for_more_results_than_stored_is_safe(store):
    store.add_chunks(sample_chunks(), SAMPLE_VECTORS)

    assert len(store.search([1.0, 0.0, 0.0], n_results=10)) == 3


def test_adding_same_chunks_twice_does_not_duplicate(store):
    store.add_chunks(sample_chunks(), SAMPLE_VECTORS)
    store.add_chunks(sample_chunks(), SAMPLE_VECTORS)

    assert store.count() == 3


def test_delete_document_removes_only_that_document(store):
    store.add_chunks(sample_chunks(), SAMPLE_VECTORS)
    store.add_chunks([Chunk("b.pdf", 1, "delta")], [[0.0, 0.0, 1.0]])

    store.delete_document("a.pdf")

    assert store.count() == 1
    assert store.search([0.0, 0.0, 1.0])[0].document_name == "b.pdf"


def test_mismatched_chunks_and_vectors_raise(store):
    with pytest.raises(ValueError):
        store.add_chunks(sample_chunks(), [[1.0, 0.0, 0.0]])