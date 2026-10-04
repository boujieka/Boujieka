"""BEAC (CEMAC) auction results: listing, double-OCR parsing, strict checks, promotion.

OCR itself is not run here (it needs tesseract and takes seconds per page): the fixtures in
tests/fixtures/beac are line samples of the two OCR passes of real notices ("label || value"),
turned into word boxes with a fixed geometry so that the parser sees what it sees on a page.
"""

import json
from datetime import date
from decimal import Decimal as D
from pathlib import Path

import pytest
from sqlalchemy import select

from app.ingest import beac, beac_check
from app.ingest.beac_check import check, luhn_isin_ok
from app.ingest.beac_extract import (
    EXTRACTOR,
    parse_amount,
    parse_announcement,
    parse_code_line,
    parse_date,
    parse_pass,
    parse_percent,
    rows_from_passes,
    stage_rows,
)
from app.ingest.beac_ocr import SIGNATURE, DocumentOcr, PageOcr, PassConfig, PassResult, Word
from app.models import Auction, AuctionExtraction, Security, SourceDocument
from app.models.enums import VerificationStatus

FIX = Path(__file__).parent / "fixtures" / "beac"
PAGE_W, PAGE_H = 2480, 3508
VALUE_X = 1600


def page_from_lines(lines: list[str], page: int = 1) -> PageOcr:
    """Synthetic word boxes: label words from x=150, the value column (after '||') at x=1600."""
    words: list[Word] = []
    top = 40
    for i, line in enumerate(lines):
        # Continuation lines of a multi-line label (lower-case start, or a bare value) sit closer
        # to the line above than a new label does, as on the printed page.
        top += 45 if (line[:1].islower() or line.startswith("||")) else 75
        label, _, value = line.partition("||")
        x = 150
        for t in label.split():
            words.append(Word(t, x, top, 18 * len(t), 40, 95.0, 1, 1, i + 1))
            x += 18 * len(t) + 15
        x = VALUE_X
        for t in value.split():
            words.append(Word(t, x, top, 18 * len(t), 40, 95.0, 1, 2, i + 1))
            x += 18 * len(t) + 15
    return PageOcr(page, PAGE_W, PAGE_H, "\n".join(lines), words)


def load_fixture(name: str) -> DocumentOcr:
    text = (FIX / name).read_text(encoding="utf-8")
    parts: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        if line.startswith("=== "):
            current = line[4:].strip()
            parts[current] = []
        elif current and line.strip():
            parts[current].append(line)
    if parts.get("B") == ["same as A"]:
        parts["B"] = list(parts["A"])
    passes = {k: PassResult(PassConfig(k, 300, 4, 0), [page_from_lines(v)]) for k, v in parts.items()}
    return DocumentOcr(SIGNATURE, passes, 1)


def staged(name: str):
    ocr = load_fixture(name)
    return rows_from_passes(parse_pass(ocr.passes["A"].pages, "A"), parse_pass(ocr.passes["B"].pages, "B"))


# --------------------------------------------------------------------------- listing


LISTING = """<table id="documents_contenu_cpt"><thead><tr><th>Titre du document</th></tr></thead><tbody>
<tr><td><a href="https://www.beac.int/wp-content/uploads/2016/11/Communiqu%C3%A9-des-r%C3%A9sultats-BTA-26-semaines-du-15-septembre-2026.pdf">Communiqué des résultats BTA 26 semaines du 15 septembre 2026 - Congo</a></td><td>233 KB</td><td>Congo</td><td>2026</td></tr>
<tr><td><a href="https://www.beac.int/wp-content/uploads/2016/11/Communiqu%C3%A9-dannonce-BTA-13-semaines-du-22-septembre-2026.pdf">Communiqué dannonce BTA 13 semaines du 22 septembre 2026 - Congo</a></td><td>352 KB</td><td>Congo</td><td>2026</td></tr>
<tr><td><a href="https://www.beac.int/wp-content/uploads/2021/03/Auctions-results-CMR-10-03-2021.pdf">Auction results communique of the Republic of Cameroon - 10th March 2021 session</a></td><td>1 MB</td><td>Cameroun</td><td>2021</td></tr>
<tr><td><a href="https://www.beac.int/wp-content/uploads/2021/06/Aviso-de-comunicado-BTA-GE-09-06-2021.pdf">Aviso de comunicado de la emision de BTA del 09 de Junio 2021 - Republica de Guinea Ecuatorial</a></td><td>1 MB</td><td>Guinée Equatoriale</td><td>2021</td></tr>
<tr><td><a href="https://www.beac.int/x/Rapport-hebdo.pdf">Rapport hebdomadaire des opérations du marché des valeurs du trésor de la CEMAC</a></td><td>1 MB</td><td>CEMAC</td><td>2022</td></tr>
<tr><td><a href="https://www.beac.int/x/SRIF.pdf">Calcul d'Indicateurs d'Inclusion Financière du Gabon</a></td><td>1 MB</td><td>Gabon</td><td>2025</td></tr>
</tbody></table>"""


