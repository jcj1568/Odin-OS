"""
Odin's action log — every action gets written here, unconditionally.
Never raises: a logging failure must not take down the agent, but it is
printed loudly to stderr so it isn't silently lost.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Any

from odin.config import get_settings
from odin.mcp.supabase_client import get_supabase_client


def log_action(event: str, detail: dict[str, Any]) -> None:
    settings = get_settings()
    timestamp = datetime.now(timezone.utc).isoformat()

    print(f"[odin:{timestamp}] {event} {detail}", file=sys.stderr)

    client = get_supabase_client()
    if client is None:
        return

    try:
        client.schema(settings.supabase_schema).table("odin_action_log").insert(
            {"venture": settings.venture, "event": event, "detail": detail}
        ).execute()
    except Exception as exc:  # noqa: BLE001 — logging must never raise upward
        print(f"[odin:{timestamp}] action_log write failed: {exc}", file=sys.stderr)
