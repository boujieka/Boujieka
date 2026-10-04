"""BVMAC Bulletin officiel de la cote: parser, strict checks, promotion, verified export/load.

Fixtures are real BOC texts (pdftotext -layout and -raw), see tests/fixtures/bvmac/SOURCES.txt.
"""

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.ingest import bvmac, bvmac_check
from app.ingest.bvmac_extract import EXTRACTOR, TIE_BREAK_NOTE, Tok, coupon_in_name, decode, isin_valid, parse, quote_constraints
from app.ingest.pdf import PdfText
from app.ingest.umoa import Fetched
from app.models import Base, BvmacQuote, Issuer, MarketObservation, Security, Source
from app.models.enums import InstrumentType, IssuerType, ObservationKind, VerificationStatus

FIX = Path(__file__).parent / "fixtures" / "bvmac"
DOCS = {
    "BOC-20261001": ("2026/10", "01 octobre 2026"),
    "BOC-20250731": ("2025/07", "31 juillet 2025"),
    "BOC-20240731": ("2024/07", "31 juillet 2024"),
    "BOC-20240103": ("2024/01", "03 janvier 2024"),
}


def text(name: str, mode: str) -> str:
    return (FIX / f"{name}.{mode}.txt").read_text(encoding="utf-8")


def url(name: str) -> str:
    return f"https://www.bvm-ac.org/wp-content/uploads/{DOCS[name][0]}/{name}.pdf"


# --------------------------------------------------------------------------- parser


class TestIsin:
    def test_check_digit(self):
        for isin in ("CM0000020305", "GA0000020636", "CG0000020444", "TD0000020331", "US0378331005"):
            assert isin_valid(isin), isin

    def test_wrong_digit_or_shape(self):
        assert not isin_valid("CM0000020306")
        assert not isin_valid("GA000002063")
        assert not isin_valid("ga0000020636")


class TestNumberGrammar:
    def test_ambiguous_order_book_is_left_out(self):
        # "10 100 100": demanded/offered could be (10 100 | 100) or (10 | 100 100).
        toks = [Tok(t, 1, i) for i, t in enumerate("0 10 100 100 0 0 0".split())]
        toks[-1].line_end = True
        spec = [("x", "num"), ("volume_demanded", "num"), ("volume_offered", "num"), ("volume_traded", "num"),
                ("value_traded", "num"), ("trades", "num")]
        decoded, total, _ = decode(toks, spec, "raw", lambda v: True)
        assert total >= 2 and len({d["volume_demanded"][0] for d in decoded}) == 2

    def test_order_book_identities_remove_readings(self):
        # "500 500 500 5 003 835 1": only one reading keeps traded <= demanded/offered.
        toks = [Tok(t, 1, i) for i, t in enumerate("500 500 500 5 003 835 1".split())]
        toks[-1].line_end = True
        spec = [("volume_demanded", "num"), ("volume_offered", "num"), ("volume_traded", "num"),
                ("value_traded", "num"), ("trades", "num")]
        decoded, total, _ = decode(toks, spec, "raw", quote_constraints)
        assert total > 1
        assert len(decoded) == 1 and decoded[0]["value_traded"][1] == "5 003 835"

    def test_coupon_in_name(self):
        assert coupon_in_name("EOG MT 6,60% NET 2024-2027") == Decimal("6.60")
        assert coupon_in_name("ECMR7 5,8% NET 2023-2026") == Decimal("5.8")
        assert coupon_in_name("BDEAC 5.45% NET 2020 - 2027") == Decimal("5.45")
        assert coupon_in_name("NO COUPON") is None


