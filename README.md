# Odin

Hymdal Labs' personal operating agent — see `hymdal-managed-agent-architecture.md`
and `hymdal-managed-agent-build-plan.md` for the full design and phased
build plan. Phase 0 status: Supabase (schema, logging) and Slack
(sending, via bot user `thor`) are live and verified. Still outstanding:
VPS provisioning, n8n, and two-way Slack (needs Socket Mode or the VPS).

## Setup

Requires Python 3.11+, [uv](https://docs.astral.sh/uv/), and Node.js.
`claude-agent-sdk` wraps the Claude Code CLI, which is a Node binary — a
Python install alone is not sufficient. Install the CLI globally (e.g.
`npm install -g @anthropic-ai/claude-code`) before running Odin.

```bash
uv sync
cp .env.example .env   # fill in ANTHROPIC_API_KEY at minimum
uv run main.py
```

## Layout

- `main.py` — entry point, persistent agent loop
- `odin/config.py` — settings, loaded from `.env` (venture-scoped)
- `odin/system_prompt.py` + `odin/prompts/persona.md` — Odin's persona and
  operating rules, including the unsupervised-vs-sign-off boundary
- `odin/action_log.py` — writes every action to stderr + Supabase
- `odin/tools/n8n.py` — n8n workflow tools, exposed as an MCP server
- `odin/mcp/supabase_client.py` — Supabase client factory
- `odin/comms/slack.py` — Slack bot integration; `send_message` is live,
  `start_listener` still needs Socket Mode or a VPS-hosted endpoint
- `db/001_logging_and_onboarding.sql` — Supabase schema to run once a
  project exists

## Verified so far

- `claude_agent_sdk`'s hook API shape in `main.py` was checked against
  the installed package (`inspect.signature`) — matches as written.
- `ODIN_MODEL_DEFAULT` (`claude-sonnet-4-6`) resolves and responds
  correctly via a live `ClaudeSDKClient` round-trip.
- Supabase: schema migrated, `service_role` granted, `log_action()`
  confirmed writing real rows to `hymdal.odin_action_log`. See
  `db/002_grant_service_role.sql` for a gotcha (non-`public` schemas
  need explicit grants) if this is ever repeated for another venture.
- Slack: bot token confirmed against the live Hymdal Labs workspace,
  `send_message()` confirmed posting to a real channel.

## Known gaps

- Direct Postgres connections must use the **connection pooler** host
  (`aws-0-<region>.pooler.supabase.com:6543`, username
  `postgres.<project_ref>`) — the direct `db.<ref>.supabase.co` host is
  IPv6-only and unreachable on networks without an IPv6 route.
- `uv`'s own downloaded Python can be blocked by Windows Application
  Control policies on locked-down machines (`unicodedata` DLL load
  failure). If so, point `.venv` at a system-installed Python instead.
- Slack `start_listener()` (two-way interaction) needs either
  `SLACK_APP_TOKEN` (Socket Mode) or a VPS-hosted Events API endpoint —
  neither exists yet.
