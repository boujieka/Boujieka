"""Phase 2 ingestion: UMOA-Titres result reports → staging → human review → VERIFIED facts.

Every expected value below was read by hand from the official document named in the test
(all are one-page PDFs, so "p1"); see tests/fixtures/umoa/SOURCES.txt for URLs and hashes.
"""

import contextlib
import hashlib
from datetime import date
from decimal import Decimal as D
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.engine.opportunities import load_market
from app.ingest import umoa
from app.ingest.pdf import extract_text, pdftotext_available
from app.ingest.queue import ReviewError, approve, list_queue, reject
from app.ingest.review import main as review_main
from app.ingest.umoa_extract import _absorption, parse_compte_rendu, parse_french_date, parse_number
from app.models import (
    Auction,
    AuctionExtraction,
    ExtractionReviewEvent,
    Security,
    SourceDocument,
)
from app.models.enums import AuctionStatus, AuctionType, DataNature, VerificationStatus

FIX = Path(__file__).parent / "fixtures" / "umoa"
NE_2026 = "Compte-Rendu-NE-ES-01.10.2026.txt"
SN_2026 = "Compte-Rendu-SN-ES-06.08.2026.txt"
CI_2026 = "Compte-Rendu-CI-ES-15.09.2026.txt"
BF_2020 = "Compte-Rendu-BF-BAT-182-jours-17.06.2020.txt"
BJ_2026 = "Compte-Rendu-BJ-ES-22.01.2026.txt"
CI_EC_2026 = "Compte-Rendu-CI-EC-29.04.2026.txt"
GW_2026 = "Compte-Rendu-GW-ES-13.01.2026.txt"
ML_2016_PDF = "CR-ML-60-mois-08.09.2016.pdf"
ML_2016_URL = "https://www.umoatitres.org/wp-content/uploads/2020/05/CR-ML-60-mois-08.09.2016.pdf"
OP_URL = "https://www.umoatitres.org/fr/emission/obligations-assimilables-du-tresor-du-mali-du-08-09-2016/"

needs_pdftotext = pytest.mark.skipif(not pdftotext_available(), reason="poppler pdftotext not installed")


def parse(name: str):
    return parse_compte_rendu((FIX / name).read_text(encoding="utf-8"))


def by_isin(doc, isin):
    return next(t for t in doc.tranches if t.value("isin") == isin)


# --------------------------------------------------------------------------- helpers


class TestHelpers:
    def test_french_numbers(self):
        assert parse_number("4 431,25 millions de F CFA, dont ONC :0") == D("4431.25")
        assert parse_number("1 000 000") == D("1000000")
        assert parse_number("48358,71 millions") == D("48358.71")
        assert parse_number("-") is None

    def test_french_dates(self):
        assert parse_french_date("Dakar le 01 octobre 2026") == date(2026, 10, 1)
        assert parse_french_date("Dakar, le 08 septembre 2016") == date(2016, 9, 8)
        assert parse_french_date("Dakar le 02.sept.26") == date(2026, 9, 2)
        assert parse_french_date("Fait à Dakar") is None


# --------------------------------------------------------------------------- parser (real documents)


class TestMultiTrancheNiger2026:
    """Compte-Rendu-NE-ES-01.10.2026.pdf, p1: Niger, 4 OAT + 1 BAT, auction 01/10/2026."""

    @pytest.fixture(scope="class")
    def doc(self):
        return parse(NE_2026)

    def test_operation(self, doc):
        assert doc.layout == "multi_tranche"
        assert doc.value("country_iso3") == "NER"  # "Emetteur : ETAT DU NIGER"
        assert doc.value("auction_date") == "2026-10-01"  # "Date d'adjudication : 01/10/2026"
        assert doc.value("settlement_date") == "2026-10-02"  # "Date de valeur : 02/10/2026"
        assert doc.value("total_amount_offered") == "39907000000"  # "39 907 millions de FCFA"
        assert doc.value("total_amount_submitted") == "39907270000"  # "39 907,27"
        assert doc.publication_date == date(2026, 10, 1)  # "Dakar le 01 octobre 2026"

    def test_isins_in_document_order(self, doc):
        assert [t.value("isin") for t in doc.tranches] == [
            "NE0000001310", "NE0000001526", "NE0000002458", "NE0000002771", "NE0000002797"]

    def test_oat_2y(self, doc):
        t = by_isin(doc, "NE0000001310")  # column "OAT - 2 ans"
        assert t.value("instrument") == "OAT"
        assert t.value("tenor") == "2 ans"
        assert t.value("maturity_date") == "2028-07-09"  # 09/07/2028
        assert t.value("coupon_rate") == "6.15"  # "Taux d'intérêt fixe annoncé 6,15%"
        assert t.value("number_of_participants") == "8"
        assert t.value("number_of_bids") == "8"
        assert t.value("amount_submitted") == "4431250000"  # "4 431,25 millions de F CFA"
        assert t.value("amount_allocated") == "4431250000"
        assert t.value("marginal_price") == "95.8606"  # "Taux/Prix marginal 95,8606%"
        assert t.value("weighted_average_price") == "96.2654"
        assert t.value("weighted_average_yield") == "8.49"  # "Rendement moyen pondéré 8,49%"
        assert t.parse_status == "complete"

    def test_oat_5y(self, doc):
        t = by_isin(doc, "NE0000002771")  # column "OAT - 5 ans"
        assert (t.value("number_of_participants"), t.value("number_of_bids")) == ("6", "7")
        assert t.value("amount_submitted") == "21043140000"  # "21 043,14"
        assert t.value("marginal_price") == "90.0625"
        assert t.value("weighted_average_price") == "91.9740"
        assert t.value("weighted_average_yield") == "8.62"
        assert t.value("maturity_date") == "2031-07-03"

    def test_bat_364d(self, doc):
        t = by_isin(doc, "NE0000002797")  # last column "BAT - 364 jours"
        assert t.value("instrument") == "BAT"
        assert t.value("tenor_days") == "364"
        assert t.value("face_value") == "1000000"
        assert t.value("marginal_rate") == "8.0000"  # for a BAT "Taux/Prix" is a rate
        assert t.value("weighted_average_rate") == "8.0000"
        assert t.value("weighted_average_yield") == "8.70"
        assert t.value("amount_submitted") == "4573000000"
        assert "coupon_rate" not in t.fields  # blank for the BAT column
        assert t.field_status["coupon_rate"] == "not_disclosed"

    def test_locators_and_confidence(self, doc):
        t = by_isin(doc, "NE0000001310")
        isin = t.fields["isin"]
        assert isin.locator == "p1:L12 'Code ISIN' col 1/5" and isin.confidence == 0.95
        y = t.fields["weighted_average_yield"]
        assert y.locator.startswith("p1:L61 'rendement moyen pondere'") and y.raw == "8,49%"
        assert 0.8 <= y.confidence <= 0.95
        amount = t.fields["amount_submitted"]
        assert amount.unit == "XOF" and "millions" in amount.note

    def test_multi_tranche_amount_offered_not_disclosed(self, doc):
        # Only one global amount is published for the five securities together.
        assert all(t.field_status["amount_offered"] == "not_disclosed" for t in doc.tranches)

    def test_consistency_checks_pass(self, doc):
        assert doc.checks and all(c["ok"] for c in doc.checks)
        assert all(c["data_nature"] == "CALCULATION" for c in doc.checks)


