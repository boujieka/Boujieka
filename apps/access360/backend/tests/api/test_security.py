"""Account security: data key encryption helpers (L13), Redis rate limiting (L14), password reset, password change
and session revocation (L15)."""
from __future__ import annotations

import time
import uuid

import pyotp
import pytest
from cryptography.fernet import Fernet, InvalidToken

from .test_api import PW, new_client, register

NEW_PW = "Another-Strong-pass-77"
REDIS_URL = "redis://127.0.0.1:6380/15"


def _redis():
    try:
        import redis
        r = redis.Redis.from_url(REDIS_URL, socket_connect_timeout=1, socket_timeout=1)
        r.ping()
        return r
    except Exception:
        return None


@pytest.fixture()
def settings(db_ready):
    from app.config import get_settings
    return get_settings()


@pytest.fixture()
def outbox():
    from app.services import email
    email.OUTBOX.clear()
    yield email.OUTBOX
    email.OUTBOX.clear()


def _token_from(mail) -> str:
    line = next(ln for ln in mail.body.splitlines() if "/reset-password?token=" in ln)
    return line.split("token=", 1)[1].strip()


def _bearer(tok: str):
    c = new_client()
    c.headers["authorization"] = f"Bearer {tok}"
    return c


# ------------------------------------------------------------------ L13 data key (helpers; column too narrow, see crypto.py)

def test_encrypted_secret_is_not_plaintext_and_totp_still_works(settings, monkeypatch):
    from app import crypto
    monkeypatch.setattr(settings, "data_key", Fernet.generate_key().decode())
    monkeypatch.setattr(settings, "data_keys_old", "")
    secret = pyotp.random_base32()
    stored = crypto.encrypt(secret)
    assert secret not in stored and not crypto.is_legacy_plaintext(stored)
    plain, rewrap = crypto.decrypt(stored)
    assert plain == secret and rewrap is False
    assert pyotp.TOTP(plain).verify(pyotp.TOTP(secret).now())


def test_legacy_plaintext_secret_is_detected_for_migration(settings, monkeypatch):
    from app import crypto
    monkeypatch.setattr(settings, "data_key", Fernet.generate_key().decode())
    secret = pyotp.random_base32()
    plain, rewrap = crypto.decrypt(secret)
    assert plain == secret and rewrap is True
    migrated = crypto.encrypt(plain)
    assert crypto.decrypt(migrated) == (secret, False)


def test_data_key_rotation(settings, monkeypatch):
    from app import crypto
    old, new = Fernet.generate_key().decode(), Fernet.generate_key().decode()
    monkeypatch.setattr(settings, "data_key", old)
    monkeypatch.setattr(settings, "data_keys_old", "")
    stored = crypto.encrypt("JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP")
    monkeypatch.setattr(settings, "data_key", new)
    monkeypatch.setattr(settings, "data_keys_old", old)
    plain, rewrap = crypto.decrypt(stored)
    assert plain == "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP" and rewrap is True
    rewrapped = crypto.encrypt(plain)
    monkeypatch.setattr(settings, "data_keys_old", "")  # old key retired
    assert crypto.decrypt(rewrapped) == (plain, False)
    with pytest.raises(InvalidToken):
        crypto.decrypt(stored)


def test_production_refuses_without_data_key(settings, monkeypatch):
    from app import crypto
    monkeypatch.setattr(settings, "data_key", "")
    monkeypatch.setattr(settings, "env", "production")
    with pytest.raises(RuntimeError):
        crypto.cipher()


def test_mfa_secret_column_too_narrow_for_fernet(settings, monkeypatch):
    """Documents why encryption is not wired yet (L13): when a migration widens the column, this test fails as a
    reminder to wire app/crypto.py into the MFA routes."""
    from app import crypto
    from app.models import User
    monkeypatch.setattr(settings, "data_key", Fernet.generate_key().decode())
    assert User.__table__.c.mfa_secret.type.length == 64
    assert len(crypto.encrypt(pyotp.random_base32())) > 64


# ------------------------------------------------------------------ L14 rate limiting

def test_redis_limiter_blocks_after_n_attempts(db_ready):
    r = _redis()
    if r is None:
        pytest.skip("Redis not reachable on 127.0.0.1:6380")
    from app.security import RateLimiter, RedisRateLimiter
    lim = RedisRateLimiter(r, RateLimiter())
    key = f"test:{uuid.uuid4().hex}"
    assert [lim.allow(key, 3, 60) for _ in range(4)] == [True, True, True, False]
    # a second instance (another API process) shares the same window
    assert RedisRateLimiter(r, RateLimiter()).allow(key, 3, 60) is False
    assert lim.allow(f"test:{uuid.uuid4().hex}", 3, 60) is True


def test_login_rate_limited_through_redis(settings, monkeypatch):
    if _redis() is None:
        pytest.skip("Redis not reachable on 127.0.0.1:6380")
    c = new_client()
    u = register(c)
    monkeypatch.setattr(settings, "redis_url", REDIS_URL)
    monkeypatch.setattr(settings, "login_rate_per_minute", 3)
    codes = [c.post("/api/auth/login", json={"email": u["email"], "password": "Wrong-password-123"}).status_code
             for _ in range(4)]
    assert codes == [401, 401, 401, 429]


