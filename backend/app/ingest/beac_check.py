"""Strict automatic check of staged BEAC (OCR) extractions; promotion of rows that pass.

Independent of app.ingest.autocheck (the UMOA-Titres checker, which compares a text layer and is
not applicable to scanned images). A staged BEAC row is approved ONLY if every check below holds;
otherwise it stays UNVERIFIED in the queue and the reasons are reported (and recorded in the row's
`checks`). Nothing is corrected, rounded or filled in by this module.

(a) double OCR. Every stored field was read identically by the two OCR passes (beac_ocr: different
    resolution, page segmentation and binarisation): the staged value is set only on agreement and
    each pass's own reading is re-compared here. Any field whose label was printed but which is
    unreadable, ambiguous ("3.400") or read differently by the two passes or in two copies of a
    bilingual notice holds the row. Every word of every stored value must also have an OCR
    confidence >= MIN_WORD_CONFIDENCE in both passes.
(b) issue code. Form CCxxxxxxxxxD (2 letters + 10 alphanumerics); prefix one of the six CEMAC
    country codes (CM CF TD CG GQ GA); BEAC codes are genuine ISINs, so the ISIN check digit
    (Luhn over the letters-to-digits expansion) must be valid — every code sampled during
    development was Luhn-valid, so a failure means a misread (or a misprint) and holds the row;
    the printed notice must name the same country (letterhead / text) in both passes.
(c) arithmetic. allotted <= submitted. When something was allotted: min <= weighted average <=
    max and min <= limit <= max; with the direction of the quotation: for rates (BTA, "Taux")
    weighted average <= limit (the limit is the highest accepted rate), for prices (OTA, "Prix")
    limit <= weighted average (the limit is the lowest accepted price). Plausibility: rates in
    (0, 30] %, prices in [50, 150] per 100.
(d) coverage. The printed "taux de couverture" equals submitted / offered x 100 within the
    printing precision: |printed - computed| <= one unit of the last printed decimal (this allows
    for rounding or truncation by the issuer). Independent cross-check of two amounts. Notices
    whose ratio is defined otherwise (e.g. submitted / allotted) fail and are held. When the
    notice also prints the coverage "par les soumissions retenues" (RCA), it must equal
    allotted / submitted x 100 the same way (a cross-check of the allotted amount).
(e) code line. Instrument consistent with the code (3rd character 1 = BTA, 2 = OTA); BTA: no
    coupon, tenor in weeks among 13/26/52 and the maturity n weeks (+-7 days) after the auction;
    OTA: coupon printed in (0, 15] %, tenor in years and the maturity after the auction and no later
    than auction + n years + 31 days (reopenings have a shorter remaining life).
(f) settlement date. Taken only from an announcement notice ("Communiqué d'annonce") of the same
    ISIN and the same auction date, read identically by both passes, between the auction date and
    10 days after it, and unique; otherwise NULL with field_status "not_available" (never a reason
    to hold).

Promotion goes through app.ingest.queue.approve (unchanged) with reviewer REVIEWER. approve() was
written for UMOA-Titres; afterwards this module adjusts only what approve() labels in UMOA terms:
yield_convention (BEAC wording), minimum/maximum bid (BEAC publishes them: stored for BTA, where
they are rates; for OTA they are prices and stay in the staging row) and the attribution note.

    python -m app.ingest.beac_check                    # dry run: report only
    python -m app.ingest.beac_check --approve --report out.json
"""

import argparse
import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingest.beac_extract import EXTRACTOR, ISIN_PREFIX_COUNTRY, parse_announcement
from app.ingest.beac_ocr import DocumentOcr
from app.ingest.queue import ReviewError, approve
from app.models import Auction, AuctionExtraction, SourceDocument
from app.models.enums import FieldStatus, VerificationStatus

REVIEWER = ("Controle strict OCR BEAC (double OCR + coherence) - autorisation de publication "
            "gratuite BEAC")