class TestMultiTrancheSenegal2026:
    """Compte-Rendu-SN-ES-06.08.2026.pdf, p1: Senegal, BAT 182 j + BAT 364 j."""

    def test_values(self):
        doc = parse(SN_2026)
        assert doc.value("country_iso3") == "SEN"  # "ETAT DU SÉNÉGAL"
        assert doc.value("total_amount_offered") == "55000000000"
        assert doc.value("coverage_bids_pct") == "112.82"
        assert doc.value("coverage_accepted_pct") == "110.00"
        assert doc.value("absorption_rate") == "97.50"
        t1, t2 = doc.tranches
        assert (t1.value("isin"), t1.value("tenor_days"), t1.value("maturity_date")) == (
            "SN0000005224", "182", "2027-02-04")
        assert t1.value("amount_submitted") == "17056000000"  # 17 056,00
        assert t1.value("amount_allocated") == "17050000000"  # 17 050,00
        assert t1.value("amount_rejected") == "6000000"  # 6,00
        assert t1.value("absorption_rate") == "99.96"
        assert (t1.value("marginal_rate"), t1.value("weighted_average_rate")) == ("7.0000", "6.7045")
        assert t1.value("weighted_average_yield") == "6.94"
        assert (t2.value("isin"), t2.value("number_of_participants"), t2.value("number_of_bids")) == (
            "SN0000005232", "14", "18")
        assert t2.value("marginal_rate") == "7.9999"
        assert t2.value("weighted_average_yield") == "8.20"
        assert all(t.parse_status == "complete" for t in doc.tranches)


class TestZeroAllotmentCoteDIvoire2026:
    """Compte-Rendu-CI-ES-15.09.2026.pdf, p1: the BAT 364 j had bids but nothing was retained."""

    def test_zero_allotment_is_flagged(self):
        doc = parse(CI_2026)
        bat = by_isin(doc, "CI0000010724")
        assert bat.value("amount_submitted") == "1700000000"  # 1 700,00
        assert bat.value("amount_allocated") == "0"  # 0,00
        assert bat.value("weighted_average_yield") == "0.00"  # printed 0,00%: kept as read …
        assert any("nothing allotted" in w for w in doc.warnings)  # … and flagged
        oat7 = by_isin(doc, "CI0000010799")
        assert (oat7.value("coupon_rate"), oat7.value("weighted_average_price"),
                oat7.value("weighted_average_yield")) == ("5.70", "92.2113", "7.15")


class TestTemplate2026Benin:
    """Compte-Rendu-BJ-ES-22.01.2026.pdf, p1: values printed on the line below their label,
    amount cells separated by one space, accrued coupon as a bare ratio."""

    def test_values(self):
        doc = parse(BJ_2026)
        assert doc.value("country_iso3") == "BEN"
        assert doc.value("auction_date") == "2026-01-22"  # value line under "Date d'adjudication :"
        assert doc.value("settlement_date") == "2026-01-23"
        assert doc.value("total_amount_offered") == "60000000000"  # "60 000 millions"
        assert [t.value("isin") for t in doc.tranches] == [
            "BJ0000002580", "BJ0000002549", "BJ0000002556", "BJ0000002564"]
        bat, oat3, oat5, oat7 = doc.tranches
        assert bat.value("tenor") == "182 jours" and bat.value("maturity_date") == "2026-07-23"
        # "97 462,00 millions de F CFA, dont ONC :0 66 462,40 millions de F CFA, …"
        assert [t.value("amount_submitted") for t in doc.tranches] == [
            "97462000000", "66462400000", "2315000000", "9000510000"]
        assert [t.value("amount_allocated") for t in doc.tranches] == [
            "16898000000", "44062400000", "2315000000", "2724200000"]
        assert oat3.value("coupon_rate") == "5.70"
        assert D(oat3.value("accrued_coupon_rate")) == D("0.2186301")  # printed 0,002186301
        assert "ratio" in oat3.fields["accrued_coupon_rate"].note
        assert (oat7.value("weighted_average_price"), oat7.value("weighted_average_yield")) == ("94.9816", "6.93")
        assert bat.value("marginal_rate") == "5.2500"
        assert all(t.parse_status == "complete" for t in doc.tranches)
        assert all(c["ok"] for c in doc.checks)


class TestGluedCellsGuineaBissau2026:
    """Compte-Rendu-GW-ES-13.01.2026.pdf, p1: "13 100,00 millions de F CFA, dont ONC :05 484,13
    millions …" (no space between cells). Found by the consistency checks in the live run."""

    def test_values(self):
        doc = parse(GW_2026)
        assert doc.value("country_iso3") == "GNB"
        assert [t.value("amount_submitted") for t in doc.tranches] == [
            "8201000000", "13100000000", "5484130000"]
        assert [t.value("amount_allocated") for t in doc.tranches] == [
            "2730000000", "6786000000", "5484130000"]
        oat = doc.tranches[2]
        assert (oat.value("tenor"), oat.value("weighted_average_price"), oat.value("weighted_average_yield")) == (
            "3 ans", "90.3761", "10.13")
        assert all(c["ok"] for c in doc.checks)  # sums match the published totals (26 785,13)


class TestExchangeIssueAndBuybackCoteDIvoire2026:
    """Compte-Rendu-CI-EC-29.04.2026-.pdf: p1 issue report (single OAT), then two buyback
    reports ("COMPTE RENDU DE RACHAT …", 3 OAT and 4 BAT) in the same PDF."""

    def test_sections(self):
        doc = parse(CI_EC_2026)
        assert [(t.value("isin"), t.kind) for t in doc.tranches] == [
            ("CI0000010189", "issue"),
            ("CI0000004776", "buyback"), ("CI0000006565", "buyback"), ("CI0000006839", "buyback"),
            ("CI0000009163", "buyback"), ("CI0000009247", "buyback"), ("CI0000009478", "buyback"),
            ("CI0000009494", "buyback")]
        issue = doc.tranches[0]
        assert issue.operation_tranches == 1
        assert issue.value("amount_offered") == "54154810000"  # "54 154,810 millions"
        assert issue.value("weighted_average_yield") == "6.14"
        assert issue.value("marginal_price") == "97.5034"
        rb = doc.tranches[1]  # first buyback column, "OAT - 117 jours"
        assert rb.tranche_key == "CI0000004776/buyback"
        assert rb.operation_tranches == 3
        assert rb.operation["total_amount_offered"].value == "48543580000"  # "48 543,58"
        assert (rb.value("amount_allocated"), rb.value("weighted_average_price"),
                rb.value("weighted_average_yield")) == ("6243580000", "100.0785", "5.25")
        assert rb.value("auction_number") == "RA-CI0000004776-53-2026"


