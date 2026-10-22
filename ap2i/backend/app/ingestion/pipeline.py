"""Shared ingestion pipeline: persistence, provenance, validation, resolution, logging (§7, §15, §31).

    run_sync(db, "worldbank_projects", trigger="manual")

Guarantees:
  * Idempotent: a source record is stored once per (connector, identifier, SHA-256); unchanged
    records are skipped; flows are keyed by source transaction keys (unique per agreement).
  * Provenance: every master-project field set from a source also produces a SourceObservation.
  * Nothing is invented: missing values stay NULL and are reported by the data-quality engine.
  * Failures are logged on the SyncRun and the connector (last_failure_at, last_error) and raise a
    notification for administrators.
"""

from __future__ import annotations

import logging
import re
import traceback
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.connectors.base import Connector, ConnectorError, NormalizedAgreement, NormalizedRecord, RawRecord, SyncParams
from app.connectors.registry import get_connector
from app.ingestion import resolution
from app.models import (
    AdminRegion,
    Country,
    DataValidation,
    Disbursement,
    Document,
    FinancingAgreement,
    FinancingCommitment,
    FinancingInstrument,
    FinancingPartner,
    IdSequence,
    Notification,
    Project,
    ProjectAlias,
    ProjectLocation,
    ProjectSourceLink,
    ProjectStatusHistory,
    ResultsIndicator,
    ResultsObservation,
    Sector,
    SourceConnector,
    SourceObservation,
    SourceRecord,
    SyncRun,
)
from app.assistant.safety import scan_for_injection

log = logging.getLogger("ap2i.ingestion")

KNOWN_CURRENCIES = {"XAF", "XOF", "USD", "EUR", "GBP", "XDR", "JPY", "CHF", "CNY", "SAR", "KWD", "AED", "CAD", "SEK",
                    "NOK", "DKK", "ZAR", "NGN", "KES", "GHS", "MAD", "EGP"}

# Which kind of evidence owns the "counted" commitments of an agreement (higher wins).
COMMITMENT_PRECEDENCE = {"iati_activity": 2, "wb_project": 1, "upload_project_row": 3}


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class RunStats:
    retrieved: int = 0
    new: int = 0
    unchanged: int = 0
    imported: int = 0
    review: int = 0
    failed: int = 0
    errors: list[dict] = field(default_factory=list)
    created_projects: list[int] = field(default_factory=list)
    log_lines: list[str] = field(default_factory=list)


def scheme_for(connector_key: str, record_type: str) -> str:
    if record_type == "wb_project":
        return "wb"
    if record_type == "iati_activity":
        return "iati"
    if record_type.startswith("upload"):
        return "upload"
    return connector_key


def mint_ap2i_id(db: Session, iso3: str, sector_code: str | None) -> str:
    seq = db.get(IdSequence, iso3, with_for_update=True)
    if seq is None:
        seq = IdSequence(key=iso3, value=0)
        db.add(seq)
        db.flush()
    seq.value += 1
    db.flush()
    return f"AP2I-{iso3}-{(sector_code or 'UNCLASSIFIED')}-{seq.value:06d}"


