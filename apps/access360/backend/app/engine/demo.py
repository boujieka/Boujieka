"""Synthetic demo project. ILLUSTRATIVE ONLY: every value is invented for testing and demonstration, describes no
real site, company, country or programme, and must never be presented as market evidence. The country and the
currency code are fictional."""
from __future__ import annotations

from datetime import date

from .inputs import (CapexItem, CustomerClass, DebtTranche, Financing, GrantMilestone, GridArrival, Macro, Opex,
                     ProjectInputs, Provenance, Subsidies, Technical)

DEMO_LABEL = "SYNTHETIC DEMO DATA: not a real project"


def demo_inputs() -> ProjectInputs:
    return ProjectInputs(
        project_name="Demo site batch A (synthetic)",
        country="Demo country (fictional)",
        currency="XDM",
        financial_close=date(2027, 1, 1),
        construction_quarters=2,
        operating_years=20,
        technical=Technical(pv_kwp=120, battery_kwh=300, diesel_kw=40, network_km=8,
                            deliverable_energy_kwh_pa=230_000, technical_loss=0.08, commercial_loss=0.03,
                            diesel_share=0.10, diesel_cost_per_kwh=420, diesel_kgco2_per_kwh=0.8,
                            battery_life_years=8, battery_replacement_usd_per_kwh=220, battery_cost_decline_pa=0.03),
        customers=[
            CustomerClass(name="Households", category="household", connections_target=600, ramp_quarters=6,
                          kwh_per_connection_month=9, demand_growth_pa=0.04, tariff_per_kwh=450, fixed_charge_month=600,
                          connection_fee=3_000, monthly_income=60_000),
            CustomerClass(name="Shops and services", category="commercial", connections_target=60, ramp_quarters=4,
                          kwh_per_connection_month=45, demand_growth_pa=0.03, tariff_per_kwh=450, fixed_charge_month=1_500,
                          connection_fee=6_000),
            CustomerClass(name="Agro processing", category="agricultural", connections_target=10, start_quarter=1,
                          ramp_quarters=4, kwh_per_connection_month=250, demand_growth_pa=0.02, tariff_per_kwh=400),
            CustomerClass(name="Health post and school", category="institutional", connections_target=3, ramp_quarters=1,
                          kwh_per_connection_month=120, tariff_per_kwh=450),
            CustomerClass(name="Telecom tower (anchor)", category="anchor", connections_target=1, ramp_quarters=1,
                          kwh_per_connection_month=1_500, tariff_per_kwh=380),
        ],
        capex=[
            CapexItem(name="PV array and inverters", category="generation", amount=150_000, currency="USD", asset_life_years=20),
            CapexItem(name="Battery bank", category="storage", amount=90_000, currency="USD", asset_life_years=8),
            CapexItem(name="Diesel genset", category="generation", amount=20_000, currency="USD", asset_life_years=10),
            CapexItem(name="Distribution network", category="network", amount=120_000, currency="USD", asset_life_years=25),
            CapexItem(name="Smart meters", category="metering", amount=45_000, currency="USD", asset_life_years=10),
            CapexItem(name="Development and permitting", category="development", amount=30_000_000, currency="LCY", asset_life_years=20),
        ],
        opex=Opex(fixed_pa=18_000_000, per_connection_pa=6_000, insurance_pct_capex=0.01, collection_efficiency=0.93),
        macro=Macro(inflation_pa=0.08, tariff_indexation=0.8, fx_lcy_per_usd=600, fx_depreciation_pa=0.06,
                    tax_rate=0.30, discount_rate_pa=0.15, equity_target_irr_pa=0.18),
        financing=Financing(
            debt=[DebtTranche(name="Senior local bank loan", kind="senior", currency="LCY", share_of_capex=0.40,
                              rate_pa=0.16, tenor_years=8, grace_quarters=4, upfront_fee=0.015),
                  DebtTranche(name="Concessional loan", kind="concessional", currency="USD", share_of_capex=0.20,
                              rate_pa=0.04, tenor_years=12, grace_quarters=4, upfront_fee=0.005)],
            dsra_quarters=2, lockup_dscr=1.2, min_cash=5_000_000),
        subsidies=Subsidies(capital_grant=100_000_000, grant_milestones=[GrantMilestone(quarter=0, share=0.5), GrantMilestone(quarter=4, share=0.5)],
                            rbf_per_connection=60_000, rbf_verification_lag_quarters=2, rbf_cap=45_000_000),
        grid_arrival=GridArrival(enabled=False),
        provenance=Provenance.ILLUSTRATIVE,
    )
