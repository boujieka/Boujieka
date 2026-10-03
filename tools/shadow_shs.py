"""Independent Python twin of the SHS PAYGo model (QA + sensitivity engine).

Re-implements the workbook logic in numpy from the same defaults (tools/shs_defaults.py).
Used to (1) cross-check the Excel formulas and (2) generate the static Sensitivity sheet.

Run: python tools/shadow_shs.py [scenario]
"""
import copy
import sys

import numpy as np
import numpy_financial as npf

from shs_defaults import GENERAL, MAX_AGE, MONTHS, PRODUCTS, SCENARIOS

N = MONTHS
YEARS = N // 12


def run(scn=1, lever=None, gen=None, products=None):
    g = dict(GENERAL, **(gen or {}))
    P = copy.deepcopy(products or PRODUCTS)
    L = {k: v[scn - 1] for k, v in SCENARIOS.items()}
    L.update(lever or {})

    t = np.arange(1, N + 1)
    year = (t - 1) // 12 + 1
    fx = g["fx0"] * (1 + L["dep"]) ** (t / 12)
    fx_prev = np.concatenate([[g["fx0"]], fx[:-1]])
    ii = (1 + g["infl"]) ** ((t - 1) / 12)
    pi = (1 + g["price_g"]) ** ((t - 1) / 12) * (fx / g["fx0"]) ** g["fx_pass"]
    tot_units = np.array([g["vols"][y - 1] for y in year]) / 12 * L["vol"]
    ages = np.arange(0, MAX_AGE + 1)

    keys = ["units", "dep", "hwrev", "fin", "due", "coll", "missed", "finc", "ecl", "recov", "rbf", "active", "rar",
            "gross", "bb", "cogs", "install", "warr", "comm", "mkt", "unlocks"]
    agg = {k: np.zeros(N) for k in keys}
    per = []
    for p in P:
        T = p["tenor"]
        inst = p["daily"] * 365 / 12
        contract = p["deposit"] + inst * T
        markup = contract - p["price"]
        h = p["hazard"] * L["haz"]
        c = min(1, p["coll"] * L["coll"])
        S = (1 - h) ** ages.astype(float)
        inT = (ages >= 1) & (ages <= T)
        due_u = np.where(inT, inst, 0.0)
        coll_u = due_u * c * S
        miss_u = due_u - coll_u
        rar_u = (1 - S) * np.maximum(0, T - ages) * (inst - markup / T)
        act_u = np.where(ages <= T, S, 0.0)
        def_u = np.zeros_like(S)
        def_u[1:] = np.where(inT[1:], S[:-1] - S[1:], 0.0)
        rec_u = np.zeros_like(S)
        for a in ages:
            b = a - g["repo_lag"]
            if 1 <= b <= T:
                rec_u[a] = def_u[b] * p["repo"] * p["recov"] * p["price"] * (1 - g["recov_cost"])
        units = tot_units * p["mix"]
        iu = units * pi
        d = {k: np.zeros(N) for k in keys}
        for k in range(N):
            m = k + 1
            for ci in range(1, m):
                a = m - ci
                d["coll"][k] += iu[ci - 1] * coll_u[a]
                d["rar"][k] += iu[ci - 1] * rar_u[a]
                d["recov"][k] += iu[ci - 1] * rec_u[a]
                d["active"][k] += units[ci - 1] * act_u[a]
                if 1 <= a <= T:
                    d["due"][k] += iu[ci - 1] * inst
                    d["finc"][k] += iu[ci - 1] * markup / T
            if m - g["rbf_lag"] >= 1:
                d["rbf"][k] = units[m - g["rbf_lag"] - 1] * p["rbf"] * fx[k] * g["rbf_on"]  # sales-based
            if m > T:
                d["unlocks"][k] = units[m - T - 1] * S[T]
        d["units"] = units
        d["dep"] = iu * p["deposit"]
        d["hwrev"] = iu * p["price"]
        d["fin"] = iu * (p["price"] - p["deposit"])
        d["missed"] = d["due"] - d["coll"]
        d["ecl"] = iu * miss_u.sum()
        d["gross"] = np.cumsum(d["fin"] + d["finc"] - d["coll"] - d["missed"])
        # RBF engine: 1 sales, 2 repayment-linked, 3 ownership-linked (0 without validated evidence), 4 hybrid
        lag = g["rbf_lag"]
        cd, cc = due_u[1:lag + 1].sum(), coll_u[1:lag + 1].sum()
        factor = min(1, (cc / cd) / g["rbf_rr_target"]) if cd > 0 else 0
        sales_rbf = d["rbf"].copy()
        own_rbf = np.zeros(N)  # ownership-linked requires validated actual data (none in the twin)
        opts = {1: sales_rbf, 2: sales_rbf * factor, 3: own_rbf,
                4: g["rbf_w"][0] * sales_rbf + g["rbf_w"][1] * sales_rbf * factor + g["rbf_w"][2] * own_rbf}
        d["rbf"] = opts[g["rbf_mode"]]
        # credit engine proxy buckets -> eligibility (lower DPD bound <= max DPD)
        perf = d["gross"] - d["rar"]
        lowers = [0, 1, 31, 61, 91, 181]
        shares_perf = [g["perf_current"], 1 - g["perf_current"]]
        elig = sum(perf * sh for lo, sh in zip(lowers[:2], shares_perf) if lo <= g["bb_max_dpd"]) + \
            sum(d["rar"] * sh for lo, sh in zip(lowers[2:], g["rar_shares"]) if lo <= g["bb_max_dpd"])
        d["bb"] = elig * p["adv"]
        d["cogs"] = units * p["hw"] * (1 + g["duty"]) * fx * L["hw"]
        d["install"] = units * p["install"] * ii
        d["warr"] = d["cogs"] * p["warranty"]
        d["comm"] = units * p["comm"] * ii
        d["mkt"] = units * p["mkt"] * ii
        for k_ in keys:
            agg[k_] += d[k_]
        per.append(d)

    cogs = agg["cogs"]
    other_rev = agg["active"] * g["other_arpu"] * ii
    cos = cogs + agg["install"] + other_rev * (1 - g["other_margin"])
    opex = (agg["warr"] + agg["comm"] + agg["mkt"] + (agg["dep"] + agg["coll"]) * g["mm_fee"]
            + agg["active"] * g["cs_cost"] * ii + (g["staff"] + g["ga"]) * ii)
    inv = np.zeros(N); inv_wd = np.zeros(N)
    for k in range(N):  # target cover; run down by consumption; written off in a month with no hardware sales
        prev = inv[k - 1] if k else 0.0
        inv_wd[k] = prev if cogs[k] <= 0 else 0.0
        inv[k] = max(cogs[k] * g["inv_cover"], prev - cogs[k] - inv_wd[k])
    inv_prev = np.concatenate([[0], inv[:-1]])
    ap = (cogs + inv - inv_prev + inv_wd) * g["ap_days"] / (365 / 12)
    cos = cos + inv_wd
    capex = g["capex"] * ii
    dep_ = np.array([capex[max(0, k - g["dep_life"] + 1):k + 1].sum() / g["dep_life"] for k in range(N)])
    ppe = np.cumsum(capex - dep_)

    # USD term loan
    tl_usd = np.zeros(N); draw = np.zeros(N); rep = np.zeros(N); tl_int = np.zeros(N)
    bal = 0.0
    for k in range(N):
        m = k + 1
        tl_int[k] = bal * g["tl_rate"] / 12 * fx[k]
        dr = g["tl_amt"] if m == g["tl_month"] else 0
        rp = min(bal, g["tl_amt"] / g["tl_amort"]) if g["tl_month"] + g["tl_grace"] < m <= g["tl_month"] + g["tl_grace"] + g["tl_amort"] else 0
        draw[k], rep[k] = dr, rp
        bal += dr - rp
        tl_usd[k] = bal
    fx_loss = np.concatenate([[0], tl_usd[:-1]]) * (fx - fx_prev)

    out = {k: np.zeros(N) for k in ["prov", "cash", "cash_pre", "rf", "rf_int", "eqtop", "ni", "ebitda", "cfo", "tax", "te", "netrec"]}
    pv = c_ = rfb = cum = mx = prev_flow = 0.0
    netrec_prev = inv_p = ap_p = 0.0
    sc = re_ = 0.0
    for k in range(N):
        m = k + 1
        pv = pv - agg["ecl"][k] + agg["missed"][k]
        netrec = agg["gross"][k] + pv
        sec = g["fin_struct"] == 2
        rf_int = rfb * (g["sec_rate"] if sec else g["rf_rate"]) / 12
        ebitda = (agg["hwrev"][k] + agg["finc"][k] + other_rev[k] - cos[k] + agg["rbf"][k] - opex[k] - agg["ecl"][k] + agg["recov"][k])
        fee = g["sec_fee"] * max(0, prev_flow) if sec else 0  # paid the month after the drawing
        pbt = ebitda - dep_[k] - tl_int[k] - rf_int - fee - fx_loss[k]
        cum += pbt
        mx_new = max(mx, cum)
        tx = g["tax"] * (max(0, mx_new) - max(0, mx))
        mx = mx_new
        ni = pbt - tx
        cfo = ni + dep_[k] + fx_loss[k] - (netrec - netrec_prev) - (inv[k] - inv_p) + (ap[k] - ap_p)
        pre_nf = c_ + cfo - capex[k] + (draw[k] - rep[k]) * fx[k] + (g["eq0"] if m == 1 else 0)
        rf_new = max(0, min(g["rf_limit"], agg["bb"][k], rfb + g["min_cash"] - pre_nf)) if m >= g["rf_start"] else 0
        pre = pre_nf + (rf_new - rfb)
        top = max(0, g["min_cash"] - pre)
        c_ = pre + top
        sc += (g["eq0"] if m == 1 else 0) + top
        re_ += ni
        for key, v in (("prov", pv), ("cash", c_), ("cash_pre", pre), ("rf", rf_new), ("rf_int", rf_int), ("eqtop", top),
                       ("ni", ni), ("ebitda", ebitda), ("cfo", cfo), ("tax", tx), ("te", sc + re_), ("netrec", netrec)):
            out[key][k] = v
        prev_flow = rf_new - rfb
        rfb, netrec_prev, inv_p, ap_p = rf_new, netrec, inv[k], ap[k]

    rev = agg["hwrev"] + agg["finc"] + other_rev
    tl_lcy = tl_usd * fx
    debt = tl_lcy + out["rf"]
    eq_cum = g["eq0"] + np.cumsum(out["eqtop"])

    # covenants (monthly)
    cr3 = np.array([agg["coll"][max(0, k - 2):k + 1].sum() / agg["due"][max(0, k - 2):k + 1].sum()
                    if agg["due"][max(0, k - 2):k + 1].sum() else 0 for k in range(N)])
    rar_ratio = np.divide(agg["rar"], agg["gross"], out=np.zeros(N), where=agg["gross"] != 0)
    lev = np.where(out["te"] <= 0, 99, debt / np.where(out["te"] == 0, 1, out["te"]))
    lowers = [31, 61, 91, 181]
    dpd30 = sum(agg["rar"] * sh for lo, sh in zip(lowers, g["rar_shares"]) if lo > 30)
    dpd90 = sum(agg["rar"] * sh for lo, sh in zip(lowers, g["rar_shares"]) if lo > 90)
    r30 = np.divide(dpd30, agg["gross"], out=np.zeros(N), where=agg["gross"] != 0)
    r90 = np.divide(dpd90, agg["gross"], out=np.zeros(N), where=agg["gross"] != 0)
    flags = np.maximum.reduce([
        ((out["rf"] > 0) & (r30 > g["cov_dpd30"])).astype(int),
        ((out["rf"] > 0) & (r90 > g["cov_dpd90"])).astype(int),
        ((out["rf"] > 0) & (cr3 < g["cov_cr"])).astype(int),
        ((out["rf"] > 0) & (rar_ratio > g["cov_rar"])).astype(int),
        ((debt > 0) & (lev > g["cov_lev"])).astype(int),
        ((debt > 0) & (out["cash_pre"] < g["cov_cash"])).astype(int)])

    # annual
    ys = [year == y for y in range(1, YEARS + 1)]
    ye = [y * 12 - 1 for y in range(1, YEARS + 1)]
    A = lambda arr: np.array([arr[s].sum() for s in ys])
    E = lambda arr: np.array([arr[e] for e in ye])
    fx_avg = np.array([fx[s].mean() for s in ys])
    ds = A(tl_int) + A(rep * fx) + A(out["rf_int"])
    d_netrec = out["netrec"] - np.concatenate([[0.0], out["netrec"][:-1]])
    cf_basis = A(out["cfo"]) + (A(d_netrec) if g.get("dscr_basis", 1) == 2 else 0.0)  # basis 2: excluding growth in receivables
    dscr = np.divide(cf_basis + A(tl_int) + A(out["rf_int"]), ds, out=np.zeros(YEARS), where=ds != 0)

    # valuation
    nwc = E(out["netrec"]) + E(inv) - E(ap)
    fcff = A(out["ebitda"]) - A(out["tax"]) - A(capex) - np.diff(np.concatenate([[0], nwc]))
    w, tg = g["wacc"], g["tg"]
    pvs = fcff / (1 + w) ** (np.arange(1, YEARS + 1) - 0.5)
    tv_fcff = (A(out["ebitda"])[-1] - A(out["tax"])[-1] - A(capex)[-1]) * (1 + tg) - tg * nwc[-1]
    tv = tv_fcff / (w - tg) if w > tg else 0
    ev = pvs.sum() + tv / (1 + w) ** YEARS
    net_debt5 = debt[-1] - out["cash"][-1]
    if g["exit_method"] == 1:
        exit_eq = max(0, g["exit_ebitda_mult"] * A(out["ebitda"])[-1] - net_debt5)
    else:
        exit_eq = max(0, g["exit_pb_mult"] * out["te"][-1])
    stake = g["inv_usd"] / (g["pre_money_usd"] + g["inv_usd"])
    flows = np.concatenate([[-g["inv_usd"]], -stake * A(out["eqtop"]) / fx_avg])
    flows[-1] += stake * exit_eq / fx[-1]
    irr = npf.irr(flows)
    moic = flows[flows > 0].sum() / -flows[flows < 0].sum()

    return dict(
        rev=A(rev), ni=A(out["ni"]), ebitda=A(out["ebitda"]), cash=E(out["cash"]), gross=E(agg["gross"]), rf=E(out["rf"]),
        cr=A(agg["coll"]) / A(agg["due"]), active=E(agg["active"]), dscr=dscr, fcff=fcff,
        peak_eq=eq_cum.max(), peak_eq_usd=eq_cum.max() / g["fx0"], rev5_usd=A(rev)[-1] / fx_avg[-1],
        ebitda_m5=A(out["ebitda"])[-1] / A(rev)[-1], cr5=A(agg["coll"])[-1] / A(agg["due"])[-1],
        ev=ev, ev_usd=ev / g["fx0"], exit_eq=exit_eq, irr=float(irr), moic=float(moic),
        breach_months=int(flags.sum()), min_cr3=cr3[2:].min(), max_rar=rar_ratio.max(), flows=flows,
    )


