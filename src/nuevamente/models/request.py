"""
NUEVAMENTE — Sistema Inteligente de Adaptación y Generación de Contenido Educativo

Módulo: models.request
Issue: IA-01 — Skeleton ejecutable del módulo Data/IA
Responsabilidad:
    Define los modelos de entrada utilizados por Data/IA para validar
    el Request recibido desde Backend.

Contrato:
    DS ↔ Backend — V1.1

Alcance:
    - Perfiles MVP: JUNIOR, SENIOR, EJECUTIVO
    - Formatos MVP: FLASHCARD, QUIZ, EXECUTIVE_SUMMARY, MIND_MAP
    - Validación estructural del Request BE → Data/IA

Nota:
    Este módulo representa únicamente el contrato de integración.
    No contiene lógica de RAG, embeddings, generación, LLM,
    Knowledge Core ni otros detalles internos del pipeline.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Profile(str, Enum):
    """Perfiles educativos definidos por el contrato V1.1."""

    JUNIOR = "JUNIOR"
    SENIOR = "SENIOR"
    EJECUTIVO = "EJECUTIVO"


class Format(str, Enum):
    """Formatos MVP definidos por el contrato V1.1."""

    FLASHCARD = "FLASHCARD"
    QUIZ = "QUIZ"
    EXECUTIVE_SUMMARY = "EXECUTIVE_SUMMARY"
    MIND_MAP = "MIND_MAP"


class DocumentRequest(BaseModel):
    """Documento normalizado recibido por Data/IA."""

    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    text: str = Field(min_length=1)


class AdaptationRequest(BaseModel):
    """Request de integración BE → Data/IA según contrato V1.1."""

    model_config = ConfigDict(extra="forbid")

    contract_version: str = Field(default="1.1")
    request_id: str = Field(min_length=1)
    document: DocumentRequest
    profile: Profile
    format: Format