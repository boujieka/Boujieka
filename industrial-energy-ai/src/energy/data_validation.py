"""Module B - energy data validation and standardisation.

Takes user data (CSV/Excel tables, PDF bills) and produces:
* a :class:`ValidationReport` listing every issue found (missing values, unit problems,
  inconsistent or duplicate timestamps, negative consumption, unreasonable capacity factors,
  conflicting fuel data);
* a standardised 8,760-hour demand profile in kW on a non-leap reference calendar, with a mask
  of the hours that were imputed.

Nothing is silently corrected: every transformation is recorded as an issue with its count.
"""

from __future__ import annotations

import io
import logging
import re
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import pandas as pd

from src.config import HOURS_PER_YEAR
from src.energy.load_profiles import LoadProfile

log = logging.getLogger(__name__)

Severity = Literal["info", "warning", "error"]
UNIT_TO_KW = {"W": 1e-3, "kW": 1.0, "MW": 1e3}


@dataclass
class Issue:
    code: str
    severity: Severity
    message: str
    count: int = 0


@dataclass
class ValidationReport:
    issues: list[Issue] = field(default_factory=list)
    coverage: float = 0.0  # share of the 8,760 reference hours backed by measurements
    rows_read: int = 0

    def add(self, code: str, severity: Severity, message: str, count: int = 0) -> None:
        self.issues.append(Issue(code, severity, message, count))

    @property
    def has_errors(self) -> bool:
        return any(i.severity == "error" for i in self.issues)

    def codes(self) -> set[str]:
        return {i.code for i in self.issues}

    def to_dict(self) -> dict:
        return {
            "coverage": self.coverage,
            "rows_read": self.rows_read,
            "issues": [i.__dict__ for i in self.issues],
        }

    @property
    def quality_score(self) -> str:
        """Coarse data-quality indicator: A (measured, complete) to D (unusable)."""
        if self.has_errors:
            return "D"
        warnings = sum(1 for i in self.issues if i.severity == "warning")
        if self.coverage >= 0.95 and warnings == 0:
            return "A"
        if self.coverage >= 0.80 and warnings <= 2:
            return "B"
        return "C"


def read_table(content: bytes, filename: str) -> pd.DataFrame:
    name = filename.lower()
    if name.endswith((".xlsx", ".xlsm", ".xls")):
        return pd.read_excel(io.BytesIO(content))
    if name.endswith((".csv", ".txt")):
        sample = content[:4096].decode("utf-8", errors="replace")
        sep = ";" if sample.count(";") > sample.count(",") else ","
        decimal = "," if sep == ";" else "."
        return pd.read_csv(io.BytesIO(content), sep=sep, decimal=decimal)
    raise ValueError("Unsupported table format (use CSV or Excel).")


def guess_columns(df: pd.DataFrame) -> tuple[str | None, str | None]:
    """Best guess of (timestamp column, numeric value column)."""
    ts_col = None
    for col in df.columns:
        if re.search(r"date|time|heure|horodat|timestamp", str(col), re.I):
            ts_col = col
            break
    numeric = [c for c in df.columns if c != ts_col and pd.api.types.is_numeric_dtype(df[c])]
    value_col = None
    for col in numeric:
        if re.search(r"kw|load|charge|demand|puissance|power|conso", str(col), re.I):
            value_col = col
            break
    if value_col is None and numeric:
        value_col = numeric[0]
    return ts_col, value_col


