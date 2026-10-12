"""Discounted cash flow helpers (quarterly periods, end of period convention, t = 0 is the first quarter)."""
from __future__ import annotations

import math

import numpy as np


def q_rate(annual: float) -> float:
    return (1.0 + annual) ** 0.25 - 1.0


def npv(rate_q: float, cf: np.ndarray) -> float:
    t = np.arange(1, len(cf) + 1)
    return float(np.sum(cf / (1.0 + rate_q) ** t))


def irr(cf: np.ndarray) -> float | None:
    """Periodic IRR by bracketing and bisection. Returns None when the flows do not change sign or no root exists
    in (-99%, +1000%) per period. Bisection is slow but cannot jump to a spurious root outside the bracket."""
    cf = np.asarray(cf, dtype=float)
    if not (np.any(cf > 0) and np.any(cf < 0)):
        return None

    def f(r: float) -> float:
        return npv(r, cf) * (1.0 + r)  # NPV at t=0 convention, same root

    grid = [-0.99, -0.9, -0.5, -0.2, -0.05, 0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 3.0, 10.0]
    vals = [f(r) for r in grid]
    bracket = None
    # among the sign changes, keep the bracket closest to zero: the economically meaningful root for conventional flows
    for i in range(len(grid) - 1):
        if vals[i] == 0:
            return grid[i]
        if vals[i] * vals[i + 1] < 0:
            cand = (grid[i], grid[i + 1])
            if bracket is None or abs(cand[0]) < abs(bracket[0]):
                bracket = cand
    if bracket is None:
        return None
    lo, hi = bracket
    flo = f(lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo, flo = mid, fm
        if hi - lo < 1e-12:
            break
    return 0.5 * (lo + hi)


def annualise(rq: float | None) -> float | None:
    if rq is None or not math.isfinite(rq):
        return None
    return (1.0 + rq) ** 4 - 1.0


def annuity_payment(principal: float, rate_q: float, n: int) -> float:
    if n <= 0:
        return principal
    if rate_q == 0:
        return principal / n
    return principal * rate_q / (1.0 - (1.0 + rate_q) ** -n)
