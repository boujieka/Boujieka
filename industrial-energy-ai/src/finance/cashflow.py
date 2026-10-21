"""Project finance model (annual, nominal terms).

Conventions
-----------
* Timeline: years 0 .. C-1 are construction (CAPEX spread evenly, end-of-year cash flows);
  years C .. C+N-1 are the N operating years. Year 0 is not discounted.
* All cash flows are NOMINAL: revenues and costs escalate with the stated rates, and every
  discount rate entered is a nominal rate. The equivalent real discount rate is reported via
  the Fisher relation for information. With zero inflation, nominal = real.
* Unlevered project cash flow = -CAPEX - replacements + EBITDA - unlevered tax.
  It contains NO debt drawdowns, interest or repayments (no double counting of financing in the
  project IRR). Unlevered tax is computed without interest deduction.
* Equity cash flow = -(CAPEX - debt drawdowns) + CFADS - debt service, with
  CFADS = EBITDA - levered tax - replacements (replacements funded from operating cash flow).
  Identity tested: equity CF = project CF + drawdowns - debt service + (unlevered tax - levered tax).
* Debt: drawn pro rata with CAPEX at the end of each construction year; interest during
  construction (IDC) is capitalised. From the commercial operation date (COD), interest-only
  for ``grace_years`` then annuity or linear repayment until ``tenor_years`` after COD.
* Tax: straight-line depreciation of CAPEX and of each replacement from the year it occurs;
  unlimited loss carry-forward. IDC is not depreciated (simplification).
* No residual value at the end of the project (conservative simplification).
"""

from __future__ import annotations

import math
from typing import Literal

import numpy as np
import numpy_financial as npf
from pydantic import BaseModel, Field, model_validator

from src.finance.common import levelized_cost


class FinanceInputs(BaseModel):
    capex: float = Field(ge=0)
    construction_years: int = Field(1, ge=1, le=5)
    operating_years: int = Field(20, ge=1, le=40)
    revenue_year1: float = Field(0.0, description="Revenue or avoided cost in the first operating year")
    opex_year1: float = Field(0.0, ge=0)
    revenue_escalation: float = Field(0.03, ge=-0.5, lt=1)
    inflation: float = Field(0.03, ge=-0.5, lt=1, description="Escalation of operating costs and replacements")
    replacements: dict[int, float] = Field(default_factory=dict, description="Operating year (1-based) -> cost in year-0 money")
    energy_year1_kwh: float = Field(0.0, ge=0)
    energy_degradation: float = Field(0.0, ge=0, lt=0.2)
    tax_rate: float = Field(0.30, ge=0, lt=1)
    depreciation_years: int = Field(10, ge=1, le=40)
    debt_share: float = Field(0.0, ge=0, le=0.95)
    interest_rate: float = Field(0.08, ge=0, lt=1)
    tenor_years: int = Field(10, ge=1, le=30)
    grace_years: int = Field(0, ge=0, le=10)
    repayment: Literal["annuity", "linear"] = "annuity"
    discount_rate: float = Field(0.10, ge=0, lt=1)
    equity_discount_rate: float | None = Field(None, ge=0, lt=1)
    currency: str = "XAF"

    @model_validator(mode="after")
    def _debt_terms(self) -> "FinanceInputs":
        if self.debt_share > 0:
            if self.tenor_years > self.operating_years:
                raise ValueError("Debt tenor cannot exceed the operating period.")
            if self.grace_years >= self.tenor_years:
                raise ValueError("Grace period must be shorter than the debt tenor.")
        return self


class FinanceResults(BaseModel):
    years: list[int]
    phase: list[str]
    capex: list[float]
    replacements: list[float]
    revenue: list[float]
    opex: list[float]
    ebitda: list[float]
    depreciation: list[float]
    tax_unlevered: list[float]
    tax_levered: list[float]
    project_cf: list[float]
    debt_drawdown: list[float]
    idc: list[float]
    interest: list[float]
    principal: list[float]
    debt_service: list[float]
    debt_balance_end: list[float]
    cfads: list[float]
    equity_cf: list[float]
    dscr: list[float | None]
    energy_kwh: list[float]
    npv_project: float
    npv_equity: float
    irr_project: float | None
    irr_equity: float | None
    payback_years: float | None
    discounted_payback_years: float | None
    min_dscr: float | None
    avg_dscr: float | None
    llcr: float | None
    lcoe_per_kwh: float | None
    total_financing_requirement: float
    debt_amount: float
    equity_amount: float
    cumulative_savings: float
    real_discount_rate: float
    currency: str


def _irr(cf: np.ndarray) -> float | None:
    if not (np.any(cf < 0) and np.any(cf > 0)):
        return None
    try:
        value = float(npf.irr(cf))
    except Exception:  # pragma: no cover - numerical failure
        return None
    return None if math.isnan(value) else value


def _npv(rate: float, cf: np.ndarray) -> float:
    return float(np.sum(cf / (1 + rate) ** np.arange(cf.size)))


def _payback(cf: np.ndarray, rate: float | None = None) -> float | None:
    values = cf / (1 + rate) ** np.arange(cf.size) if rate is not None else cf
    cum = np.cumsum(values)
    for t in range(1, cum.size):
        if cum[t] >= 0 > cum[t - 1]:
            return float(t - 1 + (-cum[t - 1]) / values[t])
    if cum.size and cum[0] >= 0:
        return 0.0
    return None


def _depreciation(amounts: np.ndarray, years: int, start_offset: int, n: int) -> np.ndarray:
    """Straight-line depreciation; an amount spent in year t depreciates from year
    max(t, start_offset) for ``years`` years (truncated at the end of the model)."""
    dep = np.zeros(n)
    for t, amount in enumerate(amounts):
        if amount <= 0:
            continue
        first = max(t, start_offset)
        for k in range(first, min(first + years, n)):
            dep[k] += amount / years
    return dep


