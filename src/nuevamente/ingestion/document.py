"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: ingestion.document
Issue: IA-02 — Ingesta de documentos

Responsabilidad:
    Recibir el documento normalizado definido por el contrato
    DS ↔ Backend V1.1 y preparar una representación interna
    para las siguientes etapas del pipeline de Data/IA.

Contrato:
    DS ↔ Backend — V1.1

Entrada:
    DocumentRequest
        - document_id
        - title
        - text

Salida:
    IngestedDocument
        - document_id
        - title
        - text

Alcance:
    - Validación básica del contenido recibido.
    - Normalización conservadora del texto.
    - Conservación de la identidad del documento.
    - Preparación para IA-03 — Chunking.

Fuera del alcance:
    - Lectura de archivos PDF/DOCX/TXT.
    - OCR.
    - Chunking.
    - Embeddings.
    - Retrieval.
    - RAG.
    - Knowledge Core.
    - LLM.

Nota:
    El contrato V1.1 establece que Data/IA recibe texto normalizado.
    Por lo tanto, esta etapa no implementa extracción desde archivos.
"""

from dataclasses import dataclass

from nuevamente.models.request import DocumentRequest


class DocumentIngestionError(ValueError):
    """Error producido cuando un documento no puede ser ingerido."""


@dataclass(frozen=True)
class IngestedDocument:
    """
    Representación interna mínima de un documento ingerido.

    Esta estructura será utilizada como entrada de las siguientes
    etapas del pipeline, comenzando por IA-03 — Chunking.
    """

    document_id: str
    title: str
    text: str


def ingest_document(document: DocumentRequest) -> IngestedDocument:
    """
    Ingresa y normaliza un documento recibido desde el contrato.

    Args:
        document:
            Documento validado según DocumentRequest.

    Returns:
        IngestedDocument:
            Documento preparado para continuar en el pipeline.

    Raises:
        DocumentIngestionError:
            Si el texto no contiene contenido utilizable.
    """

    normalized_text = _normalize_text(document.text)

    if not normalized_text:
        raise DocumentIngestionError(
            "El documento no contiene texto utilizable."
        )

    return IngestedDocument(
        document_id=document.document_id.strip(),
        title=document.title.strip(),
        text=normalized_text,
    )


def _normalize_text(text: str) -> str:
    """
    Realiza una normalización conservadora del texto.

    Se conserva la estructura de párrafos para no afectar
    las siguientes etapas del pipeline.
    """

    normalized_lines = []

    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped_line = line.strip()

        if stripped_line:
            normalized_lines.append(stripped_line)

    return "\n\n".join(normalized_lines).strip()