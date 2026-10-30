"""Grounded draft generation with explicit guardrails."""

from __future__ import annotations

from app.schemas import (
    Classification,
    DeduplicationResult,
    DraftResponse,
    RetrievedDocument,
    Ticket,
)


class DraftGenerator:
    def __init__(self, retriever: object | None = None) -> None:
        self.retriever = retriever

    def generate(
        self,
        ticket: Ticket,
        classification: Classification,
        documents: list[RetrievedDocument],
        deduplication: DeduplicationResult,
    ) -> DraftResponse:
        if deduplication.is_spam:
            return DraftResponse(
                answer="Сообщение похоже на спам и требует ручной проверки.",
                requires_human_review=True,
            )
        facts = [document.content for document in documents]
        citations = [document.source for document in documents]
        if facts:
            answer = f"Категория обращения: {classification.category}. " + facts[0]
        else:
            answer = "Мы получили ваше обращение. Специалист изучит его и ответит дополнительно."
        return DraftResponse(
            answer=answer,
            facts=facts,
            citations=citations,
            requires_human_review=not documents or classification.confidence < 0.65,
        )
