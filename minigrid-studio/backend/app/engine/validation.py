"""Input validation run before the engine (improvement: the workbook shows
#DIV/0! or #N/A, or silently computes odd results, in these situations)."""
from __future__ import annotations

from dataclasses import dataclass

from .assumptions import Assumptions


@dataclass
class Issue:
    level: str   # "error" blocks the run, "warning" is reported with the results
    field: str
    message: str


def validate(a: Assumptions) -> list[Issue]:
    out: list[Issue] = []
    inc = [l for l in a.lots if l.included == 1]
    if not inc or sum(l.grids for l in inc) <= 0:
        out.append(Issue("error", "lots", "No included lot with grids (Portfolio!S14 would be #DIV/0!)."))
    for i, l in enumerate(a.lots):
        if l.included not in (0, 1):
            out.append(Issue("error", f"lots.{i}.included", "Included flag must be 0 or 1."))
        if l.included == 1 and l.connections_per_grid <= 0:
            out.append(Issue("error", f"lots.{i}.connections_per_grid", "Included lot needs connections."))
    prof = [0.0 if v is None else v for v in a.build.build_profile]
    if any(v < 0 for v in prof):
        out.append(Issue("error", "build.build_profile", "Build shares cannot be negative."))
    if abs(sum(prof) - 1) > 1e-9:
        out.append(Issue("warning", "build.build_profile",
                         f"Build shares sum to {sum(prof):.4f}, not 1: Inputs!G141 check will flag unbuilt grids."))
    if a.reserves.dsra_months > 12:
        out.append(Issue("error", "reserves.dsra_months", "DSRA provision above 12 months (#N/A in Inputs!E375)."))
    if a.timing.construction_start <= a.timing.model_start:
        out.append(Issue("error", "timing.construction_start",
                         "Construction must start after the model start date (operations in the first column "
                         "make Model!491 read its own total)."))
    if a.timing.project_duration_years != 1:
        out.append(Issue("warning", "timing.project_duration_years",
                         "Inputs!E17 is only exact for a 1-year build; consider option fix_ops_start."))
    for name in ("sizing_method",):
        if getattr(a.debt, name) not in ("Gearing", "DSCR"):
            out.append(Issue("error", f"debt.{name}", "Must be 'Gearing' or 'DSCR'."))
        if getattr(a.refi, name) not in ("Gearing", "DSCR"):
            out.append(Issue("error", f"refi.{name}", "Must be 'Gearing' or 'DSCR'."))
    for grp, f in (("debt", "rate_choice"), ("refi", "rate_choice")):
        if getattr(getattr(a, grp), f) not in ("Fixed", "Floating"):
            out.append(Issue("error", f"{grp}.{f}", "Must be 'Fixed' or 'Floating'."))
    if a.debt.drawdown not in ("Pari Passu", "Equity first"):
        out.append(Issue("error", "debt.drawdown", "Must be 'Pari Passu' or 'Equity first'."))
    for grp, f in (("tax", "vat_capex"), ("tax", "vat_opex")):
        if getattr(a.tax, f) not in ("Recoverable", "Irrecoverable"):
            out.append(Issue("error", f"tax.{f}", "Must be 'Recoverable' or 'Irrecoverable'."))
    if a.currency.case not in (1, 2):
        out.append(Issue("error", "currency.case", "Must be 1 (USD) or 2 (LCY)."))
    if a.demand.consumption_case not in (1, 2, 3):
        out.append(Issue("error", "demand.consumption_case", "Must be 1, 2 or 3."))
    if a.debt.target_dscr <= 0:
        out.append(Issue("error", "debt.target_dscr", "Target DSCR must be positive."))
    return out


class ValidationError(ValueError):
    def __init__(self, issues: list[Issue]):
        self.issues = issues
        super().__init__("; ".join(f"{i.field}: {i.message}" for i in issues))