def test_memory_limiter_on_password_reset_requests(settings, monkeypatch):
    monkeypatch.setattr(settings, "redis_url", "")
    monkeypatch.setattr(settings, "password_rate_per_minute", 2)
    c = new_client()
    email = f"rl{uuid.uuid4().hex[:8]}@example.com"
    codes = [c.post("/api/auth/password/forgot", json={"email": email}).status_code for _ in range(3)]
    assert codes == [202, 202, 429]


# ------------------------------------------------------------------ L15 password reset

def test_forgot_password_same_answer_for_unknown_email(settings, outbox):
    c = new_client()
    u = register(c)
    known = c.post("/api/auth/password/forgot", json={"email": u["email"]})
    unknown = c.post("/api/auth/password/forgot", json={"email": f"nobody{uuid.uuid4().hex[:8]}@example.com"})
    assert known.status_code == unknown.status_code == 202
    assert known.json() == unknown.json()
    assert "token" not in known.text.lower()
    assert len(outbox) == 1 and outbox[0].to == u["email"]


def test_reset_works_once_and_ends_sessions(settings, outbox):
    c = new_client()
    u = register(c)
    old_session = c.cookies.get("a360_session")
    assert c.post("/api/auth/password/forgot", json={"email": u["email"]}).status_code == 202
    tok = _token_from(outbox[-1])
    anon = new_client()
    r = anon.post("/api/auth/password/reset", json={"token": tok, "new_password": "weakpassword"})
    assert r.status_code == 400  # policy applies; the token is still usable
    r = anon.post("/api/auth/password/reset", json={"token": tok, "new_password": NEW_PW})
    assert r.status_code == 200, r.text
    r = anon.post("/api/auth/password/reset", json={"token": tok, "new_password": "Third-Strong-pass-99"})
    assert r.status_code == 400  # single use: bound to the previous password hash
    assert _bearer(old_session).get("/api/auth/me").status_code == 401
    assert anon.post("/api/auth/login", json={"email": u["email"], "password": PW}).status_code == 401
    assert anon.post("/api/auth/login", json={"email": u["email"], "password": NEW_PW}).status_code == 200


def test_expired_or_forged_reset_token_rejected(settings, monkeypatch, outbox):
    c = new_client()
    u = register(c)
    monkeypatch.setattr(settings, "reset_token_minutes", -1)
    c.post("/api/auth/password/forgot", json={"email": u["email"]})
    expired = _token_from(outbox[-1])
    r = new_client().post("/api/auth/password/reset", json={"token": expired, "new_password": NEW_PW})
    assert r.status_code == 400
    # a session token is not a reset token, and a reset token is not a session
    session_tok = c.cookies.get("a360_session")
    assert new_client().post("/api/auth/password/reset",
                             json={"token": session_tok, "new_password": NEW_PW}).status_code == 400
    monkeypatch.setattr(settings, "reset_token_minutes", 30)
    c.post("/api/auth/password/forgot", json={"email": u["email"]})
    assert _bearer(_token_from(outbox[-1])).get("/api/auth/me").status_code == 401


# ------------------------------------------------------------------ L15 password change and session revocation

def test_password_change_rejects_old_sessions(settings):
    c = new_client()
    u = register(c)
    other_device = _bearer(c.cookies.get("a360_session"))
    assert other_device.get("/api/auth/me").status_code == 200
    r = c.post("/api/auth/password/change", json={"current_password": "Not-the-password-1", "new_password": NEW_PW})
    assert r.status_code == 400
    r = c.post("/api/auth/password/change", json={"current_password": PW, "new_password": NEW_PW})
    assert r.status_code == 200, r.text
    assert other_device.get("/api/auth/me").status_code == 401
    assert c.get("/api/auth/me").status_code == 200  # the changing session got a fresh cookie
    assert new_client().post("/api/auth/login", json={"email": u["email"], "password": NEW_PW}).status_code == 200


@pytest.mark.parametrize("use_redis", [False, True])
def test_logout_all_revokes_every_session(settings, monkeypatch, use_redis):
    if use_redis:
        if _redis() is None:
            pytest.skip("Redis not reachable on 127.0.0.1:6380")
        monkeypatch.setattr(settings, "redis_url", REDIS_URL)
    else:
        monkeypatch.setattr(settings, "redis_url", "")
    c = new_client()
    u = register(c)
    other_device = _bearer(c.cookies.get("a360_session"))
    assert c.post("/api/auth/logout-all").status_code == 200
    assert other_device.get("/api/auth/me").status_code == 401
    time.sleep(0.01)
    d = new_client()
    assert d.post("/api/auth/login", json={"email": u["email"], "password": PW}).status_code == 200
    assert d.get("/api/auth/me").status_code == 200
