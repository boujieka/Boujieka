"""SolaraPay Ltd - worked case study for Volume 2 (FICTIONAL company, FICTIONAL country).

SolaraPay Ltd is an invented PAYGo solar company in the invented "Republic of Kivara" (currency: Kivara shilling,
"KVS"). All figures, including the 24-month portfolio history, are synthetic and generated deterministically (seed below)
for teaching purposes. Any resemblance to a real company is unintended.

Two input sets:
  MANAGEMENT  - the business plan as submitted by SolaraPay management (default credit assumptions);
  CALIBRATED  - the analyst case: Tier 1-3 credit assumptions re-estimated from SolaraPay's own 24-month history.
The case workbook is built on CALIBRATED; MANAGEMENT is reproduced with the verified Python twin for comparison.
"""
import copy

import numpy as np

CASE = dict(
    key="solarapay", company="SolaraPay Ltd", country="Republic of Kivara", currency="KVS",
    title="WORKED CASE STUDY - SolaraPay Ltd (fictional)",
    out="volumes/02-solar-home-systems/case-study/SolaraPay_Case_Model_v0.7.xlsx",
)
SEED = 20261002
HIST_MONTHS = 24
HAZARD_UPLIFT = 1.30           # history shows defaults ~30% above management's assumption (Tiers 1-3)
HIST_COLL = {1: 0.86, 2: 0.87, 3: 0.89}  # observed collection on paying accounts

GENERAL_OVERRIDES = dict(
    fx0=135.0, currency="KVS", vols=[9000, 18000, 28000, 36000, 42000],
    staff=20_000_000, ga=8_000_000, eq0=1_215_000_000, min_cash=90_000_000,
    tl_amt=3_000_000, rf_limit=4_500_000_000, inv_usd=4_000_000, pre_money_usd=8_000_000,
    credit_mode=2,  # Credit_Input holds SolaraPay's 24-month history
)
MIX = {1: 0.25, 2: 0.40, 3: 0.22, 4: 0.09, 5: 0.04}
# Provenance labels shown in the workbook (brief section 13): the management plan is company data; Tier 1-3 credit
# assumptions are re-estimated from the (synthetic) history; everything else stays a model assumption.
PROVENANCE = {k: "COMPANY DATA" for k in ("vol1", "vol2", "vol3", "vol4", "vol5", "staff", "ga", "eq0", "min_cash", "tl_amt",
                                          "rf_limit", "inv_usd", "pre_money", "mix")}
PROVENANCE.update({"hazard": "CALIBRATED ASSUMPTION", "coll": "CALIBRATED ASSUMPTION"})
PROVENANCE_NOTES = {k: "Case: Tiers 1 to 3 re-estimated from SolaraPay's 24-month history (synthetic); Tiers 4 and 5 remain model assumptions."
                    for k in ("hazard", "coll")}


def apply(G, PRODUCTS, calibrated=True):
    """Mutate the shared defaults in place (so the generator and the twin both see the case)."""
    G.update(GENERAL_OVERRIDES)
    for p in PRODUCTS:
        p["mix"] = MIX[p["tier"]]
        if calibrated and p["tier"] in HIST_COLL:
            p["hazard"] = round(p["hazard"] * HAZARD_UPLIFT, 4)
            p["coll"] = HIST_COLL[p["tier"]]
    return G, PRODUCTS


def management_inputs(G0, P0):
    G, P = copy.deepcopy(G0), copy.deepcopy(P0)
    return apply(G, P, calibrated=False)


