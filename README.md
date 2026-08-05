# Odin

Hymdal Labs' personal operating agent — see `hymdal-managed-agent-architecture.md`
and `hymdal-managed-agent-build-plan.md` for the full design and phased
build plan. This is the Phase 0 local scaffold: no live VPS, Supabase
project, n8n instance, or Slack app exists yet — those are separate build
tasks.

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
- `odin/comms/slack_stub.py` — placeholder until a real Slack app exists
- `db/001_logging_and_onboarding.sql` — Supabase schema to run once a
  project exists

## Known gaps (tracked, not accidental)

- `claude_agent_sdk`'s hook API shape in `main.py` is written from
  training-era knowledge and not yet verified against the installed
  package. Run
  `python -c "import claude_agent_sdk, inspect; print(inspect.signature(claude_agent_sdk.ClaudeAgentOptions))"`
  after `uv sync` and adjust if it's drifted.
- `ODIN_MODEL_DEFAULT` / `ODIN_MODEL_ESCALATION` default to `claude-sonnet-4-6`
  / `claude-opus-4-7` per CLAUDE.md's architecture decision — confirm these
  match real published model IDs before a live deploy.
