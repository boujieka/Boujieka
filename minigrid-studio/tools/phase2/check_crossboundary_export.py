"""Check the CrossBoundary-format export end to end.

For the fictitious demo and the reference scenarios S2-S5: fill the source
workbook with the scenario and the engine's pasted values (app.exports.crossboundary),
recalculate the filled copy in headless LibreOffice WITHOUT replaying the macros,
and compare every formula cell with the engine.

    cd minigrid-studio/backend
    .venv/bin/python ../tools/phase2/check_crossboundary_export.py ../reference/<model>.xlsm ../work/cbfill

Needs LibreOffice and its Python UNO bridge (system python3), like tools/phase0.
Known LibreOffice quirks are excluded as in tests/test_reconcile_workbook.py.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.engine import reconcile as R  # noqa: E402
from app.engine.assumptions import apply_cells, from_dict  # noqa: E402
from app.engine.solver import solve  # noqa: E402
from app.exports.crossboundary import fill_template  # noqa: E402
from app.services.scenarios import load_template  # noqa: E402

LO_SKIP = {"Model!372", "Model!429", "Inputs!J364", "Inputs!L364", "Debt!F68"}
SIZING = ("check_funding_optimised", "check_senior_sized", "check_refi_sized", "check_dsra_funded")


def main() -> int:
    template, out = Path(sys.argv[1]).read_bytes(), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    base = from_dict(load_template("crossboundary_reference"))
    cases = {"demo_fictitious": from_dict(load_template("demo_fictitious"))}
    for sc in json.loads((ROOT / "tools/phase0/scenarios.json").read_text())["scenarios"][1:]:
        cases[sc["id"]] = apply_cells(base, sc["set"])
    failures = 0
    for name, a in cases.items():
        solved, L, _ = solve(a)
        p = solved.pasted
        (out / f"{name}.xlsm").write_bytes(fill_template(template, a, {
            "funding": p.funding, "dscr_limit": p.dscr_limit, "refi_limit": p.refi_limit,
            "dsra_initial": p.dsra_initial}))
        (out / f"{name}.json").write_text(json.dumps({"scenarios": [{"id": name, "set": {}, "replay_macros": False}]}))
        subprocess.run(["python3", str(ROOT / "tools/phase0/lo_scenarios.py"), str(out / f"{name}.xlsm"),
                        str(out / f"{name}.json"), str(out / "lo"), "--dump-cells"], check=True,
                       stdout=subprocess.DEVNULL)
        rep = R.reconcile(L, R.json_values(str(out / "lo" / f"{name}_cells.json")), skip_rows=LO_SKIP)
        mism = [m for m in rep.mismatches if m.key not in LO_SKIP]
        lo = json.loads((out / "lo" / f"{name}_libreoffice.json").read_text())["scalars"]
        sizing_ok = all(lo.get(c) == 0 for c in SIZING)
        ok = not mism and sizing_ok
        failures += not ok
        print(f"{name}: {'MATCH' if ok else 'DIFF'} | {rep.compared} cells compared, {len(mism)} mismatches | "
              f"sizing checks at 0: {sizing_ok}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