def _tax(taxable: np.ndarray, rate: float) -> np.ndarray:
    tax = np.zeros_like(taxable)
    loss = 0.0
    for t, value in enumerate(taxable):
        base = value - loss
        if base > 0:
            tax[t] = base * rate
            loss = 0.0
        else:
            loss = -base
    return tax


def run_finance(inp: FinanceInputs) -> FinanceResults:
    C, N = inp.construction_years, inp.operating_years
    n = C + N
    years = np.arange(n)
    op_index = np.where(years >= C, years - C + 1, 0)  # operating year number (1-based), 0 in construction

    capex = np.zeros(n)
    capex[:C] = inp.capex / C
    repl = np.zeros(n)
    for op_year, cost in inp.replacements.items():
        if 1 <= op_year <= N:
            repl[C + op_year - 1] += cost * (1 + inp.inflation) ** (C + op_year - 1)

    is_op = years >= C
    k = np.where(is_op, op_index - 1, 0)
    revenue = np.where(is_op, inp.revenue_year1 * (1 + inp.revenue_escalation) ** k, 0.0)
    opex = np.where(is_op, inp.opex_year1 * (1 + inp.inflation) ** k, 0.0)
    energy = np.where(is_op, inp.energy_year1_kwh * (1 - inp.energy_degradation) ** k, 0.0)
    ebitda = revenue - opex

    dep = _depreciation(capex, inp.depreciation_years, C, n) + _depreciation(repl, inp.depreciation_years, C, n)

    # --- Debt
    draw = capex * inp.debt_share
    idc = np.zeros(n)
    interest = np.zeros(n)
    principal = np.zeros(n)
    balance_end = np.zeros(n)
    bal = 0.0
    for t in range(C):
        idc[t] = bal * inp.interest_rate
        bal += idc[t] + draw[t]
        balance_end[t] = bal
    debt_at_cod = bal
    amort_years = max(inp.tenor_years - inp.grace_years, 1)
    annuity = debt_at_cod * (inp.interest_rate / (1 - (1 + inp.interest_rate) ** -amort_years) if inp.interest_rate > 0 else 1 / amort_years)
    for t in range(C, n):
        y = t - C + 1
        interest[t] = bal * inp.interest_rate
        if y > inp.grace_years and y <= inp.tenor_years and bal > 1e-9:
            if inp.repayment == "annuity":
                principal[t] = min(bal, annuity - interest[t])
            else:
                principal[t] = min(bal, debt_at_cod / amort_years)
        if y == inp.tenor_years:
            principal[t] = bal  # final balloon guards rounding
        bal -= principal[t]
        balance_end[t] = bal
    debt_service = interest + principal

    tax_u = _tax(ebitda - dep, inp.tax_rate)
    tax_l = _tax(ebitda - dep - interest, inp.tax_rate)
    project_cf = -capex - repl + ebitda - tax_u
    cfads = np.where(is_op, ebitda - tax_l - repl, 0.0)
    equity_cf = -(capex - draw) + cfads - debt_service

    dscr: list[float | None] = [float(cfads[t] / debt_service[t]) if debt_service[t] > 1e-9 else None for t in range(n)]
    dscr_vals = [d for d in dscr if d is not None]
    llcr = None
    if debt_at_cod > 0:
        loan_years = range(C, min(C + inp.tenor_years, n))
        pv_cfads = sum(cfads[t] / (1 + inp.interest_rate) ** (t - C + 1) for t in loan_years)
        llcr = float(pv_cfads / debt_at_cod)

    r_eq = inp.equity_discount_rate if inp.equity_discount_rate is not None else inp.discount_rate
    costs_for_lcoe = capex + repl + opex
    lcoe = levelized_cost(costs_for_lcoe, energy, inp.discount_rate) if energy.sum() > 0 else None
    return FinanceResults(
        years=[int(y) for y in years],
        phase=["construction" if t < C else "operation" for t in years],
        capex=capex.tolist(), replacements=repl.tolist(), revenue=revenue.tolist(), opex=opex.tolist(),
        ebitda=ebitda.tolist(), depreciation=dep.tolist(), tax_unlevered=tax_u.tolist(), tax_levered=tax_l.tolist(),
        project_cf=project_cf.tolist(), debt_drawdown=draw.tolist(), idc=idc.tolist(), interest=interest.tolist(),
        principal=principal.tolist(), debt_service=debt_service.tolist(), debt_balance_end=balance_end.tolist(),
        cfads=cfads.tolist(), equity_cf=equity_cf.tolist(), dscr=dscr, energy_kwh=energy.tolist(),
        npv_project=_npv(inp.discount_rate, project_cf),
        npv_equity=_npv(r_eq, equity_cf),
        irr_project=_irr(project_cf),
        irr_equity=_irr(equity_cf),
        payback_years=_payback(project_cf),
        discounted_payback_years=_payback(project_cf, inp.discount_rate),
        min_dscr=min(dscr_vals) if dscr_vals else None,
        avg_dscr=float(np.mean(dscr_vals)) if dscr_vals else None,
        llcr=llcr,
        lcoe_per_kwh=lcoe if lcoe is None or not math.isnan(lcoe) else None,
        total_financing_requirement=float(inp.capex + idc.sum()),
        debt_amount=float(debt_at_cod),
        equity_amount=float((capex - draw).sum()),
        cumulative_savings=float(ebitda[is_op].sum()),
        real_discount_rate=(1 + inp.discount_rate) / (1 + inp.inflation) - 1,
        currency=inp.currency,
    )
