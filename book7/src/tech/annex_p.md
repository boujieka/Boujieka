## Annex P. Electromechanical equipment and grid connection

### P.1 Purpose and scope

The electromechanical (E&M) package turns head and flow into saleable energy: turbines, generators, governors and excitation, transformers, switchyard, protection, SCADA, auxiliaries, and the hydromechanical gates and valves that control water to the units. Each large plant's E&M equipment is custom-designed [DE:S1]. In the IFC benchmark sample E&M averages 30.3% of total project cost, with a range of 14.9 to 56.6% [DE:S1]. The decisions a committee must test are few: turbine type, number and speed of units, turbine setting, sediment protection, and the contract and test regime that makes supplier guarantees enforceable.

### P.2 Turbine types and selection by head and flow

Turbine choice rests on the site's head and flow, including how often the turbine will run at part load because available flow is below design discharge [DE:S1]. Turbines divide into two families [DE:S1]:

- **Impulse** (Pelton, Turgo, cross-flow): the runner turns in air under one or more jets. They hold efficiency under fluctuating flow, avoid penstock overpressure, control overspeed easily and are easy to maintain.
- **Reaction** (Francis, propeller, Kaplan, bulb): the runner is immersed in a pressure casing and driven by lift; a draft tube recovers head below the runner. Runners are smaller and faster than Peltons, can run submerged, and give higher efficiency at higher power.

The IFC guide's head classes are: low head below 10 m and high head above 100 m; its medium-head range is misprinted in the text ("50 m < H < 10 m") and should not be quoted [DE:S1]. The guide's head-flow chart (Figure 4-19, on log axes of 1 to 1000 m head and 1 to 1000 m^3^/s flow) places, as far as it can be read, Pelton and Turgo at high head and low flow, Kaplan at low head and high flow, cross-flow at low to medium head and small flow, and Francis across the wide middle field; the boundaries depend on each manufacturer's design [DE:S1].

Table: Table P.1. Turbine types: principle, application and part-load features
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

### P.3 Specific speed

Specific speed condenses head, flow (or power) and rotational speed into one number that characterises runner shape: low for Pelton, intermediate for Francis, high for propeller and Kaplan. A propeller runs faster than a Francis for the same head and flow, which is why it superseded the low-head Francis [DE:S1]. ESHA makes specific speed its main selection criterion [LIT:S6], but none of the source texts available here gives numerical bands by turbine type, so the annex gives definitions only; the engineer should show the manufacturer's experience chart behind any proposed speed.

Three forms are in common use (n in rpm, Q in m^3^/s per unit, H net head in m, P shaft power per unit):

> n~s~ = n × P^0.5^ / H^1.25^ (P in kW; metric power-based form)

> n~q~ = n × Q^0.5^ / H^0.75^ (flow-based form)

> n~QE~ = (n / 60) × Q^0.5^ / (g × H)^0.75^ (dimensionless form)

The rotational speed of a synchronous unit is fixed by grid frequency f and the number of pole pairs p:

> n = 60 × f / p

Speed therefore comes in discrete steps. At fixed specific speed, speed rises as unit size falls; a higher specific speed shrinks the generator but needs a deeper setting against cavitation (P.6).

### P.4 Efficiency and part-load behaviour

Turbine selection must compare efficiency across the whole flow range, not only at the design point [DE:S1]. Pelton and Kaplan turbines keep high efficiency below design flow; cross-flow and Francis efficiency drops more sharply below half flow, which suits them to steady flows [DE:S1]. Below a minimum flow the unit must stop to avoid damage from heavy vibration [DE:S1]. The two sources state different minimum flows, and the difference matters for low-flow months.

Table: Table P.2. Minimum technical flow by turbine type, % of design flow
| Turbine | IFC guide [DE:S1] | ESHA guide [LIT:S6] |
|---|---|---|
| Pelton | 10 to 20 (depends on number of nozzles) | 10 |
| Turgo | not stated | 20 |
| Francis | 40 | 50 |
| Kaplan (double regulated) | 20 | 15 |
| Semi-Kaplan (single regulated) | 40 | 30 |
| Propeller (fixed) | not stated | 75 |
Note: IFC gives Kaplan as 20 to 40% for double and semi regulated machines respectively.

The energy estimate should apply the efficiency curve strip by strip over the flow duration curve, ending at the larger of minimum technical flow and reserved flow [LIT:S6]. Net head is lowest at maximum discharge, because losses rise with velocity squared and tailwater rises with flow [DE:S1], so a rated net head must be stated with its flow.

