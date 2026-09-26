"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: tests.test_chunking
Issue: IA-03 — Chunking

Responsabilidad:
    Validar mediante pruebas automatizadas la división determinista
    de documentos ingeridos en chunks.

Cobertura:
    - Generación de chunks.
    - Límite máximo de caracteres.
    - Conservación de párrafos.
    - Orden de los chunks.
    - Identidad del documento.
    - División de párrafos que superan el límite.
    - Validación de max_chars.

Contrato:
    DS ↔ Backend — V1.1
"""

import pytest

from nuevamente.chunking.document import (
    DocumentChunk,
    chunk_document,
)
from nuevamente.ingestion.document import IngestedDocument


def build_document(text: str) -> IngestedDocument:
    """Construye un documento ingerido para las pruebas."""

    return IngestedDocument(
        document_id="doc_001",
        title="Introducción a OCI",
        text=text,
    )


def test_chunk_document_returns_chunks():
    """Verifica que un documento produzca chunks."""

    document = build_document(
        "OCI permite crear recursos.\n\n"
        "Las VCN permiten crear redes virtuales."
    )

    chunks = chunk_document(document, max_chars=100)

    assert chunks
    assert all(isinstance(chunk, DocumentChunk) for chunk in chunks)


def test_chunks_respect_max_chars():
    """Verifica que ningún chunk supere el límite configurado."""

    document = build_document(
        "OCI permite crear recursos.\n\n"
        "Las VCN permiten crear redes virtuales.\n\n"
        "Las subredes organizan los recursos."
    )

    chunks = chunk_document(document, max_chars=60)

    assert all(len(chunk.text) <= 60 for chunk in chunks)


def test_chunks_preserve_document_identity():
    """Verifica que cada chunk conserve el document_id."""

    document = build_document(
        "Párrafo uno.\n\n"
        "Párrafo dos."
    )

    chunks = chunk_document(document, max_chars=100)

    assert all(chunk.document_id == "doc_001" for chunk in chunks)


def test_chunks_are_ordered():
    """Verifica que los chunks tengan índices consecutivos."""

    document = build_document(
        "Párrafo uno.\n\n"
        "Párrafo dos.\n\n"
        "Párrafo tres."
    )

    chunks = chunk_document(document, max_chars=20)

    assert [chunk.index for chunk in chunks] == list(range(len(chunks)))


def test_long_paragraph_is_split():
    """Verifica que un párrafo mayor al límite sea dividido."""

    document = build_document("A" * 120)

    chunks = chunk_document(document, max_chars=50)

    assert len(chunks) == 3
    assert all(len(chunk.text) <= 50 for chunk in chunks)
    assert "".join(chunk.text for chunk in chunks) == "A" * 120


def test_invalid_max_chars_is_rejected():
    """Verifica que max_chars deba ser positivo."""

    document = build_document("Texto de prueba.")

    with pytest.raises(ValueError):
        chunk_document(document, max_chars=0)