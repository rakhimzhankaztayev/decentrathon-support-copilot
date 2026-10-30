"""Text normalization and repair of legacy Kazakh cp1251 substitutions."""

CP1251_KAZAKH_MAP = str.maketrans({
    "ќ": "қ", "Ќ": "Қ",
    "ґ": "ғ", "Ґ": "Ғ",
    "ѕ": "ң", "Ѕ": "Ң",
    "є": "ә", "Є": "Ә",
    "ј": "ө", "Ј": "Ө",
    "ў": "ұ", "Ў": "Ұ",
    "ї": "ү", "Ї": "Ү",
})


def normalize_kazakh_cp1251(text: str) -> str:
    """Fix broken cp1251 Kazakh characters."""
    if not text:
        return ""
    return text.translate(CP1251_KAZAKH_MAP)
