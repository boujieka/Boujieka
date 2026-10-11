"""Read-only access to the published data feed (dist/api/v1, built by site/build.py).

The feed is the single source of truth for the agent: the same verified rows the platform shows.
It is read from a local directory when one is given (or found next to the repository), otherwise
from the public site. Nothing here computes or fills in values.
"""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.request
from pathlib import Path
from typing import Any

PUBLIC_FEED = "https://cartouche-africa.netlify.app/api/v1"
LOCAL_FEED = Path(__file__).resolve().parents[3] / "site" / "dist" / "api" / "v1"
FILES = ("index", "data", "summary", "africa", "market", "yield_points", "bvmac", "buyers", "dealers",
         "brief", "reports", "cities")
TTL_SECONDS = 15 * 60  # the feed changes once a day


class FeedError(RuntimeError):
    pass


class Feed:
    """Loads the feed files once and keeps them for TTL_SECONDS (thread-safe)."""

    def __init__(self, source: str | Path | None = None, ttl: float = TTL_SECONDS):
        env = os.environ.get("ABM_FEED")
        chosen = source or env or (LOCAL_FEED if (LOCAL_FEED / "index.json").exists() else PUBLIC_FEED)
        self.source = str(chosen)
        self.ttl = ttl
        self._data: dict[str, Any] | None = None
        self._loaded = 0.0
        self._lock = threading.Lock()

    def _read(self, name: str) -> Any:
        if self.source.startswith(("http://", "https://")):
            url = f"{self.source.rstrip('/')}/{name}.json"
            if not url.startswith("https://"):
                raise FeedError("the feed URL must use https")
            try:
                with urllib.request.urlopen(url, timeout=30) as r:  # noqa: S310 - https only, checked above
                    return json.loads(r.read().decode("utf-8"))
            except (OSError, ValueError) as e:
                raise FeedError(f"feed unavailable: {name}.json ({e})") from e
        path = Path(self.source) / f"{name}.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            raise FeedError(f"feed unavailable: {path} ({e})") from e

    def get(self) -> dict[str, Any]:
        with self._lock:
            if self._data is None or time.monotonic() - self._loaded > self.ttl:
                self._data = {name: self._read(name) for name in FILES}
                self._loaded = time.monotonic()
            return self._data
