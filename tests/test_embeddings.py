"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: tests.test_embeddings
Issue: IA-04 — Embeddings

Responsabilidad:
    Validar la generación y asociación de embeddings con los chunks
    producidos por IA-03.

Cobertura:
    - Generación de un embedding.
    - Conservación de chunk_id.
    - Conservación de document_id.
    - Conversión del vector a valores float.
    - Generación de múltiples embeddings.
    - Procesamiento de lista vacía.
    - Validación de cantidad de vectores.

Contrato:
    DS ↔ Backend — V1.1
"""

import pytest

from nuevamente.chunking.document import DocumentChunk
from nuevamente.embeddings.service import EmbeddingService


class FakeEncoder:
    """
    Encoder controlado para pruebas.

    No utiliza ningún modelo externo.
    """

    def encode(self, texts):
        return [
            [0.1, 0.2, 0.3]
            for _ in texts
        ]


class TooManyVectorsEncoder:
    """
    Encoder utilizado para verificar que embed()
    rechace una cantidad incorrecta de vectores.
    """

    def encode(self, texts):
        return [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
        ]


class TooFewVectorsEncoder:
    """
    Encoder utilizado para verificar que embed_many()
    rechace una cantidad insuficiente de vectores.
    """

    def encode(self, texts):
        return [[0.1, 0.2, 0.3]]

def build_chunk(
    chunk_id: str = "doc_001_0",
    document_id: str = "doc_001",
    text: str = "OCI permite crear recursos.",
) -> DocumentChunk:
    """Construye un chunk para las pruebas."""

    return DocumentChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        index=0,
        text=text,
    )


def test_embed_generates_embedding():
    """Verifica que un chunk produzca un embedding."""

    service = EmbeddingService(FakeEncoder())
    chunk = build_chunk()

    embedding = service.embed(chunk)

    assert embedding.vector == (0.1, 0.2, 0.3)


def test_embedding_preserves_chunk_identity():
    """Verifica que el embedding conserve la identidad del chunk."""

    service = EmbeddingService(FakeEncoder())
    chunk = build_chunk()

    embedding = service.embed(chunk)

    assert embedding.chunk_id == "doc_001_0"
    assert embedding.document_id == "doc_001"


def test_embedding_vector_contains_floats():
    """Verifica que los valores del vector sean float."""

    service = EmbeddingService(FakeEncoder())
    chunk = build_chunk()

    embedding = service.embed(chunk)

    assert all(isinstance(value, float) for value in embedding.vector)


def test_embed_many_generates_one_embedding_per_chunk():
    """Verifica que se genere un embedding por cada chunk."""

    service = EmbeddingService(FakeEncoder())

    chunks = [
        build_chunk(chunk_id="doc_001_0"),
        build_chunk(chunk_id="doc_001_1"),
        build_chunk(chunk_id="doc_001_2"),
    ]

    embeddings = service.embed_many(chunks)

    assert len(embeddings) == 3
    assert [embedding.chunk_id for embedding in embeddings] == [
        "doc_001_0",
        "doc_001_1",
        "doc_001_2",
    ]


def test_embed_many_empty_list_returns_empty_list():
    """Verifica el comportamiento ante una lista vacía."""

    service = EmbeddingService(FakeEncoder())

    assert service.embed_many([]) == []


def test_embed_rejects_invalid_vector_count():
    """Verifica que embed detecte una cantidad incorrecta de vectores."""

    service = EmbeddingService(TooManyVectorsEncoder())
    chunk = build_chunk()

    with pytest.raises(ValueError):
        service.embed(chunk)


def test_embed_many_rejects_invalid_vector_count():
    """Verifica que embed_many detecte una cantidad incorrecta de vectores."""

    service = EmbeddingService(TooFewVectorsEncoder())

    chunks = [
        build_chunk(chunk_id="doc_001_0"),
        build_chunk(chunk_id="doc_001_1"),
    ]

    with pytest.raises(ValueError):
        service.embed_many(chunks)