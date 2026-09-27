"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: generation.models
Issue: IA-06 — Generación + Adaptación

Responsabilidad:
    Definir los modelos internos utilizados por la etapa de generación
    y adaptación del contenido.

Contrato:
    Contrato interno Data/IA.
    No forma parte del contrato público Backend ↔ Data/IA.

Entrada:
    Contexto recuperado desde IA-05, perfil y formato solicitado.

Salida:
    GeneratedContent con el formato y contenido producido.

Alcance:
    - Representar el resultado de generación.
    - Mantener asociado el formato solicitado.
    - Mantener el contenido separado de la implementación del LLM.

Fuera del alcance:
    - Validación de calidad.
    - Persistencia.
    - LLM concreto.
    - Prompts concretos.
    - Knowledge Core.
    - Integración con Backend.
"""

from dataclasses import dataclass
from typing import Any

from nuevamente.models.request import Format, Profile
from nuevamente.retrieval.models import RetrievedChunk


@dataclass(frozen=True)
class GenerationContext:
    """
    Contexto que será utilizado por el generador.

    Attributes:
        chunks: Fragmentos relevantes recuperados por IA-05.
        profile: Perfil educativo solicitado.
        format: Formato de contenido solicitado.
    """

    chunks: tuple[RetrievedChunk, ...]
    profile: Profile
    format: Format


@dataclass(frozen=True)
class GeneratedContent:
    """
    Resultado interno de la etapa de generación.

    Attributes:
        profile: Perfil utilizado para la adaptación.
        format: Formato generado.
        content: Contenido producido por el generador.
    """

    profile: Profile
    format: Format
    content: dict[str, Any]