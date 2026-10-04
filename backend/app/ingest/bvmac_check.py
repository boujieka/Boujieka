"""Strict automatic checks of staged BVMAC bond lines, and promotion of the rows that pass.

For every document with UNVERIFIED `bvmac_quote` rows:
  1. re-download the PDF from its official URL and compare the SHA-256 with the stored document
     (the publication must not have changed since extraction);
  2. extract the text twice, independently: `pdftotext -layout` and `pdftotext -raw` (own calls,
     not the extraction run's), and parse each with app.ingest.bvmac_extract;
  3. per bond line, require:
       * both readings complete and equal to the staged value, field by field (17 quote columns +
         mnemo), and the issuer + bond name of the layout reading printed just before the ISIN in
         the raw reading;
       * session date: PDF header (both readings) == listing label == staged; same BOC number;
       * ISIN check digit (ISO 6166, Luhn) and CEMAC prefix; for "ETAT DU <pays>" lines, the
         country named == the ISIN country;
       * price sanity: previous, opening and closing prices in (0, 200] % of nominal;
         previous price FCFA == previous % x nominal / 100 and next reference price FCFA ==
         closing % x nominal / 100 (to the printed cent);
       * order book: whole numbers, traded <= demanded, traded <= offered, 1 <= trades <= traded,
         nothing traded <=> value 0 and 0 trades; status "NC" <=> nothing traded;
       * when traded: value traded == traded x (closing % x nominal / 100 + accrued coupon) within
         rounding (traded x 0.005 + 1 FCFA); printed variation == closing / previous - 1 (to
         0.01 %); the section "Total" line and the front-page "OBLIGATIONS" summary line print
         the sums of the section's / market's traded volumes, values and trades;
       * characteristics table read identically by both readings: coupon ("Taux facial") equal
         to the coupon in the bond name, periodicity AN / SEM / TRIM;
       * no other document for the same session prints different trade figures for the bond;
         an existing promoted security has the same coupon; an existing observation for the
         day has the same price and value.
A row passes only if every check passes; it is then marked VERIFIED and promoted:
  * `security` (once per ISIN): name, issuer, country, instrument "regional_bond" (bond listed
    on the regional exchange), currency XAF, coupon, periodicity, amortisation as printed;
    maturity / issue date / face value left NULL (not printed as such in the BOC);
  * `market_observation` kind SECONDARY_MARKET — only if the bond traded that day:
    price = printed closing price (% of nominal), volume = printed value traded (FCFA, includes
    accrued coupon), yield NULL (no yield is printed in the quote table).
Anything else stays UNVERIFIED with `hold_reasons`, for a person to decide.

    python -m app.ingest.bvmac_check                   # check + promote
    python -m app.ingest.bvmac_check --dry-run         # report only, change nothing
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingest.bvmac_extract import (
    EXTRACTOR,
    ISIN_COUNTRY,
    OPTIONAL_QUOTE_FIELDS,
    QUOTE_FIELDS,
    TIE_BREAK_NOTE,
    ParsedBoc,
    coupon_in_name,
    isin_valid,
    nospace,
    parse,
)
from app.models import BvmacQuote, Country, Issuer, MarketObservation, Security, SourceDocument
from app.models.enums import (
    CouponFrequency,
    DataNature,
    FieldStatus,
    InstrumentType,
    IssuerType,
    ObservationKind,
    VerificationStatus,
)

REVIEWER = "bvmac_check (strict automatic checks, no human review)"
PERIODICITY = {"AN": CouponFrequency.ANNUAL, "SEM": CouponFrequency.SEMI_ANNUAL, "TRIM": CouponFrequency.QUARTERLY}
SECTION_ISSUER_TYPE = {"sovereign": IssuerType.SOVEREIGN, "regional": IssuerType.SUPRANATIONAL,
                       "private": IssuerType.CORPORATE}
CENT = Decimal("0.01")
ND = FieldStatus.NOT_DISCLOSED.value
QUOTE_NAMES = ["mnemo"] + [n for n, _ in QUOTE_FIELDS]


def pdf_text(content: bytes, mode: str) -> str:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(content)
        f.flush()
        return subprocess.run(["pdftotext", f"-{mode}", "-enc", "UTF-8", f.name, "-"],
                              capture_output=True, text=True, check=True, timeout=120).stdout


def digits(d: Decimal) -> str:
    return re.sub(r"\D", "", format(d.normalize(), "f")) if d != 0 else "0"


def near(a: Decimal, b: Decimal, tol: Decimal) -> bool:
    return abs(a - b) <= tol


# --------------------------------------------------------------------------- checks


class Checks:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, name: str, ok: bool, detail: str = "") -> bool:
        self.items.append({"check": name, "ok": bool(ok), "detail": detail})
        return ok

    @property
    def problems(self) -> list[str]:
        return [f"{c['check']}: {c['detail']}" for c in self.items if not c["ok"]]


def _doc_sums(parsed: ParsedBoc) -> tuple[dict[str, tuple], tuple | None]:
    """Per-section and market-wide (volume traded, value traded, trades), or None if any line of
    that scope could not be read completely."""
    per: dict[str, list] = {}
    bad: set[str] = set()
    for q in parsed.quotes.values():
        s = q.section or "?"
        vals = [q.v("volume_traded"), q.v("value_traded"), q.v("trades")]
        if q.errors or any(v is None for v in vals):
            bad.add(s)
            continue
        acc = per.setdefault(s, [Decimal(0)] * 3)
        for i in range(3):
            acc[i] += vals[i]
    sections = {s: tuple(v) for s, v in per.items() if s not in bad}
    market = None
    if not bad:
        market = tuple(sum((v[i] for v in per.values()), Decimal(0)) for i in range(3))
    return sections, market


def check_row(row: BvmacQuote, L: ParsedBoc, R: ParsedBoc) -> Checks:
    c = Checks()
    isin = row.isin
    lq, rq = L.quotes.get(isin), R.quotes.get(isin)
    c.add("parse_status", row.parse_status == "complete", f"staged row is {row.parse_status}: {row.errors}")
    c.add("layout", L.layout == EXTRACTOR and R.layout == EXTRACTOR, f"layout={L.layout}, raw={R.layout}")
    if not c.add("present_both", lq is not None and rq is not None, "ISIN not found by both readings"):
        return c
    c.add("layout_reading_clean", not lq.errors, "; ".join(lq.errors))
    tie = [n for n in lq.notes + rq.notes if n == TIE_BREAK_NOTE]
    if tie:  # informational; the totals checks below are then what independently confirms the reading
        c.add("tie_break_by_value_identity", True, f"{len(tie)} reading(s) chose among readings by the value identity")
    c.add("raw_reading_clean", not rq.errors, "; ".join(rq.errors))
    staged = row.fields or {}
    for name in QUOTE_NAMES:
        lv, rv = lq.fields.get(name), rq.fields.get(name)
        sv = (staged.get(name) or {}).get("value")
        if name in OPTIONAL_QUOTE_FIELDS:  # may be unread (ambiguous); never promoted
            ok = (lv is None and sv is None) or (lv is not None and sv is not None and str(sv) == lv.as_dict()["value"]
                                                 and (rv is None or rv.value == lv.value))
        else:
            ok = lv is not None and rv is not None and lv.value == rv.value and sv is not None and \
                str(sv) == lv.as_dict()["value"]
        if not ok:
            c.add(f"agree:{name}", False, f"staged={sv!r} layout={lv and lv.raw!r} raw={rv and rv.raw!r}")
    c.add("agree:all_columns", not [i for i in c.items if i["check"].startswith("agree:") and not i["ok"]],
          "see agree:* above")
    who = nospace((lq.issuer or "") + (lq.name or ""))
    c.add("issuer_name_layout", bool(lq.issuer and lq.name) and who == nospace((row.issuer_name or "") + (row.security_name or "")),
          f"layout {lq.issuer!r} / {lq.name!r} vs staged {row.issuer_name!r} / {row.security_name!r}")
    c.add("issuer_name_raw", bool(who) and (rq.prefix_compact or "").endswith(who),
          f"raw text before the ISIN does not end with {who!r}")
    # Dates and document identity.
    listing = (staged.get("listing_label") or {}).get("value")
    c.add("session_date", L.session_date is not None and L.session_date == R.session_date
          and row.session_date == L.session_date and listing == L.session_date.isoformat(),
          f"layout {L.session_date} raw {R.session_date} staged {row.session_date} listing {listing}")
    c.add("boc_number", L.boc_number is not None and L.boc_number == R.boc_number == row.boc_number,
          f"{L.boc_number} / {R.boc_number} / {row.boc_number}")
    # Identity.
    c.add("isin_check_digit", isin_valid(isin), isin)
    iso3 = ISIN_COUNTRY.get(isin[:2])
    c.add("isin_cemac_prefix", iso3 is not None, isin[:2])
    c.add("section", lq.section in SECTION_ISSUER_TYPE, str(lq.section))
    if lq.section == "sovereign":
        c.add("state_matches_isin", lq.country_iso3 == iso3, f"'{lq.issuer}' -> {lq.country_iso3}, ISIN -> {iso3}")
    if any(not i["ok"] for i in c.items):
        return c
    v = {n: (lq.fields[n].value if n in lq.fields else None) for n in QUOTE_NAMES}
    prev, opn, close = v["previous_price_pct"], v["open_price_pct"], v["close_price_pct"]
    nominal, cc = v["nominal"], v["accrued_coupon"]
    c.add("prices_in_range", all(Decimal(0) < p <= Decimal(200) for p in (prev, opn, close)),
          f"previous {prev}, open {opn}, close {close}")
    c.add("previous_price_fcfa", near(v["previous_price_fcfa"], prev * nominal / 100, CENT),
          f"{v['previous_price_fcfa']} vs {prev} % x {nominal}")
    c.add("next_reference_price_fcfa", near(v["next_reference_price_fcfa"], close * nominal / 100, CENT),
          f"{v['next_reference_price_fcfa']} vs {close} % x {nominal}")
    vd, vo, vt, val, n = (v["volume_demanded"], v["volume_offered"], v["volume_traded"], v["value_traded"],
                          v["trades"])
    whole = all(x == x.to_integral_value() and x >= 0 for x in (vd, vo, vt, n) if x is not None)
    if vt == 0:
        c.add("order_book", whole and val == 0 and n == 0, f"traded 0, value {val}, trades {n}")
        c.add("status_nc", v["status"] == "NC", f"nothing traded but status {v['status']!r}")
        return c
    c.add("order_book", whole and (vd is None or vt <= vd) and (vo is None or vt <= vo) and 1 <= n <= vt,
          f"demanded {vd}, offered {vo}, traded {vt}, trades {n}")
    c.add("status_traded", v["status"] != "NC", f"traded {vt} but status NC")
    expected = vt * (close * nominal / 100 + cc)
    c.add("value_traded", near(val, expected, vt * Decimal("0.005") + 1),
          f"printed {val} vs {vt} x ({close} % x {nominal} + {cc}) = {expected:.2f}")
    c.add("variation", near(v["variation_pct"], (close / prev - 1) * 100, Decimal("0.006")),
          f"printed {v['variation_pct']} % vs close/previous = {(close / prev - 1) * 100:.4f} %")
    # Totals printed by the exchange.
    for P, label in ((L, "layout"), (R, "raw")):
        sections, market = _doc_sums(P)
        if P is L:
            tot = L.totals.get(lq.section)
            sums = sections.get(lq.section)
            want = "".join(digits(x) for x in sums) if sums else None
            c.add("section_total", tot is not None and want is not None and tot.digits == want,
                  f"'Total' digits {tot and tot.digits!r} vs sums {want!r}")
        want = "".join(digits(x) for x in market) if market else None
        c.add(f"market_summary_{label}", P.summary_digits is not None and want is not None
              and P.summary_digits.startswith(want), f"summary digits {P.summary_digits!r} vs sums {want!r}")
    return c


def check_characteristics(row: BvmacQuote, L: ParsedBoc, R: ParsedBoc, c: Checks) -> dict:
    """Characteristics both readings agree on; returns the values to promote."""
    lc, rc = L.characteristics.get(row.isin), R.characteristics.get(row.isin)
    if not c.add("characteristics_present", lc is not None and rc is not None, "ISIN missing from the characteristics table"):
        return {}
    twice = [e for e in lc.errors + rc.errors if "printed twice" in e]
    c.add("characteristics_unique", not twice, "ISIN printed on two lines of the characteristics table")
    mn = {lc.v("mnemo"), rc.v("mnemo"), row.mnemo}
    c.add("characteristics_mnemo", len(mn) == 1 and None not in mn, f"mnemo quote {row.mnemo!r} vs characteristics {sorted(map(str, mn))}")
    out = {}
    for name in ("coupon_rate", "periodicity", "amortization"):
        lv, rv = lc.fields.get(name), rc.fields.get(name)
        if c.add(f"char_agree:{name}", lv is not None and rv is not None and lv.value == rv.value,
                 f"layout {lv and lv.raw!r} raw {rv and rv.raw!r}"):
            out[name] = lv
    if "coupon_rate" in out:
        in_name = coupon_in_name(row.security_name)
        c.add("coupon_matches_name", in_name is not None and in_name == out["coupon_rate"].value,
              f"Taux facial {out['coupon_rate'].raw!r} vs name {row.security_name!r}")
        c.add("coupon_in_range", Decimal(0) < out["coupon_rate"].value <= Decimal(25), out["coupon_rate"].raw)
    if "periodicity" in out:
        c.add("periodicity_known", out["periodicity"].value in PERIODICITY, out["periodicity"].raw)
    return out


# --------------------------------------------------------------------------- promotion


def _issuer(session: Session, row: BvmacQuote, country: Country) -> Issuer:
    if row.section == "sovereign":
        name = f"Government of {country.name}"
        issuer = session.scalar(select(Issuer).where(Issuer.name == name))
        if issuer is None:
            raise RuntimeError(f"issuer {name!r} missing: run `python -m app.seed.load` first")
        return issuer
    name = row.issuer_name
    issuer = session.scalar(select(Issuer).where(Issuer.name == name, Issuer.country_id == country.country_id))
    if issuer is None:
        issuer = Issuer(name=name, country_id=country.country_id, issuer_type=SECTION_ISSUER_TYPE[row.section],
                        is_synthetic=False)
        session.add(issuer)
        session.flush()
    return issuer


def _security(session: Session, row: BvmacQuote, doc: SourceDocument, char: dict, c: Checks) -> Security | None:
    sec = session.scalar(select(Security).where(Security.isin == row.isin))
    coupon = char["coupon_rate"].value
    if sec is not None:
        c.add("security_consistent", sec.coupon_rate is None or Decimal(sec.coupon_rate) == coupon,
              f"existing security coupon {sec.coupon_rate} vs printed {coupon}")
        return sec
    country = session.scalar(select(Country).where(Country.iso3 == ISIN_COUNTRY[row.isin[:2]]))
    if not c.add("country_known", country is not None and country.currency == "XAF",
                 f"{ISIN_COUNTRY[row.isin[:2]]} missing or not an XAF country"):
        return None
    issuer = _issuer(session, row, country)
    f = row.fields
    sec = Security(
        issuer_id=issuer.issuer_id, country_id=country.country_id, instrument_type=InstrumentType.REGIONAL_BOND,
        security_name=row.security_name, isin=row.isin, local_code=row.mnemo, currency="XAF",
        coupon_rate=coupon, coupon_frequency=PERIODICITY[char["periodicity"].value],
        amortization=char["amortization"].value if "amortization" in char else None,
        listing_status="Listed on the BVMAC (Bulletin officiel de la cote)",
        source_id=doc.source_id, source_document_id=doc.document_id, source_url=doc.url,
        publication_date=row.session_date, extracted_at=row.extracted_at,
        verification_status=VerificationStatus.VERIFIED, data_nature=DataNature.FACT,
        confidence_score=Decimal("1"), is_synthetic=False,
        field_status={"maturity_date": ND, "issue_date": ND, "face_value": ND, "tenor_days": ND,
                      "minimum_denomination": ND,
                      **({} if "amortization" in char else {"amortization": ND})},
        provenance_notes=(
            f"BVMAC BOC n° {row.boc_number} du {row.session_date}: quote line "
            f"{f.get('mnemo', {}).get('locator')} and characteristics table (Taux facial "
            f"{char['coupon_rate'].raw!r} at {char['coupon_rate'].locator}, Périod "
            f"{char['periodicity'].raw!r}). Issuer as printed: {row.issuer_name!r} (section "
            f"{row.section}). Country = ISIN prefix {row.isin[:2]}. Maturity date not printed in the "
            f"BOC (only the years in the name and a maturity in years), so left empty. Verified by "
            f"{REVIEWER}. Source: BVMAC, published with its written authorisation (free, no resale)."),
    )
    session.add(sec)
    session.flush()
    return sec


def _observation(session: Session, row: BvmacQuote, sec: Security, doc: SourceDocument,
                 c: Checks) -> MarketObservation | None:
    f = row.fields
    price, value = Decimal(f["close_price_pct"]["value"]), Decimal(f["value_traded"]["value"])
    # Another BOC for the same session (e.g. a corrected edition) must print the same trade.
    others = session.scalars(select(BvmacQuote).where(
        BvmacQuote.isin == row.isin, BvmacQuote.session_date == row.session_date,
        BvmacQuote.quote_id != row.quote_id)).all()
    for o in others:
        of = o.fields or {}
        same = all((of.get(k) or {}).get("value") == (f.get(k) or {}).get("value")
                   for k in ("volume_traded", "value_traded", "close_price_pct", "trades"))
        if not c.add("same_session_documents_agree", same,
                     f"document {o.source_document_id} prints different figures for {row.isin} on {row.session_date}"):
            return None
    obs = session.scalar(select(MarketObservation).where(
        MarketObservation.security_id == sec.security_id, MarketObservation.observation_date == row.session_date,
        MarketObservation.kind == ObservationKind.SECONDARY_MARKET, MarketObservation.source_id == doc.source_id))
    if obs is not None:
        c.add("existing_observation_agrees", Decimal(obs.price) == price and Decimal(obs.volume) == value,
              f"existing {obs.price} / {obs.volume} vs {price} / {value}")
        return obs
    obs = MarketObservation(
        security_id=sec.security_id, observation_date=row.session_date, kind=ObservationKind.SECONDARY_MARKET,
        yield_pct=None, price=price, spread_bps=None, volume=value,
        source_id=doc.source_id, source_document_id=doc.document_id, source_url=doc.url,
        publication_date=row.session_date, extracted_at=row.extracted_at,
        verification_status=VerificationStatus.VERIFIED, data_nature=DataNature.FACT,
        confidence_score=Decimal("1"), is_synthetic=False,
        field_status={"yield": ND, "spread_bps": ND},
        provenance_notes=(
            f"BVMAC BOC n° {row.boc_number}, séance du {row.session_date}, {f['close_price_pct']['locator']}: "
            f"price = closing price 'Clôt.' {f['close_price_pct']['raw']!r} (% of nominal); volume = "
            f"'Valeur transigée' {f['value_traded']['raw']!r} FCFA (includes accrued coupon); "
            f"{f['volume_traded']['raw']} bonds in {f['trades']['raw']} trade(s), status "
            f"{f['status']['raw']!r}, nominal {f['nominal']['raw']!r}, accrued coupon "
            f"{f['accrued_coupon']['raw']!r}. No yield printed. Printed line: {row.raw_line.strip()!r}. "
            f"Verified by {REVIEWER}. Source: BVMAC (written authorisation, free publication, no resale)."),
    )
    session.add(obs)
    session.flush()
    return obs


# --------------------------------------------------------------------------- orchestration


def run(session: Session, dry_run: bool = False, fetch=None, pause: float | None = None,
        document_ids: set[int] | None = None, log: Callable[[str], None] = lambda _: None,
        commit: bool = False) -> dict:
    """Check every UNVERIFIED row (grouped by document) and promote those that pass. With
    commit=True (the CLI) each document's decisions are committed as soon as they are made."""
    from app.ingest import bvmac

    fetch = fetch or bvmac.http_get
    pause = bvmac.REQUEST_PAUSE_SECONDS if pause is None else pause
    report = {"documents": 0, "rows_checked": 0, "verified": 0, "held": [], "securities_created": 0,
              "observations_created": 0, "observations_linked": 0, "document_errors": []}
    rows = list(session.scalars(select(BvmacQuote).where(
        BvmacQuote.verification_status == VerificationStatus.UNVERIFIED).order_by(
        BvmacQuote.session_date, BvmacQuote.source_document_id, BvmacQuote.isin)))
    by_doc: dict[int, list[BvmacQuote]] = {}
    for r in rows:
        if document_ids is None or r.source_document_id in document_ids:
            by_doc.setdefault(r.source_document_id, []).append(r)
    now = datetime.now(timezone.utc)
    for doc_id, doc_rows in by_doc.items():
        doc = session.get(SourceDocument, doc_id)
        report["documents"] += 1
        err = None
        L = R = None
        try:
            if report["documents"] > 1:
                time.sleep(pause)
            got = fetch(doc.url)
            if got.status != 200 or not got.content:
                err = f"re-download failed: {got.error or f'HTTP {got.status}'}"
            elif hashlib.sha256(got.content).hexdigest() != doc.content_sha256:
                err = "live document changed since extraction (SHA-256 differs)"
            else:
                L, R = parse(pdf_text(got.content, "layout"), "layout"), parse(pdf_text(got.content, "raw"), "raw")
        except Exception as e:  # network or PDF error: hold, never promote on doubt
            err = f"{type(e).__name__}: {e}"[:300]
        if err:
            report["document_errors"].append({"document_id": doc_id, "url": doc.url, "error": err})
        n_new_sec = n_new_obs = 0
        for row in doc_rows:
            report["rows_checked"] += 1
            if err:
                c = Checks()
                c.add("document", False, err)
                char = {}
            else:
                c = check_row(row, L, R)
                char = check_characteristics(row, L, R, c)
            sec = obs = None
            if not c.problems and not dry_run:
                try:
                    with session.begin_nested():
                        existed = session.scalar(select(Security.security_id).where(Security.isin == row.isin))
                        sec = _security(session, row, doc, char, c)
                        if sec is not None and not c.problems and row.traded:
                            had = session.scalar(select(MarketObservation.observation_id).where(
                                MarketObservation.security_id == sec.security_id,
                                MarketObservation.observation_date == row.session_date,
                                MarketObservation.kind == ObservationKind.SECONDARY_MARKET,
                                MarketObservation.source_id == doc.source_id))
                            obs = _observation(session, row, sec, doc, c)
                            if obs is not None and not c.problems:
                                n_new_obs += int(had is None)
                                report["observations_linked"] += int(had is not None)
                        if c.problems:
                            raise _Rollback()
                        n_new_sec += int(existed is None)
                except _Rollback:
                    sec = obs = None
            row.checks = c.items
            row.checked_at = now
            if c.problems:
                row.hold_reasons = c.problems
                report["held"].append({"quote_id": row.quote_id, "isin": row.isin, "date": str(row.session_date),
                                       "traded": row.traded, "problems": c.problems})
                continue
            if dry_run:
                report["verified"] += 1
                continue
            row.hold_reasons = []
            row.verification_status = VerificationStatus.VERIFIED
            row.reviewed_by = REVIEWER
            row.reviewed_at = now
            row.promoted_security_id = sec.security_id if sec else None
            row.promoted_observation_id = obs.observation_id if obs else None
            row.provenance_notes = (row.provenance_notes or "").replace(
                "UNVERIFIED until app.ingest.bvmac_check passes.", f"VERIFIED by {REVIEWER}.")
            report["verified"] += 1
        report["securities_created"] += n_new_sec
        report["observations_created"] += n_new_obs
        session.flush()
        if commit and not dry_run:
            session.commit()
        log(f"{doc.title}: {len(doc_rows)} row(s) checked{' — ' + err if err else ''}")
    return report


class _Rollback(Exception):
    pass


def summary(report: dict) -> str:
    traded_held = sum(1 for h in report["held"] if h["traded"])
    return (f"documents {report['documents']} · rows checked {report['rows_checked']} · verified "
            f"{report['verified']} · held {len(report['held'])} (of which traded {traded_held}) · securities "
            f"created {report['securities_created']} · observations created {report['observations_created']} "
            f"(linked {report['observations_linked']}) · document errors {len(report['document_errors'])}")


def main(argv: list[str] | None = None) -> int:
    from app.db import SessionLocal

    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--dry-run", action="store_true", help="report only; change nothing")
    p.add_argument("--report", type=Path, help="write the full report as JSON")
    args = p.parse_args(argv)
    with SessionLocal() as session:
        report = run(session, dry_run=args.dry_run, log=print, commit=not args.dry_run)
        if args.dry_run:
            session.rollback()
        else:
            session.commit()
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=1, default=str))
    print(summary(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
