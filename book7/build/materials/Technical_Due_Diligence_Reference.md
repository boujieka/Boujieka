# Technical due-diligence reference

The five annexes that follow are a reference, not the core of the book. The book's method is the decision framework of the eighteen chapters. These annexes give the investment or credit committee member enough engineering and environmental knowledge to challenge the engineering case: to know what a sound hydrology study, layout, equipment choice, construction plan or environmental and social assessment looks like, and which questions expose a weak one.

They draw on the full texts of the IFC guide [DE:S1], the ESHA guide [LIT:S6], the Addleshaw Goddard and IHA investor's guide [LIT:S7] and the World Bank and ESMAP report on private solutions for large hydropower [HY-06], together with the book's source database. Each annex works through Kasiri where the case defines the values, flags every illustrative assumption it adds, and ends with decision tests. The table shows which questions of the Hydro Readiness Framework and which chapters each annex informs.

| Annex | Topic | Framework questions | Chapters |
|---|---|---|---|
| N | Hydrology and energy assessment | Q1, Q5 | 2, 12, 16 |
| O | Scheme layout, civil works and geotechnics | Q1, Q6 | 3, 9, 10 |
| P | Electromechanical equipment and grid connection | Q1, Q3, Q6 | 3, 9, 11 |
| Q | Construction, commissioning, operation and maintenance | Q6 | 9, 10, 11 |
| R | Environmental, social and climate due diligence | Q2, Q5, Q7 | 2, 7, 15, 16 |

# Annex N. Hydrology and energy assessment

## N.1 Purpose and scope

The IFC guide calls expected generation "one of the most important determinants" of viability and ranks hydrology as the highest development risk [DE:S1]. ESMAP reaches the same view for large projects and adds that climate change makes rigorous assessment more necessary [HY-06]. This annex follows the energy estimate from gauge to metered output, using Kasiri as the worked example. Kasiri values are case facts unless labelled as illustrative assumptions.

## N.2 Hydrological data: sources and quality

Water authorities usually hold measured discharge for main rivers but not for secondary rivers or future intake sites [DE:S1]. National hydrological institutes may publish gauged flows, flow statistics and runoff maps [LIT:S6]. In much of Africa the constraint is the base data itself: ESMAP lists insufficient data on hydrological flows as a barrier and recommends support to hydromet monitoring [HY-06].

A gauge records water level (stage), not discharge. Discharge comes from a rating curve fitted to paired stage and discharge measurements across the range of levels, preferably over at least a year [DE:S1; LIT:S6]:

> Q = a (H + B)<sup>n</sup>

where H is stage, B a datum correction and a, n fitted constants [LIT:S6]. High flows are seldom measured directly and are often estimated by the slope-area (Manning) method, which is sensitive to roughness: for natural streams with n of about 0.035, an error of 0.001 in n changes discharge by about 3% [LIT:S6].

The committee should ask for the share of infilled days, the highest discharge measured for the rating curve and how far it is extrapolated, whether a mobile bed shifts the curve after floods, and how the gauge is protected against floods [DE:S1].

## N.3 Length of record and record extension

The IFC guide asks for at least 15 years of flow or precipitation data, preferably consecutive [DE:S1]. Kasiri's record is 12 years, built from pre-feasibility gauging plus regional correlation. It is shorter than the benchmark and partly synthesised.

The IFC guide describes three ways to transpose station data to an intake [DE:S1]:

1. *Simultaneous measurements* at a temporary profile near the intake and an existing station, correlated and used to transpose the long series. It needs at least five dry, five average and five wet-period measurements and is the most accurate method.
2. *Specific runoff against altitude*, a regional curve of runoff (l/s/km²) against mean catchment altitude from several stations.
3. *Catchment area ratio*, which ignores vegetation, soil and geology and works best when the gauge is close to the intake:

> Q<sub>intake</sub> = Q<sub>gauge</sub> × (A<sub>intake</sub> / A<sub>gauge</sub>)

ESHA adds standardised flow duration curves (flows divided by catchment area and rainfall, or by mean flow), which allow transfer from neighbouring rivers of similar topography and climate, and rainfall-runoff estimation where no flow record exists: mean runoff depth from a catchment water balance, converted as Q<sub>m</sub> = (runoff depth in mm × area in km²) / 31,536, with the curve shape chosen from soil and base-flow indices, or a watershed model driven by daily rainfall [LIT:S6].

Two credit questions follow: does the extended series contain a drought as severe as the debt must survive, and is the correlation scatter carried into the P90? The IFC guide recommends verifying hydrology during design and, where possible, installing a permanent gauge at the intake [DE:S1].

## N.4 Flow duration curve and choice of design flow

A flow duration curve (FDC) ranks flows from highest to lowest against the percentage of time each is equalled or exceeded; Q<sub>95</sub> is often taken as the characteristic low flow [DE:S1; LIT:S6]. A flat FDC means even flow through the year, a steep one large seasonal swings [DE:S1]. The averaging period matters: monthly averages smooth out peaks the turbines cannot use, and energy from monthly data can be overestimated by 10% or more compared with daily data [DE:S1].

Table N.1 ranks the twelve Kasiri monthly means. Usable flow is river flow less the 4 m3/s environmental flow, capped at the 57 m3/s design flow; power is derived in N.6.


**Table N.1. Kasiri monthly flow duration reading (case flows)**
{: .cap}

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

*Note: Mean flow 37.8 m3/s; mean usable flow 33.1 m3/s; median about 33 m3/s. Twelve monthly means cannot resolve Q<sub>95</sub> or flood peaks. At 57 m3/s the hydraulic calculation gives 60.5 MW, slightly above the 60 MW rating; capping May at 60 MW would remove about 0.3 GWh.*

First, full load needs 61 m3/s in the river (57 + 4), which only May exceeds, so on monthly data the plant runs at full output about one month in twelve; daily data would show more full-load days. Second, the level of use f<sub>a</sub> = Q<sub>d</sub>/Q<sub>av</sub> = 57/37.8 = 1.51, at the top of the 1.0 to 1.5 range the IFC guide gives for run-of-river plants, whose first-estimate rule is a design flow available 100 to 120 days a year, about 30% of the time [DE:S1]. Third, ESHA notes that optimisation normally gives a design flow "significantly larger than" mean flow less reserved flow [LIT:S6], here 33.8 m3/s. A 57 m3/s design flow is defensible only if the optimisation is shown: IRR, NPV, benefit/cost or LCOE computed across a range of design flows, with stepwise cost changes as unit and penstock sizes change [DE:S1; LIT:S6]. It should run on daily flows: a monthly FDC rewards oversizing.

Below a technical minimum flow the turbine cannot run [DE:S1]. The IFC guide gives about 40% of design flow for Francis, 20 to 40% for Kaplan and 10 to 20% for Pelton; ESHA gives Francis 50%, Kaplan 15% and Pelton 10% [DE:S1; LIT:S6]. Two units instead of one lower the plant minimum [DE:S1]. The case does not define the units. As an illustrative assumption: with one Francis unit at a 40% minimum (22.8 m3/s), January, February and September fall below it and the monthly model loses about 14% of energy; with two equal units the minimum falls to 11.4 m3/s and no month is lost.

## N.5 Environmental flow

The environmental (residual, reserved or compensation) flow is the water a licence requires to remain in the diverted reach. Too little damages aquatic life; too much cuts output, especially in low-flow periods [LIT:S6]. The IFC guide treats minimum flow as ecological needs plus downstream uses such as irrigation, water supply and fisheries, set case by case. Its sequence is: understand the flow regime, ecology and downstream uses; consult communities whose ecosystem services are at stake; define the values to preserve; then select "the most appropriate method" and monitor the release [DE:S1]. Ecologically, the ideal release would mimic the natural regime [DE:S1].

Neither guide prescribes a method or percentage. Practice ranges from hydrological indices (a share of mean flow or a low-flow percentile) through habitat methods to expert-panel seasonal regimes; a constant release is the simplest and most exposed to revision.

Kasiri's 4 m3/s is 10.6% of mean flow and 20% of the driest monthly mean. Each extra 1 m3/s costs about 1.06 MW whenever the plant is below full load, eleven months in twelve on Table N.1, or roughly 8 GWh a year (1.06 MW × 8,760 h × 11/12 × 0.95). The IFC checklist places minimum flow in Phase 3 due diligence because flow "is the key determinant of annual energy generation" [DE:S1]. The committee should know whether the licence fixes the release for the concession term.

## N.6 Energy calculation, step by step

Power at the transformer is

> P = η<sub>t</sub> × η<sub>g</sub> × η<sub>tr</sub> × ρ × g × Q × H<sub>n</sub> / 10<sup>6</sup> (MW)

with ρ = 1,000 kg/m3 and g = 9.81 m/s2 [DE:S1]. At a typical 87% overall efficiency this reduces to P (kW) = 8.5 × Q × H [DE:S1]. Generator efficiencies are 90 to 98% and transformer efficiencies 98 to 99.5% [DE:S1].

**Gross to net head.** Gross head is headwater to tailwater for Francis and Kaplan units, and headwater to runner centre for Pelton units [DE:S1]. Net head deducts local losses (trash rack, entrance, bends, valves) and friction losses, which vary with the square of velocity, so net head is lowest at maximum flow; tailwater also rises with discharge [DE:S1; LIT:S6]. ESHA's example (3 m3/s, 85 m gross head) finds 1.52 m of losses and a 1.8% power loss [LIT:S6]. In medium and high-head schemes head can be treated as roughly constant [LIT:S6], which supports Kasiri's single 120 m net head as a first approximation.

**Energy and deductions.** Energy is the sum of power times hours over daily steps or FDC strips, stopping where flow falls below the larger of the minimum turbine flow and the reserved flow [DE:S1; LIT:S6]. Then deduct:

- *availability*: about 95% in year one (11 days scheduled maintenance, 7 days forced outage), rising to 97 to 98% after three years [DE:S1];
- *auxiliary demand*: 0.5 to 3.0% of generation [DE:S1];
- *transmission losses*, if the metering point is distant from the plant [DE:S1].

> E<sub>net</sub> = Σ<sub>i</sub> (ρ g Q<sub>u,i</sub> H<sub>n,i</sub> η<sub>i</sub> t<sub>i</sub>) × A × (1 − a<sub>aux</sub>) × (1 − l<sub>tx</sub>)


**Table N.2. Kasiri energy check from case values**
{: .cap}

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

*Note: Reproduces the case P50 (about 292 GWh) and capacity factor (about 56%); weighting months by days gives 292.7 GWh. The IFC range for run-of-river capacity factors is 40 to 70% [DE:S1].*

The arithmetic holds, but the case figure is a monthly calculation with constant head and efficiency and no minimum flow, auxiliary use or line loss. Table N.3 sizes each omission.


**Table N.3. Kasiri: items outside the case P50 (effect on 292.2 GWh, one at a time)**
{: .cap}

| Item | Basis | Result |
|---|---|---|
| Auxiliary demand 0.5 to 3.0% | [DE:S1] | 290.7 to 283.4 GWh |
| Monthly data overestimate of 10% (292.2 / 1.10) | [DE:S1] | 266 GWh |
| One Francis unit, 40% minimum flow | Illustrative assumption | about 252 GWh |
| Losses on 35 km, 132 kV line | No source value | not quantified |
| Availability 97 to 98% after year three | [DE:S1] | 298 to 301 GWh |
| All flows 10% lower | Illustrative stress | 264 GWh |

*Note: Effects are not additive. The case does not state where 292 GWh is measured; the PPA metering point decides which losses the project bears.*

Outage timing matters: maintenance in February, at about 17 MW, costs far less than the same days in May at 60 MW.

## N.7 Firm energy and seasonal profile

ESHA defines firm energy as the power deliverable during a given period with at least 90 to 95% certainty; run-of-river schemes have little, storage adds more [LIT:S6]. In the IFC example, firm capacity at 90% of the year is 11 MW for a run-of-river plant and 23 MW for a storage plant at the same site [DE:S1]. On monthly means Kasiri's firm capacity is about 17 MW (February) to 19 MW (flow exceeded in 11 of 12 months) before outages, or about 16 MW in February after 95% availability, the figure Chapter 3 uses; that is under a third of installed capacity, and a daily Q<sub>95</sub> would give less. The May to February power ratio is 3.6, milder than the ten-fold swing in the IFC central African example [DE:S1]. Where the PPA pays for capacity, the firm figure matters most.

## N.8 Inter-annual variability: P50, P90, one-year and multi-year

