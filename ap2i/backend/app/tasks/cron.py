"""Minimal 5-field cron matcher (minute hour day month weekday; supports * , - /)."""

from __future__ import annotations

from datetime import datetime, timedelta


def _field(spec: str, lo: int, hi: int) -> set[int]:
    out: set[int] = set()
    for part in spec.split(","):
        step = 1
        if "/" in part:
            part, s = part.split("/")
            step = int(s)
        if part in ("*", ""):
            a, b = lo, hi
        elif "-" in part:
            a, b = (int(x) for x in part.split("-"))
        else:
            a = b = int(part)
        if a < lo or b > hi or a > b:
            raise ValueError(f"cron field out of range: {spec}")
        out.update(range(a, b + 1, step))
    return out


def parse(expr: str):
    f = expr.split()
    if len(f) != 5:
        raise ValueError("cron expression needs 5 fields")
    return (_field(f[0], 0, 59), _field(f[1], 0, 23), _field(f[2], 1, 31), _field(f[3], 1, 12), _field(f[4], 0, 6))


def matches(expr: str, t: datetime) -> bool:
    m, h, d, mo, wd = parse(expr)
    return t.minute in m and t.hour in h and t.day in d and t.month in mo and (t.isoweekday() % 7) in wd


def last_due(expr: str, now: datetime, lookback_minutes: int = 60 * 24 * 8) -> datetime | None:
    """Most recent minute <= now matching expr (searches back up to 8 days)."""
    t = now.replace(second=0, microsecond=0)
    for _ in range(lookback_minutes):
        if matches(expr, t):
            return t
        t -= timedelta(minutes=1)
    return None
