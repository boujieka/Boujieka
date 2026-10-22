"""Persist World Bank documents and the facts parsed from ISR / ICR / ICR Review texts.

Called by the pipeline for connector `worldbank_documents` (custom run). Every parsed fact keeps its
document, source record and report date. Physical-progress percentages found in narratives are only
CANDIDATES for reviewer validation.
"""

from __future__ import annotations

import hashlib
import logging
import re
import json
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.assistant.safety import scan_for_injection
from app.connectors.base import ConnectorError, SyncParams, parse_date
from app.connectors.wb_documents import ICR, ICRR, ISR, PARSED_TYPES, WorldBankDocumentsConnector, parse_icr, parse_isr, to_decimal_value
from app.models import (
    Country,
    DataValidation,
    Document,
    FinancingAgreement,
    ImplementationProgress,
    Project,
    ProjectIdentifier,
    ResultsIndicator,
    ResultsObservation,
    SourceObservation,
    SourceRecord,
)

MAX_TEXT = 1_000_000
log = logging.getLogger("ap2i.wb_documents")


def _rating_string(ratings: dict, doc_type: str) -> str | None:
    if not ratings:
        return None
    if doc_type == ISR:
        names = {"pdo": "PDO", "ip": "IP", "risk": "Risk"}
        return "|".join(f"{names[k]}={v['current']}" for k, v in ratings.items() if v.get("current"))
    names = {"outcome": "Outcome", "risk_to_do": "RiskToDO", "bank_performance": "Bank", "borrower_performance": "Borrower",
             "me_quality": "M&E"}
    parts = []
    for k, v in ratings.items():
        s = f"{names.get(k, k)}={v.get('icr')}"
        if v.get("ieg"):
            s += f" (IEG={v['ieg']})"
        parts.append(s)
    return ("ICR: " if doc_type == ICR else "ICR Review: ") + "|".join(parts)


def run_wb_documents(db: Session, connector: WorldBankDocumentsConnector, connector_row, run, params: SyncParams, stats) -> None:
    since = int((connector_row.config or {}).get("since_year", 2011))
    countries = [c.id for c in db.scalars(select(Country).where(Country.iso3.in_(params.countries)))]
    rows = db.execute(select(ProjectIdentifier.identifier, Project).join(Project, Project.id == ProjectIdentifier.project_id).where(
        ProjectIdentifier.scheme == "wb", Project.country_id.in_(countries), Project.merged_into_id.is_(None),
        Project.tenant_id.is_(None))).all()
    projects_done = 0
    rows = [r for r in rows if re.fullmatch(r"P\d{6}", r[0])]
    for pid, project in sorted(rows, key=lambda r: r[0]):
        if params.limit and projects_done >= params.limit:
            break
        projects_done += 1
        if projects_done % 10 == 0:
            log.info("worldbank_documents: %d/%d projects, %d documents, %d parsed, %d failed", projects_done, len(rows),
                     stats.retrieved, stats.imported, stats.failed)
        try:
            docs = connector.documents(pid)
        except ConnectorError as exc:
            stats.failed += 1
            stats.errors.append({"record": pid, "stage": "list_documents", "error": str(exc)[:300]})
            continue
        latest_isr: tuple[date, object] | None = None
        for d in sorted(docs, key=lambda x: x.get("docdt") or ""):
            stats.retrieved += 1
            try:
                with db.begin_nested():
                    outcome = _store_document(db, connector, connector_row, run, project, pid, d, since, stats)
                if outcome and outcome[0] == ISR and outcome[1] is not None:
                    if latest_isr is None or outcome[1] >= latest_isr[0]:
                        latest_isr = (outcome[1], outcome[2])
            except ConnectorError as exc:
                stats.failed += 1
                stats.errors.append({"record": d.get("id"), "stage": "fetch_text", "error": str(exc)[:300]})
            except Exception as exc:  # noqa: BLE001 — one bad document must not stop the run
                stats.failed += 1
                stats.errors.append({"record": d.get("id"), "stage": "parse", "error": f"{type(exc).__name__}: {exc}"[:300]})
        if latest_isr is not None:
            _apply_latest_dates(db, project, pid, latest_isr[1])
        db.commit()


