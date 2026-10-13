"""Electrification Acceleration Score: explainable project prioritisation (0 to 100) with mandatory gates.

The weights and the scales below are INITIAL DESIGN ASSUMPTIONS of the platform, not a validated scientific standard.
Users can change both. A failed mandatory gate always excludes the project, whatever its score; an unknown gate
puts the project under review. The score never overrides a gate.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

GateState = Literal["met", "not_met", "unknown"]

GATES = {
    "land_rights": "Land rights resolved",
    "permits": "Permits and licences obtained or on track",
    "technical_feasibility": "Technical feasibility confirmed",
    "environmental_social": "No material unresolved environmental and social risk",
    "regulatory": "No unresolved regulatory restriction",
    "model_checks": "Financial model passes its integrity checks",
}


class Weights(BaseModel):
    """Initial design weights (sum 1). Configurable; not a validated standard."""

    access_impact: float = 0.20
    financial_efficiency: float = 0.20
    readiness: float = 0.15
    speed: float = 0.15
    productive_use: float = 0.15
    equity: float = 0.15


class Scales(BaseModel):
    """Anchors mapping raw values to 0..1 (linear, clipped). Initial design assumptions; configurable."""

    connections_high: float = Field(2000, gt=0, description="Connections scoring 1.0 on access impact")
    subsidy_per_connection_usd_low: float = Field(0, ge=0, description="Subsidy per connection scoring 1.0")
    subsidy_per_connection_usd_high: float = Field(1500, gt=0, description="Subsidy per connection scoring 0.0")
    dscr_low: float = Field(1.0, description="Minimum DSCR scoring 0.0")
    dscr_high: float = Field(1.5, description="Minimum DSCR scoring 1.0")
    months_fast: float = Field(6, gt=0, description="Months to first power scoring 1.0")
    months_slow: float = Field(36, gt=0, description="Months to first power scoring 0.0")


class ScoreInputs(BaseModel):
    project_id: str
    project_name: str
    connections: float | None = None
    subsidy_per_connection_usd: float | None = None
    dscr_min: float | None = None
    has_debt: bool = True
    months_to_power: float | None = None
    productive_energy_share: float | None = Field(None, ge=0, le=1)
    household_share: float | None = Field(None, ge=0, le=1)
    underserved_area: bool | None = None
    readiness_done: int = 0
    readiness_required: int = 0
    gates: dict[str, GateState] = Field(default_factory=lambda: {k: "unknown" for k in GATES})


def _lin(x: float, lo: float, hi: float) -> float:
    if hi == lo:
        return 1.0 if x >= hi else 0.0
    return max(0.0, min(1.0, (x - lo) / (hi - lo)))


def score_project(s: ScoreInputs, w: Weights = Weights(), sc: Scales = Scales()) -> dict:
    tot_w = w.access_impact + w.financial_efficiency + w.readiness + w.speed + w.productive_use + w.equity
    if tot_w <= 0:
        raise ValueError("Weights must add to more than zero")
    parts = []

    def part(key: str, label: str, weight: float, value, norm: float | None, why: str) -> None:
        contrib = None if norm is None else norm * weight / tot_w * 100
        parts.append({"criterion": key, "label": label, "weight": weight / tot_w, "raw": value, "normalised": norm,
                      "points": contrib, "explanation": why if norm is not None else f"Data unavailable: {why}"})

    part("access_impact", "Access impact", w.access_impact, s.connections,
         None if s.connections is None else _lin(s.connections, 0, sc.connections_high),
         f"connections against {sc.connections_high:,.0f} for a full score")
    fin_norm = None
    fin_why = "subsidy per connection and minimum DSCR"
    if s.subsidy_per_connection_usd is not None and (s.dscr_min is not None or not s.has_debt):
        sub = 1 - _lin(s.subsidy_per_connection_usd, sc.subsidy_per_connection_usd_low, sc.subsidy_per_connection_usd_high)
        dscr = 1.0 if not s.has_debt else _lin(s.dscr_min, sc.dscr_low, sc.dscr_high)
        fin_norm = 0.5 * sub + 0.5 * dscr
        fin_why = (f"half subsidy efficiency (USD {s.subsidy_per_connection_usd:,.0f} per connection; full score at "
                   f"{sc.subsidy_per_connection_usd_low:,.0f}, zero at {sc.subsidy_per_connection_usd_high:,.0f}), half debt cover "
                   + ("(no debt)" if not s.has_debt else f"(minimum DSCR {s.dscr_min:.2f}x; zero at {sc.dscr_low}x, full at {sc.dscr_high}x)"))
    part("financial_efficiency", "Financial and subsidy efficiency", w.financial_efficiency,
         {"subsidy_per_connection_usd": s.subsidy_per_connection_usd, "dscr_min": s.dscr_min}, fin_norm, fin_why)
    rd = None if s.readiness_required == 0 else s.readiness_done / s.readiness_required
    part("readiness", "Implementation readiness", w.readiness, f"{s.readiness_done} of {s.readiness_required}", rd,
         "share of required preparation milestones completed")
    part("speed", "Deployment speed", w.speed, s.months_to_power,
         None if s.months_to_power is None else 1 - _lin(s.months_to_power, sc.months_fast, sc.months_slow),
         f"months to first power; full score at {sc.months_fast:g} months or less, zero at {sc.months_slow:g} or more")
    part("productive_use", "Productive use potential", w.productive_use, s.productive_energy_share, s.productive_energy_share,
         "share of energy sold to productive, commercial, agricultural and anchor customers")
    eq = None
    if s.household_share is not None and s.underserved_area is not None:
        eq = 0.5 * s.household_share + 0.5 * (1.0 if s.underserved_area else 0.0)
    part("equity", "Social and territorial equity", w.equity,
         {"household_share": s.household_share, "underserved_area": s.underserved_area}, eq,
         "half the household share of connections, half whether the area is underserved (user assessment)")
    missing = [p_["criterion"] for p_ in parts if p_["normalised"] is None]
    total = sum(p_["points"] for p_ in parts if p_["points"] is not None)
    gate_rows = [{"gate": k, "label": GATES[k], "state": s.gates.get(k, "unknown")} for k in GATES]
    failed = [g["label"] for g in gate_rows if g["state"] == "not_met"]
    unknown = [g["label"] for g in gate_rows if g["state"] == "unknown"]
    if failed:
        decision = "excluded"
        why = "Excluded whatever the score: " + "; ".join(failed)
    elif unknown:
        decision = "review_required"
        why = "Review required before ranking: " + "; ".join(unknown)
    else:
        decision = "eligible"
        why = "All mandatory gates met"
    return {"project_id": s.project_id, "project_name": s.project_name, "score": round(total, 1),
            "score_is_partial": bool(missing), "missing_criteria": missing, "parts": parts, "gates": gate_rows,
            "decision": decision, "decision_explanation": why,
            "note": "Weights and scales are initial design assumptions of the platform, not a validated standard."}


def rank(projects: list[ScoreInputs], w: Weights = Weights(), sc: Scales = Scales()) -> list[dict]:
    """Eligible projects first by score; then review required; excluded projects last and never ranked."""
    scored = [score_project(p, w, sc) for p in projects]
    order = {"eligible": 0, "review_required": 1, "excluded": 2}
    scored.sort(key=lambda r: (order[r["decision"]], -r["score"]))
    pos = 0
    for r in scored:
        if r["decision"] == "eligible":
            pos += 1
            r["rank"] = pos
        else:
            r["rank"] = None
    return scored