def standardise_hourly_profile(
    df: pd.DataFrame,
    timestamp_col: str,
    value_col: str,
    unit: str = "kW",
    quantity: Literal["power", "energy"] = "power",
    declared_peak_kw: float | None = None,
    source: str = "uploaded measurements",
) -> tuple[LoadProfile | None, ValidationReport]:
    """Validate a time series and convert it to an 8,760-hour kW profile.

    ``quantity='energy'`` means each value is the energy (in ``unit``h) consumed during its
    interval; it is converted to average power by dividing by the interval length.
    """
    report = ValidationReport(rows_read=len(df))
    if unit not in UNIT_TO_KW:
        report.add("unit_unknown", "error", f"Unknown unit '{unit}'. Use W, kW or MW (or Wh, kWh, MWh with quantity=energy).")
        return None, report
    if timestamp_col not in df.columns or value_col not in df.columns:
        report.add("column_missing", "error", "Timestamp or value column not found.")
        return None, report

    ts = pd.to_datetime(df[timestamp_col], errors="coerce", dayfirst=True)
    vals = pd.to_numeric(df[value_col], errors="coerce")
    bad_ts = int(ts.isna().sum())
    if bad_ts:
        report.add("timestamp_invalid", "warning", "Rows with unreadable timestamps were dropped.", bad_ts)
    missing_vals = int((vals.isna() & ts.notna()).sum())
    if missing_vals:
        report.add("missing_values", "warning", "Missing or non-numeric values (later imputed).", missing_vals)
    series = pd.Series(vals.to_numpy(), index=ts).loc[lambda s: s.index.notna()]
    if series.empty:
        report.add("no_data", "error", "No usable rows.")
        return None, report

    if not series.index.is_monotonic_increasing:
        report.add("timestamp_unsorted", "info", "Timestamps were not in chronological order; they were sorted.")
        series = series.sort_index()
    dup = int(series.index.duplicated().sum())
    if dup:
        report.add("duplicate_timestamps", "warning", "Duplicate timestamps; duplicates were averaged.", dup)
        series = series.groupby(level=0).mean()

    neg = int((series < 0).sum())
    if neg:
        report.add("negative_consumption", "warning", "Negative consumption values were treated as missing.", neg)
        series = series.where(series >= 0)

    # Interval detection.
    diffs = series.index.to_series().diff().dropna().dt.total_seconds() / 3600.0
    if diffs.empty:
        report.add("too_short", "error", "At least two timestamps are needed.")
        return None, report
    step_h = float(diffs.median())
    irregular = int((np.abs(diffs - step_h) > 1e-6).sum())
    if irregular:
        report.add("timestamp_irregular", "warning", f"Irregular intervals around the median step of {step_h:g} h.", irregular)
    if step_h > 1.0 + 1e-9:
        report.add(
            "resolution_too_coarse", "error",
            f"Data resolution is {step_h:g} h; hourly or finer data is required. Use the synthetic profile with the annual total instead.",
        )
        return None, report

    kw = series * UNIT_TO_KW[unit]
    if quantity == "energy":
        kw = kw / step_h
    hourly = kw.resample("h").mean()

    # Map to the non-leap reference calendar: drop 29 February, average over years.
    hourly = hourly[~((hourly.index.month == 2) & (hourly.index.day == 29))]
    years = hourly.index.year.unique()
    if len(years) > 1:
        report.add("multi_year", "info", f"Data spans {len(years)} calendar years; values were averaged per hour of year.")
    key = (hourly.index.dayofyear - ((hourly.index.is_leap_year) & (hourly.index.month > 2)).astype(int) - 1) * 24 + hourly.index.hour
    by_hour = hourly.groupby(key).mean()
    profile = pd.Series(np.nan, index=np.arange(HOURS_PER_YEAR))
    profile.loc[by_hour.index.intersection(profile.index)] = by_hour
    measured = profile.notna().to_numpy()
    report.coverage = float(measured.mean())

    if report.coverage < 1.0:
        gaps = HOURS_PER_YEAR - int(measured.sum())
        sev: Severity = "warning" if report.coverage >= 0.5 else "error"
        report.add("incomplete_year", sev, f"{gaps} of {HOURS_PER_YEAR} reference hours have no data; they were imputed.", gaps)
        if sev == "error":
            report.add("insufficient_coverage", "error", "Less than 50% of the year is covered; imputation would dominate the profile.")

    filled = _impute(profile)
    values = filled.to_numpy(dtype=float)
    if np.isnan(values).any():
        report.add("imputation_failed", "error", "Profile could not be completed.")
        return None, report

    peak = float(values.max())
    mean = float(values.mean())
    lf = mean / peak if peak > 0 else 0.0
    if peak <= 0:
        report.add("zero_load", "error", "The profile has no positive consumption.")
        return None, report
    if not 0.05 <= lf <= 0.98:
        report.add("unreasonable_load_factor", "warning", f"Load factor {lf:.2f} is outside the usual 0.05-0.98 range: check the unit and the data.")
    if declared_peak_kw:
        ratio = peak / declared_peak_kw
        if ratio > 20 or ratio < 0.05:
            report.add("unit_suspect", "error", f"Peak {peak:,.1f} kW is {ratio:.3g} x the declared peak demand: the unit is probably wrong (W/kW/MW).")
        elif ratio > 1.5 or ratio < 0.5:
            report.add("peak_mismatch", "warning", f"Measured peak ({peak:,.0f} kW) differs from declared peak ({declared_peak_kw:,.0f} kW) by more than 50%.")

    profile_obj = LoadProfile(
        values_kw=values,
        is_synthetic=False,
        source=source,
        assumptions=[f"Imputed hours: {int((~measured).sum())} (same hour-of-week average, then linear interpolation)"],
        filled_mask=~measured,
    )
    return profile_obj, report


