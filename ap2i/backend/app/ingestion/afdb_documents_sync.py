"""Persist AfDB completion reports / IDEV review notes and what is parsed from them (connector `afdb_documents`),
and the shared document-upload path used for PDFs downloaded by a person (e.g. EER / IPR from www.afdb.org)."""

from __future__ import annotations

import hashlib
import io
import logging

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.assistant.safety import scan_for_injection
from app.connectors.afdb_documents import (
    BLOCKED_HOSTS,
    DIRECT_HOSTS,
    RATING_SCALE,
    AfDBDocumentsConnector,
    AfdbReport,
    parse_afdb_report,
)
from app.connectors.base import ConnectorError, SyncParams
from app.models import (
    Country,
    DataValidation,
    Document,
    FinancingAgreement,
    FinancingPartner,
    ImplementationProgress,
    Project,
    SourceConnector,
    SourceObservation,
    SourceRecord,
)

log = logging.getLogger("ap2i.afdb_documents")
MAX_TEXT = 1_000_000
LABELS = {"development_objective": "DO", "bank_performance": "Bank", "borrower_performance": "Borrower",
          "other_stakeholders": "Others", "outcomes": "Outcomes"}


def pdf_text(content: bytes) -> str:
    import pymupdf

    if not content.startswith(b"%PDF"):
        raise ValueError("not a PDF file")
    with pymupdf.open(stream=io.BytesIO(content), filetype="pdf") as doc:
        if doc.page_count > 600:
            raise ValueError("PDF too long (> 600 pages)")
        return "".join(page.get_text() for page in doc)[:MAX_TEXT]


def rating_string(rep: AfdbReport) -> str | None:
    if not rep.ratings:
        return None
    parts = [f"{LABELS[k]}={v['idev']:g} (RAP {v['rap']:g})" for k, v in rep.ratings.items()]
    return "AfDB PCR review (IDEV, 1-4): " + "|".join(parts)


def apply_report(db: Session, project: Project, doc: Document, src: SourceRecord, rep: AfdbReport) -> None:
    db.execute(delete(SourceObservation).where(SourceObservation.source_record_id == src.id))
    db.execute(delete(DataValidation).where(DataValidation.source_record_id == src.id, DataValidation.rule == "document_partially_extracted"))
    sf = f"AfDB {rep.kind} ({doc.title[:80]})"
    for key, d in rep.dates.items():
        db.add(SourceObservation(source_record_id=src.id, project_id=project.id, field=key, source_field=sf, value_date=d,
                                 reporting_date=rep.report_date))
    if rep.cancelled_ua is not None:
        db.add(SourceObservation(source_record_id=src.id, project_id=project.id, field="cancelled_amount_ua", value_numeric=rep.cancelled_ua,
                                 source_field=f"{sf} — Units of Account (UA)", reporting_date=rep.report_date))
    for key, v in rep.ratings.items():
        db.add(SourceObservation(source_record_id=src.id, project_id=project.id, field=f"afdb_rating_{key}", source_field=sf,
                                 value_text=f"IDEV {v['idev']:g} ({RATING_SCALE.get(round(v['idev']), '?')}); RAP {v['rap']:g}",
                                 value_numeric=None, reporting_date=rep.report_date))
    for note in rep.notes:
        db.add(DataValidation(source_record_id=src.id, project_id=project.id, rule="document_partially_extracted", severity="info", message=note))
    rating = rating_string(rep)
    if rating:
        if rep.report_date:
            ip = db.scalar(select(ImplementationProgress).where(ImplementationProgress.document_id == doc.id))
            if ip is None:
                ip = ImplementationProgress(project_id=project.id, report_date=rep.report_date, document_id=doc.id, source_record_id=src.id,
                                            data_nature="officially_reported", verification_status="unverified")
                db.add(ip)
            ip.rating = rating
        if not project.development_results or project.development_results.startswith("AfDB"):
            project.development_results = (f"{rating} — {doc.title[:120]}"
                                           + (f" ({rep.report_date.isoformat()})" if rep.report_date else ""))[:4000]
    # Dates: completion documents are authoritative for original/revised closing when the project has none.
    if rep.dates.get("original_closing_date") and project.original_completion_date is None:
        project.original_completion_date = rep.dates["original_closing_date"]
    if rep.dates.get("revised_closing_date") and project.revised_completion_date is None and \
            rep.dates.get("revised_closing_date") != rep.dates.get("original_closing_date"):
        project.revised_completion_date = rep.dates["revised_closing_date"]
    afdb = db.scalar(select(FinancingPartner.id).where(FinancingPartner.code == "AFDB"))
    agr = db.scalar(select(FinancingAgreement).where(FinancingAgreement.project_id == project.id, FinancingAgreement.partner_id == afdb))
    if agr is not None:
        agr.closing_date_original = agr.closing_date_original or rep.dates.get("original_closing_date")
        agr.signature_date = agr.signature_date or rep.dates.get("signature_date")
        agr.effectiveness_date = agr.effectiveness_date or rep.dates.get("effectiveness_date")


