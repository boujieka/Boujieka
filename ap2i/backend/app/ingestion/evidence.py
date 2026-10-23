"""Documentary evidence from public sources (AP²I research), with full provenance.

Each record is one fact stated by a public source that the researcher fetched, with a verbatim quote:

    {"ap2i_id", "agreement", "field", "value", "currency", "as_of", "source_url", "source_publisher",
     "source_type", "published", "quote", "retrieved_at", "confidence"}

Every record is stored as a source record (connector `documentary_research`) and a source observation, linked to the
project, so it is visible with its URL and quote. Project fields are updated ONLY from official sources (donor,
operator, government) with high/medium confidence, and only when the stated fact maps unambiguously to a field:

  * operational_status  -> projects.operational_status (+ status_source)
  * commissioning_date  -> projects.commissioning_date
  * physical_progress_pct (with a date) -> projects.physical_progress_pct / physical_progress_date
  * project_status      -> projects.status (+ dated status-history entry)
  * completion_date     -> projects.actual_completion_date (closed / completed projects only)
  * disbursed_amount    -> agreement reported cumulative disbursed, only when the agreement has no disbursement data of
                           its own and the currency is the agreement's currency

Press and other secondary sources are stored as observations to review (`needs_review`) and never change a field.
Nothing is inferred: "in operation" does not imply "fully disbursed".
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from decimal import Decimal, InvalidOperation

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    DataValidation,
    Disbursement,
    FinancingAgreement,
    Project,
    ProjectSourceLink,
    ProjectStatusHistory,
    SourceConnector,
    SourceObservation,
    SourceRecord,
)

CONNECTOR_KEY = "documentary_research"
FIELDS = {"operational_status", "commissioning_date", "physical_progress_pct", "project_status", "disbursed_amount",
          "disbursement_pct", "closing_date", "completion_date", "other"}
OFFICIAL = {"donor_official", "operator_official", "government_official"}
SOURCE_TYPES = OFFICIAL | {"press", "other"}
OPERATIONAL = {"operational", "partially_operational", "not_operational"}
STATUS_WORDS = {"completed": "completed", "closed": "closed", "active": "active", "ongoing": "active", "cancelled": "cancelled",
                "canceled": "cancelled", "suspended": "suspended", "pipeline": "pipeline", "finalisation": "completed"}


def _connector(db: Session) -> SourceConnector:
    c = db.scalar(select(SourceConnector).where(SourceConnector.key == CONNECTOR_KEY))
    if c is None:
        c = SourceConnector(key=CONNECTOR_KEY, name="AP²I documentary research (public official sources, cited)", tier=1,
                            enabled=False, status="manual", access_method="documentary_research",
                            usage_terms="Facts quoted from public pages and documents; each record keeps its URL and verbatim quote.",
                            update_frequency="On research campaigns")
        db.add(c)
        db.flush()
    return c


def _date(v) -> date | None:
    if not v:
        return None
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", str(v))
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def _num(v) -> Decimal | None:
    if v is None or isinstance(v, bool):
        return None
    try:
        return Decimal(str(v).replace(",", "").replace("%", "").strip())
    except InvalidOperation:
        return None


def validate(r: dict) -> str | None:
    """Reason why a record is rejected, or None."""
    for k in ("field", "value", "source_url", "source_publisher", "source_type", "quote"):
        if not r.get(k) and r.get(k) != 0:
            return f"missing {k}"
    if r["field"] not in FIELDS:
        return f"unknown field {r['field']}"
    if r["source_type"] not in SOURCE_TYPES:
        return f"unknown source_type {r['source_type']}"
    if not re.match(r"^https?://", str(r["source_url"])):
        return "source_url is not an http(s) URL"
    if len(str(r["quote"]).strip()) < 8:
        return "quote too short"
    if r.get("currency") and not re.match(r"^[A-Z]{3}$", str(r["currency"])):
        return "currency is not an ISO 4217 code (state amounts in units, e.g. 53270000 USD, not 'USD million')"
    return None


def _project(db: Session, ap2i_id: str | None) -> Project | None:
    if not ap2i_id:
        return None
    p = db.scalar(select(Project).where(Project.ap2i_id == ap2i_id))
    while p is not None and p.merged_into_id:
        p = db.get(Project, p.merged_into_id)
    return p


def import_evidence(db: Session, records: list[dict], apply: bool = True, today: date | None = None) -> dict:
    today = today or date.today()
    conn = _connector(db)
    out = {"records": len(records), "stored": 0, "already_stored": 0, "rejected": 0, "applied": 0, "review": 0,
           "rejections": [], "applied_changes": []}
    # oldest first, so that the most recent dated fact is the one left on the project
    records = sorted(records, key=lambda r: str(r.get("as_of") or r.get("published") or ""))
    for r in records:
        reason = validate(r)
        p = _project(db, r.get("ap2i_id"))
        if reason is None and p is None:
            reason = f"unknown project {r.get('ap2i_id')}"
        if reason:
            out["rejected"] += 1
            out["rejections"].append({"record": {k: r.get(k) for k in ("ap2i_id", "field", "source_url")}, "reason": reason})
            continue
        payload = {k: r.get(k) for k in ("ap2i_id", "agreement", "field", "value", "currency", "as_of", "source_url",
                                         "source_publisher", "source_type", "published", "quote", "retrieved_at", "confidence")}
        sha = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        ident = f"evidence:{sha[:24]}"
        if db.scalar(select(SourceRecord.id).where(SourceRecord.connector_id == conn.id, SourceRecord.source_identifier == ident)):
            out["already_stored"] += 1
            continue
        official = r["source_type"] in OFFICIAL and not str(r.get("confidence") or "").lower().startswith("low")
        src = SourceRecord(connector_id=conn.id, source_identifier=ident, record_type="evidence", country_iso3=p.country.iso3,
                           payload=payload, payload_sha256=sha, source_url=r["source_url"],
                           source_last_updated=str(r.get("published") or r.get("as_of") or "")[:40] or None,
                           processing_status="imported" if official else "review",
                           processing_note=None if official else "Secondary or low-confidence source: shown for review, no field updated")
        db.add(src)
        db.flush()
        db.add(ProjectSourceLink(project_id=p.id, source_record_id=src.id, link_type="evidence", match_rule="documentary research",
                                 active=True))
        value = r["value"]
        as_of = _date(r.get("as_of")) or _date(r.get("published"))
        num = _num(value) if r["field"] in ("physical_progress_pct", "disbursed_amount", "disbursement_pct") else None
        vdate = _date(value) if r["field"] in ("commissioning_date", "closing_date", "completion_date") else None
        db.add(SourceObservation(source_record_id=src.id, project_id=p.id, field=f"evidence_{r['field']}",
                                 source_field=f"{r['source_publisher']} ({r['source_type']})"[:200], value_text=str(value)[:2000],
                                 value_numeric=num, value_date=vdate, currency=r.get("currency"), reporting_date=as_of,
                                 data_nature="officially_reported" if r["source_type"] in OFFICIAL else "reported_secondary",
                                 verification_status="unverified" if official else "needs_review"))
        out["stored"] += 1
        if not official:
            out["review"] += 1
            continue
        if apply:
            # a record of a co-financier merged into this project describes that donor's agreement or component, not the
            # whole asset: its status is kept as evidence only
            merged = p.ap2i_id != r.get("ap2i_id")
            change = None if merged and r["field"] in ("project_status", "completion_date", "operational_status") else \
                _apply(db, p, r, src, value, as_of, num, vdate, today)
            if change:
                out["applied"] += 1
                out["applied_changes"].append({"project": p.ap2i_id, "change": change, "source": r["source_url"]})
                db.add(DataValidation(source_record_id=src.id, project_id=p.id, rule="documentary_evidence_applied", severity="info",
                                      message=f"{change} — source: {r['source_publisher']}, {r['source_url']}"[:2000]))
    db.flush()
    return out


def _apply(db: Session, p: Project, r: dict, src: SourceRecord, value, as_of, num, vdate, today: date) -> str | None:
    f = r["field"]
    who = f"{r['source_publisher']}{' (' + str(r.get('published') or r.get('as_of')) + ')' if (r.get('published') or r.get('as_of')) else ''}"
    if f == "operational_status":
        v = str(value).strip().lower()
        if v in OPERATIONAL and p.operational_status != v:
            old = p.operational_status
            p.operational_status = v
            p.status_source = f"Operational status: {who}"[:200]
            return f"operational_status {old} -> {v}"
    elif f == "commissioning_date" and vdate and vdate <= today:
        if p.commissioning_date != vdate:
            p.commissioning_date = vdate
            return f"commissioning_date -> {vdate.isoformat()}"
    elif f == "physical_progress_pct" and num is not None and Decimal(0) <= num <= Decimal(100) and as_of:
        if p.physical_progress_date is None or as_of >= p.physical_progress_date:
            p.physical_progress_pct, p.physical_progress_date = num, as_of
            return f"physical_progress_pct -> {num}% (as of {as_of.isoformat()})"
    elif f == "project_status":
        v = STATUS_WORDS.get(str(value).strip().lower())
        # evidence never reopens a closed project (a donor page left "ongoing" is often stale) nor relabels closed/completed
        if v and v != p.status and p.status not in ("completed", "closed"):
            db.add(ProjectStatusHistory(project_id=p.id, status=v, previous_status=p.status, effective_date=as_of,
                                        source_record_id=src.id, note=f"Documentary evidence: {who}"[:2000]))
            old, p.status = p.status, v
            p.status_source = f"Documentary evidence: {who}"[:200]
            return f"status {old} -> {v}"
    elif f == "completion_date" and vdate and vdate <= today and p.status in ("completed", "closed"):
        if p.actual_completion_date != vdate:
            p.actual_completion_date = vdate
            return f"actual_completion_date -> {vdate.isoformat()}"
    elif f == "disbursed_amount" and num is not None and r.get("agreement"):
        a = db.scalar(select(FinancingAgreement).where(FinancingAgreement.project_id == p.id,
                                                       FinancingAgreement.source_identifier == r["agreement"]))
        has_flows = a is not None and db.scalar(select(func.count(Disbursement.id)).where(
            Disbursement.agreement_id == a.id, Disbursement.is_counted.is_(True), Disbursement.flow_type == "disbursement"))
        if a is not None and a.reported_cumulative_disbursed is None and not has_flows and r.get("currency") == a.currency:
            a.reported_cumulative_disbursed = num
            a.reported_cumulative_as_of = as_of
            a.reported_cumulative_label = f"Published by {r['source_publisher']}: {r['source_url']}"[:300]
            return f"{a.source_identifier} cumulative disbursed -> {num} {a.currency}"
    return None


def apply_groups(db: Session, groups: list[dict]) -> dict:
    """Merge records of one physical project financed by several donors (high-confidence groups with cited evidence).
    Uses the reversible merge of entity resolution; the evidence URLs are kept in the merge reason."""
    from app.ingestion.resolution import merge_projects

    out = {"groups": 0, "merged": 0, "skipped": []}
    for g in groups:
        if not str(g.get("confidence", "")).lower().startswith("high") or not g.get("evidence"):
            out["skipped"].append({"group": g.get("group_name"), "reason": "not high confidence or no evidence"})
            continue
        lead = _project(db, g.get("lead_member"))
        if lead is None:
            out["skipped"].append({"group": g.get("group_name"), "reason": "unknown lead"})
            continue
        urls = "; ".join(e.get("source_url", "") for e in g["evidence"])[:1500]
        done = 0
        for m in g.get("members", []):
            p = _project(db, m)
            if p is None or p.id == lead.id:
                continue
            merge_projects(db, lead.id, p.id, None, f"Co-financing of one asset ({g.get('asset') or g.get('group_name')}); "
                           f"documentary evidence: {urls}")
            done += 1
        if done:
            out["groups"] += 1
            out["merged"] += done
            db.add(DataValidation(project_id=lead.id, rule="cofinancing_grouped", severity="info",
                                  message=f"{done} co-financier record(s) merged into this project: {g.get('group_name')} — {urls}"[:2000]))
    db.flush()
    return out
