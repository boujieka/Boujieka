"""SYNTHETIC market data for development and demos. NOT REAL MARKET DATA.

Every record generated here has is_synthetic=True, data_nature=SYNTHETIC and
verification_status=synthetic (enforced by a database CHECK constraint), and
every security name starts with "[SYNTHETIC]". Yield levels, amounts and
dates are random draws around arbitrary anchors chosen only so the UI has
realistic-looking shapes to render. They say nothing about any real market.

Generation is deterministic for a given (seed, reference_date).
"""

import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from app.analytics.calculations import price_from_simple_yield, quantize
from app.models.enums import (
    AuctionStatus,
    AuctionType,
    CouponFrequency,
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

# Arbitrary anchor yields (percent). NOT estimates of real market levels.
COUNTRY_PROFILE: dict[str, tuple[float, list[Line]]] = {
    "CMR": (6.0, CEMAC_LINES),
    "COG": (7.5, CEMAC_LINES),
    "GAB": (6.8, CEMAC_LINES),
    "CIV": (5.4, WAEMU_LINES),
    "SEN": (5.9, WAEMU_LINES),
    "KEN": (9.5, KENYA_LINES),
}

HISTORY_DAYS = 270
FORWARD_DAYS = 21


def _d(x: float, places: int = 4) -> Decimal:
    return quantize(Decimal(str(x)), places)  # type: ignore[return-value]


def generate(reference_date: date, seed: int = 20261003) -> dict[str, list[dict]]:
    """Return plain dicts keyed by country iso3 → list of {security, auctions}.

    Kept free of ORM objects so it can be unit-tested in isolation.
    """
    rng = random.Random(f"{seed}:{reference_date.isoformat()}")
    out: dict[str, list[dict]] = {}
    start = reference_date - timedelta(days=HISTORY_DAYS)
    end = reference_date + timedelta(days=FORWARD_DAYS)
    extracted = datetime.combine(reference_date, datetime.min.time(), tzinfo=timezone.utc)

    for iso3, (anchor, lines) in COUNTRY_PROFILE.items():
        series: list[dict] = []
        level = anchor  # slow random walk shared by all tenors of a country
        for line in lines:
            offset = rng.randint(0, line.cadence_days - 1)
            day = start + timedelta(days=offset)
            bond_security: dict | None = None
            while day <= end:
                level += rng.gauss(0, 0.04)
                is_bill = line.instrument_type == InstrumentType.TREASURY_BILL
                settlement = day + timedelta(days=2 if iso3 == "KEN" else 3)
                if is_bill or bond_security is None:
                    security = {
                        "security_name": f"{SYNTHETIC_PREFIX} {iso3} {line.label} "
                        f"{settlement.isoformat()}",
                        "local_code": f"SYN-{iso3}-{line.label.replace(' ', '')}-"
                        f"{settlement.strftime('%Y%m%d')}",
                        "instrument_type": line.instrument_type,
                        "tenor_days": line.tenor_days,
                        "issue_date": settlement,
                        "maturity_date": settlement + timedelta(days=line.tenor_days),
                        "coupon_rate": _d(line.coupon) if line.coupon else None,
                        "coupon_frequency": CouponFrequency.ANNUAL
                        if line.coupon
                        else CouponFrequency.ZERO,
                        "auctions": [],
                    }
                    series.append(security)
                    if not is_bill:
                        bond_security = security
                    auction_type = AuctionType.PRIMARY_AUCTION
                else:
                    security = bond_security
                    auction_type = AuctionType.REOPENING

                remaining_days = (security["maturity_date"] - settlement).days
                if remaining_days <= 0:
                    day += timedelta(days=line.cadence_days)
                    continue

                offered = Decimal(rng.randint(*line.offered)) * Decimal(1_000_000)
                auction: dict = {
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
                }

                if day > reference_date:
                    auction["status"] = AuctionStatus.ANNOUNCED
                    auction["field_status"] = {
                        f: FieldStatus.PENDING.value
                        for f in (
                            "amount_submitted",
                            "amount_allocated",
                            "cutoff_yield",
                            "weighted_average_yield",
                            "average_price",
                            "number_of_bidders",
                        )
                    }
                else:
                    cover = max(0.3, rng.lognormvariate(0.45, 0.45))
                    submitted = (offered * _d(cover, 3)).quantize(Decimal(1))
                    allocated = min(submitted, offered * _d(rng.uniform(0.85, 1.1), 3)).quantize(
                        Decimal(1)
                    )
                    # Thin demand pushes yields up; strong demand pulls them down.
                    way = level + line.term_premium - 0.25 * (cover - 1.5) + rng.gauss(0, 0.05)
                    cutoff = way + abs(rng.gauss(0.08, 0.04))
                    auction.update(
                        status=AuctionStatus.COMPLETED,
                        amount_submitted=submitted,
                        amount_allocated=allocated,
                        weighted_average_yield=_d(way),
                        cutoff_yield=_d(cutoff),
                        minimum_bid=_d(way - abs(rng.gauss(0.4, 0.15))),
                        maximum_bid=_d(cutoff + abs(rng.gauss(0.6, 0.2))),
                        number_of_bidders=rng.randint(6, 28),
                        publication_date=day + timedelta(days=1),
                    )
                    auction["number_of_successful_bidders"] = rng.randint(
                        3, auction["number_of_bidders"]
                    )
                    if is_bill:
                        auction["average_price"] = quantize(
                            price_from_simple_yield(
                                auction["weighted_average_yield"], remaining_days, SYNTHETIC_BASIS
                            ),
                            6,
                        )
                    else:
                        auction["average_price"] = None
                        auction["field_status"]["average_price"] = FieldStatus.NOT_AVAILABLE.value
                    # Exercise the "Not disclosed" path on a share of results.
                    if rng.random() < 0.2:
                        auction["number_of_bidders"] = None
                        auction["number_of_successful_bidders"] = None
                        auction["field_status"]["number_of_bidders"] = (
                            FieldStatus.NOT_DISCLOSED.value
                        )
                        auction["field_status"]["number_of_successful_bidders"] = (
                            FieldStatus.NOT_DISCLOSED.value
                        )
                security["auctions"].append(auction)
                day += timedelta(days=line.cadence_days)
        out[iso3] = series

    _add_status_examples(out, reference_date)
    return out


def _add_status_examples(out: dict[str, list[dict]], reference_date: date) -> None:
    """Mark one upcoming auction cancelled and one postponed so those states are visible."""
    for iso3, status in (("COG", AuctionStatus.CANCELLED), ("GAB", AuctionStatus.POSTPONED)):
        upcoming = [
            a
            for s in out[iso3]
            for a in s["auctions"]
            if a["auction_date"] > reference_date and a["status"] == AuctionStatus.ANNOUNCED
        ]
        if upcoming:
            upcoming[0]["status"] = status
