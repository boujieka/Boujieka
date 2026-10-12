"""Integrity checks, warnings and the model status.

A model is VALIDATED only when every integrity check passes, no warning is raised, the inputs are complete and a
named person has reviewed the assumptions. Running without errors is not validation.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from .finance import npv
from .inputs import Provenance, missing_inputs
from .model import ModelResult

REL_TOL = 1e-9  # residual allowed, as a share of the largest balance sheet total (floating point only)


class ModelStatus(str, Enum):
    VALIDATED = "validated"
    WARNING = "warning"
    FAILED_CHECKS = "failed_checks"
    INCOMPLETE_INPUTS = "incomplete_inputs"


@dataclass
class Check:
    code: str
    label: str
    passed: bool
    detail: str = ""


def _max_abs(x: np.ndarray) -> float:
    return float(np.max(np.abs(x))) if len(x) else 0.0


def integrity_checks(r: ModelResult) -> list[Check]:
    S, C, T = r.series, r.C, r.T
    scale = max(float(np.max(np.abs(S["total_assets"]))), 1.0)
    out: list[Check] = []

    tol = max(1e-6, REL_TOL * scale)

    def add(code: str, label: str, residual: float, detail: str = "", tolerance: float | None = None) -> None:
        lim = tol if tolerance is None else tolerance
        out.append(Check(code, label, residual <= lim, detail or f"max residual {residual:.3g}"))

    su = r.sources_uses
    add("SU", "Sources equal uses at COD (plus cash held at COD)",
        abs(su["sources_total"] - su["uses_total"] - su["cash_at_cod"]))
    # recomputed from the components, never read from a stored difference
    bs = (S["cash"] + S["dsra"] + S["mra"] + S["nbv"]) - (S["debt_balance"] + S["deferred_grant"]) \
        - (S["paid_in_capital"] + S["retained_earnings"])
    add("BS", "Balance sheet balances in every quarter", _max_abs(bs))
    open_cash = np.concatenate([[0.0], S["cash"][:-1]])
    add("CASH", "Cash roll forward: opening + net cash flow = closing", _max_abs(open_cash + S["net_cash_flow"] - S["cash"]))
    for tr in r.tranches:
        b = tr["balance"]
        ob = np.concatenate([[0.0], b[:-1]])
        res = ob + tr["draws"] - tr["principal"] - tr["prepayment"] + tr["fx_loss"] - b
        add(f"DEBT:{tr['name']}", f"Debt roll forward ({tr['name']})", _max_abs(res))
        add(f"REPAID:{tr['name']}", f"Debt fully repaid by the end of the horizon ({tr['name']})", abs(float(b[-1])))
    nbv = S["nbv"]
    onbv = np.concatenate([[0.0], nbv[:-1]])
    disp_nb = S["disposal_proceeds"] - S["disposal_gain"]
    add("FA", "Fixed asset roll forward", _max_abs(onbv + S["asset_additions"] - S["depreciation"] - disp_nb - nbv))
    dg = S["deferred_grant"]
    odg = np.concatenate([[0.0], dg[:-1]])
    add("GRANT", "Deferred grant roll forward", _max_abs(odg + S["grant_receipts"] + S["rbf_receipts"] - S["grant_income"] - dg))
    add("DSRA", "Reserve account equals its target", _max_abs(S["dsra"] - S["dsra_target"]))
    add("MRA", "Maintenance reserve never negative and fully used at each replacement",
        max(max(0.0, -float(np.min(S["mra"]))), _max_abs(np.where(S["replacement_capex"] > 0, S["mra"], 0.0))))
    add("NEGCASH", "No negative unrestricted cash", max(0.0, -float(np.min(S["cash"]))))
    add("ENERGY", "Energy balance: supplied + unserved = demand, supplied within capacity",
        max(_max_abs(S["supplied_kwh"] + S["unserved_kwh"] - S["demand_kwh"]),
            max(0.0, float(np.max(S["supplied_kwh"] - S["capacity_customer_kwh"])))))
    add("COLL", "Collections never exceed billing", max(0.0, float(np.max(S["collections"] - S["revenue"]))))
    sub = r.inputs.subsidies
    if sub.rbf_cap is not None:
        add("RBFCAP", "RBF receipts within the programme cap", max(0.0, float(S["rbf_receipts"].sum()) - sub.rbf_cap))
    add("RBFVER", "RBF receipts never exceed verified connections x rate",
        max(0.0, float(np.max(np.cumsum(S["rbf_receipts"]) - np.cumsum(S["new_connections"]) * sub.rbf_per_connection))))
    for code, key in (("IRRP", "project_irr_pre_subsidy"), ("IRRE", "equity_irr")):
        v = r.metrics.get(key)
        cf = S["project_cf_pre_subsidy"] if code == "IRRP" else S["equity_cf"]
        if v is not None:
            resid = abs(npv((1 + v) ** 0.25 - 1, cf)) / max(float(np.sum(np.abs(cf))), 1.0)
            add(code, f"NPV at the reported IRR is zero ({key})", resid, tolerance=1e-8)
    return out


def warnings(r: ModelResult) -> list[Check]:
    M, p = r.metrics, r.inputs
    w: list[Check] = []

    def warn(code: str, cond: bool, label: str, detail: str = "") -> None:
        if cond:
            w.append(Check(code, label, False, detail))

    warn("W_DSCR", M["dscr_min"] is not None and M["dscr_min"] < p.financing.lockup_dscr,
         "Minimum annual DSCR is below the lock-up level", f"min DSCR {M['dscr_min']:.2f}x" if M["dscr_min"] is not None else "")
    warn("W_SUPPORT", M["equity_support_total"] > 1.0, "Equity support is needed after COD (liquidity shortfall)",
         f"{M['equity_support_total']:,.0f} LCY in total")
    warn("W_UNSERVED", (M["unserved_share"] or 0) > 0.05, "More than 5% of demand is not served", f"{(M['unserved_share'] or 0):.1%}")
    warn("W_AFFORD", (M["max_bill_to_income"] or 0) > 0.10, "A customer class pays more than 10% of income (model policy threshold)",
         f"{(M['max_bill_to_income'] or 0):.1%}")
    warn("W_IRR", M["equity_irr"] is None, "Equity IRR cannot be computed (no sign change in equity cash flows)")
    warn("W_GRID", p.grid_arrival.enabled and not p.grid_arrival.regulatory_source, "Grid arrival treatment has no cited regulation")
    warn("W_PROV", p.provenance == Provenance.ILLUSTRATIVE, "Inputs are illustrative demo data", "Not for investment decisions")
    return w


def status(r: ModelResult) -> tuple[ModelStatus, list[Check], list[Check], list[str]]:
    miss = missing_inputs(r.inputs)
    checks = integrity_checks(r)
    warns = warnings(r)
    if miss:
        st = ModelStatus.INCOMPLETE_INPUTS
    elif not all(c.passed for c in checks):
        st = ModelStatus.FAILED_CHECKS
    elif warns or r.inputs.review is None:
        st = ModelStatus.WARNING
    else:
        st = ModelStatus.VALIDATED
    if r.inputs.review is None and not miss and all(c.passed for c in checks):
        warns = warns + [Check("W_REVIEW", False, "Assumptions not yet reviewed by a named person", "Required for VALIDATED status")]
    return st, checks, warns, miss
