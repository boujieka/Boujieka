"""
Full-engine snapshot runner for BANKABLE HYDRO.

Re-runs the complete Excel model (via LibreOffice headless) for every scenario,
financing structure and sensitivity, then writes the results as a dated, static
snapshot table into 27_SCENARIOS, 17A_STRUCTURES and 28_SENSITIVITY.
Live formulas are untouched. Re-run after changing inputs:

    python tools/run_snapshots.py [model.xlsx]

Requires LibreOffice (with Calc) and openpyxl. Uses the xlsx-skill recalc script
if available, otherwise LibreOffice directly via RECALC env var path.
"""
import json, os, re, shutil, subprocess, sys, tempfile, datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

MODEL = sys.argv[1] if len(sys.argv) > 1 else "model/Bankable_Hydro_Model.xlsx"
MAP = json.load(open("model/model_map.json"))
REF = MAP["REF"]
RECALC = os.environ.get("RECALC", "/root/.claude/skills/synced/595554f7-3334-4cb8-90b6-40da4dcb6b84_e238fe12-8a4b-4490-8c46-5bf1323948af/xlsx/scripts/recalc.py")


def addr(name):
    m = re.fullmatch(r"'([^']+)'!\$([A-Z]+)\$(\d+)", REF[name])
    return m.group(1), f"{m.group(2)}{m.group(3)}"


KPIS = [("kpi_pirr", "Project IRR", "0.0%"), ("kpi_eirr", "Equity IRR", "0.0%"), ("kpi_min_dscr", "Min DSCR", '0.00"x"'),
        ("kpi_llcr", "LLCR", '0.00"x"'), ("fin_gap", "Financing gap USDm", "#,##0"), ("lcoe", "LCOE USD/MWh", "0.0"),
        ("ut_ratio10", "Utility pay capacity (min yr1-10)", '0.00"x"'), ("rev_govreq", "Utility PPA gap USDm (life)", "#,##0"),
        ("kpi_short", "DS shortfall USDm", "#,##0"), ("fis_npv", "Fiscal NPV USDm", "#,##0;(#,##0)"),
        ("cl_peak", "Peak contingent USDm", "#,##0"), ("fis_peak_rev", "Peak cash need % rev", "0.00%"),
        ("bk_overall", "Bankability verdict", "@"), ("sc_result", "Fiscal screen", "@")]


EXTRA = [(k, "", "") for k in ["debt_m", "debt_c", "uses", "fund_base", "lcoe_sys", "kpi_avg_dscr", "kpi_npv", "cod_year", "sc_flags",
         "fis_peak", "cl_pv_el", "sc_cl", "sc_cash", "tx_gap_yrs", "evac_cod", "dem_ratio5", "rev_fixed", "kpi_plcr", "kpi_girr"]
        + [f"G{i}_status" for i in range(1, 10)] + [f"G{i}_score" for i in range(1, 10)]]
TS_SAVE = ["year", "opyr", "gen", "delivered", "gen_p50", "u_ppa", "u_maxppa", "u_gap", "f_net", "f_cum", "cl_max", "cfads", "ds",
           "dscr", "x_debt", "x_ppa", "x_term", "rev_bill", "rev_cash", "g_direct", "call_tot", "debt_bal"]


def run(settings):
    tmpd = tempfile.mkdtemp()
    f = os.path.join(tmpd, "m.xlsx")
    shutil.copy(MODEL, f)
    wb = load_workbook(f)
    for k, v in settings.items():
        s, c = addr(k)
        wb[s][c].value = v
    wb.save(f)
    out = subprocess.run([sys.executable, RECALC, f, "300"], capture_output=True, text=True)
    res = json.loads(out.stdout)
    if res.get("status") != "success":
        raise RuntimeError(f"recalc failed for {settings}: {res}")
    wv = load_workbook(f, data_only=True)
    vals = {}
    for k, *_ in KPIS + EXTRA:
        s, c = addr(k)
        vals[k] = wv[s][c].value
    vals["ts"] = {}
    for nm in TS_SAVE:
        s, r = MAP["TSROW"][nm]
        vals["ts"][nm] = [wv[s].cell(r, 5 + j).value for j in range(40)]
    shutil.rmtree(tmpd)
    return vals


OFF = {k: 0 for k in ["st_drought", "st_capex", "st_delay", "st_demand", "st_offtaker", "st_fx", "st_rate", "st_trans", "st_climate"]}
BASE = dict(OFF, case=1, gen_case=1, structure=3, debt_mode=1, backstop=1, fx_capex=0, fx_gen=0, fx_tariff=0, fx_opex=0, fx_rate=0)

print("Base (debt sized in-model)...")
base = run(BASE)
LOCK = dict(BASE, debt_mode=2, lock_m=round(base["debt_m"], 3))

