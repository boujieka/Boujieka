"""Produce the Excel benchmark values of the reference scenarios with Microsoft Excel.

Run on a Windows or macOS machine with desktop Excel and Python 3.10+:

    pip install xlwings==0.33.3
    python run_excel_benchmarks.py PATH/TO/CrossBoundary-Access-Open-Source-Model-1.0-October-2023.xlsm \
           ../phase0/scenarios.json OUT_DIR

For each scenario the script
  1. copies the workbook (the original is never modified) and checks its SHA-256;
  2. opens the copy in a hidden Excel instance with automatic calculation;
  3. writes the scenario's input cells;
  4. runs the workbook's own audited macros (Module1.Debt_Sizing, Module2.Refi_Debt_Sizing
     when the refinancing switch is on, Module7.DSRA_resize_3), repeating until the sizing
     checks Inputs!N292, N300, N344 and E373 are 0 (at most 25 rounds), as the Key sheet asks;
  5. saves the calculated copy as .xlsx and writes OUT_DIR/<id>_excel_cells.json
     ("Sheet!row,col" -> value, same format as the LibreOffice dumps) and <id>_excel_meta.json.

Macros: Excel only runs them if the copy is trusted. Either add OUT_DIR to the Trust Center's
trusted locations for the duration of the run, or allow macros when prompted. The macros were
audited in docs/audit.md (4 copy/paste-value procedures, no file, network or shell access).
The VBA loops have no iteration limit: if a macro does not return within a few minutes,
stop Excel and record the scenario as non-convergent.

Then compare with the engine (on any machine with the backend installed):

    cd minigrid-studio/backend
    .venv/bin/python ../tools/excel_benchmark/compare_with_engine.py OUT_DIR
"""
import datetime as dt
import hashlib
import json
import platform
import shutil
import sys
import time
from pathlib import Path

EXPECTED_SHA256 = "fe0ecb160b294120e3135dfce6bacf619246bff1ed85944e06b6c44c0c4bb33e"
SIZING_CHECKS = ["N292", "N300", "N344", "E373"]
MAX_ROUNDS = 25
EPOCH = dt.datetime(1899, 12, 30)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def to_json_value(v):
    if isinstance(v, dt.datetime):
        return (v - EPOCH).total_seconds() / 86400
    if isinstance(v, dt.date):
        return (dt.datetime(v.year, v.month, v.day) - EPOCH).days
    if isinstance(v, bool):
        return v
    if v is None:
        return ""
    return v


def dump_cells(book) -> dict:
    out = {}
    for sh in book.sheets:
        rng = sh.used_range
        r0, c0 = rng.row, rng.column
        formulas = rng.formula
        values = rng.options(ndim=2).value
        if not isinstance(formulas, (list, tuple)):
            formulas = [[formulas]]
        elif formulas and not isinstance(formulas[0], (list, tuple)):
            formulas = [formulas]
        for i, row in enumerate(formulas):
            for j, f in enumerate(row):
                if isinstance(f, str) and f.startswith("="):
                    out[f"{sh.name}!{r0 + i},{c0 + j}"] = to_json_value(values[i][j])
    return out


def sizing_ok(inputs) -> bool:
    return all((inputs.range(c).value or 0) == 0 for c in SIZING_CHECKS)


def run_scenario(app, src: Path, out_dir: Path, sc: dict) -> dict:
    work = out_dir / f"{sc['id']}_work.xlsm"
    shutil.copyfile(src, work)
    t0 = time.time()
    book = app.books.open(str(work))
    log = {"scenario": sc["id"], "inputs_changed": sc.get("set", {}), "rounds": 0, "steps": []}
    try:
        app.calculation = "automatic"
        for ref, value in sc.get("set", {}).items():
            sheet, addr = ref.split("!")
            book.sheets[sheet].range(addr).value = value
        app.calculate()
        inputs = book.sheets["Inputs"]
        for rnd in range(1, MAX_ROUNDS + 1):
            if sizing_ok(inputs):
                break
            book.macro("Debt_Sizing")()
            log["steps"].append("Debt_Sizing")
            if (inputs.range("G336").value or 0) == 1:
                book.macro("Refi_Debt_Sizing")()
                log["steps"].append("Refi_Debt_Sizing")
            book.macro("DSRA_resize_3")()
            log["steps"].append("DSRA_resize_3")
            log["rounds"] = rnd
        log["converged"] = sizing_ok(inputs)
        log["pasted_values"] = {k: inputs.range(k).value for k in ("G292", "G300", "G344", "E372")}
        log["dashboard_global_check"] = book.sheets["Dashboard"].range("K55").value
        cells = dump_cells(book)
        (out_dir / f"{sc['id']}_excel_cells.json").write_text(json.dumps(cells))
        book.save(str(out_dir / f"{sc['id']}_excel.xlsx"))
    finally:
        book.close()
    work.unlink(missing_ok=True)
    log["seconds"] = round(time.time() - t0, 1)
    return log


def main() -> int:
    import xlwings as xw

    src, scenarios_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    digest = sha256(src)
    if digest != EXPECTED_SHA256:
        print(f"warning: workbook SHA-256 {digest} differs from the audited file {EXPECTED_SHA256}")
    scenarios = json.loads(scenarios_path.read_text())["scenarios"]
    app = xw.App(visible=False, add_book=False)
    app.display_alerts = False
    meta_common = {"excel_version": app.version, "platform": platform.platform(), "python": platform.python_version(),
                   "workbook_sha256": digest, "run_at": dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        for sc in scenarios:
            log = run_scenario(app, src, out, sc)
            log.update(meta_common)
            (out / f"{sc['id']}_excel_meta.json").write_text(json.dumps(log, indent=1, default=str))
            print(sc["id"], "converged" if log["converged"] else "NOT converged", f"rounds={log['rounds']}",
                  f"{log['seconds']}s")
    finally:
        app.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
