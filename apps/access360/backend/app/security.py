"""Password hashing, session tokens, TOTP and a small login rate limiter."""
from __future__ import annotations

import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
import pyotp

from .config import get_settings

ALGO = "HS256"


def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode()[:72], bcrypt.gensalt(rounds=12)).decode()


def verify_password(pw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode()[:72], hashed.encode())
    except ValueError:
        return False


def password_problems(pw: str) -> list[str]:
    out = []
    if len(pw) < 12:
        out.append("at least 12 characters")
    if pw.lower() == pw or pw.upper() == pw:
        out.append("upper and lower case letters")
    if not any(ch.isdigit() for ch in pw):
        out.append("a digit")
    return out


def make_token(user_id: uuid.UUID, mfa: bool) -> str:
    s = get_settings()
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "mfa": mfa, "iat": now, "exp": now + timedelta(minutes=s.jwt_minutes)},
                      s.secret(), algorithm=ALGO)


def read_token(tok: str) -> dict | None:
    try:
        return jwt.decode(tok, get_settings().secret(), algorithms=[ALGO])
    except jwt.PyJWTError:
        return None


def new_totp_secret() -> str:
    return pyotp.random_base32()


def totp_ok(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)


def totp_uri(secret: str, email: str) -> str:
    return pyotp.TOTP(secret).provisioning_uri(name=email, issuer_name="ACCESS360 AFRICA")


class RateLimiter:
    """Sliding window per key. In memory, so per process; a Redis backed limiter is on the roadmap for multi
    instance deployments (see docs/known-limitations.md)."""

    def __init__(self) -> None:
        self.hits: dict[str, deque] = defaultdict(deque)

    def allow(self, key: str, limit: int, window_s: float = 60.0) -> bool:
        now = time.monotonic()
        q = self.hits[key]
        while q and now - q[0] > window_s:
            q.popleft()
        if len(q) >= limit:
            return False
        q.append(now)
        return True


login_limiter = RateLimiter()