def test_listing_classification_and_dates():
    entries = beac.parse_listing(LISTING)
    assert [e.kind for e in entries] == ["result", "announcement", "result", "announcement", "weekly_report", "other"]
    assert [e.language for e in entries[:4]] == ["fr", "fr", "en", "es"]
    assert entries[0].listing_date == date(2026, 9, 15)
    assert entries[2].listing_date == date(2021, 3, 10)
    assert entries[4].listing_date == date(2022, 1, 1)  # no date in the title: Année column
    chosen = beac.select_entries(entries, {"result"}, date(2026, 1, 1), None, None)
    assert [e.year for e in chosen] == [2026]


def test_polite_fetch_identifies_itself():
    assert beac.USER_AGENT.startswith("CartoucheIngest/1.0")
    assert beac.REQUEST_PAUSE_SECONDS >= 1


# --------------------------------------------------------------------------- numbers and code line


@pytest.mark.parametrize("raw,value,status", [
    ("27 550,19", D("27550.19"), None), ("10 000", D("10000"), None), ("4510", D("4510"), None),
    ("8 543,26", D("8543.26"), None), ("0", D("0"), None), ("3.400", None, "ambiguous_number"),
    ("ls 000", None, "unreadable"), ("1 5 000", None, "unreadable"),
])
def test_parse_amount(raw, value, status):
    n = parse_amount(raw)
    assert (n.value, n.status) == (value, status)


@pytest.mark.parametrize("raw,value", [("7,00%", D("7.00")), ("6,0000%", D("6.0000")), ("96,00", D("96.00")),
                                       ("100.00%", D("100.00")), ("166,6667%", D("166.6667")),
                                       ("7 00%", None), ("6,007o", None)])
def test_parse_percent(raw, value):
    assert parse_percent(raw).value == value


def test_code_line_and_dates():
    c = parse_code_line("4+ Code Emission CG1200002133 BTA-26 18-MARS-2027")
    assert (c["isin"], c["instrument_printed"], c["tenor"], c["maturity_date"]) == (
        "CG1200002133", "BTA", "26 semaines", "2027-03-18")
    c = parse_code_line("e Code Emission CM2J00000279 OTA-03 ANS 6,25% 16-SEPT-2029")
    assert (c["tenor"], c["coupon_rate"], c["maturity_date"]) == ("3 ans", "6.25", "2029-09-16")
    c = parse_code_line("Code Emission : CF2A00000132 OTA-2 ANS 6.25% 16 septembre — 2028")
    assert (c["isin"], c["coupon_rate"], c["maturity_date"]) == ("CF2A00000132", "6.25", "2028-09-16")
    assert parse_code_line("Code Emission GQ1300000734 BTA-52 08- JANV -2021")["maturity_date"] == "2021-01-08"
    # Space after the country letters, glued punctuation: the code is the 12 characters.
    assert parse_code_line("Code Emission : a TD 1200001147 BTA-26 10-Septembre- 2021")["isin"] == "TD1200001147"
    assert parse_code_line("Code Emission : :GA2J00000127.OTA 3 ANS 5,50% 03-JUIL-2023")["isin"] == "GA2J00000127"
    assert parse_code_line("Code Emission : C62J00000875 OTA-3 ans 6,00% 17-SEPT -2029") == {}  # 'G' read as '6'
    assert parse_date("SEANCE DU 14 AOÛT 2019")[0] == date(2019, 8, 14)
    assert parse_date("- 15\" January 2020 session-")[0] == date(2020, 1, 15)
    assert parse_date("Jeudi 24 septembre 2026avant 15 h 00")[0] == date(2026, 9, 24)
    assert parse_date("31 février 2026")[0] is None


