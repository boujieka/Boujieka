"""Opportunity Engine (Phase 4).

Deterministic rules over stored auction data. No LLM, no estimates: every signal is derived
from published values (FACT, or SYNTHETIC in development) by a stated formula and threshold.

Each signal carries a "passport" (Opportunity.evidence):
    facts       the published values used, each with auction, date, data nature and source
    calculation the formula, its inputs and its result (CALCULATION)
    rule        the threshold that fired and how to read it
    invalidated_if  what new information would make the signal no longer hold
    caveats     known limitations of this specific signal

Labels are neutral ("High demand relative to recent auctions"). Nothing is ranked "best" and
no signal is a recommendation.

Re-running for the same as-of date is idempotent: signals are upserted by `dedup_key`, and
signals no longer detected are marked inactive (kept for audit).
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.analytics import calculations as calc
from app.models import Auction, Opportunity, Security, Source
from app.models.enums import AuctionStatus

# Every threshold the engine uses, in one place. Changing one changes which signals fire,
# never the underlying data.
RULES: dict[str, dict] = {
    "upcoming_auction": {"window_days": 14, "newly_announced_days": 7},
    "yield_move": {"lookback_days": 30, "threshold_bps": Decimal(25)},
    "demand": {"lookback_days": 30, "min_peers": 6, "max_peers": 12, "z_threshold": Decimal("1.5")},
    "high_yield": {"lookback_days": 30, "history_days": 365, "min_history": 8, "percentile": Decimal(90)},
    "curve_inversion": {"curve_lookback_days": 120, "threshold_bps": Decimal(15)},
    "refinancing": {"horizon_days": 365, "min_share_pct": Decimal(15), "multiple_of_average": Decimal(2)},
}

LABELS = {
    "upcoming_auction": "Upcoming auction",
    "newly_announced": "Newly announced auction",
    "yield_move_up": "Significant yield movement (higher)",
    "yield_move_down": "Significant yield movement (lower)",
    "high_demand": "High demand relative to recent auctions",
    "low_demand": "Low demand relative to recent auctions",
    "high_yield": "Higher historical yield (same tenor)",
    "curve_inversion": "Yield curve inversion",
    "refinancing_concentration": "Refinancing concentration",
    "auction_cancelled": "Auction cancelled",
    "auction_postponed": "Auction postponed",
}

SeriesKey = tuple[int, str, int]  # (country_id, instrument_type, tenor_days)


@dataclass
class Draft:
    dedup_key: str
    opportunity_type: str
    label: str
    country_id: int
    currency: str
    explanation: str
    evidence: dict
    security_id: int | None = None
    auction_id: int | None = None
    auction_date: date | None = None
    yield_pct: Decimal | None = None
    maturity: date | None = None
    strength: Decimal | None = None
    risk_flags: list[str] = field(default_factory=list)
    is_synthetic: bool = False
    source_urls: list[str] = field(default_factory=list)
    data_confidence: Decimal | None = None


# --------------------------------------------------------------------------- data loading


@dataclass
class MarketData:
    as_of: date
    completed: dict[SeriesKey, list[Auction]]  # oldest first, results published on/before as_of
    upcoming: list[Auction]  # announced/cancelled/postponed with auction_date >= as_of
    sources: dict[int, Source]


def load_market(session: Session, as_of: date) -> MarketData:
    auctions = session.scalars(
        select(Auction).options(joinedload(Auction.security).joinedload(Security.country))
    ).all()
    completed: dict[SeriesKey, list[Auction]] = defaultdict(list)
    upcoming: list[Auction] = []
    for a in auctions:
        s = a.security
        if a.status == AuctionStatus.COMPLETED and a.auction_date <= as_of and s.tenor_days:
            completed[(s.country_id, s.instrument_type.value, s.tenor_days)].append(a)
        elif a.status != AuctionStatus.COMPLETED and a.auction_date >= as_of:
            upcoming.append(a)
    for series in completed.values():
        series.sort(key=lambda a: (a.auction_date, a.auction_id))
    sources = {s.source_id: s for s in session.scalars(select(Source))}
    return MarketData(as_of, completed, upcoming, sources)


# --------------------------------------------------------------------------- helpers


def _fact(a: Auction, field_name: str, label: str, value, sources: dict[int, Source], unit: str = "") -> dict:
    src = sources.get(a.source_id)
    return {
        "label": label,
        "value": None if value is None else str(value),
        "unit": unit,
        "auction_id": a.auction_id,
        "auction_date": a.auction_date.isoformat(),
        "field": field_name,
        "data_nature": a.data_nature.value,
        "source": src.name if src else None,
        "source_url": a.source_url,
    }


def _common(a: Auction) -> dict:
    s = a.security
    return {
        "country_id": s.country_id,
        "currency": s.currency,
        "security_id": s.security_id,
        "auction_id": a.auction_id,
        "auction_date": a.auction_date,
        "maturity": s.maturity_date,
        "is_synthetic": a.is_synthetic,
        "source_urls": [a.source_url] if a.source_url else [],
        "data_confidence": a.confidence_score,
    }


def _flags(auctions: list[Auction], extra: list[str] | None = None) -> list[str]:
    flags = list(extra or [])
    if any(a.is_synthetic for a in auctions):
        flags.append("synthetic_data")
    if len({a.yield_convention for a in auctions}) > 1:
        flags.append("mixed_yield_conventions")
    return flags


def _tenor_label(days: int) -> str:
    return f"{round(days / 7)}W" if days < 365 else f"{days // 365}Y"


def _q(v: Decimal | None, places: int = 4) -> Decimal | None:
    return calc.quantize(v, places)


# --------------------------------------------------------------------------- rules


def detect_upcoming(m: MarketData) -> list[Draft]:
    r = RULES["upcoming_auction"]
    out = []
    for a in m.upcoming:
        days = (a.auction_date - m.as_of).days
        s = a.security
        key = (s.country_id, s.instrument_type.value, s.tenor_days)
        last = m.completed.get(key, [])[-1:] if s.tenor_days else []
        facts = [_fact(a, "amount_offered", "Amount offered", a.amount_offered, m.sources, s.currency)]
        if last:
            facts.append(
                _fact(last[0], "weighted_average_yield", "Previous auction WA yield (same tenor)",
                      last[0].weighted_average_yield, m.sources, "%")
            )

        if a.status in (AuctionStatus.CANCELLED, AuctionStatus.POSTPONED):
            kind = f"auction_{a.status.value}"
            out.append(Draft(
                dedup_key=f"{kind}:{a.auction_id}",
                opportunity_type=kind,
                label=LABELS[kind],
                explanation=f"The {_tenor_label(s.tenor_days or 0)} auction scheduled for "
                f"{a.auction_date.isoformat()} is marked {a.status.value} by its source.",
                evidence={
                    "facts": [_fact(a, "status", "Auction status", a.status.value, m.sources)] + facts,
                    "calculation": None,
                    "rule": {"description": "Auction status published as cancelled or postponed."},
                    "invalidated_if": "The source re-schedules or confirms the auction.",
                    "caveats": [],
                },
                risk_flags=_flags([a]),
                **_common(a),
            ))
            continue

        if days > r["window_days"]:
            continue
        newly = (
            a.announcement_date is not None
            and (m.as_of - a.announcement_date).days <= r["newly_announced_days"]
        )
        kind = "newly_announced" if newly else "upcoming_auction"
        out.append(Draft(
            dedup_key=f"upcoming_auction:{a.auction_id}",
            opportunity_type="upcoming_auction",
            label=LABELS[kind],
            yield_pct=last[0].weighted_average_yield if last else None,
            explanation=f"{_tenor_label(s.tenor_days or 0)} {s.instrument_type.value.replace('_', ' ')} "
            f"auction in {days} day(s) ({a.auction_date.isoformat()}). The yield shown is the PREVIOUS "
            "auction's published result for the same tenor, not a forecast.",
            evidence={
                "facts": facts,
                "calculation": {"formula": "days_to_auction = auction_date - as_of", "result": days},
                "rule": {
                    "description": f"Auction scheduled within {r['window_days']} days; 'newly announced' "
                    f"if announced within the last {r['newly_announced_days']} days.",
                    "threshold": r["window_days"],
                },
                "invalidated_if": "The auction is cancelled, postponed or held.",
                "caveats": [] if last else ["No previous auction of this tenor in the database."],
            },
            risk_flags=_flags([a] + last),
            **_common(a),
        ))
    return out


def _recent_latest(series: list[Auction], as_of: date, lookback_days: int) -> Auction | None:
    if series and series[-1].auction_date > as_of - timedelta(days=lookback_days):
        return series[-1]
    return None


def detect_yield_moves(m: MarketData) -> list[Draft]:
    r = RULES["yield_move"]
    out = []
    for series in m.completed.values():
        latest = _recent_latest(series, m.as_of, r["lookback_days"])
        if latest is None or len(series) < 2:
            continue
        prev = series[-2]
        bps = calc.change_bps(latest.weighted_average_yield, prev.weighted_average_yield)
        if bps is None or abs(bps) < r["threshold_bps"]:
            continue
        kind = "yield_move_up" if bps > 0 else "yield_move_down"
        out.append(Draft(
            dedup_key=f"yield_move:{latest.auction_id}",
            opportunity_type="yield_move",
            label=LABELS[kind],
            yield_pct=latest.weighted_average_yield,
            strength=_q(abs(bps) / r["threshold_bps"], 2),
            explanation=f"Weighted-average yield moved {bps:+.1f} bp versus the previous "
            f"{_tenor_label(latest.security.tenor_days)} auction ({prev.auction_date.isoformat()}).",
            evidence={
                "facts": [
                    _fact(latest, "weighted_average_yield", "WA yield (this auction)",
                          latest.weighted_average_yield, m.sources, "%"),
                    _fact(prev, "weighted_average_yield", "WA yield (previous auction)",
                          prev.weighted_average_yield, m.sources, "%"),
                ],
                "calculation": {
                    "formula": "(WA yield this auction − WA yield previous auction) × 100",
                    "result": str(_q(bps, 2)),
                    "unit": "bp",
                },
                "rule": {"description": f"|change| ≥ {r['threshold_bps']} bp", "threshold": str(r["threshold_bps"])},
                "invalidated_if": "A source correction to either auction's published yield.",
                "caveats": [],
            },
            risk_flags=_flags([latest, prev]),
            **_common(latest),
        ))
    return out


def detect_demand(m: MarketData) -> list[Draft]:
    r = RULES["demand"]
    out = []
    for series in m.completed.values():
        latest = _recent_latest(series, m.as_of, r["lookback_days"])
        if latest is None:
            continue
        peers = series[:-1][-r["max_peers"]:]
        peer_ratios = [
            x for p in peers if (x := calc.bid_to_cover(p.amount_submitted, p.amount_offered)) is not None
        ]
        if len(peer_ratios) < r["min_peers"]:
            continue
        ratio = calc.bid_to_cover(latest.amount_submitted, latest.amount_offered)
        z = calc.z_score(ratio, peer_ratios)
        if z is None or abs(z) < r["z_threshold"]:
            continue
        kind = "high_demand" if z > 0 else "low_demand"
        out.append(Draft(
            dedup_key=f"demand:{latest.auction_id}",
            opportunity_type=kind,
            label=LABELS[kind],
            yield_pct=latest.weighted_average_yield,
            strength=_q(abs(z) / r["z_threshold"], 2),
            explanation=f"Bid-to-cover of {ratio:.2f}× is {z:+.2f} standard deviations from the "
            f"previous {len(peer_ratios)} {_tenor_label(latest.security.tenor_days)} auctions "
            f"(mean {calc.mean(peer_ratios):.2f}×).",
            evidence={
                "facts": [
                    _fact(latest, "amount_submitted", "Amount submitted", latest.amount_submitted,
                          m.sources, latest.security.currency),
                    _fact(latest, "amount_offered", "Amount offered", latest.amount_offered,
                          m.sources, latest.security.currency),
                ],
                "calculation": {
                    "formula": "z = (bid_to_cover − mean(peer bid_to_cover)) / sample_stdev(peer bid_to_cover); "
                    "bid_to_cover = submitted / offered",
                    "inputs": {
                        "bid_to_cover": str(_q(ratio)),
                        "peer_mean": str(_q(calc.mean(peer_ratios))),
                        "peer_stdev": str(_q(calc.sample_stdev(peer_ratios))),
                        "peer_auction_ids": [p.auction_id for p in peers],
                    },
                    "result": str(_q(z, 2)),
                    "unit": "standard deviations",
                },
                "rule": {
                    "description": f"|z| ≥ {r['z_threshold']} against at least {r['min_peers']} previous "
                    f"auctions of the same country, instrument and tenor (up to {r['max_peers']}).",
                    "threshold": str(r["z_threshold"]),
                },
                "invalidated_if": "A source correction to submitted/offered amounts, or a different "
                "bid-to-cover definition (some issuers divide by the amount allocated).",
                "caveats": ["Small sample"] if len(peer_ratios) < 8 else [],
            },
            risk_flags=_flags([latest] + peers, ["small_sample"] if len(peer_ratios) < 8 else []),
            **_common(latest),
        ))
    return out


def detect_high_yield(m: MarketData) -> list[Draft]:
    r = RULES["high_yield"]
    out = []
    for series in m.completed.values():
        latest = _recent_latest(series, m.as_of, r["lookback_days"])
        if latest is None or latest.weighted_average_yield is None:
            continue
        start = m.as_of - timedelta(days=r["history_days"])
        history = [
            a.weighted_average_yield
            for a in series[:-1]
            if a.auction_date >= start and a.weighted_average_yield is not None
        ]
        if len(history) < r["min_history"]:
            continue
        pct = calc.percentile_rank(latest.weighted_average_yield, history)
        if pct is None or pct < r["percentile"]:
            continue
        out.append(Draft(
            dedup_key=f"high_yield:{latest.auction_id}",
            opportunity_type="high_yield",
            label=LABELS["high_yield"],
            yield_pct=latest.weighted_average_yield,
            strength=_q(pct / r["percentile"], 2),
            explanation=f"WA yield of {latest.weighted_average_yield:.3f}% is above {pct:.0f}% of the "
            f"{len(history)} previous {_tenor_label(latest.security.tenor_days)} auctions in the last "
            f"{r['history_days']} days. Higher yield is not a recommendation and usually reflects risk.",
            evidence={
                "facts": [_fact(latest, "weighted_average_yield", "WA yield (this auction)",
                                latest.weighted_average_yield, m.sources, "%")],
                "calculation": {
                    "formula": "percentile rank = (count below + ½ count equal) / n × 100",
                    "inputs": {"history_n": len(history), "history_min": str(min(history)),
                               "history_max": str(max(history))},
                    "result": str(_q(pct, 1)),
                    "unit": "percentile",
                },
                "rule": {"description": f"Percentile rank ≥ {r['percentile']} with ≥ {r['min_history']} "
                         "previous auctions of the same tenor.", "threshold": str(r["percentile"])},
                "invalidated_if": "Subsequent auctions print at higher yields, or the history window changes.",
                "caveats": ["Nominal yield; not adjusted for tax, fees, FX or credit risk."],
            },
            risk_flags=_flags([latest]),
            **_common(latest),
        ))
    return out


def latest_curve(m: MarketData, country_id: int) -> dict[int, Auction]:
    """Latest completed auction per original tenor within the curve lookback window."""
    lookback = RULES["curve_inversion"]["curve_lookback_days"]
    points: dict[int, Auction] = {}
    for (cid, _, tenor), series in m.completed.items():
        if cid != country_id or not series:
            continue
        last = series[-1]
        if last.auction_date > m.as_of - timedelta(days=lookback) and last.weighted_average_yield is not None:
            if tenor not in points or points[tenor].auction_date < last.auction_date:
                points[tenor] = last
    return dict(sorted(points.items()))


def detect_curve_inversions(m: MarketData) -> list[Draft]:
    r = RULES["curve_inversion"]
    out = []
    for country_id in {k[0] for k in m.completed}:
        curve = list(latest_curve(m, country_id).items())
        for (t_short, a_short), (t_long, a_long) in zip(curve, curve[1:]):
            gap = calc.change_bps(a_short.weighted_average_yield, a_long.weighted_average_yield)
            if gap is None or gap < r["threshold_bps"]:
                continue
            out.append(Draft(
                dedup_key=f"curve_inversion:{country_id}:{t_short}-{t_long}:{a_short.auction_id}:{a_long.auction_id}",
                opportunity_type="curve_inversion",
                label=LABELS["curve_inversion"],
                yield_pct=a_short.weighted_average_yield,
                strength=_q(gap / r["threshold_bps"], 2),
                explanation=f"The {_tenor_label(t_short)} auction yield is {gap:.1f} bp above the "
                f"{_tenor_label(t_long)} yield (latest auctions of each tenor).",
                evidence={
                    "facts": [
                        _fact(a_short, "weighted_average_yield", f"WA yield {_tenor_label(t_short)}",
                              a_short.weighted_average_yield, m.sources, "%"),
                        _fact(a_long, "weighted_average_yield", f"WA yield {_tenor_label(t_long)}",
                              a_long.weighted_average_yield, m.sources, "%"),
                    ],
                    "calculation": {
                        "formula": "(yield shorter tenor − yield next longer tenor) × 100",
                        "result": str(_q(gap, 2)),
                        "unit": "bp",
                    },
                    "rule": {"description": f"Shorter tenor yields ≥ {r['threshold_bps']} bp more than the "
                             "next longer tenor.", "threshold": str(r["threshold_bps"])},
                    "invalidated_if": "Either tenor auctions again at a level that removes the gap.",
                    "caveats": [
                        "Auction dates differ between the two points.",
                        "Bills and bonds may be quoted under different yield conventions.",
                    ],
                },
                risk_flags=_flags([a_short, a_long], ["different_auction_dates"]),
                **{**_common(a_short), "maturity": None},
            ))
    return out


def detect_refinancing(m: MarketData) -> list[Draft]:
    """Months where a disproportionate share of the next year's tracked maturities fall due."""
    r = RULES["refinancing"]
    out = []
    for country_id, wall in maturity_walls(m).items():
        total = sum((row["amount"] for row in wall["months"]), Decimal(0))
        if total == 0:
            continue
        average = total / len(wall["months"])
        for row in wall["months"]:
            share = row["amount"] / total * 100
            if share < r["min_share_pct"] or row["amount"] < average * r["multiple_of_average"]:
                continue
            out.append(Draft(
                dedup_key=f"refinancing:{country_id}:{row['month']}",
                opportunity_type="refinancing_concentration",
                label=LABELS["refinancing_concentration"],
                country_id=country_id,
                currency=wall["currency"],
                strength=_q(share / r["min_share_pct"], 2),
                explanation=f"{share:.1f}% of tracked maturities in the next 12 months fall due in "
                f"{row['month']} ({row['securities']} securities).",
                evidence={
                    "facts": [{"label": f"Allocated amounts maturing in {row['month']}",
                               "value": str(row["amount"]), "unit": wall["currency"],
                               "data_nature": wall["data_nature"], "security_ids": row["security_ids"]}],
                    "calculation": {
                        "formula": "share = Σ allocated maturing in month / Σ allocated maturing in next 12 months",
                        "inputs": {"month_total": str(row["amount"]), "twelve_month_total": str(total)},
                        "result": str(_q(share, 2)),
                        "unit": "%",
                    },
                    "rule": {"description": f"Share ≥ {r['min_share_pct']}% and ≥ "
                             f"{r['multiple_of_average']}× the monthly average.",
                             "threshold": str(r["min_share_pct"])},
                    "invalidated_if": "Buybacks, exchanges, or new data on debt not tracked here.",
                    "caveats": ["Covers only auctioned securities in this database — not Eurobonds, "
                                "loans or private placements."],
                },
                risk_flags=(["synthetic_data"] if wall["is_synthetic"] else []) + ["partial_debt_coverage"],
                is_synthetic=wall["is_synthetic"],
            ))
    return out


