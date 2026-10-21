"""Currency handling with user-configured exchange rates.

Policy: the platform never invents a market exchange rate. The only built-in value is the
*legally fixed* parity between the euro and the Central African CFA franc (XAF):
1 EUR = 655.957 XAF (fixed parity since the euro's introduction in 1999). Every other rate,
including USD, must be entered by the user, with its date and source. Conversion with a missing
rate raises :class:`MissingExchangeRateError` instead of silently guessing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

SUPPORTED_CURRENCIES = ("XAF", "USD", "EUR")
XAF_PER_EUR_FIXED_PARITY = 655.957


class MissingExchangeRateError(ValueError):
    """Raised when a conversion needs a rate the user has not configured."""


@dataclass
class ExchangeRates:
    """Rates expressed as *XAF per one unit* of each currency."""

    xaf_per_unit: dict[str, float] = field(
        default_factory=lambda: {"XAF": 1.0, "EUR": XAF_PER_EUR_FIXED_PARITY}
    )
    as_of: dict[str, str] = field(default_factory=lambda: {"EUR": "fixed parity"})
    source: dict[str, str] = field(
        default_factory=lambda: {"EUR": "EUR/XAF fixed parity (BEAC / CEMAC monetary arrangement)"}
    )

    def set_rate(self, currency: str, xaf_per_unit: float, as_of: date | str, source: str) -> None:
        currency = currency.upper()
        if currency not in SUPPORTED_CURRENCIES:
            raise ValueError(f"Unsupported currency: {currency}")
        if currency == "XAF":
            raise ValueError("XAF is the base currency; its rate is always 1.")
        if not xaf_per_unit or xaf_per_unit <= 0:
            raise ValueError("Exchange rate must be strictly positive.")
        if not source:
            raise ValueError("An exchange-rate source must be documented.")
        self.xaf_per_unit[currency] = float(xaf_per_unit)
        self.as_of[currency] = str(as_of)
        self.source[currency] = source

    def has(self, currency: str) -> bool:
        return currency.upper() in self.xaf_per_unit

    def convert(self, amount: float, from_ccy: str, to_ccy: str) -> float:
        from_ccy, to_ccy = from_ccy.upper(), to_ccy.upper()
        if from_ccy == to_ccy:
            return float(amount)
        for ccy in (from_ccy, to_ccy):
            if ccy not in SUPPORTED_CURRENCIES:
                raise ValueError(f"Unsupported currency: {ccy}")
            if ccy not in self.xaf_per_unit:
                raise MissingExchangeRateError(
                    f"No exchange rate configured for {ccy}. Enter it (with date and source) in Settings."
                )
        return float(amount) * self.xaf_per_unit[from_ccy] / self.xaf_per_unit[to_ccy]

    def to_dict(self) -> dict:
        return {"xaf_per_unit": dict(self.xaf_per_unit), "as_of": dict(self.as_of), "source": dict(self.source)}

    @classmethod
    def from_dict(cls, data: dict | None) -> "ExchangeRates":
        rates = cls()
        if data:
            rates.xaf_per_unit.update({k.upper(): float(v) for k, v in data.get("xaf_per_unit", {}).items()})
            rates.as_of.update(data.get("as_of", {}))
            rates.source.update(data.get("source", {}))
        rates.xaf_per_unit["XAF"] = 1.0
        return rates


def format_money(amount: float | None, currency: str = "XAF", decimals: int = 0) -> str:
    if amount is None:
        return "n/a"
    text = f"{amount:,.{decimals}f}".replace(",", " ")
    return f"{text} {currency}"