class Pipeline:
    def __init__(self, db: Session, connector_row: SourceConnector, connector: Connector, run: SyncRun):
        self.db = db
        self.row = connector_row
        self.connector = connector
        self.run = run
        self.stats = RunStats()
        self._countries = {c.iso3: c for c in db.scalars(select(Country))}
        self._sectors = {s.code: s for s in db.scalars(select(Sector))}
        self._instruments = {i.code: i for i in db.scalars(select(FinancingInstrument))}
        self._partners = {p.code: p for p in db.scalars(select(FinancingPartner))}
        self.settings = get_settings()

    # -- raw record persistence ---------------------------------------------------------------
    def store_raw(self, raw: RawRecord, tenant_id: int | None = None) -> tuple[SourceRecord, bool]:
        sha = raw.sha256
        existing = self.db.scalar(select(SourceRecord).where(
            SourceRecord.connector_id == self.row.id, SourceRecord.source_identifier == raw.source_identifier,
            SourceRecord.payload_sha256 == sha))
        if existing is not None:
            return existing, False
        prev = self.db.scalars(select(SourceRecord).where(
            SourceRecord.connector_id == self.row.id, SourceRecord.source_identifier == raw.source_identifier,
            SourceRecord.is_latest.is_(True))).all()
        for p in prev:
            p.is_latest = False
        rec = SourceRecord(
            connector_id=self.row.id, sync_run_id=self.run.id, source_identifier=raw.source_identifier,
            record_type=raw.record_type, country_iso3=raw.country_iso3, payload=raw.payload,
            payload_format=raw.payload_format, raw_text=raw.raw_text, payload_sha256=sha, source_url=raw.source_url,
            source_last_updated=raw.source_last_updated, tenant_id=tenant_id,
        )
        self.db.add(rec)
        self.db.flush()
        return rec, True

    # -- validation -------------------------------------------------------------------------
    def validate(self, rec: NormalizedRecord, src: SourceRecord) -> list[DataValidation]:
        issues: list[tuple[str, str, str]] = []
        if not rec.title or rec.title.strip() == "":
            issues.append(("title_required", "error", "Project title missing"))
        if rec.country_iso3 not in self._countries:
            issues.append(("country_unknown", "error", f"Unknown country {rec.country_iso3}"))
        if rec.start_date and rec.planned_end_date and rec.planned_end_date < rec.start_date:
            issues.append(("dates_inconsistent", "warning", f"Planned end {rec.planned_end_date} before start {rec.start_date}"))
        if rec.approval_date and rec.approval_date > date.today().replace(year=date.today().year + 1):
            issues.append(("approval_in_future", "warning", f"Approval date {rec.approval_date} is in the future"))
        if rec.sector_code and rec.sector_code not in self._sectors:
            issues.append(("sector_unknown", "warning", f"Sector code {rec.sector_code} not in AP²I sector list"))
        if rec.sector_code is None:
            issues.append(("sector_unmapped", "info", f"No AP²I sector could be mapped (source: {rec.sector_label})"))
        for agr in rec.agreements:
            if agr.currency and agr.currency not in KNOWN_CURRENCIES and len(agr.currency) != 3:
                issues.append(("currency_invalid", "error", f"Invalid currency {agr.currency}"))
            if agr.amount_original is not None and agr.amount_original < 0:
                issues.append(("amount_negative", "error", f"Negative original amount {agr.amount_original}"))
            if agr.amount_original is not None and not agr.currency:
                issues.append(("amount_without_currency", "error", "Amount without currency"))
            for m in agr.flows:
                if m.amount < 0:
                    issues.append(("negative_flow", "warning", f"Negative {m.kind} {m.amount} {m.currency} ({m.label})"))
        for w in rec.warnings:
            issues.append(("source_warning", "info", w))
        flags = scan_for_injection(" ".join(filter(None, [rec.title, rec.description, rec.objectives])))
        if flags:
            issues.append(("prompt_injection_pattern", "warning",
                           f"Text contains instruction-like patterns {flags}; treated as data only"))
        out = []
        for rule, sev, msg in issues:
            dv = DataValidation(source_record_id=src.id, rule=rule, severity=sev, message=msg)
            self.db.add(dv)
            out.append(dv)
        return out

    # -- partner / instrument -------------------------------------------------------------------
    def partner(self, code: str) -> FinancingPartner:
        p = self._partners.get(code)
        if p is None:
            # Unknown IATI publisher: register it, clearly labelled as auto-registered.
            ref = code.split(":", 1)[1] if code.startswith("IATI:") else code
            p = FinancingPartner(code=code[:40], name=f"IATI publisher {ref}", short_name=ref[:40],
                                 partner_type="unknown", tier=3, iati_org_refs=[ref],
                                 notes="Auto-registered from an IATI reporting-org reference; to be reviewed.")
            self.db.add(p)
            self.db.flush()
            self._partners[code] = p
        return p

    # -- master project --------------------------------------------------------------------------
    def observe(self, src: SourceRecord, project_id: int | None, fieldname: str, source_field: str | None, value,
                currency: str | None = None) -> None:
        obs = SourceObservation(source_record_id=src.id, project_id=project_id, field=fieldname, source_field=source_field,
                                reporting_date=_reporting_date(src))
        if isinstance(value, Decimal):
            obs.value_numeric = value
            obs.currency = currency
        elif isinstance(value, date):
            obs.value_date = value
        elif value is not None:
            obs.value_text = str(value)[:20000]
        else:
            obs.data_nature = "missing"
        self.db.add(obs)

    def resolve_project(self, rec: NormalizedRecord, src: SourceRecord, tenant_id: int | None) -> tuple[Project, str, str | None, bool]:
        """Return (project, link_type, rule, created)."""
        scheme = scheme_for(self.row.key, src.record_type)
        own_ids = [src.source_identifier] + rec.equivalent_identifiers
        project = resolution.find_by_identifiers(self.db, own_ids)
        if project is not None:
            return project, "deterministic_match", "same_or_equivalent_identifier", False
        if rec.parent_identifier:
            parent = resolution.find_by_identifiers(self.db, [rec.parent_identifier])
            if parent is not None:
                return parent, "deterministic_match", "official_parent_link", False
        country = self._countries[rec.country_iso3]
        sector = self._sectors.get(rec.sector_code or "")
        project = Project(
            ap2i_id=mint_ap2i_id(self.db, country.iso3, sector.code if sector else None),
            country_id=country.id, tenant_id=tenant_id, title=rec.title, title_language=rec.title_language,
            sector_id=sector.id if sector else None, status=rec.status or "unknown", status_source=self.row.key,
            data_nature="officially_reported", verification_status="unverified",
            funding_type="externally_funded" if rec.agreements and all(a.partner_code != "GOV" for a in rec.agreements) else "unknown",
        )
        self.db.add(project)
        self.db.flush()
        self.stats.created_projects.append(project.id)
        if rec.parent_identifier:
            self.db.add(DataValidation(source_record_id=src.id, project_id=project.id, rule="parent_not_found",
                                       severity="info",
                                       message=f"Declared parent {rec.parent_identifier} not imported yet; created as its own project"))
        return project, "primary", None, True

    def apply_fields(self, project: Project, rec: NormalizedRecord, src: SourceRecord, is_primary: bool) -> None:
        """Primary source sets fields; secondary sources only fill gaps. Every value is observed."""
        mapping = [
            ("title", "title", rec.title), ("description", "description", rec.description),
            ("objectives", "objectives", rec.objectives), ("executing_agency", "executing_agency", rec.executing_agency),
            ("implementing_agency", "implementing_agency", rec.implementing_agency),
            ("original_approval_date", "approval_date", rec.approval_date),
            ("implementation_start_date", "start_date", rec.start_date),
            ("original_completion_date", "planned_end_date", rec.planned_end_date),
            ("actual_completion_date", "actual_end_date", rec.actual_end_date),
            ("original_estimated_cost", "original_cost", rec.original_cost),
            ("cost_currency", "cost_currency", rec.cost_currency),
        ]
        for attr, label, value in mapping:
            if value is None:
                continue
            current = getattr(project, attr)
            if is_primary or current is None:
                if attr == "title" and not is_primary:
                    continue
                setattr(project, attr, value)
            self.observe(src, project.id, attr, label, value, currency=rec.cost_currency if attr == "original_estimated_cost" else None)
        if rec.sector_code and (is_primary or project.sector_id is None):
            sector = self._sectors.get(rec.sector_code)
            if sector:
                project.sector_id = sector.id
        if rec.sector_label:
            self.observe(src, project.id, "sector_source_label", "sector", rec.sector_label)
        if is_primary and rec.status and rec.status != project.status:
            self.db.add(ProjectStatusHistory(project_id=project.id, status=rec.status, previous_status=project.status,
                                             effective_date=None, source_record_id=src.id,
                                             note=f"Status reported by {self.row.key}: {rec.status_label}"))
            project.status = rec.status
            project.status_source = self.row.key
        elif is_primary and rec.status and not self.db.scalar(select(func.count(ProjectStatusHistory.id)).where(
                ProjectStatusHistory.project_id == project.id)):
            self.db.add(ProjectStatusHistory(project_id=project.id, status=rec.status, previous_status=None,
                                             source_record_id=src.id, note=f"Initial status from {self.row.key}: {rec.status_label}"))
        if rec.status_label:
            self.observe(src, project.id, "status_source_label", "status", rec.status_label)
        for fname, sfield, value in rec.observations:
            self.observe(src, project.id, fname, sfield, value)
            if fname == "physical_progress_pct" and isinstance(value, Decimal) and (is_primary or project.physical_progress_pct is None):
                project.physical_progress_pct = value
            if fname == "physical_progress_date" and isinstance(value, date):
                project.physical_progress_date = value
            if fname == "operational_status" and value and (is_primary or project.operational_status == "unknown"):
                project.operational_status = str(value)
            if fname == "revised_estimated_cost" and isinstance(value, Decimal):
                project.revised_estimated_cost = value
        for alt, lang in rec.alt_titles + ([(rec.title, rec.title_language)] if rec.title != project.title else []):
            if alt and alt != project.title and not self.db.scalar(select(ProjectAlias).where(
                    ProjectAlias.project_id == project.id, ProjectAlias.alias == alt)):
                self.db.add(ProjectAlias(project_id=project.id, alias=alt, language=lang, source_record_id=src.id))
        project.last_source_update_at = utcnow()
        self.db.flush()

    # -- agreements and flows --------------------------------------------------------------------
    def apply_agreement(self, project: Project, agr: NormalizedAgreement, src: SourceRecord, equivalent_ids: list[str],
                        tenant_id: int | None) -> FinancingAgreement:
        partner = self.partner(agr.partner_code)
        candidates = [agr.source_identifier] + [e for e in equivalent_ids if e]
        existing = self.db.scalar(select(FinancingAgreement).where(
            FinancingAgreement.partner_id == partner.id, FinancingAgreement.source_identifier.in_(candidates)))
        if existing is None:
            existing = FinancingAgreement(project_id=project.id, partner_id=partner.id, source_identifier=agr.source_identifier,
                                          tenant_id=tenant_id, source_record_id=src.id)
            self.db.add(existing)
            is_owner = True
        else:
            is_owner = existing.source_identifier == agr.source_identifier
            if existing.project_id != project.id and is_owner:
                existing.project_id = project.id
        fill = is_owner
        def setv(attr, value):
            if value is not None and (fill or getattr(existing, attr) is None):
                setattr(existing, attr, value)
        setv("name", agr.name)
        setv("instrument_label", agr.instrument_label)
        if agr.instrument_code and agr.instrument_code in self._instruments:
            setv("instrument_id", self._instruments[agr.instrument_code].id)
        for attr in ("approval_date", "signature_date", "effectiveness_date", "closing_date_original", "closing_date_current",
                     "currency", "amount_original", "amount_label", "parent_source_identifier"):
            setv(attr, getattr(agr, attr))
        if agr.status and agr.status != "unknown" and fill:
            existing.status = agr.status
        if agr.reported_cumulative_disbursed is not None or agr.reported_current_commitment is not None:
            existing.reported_current_commitment = agr.reported_current_commitment
            existing.reported_cumulative_disbursed = agr.reported_cumulative_disbursed
            existing.reported_undisbursed = agr.reported_undisbursed
            existing.reported_cumulative_as_of = agr.reported_cumulative_as_of
            existing.reported_cumulative_label = agr.reported_cumulative_label
            self.observe(src, project.id, "cumulative_disbursed", "disbursement", agr.reported_cumulative_disbursed,
                         currency=agr.currency)
        if agr.amount_original is not None:
            self.observe(src, project.id, "financing_amount_original", agr.amount_label, agr.amount_original, agr.currency)
        self.db.flush()

        # Commitments: count only the highest-precedence source for this agreement.
        if agr.commitments:
            new_rank = COMMITMENT_PRECEDENCE.get(src.record_type, 0)
            current = self.db.scalars(select(FinancingCommitment).where(
                FinancingCommitment.agreement_id == existing.id, FinancingCommitment.is_counted.is_(True))).all()
            current_rank = max((COMMITMENT_PRECEDENCE.get(_record_type(self.db, c.source_record_id), 0) for c in current),
                               default=-1)
            counted = new_rank >= current_rank
            if counted and current and new_rank > current_rank:
                for c in current:
                    if c.source_record_id != src.id:
                        c.is_counted = False
                        c.counting_note = f"Superseded by transaction-level data from source record {src.id}"
            for m in agr.commitments:
                row = self.db.scalar(select(FinancingCommitment).where(
                    FinancingCommitment.agreement_id == existing.id, FinancingCommitment.transaction_key == m.transaction_key))
                if row is None:
                    self.db.add(FinancingCommitment(
                        agreement_id=existing.id, commitment_type=m.kind, amount=m.amount, currency=m.currency,
                        value_date=m.value_date, transaction_key=m.transaction_key, source_record_id=src.id,
                        is_counted=counted,
                        counting_note=None if counted else "Not counted: a higher-precedence source reports this agreement's commitments",
                    ))
                else:
                    row.amount, row.currency, row.value_date, row.source_record_id = m.amount, m.currency, m.value_date, src.id
        for m in agr.flows:
            row = self.db.scalar(select(Disbursement).where(
                Disbursement.agreement_id == existing.id, Disbursement.transaction_key == m.transaction_key))
            if row is None:
                self.db.add(Disbursement(agreement_id=existing.id, flow_type=m.kind, amount=m.amount, currency=m.currency,
                                         value_date=m.value_date, transaction_key=m.transaction_key, source_record_id=src.id))
            else:
                row.amount, row.currency, row.value_date, row.source_record_id = m.amount, m.currency, m.value_date, src.id
        self.db.flush()
        return existing

    # -- attachments -------------------------------------------------------------------------------
    def apply_attachments(self, project: Project, rec: NormalizedRecord, src: SourceRecord, tenant_id: int | None) -> None:
        for d in rec.documents:
            if not d.get("url"):
                continue
            if self.db.scalar(select(Document).where(Document.project_id == project.id, Document.url == d["url"])):
                continue
            self.db.add(Document(project_id=project.id, tenant_id=tenant_id, title=d.get("title") or d["url"],
                                 doc_type=d.get("doc_type"), url=d["url"], language=d.get("language"),
                                 published_date=d.get("date"), source_record_id=src.id))
        regions = None
        for loc in rec.locations:
            lat, lon = loc.get("lat"), loc.get("lon")
            if lat is not None and not (Decimal(-90) <= lat <= Decimal(90)):
                lat = None
            if lon is not None and not (Decimal(-180) <= lon <= Decimal(180)):
                lon = None
            if self.db.scalar(select(ProjectLocation).where(
                    ProjectLocation.project_id == project.id, ProjectLocation.place_name == loc.get("name"),
                    ProjectLocation.latitude == lat, ProjectLocation.longitude == lon)):
                continue
            region_id = None
            if loc.get("name"):
                if regions is None:
                    regions = self.db.scalars(select(AdminRegion).where(AdminRegion.country_id == project.country_id)).all()
                region_id = _match_region(loc["name"], regions)
            self.db.add(ProjectLocation(project_id=project.id, place_name=loc.get("name"), latitude=lat, longitude=lon,
                                        precision=loc.get("precision"), region_id=region_id, source_record_id=src.id))
            if region_id and project.region_id is None:
                project.region_id = region_id
        for r in rec.results:
            if not r.get("title"):
                continue
            ind = self.db.scalar(select(ResultsIndicator).where(ResultsIndicator.project_id == project.id,
                                                                ResultsIndicator.name == r["title"][:5000]))
            if ind is None:
                ind = ResultsIndicator(project_id=project.id, name=r["title"][:5000], measure=r.get("measure"),
                                       baseline_value=r.get("baseline"), target_value=r.get("target"), source_record_id=src.id)
                self.db.add(ind)
                self.db.flush()
            if r.get("actual") is not None:
                if not self.db.scalar(select(ResultsObservation).where(
                        ResultsObservation.indicator_id == ind.id, ResultsObservation.value == r["actual"],
                        ResultsObservation.period_end == r.get("actual_date"))):
                    self.db.add(ResultsObservation(indicator_id=ind.id, value=r["actual"], period_end=r.get("actual_date"),
                                                   source_record_id=src.id))

    # -- one record ---------------------------------------------------------------------------------
    def process(self, rec: NormalizedRecord, src: SourceRecord, tenant_id: int | None = None) -> str:
        issues = self.validate(rec, src)
        if any(i.severity == "error" for i in issues):
            src.processing_status = "review"
            src.processing_note = "; ".join(i.message for i in issues if i.severity == "error")
            return "review"
        project, link_type, rule, created = self.resolve_project(rec, src, tenant_id)
        is_primary = created or self.db.scalar(select(ProjectSourceLink).where(
            ProjectSourceLink.project_id == project.id, ProjectSourceLink.link_type == "primary",
            ProjectSourceLink.source_record_id.in_(select(SourceRecord.id).where(
                SourceRecord.connector_id == self.row.id, SourceRecord.source_identifier == src.source_identifier)))) is not None
        if rule == "official_parent_link":
            is_primary = False
        self.apply_fields(project, rec, src, is_primary)
        scheme = scheme_for(self.row.key, src.record_type)
        resolution.register_identifier(self.db, project.id, scheme, src.source_identifier, src.id)
        if rule != "official_parent_link":
            for eq in rec.equivalent_identifiers:
                resolution.register_identifier(self.db, project.id, "wb" if eq.startswith("P") else scheme, eq, src.id)
        if not self.db.scalar(select(ProjectSourceLink).where(ProjectSourceLink.project_id == project.id,
                                                              ProjectSourceLink.source_record_id == src.id)):
            self.db.add(ProjectSourceLink(project_id=project.id, source_record_id=src.id,
                                          link_type="primary" if is_primary else link_type, match_rule=rule, match_score=1.0))
        for agr in rec.agreements:
            self.apply_agreement(project, agr, src, rec.equivalent_identifiers, tenant_id)
        self.apply_attachments(project, rec, src, tenant_id)
        for i in issues:
            i.project_id = project.id
        if project.verification_status == "verified":
            project.verification_status = "needs_review"  # new source information after verification
        src.processing_status = "imported"
        src.processing_note = f"{link_type}{' (' + rule + ')' if rule else ''} -> {project.ap2i_id}"
        return "imported"


