# CLAUDE.md — Odin: Hymdal Personal Agent Build

## Objective
Build Odin — James's personal Claude Agent SDK agent — to help run Hymdal Labs, the AI consultancy agency. This is not a client-facing product; it's the internal operating agent, in the same role Dewey plays for Nick Vasilescu (personal agent that handles the day-to-day of running the business). Client-facing managed agents sold to Hymdal customers are a separate, fully isolated build — see "Personal OS vs. client agents" below.

## Current phase
**Phase 0 — Internal pilot.** Not client-facing. Goal: Odin reliably handling one real Hymdal operational workflow for at least a week without repeated correction.

**Assumption to confirm:** Phase 0 anchor task is client onboarding automation for the AI Audit → Concierge pipeline (intake form → Drive folder setup → organizing call recordings → drafting the one-pager of top 3 action items). Flag if you want a different anchor task (sales/proposal prep, content, etc.).

## Personal OS vs. client agents
- **Odin** — one agent, sees across Hymdal's own operations (and eventually other ventures James runs — QuantumHires, rank-and-rent, Evernorth — as separate scoped sub-contexts, not pooled together)
- **Client-facing managed agents** (the $3,500-5,000/mo tier Hymdal sells) — fully separate builds, isolated data stores, no shared memory with Odin or with each other
- Any extension of Odin into another venture (e.g. QuantumHires) should use a separate Supabase schema / data store per venture, with Odin as the single orchestrating layer, not a single shared database

## Architecture (target state)
- **Harness:** Claude Agent SDK (Python), persistent process
- **Model:** Claude Sonnet 4.6 default, escalate to Opus 4.7 for complex/ambiguous tasks
- **Compute:** small VPS (Hetzner/DigitalOcean), self-hosted n8n on the same box
- **Memory:** Supabase (pgvector + structured tables) — scoped per venture as Odin extends beyond Hymdal
- **Knowledge base:** Hymdal's Drive folders / Airtable base (reuse existing concierge onboarding pattern)
- **Tool orchestration:** n8n workflows, called as tools from the agent
- **Comms surface:** Slack (James's own workspace, plus iMessage/Telegram later if wanted, matching the Dewey pattern)
- **Observability:** log agent actions to a Supabase table; no third-party tracing tool yet

## Constraints and conventions
- Don't add GUI/desktop-use (E2B, Orgo, etc.) unless a specific workflow has no usable API — default to headless
- Reuse Hymdal's existing tools wherever possible (n8n, Supabase, Airtable) — don't introduce parallel systems
- Every agent action should be logged; unsupervised actions must be limited to read + draft, not send/execute, until Phase 0 exit criteria are met
- Keep it solo-operator feasible — no infrastructure that requires a team to maintain
- Naming: the agent is Odin, consistent with Hymdal's Norse/Elder Futhark brand system (Hagalaz rune mark). Reflect this in the system prompt persona.
- "Less is more" — no bloated tool stack; every component must justify its cost against the architecture doc's cost table

## Phase 0 build tasks (current focus)
1. Provision VPS, install Node/Python + `claude-agent-sdk`
2. Create Supabase project + schema for Hymdal client onboarding data (intake, Drive folder references, call recording metadata, action-item drafts)
3. Self-host n8n on the VPS; build the onboarding automation workflow (Google Forms intake → Drive folder creation → recording org)
4. Write Odin's system prompt: persona (Norse herald tone consistent with brand voice), what it can act on unsupervised vs. what needs sign-off, logging behavior
5. Create a Slack app for James's internal workspace
6. Run against real client onboarding for the next Audit → Concierge client
7. Keep a running log of every failure/hallucination/bad tool call for hardening in Phase 1

## Reference documents
- `hymdal-managed-agent-architecture.md` — full component table and cost breakdown
- `hymdal-managed-agent-build-plan.md` — all four phases with exit criteria and timeline

## Open decisions not yet locked
- Whether/when to extend Odin into QuantumHires, rank-and-rent, or Evernorth, and what scoping boundary to enforce when that happens
- Whether the client-facing managed agent tier carries a reliability/refund guarantee or a named methodology instead
