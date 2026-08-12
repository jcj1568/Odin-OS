"""
Slack comms — real Bot Token integration (build task 5).

`send_message` is wired up and verified against the live Hymdal Labs
workspace (bot user `thor`). `start_listener` is still a stub: two-way
interaction needs either Socket Mode (a `SLACK_APP_TOKEN`, `xapp-...`,
not yet issued) or a public HTTPS endpoint for the Events API (needs the
VPS, not yet provisioned). Don't wire it up half-finished — leave it
raising until one of those two prerequisites actually exists.
"""

from __future__ import annotations

import httpx

from odin.action_log import log_action
from odin.config import get_settings

SLACK_API_BASE = "https://slack.com/api"


def send_message(text: str, channel: str | None = None) -> dict:
    settings = get_settings()
    if not settings.slack_bot_token:
        raise RuntimeError("Slack is not configured yet (SLACK_BOT_TOKEN unset).")

    target = channel or settings.slack_default_channel
    if not target:
        raise RuntimeError("No Slack channel given and SLACK_DEFAULT_CHANNEL is unset.")

    response = httpx.post(
        f"{SLACK_API_BASE}/chat.postMessage",
        headers={"Authorization": f"Bearer {settings.slack_bot_token}"},
        json={"channel": target, "text": text},
        timeout=15.0,
    )
    data = response.json()

    log_action(
        event="slack_send_message",
        detail={"channel": target, "ok": data.get("ok"), "error": data.get("error")},
    )

    if not data.get("ok"):
        raise RuntimeError(f"Slack chat.postMessage failed: {data.get('error')}")

    return data


def start_listener() -> None:
    settings = get_settings()
    if not settings.slack_bot_token:
        raise RuntimeError("Slack is not configured yet (SLACK_BOT_TOKEN unset).")
    raise NotImplementedError(
        "Slack start_listener needs Socket Mode (SLACK_APP_TOKEN) or a "
        "public Events API endpoint (VPS) — neither exists yet."
    )
