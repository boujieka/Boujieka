"""Currency conversion with historical annual rates (Master prompt §16).

Methodology (published on the methodology page):
  * Flows dated in year Y are converted with the ANNUAL AVERAGE rate of year Y from the stored
    source (World Bank WDI PA.NUS.FCRF; IMF ER for SDR). Never today's rate for past flows.
  * Cross rates go through USD: amount_in_quote = amount / (base per USD) * (quote per USD).
  * If a rate for year Y is missing, the conversion is NOT performed (value = None, reason given).
    No interpolation, no substitution with another year.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ExchangeRate

Q = Decimal("0.01")


@dataclass
class Conversion:
    value: Decimal | None
    rate: Decimal | None
    source: str | None
    reason: str | None = None


class FX:
    """Caches rates for one request/computation."""

    def __init__(self, db: Session):
        self.db = db
        self._cache: dict[tuple[str, str], tuple[Decimal, str] | None] = {}

    def _usd_per_unit(self, currency: str, year: int) -> tuple[Decimal, str] | None:
        """How many USD one unit of `currency` was worth on average in `year`."""
        currency = currency.upper()
        if currency == "USD":
            return Decimal(1), "identity"
        key = (currency, str(year))
        if key in self._cache:
            return self._cache[key]
        row = self.db.scalar(select(ExchangeRate).where(ExchangeRate.base_currency == currency, ExchangeRate.quote_currency == "USD",
                                                        ExchangeRate.period == str(year), ExchangeRate.period_type == "annual_avg"))
        result = None
        if row is not None and row.rate:
            result = (Decimal(row.rate), row.source)
        else:
            row = self.db.scalar(select(ExchangeRate).where(ExchangeRate.base_currency == "USD", ExchangeRate.quote_currency == currency,
                                                            ExchangeRate.period == str(year), ExchangeRate.period_type == "annual_avg"))
            if row is not None and row.rate:
                result = (Decimal(1) / Decimal(row.rate), row.source)
        self._cache[key] = result
        return result

    def convert(self, amount: Decimal, from_cur: str, to_cur: str, year: int | None) -> Conversion:
        if from_cur.upper() == to_cur.upper():
            return Conversion(amount, Decimal(1), "identity")
        if year is None:
            return Conversion(None, None, None, "no transaction date: year-specific rate cannot be chosen")
        a = self._usd_per_unit(from_cur, year)
        b = self._usd_per_unit(to_cur, year)
        if a is None or b is None:
            missing = from_cur if a is None else to_cur
            return Conversion(None, None, None, f"no {year} annual average rate stored for {missing}")
        rate = a[0] / b[0]
        sources = sorted({s for s in (a[1], b[1]) if s != "identity"})
        return Conversion((amount * rate).quantize(Q, rounding=ROUND_HALF_EVEN), rate, "; ".join(sources))
