"""
Thin Supabase client factory. Returns None until real credentials exist
in .env, so callers never need to branch on "is Supabase configured" —
they just check for None.
"""

from __future__ import annotations

from functools import lru_cache

from supabase import Client, create_client

from odin.config import get_settings


@lru_cache(maxsize=1)
def get_supabase_client() -> Client | None:
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        return None
    return create_client(settings.supabase_url, settings.supabase_service_role_key)
