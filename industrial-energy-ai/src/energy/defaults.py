"""Default technical assumptions.

Every value here is a *generic screening default*, not a measured or vendor-specific value.
They are exposed in the UI, editable per project, and reported in the "Assumptions and
limitations" section of every report. Replace them with site measurements or equipment data
sheets before using any result for an investment decision.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Assumption:
    value: float
    unit: str
    note: str


DEFAULTS: dict[str, Assumption] = {
    # Diesel
    "diesel_lhv_mj_per_l": Assumption(35.9, "MJ/L", "Typical lower heating value of automotive gas oil; varies with fuel quality."),
    "diesel_co2_kg_per_l": Assumption(2.68, "kgCO2/L", "Combustion-only CO2 factor commonly derived from IPCC 2006 defaults; excludes upstream and transport emissions."),
    "diesel_sfc_l_per_kwh": Assumption(0.28, "L/kWh", "Indicative average specific fuel consumption at moderate load; strongly load-dependent."),
    "diesel_min_loading": Assumption(0.30, "fraction", "Generic minimum recommended loading; manufacturers specify their own limits."),
    # Solar PV
    "pv_temp_coeff_per_c": Assumption(-0.004, "1/°C", "Typical crystalline-silicon power temperature coefficient (about -0.3 to -0.5 %/°C)."),
    "pv_noct_c": Assumption(45.0, "°C", "Typical nominal operating cell temperature."),
    "pv_other_losses_pr": Assumption(0.88, "fraction", "Soiling, wiring, mismatch, availability losses EXCLUDING temperature and inverter losses (modelled separately)."),
    "pv_inverter_eff": Assumption(0.97, "fraction", "Typical weighted inverter efficiency."),
    "pv_degradation_per_year": Assumption(0.005, "fraction/yr", "Typical crystalline module degradation."),
    # Battery
    "bess_charge_eff": Assumption(0.95, "fraction", "Typical lithium-ion one-way efficiency (round trip about 0.90)."),
    "bess_discharge_eff": Assumption(0.95, "fraction", "Typical lithium-ion one-way efficiency."),
    "bess_soc_min": Assumption(0.10, "fraction", "Generic minimum state of charge."),
    "bess_soc_max": Assumption(0.95, "fraction", "Generic maximum state of charge."),
    # Biomass
    "water_latent_heat_mj_per_kg": Assumption(2.443, "MJ/kg", "Latent heat of vaporisation of water at 25 °C (physical constant used in LHV moisture correction)."),
    # Finance
    "value_of_lost_load_per_kwh_factor": Assumption(3.0, "x diesel cost", "Penalty on unserved energy used by the optimiser, expressed as a multiple of the diesel marginal cost; reflects business-interruption cost and must be set per site."),
}


def default(name: str) -> float:
    return DEFAULTS[name].value
