"""Study snapshot: the single, JSON-serialisable record of validated engine outputs.

Reports, the dashboard and the AI assistant all read from a snapshot, and every reported
number carries the snapshot path it comes from (e.g. ``finance.irr_project``), which makes each
result traceable to the model output that produced it.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

from src.config import APP_VERSION


def _clean(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, float):
        return None if (math.isnan(obj) or math.isinf(obj)) else obj
    if hasattr(obj, "item") and not isinstance(obj, (str, bytes)):
        try:
            return _clean(obj.item())
        except Exception:
            return obj
    return obj


def build_snapshot(project: dict, study, baseline, results: dict | None, recommended: str | None,
                   finance=None, finance_scenario: str | None = None, structures: list | None = None,
                   sensitivity: dict | None = None) -> dict:
    a = study.assumptions
    snap = {
        "meta": {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "app_version": APP_VERSION,
                 "currency": a.currency},
        "project": project,
        "data_flags": {
            "project_synthetic": bool(project.get("is_synthetic") or a.is_synthetic),
            "load_synthetic": bool(study.load.is_synthetic),
            "load_source": study.load.source,
            "load_assumptions": study.load.assumptions,
            "solar_synthetic": bool(study.solar.is_synthetic),
            "solar_source": study.solar.source,
            "grid_outages_synthetic": bool(a.grid.enabled),
            "notes": study.notes,
        },
        "demand": {
            "annual_kwh": study.load.annual_kwh,
            "peak_kw": study.load.peak_kw,
            "load_factor": study.load.load_factor,
            "monthly_kwh": [float(x) for x in _monthly(study.load.values_kw)],
        },
        "solar_resource": {"annual_ghi_kwh_m2": study.solar.annual_kwh_m2,
                           "specific_yield_kwh_per_kwp": float(study.profiles.pv_per_kwp.sum()) if study.profiles.pv_per_kwp is not None else None},
        "diesel_module": study.diesel_baseline.model_dump(),
        "baseline": baseline.to_summary(),
        "scenarios": {k: {"lp": v["lp"].to_summary(), "check": v["check"].to_summary()} for k, v in (results or {}).items()},
        "recommended": recommended,
        "finance_scenario": finance_scenario,
        "finance": finance.model_dump() if finance is not None else None,
        "structures": structures or [],
        "sensitivity": sensitivity or {},
        "assumptions": a.model_dump(),
    }
    return _clean(snap)


def _monthly(values) -> list[float]:
    import numpy as np

    from src.energy.load_profiles import hourly_index

    idx = hourly_index()
    v = np.asarray(values, dtype=float)
    return [float(v[idx.month == m].sum()) for m in range(1, 13)]


def get_path(snapshot: dict, path: str) -> Any:
    node: Any = snapshot
    for part in path.split("."):
        if isinstance(node, dict):
            node = node.get(part)
        elif isinstance(node, list):
            node = node[int(part)]
        else:
            return None
        if node is None:
            return None
    return node


KEY_FACTS = [
    ("demand.annual_kwh", "Annual electricity consumption", "kWh"),
    ("demand.peak_kw", "Peak demand", "kW"),
    ("baseline.metrics.annual_operating_cost", "Baseline annual operating cost", "CCY"),
    ("baseline.metrics.fuel_l", "Baseline diesel consumption", "L/yr"),
    ("baseline.metrics.co2_t", "Baseline diesel CO2", "t/yr"),
    ("diesel_module.operating_cost_per_kwh", "Diesel operating cost per kWh (existing fleet)", "CCY/kWh"),
    ("diesel_module.economic_cost_per_kwh", "Diesel full economic cost per kWh", "CCY/kWh"),
    ("diesel_module.lcoe_per_kwh", "Diesel levelised cost", "CCY/kWh"),
    ("finance.npv_project", "Project NPV", "CCY"),
    ("finance.irr_project", "Project IRR", "fraction"),
    ("finance.irr_equity", "Equity IRR", "fraction"),
    ("finance.lcoe_per_kwh", "System LCOE (project life)", "CCY/kWh"),
    ("finance.min_dscr", "Minimum DSCR", "x"),
    ("finance.avg_dscr", "Average DSCR", "x"),
    ("finance.llcr", "LLCR", "x"),
    ("finance.payback_years", "Simple payback", "years"),
    ("finance.discounted_payback_years", "Discounted payback", "years"),
    ("finance.total_financing_requirement", "Total financing requirement", "CCY"),
    ("finance.cumulative_savings", "Cumulative energy cost savings (nominal, before capital)", "CCY"),
]


def facts(snapshot: dict) -> list[dict]:
    """Flat list of validated numeric facts (with their traceability path)."""
    ccy = snapshot.get("meta", {}).get("currency", "XAF")
    out = []
    for path, label, unit in KEY_FACTS:
        out.append({"path": path, "label": label, "unit": unit.replace("CCY", ccy), "value": get_path(snapshot, path)})
    for key, sc in (snapshot.get("scenarios") or {}).items():
        chk = sc.get("check") or {}
        m = chk.get("metrics") or {}
        caps = chk.get("capacities") or {}
        for mk, unit in (("annual_cost", ccy), ("lcoe_per_kwh", f"{ccy}/kWh"), ("renewable_share", "fraction"),
                         ("unserved_fraction", "fraction"), ("fuel_l", "L/yr"), ("total_investment", ccy)):
            out.append({"path": f"scenarios.{key}.check.metrics.{mk}", "label": f"{key}: {mk}", "unit": unit, "value": m.get(mk)})
        for ck in ("pv_kwp", "battery_kwh", "battery_kw", "diesel_new_kw", "biomass_kw"):
            if caps.get(ck):
                out.append({"path": f"scenarios.{key}.check.capacities.{ck}", "label": f"{key}: {ck}", "unit": ck.split("_")[-1], "value": caps.get(ck)})
    return out
