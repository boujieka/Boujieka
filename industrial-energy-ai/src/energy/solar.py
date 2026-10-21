"""Module D - Solar PV engine (simplified screening model).

Accuracy statement: this is a simplified hourly model (no transposition to the tilted plane,
no shading, no spectral or IAM effects). Near the equator the optimum tilt is small, so using
horizontal irradiance (GHI) as plane-of-array irradiance is a reasonable *screening*
approximation, but results are NOT engineering-grade. For bankable yield estimates, import a
validated irradiance dataset (e.g. PVGIS, NSRDB/Meteonorm or on-site measurements) and confirm
with dedicated PV design software.

Hourly AC output per kWp:
    T_cell  = T_amb + (NOCT - 20) / 800 * G
    f_temp  = 1 + gamma * (T_cell - 25)
    P_ac    = min( G/1000 * PR_other * f_temp * eta_inv , inverter_limit )
where PR_other covers soiling, wiring, mismatch and availability ONLY (temperature and inverter
losses are modelled separately to avoid double counting).

Synthetic irradiance (offline demonstration only, labelled ILLUSTRATIVE): solar position from
standard declination / hour-angle formulas, Haurwitz clear-sky GHI, scaled by monthly
clearness factors and a seeded day-to-day variability.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from pydantic import BaseModel, Field

from src.config import HOURS_PER_YEAR
from src.energy.defaults import default
from src.energy.load_profiles import hourly_index
from src.finance.common import present_value

# Illustrative monthly clearness multipliers for a humid equatorial climate (Jan..Dec).
# Assumption for offline demonstration only - NOT measured data for any site.
ILLUSTRATIVE_MONTHLY_CLEARNESS = (0.62, 0.64, 0.63, 0.62, 0.60, 0.55, 0.50, 0.50, 0.55, 0.58, 0.60, 0.61)


@dataclass
class SolarResource:
    ghi_w_m2: np.ndarray
    ambient_c: np.ndarray
    is_synthetic: bool
    source: str
    assumptions: list[str] = field(default_factory=list)

    @property
    def annual_kwh_m2(self) -> float:
        return float(self.ghi_w_m2.sum() / 1000.0)


def solar_cos_zenith(latitude: float, longitude: float, utc_offset_h: float = 1.0) -> np.ndarray:
    """Cosine of the solar zenith angle at the middle of each hour of the reference year."""
    idx = hourly_index()
    doy = idx.dayofyear.to_numpy()
    clock = idx.hour.to_numpy() + 0.5
    b = 2 * math.pi * (doy - 81) / 364.0
    eot_min = 9.87 * np.sin(2 * b) - 7.53 * np.cos(b) - 1.5 * np.sin(b)
    solar_time = clock + (longitude - 15.0 * utc_offset_h) / 15.0 + eot_min / 60.0
    hour_angle = np.radians(15.0 * (solar_time - 12.0))
    decl = np.radians(23.45) * np.sin(2 * math.pi * (284 + doy) / 365.0)
    lat = math.radians(latitude)
    cosz = np.sin(lat) * np.sin(decl) + np.cos(lat) * np.cos(decl) * np.cos(hour_angle)
    return np.clip(cosz, 0.0, 1.0)


def synthetic_solar_resource(
    latitude: float,
    longitude: float,
    utc_offset_h: float = 1.0,
    monthly_clearness: tuple[float, ...] = ILLUSTRATIVE_MONTHLY_CLEARNESS,
    mean_temp_c: float = 26.0,
    daily_temp_swing_c: float = 8.0,
    variability: float = 0.25,
    seed: int = 7,
) -> SolarResource:
    if len(monthly_clearness) != 12:
        raise ValueError("12 monthly clearness factors are required.")
    cosz = solar_cos_zenith(latitude, longitude, utc_offset_h)
    with np.errstate(divide="ignore", over="ignore"):
        clear = np.where(cosz > 0.01, 1098.0 * cosz * np.exp(-0.059 / np.maximum(cosz, 1e-3)), 0.0)
    idx = hourly_index()
    month = idx.month.to_numpy()
    rng = np.random.default_rng(seed)
    daily = np.clip(rng.normal(1.0, variability, 365), 0.15, 1.35)
    day = idx.dayofyear.to_numpy() - 1
    k = np.asarray(monthly_clearness)[month - 1] * daily[day]
    ghi = np.clip(clear * k, 0.0, 1100.0)
    hours = idx.hour.to_numpy()
    ambient = mean_temp_c + daily_temp_swing_c / 2 * np.sin((hours - 9) / 24 * 2 * math.pi)
    return SolarResource(
        ghi_w_m2=ghi,
        ambient_c=ambient,
        is_synthetic=True,
        source="ILLUSTRATIVE synthetic irradiance (Haurwitz clear-sky x assumed clearness) - not measured data",
        assumptions=[
            f"Location {latitude:.3f}, {longitude:.3f}, UTC{utc_offset_h:+g}",
            "Clear-sky model: Haurwitz; GHI used as plane-of-array irradiance",
            f"Monthly clearness factors (assumed): {list(monthly_clearness)}",
            f"Day-to-day variability sigma={variability}, seed={seed}",
            f"Ambient temperature: {mean_temp_c} °C mean, {daily_temp_swing_c} °C daily swing (assumed)",
        ],
    )


def resource_from_arrays(ghi_w_m2, ambient_c=None, source: str = "uploaded irradiance") -> SolarResource:
    ghi = np.asarray(ghi_w_m2, dtype=float)
    if ghi.size != HOURS_PER_YEAR:
        raise ValueError(f"Irradiance series must contain {HOURS_PER_YEAR} hourly values (got {ghi.size}).")
    if np.any(ghi < 0) or np.any(ghi > 1500):
        raise ValueError("Irradiance values must lie between 0 and 1,500 W/m².")
    amb = np.full(HOURS_PER_YEAR, 26.0) if ambient_c is None else np.asarray(ambient_c, dtype=float)
    notes = [] if ambient_c is not None else ["Ambient temperature not supplied: constant 26 °C assumed"]
    return SolarResource(ghi, amb, False, source, notes)


class PVInputs(BaseModel):
    capacity_kwp: float = Field(ge=0)
    performance_ratio_other: float = Field(default("pv_other_losses_pr"), gt=0, le=1)
    temp_coeff_per_c: float = Field(default("pv_temp_coeff_per_c"), le=0, ge=-0.01)
    noct_c: float = Field(default("pv_noct_c"), gt=20, lt=70)
    inverter_efficiency: float = Field(default("pv_inverter_eff"), gt=0, le=1)
    dc_ac_ratio: float = Field(1.0, ge=1.0, le=2.0)
    degradation_per_year: float = Field(default("pv_degradation_per_year"), ge=0, lt=0.05)
    capex_per_kwp: float = Field(0.0, ge=0)
    opex_per_kwp_year: float = Field(0.0, ge=0)
    lifetime_years: int = Field(25, ge=1, le=50)
    discount_rate: float = Field(0.10, ge=0, lt=1)


def pv_output_per_kwp(resource: SolarResource, inputs: PVInputs) -> np.ndarray:
    """Year-1 AC output (kW per kWp DC) for each hour."""
    g = resource.ghi_w_m2
    t_cell = resource.ambient_c + (inputs.noct_c - 20.0) / 800.0 * g
    f_temp = 1.0 + inputs.temp_coeff_per_c * (t_cell - 25.0)
    p = g / 1000.0 * inputs.performance_ratio_other * f_temp * inputs.inverter_efficiency
    ac_limit = 1.0 / inputs.dc_ac_ratio
    return np.clip(p, 0.0, ac_limit)


class PVResults(BaseModel):
    annual_generation_kwh: float
    specific_yield_kwh_per_kwp: float
    capacity_factor: float
    self_consumed_kwh: float | None
    curtailed_kwh: float | None
    self_consumption_ratio: float | None
    solar_fraction_of_load: float | None
    lifetime_generation_kwh: float
    capex: float
    lcoe_per_kwh: float
    is_synthetic_resource: bool


def simulate_pv(resource: SolarResource, inputs: PVInputs, load_kw: np.ndarray | None = None) -> tuple[np.ndarray, PVResults]:
    """Return (hourly year-1 AC generation in kW, summary). Without storage, PV above the load is
    curtailed (no export is assumed)."""
    per_kwp = pv_output_per_kwp(resource, inputs)
    gen = per_kwp * inputs.capacity_kwp
    annual = float(gen.sum())
    self_c = curtailed = ratio = frac = None
    if load_kw is not None:
        load = np.asarray(load_kw, dtype=float)
        used = np.minimum(gen, load)
        self_c = float(used.sum())
        curtailed = annual - self_c
        ratio = self_c / annual if annual > 0 else None
        frac = self_c / float(load.sum()) if load.sum() > 0 else None
    years = inputs.lifetime_years
    energy = [annual * (1 - inputs.degradation_per_year) ** y for y in range(years)]
    capex = inputs.capex_per_kwp * inputs.capacity_kwp
    opex = [inputs.opex_per_kwp_year * inputs.capacity_kwp] * years
    pv_e = present_value(energy, inputs.discount_rate)
    lcoe = (capex + present_value(opex, inputs.discount_rate)) / pv_e if pv_e > 0 else float("nan")
    results = PVResults(
        annual_generation_kwh=annual,
        specific_yield_kwh_per_kwp=float(per_kwp.sum()),
        capacity_factor=float(per_kwp.mean()),
        self_consumed_kwh=self_c,
        curtailed_kwh=curtailed,
        self_consumption_ratio=ratio,
        solar_fraction_of_load=frac,
        lifetime_generation_kwh=float(sum(energy)),
        capex=capex,
        lcoe_per_kwh=lcoe,
        is_synthetic_resource=resource.is_synthetic,
    )
    return gen, results
