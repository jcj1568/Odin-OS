# Hymdal Managed Agent Tier — Scope & Architecture (Claude-native build)

**Positioning:** Sixth rung on the Hymdal ladder, above the $1-2K/mo concierge retainer. A fully managed, always-on agent for a client, billed $3,500-5,000/mo. Internally, the first instance of this doubles as the Hymdal client onboarding automation — you become client #1 before selling it.

---

## Architecture

```
Client Slack channel  ──┐
Client email inbox    ──┼──►  Claude Agent SDK process (persistent, 1 per client)
Client SMS (optional) ──┘         │
                                   ├─► Claude Sonnet 4.6 (escalate to Opus for complex tasks)
                                   ├─► MCP: Supabase (memory + structured client data)
                                   ├─► MCP: Airtable / Google Drive (client knowledge base)
                                   ├─► n8n (tool orchestration: Gmail, Calendar, CRM, etc.)
                                   └─► [optional, per-client] E2B/Orgo desktop for GUI-only tools
```

One lightweight VPS can host multiple client processes (isolated by working directory / env), or — for higher-liability clients — one small VPS per client. Start with the shared model; split out any client that needs stronger isolation.

## Component roles

| Role | Choice | Why |
|---|---|---|
| Harness | Claude Agent SDK | Same engine as Claude Code; built-in MCP client, subagents, hooks, computer-use support if ever needed. Keeps you on one vendor stack you already use. |
| Model | Claude Sonnet 4.6, Opus 4.7 for escalations | Already your default; no new billing relationship |
| Compute | Small persistent VPS (Hetzner/DigitalOcean, ~$10-25/mo) | Cheapest way to keep the process running 24/7; add E2B/Orgo per client only if a workflow genuinely needs GUI clicking with no API |
| Tool orchestration | n8n (self-hosted on the same VPS) | Already part of your automation stack; zero new tool to learn |
| Client comms | Slack app in client's workspace (primary); Postmark/Resend for a dedicated inbox; Twilio for SMS if a client needs it | Matches your existing concierge onboarding (Slack channel + Drive folder) |
| Memory | Supabase (pgvector + tables) | Already connected as an MCP; one schema per client |
| Knowledge base | Client's existing Drive folder or Airtable base | No new system — reuses your concierge intake pattern |
| Observability | Supabase logging table; add Langfuse later only if needed | Skip Latitude-equivalent cost until you actually need trace-level debugging |
| Secrets | Per-client `.env` on the VPS | Simple and sufficient at a 3-6 client cap; revisit if you scale past that |

## Build phases

**Phase 0 — Internal pilot (1-2 weeks)**
Stand up Odin against a real Hymdal onboarding workflow (AI Audit → Concierge client intake). Validates the harness, memory, and n8n tool calls before any client sees it.

**Phase 1 — Reusable template (1 week)**
Turn the working pilot into a repeatable deploy: a small script that provisions a new Slack app/channel, a new Supabase schema, and wires the standard n8n workflows and system prompt. This is your equivalent of Nick's `build_template.py`.

**Phase 2 — First paid pilot (ongoing, 30-day trial)**
Onboard through your existing discovery-call pattern (Fathom call → context dump → skill build). Deploy from the template. Cap at one client until it's been reliable for 30 days.

**Phase 3 — Productize**
Formalize as a $3,500-5,000/mo tier with an intake checklist. Cap at 3-6 concurrent clients, same discipline as your current concierge cap.

## Cost per client (steady state)

| Item | Cost |
|---|---|
| VPS (shared across clients) | ~$10-25/mo, split across active clients |
| Claude API usage | ~$50-150/mo depending on message/tool-call volume |
| Supabase | Free tier likely sufficient at this scale, or $25/mo Pro shared |
| n8n | Self-hosted, $0 marginal cost |
| Slack | Free (client's workspace) |
| Optional email/SMS | $5-15/mo if used |
| **Total per client** | **~$75-200/mo** against a $3,500-5,000/mo price — margin comparable to or better than the Orgo-based version, with no dependency on Orgo/Hermes/AgentMail/AgentPhone/AgentCard/Latitude |

## Open decisions

- **Isolation model:** one shared VPS for all clients (cheaper) vs. one VPS per client (safer, ~$10-25/mo more per client) — recommend shared until a client's data sensitivity says otherwise.
- **When to add a GUI desktop:** only bring in E2B/Orgo for a specific client if their required tools have no usable API — don't pay for desktop compute by default.
- **Guarantee or not:** decide whether this tier carries a reliability/refund guarantee, consistent with the open question already tracked for the Forward Deployment offering.
