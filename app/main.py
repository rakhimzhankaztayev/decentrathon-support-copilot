"""FastAPI entrypoint."""

from __future__ import annotations

from functools import lru_cache

from fastapi import FastAPI

from app.config import get_settings
from app.rag.generator import DraftGenerator
from app.rag.retriever import RulesRetriever
from app.schemas import Ticket, TriageResponse
from app.triage.classifier import TicketClassifier
from app.triage.deduplicator import Deduplicator

app = FastAPI(title=get_settings().app_name)


@lru_cache
def _components() -> tuple[TicketClassifier, Deduplicator, RulesRetriever, DraftGenerator]:
    settings = get_settings()
    retriever = RulesRetriever(settings.rules_path, settings.max_retrieved_documents)
    return (
        TicketClassifier(settings.taxonomy_path),
        Deduplicator(settings.duplicate_similarity_threshold),
        retriever,
        DraftGenerator(retriever),
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/triage", response_model=TriageResponse)
def triage(ticket: Ticket) -> TriageResponse:
    classifier, deduplicator, retriever, generator = _components()
    classification = classifier.classify(ticket)
    deduplication = deduplicator.check(ticket)
    documents = retriever.retrieve(ticket)
    draft = generator.generate(ticket, classification, documents, deduplication)
    return TriageResponse(
        ticket_id=ticket.id,
        classification=classification,
        deduplication=deduplication,
        draft=draft,
    )
