"""Input schema of the ACCESS FINANCE mini grid engine.

Every input is explicit and carries its unit in the field name or description. Money is in the model currency (LCY)
unless the field says USD. Rates are fractions (0.12 = 12%). The engine never fills a missing commercial input with a
hidden default: fields without a safe neutral value are required, and `missing_inputs()` reports what is absent.
"""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class Provenance(str, Enum):
    """Where an input value comes from. Shown next to every output that depends on it."""

    SOURCED = "sourced"            # taken from a cited document (source_ref must be filled)
    USER_ESTIMATE = "user_estimate"  # entered by the user as their own assumption
    ILLUSTRATIVE = "illustrative"  # synthetic demo value, never to be presented as real


class CustomerCategory(str, Enum):
    HOUSEHOLD = "household"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    AGRICULTURAL = "agricultural"
    INSTITUTIONAL = "institutional"
    ANCHOR = "anchor"


class CustomerClass(BaseModel):
    name: str
    category: CustomerCategory
    connections_target: int = Field(ge=0, description="Connections at the end of the ramp")
    start_quarter: int = Field(0, ge=0, description="Operating quarter in which connections start (0 = COD quarter)")
    ramp_quarters: int = Field(4, ge=1, description="Quarters to reach the target, linear")
    kwh_per_connection_month: float = Field(ge=0, description="Initial consumption per active connection, kWh a month")
    demand_growth_pa: float = Field(0.0, ge=-0.5, le=1.0, description="Annual growth of consumption per connection")
    tariff_per_kwh: float = Field(ge=0, description="Energy tariff at COD, LCY per kWh")
    fixed_charge_month: float = Field(0.0, ge=0, description="Fixed charge per connection, LCY a month")
    connection_fee: float = Field(0.0, ge=0, description="One-off fee paid by the customer at connection, LCY")
    monthly_income: float | None = Field(None, ge=0, description="Typical monthly income of the class, LCY (affordability)")


class CapexCategory(str, Enum):
    GENERATION = "generation"
    STORAGE = "storage"
    NETWORK = "network"
    METERING = "metering"
    DEVELOPMENT = "development"
    OTHER = "other"


class CapexItem(BaseModel):
    name: str
    category: CapexCategory
    amount: float = Field(ge=0)
    currency: Literal["LCY", "USD"] = "LCY"
    asset_life_years: float = Field(gt=0)


class Technical(BaseModel):
    """Engineering inputs from the design study. The engine does not size or dispatch the system."""

    pv_kwp: float = Field(ge=0)
    battery_kwh: float = Field(ge=0)
    diesel_kw: float = Field(0.0, ge=0)
    network_km: float = Field(0.0, ge=0)
    deliverable_energy_kwh_pa: float = Field(gt=0, description="Energy the design can deliver at the busbar per year (from the hourly study)")
    technical_loss: float = Field(0.08, ge=0, lt=0.5, description="Share of generated energy lost in the network")
    commercial_loss: float = Field(0.03, ge=0, lt=0.5, description="Share of delivered energy not billed (theft, meter faults)")
    diesel_share: float = Field(0.0, ge=0, le=1, description="Share of generated energy from diesel (from the hourly study)")
    diesel_cost_per_kwh: float = Field(0.0, ge=0, description="Fuel cost per diesel kWh at COD, LCY")
    diesel_kgco2_per_kwh: float = Field(0.0, ge=0, description="Emission factor of diesel generation")
    battery_life_years: float = Field(8.0, gt=0)
    battery_replacement_usd_per_kwh: float = Field(0.0, ge=0, description="Replacement cost at COD prices, USD per kWh")
    battery_cost_decline_pa: float = Field(0.0, ge=0, lt=0.5, description="Annual real decline of battery replacement cost")


class Opex(BaseModel):
    fixed_pa: float = Field(0.0, ge=0, description="Fixed operating cost per year at COD prices, LCY")
    per_connection_pa: float = Field(0.0, ge=0, description="Cost per active connection per year at COD prices, LCY")
    insurance_pct_capex: float = Field(0.0, ge=0, lt=0.2, description="Annual insurance as a share of initial capex")
    collection_efficiency: float = Field(0.95, gt=0, le=1, description="Share of billed revenue collected")


class Macro(BaseModel):
    inflation_pa: float = Field(0.0, ge=-0.2, le=2.0, description="Local inflation")
    tariff_indexation: float = Field(1.0, ge=0, le=1.5, description="Share of inflation passed into tariffs")
    fx_lcy_per_usd: float = Field(gt=0, description="Exchange rate at financial close, LCY per USD")
    fx_depreciation_pa: float = Field(0.0, ge=-0.5, le=2.0, description="Annual depreciation of LCY against USD")
    tax_rate: float = Field(0.0, ge=0, lt=1)
    grant_income_taxable: bool = False
    discount_rate_pa: float = Field(gt=-0.99, description="Nominal discount rate for project NPV")
    equity_target_irr_pa: float | None = Field(None, description="Target equity IRR used by the subsidy solver")


