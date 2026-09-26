"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: validation.schema
Issue: IA-01 — Skeleton ejecutable del módulo Data/IA

Responsabilidad:
    Centraliza la validación de los modelos contractuales utilizados
    en la integración Data/IA ↔ Backend.

Contrato:
    DS ↔ Backend — V1.1

Alcance:
    - Validación del Request BE → Data/IA.
    - Validación del Response Data/IA → BE.
    - Exposición de funciones simples para reutilizar la validación.

Nota:
    Este módulo no implementa lógica de negocio del pipeline de IA.
    Su responsabilidad es validar la estructura contractual.
"""

from nuevamente.models.request import AdaptationRequest
from nuevamente.models.response import AdaptationResponse


def validate_request(data: dict) -> AdaptationRequest:
    """
    Valida y convierte un diccionario al modelo AdaptationRequest.

    Args:
        data: Datos recibidos desde Backend.

    Returns:
        Request validado como AdaptationRequest.

    Raises:
        ValueError: Cuando los datos no cumplen el modelo contractual.
    """

    return AdaptationRequest.model_validate(data)


def validate_response(data: dict) -> AdaptationResponse:
    """
    Valida y convierte un diccionario al modelo AdaptationResponse.

    Args:
        data: Datos generados por Data/IA.

    Returns:
        Response validado como AdaptationResponse.

    Raises:
        ValueError: Cuando los datos no cumplen el modelo contractual.
    """

    return AdaptationResponse.model_validate(data)