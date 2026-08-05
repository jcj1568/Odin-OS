"""Loads Odin's persona as the system prompt string."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

PERSONA_PATH = Path(__file__).resolve().parent / "prompts" / "persona.md"


@lru_cache(maxsize=1)
def load_system_prompt() -> str:
    return PERSONA_PATH.read_text(encoding="utf-8")
