"""Login throttling and request-size guard.

The limiter is in memory and per process: run a single worker or put a shared
limiter (reverse proxy, Redis) in front for multi-instance deployments."""
from __future__ import annotations

import time
from collections import OrderedDict, deque

from fastapi import HTTPException, Request, status

from .config import get_settings


class SlidingWindow:
    def __init__(self, max_keys: int = 100_000):
        self.hits: OrderedDict[str, deque] = OrderedDict()
        self.max_keys = max_keys

    def hit(self, key: str, limit: int, window: float = 60.0) -> None:
        now = time.monotonic()
        q = self.hits.pop(key, deque())
        while q and now - q[0] > window:
            q.popleft()
        if len(q) >= limit:
            self.hits[key] = q
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "too many login attempts, retry in a minute")
        q.append(now)
        self.hits[key] = q
        while len(self.hits) > self.max_keys:   # bounded memory
            self.hits.popitem(last=False)


_window = SlidingWindow()


def client_ip(request: Request) -> str:
    if get_settings().trusted_proxy:
        fwd = request.headers.get("x-forwarded-for", "")
        if fwd:
            return fwd.split(",")[0].strip()
    return request.client.host if request.client else "?"


def throttle_login(request: Request, email: str) -> str:
    s = get_settings()
    ip = client_ip(request)
    _window.hit(f"ip:{ip}", s.login_attempts_per_ip_minute)
    _window.hit(f"acct:{email.lower()}", s.login_attempts_per_minute)
    return ip


def throttle_ip(request: Request) -> str:
    """Per-IP limit only, for endpoints keyed by a secret token rather than an account."""
    ip = client_ip(request)
    _window.hit(f"ip:{ip}", get_settings().login_attempts_per_ip_minute)
    return ip