class DebtTranche(BaseModel):
    name: str
    kind: Literal["senior", "concessional"] = "senior"
    currency: Literal["LCY", "USD"] = "LCY"
    share_of_capex: float = Field(ge=0, le=1, description="Share of construction capex funded by this tranche")
    rate_pa: float = Field(ge=0, lt=1)
    tenor_years: float = Field(gt=0, description="Years from COD to final repayment")
    grace_quarters: int = Field(0, ge=0, description="Interest-only quarters after COD")
    upfront_fee: float = Field(0.0, ge=0, lt=0.2, description="Fee on commitment, paid at financial close")
    amortisation: Literal["annuity", "straight_line"] = "annuity"


class Financing(BaseModel):
    debt: list[DebtTranche] = []
    debt_basis: Literal["capex_net_of_grant", "gross_capex"] = Field(
        "capex_net_of_grant", description="Debt is sized as a share of construction capex, before or after the capital grant")
    dsra_quarters: int = Field(2, ge=0, le=8, description="Quarters of debt service held in reserve")
    maintenance_reserve: bool = Field(True, description="Fund battery replacements through a reserve built up evenly beforehand")
    lockup_dscr: float = Field(1.2, ge=0, description="Distributions blocked when the quarter DSCR is below this")
    min_cash: float = Field(0.0, ge=0, description="Minimum unrestricted cash; shortfalls are met by equity support")

    @model_validator(mode="after")
    def _shares(self):
        if sum(t.share_of_capex for t in self.debt) > 1.0 + 1e-9:
            raise ValueError("Debt shares of capex add to more than 100%")
        return self


class GrantMilestone(BaseModel):
    quarter: int = Field(description="Model quarter of disbursement (0 = financial close)")
    share: float = Field(gt=0, le=1)


class Subsidies(BaseModel):
    capital_grant: float = Field(0.0, ge=0, description="Capital grant, LCY")
    grant_milestones: list[GrantMilestone] = []
    rbf_per_connection: float = Field(0.0, ge=0, description="Results based payment per verified new connection, LCY")
    rbf_verification_lag_quarters: int = Field(2, ge=0, description="Quarters between connection and payment")
    rbf_cap: float | None = Field(None, ge=0, description="Programme cap on RBF payments, LCY")
    tariff_support_per_kwh: float = Field(0.0, ge=0, description="Operating subsidy per billed kWh, LCY")
    tariff_support_years: float = Field(0.0, ge=0)

    @model_validator(mode="after")
    def _milestones(self):
        if self.capital_grant > 0:
            s = sum(m.share for m in self.grant_milestones)
            if abs(s - 1.0) > 1e-6:
                raise ValueError("Grant milestone shares must add to 100% when a capital grant is entered")
        return self


class GridArrival(BaseModel):
    """Treatment if the main grid reaches the site. Must be supported by the country's verified rules."""

    enabled: bool = False
    operating_year: int = Field(10, ge=1, description="Operating year in which the grid arrives")
    treatment: Literal["interconnect", "asset_transfer", "stranded"] = "interconnect"
    compensation_pct_nbv: float = Field(0.0, ge=0, le=2, description="Compensation as a share of net book value (asset transfer)")
    tariff_factor_after: float = Field(1.0, ge=0, le=2, description="Tariff multiplier after interconnection")
    demand_factor_after: float = Field(1.0, ge=0, le=3, description="Demand multiplier after interconnection")
    regulatory_source: str | None = Field(None, description="Citation of the country rule applied")


class Review(BaseModel):
    reviewed_by: str
    reviewed_on: date
    note: str = ""


class ProjectInputs(BaseModel):
    project_name: str
    country: str
    currency: str = Field(min_length=3, max_length=3)
    financial_close: date
    construction_quarters: int = Field(2, ge=1, le=12)
    operating_years: int = Field(20, ge=1, le=30)
    residual_value_pct_nbv: float = Field(0.0, ge=0, le=1)
    technical: Technical
    customers: list[CustomerClass]
    capex: list[CapexItem]
    opex: Opex
    macro: Macro
    financing: Financing = Financing()
    subsidies: Subsidies = Subsidies()
    grid_arrival: GridArrival = GridArrival()
    provenance: Provenance = Provenance.USER_ESTIMATE
    review: Review | None = Field(None, description="Human review of the assumptions; required for VALIDATED status")

    @field_validator("currency")
    @classmethod
    def _upper(cls, v: str) -> str:
        return v.upper()


def missing_inputs(p: ProjectInputs) -> list[str]:
    """Commercially essential inputs that are absent or zero. A model with any of these is INCOMPLETE."""
    out: list[str] = []
    if not p.customers or sum(c.connections_target for c in p.customers) == 0:
        out.append("customers: no connections planned")
    if not p.capex or sum(c.amount for c in p.capex) == 0:
        out.append("capex: no capital cost entered")
    if all(c.tariff_per_kwh == 0 and c.fixed_charge_month == 0 for c in p.customers):
        out.append("tariffs: no tariff entered for any customer class")
    if p.opex.fixed_pa == 0 and p.opex.per_connection_pa == 0:
        out.append("opex: no operating cost entered")
    if p.technical.battery_kwh > 0 and p.technical.battery_replacement_usd_per_kwh == 0:
        out.append("technical: battery replacement cost missing")
    if p.grid_arrival.enabled and not p.grid_arrival.regulatory_source:
        out.append("grid arrival: no regulatory source cited for the treatment")
    return out
