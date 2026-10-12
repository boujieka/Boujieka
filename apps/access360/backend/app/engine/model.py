"""ACCESS FINANCE: deterministic quarterly project finance engine for a mini grid site or site batch.

Order of calculation (no circularity): timeline -> demand and energy -> revenue and opex -> capex and assets ->
debt schedules (independent of cash) -> subsidies -> tax -> cash waterfall -> statements -> metrics -> checks.

Simplifications, all documented in docs/financial-engine-spec.md:
* the energy balance takes the deliverable energy from the hourly design study; it does not dispatch;
* revenue is billed and collected in the same quarter; the uncollected share is a bad debt in that quarter;
* interest during construction and upfront fees are paid by equity and capitalised;
* capital grants and RBF receipts are held as deferred income and released over the weighted asset life.

This is an analytical modelling treatment and does not constitute a determination of the applicable accounting
treatment under IFRS.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

import numpy as np

from .finance import annualise, annuity_payment, irr, npv, q_rate
from .inputs import CapexCategory, ProjectInputs

EPS = 1e-6


def _add_months(d: date, months: int) -> date:
    y, m = divmod(d.month - 1 + months, 12)
    return date(d.year + y, m + 1, 1)


@dataclass
class ModelResult:
    inputs: ProjectInputs
    T: int
    C: int
    dates: list[date]
    series: dict[str, np.ndarray] = field(default_factory=dict)
    metrics: dict[str, float | None] = field(default_factory=dict)
    annual: dict[str, list[float]] = field(default_factory=dict)
    sources_uses: dict[str, float] = field(default_factory=dict)
    tranches: list[dict] = field(default_factory=list)

    def s(self, k: str) -> np.ndarray:
        return self.series[k]


def run_model(p: ProjectInputs, *, tariff_multiplier: float = 1.0, capital_grant_override: float | None = None) -> ModelResult:
    C = p.construction_quarters
    Q = p.operating_years * 4
    T = C + Q
    t = np.arange(T, dtype=float)
    q = t - C  # operating quarter index (negative during construction)
    op = q >= 0
    dates = [_add_months(p.financial_close, 3 * i) for i in range(T)]
    S: dict[str, np.ndarray] = {}

    def z() -> np.ndarray:
        return np.zeros(T)

    m = p.macro
    fx = m.fx_lcy_per_usd * (1.0 + m.fx_depreciation_pa) ** (t / 4.0)
    qq = np.maximum(q, 0)
    cost_idx = (1.0 + m.inflation_pa) ** (qq / 4.0)
    tariff_idx = (1.0 + m.inflation_pa * m.tariff_indexation) ** (qq / 4.0)
    S["fx"] = fx

    # ---------------------------------------------------------------- grid arrival
    ga = p.grid_arrival
    t_arr = C + (ga.operating_year - 1) * 4 if ga.enabled else T + 1
    closes = ga.enabled and ga.treatment in ("asset_transfer", "stranded") and t_arr < T
    active = op & (t < t_arr) if closes else op.copy()
    after_ic = (t >= t_arr) & op if (ga.enabled and ga.treatment == "interconnect") else np.zeros(T, dtype=bool)
    tariff_factor = np.where(after_ic, ga.tariff_factor_after, 1.0)
    demand_factor = np.where(after_ic, ga.demand_factor_after, 1.0)
    S["active"] = active.astype(float)

    # ---------------------------------------------------------------- connections and demand
    conn_total, new_total, demand_total = z(), z(), z()
    per_class: list[dict[str, np.ndarray]] = []
    for c in p.customers:
        ramp = np.clip((q - c.start_quarter + 1) / c.ramp_quarters, 0.0, 1.0)
        conn = np.where(active, c.connections_target * ramp, 0.0)
        new = np.diff(np.concatenate([[0.0], conn]))
        new = np.maximum(new, 0.0)
        kwh = conn * c.kwh_per_connection_month * 3.0 * (1.0 + c.demand_growth_pa) ** (qq / 4.0) * demand_factor
        per_class.append({"conn": conn, "new": new, "demand": kwh})
        conn_total += conn
        new_total += new
        demand_total += kwh
    S["connections"], S["new_connections"], S["demand_kwh"] = conn_total, new_total, demand_total

    tech = p.technical
    cap_customer = np.where(active, tech.deliverable_energy_kwh_pa / 4.0 * (1.0 - tech.technical_loss), 0.0)
    supplied = np.minimum(demand_total, cap_customer)
    generated = np.where(active, supplied / (1.0 - tech.technical_loss), 0.0)
    unserved = demand_total - supplied
    billed_kwh = supplied * (1.0 - tech.commercial_loss)
    share = np.divide(supplied, demand_total, out=np.zeros(T), where=demand_total > EPS)
    S.update(supplied_kwh=supplied, generated_kwh=generated, unserved_kwh=unserved, billed_kwh=billed_kwh,
             capacity_customer_kwh=cap_customer)

    # ---------------------------------------------------------------- revenue
    energy_rev, fixed_rev, fee_rev = z(), z(), z()
    for c, pc in zip(p.customers, per_class):
        cls_billed = pc["demand"] * share * (1.0 - tech.commercial_loss)
        energy_rev += cls_billed * c.tariff_per_kwh * tariff_idx * tariff_factor * tariff_multiplier
        fixed_rev += pc["conn"] * c.fixed_charge_month * 3.0 * tariff_idx * tariff_factor * tariff_multiplier
        fee_rev += pc["new"] * c.connection_fee * tariff_idx
    billed = energy_rev + fixed_rev
    collected = billed * p.opex.collection_efficiency
    bad_debt = billed - collected
    sub = p.subsidies
    ts_active = active & (q < sub.tariff_support_years * 4)
    tariff_support = np.where(ts_active, billed_kwh * sub.tariff_support_per_kwh, 0.0)
    revenue = billed + fee_rev
    S.update(energy_revenue=energy_rev, fixed_revenue=fixed_rev, connection_fee_revenue=fee_rev, revenue=revenue,
             collections=collected + fee_rev, bad_debt=bad_debt, tariff_support=tariff_support)

    # ---------------------------------------------------------------- capex and assets
    capex_init, capex_items = z(), []
    for it in p.capex:
        spend = np.where(t < C, it.amount / C, 0.0)
        if it.currency == "USD":
            spend = spend * fx
        capex_items.append((it, spend))
        capex_init += spend
    total_capex = float(capex_init.sum())

    repl = z()
    if tech.battery_kwh > 0 and tech.battery_replacement_usd_per_kwh > 0:
        step = int(round(tech.battery_life_years * 4))
        k = 1
        while step > 0 and C + k * step < T:
            tt = C + k * step
            if active[tt]:
                yrs = (tt - C) / 4.0
                repl[tt] = tech.battery_kwh * tech.battery_replacement_usd_per_kwh * (1.0 - tech.battery_cost_decline_pa) ** yrs * fx[tt]
            k += 1
    S["capex"], S["replacement_capex"] = capex_init, repl
    # maintenance reserve: each replacement is pre-funded evenly from the previous replacement (or COD)
    mra_in, mra_out = z(), z()
    if p.financing.maintenance_reserve:
        prev = C
        for tt in np.nonzero(repl > 0)[0]:
            n = max(int(tt - prev), 1)
            mra_in[prev:tt] += repl[tt] / n
            mra_out[tt] += repl[tt]
            prev = int(tt) + 1
    S["mra_contribution"], S["mra_release"] = mra_in, mra_out

    opx = p.opex
    opex_fixed = np.where(active, opx.fixed_pa / 4.0 * cost_idx, 0.0)
    opex_var = np.where(active, opx.per_connection_pa / 4.0 * conn_total * cost_idx, 0.0)
    insurance = np.where(active, opx.insurance_pct_capex * total_capex / 4.0 * cost_idx, 0.0)
    fuel = generated * tech.diesel_share * tech.diesel_cost_per_kwh * cost_idx
    opex = opex_fixed + opex_var + insurance + fuel
    S.update(opex_fixed=opex_fixed, opex_per_connection=opex_var, insurance=insurance, fuel=fuel, opex=opex)
    ebitda = revenue + tariff_support - opex - bad_debt
    S["ebitda"] = ebitda

    # ---------------------------------------------------------------- debt schedules (independent of the cash waterfall)
    fin = p.financing
    grant_total = sub.capital_grant if capital_grant_override is None else capital_grant_override
    debt_base = total_capex - (grant_total if fin.debt_basis == "capex_net_of_grant" else 0.0)
    debt_base = max(debt_base, 0.0)
    spend_share = capex_init / total_capex if total_capex > EPS else z()
    tranche_out = []
    debt_lcy_close, interest_cons, interest_op, principal, fees, draws_lcy, fx_loss, prepay = (z() for _ in range(8))
    sched_ds = z()
    for tr in fin.debt:
        commit = tr.share_of_capex * debt_base
        draw = commit * spend_share  # LCY, at the quarter's rate
        r = q_rate(tr.rate_pa)
        bal_ccy = 0.0  # in tranche currency
        rate_fx = fx if tr.currency == "USD" else np.ones(T)
        n_amort = max(int(round(tr.tenor_years * 4)) - tr.grace_quarters, 1)
        pay = None
        o_int, o_pr, o_bal_lcy, o_fx, o_prepay, o_draw = z(), z(), z(), z(), z(), z()
        for i in range(T):
            open_ccy = bal_ccy
            d_ccy = draw[i] / rate_fx[i]
            interest = open_ccy * r
            pr = 0.0
            amort_q = i - C - tr.grace_quarters  # 0 = first amortising quarter
            if i >= C and amort_q >= 0 and open_ccy > EPS:
                if tr.amortisation == "annuity":
                    if pay is None:
                        pay = annuity_payment(open_ccy, r, n_amort)
                    pr = min(open_ccy, pay - interest) if amort_q < n_amort - 1 else open_ccy
                else:
                    if pay is None:
                        pay = open_ccy / n_amort
                    pr = min(open_ccy, pay) if amort_q < n_amort - 1 else open_ccy
            pp = 0.0
            if closes and i == t_arr:
                pp = open_ccy - pr  # mandatory prepayment when operations end
            bal_ccy = open_ccy + d_ccy - pr - pp
            if bal_ccy < EPS:
                bal_ccy = 0.0
            o_int[i] = interest * rate_fx[i]
            o_pr[i] = pr * rate_fx[i]
            o_prepay[i] = pp * rate_fx[i]
            o_draw[i] = draw[i]
            o_bal_lcy[i] = bal_ccy * rate_fx[i]
            # revaluation of the opening balance; draws and repayments are at the quarter's rate, so
            # previous close + draw - repayment - prepayment + fx loss = close (checked in checks.py)
            o_fx[i] = open_ccy * (rate_fx[i] - (rate_fx[i - 1] if i > 0 else rate_fx[i]))
        fee = np.where(t == 0, commit * tr.upfront_fee, 0.0)
        ic = np.where(t < C, o_int, 0.0)
        io = np.where(t >= C, o_int, 0.0)
        tranche_out.append(dict(name=tr.name, kind=tr.kind, currency=tr.currency, commitment=commit, interest=o_int,
                                principal=o_pr, prepayment=o_prepay, draws=o_draw, balance=o_bal_lcy, fx_loss=o_fx, fee=fee))
        debt_lcy_close += o_bal_lcy
        interest_cons += ic
        interest_op += io
        principal += o_pr
        prepay += o_prepay
        fees += fee
        draws_lcy += o_draw
        fx_loss += o_fx
        sched_ds += io + o_pr
    S.update(debt_balance=debt_lcy_close, interest_construction=interest_cons, interest_expense=interest_op,
             principal=principal, prepayment=prepay, financing_fees=fees, debt_draws=draws_lcy, fx_loss=fx_loss,
             debt_service=sched_ds)

    # ---------------------------------------------------------------- fixed assets and depreciation (by vintage)
    dep = z()
    additions = capex_init + repl + interest_cons + fees
    vintages: list[tuple[np.ndarray, float]] = []
    for it, spend in capex_items:
        vintages.append((spend, it.asset_life_years))
    w_life = (sum(it.amount * (fx[0] if it.currency == "USD" else 1.0) * it.asset_life_years for it in p.capex)
              / max(sum(it.amount * (fx[0] if it.currency == "USD" else 1.0) for it in p.capex), EPS))
    vintages.append((interest_cons + fees, w_life))
    vintages.append((repl, tech.battery_life_years))
    for spend, life in vintages:
        n = max(int(round(life * 4)), 1)
        for i in np.nonzero(spend > 0)[0]:
            start = max(i + 1, C)  # assets placed in service at COD, replacements the quarter after spend
            amt = spend[i] / n
            dep[start:min(start + n, T)] += amt
    dep = np.where(active | (~op), dep, 0.0)  # no depreciation after operations end
    dep[t < C] = 0.0
    S["depreciation_scheduled"] = dep.copy()

    # ---------------------------------------------------------------- capital grant and RBF receipts
    grant_cash = z()
    if grant_total > 0:
        milestones = sub.grant_milestones or []
        if not milestones:
            grant_cash[min(C, T - 1)] += grant_total
        for ms in milestones:
            if 0 <= ms.quarter < T and (ms.quarter < C or active[ms.quarter] or not closes):
                grant_cash[ms.quarter] += grant_total * ms.share
    rbf = z()
    paid = 0.0
    cap = sub.rbf_cap if sub.rbf_cap is not None else float("inf")
    for i in range(T):
        j = i - sub.rbf_verification_lag_quarters
        if j >= 0 and sub.rbf_per_connection > 0 and active[i]:
            due = new_total[j] * sub.rbf_per_connection
            amt = max(0.0, min(due, cap - paid))
            rbf[i] = amt
            paid += amt
    S["grant_receipts"], S["rbf_receipts"] = grant_cash, rbf

    # ---------------------------------------------------------------- closure, residual value and deferred grant
    nbv = z()
    nbv_open = 0.0
    disposal_gain = z()
    disposal_proceeds = z()
    defg, grant_income = z(), z()
    defg_open = 0.0
    for i in range(T):
        d = dep[i] if nbv_open + additions[i] > EPS else 0.0
        d = min(d, nbv_open + additions[i])
        dep[i] = d
        nb = nbv_open + additions[i] - d
        # deferred grant: receipts in, release pro rata to depreciation of the asset base (weighted life)
        g_in = grant_cash[i] + rbf[i]
        base = defg_open + g_in
        rel = 0.0
        if i >= C and base > EPS:
            remaining_q = max(int(round(w_life * 4)) - (i - C), 1)
            rel = base / remaining_q
        if closes and i == t_arr:
            proceeds = ga.compensation_pct_nbv * nb if ga.treatment == "asset_transfer" else 0.0
            disposal_proceeds[i] = proceeds
            disposal_gain[i] = proceeds - nb
            nb = 0.0
            rel = base  # remaining deferred grant released on disposal
        if i == T - 1 and p.residual_value_pct_nbv > 0 and nb > EPS and not (closes and i >= t_arr):
            proceeds = p.residual_value_pct_nbv * nb
            disposal_proceeds[i] += proceeds
            disposal_gain[i] += proceeds - nb
            nb = 0.0
        defg[i] = base - rel
        grant_income[i] = rel
        nbv[i] = nb
        nbv_open = nb
        defg_open = defg[i]
    S.update(depreciation=dep, nbv=nbv, deferred_grant=defg, grant_income=grant_income,
             disposal_gain=disposal_gain, disposal_proceeds=disposal_proceeds, asset_additions=additions)

    # ---------------------------------------------------------------- tax (levered), loss carry forward
    ebt = ebitda + grant_income - dep - interest_op - fx_loss + disposal_gain
    taxable = ebt - (0.0 if m.grant_income_taxable else grant_income)
    tax = z()
    losses = 0.0
    for i in range(T):
        x = taxable[i]
        if x < 0:
            losses += -x
        else:
            use = min(losses, x)
            losses -= use
            tax[i] = (x - use) * m.tax_rate
    net_income = ebt - tax
    S.update(ebt=ebt, tax=tax, net_income=net_income)

    # unlevered tax for project cash flows (no interest, no FX on debt, no capitalised finance costs)
    unlev_dep = z()
    for spend, life in vintages[:-2] + [vintages[-1]]:
        n = max(int(round(life * 4)), 1)
        for i in np.nonzero(spend > 0)[0]:
            start = max(i + 1, C)
            unlev_dep[start:min(start + n, T)] += spend[i] / n
    unlev_dep = np.where(active, unlev_dep, 0.0)
    unlev_taxable = ebitda - unlev_dep
    unlev_tax = z()
    losses = 0.0
    for i in range(T):
        x = unlev_taxable[i]
        if x < 0:
            losses += -x
        else:
            use = min(losses, x)
            losses -= use
            unlev_tax[i] = (x - use) * m.tax_rate
    S["unlevered_tax"] = unlev_tax

    # ---------------------------------------------------------------- cash waterfall
    cash_ops = collected + fee_rev + tariff_support - opex
    cfads = cash_ops - tax - repl + mra_out - mra_in
    S["cash_from_operations_pre_tax"] = cash_ops
    S["cfads"] = cfads
    # DSRA target: scheduled debt service of the next N quarters
    dsra_target = z()
    nq = fin.dsra_quarters
    for i in range(T):
        if nq > 0 and not (closes and i >= t_arr):
            dsra_target[i] = sched_ds[i + 1:i + 1 + nq].sum()
    if closes:
        dsra_target[t_arr:] = 0.0
    cash, dsra = z(), z()
    eq_in, eq_support, dist = z(), z(), z()
    cash_open, dsra_open = 0.0, 0.0
    dscr_q = np.full(T, np.nan)
    for i in range(T):
        dsra_move = dsra_target[i] - dsra_open
        if i < C:
            uses = capex_init[i] + interest_cons[i] + fees[i] + dsra_move + tax[i]
            sources = draws_lcy[i] + grant_cash[i]
            need = uses - sources - cash_open
            e = max(0.0, need)
            eq_in[i] = e
            cash[i] = cash_open + sources + e - uses
        else:
            flow = (cfads[i] + grant_cash[i] + rbf[i] + disposal_proceeds[i] + draws_lcy[i]
                    - interest_op[i] - principal[i] - prepay[i] - dsra_move - capex_init[i])
            pre = cash_open + flow
            floor = fin.min_cash if i < T - 1 else 0.0
            support = max(0.0, floor - pre)
            eq_support[i] = support
            avail = pre + support
            if sched_ds[i] > EPS:
                dscr_q[i] = cfads[i] / sched_ds[i]
            lock = sched_ds[i] > EPS and dscr_q[i] < fin.lockup_dscr
            d = 0.0 if (lock and i < T - 1) else max(0.0, avail - floor)
            dist[i] = d
            cash[i] = avail - d
        dsra[i] = dsra_open + dsra_move
        cash_open, dsra_open = cash[i], dsra[i]
    S.update(cash=cash, dsra=dsra, dsra_target=dsra_target, equity_contributions=eq_in, equity_support=eq_support,
             distributions=dist, dscr_quarter=dscr_q)

    # ---------------------------------------------------------------- balance sheet and cash flow statement
    paid_in = np.cumsum(eq_in + eq_support)
    retained = np.cumsum(net_income) - np.cumsum(dist)
    mra = np.cumsum(mra_in - mra_out)
    S["mra"] = mra
    assets = cash + dsra + mra + nbv
    liabilities = debt_lcy_close + defg
    equity = paid_in + retained
    S.update(total_assets=assets, total_liabilities=liabilities, total_equity=equity, paid_in_capital=paid_in,
             retained_earnings=retained, balance_check=assets - liabilities - equity)
    cfo = cash_ops - tax
    cfi = -(capex_init + repl + interest_cons + fees) + disposal_proceeds - (dsra - np.concatenate([[0.0], dsra[:-1]])) - (mra_in - mra_out)
    cff = draws_lcy - principal - prepay - interest_op + eq_in + eq_support - dist + grant_cash + rbf
    S.update(cfo=cfo, cfi=cfi, cff=cff, net_cash_flow=cfo + cfi + cff)

    # ---------------------------------------------------------------- project and equity cash flows
    pre_sub = np.where(t < C, -capex_init, 0.0) + np.where(op, collected + fee_rev - opex - unlev_tax - repl, 0.0) + disposal_proceeds
    post_sub = pre_sub + tariff_support + grant_cash + rbf
    eq_cf = -(eq_in + eq_support) + dist
    S.update(project_cf_pre_subsidy=pre_sub, project_cf_post_subsidy=post_sub, equity_cf=eq_cf)

    res = ModelResult(inputs=p, T=T, C=C, dates=dates, series=S)
    res.sources_uses = {
        "capex": float(capex_init.sum()),
        "interest_during_construction": float(interest_cons.sum()),
        "financing_fees": float(fees.sum()),
        "dsra_initial": float(dsra[C - 1]),
        "uses_total": float(capex_init.sum() + interest_cons.sum() + fees.sum() + dsra[C - 1]),
        "debt": float(draws_lcy[:C].sum()),
        "grants_in_construction": float(grant_cash[:C].sum()),
        "equity": float(eq_in[:C].sum()),
        "cash_at_cod": float(cash[C - 1]),
    }
    res.sources_uses["sources_total"] = res.sources_uses["debt"] + res.sources_uses["grants_in_construction"] + res.sources_uses["equity"]
    _metrics(res, tranche_out, per_class, total_capex)
    return res


def _metrics(res: ModelResult, tranches: list[dict], per_class: list[dict], total_capex: float) -> None:
    p, S, C, T = res.inputs, res.series, res.C, res.T
    m = p.macro
    rq = q_rate(m.discount_rate_pa)
    M: dict[str, float | None] = {}
    conns = sum(c.connections_target for c in p.customers)
    M["connections_target"] = float(conns)
    M["capex_total"] = total_capex
    M["capex_total_usd"] = total_capex / m.fx_lcy_per_usd
    M["cost_per_connection"] = total_capex / conns if conns else None
    M["cost_per_connection_usd"] = (total_capex / conns / m.fx_lcy_per_usd) if conns else None
    M["project_irr_pre_subsidy"] = annualise(irr(S["project_cf_pre_subsidy"]))
    M["project_irr_post_subsidy"] = annualise(irr(S["project_cf_post_subsidy"]))
    M["equity_irr"] = annualise(irr(S["equity_cf"]))
    M["project_npv_pre_subsidy"] = npv(rq, S["project_cf_pre_subsidy"])
    M["project_npv_post_subsidy"] = npv(rq, S["project_cf_post_subsidy"])
    M["equity_npv"] = npv(q_rate(m.equity_target_irr_pa), S["equity_cf"]) if m.equity_target_irr_pa is not None else None
    # annual DSCR on operating years with scheduled debt service
    yrs = p.operating_years
    cf_y = [float(S["cfads"][C + 4 * y:C + 4 * y + 4].sum()) for y in range(yrs)]
    ds_y = [float(S["debt_service"][C + 4 * y:C + 4 * y + 4].sum()) for y in range(yrs)]
    dscr_y = [cf / ds if ds > EPS else None for cf, ds in zip(cf_y, ds_y)]
    valid = [d for d in dscr_y if d is not None]
    M["dscr_min"] = min(valid) if valid else None
    M["dscr_avg"] = float(np.mean(valid)) if valid else None
    # LLCR at COD: PV of CFADS over the loan life at the weighted debt rate / debt outstanding at COD
    debt_cod = float(S["debt_balance"][C - 1])
    if debt_cod > EPS and p.financing.debt:
        w = sum(tr.share_of_capex for tr in p.financing.debt)
        rate = sum(tr.rate_pa * tr.share_of_capex for tr in p.financing.debt) / w if w else 0.0
        last = C + int(round(max(tr.tenor_years for tr in p.financing.debt) * 4))
        M["llcr_cod"] = npv(q_rate(rate), S["cfads"][C:min(last, T)]) / debt_cod
    else:
        M["llcr_cod"] = None
    # payback on post-subsidy project cash flow, years from COD
    cum = np.cumsum(S["project_cf_post_subsidy"])
    idx = np.nonzero((cum >= 0) & (np.arange(T) >= C))[0]
    M["payback_years"] = float((idx[0] - C + 1) / 4.0) if len(idx) and cum[-1] >= 0 else None
    # costs and energy
    dfac = 1.0 / (1.0 + rq) ** np.arange(1, T + 1)
    pv_cost = float(np.sum((S["capex"] + S["replacement_capex"] + S["opex"]) * dfac))
    pv_kwh = float(np.sum(S["billed_kwh"] * dfac))
    M["lcoe_per_kwh_sold"] = pv_cost / pv_kwh if pv_kwh > EPS else None
    M["lcoe_per_kwh_sold_usd"] = (M["lcoe_per_kwh_sold"] / m.fx_lcy_per_usd) if M["lcoe_per_kwh_sold"] else None
    op_years_df = float(np.sum(np.where(np.arange(T) >= C, 0.25, 0.0) * dfac))
    M["minimum_revenue_requirement_pa"] = pv_cost / op_years_df if op_years_df > EPS else None
    M["viability_gap_pv"] = max(0.0, -M["project_npv_pre_subsidy"])
    M["viability_gap_per_connection"] = M["viability_gap_pv"] / conns if conns else None
    subsidy = float(S["grant_receipts"].sum() + S["rbf_receipts"].sum() + S["tariff_support"].sum())
    M["subsidy_total_nominal"] = subsidy
    M["subsidy_per_connection"] = subsidy / conns if conns else None
    M["equity_peak"] = float(np.max(np.cumsum(S["equity_contributions"] + S["equity_support"] - S["distributions"])))
    M["equity_support_total"] = float(S["equity_support"].sum())
    dem = float(S["demand_kwh"].sum())
    M["unserved_share"] = float(S["unserved_kwh"].sum()) / dem if dem > EPS else None
    M["energy_sold_kwh_total"] = float(S["billed_kwh"].sum())
    gen = S["generated_kwh"] * p.technical.diesel_share * p.technical.diesel_kgco2_per_kwh / 1000.0
    M["diesel_tco2_total"] = float(gen.sum())
    # affordability: bill at COD for a connection of each class, against its income
    worst = None
    for c in p.customers:
        if c.monthly_income:
            bill = c.kwh_per_connection_month * c.tariff_per_kwh + c.fixed_charge_month
            ratio = bill / c.monthly_income
            worst = ratio if worst is None else max(worst, ratio)
    M["max_bill_to_income"] = worst
    tariffs = [(c.tariff_per_kwh, c.connections_target * c.kwh_per_connection_month) for c in p.customers]
    wsum = sum(w for _, w in tariffs)
    M["avg_tariff_cod"] = sum(tf * w for tf, w in tariffs) / wsum if wsum > EPS else None
    res.metrics = M
    res.annual = {
        "year": list(range(1, yrs + 1)),
        "cfads": cf_y,
        "debt_service": ds_y,
        "dscr": [d if d is not None else float("nan") for d in dscr_y],
        "revenue": [float(S["revenue"][C + 4 * y:C + 4 * y + 4].sum()) for y in range(yrs)],
        "ebitda": [float(S["ebitda"][C + 4 * y:C + 4 * y + 4].sum()) for y in range(yrs)],
        "net_income": [float(S["net_income"][C + 4 * y:C + 4 * y + 4].sum()) for y in range(yrs)],
        "energy_sold_kwh": [float(S["billed_kwh"][C + 4 * y:C + 4 * y + 4].sum()) for y in range(yrs)],
        "connections_end": [float(S["connections"][C + 4 * y + 3]) for y in range(yrs)],
    }
    res.tranches = tranches
