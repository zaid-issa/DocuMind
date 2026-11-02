"""Clean extracted PDF text before chunking."""

import re


def clean_text(text: str) -> str:
    """Normalize whitespace in text extracted from a PDF page."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    return text.strip()