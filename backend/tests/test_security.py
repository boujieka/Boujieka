"""Phase 1b: API keys, roles, rate limiting, audit log, security headers, CORS."""

import hashlib
import uuid

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.db import get_session
from app.main import create_app
from app.models import ApiKey, AuditLog
from app.models.enums import Role
from app.security import keys as keys_module
from app.security.audit import truncate_ip
from app.security.keys import authenticate, create_key, hash_key, revoke_key
from app.security.ratelimit import SlidingWindowLimiter

API = "/api/v1"
AS_OF = "2026-10-03"


def audit_rows(engine, request_id: str) -> list[AuditLog]:
    with Session(engine) as s:
        return list(s.scalars(select(AuditLog).where(AuditLog.request_id == request_id)))


def new_key(engine, role: Role, revoked: bool = False) -> tuple[int, str]:
    with Session(engine) as s:
        key, plaintext = create_key(s, f"t-{uuid.uuid4().hex[:8]}", role)
        if revoked:
            revoke_key(s, key.id)
        s.commit()
        return key.id, plaintext


def rid() -> str:
    return f"test-{uuid.uuid4().hex}"


class TestKeys:
    def test_only_the_sha256_hash_is_stored(self, db):
        key, plaintext = create_key(db, "ops", Role.ADMIN)
        assert plaintext.startswith("cart_") and len(plaintext) > 40
        assert key.key_hash == hashlib.sha256(plaintext.encode()).hexdigest() == hash_key(plaintext)
        stored = db.execute(select(ApiKey.__table__).where(ApiKey.id == key.id)).one()
        assert plaintext not in {str(v) for v in stored}

    def test_authenticate_and_revoke(self, db):
        key, plaintext = create_key(db, "analyst", Role.ANALYST)
        assert authenticate(db, plaintext).id == key.id
        assert key.last_used_at is not None
        assert authenticate(db, plaintext + "x") is None
        assert authenticate(db, "") is None
        revoke_key(db, key.id)
        assert authenticate(db, plaintext) is None

    def test_public_is_not_a_key_role(self, db):
        with pytest.raises(ValueError):
            create_key(db, "nope", Role.PUBLIC)

    def test_cli_prints_key_once_and_never_lists_secrets(self, seeded, monkeypatch, capsys):
        monkeypatch.setattr("app.db.SessionLocal", sessionmaker(bind=seeded, expire_on_commit=False))
        keys_module.main(["create", "--name", "cli-test", "--role", "analyst"])
        plaintext = capsys.readouterr().out.strip().splitlines()[-1]
        assert plaintext.startswith("cart_")
        with Session(seeded) as s:
            key = s.scalar(select(ApiKey).where(ApiKey.key_hash == hash_key(plaintext)))
            assert key is not None and key.role == Role.ANALYST

        keys_module.main(["list"])
        listing = capsys.readouterr().out
        assert "cli-test" in listing
        assert plaintext not in listing and key.key_hash not in listing

        keys_module.main(["revoke", "--id", str(key.id)])
        assert "Revoked" in capsys.readouterr().out
        with Session(seeded) as s:
            assert s.get(ApiKey, key.id).revoked_at is not None


class TestRoles:
    def test_public_endpoints_need_no_key(self, client):
        for path in ("/health", "/dashboard/summary", "/countries", "/countries/KEN", "/sources",
                     "/auctions", "/opportunities", "/market/heat-grid", "/subscription-routes"):
            assert client.get(f"{API}{path}", params={"as_of": AS_OF}).status_code == 200, path

    def test_data_quality_requires_a_key(self, client):
        r = client.get(f"{API}/data-quality")
        assert r.status_code == 401
        assert r.headers["WWW-Authenticate"] == "X-API-Key"

    def test_data_quality_allows_analyst_and_admin(self, client, analyst_headers, admin_headers):
        for headers in (analyst_headers, admin_headers):
            assert client.get(f"{API}/data-quality", headers=headers).status_code == 200

    def test_unknown_key_is_401_everywhere(self, client):
        bogus = "cart_" + "A" * 43
        for path in ("/data-quality", "/health"):
            r = client.get(f"{API}{path}", headers={"X-API-Key": bogus})
            assert r.status_code == 401
            assert bogus not in r.text and bogus not in str(r.headers)

    def test_revoked_key_is_401(self, client, seeded):
        _, plaintext = new_key(seeded, Role.ADMIN, revoked=True)
        assert client.get(f"{API}/data-quality", headers={"X-API-Key": plaintext}).status_code == 401

    def test_insufficient_role_is_403(self, client, analyst_headers):
        assert client.get(f"{API}/admin/audit-log", headers=analyst_headers).status_code == 403
        assert client.get(f"{API}/admin/audit-log").status_code == 401


