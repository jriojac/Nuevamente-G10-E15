"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: predict
Issue: IA-01 — Skeleton ejecutable del módulo Data/IA

Responsabilidad:
    Exponer el punto de entrada principal de Data/IA para procesar
    solicitudes según el contrato de integración DS ↔ Backend V1.1.

Contrato:
    DS ↔ Backend — V1.1

Flujo:
    Request
        ↓
    Validación
        ↓
    Procesamiento Data/IA
        ↓
    Response

Estado IA-01:
    El pipeline real de IA todavía no está implementado.
    Esta versión utiliza una respuesta controlada (stub) para
    demostrar que la frontera contractual es ejecutable.

Fuera del alcance de IA-01:
    - Ingestión real
    - Chunking
    - Embeddings
    - Retrieval
    - RAG
    - Knowledge Core
    - LLM
    - Prompts
    - Validación avanzada de contenido
"""

from nuevamente.models.request import AdaptationRequest, Format
from nuevamente.models.response import (
    AdaptationResponse,
    Status,
    ValidationResult,
)
from nuevamente.validation.schema import validate_request


def predict(request: AdaptationRequest | dict) -> AdaptationResponse:
    """
    Punto de entrada de Data/IA.

    Args:
        request:
            Solicitud completa según el contrato DS ↔ Backend V1.1.
            Puede recibirse como AdaptationRequest o como diccionario.

    Returns:
        AdaptationResponse:
            Respuesta que cumple la estructura contractual V1.1.

    Raises:
        ValueError:
            Si el request no cumple el contrato.

    Nota:
        La generación real de contenido será implementada en
        las siguientes etapas del pipeline IA.
    """

    validated_request = (
        request
        if isinstance(request, AdaptationRequest)
        else validate_request(request)
    )

    content = _build_stub_content(validated_request.format)

    response = AdaptationResponse(
        contract_version=validated_request.contract_version,
        request_id=validated_request.request_id,
        document_id=validated_request.document.document_id,
        profile=validated_request.profile,
        format=validated_request.format,
        status=Status.APPROVED,
        content=content,
        sources=[],
        validation=ValidationResult(
            status=Status.APPROVED,
            observations="Respuesta generada por el stub de IA-01.",
        ),
    )

    return response


def _build_stub_content(format: Format) -> dict:
    """
    Construye contenido mínimo de prueba para IA-01.

    No representa generación real de contenido.
    Su objetivo es verificar que los cuatro formatos MVP
    atraviesan correctamente la frontera contractual.
    """

    if format == Format.FLASHCARD:
        return {
            "items": []
        }

    if format == Format.QUIZ:
        return {
            "items": []
        }

    if format == Format.EXECUTIVE_SUMMARY:
        return {
            "title": "Resumen ejecutivo",
            "overview": "",
            "key_points": [],
            "considerations": [],
        }

    if format == Format.MIND_MAP:
        return {
            "central_topic": "",
            "branches": [],
        }

    raise ValueError(f"Formato no soportado: {format}")