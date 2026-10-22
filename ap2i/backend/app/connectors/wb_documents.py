"""World Bank Documents & Reports connector: supervision (ISR) and completion (ICR / ICR Review) reports.

Source: World Bank Documents & Reports API (public, no key)
  https://search.worldbank.org/api/v2/wds?format=json&proid=P157734
Each document has a PDF and a plain-text rendition (`txturl`); AP²I parses the text rendition.
Terms: World Bank Terms of Use for Datasets / documents (public disclosure); attribution kept.

What is extracted (officially reported, as written in the report):
  * ISR: report date, sequence number, ratings (Progress towards PDO, Overall Implementation Progress,
    Overall Risk — previous and current), "Implementation Status and Key Decisions" narrative, original and
    revised closing dates, per-loan disbursement table (original, revised, cancelled, disbursed, undisbursed,
    % disbursed), results indicators with baseline / previous / current / end-target values and dates
    (older ISR layout only — see below).
  * ICR: ratings by the ICR (outcome, risk to development outcome, Bank and borrower performance).
  * ICR Review (IEG): the same ratings as validated by IEG.
What is NOT inferred:
  * Overall physical progress. Percentages mentioned in the narrative (e.g. "92% completion") are stored as
    CANDIDATE observations (verification_status=needs_review); a Data Reviewer must confirm them before they
    become the project's physical progress.
  * Results tables of the post-2024 ISR layout: their values are not in the text rendition (only the indicator
    names are). They are reported as "not extractable from text" rather than guessed.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal

from app.connectors.base import Connector, RawRecord, SyncParams, parse_decimal

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
    if not r.indicators and re.search(r"Indicator Name", t):
        r.notes.append("Results table present but its values are not in the text rendition (post-2024 ISR layout); not extracted.")

    if r.narrative:
        for mm in re.finditer(r"([^.]*?\b(\d{1,3}(?:[.,]\d+)?)\s?%\s+(?:completion|completed|physical|progress|execution|avancement)[^.]*\.)",
                              r.narrative, re.I):
            pct = parse_decimal(mm.group(2).replace(",", "."))
            if pct is not None and pct <= 100:
                r.progress_candidates.append({"value": pct, "sentence": _clean(mm.group(1))[:500]})
    return r


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
