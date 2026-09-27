"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: validation.validator
Issue: IA-07 — Validación

Responsabilidad:
    Definir las reglas mínimas de validación aplicables al contenido
    generado por IA-06.

Contrato:
    Contrato interno Data/IA.

Entrada:
    GeneratedContent producido por IA-06.

Salida:
    ValidationResult.

Alcance:
    - Validar que exista contenido generado.
    - Validar que el contenido tenga una estructura utilizable.
    - Generar observaciones de validación.
    - Mantener la validación desacoplada de la generación.

Fuera del alcance:
    - Generación de contenido.
    - Retrieval.
    - Embeddings.
    - Persistencia.
    - Integración con Backend.
    - LLM-as-a-judge.
    - Cálculo definitivo de grounding.
    - Definición final del quality_score.
"""

from nuevamente.generation.models import GeneratedContent
from nuevamente.validation.models import ValidationResult, ValidationStatus


class ContentValidator:
    """
    Validador básico del contenido generado.

    Esta primera versión implementa únicamente validaciones
    estructurales mínimas.
    """

    def validate(
        self,
        content: GeneratedContent,
    ) -> ValidationResult:
        """
        Valida el contenido generado.

        Args:
            content: Resultado producido por IA-06.

        Returns:
            Resultado de la validación.
        """

        if not content.content:
            return ValidationResult(
                status=ValidationStatus.REJECTED,
                quality_score=None,
                observations=(
                    "El contenido generado está vacío.",
                ),
            )

        return ValidationResult(
            status=ValidationStatus.APPROVED,
            quality_score=None,
            observations=(
                "El contenido generado contiene información utilizable.",
            ),
        )