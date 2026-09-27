"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: validation.models
Issue: IA-07 — Validación

Responsabilidad:
    Definir los modelos internos utilizados por la etapa de validación
    del contenido generado.

Contrato:
    Contrato interno Data/IA.
    No forma parte directamente del contrato público
    Backend ↔ Data/IA.

Entrada:
    GeneratedContent producido por IA-06.

Salida:
    ValidationResult con el resultado de la validación.

Alcance:
    - Representar el estado de validación.
    - Representar observaciones.
    - Representar información de calidad.
    - Mantener separada la validación de la generación.

Fuera del alcance:
    - Generación de contenido.
    - Retrieval.
    - Embeddings.
    - Persistencia.
    - Integración con Backend.
    - Implementación concreta de un LLM-as-a-judge.
"""

from dataclasses import dataclass
from enum import Enum


class ValidationStatus(str, Enum):
    """
    Estados internos de validación.

    APPROVED:
        El contenido cumple las validaciones realizadas.

    REQUIRES_ADJUSTMENT:
        El contenido requiere ajustes antes de ser considerado válido.

    REJECTED:
        El contenido no cumple las condiciones mínimas.
    """

    APPROVED = "APPROVED"
    REQUIRES_ADJUSTMENT = "REQUIRES_ADJUSTMENT"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class ValidationResult:
    """
    Resultado de la validación de contenido.

    Attributes:
        status: Estado obtenido durante la validación.
        quality_score: Puntuación de calidad disponible, si existe.
        observations: Observaciones producidas durante la validación.
    """

    status: ValidationStatus
    quality_score: float | None
    observations: tuple[str, ...]