"""Default (illustrative) product inputs for the SHS model - shared by generator and shadow model."""

PRODUCTS = [
    # name, cash price LCY, deposit LCY, daily rate LCY, tenor (m), HW cost USD,
    # commission LCY, marketing LCY, mix, base monthly default hazard, base collection on performing
    dict(name="P1 Solar lantern kit (Tier 1)", price=6500, deposit=1000, daily=25, tenor=12,
         hw=25, comm=500, mkt=300, mix=0.40, hazard=0.025, coll=0.92),
    dict(name="P2 SHS lights+radio (Tier 2)", price=26000, deposit=3000, daily=60, tenor=18,
         hw=90, comm=1500, mkt=800, mix=0.40, hazard=0.020, coll=0.90),
    dict(name="P3 SHS with TV (Tier 3)", price=65000, deposit=6500, daily=130, tenor=24,
         hw=260, comm=3000, mkt=1500, mix=0.20, hazard=0.015, coll=0.90),
]
