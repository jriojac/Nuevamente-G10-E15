"""
NUEVAMENTE — Tests de integración de IA-05 — Retrieval.

Responsabilidad:
    Validar la integración real entre Retrieval y ChromaDB.

Alcance:
    - Almacenamiento de embeddings.
    - Búsqueda semántica.
    - Conservación de identificadores.
    - Recuperación del texto.
    - Ordenamiento por relevancia.
    - top_k.
"""

from nuevamente.embeddings.service import Embedding
from nuevamente.retrieval.store import ChromaVectorStore


def create_embedding(
    chunk_id: str,
    document_id: str,
    vector: tuple[float, ...],
) -> Embedding:
    """Crea un embedding de prueba."""
    return Embedding(
        chunk_id=chunk_id,
        document_id=document_id,
        vector=vector,
    )


def test_chroma_stores_and_retrieves_embeddings() -> None:
    store = ChromaVectorStore(
        collection_name="test_nuevamente_retrieval",
    )

    embeddings = [
        create_embedding(
            chunk_id="doc_1_0",
            document_id="doc_1",
            vector=(1.0, 0.0, 0.0),
        ),
        create_embedding(
            chunk_id="doc_1_1",
            document_id="doc_1",
            vector=(0.0, 1.0, 0.0),
        ),
    ]

    store.add(embeddings)

    results = store.search(
        query_vector=(1.0, 0.0, 0.0),
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "doc_1_0"
    assert results[0].document_id == "doc_1"


def test_chroma_orders_results_by_similarity() -> None:
    store = ChromaVectorStore(
        collection_name="test_nuevamente_similarity",
    )

    embeddings = [
        create_embedding(
            chunk_id="chunk_similar",
            document_id="doc_1",
            vector=(1.0, 0.0, 0.0),
        ),
        create_embedding(
            chunk_id="chunk_different",
            document_id="doc_1",
            vector=(0.0, 1.0, 0.0),
        ),
    ]

    store.add(embeddings)

    results = store.search(
        query_vector=(1.0, 0.0, 0.0),
        top_k=2,
    )

    assert len(results) == 2
    assert results[0].chunk_id == "chunk_similar"
    assert results[0].score > results[1].score


def test_chroma_respects_top_k() -> None:
    store = ChromaVectorStore(
        collection_name="test_nuevamente_top_k",
    )

    embeddings = [
        create_embedding(
            chunk_id=f"chunk_{index}",
            document_id="doc_1",
            vector=(1.0, float(index), 0.0),
        )
        for index in range(3)
    ]

    store.add(embeddings)

    results = store.search(
        query_vector=(1.0, 0.0, 0.0),
        top_k=2,
    )

    assert len(results) == 2


def test_chroma_preserves_document_identity() -> None:
    store = ChromaVectorStore(
        collection_name="test_nuevamente_identity",
    )

    embeddings = [
        create_embedding(
            chunk_id="chunk_001",
            document_id="document_original",
            vector=(1.0, 0.0, 0.0),
        ),
    ]

    store.add(embeddings)

    results = store.search(
        query_vector=(1.0, 0.0, 0.0),
        top_k=1,
    )

    assert results[0].chunk_id == "chunk_001"
    assert results[0].document_id == "document_original"


def test_chroma_rejects_empty_embeddings() -> None:
    store = ChromaVectorStore(
        collection_name="test_nuevamente_empty_embeddings",
    )

    try:
        store.add([])
    except ValueError as error:
        assert "embedding" in str(error).lower()
    else:
        raise AssertionError(
            "Se esperaba ValueError para una lista vacía."
        )