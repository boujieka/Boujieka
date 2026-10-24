"""Typed assumption set of the AssetCo model.

Every field carries the workbook cell it comes from (``cell`` metadata), so a
value can be traced back to the reference .xlsm and loaded from it. Units are
stated in ``unit``; amounts are in the *model currency* selected by
``currency.case`` (1 = USD, 2 = local currency), exactly as in the workbook.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
from dataclasses import dataclass, field
from typing import Any, Literal, Optional


def inp(cell: str, unit: str = "", doc: str = "", default: Any = dataclasses.MISSING):
    md = {"cell": cell, "unit": unit, "doc": doc}
    if default is dataclasses.MISSING:
        return field(metadata=md)
    if isinstance(default, list):
        return field(default_factory=lambda d=default: list(d), metadata=md)
    return field(default=default, metadata=md)


# ----------------------------------------------------------------------- currency
MoneyBasis = Literal["usd", "usd_and_lcy", "lcy_contracted"]
VatClass = Literal["capex", "opex", "none"]


@dataclass
class MoneyInput:
    """A monetary assumption of the *Currency* sheet.

    basis ``usd``: amount typed in USD (column H), LCY = USD x exchange rate.
    basis ``usd_and_lcy``: both columns typed (H and I).
    basis ``lcy_contracted``: amount contracted in LCY, typed as its USD value at
    the base rate (column K); LCY = K x base rate, USD = LCY / exchange rate.
    ``vat``: VAT gross-up class when the VAT category is irrecoverable.
    """
    value: float
    basis: MoneyBasis = "usd"
    vat: VatClass = "none"
    lcy_value: Optional[float] = None  # only for basis usd_and_lcy


@dataclass
class Currency:
    case: int = inp("Currency!F18", "1=USD, 2=LCY", "Model currency")
    effective_year: int = inp("Currency!F11", "year", "Year of the exchange rate applied to USD inputs")
    base_exchange_rate: float = inp("Currency!F16", "LCY/USD")
    mmra_starting_balance: MoneyInput = inp("Currency!H28", "currency")
    all_in_cost_of_debt: MoneyInput = inp("Currency!H29", "% p.a.", "Fixed all-in rate; LCY rate in I29")
    capex_net_of_grant: MoneyInput = inp("Currency!H33", "currency/connection")
    grant_per_connection: MoneyInput = inp("Currency!H34", "currency/connection")
    battery_cost: MoneyInput = inp("Currency!H35", "currency/kWh")
    transfer_fee: MoneyInput = inp("Currency!H36", "currency/connection")
    fixed_fee_per_grid: MoneyInput = inp("Currency!K39", "currency/grid/year")
    diesel_price: MoneyInput = inp("Currency!H40", "currency/litre")
    pv_price: MoneyInput = inp("Currency!H44", "currency/W")
    battery_racking: MoneyInput = inp("Currency!H45", "currency/kWh")
    battery_installation: MoneyInput = inp("Currency!K46", "currency/kWh")
    battery_replacement_2023: MoneyInput = inp("Currency!H47", "currency/kWh")
    inverter_price_2020: MoneyInput = inp("Currency!H48", "currency/W")
    expansion_racking: MoneyInput = inp("Currency!H49", "currency/module")
    expansion_logistics: MoneyInput = inp("Currency!K50", "currency/module")
    bnef_battery_2030: MoneyInput = inp("Currency!H51", "currency/kWh")
    inverter_2030: MoneyInput = inp("Currency!H52", "currency/W")
    fee_per_customer: MoneyInput = inp("Currency!K55", "currency/connection/month")
    admin_costs: MoneyInput = inp("Currency!H56", "currency/year")
    tariff: MoneyInput = inp("Currency!K59", "currency/kWh")
    grid_arrival_tariff: MoneyInput = inp("Currency!K60", "currency/kWh")
    amt_threshold: MoneyInput = inp("Currency!K63", "currency")
    sizing_rounding: MoneyInput = inp("Currency!H64", "digits", "ROUND(x, -digits) tolerance of the sizing macros")


# ---------------------------------------------------------------------- portfolio
@dataclass
class Lot:
    """One column E..J of the *Portfolio* sheet. Optional fields left to None
    inherit the portfolio-wide value (the workbook's =$E$.. chain)."""
    name: str
    included: int
    country: str
    grids: float
    connections_per_grid: float
    kwp_per_grid: float
    people_per_connection: float
    baseline_kwh_month: float
    peak_kwh_month: float
    expansion_module_kw: float
    tariff: Optional[float] = None
    capex_net_of_grant: Optional[float] = None
    transfer_fee: Optional[float] = None
    grant_per_connection: Optional[float] = None
    battery_cost: Optional[float] = None
    fixed_fee_per_grid: Optional[float] = None
    fee_per_customer: Optional[float] = None
    ratchet_share: Optional[float] = None
    diesel_price: Optional[float] = None


LOT_COLUMNS = "EFGHIJ"
LOT_ROWS = {  # Portfolio sheet rows
    "name": 8, "included": 9, "country": 10, "grids": 13, "connections_per_grid": 14,
    "kwp_per_grid": 16, "people_per_connection": 18, "baseline_kwh_month": 22, "peak_kwh_month": 23,
    "expansion_module_kw": 40, "tariff": 26, "capex_net_of_grant": 29, "transfer_fee": 30,
    "grant_per_connection": 34, "battery_cost": 41, "fixed_fee_per_grid": 44, "fee_per_customer": 45,
    "ratchet_share": 46, "diesel_price": 47,
}


# ------------------------------------------------------------------------- groups
@dataclass
class Timing:
    model_start: dt.date = inp("Inputs!E6", "date")
    construction_start: dt.date = inp("Inputs!E9", "date")
    project_duration_years: float = inp("Inputs!E14", "years", "Construction duration of one grid")
    lifetime_years: float = inp("Inputs!E18", "years", "Lifetime of grid / operations")


@dataclass
class Technical:
    yield_kwh_per_kwp: float = inp("Inputs!E39", "kWh/kWp/year")
    self_consumption_kwh_day: float = inp("Inputs!E50", "kWh/grid/day")
    meter_consumption_kwh_day: float = inp("Inputs!E51", "kWh/connection/day")
    distribution_losses: float = inp("Inputs!E52", "% consumption at meter")
    night_battery_share: float = inp("Inputs!E56", "% of daily PV output")
    battery_discharge_limit: float = inp("Inputs!E58", "%")
    inverter_sizing: float = inp("Inputs!E74", "inverter W / solar Wp")
    diesel_kwh_per_litre: float = inp("Inputs!E82", "kWh/litre", "40 kW generator")
    diesel_kwh_per_litre_10kw: float = inp("Inputs!E83", "kWh/litre", "Not used by any formula")
    diesel_litres_per_hour: float = inp("Inputs!E89", "litre/hour")
    diesel_threshold: float = inp("Inputs!E92", "%", "Gross consumption as % of gross production")
    diesel_share_below: float = inp("Inputs!E95", "%")
    diesel_share_above: float = inp("Inputs!E96", "%")
    max_diesel_share: float = inp("Inputs!E99", "%", "Capex expansion trigger")


@dataclass
class BuildAndRamp:
    build_profile: list = inp("Inputs!I135:N135", "share of grids per construction year")
    ramp_up: list = inp("Inputs!E149:E152", "% baseline revenue, operations years 1-4")
    ramp_discount: float = inp("Inputs!G149", "", "Discount applied to year-1 ramp-up")


@dataclass
class Demand:
    growth_base: float = inp("Inputs!I166", "%/year", "Escalation case growth")
    growth_sensitivity: float = inp("Inputs!G166", "%/year")
    tariff_sensitivity: float = inp("Inputs!G170", "%")
    consumption_case: int = inp("Inputs!E432", "1=Plateau, 2=Escalation, 3=Plateau + income growth")
    income_growth: float = inp("Inputs!E425", "%/year")


@dataclass
class Opex:
    ratchet_share: float = inp("Inputs!E174", "% of revenue above P50")
    fee_thresholds: list = inp("Inputs!I175:L175", "operations years")
    receivable_days: float = inp("Inputs!E182", "days")
    payable_days: float = inp("Inputs!E183", "days")


@dataclass
class Replacement:
    battery_life: float = inp("Inputs!E187", "years")
    inverter_life: float = inp("Inputs!E188", "years")
    stop_before_end: float = inp("Inputs!E189", "years")
    pv_cost_decline: float = inp("Inputs!E193", "%/year")
    battery_cost_decline: float = inp("Inputs!E199", "%/year")
    battery_forecast: str = inp("Inputs!E201", "", "'AssetCo Forecast' or 'BNEF New Energy Outlook…'")
    inverter_cost_decline: float = inp("Inputs!E206", "%/year")
    inverter_reference_year: int = inp("Inputs!E208", "year")


@dataclass
class Tax:
    corporate_rate: float = inp("Inputs!E215", "%")
    holiday_years: float = inp("Inputs!E217", "years")
    nol_years: float = inp("Inputs!E219", "years")
    vat_rate: float = inp("Inputs!E222", "%")
    vat_capex: str = inp("Inputs!E224", "Recoverable|Irrecoverable")
    vat_opex: str = inp("Inputs!E225", "Recoverable|Irrecoverable")
    vat_term_days: float = inp("Inputs!E227", "days")
    minimum_tax: float = inp("Inputs!E230", "% of revenue")
    dividend_wht: float = inp("Inputs!E233", "%")
    book_life_initial: float = inp("Inputs!E238", "years")
    tax_life_initial: float = inp("Inputs!E251", "years")
    tax_life_replacement: float = inp("Inputs!E255", "years")
    capital_allowance_limit: float = inp("Inputs!E262", "%")


@dataclass
class Funding:
    wacc: float = inp("Inputs!E266", "%")
    irr_period: float = inp("Inputs!E267", "years")
    grant_drawdown_rate: float = inp("Inputs!E272", "% of financing need", "Share of uses funded by grant (Model!E215)")
    developer_stake: float = inp("Inputs!E284", "%")
    owner_equity_provision: float = inp("Inputs!E287", "%")


@dataclass
class SeniorDebt:
    gearing: float = inp("Inputs!E296", "%")
    sizing_method: str = inp("Inputs!E302", "Gearing|DSCR")
    debt_switch: int = inp("Inputs!G304", "0|1")
    margin: float = inp("Inputs!I314", "% p.a.", "Margin over floating base rate")
    rate_choice: str = inp("Inputs!E316", "Fixed|Floating")
    arrangement_fee: float = inp("Inputs!E319", "% facility")
    commitment_fee_share: float = inp("Inputs!E320", "% margin", "Commission computed but never charged")
    repayment_start_ops_year: float = inp("Inputs!E324", "operations year")
    tenor_years: float = inp("Inputs!E325", "years")
    grace_years: float = inp("Inputs!E326", "years")
    target_dscr: float = inp("Inputs!E329", "x")
    drawdown: str = inp("Inputs!E332", "Equity first|Pari Passu")
    margin_by_period: Optional[list] = inp("Inputs!I314:L314", "% p.a.",
                                           "Optional override of the per-period margins (workbook: J:L copy I314)",
                                           default=None)
    fixed_rate_by_period: Optional[list] = inp("Inputs!I315:L315", "% p.a.",
                                               "Optional override of the per-period fixed rates (workbook: copies of Currency!F29)",
                                               default=None)


@dataclass
class Refinancing:
    tenor_year: float = inp("Inputs!E336", "year of senior tenor")
    on: int = inp("Inputs!G336", "0|1")
    gearing: float = inp("Inputs!E340", "%")
    sizing_rounding: float = inp("Inputs!L344", "digits")
    sizing_method: str = inp("Inputs!E346", "Gearing|DSCR")
    margin: float = inp("Inputs!I354", "% p.a.")
    rate_choice: str = inp("Inputs!E356", "Fixed|Floating")
    upfront_fee: float = inp("Inputs!E359", "% facility", "Not used by any formula")
    commitment_fee_share: float = inp("Inputs!E360", "% margin", "Commission computed but never charged")
    tenor_years: float = inp("Inputs!E364", "years")


@dataclass
class Reserves:
    dsra_on: int = inp("Inputs!E370", "0|1")
    dsra_months: float = inp("Inputs!E374", "months of debt service")
    dsra_deposit_rate: float = inp("Inputs!E377", "% p.a.")
    mmra_years: float = inp("Inputs!E385", "years of future battery capex")
    mmra_on: int = inp("Inputs!G385", "0|1")


@dataclass
class Macro:
    inflation: float = inp("Inputs!E391", "%/year")
    fx_case: int = inp("Inputs!E394", "1=Local, 2=USD to LCY")
    fx_depreciation: float = inp("Inputs!E403", "%/year", "LCY depreciation against USD")
    base_rate_years: list = inp("Inputs!I406:K406", "calendar year (last key is text '2023+')")
    base_rates: list = inp("Inputs!I407:K407", "% p.a.")


@dataclass
class GridArrivalExit:
    years_before_grid_arrival: float = inp("Inputs!E438", "years")
    exit_wacc: float = inp("Inputs!E446", "%")
    exit_lookforward_years: float = inp("Inputs!E447", "years")
    exit_ops_year: float = inp("Inputs!E448", "operations year")


@dataclass
class Constants:
    days_per_year: float = inp("Names!F12", "")
    months_per_year: float = inp("Names!F13", "")
    thousand: float = inp("Names!F17", "")


@dataclass
class PastedValues:
    """Values the VBA macros paste to break the model's circularities."""
    funding: float = inp("Inputs!G292", "currency", "Funding_paste")
    dscr_limit: float = inp("Inputs!G300", "currency", "DSCR_paste")
    refi_limit: float = inp("Inputs!G344", "currency", "Refi_Paste")
    dsra_initial: float = inp("Inputs!E372", "currency", "DSRA_Paste")


@dataclass
class Assumptions:
    timing: Timing
    currency: Currency
    lots: list[Lot]
    technical: Technical
    build: BuildAndRamp
    demand: Demand
    opex: Opex
    replacement: Replacement
    tax: Tax
    funding: Funding
    debt: SeniorDebt
    refi: Refinancing
    reserves: Reserves
    macro: Macro
    exit: GridArrivalExit
    constants: Constants
    pasted: PastedValues

    def replace(self, **changes) -> "Assumptions":
        """Copy with dotted-path changes, e.g. replace(**{"debt.sizing_method": "DSCR"})."""
        new = copy_assumptions(self)
        for path, value in changes.items():
            set_path(new, path, value)
        return new


def copy_assumptions(a: Assumptions) -> Assumptions:
    import copy
    return copy.deepcopy(a)


def set_path(obj: Any, path: str, value: Any) -> None:
    parts = path.split(".")
    for p in parts[:-1]:
        obj = obj[int(p)] if isinstance(obj, list) else getattr(obj, p)
    last = parts[-1]
    if isinstance(obj, list):
        obj[int(last)] = value
    elif isinstance(getattr(obj, last), MoneyInput) and not isinstance(value, MoneyInput):
        getattr(obj, last).value = value
    else:
        setattr(obj, last, value)


def to_dict(a: Assumptions) -> dict:
    def conv(x):
        if dataclasses.is_dataclass(x):
            return {f.name: conv(getattr(x, f.name)) for f in dataclasses.fields(x)}
        if isinstance(x, list):
            return [conv(v) for v in x]
        if isinstance(x, dt.date):
            return x.isoformat()
        return x
    return conv(a)


def from_dict(d: dict) -> Assumptions:
    def build(cls, data):
        kwargs = {}
        hints = {f.name: f for f in dataclasses.fields(cls)}
        for name, f in hints.items():
            if name not in data:
                continue
            v = data[name]
            t = f.type if isinstance(f.type, str) else getattr(f.type, "__name__", "")
            if t in ("MoneyInput",):
                v = MoneyInput(**v)
            elif t in ("dt.date",) and isinstance(v, str):
                v = dt.date.fromisoformat(v)
            kwargs[name] = v
        return cls(**kwargs)
    groups = {f.name: f.type for f in dataclasses.fields(Assumptions)}
    out = {}
    for name, t in groups.items():
        if name == "lots":
            out[name] = [Lot(**lot) for lot in d["lots"]]
        else:
            cls = globals()[t]
            out[name] = build(cls, d[name])
    return Assumptions(**out)


def field_cells(cls) -> dict[str, str]:
    return {f.name: f.metadata.get("cell", "") for f in dataclasses.fields(cls)}


def cell_paths() -> dict[str, str]:
    """Workbook input cell -> dotted assumption path (ranges expanded)."""
    from openpyxl.utils import column_index_from_string as ci, get_column_letter as cl

    out: dict[str, str] = {}
    for g in dataclasses.fields(Assumptions):
        if g.name == "lots":
            for i, col in enumerate(LOT_COLUMNS):
                for name, row in LOT_ROWS.items():
                    out[f"Portfolio!{col}{row}"] = f"lots.{i}.{name}"
            continue
        cls = globals()[g.type] if isinstance(g.type, str) else g.type
        for f in dataclasses.fields(cls):
            cell = f.metadata.get("cell", "")
            if not cell:
                continue
            sh, addr = cell.split("!")
            if ":" in addr:
                a1, a2 = addr.split(":")
                c1 = ci("".join(ch for ch in a1 if ch.isalpha()))
                c2 = ci("".join(ch for ch in a2 if ch.isalpha()))
                r1 = int("".join(ch for ch in a1 if ch.isdigit()))
                r2 = int("".join(ch for ch in a2 if ch.isdigit()))
                k = 0
                for r in range(r1, r2 + 1):
                    for c in range(c1, c2 + 1):
                        out[f"{sh}!{cl(c)}{r}"] = f"{g.name}.{f.name}.{k}"
                        k += 1
            else:
                out[cell] = f"{g.name}.{f.name}"
    return out


def apply_cells(a: "Assumptions", changes: dict[str, Any]) -> "Assumptions":
    """Copy of ``a`` with workbook-cell changes applied (e.g. {"Inputs!E302": "DSCR"})."""
    paths = cell_paths()
    unknown = [c for c in changes if c not in paths]
    if unknown:
        raise KeyError(f"not an input cell: {unknown}")
    return a.replace(**{paths[c]: v for c, v in changes.items()})
