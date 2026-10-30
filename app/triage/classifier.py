"""Baseline ticket classification interface."""

from app.schemas import TriageRequest


async def classify_ticket(ticket: TriageRequest, normalized_text: str) -> dict:
    """Return a stable triage result until the taxonomy model is connected."""
    lang = ticket.lang if ticket.lang and ticket.lang != "und" else "ru"
    lower_text = normalized_text.lower()
    if any(word in lower_text for word in ("спам", "реклама", "spam", "http://", "https://")):
        category = "spam"
        priority = "p3"
        duplicate = True
        confidence = 0.9
    elif ticket.kind == "complaint":
        category = "complaint.insult" if any(
            word in lower_text for word in ("оскорб", "insult", "мат", "семью")
        ) else "complaint.other"
        priority = "p1" if any(word in lower_text for word in ("угроз", "взлом", "threat")) else "p2"
        duplicate = False
        confidence = 0.85
    else:
        category = "report.question"
        priority = "p2"
        duplicate = False
        confidence = 0.8
    return {
        "lang": lang,
        "category": category,
        "priority": priority,
        "is_spam_or_duplicate": duplicate,
        "confidence": confidence,
    }
