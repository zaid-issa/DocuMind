"""Turn text into embedding vectors using a local model"""

from pathlib import Path

from fastembed import TextEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384
DEFAULT_CACHE_DIR = Path(__file__).resolve().parents[2] / "data" / "model_cache"


class Embedder:

    def __init__(
        self,
        model_name: str = MODEL_NAME,
        cache_dir: Path = DEFAULT_CACHE_DIR,
    ) -> None:
        self._model_name = model_name
        self._cache_dir = cache_dir
        self._model: TextEmbedding | None = None

    def _get_model(self) -> TextEmbedding:
        if self._model is None:
            self._model = TextEmbedding(
                self._model_name, cache_dir=str(self._cache_dir)
            )
        return self._model

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        """Embed document chunks, one vector per text."""
        if not texts:
            return []
        return [vector.tolist() for vector in self._get_model().passage_embed(texts)]

    def embed_query(self, text: str) -> list[float]:
        """Embed a user question as a single vector."""
        vectors = self._get_model().query_embed([text])
        return next(iter(vectors)).tolist()