def maturity_walls(m: MarketData) -> dict[int, dict]:
    """Per country: allocated amounts of tracked securities maturing in each of the next 12 months."""
    horizon = m.as_of + timedelta(days=RULES["refinancing"]["horizon_days"])
    months = []
    y, mo = m.as_of.year, m.as_of.month
    for _ in range(12):
        months.append(f"{y:04d}-{mo:02d}")
        y, mo = (y + 1, 1) if mo == 12 else (y, mo + 1)

    by_security: dict[int, list[Auction]] = defaultdict(list)
    for series in m.completed.values():
        for a in series:
            by_security[a.security_id].append(a)

    walls: dict[int, dict] = {}
    for auctions in by_security.values():
        s = auctions[0].security
        if s.maturity_date is None or not (m.as_of < s.maturity_date <= horizon):
            continue
        key = s.maturity_date.strftime("%Y-%m")
        if key not in months:
            continue
        w = walls.setdefault(s.country_id, {
            "currency": s.currency, "is_synthetic": False, "data_nature": "FACT",
            "months": [{"month": mm, "amount": Decimal(0), "securities": 0, "security_ids": []} for mm in months],
        })
        row = next(r for r in w["months"] if r["month"] == key)
        row["amount"] += sum((a.amount_allocated or Decimal(0) for a in auctions), Decimal(0))
        row["securities"] += 1
        row["security_ids"].append(s.security_id)
        if any(a.is_synthetic for a in auctions):
            w["is_synthetic"] = True
            w["data_nature"] = "SYNTHETIC"
    return walls