def test_isin_check_digit():
    """BEAC issue codes are genuine ISINs (Luhn check digit)."""
    for code in ("CG1200002133", "CM2J00000279", "CF2A00000132", "GA1100002292", "TD2A00001246", "GQ1300000734"):
        assert luhn_isin_ok(code), code
    assert not luhn_isin_ok("CF2A00000056")  # as printed on the RCA notice of 14 Sep 2026
    assert not luhn_isin_ok("CG12000O2133")


# --------------------------------------------------------------------------- double reading


def test_two_passes_must_agree_field_by_field():
    (row,) = staged("cog_bta26_2026-09-15.txt")
    f = row.fields
    assert row.tranche_key == "CG1200002133"
    assert f["amount_offered"].value == "10000000000"  # 10 000 millions, exactly x 10^6
    assert f["amount_submitted"].value == f["amount_allocated"].value == "5340000000"
    assert f["coverage_pct"].value == "53.40"  # value on the continuation line of a 3-line label
    assert f["auction_date"].value == "2026-09-15"
    assert f["limit"].value == f["weighted_average"].value == "7.00"
    # The two misreads: no value, both readings kept for the reviewer.
    for name, a, b in (("network_size", "25", "20"), ("number_of_participants", "9", "5")):
        assert f[name].value is None and f[name].status == "ocr_disagreement"
        assert (f[name].readings["A"]["value"], f[name].readings["B"]["value"]) == (a, b)


def test_multi_security_notice_gives_one_row_per_code():
    rows = staged("caf_ota_2026-09-14.txt")
    assert [r.tranche_key for r in rows] == ["CF2A00000132", "CF2A00000056"]
    first = rows[0].fields
    assert first["coverage_pct"].value == "45.10"  # not the "soumissions retenues" ratio
    assert first["amount_submitted"].value == "4510000000"
    assert rows[1].fields["amount_submitted"].value == "8543260000.00"
    assert rows[1].fields["limit"].value == "92.00"  # "92.00" and "92,00" are the same decimal


def test_announcement_settlement_dates():
    (rec,) = parse_announcement(load_fixture("cog_annonce_bta13_2026-09-22.txt"))
    assert rec["isin"] == "CG1100001458"
    assert (rec["auction_date"], rec["settlement_date"], rec["value_date"]) == ("2026-09-22", "2026-09-24", "2026-09-24")


# --------------------------------------------------------------------------- strict check


def as_extraction(row, extraction_id=1, instrument=None) -> AuctionExtraction:
    from app.ingest.beac_extract import ISIN_PREFIX_COUNTRY, _instrument_for_queue, queue_fields

    fields, status = queue_fields(row)
    isin = row.fields["isin"].value
    ad = row.fields["auction_date"].value
    return AuctionExtraction(
        extraction_id=extraction_id, tranche_key=row.tranche_key, extractor=EXTRACTOR, parse_status="complete",
        country_iso3=ISIN_PREFIX_COUNTRY.get((isin or "")[:2]), isin=isin,
        instrument=_instrument_for_queue(row.fields["instrument_printed"].value),
        auction_date=date.fromisoformat(ad) if ad else None, fields=fields, field_status=status,
        operation={**row.operation, "tranche_count": 1, "coverage_bids_pct": row.fields["coverage_pct"].as_dict()},
    )


def test_strict_check_passes_a_clean_row_and_ignores_unreadable_optional_counts():
    rows = staged("caf_ota_2026-09-14.txt")
    v = check(as_extraction(rows[0]))
    assert v.ok, v.reasons


def test_strict_check_holds_a_bad_check_digit():
    rows = staged("caf_ota_2026-09-14.txt")
    v = check(as_extraction(rows[1]))
    assert any("check digit" in r for r in v.reasons)


