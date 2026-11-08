"""Application settings, loaded from environment variables and .env."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"


@dataclass(frozen=True)
class Settings:
    groq_api_key: str
    groq_model: str


def get_settings(env_file: Path = PROJECT_ROOT / ".env") -> Settings:
    """Read settings from the .env file; real environment variables override it."""
    values = {**dotenv_values(env_file), **os.environ}
    api_key = values.get("GROQ_API_KEY") or ""
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and fill it in."
        )
    return Settings(
        groq_api_key=api_key,
        groq_model=values.get("GROQ_MODEL") or DEFAULT_GROQ_MODEL,
    )