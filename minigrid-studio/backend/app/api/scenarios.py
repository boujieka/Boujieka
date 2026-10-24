import csv
import datetime as dt
import hashlib
import io
import tempfile
import zipfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
from ..engine.assumptions import to_dict
from ..models import CalculationRun, Role, ScenarioVersion, VersionStatus
from ..schemas import SCENARIO_PATTERN, ReviewIn, ReviseIn, RunIn, RunOut, VersionDetail, VersionIn, VersionOut
from ..security import Caller, current_caller, project_for
from ..services import audit
from ..services import scenarios as svc

router = APIRouter(tags=["scenarios"])


def _version(db: Session, caller: Caller, version_id: str, capability: str = "read"):
    v = db.get(ScenarioVersion, version_id)
    if v is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    p, role = project_for(db, caller, v.project_id, capability)
    if not svc.can_see_version(role, v):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    return v, p, role


@router.post("/projects/{project_id}/versions", response_model=VersionOut, status_code=201)
def create_version(project_id: str, body: VersionIn, caller: Caller = Depends(current_caller),
                   db: Session = Depends(get_db)):
    p, _ = project_for(db, caller, project_id, "edit")
    if body.assumptions is not None:
        base, provenance = body.assumptions, {"source": "payload"}
    else:
        base, provenance = svc.load_template(body.template), {"source": "template", "template": body.template}
    assumptions = svc.apply_changes(base, body.changes) if body.changes else svc.apply_changes(base, {})
    v = svc.create_version(db, project=p, scenario=body.scenario, assumptions=assumptions, options=body.options,
                           solver_method=body.solver_method, user=caller.user, changes=body.changes,
                           provenance=provenance, note=body.note)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="version.create", entity_type="version",
                 entity_id=v.id, payload={"scenario": v.scenario, "version": v.version, "provenance": provenance,
                                          "changes": body.changes, "options": body.options})
    return v


MAX_UNCOMPRESSED = 60 * 1024 * 1024
MAX_RATIO = 100


def _check_zip(data: bytes) -> None:
    """Reject archives whose decompressed size or ratio is abnormal (zip bombs)."""
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            infos = z.infolist()
    except zipfile.BadZipFile as exc:
        raise HTTPException(422, "not a valid workbook archive") from exc
    total = sum(i.file_size for i in infos)
    if len(infos) > 2000 or total > MAX_UNCOMPRESSED:
        raise HTTPException(413, "workbook too large once decompressed")
    for i in infos:
        if i.compress_size and i.file_size / i.compress_size > MAX_RATIO and i.file_size > 1024 * 1024:
            raise HTTPException(413, "suspicious compression ratio")


@router.post("/projects/{project_id}/versions/import-xlsm", response_model=VersionOut, status_code=201)
def import_xlsm(project_id: str, file: UploadFile = File(...),
                scenario: str = Form("imported", pattern=SCENARIO_PATTERN),
                caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    """Read the assumptions of a workbook in the CrossBoundary format. The file
    is parsed as data only: formulas are not evaluated and macros never run.
    (Synchronous handler: FastAPI runs it in a worker thread, not on the event loop.)"""
    p, _ = project_for(db, caller, project_id, "edit")
    limit = get_settings().max_upload_mb * 1024 * 1024
    data = file.file.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(413, f"file above {get_settings().max_upload_mb} MB")
    name = (file.filename or "").lower()
    if not name.endswith((".xlsm", ".xlsx")) or not data.startswith(b"PK\x03\x04"):
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "expected an .xlsm/.xlsx workbook")
    _check_zip(data)
    from ..engine.loader import load_assumptions
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "upload.xlsx"   # the macro container is ignored by openpyxl
        path.write_bytes(data)
        try:
            a = load_assumptions(path)
        except Exception as exc:  # noqa: BLE001 - details are logged in the audit, not returned
            audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="version.import_rejected",
                         entity_type="project", entity_id=p.id,
                         payload={"error": f"{type(exc).__name__}: {str(exc)[:300]}"})
            db.commit()
            raise HTTPException(422, "workbook is not in the expected CrossBoundary format") from exc
    provenance = {"source": "xlsm_upload", "filename": (file.filename or "")[:200],
                  "sha256": hashlib.sha256(data).hexdigest()}
    v = svc.create_version(db, project=p, scenario=scenario, assumptions=to_dict(a), options={},
                           solver_method="excel_macros", user=caller.user, provenance=provenance)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="version.import", entity_type="version",
                 entity_id=v.id, payload=provenance)
    return v