def sensitivity_cases():
    mix_hi = copy.deepcopy(PRODUCTS)
    for p, m in zip(mix_hi, [0.20, 0.30, 0.20, 0.20, 0.10]):
        p["mix"] = m
    cases = [
        ("Base", dict(scn=1)),
        ("Downside", dict(scn=2)),
        ("Severe", dict(scn=3)),
        ("Base - default hazard x1.5", dict(lever={"haz": 1.5})),
        ("Base - collection rate x0.95", dict(lever={"coll": 0.95})),
        ("Base - sales volume -20%", dict(lever={"vol": 0.8})),
        ("Base - hardware cost +15%", dict(lever={"hw": 1.15})),
        ("Base - LCY depreciation 20% p.a.", dict(lever={"dep": 0.20})),
        ("Base - no price increase on new contracts", dict(gen={"price_g": 0.0})),
        ("Base - RBF programme off", dict(gen={"rbf_on": 0})),
        ("Base - mix T1 20%, T2 30%, T3 20%, T4 20%, T5 10%", dict(products=mix_hi)),
        ("Base - exit at 4.0x EBITDA", dict(gen={"exit_ebitda_mult": 4.0})),
        ("Base - repayment-linked RBF (mode 2)", dict(gen={"rbf_mode": 2})),
        ("Base - securitisation structure", dict(gen={"fin_struct": 2})),
        ("Base - borrowing base up to 90 DPD (base does not bind at default)", dict(gen={"bb_max_dpd": 90})),
    ]
    return [(name, run(**kw)) for name, kw in cases]


if __name__ == "__main__":
    scn = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    r = run(scn)
    for y in range(YEARS):
        print(f"Y{y + 1}: rev {r['rev'][y]:,.0f}  EBITDA {r['ebitda'][y]:,.0f}  NI {r['ni'][y]:,.0f}  cash {r['cash'][y]:,.0f}  "
              f"CR {r['cr'][y]:.3f}  active {r['active'][y]:,.0f}  rf {r['rf'][y]:,.0f}  DSCR {r['dscr'][y]:.2f}")
    print(f"peak equity {r['peak_eq']:,.0f} (USD {r['peak_eq_usd']:,.0f}) | EV USD {r['ev_usd']:,.0f} | exit eq {r['exit_eq']:,.0f}"
          f" | IRR {r['irr']:.3f} MOIC {r['moic']:.2f} | breaches {r['breach_months']} | minCR3 {r['min_cr3']:.3f}"
          f" maxRaR {r['max_rar']:.3f}")
