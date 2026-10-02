"""Default inputs for the SHS PAYGo model - single source of truth.

Shared by the Excel generator (tools/build_shs_model.py) and the independent
Python twin (tools/shadow_shs.py). ALL VALUES ARE ILLUSTRATIVE placeholders for a
fictional company in a fictional market (LCY = local currency). They are not
benchmarks. Replace with company data before any use.

Product tiers are labelled by the ESMAP Multi-Tier Framework (MTF) *capacity*
attribute only (indicative). A full MTF tier assessment also covers duration,
reliability, quality, affordability, legality and health & safety.
"""

# MTF household electricity supply - capacity attribute thresholds (minimums).
# Source: ESMAP, "Beyond Connections: Energy Access Redefined" (2015). Recalled from
# memory - status "to verify" in sources/source-register.md (S15).
MTF_CAPACITY = {
    1: "≥3 W and ≥12 Wh/day",
    2: "≥50 W and ≥200 Wh/day",
    3: "≥200 W and ≥1.0 kWh/day",
    4: "≥800 W and ≥3.4 kWh/day",
    5: "≥2 kW and ≥8.2 kWh/day",
}

PRODUCTS = [
    dict(name="Tier 1 - Pico solar kit", tier=1, wp=10, wh=40,
         loads="1-3 lamps, phone charging, radio", segment="Rural, low income, first-time PAYGo",
         price=6500, deposit=1000, daily=25, tenor=12, hw=25, install=0, comm=500, mkt=300,
         warranty=0.03, mix=0.30, hazard=0.035, coll=0.88, repo=0.00, recov=0.20, rbf=5, adv=0.50),
    dict(name="Tier 2 - SHS with TV", tier=2, wp=80, wh=300,
         loads="4-6 lamps, radio, phone, 24-32\" DC TV", segment="Rural / peri-urban households",
         price=39000, deposit=4000, daily=77, tenor=24, hw=150, install=500, comm=2000, mkt=1000,
         warranty=0.05, mix=0.35, hazard=0.026, coll=0.88, repo=0.20, recov=0.25, rbf=15, adv=0.70),
    dict(name="Tier 3 - Large SHS + DC fridge", tier=3, wp=300, wh=1500,
         loads="Lighting, TV, DC fridge, fan", segment="Peri-urban households, kiosks",
         price=117000, deposit=17550, daily=173, tenor=30, hw=450, install=2500, comm=5000, mkt=2500,
         warranty=0.05, mix=0.20, hazard=0.019, coll=0.90, repo=0.40, recov=0.35, rbf=25, adv=0.70),
    dict(name="Tier 4 - Solar inverter + lithium (~1.2 kWp / 5 kWh)", tier=4, wp=1200, wh=5000,
         loads="AC loads: TV, fridge, fans, small tools", segment="Urban households & SMEs with weak grid",
         price=390000, deposit=78000, daily=445, tenor=36, hw=1400, install=15000, comm=12000, mkt=6000,
         warranty=0.06, mix=0.10, hazard=0.013, coll=0.92, repo=0.60, recov=0.45, rbf=0, adv=0.75),
    dict(name="Tier 5 - Solar inverter + lithium (~3 kWp / 10 kWh)", tier=5, wp=3000, wh=10000,
         loads="Full household AC loads, freezer, productive-use equipment", segment="Upper-income households, SMEs, productive use",
         price=845000, deposit=211250, daily=694, tenor=48, hw=3200, install=30000, comm=20000, mkt=10000,
         warranty=0.06, mix=0.05, hazard=0.010, coll=0.93, repo=0.70, recov=0.50, rbf=0, adv=0.75),
]

GENERAL = dict(
    scenario=1, fx0=130.0, infl=0.06, tax=0.30, price_g=0.05, fx_pass=0.50,
    vols=[12000, 24000, 36000, 45000, 50000],
    mm_fee=0.02, cs_cost=150, staff=26_000_000, ga=10_400_000, duty=0.20,
    inv_cover=2.0, ap_days=60, capex=900_000, dep_life=36, min_cash=100_000_000,
    repo_lag=3, rbf_on=1, rbf_lag=6,
    eq0=1_300_000_000,
    tl_amt=5_000_000, tl_month=6, tl_rate=0.10, tl_grace=12, tl_amort=36,
    rf_limit=6_500_000_000, rf_rate=0.16, rf_start=7,
    # covenants
    cov_cr=0.70, cov_rar=0.15, cov_lev=3.0, cov_dscr=1.20, cov_cash=50_000_000,
    # valuation & transaction
    wacc=0.22, tg=0.05, inv_usd=4_000_000, pre_money_usd=8_000_000,
    exit_method=1, exit_ebitda_mult=6.0, exit_pb_mult=1.5,
)

SCENARIOS = {  # Base, Downside, Severe
    "haz": (1.0, 1.3, 1.75),
    "coll": (1.0, 0.97, 0.92),
    "vol": (1.0, 0.90, 0.75),
    "hw": (1.0, 1.05, 1.10),
    "dep": (0.05, 0.12, 0.25),
}

MONTHS = 60
MAX_AGE = 60