Variable-speed generation reduces efficiency variability off nominal head or flow and reduces abrasion [DE:S1].

### P.5 Number and size of units

The unit count trades three things:

1. **Low-flow operation.** The IFC guide's own example: instead of one 60 MW Francis unit, two 30 MW units allow operation down to 20% of plant design discharge instead of 40% [DE:S1]. Each scheme needs an assessment of whether the extra energy pays for the extra cost [DE:S1].
2. **Availability.** With one unit, every unit outage is a plant outage. Major overhauls recur every 7 to 12 years and take 4 to 6 weeks for units above 20 MW [DE:S1]; with several units they can fall in low-flow months.
3. **Cost.** More units mean more turbines, generators, valves, controls and powerhouse length; in the IFC optimisation example, IRR moves in steps with turbine unit costs [DE:S1]. Identical units share spares and need performance tests on one unit only [DE:S1].

The powerhouse crane is sized for the heaviest lift, a generator part or the runner [DE:S1], so fewer, larger units also raise crane and transport loads.

### P.6 Cavitation and turbine setting

Cavitation occurs where pressure falls below vapour pressure; the vapour cavities collapse in higher-pressure zones and can be extremely damaging [LIT:S6]. In a reaction turbine the tailwater level governs its onset [LIT:S6]. Cavitation and erosion damage runners and cut efficiency; the O&M response is inspection and in-situ weld repair [DE:S1].

The setting (elevation of the runner relative to the minimum tailwater) is governed by the plant cavitation coefficient (Thoma sigma):

> σ~plant~ = (H~atm~ − H~v~ − H~s~) / H

where H~atm~ is atmospheric pressure head (falling with altitude), H~v~ vapour pressure head, H~s~ suction head (runner above tailwater positive) and H net head. The setting must satisfy σ~plant~ above the turbine's critical sigma with a margin set by the manufacturer from model tests. The sources do not give sigma values by specific speed, so the annex quotes none. The arithmetic is still useful: at 120 m net head, each 0.01 of sigma is 1.2 m of setting depth, so a change of runner speed or a lower minimum tailwater can move the powerhouse floor by metres and change civil cost.

### P.7 Sediment abrasion and coatings

In medium- and high-head plants, suspended sediment wears hydraulic steel structures and turbines, reducing efficiency and life [DE:S1]. The higher the head, the smaller the particle that must be removed: above 100 m head, all particles larger than 0.2 mm should be retained in the sand trap; 0.3 mm is acceptable at lower heads; hard (quartz) and angular particles justify a smaller limit [DE:S1]. ESHA expresses the abrasive power of grains on a Francis runner as:

> P~e~ = μ × V~g~ × ((ρ~s~ − ρ~w~) / R) × v^3^

with μ a friction coefficient, V~g~ grain volume, ρ~s~ and ρ~w~ grain and water densities, R blade radius and v grain velocity [LIT:S6]. Because grain velocity scales with head, abrasion rises steeply with head. ESHA reports Francis repair intervals of about 6 to 7 years with a sand trap retaining 0.2 mm, 3 to 4 years at 0.3 mm and 1 to 2 years at 0.5 mm, and finds the economic optimum near 0.2 mm in severe conditions (high head, quartz) and 0.3 mm in normal conditions [LIT:S6].

Mitigations are an efficient desander, hard ceramic coatings [DE:S1], variable speed [DE:S1] and, on silty rivers, silt monitoring to plan repairs [DE:S1]. The sources do not quantify coating life or cost.

### P.8 Generators, excitation and governors

Large and medium units usually have vertical shafts; small units horizontal [DE:S1]. Excitation is brushless or with brushes [DE:S1]. **Synchronous generators** have DC or permanent-magnet excitation and a voltage regulator; their excitation is independent of the grid, so they can operate islanded and control voltage [DE:S1]. **Asynchronous generators** cannot regulate voltage, run at a speed tied to grid frequency and cannot produce power when isolated because their excitation comes from the grid [DE:S1]. For a 60 MW grid plant expected to support voltage, synchronous machines are the normal choice. Generator efficiency rises with rating, approaching 98% above 1 MW [DE:S1].

The governor moves guide vanes or needles to hold speed and load; modern practice is digital PID governors [DE:S1]. Closure time and the waterway interact: normal water hammer under governor shutdown can raise penstock pressure by 25 to 50% of gross head for reaction turbines, depending on governor time constants [LIT:S6]. ESHA's water acceleration time t~h~ tests whether the waterway is governable:

