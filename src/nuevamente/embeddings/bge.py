"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: embeddings.bge
Issue: IA-04 — Embeddings

Responsabilidad:
    Adaptar el modelo BAAI/bge-m3 al contrato interno
    EmbeddingEncoder utilizado por EmbeddingService.

Modelo:
    BAAI/bge-m3

Biblioteca:
    sentence-transformers

Salida:
    Vectores numéricos compatibles con EmbeddingService.

Alcance:
    - Carga del modelo BGE-M3.
    - Generación de embeddings para textos.
    - Adaptación al protocolo EmbeddingEncoder.
    - Configuración explícita del dispositivo de ejecución.

Fuera del alcance:
    - Vector Store.
    - Retrieval.
    - RAG.
    - Knowledge Core.
    - LLM.
    - Persistencia.

Nota:
    Este módulo contiene la dependencia concreta del modelo.
    El resto del pipeline no debe depender directamente de
    SentenceTransformer.

    El MVP utiliza CPU por defecto. El dispositivo puede cambiarse
    posteriormente sin modificar EmbeddingService.
"""

from collections.abc import Sequence

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-m3"
DEFAULT_DEVICE = "cpu"


class BGEEncoder:
    """
    Encoder concreto basado en BAAI/bge-m3.

    Implementa la interfaz esperada por EmbeddingService.
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME,
        device: str = DEFAULT_DEVICE,
    ):
        self._model = SentenceTransformer(
            model_name,
            device=device,
        )

    def encode(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        """
        Genera embeddings para los textos recibidos.

        Args:
            texts:
                Colección de textos a vectorizar.

        Returns:
            Lista de vectores numéricos.
        """

        if not texts:
            return []

        embeddings = self._model.encode(
            list(texts),
            convert_to_numpy=True,
        )

        return embeddings.tolist()