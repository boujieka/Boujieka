"""Opportunity Engine tests.

Rule tests use a small hand-built market in its own database, so expected signals can be
worked out by hand. Statistics are checked against Python's `statistics` module.
"""

import statistics
from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.analytics import calculations as calc
from app.engine.opportunities import RULES, detect, run
from app.models import Auction, Base, Country, Issuer, Opportunity, Security
from app.models.enums import (
    AuctionStatus,
    AuctionType,
    InstrumentType,
    IssuerType,
    MonetaryZone,
    VerificationStatus,
)

D = Decimal
AS_OF = date(2026, 10, 3)


class TestStatistics:
    SAMPLES = [
        [D("1.2"), D("1.5"), D("1.1"), D("2.0"), D("1.7"), D("1.3")],
        [D("10"), D("10.5"), D("9.75"), D("11.25")],
        [D("0.66"), D("3.17"), D("1.09"), D("2.58"), D("1.55"), D("2.21"), D("1.44")],
    ]

    @pytest.mark.parametrize("xs", SAMPLES)
    def test_mean_and_stdev_match_statistics_module(self, xs):
        assert abs(calc.mean(xs) - statistics.mean(xs)) < D("1e-20")
        assert abs(calc.sample_stdev(xs) - statistics.stdev(xs)) < D("1e-20")

    @pytest.mark.parametrize("xs", SAMPLES)
    def test_z_score(self, xs):
        value = D("2.5")
        expected = (value - statistics.mean(xs)) / statistics.stdev(xs)
        assert abs(calc.z_score(value, xs) - expected) < D("1e-20")

    def test_z_score_undefined_cases(self):
        assert calc.z_score(D("1"), [D("1")]) is None
        assert calc.z_score(D("1"), [D("2"), D("2"), D("2")]) is None  # no dispersion
        assert calc.z_score(None, [D("1"), D("2")]) is None

    def test_percentile_rank(self):
        hist = [D(x) for x in range(1, 11)]  # 1..10
        assert calc.percentile_rank(D("10.5"), hist) == D(100)
        assert calc.percentile_rank(D("0"), hist) == D(0)
        assert calc.percentile_rank(D("5"), hist) == D(45)  # 4 below + ½ tie → 4.5 / 10
        assert calc.percentile_rank(None, hist) is None


# --------------------------------------------------------------------------- controlled market


def _auction(sec, day, offered, submitted, way, status=AuctionStatus.COMPLETED, **kw):
    return Auction(
        security_id=sec.security_id,
        auction_date=day,
        auction_type=AuctionType.PRIMARY_AUCTION,
        status=status,
        amount_offered=D(offered),
        amount_submitted=D(submitted) if submitted is not None else None,
        amount_allocated=D(offered) if submitted is not None else None,
        weighted_average_yield=D(way) if way is not None else None,
        yield_convention="test",
        verification_status=VerificationStatus.VERIFIED,
        confidence_score=D("0.95"),
        source_url="https://example.test/result.pdf",
        **kw,
    )


@pytest.fixture
def market():
    """One country, one 91-day bill series of 10 auctions, plus one upcoming auction.

    Peer bid-to-cover ratios: 1.4 1.6 1.5 1.5 1.4 1.6 1.5 1.5 1.5 → mean 1.5, stdev ≈ 0.0707.
    Latest auction: bid-to-cover 3.0 (z ≈ 21) and yield 9.00% vs previous 8.50% (+50 bp),
    above every earlier yield (percentile 100).
    """
    eng = create_engine("sqlite://")
    Base.metadata.create_all(eng)
    with Session(eng) as s:
        c = Country(name="Testland", iso2="TL", iso3="TLD", currency="TLC", monetary_zone=MonetaryZone.NONE)
        s.add(c)
        s.flush()
        i = Issuer(country_id=c.country_id, name="Gov", issuer_type=IssuerType.SOVEREIGN)
        s.add(i)
        s.flush()
        ratios = ["1.4", "1.6", "1.5", "1.5", "1.4", "1.6", "1.5", "1.5", "1.5", "3.0"]
        yields = ["8.10", "8.20", "8.15", "8.30", "8.25", "8.40", "8.35", "8.45", "8.50", "9.00"]
        for n, (ratio, y) in enumerate(zip(ratios, yields)):
            day = AS_OF - timedelta(days=7 * (len(ratios) - 1 - n) + 1)
            sec = Security(issuer_id=i.issuer_id, country_id=c.country_id,
                           instrument_type=InstrumentType.TREASURY_BILL, security_name=f"Bill {n}",
                           currency="TLC", tenor_days=91, maturity_date=day + timedelta(days=91))
            s.add(sec)
            s.flush()
            s.add(_auction(sec, day, "100", str(D(ratio) * 100), y))
        up = Security(issuer_id=i.issuer_id, country_id=c.country_id, instrument_type=InstrumentType.TREASURY_BILL,
                      security_name="Bill next", currency="TLC", tenor_days=91,
                      maturity_date=AS_OF + timedelta(days=96))
        s.add(up)
        s.flush()
        s.add(_auction(up, AS_OF + timedelta(days=5), "100", None, None, status=AuctionStatus.ANNOUNCED,
                       announcement_date=AS_OF - timedelta(days=2)))
        s.commit()
        yield s


