"""Scenario versions and calculation runs."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import time
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..engine import ENGINE_VERSION
from ..engine.assumptions import Assumptions, cell_paths, from_dict, set_path, to_dict
from ..engine.options import EngineOptions
from ..engine.results import run_scenario
from ..engine.validation import ValidationError, validate
from ..models import CalculationRun, Project, ScenarioVersion, User, VersionStatus

TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "demo" / "templates"
TEMPLATES = {
    "demo_fictitious": "Fictitious demonstration portfolio (invented values, not a real project)",
    "crossboundary_reference": "Assumptions of the CrossBoundary Access Open Source Model 1.0 published case "
                               "(reference for reconciliation; check reuse rights before commercial use)",
}


def canonical_hash(payload: dict) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def load_template(name: str) -> dict:
    if name not in TEMPLATES:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"unknown template {name!r}")
    d = json.loads((TEMPLATES_DIR / f"{name}.json").read_text())
    d.pop("_comment", None)
    return d


def parse_assumptions(d: dict) -> Assumptions:
    try:
        a = from_dict(d)
    except (TypeError, KeyError, ValueError) as exc:
        raise HTTPException(422, f"invalid assumptions: {exc}") from exc
    errors = [i for i in validate(a) if i.level == "error"]
    if errors:
        raise HTTPException(422,
                            {"message": "assumptions rejected", "issues": [dataclasses.asdict(i) for i in errors]})
    return a


def parse_options(d: dict | None) -> EngineOptions:
    d = d or {}
    unknown = set(d) - {f.name for f in dataclasses.fields(EngineOptions)}
    if unknown:
        raise HTTPException(422, f"unknown options {sorted(unknown)}")
    return EngineOptions(**{k: bool(v) for k, v in d.items()})


def apply_changes(base: dict, changes: dict) -> dict:
    """Changes keyed by dotted path ("debt.sizing_method") or workbook cell ("Inputs!E302")."""
    if "lots" in changes:   # whole lot table replaced (add, remove or reorder lots)
        base = {**base, "lots": _parse_lots(changes["lots"])}
        changes = {k: v for k, v in changes.items() if k != "lots"}
    a = from_dict(base)
    paths = cell_paths()
    for key, value in changes.items():
        path = paths.get(key, key)
        try:
            set_path(a, path, value)
        except (AttributeError, IndexError, ValueError, TypeError) as exc:
            raise HTTPException(422, f"cannot set {key!r}: {exc}") from exc
    return to_dict(a)


def _parse_lots(lots) -> list[dict]:
    import dataclasses
    from ..engine.assumptions import LOT_COLUMNS, Lot
    if not isinstance(lots, list) or not 1 <= len(lots) <= len(LOT_COLUMNS):
        raise HTTPException(422, f"lots must be a list of 1 to {len(LOT_COLUMNS)} lots")
    fields = {f.name: f for f in dataclasses.fields(Lot)}
    out = []
    for i, lot in enumerate(lots):
        if not isinstance(lot, dict) or set(lot) - set(fields):
            raise HTTPException(422, f"lots.{i}: unknown fields {sorted(set(lot) - set(fields)) if isinstance(lot, dict) else ''}")
        clean = {}
        for name, f in fields.items():
            v = lot.get(name)
            required = f.default is dataclasses.MISSING
            if v is None:
                if required:
                    raise HTTPException(422, f"lots.{i}.{name} is required")
                clean[name] = None
            elif name in ("name", "country"):
                if not isinstance(v, str) or len(v) > 100:
                    raise HTTPException(422, f"lots.{i}.{name} must be text (100 characters at most)")
                clean[name] = v
            elif isinstance(v, bool) or not isinstance(v, (int, float)):
                raise HTTPException(422, f"lots.{i}.{name} must be a number")
            else:
                clean[name] = v
        out.append(clean)
    return out


def create_version(db: Session, *, project: Project, scenario: str, assumptions: dict, options: dict,
                   solver_method: str, user: User, parent: ScenarioVersion | None = None,
                   changes: dict | None = None, provenance: dict | None = None, note: str = "") -> ScenarioVersion:
    parse_assumptions(assumptions)
    parse_options(options)
    if solver_method not in ("excel_macros", "exact"):
        raise HTTPException(422, "solver_method must be excel_macros or exact")
    last = db.scalar(select(func.max(ScenarioVersion.version)).where(
        ScenarioVersion.project_id == project.id, ScenarioVersion.scenario == scenario)) or 0
    v = ScenarioVersion(project_id=project.id, scenario=scenario, version=last + 1,
                        parent_id=parent.id if parent else None, assumptions=assumptions, options=options or {},
                        solver_method=solver_method, changes=changes or {}, provenance=provenance or {},
                        note=note, created_by=user.id,
                        content_hash=canonical_hash({"a": assumptions, "o": options or {}, "m": solver_method}))
    db.add(v)
    db.flush()
    return v


def run_version(db: Session, version: ScenarioVersion, user: User, per_lot: bool = False) -> CalculationRun:
    a = parse_assumptions(version.assumptions)
    opts = parse_options(version.options)
    t0 = time.perf_counter()
    run = CalculationRun(version_id=version.id, engine_version=ENGINE_VERSION, created_by=user.id,
                         inputs_hash=version.content_hash, status="failed")
    try:
        res = run_scenario(a, method=version.solver_method, options=opts, per_lot=per_lot)
        run.status = res.status
        run.result = json.loads(json.dumps(res.as_dict(), default=_json_default))
    except ValidationError as exc:
        run.error = str(exc)
    except Exception as exc:  # noqa: BLE001 - stored and reported, never swallowed silently
        run.error = f"{type(exc).__name__}: {exc}"
    run.duration_ms = int((time.perf_counter() - t0) * 1000)
    db.add(run)
    db.flush()
    return run


def _json_default(o):
    if isinstance(o, float) and o != o:
        return None
    return str(o)


def can_see_version(role, version: ScenarioVersion) -> bool:
    from ..models import Role
    return role != Role.investor or version.status == VersionStatus.approved