class TestSingleTrancheBurkina2020:
    """Compte-Rendu-BF-BAT-182-jours-17.06.2020.pdf, p1: Burkina, single BAT 182 days."""

    def test_values(self):
        doc = parse(BF_2020)
        assert doc.layout == "single_tranche"
        (t,) = doc.tranches
        assert doc.value("country_iso3") == "BFA"  # "ETAT DU BURKINA"
        assert t.value("isin") == "BF0000001545"
        assert t.value("auction_number") == "ADJ-BF0000001545-BAT-09-2020"
        assert t.value("auction_date") == "2020-06-17"  # "… du : 17/06/2020"
        assert t.value("settlement_date") == "2020-06-18"
        assert t.value("maturity_date") == "2020-12-16"
        assert t.value("tenor_days") == "182"
        assert t.value("amount_offered") == "25000000000"  # "25 000 millions"
        assert doc.operation_status["total_onc_offered"] == "not_disclosed"  # "dont en ONC : ND"
        assert (t.value("number_of_participants"), t.value("number_of_bids")) == ("14", "25")
        assert t.value("amount_submitted") == "51657000000"
        assert t.value("amount_allocated") == "27500000000"
        assert t.value("amount_rejected") == "24157000000"
        assert doc.value("coverage_bids_pct") == "206.63"
        assert doc.value("absorption_rate") == "53.24"
        assert t.value("weighted_average_yield") == "5.09"
        assert (t.value("marginal_rate"), t.value("weighted_average_rate")) == ("5.1900", "4.9648")
        assert t.parse_status == "complete"

# --------------------------------------------------------------------------- layout variants
# Fixes from the review of the rows the independent checker held. Each class reads one real
# report (see SOURCES.txt); values were read by hand from the PDF.

ML_RA_2026 = "Compte-Rendu-ML-RA-OAT-26-jours-02.09.2026.txt"
CI_2024_05 = "Compte-Rendu-CI-ES-28.05.2024.txt"
GW_2024_03 = "Compte-Rendu-GW-ES-12.03.2024.txt"
CI_RS_2024 = "Compte-Rendu-CI-RS-17.09.2024.txt"
TG_EC_2024 = "Compte-Rendu-TG-EC15.03.2024.txt"
CI_2024_02 = "Compte-Rendu-CI-ES-29.02.2024.txt"
CI_2025_03 = "Compte-Rendu-CI-ES-04.03.2025.txt"
CI_EC_2026_02 = "Compte-Rendu-CI-EC-05.02.2026.txt"
CI_EC_2025_07 = "Compte-rendu-CI-EC-11.07.2025-1.txt"
ML_2025_04 = "Compte-Rendu-ML-ES-30.04.2025-1.txt"
CI_EC_2024_12 = "Compte-Rendu-CI-EC-17.12.2024.txt"


class TestSingleLayoutUnitsAndDateLabelMali2026:
    """Compte-Rendu-ML-RA-OAT-26-jours-02.09.2026.pdf, p1 (A, K2): single-security report with
    no heading; "Montant global des soumissions :   9 050,000        millions de FCFA" (unit in
    its own cell); "Adjudication N° : RA-ML0000002583-39-2026   du : 02/09/2026"."""

    def test_unit_is_part_of_the_raw_amount(self):
        (t,) = parse(ML_RA_2026).tranches
        sub = t.fields["amount_submitted"]
        assert (sub.value, sub.raw) == ("9050000000", "9 050,000 millions de FCFA")
        assert t.fields["amount_allocated"].raw == "9 050,000 millions de FCFA"
        assert t.fields["amount_rejected"].raw == "0,000 millions de FCFA"
        assert (t.value("amount_offered"), t.fields["amount_offered"].raw) == (
            "9050000000", "9 050 millions de FCFA")  # "9 050              millions de FCFA, dont en ONC : 0"

    def test_auction_date_located_by_its_printed_label(self):
        (t,) = parse(ML_RA_2026).tranches
        f = t.fields["auction_date"]
        assert (f.value, f.raw, f.locator) == ("2026-09-02", "02/09/2026", "p1:L4 'du :'")
        assert "du :" in (FIX / ML_RA_2026).read_text(encoding="utf-8").splitlines()[3]

    def test_tenor_raw_is_the_cell(self):
        (t,) = parse(ML_RA_2026).tranches
        assert (t.value("tenor"), t.fields["tenor"].raw, t.value("tenor_days")) == ("26 jours", "26 jours", "26")

    def test_ra_auction_number_means_buyback(self):
        (t,) = parse(ML_RA_2026).tranches
        assert t.value("auction_number") == "RA-ML0000002583-39-2026"
        assert t.kind == "buyback" and t.tranche_key == "ML0000002583/buyback"
        assert t.parse_status == "complete"


class TestDashlessHeader2024:
    """Compte-Rendu-CI-ES-28.05.2024.pdf, p1 (B): results header "BAT 182 jours   BAT 364 jours
    OAT 3 ans" (no dash); header cells "182   jours   364   jours   3   ans" and
    "1 000 000   FCFA   1 000 000   FCFA   10 000   FCFA"; OAT coupon "5,70%" on a line with no
    label (L14)."""

    @pytest.fixture(scope="class")
    def doc(self):
        return parse(CI_2024_05)

    def test_results_table_is_read(self, doc):
        assert [t.value("isin") for t in doc.tranches] == ["CI0000007589", "CI0000007555", "CI0000007563"]
        bat6m, bat1y, oat3y = doc.tranches
        assert (bat6m.value("number_of_participants"), bat6m.value("number_of_bids")) == ("6", "10")
        assert (bat6m.value("amount_submitted"), bat6m.value("amount_allocated"),
                bat6m.value("amount_rejected")) == ("27406000000", "23406000000", "4000000000")
        assert (bat6m.value("absorption_rate"), bat6m.value("marginal_rate"),
                bat6m.value("weighted_average_rate"), bat6m.value("weighted_average_yield")) == (
            "85.40", "6.7800", "6.6613", "6.89")
        assert bat1y.value("amount_submitted") == "8121000000"
        assert (oat3y.value("amount_submitted"), oat3y.value("marginal_price"),
                oat3y.value("weighted_average_price"), oat3y.value("weighted_average_yield")) == (
            "19156380000", "95.0000", "95.0897", "7.62")
        assert all(c["ok"] for c in doc.checks)

    def test_unit_cells_are_merged_into_their_number(self, doc):
        bat6m, bat1y, oat3y = doc.tranches
        assert [(t.value("tenor"), t.fields["tenor"].raw) for t in doc.tranches] == [
            ("182 jours", "182 jours"), ("364 jours", "364 jours"), ("3 ans", "3 ans")]
        assert [t.value("face_value") for t in doc.tranches] == ["1000000", "1000000", "10000"]
        assert oat3y.fields["face_value"].raw == "10 000"  # unit "FCFA" recorded as XOF
        assert oat3y.fields["face_value"].locator.endswith("col 3/3")
        assert bat6m.parse_status == bat1y.parse_status == "complete"

    def test_unlabelled_coupon_is_not_read_and_not_called_undisclosed(self, doc):
        oat3y = doc.tranches[2]
        assert oat3y.value("coupon_rate") is None
        assert oat3y.field_status["coupon_rate"] == "not_available"
        assert oat3y.parse_status == "partial"
        assert any("without a label" in e for e in oat3y.errors)

    def test_misspelt_header_jous(self):
        """Compte-Rendu-GW-ES-12.03.2024.pdf, p1: "BAT 107 jous   BAT 336 jours"."""
        doc = parse(GW_2024_03)
        a, b = doc.tranches
        assert (a.value("tenor"), b.value("tenor")) == ("107 jours", "336 jours")
        assert (a.value("amount_submitted"), a.value("amount_allocated"), a.value("absorption_rate"),
                a.value("weighted_average_yield")) == ("2500000000", "2000000000", "80.00", "8.98")
        assert (b.value("amount_submitted"), b.value("weighted_average_yield")) == ("4000000000", "9.65")
        assert a.parse_status == b.parse_status == "complete"


