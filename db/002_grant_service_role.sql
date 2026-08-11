-- Odin — grant service_role access to the hymdal schema
--
-- Supabase's PostgREST roles (anon, authenticated, service_role) don't
-- automatically get privileges on tables outside `public`. Schema
-- exposure (Project Settings -> API -> Exposed schemas) only controls
-- whether PostgREST will route requests to a schema at all — it doesn't
-- grant the Postgres-level permissions PostgREST still enforces
-- underneath. Both are required for hymdal.* to be reachable via the
-- REST client (odin/mcp/supabase_client.py).

grant usage on schema hymdal to service_role;
grant all on all tables in schema hymdal to service_role;
grant all on all sequences in schema hymdal to service_role;

-- Cover tables/sequences created by future migrations too, not just the
-- ones that exist right now.
alter default privileges in schema hymdal grant all on tables to service_role;
alter default privileges in schema hymdal grant all on sequences to service_role;