The IFC guide defines dry-year (P75) and very-dry-year (P95) energy and requires a DSCR above one under worst-case hydrology such as dry years [DE:S1]. A one-year P90 tests whether a single year's debt service is met; a multi-year P90 tests the average over a loan period. With the case CV of 0.15 and an assumed normal distribution:

> E<sub>Px</sub> = E<sub>P50</sub> × (1 − z<sub>x</sub> × CV / √N)

where N is the number of averaged years and z = 1.282 for P90. The √N reduction assumes independent years. Dry years tend to cluster, which widens the true spread, so MODEL 7 adds a first-order serial correlation ρ between years, set at 0.3 for Kasiri as a model assumption:

> E<sub>P90,N</sub> = E<sub>P50</sub> × (1 − 1.2816 × CV × √((1 + ρ) / (1 − ρ) / N))

A second uncertainty sits on the mean: 12 years estimate it with a standard error of about 0.15/√12 = 4.3%, before rating-curve and correlation errors, and this term does not shrink with tenor.


**Table N.4. Kasiri exceedance values (CV 0.15, normal distribution assumed)**
{: .cap}

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

*Note: Analyst calculation, except the MODEL 7 row. The two 268 GWh rows reach the same value by different routes: one widens the spread for correlated years, the other for the short record. Applied together they would give a lower figure. Skewed records give lower dry-year values still.*

The one-year P90 is 19% below P50; a multi-year view alone understates what a debt service reserve must bridge. Kariba's 2024 drought allocation cut of about 47% shows how far the tail can reach in a regional drought [CL-04]. African PPAs often share this risk through deemed energy or a hydrological floor, negotiated on the quality of the hydrological data [LIT:S7].

## N.9 Design floods

The hydrological study must also cover flood frequency and severity, described by a hydrograph and not only a peak [LIT:S6]. The normal operation design flood is the largest flood passed in normal operation, defined by a return period; the maximum inflow design flood is the largest the structures must survive without failure, usually the probable maximum flood (PMF) or a 10,000-year flood [DE:S1; LIT:S6].


**Table N.5. Typical design flood criteria by hazard class**
{: .cap}

| Hazard class | Design flood |
|---|---|
| High | Maximum inflow: PMF or similar, or 10,000-year; normal operation: 1,000-year |
| Medium | 100-year to 1,000-year |
| Low | Typically 100-year; some countries set no requirement |

*Note: Source [LIT:S6]. National legislation or industry guidelines bind [DE:S1; LIT:S6].*

Reservoir routing lowers outflow peaks, so inflow flood and spillway capacity differ; for medium and low-hazard dams rules often ignore routing and require spillway capacity above a 100 to 1,000-year peak [LIT:S6]. Statistical frequency analysis suits less critical structures; dangerous dams need hydrological modelling to a PMF [LIT:S6]. Method choice matters: ESHA's 20-year series gives a 100-year flood of 83 m3/s under a lognormal fit and 103 m3/s under log-Pearson III, almost 25% higher, and extrapolation magnifies errors [LIT:S6]. World Bank dam safety guidance covers hydrological risk [HY-15].

The risk of exceeding a T-year flood in n years is

> R = 1 − (1 − 1/T)<sup>n</sup>

For Kasiri's 3-year construction, that is 14% for a 20-year flood and 3% for a 100-year flood; over 28 years of construction and operation, 25% for the 100-year flood. A 12-year record cannot define a 1,000-year flood statistically, so regional data or a rainfall-runoff model is needed, and the diversion flood should match the contractor's insurance and EPC risk allocation.

## N.10 Sediment

The IFC guide lists sedimentation among risks investors must cover and includes sediment transport in pre-feasibility work [DE:S1]. Rivers carry large sediment loads in floods [DE:S1]; the sources give no regional yield values, so yield must come from site sampling that includes flood flows.

In medium and high-head plants suspended sediment wears turbines and steelwork, cutting efficiency and life; quartz and angular particles are most abrasive [DE:S1]. Above 100 m head, all particles larger than 0.2 mm must be removed by the sand trap, against 0.3 mm at lower heads [DE:S1], so Kasiri's 120 m puts it in the 0.2 mm class. ESHA links trap performance to Francis repair intervals of about 6 to 7 years at 0.2 mm, 3 to 4 years at 0.3 mm and 1 to 2 years at 0.5 mm [LIT:S6]. Coatings and variable-speed units reduce abrasion [DE:S1].

In run-of-river schemes a flushed sand trap is essential, since most sediment otherwise reaches the turbines [DE:S1; LIT:S6]. In reservoirs, sedimentation erodes live storage and generation; remedies include catchment protection, check structures, flushing, mechanical removal and dam raising [DE:S1]. Global storage lost to sedimentation now exceeds storage added by new reservoirs [HY-06]. The energy model should include flushing losses and sediment outages, and the O&M budget the repair interval implied by the trap.

## N.11 Climate change and non-stationarity

A historical FDC assumes the future resembles the past. The IFC guide warns that discharges may deviate from historical values because of climate change, with significant regional changes in flow volume and timing [DE:S1]. ESMAP notes it is often transferred partly or fully to government [HY-06]. Planned hydropower in eastern and southern Africa concentrates capacity in a few basins and rainfall clusters, raising the risk of simultaneous drought [CL-03]. The IHA climate resilience guide sets out a phased screening and stress-test method [CL-01].

Three tests follow: trend and break tests on the record; a stress case from basin climate projections; and confirmation that covenants hold under that stress, not only under the historical P90. For Kasiri, a uniform 10% flow cut lowers energy by about 9.7% to 264 GWh: the fixed environmental flow takes a larger share, while the spilled May peak absorbs part of the cut.

## N.12 Independent energy assessment by the lenders' technical adviser

Lenders should have the energy estimate re-run by their technical adviser, not accept the sponsor's figure. The IFC due-diligence checklist covers catchment and hydro-meteorological data, the data basis (stations, data type, record length), flow available for generation, flood discharges, minimum flow, installed capacity, annual generation and dry-year probability analysis [DE:S1].

A complete review audits gauge data and rating curves on site; re-derives the transposition and its scatter; rebuilds the model on daily flows with flow-dependent head, efficiency and minimum flow; confirms the environmental flow against licence and ESIA; applies losses to the PPA metering point; reports P50, one-year and multi-year P90 with all uncertainty sources; runs climate and sediment cases; and reconciles results with PPA hydrology risk-sharing [LIT:S7]. The adviser's P50 and P90 should drive debt sizing.

## N.13 Decision tests

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

# Annex O. Scheme layout, civil works and geotechnics

## O.1 Purpose and scope

This annex gives a credit committee enough civil engineering to test a feasibility study, an EPC price and a technical adviser's report. Civil works are the largest and least predictable block of hydropower capital cost [DE:S1]. Kasiri figures are case values; every Kasiri layout dimension is an illustrative assumption and is labelled as such.

## O.2 Scheme types and what they mean for revenue and risk

The IFC guide classifies schemes by operation as run-of-river, storage and pumped storage [DE:S1]. Two further categories matter to a financier: pondage (a run-of-river plant with a small daily or weekly storage) and cascades (several plants on one river whose operation interacts).


**Table O.1. Scheme types, revenue profile and characteristic risk**
{: .cap}

| Scheme type | How it works | Revenue profile | Characteristic civil and E&S risk |
|---|---|---|---|
| Run-of-river | Uses inflow as it arrives; little or no storage, so peaking lasts a few hours at most [DE:S1] | Follows seasonal and inter-annual flow [DE:S1] | Sediment reaches the turbines, so a sand trap is essential [DE:S1]; perceived lower E&S risk, favoured by private investors [HY-06] |
| Pondage | Run-of-river with enough storage to shift flow within the day | Same energy, part moved into peak hours | Higher weir or small dam; may cross dam safety thresholds (O.7) |
| Storage | Reservoir stores wet-season water; its volume sets the peaking period [DE:S1] | Firm energy and capacity; less exposed to dry months | Large dam; resettlement; leakage in karst [DE:S1] |
| Pumped storage | Pumps off peak, generates at peak; cycle efficiency up to about 80 percent [DE:S1] | Price spreads and ancillary services such as inertia and frequency regulation [HY-06] | Two reservoirs; revenue depends on market design |
| Cascade | Several plants on one river | Flow and head depend on the other plants | Reservoir levels must not raise tailwater at the plant upstream; upstream storage changes downstream flow [DE:S1] |

Topography usually decides the type: a steep, narrow valley allows a short high dam to form a reservoir at modest cost, while flat terrain needs a long expensive dam [DE:S1]. Pumped storage holds over 90 percent of world electricity storage capacity, 160 GW in 2021 [HY-06].

## O.3 Layout components in water order

The two basic layouts are a powerhouse at the headworks or a diversion scheme with the powerhouse downstream to gain head; the choice optimises head against waterway length [DE:S1].

1. **Diversion weir or dam.** Raises water to the intake level and passes floods. A weir only holds the upstream level; it cannot store water [DE:S1]. Gated weirs hold a constant level; fixed overflow weirs do not [DE:S1].
2. **Spillway and bottom outlet.** The spillway passes surplus flow without damaging the dam; the bottom outlet lowers or empties the reservoir for maintenance or emergencies [DE:S1].
3. **Intake.** Screen, screen cleaner and gate, ideally on a straight reach with a stable bed [DE:S1]. Submergence of about three pipe diameters prevents vortices [DE:S1]. Intakes are usually the most maintenance-intensive component [DE:S1].
4. **Trash racks.** Approach velocity is typically 0.25 to 1.0 m/s [LIT:S6]; a blocked rack is a head loss and an outage risk.
5. **Desander (sand trap).** Directly downstream of the intake. Where head exceeds 100 m, particles larger than 0.2 mm must be retained; for lower heads 0.3 mm is acceptable, and hard angular minerals such as quartz call for a smaller cut size [DE:S1].
6. **Headrace canal or tunnel.** Canal velocity between 1.0 and 1.5 m/s, freeboard about 10 cm for lined and one third of water depth (minimum 15 cm) for unlined canals [DE:S1]. Tunnel velocity below 3 to 4 m/s to limit head loss [DE:S1].
7. **Forebay or surge tank.** A forebay holds enough water for start-up, prevents air entering the penstock and absorbs load-rejection surges [DE:S1]. A surge tank (simple, restricted orifice or differential) controls water hammer on pressurised systems [DE:S1].
8. **Penstock.** Designed for static head plus water hammer; held by anchor blocks at every change of direction or slope [DE:S1]. Steel suits high heads; prestressed concrete is limited to about 15 bar, equivalent to 150 m [DE:S1].
9. **Powerhouse, surface or underground.** The crane must lift the heaviest part; underground siting can reduce environmental impact [DE:S1]. Surface powerhouses on river terraces may need special foundation treatment such as jet grouting [LIT:S6].
10. **Tailrace.** Returns water to the river; its level sets the bottom of the usable head and, in a cascade, interacts with the next reservoir [DE:S1].

The value of a metre of head is a useful yardstick when the waterway is being optimised:

> P = ρ g Q H<sub>n</sub> η<sub>t</sub> η<sub>g</sub>

> ΔP per metre of head loss at rated flow = ρ g Q<sub>d</sub> η<sub>t</sub> η<sub>g</sub>

## O.4 Dams and weirs: types and selection drivers

The IFC guide gives the selection drivers in Table O.2 [DE:S1]. The ICOLD definition of a large dam is height above 15 m, or 5 to 15 m with reservoir storage above 3 million m3 [DE:S1]. ESHA cites ICOLD's "small" dam as no more than 15 m high, crest under 500 m and storage under 1 million m3 [LIT:S6].


**Table O.2. Dam types and selection drivers**
{: .cap}

| Type | Strengths | Limitations | Selection drivers |
|---|---|---|---|
| Concrete gravity | Crest spillway, powerhouse at the toe, tolerant of overtopping [LIT:S6] | Needs sound foundation; sliding, uplift and thermal cracking govern design [LIT:S6] | Narrow U-shaped valley; rock foundation; seismic zones (with embankments) [DE:S1] |
| Roller compacted concrete (RCC) | Continuous, highly mechanised placement and low unit cost [LIT:S6] | Needs aggregate and cementitious supply at scale | Same as gravity; most new large dams are RCC or CFRD [LIT:S6] |
| Arch or cupola | Structurally efficient, much less concrete [LIT:S6] | Narrow valley and strong abutment rock are essential [LIT:S6] | Narrow V-shaped valley [DE:S1] |
| Embankment (earth or rockfill, core) | Adapts to many foundations; local materials [LIT:S6]; clay cores suit seismic areas [DE:S1] | Sensitive to overtopping, leakage and internal erosion; higher failure rate than concrete dams [LIT:S6] | Wide valleys, plains, gravel, silt or clay foundations [DE:S1] |
| Concrete faced rockfill (CFRD) | Less sensitive to leakage and erosion; no core material needed [LIT:S6] | Needs rock quarry; face slab and plinth quality critical | Rockfill available, no suitable clay [LIT:S6] |

