"""Password hashing, session and password reset tokens, session revocation, TOTP and rate limiting."""
from __future__ import annotations

import hashlib
import hmac
import logging
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
import pyotp

from .config import get_settings

ALGO = "HS256"
log = logging.getLogger("access360.security")


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


# ---------------------------------------------------------------- key derivation and fingerprints

def _derived_key(purpose: str) -> str:
    """A separate signing key per token purpose, so a token of one kind can never be accepted as another."""
    return hmac.new(get_settings().secret().encode(), f"a360:{purpose}".encode(), hashlib.sha256).hexdigest()


def _fingerprint(purpose: str, password_hash: str, n: int = 22) -> str:
    """Keyed fingerprint of the stored password hash. It changes whenever the password changes, which is what makes
    sessions revocable and reset tokens single use without any extra table. It reveals nothing about the hash."""
    return hmac.new(_derived_key(purpose).encode(), password_hash.encode(), hashlib.sha256).hexdigest()[:n]


def session_version(password_hash: str) -> str:
    return _fingerprint("session-version", password_hash, 16)


# ---------------------------------------------------------------- session tokens

def make_token(user_id: uuid.UUID, mfa: bool, password_hash: str) -> str:
    s = get_settings()
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "typ": "session", "mfa": mfa, "sv": session_version(password_hash),
                       "ims": int(time.time() * 1000), "iat": now, "exp": now + timedelta(minutes=s.jwt_minutes)},
                      s.secret(), algorithm=ALGO)


def read_token(tok: str) -> dict | None:
    """Signature, expiry and type only. The caller must also call `session_valid` with the user row."""
    try:
        claims = jwt.decode(tok, get_settings().secret(), algorithms=[ALGO], options={"require": ["exp", "sub"]})
    except jwt.PyJWTError:
        return None
    return claims if claims.get("typ") == "session" else None


def session_valid(claims: dict, user_id: uuid.UUID, password_hash: str) -> bool:
    if not hmac.compare_digest(str(claims.get("sv", "")), session_version(password_hash)):
        return False  # the password changed after this session was issued
    cutoff = revocations().revoked_before(str(user_id))
    return not (cutoff and int(claims.get("ims", 0)) <= cutoff)


# ---------------------------------------------------------------- password reset tokens

RESET_PURPOSE = "password-reset"


def make_reset_token(user_id: uuid.UUID, password_hash: str) -> str:
    s = get_settings()
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "pur": RESET_PURPOSE, "pwf": _fingerprint(RESET_PURPOSE, password_hash),
                       "iat": now, "exp": now + timedelta(minutes=s.reset_token_minutes)},
                      _derived_key(RESET_PURPOSE), algorithm=ALGO)


def read_reset_token(tok: str) -> dict | None:
    try:
        claims = jwt.decode(tok, _derived_key(RESET_PURPOSE), algorithms=[ALGO], options={"require": ["exp", "sub"]})
    except jwt.PyJWTError:
        return None
    return claims if claims.get("pur") == RESET_PURPOSE else None


def reset_token_matches(claims: dict, password_hash: str) -> bool:
    return hmac.compare_digest(str(claims.get("pwf", "")), _fingerprint(RESET_PURPOSE, password_hash))


# ---------------------------------------------------------------- TOTP

def new_totp_secret() -> str:
    return pyotp.random_base32()


def totp_ok(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)


def totp_uri(secret: str, email: str) -> str:
    return pyotp.TOTP(secret).provisioning_uri(name=email, issuer_name="ACCESS360 AFRICA")


# ---------------------------------------------------------------- Redis

_redis_lock = threading.Lock()
_redis_clients: dict[str, object] = {}


def redis_client():
    """Shared Redis client when A360_REDIS_URL is set, else None."""
    url = get_settings().redis_url
    if not url:
        return None
    with _redis_lock:
        if url not in _redis_clients:
            import redis  # imported lazily: only needed when configured
            _redis_clients[url] = redis.Redis.from_url(url, socket_timeout=2, socket_connect_timeout=2)
        return _redis_clients[url]