def _store_document(db, connector, connector_row, run, project: Project, pid: str, d: dict, since: int, stats):
    doc_id = str(d.get("id"))
    docty = " ".join((d.get("docty") or "").split())
    title = " ".join((d.get("display_title") or docty or "World Bank document").split())
    docdt = parse_date(d.get("docdt"))
    url = d.get("pdfurl") or d.get("url") or d.get("txturl")
    meta = {k: d.get(k) for k in ("id", "docty", "docdt", "display_title", "pdfurl", "txturl", "lang", "repnb", "url")}
    sha = hashlib.sha256(json.dumps(meta, sort_keys=True).encode()).hexdigest()
    ident = f"wds:{doc_id}"
    src = db.scalar(select(SourceRecord).where(SourceRecord.connector_id == connector_row.id, SourceRecord.source_identifier == ident,
                                               SourceRecord.payload_sha256 == sha))
    if src is None:
        src = SourceRecord(connector_id=connector_row.id, sync_run_id=run.id, source_identifier=ident, record_type="wb_document",
                           country_iso3=project.country.iso3 if project.country else None, payload={**meta, "project_id": pid},
                           payload_sha256=sha, source_url=url, source_last_updated=(d.get("docdt") or "")[:10],
                           processing_status="imported")
        db.add(src)
        db.flush()
        stats.new += 1
    doc = db.scalar(select(Document).where(Document.project_id == project.id, Document.url == url))
    if doc is None:
        doc = Document(project_id=project.id, title=title[:2000], doc_type=docty or None, url=url,
                       language={"English": "en", "French": "fr"}.get(d.get("lang") or "", None), published_date=docdt,
                       source_record_id=src.id)
        db.add(doc)
        db.flush()
    if docty not in PARSED_TYPES or not d.get("txturl") or (docdt and docdt.year < since):
        stats.unchanged += 0
        return None
    if doc.extracted_text:
        stats.unchanged += 1
        rep = parse_isr(doc.extracted_text, docdt) if docty == ISR else None  # local re-parse, no download
        return docty, docdt, rep
    text = connector.text(d["txturl"])[:MAX_TEXT]
    doc.extracted_text = text
    doc.sha256 = hashlib.sha256(text.encode()).hexdigest()
    doc.mime_type = "text/plain"
    doc.size_bytes = len(text.encode())
    doc.injection_flags = scan_for_injection(text)
    if doc.injection_flags:
        db.add(DataValidation(source_record_id=src.id, project_id=project.id, rule="prompt_injection_pattern", severity="warning",
                              message=f"Document text contains instruction-like patterns {doc.injection_flags}; treated as data only"))
    if docty == ISR:
        rep = parse_isr(text, docdt)
    else:
        rep = parse_icr(text, docty, docdt)
    _apply(db, project, doc, src, rep, docty, docdt, stats)
    stats.imported += 1
    return docty, docdt, rep


def _obs(db, src, project_id, field, source_field, value=None, numeric=None, vdate=None, currency=None, rdate=None,
         verification="unverified"):
    db.add(SourceObservation(source_record_id=src.id, project_id=project_id, field=field, source_field=source_field,
                             value_text=None if value is None else str(value)[:20000], value_numeric=numeric, value_date=vdate,
                             currency=currency, reporting_date=rdate, verification_status=verification))