Materials must be available locally or at short haul distance [DE:S1], so a committee should see the quarry and borrow investigation, not only the dam drawings.

## O.5 Tunnels and underground works

Rock quality drives tunnel cost [DE:S1]. Tunnels can be unlined or lined with concrete or shotcrete; the choice and the rock condition set head loss and leakage [DE:S1]. An unlined tunnel needs a larger section for the same head loss [DE:S1], so it trades excavation for lining and is only sound where the rock is competent and the internal water pressure cannot jack open joints or leak into unstable slopes.

Drill and blast is the conventional method in hard rock; tunnel boring machines (TBMs) have raised efficiency and lowered cost [DE:S1]. The trade-off is flexibility against rate: drill and blast adapts support face by face, while a TBM is fast in the ground it was specified for and slow to recover in ground it was not. Two geological characteristics govern either method: lithological variation along the alignment and the structural stability of the rock mass, including major faults [LIT:S6]. ESHA's La Rienda tunnel crossed a thrust fault in "completely altered" rock without incident only because the fault was known beforehand [LIT:S6].

Unforeseen ground is a recurring source of dispute over what counts as "unforeseen": some standard forms let the contractor claim time and cost, others put all the risk on the contractor, and many contractors will not price that risk at an acceptable level [LIT:S7]. Prudent owners have tunnels dewatered and inspected within the EPC defects notification period (for example 24 months), with a major payment milestone or credit cover held until it expires [LIT:S7].

## O.6 Geological and geotechnical investigation stages

Without accurate rock and soil parameters, the design rests on unknown variables, "a significant source of risk" [DE:S1]. ESHA notes that the need for detailed geological study is "very often" underestimated, with seepage under weirs and canal slides as the consequence [LIT:S6]. Each stage should answer the question on which the next commitment depends.


**Table O.3. Investigation stages and what each should deliver**
{: .cap}

| Stage | Typical methods | Deliverable a lender should see |
|---|---|---|
| Site identification and pre-feasibility | National geological maps (indicative only), aerial photo interpretation, walkover [DE:S1; LIT:S6] | Geological reconnaissance report; fatal-flaw screen for faults, landslides, karst and dam foundation |
| Feasibility | Geological and geomorphological mapping at 1:10,000 to 1:5,000; geophysics (electrical or seismic refraction); test pits; boreholes at dam, intake, tunnel portals and powerhouse; permeability (Lugeon) and strength tests [LIT:S6; DE:S1] | Engineering geological model; rock mass classification along the waterway; foundation and seepage assessment; borrow and quarry assessment; seismic hazard input |
| Tender and detailed design | Additional boreholes on the final alignment, in situ tests at caverns and dam foundation | Geotechnical baseline report (GBR) forming part of the contract; design basis for support classes and grouting |
| Construction | Face mapping, probe drilling, monitoring | Comparison of encountered ground with the baseline; the basis for measuring ground-condition claims |

Neither IFC nor ESHA gives a required borehole quantity; the test is that every major structure and geological unit on the waterway is represented.

**Geotechnical baseline report.** The FIDIC Emerald Book (2019), produced with the tunnelling association ITA-AITES, makes the GBR "the sole source or contractual document that describes the anticipated subsurface conditions" [DE:S47]. The employer bears ground conditions worse than the baseline and benefits if ground is better, time for completion adjusts using the contractor's production rates, and payment varies with the ground [DE:S47]. Sophisticated hydropower developers use the same principle in EPC contracts: baseline ground data plus a cost-sharing formula outside it [LIT:S7]. The GBR turns open-ended geological risk into a measurable one; the residual exposure, baseline against plausible adverse ground, must be covered by contingency or sponsor support.

## O.7 Dam safety

Dams have been described as "the single man-made structures capable of causing most deaths", and small dams can also be dangerous: Sweden's only dam-failure fatality came from a dam under 4 m high [LIT:S6].

**Classification.** Most countries require owners to classify dams by hazard (low, significant, high), based on the consequence of failure [LIT:S6; DE:S1]. Classification sets the design flood. Typical criteria are the probable maximum flood, or alternatively the 10,000-year flood, as the maximum inflow design flood for high-hazard structures with a 1,000-year normal operation flood; 100 to 1,000 years for medium hazard; and typically 100 years for low hazard [LIT:S6]. The IFC guide's rough assessment is a design discharge near the 1,000-year flood [DE:S1].

**Independent review.** IFC Performance Standard 4 requires competent professionals to design and build structural elements to good international industry practice and, in high-risk situations, external experts to review the project through its stages [DE:S1]. The World Bank Good Practice Note on Dam Safety (2021) includes sample terms of reference for a panel of experts and technical notes on hydrological and seismic risk [HY-15; R4:S1]. A panel of experts should be appointed early, review investigation, design, construction and first filling, and report to lenders as well as to the owner.

**Instrumentation and surveillance.** Dam safety improves with monitoring systems, reviews and regular inspections [LIT:S6]. Instruments should measure what the design relies on: uplift and seepage (uplift is a design load [DE:S1]), deformation and settlement, and strong motion in seismic zones. First filling should follow a written plan.

**Emergency preparedness.** The ESIA and management plans should include emergency plans [DE:S1], built on a dam break and flood inundation study that maps downstream communities, warning times and evacuation routes, tested with local authorities before impoundment.

## O.8 River diversion during construction

Cofferdams are classified as dams built to divert a river [DE:S1]. Diversion works are temporary but govern the schedule: if overtopped, the excavation floods and the critical path stops. The exceedance risk over the construction period follows from the return period:

> P<sub>exceed</sub> = 1 − (1 − 1/T)<sup>n</sup>

where T is the return period in years and n the years of exposure. ESHA tabulates this relationship: a 100-year event has a 9.6 percent chance over 10 years [LIT:S6]. The design flood should be estimated from peak flows, not monthly means, and the diversion plan should state who bears the cost of a flood above the design event: the contractor (and its insurers) or the owner.

## O.9 Civil works dominate cost and overrun risk

In Fichtner's benchmark for the IFC guide, civil works ranged from 33.2 to 76.5 percent of total plant cost, median 55.2 percent, with the middle half between 47 and 61 percent; dam schemes sit at the high end [DE:S1]. Because each project is one-off and exposed to geology, natural hazards and weather, these costs are "unpredictable and high-risk" [DE:S1].

Contingencies in the benchmark averaged 9.1 percent of total plant cost (median 9.8 percent), while industry practice is 15 percent for civil works and 7.5 to 10 percent for electromechanical equipment and grid connection [DE:S1]. The guide adds that final soil investigations have often not been done at feasibility stage, and that cost risk is "even higher if a tunnel must be built" [DE:S1]. ESMAP survey respondents ranked geotechnical and seismic risk as the most significant technical risk for large hydropower [HY-06].

The reference class for large dams is sobering: across 245 dams, real cost overrun had a median of 27 percent and a mean of 96 percent, and schedule overrun a median of 27 percent and a mean of 44 percent [HY-08]. The distribution is right-skewed. Applied to a run-of-river civil package it is a stress test, not a forecast.

Civil estimates should rest on bills of quantities benchmarked to national unit rates and checked by an independent engineer with local experience [DE:S1].

## O.10 Site access and logistics

Site selection must check whether access roads exist, need upgrading or must be built [DE:S1]. Access roads through difficult terrain can be a "deal breaker" because of cost [DE:S1], and benchmark cost outliers come from sites without infrastructure [DE:S1]. The IFC guide lists access roads, penstock construction, tunnelling, E&M manufacturing and grid connection as critical path items [DE:S1]. DFIs can support governments by financing project transmission lines [HY-06]; access roads need the same early funding.

Logistics questions that move cost: the heaviest transport load against bridge ratings; wet-season reliability of cement, steel and fuel routes; and quarry haul distance.

## O.11 Kasiri worked example

Case facts: 60 MW run-of-river, net rated head 120 m, design flow 57 m3/s, environmental flow 4 m3/s, turbine efficiency 0.92, generator and transformer efficiency 0.98, P50 about 292 GWh/yr, civil works USD 68m within a plant cost of about USD 157m, contingency 10 percent, 3-year construction. The layout (a diversion weir, desander, headrace tunnel, surge tank, surface penstock and surface powerhouse) is an **illustrative assumption**, not a case fact.

Power check: 1,000 × 9.81 × 57 × 120 × 0.92 × 0.98 ≈ 60.5 MW, consistent with 60 MW. Each metre of head lost at rated flow costs 1,000 × 9.81 × 57 × 0.92 × 0.98 ≈ 0.50 MW. Scaling P50 linearly with head gives about 292 / 120 ≈ 2.4 GWh/yr per metre; this is an upper bound because friction loss falls with the square of flow at part load.


**Table O.4. Kasiri illustrative sizing from sourced rules of thumb**
{: .cap}

| Item | Rule | Source | Kasiri result (illustrative) |
|---|---|---|---|
| Desander cut size | Head above 100 m: retain particles above 0.2 mm | [DE:S1] | 0.2 mm, smaller if sediment is quartz-rich |
| Trash rack gross area | Approach velocity 0.25 to 1.0 m/s | [LIT:S6] | 57 / 1.0 to 57 / 0.25 = 57 to 228 m2 before bar blockage factor |
| Headrace tunnel | Velocity below 3 to 4 m/s | [DE:S1] | Area 14.3 to 19.0 m2; circular equivalent diameter about 4.3 to 4.9 m |
| Headrace canal, if chosen | Velocity 1.0 to 1.5 m/s | [DE:S1] | Wetted area 38 to 57 m2 |
| Penstock material | Prestressed concrete limited to about 15 bar (150 m) | [DE:S1] | Static head above 120 m plus a water hammer allowance of 25 to 50% for reaction turbines [LIT:S6] exceeds 150 m; steel is the expected choice |

Pondage (illustrative): in February the mean flow is 20 m3/s, leaving 16 m3/s after the environmental flow. Running at 57 m3/s for 4 peak hours requires (57 − 16) × 14,400 s ≈ 0.59 million m3 of live storage. That is below the 1 million m3 in ESHA's small-dam definition [LIT:S6], but a weir high enough to hold it could still exceed 15 m or need dam safety classification. Pondage pays only if the PPA rewards peak delivery, which the case does not define.

River diversion: monthly flows (20 m3/s in February, 22 m3/s in September, 70 m3/s in May) give two dry windows a year for riverbed works. Over the 3-year build, the chance that the diversion design flood is exceeded at least once is about 27 percent for a 10-year flood, 14 percent for a 20-year flood, 6 percent for a 50-year flood and 3 percent for a 100-year flood. Kasiri's 12-year record is shorter than the 15 years the IFC guide expects for hydrology [DE:S1], so flood peaks for these return periods carry wide uncertainty and should be checked by regional analysis.

Cost: civil works of USD 68m are 43 percent of the USD 157m plant cost and 54 percent of the USD 127m sum of the six base cost lines, close to the benchmark median of 55.2 percent [DE:S1]. The model's plant cost adds to those lines USD 9.0m of development costs reimbursed at close and a USD 6.6m contractor's risk premium, giving a subtotal of USD 142.6m, and then a 10 percent contingency of USD 14.3m. That contingency is close to what industry practice would give on the works alone (15 percent on civil, 7.5 to 10 percent on the USD 42m of equipment: USD 13.4m to 14.4m) [DE:S1], but only because it is also charged on development costs and the premium, which carry no physical risk. Charged on the six base lines alone, 10 percent would be USD 12.7m, below that practice range, and below what a scheme with a tunnel warrants. A civil overrun at the large-dam median of 27 percent [HY-08] adds USD 18.4m; at the mean of 96 percent, USD 65.3m. With the illustrative tunnel, the gap between contingency and the median stress case should be covered by GBR risk sharing, sponsor support or a standby facility.

## O.12 Component risks and the evidence lenders ask for


**Table O.5. Component, typical risk and lender evidence**
{: .cap}