class TestIsinHeadedBuyback2024:
    """Compte-Rendu-CI-RS-17.09.2024.pdf, p1 (C): buyback of 7 BAT; results table headed by the
    ISIN codes "CI0000006813   CI0000006920 …"."""

    def test_columns_mapped_by_isin(self):
        doc = parse(CI_RS_2024)
        assert len(doc.tranches) == 7 and all(t.kind == "buyback" for t in doc.tranches)
        first, second, last = doc.tranches[0], doc.tranches[1], doc.tranches[-1]
        assert (first.value("isin"), first.value("amount_submitted"), first.value("marginal_rate"),
                first.value("weighted_average_rate"), first.value("weighted_average_yield")) == (
            "CI0000006813", "16074000000", "2.0000", "2.7389", "2.74")
        assert (second.value("isin"), second.value("amount_allocated"), second.value("weighted_average_yield")) == (
            "CI0000006920", "1000000000", "3.51")
        assert (last.value("isin"), last.value("amount_submitted"), last.value("weighted_average_yield")) == (
            "CI0000007985", "2000000000", "3.02")
        assert all(t.parse_status == "complete" for t in doc.tranches)
        assert all(c["ok"] for c in doc.checks)  # 16 074 + 1 000 + … = 41 074 published

    def test_absorption_ratio_and_range(self):
        # Column 1 prints a bare "1" (Excel ratio, 16 074 of 16 074 retained) → 100 %.
        first = parse(CI_RS_2024).tranches[0]
        assert (first.value("absorption_rate"), first.fields["absorption_rate"].raw) == ("100", "1")
        # The same cell as rendered in the diagnosis ("1 100,00%") must never become 1100 %.
        assert _absorption("1 100,00%", "p1:L32", 0.9) == (None, "not_available")
        assert _absorption("100,00%", "p1:L32", 0.9)[0].value == "100.00"


class TestFractionalTenor2024:
    """Compte-Rendu-TG-EC15.03.2024.pdf, p1 (D): reopened OAT "Durée : … 2,85 ans …", results
    header "OAT - 2,85 ans"."""

    def test_decimal_tenor(self):
        doc = parse(TG_EC_2024)
        oat = by_isin(doc, "TG0000002617")
        assert (oat.value("tenor"), oat.fields["tenor"].raw) == ("2.85 ans", "2,85 ans")
        assert oat.value("tenor_days") == "1040"  # round(2.85 × 365) = round(1040.25)
        assert "converted to days" in oat.fields["tenor_days"].note
        assert "fractional" in oat.fields["tenor_days"].note
        # The results column "OAT - 2,85 ans" is found and matched.
        assert (oat.value("amount_submitted"), oat.value("marginal_price"), oat.value("weighted_average_yield")) == (
            "12562410000", "94.4503", "8.40")
        assert oat.parse_status == "complete" and not oat.errors
        assert by_isin(doc, "TG0000002724").fields["tenor_days"].note is None  # "364 jours"


class TestStaggeredBuybackHeader2024:
    """Compte-Rendu-CI-ES-29.02.2024.pdf, p2 (E): "Dénomination de l'émission :
    CI0000006417-BAT-05-2024" then, on the next line, "CI0000004453-OAT-06-2024
    CI0000007068-BAT-04-2024 …"; same for durée, échéance, valeur nominale, adjudication n°."""

    def test_second_line_cells_by_column(self):
        doc = parse(CI_2024_02)
        rb = [t for t in doc.tranches if t.kind == "buyback"]
        assert [t.value("security_name") for t in rb[:3]] == [
            "CI0000006417-BAT-05-2024", "CI0000004453-OAT-06-2024", "CI0000007068-BAT-04-2024"]
        oat = rb[1]
        assert (oat.value("isin"), oat.value("instrument"), oat.value("tenor"), oat.value("maturity_date"),
                oat.value("face_value"), oat.value("auction_number")) == (
            "CI0000004453", "OAT", "108 jours", "2024-06-16", "10000", "RA-CI0000004453-OAT3A-2-2024")
        assert (oat.value("marginal_price"), oat.value("weighted_average_price")) == ("100.7068", "100.6238")
        # Located on the continuation line, under the label's name.
        assert oat.fields["maturity_date"].locator == "p2:L19 'date d'echeance' col 2/8"
        assert rb[0].fields["maturity_date"].locator == "p2:L18 'date d'echeance' col 1/8"
        assert all(t.parse_status == "complete" for t in rb)

    def test_issue_section_fractional_tenor(self):
        oat = by_isin(parse(CI_2024_02), "CI0000005922")
        assert (oat.value("tenor"), oat.value("tenor_days")) == ("1.94 ans", "708")
        assert oat.value("marginal_price") == "96.8275" and oat.parse_status == "complete"


class TestZeroBidTrancheBlankAbsorption2025:
    """Compte-Rendu-CI-ES-04.03.2025.pdf, p1 (F): OAT 3 ans and OAT 5 ans received no bids
    ("0 millions de F CFA"), and "Taux d'absorption   70,13%   100,00%   100,00%" leaves their
    cells blank."""

    def test_blank_absorption_is_not_disclosed_with_note(self):
        doc = parse(CI_2025_03)
        for isin in ("CI0000008926", "CI0000008934"):
            t = by_isin(doc, isin)
            assert (t.value("amount_submitted"), t.value("amount_allocated")) == ("0", "0")
            assert t.value("absorption_rate") is None
            assert t.field_status["absorption_rate"] == "not_disclosed"
            assert any("no bids" in n for n in t.notes)
            assert t.parse_status == "complete" and not t.errors
        assert by_isin(doc, "CI0000008942").value("absorption_rate") == "100.00"

    def test_blank_cell_with_bids_is_still_an_error(self):
        text = (FIX / CI_2025_03).read_text(encoding="utf-8").replace(
            "Taux d'absorption                      70,13%", "Taux d'absorption                            ")
        t = by_isin(parse_compte_rendu(text), "CI0000008959")  # 124 360 submitted
        assert t.field_status["absorption_rate"] == "not_available" and t.parse_status == "partial"


