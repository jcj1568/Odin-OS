"""
Odin configuration — loads environment variables (scoped per venture) and
exposes typed settings to the rest of the app.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    venture: str
    model_default: str
    model_escalation: str
    permission_mode: str
    unsupervised_mode: str

    supabase_url: str | None
    supabase_service_role_key: str | None
    supabase_schema: str

    n8n_base_url: str | None
    n8n_webhook_token: str | None

    slack_bot_token: str | None
    slack_default_channel: str | None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load settings once per process. Looks for a venture-scoped .env
    first (`.env.<venture>`), falling back to the shared `.env`. Hymdal is
    the only venture right now; this scoping exists so Odin can extend to
    other ventures (QuantumHires, rank-and-rent, Evernorth) without a
    restructure — each venture gets its own env file and Supabase schema,
    never a shared one.
    """
    venture = os.environ.get("ODIN_VENTURE", "hymdal")

    venture_env = ROOT_DIR / f".env.{venture}"
    default_env = ROOT_DIR / ".env"
    load_dotenv(venture_env if venture_env.exists() else default_env)

    return Settings(
        venture=venture,
        model_default=os.environ.get("ODIN_MODEL_DEFAULT", "claude-sonnet-4-6"),
        model_escalation=os.environ.get("ODIN_MODEL_ESCALATION", "claude-opus-4-7"),
        permission_mode=os.environ.get("ODIN_PERMISSION_MODE", "default"),
        unsupervised_mode=os.environ.get("ODIN_UNSUPERVISED_MODE", "read_draft_only"),
        supabase_url=os.environ.get("SUPABASE_URL"),
        supabase_service_role_key=os.environ.get("SUPABASE_SERVICE_ROLE_KEY"),
        supabase_schema=os.environ.get("SUPABASE_SCHEMA", venture),
        n8n_base_url=os.environ.get("N8N_BASE_URL"),
        n8n_webhook_token=os.environ.get("N8N_WEBHOOK_TOKEN"),
        slack_bot_token=os.environ.get("SLACK_BOT_TOKEN"),
        slack_default_channel=os.environ.get("SLACK_DEFAULT_CHANNEL"),
    )
