"""Wire the pipeline together: index PDFs and retrieve relevant chunks."""

from pathlib import Path

from app.services.chunker import chunk_pages
from app.services.embedder import Embedder
from app.services.pdf_extractor import extract_pages
from app.services.vector_store import SearchResult, VectorStore


class Retriever:
    """Indexes PDFs into the vector store and finds chunks for a question."""

    def __init__(self, embedder: Embedder, store: VectorStore) -> None:
        self._embedder = embedder
        self._store = store

    def index_pdf(self, pdf_path: str | Path) -> int:
        """Extract, chunk, embed and store a PDF. Returns the number of chunks."""
        path = Path(pdf_path)
        chunks = chunk_pages(extract_pages(path), document_name=path.name)
        vectors = self._embedder.embed_passages([chunk.text for chunk in chunks])
        self._store.delete_document(path.name)
        self._store.add_chunks(chunks, vectors)
        return len(chunks)

    def retrieve(self, question: str, n_results: int = 4) -> list[SearchResult]:
        """Return the chunks most relevant to the question, best first."""
        return self._store.search(self._embedder.embed_query(question), n_results)