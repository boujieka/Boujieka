"""Excel semantics the reference workbook relies on, reproduced exactly.

Every function documents the Excel behaviour it mirrors. Nothing here is an
approximation of a financial formula: these are the building blocks the
workbook's formulas are made of (dates, rounding, LOOKUP, IRR family).
"""
from __future__ import annotations

import calendar
import datetime as _dt
import math
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_UP, Decimal
from typing import Iterable, Sequence

# --------------------------------------------------------------------------- dates
# Excel's 1900 date system: serial 1 = 1900-01-01, serial 60 = the fictitious
# 1900-02-29, serial 61 = 1900-03-01. For serials >= 61 the epoch 1899-12-30 is exact.
_EPOCH = _dt.date(1899, 12, 30)


def to_serial(d: _dt.date) -> int:
    if d < _dt.date(1900, 3, 1):
        raise ValueError("dates before 1900-03-01 are not supported")
    return (d - _EPOCH).days


def _ymd(serial: float) -> tuple[int, int, int]:
    """Year, month, day of an Excel serial, including Excel's 1900 quirks
    (serial 0 is 1900-01-00, serial 60 is 1900-02-29)."""
    s = int(math.floor(serial))
    if s >= 61:
        d = _EPOCH + _dt.timedelta(days=s)
        return d.year, d.month, d.day
    if s == 60:
        return 1900, 2, 29
    if s == 0:
        return 1900, 1, 0
    if 1 <= s < 60:
        d = _dt.date(1899, 12, 31) + _dt.timedelta(days=s)
        return d.year, d.month, d.day
    raise ValueError(f"negative date serial {serial}")


def from_serial(serial: float) -> _dt.date:
    y, m, d = _ymd(serial)
    if d == 0 or (y, m, d) == (1900, 2, 29):
        raise ValueError(f"serial {serial} has no calendar date")
    return _dt.date(y, m, d)


def eomonth(serial: float, months: float) -> int:
    """EOMONTH(start, months): last day of the month `months` after start
    (months truncated toward zero, as Excel does)."""
    y, m, _ = _ymd(serial)
    total = (y * 12 + (m - 1)) + int(months)
    ny, nm = divmod(total, 12)
    nm += 1
    last = calendar.monthrange(ny, nm)[1]
    return to_serial(_dt.date(ny, nm, last))


def year(serial: float) -> int:
    return _ymd(serial)[0]


# ------------------------------------------------------------------------ rounding
def _dec(x: float) -> Decimal:
    # Excel works on 15 significant digits: 2.675 rounds to 2.68, not 2.67.
    return Decimal(repr(float(f"{x:.15g}")))


def xround(x: float, digits: int = 0) -> float:
    """ROUND: half away from zero (never banker's rounding)."""
    q = Decimal(1).scaleb(-digits)
    d = _dec(x)
    r = abs(d).quantize(q, rounding=ROUND_HALF_UP) if digits >= 0 else \
        (abs(d) / q).quantize(Decimal(1), rounding=ROUND_HALF_UP) * q
    return float(r if d >= 0 else -r)


def roundup(x: float, digits: int = 0) -> float:
    """ROUNDUP: away from zero."""
    q = Decimal(1).scaleb(-digits)
    d = _dec(x)
    r = (abs(d) / q).quantize(Decimal(1), rounding=ROUND_CEILING) * q
    return float(r if d >= 0 else -r)


def rounddown(x: float, digits: int = 0) -> float:
    """ROUNDDOWN: toward zero."""
    q = Decimal(1).scaleb(-digits)
    d = _dec(x)
    r = (abs(d) / q).quantize(Decimal(1), rounding=ROUND_DOWN) * q
    return float(r if d >= 0 else -r)


# -------------------------------------------------------------------------- lookup
class ExcelNA(ValueError):
    """#N/A: the workbook would show an error in this cell."""


