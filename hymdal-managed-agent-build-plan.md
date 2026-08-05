# Hymdal Managed Agent Tier — Build Plan & Execution Steps

Companion to `hymdal-managed-agent-architecture.md`. This maps each phase into concrete, ordered tasks.

---

## Phase 0 — Internal Pilot (Hymdal client onboarding automation (AI Audit → Concierge pipeline))
**Target: 1-2 weeks. Goal: prove the harness works on a real task before any client sees it.**

1. **Provision compute** — spin up one small VPS (Hetzner CX22 or DigitalOcean droplet, ~$10-25/mo). Install Node/Python, `claude-agent-sdk`.
2. **Stand up memory** — create a Supabase project; build a minimal schema (candidates, clients, interaction log, embeddings table for pgvector).
3. **Connect n8n** — self-host on the same VPS; build the two core workflows this pilot needs:
   - Intake-to-Drive-folder automation (new client triggers folder + subfolder structure)
   - Call recording org + one-pager draft generation
4. **Write the agent's system prompt / persona** — define its rigor contract, what it's allowed to do unsupervised vs. what needs your sign-off, and how it logs actions to Supabase.
5. **Wire a Slack channel** (internal, just you) so you can talk to the agent the way Nick talks to Dewey.
6. **Run it for real** — point it at actual live client onboarding data (intake, Drive folder refs, call recordings, action-item drafts) in Airtable/Supabase and let it draft reactivation outreach for your review.
7. **Log what breaks** — every failure, hallucination, or bad tool call goes in a running doc. This becomes your Phase 1 hardening list.

**Exit criteria:** agent reliably drafts correct reactivation outreach for at least a week without you correcting the same mistake twice.

---

## Phase 1 — Reusable Template
**Target: 1 week. Goal: turn the one-off pilot into a repeatable deploy.**

1. **Extract the provisioning steps into a script** — new Slack app registration, new Supabase schema (via migration file, not manual clicking), new working directory on the VPS, system prompt templated with `{{client_name}}` / `{{industry}}` placeholders.
2. **Parameterize the n8n workflows** — same logic, different client data source (Airtable base ID, Drive folder ID, etc. passed as variables).
3. **Write the runbook** — a checklist doc (not just code) so this can eventually be handed to a VA or contractor, not just run by you.
4. **Dogfood it** — spin up a second instance from the template for a different internal Hymdal workflow to confirm nothing is hardcoded to the first use case.

**Exit criteria:** you can go from "new client" to "agent live in their Slack" in under a day using only the template, not manual setup.

---

## Phase 2 — First Paid Client Pilot
**Target: 30-day trial. Goal: prove it holds up on a real paying client before you productize.**

1. **Run discovery** using your existing mini-assessment structure — Fathom-recorded call, five ordered questions, pain identification.
2. **Context dump** — same pattern Nick uses: have the client dump past materials, examples, and workflow context into their onboarding channel/Drive folder.
3. **Feed the transcript + context dump to Claude** to extract the specific skills/automations this client's agent needs (you already have a Claude analysis prompt pattern from the assessment playbook — reuse/extend it here).
4. **Deploy from template** — day 1: agent live in their Slack with the core stack.
5. **Build client-specific skills** — day 2: the custom automations/integrations this client actually needs, based on step 3.
6. **Weekly check-in cadence** — same as your concierge retainer rhythm, but focused on what's working/broken with the agent specifically.
7. **Track reliability for 30 days** — uptime, error log entries, number of times you had to manually intervene, client satisfaction. This is your go/no-go data for Phase 3.

**Exit criteria:** 30 days with no client-facing failure that damaged trust, and the client would renew.

---

## Phase 3 — Productize
**Target: after Phase 2 passes. Goal: make this a repeatable, sellable tier.**

1. **Set final pricing** — $3,500-5,000/mo, positioned as the step up from the concierge retainer.
2. **Build a dedicated intake checklist** for this tier, extending your existing 42-question discovery questionnaire with agent-specific questions (what should it never do unsupervised, what tools does it need, who owns the Slack workspace).
3. **Decide the guarantee question** — same open decision already tracked for Forward Deployment: does this tier carry a reliability/refund guarantee, or a named methodology instead.
4. **Cap at 3-6 concurrent clients**, mirroring your existing concierge cap — this is still solo-operator fulfillment.
5. **Fold into your expansion menu / website copy** as the top tier above the concierge retainer.

---

## Rough timeline

| Phase | Duration | Depends on |
|---|---|---|
| 0 — Internal pilot | 1-2 weeks | Onboarding data structure defined in Airtable (intake fields, folder taxonomy) |
| 1 — Template | 1 week | Phase 0 exit criteria met |
| 2 — Paid pilot | 30 days | Phase 1 template working; a suitable existing or new client identified |
| 3 — Productize | ongoing after | Phase 2 exit criteria met |

**Total time to a sellable tier: roughly 6-8 weeks** from a standing start, assuming no major surprises in Phase 0.