class TestBuybackOverSeveralPages2026:
    """Compte-Rendu-CI-EC-05.02.2026.pdf (H): issue of 3 OAT (p1), then one buyback of 12
    securities printed on pages 2–4, each repeating "Montant global mis en adjudication:
    114 033,00"; only page 2 prints "Montant global des soumissions : 114 033,00"."""

    @pytest.fixture(scope="class")
    def doc(self):
        return parse(CI_EC_2026_02)

    def test_pages_form_one_operation(self, doc):
        rb = [t for t in doc.tranches if t.kind == "buyback"]
        assert len(rb) == 12 and all(t.operation_tranches == 12 for t in rb)
        total = sum(int(t.value("amount_submitted")) for t in rb)
        assert total == 114_033_000_000
        sums = [c for c in rb[-1].checks if c["check"].startswith("sum_")]
        assert sums and all(c["ok"] for c in sums)
        assert all(t.parse_status == "complete" for t in doc.tranches)

    def test_checks_are_scoped_to_their_tranches(self, doc):
        issue = doc.tranches[0]
        assert issue.kind == "issue"
        assert all("/buyback" not in c["check"] for c in issue.checks)
        own = [c["check"] for c in issue.checks if ":" in c["check"]]
        assert own and all(c.startswith("CI0000006201:") for c in own)

    def test_failed_check_holds_only_its_tranche(self):
        # Rejected amount of the first buyback security changed by hand: only that row fails.
        text = (FIX / CI_EC_2026_02).read_text(encoding="utf-8")
        line = next(ln for ln in text.splitlines() if ln.startswith("Soumissions rejetées") and "0,00 millions" in ln)
        text = text.replace(line, line.replace("0,00 millions", "9,00 millions", 1), 1)
        doc = parse_compte_rendu(text)
        bad = [t.tranche_key for t in doc.tranches if any(not c["ok"] for c in t.checks)]
        assert len(bad) == 1


class TestSpacedDecimalComma2025:
    """J: "20 208, 7 millions de F CFA" (Compte-rendu-CI-EC-11.07.2025-1.pdf, p1 L31) and
    "6 622 ,4millions de F CFA" (Compte-Rendu-ML-ES-30.04.2025-1.pdf, p1 L32); the next row
    prints them normally ("20 208,7 millions", "6 622,4 millions")."""

    def test_amounts(self):
        oat = by_isin(parse(CI_EC_2025_07), "CI0000009346")
        sub = oat.fields["amount_submitted"]
        assert (sub.value, sub.raw) == ("20208700000", "20 208, 7 millions de F CFA")
        assert "space around the decimal comma" in sub.note
        assert oat.value("amount_allocated") == "20208700000"
        assert all(c["ok"] for c in oat.checks)
        ml = by_isin(parse(ML_2025_04), "ML0000003615")
        assert (ml.value("amount_submitted"), ml.fields["amount_submitted"].raw) == (
            "6622400000", "6 622 ,4millions de F CFA")
        assert ml.value("amount_allocated") == "6622400000"

    def test_neighbouring_cells_unchanged(self):
        ml = parse(ML_2025_04)
        assert by_isin(ml, "ML0000003607").value("amount_submitted") == "4173500000"  # "4 173,5"
        assert by_isin(ml, "ML0000003599").value("amount_submitted") == "35045000000"


class TestMisspeltBuybackHeading2024:
    """Compte-Rendu-CI-EC-17.12.2024.pdf (K2): "COMPTE RENDU DE RACAHT DE BONS DU TRESOR",
    "Adjudication N° : RA-CI0000008355-BAT1M-2024  du : 17/12/2024", settlement 18/12/2024
    after maturity 17/12/2024 as printed."""

    def test_classified_as_buyback_and_checks_scoped(self):
        doc = parse(CI_EC_2024_12)
        issue, rb = doc.tranches
        assert (issue.tranche_key, rb.tranche_key) == ("CI0000008074", "CI0000008355/buyback")
        assert any("RA-" in w for w in doc.warnings)
        # The printed dates of the buyback fail its own check, and only its own.
        assert not all(c["ok"] for c in rb.checks)
        assert all(c["ok"] for c in issue.checks) and issue.parse_status == "complete"
        assert issue.fields["auction_date"].locator == "p1:L6 'du :'"


@needs_pdftotext
class TestPdfMali2016:
    """CR-ML-60-mois-08.09.2016.pdf (original PDF), p1: Mali, single OAT 5 years."""

    def test_pdf_text_and_values(self):
        pdf = extract_text((FIX / ML_2016_PDF).read_bytes())
        assert pdf.method == "pdftotext-layout" and pdf.has_text
        doc = parse_compte_rendu(pdf.text)
        (t,) = doc.tranches
        assert t.value("isin") == "ML0000000587"
        assert t.value("maturity_date") == "2021-09-09"
        assert t.value("tenor_days") == "1825"  # "Durée : 5 ans" → 5 × 365 (noted)
        assert "365" in t.fields["tenor_days"].note
        assert t.value("coupon_rate") == "6.00"
        assert doc.value("total_onc_offered") == "7500000000"
        assert t.value("amount_submitted") == "32937500000"  # 32 937,5
        assert t.value("marginal_price") == "9600.0000"
        assert t.fields["weighted_average_price"].unit == "XOF_per_unit"  # 9 877,6257 FCFA
        assert doc.value("coverage_bids_pct") == "109.79"
        # This 2016 format publishes no weighted average yield: not disclosed, not guessed.
        assert t.value("weighted_average_yield") is None
        assert t.field_status["weighted_average_yield"] == "not_disclosed"

    def test_not_a_result_report(self):
        doc = parse_compte_rendu("Avis d'appel d'offres\nMontant : 30 000 millions")
        assert doc.tranches == [] and doc.layout == "unknown"


# --------------------------------------------------------------------------- official pages


class TestPages:
    def test_listing(self):
        ops = umoa.parse_listing((FIX / "emissions_listing_excerpt.html").read_text(encoding="utf-8"))
        assert len(ops) == 3  # 8 rows: 5 + 2 securities of Niger, 1 buyback of Mali
        first = ops[0]
        assert first.url.endswith("/emission-simultanee-dobligations-du-tresor-du-niger-du-01-10-2026/")
        assert first.issuer == "Niger" and first.operation_date == date(2026, 10, 1)
        assert first.instruments == ["BAT", "OAT"]

    def test_operation_page_documents(self):
        html = (FIX / "operation_page_NE_01-10-2026_documents.html").read_text(encoding="utf-8")
        links = umoa.parse_operation_page(html, "https://www.umoatitres.org/fr/emission/x/")
        assert [(d.label, d.document_type) for d in links] == [
            ("annonce", "result_announcement"), ("compte rendu", "auction_result")]
        assert links[1].url.endswith("/2026/10/Compte-Rendu-NE-ES-01.10.2026.pdf")


