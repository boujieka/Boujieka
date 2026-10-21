"""Three SYNTHETIC demonstration projects (Republic of Congo).

All values are invented for demonstration. They do not describe any real company, site,
contract or tariff, and the monetary values are placeholders, not market prices.
Company names are prefixed "DEMO" and every project is flagged ``is_synthetic=True``.
"""

from __future__ import annotations

from src.assumptions import (
    BatteryAssumptions,
    BiomassAssumptions,
    DieselAssumptions,
    FinanceAssumptions,
    GridAssumptions,
    ProjectAssumptions,
    PVAssumptions,
    ReliabilityAssumptions,
    SiteData,
)

SYNTHETIC_NOTICE = ("SYNTHETIC DEMONSTRATION DATA - invented values for illustration only; "
                    "not measured data, not market prices, not a real company.")


def forestry() -> dict:
    a = ProjectAssumptions(
        baseline_scenario="diesel_only",
        site=SiteData(latitude=1.61, longitude=16.05, annual_consumption_kwh=6_000_000, declared_peak_kw=1300, load_seed=101),
        diesel=DieselAssumptions(existing_kw=2000, n_units=4, sfc_l_per_kwh=0.30, fuel_price_per_l=750, fuel_transport_per_l=110,
                                 variable_om_per_kwh=14, fixed_om_per_year=40_000_000, overhaul_cost=60_000_000, overhaul_interval_hours=24_000),
        pv=PVAssumptions(capex_per_kwp=480_000, opex_per_kwp_year=7_000, max_kwp=6_000),
        battery=BatteryAssumptions(capex_per_kwh=230_000, capex_per_kw=60_000),
        biomass=BiomassAssumptions(enabled=True, biomass_type="wood_residues", annual_availability_t=12_000, lhv_dry_mj_per_kg=18.5,
                                   moisture_content=0.45, electrical_efficiency=0.18, thermal_efficiency=0.45, capex_per_kw=2_300_000,
                                   fixed_opex_per_kw_year=75_000, variable_opex_per_kwh=15, fuel_cost_per_t=2_000,
                                   fuel_preparation_cost_per_t=3_000, max_kw=1_000, heat_value_per_kwh_th=0),
        grid=GridAssumptions(enabled=False),
        reliability=ReliabilityAssumptions(value_of_lost_load_per_kwh=2_500, max_unserved_fraction=0.001),
        finance=FinanceAssumptions(debt_share=0.6, interest_rate=0.08, tenor_years=8, grace_years=1, equipment_currency="EUR",
                                   equipment_cost_share=0.7, ppa_tariff_per_kwh=230, eaas_fee_per_year=900_000_000),
        notes=SYNTHETIC_NOTICE + " Sawmill and kiln drying in Sangha (northern Congo); off-grid; wood residues available on site.",
    )
    return {
        "code": "DEMO-FOR-01", "company_name": "DEMO Bois du Nord (synthetic)", "sector": "forestry_timber",
        "region": "Sangha (northern Republic of Congo)", "latitude": 1.61, "longitude": 16.05,
        "annual_demand_kwh": 6_000_000, "peak_demand_kw": 1300, "installed_capacity_kw": 2000,
        "existing_technologies": ["diesel"], "annual_fuel_l": 1_800_000, "operating_hours": 8760,
        "data_sources": SYNTHETIC_NOTICE, "data_quality": "C", "is_synthetic": True,
        "notes": a.notes, "assumptions": a.model_dump(),
    }


