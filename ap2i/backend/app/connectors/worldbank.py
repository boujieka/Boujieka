"""World Bank Projects API connector (Master prompt §9).

Source: World Bank Projects & Operations search API (public, no key)
  https://search.worldbank.org/api/v2/projects?format=json&countrycode_exact=CM
Documentation: https://projects.worldbank.org/en/projects-operations/project-search (API page:
  https://documents.worldbank.org/en/publication/documents-reports/api — same search service family).
Terms: World Bank data is published under the World Bank Terms of Use for Datasets (CC BY 4.0 for
  most datasets); attribution is kept with every record.

What the API publishes (verified 2026-10-22 on Cameroon records) and how AP²I uses it:
  * totalamt (US$)           -> agreement.amount_original, labelled "WB totalamt (IBRD+IDA commitment)"
  * commitment/disbursement/available (US$ millions, 2 decimals, per loan, cumulative at retrieval)
                             -> agreement.reported_* cumulative fields, as_of = retrieval date
  * boardapprovaldate, closingdate (current closing date, not necessarily the original one)
  * parentprojid             -> deterministic link: an Additional Financing belongs to its parent
  * fincrname/fincr_usd_amt  -> financing plan lines (e.g. Borrower/Recipient counterpart)
  NOT available and therefore never inferred: annual disbursement series by transaction type,
  original closing date, physical progress. The per-year `amount` arrays are published without a
  transaction-type label, so they are stored as raw provenance only and NOT used as flows.

Incremental updates: the API offers no reliable "modified since" filter for this query, so each run
re-reads the country list (one or two pages) and the pipeline skips records whose SHA-256 is
unchanged. That is cheap (≈160 records for Cameroon) and exact.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone
from decimal import Decimal

from app.connectors.base import (
    Connector,
    Money,
    NormalizedAgreement,
    NormalizedRecord,
    RawRecord,
    SyncParams,
    parse_date,
    parse_decimal,
)
from app.reference.catalog import WB_LENDING_INSTRUMENT_TO_INSTRUMENT, WB_MAJOR_SECTOR_TO_SECTOR
from app.reference.countries import BY_ISO3

FIELDS = (
    "id,project_name,status,boardapprovaldate,closingdate,countrycode,countryshortname,totalamt,"
    "grantamt,ibrdcommamt,idacommamt,curr_total_commitment,curr_project_cost,lendprojectcost,"
    "lendinginstr,impagency,borrower,pdo,project_abstract,sector,mjsector_namecode,commitment,"
    "disbursement,available,loantypedesc,financier_loan,fincrname,fincr_usd_amt,fincr_curr_amt,"
    "fincr_curr_id,supplementprojectflg,parentprojid,url,locations,projectdocs,p2a_updated_date,"
    "proj_last_upd_date,last_stage_reached_name,approvalfy"
)

STATUS_MAP = {"active": "active", "closed": "closed", "dropped": "dropped", "pipeline": "pipeline"}


def _first(v):
    if isinstance(v, list):
        return v[0] if v else None
    return v


def _text(v) -> str | None:
    if v is None:
        return None
    if isinstance(v, dict):
        v = v.get("cdata!") or v.get("cdata") or next(iter(v.values()), None)
    if isinstance(v, list):
        v = " ".join(str(x) for x in v if x)
    s = str(v).strip()
    return s or None


def _sum_millions(values) -> Decimal | None:
    """Sum per-loan US$-million figures and convert to US$. None if nothing was published."""
    if not values:
        return None
    if not isinstance(values, list):
        values = [values]
    parsed = [parse_decimal(v) for v in values]
    parsed = [p for p in parsed if p is not None]
    if not parsed:
        return None
    return sum(parsed, Decimal("0")) * Decimal("1000000")


class WorldBankProjectsConnector(Connector):
    key = "worldbank_projects"
    name = "World Bank — Projects & Operations API"
    partner_code = "WB"
    tier = 1
    access_method = "public_json_api"
    base_url = "https://search.worldbank.org/api/v2/projects"
    documentation_url = "https://projects.worldbank.org/en/projects-operations/project-search"
    usage_terms = "World Bank Terms of Use for Datasets; attribution to the World Bank required."
    update_frequency = "Continuous (project records updated by the World Bank as operations evolve)"
    default_schedule = "0 2 * * *"
    page_size = 200

    def fetch(self, params: SyncParams) -> Iterator[RawRecord]:
        url = self.config.get("base_url") or self.settings.worldbank_projects_url
        retrieved = 0
        for iso3 in params.countries:
            ref = BY_ISO3.get(iso3)
            if ref is None:
                continue
            offset = 0
            while True:
                resp = self.get(url, params={
                    "format": "json", "countrycode_exact": ref.iso2, "rows": self.page_size,
                    "os": offset, "fl": FIELDS,
                })
                data = resp.json()
                projects = data.get("projects") or {}
                total = int(data.get("total") or 0)
                for pid, p in projects.items():
                    approval = parse_date(p.get("boardapprovaldate"))
                    if params.date_from and approval and approval < params.date_from:
                        continue
                    if params.date_to and approval and approval > params.date_to:
                        continue
                    yield RawRecord(
                        source_identifier=pid,
                        record_type="wb_project",
                        country_iso3=iso3,
                        payload=p,
                        source_url=p.get("url") or f"https://projects.worldbank.org/en/projects-operations/project-detail/{pid}",
                        source_last_updated=p.get("proj_last_upd_date") or p.get("p2a_updated_date"),
                    )
                    retrieved += 1
                    if params.limit and retrieved >= params.limit:
                        return
                offset += self.page_size
                if offset >= total or not projects:
                    break

    def normalize(self, raw: RawRecord) -> NormalizedRecord | None:
        p = raw.payload
        pid = raw.source_identifier
        status_label = p.get("status")
        status = STATUS_MAP.get((status_label or "").lower(), "unknown")
        approval = parse_date(p.get("boardapprovaldate"))
        closing = parse_date(p.get("closingdate"))
        retrieved_on = datetime.now(timezone.utc).date()

        sector_code = None
        sector_label = None
        mj = p.get("mjsector_namecode") or []
        if mj:
            sector_label = mj[0].get("name")
            sector_code = WB_MAJOR_SECTOR_TO_SECTOR.get((sector_label or "").strip().lower())
        sectors = p.get("sector") or []
        if sectors and not sector_label:
            sector_label = sectors[0].get("Name")

        warnings: list[str] = []
        totalamt = parse_decimal(p.get("totalamt"))
        amount_original: Decimal | None = totalamt
        if totalamt is not None and totalamt == 0 and status in ("pipeline", "dropped"):
            # A zero on an unapproved/dropped operation means "no commitment", not a zero-value loan.
            amount_original = None
            warnings.append(f"totalamt=0 on a {status} project: treated as no commitment (not as a zero amount)")

        instrument_label = p.get("lendinginstr")
        instrument_code = WB_LENDING_INSTRUMENT_TO_INSTRUMENT.get((instrument_label or "").lower(), "OTHER") if instrument_label else None
        grant = parse_decimal(p.get("grantamt"))
        if grant and totalamt and grant == totalamt:
            instrument_code = "GRANT"

        parent = _first(p.get("parentprojid"))
        agreement = NormalizedAgreement(
            partner_code="WB",
            source_identifier=pid,
            name=p.get("project_name"),
            instrument_code=instrument_code,
            instrument_label=instrument_label,
            approval_date=approval,
            closing_date_current=closing,
            status=status,
            currency="USD",
            amount_original=amount_original,
            amount_label="World Bank Projects API `totalamt` (IBRD + IDA commitment, US$)",
            parent_source_identifier=parent,
        )
        if amount_original and amount_original > 0:
            agreement.commitments.append(Money(
                amount=amount_original, currency="USD", value_date=approval,
                transaction_key=f"{pid}:totalamt", kind="additional" if parent else "original",
                label="totalamt at board approval date",
            ))
        cum_commit = _sum_millions(p.get("commitment"))
        cum_disb = _sum_millions(p.get("disbursement"))
        undisb = _sum_millions(p.get("available"))
        if cum_disb is not None or cum_commit is not None:
            agreement.reported_current_commitment = cum_commit
            agreement.reported_cumulative_disbursed = cum_disb
            agreement.reported_undisbursed = undisb
            agreement.reported_cumulative_as_of = retrieved_on
            agreement.reported_cumulative_label = (
                "World Bank Projects API `commitment`/`disbursement`/`available` (US$ millions, "
                "2 decimals, cumulative, as published on the retrieval date)"
            )

        rec = NormalizedRecord(
            country_iso3=raw.country_iso3 or "",
            title=p.get("project_name") or pid,
            title_language="en",
            description=_text(p.get("project_abstract")),
            objectives=_text(p.get("pdo")),
            sector_code=sector_code or ("OTHER" if sector_label else None),
            sector_label=sector_label,
            status=status,
            status_label=status_label,
            executing_agency=_text(p.get("impagency")),
            approval_date=approval,
            planned_end_date=closing,
            original_cost=None,  # lendprojectcost is the Bank-financed cost, not total project cost
            agreements=[agreement],
            equivalent_identifiers=[f"44000-{pid}"],
            parent_identifier=parent,
            warnings=warnings,
        )
        project_cost = parse_decimal(p.get("curr_project_cost"))
        if project_cost:
            rec.observations.append(("total_project_cost_usd", "curr_project_cost", project_cost))
        for fname, famount, fcur in zip(p.get("fincrname") or [], p.get("fincr_curr_amt") or [], p.get("fincr_curr_id") or []):
            amt = parse_decimal(famount)
            if amt is not None:
                rec.observations.append((f"financing_plan:{fname}", "fincrname/fincr_curr_amt", f"{amt} {fcur}"))
        rec.observations.append(("wb_status", "status", status_label))
        if p.get("supplementprojectflg") == "Y":
            rec.observations.append(("wb_supplemental_financing", "supplementprojectflg", "Y"))
        if p.get("borrower"):
            rec.observations.append(("borrower", "borrower", _text(p.get("borrower"))))
        for loc in p.get("locations") or []:
            try:
                rec.locations.append({
                    "name": loc.get("geoLocName") or loc.get("name"),
                    "lat": parse_decimal(loc.get("latitude")),
                    "lon": parse_decimal(loc.get("longitude")),
                    "precision": "as published by World Bank",
                })
            except AttributeError:
                continue
        for d in p.get("projectdocs") or []:
            if isinstance(d, dict) and d.get("DocURL"):
                rec.documents.append({
                    "title": d.get("DocTypeDesc") or d.get("DocType") or "World Bank document",
                    "url": d.get("DocURL"), "doc_type": d.get("DocType"),
                    "date": parse_date(d.get("DocDate")), "language": None,
                })
        if approval is None and status not in ("pipeline", "dropped"):
            warnings.append("Board approval date not published")
        return rec

