"""
n8n tool wrappers, exposed to Odin as an in-process MCP server.
No live n8n instance exists yet (build task 3) — these call
settings.n8n_base_url, which is a placeholder until the VPS is
provisioned.
"""

from __future__ import annotations

import httpx
from claude_agent_sdk import create_sdk_mcp_server, tool

from odin.config import get_settings


@tool(
    "trigger_workflow",
    "Trigger an n8n workflow by ID with a JSON payload. Touches a live "
    "system on Hymdal's behalf — requires James's sign-off per Odin's "
    "system prompt before this is actually called.",
    {"workflow_id": str, "payload": dict},
)
async def trigger_workflow(args: dict) -> dict:
    settings = get_settings()
    if not settings.n8n_base_url:
        return {"content": [{"type": "text", "text": "n8n is not configured yet (N8N_BASE_URL unset)."}]}

    url = f"{settings.n8n_base_url}/webhook/{args['workflow_id']}"
    headers = {"Authorization": f"Bearer {settings.n8n_webhook_token}"} if settings.n8n_webhook_token else {}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=args["payload"], headers=headers, timeout=30.0)
        response.raise_for_status()
        return {"content": [{"type": "text", "text": response.text}]}


@tool(
    "get_workflow_status",
    "Read-only status check for an n8n workflow run. Safe to call unsupervised.",
    {"workflow_id": str},
)
async def get_workflow_status(args: dict) -> dict:
    settings = get_settings()
    if not settings.n8n_base_url:
        return {"content": [{"type": "text", "text": "n8n is not configured yet (N8N_BASE_URL unset)."}]}

    url = f"{settings.n8n_base_url}/webhook/{args['workflow_id']}/status"
    headers = {"Authorization": f"Bearer {settings.n8n_webhook_token}"} if settings.n8n_webhook_token else {}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=30.0)
        response.raise_for_status()
        return {"content": [{"type": "text", "text": response.text}]}


n8n_server = create_sdk_mcp_server(name="n8n", version="0.1.0", tools=[trigger_workflow, get_workflow_status])
