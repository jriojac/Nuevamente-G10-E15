"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: tests.test_predict
Issue: IA-01 — Skeleton ejecutable del módulo Data/IA

Responsabilidad:
    Validar mediante pruebas automatizadas el punto de entrada
    predict() y el cumplimiento básico del contrato DS ↔ Backend V1.1.

Cobertura:
    - Request válido.
    - Response contractual.
    - Perfiles MVP.
    - Formatos MVP.
    - Rechazo de perfil inválido.
    - Rechazo de formato fuera del MVP.
    - Soporte del formato MIND_MAP.
"""

import pytest
from pydantic import ValidationError

from nuevamente.models.request import AdaptationRequest
from nuevamente.models.response import Status
from nuevamente.predict import predict


def build_request(
    profile: str = "JUNIOR",
    format: str = "FLASHCARD",
) -> dict:
    """Construye un Request válido para las pruebas."""

    return {
        "contract_version": "1.1",
        "request_id": "req_test_001",
        "document": {
            "document_id": "doc_test_001",
            "title": "Introducción a Redes en OCI",
            "text": "Texto normalizado de prueba.",
        },
        "profile": profile,
        "format": format,
    }


def test_predict_accepts_valid_request():
    """Verifica que predict() acepte un Request válido."""

    response = predict(build_request())

    assert response.request_id == "req_test_001"
    assert response.document_id == "doc_test_001"


def test_predict_returns_contract_response():
    """Verifica la estructura básica del Response V1.1."""

    response = predict(build_request())

    assert response.contract_version == "1.1"
    assert response.profile.value == "JUNIOR"
    assert response.format.value == "FLASHCARD"
    assert response.status == Status.APPROVED
    assert response.content is not None
    assert response.sources == []
    assert response.validation.status == Status.APPROVED


def test_predict_supports_mind_map():
    """Verifica que MIND_MAP esté contemplado en el MVP."""

    response = predict(
        build_request(format="MIND_MAP")
    )

    assert response.format.value == "MIND_MAP"
    assert "central_topic" in response.content
    assert "branches" in response.content


def test_invalid_profile_is_rejected():
    """Verifica que un perfil fuera del contrato sea rechazado."""

    with pytest.raises(ValidationError):
        AdaptationRequest.model_validate(
            build_request(profile="EXPERTO")
        )


def test_step_by_step_is_rejected():
    """Verifica que STEP_BY_STEP no forme parte del MVP."""

    with pytest.raises(ValidationError):
        AdaptationRequest.model_validate(
            build_request(format="STEP_BY_STEP")
        )