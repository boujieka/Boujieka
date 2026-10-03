"""SYNTHETIC market data for development and demos. NOT REAL MARKET DATA.

Every record generated here has is_synthetic=True, data_nature=SYNTHETIC and
verification_status=synthetic (enforced by a database CHECK constraint), and
every security name starts with "[SYNTHETIC]". Yield levels, amounts and
dates are random draws around arbitrary anchors chosen only so the UI has
realistic-looking shapes to render. They say nothing about any real market.

Generation is rolling and deterministic: every auction is drawn from its own seed
(country, line, date), and history starts at a fixed EPOCH. Re-running on a later date
reproduces the same past auctions and only adds new ones; an auction announced earlier
gets its (synthetic) result once its date has passed.

All 54 countries are generated. The six MVP countries keep hand-set anchor yields; the other
48 get anchors drawn from a hash of their ISO code, deliberately unrelated to any real market.
Whether a given country actually runs regular domestic auctions has NOT been verified.
"""

import hashlib
import math
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from app.analytics.calculations import price_from_simple_yield, quantize
from app.seed.africa import AFRICA
from app.models.enums import (
    AuctionStatus,
    AuctionType,
    CouponFrequency,
    MonetaryZone,
    DataNature,
    FieldStatus,
    InstrumentType,
    VerificationStatus,
)

SYNTHETIC_PREFIX = "[SYNTHETIC]"
SYNTHETIC_CONVENTION = "SYNTHETIC: simple interest ACT/360"
SYNTHETIC_NOTE = "Synthetic development data. Not real market data. Do not use for decisions."
SYNTHETIC_BASIS = 360

SYNTHETIC_PROVENANCE = {
    "is_synthetic": True,
    "data_nature": DataNature.SYNTHETIC,
    "verification_status": VerificationStatus.SYNTHETIC,
    "confidence_score": None,
    "provenance_notes": SYNTHETIC_NOTE,
}


@dataclass(frozen=True)
class Line:
    """An instrument programme to simulate for one country."""

    label: str
    instrument_type: InstrumentType
    tenor_days: int
    cadence_days: int  # days between auctions
    offered: tuple[int, int]  # amount offered range, in millions of local currency
    term_premium: float  # percentage points above the country anchor
    coupon: float | None = None  # bonds only


CEMAC_LINES = [
    Line("BTA 13W", InstrumentType.TREASURY_BILL, 91, 14, (10_000, 25_000), 0.0),
    Line("BTA 26W", InstrumentType.TREASURY_BILL, 182, 14, (15_000, 35_000), 0.4),
    Line("BTA 52W", InstrumentType.TREASURY_BILL, 364, 28, (20_000, 40_000), 0.9),
    Line("OTA 3Y", InstrumentType.TREASURY_BOND, 3 * 365, 56, (25_000, 60_000), 1.8, 6.0),
    Line("OTA 5Y", InstrumentType.TREASURY_BOND, 5 * 365, 84, (25_000, 75_000), 2.5, 6.75),
]
WAEMU_LINES = [
    Line("BAT 3M", InstrumentType.TREASURY_BILL, 91, 14, (20_000, 40_000), 0.0),
    Line("BAT 6M", InstrumentType.TREASURY_BILL, 182, 14, (25_000, 50_000), 0.3),
    Line("BAT 12M", InstrumentType.TREASURY_BILL, 364, 28, (30_000, 60_000), 0.7),
    Line("OAT 3Y", InstrumentType.TREASURY_BOND, 3 * 365, 42, (30_000, 80_000), 1.2, 6.0),
    Line("OAT 5Y", InstrumentType.TREASURY_BOND, 5 * 365, 70, (30_000, 100_000), 1.7, 6.5),
]
KENYA_LINES = [
    Line("T-Bill 91D", InstrumentType.TREASURY_BILL, 91, 7, (4_000, 4_000), 0.0),
    Line("T-Bill 182D", InstrumentType.TREASURY_BILL, 182, 7, (10_000, 10_000), 0.3),
    Line("T-Bill 364D", InstrumentType.TREASURY_BILL, 364, 7, (10_000, 10_000), 0.7),
    Line("FXD 5Y", InstrumentType.TREASURY_BOND, 5 * 365, 28, (20_000, 30_000), 1.8, 11.5),
    Line("FXD 10Y", InstrumentType.TREASURY_BOND, 10 * 365, 56, (20_000, 30_000), 2.6, 13.0),
]

