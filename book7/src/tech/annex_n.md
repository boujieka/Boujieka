## Annex N. Hydrology and energy assessment

### N.1 Purpose and scope

The IFC guide calls expected generation "one of the most important determinants" of viability and ranks hydrology as the highest development risk [DE:S1]. ESMAP reaches the same view for large projects and adds that climate change makes rigorous assessment more necessary [HY-06]. This annex follows the energy estimate from gauge to metered output, using Kasiri as the worked example. Kasiri values are case facts unless labelled as illustrative assumptions.

### N.2 Hydrological data: sources and quality

Water authorities usually hold measured discharge for main rivers but not for secondary rivers or future intake sites [DE:S1]. National hydrological institutes may publish gauged flows, flow statistics and runoff maps [LIT:S6]. In much of Africa the constraint is the base data itself: ESMAP lists insufficient data on hydrological flows as a barrier and recommends support to hydromet monitoring [HY-06].

A gauge records water level (stage), not discharge. Discharge comes from a rating curve fitted to paired stage and discharge measurements across the range of levels, preferably over at least a year [DE:S1; LIT:S6]:

> Q = a (H + B)^n^

where H is stage, B a datum correction and a, n fitted constants [LIT:S6]. High flows are seldom measured directly and are often estimated by the slope-area (Manning) method, which is sensitive to roughness: for natural streams with n of about 0.035, an error of 0.001 in n changes discharge by about 3% [LIT:S6].

The committee should ask for the share of infilled days, the highest discharge measured for the rating curve and how far it is extrapolated, whether a mobile bed shifts the curve after floods, and how the gauge is protected against floods [DE:S1].

### N.3 Length of record and record extension

The IFC guide asks for at least 15 years of flow or precipitation data, preferably consecutive [DE:S1]. Kasiri's record is 12 years, built from pre-feasibility gauging plus regional correlation. It is shorter than the benchmark and partly synthesised.

The IFC guide describes three ways to transpose station data to an intake [DE:S1]:

1. *Simultaneous measurements* at a temporary profile near the intake and an existing station, correlated and used to transpose the long series. It needs at least five dry, five average and five wet-period measurements and is the most accurate method.
2. *Specific runoff against altitude*, a regional curve of runoff (l/s/km²) against mean catchment altitude from several stations.
3. *Catchment area ratio*, which ignores vegetation, soil and geology and works best when the gauge is close to the intake:

> Q~intake~ = Q~gauge~ × (A~intake~ / A~gauge~)

ESHA adds standardised flow duration curves (flows divided by catchment area and rainfall, or by mean flow), which allow transfer from neighbouring rivers of similar topography and climate, and rainfall-runoff estimation where no flow record exists: mean runoff depth from a catchment water balance, converted as Q~m~ = (runoff depth in mm × area in km²) / 31,536, with the curve shape chosen from soil and base-flow indices, or a watershed model driven by daily rainfall [LIT:S6].

Two credit questions follow: does the extended series contain a drought as severe as the debt must survive, and is the correlation scatter carried into the P90? The IFC guide recommends verifying hydrology during design and, where possible, installing a permanent gauge at the intake [DE:S1].

### N.4 Flow duration curve and choice of design flow

A flow duration curve (FDC) ranks flows from highest to lowest against the percentage of time each is equalled or exceeded; Q~95~ is often taken as the characteristic low flow [DE:S1; LIT:S6]. A flat FDC means even flow through the year, a steep one large seasonal swings [DE:S1]. The averaging period matters: monthly averages smooth out peaks the turbines cannot use, and energy from monthly data can be overestimated by 10% or more compared with daily data [DE:S1].

Table N.1 ranks the twelve Kasiri monthly means. Usable flow is river flow less the 4 m3/s environmental flow, capped at the 57 m3/s design flow; power is derived in N.6.