def store_text(db: Session, doc: Document, text: str, src: SourceRecord) -> None:
    doc.extracted_text = text
    doc.sha256 = hashlib.sha256(text.encode()).hexdigest()
    doc.mime_type = "application/pdf"
    doc.injection_flags = scan_for_injection(text)
    if doc.injection_flags:
        db.add(DataValidation(source_record_id=src.id, project_id=doc.project_id, rule="prompt_injection_pattern", severity="warning",
                              message=f"Document text contains instruction-like patterns {doc.injection_flags}; treated as data only"))


def run_afdb_documents(db: Session, connector: AfDBDocumentsConnector, connector_row: SourceConnector, run, params: SyncParams, stats) -> None:
    countries = [c.id for c in db.scalars(select(Country).where(Country.iso3.in_(params.countries)))]
    iati = db.scalar(select(SourceConnector.id).where(SourceConnector.key == "afdb_iati"))
    docs = db.execute(select(Document, Project).join(Project, Project.id == Document.project_id)
                      .join(SourceRecord, SourceRecord.id == Document.source_record_id)
                      .where(SourceRecord.connector_id == iati, Project.country_id.in_(countries), Project.merged_into_id.is_(None))).all()
    blocked = 0
    for doc, project in docs:
        url = doc.url or ""
        stats.retrieved += 1
        if any(h in url for h in BLOCKED_HOSTS):
            blocked += 1
            continue
        if not any(h in url for h in DIRECT_HOSTS) or not url.lower().endswith(".pdf"):
            continue
        if params.limit and stats.imported >= params.limit:
            break
        try:
            with db.begin_nested():
                ident = "afdb-doc:" + url.rsplit("/", 1)[-1]
                src = db.scalar(select(SourceRecord).where(SourceRecord.connector_id == connector_row.id, SourceRecord.source_identifier == ident))
                if src is None:
                    if doc.extracted_text and not params.reprocess:
                        stats.unchanged += 1
                        continue
                    content = connector.download(url.replace("http://", "https://", 1))
                    text = pdf_text(content)
                    src = SourceRecord(connector_id=connector_row.id, sync_run_id=run.id, source_identifier=ident, record_type="afdb_document",
                                       country_iso3=project.country.iso3 if project.country else None,
                                       payload={"url": url, "title": doc.title, "bytes": len(content)},
                                       payload_sha256=hashlib.sha256(content).hexdigest(), source_url=url, processing_status="imported")
                    db.add(src)
                    db.flush()
                    store_text(db, doc, text, src)
                    stats.new += 1
                elif not params.reprocess:
                    stats.unchanged += 1
                    continue
                rep = parse_afdb_report(doc.extracted_text or "", url.rsplit("/", 1)[-1])
                apply_report(db, project, doc, src, rep)
                stats.imported += 1
        except (ConnectorError, ValueError) as exc:
            stats.failed += 1
            stats.errors.append({"record": url, "stage": "download_or_parse", "error": str(exc)[:300]})
        except Exception as exc:  # noqa: BLE001
            stats.failed += 1
            stats.errors.append({"record": url, "stage": "parse", "error": f"{type(exc).__name__}: {exc}"[:300]})
    db.commit()
    stats.log_lines.append(f"{blocked} document link(s) on www.afdb.org/mapafrica/idev not fetched: anti-bot challenge "
                           "(not circumvented). Use the document upload workflow for these.")
    log.info("afdb_documents: %d links, %d parsed, %d blocked by anti-bot protection", stats.retrieved, stats.imported, blocked)
