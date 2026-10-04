"""Cross-check of verified auctions against the official results announcements, and refinement of
values the result report printed ROUNDED (category B only).

Every expected value below was read by hand from the official documents named in
tests/fixtures/announcements/SOURCES.txt (URLs and SHA-256 there).
"""

import hashlib
import json
from decimal import Decimal as D
from pathlib import Path

import pytest
from sqlalchemy import select

from app.ingest import amend, announcements as ann_mod, umoa
from app.ingest.announcements import (
    classify,
    map_columns,
    parse_announcement,
    proposals,
    read_announcement,
    split_values,
)
from app.ingest.pdf import pdftotext_available
from app.ingest.queue import approve
from app.ingest.umoa_extract import parse_compte_rendu
from app.models import Auction, Security, SourceDocument
from app.models.enums import DataNature, VerificationStatus
from app.seed import verified

FIX = Path(__file__).parent / "fixtures" / "announcements"
UMOA_FIX = Path(__file__).parent / "fixtures" / "umoa"
BASE = "https://www.umoatitres.org/wp-content/uploads/"


def ann(name: str):
    return parse_announcement((FIX / name).read_text(encoding="utf-8"))


def cells(block, row):
    return [c.raw for c in block.rows[row]]


# --------------------------------------------------------------------------- parsing


