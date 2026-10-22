"""World Bank Documents & Reports connector: supervision (ISR) and completion (ICR / ICR Review) reports.

Source: World Bank Documents & Reports API (public, no key)
  https://search.worldbank.org/api/v2/wds?format=json&proid=P157734
Each document has a PDF and a plain-text rendition (`txturl`); AP²I parses the text rendition, and reads the
results table from the PDF itself when the text rendition does not contain its values (post-2024 ISRs).
Terms: World Bank Terms of Use for Datasets / documents (public disclosure); attribution kept.

What is extracted (officially reported, as written in the report):
  * ISR: report date, sequence number, ratings (Progress towards PDO, Overall Implementation Progress,
    Overall Risk — previous and current), "Implementation Status and Key Decisions" narrative, original and
    revised closing dates, per-loan disbursement table (original, revised, cancelled, disbursed, undisbursed,
    % disbursed), results indicators with baseline / previous / current / end-target values and dates.
  * ICR: ratings by the ICR (outcome, risk to development outcome, Bank and borrower performance).
  * ICR Review (IEG): the same ratings as validated by IEG.
What is NOT inferred:
  * Overall physical progress. Percentages mentioned in the narrative (e.g. "92% completion") are stored as
    CANDIDATE observations (verification_status=needs_review); a Data Reviewer must confirm them before they
    become the project's physical progress.
  * Results tables of the post-2024 ISR layout: their values are not in the text rendition (only the indicator
    names are). They are read from the PDF by word position (`parse_isr_pdf_results`); a row whose words do not
    fit the table's columns is dropped, never guessed. "Month/Year" dates (e.g. "Jun/2020") have no day: the date
    is left empty rather than given an invented day.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal

from app.connectors.base import Connector, ConnectorError, RawRecord, SyncParams, parse_decimal

ISR = "Implementation Status and Results Report"
ICR = "Implementation Completion and Results Report"
ICRR = "Implementation Completion Report Review"
PARSED_TYPES = {ISR, ICR, ICRR}

RATING_WORDS = r"(?:Highly Satisfactory|Moderately Satisfactory|Satisfactory|Moderately Unsatisfactory|Highly Unsatisfactory|" \
               r"Unsatisfactory|Not Rated|Negligible to Low|Negligible|Low|Moderate|Substantial|High|Modest|--)"
UNSATISFACTORY = {"Moderately Unsatisfactory", "Unsatisfactory", "Highly Unsatisfactory"}
DATE_RX = r"\d{2}-[A-Z][a-z]{2}-\d{4}"


def wb_date(s: str | None) -> date | None:
    if not s:
        return None
    s = s.strip().lstrip(":")
    for fmt in ("%d-%b-%Y", "%b %d, %Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _cols(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"\s{2,}", line.strip()) if c.strip()]


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\u0080-\u009f\u00a0\u2007\u202f]", " ", text)  # C1 controls and non-breaking spaces  # C1 control characters left by some PDF-to-text conversions
    return re.sub(r"[\ue000-\uf8ff]", " ", text)  # private-use glyphs (checkbox/bullet fonts)


def _strip_page_furniture(text: str) -> str:
    text = _normalize(text)
    lines = []
    for ln in text.splitlines():
        if re.search(r"Public Disclosure Copy|Page \d+ of \d+|^\s*The World Bank\s+Implementation Status", ln):
            continue
        lines.append(ln)
    return "\n".join(lines)


@dataclass
class ParsedReport:
    doc_type: str
    report_date: date | None = None
    sequence: str | None = None
    ratings: dict[str, dict[str, str]] = field(default_factory=dict)  # name -> {previous, current} or {icr, ieg}
    narrative: str | None = None
    original_closing: date | None = None
    revised_closing: date | None = None
    loans: list[dict] = field(default_factory=list)
    indicators: list[dict] = field(default_factory=list)
    progress_candidates: list[dict] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def parse_isr(text: str, report_date: date | None = None) -> ParsedReport:
    r = ParsedReport(ISR, report_date=report_date)
    t = _strip_page_furniture(text)
    m = re.search(r"Seq No:\s*(\d+)", t)
    r.sequence = m.group(1) if m else None

    for name, key in (("Progress towards achievement of PDO", "pdo"), ("Overall Implementation Progress (IP)", "ip"),
                      ("Overall Risk Rating", "risk")):
        m = re.search(re.escape(name) + r"[ \t]+(.+)", t)
        if m:
            vals = [v for v in _cols(m.group(1)) if re.fullmatch(RATING_WORDS, v)]
            if len(vals) >= 2:
                r.ratings[key] = {"previous": vals[-2], "current": vals[-1]}
            elif len(vals) == 1:
                r.ratings[key] = {"previous": None, "current": vals[0]}

    m = re.search(r"Implementation Status and Key Decisions\s*\n(.+?)(?:\n\s*(?:Key Government Actions|Risks\b|3\.2|4\.\s|"
                  r"KEY ISSUES|Systematic Operations|Guarantee Conditions)|\Z)", t, re.S)
    if m:
        r.narrative = _clean(m.group(1))[:4000] or None

    m = re.search(r"Original Closing Date:\s*(" + DATE_RX + ")", t)
    if m:
        r.original_closing = wb_date(m.group(1))
    m = re.search(r"Revised Closing Date:\s*(" + DATE_RX + ")", t)
    if m:
        r.revised_closing = wb_date(m.group(1))

    # Per-loan key dates rows: <loan> <status> approval signing effectiveness orig.closing rev.closing
    for ln in t.splitlines():
        dates = re.findall(DATE_RX, ln)
        lm = re.match(r"\s*(?:P\d{6}\s+)?((?:IDA|IBRD|TF|IFC)[-\w]+)\s+", ln)
        if lm and len(dates) == 5:
            if r.original_closing is None:
                r.original_closing = wb_date(dates[3])
            if r.revised_closing is None:
                r.revised_closing = wb_date(dates[4])

    # Disbursement table rows
    loan_rx = re.compile(r"^\s*(?:P\d{6}\s+)?((?:IDA|IBRD|TF)[-\w]*\d[-\w]*)\s+(Effective|Closed|Not Effective|Signed|Approved|"
                         r"Disbursing|Fully Disbursed|Disbursing&Repaying|Repaying|Terminated)\s+(?:([A-Z]{3})\s+)?"
                         r"([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)\s+([\d.]+)\s?%")
    for ln in t.splitlines():
        m = loan_rx.match(ln)
        if m:
            r.loans.append({
                "loan": m.group(1), "status": m.group(2), "currency": m.group(3),
                "original": parse_decimal(m.group(4)), "revised": parse_decimal(m.group(5)),
                "cancelled": parse_decimal(m.group(6)), "disbursed": parse_decimal(m.group(7)),
                "undisbursed": parse_decimal(m.group(8)), "pct_disbursed": parse_decimal(m.group(9)),
                "unit": "millions" + (f" {m.group(3)}" if m.group(3) else " (currency not stated in the text rendition)"),
            })

    # Results indicators (pre-2024 layouts): a header "Baseline  Actual (Previous)  Actual (Current)  End Target",
    # the indicator name in the lines just above it, then a "Value" row and a "Date" row.
    lines = t.splitlines()
    header = re.compile(r"Baseline\s+Actual \(Previous\)\s+Actual \(Current\)\s+End Target")
    stop = re.compile(r"^\s*$|^(PHIND|IN\d{5}|Comments|Date\b|Value\b|.*Indicators by|.*Indicators$|\d{1,2}/\d{1,2}/\d{4}\s)")
    for h, ln in enumerate(lines):
        if not header.search(ln):
            continue
        name_lines: list[str] = []
        k = h - 1
        while k >= 0 and not lines[k].strip():
            k -= 1
        while k >= 0 and not stop.match(lines[k].strip()) and len(name_lines) < 5:
            name_lines.insert(0, lines[k].strip().lstrip("►").strip())
            k -= 1
        name = _clean(" ".join(name_lines))
        values = dates = None
        for n in range(h + 1, min(len(lines), h + 25)):
            st = lines[n].strip()
            if header.search(st):
                break
            if st.startswith("Value") and values is None:
                values = _cols(st)[1:]
            elif st.startswith("Date") and values is not None:
                dates = [wb_date(d) for d in re.findall(DATE_RX, st)]
                break
        if not name or not values or len(values) != 4:
            continue
        um = re.search(r"\(([^()]*),\s*(Corporate|Custom|Core|Supplemental|Number|Percentage|Text|Yes/No)\)\s*$", name)
        unit = um.group(1) if um else None
        clean_name = name[: um.start()].strip() if um else name
        ind = {"name": clean_name, "unit": unit, "baseline": values[0], "previous": values[1], "current": values[2], "target": values[3]}
        if dates and len(dates) == 4:
            ind.update({"baseline_date": dates[0], "previous_date": dates[1], "current_date": dates[2], "target_date": dates[3]})
        r.indicators.append(ind)
    if not r.indicators:
        r.indicators = _columnar_indicators(lines)
    if not r.indicators and re.search(r"Indicator Name", t):
        r.notes.append("Results table present but its values are not in the text rendition (post-2024 ISR layout); not extracted.")

    if r.narrative:
        for mm in re.finditer(r"([^.]*?\b(\d{1,3}(?:[.,]\d+)?)\s?%\s+(?:completion|completed|physical|progress|execution|avancement)[^.]*\.)",
                              r.narrative, re.I):
            pct = parse_decimal(mm.group(2).replace(",", "."))
            if pct is not None and pct <= 100:
                r.progress_candidates.append({"value": pct, "sentence": _clean(mm.group(1))[:500]})
    return r


def _cells(ln: str, start: int, starts: list[int]) -> list[str | None] | None:
    """Values of a Value/Date row of the pre-2015 layout, one per column (baseline, current, end target).

    The text rendition does not keep a fixed column grid: the same table has rows shifted by up to ~15 characters.
    Header positions are used only when every token starts at a header column (±3); otherwise a row with exactly
    three tokens is read in order; any other row is ambiguous and returns None (dropped, never guessed)."""
    toks = [(m.start() + start, m.group()) for m in re.finditer(r"\S+(?: \S+)*", ln[start:])]
    if not toks:
        return [None, None, None]
    out: list[str | None] = [None, None, None]
    if all(any(abs(pos - c) <= 3 for c in starts) for pos, _ in toks):
        for pos, tok in toks:
            k = min(range(3), key=lambda i: abs(starts[i] - pos))
            if out[k] is not None:
                return None
            out[k] = tok
        return out
    if len(toks) == 3:
        return [t for _, t in toks]
    return None


def _columnar_indicators(lines: list[str]) -> list[dict]:
    """Pre-2015 ISR layout: 'Indicator Name  Core Unit of Measure  Baseline  Current  End Target', then per indicator
    a 'Value' row and a 'Date' row. Name and unit are read from the text before 'Value' (split on wide gaps)."""
    out: list[dict] = []
    hdr = re.compile(r"Indicator Name\s+(?:Core\s+)?Unit of Measure\s+Baseline\s+Current\s+End Target")
    end = re.compile(r"Data on Financial Performance|Disbursements \(by loan\)")
    furniture = re.compile(r"^\s*(Comments|Public Disclosure|Intermediate Results|Project Development|The World Bank|Report No)")
    i = 0
    while i < len(lines):
        h = lines[i]
        if not hdr.search(h):
            i += 1
            continue
        starts = [h.index("Baseline"), h.index("Current"), h.index("End Target")]
        cur: dict | None = None
        i += 1
        while i < len(lines) and not hdr.search(lines[i]) and not end.search(lines[i]):
            ln = lines[i]
            vm = re.search(r"\s{2,}Value\s{2,}|\s{2,}Value$", ln)
            dm = re.search(r"\s{2,}Date\s{2,}|\s{2,}Date$", ln)
            if vm and cur is not None and cur.get("_pending"):
                cur = None  # previous indicator had no Date row
            if vm:
                head = [x for x in re.split(r"\s{2,}", ln[: vm.start()].strip()) if x]
                unit = head[-1] if len(head) >= 2 else None
                name = " ".join(head[:-1] if len(head) >= 2 else head)
                vals = _cells(ln, vm.end(), starts)
                cur = {"name": name, "unit": unit, "previous": None, "_ok": vals is not None, "_pending": True}
                cur.update(dict(zip(("baseline", "current", "target"), vals or [None, None, None])))
                out.append(cur)
            elif dm and cur is not None and cur.get("_pending"):
                ds = _cells(ln, dm.end(), starts)
                if ds is None:
                    cur["_ok"] = False
                else:
                    for k, v in zip(("baseline_date", "current_date", "target_date"), ds):
                        cur[k] = wb_date(v)
                cont = ln[: dm.start()].strip()
                if cont:
                    cur["name"] = _clean(cur["name"] + " " + cont)
                cur["_pending"] = False
            elif cur is not None and not cur.get("_pending") and ln.strip() and not furniture.match(ln):
                # wrapped indicator name: text in the name column only (comments sit further right)
                left = re.split(r"\s{2,}", ln.strip())[0] if len(ln) - len(ln.lstrip()) < starts[0] - 40 else ""
                if left and "current_date" in cur and len(re.split(r"\s{2,}", ln.strip())) == 1 and len(ln.rstrip()) < starts[0] - 20:
                    cur["name"] = _clean(cur["name"] + " " + left)
            i += 1
    return [{k: v for k, v in x.items() if not k.startswith("_")} for x in out if x["name"] and x["_ok"]]


def parse_icr(text: str, doc_type: str, report_date: date | None = None) -> ParsedReport:
    r = ParsedReport(doc_type, report_date=report_date)
    t = _strip_page_furniture(text)
    labels = {"outcome": r"Outcomes?", "risk_to_do": r"Risk to Development Outcome", "bank_performance": r"Bank Performance",
              "borrower_performance": r"Borrower Performance", "me_quality": r"Quality of M&E"}
    for key, lab in labels.items():
        for m in re.finditer(r"^\s*" + lab + r"\s*:?[ \t]+(.+)$", t, re.M):
            vals = [v for v in _cols(m.group(1)) if re.fullmatch(RATING_WORDS, v)]
            if not vals:
                continue
            if doc_type == ICRR and len(vals) >= 2:
                r.ratings[key] = {"icr": vals[0], "ieg": vals[1]}
            else:
                r.ratings[key] = {"icr": vals[0]}
            break
    if not r.ratings:
        # Newer ICRs: a "KEY RATINGS" block with labels on one line and values on the next.
        lines = t.splitlines()
        keymap = {"Outcome": "outcome", "Bank Performance": "bank_performance", "M&E Quality": "me_quality",
                  "Risk to Development Outcome": "risk_to_do", "Borrower Performance": "borrower_performance"}
        for n, ln in enumerate(lines):
            if not re.search(r"KEY RATINGS", ln, re.I):
                continue
            nonempty = [x for x in lines[n + 1:n + 20] if x.strip()]
            for a, bline in zip(nonempty, nonempty[1:]):
                labels, values = _cols(a), _cols(bline)
                if labels and len(labels) == len(values) and all(lab in keymap for lab in labels) \
                        and all(re.fullmatch(RATING_WORDS, v) for v in values):
                    for lab, val in zip(labels, values):
                        r.ratings[keymap[lab]] = {"icr": val}
                    break
            if r.ratings:
                break
    if not r.ratings:
        r.notes.append("No ratings recognised in the text rendition.")
    return r


class WorldBankDocumentsConnector(Connector):
    key = "worldbank_documents"
    name = "World Bank — Documents & Reports (ISR, ICR, ICR Review)"
    partner_code = "WB"
    tier = 1
    access_method = "public_json_api + plain-text document renditions"
    base_url = "https://search.worldbank.org/api/v2/wds"
    documentation_url = "https://documents.worldbank.org/en/publication/documents-reports/api"
    usage_terms = "World Bank Terms of Use; publicly disclosed documents; attribution to the World Bank."
    update_frequency = "ISRs roughly twice a year per active project; ICRs at closing"
    default_schedule = "0 4 * * *"
    custom_run = True
    min_interval_seconds = 1.0

    def documents(self, project_id: str) -> list[dict]:
        resp = self.get(self.config.get("base_url") or self.base_url, params={
            "format": "json", "proid": project_id, "rows": 200,
            "fl": "id,docty,docdt,display_title,pdfurl,txturl,lang,repnb,url"})
        docs = resp.json().get("documents") or {}
        return [v for k, v in docs.items() if k != "facets" and isinstance(v, dict)]

    def text(self, url: str) -> str:
        return self.get(url.replace("http://", "https://", 1)).content.decode("utf-8", errors="replace")

    def pdf(self, url: str) -> bytes:
        content = self.get(url.replace("http://", "https://", 1)).content
        if not content.startswith(b"%PDF"):
            raise ConnectorError(f"not a PDF: {url}")
        return content

    def fetch(self, params: SyncParams) -> Iterator[RawRecord]:  # pragma: no cover - custom run
        return iter(())

    def normalize(self, raw: RawRecord):  # pragma: no cover - custom run
        return None


def to_decimal_value(v: str | None) -> Decimal | None:
    if v is None:
        return None
    s = v.strip().replace(",", "")
    m = re.fullmatch(r"-?\d+(?:\.\d+)?", s.rstrip("%"))
    return Decimal(m.group(0)) if m else None


# --- Post-2024 ISR layout: results tables read from the PDF by word position ----------------------------------
# Since ~2024 the text rendition of an ISR contains the indicator names but not the table values. The PDF has them:
#   header      Baseline | Actual (Previous) | Actual (Current) | Closing Period
#   sub-header  Value Month/Year | Value Date | Value Date | Value Month/Year
#   value row   one line of numbers/dates in those 8 sub-columns (empty cells simply have no word)
#   name        in the left column, on the value row and/or the lines just below it; "Comments on achieving targets"
#               and the comment text sit in the middle/right columns of the same lines.
# Each word is assigned to the nearest sub-column; a word whose kind (value vs date) does not match its column, or two
# words in one cell, make the whole row rejected rather than guessed.

VALUE_TOKEN = re.compile(r"^(?:-?[\d,]+(?:\.\d+)?%?|\d{2}-[A-Z][a-z]{2}-\d{4}|[A-Z][a-z]{2}/\d{4}|Yes|No|N/A)$")
FULL_DATE = re.compile(r"^\d{2}-[A-Z][a-z]{2}-\d{4}$")
MONTH_YEAR = re.compile(r"^[A-Z][a-z]{2}/\d{4}$")
SLOTS = ["baseline", "previous", "current", "target"]
SUBHEAD = ("Value", "Date", "Month/Year")


def _rows(words, tol: float = 3.0) -> list[list]:
    rows: list[list] = []
    for w in sorted(words, key=lambda w: (w[1], w[0])):
        if rows and abs(rows[-1][0][1] - w[1]) <= tol:
            rows[-1].append(w)
        else:
            rows.append([w])
    return [sorted(r, key=lambda w: w[0]) for r in rows]


def _subheader_columns(row) -> list[tuple[float, str, str]] | None:
    """(x-center, slot, 'value'|'date') for the sub-columns of a 'Value / Date / Month/Year' header row."""
    if len(row) < 6 or any(w[4] not in SUBHEAD for w in row):
        return None
    if len(row) == 8:
        slots = SLOTS
    elif len(row) == 6:
        slots = ["baseline", "current", "target"]  # layout without an "Actual (Previous)" column
    else:
        return None
    cols = [((w[0] + w[2]) / 2, slots[i // 2], "value" if w[4] == "Value" else "date") for i, w in enumerate(row)]
    if any(c[2] != ("value" if i % 2 == 0 else "date") for i, c in enumerate(cols)):
        return None
    return cols


def _table_words(page) -> list:
    """Words of the page body, without page furniture (running header, footer) and bold section titles."""
    skip = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln["spans"]:
                # bold = section / page titles; small = footer; top band = running header (project name)
                if sp["flags"] & 16 or sp["size"] < 9 or sp["bbox"][3] < 65:
                    skip.append(sp["bbox"])
    out = []
    for w in page.get_text("words"):
        cx, cy = (w[0] + w[2]) / 2, (w[1] + w[3]) / 2
        if not any(x0 <= cx <= x1 and y0 <= cy <= y1 for x0, y0, x1, y1 in skip):
            out.append(w)
    return out


def parse_isr_pdf_results(pdf: bytes) -> list[dict]:
    import pymupdf

    found: list[dict] = []
    cols = None
    current: dict | None = None
    with pymupdf.open(stream=pdf, filetype="pdf") as doc:
        for page in doc:
            if current is not None and current["name"] and current["name"][-1].rstrip().endswith(")"):
                current = None  # names end with their unit "(...)": a complete name does not continue on the next page
            for row in _rows(_table_words(page)):
                texts = [w[4] for w in row]
                sub = _subheader_columns(row)
                if sub:
                    cols, current = sub, None
                    continue
                if "Baseline" in texts or ("Indicator" in texts and "Name" in texts):
                    current = None
                    continue
                if not cols:
                    continue
                # name column ends left of the baseline values (which start ~35pt left of the "Value" header centre)
                name_limit = min(c[0] for c in cols) - 38
                left = [w for w in row if w[0] < name_limit]
                right = [w for w in row if w[0] >= name_limit]
                if right and all(VALUE_TOKEN.match(w[4]) for w in right) and (len(right) >= 2 or left):
                    cells: dict[str, dict[str, str]] = {}
                    ok = True
                    for w in right:
                        cx = (w[0] + w[2]) / 2
                        _, slot, kind = min(cols, key=lambda c: abs(c[0] - cx))
                        is_date = bool(FULL_DATE.match(w[4]) or MONTH_YEAR.match(w[4]))
                        if (kind == "date") != is_date or kind in cells.get(slot, {}):
                            ok = False  # token does not fit its column: reject the row, never guess
                            break
                        cells.setdefault(slot, {})[kind] = w[4]
                    current = {"name": [], "cells": cells, "ok": ok}
                    found.append(current)
                if current is not None and left:
                    current["name"].append(" ".join(w[4] for w in left))
    out = []
    for r in found:
        name = _clean(" ".join(r["name"]))
        if not r["ok"] or not name:
            continue
        um = re.search(r"\(([^()]*(?:\([^()]*\))?[^()]*)\)\s*$", name)
        ind = {"name": name[: um.start()].strip() if um else name, "unit": um.group(1) if um else None}
        for slot in SLOTS:
            c = r["cells"].get(slot, {})
            ind[slot] = c.get("value")
            d = c.get("date")
            # "Jun/2020" has no day: the date is left empty (no day invented) and the period kept as text
            ind[f"{slot}_date"] = wb_date(d) if d and FULL_DATE.match(d) else None
            if d and MONTH_YEAR.match(d):
                ind[f"{slot}_period"] = d
        if any(ind[s] is not None for s in SLOTS):
            out.append(ind)
    return out
