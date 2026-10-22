"""Load reference data (idempotent). Never loads project data: projects come only from connectors.

    python -m app.reference.seed
"""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.connectors.registry import CONNECTORS, DEFAULT_ENABLED
from app.models import (
    AdminRegion,
    AlertThreshold,
    Country,
    CountryDataSource,
    FinancingInstrument,
    FinancingPartner,
    Plan,
    RoleDef,
    Sector,
    SectorIndicator,
    SourceConnector,
)
from app.reference.catalog import DONORS, INSTRUMENTS, PLANS, ROLES, SECTOR_INDICATORS, SECTORS
from app.reference.countries import ADMIN_DIVISIONS, COUNTRIES, COUNTRY_SOURCES

REFERENCE_NOTE = (
    "Compiled reference data (ISO codes, names, AU region, UN M49 sub-region, ISO 4217 currency, main official "
    "languages). Not yet verified against an official register; see app/reference/countries.py."
)

# Default early-warning thresholds (Master prompt §20). Institutions may override per organization.
DEFAULT_THRESHOLDS = [
    ("LOW_DISBURSEMENT", "max_disbursement_ratio", Decimal("0.30")),
    ("LOW_DISBURSEMENT", "min_elapsed_ratio", Decimal("0.50")),
    ("CLOSING_DATE_PASSED", "grace_days", Decimal("0")),
    ("SCHEDULE_EXTENSION", "min_extension_months", Decimal("12")),
    ("COST_REVISION", "max_ratio", Decimal("1.20")),
    ("REPEATED_AMENDMENTS", "min_count", Decimal("3")),
    ("PHYS_FIN_GAP", "max_gap_points", Decimal("25")),
    ("MISSING_PROGRESS_REPORT", "max_age_months", Decimal("12")),
    ("CANCELLATION", "min_cancelled_ratio", Decimal("0.20")),
    ("FINANCING_GAP", "min_gap_ratio", Decimal("0.05")),
]


