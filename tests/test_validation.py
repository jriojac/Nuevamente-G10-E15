"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: tests.test_validation
Issue: IA-07 — Validación

Responsabilidad:
    Verificar el comportamiento de la etapa de validación del contenido
    generado por IA-06.

Alcance:
    - Validar contenido generado con información.
    - Validar contenido generado vacío.
    - Verificar el estado de validación.
    - Verificar observaciones.
    - Verificar la integración ValidationService → ContentValidator.

Fuera del alcance:
    - LLM-as-a-judge.
    - Grounding.
    - Evaluación pedagógica avanzada.
    - Integración con Backend.
"""


from nuevamente.generation.models import GeneratedContent
from nuevamente.models.request import Format, Profile
from nuevamente.validation.models import ValidationStatus
from nuevamente.validation.service import ValidationService
from nuevamente.validation.validator import ContentValidator


def _build_valid_content() -> GeneratedContent:
    """Construye contenido generado válido para las pruebas."""

    return GeneratedContent(
        profile=Profile.JUNIOR,
        format=Format.FLASHCARD,
        content={
            "items": [
                {
                    "question": "¿Qué es OCI?",
                    "answer": "Oracle Cloud Infrastructure.",
                }
            ]
        },
    )


def _build_empty_content() -> GeneratedContent:
    """Construye contenido generado vacío para las pruebas."""

    return GeneratedContent(
        profile=Profile.JUNIOR,
        format=Format.FLASHCARD,
        content={},
    )


def test_validator_approves_content_with_information() -> None:
    """Debe aprobar contenido que contiene información."""

    validator = ContentValidator()

    result = validator.validate(_build_valid_content())

    assert result.status == ValidationStatus.APPROVED
    assert result.quality_score is None
    assert len(result.observations) == 1


def test_validator_rejects_empty_content() -> None:
    """Debe rechazar contenido generado vacío."""

    validator = ContentValidator()

    result = validator.validate(_build_empty_content())

    assert result.status == ValidationStatus.REJECTED
    assert result.quality_score is None
    assert "vacío" in result.observations[0]


def test_validation_service_delegates_to_validator() -> None:
    """Debe delegar la validación al ContentValidator."""

    validator = ContentValidator()
    service = ValidationService(validator)

    content = _build_valid_content()

    result = service.validate(content)

    assert result.status == ValidationStatus.APPROVED


def test_validation_result_contains_observations() -> None:
    """Debe devolver observaciones asociadas al resultado."""

    validator = ContentValidator()

    result = validator.validate(_build_valid_content())

    assert result.observations