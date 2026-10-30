"""Deterministic baseline classifier for categories and priorities."""

from __future__ import annotations

import json
from pathlib import Path

from app.core.preprocessor import normalize_text
from app.schemas import Classification, Ticket


DEFAULT_CATEGORIES = {
    "access": ["парол", "вход", "логин", "password", "login", "access"],
    "billing": ["оплат", "счет", "платеж", "invoice", "billing", "charge"],
    "technical": ["ошиб", "не работает", "сбой", "error", "broken", "failed"],
}


class TicketClassifier:
    def __init__(self, taxonomy_path: Path | None = None) -> None:
        self.categories = self._load_categories(taxonomy_path)

    @staticmethod
    def _load_categories(path: Path | None) -> dict[str, list[str]]:
        if path and path.exists():
            with path.open(encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict) and isinstance(data.get("categories"), dict):
                return data["categories"]
        return DEFAULT_CATEGORIES

    def classify(self, ticket: Ticket) -> Classification:
        text = normalize_text(f"{ticket.subject} {ticket.text}")
        scores = {
            category: sum(1 for keyword in keywords if normalize_text(keyword) in text)
            for category, keywords in self.categories.items()
        }
        category, matches = max(scores.items(), key=lambda item: item[1], default=("general", 0))
        confidence = min(0.95, 0.5 + matches * 0.15) if matches else 0.35
        priority = "urgent" if any(word in text for word in ("срочно", "urgent", "critical")) else "normal"
        if any(word in text for word in ("заблок", "невозможно", "security", "взлом")):
            priority = "high"
        return Classification(category=category, priority=priority, confidence=confidence)
