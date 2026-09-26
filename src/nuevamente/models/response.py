"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: models.response
Issue: IA-01 — Skeleton ejecutable del módulo Data/IA

Responsabilidad:
    Define los modelos de salida utilizados por Data/IA para responder
    a Backend según el contrato de integración DS ↔ Backend V1.1.

Contrato:
    DS ↔ Backend — V1.1

Alcance:
    - Estados funcionales: APPROVED, REQUIRES_ADJUSTMENT, REJECTED
    - Perfiles MVP: JUNIOR, SENIOR, EJECUTIVO
    - Formatos MVP: FLASHCARD, QUIZ, EXECUTIVE_SUMMARY, MIND_MAP
    - Fuentes y trazabilidad
    - Información de validación

Nota:
    El contenido específico de cada formato se mantiene como un objeto
    flexible en IA-01. Los schemas definitivos de FLASHCARD, QUIZ,
    EXECUTIVE_SUMMARY y MIND_MAP se implementarán posteriormente,
    respetando el contrato aprobado.

    Los detalles internos del pipeline, como embeddings, chunks,
    retrieval, vector store, prompts, LLM y Knowledge Core,
    no forman parte de este modelo contractual.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from .request import Format, Profile


class Status(str, Enum):
    """Estados funcionales de generación definidos por el contrato V1.1."""

    APPROVED = "APPROVED"
    REQUIRES_ADJUSTMENT = "REQUIRES_ADJUSTMENT"
    REJECTED = "REJECTED"


class Source(BaseModel):
    """Fuente utilizada para construir el contenido generado."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    reference: str = Field(min_length=1)
    page: int | None = Field(default=None, ge=1)
    section: str | None = None


class ValidationResult(BaseModel):
    """
    Resultado de la validación del contenido generado.

    Los campos definitivos de validation permanecen abiertos en el
    contrato V1.1, por lo que este modelo mantiene únicamente
    información compatible con la propuesta actual.
    """

    model_config = ConfigDict(extra="forbid")

    status: Status
    quality_score: float | None = Field(default=None, ge=0.0, le=1.0)
    observations: str | None = None
    reason: str | None = None


class AdaptationResponse(BaseModel):
    """Response de integración Data/IA → Backend según contrato V1.1."""

    model_config = ConfigDict(extra="forbid")

    contract_version: str = Field(default="1.1")
    request_id: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    profile: Profile
    format: Format
    status: Status
    content: dict | None = None
    sources: list[Source] = Field(default_factory=list)
    validation: ValidationResult