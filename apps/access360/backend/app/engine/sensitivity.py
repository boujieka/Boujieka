"""Deterministic sensitivities, scenario comparison and the minimum subsidy solver.

Each case changes one input (or one group) on a copy of the base inputs and reruns the full engine, so every
case passes through the same integrity checks as the base."""
from __future__ import annotations

from typing import Callable

from .checks import integrity_checks
from .inputs import ProjectInputs
from .model import ModelResult, run_model

KEY_METRICS = ("project_irr_post_subsidy", "equity_irr", "project_npv_post_subsidy", "dscr_min", "lcoe_per_kwh_sold",
               "equity_support_total")


def _copy(p: ProjectInputs) -> ProjectInputs:
    return p.model_copy(deep=True)


def _scale_capex(f: float) -> Callable[[ProjectInputs], None]:
    def go(p: ProjectInputs) -> None:
        for it in p.capex:
            it.amount *= f
    return go


def _demand_growth(dpp: float):
    def go(p):
        for c in p.customers:
            c.demand_growth_pa += dpp
    return go


def _uptake(f: float):
    def go(p):
        for c in p.customers:
            c.connections_target = int(round(c.connections_target * f))
    return go


def _tariff(f: float):
    def go(p):
        for c in p.customers:
            c.tariff_per_kwh *= f
            c.fixed_charge_month *= f
    return go


def _collection(dpp: float):
    def go(p):
        p.opex.collection_efficiency = min(1.0, max(0.01, p.opex.collection_efficiency + dpp))
    return go


def _battery(f: float):
    def go(p):
        p.technical.battery_replacement_usd_per_kwh *= f
    return go


def _rates(dpp: float):
    def go(p):
        for tr in p.financing.debt:
            tr.rate_pa = max(0.0, tr.rate_pa + dpp)
    return go


def _fx(dpp: float):
    def go(p):
        p.macro.fx_depreciation_pa += dpp
    return go


def _subsidy_delay(nq: int):
    def go(p):
        last = p.construction_quarters + p.operating_years * 4 - 1
        for ms in p.subsidies.grant_milestones:
            if ms.quarter >= p.construction_quarters:
                ms.quarter = min(ms.quarter + nq, last)  # never pushed beyond the horizon
        p.subsidies.rbf_verification_lag_quarters += nq
    return go


def _construction_delay(nq: int):
    def go(p):
        p.construction_quarters += nq
    return go


def _grid(year: int):
    """Uses the project's own grid arrival treatment when one is configured; otherwise the stranded asset case
    (operations stop, no compensation), the most severe treatment, so the case is never silently neutral."""
    def go(p):
        if not p.grid_arrival.enabled:
            p.grid_arrival.treatment = "stranded"
            p.grid_arrival.compensation_pct_nbv = 0.0
            p.grid_arrival.regulatory_source = "Sensitivity case only: stranded asset assumption, no country rule applied"
        p.grid_arrival.enabled = True
        p.grid_arrival.operating_year = year
    return go


def standard_cases() -> list[tuple[str, str, Callable[[ProjectInputs], None]]]:
    cases = []
    for f in (-0.30, -0.20, -0.10, 0.10, 0.20, 0.30):
        cases.append(("capex", f"CAPEX {f:+.0%}", _scale_capex(1 + f)))
    cases += [
        ("demand", "Demand growth -2pp a year", _demand_growth(-0.02)),
        ("demand", "Demand growth +2pp a year", _demand_growth(0.02)),
        ("uptake", "Customer uptake -20%", _uptake(0.8)),
        ("tariff", "Tariff -10%", _tariff(0.9)),
        ("tariff", "Tariff +10%", _tariff(1.1)),
        ("collection", "Collection -10pp", _collection(-0.10)),
        ("battery", "Battery replacement cost +30%", _battery(1.3)),
        ("rates", "Interest rates +2pp", _rates(0.02)),
        ("fx", "LCY depreciation +5pp a year", _fx(0.05)),
        ("subsidy_delay", "Subsidy payments 4 quarters later", _subsidy_delay(4)),
        ("construction_delay", "Construction 2 quarters longer", _construction_delay(2)),
        ("grid", "Grid arrives in operating year 8 (configured treatment, else stranded)", _grid(8)),
    ]
    return cases


def run_case(base: ProjectInputs, change: Callable[[ProjectInputs], None]) -> ModelResult:
    p = _copy(base)
    change(p)
    p = ProjectInputs.model_validate(p.model_dump())  # re-validate the changed inputs
    return run_model(p)


