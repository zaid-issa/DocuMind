"""Store chunk vectors in ChromaDB and search them by similarity."""

from dataclasses import dataclass
from pathlib import Path

import chromadb
from chromadb.config import Settings

from app.services.chunker import Chunk

DEFAULT_DB_DIR = Path(__file__).resolve().parents[2] / "data" / "chroma_db"
COLLECTION_NAME = "documind_chunks"


@dataclass(frozen=True)
class SearchResult:
    """A retrieved chunk with its source. Lower distance means a closer match."""

    document_name: str
    page_number: int
    text: str
    distance: float


class VectorStore:
    """Persistent vector store backed by a local ChromaDB folder."""

    def __init__(
        self,
        db_dir: Path = DEFAULT_DB_DIR,
        collection_name: str = COLLECTION_NAME,
    ) -> None:
        client = chromadb.PersistentClient(
            path=str(db_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def count(self) -> int:
        """Number of chunks stored."""
        return self._collection.count()

    def add_chunks(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Store chunks with their vectors. Re-adding the same chunks overwrites them."""
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors must have the same length")
        if not chunks:
            return
        self._collection.upsert(
            ids=[f"{chunk.document_name}:{i}" for i, chunk in enumerate(chunks)],
            embeddings=vectors,
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {"document_name": chunk.document_name, "page_number": chunk.page_number}
                for chunk in chunks
            ],
        )

    def delete_document(self, document_name: str) -> None:
        """Remove every chunk that came from the given document."""
        self._collection.delete(where={"document_name": document_name})

    def search(self, query_vector: list[float], n_results: int = 5) -> list[SearchResult]:
        """Return the chunks closest to the query vector, nearest first."""
        stored = self._collection.count()
        if stored == 0:
            return []
        results = self._collection.query(
            query_embeddings=[query_vector],
            n_results=min(n_results, stored),
            include=["documents", "metadatas", "distances"],
        )
        return [
            SearchResult(
                document_name=metadata["document_name"],
                page_number=metadata["page_number"],
                text=text,
                distance=distance,
            )
            for text, metadata, distance in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]