"""AfDB project documents: completion reports (PCR / RAP) and IDEV PCR review notes (PCR-EVN / Note de revue de RAP).

Where the documents come from: the document links that AfDB itself publishes in its IATI activities
(connector `afdb_iati`). Two hosts are involved (checked 2026-10-22):
  * evrd.afdb.org — AfDB Independent Development Evaluation repository: PDFs downloadable directly. These are
    completion reports (file names PR…) and IDEV review notes of completion reports (PN…).
  * www.afdb.org (and mapafrica / idev.afdb.org) — return an anti-bot challenge page (HTTP 403 "Just a moment…").
    AP²I does NOT try to get around that protection. Those documents (incl. the EER / IPR supervision reports)
    are catalogued with their link and can be added through the document upload workflow by a person who
    downloaded them from the AfDB website.

What is extracted (officially reported, from the PDF text layer):
  * "Données de base / Basic data" header: approval, signature and effectiveness dates, original and revised
    closing dates, completion-report date, cancelled amount (in Units of Account — UA, the AfDB's SDR-based unit).
    The financing-sources table is not extracted (columns misread too often on the real corpus).
  * IDEV review notes (2012+ template): numeric ratings on the 1–4 scale (4 = highly satisfactory,
    1 = highly unsatisfactory) for the development objective, Bank performance, borrower performance and other
    stakeholders, as given by the completion report (RAP) and as validated by IDEV. A rating is kept only when
    both numbers are present; text labels are not used (they are often misaligned in the PDF text layer).
Completion reports' own rating tables vary too much between templates and are not parsed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation

RATING_SCALE = {4: "Highly satisfactory", 3: "Satisfactory", 2: "Unsatisfactory", 1: "Highly unsatisfactory"}

PN_RATINGS = {
    "development_objective": r"NOTE DE L.OBJECTIF DE D[ÉE]VELOPPEMENT",
    "bank_performance": r"NOTATION DE LA PERFORMANCE DE LA BANQUE",
    "borrower_performance": r"NOTATION DE LA PERFORMANCE DE L.EMPRUNTEUR",
    "other_stakeholders": r"NOTATION DE LA PERFORMANCE DES AUTRES PARTIES\s+PRENANTES",
    "outcomes": r"Note globale pour les effets",
}

DATE_LABELS = {
    "approval_date": [r"Date d.approbation", r"Approval date", r"Date of approval"],
    "signature_date": [r"Date de signature", r"Signature date", r"Date of signature"],
    "effectiveness_date": [r"Date d.entr[ée]e en vigueur(?! du premier)", r"Effectiveness date", r"Date of effectiveness"],
    "original_closing_date": [r"Date initiale de cl[ôo]ture", r"Date de cl[ôo]ture initiale", r"Original closing date"],
    "revised_closing_date": [r"Date de cl[ôo]ture r[ée]vis[ée]e", r"Revised closing date"],
}
DATE_VALUE = r"(\d{1,2}\s?/\s?\d{1,2}\s?/\s?\d{4}|\d{1,2}[- ][A-Za-zéû]{3,9}[- ]\d{4})"
MONTHS = {"jan": 1, "janv": 1, "janvier": 1, "january": 1, "feb": 2, "fev": 2, "fév": 2, "février": 2, "fevrier": 2,
          "february": 2, "mar": 3, "mars": 3, "march": 3, "apr": 4, "avr": 4, "avril": 4, "april": 4, "may": 5, "mai": 5,
          "jun": 6, "juin": 6, "june": 6, "jul": 7, "juil": 7, "juillet": 7, "july": 7, "aug": 8, "aout": 8, "août": 8,
          "august": 8, "sep": 9, "sept": 9, "septembre": 9, "september": 9, "oct": 10, "octobre": 10, "october": 10,
          "nov": 11, "novembre": 11, "november": 11, "dec": 12, "déc": 12, "décembre": 12, "decembre": 12, "december": 12}


def parse_any_date(s: str | None) -> date | None:
    if not s:
        return None
    s = re.sub(r"\s", "", s) if "/" in s else s.strip()
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    try:
        if m:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        m = re.fullmatch(r"(\d{1,2})[- ]([A-Za-zéû]+)[- ](\d{4})", s)
        if m and m.group(2).lower().rstrip(".") in MONTHS:
            return date(int(m.group(3)), MONTHS[m.group(2).lower().rstrip(".")], int(m.group(1)))
    except ValueError:
        return None  # e.g. "31/11/2019" (non-existent day) stays missing, never corrected by guess
    return None


def parse_amount(s: str) -> Decimal | None:
    """French/English formatted amounts: '39 626 926,07', '47,260,000', '12.5'."""
    s = s.strip().replace(" ", " ").replace(" ", " ")
    if re.fullmatch(r"\d{1,3}( \d{3})+(,\d+)?", s) or re.fullmatch(r"\d+,\d{1,2}", s):
        s = s.replace(" ", "").replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", s):
        s = s.replace(",", "")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", s):
        s = s.replace(".", "").replace(",", ".")
    s = s.replace(" ", "")
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


@dataclass
class AfdbReport:
    kind: str  # pcr_review_note | completion_report | other
    project_code: str | None = None
    dates: dict[str, date] = field(default_factory=dict)
    cancelled_ua: Decimal | None = None
    report_date: date | None = None
    ratings: dict[str, dict[str, int]] = field(default_factory=dict)  # name -> {"rap": n, "idev": n}
    notes: list[str] = field(default_factory=list)


def classify(filename: str, text: str) -> str:
    name = filename.upper()
    if name.startswith("PN") or re.search(r"NOTE DE REVUE DE RAP|PCR EVALUATION NOTE|PCR-?EVN", text, re.I):
        return "pcr_review_note"
    if name.startswith("PR") or re.search(r"RAPPORT D.ACH[ÈE]VEMENT|PROJECT COMPLETION REPORT", text, re.I):
        return "completion_report"
    return "other"


def parse_afdb_report(text: str, filename: str = "") -> AfdbReport:
    flat = re.sub(r"[  ]", " ", text)
    flat = re.sub(r"\s+", " ", flat)
    r = AfdbReport(kind=classify(filename, flat))
    m = re.search(r"P-[A-Z]{2}-[A-Z0-9]{3}-\d{3}", flat)
    r.project_code = m.group(0) if m else None

    head = flat[:12000]  # "Données de base / Basic data" is at the top of both templates
    for key, labels in DATE_LABELS.items():
        for lab in labels:
            m = re.search(lab + r"\s*:?\s*" + DATE_VALUE, head, re.I)
            if m:
                d = parse_any_date(m.group(1))
                if d:
                    r.dates[key] = d
                    break
    m = re.search(r"Montants? annul[ée]s?\s*:?\s*([\d][\d ,.]*\d)\s*UC", head, re.I) or \
        re.search(r"Cancell?ed amounts?\s*:?\s*(?:UA\s*)?([\d][\d ,.]*\d)", head, re.I)
    if m:
        r.cancelled_ua = parse_amount(m.group(1))

    m = re.search(r"Date du RAP\s*:?\s*" + DATE_VALUE, head, re.I) or re.search(r"Date of (?:the )?PCR\s*:?\s*" + DATE_VALUE, head, re.I)
    if m:
        r.report_date = parse_any_date(m.group(1))
    # The financing-sources table is NOT extracted: on the real corpus its columns were too often misread
    # (wrong totals), and a wrong amount is worse than a missing one.

    if r.kind == "pcr_review_note":
        for key, rx in PN_RATINGS.items():
            m = re.search(rx + r"\s+([1-4](?:[.,]\d)?)\s+([1-4](?:[.,]\d)?)\b", flat, re.I)
            if m:
                rap, idev = (Decimal(x.replace(",", ".")) for x in m.groups())
                r.ratings[key] = {"rap": float(rap), "idev": float(idev)}
        if not r.ratings:
            r.notes.append("Review-note ratings not recognised (older template or table not in the text layer).")
    elif r.kind == "completion_report":
        r.notes.append("Completion-report rating tables are not parsed (templates vary); text stored for reading.")
    return r


from app.connectors.base import Connector, RawRecord, SyncParams  # noqa: E402

DIRECT_HOSTS = ("evrd.afdb.org/documents/docs/",)
BLOCKED_HOSTS = ("www.afdb.org", "mapafrica.afdb.org", "idev.afdb.org", "projectsportal.afdb.org", "esa.afdb.org")


class AfDBDocumentsConnector(Connector):
    key = "afdb_documents"
    name = "AfDB — completion reports and IDEV review notes (evrd.afdb.org)"
    partner_code = "AFDB"
    tier = 1
    access_method = "direct_pdf_download (evrd.afdb.org links from AfDB IATI)"
    base_url = "https://evrd.afdb.org"
    documentation_url = "https://idev.afdb.org"
    usage_terms = ("Public AfDB documents. www.afdb.org serves an anti-bot challenge: those documents are not fetched "
                   "automatically and can be added through the document upload workflow.")
    update_frequency = "At project completion and evaluation"
    default_schedule = "0 5 * * 1"  # weekly
    custom_run = True
    min_interval_seconds = 1.0

    def download(self, url: str) -> bytes:
        return self.get(url).content

    def fetch(self, params: SyncParams):  # pragma: no cover - custom run
        return iter(())

    def normalize(self, raw: RawRecord):  # pragma: no cover - custom run
        return None
