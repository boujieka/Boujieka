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
RECALC = os.environ.get("RECALC", "recalc.py")  # path to a LibreOffice recalculation script


def addr(name):
    m = re.fullmatch(r"'([^']+)'!\$([A-Z]+)\$(\d+)", REF[name])
    return m.group(1), f"{m.group(2)}{m.group(3)}"


KPIS = [("kpi_pirr", "Project IRR", "0.0%"), ("kpi_eirr", "Equity IRR", "0.0%"), ("kpi_min_dscr", "Min DSCR", '0.00"x"'),
        ("kpi_llcr", "LLCR", '0.00"x"'), ("fin_gap", "Financing gap USDm", "#,##0"), ("lcoe", "LCOE USD/MWh", "0.0"),
        ("ut_ratio10", "Utility pay capacity (min yr1-10)", '0.00"x"'), ("rev_govreq", "Utility PPA gap USDm (life)", "#,##0"),
        ("kpi_short", "DS shortfall USDm", "#,##0"), ("fis_npv", "Fiscal NPV USDm", "#,##0;(#,##0)"),
        ("cl_peak", "Peak contingent USDm", "#,##0"), ("fis_peak_rev", "Peak cash need % rev", "0.00%"),
        ("fis_npv_cons", "Consolidated fiscal NPV USDm", "#,##0;(#,##0)"),
        ("dev_irr", "Developer IRR (success path)", "0.0%"), ("dev_enpv", "Risk-weighted developer NPV USDm", "0.00"),
        ("fc_decision", "Financial close decision", "@"),
        ("bk_overall", "Bankability verdict", "@"), ("sc_result", "Fiscal screen", "@")]


EXTRA = [(k, "", "") for k in ["sv1", "sv3", "sv6", "dev_be_p", "dev_mult", "dev_peak", "dev_npv_success", "dev_be_prem_pct", "dev_pfc", "val_step_fc", "val_step_cod", "sell_proceeds", "fc_met", "capex_kw", "capex_real", "p50", "p90", "p90_10", "cf", "lcoe", "s_grant", "s_goveq", "gearing", "u_idc", "debt_m", "debt_c", "uses", "fund_base", "lcoe_sys", "kpi_avg_dscr", "kpi_npv", "cod_year", "sc_flags",
         "fis_peak", "cl_pv_el", "sc_cl", "sc_cash", "tx_gap_yrs", "evac_cod", "dem_ratio5", "rev_fixed", "kpi_plcr", "kpi_girr"]
        + [f"G{i}_status" for i in range(1, 10)] + [f"G{i}_score" for i in range(1, 10)]]
TS_SAVE = ["m_prin", "m_target", "f_net_cons", "f_soe", "u_unserved", "year", "opyr", "gen", "delivered", "gen_p50", "u_ppa", "u_maxppa", "u_gap", "f_net", "f_cum", "cl_max", "cfads", "ds",
           "dscr", "x_debt", "x_ppa", "x_term", "rev_bill", "rev_cash", "g_direct", "call_tot", "debt_bal"]


def run(settings):
    tmpd = tempfile.mkdtemp()
    f = os.path.join(tmpd, "m.xlsx")
    shutil.copy(MODEL, f)
    wb = load_workbook(f)
    for k, v in settings.items():
        if k == "lock_ds":
            s, r = MAP["TSROW"]["lock_ds"]
            for j, x in enumerate(v):
                wb[s].cell(r, 5 + j).value = x
            continue
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
BASE = dict(OFF, case=1, gen_case=1, structure=2, debt_mode=1, backstop=1, fx_capex=0, fx_gen=0, fx_tariff=0, fx_opex=0, fx_rate=0, epc_struct=2)

print("Base (debt sized in-model)...")
base = run(BASE)
lock_ds = [0.0] * 40
for j, k in enumerate(base["ts"]["opyr"]):
    if k and k >= 1:
        lock_ds[k - 1] = base["ts"]["m_prin"][j] or 0.0
LOCK = dict(BASE, debt_mode=2, lock_m=base["debt_m"], lock_c=base["debt_c"], lock_grant=base["s_grant"], lock_goveq=base["s_goveq"], lock_ds=lock_ds)

SCEN = [("Base — debt sized in-model", BASE), ("Base — debt locked", LOCK),
        ("Low case", dict(LOCK, case=2)), ("High case", dict(LOCK, case=3)),
        ("Drought", dict(LOCK, st_drought=1)), ("CAPEX overrun", dict(LOCK, st_capex=1)), ("CAPEX overrun, reference-class mean (+96%)", dict(LOCK, st_capex=1, p_overrun=0.96)),
        ("Construction delay", dict(LOCK, st_delay=1)), ("Low demand", dict(LOCK, st_demand=1)),
        ("Offtaker stress", dict(LOCK, st_offtaker=1)), ("Offtaker stress, no budget backstop (PPA guarantee called)", dict(LOCK, st_offtaker=1, backstop=0)),
        ("FX step devaluation at COD", dict(LOCK, st_fx=1)), ("High interest rate", dict(LOCK, st_rate=1)),
        ("Transmission delay", dict(LOCK, st_trans=1)), ("Climate trend", dict(LOCK, st_climate=1)),
        ("Combined: overrun + delay + offtaker + FX", dict(LOCK, st_capex=1, st_delay=1, st_offtaker=1, st_fx=1))]
