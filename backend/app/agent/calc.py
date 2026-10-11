"""Bond arithmetic for the agent (CALCULATION). Same formulas as site/simcalc.js, tested against it.

Rates are percent per year, annual coupons, whole years. Every function returns None outside its
domain rather than an infinite or meaningless number.
"""

from __future__ import annotations

import math


def _fin(*v) -> bool:
    return all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in v)


def _ok_yield(y) -> bool:
    return _fin(y) and -100 < y <= 100


def _ok_h(h) -> bool:
    return isinstance(h, int) and not isinstance(h, bool) and 1 <= h <= 50


def price(y: float, c: float, h: int) -> float | None:
    """Price per 100 of nominal of a bond paying an annual coupon c (%) for h years at yield y (%)."""
    if not _ok_yield(y) or not _fin(c) or c < 0 or not _ok_h(h):
        return None
    r = y / 100
    return sum(c / (1 + r) ** t for t in range(1, h + 1)) + 100 / (1 + r) ** h


def hold(amount: float, y: float, coupon: float | None, h: int) -> dict | None:
    """Hold to maturity: buy at the price implied by the published yield, cash every coupon, get the
    nominal back. Without a coupon (bill): simple interest at the published rate over h years."""
    if not _fin(amount) or amount <= 0 or not _ok_yield(y) or not _ok_h(h):
        return None
    if coupon is None:
        gain = amount * y / 100 * h
        return {"kind": "bill", "price": None, "nominal": None, "annual_income": amount * y / 100,
                "coupons": gain, "repaid": amount, "total": amount + gain, "gain": gain}
    p = price(y, coupon, h)
    if p is None or p <= 0:
        return None
    nominal = amount * 100 / p
    annual = nominal * coupon / 100
    out = {"kind": "bond", "price": p, "nominal": nominal, "annual_income": annual, "coupons": annual * h,
           "repaid": nominal, "total": nominal + annual * h, "gain": nominal + annual * h - amount}
    return out if all(v is None or _fin(v) for v in out.values() if not isinstance(v, str)) else None


def reinvested(amount: float, y: float, h: int) -> float | None:
    """Value at the horizon if every coupon is reinvested at the same rate."""
    return amount * (1 + y / 100) ** h if _fin(amount) and amount > 0 and _ok_yield(y) and _ok_h(h) else None


def sensitivity(y: float, coupon: float | None, h: int, d: float = 1.0) -> dict | None:
    """Change in resale value right after purchase if market yields move by d points (exact repricing)."""
    if coupon is None or not _ok_h(h) or h < 2 or not _fin(d):
        return None
    p0, pd, pu = price(y, coupon, h), price(y + d, coupon, h), price(y - d, coupon, h)
    if not p0 or pd is None or pu is None:
        return None
    return {"if_yields_rise": pd / p0 - 1, "if_yields_fall": pu / p0 - 1}


def goal(capital: float, target: float, y: float, h: int) -> dict | None:
    """Monthly saving needed to reach target from capital at a constant rate y (0-40 %) over h years."""
    if not _fin(capital, target, y) or capital < 0 or target <= 0 or not 0 <= y <= 40 or not _ok_h(h):
        return None
    i, n = y / 1200, h * 12
    growth = 0.0 if i < 1e-9 else math.expm1(n * math.log1p(i))
    fv_cap = capital * (1 + growth)
    if fv_cap >= target:
        return {"monthly": 0.0, "months": n, "already_reached": True}
    m = (target - capital) / n if i < 1e-9 else (target - fv_cap) * i / growth
    return {"monthly": m, "months": n, "already_reached": False} if math.isfinite(m) else None
