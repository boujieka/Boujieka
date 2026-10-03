from datetime import date
from decimal import Decimal
from fractions import Fraction

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.models import Auction, Country, Issuer, Security, Source
from app.models.enums import (
    AuctionStatus,
    AuctionType,
    DataNature,
    InstrumentType,
    SourceStatus,
    VerificationStatus,
)
from app.seed import synthetic
from app.seed.load import load_reference, load_synthetic
from tests.conftest import REFERENCE_DATE


@pytest.fixture(scope="module")
def generated():
    return synthetic.generate(REFERENCE_DATE)


def all_auctions(gen):
    return [(iso3, s, a) for iso3, series in gen.items() for s in series for a in s["auctions"]]


class TestSyntheticGenerator:
    def test_deterministic(self, generated):
        again = synthetic.generate(REFERENCE_DATE)
        assert [s["local_code"] for v in again.values() for s in v] == [
            s["local_code"] for v in generated.values() for s in v
        ]

    def test_every_security_is_labelled(self, generated):
        for series in generated.values():
            for s in series:
                assert s["security_name"].startswith("[SYNTHETIC]")
                assert s["local_code"].startswith("SYN-")

    def test_upcoming_auctions_have_no_results(self, generated):
        for _, _, a in all_auctions(generated):
            if a["auction_date"] > REFERENCE_DATE:
                assert a["status"] != AuctionStatus.COMPLETED
                assert a["weighted_average_yield"] is None
                if a["status"] == AuctionStatus.ANNOUNCED:
                    assert a["field_status"]["weighted_average_yield"] == "pending"

    def test_completed_results_are_internally_consistent(self, generated):
        completed = [a for _, _, a in all_auctions(generated) if a["status"] == AuctionStatus.COMPLETED]
        assert completed
        for a in completed:
            assert a["auction_date"] <= REFERENCE_DATE
            assert a["minimum_bid"] <= a["weighted_average_yield"] <= a["cutoff_yield"] <= a["maximum_bid"]
            assert a["amount_allocated"] <= a["amount_submitted"]
            if a["number_of_bidders"] is not None:
                assert a["number_of_successful_bidders"] <= a["number_of_bidders"]

    def test_bill_price_matches_yield(self, generated):
        """Independent check: price = 100 / (1 + y * d / 360) using exact fractions."""
        checked = 0
        for _, s, a in all_auctions(generated):
            if s["instrument_type"] == InstrumentType.TREASURY_BILL and a.get("average_price"):
                days = (s["maturity_date"] - a["settlement_date"]).days
                expected = Fraction(100) / (
                    1 + Fraction(a["weighted_average_yield"]) / 100 * Fraction(days, 360)
                )
                assert abs(Fraction(a["average_price"]) - expected) <= Fraction(1, 2_000_000)
                checked += 1
        assert checked > 100

    def test_bond_reopenings_share_security(self, generated):
        for series in generated.values():
            bonds = [s for s in series if s["instrument_type"] == InstrumentType.TREASURY_BOND]
            for b in bonds:
                types = [a["auction_type"] for a in b["auctions"]]
                assert types[0] == AuctionType.PRIMARY_AUCTION
                assert all(t == AuctionType.REOPENING for t in types[1:])

    def test_covers_all_54_countries(self, generated):
        assert len(generated) == 54
        assert all(series for series in generated.values())

    def test_rolling_forward_keeps_the_past(self, generated):
        """A later as-of date must not rewrite history, only add auctions and results."""
        from datetime import timedelta

        later = synthetic.generate(REFERENCE_DATE + timedelta(days=7))
        key = lambda s, a: (s["local_code"], a["auction_date"])  # noqa: E731
        before = {key(s, a): a for v in generated.values() for s in v for a in s["auctions"]}
        after = {key(s, a): a for v in later.values() for s in v for a in s["auctions"]}
        assert set(before) <= set(after)
        transitions = 0
        for k, a in before.items():
            if a["status"] == AuctionStatus.COMPLETED:
                assert after[k]["weighted_average_yield"] == a["weighted_average_yield"]
            elif a["status"] == AuctionStatus.ANNOUNCED and after[k]["status"] == AuctionStatus.COMPLETED:
                transitions += 1
        assert transitions > 0

    def test_non_mvp_anchors_are_hash_derived(self):
        from app.models.enums import MonetaryZone

        a1, _, _ = synthetic.country_profile("NGA", MonetaryZone.NONE)
        a2, _, _ = synthetic.country_profile("NGA", MonetaryZone.NONE)
        assert a1 == a2 and 4.0 <= a1 <= 14.0

    def test_cancelled_and_postponed_examples(self, generated):
        statuses = {a["status"] for _, _, a in all_auctions(generated)}
        assert {AuctionStatus.CANCELLED, AuctionStatus.POSTPONED} <= statuses


