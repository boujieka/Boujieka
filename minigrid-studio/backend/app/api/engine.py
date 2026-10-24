import dataclasses

from fastapi import APIRouter, Depends

from ..engine import ENGINE_VERSION, RECONCILIATION
from ..engine import assumptions as A
from ..engine.options import EngineOptions, option_docs
from ..security import Caller, current_caller
from ..exports.labels import field_entries, labels
from ..services.scenarios import TEMPLATES

router = APIRouter(prefix="/engine", tags=["engine"])


@router.get("/info")
def info():
    return {"engine_version": ENGINE_VERSION, "reconciliation": RECONCILIATION,
            "deterministic": True, "uses_generative_ai": False,
            "solver_methods": {"excel_macros": "faithful replay of the workbook macros (default)",
                               "exact": "exact fixed point (variant)"}}


@router.get("/options")
def options():
    docs = option_docs()
    return [{"name": f.name, "default": f.default, "doc": docs[f.name]} for f in dataclasses.fields(EngineOptions)]


@router.get("/assumption-schema")
def assumption_schema(_: Caller = Depends(current_caller)):
    out = []
    for g in dataclasses.fields(A.Assumptions):
        if g.name == "lots":
            for name, row in A.LOT_ROWS.items():
                out.append({"path": f"lots.<i>.{name}", "cell": f"Portfolio!E..J{row}", "unit": "", "doc": ""})
            continue
        cls = getattr(A, g.type)
        for f in dataclasses.fields(cls):
            out.append({"path": f"{g.name}.{f.name}", "cell": f.metadata.get("cell", ""),
                        "unit": f.metadata.get("unit", ""), "doc": f.metadata.get("doc", ""), "type": str(f.type)})
    return out


@router.get("/labels")
def get_labels(lang: str = "fr"):
    """FR/EN labels of groups, fields, indicators, series, checks and units, plus the rules that give the
    French form of engine messages (Python regex syntax; replacement groups written \\1)."""
    return labels("fr" if lang == "fr" else "en")


@router.get("/fields")
def get_fields(_: Caller = Depends(current_caller)):
    """Editable assumptions with their group, FR/EN labels, unit, workbook cell and note."""
    return field_entries()


@router.get("/templates")
def templates():
    return [{"name": k, "description": v} for k, v in TEMPLATES.items()]