| Component | Typical risk | Evidence a lender asks for |
|---|---|---|
| Weir or dam | Foundation seepage and undermining; sliding; overtopping | Foundation boreholes and permeability tests; stability for all load cases [DE:S1]; hazard class |
| Spillway and bottom outlet | Undersized for floods; gate failure | Flood study matched to hazard class [LIT:S6]; gate reliability |
| Intake and trash racks | Blockage, vortices, sediment entry | Siting and submergence check [DE:S1]; rack cleaning |
| Desander | Turbine abrasion; flushing failure | Sediment sampling and mineralogy; settling design [DE:S1] |
| Headrace canal | Leakage triggering slope failure | Slope stability, drainage and lining design [LIT:S6] |
| Headrace tunnel | Adverse ground, faults, water inflow, collapse; lining leakage | Geological long section; rock mass classes; GBR and risk sharing [DE:S47; LIT:S7]; dewatering inspection [LIT:S7] |
| Forebay or surge tank | Air entrainment; water hammer; foundation load | Load rejection transient analysis |
| Penstock | Rupture under water hammer; anchor block movement on slopes | Pressure class including surge; anchor geotechnics [DE:S1] |
| Powerhouse | Foundation settlement; flooding; cavern stability if underground | Foundation investigation; flood levels; cavern support |
| Tailrace | Backwater from floods or downstream reservoir | Tailwater rating curve; cascade operating rules [DE:S1] |
| Diversion works | Overtopping during construction | Exceedance probability; risk allocation |
| Access and logistics | Delay on the critical path; heavy load transport | Route survey; wet-season plan [DE:S1] |

## O.13 Decision tests

1. Does the scheme type match the revenue contract: if the PPA pays for peak or firm capacity, is there storage to deliver it, and if not, is the tariff energy-only?
2. Has the waterway been optimised on lifecycle value, with the energy cost of each metre of head loss (about 2.4 GWh/yr per metre at Kasiri as an upper bound) priced against excavation and lining cost?
3. Is the dam type supported by foundation boreholes and by an investigated quarry or borrow source within short haul distance?
4. Does every major structure and every geological unit along the waterway have site-specific investigation, or are parts of the design still based on regional maps?
5. Is there a GBR in the civil contract, who bears ground worse than the baseline, and is the employer's share covered by contingency or committed sponsor funding?
6. What hazard class has the dam or weir been given, which design and check floods follow from it, and were they estimated from peak-flow data rather than monthly means?
7. Has an independent panel reviewed design and construction, will it review first filling, and are a dam break study, emergency plan and instrumentation plan in place?
8. What is the probability that the diversion design flood is exceeded during construction, and who pays if it is?
9. Is the civil contingency at least the 15 percent industry norm, and does the sources and uses survive a civil overrun at the 27 percent median of the large-dam reference class?
10. Are access roads, heavy load routes and the grid connection on the critical path funded and permitted before notice to proceed?
11. Will tunnels be dewatered and inspected before the EPC defects notification period ends, with retention or credit cover still in place?

# Annex P. Electromechanical equipment and grid connection

## P.1 Purpose and scope

The electromechanical (E&M) package turns head and flow into saleable energy: turbines, generators, governors and excitation, transformers, switchyard, protection, SCADA, auxiliaries, and the hydromechanical gates and valves that control water to the units. Each large plant's E&M equipment is custom-designed [DE:S1]. In the IFC benchmark sample E&M averages 30.3% of total plant cost (median 29.2%), with a range of 14.9 to 56.6% [DE:S1]. The decisions a committee must test are few: turbine type, number and speed of units, turbine setting, sediment protection, and the contract and test regime that makes supplier guarantees enforceable.

## P.2 Turbine types and selection by head and flow

Turbine choice rests on the site's head and flow, including how often the turbine will run at part load because available flow is below design discharge [DE:S1]. Turbines divide into two families [DE:S1]:

- **Impulse** (Pelton, Turgo, cross-flow): the runner turns in air under one or more jets. They hold efficiency under fluctuating flow, avoid penstock overpressure, control overspeed easily and are easy to maintain.
- **Reaction** (Francis, propeller, Kaplan, bulb): the runner is immersed in a pressure casing and driven by lift; a draft tube recovers head below the runner. Runners are smaller and faster than Peltons, can run submerged, and give higher efficiency at higher power.

The IFC guide classes schemes as high head above 100 m, medium head 30 to 100 m and low head below 30 m [DE:S1]. Its turbine section uses a different low-head limit (below 10 m) and misprints the medium range ("50 m < H < 10 m"), so quote the scheme classes [DE:S1]. The guide's head-flow chart (Figure 4-19, on log axes of 1 to 1000 m head and 1 to 1000 m<sup>3</sup>/s flow) places, as far as it can be read, Pelton and Turgo at high head and low flow, Kaplan at low head and high flow, cross-flow at low to medium head and small flow, and Francis across the wide middle field; the boundaries depend on each manufacturer's design [DE:S1].


**Table P.1. Turbine types: principle, application and part-load features**
{: .cap}

| Type | Principle | Application as stated in the sources | Features relevant to a committee |
|---|---|---|---|
| Pelton | Impulse; double-spoon buckets, one or more nozzles with needle valves | High head, low flow; most widely used impulse turbine [DE:S1] | Up to 2 nozzles (horizontal) or 6 (vertical); deflector limits overspeed on load rejection [DE:S1] |
| Turgo | Impulse; jet strikes runner plane at about 20 degrees | Pelton field, higher flow per runner [DE:S1] | Smaller runner than a Pelton for the same power [DE:S1] |
| Cross-flow (Banki-Michell) | Impulse; drum rotor, water crosses runner twice | Low to medium head, small flow (as read from the IFC chart) [DE:S1] | Gross head counts only 2/3 of runner-to-tailwater drop [DE:S1] |
| Francis | Reaction; radial inflow, axial outflow, spiral case with guide vanes | Most common turbine in use; broad middle field of head and flow [DE:S1] | Efficiency falls sharply below about half design flow [DE:S1] |
| Propeller (fixed blade) | Reaction; axial flow, 3 to 6 blades | Low head [DE:S1] | Minimum technical flow 75% of design [LIT:S6] |
| Kaplan | Propeller with adjustable blades and guide vanes (double regulated) | Low head, variable flow [DE:S1] | Higher cost, high efficiency over a wide flow range [DE:S1] |
| Bulb | Horizontal Kaplan with generator in a watertight bulb | Heads up to 30 m, high output [DE:S1] | Smaller excavation than vertical Kaplan [DE:S1] |

Low-head bulb and Kaplan plants use low-speed generators; high-head Francis and Pelton plants use high-speed ones [DE:S1].

## P.3 Specific speed

Specific speed condenses head, flow (or power) and rotational speed into one number that characterises runner shape: low for Pelton, intermediate for Francis, high for propeller and Kaplan. A propeller runs faster than a Francis for the same head and flow, which is why it superseded the low-head Francis [DE:S1]. ESHA makes specific speed its main selection criterion [LIT:S6], but none of the source texts available here gives numerical bands by turbine type, so the annex gives definitions only; the engineer should show the manufacturer's experience chart behind any proposed speed.

Three forms are in common use (n in rpm, Q in m<sup>3</sup>/s per unit, H net head in m, P shaft power per unit):

> n<sub>s</sub> = n × P<sup>0.5</sup> / H<sup>1.25</sup> (P in kW; metric power-based form)

> n<sub>q</sub> = n × Q<sup>0.5</sup> / H<sup>0.75</sup> (flow-based form)

> n<sub>QE</sub> = (n / 60) × Q<sup>0.5</sup> / (g × H)<sup>0.75</sup> (dimensionless form)

The rotational speed of a synchronous unit is fixed by grid frequency f and the number of pole pairs p:

> n = 60 × f / p

Speed therefore comes in discrete steps. At fixed specific speed, speed rises as unit size falls; a higher specific speed shrinks the generator but needs a deeper setting against cavitation (P.6).

## P.4 Efficiency and part-load behaviour

Turbine selection must compare efficiency across the whole flow range, not only at the design point [DE:S1]. Pelton and Kaplan turbines keep high efficiency below design flow; cross-flow and Francis efficiency drops more sharply below half flow, which suits them to steady flows [DE:S1]. Below a minimum flow the unit must stop to avoid damage from heavy vibration [DE:S1]. The two sources state different minimum flows, and the difference matters for low-flow months.


**Table P.2. Minimum technical flow by turbine type, % of design flow**
{: .cap}

| Turbine | IFC guide [DE:S1] | ESHA guide [LIT:S6] |
|---|---|---|
| Pelton | 10 to 20 (depends on number of nozzles) | 10 |
| Turgo | not stated | 20 |
| Francis | 40 | 50 |
| Kaplan (double regulated) | 20 | 15 |
| Semi-Kaplan (single regulated) | 40 | 30 |
| Propeller (fixed) | not stated | 75 |

*Note: IFC gives Kaplan as 20 to 40% for double and semi regulated machines respectively.*

The energy estimate should apply the efficiency curve strip by strip over the flow duration curve, ending at the larger of minimum technical flow and reserved flow [LIT:S6]. Net head is lowest at maximum discharge, because losses rise with velocity squared and tailwater rises with flow [DE:S1], so a rated net head must be stated with its flow.

Variable-speed generation reduces efficiency variability off nominal head or flow and reduces abrasion [DE:S1].

## P.5 Number and size of units

The unit count trades three things:

1. **Low-flow operation.** The IFC guide's own example: instead of one 60 MW Francis unit, two 30 MW units allow operation down to 20% of plant design discharge instead of 40% [DE:S1]. Each scheme needs an assessment of whether the extra energy pays for the extra cost [DE:S1].
2. **Availability.** With one unit, every unit outage is a plant outage. Major overhauls recur every 7 to 12 years and take 4 to 6 weeks for units above 20 MW [DE:S1]; with several units they can fall in low-flow months.
3. **Cost.** More units mean more turbines, generators, valves, controls and powerhouse length; in the IFC optimisation example, IRR moves in steps with turbine unit costs [DE:S1]. Identical units share spares and need performance tests on one unit only [DE:S1].

The powerhouse crane is sized for the heaviest lift, a generator part or the runner [DE:S1], so fewer, larger units also raise crane and transport loads.

## P.6 Cavitation and turbine setting

Cavitation occurs where pressure falls below vapour pressure; the vapour cavities collapse in higher-pressure zones and can be extremely damaging [LIT:S6]. In a reaction turbine the tailwater level governs its onset [LIT:S6]. Cavitation and erosion damage runners and cut efficiency; the O&M response is inspection and in-situ weld repair [DE:S1].

The setting (elevation of the runner relative to the minimum tailwater) is governed by the plant cavitation coefficient (Thoma sigma):

> σ<sub>plant</sub> = (H<sub>atm</sub> − H<sub>v</sub> − H<sub>s</sub>) / H

where H<sub>atm</sub> is atmospheric pressure head (falling with altitude), H<sub>v</sub> vapour pressure head, H<sub>s</sub> suction head (runner above tailwater positive) and H net head. The setting must satisfy σ<sub>plant</sub> above the turbine's critical sigma with a margin set by the manufacturer from model tests. The sources do not give sigma values by specific speed, so the annex quotes none. The arithmetic is still useful: at 120 m net head, each 0.01 of sigma is 1.2 m of setting depth, so a change of runner speed or a lower minimum tailwater can move the powerhouse floor by metres and change civil cost.

## P.7 Sediment abrasion and coatings

In medium- and high-head plants, suspended sediment wears hydraulic steel structures and turbines, reducing efficiency and life [DE:S1]. The higher the head, the smaller the particle that must be removed: above 100 m head, all particles larger than 0.2 mm should be retained in the sand trap; 0.3 mm is acceptable at lower heads; hard (quartz) and angular particles justify a smaller limit [DE:S1]. ESHA expresses the abrasive power of grains on a Francis runner as:

> P<sub>e</sub> = μ × V<sub>g</sub> × ((ρ<sub>s</sub> − ρ<sub>w</sub>) / R) × v<sup>3</sup>

with μ a friction coefficient, V<sub>g</sub> grain volume, ρ<sub>s</sub> and ρ<sub>w</sub> grain and water densities, R blade radius and v grain velocity [LIT:S6]. Because grain velocity scales with head, abrasion rises steeply with head. ESHA reports Francis repair intervals of about 6 to 7 years with a sand trap retaining 0.2 mm, 3 to 4 years at 0.3 mm and 1 to 2 years at 0.5 mm, and finds the economic optimum near 0.2 mm in severe conditions (high head, quartz) and 0.3 mm in normal conditions [LIT:S6].

Mitigations are an efficient desander, hard ceramic coatings [DE:S1], variable speed [DE:S1] and, on silty rivers, silt monitoring to plan repairs [DE:S1]. The sources do not quantify coating life or cost.

## P.8 Generators, excitation and governors