def seed_reference(db: Session) -> dict:
    settings = get_settings()
    counts: dict[str, int] = {}

    existing = {c.iso3: c for c in db.scalars(select(Country))}
    for c in COUNTRIES:
        row = existing.get(c.iso3)
        if row is None:
            row = Country(iso3=c.iso3)
            db.add(row)
        row.iso2, row.iso_numeric, row.name_en, row.name_fr = c.iso2, c.numeric, c.name_en, c.name_fr
        row.region, row.subregion, row.currency = c.region, c.subregion, c.currency
        row.official_languages = list(c.languages)
        row.is_active = c.iso3 in settings.active_countries
        row.reference_status = "unverified"
        row.reference_note = REFERENCE_NOTE
        row.reporting_config = row.reporting_config or {"fiscal_year": "calendar", "reporting_currency": c.currency}
    db.flush()
    counts["countries"] = len(COUNTRIES)

    by_iso3 = {c.iso3: c for c in db.scalars(select(Country))}
    for iso3, divisions in ADMIN_DIVISIONS.items():
        country = by_iso3[iso3]
        have = {r.code for r in db.scalars(select(AdminRegion).where(AdminRegion.country_id == country.id))}
        for code, en, fr in divisions:
            if code not in have:
                db.add(AdminRegion(country_id=country.id, code=code, name_en=en, name_fr=fr, level=1, division_type="region"))
    for iso3, sources in COUNTRY_SOURCES.items():
        country = by_iso3[iso3]
        have = {(s.institution, s.name) for s in db.scalars(select(CountryDataSource).where(CountryDataSource.country_id == country.id))}
        for s in sources:
            if (s["institution"], s["name"]) not in have:
                db.add(CountryDataSource(country_id=country.id, **s))

    sectors = {s.code: s for s in db.scalars(select(Sector))}
    for i, (code, en, fr) in enumerate(SECTORS):
        if code not in sectors:
            sectors[code] = Sector(code=code, name_en=en, name_fr=fr, sort_order=i)
            db.add(sectors[code])
    db.flush()
    have_ind = {(i.sector_id, i.code) for i in db.scalars(select(SectorIndicator))}
    for sec, code, en, fr, unit, kind in SECTOR_INDICATORS:
        sid = sectors[sec].id
        if (sid, code) not in have_ind:
            db.add(SectorIndicator(sector_id=sid, code=code, name_en=en, name_fr=fr, unit=unit, kind=kind))

    have_instr = {i.code for i in db.scalars(select(FinancingInstrument))}
    for code, en, fr in INSTRUMENTS:
        if code not in have_instr:
            db.add(FinancingInstrument(code=code, name_en=en, name_fr=fr))

    partners = {p.code: p for p in db.scalars(select(FinancingPartner))}
    for d in DONORS:
        p = partners.get(d["code"])
        if p is None:
            p = FinancingPartner(code=d["code"])
            db.add(p)
            partners[d["code"]] = p
        p.name, p.short_name, p.partner_type, p.tier = d["name"], d["short_name"], d["partner_type"], d["tier"]
        p.iati_org_refs, p.connector_key, p.website, p.notes = d["iati_org_refs"], d["connector_key"], d.get("website"), d.get("notes")
    db.flush()

    connectors = {c.key: c for c in db.scalars(select(SourceConnector))}
    for key, cls in CONNECTORS.items():
        row = connectors.get(key)
        if row is None:
            row = SourceConnector(key=key, enabled=key in DEFAULT_ENABLED,
                                  status="not_implemented" if not cls.implemented else ("manual" if key == "manual_upload" else "not_tested"),
                                  config={"countries": list(settings.active_countries)},
                                  schedule_cron=cls.default_schedule)
            db.add(row)
        row.name, row.tier, row.access_method = cls.name, cls.tier, cls.access_method
        row.base_url, row.documentation_url = cls.base_url, cls.documentation_url
        row.usage_terms, row.update_frequency = cls.usage_terms, cls.update_frequency
        row.partner_id = partners[cls.partner_code].id if cls.partner_code in partners else None
        if not cls.implemented:
            row.status, row.enabled = "not_implemented", False
            if key in ("afdb_portal", "afd_opendata"):
                row.status = "blocked"
            row.status_evidence = cls.usage_terms

    have_roles = {r.code: r for r in db.scalars(select(RoleDef))}
    for code, en, fr, perms in ROLES:
        r = have_roles.get(code) or RoleDef(code=code)
        r.name_en, r.name_fr, r.permissions = en, fr, perms
        db.add(r)

    have_plans = {p.code: p for p in db.scalars(select(Plan))}
    for pl in PLANS:
        p = have_plans.get(pl["code"])
        if p is None:
            p = Plan(code=pl["code"], price_amount=pl["price_amount"], price_currency=pl["price_currency"])
            db.add(p)
        p.name_en, p.name_fr, p.billing_period = pl["name_en"], pl["name_fr"], pl["billing_period"]
        p.features, p.sort_order = pl["features"], pl["sort_order"]

    have_thr = {(t.rule_code, t.parameter) for t in db.scalars(select(AlertThreshold).where(AlertThreshold.organization_id.is_(None)))}
    for rule, param, value in DEFAULT_THRESHOLDS:
        if (rule, param) not in have_thr:
            db.add(AlertThreshold(organization_id=None, rule_code=rule, parameter=param, value=value))

    db.commit()
    counts["connectors"] = len(CONNECTORS)
    counts["donors"] = len(DONORS)
    return counts


def sync_active_countries(db: Session) -> list[str]:
    """Mirror AP2I_ACTIVE_COUNTRIES into the countries table. Activation is configuration only."""
    active = set(get_settings().active_countries)
    for c in db.scalars(select(Country)):
        c.is_active = c.iso3 in active
    for conn in db.scalars(select(SourceConnector)):
        cfg = dict(conn.config or {})
        if cfg.get("follow_active_countries", True):
            cfg["countries"] = sorted(active)
            conn.config = cfg
    db.commit()
    return sorted(active)


if __name__ == "__main__":
    from app.db import SessionLocal

    with SessionLocal() as s:
        print(seed_reference(s))