# --------------------------------------------------------------------------- pipeline


LISTING_HTML = f"""<table id="emission-hub-passees-par"><thead><tr><th>Émetteur</th></tr></thead><tbody>
<tr class='emission-sim'><td> Mali<br><i>OAT</i></td><td>OAT</td><td></td><td>08/09/2016</td>
<td>09/09/2016</td><td>09/09/2021</td><td>60</td><td>--</td><td class='all'><a href='{OP_URL}'>Plus d'infos</a></td>
<td>réalisée</td><td></td></tr></tbody></table>"""
OP_HTML = f"""<h3>Annonce</h3><p>Indisponible</p><h3>Compte rendu</h3>
<p><a href='{ML_2016_URL}' target='_blank'><button>Télécharger</button></a></p>"""


def fake_fetcher(pdf_bytes: bytes, calls: list[str]):
    pages = {umoa.LISTING_URL: (LISTING_HTML.encode(), "text/html"), OP_URL: (OP_HTML.encode(), "text/html"),
             ML_2016_URL: (pdf_bytes, "application/pdf")}

    def fetch(url: str) -> umoa.Fetched:
        calls.append(url)
        body, ctype = pages.get(url, (b"", None))
        return umoa.Fetched(200 if body else 404, url, body, ctype)

    return fetch


@pytest.fixture
def store(tmp_path, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "document_store_dir", str(tmp_path / "docs"))
    return tmp_path / "docs"


@pytest.fixture
def ingested(db, store):
    """Run the pipeline once on the real 2016 Mali report served by a fake fetcher."""
    if not pdftotext_available():
        pytest.skip("poppler pdftotext not installed")
    calls: list[str] = []
    stats = umoa.run(db, fetch=fake_fetcher((FIX / ML_2016_PDF).read_bytes(), calls), pause=0)
    return stats, calls


def _stage_text(db, name: str) -> list[AuctionExtraction]:
    """Stage a text fixture as if its PDF had just been fetched (the PDF itself is not stored)."""
    source = umoa.get_source(db)
    text = (FIX / name).read_text(encoding="utf-8")
    doc = SourceDocument(source_id=source.source_id, url=f"https://www.umoatitres.org/test/{name}",
                         title=name, document_type="auction_result",
                         content_sha256=hashlib.sha256(text.encode()).hexdigest())
    db.add(doc)
    db.flush()
    parsed = parse_compte_rendu(text)
    doc.publication_date = parsed.publication_date
    rows = [umoa._upsert_extraction(db, doc, parsed, t) for t in parsed.tranches]
    db.flush()
    return rows


class TestPipeline:
    def test_run_stores_document_and_stages_extraction(self, db, ingested, store):
        stats, calls = ingested
        assert stats["documents_new"] == 1 and stats["extractions"] == 1
        assert stats["documents_complete"] == 1
        doc = db.scalar(select(SourceDocument).where(SourceDocument.url == ML_2016_URL))
        assert doc.content_sha256 == hashlib.sha256((FIX / ML_2016_PDF).read_bytes()).hexdigest()
        assert doc.mime_type == "application/pdf" and doc.retrieved_at is not None
        assert doc.publication_date == date(2016, 9, 8)  # "Dakar, le 08 septembre 2016"
        assert doc.extraction_status == "complete" and doc.is_synthetic is False
        assert Path(doc.storage_path).read_bytes()[:5] == b"%PDF-"
        assert Path(doc.storage_path).with_suffix(".txt").exists()  # text kept for reviewers
        (ext,) = db.scalars(select(AuctionExtraction).where(AuctionExtraction.source_document_id == doc.document_id))
        assert ext.data_nature == DataNature.FACT
        assert ext.verification_status == VerificationStatus.UNVERIFIED
        assert ext.is_synthetic is False
        assert (ext.isin, ext.country_iso3, ext.instrument, ext.auction_date) == (
            "ML0000000587", "MLI", "OAT", date(2016, 9, 8))
        assert ext.fields["amount_allocated"]["value"] == "30000000000"
        assert ext.fields["amount_allocated"]["locator"].startswith("p1:L")
        assert ext.source_url == ML_2016_URL and ext.extracted_at is not None

    def test_idempotent(self, db, ingested, store):
        _, calls = ingested
        fetch = fake_fetcher((FIX / ML_2016_PDF).read_bytes(), calls)
        again = umoa.run(db, fetch=fetch, pause=0)
        assert again["documents_skipped_known_url"] == 1 and again["documents_downloaded"] == 0
        refreshed = umoa.run(db, fetch=fetch, refresh=True, pause=0)  # same bytes re-downloaded
        assert refreshed["documents_downloaded"] == 1 and refreshed["documents_new"] == 0
        assert db.scalar(select(func.count()).select_from(SourceDocument)
                         .where(SourceDocument.url == ML_2016_URL)) == 1
        assert db.scalar(select(func.count()).select_from(AuctionExtraction)
                         .where(AuctionExtraction.isin == "ML0000000587")) == 1

    def test_same_bytes_other_url_is_one_document(self, db, store):
        source = umoa.get_source(db)
        content = (FIX / ML_2016_PDF).read_bytes()
        d1, created1 = umoa.save_document(db, source, ML_2016_URL, content, "application/pdf", "t", "auction_result")
        d2, created2 = umoa.save_document(db, source, ML_2016_URL + "?copy", content, None, "t", "auction_result")
        assert created1 and not created2 and d1.document_id == d2.document_id

    def test_listing_failure_is_reported_not_raised(self, db, store):
        stats = umoa.run(db, fetch=lambda url: umoa.Fetched(None, url, b"", None, "ConnectError"), pause=0)
        assert stats["operations_listed"] == 0 and "ConnectError" in stats["errors"][0]
        assert umoa.get_source(db).last_error.startswith("listing:")

    def test_reviewed_rows_are_not_overwritten(self, db, store):
        rows = _stage_text(db, SN_2026)
        reject(db, rows[0].extraction_id, "analyst-a", "test")
        doc = rows[0].document
        parsed = parse_compte_rendu((FIX / SN_2026).read_text(encoding="utf-8"))
        assert umoa._upsert_extraction(db, doc, parsed, parsed.tranches[0]) is None
        assert rows[0].verification_status == VerificationStatus.REJECTED

    def test_reclassified_section_updates_its_unreviewed_row(self, db, store):
        """A row staged by the earlier parser as an issue ("ML0000002583") is re-keyed in place
        when the section is now read as a buyback (RA- auction number): no stale duplicate."""
        (row,) = _stage_text(db, "Compte-Rendu-ML-RA-OAT-26-jours-02.09.2026.txt")
        row.tranche_key = "ML0000002583"  # as staged before the fix
        db.flush()
        parsed = parse_compte_rendu((FIX / "Compte-Rendu-ML-RA-OAT-26-jours-02.09.2026.txt").read_text(encoding="utf-8"))
        again = umoa._upsert_extraction(db, row.document, parsed, parsed.tranches[0],
                                        {t.tranche_key for t in parsed.tranches})
        assert again.extraction_id == row.extraction_id and again.tranche_key == "ML0000002583/buyback"
        assert db.scalar(select(func.count()).select_from(AuctionExtraction).where(
            AuctionExtraction.source_document_id == row.source_document_id)) == 1

    def test_rows_carry_only_their_own_checks_and_notes(self, db, store):
        rows = _stage_text(db, "Compte-Rendu-CI-ES-04.03.2025.txt")
        zero = next(r for r in rows if r.isin == "CI0000008926")
        assert {c["check"] for c in zero.checks} >= {"sum_amount_submitted", "CI0000008926: submitted = allocated + rejected"}
        assert all(c["check"].startswith(("sum_", "CI0000008926:")) for c in zero.checks)
        assert any("no bids" in w for w in zero.warnings)
        assert zero.parse_status == "complete"

    def test_staging_rows_must_not_be_labelled_synthetic(self, db, store):
        rows = _stage_text(db, BF_2020)
        rows[0].is_synthetic = True  # FACT + unverified + synthetic violates the CHECK
        with pytest.raises(IntegrityError):
            with db.begin_nested():
                db.flush()