Large and medium units usually have vertical shafts; small units horizontal [DE:S1]. Excitation is brushless or with brushes [DE:S1]. **Synchronous generators** have DC or permanent-magnet excitation and a voltage regulator; their excitation is independent of the grid, so they can operate islanded and control voltage [DE:S1]. **Asynchronous generators** cannot regulate voltage, run at a speed tied to grid frequency and cannot produce power when isolated because their excitation comes from the grid [DE:S1]. For a 60 MW grid plant expected to support voltage, synchronous machines are the normal choice. Generator efficiency rises with rating, approaching 98% above 1 MW [DE:S1].

The governor moves guide vanes or needles to hold speed and load; modern practice is digital PID governors [DE:S1]. Closure time and the waterway interact: normal water hammer under governor shutdown can raise penstock pressure by 25 to 50% of gross head for reaction turbines, depending on governor time constants [LIT:S6]. ESHA's water acceleration time t<sub>h</sub> tests whether the waterway is governable:

> t<sub>h</sub> = V × L / (g × H)

If t<sub>h</sub> is below 3 s a surge tower is unnecessary; above 6 s a surge tower or other device is needed to avoid strong oscillation in the turbine controller, and a badly designed governor can interact with surge-tank oscillation [LIT:S6]. Where valves must close fast, a relief valve in parallel with the turbine slows flow changes in the penstock [LIT:S6].

## P.9 Transformers, switchyard, protection, SCADA and auxiliaries

Step-up transformers raise voltage to cut line losses [DE:S1]. The switchyard should sit close to the powerhouse, above design tailwater (for example the 100-year flood level), sized by the number and direction of outgoing lines [DE:S1]. Transformer upkeep relies on oil and winding temperature monitoring, dissolved gas analysis and tan delta tests [DE:S1]. Protection receives primary and secondary injection testing, and generator relays are function-tested on no-load runs [DE:S1]. Software-based control and SCADA allow remote diagnostics where permanent supplier presence is uneconomic [DE:S1]. Auxiliaries comprise drainage and dewatering pumps, cooling, compressed air, ventilation, AC and DC supplies and the emergency diesel [DE:S1].


**Table P.3. Expected useful life of E&M components [DE:S1]**
{: .cap}

| Component | Life (years) |
|---|---|
| Turbine (excluding runner), generator, governor, excitation, main inlet valves | 40 |
| Turbine runners | 10 |
| Power transformers; HV switchgear and switchyard | 40 |
| MV and LV switchgear | 30 |
| Control, protection, SCADA, communications, metering | 20 |
| Auxiliary mechanical and electrical equipment | 30 |
| Penstocks, gates, stoplogs, trash racks; transmission lines | 70 |

*Note: averages; actual life depends on water quality, sediment load, climate and number of starts and stops [DE:S1].*

## P.10 Hydromechanical equipment

Hydraulic steel structures are classed by purpose [DE:S1]: service gates regulate flow or level (spillway, bottom outlet); emergency gates are only fully open or shut (intake, draft tube, upstream of penstock valves); maintenance gates, usually stoplogs, dewater conduits; guide vanes or needles regulate turbine flow; trash racks protect intakes. Gate type depends on purpose, opening size, climate and operation [DE:S1]. Commissioning checks gate speeds, leakage of closed gates and emergency valves, and inlet valve timing [DE:S1].

## P.11 Grid connection and grid code

Grid connection cost is driven mainly by distance to the grid [DE:S1]. Industry contingency practice is 7.5 to 10% for grid connection and E&M, against 15% for civil works [DE:S1]. Missing transmission and grid upgrades are a key barrier to commercial operation, producing large deemed-energy claims on offtakers [HY-06], and commissioning needs early coordination with the grid operator [DE:S1].

The sources quote no grid code numbers (frequency and voltage ranges, fault ride-through, reserve). Its test content is visible in the commissioning list: synchronisation, reactive capability test, power system stabiliser test, V-curve, load rejection at 25, 50, 75, 100 and 110% of design load, and joint active and reactive power sharing for multi-unit plants, with results compared against the supply contract and the PPA [DE:S1]. The committee should obtain the national grid code and map each clause to an equipment specification item and a test.

## P.12 Supply contracts, factory and site testing

Developers often split civil, E&M and grid contracts; lenders generally prefer a turnkey EPC, which costs more because risk moves to the contractor [DE:S1]. Split packages typically use FIDIC Yellow Book for E&M and Red Book for civil works, and only a handful of turbine suppliers compete [LIT:S7]. E&M payments are typically 30% advance, 50% on delivery, 20% on acceptance [DE:S1], and E&M manufacturing sits on the critical path [DE:S1]. Supplier warranties often outlast the EPC defects period (for example 24 months); the owner should capture them by assignment or collateral warranty [LIT:S7].

Future O&M staff should attend shop assembly and testing [DE:S1]. Site tests run dry (alignment, bearing clearances, gate and valve timing, winding insulation and withstand, governor logic), no-load (overspeed, vibration, excitation) and on load [DE:S1]. For units above 5 MW, an IEC 60041 field acceptance test and an index test verify turbine efficiency on at least one unit, and generator losses are measured on at least one generator [DE:S1]. Large projects commonly run a 30-day trial per unit; a defect forces a restart [DE:S1]. Spares stock is about 2.5 to 3.0% of FOB equipment price, and the annual E&M maintenance budget about 2.0 to 2.5% of initial investment, of which about 60% is a reserve for the 7 to 12 year major overhauls [DE:S1]. First-year availability is about 95%, improving to 97 to 98% after three years [DE:S1].

## P.13 Kasiri worked example

**Power check.** With the case values:

> P = ρ × g × Q × H × η = 1,000 × 9.81 × 57 × 120 × 0.92 × 0.98 = 60.5 MW

Hydraulic power is 67.1 MW, shaft power 61.7 MW and output 60.5 MW, so the 60 MW rating is consistent. Two comments. First, 0.92 is a design-point efficiency; at part load the Francis curve falls (P.4), so the energy model needs a curve, not a constant. Second, 0.98 for generator and transformer combined is optimistic: IFC puts generator efficiency alone at up to about 98% above 1 MW [DE:S1], and transformer losses come on top. The P50 of about 292 GWh over 60 MW × 8,760 h gives the case capacity factor of 55.6% (Table N.2).

**Turbine type.** At 120 m net head and 57 m<sup>3</sup>/s (19 to 57 m<sup>3</sup>/s per unit), Kasiri sits in the high-head class (above 100 m) and in the Francis field of the IFC head-flow chart, well above the bulb ceiling of 30 m and at flows beyond the Pelton field [DE:S1]. The design ratio Q<sub>d</sub>/Q<sub>av</sub> = 57/38 = 1.5 is at the top of the 1.0 to 1.5 range for run-of-river, and the 56% capacity factor lies within the 40 to 70% run-of-river range [DE:S1].

**Specific speed.** The case sets two units (Chapter 3). The one- and three-unit rows, the grid frequency (50 Hz) and the speeds below are illustrative assumptions, used to show why two units were chosen.


**Table P.4. Illustrative Kasiri unit configurations (H = 120 m, η<sub>t</sub> = 0.92, 50 Hz)**
{: .cap}

| Units | Q per unit (m<sup>3</sup>/s) | Shaft power per unit (MW) | Speed (rpm) | Pole pairs | n<sub>s</sub> (kW) | n<sub>q</sub> | n<sub>QE</sub> |
|---|---|---|---|---|---|---|---|
| 1 | 57.0 | 61.7 | 214.3 | 14 | 134 | 44.6 | 0.134 |
| 2 | 28.5 | 30.9 | 300.0 | 10 | 133 | 44.2 | 0.133 |
| 2 | 28.5 | 30.9 | 333.3 | 9 | 147 | 49.1 | 0.148 |
| 3 | 19.0 | 20.6 | 375.0 | 8 | 135 | 45.1 | 0.136 |
| 3 | 19.0 | 20.6 | 428.6 | 7 | 155 | 51.5 | 0.155 |

*Note: H<sup>1.25</sup> = 397.2; H<sup>0.75</sup> = 36.3; (gH)<sup>0.75</sup> = 201.0. Speeds are synchronous steps n = 3000/p.*

Holding specific speed near 134, moving from one to three units raises speed from 214 to 375 rpm and shrinks each generator; the next speed step raises specific speed by 11 to 15%, saving generator cost but needing a deeper setting. The supplier must confirm the choice against its reference list and model tests.

**Low-flow operation.** Available turbine flow is river flow less the 4 m<sup>3</sup>/s environmental flow, capped at 57 m<sup>3</sup>/s.


**Table P.5. Months below minimum technical flow, Kasiri monthly means (illustrative unit counts)**
{: .cap}

| Configuration | Unit design flow (m<sup>3</sup>/s) | Minimum flow, IFC 40% (m<sup>3</sup>/s) | Months below (IFC) | Minimum flow, ESHA 50% (m<sup>3</sup>/s) | Months below (ESHA) |
|---|---|---|---|---|---|
| 1 × Francis | 57.0 | 22.8 | Jan, Feb, Sep | 28.5 | Jan, Feb, Mar, Aug, Sep, Oct |
| 2 × Francis | 28.5 | 11.4 | none | 14.3 | none |
| 3 × Francis | 19.0 | 7.6 | none | 9.5 | none |

*Note: available flows Jan to Dec are 20, 16, 24, 48, 57, 54, 36, 24, 18, 26, 42, 32 m<sup>3</sup>/s. Monthly means hide daily lows, so the daily flow duration curve must confirm the result.*

A single unit would stop for three to six months of an average year, inconsistent with a 56% capacity factor. Two units remove the problem on monthly means and allow overhauls in February or September; three add dry-year margin (energy CV 0.15) at extra cost. Two units is the natural base case to test.

**Sediment and cost.** At 120 m head the sand trap should retain particles above 0.2 mm [DE:S1], and quartz content must be known before runner coating is specified. E&M at USD 33m is 26% of the USD 127m of listed base components (33% with hydromechanical), within IFC's 14.9 to 56.6% range [DE:S1], or about USD 550 per kW. The 0.95 availability matches IFC's first-year figure and is conservative against the 97 to 98% expected after year three [DE:S1].

## P.14 Decision tests

1. Does the feasibility study show the head-flow point on a selection chart and justify the turbine type against the full flow duration curve, not only the design point?
2. Is the rated net head stated at rated flow, with the head loss and tailwater rating curve used to compute it?
3. What efficiency curve (by supplier or reference machine) underlies the energy estimate, and is part-load efficiency applied strip by strip?
4. Which minimum technical flow (IFC 40% or ESHA 50% for Francis) is assumed, and how many days per average and dry year would each unit configuration stop?
5. What unit count and speed are proposed, and does the optimisation show the incremental cost of each extra unit against the energy and availability gained?
6. What setting below minimum tailwater is proposed, what sigma margin does it assume, and has the supplier confirmed it from model tests?
7. What are the measured sediment concentration, grain size and quartz content, what particle size will the desander retain, and what runner coating and repair interval are assumed in OPEX?
8. Does the governor and waterway analysis show the water acceleration time and pressure rise on load rejection within penstock design limits?
9. Has the grid operator issued a connection offer for the 132 kV line, and is each grid code clause mapped to an equipment specification and a commissioning test?
10. Who bears deemed-energy risk if the line or grid upgrades are late?
11. Do the E&M contract guarantees (output, efficiency, pressure rise, speed rise) carry liquidated damages, and are they verified by an IEC 60041 field test?
12. Are extended manufacturer warranties assigned to the owner, and are spares (2.5 to 3.0% of FOB price) and the major overhaul reserve in the budget?

# Annex Q. Construction, commissioning, operation and maintenance

## Q.1 Purpose and scope

Hydropower value is won or lost in two windows: construction, when the plant only consumes capital, and the first decade of operation, when learning-curve outages, warranty claims and the first major overhaul occur. No revenue flows before commissioning, so a shorter construction period shortens payback [DE:S1]. This annex gives a committee the benchmarks needed to test a contractor's programme, a commissioning plan and an O&M budget. Where the sources give no number, it states the method.

## Q.2 Construction planning and the critical path

Construction starts before the first concrete is poured. Hydro sites are often remote, access can be difficult, and weather can stop work in rainy seasons, so access roads, offices and worker accommodation must be built before work on the scheme itself begins [DE:S1]. The schedule should show durations, contingency per task, milestones, interdependencies, responsibilities, the critical path and progress against plan, broken down by lot: access; dam and diversion; headrace and penstock; powerhouse; electromechanical (E&M) manufacture, transport and installation; switchyard and grid connection; commissioning [DE:S1].

