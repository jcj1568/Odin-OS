"""
Slack comms stub. No Slack app is registered yet (build task 5) — this
exists so main.py and future callers have a stable interface to wire up
once one is.
"""

from __future__ import annotations

from odin.config import get_settings


def send_message(text: str, channel: str | None = None) -> None:
    settings = get_settings()
    target = channel or settings.slack_default_channel
    if not settings.slack_bot_token:
        raise RuntimeError("Slack is not configured yet (SLACK_BOT_TOKEN unset).")
    raise NotImplementedError(f"Slack send_message to {target!r} not yet wired up.")


def start_listener() -> None:
    settings = get_settings()
    if not settings.slack_bot_token:
        raise RuntimeError("Slack is not configured yet (SLACK_BOT_TOKEN unset).")
    raise NotImplementedError("Slack start_listener not yet wired up.")
