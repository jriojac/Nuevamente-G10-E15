"""
NUEVAMENTE — Tests de integración BGE-M3 + Chroma para IA-05.

Responsabilidad:
    Validar el flujo real de Retrieval utilizando el mismo encoder
    BGE-M3 implementado en IA-04 y ChromaDB como Vector Store.

Flujo validado:

    Texto de consulta
        ↓
    BGE-M3
        ↓
    Vector de consulta
        ↓
    ChromaDB
        ↓
    RetrievedChunk

Alcance:
    - Integración BGE-M3.
    - Integración ChromaDB.
    - Recuperación semántica.
    - Conservación de identidad del documento y chunk.

Fuera del alcance:
    - LLM.
    - Generación.
    - Prompts.
    - Knowledge Core.
    - Validación pedagógica.
    - LangGraph.
"""

from nuevamente.embeddings.bge import BGEEncoder
from nuevamente.embeddings.service import Embedding
from nuevamente.retrieval.service import Retriever
from nuevamente.retrieval.store import ChromaVectorStore


def test_bge_and_chroma_retrieve_relevant_chunk() -> None:
    encoder = BGEEncoder()

    store = ChromaVectorStore(
        collection_name="test_nuevamente_bge_retrieval",
    )

    document_embeddings = [
        Embedding(
            chunk_id="doc_redes_0",
            document_id="doc_redes",
            vector=tuple(
                encoder.encode(
                    [
                        "Una VCN permite crear una red virtual "
                        "privada dentro de OCI."
                    ]
                )[0]
            ),
        ),
        Embedding(
            chunk_id="doc_redes_1",
            document_id="doc_redes",
            vector=tuple(
                encoder.encode(
                    [
                        "Una base de datos almacena información "
                        "estructurada para su consulta."
                    ]
                )[0]
            ),
        ),
    ]

    store.add(document_embeddings)

    retriever = Retriever(
        encoder=encoder,
        store=store,
    )

    results = retriever.retrieve(
        "¿Qué es una red virtual en OCI?",
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].chunk_id == "doc_redes_0"
    assert results[0].document_id == "doc_redes"


def test_bge_and_chroma_return_similarity_score() -> None:
    encoder = BGEEncoder()

    store = ChromaVectorStore(
        collection_name="test_nuevamente_bge_score",
    )

    embedding = Embedding(
        chunk_id="doc_oci_0",
        document_id="doc_oci",
        vector=tuple(
            encoder.encode(
                [
                    "OCI proporciona servicios de computación "
                    "en la nube."
                ]
            )[0]
        ),
    )

    store.add([embedding])

    retriever = Retriever(
        encoder=encoder,
        store=store,
    )

    results = retriever.retrieve(
        "servicios de computación en OCI",
        top_k=1,
    )

    assert len(results) == 1
    assert isinstance(results[0].score, float)
    assert results[0].score > 0