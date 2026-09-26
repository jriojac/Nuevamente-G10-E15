"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: tests.test_ingestion
Issue: IA-02 — Ingesta de documentos

Responsabilidad:
    Validar mediante pruebas automatizadas la ingesta y normalización
    básica de documentos recibidos por Data/IA.

Cobertura:
    - Ingesta de un documento válido.
    - Conservación de document_id y title.
    - Normalización de espacios.
    - Normalización de saltos de línea.
    - Rechazo de texto sin contenido utilizable.

Contrato:
    DS ↔ Backend — V1.1
"""

import pytest

from nuevamente.ingestion.document import (
    DocumentIngestionError,
    IngestedDocument,
    ingest_document,
)
from nuevamente.models.request import DocumentRequest


def build_document(
    document_id: str = "doc_001",
    title: str = "Manual de Docker",
    text: str = "Docker permite ejecutar aplicaciones en contenedores.",
) -> DocumentRequest:
    """Construye un documento válido para las pruebas."""

    return DocumentRequest(
        document_id=document_id,
        title=title,
        text=text,
    )


def test_ingest_document_returns_ingested_document():
    """Verifica que un documento válido sea ingerido correctamente."""

    document = build_document()

    result = ingest_document(document)

    assert isinstance(result, IngestedDocument)
    assert result.document_id == "doc_001"
    assert result.title == "Manual de Docker"
    assert result.text == (
        "Docker permite ejecutar aplicaciones en contenedores."
    )


def test_ingest_document_normalizes_spaces():
    """Verifica que se eliminen espacios innecesarios."""

    document = build_document(
        title="  Manual de Docker  ",
        text="   Docker permite ejecutar aplicaciones.   ",
    )

    result = ingest_document(document)

    assert result.title == "Manual de Docker"
    assert result.text == "Docker permite ejecutar aplicaciones."


def test_ingest_document_normalizes_line_breaks():
    """
    Verifica que se normalicen los saltos de línea conservando
    la separación entre párrafos.
    """

    document = build_document(
        text=(
            "Docker es una plataforma.\n"
            "\n"
            "\n"
            "Permite ejecutar aplicaciones en contenedores.\n"
            "   \n"
            "Es ampliamente utilizado en desarrollo."
        )
    )

    result = ingest_document(document)

    assert result.text == (
        "Docker es una plataforma.\n\n"
        "Permite ejecutar aplicaciones en contenedores.\n\n"
        "Es ampliamente utilizado en desarrollo."
    )


def test_ingest_document_rejects_empty_text():
    """Verifica que un documento sin contenido sea rechazado."""

    document = build_document(text="   \n   ")

    with pytest.raises(DocumentIngestionError):
        ingest_document(document)


def test_ingest_document_preserves_document_identity():
    """Verifica que la identidad del documento se conserve."""

    document = build_document(
        document_id="doc_oci_001",
        title="Introducción a OCI",
    )

    result = ingest_document(document)

    assert result.document_id == "doc_oci_001"
    assert result.title == "Introducción a OCI"