MIN_WORD_CONFIDENCE = 50.0
YIELD_CONVENTION_BTA = "BEAC: taux moyen pondéré (BTA, intérêts précomptés), as published"
YIELD_CONVENTION_OTA = "BEAC: prix moyen pondéré (OTA, % du nominal), as published"

# Fields whose value, when present, is stored (promoted or kept as a fact in the staging row).
STORED = ("isin", "instrument_printed", "tenor", "maturity_date", "coupon_rate", "auction_date",
          "network_size", "number_of_participants", "amount_offered", "amount_submitted",
          "amount_allocated", "minimum_bid", "maximum_bid", "limit", "weighted_average",
          "printed_yield_rate", "coverage_pct", "coverage_retained_pct")
REQUIRED = ("isin", "instrument_printed", "tenor", "maturity_date", "auction_date", "amount_offered",
            "amount_submitted", "amount_allocated", "coverage_pct")
REQUIRED_IF_ALLOTTED = ("minimum_bid", "maximum_bid", "limit", "weighted_average")
# Lines some formats do not print at all (Chad prints only the minimum and maximum bids): when
# NEITHER pass finds the label, the value is NULL with field_status "not_disclosed".
NOT_PRINTED_OK = ("limit", "weighted_average")
OPTIONAL = ("network_size", "number_of_participants", "printed_yield_rate", "coverage_retained_pct")
CODE_FIELDS = ("isin", "instrument_printed", "tenor", "maturity_date", "coupon_rate")


def luhn_isin_ok(code: str) -> bool:
    if len(code) != 12 or not code[:2].isalpha() or not code[-1].isdigit() or not code.isalnum():
        return False
    digits = "".join(str(int(c, 36)) for c in code[:-1].upper())
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch) * (2 if i % 2 == 0 else 1)
        total += d // 10 + d % 10
    return (10 - total % 10) % 10 == int(code[-1])


def _dec(v) -> Decimal | None:
    try:
        return Decimal(str(v)) if v is not None else None
    except (InvalidOperation, ValueError):
        return None


def _decimals(raw: str | None) -> int | None:
    if not raw:
        return None
    s = raw.strip().rstrip("%").strip()
    for sep in (",", "."):
        if sep in s:
            return len(s.rsplit(sep, 1)[1])
    return 0


@dataclass
class Verdict:
    extraction_id: int
    isin: str | None
    country: str | None
    auction_date: date | None
    reasons: list[str] = field(default_factory=list)
    settlement: dict | None = None

    @property
    def ok(self) -> bool:
        return not self.reasons


# --------------------------------------------------------------------------- announcements


def announcement_index(session: Session, source_id: int) -> dict[tuple[str, str], list[dict]]:
    """(ISIN, auction date) → agreed settlement readings from every stored announcement."""
    idx: dict[tuple[str, str], list[dict]] = {}
    docs = session.scalars(select(SourceDocument).where(
        SourceDocument.source_id == source_id, SourceDocument.document_type == "auction_announcement"))
    for doc in docs:
        cache = Path(doc.storage_path or "").with_suffix(".ocr.json")
        if not cache.is_file():
            continue
        try:
            recs = parse_announcement(DocumentOcr.from_json(cache.read_text(encoding="utf-8")))
        except (ValueError, KeyError):
            continue
        for r in recs:
            if r.get("isin") and r.get("auction_date"):
                idx.setdefault((r["isin"], r["auction_date"]), []).append(
                    {**r, "document_id": doc.document_id, "url": doc.url, "sha256": doc.content_sha256})
    return idx


