"""Grounded response generation interface with human-review guardrails."""

from app.schemas import DraftReply, ExtractedFacts, TriageRequest


async def generate_rag_response(
    ticket: TriageRequest,
    normalized_text: str,
    lang: str,
    category: str,
) -> dict:
    """Extract evidence and return a safe administrator-review draft."""
    attachments_count = ticket.images_count or sum(
        message.attachments or 0 for message in ticket.messages
    )
    has_evidence = attachments_count > 0 or "скрин" in normalized_text.lower()
    extracted = ExtractedFacts(
        nickname=ticket.reported_nick,
        rule_refs=[ticket.rule_refs_raw] if ticket.rule_refs_raw else [],
        has_evidence=has_evidence,
        server=ticket.region,
    )
    draft = DraftReply(
        lang=lang,
        text="Здравствуйте! Ваше обращение принято в обработку и передано администратору.",
        cited=[],
    )
    return {
        "extracted": extracted,
        "draft_reply": draft,
        "needs_human": True,
        "reasons": ["решение о наказании подтверждает администратор"],
    }
