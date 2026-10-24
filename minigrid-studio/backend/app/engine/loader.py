"""Load an :class:`Assumptions` set from the reference workbook (read-only,
formulas are not evaluated and macros are never run)."""
from __future__ import annotations

import dataclasses
import datetime as dt
from pathlib import Path

import openpyxl

from . import assumptions as A

CURRENCY_ROWS = {  # field -> Currency sheet row
    "mmra_starting_balance": 28, "all_in_cost_of_debt": 29, "capex_net_of_grant": 33,
    "grant_per_connection": 34, "battery_cost": 35, "transfer_fee": 36, "fixed_fee_per_grid": 39,
    "diesel_price": 40, "pv_price": 44, "battery_racking": 45, "battery_installation": 46,
    "battery_replacement_2023": 47, "inverter_price_2020": 48, "expansion_racking": 49,
    "expansion_logistics": 50, "bnef_battery_2030": 51, "inverter_2030": 52, "fee_per_customer": 55,
    "admin_costs": 56, "tariff": 59, "grid_arrival_tariff": 60, "amt_threshold": 63, "sizing_rounding": 64,
}


def _is_formula(v) -> bool:
    return isinstance(v, str) and v.startswith("=")


class WorkbookReader:
    def __init__(self, path: str | Path):
        self.wb = openpyxl.load_workbook(path)

    def get(self, ref: str):
        sh, addr = ref.split("!")
        v = self.wb[sh][addr].value
        if _is_formula(v):
            raise ValueError(f"{ref} holds a formula ({v}), not an input")
        if isinstance(v, dt.datetime):
            return v.date()
        return v

    def row_values(self, ref: str) -> list:
        sh, rng = ref.split("!")
        cells = self.wb[sh][rng]
        return [c.value for row in cells for c in row]

    def money(self, row: int) -> A.MoneyInput:
        ws = self.wb["Currency"]
        h, i, k, g = (ws.cell(row, c).value for c in (8, 9, 11, 7))
        vat = "none"
        if _is_formula(g):
            g = g.replace("$", "")
            vat = "capex" if "E224" in g else "opex" if "E225" in g else "none"
        if k is not None and not _is_formula(k):
            return A.MoneyInput(value=float(k), basis="lcy_contracted", vat=vat)
        if not _is_formula(h) and i is not None and not _is_formula(i):
            return A.MoneyInput(value=float(h), basis="usd_and_lcy", vat=vat, lcy_value=float(i))
        return A.MoneyInput(value=float(h), basis="usd", vat=vat)


def _fill(cls, reader: WorkbookReader, skip=()):
    kwargs = {}
    for f in dataclasses.fields(cls):
        if f.name in skip:
            continue
        cell = f.metadata["cell"]
        if f.default is None:  # optional overrides: the workbook holds formulas there
            continue
        if ":" in cell:
            vals = reader.row_values(cell)
            if any(_is_formula(v) for v in vals):
                raise ValueError(f"{cell} contains formulas")
            kwargs[f.name] = vals
        else:
            kwargs[f.name] = reader.get(cell)
    return kwargs


def load_assumptions(path: str | Path) -> A.Assumptions:
    r = WorkbookReader(path)
    currency_kwargs = _fill(A.Currency, r, skip=set(CURRENCY_ROWS))
    currency_kwargs.update({name: r.money(row) for name, row in CURRENCY_ROWS.items()})

    lots = []
    ws = r.wb["Portfolio"]
    for col in A.LOT_COLUMNS:
        kw = {}
        for name, row in A.LOT_ROWS.items():
            v = ws[f"{col}{row}"].value
            kw[name] = None if _is_formula(v) else v
        lots.append(A.Lot(**kw))

    groups = {}
    for f in dataclasses.fields(A.Assumptions):
        if f.name in ("currency", "lots"):
            continue
        cls = getattr(A, f.type) if isinstance(f.type, str) else f.type
        groups[f.name] = cls(**_fill(cls, r))
    return A.Assumptions(currency=A.Currency(**currency_kwargs), lots=lots, **groups)