class TestAudit:
    def test_protected_request_is_audited_without_query_string(self, client, seeded, api_keys, analyst_headers):
        request_id = rid()
        r = client.get(
            f"{API}/data-quality",
            params={"as_of": AS_OF, "token": "s3cret-in-query"},
            headers={**analyst_headers, "X-Request-ID": request_id},
        )
        assert r.status_code == 200 and r.headers["X-Request-ID"] == request_id
        [row] = audit_rows(seeded, request_id)
        with Session(seeded) as s:
            key_id = s.scalar(select(ApiKey.id).where(ApiKey.key_hash == hash_key(api_keys[Role.ANALYST])))
        assert (row.api_key_id, row.role, row.method, row.status_code) == (key_id, Role.ANALYST, "GET", 200)
        assert row.path == "/api/v1/data-quality"
        assert row.client_ip == "testclient"

    @pytest.mark.parametrize(
        ("path", "headers", "status"),
        [
            ("/data-quality", {}, 401),
            ("/health", {"X-API-Key": "cart_wrong"}, 401),
            ("/admin/audit-log", "analyst", 403),
        ],
    )
    def test_auth_failures_are_audited(self, client, seeded, analyst_headers, path, headers, status):
        request_id = rid()
        headers = analyst_headers if headers == "analyst" else headers
        assert client.get(f"{API}{path}", headers={**headers, "X-Request-ID": request_id}).status_code == status
        [row] = audit_rows(seeded, request_id)
        assert row.status_code == status

    def test_public_requests_are_not_audited(self, client, seeded):
        request_id = rid()
        client.get(f"{API}/health", headers={"X-Request-ID": request_id})
        assert audit_rows(seeded, request_id) == []

    def test_malformed_request_id_is_replaced(self, client):
        r = client.get(f"{API}/health", headers={"X-Request-ID": "bad id\twith spaces"})
        assert r.headers["X-Request-ID"] != "bad id\twith spaces"

    def test_admin_audit_log_endpoint_leaks_no_secret(self, client, seeded, api_keys, admin_headers):
        client.get(f"{API}/data-quality", headers=admin_headers)
        r = client.get(f"{API}/admin/audit-log", params={"limit": 5}, headers=admin_headers)
        assert r.status_code == 200
        rows = r.json()
        assert 1 <= len(rows) <= 5
        assert [x["id"] for x in rows] == sorted((x["id"] for x in rows), reverse=True)
        assert set(rows[0]) == {"id", "at", "api_key_id", "role", "method", "path", "status_code",
                                "client_ip", "request_id"}
        for plaintext in api_keys.values():
            assert plaintext not in r.text and hash_key(plaintext) not in r.text

    def test_limit_is_validated(self, client, admin_headers):
        assert client.get(f"{API}/admin/audit-log", params={"limit": 0}, headers=admin_headers).status_code == 422

    def test_ip_truncation(self):
        assert truncate_ip("203.0.113.77") == "203.0.113.0/24"
        assert truncate_ip("2001:db8:abcd:12::1") == "2001:db8:abcd::/48"
        assert truncate_ip(None) is None


class TestRateLimit:
    @pytest.fixture
    def limited(self, seeded):
        """A separate app with the limiter active for TestClient (not exempt) and tiny limits."""
        settings = Settings(
            rate_limit_enabled=True, rate_limit_per_minute=3, rate_limit_per_minute_key=5,
            rate_limit_exempt_hosts=[],
        )
        factory = sessionmaker(bind=seeded, expire_on_commit=False)

        def override():
            with factory() as s:
                yield s

        app = create_app(settings)
        app.dependency_overrides[get_session] = override
        with TestClient(app) as c:
            yield c

    def test_public_limit_returns_429_with_retry_after(self, limited, seeded):
        for _ in range(3):
            assert limited.get(f"{API}/health").status_code == 200
        request_id = rid()
        r = limited.get(f"{API}/health", headers={"X-Request-ID": request_id})
        assert r.status_code == 429
        assert 1 <= int(r.headers["Retry-After"]) <= 60
        assert r.headers["X-Content-Type-Options"] == "nosniff"
        [row] = audit_rows(seeded, request_id)
        assert row.status_code == 429 and row.role == Role.PUBLIC

    def test_keys_have_their_own_higher_budget(self, limited, seeded):
        _, plaintext = new_key(seeded, Role.ANALYST)
        for _ in range(3):
            limited.get(f"{API}/health")
        assert limited.get(f"{API}/health").status_code == 429
        statuses = [limited.get(f"{API}/health", headers={"X-API-Key": plaintext}).status_code for _ in range(6)]
        assert statuses == [200] * 5 + [429]

    def test_testclient_is_exempt_by_default(self, client):
        """site/build.py and the tests call the API in bursts through TestClient."""
        assert Settings().rate_limit_exempt_hosts == ["testclient"]
        assert all(client.get(f"{API}/health").status_code == 200 for _ in range(150))

    def test_sliding_window(self):
        now = [0.0]
        limiter = SlidingWindowLimiter(window=60, clock=lambda: now[0])
        assert limiter.hit("a", 2) is None and limiter.hit("a", 2) is None
        assert limiter.hit("a", 2) == pytest.approx(60)
        assert limiter.hit("b", 2) is None  # Clients are independent.
        now[0] = 30
        assert limiter.hit("a", 2) == pytest.approx(30)
        now[0] = 60.5
        assert limiter.hit("a", 2) is None


class TestHeadersAndCors:
    def test_security_headers(self, client):
        r = client.get(f"{API}/health")
        assert r.headers["X-Frame-Options"] == "DENY"
        assert r.headers["Referrer-Policy"] == "no-referrer"
        assert r.headers["X-Content-Type-Options"] == "nosniff"
        assert "default-src 'none'" in r.headers["Content-Security-Policy"]
        assert "server" not in {h.lower() for h in r.headers}

    def test_cors_allows_only_configured_origins(self, client):
        ok = client.get(f"{API}/health", headers={"Origin": "http://localhost:3000"})
        assert ok.headers["access-control-allow-origin"] == "http://localhost:3000"
        bad = client.get(f"{API}/health", headers={"Origin": "https://evil.example"})
        assert "access-control-allow-origin" not in bad.headers

    def test_wildcard_origin_is_refused(self):
        with pytest.raises(ValidationError):
            Settings(cors_origins=["*"])