def settlement_for(ext: AuctionExtraction, idx: dict) -> tuple[dict | None, str]:
    if not ext.isin or not ext.auction_date:
        return None, "no ISIN/auction date"
    recs = idx.get((ext.isin, ext.auction_date.isoformat()), [])
    dates = {r["settlement_date"] for r in recs if r.get("settlement_date")}
    if not recs:
        return None, "no announcement with this ISIN and auction date"
    if len(dates) != 1:
        return None, f"{len(dates)} distinct agreed settlement dates on {len(recs)} announcement(s)"
    d = date.fromisoformat(next(iter(dates)))
    if not (ext.auction_date <= d <= ext.auction_date + timedelta(days=10)):
        return None, f"settlement date {d} not within 10 days after the auction"
    rec = next(r for r in recs if r.get("settlement_date") == d.isoformat())
    return rec, "ok"


# --------------------------------------------------------------------------- the checks


def _val(ext: AuctionExtraction, name: str):
    return ((ext.fields or {}).get(name) or {}).get("value")


def check(ext: AuctionExtraction) -> Verdict:
    f = ext.fields or {}
    v = Verdict(ext.extraction_id, ext.isin, ext.country_iso3, ext.auction_date)
    r = v.reasons
    if ext.extractor != EXTRACTOR:
        r.append(f"not a {EXTRACTOR} row")
        return v

    # (a) double OCR, field by field
    for name in STORED:
        fd = f.get(name)
        if fd is None:
            continue
        a, b = (fd.get("ocr") or {}).get("A", {}), (fd.get("ocr") or {}).get("B", {})
        status = fd.get("status")
        if fd.get("value") is None:
            if status == "not_printed" or (name == "coupon_rate" and _val(ext, "instrument_printed") == "BTA"):
                continue
            both_read = a.get("value") is not None and b.get("value") is not None
            if name in OPTIONAL and not both_read and "disagreement" not in (status or "") \
                    and "ambiguous" not in (status or ""):
                continue  # optional field unreadable in a pass: stays NULL (not_available)
            r.append(f"(a) {name}: {status or 'empty'}")
            continue
        if a.get("value") != fd["value"] or b.get("value") != fd["value"]:
            r.append(f"(a) {name}: passes differ (A={a.get('value')!r}, B={b.get('value')!r})")
            continue
        for p, rd in (("A", a), ("B", b)):
            if rd.get("conf") is not None and rd["conf"] < MIN_WORD_CONFIDENCE:
                r.append(f"(a) {name}: low OCR confidence in pass {p} ({rd['conf']:.0f} < {MIN_WORD_CONFIDENCE:.0f})")
    for name in REQUIRED:
        if _val(ext, name) is None and not any(x.startswith(f"(a) {name}:") for x in r):
            r.append(f"(a) {name}: not printed / not found")

    instrument = _val(ext, "instrument_printed")
    offered, submitted, allotted = (_dec(_val(ext, k)) for k in ("amount_offered", "amount_submitted", "amount_allocated"))
    if allotted is not None and allotted > 0:
        for name in REQUIRED_IF_ALLOTTED:
            if (name in NOT_PRINTED_OK and (f.get(name) or {}).get("status") == "not_printed"
                    and _val(ext, "minimum_bid") is not None and _val(ext, "maximum_bid") is not None):
                continue  # format without this line (e.g. Chad): NULL, not_disclosed
            if _val(ext, name) is None and not any(x.startswith(f"(a) {name}:") for x in r):
                r.append(f"(a) {name}: not printed / not found")

    # (b) issue code
    isin = _val(ext, "isin")
    if isin:
        prefix_country = ISIN_PREFIX_COUNTRY.get(isin[:2])
        if prefix_country is None:
            r.append(f"(b) code {isin}: prefix {isin[:2]} is not a CEMAC country code")
        if not luhn_isin_ok(isin):
            r.append(f"(b) code {isin}: ISIN check digit invalid")
        named = (ext.operation or {}).get("countries_in_text", {})
        if prefix_country and not all(prefix_country in (named.get(p) or []) for p in ("A", "B")):
            r.append(f"(b) code {isin}: country {prefix_country} not named in the notice by both passes "
                     f"(A={named.get('A')}, B={named.get('B')})")

    # (c) arithmetic
    if allotted is not None and submitted is not None and allotted > submitted:
        r.append(f"(c) allotted {allotted} > submitted {submitted}")
    lo, hi, lim, avg = (_dec(_val(ext, k)) for k in ("minimum_bid", "maximum_bid", "limit", "weighted_average"))
    kinds = {((f.get(k) or {}).get("note") or "").split("; ")[-1] for k in ("minimum_bid", "maximum_bid", "limit", "weighted_average")
             if (f.get(k) or {}).get("value") is not None}
    is_price = instrument == "OTA"
    expected_kind = "price" if is_price else "rate"
    if allotted is not None and allotted > 0 and None not in (lo, hi):
        if kinds and kinds != {expected_kind}:
            r.append(f"(c) quotation labels {sorted(kinds)} do not match the instrument {instrument} ({expected_kind})")
        if lo > hi and is_price:
            # Congo and Chad name the price bounds after the rate they imply: "prix minimum"
            # is the bid with the lowest rate, i.e. the HIGHEST price (e.g. min 95,00 / max
            # 90,00 / limite 90,00 / moyen 90,59). Values are kept under their printed labels;
            # only the interval used for the checks below is ordered.
            lo, hi = hi, lo
        elif lo > hi:
            r.append(f"(c) minimum {lo} > maximum {hi}")
        if avg is not None and not (lo <= avg <= hi):
            r.append(f"(c) weighted average {avg} not within [min {lo}, max {hi}]")
        if lim is not None and not (lo <= lim <= hi):
            r.append(f"(c) limit {lim} not within [min {lo}, max {hi}]")
        if None not in (lim, avg):
            if is_price and not lim <= avg:
                r.append(f"(c) price: limit {lim} > weighted average {avg} (the limit is the lowest accepted price)")
            if not is_price and not avg <= lim:
                r.append(f"(c) rate: weighted average {avg} > limit {lim} (the limit is the highest accepted rate)")
        for name, x in (("min", lo), ("max", hi), ("limit", lim), ("average", avg)):
            if x is None:
                continue
            plausible = (Decimal(50) <= x <= Decimal(150)) if is_price else (Decimal(0) < x <= Decimal(30))
            if not plausible:
                r.append(f"(c) {name} {x} outside the plausible range ({'50-150 per 100' if is_price else '0-30 %'})")

    # (d) coverage = submitted / offered
    cov_f = f.get("coverage_pct") or {}
    cov = _dec(cov_f.get("value"))
    if cov is not None and offered and submitted is not None:
        computed = submitted / offered * 100
        places = _decimals(cov_f.get("raw")) or 0
        if abs(cov - computed) > Decimal(1).scaleb(-places):
            r.append(f"(d) printed coverage {cov}% != submitted/offered = {computed:.4f}%")
    elif cov is not None and offered == 0:
        r.append("(d) amount offered is 0")
    # (d') when the notice also prints the coverage by the retained bids (served / submitted),
    # it must match too: an independent check of the allotted amount.
    ret_f = f.get("coverage_retained_pct") or {}
    ret = _dec(ret_f.get("value"))
    if ret is not None and submitted and allotted is not None:
        computed = allotted / submitted * 100
        places = _decimals(ret_f.get("raw")) or 0
        if abs(ret - computed) > Decimal(1).scaleb(-places):
            r.append(f"(d) printed coverage by retained bids {ret}% != allotted/submitted = {computed:.4f}%")

    # (e) code line consistency
    if isin and instrument:
        expected = {"BTA": "1", "OTA": "2"}[instrument]
        if len(isin) > 2 and isin[2] != expected:
            r.append(f"(e) {instrument} but code {isin} has instrument digit {isin[2]} (expected {expected})")
    tenor, mat, coupon = _val(ext, "tenor"), _val(ext, "maturity_date"), _dec(_val(ext, "coupon_rate"))
    ad = ext.auction_date
    if tenor and mat and ad and instrument:
        n, unit = tenor.split()
        n = int(n)
        m = date.fromisoformat(mat)
        if instrument == "BTA":
            if unit != "semaines" or n not in (13, 26, 52):
                r.append(f"(e) BTA tenor {tenor!r} not among 13/26/52 weeks")
            elif abs((m - ad).days - 7 * n) > 7:
                r.append(f"(e) BTA {n} weeks but maturity {m} is {(m - ad).days} days after the auction {ad}")
            if coupon is not None:
                r.append("(e) BTA with a coupon")
        else:
            if unit != "ans":
                r.append(f"(e) OTA tenor {tenor!r} not in years")
            else:
                try:
                    latest = ad.replace(year=ad.year + n)
                except ValueError:
                    latest = ad.replace(year=ad.year + n, day=28)
                if not (ad < m <= latest + timedelta(days=31)):
                    r.append(f"(e) OTA {n} years: maturity {m} not within (auction {ad}, auction + {n} years + 31 days]")
            if coupon is None or not (Decimal(0) < coupon <= Decimal(15)):
                r.append(f"(e) OTA coupon {coupon} missing or outside (0, 15] %")
    if ext.country_iso3 is None:
        r.append("(b) no CEMAC country from the code")
    return v