def test_strict_check_holds_disagreeing_counts():
    (row,) = staged("cog_bta26_2026-09-15.txt")
    v = check(as_extraction(row))
    assert any(r.startswith("(a) network_size: ocr_disagreement") for r in v.reasons)
    assert any(r.startswith("(a) number_of_participants: ocr_disagreement") for r in v.reasons)
    assert not any(r.startswith(("(c)", "(d)", "(e)", "(b)")) for r in v.reasons), v.reasons


def _tamper(ext: AuctionExtraction, name: str, value: str, raw: str | None = None) -> None:
    fields = json.loads(json.dumps(ext.fields))
    fd = fields[name]
    fd["value"] = value
    for p in ("A", "B"):
        fd["ocr"][p]["value"] = value
    if raw:
        fd["raw"] = raw
    ext.fields = fields


def test_strict_check_arithmetic_and_coverage():
    rows = staged("caf_ota_2026-09-14.txt")
    ext = as_extraction(rows[0])
    _tamper(ext, "amount_allocated", "5000000000")
    assert any(r.startswith("(c) allotted") for r in check(ext).reasons)

    ext = as_extraction(rows[0])
    _tamper(ext, "amount_submitted", "4610000000")  # coverage 45,10 % no longer matches
    assert any(r.startswith("(d)") for r in check(ext).reasons)

    ext = as_extraction(rows[0])
    _tamper(ext, "limit", "94.50")  # price: the limit cannot exceed the weighted average
    assert any("price: limit" in r for r in check(ext).reasons)

    ext = as_extraction(rows[0])
    _tamper(ext, "maturity_date", "2031-09-16")  # 2-year OTA maturing 5 years later
    assert any(r.startswith("(e) OTA 2 years") for r in check(ext).reasons)


def test_low_confidence_holds():
    rows = staged("caf_ota_2026-09-14.txt")
    ext = as_extraction(rows[0])
    fields = json.loads(json.dumps(ext.fields))
    fields["amount_offered"]["ocr"]["B"]["conf"] = 41.0
    ext.fields = fields
    assert any("low OCR confidence in pass B" in r for r in check(ext).reasons)


# --------------------------------------------------------------------------- staging → promotion


def _store(tmp_path: Path, name: str, ocr: DocumentOcr) -> str:
    pdf = tmp_path / f"{name}.pdf"
    pdf.write_bytes(b"%PDF-1.4 fixture")
    pdf.with_suffix(".ocr.json").write_text(ocr.to_json(), encoding="utf-8")
    return str(pdf)


def test_stage_check_and_promote(db, tmp_path):
    source = beac.get_or_create_source(db)
    assert source.country_id is None and source.institution.startswith("Banque des États")
    res = SourceDocument(source_id=source.source_id, url="https://www.beac.int/x/caf-resultats.pdf",
                         title="BEAC — résultats CAF", document_type="auction_result", content_sha256="a" * 64,
                         storage_path=_store(tmp_path, "res", load_fixture("caf_ota_2026-09-14.txt")))
    db.add(res)
    db.flush()
    from app.ingest.beac_extract import extract_result

    rows = extract_result(db, res, load_fixture("caf_ota_2026-09-14.txt"))
    assert len(rows) == 2 and all(r.verification_status == VerificationStatus.UNVERIFIED for r in rows)
    assert rows[0].operation["attribution"] == beac.ATTRIBUTION

    out = beac_check.run(db, do_approve=True)
    assert (out["passed"], out["approved"], out["held"]) == (1, 1, 1)
    ok = db.scalar(select(AuctionExtraction).where(AuctionExtraction.tranche_key == "CF2A00000132"))
    assert ok.verification_status == VerificationStatus.VERIFIED and ok.reviewed_by == beac_check.REVIEWER
    a = db.get(Auction, ok.promoted_auction_id)
    assert a.amount_offered == D("10000000000") and a.amount_allocated == D("4510000000")
    assert a.average_price == D("94.00") and a.cutoff_yield is None
    assert a.reported_bid_to_cover == D("0.451")
    assert a.settlement_date is None and a.field_status["settlement_date"] == "not_available"
    assert a.yield_convention.startswith("BEAC") and beac.ATTRIBUTION in a.provenance_notes
    sec = db.get(Security, a.security_id)
    assert (sec.isin, sec.coupon_rate, sec.maturity_date) == ("CF2A00000132", D("6.25"), date(2028, 9, 16))
    assert sec.currency == "XAF"
    held = db.scalar(select(AuctionExtraction).where(AuctionExtraction.tranche_key == "CF2A00000056"))
    assert held.verification_status == VerificationStatus.UNVERIFIED
    assert any("check digit" in r for r in held.checks[0]["reasons"])


