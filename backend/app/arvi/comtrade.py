"""UN Comtrade public API client (no key): fetch, archive, normalise.

Every response is archived byte-for-byte under var/arvi/raw/<sha256>.json.gz and listed in a
manifest (URL, SHA-256, fetch time, record count), so each figure can be traced back to the exact
response it came from. Raw responses are NOT committed: UN Comtrade data may not be
re-disseminated without permission of the UN Statistics Division (see docs/arvi/DATA_SOURCES.md).

The public "preview" endpoint accepts one period per call, returns at most 500 records and is
rate-limited: calls go year by year, are spaced and retried with backoff, and a query hitting
the cap is split by HS code.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

BASE = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"
REFERENCE = "https://comtradeapi.un.org/files/v1/app/reference/{name}.json"
PREVIEW_CAP = 500
SPACING_S = 2.5
BACKOFF_S = (5, 10, 20, 40, 80)

DATA_DIR = Path(__file__).resolve().parents[2] / "var" / "arvi"


@dataclass(frozen=True)
class Flow:
    """One declared trade flow, as published (FACT)."""

    reporter: str  # ISO3 of the declaring country
    partner: str  # ISO3 (or Comtrade code for "nes" areas)
    flow: str  # X (export) or M (import)
    hs: str
    year: int
    value_usd: Decimal
    valuation: str  # FOB, CIF or "unknown"
    net_kg: Decimal | None  # None when not declared
    net_kg_estimated: bool
    sha256: str  # archived response this row comes from

    def to_json(self) -> dict:
        d = asdict(self)
        d["value_usd"] = str(self.value_usd)
        d["net_kg"] = None if self.net_kg is None else str(self.net_kg)
        return d

    @classmethod
    def from_json(cls, d: dict) -> Flow:
        return cls(**{**d, "value_usd": Decimal(d["value_usd"]),
                      "net_kg": None if d["net_kg"] is None else Decimal(d["net_kg"])})


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Archive:
    """Raw response store + manifest."""

    def __init__(self, root: Path = DATA_DIR):
        self.root = root
        (root / "raw").mkdir(parents=True, exist_ok=True)
        self.manifest_path = root / "manifest.json"
        self.manifest: list[dict] = (
            json.loads(self.manifest_path.read_text()) if self.manifest_path.exists() else []
        )

    def store(self, url: str, body: bytes, count: int | None) -> str:
        sha = hashlib.sha256(body).hexdigest()
        path = self.root / "raw" / f"{sha}.json.gz"
        if not path.exists():
            path.write_bytes(gzip.compress(body))
        if not any(m["sha256"] == sha and m["url"] == url for m in self.manifest):
            self.manifest.append({"url": url, "sha256": sha, "fetched_at": _now(), "records": count})
            self.manifest_path.write_text(json.dumps(self.manifest, indent=1))
        return sha


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "ARVI-pilot/0.1 (research)"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


class Comtrade:
    def __init__(self, archive: Archive, get: Callable[[str], bytes] = http_get,
                 sleep: Callable[[float], None] = time.sleep):
        self.archive, self.get, self.sleep = archive, get, sleep
        self._last = 0.0

    def _call(self, url: str) -> tuple[dict, str]:
        for wait in (0, *BACKOFF_S):
            if wait:
                self.sleep(wait)
            gap = time.monotonic() - self._last
            if gap < SPACING_S:
                self.sleep(SPACING_S - gap)
            self._last = time.monotonic()
            try:
                body = self.get(url)
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code >= 500:
                    continue
                raise RuntimeError(f"Comtrade refused the query ({e.code}: {e.read()[:200]!r}): {url}") from e
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict) and isinstance(payload.get("data"), list):
                sha = self.archive.store(url, body, payload.get("count"))
                return payload, sha
        raise RuntimeError(f"Comtrade did not return data after retries: {url}")

    def reference(self, name: str) -> list[dict]:
        url = REFERENCE.format(name=name)
        body = self.get(url)
        self.archive.store(url, body, None)
        return json.loads(body)["results"]

    def query(self, *, flow: str, cmd: Iterable[str], years: Iterable[int],
              reporter: int | None = None, partner: int | None = None) -> list[tuple[dict, str]]:
        """All records for the query, one year per call, split by code at the preview cap."""
        cmd, years = list(cmd), list(years)
        if len(years) > 1:
            return [x for y in years for x in self.query(flow=flow, cmd=cmd, years=[y],
                                                         reporter=reporter, partner=partner)]
        params = {"flowCode": flow, "cmdCode": ",".join(cmd), "period": ",".join(map(str, years))}
        if reporter is not None:
            params["reporterCode"] = str(reporter)
        if partner is not None:
            params["partnerCode"] = str(partner)
        url = f"{BASE}?{urllib.parse.urlencode(params, safe=',')}"
        payload, sha = self._call(url)
        rows = payload["data"]
        if len(rows) < PREVIEW_CAP:
            return [(r, sha) for r in rows]
        if len(cmd) > 1:
            return [x for c in cmd for x in self.query(flow=flow, cmd=[c], years=years,
                                                       reporter=reporter, partner=partner)]
        raise RuntimeError(f"Single-code, single-year query exceeds the preview cap: {url}")


def _dec(v) -> Decimal | None:
    return None if v is None else Decimal(str(v))


def normalise(record: dict, sha: str, codes: dict[int, str]) -> Flow | None:
    """One Comtrade record -> Flow, or None if it is a breakdown we do not use.

    Kept: totals over customs procedure (C00), mode of transport (0) and second partner (0),
    individual partners only (no "World" total, no country groups).
    """
    if record.get("customsCode") != "C00" or record.get("motCode") != 0 or record.get("partner2Code") != 0:
        return None
    if record["partnerCode"] == 0 or record["reporterCode"] not in codes or record["partnerCode"] not in codes:
        return None
    value = _dec(record.get("primaryValue"))
    if value is None:
        return None
    if record["flowCode"] == "X":
        valuation = "FOB" if record.get("fobvalue") is not None else "unknown"
    else:
        valuation = "CIF" if record.get("cifvalue") is not None else (
            "FOB" if record.get("fobvalue") is not None else "unknown")
    kg = _dec(record.get("netWgt"))
    if kg is not None and kg <= 0:
        kg = None
    return Flow(
        reporter=codes[record["reporterCode"]], partner=codes[record["partnerCode"]],
        flow=record["flowCode"], hs=str(record["cmdCode"]), year=int(record["refYear"]),
        value_usd=value, valuation=valuation, net_kg=kg,
        net_kg_estimated=bool(record.get("isNetWgtEstimated")) if kg is not None else False,
        sha256=sha,
    )


def area_codes(reporters: list[dict], partners: list[dict]) -> tuple[dict[int, str], dict[str, int]]:
    """Comtrade numeric code -> ISO3 for individual areas (groups excluded), and ISO3 -> code."""
    codes: dict[int, str] = {}
    for r in reporters:
        if not r.get("isGroup"):
            codes[r["reporterCode"]] = r["reporterCodeIsoAlpha3"]
    for p in partners:
        if not p.get("isGroup") and p["PartnerCode"] != 0:
            codes.setdefault(p["PartnerCode"], p["PartnerCodeIsoAlpha3"])
    iso_to_code = {r["reporterCodeIsoAlpha3"]: r["reporterCode"] for r in reporters if not r.get("isGroup")}
    return codes, iso_to_code


def partner_names(partners: list[dict]) -> dict[str, str]:
    """ISO3 -> current name; historical entries (e.g. "India (...1974)") never win."""
    names: dict[str, str] = {}
    for p in sorted(partners, key=lambda p: "..." not in p["PartnerDesc"]):
        if p["PartnerCode"] != 0:
            names[p["PartnerCodeIsoAlpha3"]] = p["PartnerDesc"]
    return names