Table: Table N.1. Kasiri monthly flow duration reading (case flows)
| Rank | Month | Flow (m3/s) | Exceedance m/12 (%) | Exceedance m/13 (%) | Usable flow (m3/s) | Power (MW) |
|---|---|---|---|---|---|---|
| 1 | May | 70 | 8.3 | 7.7 | 57 (9 spilled) | 60.5 |
| 2 | Jun | 58 | 16.7 | 15.4 | 54 | 57.3 |
| 3 | Apr | 52 | 25.0 | 23.1 | 48 | 50.9 |
| 4 | Nov | 46 | 33.3 | 30.8 | 42 | 44.6 |
| 5 | Jul | 40 | 41.7 | 38.5 | 36 | 38.2 |
| 6 | Dec | 36 | 50.0 | 46.2 | 32 | 34.0 |
| 7 | Oct | 30 | 58.3 | 53.8 | 26 | 27.6 |
| 8 | Mar | 28 | 66.7 | 61.5 | 24 | 25.5 |
| 9 | Aug | 28 | 75.0 | 69.2 | 24 | 25.5 |
| 10 | Jan | 24 | 83.3 | 76.9 | 20 | 21.2 |
| 11 | Sep | 22 | 91.7 | 84.6 | 18 | 19.1 |
| 12 | Feb | 20 | 100.0 | 92.3 | 16 | 17.0 |
Note: Mean flow 37.8 m3/s; mean usable flow 33.1 m3/s; median about 33 m3/s. Twelve monthly means cannot resolve Q~95~ or flood peaks. At 57 m3/s the hydraulic calculation gives 60.5 MW, slightly above the 60 MW rating; capping May at 60 MW would remove about 0.3 GWh.

First, full load needs 61 m3/s in the river (57 + 4), which only May exceeds, so on monthly data the plant runs at full output about one month in twelve; daily data would show more full-load days. Second, the level of use f~a~ = Q~d~/Q~av~ = 57/37.8 = 1.51, at the top of the 1.0 to 1.5 range the IFC guide gives for run-of-river plants, whose first-estimate rule is a design flow available 100 to 120 days a year, about 30% of the time [DE:S1]. Third, ESHA notes that optimisation normally gives a design flow "significantly larger than" mean flow less reserved flow [LIT:S6], here 33.8 m3/s. A 57 m3/s design flow is defensible only if the optimisation is shown: IRR, NPV, benefit/cost or LCOE computed across a range of design flows, with stepwise cost changes as unit and penstock sizes change [DE:S1; LIT:S6]. It should run on daily flows: a monthly FDC rewards oversizing.

Below a technical minimum flow the turbine cannot run [DE:S1]. The IFC guide gives about 40% of design flow for Francis, 20 to 40% for Kaplan and 10 to 20% for Pelton; ESHA gives Francis 50%, Kaplan 15% and Pelton 10% [DE:S1; LIT:S6]. Two units instead of one lower the plant minimum [DE:S1]. The case does not define the units. As an illustrative assumption: with one Francis unit at a 40% minimum (22.8 m3/s), January, February and September fall below it and the monthly model loses about 14% of energy; with two equal units the minimum falls to 11.4 m3/s and no month is lost.

### N.5 Environmental flow

The environmental (residual, reserved or compensation) flow is the water a licence requires to remain in the diverted reach. Too little damages aquatic life; too much cuts output, especially in low-flow periods [LIT:S6]. The IFC guide treats minimum flow as ecological needs plus downstream uses such as irrigation, water supply and fisheries, set case by case. Its sequence is: understand the flow regime, ecology and downstream uses; consult communities whose ecosystem services are at stake; define the values to preserve; then select "the most appropriate method" and monitor the release [DE:S1]. Ecologically, the ideal release would mimic the natural regime [DE:S1].

Neither guide prescribes a method or percentage. Practice ranges from hydrological indices (a share of mean flow or a low-flow percentile) through habitat methods to expert-panel seasonal regimes; a constant release is the simplest and most exposed to revision.

Kasiri's 4 m3/s is 10.6% of mean flow and 20% of the driest monthly mean. Each extra 1 m3/s costs about 1.06 MW whenever the plant is below full load, eleven months in twelve on Table N.1, or roughly 8 GWh a year (1.06 MW × 8,760 h × 11/12 × 0.95). The IFC checklist places minimum flow in Phase 3 due diligence because flow "is the key determinant of annual energy generation" [DE:S1]. The committee should know whether the licence fixes the release for the concession term.

### N.6 Energy calculation, step by step

Power at the transformer is

> P = η~t~ × η~g~ × η~tr~ × ρ × g × Q × H~n~ / 10^6^ (MW)

