"""Independent Python re-implementation of the SHS model logic (QA "shadow model").

Used to cross-check the Excel formulas: identical inputs must give identical outputs.
Run: python tools/shadow_shs.py [scenario]
"""
import sys

import numpy as np

from shs_defaults import PRODUCTS  # same default inputs

SCN = int(sys.argv[1]) if len(sys.argv) > 1 else 1
lev = {
    "haz": (1.0, 1.5, 2.0), "coll": (1.0, 0.95, 0.88), "vol": (1.0, 0.85, 0.70),
    "hw": (1.0, 1.05, 1.10), "dep": (0.05, 0.15, 0.30),
}
L = {k: v[SCN - 1] for k, v in lev.items()}
N = 60
fx0, infl, tax, pg = 130, 0.06, 0.30, 0.05
vols = [12000, 24000, 36000, 45000, 50000]
mm, cs, staff, ga, warr, duty = 0.02, 60, 6_500_000, 2_600_000, 0.05, 0.20
inv_cover, ap_days, capex_m, life, min_cash = 2, 60, 650_000, 36, 65_000_000
eq0, tl_amt, tl_m, tl_r, tl_g, tl_am = 390_000_000, 2_000_000, 6, 0.10, 12, 36
rf_lim, rf_adv, rf_r, rf_start = 1_300_000_000, 0.70, 0.16, 7

t = np.arange(1, N + 1)
year = (t - 1) // 12 + 1
fx = fx0 * (1 + L["dep"]) ** (t / 12)
fx_prev = np.concatenate([[fx0], fx[:-1]])
ii = (1 + infl) ** ((t - 1) / 12)
pi = (1 + pg) ** ((t - 1) / 12)
tot_units = np.array([vols[y - 1] for y in year]) / 12 * L["vol"]

agg = {k: np.zeros(N) for k in ["units", "iu", "dep", "hwrev", "fin", "due", "coll", "missed", "finc", "ecl",
                                "active", "rar", "cogs", "comm", "mkt"]}
for p in PRODUCTS:
    T = p["tenor"]
    inst = p["daily"] * 365 / 12
    contract = p["deposit"] + inst * T
    markup = contract - p["price"]
    h = p["hazard"] * L["haz"]
    c = min(1, p["coll"] * L["coll"])
    ages = np.arange(0, 61)
    S = (1 - h) ** ages
    due_u = np.where((ages >= 1) & (ages <= T), inst, 0)
    coll_u = due_u * c * S
    miss_u = due_u - coll_u
    rar_u = (1 - S) * np.maximum(0, T - ages) * (inst - markup / T)
    act_u = np.where(ages <= T, S, 0)
    units = tot_units * p["mix"]
    iu = units * pi
    for k in range(N):  # calendar month k (0-based)
        for cidx in range(k):  # cohorts sold before
            a = k - cidx
            agg["coll"][k] += iu[cidx] * coll_u[a]
            agg["rar"][k] += iu[cidx] * rar_u[a]
            agg["active"][k] += units[cidx] * act_u[a]
            if 1 <= a <= T:
                agg["due"][k] += iu[cidx] * inst
                agg["finc"][k] += iu[cidx] * markup / T
    agg["units"] += units
    agg["iu"] += iu
    agg["dep"] += iu * p["deposit"]
    agg["hwrev"] += iu * p["price"]
    agg["fin"] += iu * (p["price"] - p["deposit"])
    agg["ecl"] += iu * miss_u.sum()
    agg["cogs"] += units * p["hw"] * (1 + duty) * fx * L["hw"]
    agg["comm"] += units * p["comm"] * ii
    agg["mkt"] += units * p["mkt"] * ii
agg["missed"] = agg["due"] - agg["coll"]

cogs = agg["cogs"]
opex = cogs * warr + agg["comm"] + agg["mkt"] + (agg["dep"] + agg["coll"]) * mm + agg["active"] * cs * ii + (staff + ga) * ii
inv = cogs * inv_cover
inv_prev = np.concatenate([[0], inv[:-1]])
purch = cogs + inv - inv_prev
ap = purch * ap_days / (365 / 12)
capex = capex_m * ii
dep_ = np.array([capex[max(0, k - life + 1):k + 1].sum() / life for k in range(N)])
ppe = np.cumsum(capex - dep_)

# term loan
tl_usd = np.zeros(N); draw = np.zeros(N); rep = np.zeros(N); tl_int = np.zeros(N)
bal = 0.0
for k in range(N):
    m = k + 1
    tl_int[k] = bal * tl_r / 12 * fx[k]
    d = tl_amt if m == tl_m else 0
    r = min(bal, tl_amt / tl_am) if (tl_m + tl_g < m <= tl_m + tl_g + tl_am) else 0
    fxl = bal * (fx[k] - fx_prev[k])
    draw[k], rep[k] = d, r
    bal = bal + d - r
    tl_usd[k] = bal
fx_loss = np.concatenate([[0], tl_usd[:-1]]) * (fx - fx_prev)

gross = np.zeros(N); prov = np.zeros(N); cash = np.zeros(N); rf = np.zeros(N); eqtop = np.zeros(N)
ni = np.zeros(N); re = np.zeros(N)
g = pv = c_ = rfb = cum = mx = 0.0
netrec_prev = inv_p = ap_p = 0.0
for k in range(N):
    m = k + 1
    g = g + agg["fin"][k] + agg["finc"][k] - agg["coll"][k] - agg["missed"][k]
    pv = pv - agg["ecl"][k] + agg["missed"][k]
    netrec = g + pv
    elig = max(0, g - agg["rar"][k])
    rf_new = min(rf_lim, elig * rf_adv) if m >= rf_start else 0
    rf_int = rfb * rf_r / 12
    ebitda = agg["hwrev"][k] + agg["finc"][k] - cogs[k] - opex[k] - agg["ecl"][k]
    pbt = ebitda - dep_[k] - tl_int[k] - rf_int - fx_loss[k]
    cum += pbt
    mx_new = max(mx, cum)
    tx = tax * (max(0, mx_new) - max(0, mx))
    mx = mx_new
    n_ = pbt - tx
    cfo = n_ + dep_[k] + fx_loss[k] - (netrec - netrec_prev) - (inv[k] - inv_p) + (ap[k] - ap_p)
    pre = c_ + cfo - capex[k] + (draw[k] - rep[k]) * fx[k] + (rf_new - rfb) + (eq0 if m == 1 else 0)
    top = max(0, min_cash - pre)
    c_ = pre + top
    gross[k], prov[k], cash[k], rf[k], eqtop[k], ni[k] = g, pv, c_, rf_new, top, n_
    rfb, netrec_prev, inv_p, ap_p = rf_new, netrec, inv[k], ap[k]

rev = agg["hwrev"] + agg["finc"]
for y in range(1, 6):
    s = year == y
    e = y * 12 - 1
    print(f"Y{y}: rev {rev[s].sum():,.0f}  NI {ni[s].sum():,.0f}  cash {cash[e]:,.0f}  "
          f"CR {agg['coll'][s].sum() / agg['due'][s].sum():.3f}  active {agg['active'][e]:,.0f}  "
          f"gross {gross[e]:,.0f}  rf {rf[e]:,.0f}")
print(f"peak equity: {eq0 + eqtop.sum():,.0f}  (USD {(eq0 + eqtop.sum()) / fx0:,.0f})")
