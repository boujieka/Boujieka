"""Quarterly report (site/report.py): calculations on hand-built rows, and the edition split."""

import importlib.util
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

SITE = Path(__file__).resolve().parents[2] / "site"
spec = importlib.util.spec_from_file_location("report", SITE / "report.py")
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


def row(country="SEN", d="2026-08-01", typ="primary_auction", alloc=None, sub=None, yld=None,
        instr="treasury_bond", mat="2029-08-01", url="https://www.umoatitres.org/x.pdf", isin="SN0"):
    dd = date.fromisoformat(d)
    m = date.fromisoformat(mat) if mat else None
    dec = lambda v: None if v is None else Decimal(str(v))  # noqa: E731
    return {"country": country, "date": dd, "type": typ, "isin": isin, "name": isin, "instr": instr, "maturity": m,
            "residual_years": (m - dd).days / 365.25 if m else None, "alloc": dec(alloc), "sub": dec(sub),
            "yld": dec(yld), "url": url}


def test_quarter_helpers():
    assert report.quarter(date(2026, 9, 30)) == (2026, 3)
    assert report.shift((2026, 1), -1) == (2025, 4)
    assert report.shift((2026, 3), -4) == (2025, 3)
    assert report.bounds((2026, 4)) == (date(2026, 10, 1), date(2026, 12, 31))
    rows = [row(d="2026-09-30"), row(d="2026-10-01")]
    assert report.complete_quarters(rows, date(2026, 10, 4)) == [(2026, 3)]  # Q4 not finished


def test_stats_excludes_buybacks_and_weights_by_allotted_amount():
    rows = [
        row(alloc=100e9, sub=150e9, yld=6),
        row(alloc=300e9, sub=300e9, yld=8, instr="treasury_bill", mat="2027-02-01"),
        row(alloc=50e9, sub=None, yld=None),           # no published yield or bid amount
        row(typ="buyback", alloc=999e9, sub=999e9, yld=1),  # never counted as issuance
    ]
    s = report.stats(rows)
    assert s["n"] == 3 and s["bb_n"] == 1 and s["bb_amount"] == Decimal("999e9")
    assert s["alloc"] == Decimal("450e9")
    assert s["yld"] == Decimal(7.5)  # (6*100 + 8*300) / 400
    assert s["ratio"] == Decimal(450) / Decimal(400)  # only rows with both amounts
    assert s["no_yield"] == 1
    assert s["bills"] == Decimal("300e9") and s["bonds"] == Decimal("150e9")
    assert s["buckets"]["b1"]["n"] == 1 and s["buckets"]["b3"]["n"] == 2  # 0.5 y and 3 y residual


def test_stats_on_empty_quarter_reports_nothing_rather_than_zero():
    s = report.stats([row(typ="buyback", alloc=1e9)])
    assert s["n"] == 0 and s["alloc"] is None and s["yld"] is None and s["ratio"] is None


def test_deltas_and_formats():
    assert report.delta_amount(Decimal(110), Decimal(100), "fr") == "+10,0 %"
    assert report.delta_amount(Decimal(90), Decimal(100), "en") == "−10.0%"
    assert report.delta_bp(Decimal("7.25"), Decimal("7.00"), "fr") == "+25 pb"
    assert report.delta_amount(Decimal(1), None, "fr") is None
    assert report.fmt_bn(Decimal("2331866050000"), "fr") == "2 331,9 Md FCFA"


@pytest.mark.parametrize("lang", ["fr", "en"])
def test_preview_has_no_country_pages_and_complete_has_them(lang):
    rows = [row(country=c, alloc=10e9, sub=12e9, yld=7) for c in ("SEN", "CIV")]
    prev = report.render((2026, 3), rows, date(2026, 10, 4), lang, "preview", "https://example.org/buy", {}, embed=False)
    full = report.render((2026, 3), rows, date(2026, 10, 4), lang, "complete", None, {}, embed=True)
    assert prev.count('class="page"') + prev.count('class="page ') == 5  # cover, summary, countries, method, credits
    assert full.count('class="chead"') == 2 and "https://www.umoatitres.org/x.pdf" in full
    assert "https://example.org/buy" in prev and "example.org" not in full
    assert "x.pdf" not in prev  # source list and operations stay in the complete edition


def test_emblem_manifest_is_consistent():
    p = report.EMBLEMS / "emblems.json"
    if not p.exists():
        pytest.skip("emblems not fetched")
    import hashlib
    for iso3, kinds in json.loads(p.read_text())["countries"].items():
        for kind, e in kinds.items():
            body = (report.EMBLEMS / e["file"]).read_bytes()
            assert hashlib.sha256(body).hexdigest() == e["sha256"], (iso3, kind)
            assert e["page"].startswith("https://commons.wikimedia.org/") and e["license"]
            assert b"<script" not in body.lower()


def _load(name):
    import sys
    sys.path.insert(0, str(SITE))  # brief/dataset import `report` by name
    s = importlib.util.spec_from_file_location(name, SITE / f"{name}.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def test_brief_window_and_totals_match_the_verified_data():
    brief = _load("brief")
    b = brief.build(date(2026, 10, 4))
    rows = report.load_rows()
    lo = date.fromisoformat(b["from"])
    assert lo == date(2026, 9, 28)
    assert len(b["results"]) == sum(1 for r in rows if lo <= r["date"] <= date(2026, 10, 4))
    issue = [r for r in rows if lo <= r["date"] <= date(2026, 10, 4) and r["type"] not in report.NON_ISSUANCE]
    assert b["totals"]["current"]["n"] == len(issue)
    assert Decimal(b["totals"]["current"]["allotted"]) == sum((r["alloc"] or 0 for r in issue), Decimal(0))
    assert all(date(2026, 10, 4) < date.fromisoformat(m["maturity"]) <= date(2026, 10, 18) for m in b["maturing"])
    html = brief.email_html(b, "fr")
    assert "<script" not in html and "conseil" in html


def test_dataset_files_keep_every_verified_row_and_the_sample_stays_small(tmp_path):
    import csv
    dataset = _load("dataset")
    out = dataset.write(date(2026, 10, 4), tmp_path / "dist", tmp_path / "private")
    full = list(csv.DictReader(open(tmp_path / "private" / "auctions.csv", encoding="utf-8-sig")))
    sample = list(csv.DictReader(open(tmp_path / "dist" / "donnees" / "echantillon.csv", encoding="utf-8-sig")))
    assert len(full) == out["auctions"] == len(report.load_rows())
    assert len(sample) == dataset.SAMPLE and set(sample[0]) == set(full[0])
    assert all(r["source_url"].startswith("https://www.umoatitres.org/") and len(r["document_sha256"]) == 64 for r in full)
    assert not (tmp_path / "dist" / "donnees" / "auctions.csv").exists()  # full file never in the deployed tree
