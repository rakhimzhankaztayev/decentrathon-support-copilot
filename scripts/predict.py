"""Concurrent batch inference with latency metrics."""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.main import process_single_ticket
from app.schemas import TriageRequest


async def run_batch(input_path: str, output_path: str, concurrency: int = 10) -> None:
    semaphore = asyncio.Semaphore(concurrency)
    latencies = []
    with open(input_path, "r", encoding="utf-8") as source:
        lines = [line.strip() for line in source if line.strip()]

    async def worker(index: int, raw_line: str) -> tuple:
        async with semaphore:
            started = time.perf_counter()
            request = TriageRequest.model_validate(json.loads(raw_line))
            response = await process_single_ticket(request)
            latencies.append(time.perf_counter() - started)
            result = response.model_dump()
            if request.ticket_id:
                result["ticket_id"] = request.ticket_id
            return index, result

    results = await asyncio.gather(*(worker(index, line) for index, line in enumerate(lines)))
    results.sort(key=lambda item: item[0])
    with open(output_path, "w", encoding="utf-8") as target:
        for _, result in results:
            target.write(json.dumps(result, ensure_ascii=False) + "\n")
    if latencies:
        print(
            f"Processed {len(results)} tickets | "
            f"p50: {np.percentile(latencies, 50):.3f}s | "
            f"p95: {np.percentile(latencies, 95):.3f}s"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--concurrency", type=int, default=10)
    arguments = parser.parse_args()
    asyncio.run(run_batch(arguments.input, arguments.output, arguments.concurrency))
