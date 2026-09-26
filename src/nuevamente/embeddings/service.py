"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: embeddings.service
Issue: IA-04 — Embeddings

Responsabilidad:
    Generar representaciones vectoriales de los chunks producidos
    por IA-03.

Entrada:
    DocumentChunk.

Salida:
    Embedding con:
        - chunk_id
        - document_id
        - vector

Modelo MVP:
    BAAI/bge-m3.

Arquitectura:
    EmbeddingService desacopla el pipeline del modelo concreto
    utilizado para generar los embeddings.

Contrato:
    DS ↔ Backend — V1.1

Alcance:
    - Generación de embeddings.
    - Procesamiento individual de chunks.
    - Procesamiento de múltiples chunks.
    - Conservación de la identidad del chunk.
    - Abstracción del encoder.

Fuera del alcance:
    - Vector Store.
    - Similarity Search.
    - Retrieval.
    - RAG.
    - Knowledge Core.
    - LLM.
    - Persistencia.

Nota:
    Los embeddings son una representación interna de Data/IA.
    No forman parte del contrato público DS ↔ Backend.
"""

from dataclasses import dataclass
from typing import Protocol, Sequence

from nuevamente.chunking.document import DocumentChunk


@dataclass(frozen=True)
class Embedding:
    """
    Representación vectorial de un DocumentChunk.
    """

    chunk_id: str
    document_id: str
    vector: tuple[float, ...]


class EmbeddingEncoder(Protocol):
    """
    Interfaz mínima requerida por un encoder de embeddings.

    El modelo concreto, como BGE-M3, debe proporcionar un método
    encode que reciba textos y devuelva vectores numéricos.
    """

    def encode(
        self,
        texts: Sequence[str],
    ) -> Sequence[Sequence[float]]:
        """Genera vectores para una colección de textos."""


class EmbeddingService:
    """
    Servicio responsable de transformar DocumentChunk en Embedding.

    El encoder se inyecta para mantener desacoplado el pipeline
    del modelo concreto utilizado.
    """

    def __init__(self, encoder: EmbeddingEncoder):
        self._encoder = encoder

    def embed(self, chunk: DocumentChunk) -> Embedding:
        """
        Genera el embedding correspondiente a un único chunk.

        Args:
            chunk:
                Chunk generado por IA-03.

        Returns:
            Embedding asociado al chunk.

        Raises:
            ValueError:
                Si el encoder no devuelve exactamente un vector.
        """

        vectors = self._encoder.encode([chunk.text])

        if len(vectors) != 1:
            raise ValueError(
                "El encoder debe devolver exactamente un vector "
                "para un chunk."
            )

        return Embedding(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            vector=tuple(float(value) for value in vectors[0]),
        )

    def embed_many(
        self,
        chunks: Sequence[DocumentChunk],
    ) -> list[Embedding]:
        """
        Genera embeddings para múltiples chunks.

        Args:
            chunks:
                Colección de chunks generados por IA-03.

        Returns:
            Lista ordenada de embeddings.
        """

        if not chunks:
            return []

        texts = [chunk.text for chunk in chunks]
        vectors = self._encoder.encode(texts)

        if len(vectors) != len(chunks):
            raise ValueError(
                "El encoder debe devolver un vector por cada chunk."
            )

        return [
            Embedding(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                vector=tuple(float(value) for value in vector),
            )
            for chunk, vector in zip(chunks, vectors)
        ]