# ---------------------------------------------------------------- rate limiting

class RateLimiter:
    """Sliding window per key, in memory (per process). Used in development and as the fallback when Redis fails."""

    def __init__(self) -> None:
        self.hits: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, key: str, limit: int, window_s: float = 60.0) -> bool:
        now = time.monotonic()
        with self._lock:
            q = self.hits[key]
            while q and now - q[0] > window_s:
                q.popleft()
            if len(q) >= limit:
                return False
            q.append(now)
            return True


# Atomic sliding window on a sorted set; the Redis server clock is used so instances need not agree on time.
_SLIDING_WINDOW_LUA = """
local t = redis.call('TIME')
local now = tonumber(t[1]) * 1000 + math.floor(tonumber(t[2]) / 1000)
local window = tonumber(ARGV[1])
local limit = tonumber(ARGV[2])
redis.call('ZREMRANGEBYSCORE', KEYS[1], '-inf', now - window)
if redis.call('ZCARD', KEYS[1]) >= limit then
  return 0
end
redis.call('ZADD', KEYS[1], now, now .. '-' .. ARGV[3])
redis.call('PEXPIRE', KEYS[1], window)
return 1
"""


class RedisRateLimiter:
    """Sliding window shared by every API instance. If Redis is unreachable it falls back to the in-memory limiter
    (logged), so an outage degrades to per-process limits rather than blocking all logins."""

    prefix = "a360:rl:"

    def __init__(self, client, fallback: RateLimiter) -> None:
        self.client = client
        self.fallback = fallback
        self._script = client.register_script(_SLIDING_WINDOW_LUA)

    def allow(self, key: str, limit: int, window_s: float = 60.0) -> bool:
        try:
            return bool(self._script(keys=[self.prefix + key], args=[int(window_s * 1000), limit, uuid.uuid4().hex]))
        except Exception as exc:  # redis.exceptions.RedisError and socket errors
            log.error('"redis rate limiter unavailable, using in-memory fallback: %s"', type(exc).__name__)
            return self.fallback.allow(key, limit, window_s)


login_limiter = RateLimiter()  # in-memory instance (kept under its historical name)


def limiter() -> RateLimiter | RedisRateLimiter:
    client = redis_client()
    if client is None:
        return login_limiter
    return RedisRateLimiter(client, login_limiter)


# ---------------------------------------------------------------- session revocation ("log out everywhere")

class MemoryRevocations:
    def __init__(self) -> None:
        self.cutoffs: dict[str, int] = {}

    def revoke_all(self, user_id: str, ttl_s: int) -> None:
        self.cutoffs[user_id] = int(time.time() * 1000)

    def revoked_before(self, user_id: str) -> int | None:
        return self.cutoffs.get(user_id)


class RedisRevocations:
    """Per user cut-off time in Redis; it only needs to live as long as the longest session (A360_JWT_MINUTES)."""

    prefix = "a360:revoked:"

    def __init__(self, client) -> None:
        self.client = client

    def revoke_all(self, user_id: str, ttl_s: int) -> None:
        _memory_revocations.revoke_all(user_id, ttl_s)  # also effective in this process if Redis later fails
        self.client.set(self.prefix + user_id, int(time.time() * 1000), ex=max(ttl_s, 1))

    def revoked_before(self, user_id: str) -> int | None:
        try:
            v = self.client.get(self.prefix + user_id)
        except Exception as exc:
            log.error('"redis revocation lookup failed: %s"', type(exc).__name__)
            return _memory_revocations.revoked_before(user_id)
        return int(v) if v else None


_memory_revocations = MemoryRevocations()


def revocations() -> MemoryRevocations | RedisRevocations:
    client = redis_client()
    return _memory_revocations if client is None else RedisRevocations(client)