STRS = [(f"Structure {i}", dict(BASE, structure=i)) for i in range(1, 6)]
DEVS = [("Dev: discount rate 18%", dict(BASE, dev_rate=0.18)), ("Dev: premium 6%", dict(BASE, dev_prem_pct=0.06)),
        ("Dev: stage odds +10pp", dict(BASE, dev_p1=0.7, dev_p2=0.7, dev_p3=0.8, dev_p4=0.95, dev_p5=0.9, dev_p6=0.95)),
        ("Dev: grant funds half of feasibility", dict(BASE, dev_c3=2.25)),
        ("Dev: tariff +10%", dict(BASE, fx_tariff=0.10)),
        ("Dev: all four levers", dict(BASE, dev_rate=0.18, dev_prem_pct=0.06, dev_p1=0.7, dev_p2=0.7, dev_p3=0.8, dev_p4=0.95, dev_p5=0.9, dev_p6=0.95, dev_c3=2.25))]
EPCS = [(f"EPC {k} base", dict(BASE, epc_struct=k)) for k in (1, 2, 3)] + [(f"EPC {k} overrun 96%", dict(BASE, epc_struct=k, st_capex=1, p_overrun=0.96)) for k in (1, 2, 3)]
SENS = [("CAPEX -20%", dict(LOCK, fx_capex=-0.2)), ("CAPEX +20%", dict(LOCK, fx_capex=0.2)),
        ("Generation -10%", dict(LOCK, fx_gen=-0.1)), ("Generation +10%", dict(LOCK, fx_gen=0.1)),
        ("Tariff -10%", dict(LOCK, fx_tariff=-0.1)), ("Tariff +10%", dict(LOCK, fx_tariff=0.1)),
        ("OPEX +20%", dict(LOCK, fx_opex=0.2)), ("Commercial rate +200bp", dict(LOCK, fx_rate=0.02)),
        ("P90 generation in cash flows", dict(LOCK, gen_case=3))]

def req_tariff(i):
    hurdle = [0.10, 0.15, 0.14, 0.14, 0.13][i - 1]
    lo, hi = -0.4, 0.8
    for _ in range(9):
        mid = (lo + hi) / 2
        v = run(dict(BASE, structure=i, fx_tariff=mid))["kpi_eirr"]
        v = v if isinstance(v, (int, float)) else -1
        if v < hurdle:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


results = {}
LENS = [("Lender case: P90 one-year", dict(BASE, lender_case=3))]
for grp in (SCEN, STRS, SENS, EPCS, DEVS, LENS):
    for lab, st in grp:
        print("running", lab)
        results[lab] = base if st is BASE else run(st)

REQ = {}
for i in range(2, 6):
    print("required tariff, structure", i)
    REQ[f"s{i}"] = req_tariff(i)


def breakeven_flow():
    lo, hi = -0.6, 0.0
    for _ in range(9):
        mid = (lo + hi) / 2
        v = run(dict(LOCK, fx_gen=mid))["kpi_min_dscr"]
        if v < 1.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


print("break-even flow")
BE_FLOW = breakeven_flow()
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
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "model", "excel_quote_fix.py"), MODEL], check=True)  # Excel needs quoted digit-leading sheet names
SLUG = {"Base — debt sized in-model": "base_sized", "Base — debt locked": "base_locked", "Low case": "low", "High case": "high",
        "Drought": "drought", "CAPEX overrun": "overrun", "CAPEX overrun, reference-class mean (+96%)": "overrun96", "Construction delay": "delay", "Low demand": "lowdem",
        "Offtaker stress": "offtaker", "Offtaker stress, no budget backstop (PPA guarantee called)": "offtaker_nobs",
        "FX step devaluation at COD": "fx", "High interest rate": "rate", "Transmission delay": "trans", "Climate trend": "climate",
        "Combined: overrun + delay + offtaker + FX": "combined", "Structure 1": "s1", "Structure 2": "s2", "Structure 3": "s3",
        "Structure 4": "s4", "Structure 5": "s5", "CAPEX -20%": "capex_m20", "CAPEX +20%": "capex_p20", "Generation -10%": "gen_m10",
        "Generation +10%": "gen_p10", "Tariff -10%": "tar_m10", "Tariff +10%": "tar_p10", "OPEX +20%": "opex_p20",
        "Commercial rate +200bp": "rate_p200", "P90 generation in cash flows": "p90cf",
        "Dev: discount rate 18%": "dev_r18", "Dev: premium 6%": "dev_prem6", "Dev: stage odds +10pp": "dev_odds", "Dev: grant funds half of feasibility": "dev_grant", "Dev: tariff +10%": "dev_tar10", "Dev: all four levers": "dev_all", "Lender case: P90 one-year": "len1",
        "EPC 1 base": "epc1", "EPC 2 base": "epc2", "EPC 3 base": "epc3", "EPC 1 overrun 96%": "epc1_ov", "EPC 2 overrun 96%": "epc2_ov", "EPC 3 overrun 96%": "epc3_ov"}
out = {SLUG.get(k, k): dict(v, label=k) for k, v in results.items()}
for k, v in REQ.items():
    out[k]["req_tariff_flex"] = v
out["base_locked"]["be_flow_flex"] = BE_FLOW
json.dump(out, open("model/snapshot_results.json", "w"), indent=1, default=str)
print("done")