The typical critical path given by the IFC guide runs through access roads, penstock construction, tunnelling, E&M equipment manufacturing and connection to the grid, although critical items vary by project [DE:S1]. E&M installation can only follow completion of powerhouse civil works, and long-lead items must be ordered in time, though equipment that arrives too early must be stored on site at added risk [DE:S1]. River diversion is the hinge between these chains: the dam and powerhouse foundations cannot be built in the dry until the river has been diverted, and on run-of-river projects dry commissioning tests must be completed before the construction pit is flooded and the cofferdams removed (Q.6) [DE:S1]. A programme that shows diversion slipping past a dry season, without showing the knock-on to the next low-flow window, is incomplete.

Missing transmission lines and grid upgrades are often a key barrier to reaching COD, leading to deemed energy claims that burden offtakers [HY-06].


**Table Q.1. Schedule benchmarks from the sources**
{: .cap}

| Item | Benchmark | Source |
|---|---|---|
| Detailed design | A few months (small HPP); more than a year (large HPP) | [DE:S1] |
| Tendering and procuring EPC contractors, medium and large HPP | Up to 18 months; up to two years for a BOO tender | [DE:S1] |
| Construction, small HPP | 9 to 18 months | [DE:S1] |
| Construction, medium and large HPP | Up to four years | [DE:S1] |
| Observed: Nyamwamba II, 7.8 MW, Uganda | About 29 months, construction start to COD | [DE:S12] |
| Observed: Nachtigal, 420 MW, Cameroon | Five-year construction period | [DE:S13] |
| Large hydro, initiation to COD | Typically 8 to 10 years or more | [HY-06] |
| Schedule overrun, large dams reference class | Median 27%, mean 44% of planned period | [HY-08] |
| Commissioning, one test phase | About one month each; less for small HPP | [DE:S1] |
| Commissioning, two 150 MW units (E&M plant) | About seven months in the IFC example schedule | [DE:S1] |

*Note: The HY-08 overrun data refer to large dams (245 projects in 65 countries) and are a reference class, not an Africa-specific or run-of-river distribution.*

Payment profile is part of planning. The IFC guide gives a typical EPC payment schedule: civil works 10% advance, 80% against milestones and 10% on handover; E&M 30% advance, 50% on delivery of equipment and 20% on acceptance [DE:S1]. Contractors tend to load cost into delivery items, so the commissioning line in a price schedule does not represent actual commissioning cost [DE:S1].

## Q.3 Construction methods and their risks

Civil works are 50% or more of project cost and the least predictable block, driven by geology, natural hazards and weather [DE:S1]. Stakeholders rank geotechnical and seismic conditions as the top technical risk [HY-06].

Underground works. Drill and blast is conventional in hard rock; tunnel boring machines (TBMs) raise efficiency and install support as they advance [DE:S1]. Poor rock entails large costs, so an experienced geologist should assess tunnel risk individually [DE:S1]. ESHA documents a tunnel under heterogeneous colluvium where TBMs were not feasible and excavation proceeded metre by metre with small charges and grouting, and a fault zone that needed an entirely different support system; lithology along the alignment decides the method, and major faults must be known in advance [LIT:S6].

Surface works and first filling. ESHA records a canal on weathered sandstone where first filling saturated the slope and a landslide broke the reservoir embankment [LIT:S6]. First filling is a construction risk, not an operating event.

Risk allocation for ground conditions. "Unforeseen conditions" clauses breed disputes, and full transfer of ground risk is often refused or priced high; experienced developers agree a geotechnical baseline with a cost-sharing formula outside it [LIT:S7]. Turnkey EPC passes most risk but is expensive and few contractors can do everything, so many owners split the work into an E&M contract with a turbine supplier, a civil contract (often with local contractors where local content rules apply) and a transmission contract [LIT:S7]. FIDIC is the market standard: Silver Book for turnkey EPC, Yellow Book for E&M and transmission, Red Book for civil works [LIT:S7; DE:S1]. Splitting lots moves interface risk to the owner, and the IFC guide calls interface management a demanding task requiring highly experienced engineering [DE:S1].

Contingency. Estimates in the IFC sample average 9.1% of total plant cost, while industry practice is 15% on civil works, 7.5% to 10% on E&M and 7.5% to 10% on grid connection [DE:S1]. Real cost overruns on large dams have a median of 27% and a mean of 96% [HY-08].

## Q.4 Quality assurance, supervision and lender monitoring

Three parties check the contractor.

- The owner's engineer supervises the EPC contractor on the owner's behalf and, under split-lot procurement, manages the interfaces between lots and specifies them in the detailed design [DE:S1]. Under the FIDIC Silver Book there is no independent "Engineer" in the contract, so the employer carries the engineering role itself [DE:S1].
- The lenders' technical adviser (independent engineer) reviews the feasibility study and draft contracts during due diligence, then monitors construction for lenders [DE:S1]. Monitoring uses progress reports and site visits, with quarterly reviews; lenders may also hire an independent engineer for commissioning [DE:S1].
- The commissioning engineer receives, before any commissioning test, all quality certificates, test procedures and installation test results [DE:S1].

Construction and installation quality is a key technical risk: plants are one-off designs and terminating an underperforming contractor is expensive and slow, so contractor due diligence, full specifications, performance guarantees and adequate supervision are needed [HY-06]. The IFC guide adds that design must conform to national standards and, where these are silent, to USACE manuals and ICOLD bulletins [DE:S1].

A useful monitoring report (recommended format, not a source requirement) shows float on the critical path, cost to complete and contingency drawn, ground encountered against the baseline, open non-conformances, safety and E&S performance, and long-lead equipment status.

## Q.5 Health, safety and construction-phase E&S

The IFC guide requires that human health and safety be considered at all times during construction and flags worker health and safety as a specific issue where tunnelling is involved, together with noise, dust and vibration [DE:S1]. Under the Equator Principles, projects in non-designated countries, which include all of sub-Saharan Africa, are assessed against the IFC Performance Standards and the World Bank Group EHS Guidelines [DE:S1; DE:S49]. Contractor environmental rules, with penalties for non-compliance, should cover camp siting, gravel extraction, waste disposal, water pollution and worker behaviour; access road impacts can exceed those of the reservoir [DE:S1].

The sources do not give accident frequency benchmarks for hydro construction. A committee should ask for the contractor's injury record on comparable underground work.

## Q.6 Commissioning sequence and tests

Commissioning tests the plant "from water to wire" and requires civil, mechanical and electrical expertise [DE:S1]. The sequence below follows the IFC guide.


**Table Q.2. Commissioning sequence and principal tests**
{: .cap}

| Phase | Preconditions | Principal tests | Source |
|---|---|---|---|
| Dry tests | Installation complete; before impounding, waterway filling, or (run-of-river) flooding of the construction pit and cofferdam removal | Gate speeds; alignment and bearing clearances; tightness tests; wicket gate and valve timing; governor sequences with simulated signals; winding insulation and high-voltage withstand; protection checks | [DE:S1] |
| Wet tests, hydro-mechanical | Water-retaining structures inspected; impounding and waterway filling planned with groundwater, leakage and deformation monitoring | Leakage of closed gates and valves; pressure tests on tunnels and penstocks; discharge tests on regulating gates (spillway tests may wait for the right season) | [DE:S1] |
| Speed-no-load tests | Waterways filled | Start and stop sequences with braking; initial run with over-speed test; bearing temperature stabilisation; shaft run-out and vibration; protection and excitation tests; short-circuit and no-load curves; synchronisation | [DE:S1] |
| Load tests | Switchyard and line tested and ready | Load rejection at 25, 50, 75, 100 and 110% of design load; reactive capability; power system stabiliser; V-curve; temperature rise and output; vibration | [DE:S1] |
| Joint tests (multi-unit) | All units commissioned | Simultaneous load rejection at maximum load, checking pressure and speed rise against contract limits; active and reactive power sharing | [DE:S1] |
| Performance tests | Units above 5 MW | Field acceptance test to IEC 60041 for turbine efficiency and an index test on at least one turbine; generator losses on at least one generator | [DE:S1] |
| Trial operation and reliability run | Tests on completion passed | Continuous normal operation across a range of loads: 3 to 10 days for small projects, about 30 days per unit for large projects; restarted in full if a defect shows reliability is not achieved | [DE:S1] |

Three points matter for a lender. First, if units are identical, performance tests are normally done on one unit only, but any sign that guarantees will be missed may require tests on all units to establish the basis for liquidated damages [DE:S1]. Second, the index test measures relative efficiency; its value is as a baseline for later index tests, so it must be recorded and kept. Third, turnover points between contractors must be signed, for example line readiness before synchronisation, and the grid operator, which usually controls the line, must be engaged early [DE:S1].

## Q.7 Taking-over, defects liability and warranties

The acceptance certificate usually releases the EPC contractor and triggers final payment [DE:S1]. The IFC example schedule shows a provisional acceptance certificate per unit after its reliability run and a final acceptance certificate after joint tests [DE:S1].

During the defects notification period, for example 24 months, the contractor must return to rectify defects found after taking-over [LIT:S7]. Prudent owners de-water and re-inspect tunnels inside that period, with a major payment milestone or credit cover tied to its expiry, and capture longer manufacturer warranties by assignment, collateral warranty or a multi-layered defects regime [LIT:S7].

## Q.8 O&M organisation and staffing

Three organisational models appear in the sources.

- Owner-operated. Large utilities typically have their own O&M division [DE:S1]. Utilities with many plants operate them remotely from a central control room, with "flying teams" for scheduled maintenance and troubleshooting [DE:S1].
- O&M contractor. Smaller producers often outsource to specialised O&M companies or to equipment suppliers. The contract should require the operator to meet the owner's PPA obligations, with PPA responsibilities and non-performance penalties passed through [DE:S1].
- Manufacturer support. Supplier presence on site during the guarantee period on larger projects; on smaller projects, remote diagnostics and parameter adjustment through software-based control systems [DE:S1].

Future staff should train at the manufacturer and join installation and commissioning [DE:S1]. For a 300 MW, two-unit plant in a middle-income country, the IFC guide gives 40 staff, including 14 shift operators; in a developing country with high unemployment, three to ten times as many [DE:S1].

## Q.9 Maintenance regime, intervals and component lives

Preventive (scheduled) maintenance remains the core of most programmes; reliability-centred maintenance must never become a cost-cutting substitute for it; condition-based (predictive) maintenance, monitoring temperature, vibration and dissolved gas, is unsuitable as the sole regime. The recommended practice combines them, using as-found records at each teardown to adjust intervals [DE:S1]. Starts and stops should be minimised to extend life, and spares procurement should follow actual consumption [DE:S1].

Routine tasks include gate and valve testing, dam monitoring, waterway inspection, runner cavitation repair, silt monitoring and transformer oil analysis [DE:S1].


**Table Q.3. Component lives and maintenance intervals**
{: .cap}

| Item | Value | Source |
|---|---|---|
| Economic life of plant, with rehabilitation | 70 to 100 years | [DE:S1] |
| Main generating equipment (turbine other than runner, generator, governor, excitation, inlet valves) | 40 years | [DE:S1] |
| Turbine runners | 10 years | [DE:S1] |
| Power transformers; HV switchgear and switchyard | 40 years | [DE:S1] |
| MV and LV switchgear; plant auxiliaries | 30 years | [DE:S1] |
| Control, protection, SCADA, communication, metering | 20 years | [DE:S1] |
| Penstocks, gates, stoplogs, trash racks; transmission lines | 70 years | [DE:S1] |
| Major overhaul of generating units | Every 7 to 12 years; 4 to 6 weeks for units above 20 MW, 1 to 3 weeks below 5 MW | [DE:S1] |
| Major rehabilitation and upgrade of E&M | Typically at plant age 45 to 60 years | [HY-06] |

*Note: IFC lives are averages under normal conditions; sediment load, water quality, climate and the number of starts change them [DE:S1].*

O&M cost. Annual O&M is quoted at 1.0% to 4.0% of investment; IEA assumes 2.2% for large plants, and including major E&M replacement IFC gives about USD 45/kW/yr for large and USD 52/kW/yr for small plants [DE:S1]. IRENA's sample gives 1% to 3% of total installed cost, averaging slightly below 2% [HY-01]. The IFC guide breaks this down: E&M maintenance at 2.0% to 2.5% of initial E&M investment, of which about 40% for ongoing maintenance, spares and services and about 60% for a reserve fund for the major works every 7 to 12 years; civil maintenance at 0.4% to 0.6% of civil cost; and a spares stock worth 2.5% to 3.0% of the FOB equipment price [DE:S1]. OPEX also includes insurance and, in some countries, concession and water fees [DE:S1].

## Q.10 Performance monitoring

Availability is defined on a period basis; the formulas below are standard definitions.

> A = (T − SO<sub>h</sub> − FO<sub>h</sub>) / T