def _impute(profile: pd.Series) -> pd.Series:
    """Fill gaps: short gaps (<=3 h) by linear interpolation, longer gaps with the mean of the
    same hour of the week, finally any remainder with the same hour of day."""
    s = profile.copy()
    s = s.interpolate(limit=3, limit_area="inside")
    how = np.arange(HOURS_PER_YEAR) % 168
    how_mean = s.groupby(how).transform("mean")
    s = s.fillna(how_mean)
    hod_mean = s.groupby(np.arange(HOURS_PER_YEAR) % 24).transform("mean")
    return s.fillna(hod_mean)


def check_fuel_consistency(
    annual_fuel_l: float | None,
    annual_generation_kwh: float | None,
    installed_capacity_kw: float | None = None,
    operating_hours: float | None = None,
) -> list[Issue]:
    """Cross-check declared diesel fuel, generation, capacity and running hours."""
    issues: list[Issue] = []
    if annual_fuel_l and annual_generation_kwh:
        sfc = annual_fuel_l / annual_generation_kwh
        if sfc < 0.20 or sfc > 0.60:
            issues.append(Issue("fuel_conflict", "warning", f"Implied specific fuel consumption {sfc:.3f} L/kWh is outside 0.20-0.60 L/kWh: fuel and generation records conflict or units are wrong."))
    if installed_capacity_kw and annual_generation_kwh:
        cf = annual_generation_kwh / (installed_capacity_kw * HOURS_PER_YEAR)
        if cf > 1.0:
            issues.append(Issue("capacity_factor_impossible", "error", f"Generation implies a capacity factor of {cf:.0%} (>100%)."))
        elif cf > 0.9:
            issues.append(Issue("capacity_factor_high", "warning", f"Capacity factor {cf:.0%} is unusually high for a diesel fleet."))
    if installed_capacity_kw and annual_generation_kwh and operating_hours:
        if operating_hours > HOURS_PER_YEAR:
            issues.append(Issue("hours_impossible", "error", "Operating hours exceed 8,760 h/year."))
        elif annual_generation_kwh > installed_capacity_kw * operating_hours * 1.0001:
            issues.append(Issue("hours_conflict", "error", "Generation exceeds capacity x operating hours."))
    return issues


# --------------------------------------------------------------------------------------------
# PDF electricity bills: candidate extraction only. Values are proposals that the user must
# confirm; the text is untrusted and is never passed to an AI model as instructions.
# --------------------------------------------------------------------------------------------
_NUM = r"(\d{1,3}(?:[ .  ]\d{3})+|\d+)(?:[,.](\d+))?"


def _to_float(int_part: str, dec: str | None) -> float:
    return float(re.sub(r"[ .  ]", "", int_part) + ("." + dec if dec else ""))


def extract_pdf_text(content: bytes, max_pages: int = 20) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(content))
    return "\n".join((page.extract_text() or "") for page in reader.pages[:max_pages])


def extract_bill_candidates(text: str) -> dict[str, list[float]]:
    """Find candidate kWh quantities and amounts in a bill's text."""
    kwh = [_to_float(m.group(1), m.group(2)) for m in re.finditer(_NUM + r"\s*kWh", text, re.I)]
    amounts = [_to_float(m.group(1), m.group(2)) for m in re.finditer(_NUM + r"\s*(?:FCFA|XAF|F\s?CFA)", text, re.I)]
    return {"kwh": kwh, "amount_xaf": amounts}