class TestLayout2026:
    @pytest.fixture(scope="class")
    def doc(self):
        return parse(text("BOC-20261001", "layout"), "layout")

    def test_document(self, doc):
        assert doc.layout == EXTRACTOR
        assert (doc.boc_number, doc.session_date) == ("2607", date(2026, 10, 1))
        assert doc.declared_lines == 31 and len(doc.quotes) == 31 and len(doc.characteristics) == 31
        assert doc.summary_digits == "500500383517"  # OBLIGATIONS 500 5 003 835 1 7
        assert doc.totals["sovereign"].digits == "50050038351"

    def test_sections_and_issuers(self, doc):
        sections = [q.section for q in doc.quotes.values()]
        assert sections.count("sovereign") == 20 and sections.count("regional") == 6 and sections.count("private") == 5
        q = doc.quotes["TD0000020331"]
        assert (q.issuer, q.name, q.country_iso3) == ("ETAT DU TCHAD", "EOTD 6.5% NET 2022-2027", "TCD")
        q = doc.quotes["CG0000020584"]
        assert (q.issuer, q.name, q.section) == ("SNPC", "SNPC 6,5% NET 2024-2029", "private")
        q = doc.quotes["CG0000020444"]
        assert (q.issuer, q.section) == ("BDEAC", "regional")

    def test_name_running_into_isin_column(self, doc):
        q = doc.quotes["GA0000020560"]  # printed "EOG MT 6,75% NET 2024-2028-IIGA0000020560"
        assert q.name == "EOG MT 6,75% NET 2024-2028-II" and not q.errors

    def test_traded_line(self, doc):
        q = doc.quotes["GA0000020636"]
        assert not q.errors and q.readings_kept == 1
        raw = {k: v.raw for k, v in q.fields.items()}
        assert raw == {
            "mnemo": "EGA20", "previous_price_date": "30/09/2026", "previous_price_pct": "100,00",
            "previous_price_fcfa": "10 000,00", "nominal": "10 000,000", "accrued_coupon": "7,67",
            "volume_demanded": "500", "volume_offered": "500", "volume_traded": "500",
            "value_traded": "5 003 835", "trades": "1", "status": "PEq", "open_price_pct": "100,00",
            "close_price_pct": "100,00", "upper_limit_pct": "106,00", "lower_limit_pct": "94,00",
            "variation_pct": "0,00%", "next_reference_price_fcfa": "10 000,00"}
        assert q.v("value_traded") == Decimal("5003835")
        assert q.fields["close_price_pct"].locator.startswith(f"p{q.page}:L{q.line_no} t")

    def test_untraded_line(self, doc):
        q = doc.quotes["CG0000020261"]
        assert q.v("status") == "NC" and q.v("volume_traded") == 0 and q.v("volume_offered") == 5000
        assert q.v("previous_price_pct") == Decimal("98.50") and q.v("nominal") == Decimal("6000.000")

    def test_characteristics(self, doc):
        for isin, c in doc.characteristics.items():
            assert c.v("coupon_rate") == coupon_in_name(doc.quotes[isin].name), isin
            assert c.v("periodicity") in ("AN", "SEM", "TRIM")
        c = doc.characteristics["GA0000020487"]
        assert c.v("amortization") == "IN FINE" and c.v("outstanding_amount") == Decimal("109889950000")
        assert c.v("next_payment_date") == date(2027, 3, 29)

    def test_equities_ignored(self, doc):
        assert "CM0000010009" not in doc.quotes and "GQ0000010050" not in doc.quotes


@pytest.mark.parametrize("name", list(DOCS))
def test_layout_and_raw_agree(name):
    lay, raw = parse(text(name, "layout"), "layout"), parse(text(name, "raw"), "raw")
    assert lay.layout == raw.layout == EXTRACTOR
    assert lay.session_date == raw.session_date and lay.summary_digits == raw.summary_digits
    assert set(lay.quotes) == set(raw.quotes) and set(lay.characteristics) == set(raw.characteristics)
    for isin, q in lay.quotes.items():
        r = raw.quotes[isin]
        assert not q.errors and not r.errors, (isin, q.errors, r.errors)
        assert {k: v.value for k, v in q.fields.items()} == {k: v.value for k, v in r.fields.items()}, isin
        assert r.prefix_compact.endswith((q.issuer + q.name).replace(" ", "").upper().replace("É", "E"))