# --------------------------------------------------------------------------- isolation


class TestUnverifiedIsolation:
    def test_staged_rows_never_reach_core_tables(self, db, store):
        before = db.scalar(select(func.count()).select_from(Auction))
        _stage_text(db, NE_2026)
        assert db.scalar(select(func.count()).select_from(Auction)) == before
        assert db.scalar(select(Security).where(Security.isin == "NE0000001310")) is None

    def test_engine_ignores_unverified_auction_rows(self, db):
        sec = db.scalar(select(Security).where(Security.is_synthetic, Security.tenor_days.is_not(None)))
        stray = Auction(security_id=sec.security_id, auction_date=date(2026, 9, 1),
                        auction_type=AuctionType.TAP, status=AuctionStatus.COMPLETED,
                        weighted_average_yield=D("99"), verification_status=VerificationStatus.UNVERIFIED)
        db.add(stray)
        db.flush()
        market = load_market(db, date(2026, 10, 3))
        loaded = {a.auction_id for series in market.completed.values() for a in series}
        assert stray.auction_id not in loaded
        assert loaded  # synthetic rows still feed the engine

    def test_public_endpoints_do_not_serve_staged_rows(self, client, seeded, analyst_headers):
        from sqlalchemy.orm import Session

        with Session(seeded) as s:
            rows = _stage_text(s, SN_2026)
            s.commit()
            ids = [r.extraction_id for r in rows]
        try:
            real = client.get("/api/v1/auctions", params={"country": "SEN", "include_synthetic": "false"}).json()
            assert real["total"] == 0
            synthetic = client.get("/api/v1/auctions", params={"country": "SEN"}).json()
            assert synthetic["total"] > 0 and all(a["provenance"]["is_synthetic"] for a in synthetic["items"])
            secs = client.get("/api/v1/securities", params={"country": "SEN", "limit": 500}).json()
            assert all(s_["isin"] not in ("SN0000005224", "SN0000005232") for s_ in secs["items"])
            assert client.get("/api/v1/ingest/queue", params={"country": "SEN"}).status_code == 401
            queue = client.get("/api/v1/ingest/queue", params={"country": "SEN"}, headers=analyst_headers).json()
            assert queue["total"] == 2
            item = queue["items"][0]
            assert item["verification_status"] == "unverified" and item["data_nature"] == "FACT"
            assert item["notice"].startswith("UNVERIFIED")
            assert item["fields"]["weighted_average_yield"]["locator"].startswith("p1:L")
            assert item["document"]["document_type"] == "auction_result"
        finally:
            with Session(seeded) as s:
                for e in s.scalars(select(AuctionExtraction).where(AuctionExtraction.extraction_id.in_(ids))):
                    doc = e.document
                    s.delete(e)
                    s.flush()
                    if doc is not None and not s.scalar(select(AuctionExtraction).where(
                            AuctionExtraction.source_document_id == doc.document_id)):
                        s.delete(doc)
                s.commit()


# --------------------------------------------------------------------------- review