> t~h~ = V × L / (g × H)

If t~h~ is below 3 s a surge tower is unnecessary; above 6 s a surge tower or other device is needed to avoid strong oscillation in the turbine controller, and a badly designed governor can interact with surge-tank oscillation [LIT:S6]. Where valves must close fast, a relief valve in parallel with the turbine slows flow changes in the penstock [LIT:S6].

### P.9 Transformers, switchyard, protection, SCADA and auxiliaries

Step-up transformers raise voltage to cut line losses [DE:S1]. The switchyard should sit close to the powerhouse, above design tailwater (for example the 100-year flood level), sized by the number and direction of outgoing lines [DE:S1]. Transformer upkeep relies on oil and winding temperature monitoring, dissolved gas analysis and tan delta tests [DE:S1]. Protection receives primary and secondary injection testing, and generator relays are function-tested on no-load runs [DE:S1]. Software-based control and SCADA allow remote diagnostics where permanent supplier presence is uneconomic [DE:S1]. Auxiliaries comprise drainage and dewatering pumps, cooling, compressed air, ventilation, AC and DC supplies and the emergency diesel [DE:S1].

Table: Table P.3. Expected useful life of E&M components [DE:S1]
| Component | Life (years) |
|---|---|
| Turbine (excluding runner), generator, governor, excitation, main inlet valves | 40 |
| Turbine runners | 10 |
| Power transformers; HV switchgear and switchyard | 40 |
| MV and LV switchgear | 30 |
| Control, protection, SCADA, communications, metering | 20 |
| Auxiliary mechanical and electrical equipment | 30 |
| Penstocks, gates, stoplogs, trash racks; transmission lines | 70 |
Note: averages; actual life depends on water quality, sediment load, climate and number of starts and stops [DE:S1].

### P.10 Hydromechanical equipment

Hydraulic steel structures are classed by purpose [DE:S1]: service gates regulate flow or level (spillway, bottom outlet); emergency gates are only fully open or shut (intake, draft tube, upstream of penstock valves); maintenance gates, usually stoplogs, dewater conduits; guide vanes or needles regulate turbine flow; trash racks protect intakes. Gate type depends on purpose, opening size, climate and operation [DE:S1]. Commissioning checks gate speeds, leakage of closed gates and emergency valves, and inlet valve timing [DE:S1].

### P.11 Grid connection and grid code

Grid connection cost is driven mainly by distance to the grid [DE:S1]. Industry contingency practice is 7.5 to 10% for grid connection and E&M, against 15% for civil works [DE:S1]. Missing transmission and grid upgrades are a key barrier to commercial operation, producing large deemed-energy claims on offtakers [HY-06], and commissioning needs early coordination with the grid operator [DE:S1].

The sources quote no grid code numbers (frequency and voltage ranges, fault ride-through, reserve). Its test content is visible in the commissioning list: synchronisation, reactive capability test, power system stabiliser test, V-curve, load rejection at 25, 50, 75, 100 and 110% of design load, and joint active and reactive power sharing for multi-unit plants, with results compared against the supply contract and the PPA [DE:S1]. The committee should obtain the national grid code and map each clause to an equipment specification item and a test.

### P.12 Supply contracts, factory and site testing

Developers often split civil, E&M and grid contracts; lenders generally prefer a turnkey EPC, which costs more because risk moves to the contractor [DE:S1]. Split packages typically use FIDIC Yellow Book for E&M and Red Book for civil works, and only a handful of turbine suppliers compete [LIT:S7]. E&M payments are typically 30% advance, 50% on delivery, 20% on acceptance [DE:S1], and E&M manufacturing sits on the critical path [DE:S1]. Supplier warranties often outlast the EPC defects period (for example 24 months); the owner should capture them by assignment or collateral warranty [LIT:S7].

Future O&M staff should attend shop assembly and testing [DE:S1]. Site tests run dry (alignment, bearing clearances, gate and valve timing, winding insulation and withstand, governor logic), no-load (overspeed, vibration, excitation) and on load [DE:S1]. For units above 5 MW, an IEC 60041 field acceptance test and an index test verify turbine efficiency on at least one unit, and generator losses are measured on at least one generator [DE:S1]. Large projects commonly run a 30-day trial per unit; a defect forces a restart [DE:S1]. Spares stock is about 2.5 to 3.0% of FOB equipment price, and the annual E&M maintenance budget about 2.0 to 2.5% of initial investment, of which about 60% is a reserve for the 7 to 12 year major overhauls [DE:S1]. First-year availability is about 95%, improving to 97 to 98% after three years [DE:S1].