with ρ = 1,000 kg/m3 and g = 9.81 m/s2 [DE:S1]. At a typical 87% overall efficiency this reduces to P (kW) = 8.5 × Q × H [DE:S1]. Generator efficiencies are 90 to 98% and transformer efficiencies 98 to 99.5% [DE:S1].

**Gross to net head.** Gross head is headwater to tailwater for Francis and Kaplan units, and headwater to runner centre for Pelton units [DE:S1]. Net head deducts local losses (trash rack, entrance, bends, valves) and friction losses, which vary with the square of velocity, so net head is lowest at maximum flow; tailwater also rises with discharge [DE:S1; LIT:S6]. ESHA's example (3 m3/s, 85 m gross head) finds 1.52 m of losses and a 1.8% power loss [LIT:S6]. In medium and high-head schemes head can be treated as roughly constant [LIT:S6], which supports Kasiri's single 120 m net head as a first approximation.

**Energy and deductions.** Energy is the sum of power times hours over daily steps or FDC strips, stopping where flow falls below the larger of the minimum turbine flow and the reserved flow [DE:S1; LIT:S6]. Then deduct:

- *availability*: about 95% in year one (11 days scheduled maintenance, 7 days forced outage), rising to 97 to 98% after three years [DE:S1];
- *auxiliary demand*: 0.5 to 3.0% of generation [DE:S1];
- *transmission losses*, if the metering point is distant from the plant [DE:S1].

> E~net~ = Σ~i~ (ρ g Q~u,i~ H~n,i~ η~i~ t~i~) × A × (1 − a~aux~) × (1 − l~tx~)

Table: Table N.2. Kasiri energy check from case values
| Step | Calculation | Result |
|---|---|---|
| Overall efficiency | 0.92 × 0.98 | 0.9016 |
| Rated power | 9.81 × 57 × 120 × 0.9016 / 1,000 | 60.5 MW |
| Power per m3/s | 9.81 × 120 × 0.9016 / 1,000 | 1.061 MW |
| Mean usable flow | Table N.1 | 33.1 m3/s |
| Mean power | 1.061 × 33.1 | 35.1 MW |
| Gross energy | 35.1 × 8,760 h | 307.6 GWh |
| After availability | × 0.95 | 292.2 GWh |
| Capacity factor | 292.2 / (60 × 8.76) | 55.6% |
Note: Reproduces the case P50 (about 292 GWh) and capacity factor (about 56%); weighting months by days gives 292.7 GWh. The IFC range for run-of-river capacity factors is 40 to 70% [DE:S1].

The arithmetic holds, but the case figure is a monthly calculation with constant head and efficiency and no minimum flow, auxiliary use or line loss. Table N.3 sizes each omission.

Table: Table N.3. Kasiri: items outside the case P50 (effect on 292.2 GWh, one at a time)
| Item | Basis | Result |
|---|---|---|
| Auxiliary demand 0.5 to 3.0% | [DE:S1] | 290.7 to 283.4 GWh |
| Monthly data overestimate of 10% (292.2 / 1.10) | [DE:S1] | 266 GWh |
| One Francis unit, 40% minimum flow | Illustrative assumption | about 252 GWh |
| Losses on 35 km, 132 kV line | No source value | not quantified |
| Availability 97 to 98% after year three | [DE:S1] | 298 to 301 GWh |
| All flows 10% lower | Illustrative stress | 264 GWh |
Note: Effects are not additive. The case does not state where 292 GWh is measured; the PPA metering point decides which losses the project bears.

Outage timing matters: maintenance in February, at about 17 MW, costs far less than the same days in May at 60 MW.

### N.7 Firm energy and seasonal profile

ESHA defines firm energy as the power deliverable during a given period with at least 90 to 95% certainty; run-of-river schemes have little, storage adds more [LIT:S6]. In the IFC example, firm capacity at 90% of the year is 11 MW for a run-of-river plant and 23 MW for a storage plant at the same site [DE:S1]. On monthly means Kasiri's firm capacity is about 17 MW (February) to 19 MW (flow exceeded in 11 of 12 months) before outages, or about 16 MW in February after 95% availability, the figure Chapter 3 uses; that is under a third of installed capacity, and a daily Q~95~ would give less. The May to February power ratio is 3.6, milder than the ten-fold swing in the IFC central African example [DE:S1]. Where the PPA pays for capacity, the firm figure matters most.

