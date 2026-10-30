"""Shared request and response contracts for triage."""

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class MessageItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    role: Literal["player", "reported_player", "admin"] = "player"
    text: str
    ts: Optional[str] = None
    attachments: Optional[int] = 0


class TriageRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    ticket_id: Optional[str] = None
    kind: Literal["complaint", "report"]
    created_at: Optional[str] = None
    region: Optional[str] = None
    server_lang: Optional[str] = None
    lang: Optional[str] = None
    reporter_hash: Optional[str] = None
    reported_hash: Optional[str] = None
    reported_nick: Optional[str] = None
    rule_refs_raw: Optional[str] = None
    images_count: Optional[int] = 0
    messages: List[MessageItem]


class ExtractedFacts(BaseModel):
    nickname: Optional[str] = None
    rule_refs: List[str] = Field(default_factory=list)
    has_evidence: bool = False
    server: Optional[str] = None


class DraftReply(BaseModel):
    lang: str
    text: str
    cited: List[str] = Field(default_factory=list)


class TriageResponse(BaseModel):
    lang: str
    category: str
    priority: Literal["p0", "p1", "p2", "p3"]
    is_spam_or_duplicate: bool
    extracted: ExtractedFacts
    draft_reply: DraftReply
    needs_human: bool
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: List[str] = Field(default_factory=list)
