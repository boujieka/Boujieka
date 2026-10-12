"""Execute the engine for a project and turn the result into storable, JSON safe records."""
from __future__ import annotations

import hashlib
import json
import math

import numpy as np

from ..config import ENGINE_VERSION
from ..engine.checks import status
from ..engine.inputs import ProjectInputs
from ..engine.model import run_model

QUARTERLY_KEYS = ("connections", "billed_kwh", "unserved_kwh", "revenue", "opex", "bad_debt", "ebitda", "cfads", "debt_service",
                  "dscr_quarter", "cash", "debt_balance", "nbv", "equity_contributions", "equity_support", "distributions",
                  "grant_receipts", "rbf_receipts", "tariff_support", "replacement_capex", "capex", "net_income",
                  "total_assets", "total_liabilities", "total_equity", "cfo", "cfi", "cff", "fx")


def clean(x):
    """JSON safe: numpy to Python, NaN and infinities to None."""
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, np.ndarray):
        return [clean(v) for v in x.tolist()]
    if isinstance(x, (np.floating, float)):
        f = float(x)
        return None if not math.isfinite(f) else f
    if isinstance(x, np.integer):
        return int(x)
    if hasattr(x, "value") and hasattr(x, "name"):  # enums
        return x.value
    return x


def inputs_hash(p: ProjectInputs) -> str:
    return hashlib.sha256(json.dumps(p.model_dump(mode="json"), sort_keys=True).encode()).hexdigest()


def execute(p: ProjectInputs) -> dict:
    r = run_model(p)
    st, checks, warns, missing = status(r)
    quarterly = {"date": [d.isoformat() for d in r.dates], **{k: r.series[k] for k in QUARTERLY_KEYS}}
    return clean({
        "engine_version": ENGINE_VERSION,
        "status": st.value,
        "metrics": r.metrics,
        "checks": [c.__dict__ for c in checks],
        "warnings": [c.__dict__ for c in warns],
        "missing_inputs": missing,
        "annual": r.annual,
        "sources_uses": r.sources_uses,
        "quarterly": quarterly,
        "inputs_sha256": inputs_hash(p),
    })
