"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: generation.service
Issue: IA-06 — Generación + Adaptación

Responsabilidad:
    Orquestar la generación de contenido utilizando un generador
    compatible con el contrato interno de IA-06.

Contrato:
    Contrato interno Data/IA.

Entrada:
    GenerationContext.

Salida:
    GeneratedContent.

Alcance:
    - Recibir el contexto de generación.
    - Delegar la generación al ContentGenerator.
    - Devolver el resultado generado.

Fuera del alcance:
    - Retrieval.
    - Embeddings.
    - Validación de calidad.
    - Persistencia.
    - Integración con Backend.
    - Conocer el proveedor LLM concreto.
"""

from nuevamente.generation.generator import ContentGenerator
from nuevamente.generation.models import GeneratedContent, GenerationContext


class GenerationService:
    """
    Servicio de generación y adaptación de contenido.

    Mantiene desacoplada la orquestación de IA-06 respecto
    del proveedor concreto de generación.
    """

    def __init__(self, generator: ContentGenerator) -> None:
        self._generator = generator

    def generate(
        self,
        context: GenerationContext,
    ) -> GeneratedContent:
        """
        Genera contenido utilizando el generador configurado.

        Args:
            context: Contexto con chunks recuperados, perfil y formato.

        Returns:
            Contenido generado por el proveedor configurado.
        """

        if not context.chunks:
            raise ValueError(
                "GenerationContext debe contener al menos un chunk."
            )

        return self._generator.generate(context)