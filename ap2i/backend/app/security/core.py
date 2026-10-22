"""Authentication primitives: Argon2 password hashing, JWT access tokens, TOTP MFA, one-time tokens."""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt
import pyotp
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from app.config import get_settings

_ph = PasswordHasher()
ALGORITHM = "HS256"
COMMON_PASSWORDS = {"password", "password123", "123456789012", "motdepasse123", "azertyuiop12", "qwertyuiop12",
                    "cameroun2024!", "admin1234567"}


def hash_password(password: str) -> str:
    return _ph.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _ph.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def password_problems(password: str, email: str | None = None) -> list[str]:
    s = get_settings()
    problems = []
    if len(password) < s.password_min_length:
        problems.append(f"at least {s.password_min_length} characters")
    if password.lower() in COMMON_PASSWORDS:
        problems.append("too common")
    if email and email.split("@")[0].lower() in password.lower():
        problems.append("must not contain the email name")
    classes = sum([any(c.islower() for c in password), any(c.isupper() for c in password),
                   any(c.isdigit() for c in password), any(not c.isalnum() for c in password)])
    if classes < 3:
        problems.append("use at least 3 of: lowercase, uppercase, digit, symbol")
    return problems


def create_access_token(user_id: int, token_version: int, mfa: bool, extra: dict | None = None) -> str:
    s = get_settings()
    now = datetime.now(timezone.utc)
    payload = {"sub": str(user_id), "tv": token_version, "mfa": mfa, "iat": now,
               "exp": now + timedelta(minutes=s.access_token_minutes), "typ": "access", **(extra or {})}
    return jwt.encode(payload, s.secret_key, algorithm=ALGORITHM)


def create_mfa_challenge(user_id: int) -> str:
    s = get_settings()
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "typ": "mfa_challenge", "iat": now, "exp": now + timedelta(minutes=5)},
                      s.secret_key, algorithm=ALGORITHM)


def decode_token(token: str, expected_type: str = "access") -> dict:
    payload = jwt.decode(token, get_settings().secret_key, algorithms=[ALGORITHM])
    if payload.get("typ") != expected_type:
        raise jwt.InvalidTokenError("wrong token type")
    return payload


def new_totp_secret() -> str:
    return pyotp.random_base32()


def totp_uri(secret: str, email: str) -> str:
    return pyotp.TOTP(secret).provisioning_uri(name=email, issuer_name="AP2I")


def verify_totp(secret: str, code: str) -> bool:
    return bool(secret) and pyotp.TOTP(secret).verify(code.strip(), valid_window=1)


def new_one_time_token() -> tuple[str, str]:
    raw = secrets.token_urlsafe(32)
    return raw, sha256(raw)


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def new_api_key() -> tuple[str, str, str]:
    raw = "ap2i_" + secrets.token_urlsafe(32)
    return raw, raw[:12], sha256(raw)