class TestSeedLoader:
    def test_idempotent(self, db):
        before = db.scalar(select(func.count()).select_from(Auction))
        countries = load_reference(db)
        assert load_synthetic(db, countries, REFERENCE_DATE) == 0
        assert db.scalar(select(func.count()).select_from(Auction)) == before
        assert db.scalar(select(func.count()).select_from(Country)) == 54

    def test_reference_data_is_unverified_not_synthetic(self, db):
        for c in db.scalars(select(Country)):
            assert c.verification_status == VerificationStatus.UNVERIFIED
            assert c.is_synthetic is False
            assert c.confidence_score is None
            assert c.provenance_notes

    def test_no_guessed_source_urls(self, db):
        for s in db.scalars(select(Source).where(Source.is_synthetic.is_(False))):
            assert s.base_url is None
            assert s.status == SourceStatus.PENDING_CONFIGURATION

    def test_all_seeded_market_data_is_synthetic(self, db):
        assert db.scalar(select(func.count()).select_from(Auction).where(Auction.is_synthetic.is_(False))) == 0
        assert db.scalar(select(func.count()).select_from(Security).where(Security.is_synthetic.is_(False))) == 0


class TestConstraints:
    def _security(self, db) -> Security:
        return db.scalars(select(Security)).first()

    def test_unlabelled_synthetic_rejected(self, db):
        sec = self._security(db)
        db.add(
            Auction(
                security_id=sec.security_id,
                auction_date=date(2030, 1, 1),
                auction_type=AuctionType.PRIMARY_AUCTION,
                status=AuctionStatus.ANNOUNCED,
                is_synthetic=True,
                data_nature=DataNature.FACT,  # claims to be a fact: must be refused
                verification_status=VerificationStatus.VERIFIED,
            )
        )
        with pytest.raises(IntegrityError):
            db.flush()

    def test_duplicate_auction_rejected(self, db):
        existing = db.scalars(select(Auction)).first()
        db.add(
            Auction(
                security_id=existing.security_id,
                auction_date=existing.auction_date,
                auction_type=existing.auction_type,
                status=AuctionStatus.ANNOUNCED,
                **synthetic.SYNTHETIC_PROVENANCE,
            )
        )
        with pytest.raises(IntegrityError):
            db.flush()

    def test_confidence_out_of_range_rejected(self, db):
        sec = self._security(db)
        db.add(
            Auction(
                security_id=sec.security_id,
                auction_date=date(2030, 1, 2),
                auction_type=AuctionType.PRIMARY_AUCTION,
                status=AuctionStatus.ANNOUNCED,
                confidence_score=Decimal("1.5"),
            )
        )
        with pytest.raises(IntegrityError):
            db.flush()

    def test_negative_amount_rejected(self, db):
        sec = self._security(db)
        db.add(
            Auction(
                security_id=sec.security_id,
                auction_date=date(2030, 1, 3),
                auction_type=AuctionType.PRIMARY_AUCTION,
                status=AuctionStatus.ANNOUNCED,
                amount_offered=Decimal("-1"),
            )
        )
        with pytest.raises(IntegrityError):
            db.flush()

    def test_real_record_defaults_to_unverified_fact(self, db):
        country = db.scalars(select(Country)).first()
        issuer = db.scalars(select(Issuer)).first()
        sec = Security(
            issuer_id=issuer.issuer_id,
            country_id=country.country_id,
            instrument_type=InstrumentType.TREASURY_BILL,
            security_name="Test bill",
            currency=country.currency,
        )
        db.add(sec)
        db.flush()
        assert sec.data_nature == DataNature.FACT
        assert sec.verification_status == VerificationStatus.UNVERIFIED
        assert sec.is_synthetic is False


