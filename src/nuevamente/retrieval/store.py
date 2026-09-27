"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: retrieval.store
Issue: IA-05 — Retrieval

Responsabilidad:
    Definir la abstracción del almacenamiento vectorial y proporcionar
    la implementación concreta utilizando ChromaDB.

Contrato:
    Contrato interno Data/IA.
    La implementación del Vector Store no forma parte del contrato
    público Backend ↔ Data/IA.

Alcance:
    - Almacenar embeddings asociados a chunks.
    - Mantener document_id y chunk_id.
    - Ejecutar búsqueda semántica.
    - Devolver RetrievedChunk.
    - Encapsular ChromaDB.

Fuera del alcance:
    - Generación de embeddings.
    - LLM.
    - Prompts.
    - Knowledge Core.
    - Generación de contenido.
    - Validación pedagógica.
    - Persistencia OCI.
"""

from collections.abc import Sequence
from typing import Protocol

import chromadb

from nuevamente.embeddings.service import Embedding
from nuevamente.retrieval.models import RetrievedChunk


class VectorStore(Protocol):
    """
    Contrato interno para un almacenamiento vectorial.

    Retrieval depende de esta abstracción y no de una tecnología concreta.
    """

    def add(
        self,
        embeddings: Sequence[Embedding],
    ) -> None:
        """Almacena embeddings para su posterior recuperación."""
        ...

    def search(
        self,
        query_vector: Sequence[float],
        top_k: int,
    ) -> list[RetrievedChunk]:
        """Busca los fragmentos más similares al vector de consulta."""
        ...


class ChromaVectorStore:
    """
    Implementación de VectorStore utilizando ChromaDB.

    El almacenamiento es efímero por defecto para el MVP de IA-05.
    La persistencia definitiva queda fuera del alcance de este issue.
    """

    def __init__(
        self,
        collection_name: str = "nuevamente_chunks",
    ) -> None:
        self._client = chromadb.Client()

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            configuration={
                "hnsw": {
                    "space": "cosine",
                }
            },
        )

    def add(
        self,
        embeddings: Sequence[Embedding],
    ) -> None:
        """
        Almacena embeddings en Chroma.

        Args:
            embeddings: Embeddings asociados a chunks.

        Raises:
            ValueError:
                Si no se proporcionan embeddings.
        """

        if not embeddings:
            raise ValueError(
                "Debe proporcionarse al menos un embedding."
            )

        self._collection.upsert(
            ids=[embedding.chunk_id for embedding in embeddings],
            embeddings=[
                list(embedding.vector)
                for embedding in embeddings
            ],
            metadatas=[
                {
                    "document_id": embedding.document_id,
                }
                for embedding in embeddings
            ],
        )

    def search(
        self,
        query_vector: Sequence[float],
        top_k: int,
    ) -> list[RetrievedChunk]:
        """
        Busca los chunks más similares a un vector de consulta.

        Args:
            query_vector: Vector de la consulta.
            top_k: Cantidad máxima de resultados.

        Returns:
            Lista de RetrievedChunk ordenada por relevancia.

        Raises:
            ValueError:
                Si el vector está vacío o top_k no es válido.
        """

        if not query_vector:
            raise ValueError(
                "El vector de consulta no puede estar vacío."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k debe ser mayor que cero."
            )

        result = self._collection.query(
            query_embeddings=[list(query_vector)],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        ids = result["ids"][0]
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]

        return [
            RetrievedChunk(
                chunk_id=chunk_id,
                document_id=metadata["document_id"],
                text=document or "",
                score=1.0 - distance,
            )
            for chunk_id, document, metadata, distance in zip(
                ids,
                documents,
                metadatas,
                distances,
            )
        ]