def test_settlement_date_from_matching_announcement(db, tmp_path):
    source = beac.get_or_create_source(db)
    ann = SourceDocument(source_id=source.source_id, url="https://www.beac.int/x/annonce.pdf", title="annonce",
                         document_type="auction_announcement", content_sha256="b" * 64,
                         storage_path=_store(tmp_path, "ann", load_fixture("cog_annonce_bta13_2026-09-22.txt")))
    db.add(ann)
    db.flush()
    idx = beac_check.announcement_index(db, source.source_id)
    ext = AuctionExtraction(isin="CG1100001458", auction_date=date(2026, 9, 22))
    rec, why = beac_check.settlement_for(ext, idx)
    assert why == "ok" and rec["settlement_date"] == "2026-09-24"
    ext.auction_date = date(2026, 9, 29)  # a later reopening: no announcement for that date
    assert beac_check.settlement_for(ext, idx)[0] is None


# --------------------------------------------------------------------------- layout rules


def _page(rows: list[tuple[int, str, str]]) -> PageOcr:
    """(top, label, value) rows with explicit vertical positions (value column at x=1600)."""
    words = []
    for n, (top, label, value) in enumerate(rows):
        x = 150
        for t in label.split():
            words.append(Word(t, x, top, 18 * len(t), 40, 95.0, 1, 1, 2 * n + 1))
            x += 18 * len(t) + 15
        x = VALUE_X
        for t in value.split():
            # the values of this page sit 25 px above their label (skewed scan), each on its own
            # OCR line, as tesseract returns them
            words.append(Word(t, x, top - 25, 18 * len(t), 40, 95.0, 2, 1, 2 * n + 2))
            x += 18 * len(t) + 15
    return PageOcr(1, PAGE_W, PAGE_H, "", words)


def test_values_go_to_the_nearest_label_never_to_the_neighbour():
    page = _page([
        (100, "Séance du 12 février 2020", ""),
        (200, "Code Emission CM1200000865 BTA-26 14-AOUT-2020", ""),
        (300, "Total amount announced (in millions of CFAF)", "20 000"),
        (380, "Total amount of bids (in millions of CFAF)", "18 900"),
        (460, "Total amount served (in millions of CFAF)", "5 200"),
        (540, "Coverage rate of amount", "94,50%"),
    ])
    (blk,) = parse_pass([page], "A").blocks
    assert {k: r.value for k, r in blk.readings.items()} == {
        "amount_offered": "20000000000", "amount_submitted": "18900000000",
        "amount_allocated": "5200000000", "coverage_pct": "94.50"}


def test_garbage_in_the_value_column_is_unreadable_not_borrowed():
    """'0' read as '6)': the label must not take the value printed on the line above."""
    page = _page([
        (100, "Séance du 19 août 2025", ""),
        (200, "Code Emission CG1300000979 BTA-52 20-AOUT-2026", ""),
        (300, "Montant total des soumissions (en millions de", "153"),
        (380, "Montant total servi (en millions de FCFA) || 6)", ""),
    ])
    # put "6)" in the value column of the "servi" line
    for w in page.words:
        if w.text == "||":
            page.words.remove(w)
    six = next(w for w in page.words if w.text == "6)")
    six.left = VALUE_X
    (blk,) = parse_pass([page], "A").blocks
    assert blk.readings["amount_submitted"].value == "153000000"
    assert blk.readings["amount_allocated"].value is None
    assert blk.readings["amount_allocated"].status == "unreadable"