def _by_type(drafts):
    out = {}
    for d in drafts:
        out.setdefault(d.opportunity_type, []).append(d)
    return out


class TestRules:
    def test_expected_signals_fire(self, market):
        found = _by_type(detect(market, AS_OF))
        assert set(found) >= {"high_demand", "yield_move", "high_yield", "upcoming_auction"}
        assert "low_demand" not in found

    def test_demand_z_matches_hand_calculation(self, market):
        d = _by_type(detect(market, AS_OF))["high_demand"][0]
        peers = [D(x) for x in ["1.4", "1.6", "1.5", "1.5", "1.4", "1.6", "1.5", "1.5", "1.5"]]
        expected = (D("3.0") - statistics.mean(peers)) / statistics.stdev(peers)
        assert D(d.evidence["calculation"]["result"]) == calc.quantize(expected, 2)
        assert d.label == "High demand relative to recent auctions"

    def test_yield_move(self, market):
        d = _by_type(detect(market, AS_OF))["yield_move"][0]
        assert D(d.evidence["calculation"]["result"]) == D("50.00")
        assert d.label == "Significant yield movement (higher)"
        assert d.strength == D("2.00")  # 50 bp / 25 bp threshold

    def test_high_yield_percentile(self, market):
        d = _by_type(detect(market, AS_OF))["high_yield"][0]
        assert D(d.evidence["calculation"]["result"]) == D("100.0")

    def test_upcoming_uses_previous_result_not_a_forecast(self, market):
        d = _by_type(detect(market, AS_OF))["upcoming_auction"][0]
        assert d.label == "Newly announced auction"  # announced 2 days ago
        assert d.yield_pct == D("9.00")  # last published result of the same tenor
        assert "not a forecast" in d.explanation

    def test_threshold_is_respected(self, market, monkeypatch):
        monkeypatch.setitem(RULES["yield_move"], "threshold_bps", D(60))
        assert "yield_move" not in _by_type(detect(market, AS_OF))

    def test_too_few_peers_means_no_demand_signal(self, market, monkeypatch):
        monkeypatch.setitem(RULES["demand"], "min_peers", 20)
        assert "high_demand" not in _by_type(detect(market, AS_OF))

    def test_run_is_idempotent_and_deactivates(self, market):
        first = run(market, AS_OF)
        second = run(market, AS_OF)
        assert first["created"] == first["detected"] > 0
        assert second == {"detected": first["detected"], "created": 0,
                          "updated": first["detected"], "deactivated": 0}
        # Remove the spike: the demand signal must be deactivated, not deleted.
        spike = market.scalars(select(Auction).order_by(Auction.auction_date.desc())
                               .where(Auction.status == AuctionStatus.COMPLETED)).first()
        spike.amount_submitted = D("150")
        market.flush()
        third = run(market, AS_OF)
        assert third["deactivated"] >= 1
        demand = market.scalars(select(Opportunity).where(Opportunity.opportunity_type == "high_demand")).one()
        assert demand.is_active is False


class TestPassportOnSeededData:
    """Every active signal on the seeded dataset must carry a complete, truthful passport."""

    @pytest.fixture
    def signals(self, db):
        run(db, AS_OF)
        return db.scalars(select(Opportunity).where(Opportunity.is_active.is_(True))).all()

    def test_signals_exist(self, signals):
        assert len(signals) > 10

    def test_passport_complete(self, signals):
        for o in signals:
            ev = o.evidence
            assert ev["facts"], o.dedup_key
            assert ev["rule"]["description"]
            assert ev["invalidated_if"]
            assert ev["rules_version"] and ev["as_of"] == AS_OF.isoformat()

    def test_facts_match_database_values(self, db, signals):
        checked = 0
        for o in signals:
            for f in o.evidence["facts"]:
                if "auction_id" not in f or f.get("field") == "status":
                    continue
                a = db.get(Auction, f["auction_id"])
                stored = getattr(a, f["field"])
                assert f["value"] == (None if stored is None else str(stored)), (o.dedup_key, f)
                assert f["data_nature"] == a.data_nature.value
                checked += 1
        assert checked > 20

    def test_synthetic_inputs_are_flagged(self, signals):
        assert all(o.is_synthetic and "synthetic_data" in o.risk_flags for o in signals)

    def test_neutral_language(self, signals):
        for o in signals:
            text = f"{o.label} {o.explanation}".lower()
            for banned in ("best", "buy", "sell", "guarantee", "recommend "):
                assert banned not in text, (banned, o.dedup_key)