def _record_type(db: Session, source_record_id: int | None) -> str:
    if source_record_id is None:
        return ""
    return db.scalar(select(SourceRecord.record_type).where(SourceRecord.id == source_record_id)) or ""


def _reporting_date(src: SourceRecord) -> date | None:
    from app.connectors.base import parse_date

    return parse_date(src.source_last_updated) if src.source_last_updated else None


def _match_region(name: str, regions) -> int | None:
    import unicodedata

    def norm(s: str) -> str:
        return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

    n = norm(name)
    for r in regions:
        for label in (r.name_en, r.name_fr):
            ln = norm(label)
            if re.search(rf"\b{re.escape(ln)}\b", n) and len(ln) > 3:
                # "Nord" must not match "Nord-Ouest": prefer the longest matching label
                longer = [x for x in regions if x is not r and ln in norm(x.name_fr) and re.search(rf"\b{re.escape(norm(x.name_fr))}\b", n)]
                return (longer[0] if longer else r).id
    return None


def run_sync(db: Session, connector_key: str, trigger: str = "manual", params: SyncParams | None = None,
             connector: Connector | None = None, tenant_id: int | None = None, force: bool = False) -> SyncRun:
    row = db.scalar(select(SourceConnector).where(SourceConnector.key == connector_key))
    if row is None:
        raise ConnectorError(f"Connector {connector_key} is not registered (run the reference seed)")
    if not row.enabled and not force and trigger == "scheduled":
        raise ConnectorError(f"Connector {connector_key} is disabled")
    cfg = dict(row.config or {})
    params = params or SyncParams(countries=cfg.get("countries") or list(get_settings().active_countries),
                                  date_from=_d(cfg.get("date_from")), date_to=_d(cfg.get("date_to")),
                                  limit=cfg.get("limit"), cursor=row.cursor or {})
    connector = connector or get_connector(connector_key, cfg)
    if get_settings().is_production and cfg.get("synthetic"):
        raise ConnectorError("Synthetic connectors are refused in production")
    run = SyncRun(connector_id=row.id, trigger=trigger, params={
        "countries": params.countries, "date_from": str(params.date_from) if params.date_from else None,
        "date_to": str(params.date_to) if params.date_to else None, "limit": params.limit,
    })
    db.add(run)
    db.commit()
    pipe = Pipeline(db, row, connector, run)
    st = pipe.stats
    staged: list[tuple[NormalizedRecord, SourceRecord]] = []
    fatal: str | None = None
    try:
        for raw in connector.fetch(params):
            st.retrieved += 1
            try:
                with db.begin_nested():
                    src, is_new = pipe.store_raw(raw, tenant_id)
            except Exception as exc:  # noqa: BLE001 — one bad record must not stop the run
                st.failed += 1
                st.errors.append({"record": raw.source_identifier, "stage": "store", "error": str(exc)[:500]})
                continue
            if not is_new and src.processing_status in ("imported", "skipped"):
                st.unchanged += 1
                continue
            st.new += int(is_new)
            try:
                norm = connector.normalize(raw)
            except Exception as exc:  # noqa: BLE001
                src.processing_status = "failed"
                src.processing_note = f"normalize: {exc}"[:2000]
                st.failed += 1
                st.errors.append({"record": raw.source_identifier, "stage": "normalize", "error": str(exc)[:500]})
                continue
            if norm is None:
                src.processing_status = "skipped"
                continue
            staged.append((norm, src))
        db.commit()
    except ConnectorError as exc:
        fatal = str(exc)
    except Exception as exc:  # noqa: BLE001
        fatal = f"{type(exc).__name__}: {exc}"
        st.log_lines.append(traceback.format_exc()[-4000:])

    # Parents first, so children and Additional Financing attach deterministically.
    staged.sort(key=lambda t: (t[0].parent_identifier is not None,))
    for norm, src in staged:
        try:
            with db.begin_nested():
                outcome = pipe.process(norm, src, tenant_id)
            if outcome == "imported":
                st.imported += 1
            else:
                st.review += 1
        except Exception as exc:  # noqa: BLE001 — the savepoint was rolled back; keep going
            src.processing_status = "failed"
            src.processing_note = f"process: {exc}"[:2000]
            st.failed += 1
            st.errors.append({"record": src.source_identifier, "stage": "process", "error": str(exc)[:500]})
            log.exception("process failed for %s", src.source_identifier)
    db.commit()

    candidates = 0
    if st.created_projects:
        candidates = resolution.generate_candidates(db, st.created_projects)
        st.review += candidates
        db.commit()

    run = db.get(SyncRun, run.id)
    row = db.get(SourceConnector, row.id)
    run.finished_at = utcnow()
    run.records_retrieved, run.records_new, run.records_unchanged = st.retrieved, st.new, st.unchanged
    run.records_imported, run.records_review, run.records_failed = st.imported, st.review, st.failed
    run.errors = st.errors[:200]
    st.log_lines.insert(0, f"retrieved={st.retrieved} new={st.new} unchanged={st.unchanged} imported={st.imported} "
                           f"review={st.review} failed={st.failed} new_projects={len(st.created_projects)} "
                           f"match_candidates={candidates}")
    if fatal:
        st.log_lines.append(f"FATAL: {fatal}")
    run.log = "\n".join(st.log_lines)
    if fatal and st.retrieved == 0:
        run.status = "failed"
    elif fatal or st.failed:
        run.status = "partial"
    else:
        run.status = "success"
    if run.status == "failed":
        row.last_failure_at = utcnow()
        row.last_error = fatal
        if row.status == "not_tested":
            row.status = "blocked"
        db.add(Notification(kind="sync_failed", title=f"Synchronisation failed: {row.key}", body=fatal,
                            link=f"/admin/connectors/{row.key}"))
    else:
        row.last_success_at = utcnow()
        if fatal:
            row.last_failure_at = utcnow()
            row.last_error = fatal
        persisted = db.scalar(select(func.count(SourceRecord.id)).where(SourceRecord.connector_id == row.id,
                                                                        SourceRecord.processing_status == "imported"))
        if persisted and row.key != "manual_upload":
            row.status = "operational" if run.status == "success" else "partial"
            row.status_evidence = (f"Run #{run.id} ({run.finished_at:%Y-%m-%d %H:%M} UTC): {st.retrieved} real records "
                                   f"retrieved, {st.imported} imported; {persisted} records persisted in total.")
        if st.retrieved and st.imported:
            cursor = dict(row.cursor or {})
            cursor["last_run_id"] = run.id
            cursor["last_success"] = utcnow().isoformat()
            row.cursor = cursor
    db.commit()
    return run


def _d(v) -> date | None:
    if not v:
        return None
    return v if isinstance(v, date) else date.fromisoformat(str(v))
