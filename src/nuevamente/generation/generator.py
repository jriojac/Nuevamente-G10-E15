"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: generation.generator
Issue: IA-06 — Generación + Adaptación

Responsabilidad:
    Definir la abstracción del generador de contenido utilizado por
    IA-06 y proporcionar un generador falso para pruebas.

Contrato:
    Contrato interno Data/IA.

Entrada:
    GenerationContext.

Salida:
    GeneratedContent.

Alcance:
    - Definir la interfaz del generador.
    - Permitir desacoplar IA-06 de un proveedor LLM concreto.
    - Proporcionar FakeGenerator para pruebas unitarias.

Fuera del alcance:
    - Integración con Gemini.
    - Prompts definitivos.
    - Validación de calidad.
    - Persistencia.
    - Knowledge Core.
"""

from typing import Protocol

from nuevamente.generation.models import GeneratedContent, GenerationContext


class ContentGenerator(Protocol):
    """
    Contrato interno para un generador de contenido.

    IA-06 depende de esta abstracción y no de un proveedor LLM concreto.
    """

    def generate(
        self,
        context: GenerationContext,
    ) -> GeneratedContent:
        """Genera contenido a partir del contexto proporcionado."""
        ...


class FakeGenerator:
    """
    Generador determinista utilizado para pruebas.

    No utiliza ningún LLM ni servicio externo.
    """

    def __init__(self) -> None:
        self.received_context: GenerationContext | None = None

    def generate(
        self,
        context: GenerationContext,
    ) -> GeneratedContent:
        """
        Genera contenido de prueba.

        El objetivo es comprobar el flujo de IA-06 sin depender
        de un proveedor externo.
        """

        self.received_context = context

        return GeneratedContent(
            profile=context.profile,
            format=context.format,
            content={
                "generated_by": "fake_generator",
                "chunks_used": len(context.chunks),
            },
        )