"""Small, dependency-free financial helpers shared by the engines."""

from __future__ import annotations

from collections.abc import Sequence


def crf(rate: float, years: float) -> float:
    """Capital recovery factor: converts a present value into an equal annual annuity."""
    if years <= 0:
        raise ValueError("years must be positive")
    if abs(rate) < 1e-12:
        return 1.0 / years
    return rate * (1 + rate) ** years / ((1 + rate) ** years - 1)


def present_value(values: Sequence[float], rate: float, start_period: int = 1) -> float:
    """PV of ``values`` where values[0] occurs at period ``start_period`` (end-of-period convention)."""
    return float(sum(v / (1 + rate) ** (i + start_period) for i, v in enumerate(values)))


def levelized_cost(costs: Sequence[float], energy: Sequence[float], rate: float, start_period: int = 0) -> float:
    """Standard levelised cost: PV(costs) / PV(energy), both discounted with the same rate."""
    pv_e = present_value(energy, rate, start_period)
    if pv_e <= 0:
        return float("nan")
    return present_value(costs, rate, start_period) / pv_e