# --------------------------------------------------------------------------- run


def _security_name(ext: AuctionExtraction) -> str:
    instrument, tenor = _val(ext, "instrument_printed"), _val(ext, "tenor")
    mat = _val(ext, "maturity_date")
    coupon = _val(ext, "coupon_rate")
    bits = [f"{instrument} {tenor}"]
    if coupon:
        bits.append(f"{coupon.replace('.', ',')} %")
    bits.append(f"échéance {date.fromisoformat(mat).strftime('%d/%m/%Y')}")
    return f"{ext.isin} " + " ".join(bits)


def _apply_settlement(ext: AuctionExtraction, rec: dict | None, why: str) -> None:
    fields = dict(ext.fields or {})
    status = dict(ext.field_status or {})
    if rec is None:
        fields.pop("settlement_date", None)
        status["settlement_date"] = FieldStatus.NOT_AVAILABLE.value
    else:
        detail = rec["settlement_date_detail"]
        fields["settlement_date"] = {**detail, "value": rec["settlement_date"],
                                     "note": f"from the announcement notice {rec['url']} (SHA-256 {rec['sha256']}), "
                                             "same ISIN and auction date, read identically by both OCR passes"}
        status.pop("settlement_date", None)
    ext.fields = fields
    ext.field_status = status


def _after_approve(session: Session, ext: AuctionExtraction, auction: Auction) -> None:
    from app.ingest.beac import ATTRIBUTION

    instrument = _val(ext, "instrument_printed")
    fs = dict(auction.field_status or {})
    auction.yield_convention = YIELD_CONVENTION_BTA if instrument == "BTA" else YIELD_CONVENTION_OTA
    if instrument == "BTA" and _dec(_val(ext, "amount_allocated")):
        auction.minimum_bid = _dec(_val(ext, "minimum_bid"))
        auction.maximum_bid = _dec(_val(ext, "maximum_bid"))
        fs.pop("minimum_bid", None)
        fs.pop("maximum_bid", None)
    elif instrument == "OTA":
        fs["minimum_bid"] = fs["maximum_bid"] = FieldStatus.NOT_DISCLOSED.value
    if auction.settlement_date is None:
        fs["settlement_date"] = FieldStatus.NOT_AVAILABLE.value  # no matching announcement read twice
    for f in ("number_of_bidders",):
        if getattr(auction, f) is None:
            fs.setdefault(f, (ext.field_status or {}).get("number_of_participants", FieldStatus.NOT_AVAILABLE.value))
    auction.field_status = fs
    notes = [auction.provenance_notes or ""]
    if instrument == "OTA":
        notes.append("OTA: minimum/maximum bids and the limit are published as prices (kept in the staging row).")
    notes.append("Amounts: printed in millions of FCFA, stored x 10^6 exactly. Double OCR (beac_ocr passes A/B) "
                 "and strict checks (app.ingest.beac_check).")
    notes.append(ATTRIBUTION)
    auction.provenance_notes = " ".join(n for n in notes if n)
    sec = auction.security
    if sec.source_document_id == ext.source_document_id and ATTRIBUTION not in (sec.provenance_notes or ""):
        sec.provenance_notes = f"{sec.provenance_notes or ''} {ATTRIBUTION}".strip()
    session.flush()


