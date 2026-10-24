"""Compare the engine with Excel benchmark dumps written by run_excel_benchmarks.py.

    cd minigrid-studio/backend
    .venv/bin/python ../tools/excel_benchmark/compare_with_engine.py OUT_DIR [--write-reference]

Scenarios come from tools/phase0/scenarios.json and feature_scenarios.json; those
without a dump in OUT_DIR are skipped. Exit code 0 when every dumped scenario matches
cell by cell (max(1e-9 relative, 1e-6 absolute), as reconcile.close). With
--write-reference the per-scenario output summaries are written to
reference_values/excel/<id>_excel.json (genuine Excel benchmark values).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.engine import reconcile as R  # noqa: E402
from app.engine.assumptions import apply_cells, from_dict  # noqa: E402
from app.engine.solver import solve  # noqa: E402


def main() -> int:
    out = Path(sys.argv[1])
    write = "--write-reference" in sys.argv
    base = from_dict(json.loads((ROOT / "reference_values" / "S1_base_inputs.json").read_text()))
    scenarios = [sc for f in ("scenarios.json", "feature_scenarios.json")
                 for sc in json.loads((ROOT / "tools" / "phase0" / f).read_text())["scenarios"]]
    spec = json.loads((ROOT / "tools" / "phase0" / "outputs_spec.json").read_text())
    failures = 0
    for sc in scenarios:
        cells_path = out / f"{sc['id']}_excel_cells.json"
        if not cells_path.exists():
            print(sc["id"], "no Excel dump, skipped")
            continue
        meta = json.loads((out / f"{sc['id']}_excel_meta.json").read_text())
        solved, L, log = solve(apply_cells(base, sc["set"]))
        rep = R.reconcile(L, R.json_values(str(cells_path)))
        pasted_engine = {"G292": solved.pasted.funding, "G300": solved.pasted.dscr_limit,
                         "G344": solved.pasted.refi_limit, "E372": solved.pasted.dsra_initial}
        pasted_ok = all(R.close(meta["pasted_values"][k] or 0, v) for k, v in pasted_engine.items())
        status = "MATCH" if rep.ok and pasted_ok and meta["converged"] else "DIFF"
        failures += status != "MATCH"
        print(f"{sc['id']}: {status} | Excel {meta['excel_version']} converged={meta['converged']} "
              f"| pasted values equal={pasted_ok}")
        print("   " + rep.summary(15).replace("\n", "\n   "))
        if write and status == "MATCH":
            value_of = R.json_values(str(cells_path))
            dest = ROOT / "reference_values" / "excel"
            dest.mkdir(exist_ok=True)
            from openpyxl.utils import column_index_from_string as ci
            def get(ref):
                sh, addr = ref.split("!")
                col = "".join(c for c in addr if c.isalpha())
                row = int("".join(c for c in addr if c.isdigit()))
                return value_of(sh, row, ci(col))
            summary = {"scenario": sc["id"], "engine": f"Microsoft Excel {meta['excel_version']}",
                       "source_sha256": meta["workbook_sha256"], "inputs_changed": sc["set"],
                       "scalars": {k: get(ref) for k, (ref, _l, _u) in spec["scalars"].items()},
                       "pasted_values": {k: get(ref) for k, ref in spec["pasted_values"].items()},
                       "series": {k: [value_of(sh, row, 10 + t) for t in range(69)]
                                  for k, (sh, row, _l) in spec["series"].items()},
                       "excel_run": meta}
            (dest / f"{sc['id']}_excel.json").write_text(json.dumps(summary, indent=1, default=str))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
