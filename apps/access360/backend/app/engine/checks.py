"""Integrity checks, warnings and the model status.

A model is VALIDATED only when every integrity check passes, no warning is raised, the inputs are complete and a
named person has reviewed the assumptions. Running without errors is not validation.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from .finance import annuity_payment, npv, q_rate
from .inputs import Provenance, missing_inputs
from .model import ModelResult, tax_with_losses

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
        out.append(Check(code, label, bool(residual <= lim), detail or f"max residual {float(residual):.3g}"))

    su = r.sources_uses
    add("SU", "Sources equal uses at COD (plus cash held at COD)",
        abs(su["sources_total"] - su["uses_total"] - su["cash_at_cod"]))
    # recomputed from the components, never read from a stored difference
    bs = (S["cash"] + S["dsra"] + S["mra"] + S["nbv"] + S["receivables"]) - (S["debt_balance"] + S["deferred_grant"] + S["payables"]) \
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
    add("DSRA", "Reserve account between zero and its target; full whenever a distribution is paid",
        max(max(0.0, float(np.max(S["dsra"] - S["dsra_target"]))), max(0.0, -float(np.min(S["dsra"]))),
            float(np.max(np.where(S["distributions"][:-1] > 0, np.abs(S["dsra"][:-1] - S["dsra_target"][:-1]), 0.0)))))
    add("MRA", "Maintenance reserve never negative and fully used at each replacement",
        max(max(0.0, -float(np.min(S["mra"]))), _max_abs(np.where(S["replacement_capex"] > 0, S["mra"], 0.0))))
    add("NEGCASH", "No negative unrestricted cash", max(0.0, -float(np.min(S["cash"]))))
    add("ENERGY", "Energy balance: supplied + unserved = demand, supplied within capacity",
        max(_max_abs(S["supplied_kwh"] + S["unserved_kwh"] - S["demand_kwh"]),
            max(0.0, float(np.max(S["supplied_kwh"] - S["capacity_customer_kwh"])))))
    add("COLL", "Cumulative collections never exceed cumulative billing",
        max(0.0, float(np.max(np.cumsum(S["collections"]) - np.cumsum(S["revenue"])))))
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
    out += recomputation_checks(r, tol)
    return out


def recomputation_checks(r: ModelResult, tol: float) -> list[Check]:
    """Independent recomputation of key lines from inputs and primitive series. The roll forwards above cannot see
    an error that keeps double entry consistent (interest at the wrong rate, tax charged twice, a doubled subsidy);
    these checks recompute such lines another way and compare."""
    p, S, C, T, I = r.inputs, r.series, r.C, r.T, r.internals
    out: list[Check] = []
    t = np.arange(T)
    active = S["active"] > 0.5

    def add(code, label, resid, lim=None):
        lim = tol if lim is None else lim
        out.append(Check(code, label, bool(resid <= lim), f"max residual {float(resid):.3g}"))

    fx = S["fx"]
    # interest = opening balance x quarterly rate, per tranche, in the tranche currency
    for tr_in, tr in zip(p.financing.debt, r.tranches):
        rf = fx if tr_in.currency == "USD" else np.ones(T)
        open_ccy = np.concatenate([[0.0], tr["balance"][:-1] / rf[:-1]])
        exp = open_ccy * q_rate(tr_in.rate_pa) * rf
        add(f"R_INT:{tr_in.name}", f"Interest recomputed from opening balance and rate ({tr_in.name})", _max_abs(exp - tr["interest"]))
        n_amort = max(int(round(tr_in.tenor_years * 4)) - tr_in.grace_quarters, 1)
        first = C + tr_in.grace_quarters
        maturity = C + int(round(tr_in.tenor_years * 4)) - 1
        amort = np.nonzero(tr["principal"] > 1e-9)[0]
        if len(amort) and not I["closes"]:
            add(f"R_MAT:{tr_in.name}", f"Final repayment falls at the stated maturity ({tr_in.name})", float(abs(int(amort[-1]) - maturity)), 0.0)
        if tr_in.amortisation == "annuity" and first < T and open_ccy[first] > 1e-9:
            pay = annuity_payment(open_ccy[first], q_rate(tr_in.rate_pa), n_amort)
            ds_ccy = (tr["interest"] + tr["principal"]) / rf
            body = [i for i in amort if i < maturity and (not I["closes"] or i < I["t_arr"])]
            if body:
                add(f"R_ANN:{tr_in.name}", f"Annuity instalment recomputed from the balance at the end of grace ({tr_in.name})",
                    float(np.max(np.abs(ds_ccy[body] - pay))), max(1e-6, 1e-9 * pay))
    # operating lines recomputed from primitives
    tech, opx, sub = p.technical, p.opex, p.subsidies
    fuel = S["generated_kwh"] * tech.diesel_share * tech.diesel_cost_per_kwh * I["cost_idx"]
    add("R_FUEL", "Fuel cost recomputed from generation, diesel share and price", _max_abs(fuel - S["fuel"]))
    ts_on = active & ((t - C) < sub.tariff_support_years * 4)
    ts = np.where(ts_on, S["billed_kwh"] * sub.tariff_support_per_kwh, 0.0)
    add("R_TS", "Tariff support recomputed from billed energy and rate", _max_abs(ts - S["tariff_support"]))
    billed = S["energy_revenue"] + S["fixed_revenue"]
    collectable = billed * opx.collection_efficiency
    rec = np.where(active, collectable * opx.receivable_days / (365.0 / 4.0), 0.0)
    add("R_COLL", "Collections recomputed from billing, collection efficiency and receivable days",
        _max_abs(collectable - np.diff(np.concatenate([[0.0], rec])) + S["connection_fee_revenue"] - S["collections"]))
    pay = np.where(active, S["opex"] * opx.payable_days / (365.0 / 4.0), 0.0)
    add("R_WC", "Receivable and payable balances recomputed", max(_max_abs(rec - S["receivables"]), _max_abs(pay - S["payables"])))
    ebitda = S["revenue"] + S["tariff_support"] - S["opex"] - S["bad_debt"]
    add("R_EBITDA", "EBITDA recomputed from its lines", _max_abs(ebitda - S["ebitda"]))
    # tax recomputed from the components of taxable income with a loss pool
    m = p.macro
    ebt = S["ebitda"] + S["grant_income"] - S["depreciation"] - S["interest_expense"] - S["fx_loss"] + S["disposal_gain"]
    taxable = ebt - (0.0 if m.grant_income_taxable else S["grant_income"])
    add("R_TAX", "Tax recomputed from taxable income and the loss pool", _max_abs(tax_with_losses(taxable, m.tax_rate) - S["tax"]))
    add("R_NI", "Net income recomputed", _max_abs(ebt - S["tax"] - S["net_income"]))
    # depreciation recomputed from the input lives (physical assets, before disposal)
    dep = np.zeros(T)
    sched = [(spend, it.asset_life_years) for it, spend in I["capex_items"]]
    sched += [(S["battery_replacement"], tech.battery_life_years)] + list(I["item_replacements"]) + [I["fin_vintage"]]
    for spend, life in sched:
        n = max(int(round(life * 4)), 1)
        for i in np.nonzero(spend > 0)[0]:
            st = max(i + 1, C)
            dep[st:min(st + n, T)] += spend[i] / n
    dep = np.where(active, dep, 0.0)
    nbv_open = np.concatenate([[0.0], S["nbv"][:-1]]) + S["asset_additions"]
    dep = np.minimum(dep, nbv_open)
    add("R_DEP", "Depreciation recomputed from input asset lives", _max_abs(dep - S["depreciation"]))
    # DSRA target recomputed from the tranche schedules
    nq = p.financing.dsra_quarters
    ds = np.zeros(T)
    for tr in r.tranches:
        ds += np.where(t >= C, tr["interest"], 0.0) + tr["principal"]
    if I["closes"]:
        ds[I["t_arr"]] = 0.0
    target = np.array([ds[i + 1:i + 1 + nq].sum() if nq else 0.0 for i in range(T)])
    if I["closes"]:
        target[I["t_arr"]:] = 0.0
    add("R_DSRA", "DSRA target recomputed from the debt schedules", _max_abs(target - S["dsra_target"]))
    shortfall = (S["dsra"] < S["dsra_target"] - 1e-6) & (t >= C)
    add("R_DSRADRAW", "The reserve is below target only when cash is at the minimum and nothing is distributed",
        float(np.sum(np.where(shortfall, S["distributions"] + np.maximum(S["cash"] - p.financing.min_cash, 0.0) * (t < T - 1), 0.0))))
    for tr_in, tr in zip(p.financing.debt, r.tranches):
        if tr.get("sculpted") and tr.get("sculpt_ds") is not None and r.metrics.get("sculpt_converged"):
            first, last = C + tr_in.grace_quarters, C + int(round(tr_in.tenor_years * 4)) - 2
            ds_s = (tr["interest"] + tr["principal"])[first:last + 1]
            other = S["debt_service"][first:last + 1] - ds_s
            room = np.maximum(S["cfads"][first:last + 1], 0.0) / p.financing.target_dscr - other
            # the sculpted tranche pays a constant share k <= 1 of the room left at the target DSCR
            # (k = 1 unless its gearing cap binds), wherever that room is positive
            mask = room > 1e-6 * max(float(np.max(np.abs(room))), 1.0)
            ratio = ds_s[mask] / room[mask]
            if len(ratio):
                add(f"R_SCULPT:{tr_in.name}", f"Total debt service proportional to CFADS, DSCR at or above the target where the sculpted tranche pays ({tr_in.name})",
                    max(float(np.max(ratio) - np.min(ratio)), max(0.0, float(np.max(ratio)) - 1.0)), 1e-4)
    # lock up: no distribution in a quarter whose DSCR is below the lock up level (except the last quarter)
    dq = S["dscr_quarter"]
    locked = (~np.isnan(dq)) & (dq < p.financing.lockup_dscr) & (t < T - 1)
    add("R_LOCK", "No distribution while the DSCR is below the lock up level", float(np.sum(S["distributions"][locked])))
    # grant income recomputed: receipts deferred and released over the remaining weighted asset life
    gi = np.zeros(T)
    bal = 0.0
    wq = int(round(I["w_life"] * 4))
    for i in range(T):
        base_g = bal + S["grant_receipts"][i] + S["rbf_receipts"][i]
        rel = base_g / max(wq - (i - C), 1) if (i >= C and base_g > 1e-12) else 0.0
        if (I["closes"] and i == I["t_arr"]) or (i == T - 1 and S["disposal_proceeds"][i] > 0):
            rel = base_g
        gi[i] = rel
        bal = base_g - rel
    add("R_GRANTINC", "Grant income recomputed from receipts and the weighted asset life", _max_abs(gi - S["grant_income"]))
    # project cash flows recomputed from primitives
    capex = S["capex"]
    op = t >= C
    base = np.where(t < C, -capex, 0.0) + np.where(op, S["collections"] - S["cash_opex"] - S["replacement_capex"], 0.0) + S["disposal_proceeds"]
    pre_tax = tax_with_losses(S["ebitda"] - S["tariff_support"] - S["unlevered_depreciation"] + S["disposal_gain"], m.tax_rate)
    add("R_PCF", "Project cash flow before subsidy recomputed (no subsidy, no tax on subsidy)",
        _max_abs(base - pre_tax - S["project_cf_pre_subsidy"]))
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
         f"{M['equity_support_total']:,.0f} {p.currency} in total")
    warn("W_UNSERVED", (M["unserved_share"] or 0) > 0.05, "More than 5% of demand is not served", f"{(M['unserved_share'] or 0):.1%}")
    warn("W_AFFORD", (M["max_bill_to_income"] or 0) > 0.10, "A customer class pays more than 10% of income (model policy threshold)",
         f"{(M['max_bill_to_income'] or 0):.1%}")
    warn("W_IRR", M["equity_irr"] is None, "Equity IRR cannot be computed (no sign change in equity cash flows)")
    warn("W_GRID", p.grid_arrival.enabled and not p.grid_arrival.regulatory_source, "Grid arrival treatment has no cited regulation")
    warn("W_GRANT", abs(M.get("capital_grant_undisbursed") or 0.0) > 1.0,
         "Part of the capital grant is never disbursed (operations end first); debt was sized on the full grant",
         f"{M.get('capital_grant_undisbursed', 0):,.0f} {p.currency} undisbursed")
    warn("W_CLOSE", M.get("closure_cover") is not None and M["closure_cover"] < 1.0,
         "At grid closure, cash and compensation do not cover the debt prepayment", f"cover {M.get('closure_cover') or 0:.2f}x")
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
        warns = warns + [Check("W_REVIEW", "Assumptions not yet reviewed by a named person", False, "Required for VALIDATED status")]
    return st, checks, warns, miss