DETECTORS = (
    detect_upcoming,
    detect_yield_moves,
    detect_demand,
    detect_high_yield,
    detect_curve_inversions,
    detect_refinancing,
)


def detect(session: Session, as_of: date) -> list[Draft]:
    m = load_market(session, as_of)
    drafts = [d for detector in DETECTORS for d in detector(m)]
    keys = [d.dedup_key for d in drafts]
    assert len(keys) == len(set(keys)), "dedup keys must be unique per run"
    return drafts


def run(session: Session, as_of: date) -> dict[str, int]:
    """Upsert detected signals; deactivate ones no longer detected. Idempotent per as_of."""
    drafts = detect(session, as_of)
    existing = {o.dedup_key: o for o in session.scalars(select(Opportunity))}
    created = updated = 0
    for d in drafts:
        values = {k: v for k, v in d.__dict__.items()}
        values["evidence"] = {**d.evidence, "rules_version": "phase4-v1", "as_of": as_of.isoformat()}
        opp = existing.pop(d.dedup_key, None)
        if opp is None:
            session.add(Opportunity(**values, as_of=as_of, is_active=True))
            created += 1
        else:
            for k, v in values.items():
                setattr(opp, k, v)
            opp.as_of = as_of
            opp.is_active = True
            updated += 1
    deactivated = 0
    for opp in existing.values():
        if opp.is_active:
            opp.is_active = False
            deactivated += 1
    session.flush()
    return {"detected": len(drafts), "created": created, "updated": updated, "deactivated": deactivated}
