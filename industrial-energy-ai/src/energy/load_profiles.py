"""Synthetic hourly load profiles.

Used ONLY when measured hourly data is unavailable. Every profile produced here carries
``is_synthetic=True`` and the list of assumptions used to build it; the UI and reports label it
"SYNTHETIC - illustrative" and it must never be presented as measured data.

Construction (documented assumptions):
* reference calendar: non-leap year starting on a Sunday (2023), 8,760 hours;
* hourly shape = base_load + (1 - base_load) x activity(hour, weekday) + cooling bump;
* activity is 1 inside the sector's operating window and 0 outside, with 1-hour ramps;
* optional seasonal multiplier (e.g. harvest season for agro-industry);
* optional annual shutdown (planned maintenance) where load drops to the base share;
* small multiplicative noise (seeded, reproducible) to avoid an unrealistically flat profile;
* the profile is finally scaled so its annual sum equals the stated annual consumption.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

import numpy as np
import pandas as pd

from src.config import HOURS_PER_YEAR

REFERENCE_YEAR = 2023  # non-leap, starts on a Sunday


def hourly_index() -> pd.DatetimeIndex:
    return pd.date_range(f"{REFERENCE_YEAR}-01-01", periods=HOURS_PER_YEAR, freq="h")


@dataclass(frozen=True)
class SectorTemplate:
    label_fr: str
    label_en: str
    base_load: float  # share of load present 24/7 (kilns, cold rooms, ventilation...)
    start_hour: int
    end_hour: int  # exclusive
    working_days: tuple[int, ...]  # Monday=0
    cooling_bump: float = 0.0  # extra afternoon load fraction (cooling)
    season_months: tuple[int, ...] = ()
    season_factor: float = 1.0
    shutdown_days: int = 0


SECTORS: dict[str, SectorTemplate] = {
    "forestry_timber": SectorTemplate("Forêt et transformation du bois", "Forestry and timber processing", 0.30, 6, 22, (0, 1, 2, 3, 4, 5), 0.0, (), 1.0, 10),
    "cement": SectorTemplate("Cimenterie", "Cement factory", 0.80, 0, 24, (0, 1, 2, 3, 4, 5, 6), 0.0, (), 1.0, 14),
    "mining": SectorTemplate("Mines", "Mining operations", 0.75, 0, 24, (0, 1, 2, 3, 4, 5, 6), 0.0, (), 1.0, 7),
    "agro_industrial": SectorTemplate("Agro-industrie", "Agro-industrial facility", 0.25, 6, 20, (0, 1, 2, 3, 4, 5), 0.05, (6, 7, 8, 9), 1.3, 7),
    "manufacturing": SectorTemplate("Industrie manufacturière", "Manufacturing plant", 0.20, 6, 22, (0, 1, 2, 3, 4), 0.05, (), 1.0, 10),
    "industrial_zone": SectorTemplate("Zone économique industrielle", "Industrial economic zone", 0.35, 6, 22, (0, 1, 2, 3, 4, 5), 0.10, (), 1.0, 0),
    "commercial_center": SectorTemplate("Centre commercial", "Commercial center", 0.25, 8, 21, (0, 1, 2, 3, 4, 5, 6), 0.20, (), 1.0, 0),
    "hotel": SectorTemplate("Hôtel", "Hotel", 0.45, 6, 23, (0, 1, 2, 3, 4, 5, 6), 0.15, (), 1.0, 0),
    "cold_storage": SectorTemplate("Entreposage frigorifique", "Cold storage facility", 0.70, 7, 19, (0, 1, 2, 3, 4, 5), 0.20, (), 1.0, 0),
    "logistics": SectorTemplate("Logistique", "Logistics facility", 0.30, 6, 22, (0, 1, 2, 3, 4, 5), 0.05, (), 1.0, 0),
}


@dataclass
class LoadProfile:
    values_kw: np.ndarray
    is_synthetic: bool
    source: str
    assumptions: list[str] = field(default_factory=list)
    filled_mask: np.ndarray | None = None  # True where values were filled/imputed

    @property
    def annual_kwh(self) -> float:
        return float(self.values_kw.sum())

    @property
    def peak_kw(self) -> float:
        return float(self.values_kw.max())

    @property
    def load_factor(self) -> float:
        peak = self.peak_kw
        return float(self.values_kw.mean() / peak) if peak > 0 else 0.0

    def to_dict(self) -> dict:
        return {
            "values_kw": [round(float(v), 4) for v in self.values_kw],
            "is_synthetic": self.is_synthetic,
            "source": self.source,
            "assumptions": list(self.assumptions),
            "filled_mask": None if self.filled_mask is None else [bool(x) for x in self.filled_mask],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LoadProfile":
        mask = data.get("filled_mask")
        return cls(
            values_kw=np.asarray(data["values_kw"], dtype=float),
            is_synthetic=bool(data["is_synthetic"]),
            source=data.get("source", ""),
            assumptions=list(data.get("assumptions", [])),
            filled_mask=None if mask is None else np.asarray(mask, dtype=bool),
        )


def _activity(hours: np.ndarray, start: int, end: int) -> np.ndarray:
    """1 inside [start, end) with 1-hour linear ramps at both edges."""
    if start == 0 and end == 24:
        return np.ones_like(hours, dtype=float)
    act = ((hours >= start) & (hours < end)).astype(float)
    act[hours == start] = 0.5
    act[hours == end - 1] = 0.5
    return act


def synthetic_load_profile(
    sector: str,
    annual_kwh: float,
    seed: int = 42,
    noise: float = 0.03,
    template: SectorTemplate | None = None,
) -> LoadProfile:
    if annual_kwh <= 0:
        raise ValueError("Annual consumption must be positive to build a synthetic profile.")
    tpl = template or SECTORS.get(sector)
    if tpl is None:
        raise ValueError(f"Unknown sector '{sector}'. Known: {sorted(SECTORS)}")
    idx = hourly_index()
    hours = idx.hour.to_numpy()
    weekday = idx.weekday.to_numpy()
    month = idx.month.to_numpy()
    doy = idx.dayofyear.to_numpy()

    working = np.isin(weekday, tpl.working_days)
    activity = _activity(hours, tpl.start_hour, tpl.end_hour) * working
    cooling = tpl.cooling_bump * np.clip(np.sin((hours - 9) / 10 * np.pi), 0, None)
    shape = tpl.base_load + (1 - tpl.base_load) * activity + cooling
    if tpl.season_months:
        shape = np.where(np.isin(month, tpl.season_months), shape * tpl.season_factor, shape)
    if tpl.shutdown_days:
        # Planned shutdown placed in August (dry-season maintenance window, assumption).
        start_doy = 213
        in_shutdown = (doy >= start_doy) & (doy < start_doy + tpl.shutdown_days)
        shape = np.where(in_shutdown, tpl.base_load * 0.5, shape)
    rng = np.random.default_rng(seed)
    shape = shape * rng.lognormal(mean=0.0, sigma=noise, size=shape.size)
    values = shape / shape.sum() * annual_kwh

    assumptions = [
        f"Sector template: {tpl.label_en}",
        f"Base (24/7) load share: {tpl.base_load:.0%}",
        f"Operating window: {tpl.start_hour:02d}:00-{tpl.end_hour:02d}:00 on days {list(tpl.working_days)} (Mon=0)",
        f"Afternoon cooling bump: {tpl.cooling_bump:.0%}",
        f"Seasonal factor {tpl.season_factor} in months {list(tpl.season_months)}" if tpl.season_months else "No seasonality",
        f"Planned shutdown: {tpl.shutdown_days} days from day 213 (assumption)" if tpl.shutdown_days else "No planned shutdown",
        f"Multiplicative noise sigma={noise}, seed={seed}",
        f"Scaled to {annual_kwh:,.0f} kWh/year",
    ]
    return LoadProfile(values, True, f"SYNTHETIC profile - sector template '{sector}'", assumptions)


def template_as_dict(sector: str) -> dict:
    return asdict(SECTORS[sector])
