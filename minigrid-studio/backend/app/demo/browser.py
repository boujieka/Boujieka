"""Entry points of the in-browser demo (Pyodide). JSON in, JSON out; no I/O, no network.

The same engine, labels, comparison and Studio export as the server; storage, projects
and versions live in the browser. Only the fictitious template is shipped."""
from __future__ import annotations

import base64
import dataclasses
import hashlib
import json
import time

from ..engine import ENGINE_VERSION
from ..engine.assumptions import from_dict
from ..engine.changes import ChangeError, apply_changes
from ..engine.options import EngineOptions, option_docs
from ..engine.results import run_scenario
from ..engine.validation import ValidationError
from ..exports.compare import compare_runs
from ..exports.labels import field_entries, labels

TEMPLATE_DESCRIPTIONS = {"demo_fictitious": "Fictitious demonstration portfolio (invented values, not a real project)"}


def _json_default(o):
    if isinstance(o, float) and o != o:
        return None
    if hasattr(o, "isoformat"):
        return o.isoformat()
    return str(o)


def _dump(o) -> str:
    return json.dumps(o, default=_json_default)


def meta(lang: str) -> str:
    docs = option_docs()
    return _dump({
        "engine_version": ENGINE_VERSION,
        "labels": labels("fr" if lang == "fr" else "en"),
        "fields": field_entries(),
        "options": [{"name": f.name, "default": f.default, "doc": docs[f.name]} for f in dataclasses.fields(EngineOptions)],
        "templates": [{"name": k, "description": v} for k, v in TEMPLATE_DESCRIPTIONS.items()],
    })


def revise(assumptions_json: str, changes_json: str) -> str:
    try:
        return _dump({"ok": True, "assumptions": apply_changes(json.loads(assumptions_json), json.loads(changes_json))})
    except ChangeError as exc:
        return _dump({"ok": False, "error": str(exc)})


def run(assumptions_json: str, options_json: str, solver: str, per_lot: bool) -> str:
    a_dict = json.loads(assumptions_json)
    opts = json.loads(options_json or "{}")
    t0 = time.perf_counter()
    out = {"engine_version": ENGINE_VERSION, "status": "failed", "error": "", "result": {},
           "inputs_hash": hashlib.sha256(json.dumps({"a": a_dict, "o": opts, "m": solver}, sort_keys=True,
                                                    default=str).encode()).hexdigest()}
    try:
        unknown = set(opts) - {f.name for f in dataclasses.fields(EngineOptions)}
        if unknown:
            raise ValueError(f"unknown options {sorted(unknown)}")
        res = run_scenario(from_dict(a_dict), method=solver, options=EngineOptions(**{k: bool(v) for k, v in opts.items()}),
                           per_lot=bool(per_lot))
        out["status"] = res.status
        out["result"] = json.loads(_dump(res.as_dict()))
    except ValidationError as exc:
        out["error"] = str(exc)
    except Exception as exc:  # noqa: BLE001 - shown to the user, never hidden
        out["error"] = f"{type(exc).__name__}: {exc}"
    out["duration_ms"] = int((time.perf_counter() - t0) * 1000)
    return _dump(out)


def compare(items_json: str, lang: str) -> str:
    return _dump(compare_runs(json.loads(items_json), lang))


def studio_xlsx(project_json: str, version_json: str, run_json: str, lang: str) -> str:
    from ..exports.xlsx_studio import build_studio_workbook   # needs openpyxl, loaded on demand
    data = build_studio_workbook(project=json.loads(project_json), version=json.loads(version_json),
                                 run=json.loads(run_json), lang=lang)
    return base64.b64encode(data).decode()
