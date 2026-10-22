"""Migration from the AP²I Cameroon MVP v0.1 (single-file app.py; SQLite or PostgreSQL).

    python -m app.cli migrate-mvp sqlite:///path/to/ap2i.db

MVP schema (legacy_mvp/app.py): countries(code,name), projects(id, country_code, name, sector, agency,
status, start_year, end_year, initial_cost, revised_cost, currency, physical_progress, operational_status,
source_url, source_date, notes), financings(id, project_id, funder, instrument, committed, currency,
source_url), disbursements(id, financing_id, year, amount, source_url), amendments(id, project_id, date,
amount, currency, reason, source_url), actions(id, project_id, problem, recommendation, owner, due_date, status).

Rules: nothing is silently discarded. Every legacy row becomes a preserved source record (connector
`legacy_mvp`); values are mapped into the new model; anything that cannot be mapped is kept as a source
observation and listed in the migration report. Year-only data stays year-only (no invented day).
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import MetaData, Text, create_engine, select
from sqlalchemy.orm import Session

from app.assistant.service import SECTOR_PATTERNS
from app.connectors.base import parse_date
from app.ingestion.pipeline import mint_ap2i_id
from app.ingestion.resolution import register_identifier
from app.models import (
    Country,
    DataValidation,
    Disbursement,
    FinancingAgreement,
    FinancingCommitment,
    FinancingPartner,
    Project,
    ProjectSourceLink,
    RecoveryAction,
    RecoveryPlan,
    Sector,
    SourceConnector,
    SourceObservation,
    SourceRecord,
)
from app.rescue.engine import FURTHER

STATUS_MAP = {"non renseigne": "unknown", "en cours": "active", "en execution": "active", "actif": "active", "active": "active",
              "acheve": "completed", "termine": "completed", "complete": "completed", "completed": "completed",
              "cloture": "closed", "closed": "closed", "suspendu": "suspended", "annule": "cancelled",
              "operationnel": "completed", "en preparation": "pipeline", "pipeline": "pipeline"}
OPS_MAP = {"operationnel": "operational", "operational": "operational", "fonctionnel": "operational",
           "partiellement operationnel": "partially_operational", "non operationnel": "not_operational",
           "non fonctionnel": "not_operational", "not operational": "not_operational"}
ACTION_STATUS = {"a faire": "not_started", "en cours": "in_progress", "fait": "done", "termine": "done", "bloque": "blocked",
                 "annule": "cancelled"}
FUNDER_MAP = [(r"banque mondiale|world ?bank|\bida\b|\bbird\b|\bibrd\b", "WB"),
              (r"\bbad\b|\bafdb\b|banque africaine|african development", "AFDB"),
              (r"\bafd\b|agence fran", "AFD"), (r"\bbei\b|\beib\b", "EIB"), (r"union europ|\bue\b|\beu\b", "EU"),
              (r"\bbid\b|\bisdb\b|islamique", "ISDB"), (r"kfw", "KFW"), (r"jica", "JICA"), (r"badea", "BADEA"),
              (r"etat|gouvernement|government|\bbip\b|budget", "GOV")]


def _n(s: str | None) -> str:
    return unicodedata.normalize("NFKD", (s or "").strip()).encode("ascii", "ignore").decode().lower()


def _dec(v) -> Decimal | None:
    return None if v is None else Decimal(str(v))


def _legacy_connector(db: Session) -> SourceConnector:
    c = db.scalar(select(SourceConnector).where(SourceConnector.key == "legacy_mvp"))
    if c is None:
        c = SourceConnector(key="legacy_mvp", name="Legacy AP²I Cameroon MVP v0.1 database", tier=1, enabled=False, status="manual",
                            access_method="one_time_migration", usage_terms="Rows entered in the MVP; each cites its own source_url.",
                            config={}, notes="Created by app.migration.mvp")
        db.add(c)
        db.flush()
    return c


def _record(db: Session, conn: SourceConnector, table: str, r: dict) -> tuple[SourceRecord, bool]:
    payload = {k: (str(v) if isinstance(v, (Decimal, date, datetime)) else v) for k, v in r.items()}
    sha = hashlib.sha256(json.dumps({"table": table, **payload}, sort_keys=True, default=str).encode()).hexdigest()
    ident = f"mvp:{table}:{r['id']}"
    existing = db.scalar(select(SourceRecord).where(SourceRecord.connector_id == conn.id, SourceRecord.source_identifier == ident,
                                                    SourceRecord.payload_sha256 == sha))
    if existing:
        return existing, False
    sr = SourceRecord(connector_id=conn.id, source_identifier=ident, record_type=f"legacy_mvp_{table}", payload={"table": table, **payload},
                      payload_sha256=sha, source_url=r.get("source_url"), source_last_updated=r.get("source_date"),
                      processing_status="imported", country_iso3=r.get("country_code"))
    db.add(sr)
    db.flush()
    return sr, True


def _partner(db: Session, funder: str) -> FinancingPartner:
    for rx, code in FUNDER_MAP:
        if re.search(rx, _n(funder)):
            return db.scalar(select(FinancingPartner).where(FinancingPartner.code == code))
    code = ("LEGACY:" + re.sub(r"[^A-Z0-9]+", "_", _n(funder).upper()))[:40]
    p = db.scalar(select(FinancingPartner).where(FinancingPartner.code == code))
    if p is None:
        p = FinancingPartner(code=code, name=funder, short_name=funder[:40], partner_type="unknown", tier=3, iati_org_refs=[],
                             notes="Created from a free-text funder in the legacy MVP; to be reviewed.")
        db.add(p)
        db.flush()
    return p


def migrate(source_url: str, db: Session) -> dict:
    src_engine = create_engine(source_url)
    md = MetaData()
    md.reflect(src_engine)
    tables = {t: md.tables[t] for t in ("countries", "projects", "financings", "disbursements", "amendments", "actions") if t in md.tables}
    with src_engine.connect() as conn:
        data = {t: [dict(r._mapping) for r in conn.execute(select(tbl))] for t, tbl in tables.items()}
    report = {"source": source_url.split("@")[-1], "migrated_at": datetime.now(timezone.utc).isoformat(),
              "read": {t: len(v) for t, v in data.items()}, "created": {}, "unmapped": [], "warnings": []}
    created = {"projects": 0, "agreements": 0, "commitments": 0, "disbursements": 0, "amendment_observations": 0,
               "recovery_actions": 0, "skipped_existing": 0}
    conn_row = _legacy_connector(db)
    countries = {c.iso3: c for c in db.scalars(select(Country))}
    sectors = {s.code: s for s in db.scalars(select(Sector))}
    for c in data.get("countries", []):
        if c["code"].upper() not in countries:
            report["unmapped"].append({"table": "countries", "id": c["code"], "reason": "not one of the 54 reference countries"})

    project_map: dict[str, Project] = {}
    for r in data.get("projects", []):
        sr, new = _record(db, conn_row, "projects", r)
        existing = db.scalar(select(Project).join(ProjectSourceLink, ProjectSourceLink.project_id == Project.id).where(
            ProjectSourceLink.source_record_id == sr.id))
        if not new and existing:
            project_map[r["id"]] = existing
            created["skipped_existing"] += 1
            continue
        iso3 = (r.get("country_code") or "").upper()
        if iso3 not in countries:
            report["unmapped"].append({"table": "projects", "id": r["id"], "reason": f"unknown country {iso3}"})
            sr.processing_status = "review"
            continue
        sector_code = next((code for code, pats in SECTOR_PATTERNS.items() if any(re.search(p, _n(r.get("sector"))) for p in pats)), None)
        status = STATUS_MAP.get(_n(r.get("status")), "unknown")
        ops = OPS_MAP.get(_n(r.get("operational_status")), "unknown")
        p = Project(ap2i_id=mint_ap2i_id(db, iso3, sector_code), country_id=countries[iso3].id, title=r["name"], status=status,
                    status_source="legacy_mvp", executing_agency=r.get("agency"), sector_id=sectors[sector_code].id if sector_code else None,
                    original_estimated_cost=_dec(r.get("initial_cost")), revised_estimated_cost=_dec(r.get("revised_cost")),
                    cost_currency=(r.get("currency") or None) if (r.get("initial_cost") is not None or r.get("revised_cost") is not None) else None,
                    physical_progress_pct=_dec(r.get("physical_progress")), operational_status=ops,
                    physical_progress_date=parse_date(r.get("source_date")) if r.get("physical_progress") is not None else None,
                    data_nature="officially_reported", verification_status="unverified" if r.get("source_url") else "needs_review")
        db.add(p)
        db.flush()
        project_map[r["id"]] = p
        created["projects"] += 1
        register_identifier(db, p.id, "legacy_mvp", r["id"], sr.id)
        db.add(ProjectSourceLink(project_id=p.id, source_record_id=sr.id, link_type="primary", match_rule="legacy_mvp_migration"))
        for field, value in (("legacy_sector_label", r.get("sector")), ("legacy_status_label", r.get("status")),
                             ("legacy_operational_status_label", r.get("operational_status")), ("legacy_start_year", r.get("start_year")),
                             ("legacy_end_year", r.get("end_year")), ("legacy_notes", r.get("notes"))):
            if value not in (None, ""):
                db.add(SourceObservation(source_record_id=sr.id, project_id=p.id, field=field, source_field=field.replace("legacy_", ""),
                                         value_text=str(value), reporting_date=parse_date(r.get("source_date"))))
        if r.get("start_year") or r.get("end_year"):
            report["warnings"].append(f"Project {r['id']}: start/end years kept as observations (the MVP stored years, not dates).")
        if sector_code is None and r.get("sector"):
            report["unmapped"].append({"table": "projects", "id": r["id"], "field": "sector", "value": r["sector"],
                                       "reason": "no AP²I sector matched; kept as observation"})
        if status == "unknown" and r.get("status") and _n(r.get("status")) != "non renseigne":
            report["unmapped"].append({"table": "projects", "id": r["id"], "field": "status", "value": r["status"]})
        if not r.get("source_url"):
            db.add(DataValidation(source_record_id=sr.id, project_id=p.id, rule="legacy_without_source", severity="warning",
                                  message="Legacy project has no source URL: needs review"))

    agreement_map: dict[str, FinancingAgreement] = {}
    for r in data.get("financings", []):
        sr, _ = _record(db, conn_row, "financings", r)
        p = project_map.get(r["project_id"])
        if p is None:
            report["unmapped"].append({"table": "financings", "id": r["id"], "reason": "project not migrated"})
            continue
        ident = f"mvp:{r['id']}"
        partner = _partner(db, r["funder"])
        agr = db.scalar(select(FinancingAgreement).where(FinancingAgreement.partner_id == partner.id,
                                                         FinancingAgreement.source_identifier == ident))
        if agr is None:
            agr = FinancingAgreement(project_id=p.id, partner_id=partner.id, source_identifier=ident, name=p.title,
                                     instrument_label=r.get("instrument"), currency=r.get("currency"),
                                     amount_original=_dec(r.get("committed")),
                                     amount_label="Committed amount entered in the legacy MVP" if r.get("committed") is not None else None,
                                     source_record_id=sr.id)
            db.add(agr)
            db.flush()
            created["agreements"] += 1
            if r.get("committed") is not None and r.get("currency"):
                db.add(FinancingCommitment(agreement_id=agr.id, commitment_type="original", amount=_dec(r["committed"]), currency=r["currency"],
                                           value_date=None, transaction_key=f"{ident}:committed", source_record_id=sr.id))
                created["commitments"] += 1
        agreement_map[r["id"]] = agr
        if not db.scalar(select(ProjectSourceLink).where(ProjectSourceLink.project_id == p.id, ProjectSourceLink.source_record_id == sr.id)):
            db.add(ProjectSourceLink(project_id=p.id, source_record_id=sr.id, link_type="deterministic_match", match_rule="legacy_mvp_migration"))

    for r in data.get("disbursements", []):
        sr, _ = _record(db, conn_row, "disbursements", r)
        agr = agreement_map.get(r["financing_id"])
        if agr is None or not agr.currency:
            report["unmapped"].append({"table": "disbursements", "id": r["id"], "reason": "financing missing or without currency"})
            continue
        key = f"mvp:disb:{r['id']}"
        if not db.scalar(select(Disbursement).where(Disbursement.agreement_id == agr.id, Disbursement.transaction_key == key)):
            db.add(Disbursement(agreement_id=agr.id, flow_type="disbursement", amount=_dec(r["amount"]), currency=agr.currency, value_date=None,
                                period_year=int(r["year"]), transaction_key=key, source_record_id=sr.id))
            created["disbursements"] += 1

    for r in data.get("amendments", []):
        sr, _ = _record(db, conn_row, "amendments", r)
        p = project_map.get(r["project_id"])
        if p is None:
            report["unmapped"].append({"table": "amendments", "id": r["id"], "reason": "project not migrated"})
            continue
        if db.scalar(select(SourceObservation).where(SourceObservation.source_record_id == sr.id, SourceObservation.field == "legacy_amendment")):
            continue
        db.add(SourceObservation(source_record_id=sr.id, project_id=p.id, field="legacy_amendment", source_field="amendments",
                                 value_numeric=_dec(r.get("amount")), currency=r.get("currency"), value_date=parse_date(r.get("date")),
                                 value_text=r.get("reason")))
        created["amendment_observations"] += 1
    if data.get("amendments"):
        report["warnings"].append("MVP amendments were project-level without a contract: kept as observations "
                                  "(field legacy_amendment), not as contract amendments, to avoid inventing contracts.")

    plans: dict[int, RecoveryPlan] = {}
    for r in data.get("actions", []):
        sr, _ = _record(db, conn_row, "actions", r)
        p = project_map.get(r["project_id"])
        if p is None:
            report["unmapped"].append({"table": "actions", "id": r["id"], "reason": "project not migrated"})
            continue
        if db.scalar(select(RecoveryAction).where(RecoveryAction.evidence.cast(Text).contains(f'"source_record_id": {sr.id}'))):
            continue
        plan = plans.get(p.id) or db.scalar(select(RecoveryPlan).where(RecoveryPlan.project_id == p.id, RecoveryPlan.method == "legacy_mvp"))
        if plan is None:
            plan = RecoveryPlan(project_id=p.id, title=f"Legacy MVP actions — {p.title[:200]}", diagnosis={"origin": "legacy_mvp"},
                                status="in_progress", method="legacy_mvp")
            db.add(plan)
            db.flush()
            plans[p.id] = plan
        db.add(RecoveryAction(plan_id=plan.id, problem=r.get("problem") or "", evidence=[{"source": "legacy MVP action", "source_record_id": sr.id}],
                              contributing_factors=FURTHER, recommended_action=r.get("recommendation") or "",
                              responsible_institution=r.get("owner"), priority="not_set", origin="user", data_nature="officially_reported",
                              approval_status="approved", implementation_status=ACTION_STATUS.get(_n(r.get("status")), "not_started"),
                              due_date=parse_date(r.get("due_date"))))
        created["recovery_actions"] += 1

    db.commit()
    report["created"] = created
    return report