def cement() -> dict:
    a = ProjectAssumptions(
        baseline_scenario="grid_diesel",
        site=SiteData(latitude=-4.20, longitude=13.90, annual_consumption_kwh=40_000_000, declared_peak_kw=5_800, load_seed=202),
        diesel=DieselAssumptions(existing_kw=6000, n_units=6, sfc_l_per_kwh=0.27, fuel_price_per_l=700, fuel_transport_per_l=40,
                                 variable_om_per_kwh=10, fixed_om_per_year=90_000_000, overhaul_cost=150_000_000,
                                 overhaul_interval_hours=30_000, allow_new_capacity=False),
        pv=PVAssumptions(capex_per_kwp=430_000, opex_per_kwp_year=6_000, max_kwp=15_000),
        battery=BatteryAssumptions(capex_per_kwh=210_000, capex_per_kw=55_000),
        biomass=BiomassAssumptions(enabled=False),
        grid=GridAssumptions(enabled=True, existing_connection=True, voltage_level="HV", energy_tariff_per_kwh=85,
                             transmission_charge_per_kwh=0, distribution_charge_per_kwh=0, demand_charge_per_kw_month=1_500,
                             fixed_charge_per_month=2_000_000, maintenance_cost_per_year=30_000_000, availability=0.85,
                             average_outage_hours=6, max_import_kw=8_000),
        reliability=ReliabilityAssumptions(value_of_lost_load_per_kwh=3_000, max_unserved_fraction=0.001),
        finance=FinanceAssumptions(debt_share=0.65, interest_rate=0.075, tenor_years=10, grace_years=1, equipment_currency="EUR",
                                   equipment_cost_share=0.75, ppa_tariff_per_kwh=95),
        notes=SYNTHETIC_NOTICE + " Electrical loads only (grinding, kiln drives, fans, conveyors). Thermal process energy for the kiln "
              "(clinker burning, about 3.0-3.5 GJ per tonne of clinker in modern dry-process kilns - indicative literature range) is "
              "supplied by kiln fuel and is NOT modelled in the electrical optimisation.",
    )
    return {
        "code": "DEMO-CEM-02", "company_name": "DEMO Ciments du Sud (synthetic)", "sector": "cement",
        "region": "Bouenza (southern Republic of Congo)", "latitude": -4.20, "longitude": 13.90,
        "annual_demand_kwh": 40_000_000, "peak_demand_kw": 5800, "installed_capacity_kw": 6000,
        "existing_technologies": ["grid", "diesel"], "annual_fuel_l": None, "operating_hours": 8760,
        "data_sources": SYNTHETIC_NOTICE, "data_quality": "C", "is_synthetic": True,
        "notes": a.notes, "assumptions": a.model_dump(),
        "thermal_process_energy": {"clinker_t_per_year": 350_000, "specific_heat_gj_per_t_clinker": 3.3,
                                   "annual_thermal_gj": 350_000 * 3.3, "note": "Synthetic; outside the electrical model."},
    }


def cold_storage() -> dict:
    a = ProjectAssumptions(
        baseline_scenario="grid_diesel",
        site=SiteData(latitude=-4.26, longitude=15.24, annual_consumption_kwh=2_500_000, declared_peak_kw=420, load_seed=303),
        diesel=DieselAssumptions(existing_kw=600, n_units=2, sfc_l_per_kwh=0.29, fuel_price_per_l=700, fuel_transport_per_l=20,
                                 variable_om_per_kwh=15, fixed_om_per_year=8_000_000, overhaul_cost=15_000_000, overhaul_interval_hours=20_000),
        pv=PVAssumptions(capex_per_kwp=470_000, opex_per_kwp_year=7_000, max_kwp=1_200),
        battery=BatteryAssumptions(capex_per_kwh=230_000, capex_per_kw=60_000),
        biomass=BiomassAssumptions(enabled=False),
        grid=GridAssumptions(enabled=True, existing_connection=True, voltage_level="MV", energy_tariff_per_kwh=95,
                             demand_charge_per_kw_month=1_200, fixed_charge_per_month=250_000, maintenance_cost_per_year=3_000_000,
                             availability=0.80, average_outage_hours=4, max_import_kw=600),
        reliability=ReliabilityAssumptions(value_of_lost_load_per_kwh=4_000, max_unserved_fraction=0.0005),
        finance=FinanceAssumptions(debt_share=0.5, interest_rate=0.085, tenor_years=7, grace_years=1, equipment_currency="EUR",
                                   equipment_cost_share=0.7, ppa_tariff_per_kwh=140),
        notes=SYNTHETIC_NOTICE + " Cold store in Brazzaville; refrigeration compressors run 24/7 with afternoon peak; frequent grid outages.",
    )
    return {
        "code": "DEMO-COLD-03", "company_name": "DEMO Froid Brazzaville (synthetic)", "sector": "cold_storage",
        "region": "Brazzaville", "latitude": -4.26, "longitude": 15.24,
        "annual_demand_kwh": 2_500_000, "peak_demand_kw": 420, "installed_capacity_kw": 600,
        "existing_technologies": ["grid", "diesel"], "annual_fuel_l": None, "operating_hours": 8760,
        "data_sources": SYNTHETIC_NOTICE, "data_quality": "C", "is_synthetic": True,
        "notes": a.notes, "assumptions": a.model_dump(),
    }


def all_case_studies() -> list[dict]:
    return [forestry(), cement(), cold_storage()]


def seed_demo_projects(session) -> list:
    """Insert the demonstration projects if they are not present (idempotent)."""
    from sqlalchemy import select

    from src.database.models import Project
    from src.database.repository import create_project

    created = []
    for case in all_case_studies():
        if session.scalar(select(Project.id).where(Project.code == case["code"])):
            continue
        data = {k: v for k, v in case.items() if k != "thermal_process_energy"}
        if "thermal_process_energy" in case:
            data["notes"] = data["notes"] + f" [thermal: {case['thermal_process_energy']}]"
        created.append(create_project(session, data))
    return created
