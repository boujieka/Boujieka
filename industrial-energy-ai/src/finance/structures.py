"""Financing structures: responsibilities and client-side cash-flow comparison.

For each structure the table states which contractual party is responsible for the
investment, operations and the main risks. The cash-flow comparison is a simplified screening
view from the industrial client's perspective (annual payments and savings versus the baseline);
contract terms (tariffs, fees, lease rates) are user inputs, never defaults presented as market
prices.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from pydantic import BaseModel, Field

from src.finance.common import crf


@dataclass(frozen=True)
class Structure:
    key: str
    label_fr: str
    label_en: str
    investor: str
    operator: str
    risks: dict[str, str]
    payment_basis: str



STRUCTURES: dict[str, Structure] = {
    s.key: s
    for s in [
        Structure("self_financing", "Autofinancement", "Corporate self-financing", "Client", "Client",
                  {"performance": "Client", "fuel_price": "Client", "demand": "Client", "credit": "Client (balance sheet)",
                   "technology": "Client", "fx": "Client"}, "Client pays CAPEX and OPEX; keeps all savings."),
        Structure("epc_om", "EPC + O&M", "EPC + O&M", "Client", "O&M contractor",
                  {"performance": "EPC (warranty period) then O&M contractor (availability guarantees)", "fuel_price": "Client",
                   "demand": "Client", "credit": "Client", "technology": "EPC contractor (construction), client (long term)", "fx": "Client"},
                  "Client pays the EPC price and an annual O&M fee."),
        Structure("corporate_ppa", "PPA d'entreprise", "Corporate PPA", "Developer / IPP", "Developer",
                  {"performance": "Developer", "fuel_price": "Shared (tariff indexation)", "demand": "Client (take-or-pay)",
                   "credit": "Developer bears client credit risk", "technology": "Developer", "fx": "Depends on tariff currency"},
                  "Client pays a tariff per kWh delivered."),
        Structure("energy_as_a_service", "Énergie en tant que service", "Energy-as-a-Service", "Service provider", "Service provider",
                  {"performance": "Provider (service levels)", "fuel_price": "Provider or shared", "demand": "Client (fixed fee)",
                   "credit": "Provider bears client credit risk", "technology": "Provider", "fx": "Depends on fee currency"},
                  "Client pays a fixed periodic fee (optionally plus a per-kWh component)."),
        Structure("equipment_leasing", "Crédit-bail", "Equipment leasing", "Lessor", "Client (or O&M contractor)",
                  {"performance": "Client", "fuel_price": "Client", "demand": "Client", "credit": "Lessor bears client credit risk",
                   "technology": "Client", "fx": "Depends on lease currency"},
                  "Client pays lease instalments; ownership may transfer at term."),
        Structure("developer_owned", "Propriété du développeur (BOO)", "Developer-owned power system (BOO)", "Developer", "Developer",
                  {"performance": "Developer", "fuel_price": "Developer (unless passed through)", "demand": "Client (minimum offtake)",
                   "credit": "Developer bears client credit risk", "technology": "Developer", "fx": "Depends on tariff currency"},
                  "Developer builds, owns and operates; client buys all supplied energy at a tariff."),
    ]
}


class StructureInputs(BaseModel):
    capex: float = Field(ge=0)
    annual_opex: float = Field(ge=0, description="O&M + fuel + other running costs of the new system")
    baseline_annual_cost: float = Field(ge=0)
    annual_energy_kwh: float = Field(gt=0, description="Energy supplied by the new system to the client")
    years: int = Field(20, ge=1, le=40)
    discount_rate: float = Field(0.10, ge=0, lt=1)
    escalation: float = Field(0.03, ge=-0.5, lt=1)
    om_fee_per_year: float = Field(0.0, ge=0, description="EPC+O&M: contractor fee (replaces in-house O&M share)")
    ppa_tariff_per_kwh: float = Field(0.0, ge=0)
    eaas_fee_per_year: float = Field(0.0, ge=0)
    eaas_fee_per_kwh: float = Field(0.0, ge=0)
    lease_rate: float = Field(0.10, ge=0, lt=1)
    lease_term_years: int = Field(7, ge=1, le=20)
    client_residual_opex_share: float = Field(0.0, ge=0, le=1, description="Share of running costs still borne by the client under third-party structures (e.g. backup fuel)")


def client_cash_flows(key: str, inp: StructureInputs) -> dict:
    """Annual client cash flows (year 0 = investment) and the NPV of savings vs the baseline."""
    n = inp.years
    esc = (1 + inp.escalation) ** np.arange(n)
    baseline = inp.baseline_annual_cost * esc
    upfront = 0.0
    if key == "self_financing":
        payments = inp.annual_opex * esc
        upfront = inp.capex
    elif key == "epc_om":
        payments = (inp.annual_opex + inp.om_fee_per_year) * esc
        upfront = inp.capex
    elif key in ("corporate_ppa", "developer_owned"):
        payments = (inp.ppa_tariff_per_kwh * inp.annual_energy_kwh + inp.client_residual_opex_share * inp.annual_opex) * esc
    elif key == "energy_as_a_service":
        payments = (inp.eaas_fee_per_year + inp.eaas_fee_per_kwh * inp.annual_energy_kwh + inp.client_residual_opex_share * inp.annual_opex) * esc
    elif key == "equipment_leasing":
        instalment = inp.capex * crf(inp.lease_rate, inp.lease_term_years)
        lease = np.array([instalment if y < inp.lease_term_years else 0.0 for y in range(n)])
        payments = inp.annual_opex * esc + lease
    else:
        raise ValueError(f"Unknown structure '{key}'")
    savings = baseline - payments
    cf = np.concatenate(([-upfront], savings))
    npv = float(np.sum(cf / (1 + inp.discount_rate) ** np.arange(cf.size)))
    return {
        "structure": key,
        "upfront_investment": upfront,
        "annual_payments": payments.tolist(),
        "annual_savings": savings.tolist(),
        "client_cash_flow": cf.tolist(),
        "client_npv": npv,
        "cumulative_savings": float(savings.sum() - upfront),
    }


def developer_cash_flows(key: str, inp: StructureInputs) -> dict | None:
    """Third-party investor view (unlevered, pre-tax screening) for PPA, EaaS, BOO and leasing."""
    import numpy_financial as npf

    n = inp.years
    esc = (1 + inp.escalation) ** np.arange(n)
    if key in ("corporate_ppa", "developer_owned"):
        revenue = inp.ppa_tariff_per_kwh * inp.annual_energy_kwh * esc
        costs = (1 - inp.client_residual_opex_share) * inp.annual_opex * esc
    elif key == "energy_as_a_service":
        revenue = (inp.eaas_fee_per_year + inp.eaas_fee_per_kwh * inp.annual_energy_kwh) * esc
        costs = (1 - inp.client_residual_opex_share) * inp.annual_opex * esc
    elif key == "equipment_leasing":
        instalment = inp.capex * crf(inp.lease_rate, inp.lease_term_years)
        revenue = np.array([instalment if y < inp.lease_term_years else 0.0 for y in range(n)])
        costs = np.zeros(n)
    else:
        return None
    cf = np.concatenate(([-inp.capex], revenue - costs))
    irr = float(npf.irr(cf)) if (cf > 0).any() and (cf < 0).any() else None
    return {"structure": key, "investor_cash_flow": cf.tolist(), "investor_irr": None if irr is None or np.isnan(irr) else irr,
            "investor_npv": float(np.sum(cf / (1 + inp.discount_rate) ** np.arange(cf.size)))}


def break_even_ppa_tariff(inp: StructureInputs, target_irr: float) -> float:
    """PPA tariff per kWh giving the investor exactly ``target_irr`` (closed form on escalating annuity)."""
    n = inp.years
    esc = (1 + inp.escalation) ** np.arange(n)
    disc = (1 + target_irr) ** -np.arange(1, n + 1)
    costs_pv = float(np.sum((1 - inp.client_residual_opex_share) * inp.annual_opex * esc * disc))
    energy_pv = float(np.sum(inp.annual_energy_kwh * esc * disc))
    return (inp.capex + costs_pv) / energy_pv