### P.13 Kasiri worked example

**Power check.** With the case values:

> P = ρ × g × Q × H × η = 1,000 × 9.81 × 57 × 120 × 0.92 × 0.98 = 60.5 MW

Hydraulic power is 67.1 MW, shaft power 61.7 MW and output 60.5 MW, so the 60 MW rating is consistent. Two comments. First, 0.92 is a design-point efficiency; at part load the Francis curve falls (P.4), so the energy model needs a curve, not a constant. Second, 0.98 for generator and transformer combined is optimistic: IFC puts generator efficiency alone at up to about 98% above 1 MW [DE:S1], and transformer losses come on top. The energy check (60.5 MW × 8,760 h × 0.56 ≈ 297 GWh) agrees with the P50 of about 292 GWh.

**Turbine type.** At 120 m net head and 57 m^3^/s (19 to 57 m^3^/s per unit), Kasiri sits in the high-head class (above 100 m) and in the Francis field of the IFC head-flow chart, well above the bulb ceiling of 30 m and at flows beyond the Pelton field [DE:S1]. The design ratio Q~d~/Q~av~ = 57/38 = 1.5 is at the top of the 1.0 to 1.5 range for run-of-river, and the 56% capacity factor lies within the 40 to 70% run-of-river range [DE:S1].

**Specific speed.** Unit count, grid frequency (50 Hz) and speeds below are illustrative assumptions, not case facts.

Table: Table P.4. Illustrative Kasiri unit configurations (H = 120 m, η~t~ = 0.92, 50 Hz)
| Units | Q per unit (m^3^/s) | Shaft power per unit (MW) | Speed (rpm) | Pole pairs | n~s~ (kW) | n~q~ | n~QE~ |
|---|---|---|---|---|---|---|---|
| 1 | 57.0 | 61.7 | 214.3 | 14 | 134 | 44.6 | 0.134 |
| 2 | 28.5 | 30.9 | 300.0 | 10 | 133 | 44.2 | 0.133 |
| 2 | 28.5 | 30.9 | 333.3 | 9 | 147 | 49.1 | 0.148 |
| 3 | 19.0 | 20.6 | 375.0 | 8 | 135 | 45.1 | 0.136 |
| 3 | 19.0 | 20.6 | 428.6 | 7 | 155 | 51.5 | 0.155 |
Note: H^1.25^ = 397.2; H^0.75^ = 36.3; (gH)^0.75^ = 201.0. Speeds are synchronous steps n = 3000/p.

Holding specific speed near 134, moving from one to three units raises speed from 214 to 375 rpm and shrinks each generator; the next speed step raises specific speed by 11 to 15%, saving generator cost but needing a deeper setting. The supplier must confirm the choice against its reference list and model tests.

**Low-flow operation.** Available turbine flow is river flow less the 4 m^3^/s environmental flow, capped at 57 m^3^/s.

Table: Table P.5. Months below minimum technical flow, Kasiri monthly means (illustrative unit counts)
| Configuration | Unit design flow (m^3^/s) | Minimum flow, IFC 40% (m^3^/s) | Months below (IFC) | Minimum flow, ESHA 50% (m^3^/s) | Months below (ESHA) |
|---|---|---|---|---|---|
| 1 × Francis | 57.0 | 22.8 | Jan, Feb, Sep | 28.5 | Jan, Feb, Mar, Aug, Sep, Oct |
| 2 × Francis | 28.5 | 11.4 | none | 14.3 | none |
| 3 × Francis | 19.0 | 7.6 | none | 9.5 | none |
Note: available flows Jan to Dec are 20, 16, 24, 48, 57, 54, 36, 24, 18, 26, 42, 32 m^3^/s. Monthly means hide daily lows, so the daily flow duration curve must confirm the result.

A single unit would stop for three to six months of an average year, inconsistent with a 56% capacity factor. Two units remove the problem on monthly means and allow overhauls in February or September; three add dry-year margin (energy CV 0.15) at extra cost. Two units is the natural base case to test.

**Sediment and cost.** At 120 m head the sand trap should retain particles above 0.2 mm [DE:S1], and quartz content must be known before runner coating is specified. E&M at USD 33m is 26% of the USD 127m of listed base components (33% with hydromechanical), within IFC's 14.9 to 56.6% range [DE:S1], or about USD 550 per kW. The 0.95 availability matches IFC's first-year figure and is conservative against the 97 to 98% expected after year three [DE:S1].

### P.14 Decision tests

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