def sensitivity_table(base: ProjectInputs) -> list[dict]:
    b = run_model(base)
    rows = [{"group": "base", "case": "Base case", "checks_passed": all(c.passed for c in integrity_checks(b)),
             **{k: b.metrics.get(k) for k in KEY_METRICS}}]
    for group, name, fn in standard_cases():
        r = run_case(base, fn)
        rows.append({"group": group, "case": name, "checks_passed": all(c.passed for c in integrity_checks(r)),
                     **{k: r.metrics.get(k) for k in KEY_METRICS}})
    return rows


def tornado(rows: list[dict], metric: str = "project_npv_post_subsidy") -> list[dict]:
    """Low and high value of one metric per input group, sorted by swing (largest first)."""
    base = rows[0][metric]
    groups: dict[str, list[float]] = {}
    for r in rows[1:]:
        if r[metric] is not None:
            groups.setdefault(r["group"], []).append(r[metric])
    out = [{"group": g, "low": min(v), "high": max(v), "base": base,
            "swing": (max(max(v), base) - min(min(v), base)) if base is not None else None} for g, v in groups.items()]
    return sorted(out, key=lambda x: -(x["swing"] or 0))


def minimum_capital_grant(base: ProjectInputs, *, min_dscr: float | None = 1.3, min_equity_irr: float | None = None,
                          max_grant: float | None = None, tol: float = 1.0, grid_points: int = 24) -> dict:
    """Smallest capital grant (LCY, same milestones as the base) at which the project meets the thresholds.

    Method: test zero first; scan a grid from zero to the maximum to find the first feasible grant; bisect between
    the last infeasible and the first feasible point; then confirm the answer and report whether feasibility was
    monotone over the grid. An equity IRR that cannot be computed because equity puts in almost nothing while
    receiving distributions counts as meeting any IRR target.
    """
    total_capex = float(run_model(base).series["capex"].sum())
    hi = max_grant if max_grant is not None else total_capex

    def ok(g: float) -> tuple[bool, ModelResult]:
        r = run_model(base, capital_grant_override=g)
        good = True
        if min_dscr is not None:
            no_debt = float(r.series["debt_service"].sum()) <= 1e-6
            good &= no_debt or (r.metrics["dscr_min"] is not None and r.metrics["dscr_min"] >= min_dscr)
        if min_equity_irr is not None:
            eirr = r.metrics["equity_irr"]
            if eirr is None:
                put_in = float((r.series["equity_contributions"] + r.series["equity_support"]).sum())
                got = float(r.series["distributions"].sum())
                good &= put_in <= max(1.0, 1e-6 * total_capex) and got > 0
            else:
                good &= eirr >= min_equity_irr
        return good, r

    conns = sum(c.connections_target for c in base.customers)

    def answer(g: float, r: ModelResult, reason: str, monotone: bool = True) -> dict:
        return {"feasible": True, "grant": float(g), "grant_per_connection": float(g) / conns if conns else None,
                "dscr_min": r.metrics["dscr_min"], "equity_irr": r.metrics["equity_irr"], "monotone": monotone, "reason": reason}

    good0, r0 = ok(0.0)
    if good0:
        return answer(0.0, r0, "Thresholds met without a capital grant")
    grid = [hi * k / grid_points for k in range(1, grid_points + 1)]
    flags = [ok(g)[0] for g in grid]
    if not any(flags):
        _, r_hi = ok(hi)
        return {"feasible": False, "grant": None, "grant_per_connection": None, "monotone": None,
                "reason": "Thresholds not met at any grant up to the maximum",
                "dscr_min_at_max": r_hi.metrics["dscr_min"], "equity_irr_at_max": r_hi.metrics["equity_irr"]}
    k = flags.index(True)
    monotone = all(flags[k:])
    lo, up = (grid[k - 1] if k > 0 else 0.0), grid[k]
    while up - lo > tol:
        mid = 0.5 * (lo + up)
        if ok(mid)[0]:
            up = mid
        else:
            lo = mid
    good, r = ok(up)
    out = answer(up, r, "Smallest grant meeting the thresholds (grid scan, bisection, checked)", monotone)
    out["feasible"] = good
    if not monotone:
        out["reason"] += "; warning: feasibility is not monotone in the grant, a larger grant fails somewhere"
    return out
