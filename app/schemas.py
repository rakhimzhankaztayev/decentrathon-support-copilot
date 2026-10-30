"""Shared request and response contracts."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class Ticket(BaseModel):
    """Incoming support ticket."""

    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = None
    subject: str = ""
    text: str = Field(min_length=1)
    customer_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Classification(BaseModel):
    category: str
    priority: str
    confidence: float = Field(ge=0, le=1)


class DuplicateMatch(BaseModel):
    ticket_id: str
    similarity: float = Field(ge=0, le=1)


class DeduplicationResult(BaseModel):
    is_spam: bool = False
    is_duplicate: bool = False
    matches: list[DuplicateMatch] = Field(default_factory=list)


class RetrievedDocument(BaseModel):
    title: str
    content: str
    score: float = Field(ge=0, le=1)
    source: str


class DraftResponse(BaseModel):
    answer: str
    facts: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    requires_human_review: bool = False


class TriageResponse(BaseModel):
    ticket_id: Optional[str] = None
    classification: Classification
    deduplication: DeduplicationResult
    draft: DraftResponse
