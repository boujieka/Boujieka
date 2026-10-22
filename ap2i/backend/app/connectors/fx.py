"""Historical exchange-rate ingestion (Master prompt §16).

Sources (verified reachable 2026-10-22):
  * World Bank WDI indicator PA.NUS.FCRF — "Official exchange rate (LCU per US$, period average)",
    annual. Gives XAF/USD (CMR), XOF/USD, EUR/USD (economy code EMU), and any national currency.
    https://api.worldbank.org/v2/country/{code}/indicator/PA.NUS.FCRF?format=json
  * IMF Exchange Rates dataset (IMF.STA:ER) — US$ per SDR, annual period average (USA.XDC_XDR.PA_RT.A).
    Needed because AfDB publishes amounts in SDR/units of account (currency code XDR).
    https://api.imf.org/external/sdmx/2.1/data/IMF.STA,ER/USA.XDC_XDR.PA_RT.A

Rates are stored as "1 base = rate quote" with period "YYYY" and period_type "annual_avg".
"""

from __future__ import annotations

from decimal import Decimal

import httpx
from lxml import etree
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import ExchangeRate
from app.reference.countries import COUNTRIES

WB_ECONOMY_FOR_CURRENCY = {"EUR": "EMU"}


def _client() -> httpx.Client:
    s = get_settings()
    return httpx.Client(timeout=s.http_timeout_seconds, headers={"User-Agent": s.http_user_agent}, follow_redirects=True)


def _upsert(db: Session, base: str, quote: str, rate: Decimal, period: str, source: str, url: str) -> bool:
    existing = db.scalar(select(ExchangeRate).where(
        ExchangeRate.base_currency == base, ExchangeRate.quote_currency == quote,
        ExchangeRate.period == period, ExchangeRate.period_type == "annual_avg", ExchangeRate.source == source))
    if existing:
        if existing.rate != rate:
            existing.rate = rate
        return False
    db.add(ExchangeRate(base_currency=base, quote_currency=quote, rate=rate, period=period,
                        period_type="annual_avg", source=source, source_url=url))
    return True


def fetch_worldbank_lcu_per_usd(db: Session, currency: str, economy: str, first_year: int, last_year: int,
                                client: httpx.Client | None = None) -> int:
    s = get_settings()
    url = f"{s.worldbank_indicator_url}/country/{economy}/indicator/PA.NUS.FCRF"
    c = client or _client()
    resp = c.get(url, params={"format": "json", "date": f"{first_year}:{last_year}", "per_page": 200})
    resp.raise_for_status()
    body = resp.json()
    if not isinstance(body, list) or len(body) < 2 or body[1] is None:
        return 0
    n = 0
    for obs in body[1]:
        if obs.get("value") is None:
            continue  # missing stays missing
        rate = Decimal(str(obs["value"]))
        n += _upsert(db, "USD", currency, rate, str(obs["date"]),
                     "World Bank WDI PA.NUS.FCRF (official exchange rate, LCU per US$, period average)",
                     f"{url}?format=json&date={obs['date']}")
    return n


def fetch_imf_usd_per_sdr(db: Session, first_year: int, client: httpx.Client | None = None) -> int:
    s = get_settings()
    url = f"{s.imf_sdmx_url}/data/IMF.STA,ER/USA.XDC_XDR.PA_RT.A"
    c = client or _client()
    resp = c.get(url, params={"startPeriod": str(first_year)})
    resp.raise_for_status()
    root = etree.fromstring(resp.content)
    n = 0
    for obs in root.iter("{*}Obs", "Obs"):
        period = obs.get("TIME_PERIOD")
        value = obs.get("OBS_VALUE")
        if not period or value in (None, "", "NaN"):
            continue
        n += _upsert(db, "XDR", "USD", Decimal(value), period,
                     "IMF Exchange Rates (IMF.STA:ER) USA.XDC_XDR.PA_RT.A — US$ per SDR, period average",
                     f"{url}?startPeriod={first_year}")
    return n


def refresh_rates(db: Session, countries: list[str], first_year: int = 2000, last_year: int = 2026) -> dict:
    """Fetch the rates needed for the given active countries plus EUR and XDR."""
    out: dict[str, int | str] = {}
    currencies = {c.currency: c.iso3 for c in COUNTRIES if c.iso3 in countries}
    with _client() as client:
        for cur, iso3 in currencies.items():
            try:
                out[cur] = fetch_worldbank_lcu_per_usd(db, cur, iso3, first_year, last_year, client)
            except httpx.HTTPError as exc:
                out[cur] = f"error: {exc}"
        try:
            out["EUR"] = fetch_worldbank_lcu_per_usd(db, "EUR", "EMU", first_year, last_year, client)
        except httpx.HTTPError as exc:
            out["EUR"] = f"error: {exc}"
        try:
            out["XDR"] = fetch_imf_usd_per_sdr(db, first_year, client)
        except httpx.HTTPError as exc:
            out["XDR"] = f"error: {exc}"
    db.commit()
    return out
