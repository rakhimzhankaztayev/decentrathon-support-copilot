"""Batch prediction CLI for JSONL tickets."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from app.config import get_settings
from app.main import _components
from app.schemas import Ticket


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input JSONL file")
    parser.add_argument("-o", "--output", type=Path, default=Path("predictions.jsonl"))
    args = parser.parse_args()
    classifier, deduplicator, retriever, generator = _components()
    started = time.perf_counter()
    count = 0
    with args.input.open(encoding="utf-8") as source, args.output.open("w", encoding="utf-8") as target:
        for line in source:
            if not line.strip():
                continue
            ticket = Ticket.model_validate(json.loads(line))
            classification = classifier.classify(ticket)
            deduplication = deduplicator.check(ticket)
            draft = generator.generate(ticket, classification, retriever.retrieve(ticket), deduplication)
            target.write(json.dumps({
                "ticket_id": ticket.id,
                "category": classification.category,
                "priority": classification.priority,
                "confidence": classification.confidence,
                "is_spam": deduplication.is_spam,
                "is_duplicate": deduplication.is_duplicate,
                "draft": draft.answer,
            }, ensure_ascii=False) + "\n")
            count += 1
    elapsed = time.perf_counter() - started
    print(json.dumps({"tickets": count, "seconds": round(elapsed, 4), "tickets_per_second": round(count / elapsed, 2) if elapsed else 0}))


if __name__ == "__main__":
    main()