def test_raw_line_breaks_inside_isin_and_mnemo():
    raw = parse(text("BOC-20250731", "raw"), "raw")
    assert raw.quotes["GA0000020313"].v("mnemo") == "EGA07"  # "GA000002031⏎3 EGA07"
    assert raw.quotes["GA0000020511"].v("mnemo") == "EGA12"  # "GA000002051⏎1 EGA1⏎2"
    lay = parse(text("BOC-20250731", "layout"), "layout")
    assert lay.quotes["CM0000020305"].v("mnemo") == "ECMR6"  # printed "ECM R6"


def test_single_spaced_order_book_tie_break():
    # Real line of BOC n° 1932 (19/01/2024, https://www.bvm-ac.org/wp-content/uploads/2024/01/BOC-20240119.pdf):
    # "500 000 500 000 500 000 5 198 260 000" has several readings; only one satisfies
    # value = traded x (close % x nominal / 100 + accrued coupon) = 500 000 x (10 000 + 396,52).
    line = ("ETAT DU CAMEROUN ECMR 6,75% NET 2023-2029 CM0000020370 ECMR9 18/01/2024 100 10 000,00 10 000,000"
            "                                          396,52 500 000 500 000 500 000 5 198 260 000"
            "                        1 PEq 100,00 100,00 106,00 94,00                0,00% 10 000,00")
    doc = parse("MARCHE DES OBLIGATIONS\nOBLIGATIONS DES ETATS\n" + line + "\n", "layout")
    q = doc.quotes["CM0000020370"]
    assert not q.errors and TIE_BREAK_NOTE in q.notes  # tie-break recorded
    assert (q.v("volume_traded"), q.v("value_traded")) == (Decimal("500000"), Decimal("5198260000"))
    # When no reading satisfies the identity, the readings are left as they are: still ambiguous
    # -> the columns are not read (held), nothing is guessed.
    bad = parse("MARCHE DES OBLIGATIONS\nOBLIGATIONS DES ETATS\n" + line.replace("5 198 260 000", "5 198 360 000") + "\n",
                "layout").quotes["CM0000020370"]
    assert TIE_BREAK_NOTE not in bad.notes and any("possible readings" in e for e in bad.errors) and "volume_traded" not in bad.fields


def test_old_layout_without_isin_is_unsupported():
    old = ("BULLETIN OFFICIEL DE LA COTE N° 700 DU 27/06/2022\nMARCHE DES OBLIGATIONS\n"
           " 2010      ECMR.05-18/23        5 000        99,20          99,20        174,14   0  0  0  0,000  NC\n")
    assert parse(old, "layout").layout == "unsupported"


# --------------------------------------------------------------------------- pipeline


def listing_html(names) -> bytes:
    items = "".join(f'<li><a href="{url(n)}">BOC Séance de cotation du {DOCS[n][1]}</a></li>' for n in names)
    return f"<html><body><ul>{items}<li><a href=\"https://https://x/BOC-1.pdf\">BOC x</a></li></ul></body></html>".encode()


class FakeSite:
    """Serves the listing and fake PDF bytes; text extraction is patched to the fixture texts."""

    def __init__(self, names, tamper=None):
        self.names = list(names)
        self.bytes = {n: f"%PDF-1.4 fixture {n}".encode() for n in names}
        self.tamper = tamper or (lambda name, mode, t: t)
        self.calls: list[str] = []

    def fetch(self, u: str) -> Fetched:
        self.calls.append(u)
        if u == bvmac.LISTING_URL:
            return Fetched(200, u, listing_html(self.names), "text/html")
        for n in self.names:
            if u == url(n):
                return Fetched(200, u, self.bytes[n], "application/pdf")
        return Fetched(404, u, b"", None)

    def name_of(self, content: bytes) -> str:
        return next(n for n, b in self.bytes.items() if b == content)

    def install(self, monkeypatch):
        monkeypatch.setattr(bvmac, "extract_text", lambda content: PdfText(
            self.tamper(self.name_of(content), "layout", text(self.name_of(content), "layout")), "pdftotext-layout"))
        monkeypatch.setattr(bvmac_check, "pdf_text",
                            lambda content, mode: self.tamper(self.name_of(content), mode,
                                                              text(self.name_of(content), mode)))


