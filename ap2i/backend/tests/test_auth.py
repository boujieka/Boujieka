import re

import pyotp
from conftest import make_user, token_for
from sqlalchemy import select

import app.models as m
from app.security.email import OUTBOX


def _token_from_outbox(kind: str) -> str:
    msg = next(x for x in reversed(OUTBOX) if kind in x["body"])
    return re.search(r"token=([\w\-]+)", msg["body"]).group(1)


def test_register_verify_login_flow(client, db):
    r = client.post("/api/v1/auth/register", json={"email": "ana@example.org", "password": "Weak", "full_name": "Ana"})
    assert r.status_code == 422
    r = client.post("/api/v1/auth/register", json={"email": "ana@example.org", "password": "C0rrect-Horse-Battery", "full_name": "Ana Test"})
    assert r.status_code == 201
    assert client.post("/api/v1/auth/login", json={"email": "ana@example.org", "password": "C0rrect-Horse-Battery"}).status_code == 403
    assert client.post("/api/v1/auth/verify-email", json={"token": _token_from_outbox("verify-email")}).status_code == 200
    r = client.post("/api/v1/auth/login", json={"email": "ana@example.org", "password": "C0rrect-Horse-Battery"})
    assert r.status_code == 200
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {r.json()['access_token']}"}).json()
    assert me["email"] == "ana@example.org" and me["roles"] == ["registered_user"]
    stored = db.scalar(select(m.User).where(m.User.email == "ana@example.org"))
    assert stored.password_hash.startswith("$argon2")
    # token stored hashed only
    assert all(len(t.token_hash) == 64 for t in db.scalars(select(m.UserToken)))


def test_duplicate_registration_does_not_reveal_account(client, db):
    make_user(db, "bob@example.org", ["registered_user"])
    r = client.post("/api/v1/auth/register", json={"email": "bob@example.org", "password": "C0rrect-Horse-Battery", "full_name": "Bob"})
    assert r.status_code == 201 and r.json() == {"status": "verification_sent"}


def test_lockout_after_failed_logins(client, db):
    make_user(db, "eve@example.org", ["registered_user"])
    for _ in range(5):
        assert client.post("/api/v1/auth/login", json={"email": "eve@example.org", "password": "wrong"}).status_code == 401
    assert client.post("/api/v1/auth/login", json={"email": "eve@example.org", "password": "Str0ng!Passw0rd#"}).status_code == 423


def test_mfa_flow(client, db):
    make_user(db, "mfa@example.org", ["registered_user"])
    h = token_for(client, "mfa@example.org")
    secret = client.post("/api/v1/auth/mfa/setup", headers=h).json()["secret"]
    assert client.post("/api/v1/auth/mfa/enable", headers=h, json={"code": "000000"}).status_code == 400
    assert client.post("/api/v1/auth/mfa/enable", headers=h, json={"code": pyotp.TOTP(secret).now()}).status_code == 200
    assert client.get("/api/v1/auth/me", headers=h).status_code == 401  # old session revoked
    r = client.post("/api/v1/auth/login", json={"email": "mfa@example.org", "password": "Str0ng!Passw0rd#"}).json()
    assert r["mfa_required"] and "access_token" not in r
    assert client.post("/api/v1/auth/login/mfa", json={"challenge": r["challenge"], "code": "123456"}).status_code == 401
    ok = client.post("/api/v1/auth/login/mfa", json={"challenge": r["challenge"], "code": pyotp.TOTP(secret).now()})
    assert ok.status_code == 200
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {ok.json()['access_token']}"}).json()["mfa_enabled"]


def test_password_reset(client, db):
    make_user(db, "rst@example.org", ["registered_user"])
    old = token_for(client, "rst@example.org")
    assert client.post("/api/v1/auth/password/forgot", json={"email": "rst@example.org"}).status_code == 200
    assert client.post("/api/v1/auth/password/forgot", json={"email": "nobody@example.org"}).json()["status"].startswith("if_the_account")
    tok = _token_from_outbox("reset-password")
    assert client.post("/api/v1/auth/password/reset", json={"token": tok, "new_password": "N3w-Secure-Passphrase"}).status_code == 200
    assert client.post("/api/v1/auth/password/reset", json={"token": tok, "new_password": "N3w-Secure-Passphrase2"}).status_code == 400
    assert client.get("/api/v1/auth/me", headers=old).status_code == 401
    token_for(client, "rst@example.org", "N3w-Secure-Passphrase")


def test_invalid_token_rejected(client):
    assert client.get("/api/v1/auth/me", headers={"Authorization": "Bearer abc"}).status_code == 401
    assert client.get("/api/v1/auth/me").status_code == 401


def test_audit_log_written(client, db):
    make_user(db, "aud@example.org", ["registered_user"])
    token_for(client, "aud@example.org")
    assert db.scalar(select(m.AuditLog).where(m.AuditLog.action == "auth.login")) is not None


def test_login_accepts_internal_domain_accounts(client, db):
    make_user(db, "admin@ap2i.local", ["ap2i_super_admin"])
    token_for(client, "admin@ap2i.local")
