"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: validation.service
Issue: IA-07 — Validación

Responsabilidad:
    Orquestar la validación del contenido generado por IA-06.

Contrato:
    Contrato interno Data/IA.

Entrada:
    GeneratedContent producido por IA-06.

Salida:
    ValidationResult producido por ContentValidator.

Alcance:
    - Recibir contenido generado.
    - Delegar la validación al ContentValidator.
    - Devolver el resultado de validación.

Fuera del alcance:
    - Generación de contenido.
    - Retrieval.
    - Embeddings.
    - Persistencia.
    - Integración con Backend.
    - Implementación concreta de LLM-as-a-judge.
"""

from nuevamente.generation.models import GeneratedContent
from nuevamente.validation.models import ValidationResult
from nuevamente.validation.validator import ContentValidator


class ValidationService:
    """
    Servicio de validación del contenido generado.

    Mantiene desacoplada la orquestación de IA-07 respecto
    de las reglas concretas de validación.
    """

    def __init__(self, validator: ContentValidator) -> None:
        self._validator = validator

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

        return self._validator.validate(content)