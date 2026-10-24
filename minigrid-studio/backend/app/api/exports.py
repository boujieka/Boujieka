"""Exports of a run (Studio .xlsx, PDF report, CrossBoundary-format workbook) and
side-by-side comparison of runs."""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
from ..engine.assumptions import from_dict
from ..models import Role, ScenarioVersion
from ..security import Caller, current_caller
from ..services import audit
from ..exports.crossboundary import TemplateMismatch, fill_template
from ..exports.labels import kpi_label, labels, series_label
from ..exports.pdf_report import build_pdf_report
from ..exports.xlsx_studio import build_studio_workbook
from .scenarios import _check_zip, _run

router = APIRouter(tags=["exports"])
Lang = Literal["fr", "en"]
XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
XLSM = "application/vnd.ms-excel.sheet.macroEnabled.12"


def _context(db: Session, caller: Caller, run_id: str):
    r, p, role = _run(db, caller, run_id)
    if not r.result:
        raise HTTPException(409, "run has no result")
    v = db.get(ScenarioVersion, r.version_id)
    project = {"name": p.name, "country": p.country}
    version = {"scenario": v.scenario, "version": v.version, "status": v.status.value, "assumptions": v.assumptions}
    run = {"id": r.id, "status": r.status, "engine_version": r.engine_version, "inputs_hash": r.inputs_hash,
           "error": "calculation failed" if role == Role.investor and r.error else r.error, "result": r.result}
    return r, p, project, version, run


def _filename(project: dict, version: dict, ext: str) -> str:
    base = "".join(c if c.isalnum() or c in "-_" else "-" for c in f"{project['name']}-{version['scenario']}-v{version['version']}")
    return f"{base[:80]}.{ext}"


@router.get("/runs/{run_id}/export.xlsx")
def export_xlsx(run_id: str, lang: Lang = "fr", caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    """Studio workbook: engine values with their workbook source, and live Excel formulas that recompute
    the accounting identities, DSCR, project IRR (XIRR) and NPV (XNPV) next to a gap column."""
    r, p, project, version, run = _context(db, caller, run_id)
    data = build_studio_workbook(project=project, version=version, run=run, lang=lang)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="run.export_xlsx", entity_type="run", entity_id=r.id)
    return Response(data, media_type=XLSX,
                    headers={"Content-Disposition": f'attachment; filename="{_filename(project, version, "xlsx")}"'})


@router.get("/runs/{run_id}/report.pdf")
def export_pdf(run_id: str, lang: Lang = "fr", caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    """PDF report: status, alerts, indicators with sources, charts, annual summary, checks, assumptions, lots."""
    r, p, project, version, run = _context(db, caller, run_id)
    data = build_pdf_report(project=project, version=version, run=run, lang=lang)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="run.export_pdf", entity_type="run", entity_id=r.id)
    return Response(data, media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="{_filename(project, version, "pdf")}"'})


@router.post("/runs/{run_id}/export-crossboundary")
def export_crossboundary(run_id: str, template: UploadFile = File(...), caller: Caller = Depends(current_caller),
                         db: Session = Depends(get_db)):
    """Fill YOUR copy of the CrossBoundary workbook with this run's assumptions and pasted values. The template
    is not stored; only input cells are rewritten, formulas, charts and macros are kept; Excel recalculates on
    opening. Variant runs are refused: the workbook does not implement the engine options."""
    r, p, project, version, run = _context(db, caller, run_id)
    if r.status != "reconciled-engine":
        raise HTTPException(422, "only reconciled-engine runs (faithful options, macro solver) can be written "
                                 "into the CrossBoundary workbook")
    limit = get_settings().max_upload_mb * 1024 * 1024
    data = template.file.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(413, f"file above {get_settings().max_upload_mb} MB")
    if not (template.filename or "").lower().endswith((".xlsm", ".xlsx")) or not data.startswith(b"PK\x03\x04"):
        raise HTTPException(415, "expected an .xlsm/.xlsx workbook")
    _check_zip(data)
    try:
        out = fill_template(data, from_dict(version["assumptions"]), r.result.get("pasted_values") or {})
    except TemplateMismatch as exc:
        raise HTTPException(422, {"message": "the scenario cannot be written into this template",
                                  "problems": exc.problems[:50]}) from exc
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="run.export_crossboundary", entity_type="run",
                 entity_id=r.id)
    ext = "xlsm" if (template.filename or "").lower().endswith(".xlsm") else "xlsx"
    return Response(out, media_type=XLSM if ext == "xlsm" else XLSX,
                    headers={"Content-Disposition": f'attachment; filename="{_filename(project, version, ext)}"'})


class CompareIn(BaseModel):
    run_ids: list[str] = Field(min_length=2, max_length=4)
    lang: Lang = "fr"


COMPARE_SERIES = ["revenue", "ebitda", "cfads", "debt_service", "dscr", "senior_debt_balance", "project_cash_flow",
                  "distributions"]


def _flat(d, prefix=""):
    if isinstance(d, dict):
        for k, v in d.items():
            yield from _flat(v, f"{prefix}{k}.")
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from _flat(v, f"{prefix}{i}.")
    else:
        yield prefix[:-1], d


@router.post("/compare")
def compare(body: CompareIn, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    """Indicators, key series and differing assumptions of 2 to 4 runs (the first is the base)."""
    ctx = [_context(db, caller, rid) for rid in body.run_ids]
    lab = labels(body.lang)
    runs = [{"run_id": r.id, "project": proj["name"], "scenario": ver["scenario"], "version": ver["version"],
             "status": r.status, "version_status": ver["status"], "options": r.result.get("options", []),
             "solver": r.result.get("solver", {}).get("method")} for r, _p, proj, ver, _run in ctx]
    keys = []
    for r, *_ in ctx:
        keys += [k for k in r.result.get("kpis", {}) if k not in keys]
    kpis = {}
    for k in keys:
        vals = [r.result["kpis"].get(k, {}).get("value") for r, *_ in ctx]
        first = next((r.result["kpis"][k] for r, *_ in ctx if k in r.result["kpis"]), {})
        base = vals[0]
        kpis[k] = {"label": kpi_label(k, first.get("label", k), body.lang), "unit": first.get("unit", ""),
                   "source": first.get("source", ""), "values": vals,
                   "deltas": [None if v is None or base is None else v - base for v in vals]}
    series = {}
    for k in COMPARE_SERIES:
        if all(k in r.result.get("series", {}) for r, *_ in ctx):
            s0 = ctx[0][0].result["series"][k]
            series[k] = {"label": series_label(k, s0["label"], body.lang), "unit": s0["unit"],
                         "values": [r.result["series"][k]["values"] for r, *_ in ctx]}
    years = ctx[0][0].result["series"]["year"]["values"]
    flats = [dict(_flat(ver["assumptions"])) for _r, _p, _proj, ver, _run in ctx]
    paths = []
    for f in flats:
        paths += [k for k in f if k not in paths]
    diffs = []
    for path in paths:
        vals = [f.get(path) for f in flats]
        if any(v != vals[0] for v in vals[1:]):
            parts = path.split(".")
            key = f"lots.<i>.{parts[2]}" if parts[0] == "lots" and len(parts) > 2 else ".".join(parts[:2])
            diffs.append({"path": path, "label": lab["fields"].get(key, path), "values": vals})
    return {"runs": runs, "years": years, "kpis": kpis, "series": series, "assumption_diffs": diffs[:500]}