# ---------------------------------------------------------------- synthetic history
def history(PRODUCTS, G):
    """Monthly portfolio history (Tiers 1-3) and cohort checkpoints, generated with the CALIBRATED behaviour + noise."""
    rng = np.random.default_rng(SEED)
    credit, vintage = {}, {}
    for j, p in enumerate(PRODUCTS):
        if p["tier"] not in HIST_COLL:
            continue
        T, inst = p["tenor"], p["daily"] * 365 / 12
        markup = p["deposit"] + inst * T - p["price"]
        h, c = p["hazard"], p["coll"]
        orig = np.round(np.linspace(150, 420, HIST_MONTHS) * {1: 1.0, 2: 1.4, 3: 0.7}[p["tier"]] * rng.uniform(0.9, 1.1, HIST_MONTHS))
        S = lambda a: (1 - h) ** a
        rows, gross = [], 0.0
        for t in range(1, HIST_MONTHS + 1):
            due = coll = rar = unlock = 0.0
            for ci in range(1, t):
                a = t - ci
                n = orig[ci - 1]
                if 1 <= a <= T:
                    eps = rng.normal(1, 0.03)
                    due += n * inst
                    coll += n * inst * c * S(a) * eps
                    rar += n * (1 - S(a)) * (T - a) * (inst - markup / T)
                if a == T:
                    unlock += n * S(T)
            missed = due - coll
            gross += orig[t - 1] * (p["price"] - p["deposit"]) + markup / T * sum(
                orig[ci - 1] for ci in range(1, t) if 1 <= t - ci <= T) - coll - missed
            perf = max(0.0, gross - rar)
            sh = rng.dirichlet([60, 12, 6, 5, 7, 10])
            b0, b1 = perf * 0.86, perf * 0.14
            b_rar = [rar * s for s in (sh[2:] / sh[2:].sum())]
            resale = 0.0 if p["repo"] == 0 else missed * 0.05 * p["repo"]
            rows.append(dict(
                date=f"2024-{(t - 1) % 12 + 1:02d}-28" if t <= 12 else f"2025-{(t - 13) % 12 + 1:02d}-28",
                orig=orig[t - 1], gross=gross, b0=b0, b1=b1, b2=b_rar[0], b3=b_rar[1], b4=b_rar[2], b5=b_rar[3],
                dflt=b_rar[3], repo_units=round(resale / max(1, p["recov"] * p["price"])), resale=resale,
                rcost=resale * G["recov_cost"], cures=0, wo=missed, coll=coll, due=due, own=round(unlock),
                notes="SYNTHETIC - teaching data"))
        credit[j] = rows
        # vintage checkpoints for the first 18 cohorts (cumulative, at ages available within the history)
        vrows = {}
        for ci in range(1, 19):
            n = orig[ci - 1]
            age_max = HIST_MONTHS - ci
            cp = {}
            prev = None
            for k, m in enumerate([3, 6, 12, 18, 24, 36, 48, 60]):
                if m > age_max:
                    continue
                ages = range(1, min(m, T) + 1)
                due_c = n * inst * len(ages)
                coll_c = sum(n * inst * c * S(a) for a in ages) * rng.normal(1, 0.02)
                if prev is not None and prev[0] >= T:
                    # v0.8: past the tenor no instalment falls due and this synthetic behaviour has no late payments, so the
                    # cumulative collections stay where they were (the draw above is kept so that the random stream is unchanged)
                    coll_c = prev[1]
                prev = (m, coll_c)
                arrears = lambda kk: sum(n * inst * (1 - S(min(a, max(0, min(m, T) - kk + 1)))) for a in ages)
                rar_m = n * (1 - S(m)) * max(0, T - m) * (inst - markup / T)
                cp[k] = dict(coll=coll_c, due=due_c, dpd30=arrears(2) + rar_m * 0.75, dpd90=arrears(4) + rar_m * 0.55,
                             def180=arrears(7) + rar_m * 0.30, recov=0.0, active=n * (S(m) if m <= T else 0))
            own = None
            if 2 * T <= age_max:
                own = round(S(T) * rng.uniform(0.9, 0.97), 3)
            vrows[ci] = dict(units=n, cp=cp, own=own)
        vintage[j] = vrows
    return credit, vintage