@pytest.fixture
def store(tmp_path, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "document_store_dir", str(tmp_path / "docs"))
    return tmp_path / "docs"


def ingest(db, site, monkeypatch, **kw):
    site.install(monkeypatch)
    stats = bvmac.run(db, fetch=site.fetch, pause=0, **kw)
    report = bvmac_check.run(db, fetch=site.fetch, pause=0)
    return stats, report


class TestPipeline:
    def test_run_check_and_promote(self, db, store, monkeypatch):
        site = FakeSite(["BOC-20261001", "BOC-20240731"])
        stats, report = ingest(db, site, monkeypatch)
        assert stats["selected"] == 2 and stats["documents_new"] == 2 and stats["rows_staged"] == 31 + 16
        assert stats["links_malformed"] == 1
        assert report["rows_checked"] == 47 and report["verified"] == 47 and not report["held"], report["held"]
        assert report["observations_created"] == 2
        source = db.scalar(select(Source).where(Source.name == bvmac.SOURCE_NAME))
        assert source.category.value == "stock_exchange" and "authorisation" in source.notes

        obs = db.scalars(select(MarketObservation).where(MarketObservation.source_id == source.source_id)
                         .order_by(MarketObservation.observation_date)).all()
        assert [(o.observation_date, Decimal(o.price), Decimal(o.volume)) for o in obs] == [
            (date(2024, 7, 31), Decimal("100"), Decimal("303596")),
            (date(2026, 10, 1), Decimal("100"), Decimal("5003835"))]
        for o in obs:
            assert o.kind == ObservationKind.SECONDARY_MARKET and o.yield_pct is None
            assert o.verification_status == VerificationStatus.VERIFIED and o.field_status["yield"] == "not_disclosed"
            assert o.source_url and o.source_document_id and "Clôt." in o.provenance_notes

        sec = db.scalar(select(Security).where(Security.isin == "GA0000020636"))
        assert sec.instrument_type == InstrumentType.REGIONAL_BOND and sec.currency == "XAF"
        assert sec.coupon_rate == Decimal("5.6") and sec.maturity_date is None
        assert sec.field_status["maturity_date"] == "not_disclosed"
        assert sec.verification_status == VerificationStatus.VERIFIED
        types = {i.name: i.issuer_type for i in db.scalars(select(Issuer).join(Security, Security.issuer_id == Issuer.issuer_id)
                                                          .where(Security.source_id == source.source_id))}
        assert types["BDEAC"] == IssuerType.SUPRANATIONAL and types["SNPC"] == IssuerType.CORPORATE
        assert types["Government of Gabon"] == IssuerType.SOVEREIGN
        # A bond that did not trade gets a security but never an observation (stale "NC" price).
        nc = db.scalar(select(Security).where(Security.isin == "CG0000020261"))
        assert db.scalar(select(MarketObservation).where(MarketObservation.security_id == nc.security_id)) is None

    def test_idempotent(self, db, store, monkeypatch):
        site = FakeSite(["BOC-20261001"])
        ingest(db, site, monkeypatch)
        stats, report = ingest(db, site, monkeypatch)
        assert stats["skipped_known_url"] == 1 and stats["rows_staged"] == 0 and report["rows_checked"] == 0

    def test_readings_disagree_is_held(self, db, store, monkeypatch):
        def tamper(name, mode, t):  # the raw reading prints another value traded
            return t.replace("500 500 500 5 003 835 1", "500 500 500 5 003 836 1") if mode == "raw" else t

        site = FakeSite(["BOC-20261001"], tamper)
        _, report = ingest(db, site, monkeypatch)
        held = {h["isin"]: h for h in report["held"]}
        assert set(held) == {"GA0000020636"} and report["observations_created"] == 0
        assert any(p.startswith("agree:value_traded") for p in held["GA0000020636"]["problems"])
        row = db.scalar(select(BvmacQuote).where(BvmacQuote.isin == "GA0000020636"))
        assert row.verification_status == VerificationStatus.UNVERIFIED and row.hold_reasons

    def test_inconsistent_value_is_held(self, db, store, monkeypatch):
        def tamper(name, mode, t):  # both readings print a value that does not match volume x price
            return t.replace("5 003 835", "5 003 935")

        site = FakeSite(["BOC-20261001"], tamper)
        _, report = ingest(db, site, monkeypatch)
        problems = {h["isin"]: h["problems"] for h in report["held"]}["GA0000020636"]
        assert not any(p.startswith("agree:") for p in problems), problems  # both readings say the same…
        assert any(p.startswith("value_traded") for p in problems)  # …but it is not volume x price
        assert db.scalar(select(MarketObservation).where(MarketObservation.observation_date == date(2026, 10, 1))) is None

    def test_section_total_must_match(self, db, store, monkeypatch):
        def tamper(name, mode, t):  # only the sovereign "Total" line of the layout text changes
            return t.replace("Total          500     5 003 835          1", "Total          500     5 003 836          1")

        site = FakeSite(["BOC-20261001"], tamper)
        _, report = ingest(db, site, monkeypatch)
        held = {h["isin"]: h["problems"] for h in report["held"]}
        assert set(held) == {"GA0000020636"}  # lines that did not trade do not depend on the totals
        assert any(p.startswith("section_total") for p in held["GA0000020636"])

    def test_changed_document_is_held(self, db, store, monkeypatch):
        site = FakeSite(["BOC-20261001"])
        site.install(monkeypatch)
        bvmac.run(db, fetch=site.fetch, pause=0)
        site.bytes["BOC-20261001"] = b"%PDF-1.4 republished"
        report = bvmac_check.run(db, fetch=site.fetch, pause=0)
        assert report["verified"] == 0 and len(report["held"]) == 31
        assert "SHA-256" in report["document_errors"][0]["error"]

    def test_listing_date_must_match_header(self, db, store, monkeypatch):
        site = FakeSite(["BOC-20261001"])
        site.install(monkeypatch)
        monkeypatch.setitem(DOCS, "BOC-20261001", ("2026/10", "02 octobre 2026"))
        bvmac.run(db, fetch=site.fetch, pause=0)
        report = bvmac_check.run(db, fetch=site.fetch, pause=0)
        assert report["verified"] == 0
        assert all(any(p.startswith("session_date") for p in h["problems"]) for h in report["held"])


def test_verified_export_and_load_roundtrip(db, store, monkeypatch, tmp_path):
    from app.seed import verified
    from app.seed.load import load_reference

    site = FakeSite(["BOC-20261001"])
    ingest(db, site, monkeypatch)
    out = tmp_path / "verified.json"
    counts = verified.export(db, out)
    assert counts["market_observations"] == 1 and counts["securities"] >= 31

    eng = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(eng)
    with Session(eng) as fresh:
        load_reference(fresh)
        added = verified.load(fresh, out)
        assert added["market_observations"] == 1 and added["securities"] == counts["securities"]
        assert verified.load(fresh, out) == {"documents": 0, "securities": 0, "auctions": 0, "market_observations": 0}
        o = fresh.scalar(select(MarketObservation))
        sec = fresh.get(Security, o.security_id)
        assert sec.isin == "GA0000020636" and Decimal(o.volume) == Decimal("5003835")
        assert fresh.scalar(select(Issuer).where(Issuer.name == "SNPC")).issuer_type == IssuerType.CORPORATE
        assert fresh.scalar(select(Source).where(Source.name == bvmac.SOURCE_NAME)) is not None
    eng.dispose()
