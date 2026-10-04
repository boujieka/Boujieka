"""Deterministic financial calculations. Every output here is a CALCULATION.

Conventions
-----------
* Yields and rates are in PERCENT (10 means 10%).
* Prices are per 100 of face value.
* Day-count basis is always an explicit argument. African markets differ
  (e.g. ACT/360 vs ACT/365) and the correct basis for a given market must come
  from that market's official documentation, never from a default here.
* Decimal throughout; floats are never used for money.
* Functions return None when an input is missing rather than guessing.
"""

from decimal import ROUND_HALF_EVEN, Decimal, localcontext

HUNDRED = Decimal(100)
VALID_BASES = (360, 365)


def _check_basis(basis: int) -> None:
    if basis not in VALID_BASES:
        raise ValueError(f"Unsupported day-count basis {basis}; expected one of {VALID_BASES}")


def _check_days(days: int) -> None:
    if days <= 0:
        raise ValueError("days to maturity must be positive")


def bid_to_cover(submitted: Decimal | None, offered: Decimal | None) -> Decimal | None:
    """Total bids received divided by the amount offered.

    Note: some issuers define the ratio against the amount *allocated* instead;
    see `submitted_to_allocated`. The API reports which definition it used.
    """
    if submitted is None or offered is None or offered == 0:
        return None
    return submitted / offered


def submitted_to_allocated(submitted: Decimal | None, allocated: Decimal | None) -> Decimal | None:
    if submitted is None or allocated is None or allocated == 0:
        return None
    return submitted / allocated


def allocation_rate(allocated: Decimal | None, offered: Decimal | None) -> Decimal | None:
    """Share of the offered amount actually raised (can exceed 1 if upsized)."""
    if allocated is None or offered is None or offered == 0:
        return None
    return allocated / offered


def acceptance_rate(allocated: Decimal | None, submitted: Decimal | None) -> Decimal | None:
    """Share of bids received that were accepted."""
    if allocated is None or submitted is None or submitted == 0:
        return None
    return allocated / submitted


def change_bps(current_pct: Decimal | None, previous_pct: Decimal | None) -> Decimal | None:
    """Yield change in basis points (1 bp = 0.01 percentage point)."""
    if current_pct is None or previous_pct is None:
        return None
    return (current_pct - previous_pct) * HUNDRED


def price_from_simple_yield(yield_pct: Decimal, days: int, basis: int) -> Decimal:
    """Price of a zero-coupon bill quoted on a simple-interest (money-market) yield.

    P = 100 / (1 + y * d / B)
    """
    _check_basis(basis)
    _check_days(days)
    with localcontext() as ctx:
        ctx.prec = 34
        return HUNDRED / (1 + (yield_pct / HUNDRED) * Decimal(days) / Decimal(basis))


def simple_yield_from_price(price: Decimal, days: int, basis: int) -> Decimal:
    """Inverse of `price_from_simple_yield`: y = (100/P - 1) * B / d, in percent."""
    _check_basis(basis)
    _check_days(days)
    if price <= 0:
        raise ValueError("price must be positive")
    with localcontext() as ctx:
        ctx.prec = 34
        return (HUNDRED / price - 1) * Decimal(basis) / Decimal(days) * HUNDRED


def price_from_discount_rate(discount_pct: Decimal, days: int, basis: int) -> Decimal:
    """Price of a bill quoted on a bank-discount rate: P = 100 * (1 - dr * d / B)."""
    _check_basis(basis)
    _check_days(days)
    with localcontext() as ctx:
        ctx.prec = 34
        return HUNDRED * (1 - (discount_pct / HUNDRED) * Decimal(days) / Decimal(basis))


def discount_rate_from_price(price: Decimal, days: int, basis: int) -> Decimal:
    """Inverse of `price_from_discount_rate`: dr = (1 - P/100) * B / d, in percent."""
    _check_basis(basis)
    _check_days(days)
    with localcontext() as ctx:
        ctx.prec = 34
        return (1 - price / HUNDRED) * Decimal(basis) / Decimal(days) * HUNDRED


def discount_rate_to_simple_yield(discount_pct: Decimal, days: int, basis: int) -> Decimal:
    """Money-market yield equivalent of a bank-discount rate, same basis."""
    return simple_yield_from_price(price_from_discount_rate(discount_pct, days, basis), days, basis)


def quantize(value: Decimal | None, places: int = 4) -> Decimal | None:
    if value is None:
        return None
    return value.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN)


def mean(values: list[Decimal]) -> Decimal | None:
    if not values:
        return None
    return sum(values, Decimal(0)) / len(values)


def sample_stdev(values: list[Decimal]) -> Decimal | None:
    """Sample standard deviation (n - 1 denominator). None for fewer than two values."""
    if len(values) < 2:
        return None
    m = mean(values)
    with localcontext() as ctx:
        ctx.prec = 34
        return (sum(((v - m) ** 2 for v in values), Decimal(0)) / (len(values) - 1)).sqrt()


def z_score(value: Decimal | None, history: list[Decimal]) -> Decimal | None:
    """How many sample standard deviations `value` sits from the mean of `history`.

    None when the value is missing, history has < 2 points, or history has no dispersion.
    """
    if value is None:
        return None
    sd = sample_stdev(history)
    if sd is None or sd == 0:
        return None
    return (value - mean(history)) / sd


def percentile_rank(value: Decimal | None, history: list[Decimal]) -> Decimal | None:
    """Share of `history` strictly below `value`, plus half the ties, in percent (0–100)."""
    if value is None or not history:
        return None
    below = sum(1 for h in history if h < value)
    ties = sum(1 for h in history if h == value)
    return (Decimal(below) + Decimal(ties) / 2) / len(history) * HUNDRED