def run(session: Session, do_approve: bool = False, reviewer: str = REVIEWER) -> dict:
    from app.ingest.beac import get_or_create_source

    source = get_or_create_source(session)
    idx = announcement_index(session, source.source_id)
    rows = list(session.scalars(select(AuctionExtraction).where(
        AuctionExtraction.extractor == EXTRACTOR,
        AuctionExtraction.verification_status == VerificationStatus.UNVERIFIED)
        .order_by(AuctionExtraction.auction_date, AuctionExtraction.extraction_id)))
    out = {"checked": len(rows), "passed": 0, "approved": 0, "held": 0, "held_by_reason": Counter(),
           "settlement_found": 0, "settlement_reasons": Counter(), "rows": []}
    for ext in rows:
        rec, why = settlement_for(ext, idx)
        _apply_settlement(ext, rec, why)
        if rec:
            out["settlement_found"] += 1
        else:
            out["settlement_reasons"][why.split(" on ")[0] if why.startswith(("0 ", "2 ", "3 ")) else why] += 1
        fields = dict(ext.fields)
        if ext.isin and _val(ext, "maturity_date") and _val(ext, "tenor"):
            fields["security_name"] = {"value": _security_name(ext),
                                       "note": "composed from the code line values read identically by both passes"}
        ext.fields = fields
        v = check(ext)
        v.settlement = {"found": bool(rec), "why": why}
        ext.checks = [{"check": "beac_strict", "passed": v.ok, "reasons": v.reasons, "settlement": why}]
        if v.ok:
            out["passed"] += 1
            if do_approve:
                try:
                    with session.begin_nested():
                        auction = approve(session, ext.extraction_id, reviewer)
                        _after_approve(session, ext, auction)
                    out["approved"] += 1
                except ReviewError as e:
                    v.reasons.append(f"approve refused: {e}")
                    ext.checks = [{"check": "beac_strict", "passed": False, "reasons": v.reasons, "settlement": why}]
        if not v.ok:
            out["held"] += 1
            for reason in v.reasons:
                out["held_by_reason"][_group(reason)] += 1
        out["rows"].append({"extraction_id": ext.extraction_id, "isin": ext.isin, "country": ext.country_iso3,
                            "auction_date": ext.auction_date.isoformat() if ext.auction_date else None,
                            "ok": v.ok, "reasons": v.reasons, "settlement": v.settlement})
    session.flush()
    return out


