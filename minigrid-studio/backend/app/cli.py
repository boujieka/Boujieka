"""Run the engine without the API or a database.

    python -m app.cli --template demo_fictitious
    python -m app.cli --assumptions my.json --set Inputs!E302=DSCR --option cap_principal_at_balance
    python -m app.cli --xlsm workbook.xlsm --reconcile      # cell-by-cell check against its cached values
"""
import argparse
import json
import sys

from .engine.assumptions import apply_cells, from_dict
from .engine.options import EngineOptions
from .engine.results import run_scenario
from .services.scenarios import load_template


def _value(s: str):
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return s


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--template")
    src.add_argument("--assumptions")
    src.add_argument("--xlsm")
    ap.add_argument("--set", action="append", default=[], help="CELL=VALUE, e.g. Inputs!E302=DSCR")
    ap.add_argument("--option", action="append", default=[])
    ap.add_argument("--method", default="excel_macros", choices=["excel_macros", "exact"])
    ap.add_argument("--per-lot", action="store_true")
    ap.add_argument("--reconcile", action="store_true", help="with --xlsm: compare every cell to Excel")
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = ap.parse_args(argv)

    if args.xlsm:
        from .engine.loader import load_assumptions
        a = load_assumptions(args.xlsm)
        if args.reconcile:
            from .engine import reconcile as R
            from .engine.model import run_model
            from .engine.prepare import prepare
            p = prepare(a)
            rep = R.reconcile(run_model(a, p), R.workbook_values(args.xlsm))
            tab = R.reconcile_tables(p.tables, R.workbook_values(args.xlsm))
            print(rep.summary())
            print("tables:", tab.summary())
            return 0 if rep.ok and tab.ok else 1
    elif args.template:
        a = from_dict(load_template(args.template))
    else:
        d = json.load(open(args.assumptions))
        d.pop("_comment", None)
        a = from_dict(d)
    if args.set:
        a = apply_cells(a, {k: _value(v) for k, v in (s.split("=", 1) for s in args.set)})
    res = run_scenario(a, args.method, EngineOptions(**{o: True for o in args.option}), per_lot=args.per_lot)
    if args.json:
        json.dump(res.as_dict(), sys.stdout, indent=1, default=str)
        return 0
    print(f"status: {res.status}  solver: {res.solver['method']} rounds={res.solver['rounds']}")
    for k, i in res.kpis.items():
        tag = " [derived]" if i.derived else ""
        tag += " [experimental]" if i.experimental else ""
        val = "n/a" if i.value is None else (f"{i.value:.4%}" if i.unit == "%" else f"{i.value:,.2f}")
        print(f"  {i.label:<60} {val:>18}  ({i.source}){tag}")
    if res.failed_checks:
        print("checks not passed:", ", ".join(res.failed_checks))
    for w in res.warnings:
        print("warning:", w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