class TestParsing:
    def test_header_table_after_global_result(self):
        a = ann("Annonce-au-MTP-NE-ES-01.10.2026.txt")
        glob, issue = a.blocks
        assert glob.kind == "global" and cells(glob, "amount_submitted") == ["39 907 270 000"]
        assert issue.kind == "issue"
        assert issue.labels == ["OAT - 2 ans", "OAT - 3 ans", "OAT - 4 ans", "OAT - 5 ans", "BAT - 364 jours"]
        assert cells(issue, "amount_submitted") == ["4 431 250 000", "2 775 340 000", "7 084 540 000",
                                                    "21 043 140 000", "4 573 000 000"]
        assert cells(issue, "weighted_average") == ["96,27%", "93,20%", "96,51%", "91,97%", "8,00%"]
        assert cells(issue, "number_of_participants") == ["8", "7", "2", "6", "7"]  # "Participants directs"
        assert cells(issue, "number_of_bids") == ["8", "7", "2", "7", "7"]
        assert issue.rows["amount_submitted"][3].value == D("21043140000")
        assert not a.errors

    def test_issue_and_buyback_tables_with_isin_headers_and_wrapped_label(self):
        a = ann("Annonce-au-MTP-CI-ES-06.03.2024.txt")
        kinds = [(b.kind, b.labels, b.isins) for b in a.blocks]
        assert kinds == [("global", [], []),
                         ("issue", ["BAT - 364 jours", "OAT - 3 ans"], []),
                         ("buyback", [], ["CI0000004453", "CI0000006441", "CI0000006557"]),
                         ("buyback", [], ["CI0000007126", "CI0000006508", "CI0000006227"])]
        # "Montant global des soumissions (F" / values / "CFA)": the values belong to that label.
        assert cells(a.blocks[2], "amount_submitted") == ["2 500 000 000", "20 240 000 000", "7 287 000 000"]
        assert cells(a.blocks[2], "marginal") == ["100,8806%", "3,0000%", "2,5000%"]
        assert cells(a.blocks[3], "weighted_average_yield") == ["5,57%", "2,52%", "3,50%"]

    def test_single_column_issue_and_buyback(self):
        a = ann("Annonce-au-MTP-GW-EC-20.08.2024.txt")
        assert [(b.kind, b.columns) for b in a.blocks] == [("issue", 1), ("buyback", 1)]
        assert cells(a.blocks[0], "amount_allocated") == ["2 335 000 000"]
        assert cells(a.blocks[1], "weighted_average_yield") == ["6,45%"]

    def test_greedy_split_is_used_only_when_unique(self):
        # Every number starts with a short group: one split only.
        assert split_values("15 084 000 000 4 400 000 000 26 707 730 000 14 089 030 000") == (
            ["15 084 000 000", "4 400 000 000", "26 707 730 000", "14 089 030 000"], True)
        # "193" could continue "5 988 000 000" or start a number: the greedy split has fewer cells
        # than columns, so the parser must not accept it.
        got, ok = split_values("5 988 000 000 193 667 000 000")
        assert ok and len(got) == 1

    def test_ambiguous_row_is_not_read_without_geometry(self):
        text = "Résultats de l'émission   BAT - 28 jours   BAT - 91 jours\n" \
               "Montant retenu (en FCFA)   5 988 000 000 193 667 000 000\n"
        a = parse_announcement(text)
        assert "amount_allocated" not in a.blocks[0].rows
        assert a.errors and "2 column(s)" in a.errors[0]

    @pytest.mark.skipif(not pdftotext_available(), reason="poppler pdftotext not installed")
    def test_ambiguous_row_split_by_printed_positions(self):
        _, a = read_announcement((FIX / "Annonce-au-MTP-CI-ES-26.11.2024.pdf").read_bytes())
        issue = next(b for b in a.blocks if b.kind == "issue")
        assert issue.labels[:2] == ["BAT - 28 jours", "BAT - 91 jours"]
        assert cells(issue, "amount_allocated") == ["5 988 000 000", "193 667 000 000", "12 700 000 000",
                                                    "50 000 000 000", "8 388 260 000", "4 256 380 000"]
        assert cells(issue, "amount_submitted")[:2] == ["6 006 000 000", "193 667 000 000"]

    def test_a_result_report_is_not_an_announcement(self):
        report = (UMOA_FIX / "Compte-Rendu-NE-ES-01.10.2026.txt").read_text(encoding="utf-8")
        assert ann_mod.is_result_report(report)
        assert not ann_mod.is_result_report((FIX / "Annonce-au-MTP-NE-ES-01.10.2026.txt").read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- mapping


def tranches_of(report_name: str, fixdir: Path = FIX):
    """Report columns as app.ingest.announcements.report_tranches builds them (no database)."""
    parsed = parse_compte_rendu((fixdir / report_name).read_text(encoding="utf-8"))
    out = []
    for i, t in enumerate(parsed.tranches):
        out.append(ann_mod.Tranche(t.value("isin"), t.kind or "issue",
                                   ann_mod.norm_label(f"{t.value('instrument')} {t.value('tenor') and t.fields['tenor'].raw}"),
                                   (1, 0, i), None))
    return out


class TestMapping:
    def test_headers_equal_to_report_tranches_in_order(self):
        a = ann("Annonce-au-MTP-NE-ES-01.10.2026.txt")
        mapped, unmapped = map_columns(a, tranches_of("Compte-Rendu-NE-ES-01.10.2026.txt", UMOA_FIX))
        assert not unmapped
        assert {k: (b.kind, i, m) for k, (b, i, m) in mapped.items()} == {
            "NE0000001310": ("issue", 0, "header"), "NE0000001526": ("issue", 1, "header"),
            "NE0000002458": ("issue", 2, "header"), "NE0000002771": ("issue", 3, "header"),
            "NE0000002797": ("issue", 4, "header")}

    def _tranche(self, isin, kind, label, n):
        return ann_mod.Tranche(isin, kind, label, (1, 0, n), None)

    def test_isin_headers_map_directly(self):
        a = ann("Annonce-au-MTP-CI-ES-06.03.2024.txt")
        reps = [self._tranche("CI0000007332", "issue", "BAT - 364 jours", 0),
                self._tranche("CI0000007340", "issue", "OAT - 3 ans", 1),
                self._tranche("CI0000007126", "buyback", "BAT - 77 jours", 2),
                self._tranche("CI0000004453", "buyback", "OAT - 102 jours", 3)]
        mapped, unmapped = map_columns(a, reps)
        b, i, m = mapped["CI0000007126"]
        assert (b.isins[i], m) == ("CI0000007126", "isin")
        assert b.rows["amount_submitted"][i].raw == "958 000 000"
        assert mapped["CI0000007340"][1:] == (1, "header")

    def test_same_distinct_labels_in_another_order(self):
        text = ("Résultats de l'émission   OAT - 3 ans   BAT - 364 jours\n"
                "Montant retenu (en FCFA)   1 000 000 000   2 000 000 000\n")
        reps = [self._tranche("X1", "issue", "BAT - 364 jours", 0), self._tranche("X2", "issue", "OAT - 3 ans", 1)]
        mapped, _ = map_columns(parse_announcement(text), reps)
        assert mapped["X1"][1] == 1 and mapped["X2"][1] == 0

    def test_repeated_labels_are_unmapped(self):
        text = ("Résultats de l'émission   OAT - 3 ans   OAT - 3 ans\n"
                "Montant retenu (en FCFA)   1 000 000 000   2 000 000 000\n")
        reps = [self._tranche("X1", "issue", "OAT - 3 ans", 0), self._tranche("X2", "issue", "OAT - 3 ans", 1)]
        mapped, unmapped = map_columns(parse_announcement(text), reps)
        assert not mapped and "repeated" in unmapped["X1"]

    def test_different_labels_are_unmapped(self):
        # Mali 03.09.2025: the announcement says "OAT - 7 ans", the report "6 ans" (a reopening).
        text = ("Résultats de l'émission   BAT - 364 jours   OAT - 7 ans\n"
                "Montant retenu (en FCFA)   1 000 000 000   2 000 000 000\n")
        reps = [self._tranche("X1", "issue", "BAT - 364 jours", 0), self._tranche("X2", "issue", "OAT - 6 ans", 1)]
        mapped, unmapped = map_columns(parse_announcement(text), reps)
        assert not mapped and "differ" in unmapped["X2"]

    def test_bare_single_column_maps_only_a_single_tranche(self):
        a = ann("Annonce-au-MTP-GW-EC-20.08.2024.txt")
        one = [self._tranche("GW0000000236", "buyback", "OAT - 28 jours", 0)]
        assert map_columns(a, one)[0]["GW0000000236"][2] == "single"
        two = one + [self._tranche("GW0000000999", "buyback", "BAT - 10 jours", 1)]
        mapped, unmapped = map_columns(a, two)
        assert not mapped and len(unmapped) == 2


# --------------------------------------------------------------------------- classification


class TestClassification:
    def test_identical(self):
        assert classify(D("4431250000"), "4 431,25 millions de F CFA", D("4431250000"), "4 431 250 000", True)[0] == "A"

    def test_rounding_whole_millions(self):
        cat, why = classify(D("45677000000"), "45 677 millions de F CFA", D("45676800000"), "45 676 800 000", True)
        assert cat == "B" and "step 1000000" in why

    def test_rounding_hundredths_of_a_million(self):
        assert classify(D("4431250000"), "4 431,25 millions", D("4431254000"), "4 431 254 000", True)[0] == "B"

    def test_rounding_price_two_decimals(self):
        assert classify(D("98.45"), "98,45%", D("98.4534"), "98,4534%", False)[0] == "B"

    def test_announcement_coarser_is_consistent(self):
        assert classify(D("96.2654"), "96,2654%", D("96.27"), "96,27%", False)[0] == "A2"
        assert classify(D("94.005"), "94,0050%", D("94.00"), "94,00%", False)[0] == "A2"  # half-even

    @pytest.mark.parametrize("stored,raw,exact,exact_raw,amount", [
        # GW 08.08.2024: report "4 450,55 millions" vs announcement "4 450 660 000".
        (D("4450550000"), "4 450,55 millions de F CFA", D("4450660000"), "4 450 660 000", True),
        # More than half a step away (rounded value of 29 936 350 000 is 29 936, not 29 937).
        (D("29937000000"), "29 937 millions de FCFA", D("29936350000"), "29 936 350 000", True),
        # Truncation instead of rounding is not the relation we prove.
        (D("98.45"), "98,45%", D("98.4561"), "98,4561%", False),
        # Report printed 4 decimals: no rounding to explain a different 4-decimal value.
        (D("3.0000"), "3,0000%", D("5.1000"), "5,1000%", False),
        # The unit matters: same digits in another unit are not a rounding.
        (D("29936"), "29 936", D("29936350000"), "29 936 350 000", True),
        # Integers (bidders) are never refined.
        (D("4"), "4", D("6"), "6", False),
    ])
    def test_everything_else_is_a_discrepancy(self, stored, raw, exact, exact_raw, amount):
        assert classify(stored, raw, exact, exact_raw, amount)[0] == "C"

    def test_not_printed_or_not_stored(self):
        assert classify(None, "x", D(1), "1", True)[0] == "D"
        assert classify(D(1), "1", None, None, True)[0] == "D"


# --------------------------------------------------------------------------- campaign + amend


LISTING = "https://www.umoatitres.org/fr/emissions/"


def _listing_html(op_url, day):
    return (f"<table id='emission-hub-passees-par'><tbody><tr><td>Sénégal<br><i>OAT</i></td><td>OAT</td><td></td>"
            f"<td>{day}</td><td></td><td></td><td></td><td></td><td><a href='{op_url}'>Plus</a></td>"
            f"<td>réalisée</td><td></td></tr></tbody></table>")


class Server:
    """Fake umoatitres.org serving the real fixture documents (as their text)."""

    def __init__(self, op_slug: str, day: str, report: str, announcement: str):
        self.op_url = f"https://www.umoatitres.org/fr/emission/{op_slug}/"
        self.report_url = BASE + report.replace(".txt", ".pdf")
        self.ann_url = BASE + announcement.replace(".txt", ".pdf")
        self.report_bytes = (FIX / report).read_bytes()
        self.ann_bytes = (FIX / announcement).read_bytes()
        page = (f"<h3>Annonce</h3><a href='{self.ann_url}'>x</a>"
                f"<h3>Compte rendu</h3><a href='{self.report_url}'>x</a>")
        self.pages = {LISTING: _listing_html(self.op_url, day).encode(), self.op_url: page.encode(),
                      self.report_url: self.report_bytes, self.ann_url: self.ann_bytes}
        self.calls: list[str] = []

    def __call__(self, url: str) -> umoa.Fetched:
        self.calls.append(url)
        body = self.pages.get(url, b"")
        return umoa.Fetched(200 if body else 404, url, body, "application/pdf")


@pytest.fixture
def store(tmp_path, monkeypatch):
    from app.config import get_settings

    monkeypatch.setattr(get_settings(), "document_store_dir", str(tmp_path / "docs"))
    return tmp_path / "docs"


def _verified_auctions(db, server: Server) -> list[Auction]:
    """Stage the real report as the ingester would, then approve every tranche (VERIFIED)."""
    source = umoa.get_source(db)
    doc = SourceDocument(source_id=source.source_id, url=server.report_url, title="report",
                         document_type="auction_result",
                         content_sha256=hashlib.sha256(server.report_bytes).hexdigest())
    db.add(doc)
    db.flush()
    parsed = parse_compte_rendu(server.report_bytes.decode("utf-8"))
    rows = [umoa._upsert_extraction(db, doc, parsed, t) for t in parsed.tranches]
    db.flush()
    return [approve(db, r.extraction_id, "test reviewer") for r in rows]


def _auction(db, isin):
    return db.scalar(select(Auction).join(Security).where(Security.isin == isin, Auction.is_synthetic.is_(False)))


SN = ("emission-sn-31-05-2024", "31/05/2024", "Compte-Rendu-SN-ES-31.05.2024.txt", "Annonce-au-MTP-SN-ES-31.05.2024.txt")
GW = ("emission-gw-08-08-2024", "08/08/2024", "Compte-Rendu-GW-ES-08.08.2024.txt", "Annonce-au-MTP-GW-ES-08.08.2024.txt")


class TestCampaignAndAmend:
    def test_cross_check_stores_announcement_and_proposes_exact_values(self, db, store):
        server = Server(*SN)
        _verified_auctions(db, server)
        report = ann_mod.run(db, server)
        s = report["stats"]
        assert (s["auctions"], s["auctions_mapped"], s["auctions_unmapped"]) == (3, 3, 0)
        doc = db.scalar(select(SourceDocument).where(SourceDocument.url == server.ann_url))
        assert doc.document_type == "auction_results_announcement"
        assert doc.content_sha256 == hashlib.sha256(server.ann_bytes).hexdigest()
        data = proposals(report)
        got = {(r["isin"], r["field"]): (r["stored"], r["proposed"]) for r in data["refinements"]}
        assert got == {
            ("SN0000003161", "amount_submitted"): ("45677000000", "45676800000"),
            ("SN0000003161", "amount_allocated"): ("32178000000", "32178130000"),
            ("SN0000003179", "amount_submitted"): ("10910000000", "10910370000"),
            ("SN0000003179", "amount_allocated"): ("10541000000", "10540870000"),
        }
        assert data["discrepancies"] == []
        assert not any(_auction(db, i).amount_submitted != D(v[0]) for (i, f), v in got.items()
                       if f == "amount_submitted")  # the cross-check itself never writes

    def test_amend_applies_category_b_with_evidence_and_is_idempotent(self, db, store, tmp_path):
        server = Server(*SN)
        _verified_auctions(db, server)
        data = proposals(ann_mod.run(db, server))
        dry = amend.apply(db, data, do_apply=False, fetch=server, today="2026-10-04")
        assert (dry["verified"], dry["applied"]) == (4, 0)
        assert _auction(db, "SN0000003161").amount_submitted == D("45677000000")
        done = amend.apply(db, data, do_apply=True, fetch=server, today="2026-10-04", commit=False)
        assert (done["verified"], done["applied"], done["failed"]) == (4, 4, [])
        a = _auction(db, "SN0000003161")
        assert (a.amount_submitted, a.amount_allocated) == (D("45676800000"), D("32178130000"))
        assert a.verification_status == VerificationStatus.VERIFIED and a.data_nature == DataNature.FACT
        sha = hashlib.sha256(server.ann_bytes).hexdigest()
        assert (f"amount_submitted refined from 45677000000 to 45676800000 on 2026-10-04: exact figure printed in "
                f"{server.ann_url} (sha256 {sha}); the result report printed the rounded value "
                f"'45 677 millions de F CFA'") in a.provenance_notes
        untouched = _auction(db, "SN0000003153")  # BAT: identical in both documents
        assert untouched.amount_submitted == D("26325000000") and "refined" not in untouched.provenance_notes
        again = amend.apply(db, data, do_apply=True, fetch=server, today="2026-10-05", commit=False)
        assert (again["applied"], again["already_applied"]) == (0, 4)
        assert a.provenance_notes.count("refined from") == 2
        # The verified dataset export carries the refined values and they load back.
        path = tmp_path / "verified.json"
        verified.export(db, path)
        row = next(r for r in json.loads(path.read_text())["auctions"] if r["isin"] == "SN0000003161")
        assert D(row["amount_submitted"]) == D("45676800000") and "refined from" in row["provenance_notes"]
        assert verified._coerce(Auction, row)["amount_allocated"] == D("32178130000")

    @pytest.mark.parametrize("tamper,why", [
        ("bytes", "SHA-256"),
        ("missing", "download failed"),
        ("line", "not printed in the announcement"),
        ("proposed", "record proposes"),
        ("stored_changed", "stored value is now"),
        ("report_raw", "not printed in the result report"),
    ])
    def test_amend_fails_closed(self, db, store, tamper, why):
        server = Server(*SN)
        _verified_auctions(db, server)
        data = proposals(ann_mod.run(db, server))
        rec = data["refinements"][0]
        if tamper == "bytes":
            server.pages[server.ann_url] = server.ann_bytes.replace(b"45 676 800 000", b"45 676 900 000")
        elif tamper == "missing":
            server.pages[server.ann_url] = b""
        elif tamper == "line":
            rec["announcement_line"] = rec["announcement_line"].replace("000", "001", 1)
        elif tamper == "proposed":
            rec["proposed"] = str(D(rec["proposed"]) + 1)
        elif tamper == "stored_changed":
            setattr(_auction(db, rec["isin"]), rec["field"], D(rec["stored"]) + 1000000)
        elif tamper == "report_raw":
            rec["report_raw"] = "45 999 millions de F CFA"
        before = getattr(_auction(db, rec["isin"]), rec["field"])
        out = amend.apply(db, {"refinements": [rec]}, do_apply=True, fetch=server, commit=False)
        assert out["applied"] == 0 and len(out["failed"]) == 1 and why in out["failed"][0]["why"]
        assert getattr(_auction(db, rec["isin"]), rec["field"]) == before

    def test_discrepancy_is_flagged_and_never_applied(self, db, store):
        server = Server(*GW)
        _verified_auctions(db, server)
        data = proposals(ann_mod.run(db, server))
        (c,) = [d for d in data["discrepancies"] if d["isin"] == "GW0000001242"]
        assert (c["field"], c["stored"], c["announcement_value"]) == ("amount_submitted", "4450550000", "4450660000")
        assert c["report_raw"] == "4 450,55 millions de F CFA" and c["status"] == "flagged_for_human"
        assert not any(r["isin"] == "GW0000001242" and r["field"] == "amount_submitted" for r in data["refinements"])
        # Even if someone moved it into the refinements, the rounding relation is re-checked.
        forced = {"refinements": [{**c, "proposed": c["announcement_value"]}]}
        out = amend.apply(db, forced, do_apply=True, fetch=server, commit=False)
        assert out["applied"] == 0 and "rounding relation does not hold" in out["failed"][0]["why"]
        assert _auction(db, "GW0000001242").amount_submitted == D("4450550000")
