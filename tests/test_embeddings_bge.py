"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: tests.test_embeddings_bge
Issue: IA-04 — Embeddings

Responsabilidad:
    Validar la integración real entre DocumentChunk,
    EmbeddingService y el modelo BAAI/bge-m3.

Cobertura:
    - Generación real de un embedding.
    - Dimensión esperada de 1024.
    - Conservación de chunk_id.
    - Conservación de document_id.
    - Generación de múltiples embeddings.
    - Correspondencia entre chunks y embeddings.

Modelo:
    BAAI/bge-m3

Dispositivo:
    CPU

Nota:
    Estas pruebas son de integración y requieren que BGE-M3
    esté disponible localmente.
"""

from nuevamente.chunking.document import DocumentChunk
from nuevamente.embeddings.bge import BGEEncoder
from nuevamente.embeddings.service import EmbeddingService


def build_chunk(
    chunk_id: str,
    document_id: str = "doc_001",
    text: str = "OCI permite crear recursos en la nube.",
) -> DocumentChunk:
    """Construye un chunk para las pruebas de integración."""

    return DocumentChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        index=int(chunk_id.split("_")[-1]),
        text=text,
    )


def test_bge_generates_1024_dimension_embedding():
    """Verifica que BGE-M3 genere un vector de 1024 dimensiones."""

    service = EmbeddingService(BGEEncoder())
    chunk = build_chunk("doc_001_0")

    embedding = service.embed(chunk)

    assert len(embedding.vector) == 1024
    assert embedding.chunk_id == "doc_001_0"
    assert embedding.document_id == "doc_001"


def test_bge_generates_one_embedding_per_chunk():
    """Verifica la generación de un embedding por cada chunk."""

    service = EmbeddingService(BGEEncoder())

    chunks = [
        build_chunk(
            "doc_001_0",
            text="OCI permite crear recursos en la nube.",
        ),
        build_chunk(
            "doc_001_1",
            text="Las VCN permiten crear redes virtuales.",
        ),
    ]

    embeddings = service.embed_many(chunks)

    assert len(embeddings) == 2
    assert all(len(embedding.vector) == 1024 for embedding in embeddings)

    assert [embedding.chunk_id for embedding in embeddings] == [
        "doc_001_0",
        "doc_001_1",
    ]

    assert all(
        embedding.document_id == "doc_001"
        for embedding in embeddings
    )