GENERIC_LINES = [
    Line("T-Bill 91D", InstrumentType.TREASURY_BILL, 91, 14, (5_000, 25_000), 0.0),
    Line("T-Bill 182D", InstrumentType.TREASURY_BILL, 182, 14, (5_000, 30_000), 0.4),
    Line("T-Bill 364D", InstrumentType.TREASURY_BILL, 364, 28, (10_000, 40_000), 0.9),
    Line("T-Bond 3Y", InstrumentType.TREASURY_BOND, 3 * 365, 56, (10_000, 60_000), 1.6, 9.0),
    Line("T-Bond 5Y", InstrumentType.TREASURY_BOND, 5 * 365, 84, (10_000, 80_000), 2.3, 10.0),
]

# Hand-set anchors for the six MVP countries (arbitrary; NOT estimates of real levels).
MVP_PROFILE: dict[str, tuple[float, list[Line]]] = {
    "CMR": (6.0, CEMAC_LINES),
    "COG": (7.5, CEMAC_LINES),
    "GAB": (6.8, CEMAC_LINES),
    "CIV": (5.4, WAEMU_LINES),
    "SEN": (5.9, WAEMU_LINES),
    "KEN": (9.5, KENYA_LINES),
}

EPOCH = date(2026, 1, 1)  # first synthetic auction date; history grows from here
FORWARD_DAYS = 21  # how far ahead announced auctions are generated
DISRUPTION_RATE = 0.015  # share of auctions marked cancelled or postponed


def _h(*parts: object) -> int:
    """Stable integer hash (Python's hash() is salted per process)."""
    return int.from_bytes(hashlib.sha256(":".join(map(str, parts)).encode()).digest()[:8], "big")


def _rng(*parts: object) -> random.Random:
    return random.Random(_h(*parts))


def country_profile(iso3: str, zone: MonetaryZone) -> tuple[float, list[Line], float]:
    """(anchor yield %, instrument lines, amount scale). Hash-derived outside the MVP six."""
    if iso3 in MVP_PROFILE:
        anchor, lines = MVP_PROFILE[iso3]
        return anchor, lines, 1.0
    anchor = 4.0 + (_h("anchor", iso3) % 10_000) / 1_000  # 4.0 – 14.0 %
    lines = {MonetaryZone.CEMAC: CEMAC_LINES, MonetaryZone.WAEMU: WAEMU_LINES}.get(zone, GENERIC_LINES)
    scale = (0.1, 1.0, 10.0)[_h("scale", iso3) % 3]
    return anchor, lines, scale


def _level(iso3: str, anchor: float, day: date) -> float:
    """Smooth, deterministic country yield level for a date (no dependence on as-of)."""
    t = (day - EPOCH).days
    p1 = (_h("p1", iso3) % 628) / 100
    p2 = (_h("p2", iso3) % 628) / 100
    return anchor + 0.5 * math.sin(2 * math.pi * t / 240 + p1) + 0.2 * math.sin(2 * math.pi * t / 57 + p2)


def _d(x: float, places: int = 4) -> Decimal:
    return quantize(Decimal(str(x)), places)  # type: ignore[return-value]


PENDING_FIELDS = (
    "amount_submitted",
    "amount_allocated",
    "cutoff_yield",
    "weighted_average_yield",
    "average_price",
    "number_of_bidders",
)


