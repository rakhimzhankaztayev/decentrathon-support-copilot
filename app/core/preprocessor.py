"""Text normalization, including safe cp1251 recovery."""

from __future__ import annotations

import re
from typing import Union


def decode_text(value: Union[str, bytes]) -> str:
    """Decode bytes as UTF-8, falling back to cp1251 for legacy exports."""
    if isinstance(value, str):
        return value
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError:
        return value.decode("cp1251", errors="replace")


def normalize_text(value: Union[str, bytes]) -> str:
    """Normalize whitespace and case while preserving readable text."""
    text = decode_text(value).replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip().casefold()
