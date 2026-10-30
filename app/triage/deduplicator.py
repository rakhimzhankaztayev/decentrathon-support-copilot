"""Spam and near-duplicate detection."""

from __future__ import annotations

import re
from difflib import SequenceMatcher

from app.core.preprocessor import normalize_text
from app.schemas import DeduplicationResult, DuplicateMatch, Ticket


class Deduplicator:
    def __init__(self, similarity_threshold: float = 0.88) -> None:
        self.similarity_threshold = similarity_threshold
        self._history: list[tuple[str, str]] = []

    def check(self, ticket: Ticket) -> DeduplicationResult:
        text = normalize_text(f"{ticket.subject} {ticket.text}")
        is_spam = self._looks_like_spam(text)
        matches = [
            DuplicateMatch(ticket_id=ticket_id, similarity=round(SequenceMatcher(None, text, old_text).ratio(), 4))
            for ticket_id, old_text in self._history
            if SequenceMatcher(None, text, old_text).ratio() >= self.similarity_threshold
        ]
        ticket_id = ticket.id or f"ticket-{len(self._history) + 1}"
        self._history.append((ticket_id, text))
        return DeduplicationResult(is_spam=is_spam, is_duplicate=bool(matches), matches=matches)

    @staticmethod
    def _looks_like_spam(text: str) -> bool:
        words = re.findall(r"\w+", text)
        if len(words) < 3:
            return True
        return len(set(words)) / len(words) < 0.25 or text.count("http") > 3
