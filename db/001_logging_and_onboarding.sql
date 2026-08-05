-- Odin — Supabase schema (Hymdal venture)
-- Phase 0 placeholder. No live Supabase project exists yet; run this
-- migration once one does (build task 2).
--
-- One schema per venture, per CLAUDE.md — this file targets `hymdal`
-- specifically. A future venture gets its own copy under its own schema
-- name, not new tables bolted onto this one.

create schema if not exists hymdal;

create table if not exists hymdal.odin_action_log (
    id           bigint generated always as identity primary key,
    venture      text not null default 'hymdal',
    event        text not null,          -- e.g. 'user_message', 'n8n_trigger_workflow', 'tool_blocked'
    detail       jsonb not null default '{}',
    created_at   timestamptz not null default now()
);

create index if not exists idx_odin_action_log_created_at
    on hymdal.odin_action_log (created_at desc);
create index if not exists idx_odin_action_log_event
    on hymdal.odin_action_log (event);

-- Client onboarding data (Phase 0 anchor task: AI Audit -> Concierge).
-- First-pass columns — expect to change once Odin runs against real intake.
create table if not exists hymdal.onboarding_clients (
    id                bigint generated always as identity primary key,
    client_name       text not null,
    intake_source     text,              -- e.g. 'google_form', 'manual'
    intake_payload    jsonb not null default '{}',
    drive_folder_id   text,
    status            text not null default 'intake_received',
    created_at        timestamptz not null default now(),
    updated_at        timestamptz not null default now()
);

create table if not exists hymdal.onboarding_call_recordings (
    id               bigint generated always as identity primary key,
    client_id        bigint not null references hymdal.onboarding_clients (id) on delete cascade,
    recording_url    text,
    transcript_text  text,
    recorded_at      timestamptz,
    created_at       timestamptz not null default now()
);

create table if not exists hymdal.onboarding_action_items (
    id           bigint generated always as identity primary key,
    client_id    bigint not null references hymdal.onboarding_clients (id) on delete cascade,
    draft_text   text not null,
    status       text not null default 'draft',   -- 'draft' | 'approved' | 'sent'
    created_at   timestamptz not null default now()
);

-- Memory (pgvector) — placeholder, uncomment once the Supabase project
-- has the pgvector extension enabled.
-- create extension if not exists vector;
--
-- create table if not exists hymdal.odin_memory (
--     id           bigint generated always as identity primary key,
--     content      text not null,
--     embedding    vector(1536),
--     metadata     jsonb not null default '{}',
--     created_at   timestamptz not null default now()
-- );
