"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: retrieval.models
Issue: IA-05 — Retrieval

Responsabilidad:
    Definir los modelos internos utilizados por la etapa de Retrieval.

Contrato:
    Contrato interno Data/IA.
    No forma parte del contrato público Backend ↔ Data/IA.

Entrada:
    Resultados provenientes del Vector Store.

Salida:
    RetrievedChunk con la información necesaria para las
    siguientes etapas del pipeline.

Alcance:
    - Representar fragmentos recuperados.
    - Preservar identidad del documento y del chunk.
    - Exponer el score de similitud.

Fuera del alcance:
    - Generación de contenido.
    - LLM.
    - Prompts.
    - RAG completo.
    - Knowledge Core.
    - Validación pedagógica.
    - Persistencia OCI.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    """
    Representa un fragmento recuperado mediante búsqueda semántica.

    Attributes:
        chunk_id: Identificador único del fragmento.
        document_id: Identificador del documento de origen.
        text: Contenido textual del fragmento.
        score: Puntaje de similitud obtenido durante la búsqueda.
    """

    chunk_id: str
    document_id: str
    text: str
    score: float