import numpy as np
import pytest

from app.services.embedder import EMBEDDING_DIM, Embedder


@pytest.fixture(scope="module")
def embedder():
    return Embedder()


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def test_embed_passages_returns_one_vector_per_text(embedder):
    vectors = embedder.embed_passages(["first text", "second text"])

    assert len(vectors) == 2
    assert all(len(vector) == EMBEDDING_DIM for vector in vectors)


def test_embed_passages_with_no_texts_returns_empty_list(embedder):
    assert embedder.embed_passages([]) == []


def test_embed_query_returns_a_single_vector(embedder):
    vector = embedder.embed_query("What are the main duties?")

    assert len(vector) == EMBEDDING_DIM


def test_related_text_is_closer_than_unrelated_text(embedder):
    query = embedder.embed_query("What are the main duties of the job?")
    related, unrelated = embedder.embed_passages(
        [
            "Key responsibilities include planning projects and reviewing code.",
            "Chocolate cake needs flour, sugar, eggs and cocoa.",
        ]
    )

    assert cosine_similarity(query, related) > cosine_similarity(query, unrelated)