> FOR = FO<sub>h</sub> / (FO<sub>h</sub> + S<sub>h</sub>)

> η = P / (ρ g Q H)

where T is period hours, SO<sub>h</sub> scheduled outage hours, FO<sub>h</sub> forced outage hours, S<sub>h</sub> service hours, P electrical or shaft power, Q flow and H net head. The IFC guide gives a typical trajectory: about 95% availability in year one (18 days unavailable: 11 days scheduled, 7 days forced), improving to 97% to 98% after three years (4 to 6 days scheduled, 3 to 5 days forced) [DE:S1]. Required availability is usually set in the PPA [DE:S1]. Efficiency degradation is tracked by repeating index tests against the commissioning baseline. Plants should keep event and incident reports to detect equipment weaknesses, and often must record discharges and levels daily or hourly under the water permit [DE:S1].

## Q.11 Insurance

The IFC guide distinguishes pre-completion insurance (construction risks, environmental and political risks) from post-completion insurance (operational failures, environmental, political, non-payment and transfer risks), and notes that obligatory construction insurances are usually required [DE:S1]. Political risk insurance is typically available to both equity and debt where credit-worthy cover is needed [LIT:S7]. Parametric weather insurance and hydrological hedges have not been widely deployed in Africa and remain difficult to place and expensive because local capital and insurance markets lack depth [LIT:S7]. The sources give no premium rates; a committee should ask for quoted rates, deductibles and the treatment of underground works.

## Q.12 Refurbishment and end of concession

Under a BOT concession the facility is transferred to the public authority at the end of the term without further payment [DE:S1]. Nachtigal is being developed as a BOT with transfer to the government of Cameroon after 35 years [LIT:S7]. With main equipment lasting about 40 years [DE:S1], transfer condition is a negotiated issue; the sources set no hand-back tests. The method is to define, in the concession, minimum residual-life or condition criteria per component class (Table Q.3), a final joint inspection including waterway de-watering, and a hand-back reserve funded in the last years.

In Africa, refurbishment is a large market in its own right: 60% of screened facilities have a high or medium need for refurbishment, totalling USD 6.8 billion and 14.7 GW [HY-06]. Rehabilitation is lower risk than greenfield, but uncertainty over ownership, valuation and tariffs has limited private participation [HY-06].

## Q.13 Kasiri illustration

Case values: 60 MW, construction three years, operations 25 years, plant cost about USD 157m (civil 68, hydromechanical 9, electromechanical 33), contingency 10%, availability 0.95, P50 about 292 GWh/yr. Check: P = 1,000 × 9.81 × 57 × 120 × 0.92 × 0.98 ≈ 60.5 MW, consistent with the rating.


**Table Q.4. Kasiri construction and O&M checks using source benchmarks**
{: .cap}

| Check | Calculation | Result |
|---|---|---|
| Schedule against reference class | 36 months × 1.27 (median) and × 1.44 (mean) [HY-08] | About 46 and 52 months |
| Contingency at industry practice | 15% × 68 + (7.5% to 10%) × (9 + 33) [DE:S1] | USD 13.4m to 14.4m, about 12% to 13% of these lines; the case charges 10% on a USD 142.6m subtotal that includes development costs and the contractor's premium (USD 14.3m) |
| EPC advances | 10% × 68 civil; 30% × 42 HM and E&M [DE:S1] | USD 6.8m and 12.6m |
| E&M maintenance budget | 2.0% to 2.5% × 42 [DE:S1] | USD 0.84m to 1.05m/yr, of which about 60% to the major overhaul reserve |
| Civil maintenance | 0.4% to 0.6% × 68 [DE:S1] | USD 0.27m to 0.41m/yr |
| Total O&M cross-check | USD 45/kW/yr × 60,000 kW [DE:S1] | USD 2.7m/yr, about 1.7% of plant cost |
| Overhauls in 25 years | 7 to 12 year cycle [DE:S1] | Two to three per unit |
| Runner and control system renewal | 10 and 20 year lives [DE:S1] | Runners around years 10 and 20; controls around year 20 |
| Availability | Case 0.95 against IFC year 1 of 95% and later 97% to 98% [DE:S1] | Conservative after year 3 |

*Note: Applying the IFC E&M percentage to hydromechanical as well as electromechanical cost is an analyst assumption.*

Each percentage point of availability is worth roughly 292 / 0.95 × 0.01 ≈ 3.1 GWh/yr if outages fell evenly across the year. They need not. Usable flow in February is 20 minus 4 = 16 m3/s, 28% of rated flow. Under the two-unit base case of Annex P (28.5 m3/s each, not a case fact), one unit can pass all usable February flow and stays above its 40% minimum of 11.4 m3/s, so an overhaul of the other unit then loses almost no energy, subject to part-load efficiency. The O&M plan should therefore place overhauls in the lowest-flow months (February, September and January), and the model should not deduct scheduled outages pro rata.

## Q.14 Decision tests

1. Does the baseline programme show the critical path through access, diversion, tunnelling, powerhouse, E&M delivery and grid connection, with float stated for each, and does it survive a 27% schedule overrun on debt sizing?
2. Is diversion timed to a named dry season, and what is the delay if that window is missed?
3. How is ground risk allocated: a geotechnical baseline with a sharing formula, full contractor risk, or "unforeseen conditions" claims, and what does the price include for it?
4. Is contingency on civil works at least 15%, or is a lower figure justified by completed underground investigations?
5. Who manages interfaces between lots, and how many engineers with comparable underground and E&M experience are on the owner's engineer's team?
6. What do the lenders' technical adviser's reports cover, how often, and who receives them?
7. Does the commissioning plan include an IEC 60041 field test and a recorded index-test baseline, and do liquidated damages attach to measured efficiency and output?
8. Is the reliability run defined in days per unit, with full restart if it fails, and linked to provisional acceptance?
9. Is a tunnel de-watering inspection scheduled inside the defects notification period, with a payment milestone or security still held, and are manufacturer warranties assigned to the owner?
10. Who will operate the plant, what are its staffing plan and training programme, and are PPA availability obligations passed through to the O&M contractor with penalties?
11. Is there a funded major-maintenance reserve sized for overhauls every 7 to 12 years and runner and control-system renewal?
12. For a concession, what condition and residual-life criteria apply at hand-back, and who pays for works needed to meet them?

# Annex R. Environmental, social and climate due diligence

## R.1 Why E&S risk is credit risk

Lenders treat environmental and social (E&S) performance as a loan condition. Under Equator Principles transactions the borrower covenants to carry out specified E&S actions; failure is a breach that lets the lender act, up to cancelling the loan and demanding repayment [DE:S1]. Private participants in large hydro rank resettlement and biodiversity risk among the main barriers to investment, and prefer projects with minimal resettlement, community support and IFC-compliant standards [HY-06]. Site selection is the largest determinant of E&S risk: on an unsuitable site no mitigation can redress the balance of costs and benefits [DE:S1]. Due diligence therefore starts at screening, not after the design is fixed.

## R.2 The lender standards framework

