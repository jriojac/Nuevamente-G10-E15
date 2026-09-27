"""
NUEVAMENTE — Tests de IA-05 — Retrieval.

Responsabilidad:
    Validar el comportamiento del servicio de Retrieval
    utilizando dobles de prueba.

Alcance:
    - Validación de consultas.
    - Validación de top_k.
    - Generación del embedding de consulta.
    - Delegación al Vector Store.
    - Conservación de resultados.
"""

from collections.abc import Sequence

import pytest

from nuevamente.retrieval.models import RetrievedChunk
from nuevamente.retrieval.service import RetrievalError, Retriever


class FakeEncoder:
    """Encoder falso utilizado para pruebas unitarias."""

    def __init__(self) -> None:
        self.received_texts: list[str] = []

    def encode(self, texts: Sequence[str]) -> list[list[float]]:
        self.received_texts.extend(texts)
        return [[0.1, 0.2, 0.3]]


class FakeVectorStore:
    """Vector Store falso utilizado para pruebas unitarias."""

    def __init__(self) -> None:
        self.received_vector: Sequence[float] | None = None
        self.received_top_k: int | None = None

    def search(
        self,
        query_vector: Sequence[float],
        top_k: int,
    ) -> list[RetrievedChunk]:
        self.received_vector = query_vector
        self.received_top_k = top_k

        return [
            RetrievedChunk(
                chunk_id="doc_1_0",
                document_id="doc_1",
                text="Contenido relevante.",
                score=0.95,
            )
        ]


def create_retriever() -> tuple[Retriever, FakeEncoder, FakeVectorStore]:
    """Crea un Retriever utilizando dependencias falsas."""
    encoder = FakeEncoder()
    store = FakeVectorStore()

    retriever = Retriever(
        encoder=encoder,
        store=store,
    )

    return retriever, encoder, store


def test_retrieve_returns_relevant_chunks() -> None:
    retriever, _, _ = create_retriever()

    results = retriever.retrieve("¿Qué es una red?")

    assert len(results) == 1
    assert results[0].chunk_id == "doc_1_0"
    assert results[0].document_id == "doc_1"
    assert results[0].score == 0.95


def test_retrieve_generates_embedding_for_query() -> None:
    retriever, encoder, _ = create_retriever()

    retriever.retrieve("  ¿Qué es una red?  ")

    assert encoder.received_texts == ["¿Qué es una red?"]


def test_retrieve_uses_default_top_k() -> None:
    retriever, _, store = create_retriever()

    retriever.retrieve("¿Qué es una red?")

    assert store.received_top_k == 3


def test_retrieve_uses_custom_top_k() -> None:
    retriever, _, store = create_retriever()

    retriever.retrieve("¿Qué es una red?", top_k=5)

    assert store.received_top_k == 5


def test_retrieve_rejects_empty_query() -> None:
    retriever, _, _ = create_retriever()

    with pytest.raises(RetrievalError):
        retriever.retrieve("   ")


def test_retrieve_rejects_invalid_top_k() -> None:
    retriever, _, _ = create_retriever()

    with pytest.raises(RetrievalError):
        retriever.retrieve("¿Qué es una red?", top_k=0)


def test_retrieve_returns_empty_when_store_has_no_results() -> None:
    class EmptyVectorStore:
        def search(
            self,
            query_vector: Sequence[float],
            top_k: int,
        ) -> list[RetrievedChunk]:
            return []

    encoder = FakeEncoder()
    retriever = Retriever(
        encoder=encoder,
        store=EmptyVectorStore(),
    )

    results = retriever.retrieve("consulta sin resultados")

    assert results == []