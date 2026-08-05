"""
Odin — Hymdal Labs' personal operating agent.

Entry point for running Odin as a persistent Claude Agent SDK process
(architecture doc: "persistent process, not one-shot CLI invocations").
Phase 0: local/interactive run only — Slack wiring is a stub
(see odin/comms/slack_stub.py) until build task 5 is real.

NOTE: the hooks block below is the part of this file most likely to need
adjustment against the currently-installed claude-agent-sdk version —
verify HookMatcher / hook return shape before relying on it (see plan
caveats).
"""

from __future__ import annotations

import asyncio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    HookMatcher,
    TextBlock,
)

from odin.action_log import log_action
from odin.config import get_settings
from odin.system_prompt import load_system_prompt
from odin.tools.n8n import n8n_server

# Tools that touch a live system on Hymdal's behalf and therefore require
# James's sign-off per odin/prompts/persona.md. Read-only / status-check
# tools are not in this set and run unsupervised.
SIGN_OFF_REQUIRED_TOOLS = {
    "mcp__n8n__trigger_workflow",
}


async def gate_unsupervised_actions(input_data: dict, tool_use_id: str | None, context: dict) -> dict:
    """PreToolUse hook: logs every tool call, and blocks anything outside
    the read/draft-only boundary until Phase 0 exit criteria are met.
    This is the code-level enforcement of the boundary described in
    odin/prompts/persona.md — the prompt sets intent, this hook is the
    backstop.
    """
    settings = get_settings()
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    log_action(event="pre_tool_use", detail={"tool": tool_name, "input": tool_input})

    if settings.unsupervised_mode != "full" and tool_name in SIGN_OFF_REQUIRED_TOOLS:
        log_action(event="tool_blocked", detail={"tool": tool_name, "reason": "requires sign-off"})
        return {
            "decision": "block",
            "reason": (
                f"'{tool_name}' requires James's sign-off before it runs "
                f"(ODIN_UNSUPERVISED_MODE={settings.unsupervised_mode})."
            ),
        }

    return {}


async def main() -> None:
    settings = get_settings()

    options = ClaudeAgentOptions(
        system_prompt=load_system_prompt(),
        model=settings.model_default,
        permission_mode=settings.permission_mode,
        mcp_servers={"n8n": n8n_server},
        allowed_tools=[
            "mcp__n8n__trigger_workflow",
            "mcp__n8n__get_workflow_status",
        ],
        hooks={
            "PreToolUse": [HookMatcher(matcher=None, hooks=[gate_unsupervised_actions])],
        },
        cwd=".",
    )

    async with ClaudeSDKClient(options=options) as client:
        log_action(event="session_start", detail={"venture": settings.venture, "model": settings.model_default})
        print(f"Odin is listening (venture={settings.venture}, model={settings.model_default}). Ctrl+C to exit.")

        while True:
            try:
                user_input = input("\nyou> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit"}:
                break

            log_action(event="user_message", detail={"text": user_input})
            await client.query(user_input)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"odin> {block.text}")
                log_action(event="agent_message", detail={"message_type": type(message).__name__})

        log_action(event="session_end", detail={})


if __name__ == "__main__":
    asyncio.run(main())