class TestSourceCandidates:
    def test_candidates_reference_registered_sources(self):
        from app.seed.reference import SOURCES
        from app.seed.source_candidates import CANDIDATES

        names = {name for name, *_ in SOURCES}
        assert set(CANDIDATES) <= names

    def test_candidates_are_https_and_carry_evidence(self):
        from app.seed.source_candidates import CANDIDATES

        for entries in CANDIDATES.values():
            for c in entries:
                assert c["url"].startswith("https://")
                assert c["check"] in {"http_200", "http_403", "search_only"}
                assert c["evidence"] and c["purpose"]

    def test_candidates_loaded_but_never_promoted(self, db):
        source = db.scalar(select(Source).where(Source.name.like("BEAC%")))
        assert source.candidates and source.base_url is None
        assert source.status == SourceStatus.PENDING_CONFIGURATION
        # Re-running the loader keeps exactly one copy of the candidates.
        load_reference(db)
        assert len(source.candidates) == len({c["url"] for c in source.candidates})



class TestAfricaReference:
    def test_54_unique_countries(self):
        from app.seed.africa import AFRICA

        assert len(AFRICA) == 54
        for attr in ("iso3", "iso2", "tile"):
            assert len({getattr(c, attr) for c in AFRICA}) == 54, attr

    def test_codes_are_well_formed(self):
        from app.seed.africa import AFRICA

        for c in AFRICA:
            assert len(c.iso3) == 3 and c.iso3.isupper()
            assert len(c.iso2) == 2 and c.iso2.isupper()
            assert len(c.currency) == 3 and c.currency.isupper()
            assert c.region in {"north", "west", "central", "east", "southern"}

    def test_cfa_zones_consistent(self):
        from app.models.enums import MonetaryZone
        from app.seed.africa import AFRICA

        for c in AFRICA:
            if c.zone == MonetaryZone.CEMAC:
                assert c.currency == "XAF" and "BEAC" in c.central_bank
            elif c.zone == MonetaryZone.WAEMU:
                assert c.currency == "XOF" and "BCEAO" in c.central_bank
            else:
                assert c.currency not in ("XAF", "XOF")
        zones = [c.zone for c in AFRICA]
        assert zones.count(MonetaryZone.CEMAC) == 6 and zones.count(MonetaryZone.WAEMU) == 8


class TestSubscriptionRouteSources:
    def test_sources_are_verified_official_pages(self):
        """Each route cites a page whose URL is among the checked official candidates or pages read
        on the verification date."""
        from app.seed import subscription_routes as sr

        allowed = {sr.BEAC_URL, sr.UMOA_MARKET_URL, sr.UMOA_RETAIL_URL, sr.CBK_BILLS_URL}
        for r in sr.ZONE_ROUTES + sr.COUNTRY_ROUTES:
            assert r["source_url"] in allowed
            assert r["quotes"]

    def test_loader_is_idempotent(self, db):
        from app.models import SubscriptionRoute
        from app.seed.load import load_reference

        before = db.scalar(select(func.count()).select_from(SubscriptionRoute))
        load_reference(db)
        assert db.scalar(select(func.count()).select_from(SubscriptionRoute)) == before == 30