SCEN = [("Base — debt sized in-model", BASE), ("Base — debt locked", LOCK),
        ("Low case", dict(LOCK, case=2)), ("High case", dict(LOCK, case=3)),
        ("Drought", dict(LOCK, st_drought=1)), ("CAPEX overrun", dict(LOCK, st_capex=1)),
        ("Construction delay", dict(LOCK, st_delay=1)), ("Low demand", dict(LOCK, st_demand=1)),
        ("Offtaker stress", dict(LOCK, st_offtaker=1)), ("Offtaker stress, no budget backstop (PPA guarantee called)", dict(LOCK, st_offtaker=1, backstop=0)),
        ("FX step devaluation at COD", dict(LOCK, st_fx=1)), ("High interest rate", dict(LOCK, st_rate=1)),
        ("Transmission delay", dict(LOCK, st_trans=1)), ("Climate trend", dict(LOCK, st_climate=1)),
        ("Combined: overrun + delay + offtaker + FX", dict(LOCK, st_capex=1, st_delay=1, st_offtaker=1, st_fx=1))]
STRS = [(f"Structure {i}", dict(BASE, structure=i)) for i in range(1, 6)]
SENS = [("CAPEX -20%", dict(LOCK, fx_capex=-0.2)), ("CAPEX +20%", dict(LOCK, fx_capex=0.2)),
        ("Generation -10%", dict(LOCK, fx_gen=-0.1)), ("Generation +10%", dict(LOCK, fx_gen=0.1)),
        ("Tariff -10%", dict(LOCK, fx_tariff=-0.1)), ("Tariff +10%", dict(LOCK, fx_tariff=0.1)),
        ("OPEX +20%", dict(LOCK, fx_opex=0.2)), ("Commercial rate +200bp", dict(LOCK, fx_rate=0.02)),
        ("P90 generation in cash flows", dict(LOCK, gen_case=3))]

results = {}
for grp in (SCEN, STRS, SENS):
    for lab, st in grp:
        print("running", lab)
        results[lab] = base if st is BASE else run(st)

wb = load_workbook(MODEL)
stamp = datetime.date.today().isoformat()
HF = Font(name="Arial", size=10, bold=True, color="FFFFFF"); HB = PatternFill("solid", fgColor="2F5597")
BF = Font(name="Arial", size=10)


def table(ws, r0, title, rows):
    ws.cell(r0, 1, f"{title} — FULL-ENGINE SNAPSHOT (static values, generated {stamp} by tools/run_snapshots.py; stresses run with commercial debt LOCKED at base amount, annuity profile)").font = Font(name="Arial", size=10, bold=True, color="1F3864")
    hdr = ["Run"] + [k[1] for k in KPIS]
    for j, h in enumerate(hdr):
        c = ws.cell(r0 + 1, 1 + j, h); c.font = HF; c.fill = HB
    for i, lab in enumerate(rows):
        ws.cell(r0 + 2 + i, 1, lab).font = BF
        for j, (k, _, fmt) in enumerate(KPIS):
            c = ws.cell(r0 + 2 + i, 2 + j, results[lab][k]); c.font = BF; c.number_format = fmt


table(wb["27_SCENARIOS"], MAP["SCEN_SNAP_ROW"], "SCENARIOS", [l for l, _ in SCEN])
table(wb["17A_STRUCTURES"], MAP["CMP_SNAP"], "STRUCTURES (base case, debt sized in-model)", [l for l, _ in STRS])
table(wb["28_SENSITIVITY"], MAP["SENS_SNAP_ROW"], "SENSITIVITIES", ["Base — debt locked"] + [l for l, _ in SENS])
wb.save(MODEL)
subprocess.run([sys.executable, RECALC, MODEL, "300"], check=True)
SLUG = {"Base — debt sized in-model": "base_sized", "Base — debt locked": "base_locked", "Low case": "low", "High case": "high",
        "Drought": "drought", "CAPEX overrun": "overrun", "Construction delay": "delay", "Low demand": "lowdem",
        "Offtaker stress": "offtaker", "Offtaker stress, no budget backstop (PPA guarantee called)": "offtaker_nobs",
        "FX step devaluation at COD": "fx", "High interest rate": "rate", "Transmission delay": "trans", "Climate trend": "climate",
        "Combined: overrun + delay + offtaker + FX": "combined", "Structure 1": "s1", "Structure 2": "s2", "Structure 3": "s3",
        "Structure 4": "s4", "Structure 5": "s5", "CAPEX -20%": "capex_m20", "CAPEX +20%": "capex_p20", "Generation -10%": "gen_m10",
        "Generation +10%": "gen_p10", "Tariff -10%": "tar_m10", "Tariff +10%": "tar_p10", "OPEX +20%": "opex_p20",
        "Commercial rate +200bp": "rate_p200", "P90 generation in cash flows": "p90cf"}
out = {SLUG.get(k, k): dict(v, label=k) for k, v in results.items()}
json.dump(out, open("model/snapshot_results.json", "w"), indent=1, default=str)
print("done")
