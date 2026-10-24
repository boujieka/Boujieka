"""Named, traceable results of a solved scenario.

Each KPI and series names the workbook cell or row it comes from ("source").
Indicators the workbook does not compute are marked ``derived=True``: they
are built only from reconciled rows but have no Excel value to compare with.
Per-lot results are ``experimental=True`` (the workbook blends lots, audit
observation 2).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from . import excel as X
from .assumptions import Assumptions
from .model import T, Ledger
from .options import FAITHFUL, EngineOptions
from .solver import SolveLog, solve

KPIS = {  # name: (source cell, unit, label)
    "project_irr": ("Model!E375", "%", "Project IRR (XIRR, incl. grant)"),
    "payback_years": ("Model!I378", "years", "Payback period"),
    "project_npv": ("Model!E376", "currency", "Project XNPV at WACC"),
    "project_npv_ex_purchases": ("Model!E392", "currency", "Project XNPV ex. grid purchases, incl. grant"),
    "npv_per_connection": ("Model!E394", "currency/connection", "NPV per connection"),
    "equity_irr_incl_grant": ("Model!E413", "%", "AssetCo equity XIRR incl. grant"),
    "equity_irr_excl_grant": ("Model!E418", "%", "AssetCo equity XIRR excl. grant"),
    "owner_irr_incl_grant": ("Model!E436", "%", "Owner XIRR incl. grant"),
    "owner_irr_excl_grant": ("Model!E441", "%", "Owner XIRR excl. grant"),
    "senior_debt": ("Inputs!E305", "currency", "Senior debt drawn"),
    "grant": ("Inputs!E270", "currency", "Grant to AssetCo"),
    "owner_equity": ("Inputs!E279", "currency", "Owner equity"),
    "total_funding": ("Inputs!E292", "currency", "Total funding requirement"),
    "dscr_capacity": ("Inputs!E300", "currency", "Debt capacity under DSCR sculpting"),
    "dsra_initial": ("Inputs!E371", "currency", "DSRA initial funding"),
    "mean_monthly_arpu": ("Dashboard!K34", "currency/month", "Mean monthly ARPU"),
    "mean_monthly_consumption": ("Dashboard!K35", "kWh/month", "Mean monthly consumption"),
    "avg_tariff": ("Dashboard!K36", "currency/kWh", "Average tariff (time weighted)"),
    "people_served": ("Inputs!E27", "people", "People served"),
    "connections": ("Inputs!E25", "connections", "Total connections"),
    "grids": ("Inputs!E24", "grids", "Number of grids"),
}

SERIES = {  # name: (source row, unit, label)
    "year": ("Model!11", "year", "Calendar year"),
    "construction_flag": ("Model!6", "flag", "Construction period"),
    "operations_flag": ("Model!7", "flag", "Operations period"),
    "operational_grids": ("Model!23", "grids", "Operational grids at year end"),
    "connections": ("Model!26", "connections", "Fully operational connections"),
    "consumption_kwh": ("Model!60", "kWh", "Customer consumption"),
    "gross_production_kwh": ("Model!33", "kWh", "Gross PV production"),
    "diesel_production_kwh": ("Model!609", "kWh", "Diesel production"),
    "revenue": ("Model!87", "currency", "Revenue"),
    "opco_fees": ("Model!121", "currency", "OpCo operating fee"),
    "diesel_cost": ("Model!124", "currency", "Diesel cost"),
    "admin_costs": ("Model!130", "currency", "Administrative costs"),
    "total_opex": ("Model!132", "currency", "Total opex"),
    "ebitda": ("FinStat!14", "currency", "EBITDA"),
    "depreciation": ("FinStat!16", "currency", "Depreciation"),
    "ebit": ("FinStat!17", "currency", "EBIT"),
    "interest": ("FinStat!20", "currency", "Senior interest (P&L)"),
    "ebt": ("FinStat!23", "currency", "EBT"),
    "npat": ("FinStat!28", "currency", "Net profit after tax"),
    "grid_purchases": ("Model!199", "currency", "Grid purchases"),
    "ongoing_capex": ("Model!276", "currency", "Ongoing capex"),
    "tax_paid": ("Model!287", "currency", "Tax paid"),
    "cfads": ("Model!291", "currency", "Cash flow available for debt service"),
    "senior_interest": ("Model!305", "currency", "Senior interest paid"),
    "senior_principal": ("Model!306", "currency", "Senior principal repaid"),
    "senior_debt_balance": ("Debt!34", "currency", "Senior debt balance c/f"),
    "refi_debt_balance": ("Debt!77", "currency", "Refinanced debt balance c/f"),
    "dsra_balance": ("Debt!198", "currency", "DSRA balance c/f"),
    "mmra_balance": ("Debt!121", "currency", "MMRA balance c/f"),
    "distributions": ("Model!405", "currency", "Distributions net of WHT"),
    "project_cash_flow": ("Model!365", "currency", "Project cash flow"),
    "cash_balance": ("FinStat!135", "currency", "Cash balance c/f"),
    "total_assets_current": ("FinStat!44", "currency", "Current assets"),
    "fixed_assets": ("FinStat!48", "currency", "Fixed assets"),
    "liabilities": ("FinStat!58", "currency", "Liabilities"),
    "net_assets": ("FinStat!60", "currency", "Net assets"),
    "equity": ("FinStat!65", "currency", "Equity"),
    "balance_check": ("FinStat!67", "currency", "Balance sheet check (0 = OK)"),
}

CHECKS = {
    "balance_sheet_balances": "Dashboard!K42", "equity_required": "Dashboard!K43",
    "senior_debt_repaid": "Dashboard!K44", "funding_optimised": "Dashboard!K45",
    "senior_debt_sized": "Dashboard!K46", "refi_debt_repaid": "Dashboard!K47",
    "refi_debt_sized": "Dashboard!K48", "no_additional_equity": "Dashboard!K49",
    "no_equity_injection": "Dashboard!K50", "grids_built": "Dashboard!K51",
    "mmra_end_balance": "Dashboard!K52", "dsra_funded": "Dashboard!K53",
}


CHECK_TOLERANCE = 1e-6


@dataclass
class Indicator:
    value: float | None
    unit: str
    label: str
    source: str
    derived: bool = False
    experimental: bool = False


@dataclass
class Series:
    values: list
    unit: str
    label: str
    source: str
    derived: bool = False


@dataclass
class ScenarioResult:
    status: str                      # "reconciled-engine" or "variant"
    options: list[str]
    solver: dict
    kpis: dict[str, Indicator]
    series: dict[str, Series]
    checks: dict[str, float]
    failed_checks: list[str]
    pasted_values: dict
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


def _cell(L: Ledger, ref: str):
    sh, addr = ref.split("!")
    if addr.startswith("I") and addr[1:].isdigit():
        return L.totals.get(f"{sh}!{addr[1:]}")
    return L.s.get(ref)


def _derived(a: Assumptions, L: Ledger) -> tuple[dict, dict]:
    v = L.v
    cfads = v["Model!291"]
    ds = [-(v["Model!305"][t] + v["Model!306"][t] + v["Model!310"][t] + v["Model!311"][t]) for t in range(T)]
    dscr = [cfads[t] / ds[t] if ds[t] > 1e-9 else None for t in range(T)]
    repaying = [t for t in range(T) if v["Debt!23"][t] == 1 and ds[t] > 1e-9]
    grace = [t for t in range(T) if v["Debt!22"][t] == 1 and ds[t] > 1e-9]
    kp, se = {}, {}
    se["dscr"] = Series(dscr, "x", "DSCR = CFADS / (senior + refinanced debt service)", "Model!291 / Model!305:311", True)
    vals = [dscr[t] for t in repaying]
    kp["min_dscr_repayment"] = Indicator(min(vals) if vals else None, "x", "Minimum DSCR over repayment years",
                                         "derived from Model!291, Model!305:311", True)
    kp["avg_dscr_repayment"] = Indicator(sum(vals) / len(vals) if vals else None, "x",
                                         "Average DSCR over repayment years", "derived", True)
    gv = [dscr[t] for t in grace]
    kp["min_dscr_grace"] = Indicator(min(gv) if gv else None, "x", "Minimum DSCR during grace period", "derived", True)
    # LLCR at the start of the first repayment year: NPV(CFADS over remaining tenor at the debt rate) / opening debt
    if repaying:
        t0 = repaying[0]
        rate = v["Debt!45"][t0]
        last = max(repaying)
        npv = X.npv(rate, cfads[t0:last + 1])
        opening = v["Debt!30"][t0]
        kp["llcr_first_repayment"] = Indicator(npv / opening if opening else None, "x",
                                               "LLCR at first repayment year (NPV of CFADS at the debt rate / opening debt)",
                                               "derived", True)
    covenant = a.debt.target_dscr
    se["dscr_below_target"] = Series([1 if (d is not None and t in repaying and d < covenant - 1e-9) else 0
                                      for t, d in enumerate(dscr)], "flag",
                                     f"DSCR below target {covenant:.2f}x in a repayment year", "derived", True)
    # unlevered, pre-tax project cash flow (no grant, no tax, no financing)
    unlev = [v["Model!358"][t] + v["Model!360"][t] + v["Model!361"][t] + v["Model!362"][t] + v["Model!363"][t]
             for t in range(T)]
    flags = v["Model!368"]
    cf = [-1e-7] + [unlev[t] * flags[t] for t in range(T)]
    dates = [L.s["Inputs!E6"]] + list(v["Model!5"])
    kp["project_irr_unlevered_pretax"] = Indicator(X.iferror(lambda: X.xirr(cf, dates), None), "%",
                                                   "Unlevered pre-tax project IRR (no grant, no tax)", "derived", True)
    cfg = [-1e-7] + [(unlev[t] + v["Model!231"][t]) * flags[t] for t in range(T)]
    kp["project_irr_unlevered_pretax_grant"] = Indicator(X.iferror(lambda: X.xirr(cfg, dates), None), "%",
                                                         "Unlevered pre-tax project IRR incl. grant", "derived", True)
    return kp, se


def build_result(a: Assumptions, L: Ledger, log: SolveLog, options: EngineOptions = FAITHFUL) -> ScenarioResult:
    kpis = {k: Indicator(_cell(L, ref), unit, label, ref) for k, (ref, unit, label) in KPIS.items()}
    series = {k: Series(list(L.v[ref]), unit, label, ref) for k, (ref, unit, label) in SERIES.items()}
    dk, ds = _derived(a, L)
    kpis.update(dk)
    series.update(ds)
    checks = {k: L.s[ref] for k, ref in CHECKS.items()}
    # checks are sums of opposite flows: residues below 1e-6 are floating-point noise
    failed = [k for k, val in checks.items() if abs(val) > CHECK_TOLERANCE]
    warnings = []
    if not options.faithful:
        warnings.append("Variant run: options " + ", ".join(options.enabled()) + " depart from the reference workbook.")
    if log.method != "excel_macros":
        warnings.append("Exact solver: sizing differs from Excel by up to the macros' tolerance (50,000).")
    if failed:
        warnings.append("Workbook checks not passed: " + ", ".join(failed))
    mind = dk.get("min_dscr_repayment")
    if mind and mind.value is not None and mind.value < a.debt.target_dscr - 1e-9:
        warnings.append(f"Derived DSCR falls to {mind.value:.2f}x in a repayment year, below the "
                        f"{a.debt.target_dscr:.2f}x target (the workbook has no DSCR covenant test).")
    if min(L.v["Debt!34"]) < -1:
        warnings.append("Senior debt balance becomes negative: the workbook repays more than is owed "
                        "(Debt!32 is not capped). Option cap_principal_at_balance prevents it.")
    if min(L.v["Debt!77"]) < -1:
        warnings.append("Refinanced debt balance becomes negative.")
    status = "reconciled-engine" if options.faithful and log.method == "excel_macros" else "variant"
    return ScenarioResult(status=status, options=options.enabled(),
                          solver={"method": log.method, "converged": log.converged, "rounds": log.rounds,
                                  "runs": log.runs, "steps": log.steps},
                          kpis=kpis, series=series, checks=checks, failed_checks=failed,
                          pasted_values={"funding": a.pasted.funding, "dscr_limit": a.pasted.dscr_limit,
                                         "refi_limit": a.pasted.refi_limit, "dsra_initial": a.pasted.dsra_initial},
                          warnings=warnings)


def run_scenario(a: Assumptions, method: str = "excel_macros", options: EngineOptions = FAITHFUL,
                 per_lot: bool = False) -> ScenarioResult:
    from .validation import ValidationError, validate
    issues = validate(a)
    errors = [i for i in issues if i.level == "error"]
    if errors:
        raise ValidationError(errors)
    solved, L, log = solve(a, method, options)
    res = build_result(solved, L, log, options)
    res.warnings.extend(f"{i.field}: {i.message}" for i in issues if i.level == "warning")
    if per_lot:
        res.kpis.update(lot_irrs(a, method, options))
    return res


def lot_irrs(a: Assumptions, method: str = "excel_macros", options: EngineOptions = FAITHFUL) -> dict:
    """Experimental: each included lot run alone (other lots excluded), giving
    the batch-level project IRR the PSA Asset Transfer term sheet refers to.
    Financing is re-sized for the lot alone; no Excel reference exists."""
    out = {}
    for i, lot in enumerate(a.lots):
        if lot.included != 1 or not lot.grids:
            continue
        b = a.replace()
        for j, other in enumerate(b.lots):
            other.included = 1 if j == i else 0
        try:
            solved, L, _ = solve(b, method, options)
            val = L.s["Model!E375"]
        except Exception as exc:  # noqa: BLE001 - reported, not hidden
            val = None
            out[f"lot_{i + 1}_error"] = Indicator(None, "", f"{lot.name}: {exc}", "experimental", True, True)
        out[f"lot_{i + 1}_project_irr"] = Indicator(val, "%", f"Project IRR of {lot.name} alone", "experimental",
                                                    True, True)
    return out