def _apply(db: Session, project: Project, doc: Document, src: SourceRecord, rep, docty: str, docdt: date | None, stats) -> None:
    rating = _rating_string(rep.ratings, docty)
    fin_pct = None
    if docty == ISR and len(rep.loans) == 1 and rep.loans[0]["pct_disbursed"] is not None:
        fin_pct = rep.loans[0]["pct_disbursed"]
    if docdt and not db.scalar(select(ImplementationProgress).where(ImplementationProgress.project_id == project.id,
                                                                   ImplementationProgress.document_id == doc.id)):
        db.add(ImplementationProgress(project_id=project.id, report_date=docdt, physical_progress_pct=None, financial_progress_pct=fin_pct,
                                      narrative=rep.narrative, rating=rating, document_id=doc.id, source_record_id=src.id,
                                      data_nature="officially_reported", verification_status="unverified"))
    sf = f"{docty} {rep.sequence or ''}".strip()
    for key, v in rep.ratings.items():
        _obs(db, src, project.id, f"wb_rating_{key}", sf, json.dumps(v), rdate=docdt)
    if rep.narrative:
        _obs(db, src, project.id, "wb_implementation_status", sf, rep.narrative, rdate=docdt)
    if rep.original_closing:
        _obs(db, src, project.id, "original_closing_date", sf, vdate=rep.original_closing, rdate=docdt)
    if rep.revised_closing:
        _obs(db, src, project.id, "revised_closing_date", sf, vdate=rep.revised_closing, rdate=docdt)
    for ln in rep.loans:
        for k in ("original", "revised", "cancelled", "disbursed", "undisbursed"):
            if ln[k] is not None:
                _obs(db, src, project.id, f"wb_loan_{k}:{ln['loan']}", f"{sf} — {ln['unit']}", numeric=ln[k], currency=ln["currency"], rdate=docdt)
        if ln["pct_disbursed"] is not None:
            _obs(db, src, project.id, f"wb_loan_pct_disbursed:{ln['loan']}", sf, numeric=ln["pct_disbursed"], rdate=docdt)
    for note in rep.notes:
        db.add(DataValidation(source_record_id=src.id, project_id=project.id, rule="document_partially_extracted", severity="info", message=note))
    for ind in rep.indicators:
        ri = db.scalar(select(ResultsIndicator).where(ResultsIndicator.project_id == project.id, ResultsIndicator.name == ind["name"][:5000]))
        if ri is None:
            ri = ResultsIndicator(project_id=project.id, name=ind["name"][:5000], unit=ind.get("unit"), measure="as reported",
                                  source_record_id=src.id)
            db.add(ri)
            db.flush()
        b, t = to_decimal_value(ind["baseline"]), to_decimal_value(ind["target"])
        ri.baseline_value, ri.target_value = b, t
        ri.baseline_date, ri.target_date = ind.get("baseline_date"), ind.get("target_date")
        for which in ("previous", "current"):
            val, when = ind[which], ind.get(f"{which}_date")
            if when is None:
                continue
            num = to_decimal_value(val)
            exists = db.scalar(select(ResultsObservation).where(ResultsObservation.indicator_id == ri.id, ResultsObservation.period_end == when))
            if exists is None:
                db.add(ResultsObservation(indicator_id=ri.id, value=num, value_text=None if num is not None else val, period_end=when,
                                          source_record_id=src.id, data_nature="officially_reported"))
    for c in rep.progress_candidates:
        _obs(db, src, project.id, "physical_progress_candidate", f"{sf} narrative", c["sentence"], numeric=c["value"], vdate=docdt,
             rdate=docdt, verification="needs_review")
        db.add(DataValidation(source_record_id=src.id, project_id=project.id, rule="physical_progress_candidate", severity="info",
                              message=f"Narrative states {c['value']}%: \"{c['sentence'][:300]}\" — confirm before use as physical progress"))
        src.processing_status = "review"
        src.processing_note = "Physical-progress candidate awaiting reviewer validation"
        stats.review += 1
    if docty in (ICR, ICRR) and rating:
        project.development_results = f"{rating} ({docty}, {docdt.isoformat() if docdt else 'undated'})"[:4000]


def _apply_latest_dates(db: Session, project: Project, pid: str, rep) -> None:
    """Dates from the latest ISR are the officially reported original and current closing dates."""
    if rep is None:
        return
    if rep.original_closing:
        project.original_completion_date = rep.original_closing
    if rep.revised_closing and rep.original_closing and rep.revised_closing != rep.original_closing:
        project.revised_completion_date = rep.revised_closing
    agr = db.scalar(select(FinancingAgreement).where(FinancingAgreement.project_id == project.id,
                                                     FinancingAgreement.source_identifier == pid))
    if agr is not None and rep.original_closing and agr.closing_date_original is None:
        agr.closing_date_original = rep.original_closing


__all__ = ["run_wb_documents", "Decimal"]