def _group(reason: str) -> str:
    """'(a) amount_offered: passes differ (...)' → '(a) amount_offered: passes differ'."""
    head = reason.split(" (")[0] if reason.startswith("(a)") else reason[:3]
    if reason.startswith("(a)"):
        return head.split(": ")[0] + ": " + head.split(": ", 1)[1].split(" in pass")[0] if ": " in head else head
    tails = {"(b)": ("check digit", "prefix", "not named", "no CEMAC"), "(c)": ("allotted", "weighted average", "limit",
             "price:", "rate:", "outside", "quotation", "minimum"), "(e)": ("instrument digit", "tenor", "weeks but", "years:",
             "coupon", "with a coupon")}
    for t in tails.get(head, ()):
        if t in reason:
            return f"{head} {t}"
    if reason.startswith("approve refused"):
        return "approve refused: " + ("duplicate" if "already exists" in reason else reason[17:60])
    return head


def audit_crops(session: Session, out_dir: Path, extraction_ids: list[int]) -> list[dict]:
    """Render, for each promoted row, the page region from its code line to its last value (pass
    A raster, 300 dpi) to a PNG, with the promoted values to compare against, for a visual audit
    by a person."""
    from app.ingest.beac_ocr import PASSES, crop_png

    dpi = next(p.dpi for p in PASSES if p.name == "A")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = []
    for eid in extraction_ids:
        ext = session.get(AuctionExtraction, eid)
        if ext is None or ext.document is None:
            continue
        boxes: dict[int, list[list[int]]] = {}
        for name in STORED:
            rd = ((ext.fields or {}).get(name) or {}).get("ocr", {}).get("A", {})
            if rd.get("box") and rd.get("page") and name != "auction_date":
                boxes.setdefault(rd["page"], []).append(rd["box"])
        pages = []
        for page, bs in sorted(boxes.items()):
            y0, y1 = min(b[1] for b in bs), max(b[3] for b in bs)
            png = crop_png(Path(ext.document.storage_path), page, (0, y0, int(8.27 * dpi), y1), dpi,
                           out_dir / f"row{eid}-p{page}.png", margin=40)
            pages.append(str(png))
        ad = (ext.fields or {}).get("auction_date", {}).get("ocr", {}).get("A", {})
        if ad.get("box") and ad.get("page"):
            b = ad["box"]
            pages.append(str(crop_png(Path(ext.document.storage_path), ad["page"], (0, b[1], int(8.27 * dpi), b[3]),
                                      dpi, out_dir / f"row{eid}-date.png", margin=30)))
        a = session.get(Auction, ext.promoted_auction_id) if ext.promoted_auction_id else None
        out.append({"extraction_id": eid, "isin": ext.isin, "country": ext.country_iso3,
                    "auction_date": str(ext.auction_date), "url": ext.source_url, "pngs": pages,
                    "values": {k: (ext.fields.get(k) or {}).get("value") for k in STORED},
                    "auction": None if a is None else {
                        "amount_offered": str(a.amount_offered), "amount_submitted": str(a.amount_submitted),
                        "amount_allocated": str(a.amount_allocated), "cutoff_yield": str(a.cutoff_yield),
                        "weighted_average_yield": str(a.weighted_average_yield), "average_price": str(a.average_price),
                        "minimum_bid": str(a.minimum_bid), "maximum_bid": str(a.maximum_bid),
                        "reported_bid_to_cover": str(a.reported_bid_to_cover),
                        "number_of_bidders": a.number_of_bidders, "settlement_date": str(a.settlement_date)}})
    return out


def main() -> None:
    from app.db import SessionLocal

    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--approve", action="store_true", help="promote passing rows (otherwise dry run)")
    p.add_argument("--reviewer", default=REVIEWER)
    p.add_argument("--report", type=Path, help="write the per-row verdicts as JSON")
    p.add_argument("--audit", nargs="+", type=int, metavar="EXTRACTION_ID",
                   help="render the page regions of these staging rows to PNG (no checks run)")
    p.add_argument("--audit-dir", type=Path, default=Path("var/beac_audit"))
    args = p.parse_args()
    if args.audit:
        with SessionLocal() as session:
            print(json.dumps(audit_crops(session, args.audit_dir, args.audit), ensure_ascii=False, indent=1))
        return
    with SessionLocal() as session:
        out = run(session, do_approve=args.approve, reviewer=args.reviewer)
        session.commit()
    rows = out.pop("rows")
    if args.report:
        args.report.write_text(json.dumps({**out, "rows": rows}, default=str, ensure_ascii=False, indent=1))
    for k, v in out.items():
        if isinstance(v, Counter):
            print(f"{k}:")
            for reason, n in v.most_common():
                print(f"  {n:4d}  {reason}")
        else:
            print(f"{k}: {v}")


if __name__ == "__main__":
    main()