@router.get("/projects/{project_id}/versions", response_model=list[VersionOut])
def list_versions(project_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    p, role = project_for(db, caller, project_id)
    q = select(ScenarioVersion).where(ScenarioVersion.project_id == p.id)
    if role == Role.investor:
        q = q.where(ScenarioVersion.status == VersionStatus.approved)
    return db.scalars(q.order_by(ScenarioVersion.scenario, ScenarioVersion.version)).all()


@router.get("/versions/{version_id}", response_model=VersionDetail)
def get_version(version_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    return _version(db, caller, version_id)[0]


@router.post("/versions/{version_id}/revise", response_model=VersionOut, status_code=201)
def revise(version_id: str, body: ReviseIn, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    parent, p, _ = _version(db, caller, version_id, "edit")
    assumptions = svc.apply_changes(parent.assumptions, body.changes)
    v = svc.create_version(db, project=p, scenario=parent.scenario, assumptions=assumptions,
                           options=parent.options if body.options is None else body.options,
                           solver_method=body.solver_method or parent.solver_method, user=caller.user,
                           parent=parent, changes=body.changes, provenance={"source": "revision", "parent": parent.id},
                           note=body.note)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="version.revise", entity_type="version",
                 entity_id=v.id, payload={"parent": parent.id, "changes": body.changes})
    return v


@router.post("/versions/{version_id}/submit", response_model=VersionOut)
def submit(version_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    v, p, _ = _version(db, caller, version_id, "edit")
    if v.status not in (VersionStatus.draft, VersionStatus.rejected):
        raise HTTPException(status.HTTP_409_CONFLICT, f"version is {v.status.value}")
    if not db.scalar(select(CalculationRun).where(CalculationRun.version_id == v.id,
                                                  CalculationRun.status != "failed")):
        raise HTTPException(status.HTTP_409_CONFLICT, "run the calculation before submitting for review")
    v.status = VersionStatus.submitted
    v.submitted_by = caller.user.id
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="version.submit", entity_type="version",
                 entity_id=v.id)
    return v


@router.post("/versions/{version_id}/review", response_model=VersionOut)
def review(version_id: str, body: ReviewIn, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    v, p, _ = _version(db, caller, version_id, "review")
    if v.status != VersionStatus.submitted:
        raise HTTPException(status.HTTP_409_CONFLICT, "only submitted versions can be reviewed")
    if caller.user.id in (v.created_by, v.submitted_by):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            "four-eyes rule: the author or submitter cannot review this version")
    v.status = VersionStatus.approved if body.decision == "approve" else VersionStatus.rejected
    v.reviewed_by, v.reviewed_at, v.review_comment = caller.user.id, dt.datetime.now(dt.timezone.utc), body.comment
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action=f"version.{body.decision}",
                 entity_type="version", entity_id=v.id, payload={"comment": body.comment})
    return v


@router.post("/versions/{version_id}/runs", response_model=RunOut, status_code=201)
def run(version_id: str, body: RunIn = RunIn(), caller: Caller = Depends(current_caller),
        db: Session = Depends(get_db)):
    v, p, _ = _version(db, caller, version_id, "edit")
    r = svc.run_version(db, v, caller.user, per_lot=body.per_lot)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="run.create", entity_type="run",
                 entity_id=r.id, payload={"version": v.id, "status": r.status, "engine": r.engine_version})
    return r


@router.get("/versions/{version_id}/runs", response_model=list[RunOut])
def list_runs(version_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    v, _, role = _version(db, caller, version_id)
    rows = db.scalars(select(CalculationRun).where(CalculationRun.version_id == v.id)
                      .order_by(CalculationRun.created_at)).all()
    return [_public(r, role) for r in rows]


def _public(r: CalculationRun, role: Role) -> RunOut:
    out = RunOut.model_validate(r)
    if role == Role.investor and out.error:
        out.error = "calculation failed"   # internal details stay with the project team
    return out


def _run(db: Session, caller: Caller, run_id: str):
    r = db.get(CalculationRun, run_id)
    if r is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    _, p, role = _version(db, caller, r.version_id)
    return r, p, role


@router.get("/runs/{run_id}", response_model=RunOut)
def get_run(run_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    r, _, role = _run(db, caller, run_id)
    return _public(r, role)


@router.get("/runs/{run_id}/series.csv")
def export_series(run_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    """Annual series with their unit and workbook source row, one column per year."""
    r, p, _ = _run(db, caller, run_id)
    audit.record(db, org_id=p.org_id, user_id=caller.user.id, action="run.export_csv", entity_type="run",
                 entity_id=r.id)
    if not r.result:
        raise HTTPException(status.HTTP_409_CONFLICT, "run has no result")
    series = r.result["series"]
    years = [int(y) for y in series["year"]["values"]]
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["series", "label", "unit", "source", "derived"] + years)
    for k, s in series.items():
        w.writerow([k, s["label"], s["unit"], s["source"], s.get("derived", False)] +
                   ["" if x is None else x for x in s["values"]])
    w.writerow([])
    w.writerow(["engine_version", r.engine_version, "status", r.status, "inputs_sha256", r.inputs_hash])
    return Response(buf.getvalue(), media_type="text/csv",
                    headers={"Content-Disposition": f'attachment; filename="run-{r.id}.csv"'})
