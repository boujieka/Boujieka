"""Running behind the Netlify-hosted Next.js proxy and a container host: client IP for rate limits, and the
production start-up checks."""
from __future__ import annotations

import random
import uuid

import pytest
from starlette.requests import Request

from .test_api import PW, new_client


def _req(peer: str, xff: str | None) -> Request:
    headers = [(b"x-forwarded-for", xff.encode())] if xff is not None else []
    return Request({"type": "http", "method": "POST", "path": "/", "headers": headers, "client": (peer, 1234)})


@pytest.fixture()
def settings(db_ready):
    from app.config import get_settings
    return get_settings()


def test_client_ip_ignores_forwarded_for_by_default(settings, monkeypatch):
    from app.routers.auth import _ip
    monkeypatch.setattr(settings, "trusted_proxy_hops", 0)
    assert _ip(_req("10.0.0.9", "1.2.3.4")) == "10.0.0.9"


def test_client_ip_takes_nth_entry_from_the_right(settings, monkeypatch):
    from app.routers.auth import _ip
    monkeypatch.setattr(settings, "trusted_proxy_hops", 2)
    # forged entry, real client (added by proxy 1), proxy 1 address (added by proxy 2); peer is proxy 2
    assert _ip(_req("10.0.0.9", "6.6.6.6, 203.0.113.7, 198.51.100.2")) == "203.0.113.7"
    monkeypatch.setattr(settings, "trusted_proxy_hops", 1)
    assert _ip(_req("10.0.0.9", "6.6.6.6, 203.0.113.7")) == "203.0.113.7"
    # too few entries: the request did not come through the chain, fall back to the TCP peer
    monkeypatch.setattr(settings, "trusted_proxy_hops", 2)
    assert _ip(_req("10.0.0.9", "203.0.113.7")) == "10.0.0.9"
    assert _ip(_req("10.0.0.9", None)) == "10.0.0.9"


def _register(c, ip: str) -> int:
    return c.post("/api/auth/register", headers={"x-forwarded-for": f"{ip}, 198.51.100.2"},
                  json={"email": f"p{uuid.uuid4().hex[:10]}@example.com", "password": PW, "full_name": "P",
                        "org_name": "O", "org_kind": "developer", "accept_terms": True}).status_code


def test_register_limit_is_per_client_behind_the_proxy(settings, monkeypatch):
    monkeypatch.setattr(settings, "trusted_proxy_hops", 2)
    monkeypatch.setattr(settings, "register_rate_per_minute", 1)
    a, b = (f"203.0.{random.randint(0, 255)}.{random.randint(1, 254)}" for _ in range(2))
    while b == a:
        b = f"203.0.{random.randint(0, 255)}.{random.randint(1, 254)}"
    c = new_client()
    assert _register(c, a) == 201
    assert _register(c, b) == 201  # another user behind the same proxy is not blocked
    assert _register(c, a) == 429


def test_production_start_up_lists_missing_settings(monkeypatch):
    from app.config import Settings
    for v in ("A360_DATABASE_URL", "A360_JWT_SECRET", "A360_DATA_KEY"):
        monkeypatch.delenv(v, raising=False)
    s = Settings(_env_file=None, env="production", jwt_secret="", data_key="")
    problems = " ".join(s.startup_problems())
    for name in ("A360_DATABASE_URL", "A360_JWT_SECRET", "A360_DATA_KEY"):
        assert name in problems
    ok = Settings(_env_file=None, env="production", database_url="postgresql+psycopg://a:b@h/d", jwt_secret="x" * 40,
                  data_key="k")
    assert ok.startup_problems() == []
    assert Settings(_env_file=None, env="development", jwt_secret="", data_key="").startup_problems() == []


def test_database_url_from_environment_counts_as_set(monkeypatch):
    from app.config import Settings
    monkeypatch.setenv("A360_DATABASE_URL", "postgresql+psycopg://a:b@h/d")
    s = Settings(_env_file=None, env="production", jwt_secret="x" * 40, data_key="k")
    assert s.startup_problems() == []