class TestReview:
    def test_approve_single_tranche_bond(self, db, ingested):
        ext = db.scalar(select(AuctionExtraction).where(AuctionExtraction.isin == "ML0000000587"))
        auction = approve(db, ext.extraction_id, "analyst-a", note="checked against PDF p1")
        sec = auction.security
        assert (sec.isin, sec.instrument_type.value, sec.currency, sec.tenor_days) == (
            "ML0000000587", "treasury_bond", "XOF", 1825)
        assert sec.coupon_rate == D("6.00") and sec.maturity_date == date(2021, 9, 9)
        assert sec.verification_status == VerificationStatus.VERIFIED and sec.is_synthetic is False
        assert sec.field_status["issue_date"] == "not_disclosed"
        assert auction.verification_status == VerificationStatus.VERIFIED
        assert auction.data_nature == DataNature.FACT and auction.is_synthetic is False
        assert auction.status == AuctionStatus.COMPLETED
        assert auction.auction_type == AuctionType.PRIMARY_AUCTION
        assert auction.amount_offered == D("30000000000")
        assert auction.amount_submitted == D("32937500000")
        assert auction.amount_allocated == D("30000000000")
        assert auction.number_of_bidders == 15
        # 9 877,6257 FCFA per 10 000 nominal → 98.776257 per 100 (unit conversion, noted)
        assert auction.average_price == D("98.776257")
        assert "converted" in auction.provenance_notes
        assert auction.reported_bid_to_cover == D("1.0979")  # 109,79 % / 100
        assert auction.cutoff_yield is None and auction.field_status["cutoff_yield"] == "not_disclosed"
        assert auction.weighted_average_yield is None
        assert auction.field_status["weighted_average_yield"] == "not_disclosed"
        assert auction.source_document_id == ext.source_document_id
        assert auction.source_url == ML_2016_URL and auction.publication_date == date(2016, 9, 8)
        assert ext.verification_status == VerificationStatus.VERIFIED
        assert ext.reviewed_by == "analyst-a" and ext.reviewed_at is not None
        assert ext.promoted_auction_id == auction.auction_id
        (event,) = db.scalars(select(ExtractionReviewEvent).where(
            ExtractionReviewEvent.extraction_id == ext.extraction_id))
        assert (event.action, event.reviewer, event.details["auction_id"]) == (
            "approved", "analyst-a", auction.auction_id)
        with pytest.raises(ReviewError, match="already verified"):
            approve(db, ext.extraction_id, "analyst-b")
        # Approved rows feed the engine like any verified fact.
        assert auction.auction_id in {a.auction_id for s in load_market(db, date(2021, 1, 1)).completed.values()
                                      for a in s}

    def test_approve_multi_tranche_bill(self, db, store):
        rows = _stage_text(db, NE_2026)
        bat = next(r for r in rows if r.isin == "NE0000002797")
        a = approve(db, bat.extraction_id, "analyst-a")
        assert a.security.instrument_type.value == "treasury_bill" and a.security.coupon_rate is None
        assert a.cutoff_yield == D("8.0000") and a.weighted_average_yield == D("8.70")
        assert a.amount_submitted == D("4573000000") and a.settlement_date == date(2026, 10, 2)
        assert a.amount_offered is None and a.field_status["amount_offered"] == "not_disclosed"
        assert a.reported_bid_to_cover is None and a.average_price is None
        assert a.field_status["number_of_successful_bidders"] == "not_disclosed"

    def test_buyback_promoted_as_buyback(self, db, store):
        rows = _stage_text(db, CI_EC_2026)
        rb = next(r for r in rows if r.tranche_key == "CI0000004776/buyback")
        assert rb.operation["operation_kind"] == "buyback"
        a = approve(db, rb.extraction_id, "analyst-a")
        assert a.auction_type == AuctionType.BUYBACK
        assert a.amount_offered is None  # 3 securities share one published amount
        issue = next(r for r in rows if r.tranche_key == "CI0000010189")
        b = approve(db, issue.extraction_id, "analyst-a")
        assert b.auction_type == AuctionType.PRIMARY_AUCTION
        assert b.amount_offered == D("54154810000") and b.reported_bid_to_cover == D("1")

    def test_zero_allotment_yields_not_promoted(self, db, store):
        rows = _stage_text(db, CI_2026)
        bat = next(r for r in rows if r.isin == "CI0000010724")
        a = approve(db, bat.extraction_id, "analyst-a")
        assert a.amount_allocated == D("0")
        assert a.weighted_average_yield is None and a.cutoff_yield is None
        assert a.field_status["weighted_average_yield"] == "not_disclosed"
        assert "Nothing was allotted" in a.provenance_notes

    def test_reject_requires_reason_and_is_audited(self, db, store):
        rows = _stage_text(db, BF_2020)
        ext = rows[0]
        with pytest.raises(ReviewError, match="reason"):
            reject(db, ext.extraction_id, "analyst-a", "  ")
        reject(db, ext.extraction_id, "analyst-a", "wrong ISIN column")
        assert ext.verification_status == VerificationStatus.REJECTED
        assert (ext.reviewed_by, ext.review_reason) == ("analyst-a", "wrong ISIN column")
        with pytest.raises(ReviewError, match="already rejected"):
            approve(db, ext.extraction_id, "analyst-b")
        assert db.scalar(select(Security).where(Security.isin == "BF0000001545")) is None
        assert [e.action for e in db.scalars(select(ExtractionReviewEvent).where(
            ExtractionReviewEvent.extraction_id == ext.extraction_id))] == ["rejected"]

    def test_duplicate_extraction_cannot_create_second_auction(self, db, store):
        first = _stage_text(db, BF_2020)[0]
        approve(db, first.extraction_id, "analyst-a")
        text = (FIX / BF_2020).read_text(encoding="utf-8") + "\n"  # same report, different bytes
        source = umoa.get_source(db)
        doc = SourceDocument(source_id=source.source_id, url="https://www.umoatitres.org/test/dup",
                             title="dup", document_type="auction_result",
                             content_sha256=hashlib.sha256(text.encode()).hexdigest())
        db.add(doc)
        db.flush()
        parsed = parse_compte_rendu(text)
        dup = umoa._upsert_extraction(db, doc, parsed, parsed.tranches[0])
        db.flush()
        with pytest.raises(ReviewError, match="already exists"):
            approve(db, dup.extraction_id, "analyst-a")

    def test_queue_listing(self, db, store):
        _stage_text(db, SN_2026)
        page = list_queue(db, VerificationStatus.UNVERIFIED, "SEN")
        assert page.total == 2 and {e.isin for e in page.items} == {"SN0000005224", "SN0000005232"}
        assert list_queue(db, VerificationStatus.VERIFIED, "SEN").total == 0

    def test_cli(self, db, store, capsys, monkeypatch):
        rows = _stage_text(db, SN_2026)
        # The CLI commits; keep the test's outer transaction (SQLite savepoints + pysqlite
        # would otherwise commit for real and leak rows into other tests).
        monkeypatch.setattr(db, "commit", db.flush)
        monkeypatch.setattr(db, "rollback", lambda: None)
        factory = lambda: contextlib.nullcontext(db)  # noqa: E731
        assert review_main(["list", "--country", "SEN"], factory) == 0
        assert "SN0000005224" in capsys.readouterr().out
        assert review_main(["show", str(rows[0].extraction_id)], factory) == 0
        out = capsys.readouterr().out
        assert "'Code ISIN' col 1/2" in out and "UNVERIFIED" in out
        assert review_main(["approve", str(rows[0].extraction_id), "--reviewer", "analyst-a"], factory) == 0
        assert review_main(["reject", str(rows[1].extraction_id), "--reason", "test", "--reviewer", "b"], factory) == 0
        assert review_main(["approve", str(rows[1].extraction_id), "--reviewer", "a"], factory) == 1
        assert rows[0].verification_status == VerificationStatus.VERIFIED
        assert rows[1].verification_status == VerificationStatus.REJECTED


class TestVerifiedExport:
    def test_export_then_load_restores_the_same_rows(self, db, store, tmp_path):
        from app.seed import verified

        rows = _stage_text(db, NE_2026)
        bat = next(r for r in rows if r.isin == "NE0000002797")
        approve(db, bat.extraction_id, "analyst-a")
        db.flush()
        path = tmp_path / "verified.json"
        counts = verified.export(db, path)
        assert counts["securities"] >= 1 and counts["auctions"] >= 1 and counts["documents"] >= 1

        before = db.scalar(select(Auction).join(Security).where(Security.isin == "NE0000002797"))
        snapshot = {k: getattr(before, k) for k in ("auction_date", "amount_submitted", "amount_allocated",
                                                    "cutoff_yield", "weighted_average_yield", "provenance_notes",
                                                    "verification_status", "confidence_score")}
        sec = before.security
        db.delete(before)
        db.flush()
        db.delete(sec)
        db.flush()

        assert verified.load(db, path)["auctions"] >= 1
        after = db.scalar(select(Auction).join(Security).where(Security.isin == "NE0000002797"))
        assert {k: getattr(after, k) for k in snapshot} == snapshot
        assert after.is_synthetic is False and after.source_document_id is not None
        assert verified.load(db, path) == {"documents": 0, "securities": 0, "auctions": 0}  # idempotent

    def test_buybacks_stay_out_of_issuance_series(self, db, store):
        rows = _stage_text(db, CI_EC_2026)
        rb = next(r for r in rows if r.tranche_key == "CI0000004776/buyback")
        a = approve(db, rb.extraction_id, "analyst-a")
        db.flush()
        m = load_market(db, a.auction_date)
        assert all(x.auction_id != a.auction_id for series in m.completed.values() for x in series)
