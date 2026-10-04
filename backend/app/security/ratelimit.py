"""In-memory sliding-window rate limiter.

State lives in this process only: with several workers or instances each one
counts separately, so the effective limit is multiplied by the process count.
A Redis-backed limiter is the production step (docs/SECURITY.md).
"""

import math
import threading
import time
from collections import deque
from collections.abc import Callable

WINDOW_SECONDS = 60.0
_SWEEP_EVERY = 1000  # Drop idle clients every N checks so memory stays bounded.


class SlidingWindowLimiter:
    def __init__(self, window: float = WINDOW_SECONDS, clock: Callable[[], float] = time.monotonic):
        self.window = window
        self.clock = clock
        self._hits: dict[str, deque[float]] = {}
        self._lock = threading.Lock()
        self._checks = 0

    def hit(self, client: str, limit: int) -> float | None:
        """Record a request. Return None if allowed, else seconds until the next slot frees."""
        now = self.clock()
        with self._lock:
            self._checks += 1
            if self._checks % _SWEEP_EVERY == 0:
                self._sweep(now)
            hits = self._hits.setdefault(client, deque())
            while hits and hits[0] <= now - self.window:
                hits.popleft()
            if len(hits) >= limit:
                return max(hits[0] + self.window - now, 0.0)
            hits.append(now)
            return None

    def _sweep(self, now: float) -> None:
        for client in [c for c, h in self._hits.items() if not h or h[-1] <= now - self.window]:
            del self._hits[client]


def retry_after_header(seconds: float) -> str:
    return str(max(1, math.ceil(seconds)))
