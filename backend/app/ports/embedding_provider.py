"""Port for text embedding models used during indexing and retrieval."""

from typing import Protocol

# Dimensão esperada do adaptador padrão BAAI/bge-m3.
BGE_M3_VECTOR_SIZE = 1024

EmbeddingVector = list[float]


class EmbeddingProvider(Protocol):
    """Embeds text batches into dense vectors for semantic retrieval."""

    def embed_texts(self, texts: list[str]) -> list[EmbeddingVector]:
        """Return one embedding vector per input text."""
        ...