**National law.** An environmental licence normally depends on an approved E&S impact assessment (ESIA) and carries obligations for mitigation, monitoring and reporting over the project life [DE:S1]. Licences can lapse if construction does not start in time (one year in Jordan, in the IFC guide's example), and fees apply; Mozambique's was 0.2 percent of total project cost [DE:S1]. A heritage clearance, a water use permit that also covers transboundary conflicts, and confirmation that the site is outside protected areas are typical related permits [DE:S1].

**IFC Performance Standards (2012).** The eight Performance Standards (PS) are de facto the private sector E&S benchmark, have no size threshold, and are mirrored closely by the African Development Bank, EBRD and other multilaterals [DE:S1]. Uganda's GET FiT programme made PS compliance an eligibility condition for small hydro [DE:S9].

**Equator Principles.** EP4 took effect on 1 October 2020 and applies to project finance with total capital cost of USD 10 million or more [DE:S49; DE:S50]. In non-designated countries, which include all of sub-Saharan Africa, the review tests compliance with the PS and the World Bank Group EHS Guidelines [DE:S1; DE:S49; DE:S50]. The IFC guide lists the ten EP III principles: categorisation, assessment, applicable standards, management system and action plan, stakeholder engagement, grievance mechanism, independent review, covenants, independent monitoring, and reporting [DE:S1]. EP4's changes should be checked against its text; the sources reviewed do not summarise them.

**World Bank framework.** Where the World Bank lends or guarantees, its own framework applies, including its good practice note on dam safety [HY-15]. IDA-financed Rusumo Falls was supervised against a safeguards rating [A2:S16].

**Categorisation.** FMO classified Kikagati in Uganda as Category A and Siti and Nyamwamba as B+ [DE:S51; DE:S52; DE:S40b]. Installed capacity does not indicate impact [DE:S1]; the dewatered reach, land take and habitat decide the category.


**Table R.1. IFC Performance Standards: typical hydro issues and evidence lenders request**
{: .cap}

| Performance Standard | Typical hydro issues | Evidence lenders ask for |
|---|---|---|
| PS 1 Assessment and management | Area of influence; cumulative impacts of other plants; greenhouse gas significance; emergency plans [DE:S1] | ESIA to PS and EHS Guidelines; management system; ESMP and sub-plans; cumulative assessment; engagement plan and grievance mechanism [DE:S1] |
| PS 2 Labour | Large workforce, tunnelling safety, camps, subcontractor terms [DE:S1] | HR policy; contractor E&S clauses; underground safety plan; worker grievance channel |
| PS 3 Pollution prevention | Spoil, runoff, noise, dust, vibration, blasting [DE:S1] | Spoil and waste plan [DE:S1]; water quality baseline; blasting plan |
| PS 4 Community health and safety | Dam safety, releases, drowning, vector-borne disease, traffic [DE:S1] | Design to good practice with external review where risk is high [DE:S1]; design flood basis; emergency preparedness plan; dam safety panel where required [HY-15] |
| PS 5 Land and resettlement | Land for headworks, roads, quarries and line; customary tenure; loss of fishing, farming, grazing [DE:S1; LIT:S7] | RAP or livelihood restoration plan; census and cut-off date; entitlement matrix; budget; completion audit |
| PS 6 Biodiversity | Habitat conversion, river fragmentation, fish migration, flow change, threatened species [DE:S1] | Seasonal baseline; critical habitat assessment; e-flow study; biodiversity management plan [DE:S1]; offset design for residual loss |
| PS 7 Indigenous peoples | Groups with distinct identity and customary resource use [DE:S1] | Screening; tailored consultation record; indigenous peoples plan if triggered |
| PS 8 Cultural heritage | Archaeological and sacred sites in inundation or works areas [DE:S1] | Heritage survey; authority clearance [DE:S1]; chance finds procedure |

*Note: Uncited evidence items are the standard outputs of a PS review, listed as a checklist.*

## R.3 The ESIA: process and scope

The ESIA starts at site selection, informs the feasibility design and produces an E&S management plan (ESMP) made of specific plans, such as a resettlement action plan (RAP), biodiversity plan, spoil plan and stakeholder engagement plan [DE:S1]. The feasibility study should report ESIA results and management plans next to the technical concept [DE:S1]. The logic is the mitigation hierarchy: avoid, minimise, then compensate or offset [DE:S1].

**Area of influence.** PS 1 requires it to be defined [DE:S1]. For a diversion scheme it covers the impoundment, headworks, dewatered reach, river below the tailrace, roads, quarries, spoil areas, camps and the line corridor. Access roads can have impacts far larger than the reservoir, lines fragment forest and kill large birds, and quarries enlarge the land lost [DE:S1]. Kasiri's 35 km, 132 kV line is inside the area of influence.

**Baseline seasons.** The sources set no minimum duration. The test is whether surveys cover the flow extremes that drive impacts. Kasiri's mean monthly flow ranges from 20 m3/s in February to 70 m3/s in May (case values); a single-season baseline would miss either low-flow stress in the dewatered reach or high-flow conditions for fish movement.

**Cumulative impact assessment.** The ESIA for the first dam on a river should assess all known proposed dams, and cumulative mitigation should be complete or well advanced before the second dam is built [DE:S1]. In a cascade each reservoir must not raise the tailwater of the plant upstream [DE:S1]. The World Bank report proposes that DFIs help governments prepare pre-feasibility studies that include river basin management plans and cumulative impact assessments [HY-06].

## R.4 Key hydro impacts

**Flow alteration.** Downstream regime change can destroy floodplain ecosystems, worsen low-flow pollution and cut sediment and nutrient loads [DE:S1]; diversion can leave a reach almost dry [DE:S1; LIT:S6]. Base-load operation reproduces natural flows more easily than peaking [DE:S1]. Management plans should specify environmental releases, including for private dams [DE:S1].

**Environmental flows.** The residual, reserved or compensation flow is almost always a permit condition; too little damages aquatic life, too much cuts output, especially in dry periods [LIT:S6]. Setting it is specialist work: understand the river, ecology and downstream uses, consult dependent communities, define values to protect, choose a method, then monitor [DE:S1]. The flow duration curve and low-flow statistics such as Q<sub>95</sub> give the hydrological reference [LIT:S6]. The energy cost follows from the case data:

> E<sub>loss</sub> = ρ × g × H<sub>n</sub> × η<sub>t</sub> × η<sub>gt</sub> × A × Σ (Q<sub>e</sub> × h<sub>m</sub>), over months where Q<sub>m</sub> < Q<sub>d</sub> + Q<sub>e</sub>

With H<sub>n</sub> = 120 m, η<sub>t</sub> = 0.92, η<sub>gt</sub> = 0.98 and A = 0.95, each m3/s gives about 1.01 MW. Only May's mean (70 m3/s) exceeds Q<sub>d</sub> + Q<sub>e</sub> = 61 m3/s, so the release costs energy in eleven months, about 8,016 hours.


**Table R.2. Kasiri environmental flow by month (case mean flows)**
{: .cap}

| Month | Mean flow (m3/s) | Turbine flow after 4 m3/s release | Release as share of flow |
|---|---|---|---|
| Jan | 24 | 20 | 17% |
| Feb | 20 | 16 | 20% |
| Mar | 28 | 24 | 14% |
| Apr | 52 | 48 | 8% |
| May | 70 | 57 (9 spilled) | 6% |
| Jun | 58 | 54 | 7% |
| Jul | 40 | 36 | 10% |
| Aug | 28 | 24 | 14% |
| Sep | 22 | 18 | 18% |
| Oct | 30 | 26 | 13% |
| Nov | 46 | 42 | 9% |
| Dec | 36 | 32 | 11% |

*Note: Derived from case values; monthly means hide daily variation. The same method reproduces the case P50 of about 292 GWh/yr.*

The release costs about 32 GWh/yr, 11 percent of P50. Each further 1 m3/s costs about 8 GWh/yr (close to 3 percent of P50) until the release exceeds 13 m3/s and bites in May too. The release is 10.6 percent of mean flow but 17 to 20 percent of flow in the driest months, where ecologists will test its adequacy.

**Fish passage.** Dams block upstream migration, downstream passage through turbines and spillways often fails, and ladders, lifts and trap-and-truck schemes are usually of limited effectiveness [DE:S1]. Fish-friendly turbines are emerging [DE:S1]; intakes need fish diversion and passes where required [LIT:S6]. Stocking with non-native species is undesirable [DE:S1].

**Sediment.** Sedimentation erodes live storage; catchment management, flushing, check structures and mechanical removal are the responses [DE:S1]. Hard sediment abrades turbines [DE:S1]. At Rusumo, sediment and organic matter in the cooling-water system caused shaft-seal wear and outages [A2:S16].

**Water quality.** Impoundment lowers oxygen and dilution, flooded biomass decays, and low oxygen or gas supersaturation kills fish; selective clearing before filling is standard mitigation [DE:S1].

**Reservoir greenhouse gases.** Flooded biomass emits carbon dioxide and methane. Most hydro more than offsets this, but some reservoirs, such as Balbina in Brazil, appear to emit more than gas-fired generation would for many years; the best mitigation is to flood little land, especially forest [DE:S1]. PS 1 requires significance to be assessed [DE:S1], and Climate Bonds Initiative criteria require low greenhouse gas infrastructure [HY-06]. The sources give no threshold; for run-of-river with small pondage the issue is usually minor, but the ESIA should state flooded area and biomass.

**Biodiversity and critical habitat.** Flooded riverine forest is usually worth more than the aquatic habitat created [DE:S1]. PS 6 bars significant conversion of natural and critical habitat unless specific conditions are met; compensatory protected areas of comparable size and quality are the preferred offset, and wildlife rescue rarely succeeds [DE:S1].

## R.5 Land acquisition and resettlement

Involuntary displacement is considered the most adverse social impact of hydro [DE:S1]. PS 5 requires design alternatives that avoid or minimise displacement and aims to restore or improve livelihoods; economic losses from fisheries, farmland, grazing or clay need replacement resources or income restoration [DE:S1]. Land registration may be incomplete and land may be state or customary, so acquisition is negotiated or compulsory; lenders want the government's commitment to compulsory acquisition, and the allocation of resettlement cost, written into the implementation agreement [LIT:S7]. Customary ownership is often contested and entitlement is hard to determine [HY-06].

Resettlement is a cost and schedule risk. At Rusumo Falls the livelihood restoration and local development programmes rose from USD 18 million to about USD 38 million, more than double; after blasting damage, 580 structures in Tanzania needed repair; 80 households in Rwanda had to be relocated, with the decision taken only in 2023; and the closing date moved from December 2020 to June 2025 through three restructurings [A2:S16]. Not all of that delay was E&S, but the case shows a land line item doubling on the critical path. The RAP should contain a census and cut-off date, entitlement matrix, budget with its own contingency, and a schedule tied to contractor access dates, because late access becomes a claim.

## R.6 Indigenous peoples and cultural heritage

PS 7 requires full respect for indigenous peoples' rights, livelihoods and culture, recognising their often marginal legal and economic status [DE:S1]. The IFC guide's summary does not set out PS 7's consent conditions, so the committee should ask whether screening found indigenous peoples and which PS 7 requirements apply. Under PS 8, heritage objects can be salvaged, but sacred sites usually cannot be replaced [DE:S1]. Many countries require a heritage clearance for the land [DE:S1]; a chance finds procedure belongs in the construction contract.

## R.7 Community health, safety and dam safety

PS 4 requires design, construction and operation to good international practice by competent professionals, with external review in high-risk cases [DE:S1]. The IFC guide distinguishes the normal operation design flood, defined by a return period such as 100 years and set by national rules for the hazard class, from the maximum design flood the structures must survive, the probable maximum or 10,000-year flood [DE:S1]. The World Bank's dam safety note is accompanied by technical notes on hydrological and seismic risk [HY-15; R4:S1]. Other risks are drowning, which needs access control, and water-related disease such as malaria and schistosomiasis around reservoirs in warm climates [DE:S1]. PS 1 requires emergency plans [DE:S1]; for a dam this means a tested emergency preparedness plan for downstream communities.

## R.8 Stakeholder engagement and grievance

PS 1 requires stakeholder engagement, disclosure and a grievance mechanism, and the Equator Principles treat engagement and grievance as separate principles [DE:S1]. Even small projects face local distrust, and communication must run from inception to commissioning [DE:S1]. Benefit sharing through local content, a revenue contribution such as a water royalty, or profit sharing can reduce opposition [LIT:S7]. The committee should ask for the grievance log: numbers, categories, time to close and open cases.

## R.9 Transboundary rivers

Water use is treated as a sovereignty matter where rivers cross borders, as the Grand Ethiopian Renaissance Dam dispute shows; treaties such as that behind the Zambezi River Authority provide cooperation and dispute resolution [LIT:S7]. The host government may need to join international agreements [HY-06], and the water permit covers transboundary conflicts [DE:S1]. Rusumo, on a border river, is owned equally by three states [A2:S16]. Multilateral lenders apply their own procedures for international waterways; the sources do not describe them, so obtain the requirement in writing and put any riparian notification on the schedule.

## R.10 Sustainability tools and green labels

The Hydropower Sustainability Tools comprise the good practice guidelines, the Assessment Protocol (HSAP) and the ESG Gap Analysis Tool (HESG), covering more than 20 topics; an HESG review found Gabon's Dibwangui scheme met 11 of 12 good practice criteria [LIT:S7]. The Hydropower Sustainability Standard certifies at Bronze, Silver and Gold [HY-03]. One green bond index admits large hydro only with an HSAP score of 3 or more or a commitment to the eight PS [HY-06]. A pre-emptive gap analysis is a cheap way to find weaknesses before lenders do.

## R.11 Climate resilience and screening

Climate change may bring significant regional changes in flow volume and timing; the uncertainty is outside the developer's control but can be simulated [DE:S1]. A 2015 drought at Kariba caused load shedding in Zambia [LIT:S7], and the 2024 Kariba generation allocation was cut by about 47 percent, from 30 to 16 billion m3 [CL-04]. Planned dams would concentrate regional capacity in single basins, raising the risk of simultaneous shortfall [CL-03]. Methods exist: a six-phase screening and stress test [CL-01], basin-level revenue studies for African rivers [CL-02], and contract allocation of hydrology and flood risk [CL-06]. Hydrology risk transferred to government becomes a contingent liability [HY-06].

For Kasiri, scaling every monthly mean flow by 0.9 with the 4 m3/s release held fixed cuts modelled energy by about 10 percent, to roughly 264 GWh/yr; in February the release would then be 22 percent of flow. The 10 percent scenario is an analyst's test value, not a projection. The 12-year record is shorter than the 15 years the IFC guide expects [DE:S1], widening uncertainty before any climate adjustment. Screening should also re-run the design floods for heavier extreme rainfall and report spillway capacity and freeboard.

## R.12 E&S action plan and covenants

Lender review ends in an E&S action plan (ESAP): each gap against the PS, the action, owner, deadline and completion evidence. Action plan, independent review, covenants and monitoring are separate Equator Principles [DE:S1]. The IFC guide advises monitorable outcomes, annual work plans and budgets, and warns that delays can threaten a company's ability to meet E&S commitments [DE:S1].


**Table R.3. Where E&S requirements sit in the financing documents**
{: .cap}

| Stage | Typical requirement | What to verify |
|---|---|---|
| Conditions precedent | ESIA licence; ESAP agreed; RAP approved; early-works land secured; E&S staff in place | Licence expiry; ESAP status; land dates against contractor programme |
| Construction | ESMP and ESAP to deadline; contractor obligations; independent monitoring | Contractor clauses; reporting frequency; adviser budget |
| Before impoundment or COD | RAP implemented; e-flow outlet and gauge installed; emergency plan tested; dam safety review | Completion audit; e-flow data logging; drill record |
| Operation | E-flow compliance; grievance mechanism; annual E&S report; incident notice | Compliance history; grievance statistics |

*Note: Sequence follows the Equator Principles as described in the IFC guide [DE:S1]; items are a checklist, not quotations from a loan agreement.*

ESAP deadlines that depend on government action, such as land acquisition, should be matched by government undertakings in the implementation agreement [LIT:S7].

## R.13 E&S cost and schedule

Kasiri carries USD 5m for E&S within a plant cost of about USD 157m (case values), about 3.2 percent. The line should be built up from the ESMP and RAP: land and compensation, livelihood restoration, e-flow outlet and monitoring, fish measures, biodiversity, community safety, the E&S team and lenders' adviser. Study costs sit in development costs; single data points are about USD 4.8 million for the feasibility study and ESIA of the 53 MW Kakono project and line [DE:S16], and a USD 992,000 preparation grant, including the ESIA, for a 7.8 MW Kenyan community hydro [DE:S17].

If Kasiri's E&S line doubled, as Rusumo's livelihood programmes did [A2:S16], the extra USD 5m would equal about 3 percent of plant cost and absorb part of the 10 percent contingency. Schedule risk can exceed cost risk: a missed survey season, late RAP, open grievance or e-flow dispute can delay close or site access, and a lapsed licence must be renewed [DE:S1]. The schedule should show survey windows, disclosure periods, licence issue, RAP implementation and lender review as linked tasks with float.

## R.14 Decision tests

1. Which E&S category has each lender assigned, and does the ESIA scope match it?
2. Does the area of influence include the dewatered reach, roads, quarries, camps and the 35 km line, each with baseline data?
3. Did baseline surveys cover both the low-flow months (January to March, September) and the high-flow months (April to June)?
4. Is the 4 m3/s e-flow fixed in the water permit, what method set it, and does the model show about 8 GWh/yr lost per additional 1 m3/s?
5. Are other plants existing or planned on the river, and has a cumulative impact assessment been done?
6. How many households are physically or economically displaced, and is the RAP budget built from the census with its own contingency?
7. Has the government committed to compulsory acquisition if needed, and who bears resettlement overruns?
8. What did screening find on indigenous peoples, critical habitat and cultural heritage?
9. Which design floods were used, has an independent reviewer accepted them, and is there a tested emergency preparedness plan?
10. Is the river transboundary, and are notification or treaty steps on the schedule?
11. What are P50 energy and minimum DSCR under a 10 percent flow reduction?
12. Which ESAP items are conditions precedent, which depend on government action, and are their deadlines achievable?