"""Connector plugin framework (Master prompt §7, §8).

A connector knows ONE source. It fetches raw records (`fetch`) and normalizes them into
`NormalizedRecord`s; the shared pipeline (app.ingestion.pipeline) does persistence, provenance,
entity resolution, validation and logging. Connectors never write financial facts directly.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any, ClassVar

import httpx

from app.config import get_settings

log = logging.getLogger("ap2i.connectors")


class ConnectorError(Exception):
    """Raised for an unrecoverable source error (after retries)."""


@dataclass
class SyncParams:
    countries: list[str]  # ISO3
    date_from: date | None = None
    date_to: date | None = None
    incremental: bool = True
    limit: int | None = None  # cap for tests / manual sampling
    reprocess: bool = False  # re-apply parsing/mappings to records already stored
    cursor: dict = field(default_factory=dict)


@dataclass
class RawRecord:
    source_identifier: str
    record_type: str
    country_iso3: str | None
    payload: dict
    source_url: str | None
    source_last_updated: str | None = None
    raw_text: str | None = None
    payload_format: str = "json"

    @property
    def sha256(self) -> str:
        body = self.raw_text if self.raw_text is not None else json.dumps(self.payload, sort_keys=True, default=str)
        return hashlib.sha256(body.encode("utf-8")).hexdigest()


@dataclass
class Money:
    amount: Decimal
    currency: str
    value_date: date | None
    transaction_key: str
    kind: str  # commitment types: original|additional|cancellation|revision ; flows: disbursement|expenditure
    label: str  # the source field / transaction type it comes from


@dataclass
class NormalizedAgreement:
    partner_code: str
    source_identifier: str
    name: str | None = None
    instrument_code: str | None = None
    instrument_label: str | None = None
    approval_date: date | None = None
    signature_date: date | None = None
    effectiveness_date: date | None = None
    closing_date_original: date | None = None
    closing_date_current: date | None = None
    status: str = "unknown"
    currency: str | None = None
    amount_original: Decimal | None = None
    amount_label: str | None = None
    commitments: list[Money] = field(default_factory=list)
    flows: list[Money] = field(default_factory=list)
    reported_current_commitment: Decimal | None = None
    reported_cumulative_disbursed: Decimal | None = None
    reported_undisbursed: Decimal | None = None
    reported_cumulative_as_of: date | None = None
    reported_cumulative_label: str | None = None
    parent_source_identifier: str | None = None


@dataclass
class NormalizedRecord:
    """Everything a source says about one project-level entity, in AP²I vocabulary.

    Fields left as None are MISSING — they are reported as gaps, never filled with zero.
    """

    country_iso3: str
    title: str
    title_language: str | None = None
    alt_titles: list[tuple[str, str | None]] = field(default_factory=list)  # (title, lang)
    description: str | None = None
    objectives: str | None = None
    sector_code: str | None = None
    sector_label: str | None = None  # original source wording
    status: str = "unknown"
    status_label: str | None = None
    executing_agency: str | None = None
    implementing_agency: str | None = None
    approval_date: date | None = None
    start_date: date | None = None
    planned_end_date: date | None = None
    actual_end_date: date | None = None
    original_cost: Decimal | None = None
    cost_currency: str | None = None
    agreements: list[NormalizedAgreement] = field(default_factory=list)
    documents: list[dict] = field(default_factory=list)  # {title, url, doc_type, language, date}
    locations: list[dict] = field(default_factory=list)  # {name, lat, lon, precision}
    results: list[dict] = field(default_factory=list)  # {title, measure, baseline, target, actuals}
    participating_orgs: list[dict] = field(default_factory=list)  # {role, ref, name}
    # Identifiers that deterministically designate the SAME underlying project in other sources.
    equivalent_identifiers: list[str] = field(default_factory=list)
    # Identifier of a parent record this one belongs to (IATI hierarchy), if any.
    parent_identifier: str | None = None
    observations: list[tuple[str, str, Any]] = field(default_factory=list)  # (field, source_field, value)
    warnings: list[str] = field(default_factory=list)


class Connector:
    """Base class. Subclasses set the metadata and implement fetch() + normalize()."""

    key: ClassVar[str]
    name: ClassVar[str]
    partner_code: ClassVar[str | None] = None
    tier: ClassVar[int] = 1
    access_method: ClassVar[str] = "api"
    base_url: ClassVar[str | None] = None
    documentation_url: ClassVar[str | None] = None
    usage_terms: ClassVar[str | None] = None
    update_frequency: ClassVar[str | None] = None
    default_schedule: ClassVar[str | None] = "0 3 * * *"  # daily discovery by default
    implemented: ClassVar[bool] = True

    def __init__(self, config: dict | None = None, client: httpx.Client | None = None):
        self.config = config or {}
        self.settings = get_settings()
        self._client = client
        self._last_request_at = 0.0

    # -- HTTP with retry, backoff and rate limiting -------------------------------------------
    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                timeout=self.settings.http_timeout_seconds,
                headers={"User-Agent": self.settings.http_user_agent},
                follow_redirects=True,
            )
        return self._client

    min_interval_seconds: float = 0.5
    max_attempts: int = 4

    def get(self, url: str, params: dict | None = None) -> httpx.Response:
        last_exc: Exception | None = None
        for attempt in range(1, self.max_attempts + 1):
            wait = self.min_interval_seconds - (time.monotonic() - self._last_request_at)
            if wait > 0:
                time.sleep(wait)
            try:
                self._last_request_at = time.monotonic()
                resp = self.client.get(url, params=params)
                if resp.status_code in (429, 500, 502, 503, 504):
                    raise httpx.HTTPStatusError(f"HTTP {resp.status_code}", request=resp.request, response=resp)
                resp.raise_for_status()
                return resp
            except (httpx.HTTPError,) as exc:  # network error or retryable status
                last_exc = exc
                log.warning("%s: attempt %d/%d failed for %s: %s", self.key, attempt, self.max_attempts, url, exc)
                status = getattr(getattr(exc, "response", None), "status_code", None)
                if status is not None and status not in (429, 500, 502, 503, 504):
                    break
                if attempt < self.max_attempts:
                    time.sleep(min(2 ** attempt, 16))
        raise ConnectorError(f"{self.key}: GET {url} failed after retries: {last_exc}")

    # -- Contract --------------------------------------------------------------------------
    def fetch(self, params: SyncParams) -> Iterator[RawRecord]:
        raise NotImplementedError

    def normalize(self, raw: RawRecord) -> NormalizedRecord | None:
        """Return None for records that are not project-level (they are kept as raw provenance)."""
        raise NotImplementedError

    def describe(self) -> dict:
        return {
            "key": self.key,
            "name": self.name,
            "partner_code": self.partner_code,
            "tier": self.tier,
            "access_method": self.access_method,
            "base_url": self.base_url,
            "documentation_url": self.documentation_url,
            "usage_terms": self.usage_terms,
            "update_frequency": self.update_frequency,
            "implemented": self.implemented,
        }


# --- small parsing helpers shared by connectors ------------------------------------------------

NULL_DATE_SENTINELS = {date(1900, 1, 1), date(1899, 12, 30), date(1, 1, 1)}


def parse_date(value: Any) -> date | None:
    """Parse the date formats seen in sources. Unparseable -> None (missing), never a guess.

    Placeholder dates used by some sources for "no date" (e.g. 1900-01-01) are treated as missing.
    """
    d = _parse_date(value)
    return None if d in NULL_DATE_SENTINELS else d


def _parse_date(value: Any) -> date | None:
    if value in (None, "", "null"):
        return None
    s = str(value).strip()
    from datetime import datetime

    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d", "%m/%d/%Y %I:%M:%S %p", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    if len(s) >= 10:
        try:
            return date.fromisoformat(s[:10])
        except ValueError:
            return None
    return None


def parse_decimal(value: Any) -> Decimal | None:
    if value in (None, "", "null"):
        return None
    s = str(value).replace(",", "").replace(" ", "").strip()
    try:
        return Decimal(s)
    except Exception:
        return None
