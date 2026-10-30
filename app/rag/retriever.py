"""Simple local retrieval over administrator rules."""

from __future__ import annotations

import json
from pathlib import Path

from app.core.preprocessor import normalize_text
from app.schemas import RetrievedDocument, Ticket


class RulesRetriever:
    def __init__(self, rules_path: Path, limit: int = 5) -> None:
        self.limit = limit
        self.rules = self._load(rules_path)

    @staticmethod
    def _load(path: Path) -> list[dict[str, str]]:
        if not path.exists():
            return []
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else data.get("rules", [])

    def retrieve(self, ticket: Ticket) -> list[RetrievedDocument]:
        query = set(normalize_text(f"{ticket.subject} {ticket.text}").split())
        ranked = []
        for rule in self.rules:
            content = str(rule.get("content", ""))
            tokens = set(normalize_text(f"{rule.get('title', '')} {content}").split())
            score = len(query & tokens) / max(len(query), 1)
            if score:
                ranked.append((score, RetrievedDocument(
                    title=str(rule.get("title", "Support rule")),
                    content=content,
                    score=score,
                    source=str(rule.get("source", "rules.json")),
                )))
        return [document for _, document in sorted(ranked, reverse=True, key=lambda item: item[0])[: self.limit]]
