"""Optional improvements over the reference workbook.

Every option defaults to the workbook's behaviour (``False``). A run with any
option enabled is no longer comparable to Excel: results carry the list of
enabled options and are labelled "variant" (not "reconciled").
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, fields


@dataclass(frozen=True)
class EngineOptions:
    fix_ops_start: bool = False
    """Inputs!E17 uses EOMONTH(Con_Start, E14*(12-1))+1, right only for a
    one-year build. Variant: EOMONTH(Con_Start, E14*12-1)+1 (audit obs. 1)."""

    fix_fixed_rate_by_year: bool = False
    """Debt!43 looks up the fixed all-in rate with the tenor flag (always
    period 1). Variant: look it up with the year in tenor, as Debt!39 and the
    refinancing rows do."""

    fix_base_rate_lookup: bool = False
    """Inputs!K406 holds the text "2023+", which LOOKUP skips: years from 2023
    use the 2022 base rate. Variant: treat "2023+" as 2023 (audit section 5)."""

    cap_principal_at_balance: bool = False
    """Debt!32 can repay more than the outstanding balance when CFADS is high.
    Variant: principal capped at opening balance + drawdown."""

    include_expansion_racking: bool = False
    """Model!645 (expansion racking) is empty although Inputs!E120 prices it.
    Variant: add Inputs!E120 per module, FX-adjusted like PV (row 630)."""

    def enabled(self) -> list[str]:
        return [f.name for f in fields(self) if getattr(self, f.name)]

    @property
    def faithful(self) -> bool:
        return not self.enabled()

    def as_dict(self) -> dict:
        return asdict(self)


FAITHFUL = EngineOptions()


def option_docs() -> dict[str, str]:
    """Docstrings written under each field above, for the API."""
    import inspect
    src = inspect.getsource(EngineOptions)
    out = {}
    for name in EngineOptions.__dataclass_fields__:
        doc = src.split(f"{name}: bool = False", 1)[1].split('"""')[1]
        out[name] = " ".join(doc.split())
    return out