def _auction(iso3: str, line: Line, day: date, security: dict, auction_type: AuctionType,
             anchor: float, scale: float, as_of: date, extracted: datetime) -> dict:
    r = _rng("auction", iso3, line.label, day.isoformat())
    settlement = day + timedelta(days=2 if iso3 == "KEN" else 3)
    remaining_days = (security["maturity_date"] - settlement).days
    offered = (Decimal(r.randint(*line.offered)) * Decimal(1_000_000) * _d(scale, 2)).quantize(Decimal(1))
    a: dict = {
        "auction_date": day,
        "announcement_date": day - timedelta(days=7),
        "settlement_date": settlement,
        "auction_type": auction_type,
        "amount_offered": offered,
        "yield_convention": SYNTHETIC_CONVENTION,
        "source_url": None,
        "publication_date": day - timedelta(days=7),
        "extracted_at": extracted,
        "field_status": {},
        # Results default to empty; filled below for completed auctions.
        "amount_submitted": None, "amount_allocated": None, "weighted_average_yield": None,
        "cutoff_yield": None, "minimum_bid": None, "maximum_bid": None, "average_price": None,
        "number_of_bidders": None, "number_of_successful_bidders": None,
    }
    disruption = r.random()
    if disruption < DISRUPTION_RATE:
        a["status"] = AuctionStatus.CANCELLED if disruption < DISRUPTION_RATE / 2 else AuctionStatus.POSTPONED
        return a
    if day > as_of:
        a["status"] = AuctionStatus.ANNOUNCED
        a["field_status"] = {f: FieldStatus.PENDING.value for f in PENDING_FIELDS}
        return a

    cover = max(0.3, r.lognormvariate(0.45, 0.45))
    submitted = (offered * _d(cover, 3)).quantize(Decimal(1))
    allocated = min(submitted, offered * _d(r.uniform(0.85, 1.1), 3)).quantize(Decimal(1))
    # Thin demand pushes yields up; strong demand pulls them down.
    way = _level(iso3, anchor, day) + line.term_premium - 0.25 * (cover - 1.5) + r.gauss(0, 0.05)
    cutoff = way + abs(r.gauss(0.08, 0.04))
    bidders = r.randint(6, 28)
    a.update(
        status=AuctionStatus.COMPLETED,
        amount_submitted=submitted,
        amount_allocated=allocated,
        weighted_average_yield=_d(way),
        cutoff_yield=_d(cutoff),
        minimum_bid=_d(way - abs(r.gauss(0.4, 0.15))),
        maximum_bid=_d(cutoff + abs(r.gauss(0.6, 0.2))),
        number_of_bidders=bidders,
        number_of_successful_bidders=r.randint(3, bidders),
        publication_date=day + timedelta(days=1),
    )
    if line.instrument_type == InstrumentType.TREASURY_BILL:
        a["average_price"] = quantize(
            price_from_simple_yield(a["weighted_average_yield"], remaining_days, SYNTHETIC_BASIS), 6
        )
    else:
        a["field_status"]["average_price"] = FieldStatus.NOT_AVAILABLE.value
    # Exercise the "Not disclosed" path on a share of results.
    if r.random() < 0.2:
        a["number_of_bidders"] = None
        a["number_of_successful_bidders"] = None
        a["field_status"]["number_of_bidders"] = FieldStatus.NOT_DISCLOSED.value
        a["field_status"]["number_of_successful_bidders"] = FieldStatus.NOT_DISCLOSED.value
    return a


def generate(as_of: date, seed: int = 20261003, countries: list[str] | None = None) -> dict[str, list[dict]]:
    """Plain dicts keyed by country iso3 → list of {security fields..., auctions: [...]}.

    Auctions run from EPOCH to as_of + FORWARD_DAYS. Kept free of ORM objects for testing.
    """
    out: dict[str, list[dict]] = {}
    end = as_of + timedelta(days=FORWARD_DAYS)
    extracted = datetime.combine(as_of, datetime.min.time(), tzinfo=timezone.utc)
    wanted = set(countries) if countries else None

    for c in AFRICA:
        if wanted is not None and c.iso3 not in wanted:
            continue
        anchor, lines, scale = country_profile(c.iso3, c.zone)
        series: list[dict] = []
        for line in lines:
            offset = _rng(seed, "offset", c.iso3, line.label).randint(0, line.cadence_days - 1)
            day = EPOCH + timedelta(days=offset)
            bond: dict | None = None
            is_bill = line.instrument_type == InstrumentType.TREASURY_BILL
            while day <= end:
                settlement = day + timedelta(days=2 if c.iso3 == "KEN" else 3)
                if is_bill or bond is None or bond["maturity_date"] <= settlement:
                    security = {
                        "security_name": f"{SYNTHETIC_PREFIX} {c.iso3} {line.label} {settlement.isoformat()}",
                        "local_code": f"SYN-{c.iso3}-{line.label.replace(' ', '')}-{settlement.strftime('%Y%m%d')}",
                        "instrument_type": line.instrument_type,
                        "tenor_days": line.tenor_days,
                        "issue_date": settlement,
                        "maturity_date": settlement + timedelta(days=line.tenor_days),
                        "coupon_rate": _d(line.coupon) if line.coupon else None,
                        "coupon_frequency": CouponFrequency.ANNUAL if line.coupon else CouponFrequency.ZERO,
                        "auctions": [],
                    }
                    series.append(security)
                    if not is_bill:
                        bond = security
                    auction_type = AuctionType.PRIMARY_AUCTION
                else:
                    security = bond
                    auction_type = AuctionType.REOPENING
                security["auctions"].append(
                    _auction(c.iso3, line, day, security, auction_type, anchor, scale, as_of, extracted)
                )
                day += timedelta(days=line.cadence_days)
        out[c.iso3] = series
    return out