### N.8 Inter-annual variability: P50, P90, one-year and multi-year

The IFC guide defines dry-year (P75) and very-dry-year (P95) energy and requires a DSCR above one under worst-case hydrology such as dry years [DE:S1]. A one-year P90 tests whether a single year's debt service is met; a multi-year P90 tests the average over a loan period. With the case CV of 0.15 and an assumed normal distribution:

> E~Px~ = E~P50~ × (1 − z~x~ × CV / √N)

where N is the number of averaged years and z = 1.282 for P90. The √N reduction assumes independent years. Dry years tend to cluster, which widens the true spread, so MODEL 7 adds a first-order serial correlation ρ between years, set at 0.3 for Kasiri as a model assumption:

> E~P90,N~ = E~P50~ × (1 − 1.2816 × CV × √((1 + ρ) / (1 − ρ) / N))

A second uncertainty sits on the mean: 12 years estimate it with a standard error of about 0.15/√12 = 4.3%, before rating-curve and correlation errors, and this term does not shrink with tenor.

Table: Table N.4. Kasiri exceedance values (CV 0.15, normal distribution assumed)
| Measure | Spread | GWh |
|---|---|---|
| P50 | none | 292 |
| P75, one year | 0.674 × 0.15 | 262 |
| P90, one year | 1.282 × 0.15 | 236 |
| P95, one year | 1.645 × 0.15 | 220 |
| P99, one year | 2.326 × 0.15 | 190 |
| P90, ten-year average | 1.282 × 0.15/√10 | 274 |
| P90, ten-year average, serial correlation 0.3 (MODEL 7 lender case) | 1.282 × 0.15 × √(1.857/10) | 268 |
| P90, 25-year average | 1.282 × 0.15/√25 | 281 |
| P90, ten-year average, with 4.3% mean uncertainty | 1.282 × √(0.047² + 0.043²) | 268 |
Note: Analyst calculation, except the MODEL 7 row. The two 268 GWh rows reach the same value by different routes: one widens the spread for correlated years, the other for the short record. Applied together they would give a lower figure. Skewed records give lower dry-year values still.

The one-year P90 is 19% below P50; a multi-year view alone understates what a debt service reserve must bridge. Kariba's 2024 drought allocation cut of about 47% shows how far the tail can reach in a regional drought [CL-04]. African PPAs often share this risk through deemed energy or a hydrological floor, negotiated on the quality of the hydrological data [LIT:S7].

### N.9 Design floods

The hydrological study must also cover flood frequency and severity, described by a hydrograph and not only a peak [LIT:S6]. The normal operation design flood is the largest flood passed in normal operation, defined by a return period; the maximum inflow design flood is the largest the structures must survive without failure, usually the probable maximum flood (PMF) or a 10,000-year flood [DE:S1; LIT:S6].

Table: Table N.5. Typical design flood criteria by hazard class
| Hazard class | Design flood |
|---|---|
| High | Maximum inflow: PMF or similar, or 10,000-year; normal operation: 1,000-year |
| Medium | 100-year to 1,000-year |
| Low | Typically 100-year; some countries set no requirement |
Note: Source [LIT:S6]. National legislation or industry guidelines bind [DE:S1; LIT:S6].

Reservoir routing lowers outflow peaks, so inflow flood and spillway capacity differ; for medium and low-hazard dams rules often ignore routing and require spillway capacity above a 100 to 1,000-year peak [LIT:S6]. Statistical frequency analysis suits less critical structures; dangerous dams need hydrological modelling to a PMF [LIT:S6]. Method choice matters: ESHA's 20-year series gives a 100-year flood of 83 m3/s under a lognormal fit and 103 m3/s under log-Pearson III, almost 25% higher, and extrapolation magnifies errors [LIT:S6]. World Bank dam safety guidance covers hydrological risk [HY-15].

The risk of exceeding a T-year flood in n years is

> R = 1 − (1 − 1/T)^n^

For Kasiri's 3-year construction, that is 14% for a 20-year flood and 3% for a 100-year flood; over 28 years of construction and operation, 25% for the 100-year flood. A 12-year record cannot define a 1,000-year flood statistically, so regional data or a rainfall-runoff model is needed, and the diversion flood should match the contractor's insurance and EPC risk allocation.

