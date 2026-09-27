"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: tests.test_generation
Issue: IA-06 — Generación + Adaptación

Responsabilidad:
    Verificar el comportamiento de la etapa de generación y adaptación
    utilizando un generador falso, sin depender de un LLM externo.

Alcance:
    - Validar el flujo GenerationContext → GenerationService.
    - Validar la delegación al ContentGenerator.
    - Validar el resultado GeneratedContent.
    - Validar el rechazo de contexto vacío.

Fuera del alcance:
    - Integración con Gemini.
    - Validación de calidad.
    - Evaluación de grounding.
    - Pruebas de prompts.
"""


import pytest

from nuevamente.generation.generator import FakeGenerator
from nuevamente.generation.models import GenerationContext
from nuevamente.generation.service import GenerationService
from nuevamente.models.request import Format, Profile
from nuevamente.retrieval.models import RetrievedChunk


def _build_context() -> GenerationContext:
    """Construye un contexto válido para las pruebas de IA-06."""

    chunk = RetrievedChunk(
        chunk_id="doc_001_0",
        document_id="doc_001",
        text="Introducción a redes en OCI.",
        score=0.95,
    )

    return GenerationContext(
        chunks=(chunk,),
        profile=Profile.JUNIOR,
        format=Format.FLASHCARD,
    )


def test_generation_service_returns_generated_content() -> None:
    """Debe devolver contenido generado por el generador configurado."""

    generator = FakeGenerator()
    service = GenerationService(generator)

    context = _build_context()

    result = service.generate(context)

    assert result.profile == Profile.JUNIOR
    assert result.format == Format.FLASHCARD
    assert result.content["generated_by"] == "fake_generator"


def test_generation_service_delegates_context_to_generator() -> None:
    """Debe entregar el contexto recibido al generador."""

    generator = FakeGenerator()
    service = GenerationService(generator)

    context = _build_context()

    service.generate(context)

    assert generator.received_context == context


def test_generation_service_preserves_number_of_chunks() -> None:
    """Debe conservar la información sobre los chunks utilizados."""

    generator = FakeGenerator()
    service = GenerationService(generator)

    context = _build_context()

    result = service.generate(context)

    assert result.content["chunks_used"] == 1


def test_generation_service_rejects_empty_context() -> None:
    """Debe rechazar un contexto sin chunks."""

    generator = FakeGenerator()
    service = GenerationService(generator)

    context = GenerationContext(
        chunks=(),
        profile=Profile.JUNIOR,
        format=Format.FLASHCARD,
    )

    with pytest.raises(
        ValueError,
        match="GenerationContext debe contener al menos un chunk",
    ):
        service.generate(context)