def lookup(value: float, keys: Sequence, results: Sequence, numeric_only: bool = True):
    """LOOKUP(value, lookup_vector, result_vector), approximate match on an
    ascending vector: the last key <= value. Text keys are skipped when the
    lookup value is a number (Excel compares numbers and text as different
    types; the base-rate table Inputs!I406:K406 mixes 2021, 2022 and "2023+").
    """
    best = None
    for i, k in enumerate(keys):
        if k is None:
            continue
        if numeric_only and isinstance(k, str):
            continue
        if k <= value:
            best = i
        else:
            break
    if best is None:
        raise ExcelNA(f"LOOKUP({value}) below first key {keys[0]!r}")
    return results[best]


def lookup_text(value: str, keys: Sequence[str], results: Sequence):
    """LOOKUP on an alphabetically sorted text vector (exact names in this workbook)."""
    best = None
    for i, k in enumerate(keys):
        if k.lower() <= value.lower():
            best = i
    if best is None:
        raise ExcelNA(value)
    return results[best]


# ---------------------------------------------------------------- aggregate helpers
def average_nonzero(values: Iterable[float]) -> float:
    """AVERAGEIF(range, "<>0")."""
    v = [x for x in values if x != 0]
    if not v:
        raise ZeroDivisionError("AVERAGEIF: no non-zero value (#DIV/0!)")
    return sum(v) / len(v)


def npv(rate: float, values: Sequence[float]) -> float:
    """NPV: first value discounted one full period."""
    return sum(v / (1 + rate) ** (i + 1) for i, v in enumerate(values))


def xnpv(rate: float, values: Sequence[float], dates: Sequence[float]) -> float:
    d0 = dates[0]
    return sum(v / (1 + rate) ** ((d - d0) / 365.0) for v, d in zip(values, dates))


def _safe(f):
    def g(x):
        try:
            y = f(x)
        except (ZeroDivisionError, OverflowError):
            return math.nan
        return y if math.isfinite(y) else math.nan
    return g


def _solve(f, lo: float, hi: float, guess: float) -> float:
    """Newton from Excel's default guess, falling back to bisection on a bracket.
    The lower bound is raised until the function is finite (rates close to
    -100 % overflow over long horizons)."""
    f = _safe(f)
    for cand in (lo, -0.99999, -0.9999, -0.999, -0.99, -0.95, -0.9):
        if cand >= lo and not math.isnan(f(cand)):
            lo = cand
            break
    x = guess
    for _ in range(100):
        fx = f(x)
        h = 1e-7 * max(1.0, abs(x))
        d = (f(x + h) - fx) / h
        if math.isnan(fx) or d == 0 or not math.isfinite(d):
            break
        nx = x - fx / d
        if not (lo < nx < hi):
            break
        if abs(nx - x) < 1e-12:
            return nx
        x = nx
    a, b = lo, hi
    fa, fb = f(a), f(b)
    if math.isnan(fa) or math.isnan(fb) or fa * fb > 0:
        raise ArithmeticError("no sign change: #NUM!")
    for _ in range(300):
        m = (a + b) / 2
        fm = f(m)
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
        if b - a < 1e-15:
            break
    return (a + b) / 2


def xirr(values: Sequence[float], dates: Sequence[float], guess: float = 0.1) -> float:
    if not (any(v > 0 for v in values) and any(v < 0 for v in values)):
        raise ArithmeticError("XIRR needs positive and negative flows: #NUM!")
    return _solve(lambda r: xnpv(r, values, dates), -0.999999, 1e3, guess)


def irr(values: Sequence[float], guess: float = 0.1) -> float:
    if not (any(v > 0 for v in values) and any(v < 0 for v in values)):
        raise ArithmeticError("IRR needs positive and negative flows: #NUM!")
    f = lambda r: sum(v / (1 + r) ** i for i, v in enumerate(values))  # noqa: E731
    return _solve(f, -0.999999, 1e3, guess)


def iferror(fn, fallback=0.0):
    try:
        v = fn()
        if isinstance(v, float) and not math.isfinite(v):
            return fallback
        return v
    except (ArithmeticError, ValueError, ZeroDivisionError):
        return fallback