### N.10 Sediment

The IFC guide lists sedimentation among risks investors must cover and includes sediment transport in pre-feasibility work [DE:S1]. Rivers carry large sediment loads in floods [DE:S1]; the sources give no regional yield values, so yield must come from site sampling that includes flood flows.

In medium and high-head plants suspended sediment wears turbines and steelwork, cutting efficiency and life; quartz and angular particles are most abrasive [DE:S1]. Above 100 m head, all particles larger than 0.2 mm must be removed by the sand trap, against 0.3 mm at lower heads [DE:S1], so Kasiri's 120 m puts it in the 0.2 mm class. ESHA links trap performance to Francis repair intervals of about 6 to 7 years at 0.2 mm, 3 to 4 years at 0.3 mm and 1 to 2 years at 0.5 mm [LIT:S6]. Coatings and variable-speed units reduce abrasion [DE:S1].

In run-of-river schemes a flushed sand trap is essential, since most sediment otherwise reaches the turbines [DE:S1; LIT:S6]. In reservoirs, sedimentation erodes live storage and generation; remedies include catchment protection, check structures, flushing, mechanical removal and dam raising [DE:S1]. Global storage lost to sedimentation now exceeds storage added by new reservoirs [HY-06]. The energy model should include flushing losses and sediment outages, and the O&M budget the repair interval implied by the trap.

### N.11 Climate change and non-stationarity

A historical FDC assumes the future resembles the past. The IFC guide warns that discharges may deviate from historical values because of climate change, with significant regional changes in flow volume and timing [DE:S1]. ESMAP notes it is often transferred partly or fully to government [HY-06]. Planned hydropower in eastern and southern Africa concentrates capacity in a few basins and rainfall clusters, raising the risk of simultaneous drought [CL-03]. The IHA climate resilience guide sets out a phased screening and stress-test method [CL-01].

Three tests follow: trend and break tests on the record; a stress case from basin climate projections; and confirmation that covenants hold under that stress, not only under the historical P90. For Kasiri, a uniform 10% flow cut lowers energy by about 9.7% to 264 GWh: the fixed environmental flow takes a larger share, while the spilled May peak absorbs part of the cut.

### N.12 Independent energy assessment by the lenders' technical adviser

Lenders should have the energy estimate re-run by their technical adviser, not accept the sponsor's figure. The IFC due-diligence checklist covers catchment and hydro-meteorological data, the data basis (stations, data type, record length), flow available for generation, flood discharges, minimum flow, installed capacity, annual generation and dry-year probability analysis [DE:S1].

A complete review audits gauge data and rating curves on site; re-derives the transposition and its scatter; rebuilds the model on daily flows with flow-dependent head, efficiency and minimum flow; confirms the environmental flow against licence and ESIA; applies losses to the PPA metering point; reports P50, one-year and multi-year P90 with all uncertainty sources; runs climate and sediment cases; and reconciles results with PPA hydrology risk-sharing [LIT:S7]. The adviser's P50 and P90 should drive debt sizing.

### N.13 Decision tests

1. How many of Kasiri's 12 record years were measured near the intake, how many transposed, with what correlation scatter, and why is the record below the IFC's 15 years?
2. What is the highest measured discharge behind the rating curve, and what share of usable flow lies above it?
3. Was energy modelled on daily flows, and if not, what correction offsets the monthly overestimate of up to 10% or more?
4. Where is the IRR or LCOE curve against design flow that justifies 57 m3/s, given a level of use of 1.51?
5. How many units, of what type and minimum flow, and how much dry-season energy is lost below that minimum?
6. Is the 4 m3/s environmental flow fixed for the concession term, and what happens to debt service if a higher or seasonal release is imposed?
7. At which metering point is 292 GWh measured, and are auxiliary use and losses on the 35 km line deducted?
8. Does the debt service reserve cover a one-year P90 shortfall of about 56 GWh at the minimum DSCR?
9. Does the record show clustering of dry years, and has the multi-year P90 been widened for it?
10. Which design floods were used for spillway, diversion and powerhouse, how were they derived from 12 years of data, and which hazard class applies?
11. What sediment load was measured at what flows, what particle size does the trap remove, and what runner repair interval does the O&M budget assume?
12. Which climate stress case was run, and do covenants hold under it?
