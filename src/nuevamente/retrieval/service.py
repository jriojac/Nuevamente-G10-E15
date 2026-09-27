"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: retrieval.service
Issue: IA-05 — Retrieval

Responsabilidad:
    Coordinar la generación del embedding de una consulta y la búsqueda
    semántica sobre el Vector Store.

Contrato:
    Contrato interno Data/IA.

Entrada:
    Consulta textual y parámetros de recuperación.

Salida:
    Lista de RetrievedChunk ordenados por relevancia según el Vector Store.

Alcance:
    - Generar embedding de la consulta.
    - Ejecutar búsqueda semántica.
    - Controlar top_k.
    - Mantener desacoplamiento respecto al Vector Store.

Fuera del alcance:
    - Generación de contenido.
    - LLM.
    - Prompts.
    - Knowledge Core.
    - Validación.
    - GraphRAG.
    - Persistencia OCI.
"""

from collections.abc import Sequence

from nuevamente.embeddings.service import EmbeddingEncoder
from nuevamente.retrieval.models import RetrievedChunk
from nuevamente.retrieval.store import VectorStore


DEFAULT_TOP_K = 3


class RetrievalError(ValueError):
    """Error producido durante una operación de Retrieval."""


class Retriever:
    """
    Servicio responsable de recuperar fragmentos relevantes.

    Attributes:
        encoder: Encoder utilizado para convertir la consulta en vector.
        store: Implementación del almacenamiento vectorial.
    """

    def __init__(
        self,
        encoder: EmbeddingEncoder,
        store: VectorStore,
    ) -> None:
        self._encoder = encoder
        self._store = store

    def retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
    ) -> list[RetrievedChunk]:
        """
        Recupera los fragmentos más relevantes para una consulta.

        Args:
            query: Texto de consulta.
            top_k: Cantidad máxima de resultados.

        Returns:
            Lista de fragmentos recuperados.

        Raises:
            RetrievalError:
                Si la consulta está vacía o top_k no es válido.
        """

        normalized_query = query.strip()

        if not normalized_query:
            raise RetrievalError(
                "La consulta de Retrieval no puede estar vacía."
            )

        if top_k <= 0:
            raise RetrievalError(
                "top_k debe ser mayor que cero."
            )

        query_vectors = self._encoder.encode([normalized_query])

        if len(query_vectors) != 1:
            raise RetrievalError(
                "El encoder debe devolver exactamente un vector "
                "para una consulta."
            )

        query_vector: Sequence[float] = query_vectors[0]

        return self._store.search(
            query_vector=query_vector,
            top_k=top_k,
        )