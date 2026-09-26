"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: chunking.document
Issue: IA-03 — Chunking

Responsabilidad:
    Dividir un documento ingerido en unidades de texto manejables
    para las siguientes etapas del pipeline de Data/IA.

Entrada:
    IngestedDocument generado por IA-02.

Salida:
    Lista de DocumentChunk.

Contrato:
    DS ↔ Backend — V1.1

Alcance:
    - Chunking determinista.
    - Respeto de límites por párrafos cuando sea posible.
    - Tamaño máximo de 500 caracteres por chunk.
    - Identificación y orden de cada chunk.
    - Conservación del document_id.

Fuera del alcance:
    - Embeddings.
    - Retrieval.
    - RAG.
    - Vector Store.
    - Knowledge Core.
    - LLM.
    - Overlap entre chunks.

Nota:
    Los chunks son una representación interna de Data/IA.
    No forman parte del contrato público DS ↔ Backend.
"""

from dataclasses import dataclass

from nuevamente.ingestion.document import IngestedDocument


DEFAULT_MAX_CHARS = 500


@dataclass(frozen=True)
class DocumentChunk:
    """
    Representa una unidad de texto generada durante el chunking.
    """

    chunk_id: str
    document_id: str
    index: int
    text: str


def chunk_document(
    document: IngestedDocument,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> list[DocumentChunk]:
    """
    Divide un documento en chunks de tamaño controlado.

    Los párrafos se agrupan mientras el tamaño resultante no
    supere max_chars. Cuando un párrafo individual supera el
    límite, se divide en bloques de max_chars.

    Args:
        document:
            Documento ingerido por IA-02.

        max_chars:
            Cantidad máxima de caracteres permitida por chunk.

    Returns:
        Lista ordenada de DocumentChunk.

    Raises:
        ValueError:
            Si max_chars no es un valor positivo.
    """

    if max_chars <= 0:
        raise ValueError("max_chars debe ser mayor que cero.")

    paragraphs = [
        paragraph.strip()
        for paragraph in document.text.split("\n\n")
        if paragraph.strip()
    ]

    chunks: list[DocumentChunk] = []
    current_parts: list[str] = []
    current_length = 0

    for paragraph in paragraphs:
        if len(paragraph) > max_chars:
            if current_parts:
                chunks.append(
                    _build_chunk(
                        document=document,
                        index=len(chunks),
                        parts=current_parts,
                    )
                )
                current_parts = []
                current_length = 0

            for start in range(0, len(paragraph), max_chars):
                text = paragraph[start:start + max_chars].strip()

                if text:
                    chunks.append(
                        DocumentChunk(
                            chunk_id=f"{document.document_id}_{len(chunks)}",
                            document_id=document.document_id,
                            index=len(chunks),
                            text=text,
                        )
                    )

            continue

        additional_length = (
            len(paragraph)
            if not current_parts
            else len(paragraph) + 2
        )

        if current_parts and current_length + additional_length > max_chars:
            chunks.append(
                _build_chunk(
                    document=document,
                    index=len(chunks),
                    parts=current_parts,
                )
            )
            current_parts = [paragraph]
            current_length = len(paragraph)
        else:
            current_parts.append(paragraph)
            current_length += additional_length

    if current_parts:
        chunks.append(
            _build_chunk(
                document=document,
                index=len(chunks),
                parts=current_parts,
            )
        )

    return chunks


def _build_chunk(
    document: IngestedDocument,
    index: int,
    parts: list[str],
) -> DocumentChunk:
    """Construye un chunk a partir de uno o varios párrafos."""

    text = "\n\n".join(parts).strip()

    return DocumentChunk(
        chunk_id=f"{document.document_id}_{index}",
        document_id=document.document_id,
        index=index,
        text=text,
    )