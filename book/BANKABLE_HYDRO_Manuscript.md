# BANKABLE HYDRO
## Structuring Hydropower Projects Without Creating Unsustainable Public Liabilities

*Africa Energy Finance Series, Product 7*
*First-draft manuscript, v1.0 (2026-10-03)*

---

### How to read this book

The book has a companion model, the **Bankable Hydro Integrated Bankability Model** (`model/Bankable_Hydro_Model.xlsx`). Each chapter ends with a **"In the model"** box that names the sheets that put the chapter's ideas into practice. The worked examples use the model's fictional reference project, the *Lumora Falls Hydropower Project* (400 MW, Republic of Navaria). Every Lumora/Navaria number is invented for teaching. No confidential data is used.

**Citation convention.** Sources are cited by ID against the research database in this repository:

- `[SD xx-nn]`: `research/source_database.md` (institutional and academic sources)
- `[A1 Sn]`, `[A2 Sn]`: African case files `research/case_studies/africa_part1.md` and `africa_part2.md`
- `[INT Sn]`: `research/case_studies/international_benchmarks.md`
- `[CI]`: `research/competitive_intelligence.md`

Several sources could only be read as search snippets; those are flagged in the research files and should be re-verified before the book is published. Interpretation is labelled as such. Where a case file reads "PUBLIC DATA NOT FOUND", this book does not fill the gap.

---

## Contents

**Part I: The problem**
1. Technical feasibility is not bankability, and bankability is not sustainable public finance
2. The value chain: from river to financial close

**Part II: The project layer**
3. Hydrology: from flow to P90
4. Configuration, CAPEX and the construction-risk reference class
5. Operating costs, tariffs and LCOE: plant versus system

**Part III: The power-system layer**
6. Transmission: the readiness gap
7. Grid and demand: potential, commercial, contracted and bankable demand

**Part IV: The offtaker and regulatory layer**
8. The utility: the maximum sustainable PPA payment
9. Regulation as a bankability input
10. The PPA: allocating hydrology, volume, currency and termination risk

**Part V: The finance layer**
11. Project finance for hydro: sizing, sculpting and the lender case
12. Five structures, one project: public, IPP, PPP, hybrid, blended

**Part VI: The public-finance layer**
13. Direct support and contingent liabilities
14. Project-level fiscal exposure screening

**Part VII: Decision**
15. Risk allocation: who really bears what
16. The Hydropower Bankability Framework™
17. Ten rules for financial close without unsustainable liabilities

Annex A: Case library summary · Annex B: Benchmark ranges · Annex C: Glossary · Annex D: Model map

---

# PART I: THE PROBLEM

## Chapter 1. Technical feasibility is not bankability, and bankability is not sustainable public finance

Hydropower projects in Africa usually get stuck at one of three points.

1. **The engineering checks out but nobody will lend.** The dam can be built and the river can turn the turbines, yet no lender will commit because the buyer of the power cannot be shown to pay. In other cases the evacuation line has no financing, or the regulatory framework cannot enforce the contract.
2. **Lenders will lend, but only once the risk has been moved to the state.** Payment guarantees, loan guarantees, termination payments and take-or-pay obligations can make a project bankable. Each of them is a claim on the public budget that may never be recorded as debt.
3. **The project closes and the liability turns up later.** Utility arrears to IPPs, called guarantees, deemed-energy payments for power that cannot be evacuated, and arrears on sovereign-guaranteed loans move from the power sector onto the sovereign balance sheet.

The public record shows all three.

- **Kafue Gorge Lower (Zambia).** The cost rose from about USD 1.48 bn to about USD 2 bn [A1 S57], including about USD 312 m of capitalised interest [A1 S58]. In the 2024 joint World Bank–IMF debt sustainability analysis, ZESCO's payables to IPPs (USD 1.2 bn domestic) were brought inside the sovereign debt perimeter [SD DB-03].
- **Lao PDR (international benchmark).** Public and publicly guaranteed debt stood at 112% of GDP at end-2022, with the energy sector about 43% of it [INT S13]. That position was built up largely through take-or-pay arrangements with a weak domestic utility.
- **Sub-Saharan Africa overall.** Power-sector quasi-fiscal deficits averaged about 1.5% of GDP and exceeded 5% in several countries [SD UT-02]. Across developing countries, annual fiscal injections into power SOEs averaged 0.25% of GDP [SD FR-17].

**The thesis of this book.** A hydropower project is bankable *and* fiscally sustainable only if five layers are tested together:

| Layer | Question |
|---|---|
| Project | Does the plant produce enough, at a cost, to service its debt? |
| Power system | Can the energy be evacuated and absorbed? |
| Offtaker / utility | Can the buyer pay, after everything else it must pay? |
| Regulation / PPP | Is the contract chain enforceable and the risk allocation coherent? |
| Sovereign | What has the state really promised, and can it afford it if called? |

Most tools test one layer each. This book and its model test them together, with one engine and one set of assumptions.

> **In the model:** `00_README`, `01_CONTROL_PANEL`, `32_DASHBOARD`.

## Chapter 2. The value chain: from river to financial close

The value chain the book follows is:

HYDRO RESOURCE → PLANT → TRANSMISSION → GRID → DEMAND → OFFTAKER → UTILITY → REGULATION → PPA → FINANCING → PPP/IPP → GOVERNMENT SUPPORT → FISCAL EXPOSURE → DEBT SUSTAINABILITY → BANKABILITY → FINANCIAL CLOSE

Two ideas run through the book.

**Idea 1: risk is conserved.** Contracts do not remove hydrology, demand, currency or construction risk. They move it to someone else. A deemed-energy clause moves transmission risk from the IPP to the utility. A sovereign PPA guarantee moves it from the utility to the Treasury. A tariff freeze then moves it from the Treasury to arrears owed to the IPP, which brings it back to lenders. The model routes every shortfall explicitly, so the reader can see where each risk ends up.

**Idea 2: "off balance sheet" does not mean "off the public's books".** The Reventazón trust-and-lease structure in Costa Rica keeps the plant off the utility's balance sheet in form. In substance, construction, operating and overrun risk pass through to ICE, the state utility [INT S20]. Our structure comparison (Chapter 12) shows that, for the same project, gross public exposure at COD changes little across very different structures. What changes is the form the exposure takes (direct debt, guarantee, termination obligation, grant) and when it falls due.

> **In the model:** the sheet sequence 02 → 32 follows the chain. `33_CHECKS` confirms internal consistency.

---

# PART II: THE PROJECT LAYER

## Chapter 3. Hydrology: from flow to P90

### 3.1 Four kinds of "capacity"

A financier must keep four quantities apart:

- **Installed capacity (MW):** nameplate.
- **Available capacity (MW):** installed × availability.
- **Expected generation (GWh):** what the river allows on average (P50).
- **Contracted energy (GWh):** what the PPA refers to. It may differ from what is delivered (curtailment) and from what is paid (deemed energy).

Belo Monte is the extreme illustration: 11,233 MW installed against 4,571 MW of assured energy, about 41% of nameplate [INT S8].

### 3.2 From flow to energy

The model computes monthly average power as

P = MIN(ρ · g · Q_usable · H · η_turbine · η_generator / 10⁶ , P_installed)

where Q_usable = MIN(MAX(Q_river − Q_environmental, 0), Q_design). Monthly energy equals power × hours × availability. In the Lumora example, mean monthly flows from 120 to 520 m³/s produce a P50 of about 1,666 GWh/yr and a capacity factor of about 47.5%. That sits inside the 33%–81% band (5th–95th percentile) that IRENA reports for large African hydro commissioned 2018–24, close to the 48% weighted average [SD HY-01].

*Methodological caution.* Computing energy from long-term mean monthly flows overstates output wherever flows exceed the design flow in some years. The model flags this. For a bankable study, use a simulated generation series over the full record.

### 3.3 P50, P75, P90

Lenders size debt on a downside generation case, typically P90. The model uses a normal approximation:

P90 = P50 × (1 − 1.2816 × CV),  P75 = P50 × (1 − 0.6745 × CV)

The input is the coefficient of variation (CV) of annual energy, 12% in the Lumora case. Where an empirical distribution exists, it should replace the approximation. Gate 1 of the bankability framework tests three things:

- the length of the reliable flow record;
- the P90/P50 ratio;
- the maturity of the hydrology study.

### 3.4 Drought and climate

Kariba shows that multi-year drought is a debt-service risk as well as an engineering one. News reporting in 2024 described the water allocation for generation being cut from 30 to 16 bn m³ [SD CL-04]. Peer-reviewed work warns that planned hydropower expansion in eastern and southern Africa raises the risk of *concurrent* climate-related supply disruption across interconnected systems [SD CL-03].

The model therefore offers two stresses:

- a **drought window**: a flow factor applied for N operating years;
- a **climate trend**: a percentage change in mean flow per decade, labelled illustrative until a basin study supports it.

**Worked result (Lumora, PPP structure, debt locked).** A three-year drought at 70% of normal flows reduces minimum DSCR from 1.75x to 1.64x. Equity IRR barely moves (15.1% → 14.7%). The reason is the two-part tariff: about 71% of revenue is capacity payment, so hydrology risk falls only on the energy component. Chapter 10 discusses who pays for that protection.

> **In the model:** `03_HYDROLOGY`, `04_GENERATION`, stress toggles `st_drought`, `st_climate`.

## Chapter 4. Configuration, CAPEX and the construction-risk reference class

### 4.1 Benchmarks

IRENA reports a weighted-average installed cost for large hydro in Africa of USD 2,330/kW (2010–17) and USD 2,515/kW (2018–24), in 2024 USD [SD HY-01]. The World Bank appraisal for Nachtigal implies about USD 3,290/kW (USD 1,383 m for 420 MW; analyst calculation) [SD PF-11].

Unit costs in the case library vary widely: about 1,000 USD/kW for GERD to above 5,800 USD/kW for Rusumo Falls (80 MW). These are nominal, unadjusted and scope-inconsistent (see Annex A). The case-library median is about 3,050 USD/kW.

**Scope discipline matters more than the headline number.** The Three Gorges budget ranged from 57 to 205 bn CNY depending on whether resettlement, transmission and interest were included [INT S2]. A bankable cost estimate must state whether it includes IDC, transmission, E&S and owner's costs. The model reports "plant CAPEX", "funding base", "total uses" and "system cost incl. public transmission" separately.

### 4.2 The reference class for overruns

Ansar et al. studied 245 large dams and found a median real cost overrun of +27% and a mean of +96%, together with a median schedule overrun of +27% (1.7 years) and a mean of +44% (2.3 years) [SD HY-08]. African cases fit the pattern:

| Project | Reported overrun |
|---|---|
| Bui | +USD 168 m (+27%) [A1 S38] |
| Rusumo | civil-works contract +47% [A2 S16] |
| Karuma | about five years late [A2 S40] |
| Kafue Gorge Lower | about three years late [A1 S57] |

The model's default overrun stress (+27%) is the median, not the mean. A user who believes the project sits in the right-hand tail should run +50% or higher.

**Worked result.** Applying the +27% CAPEX overrun stress to Lumora with debt locked:

- Financing gap rises from about USD 62 m to about USD 177 m.
- Equity IRR falls to about 10%.
- Fiscal NPV moves from about +USD 28 m to about −USD 124 m. Government equity, VGF and public transmission all scale with cost, and contingent exposure peaks at about USD 1.5 bn.

### 4.3 Delay

Delay costs money twice: through interest during construction and escalation, and through revenue deferred. Kafue Gorge Lower's USD 312 m of capitalised interest is about 16% of a USD 2 bn total [A1 S58]. The model adds a per-year delay cost (default 4%) and extends the S-curve. A two-year delay raises the Lumora financing gap to about USD 159 m.

> **In the model:** `05_PLANT_CAPEX`, `06_CONSTRUCTION`, stresses `st_capex`, `st_delay`; Gate 3.

## Chapter 5. Operating costs, tariffs and LCOE: plant versus system

IRENA reports hydro fixed O&M of 1–3% of installed cost per year, averaging slightly under 2% [SD HY-01]. Lumora's fixed O&M is about 1.7%.

The model computes two LCOEs:

- **Plant LCOE**: project CAPEX, OPEX and royalties over energy delivered plus deemed energy.
- **Delivered system LCOE**: plant LCOE plus publicly funded transmission CAPEX and O&M, over energy delivered to load net of transmission losses.

For Lumora, plant LCOE is about USD 111/MWh (nominal, levelised at 10%) and system LCOE about USD 134/MWh. The USD 23/MWh difference is cost that sits on the public side of the ledger, and a plant-only analysis never shows it. This is why the book argues for a *system* view of cost.

> **In the model:** `07_OPEX`, `15_TARIFF`, `17_PROJECT_FINANCE` (lcoe, lcoe_sys), `28_SENSITIVITY`.

---

# PART III: THE POWER-SYSTEM LAYER

## Chapter 6. Transmission: the readiness gap

*Can the plant evacuate the electricity it generates?* The question sounds trivial. In practice the plant and its evacuation line are often procured, financed and built by different parties to different timetables.

- **Rusumo Falls.** Generation was IDA-financed, while transmission was parallel-financed by AfDB and the EU [A2 S16]. Grid supply had to wait for cross-border lines and three separate PPAs.
- **Uganda.** In 2020, 9% of UETCL's purchases were "deemed energy" (Shs 104.4 bn), paid for but not evacuated [A2 S55; press, search-result only, so verify before external use].

### 6.1 Measuring the gap

The model defines a **Transmission Readiness Gap** in two parts:

- **Timing:** transmission COD minus plant COD, in years.
- **Capacity:** installed MW minus evacuation MW in the first operating year.

Effective evacuation each year = MIN(line capacity if in service, otherwise interim capacity via the existing network; grid absorption limit at minimum load). Delivered energy = generation × MIN(1, evacuation MW / installed MW). This proportional rule is conservative for a plant with pondage and is documented as a simplification.

### 6.2 Costing the line

The EAPP Master Plan (2014) lists 400 kV AC line costs of about USD 0.36–0.70 m/km, in 2012 USD including IDC [SD TX-04]. Lumora's 180 km at USD 0.55 m/km, plus substations and reinforcement, comes to about USD 219 m in real 2026 terms (analyst calculation from model inputs). That is about 21% of plant CAPEX and roughly USD 550/kW of plant.

### 6.3 Who pays when the line is late?

The answer depends on the PPA's deemed-energy clause and on who builds the line.

**Worked result.** A two-year transmission delay at Lumora, with deemed energy payable, leaves the IPP's DSCR unchanged, because the utility pays for energy it cannot receive. The utility's payment-capacity ratio falls from about 2.0x to 1.6x, and Gate 4 moves to CRITICAL GAP. Fiscal NPV actually *improves* slightly, because public transmission spending is deferred. This is an example of a fiscal indicator rewarding a bad outcome, and it is why the framework never relies on a single metric.

> **In the model:** `08_TRANSMISSION`, `09_GRID`, `04_GENERATION`, stress `st_trans`; Gate 4.

## Chapter 7. Grid and demand: potential, commercial, contracted and bankable demand

The model distinguishes four kinds of demand:

| Concept | Definition in the model |
|---|---|
| Potential | Sum of segment demand (residential, commercial, industrial, mining, productive use, public) + export potential |
| Commercial | Segment demand weighted by the share from customers able and willing to pay |
| Contracted | PPA contracted energy (P50) |
| Bankable | MIN(contracted, absorbable × commercial ratio) |

Absorbable energy = supply gap after other committed supply + displaceable thermal + signed exports.

Tanzania's experience after Julius Nyerere (2,115 MW) shows the risk of building ahead of demand. National installed capacity reaches about 4.6 GW against a 2.27 GW peak, a surplus of 2.38 GW, and exports are being discussed to absorb it [A2 S30].

The project's share of system peak is a grid-integration warning sign. Lumora at COD is about 19% of national peak, so Gate 2 rates it CONDITIONAL.

> **In the model:** `10_DEMAND`, `09_GRID`; Gate 2.

---

# PART IV: THE OFFTAKER AND REGULATORY LAYER

## Chapter 8. The utility: the maximum sustainable PPA payment

### 8.1 The question models usually skip

Most project models assume the offtaker pays. In Sub-Saharan Africa the evidence says otherwise:

- Transmission and distribution losses average about 15% (23% excluding South Africa), against a 10% benchmark [SD UT-02].
- Collection rates range from about 58% to about 100% [SD UT-02].
- The case files repeatedly show utilities owing IPPs hundreds of millions. One example is ECG owing Bui Power Authority USD 612 m (March 2023) [A1 S40].

### 8.2 A simplified utility cash model

`12_UTILITY` builds the utility's cash position year by year, in USD equivalents of local-currency flows:

```
Cash available before new PPA
  = collections (sales × tariff ÷ FX × collection rate)
  + government transfers
  − utility OPEX
  − cost of other supply
  − existing debt service

Maximum sustainable PPA payment = MAX(0, cash available) ÷ coverage buffer (default 1.2x)

Offtaker Payment Capacity Gap = MAX(0, PPA bill − maximum sustainable payment)
```

The gap is then routed in this order:

1. to a **government budget backstop**, if the control switch is on;
2. otherwise to a **sovereign PPA guarantee call**, if the structure has one;
3. otherwise to **unpaid arrears** to the IPP, which reduce project cash revenue and therefore DSCR.

### 8.3 What breaks the utility

**Worked results (Lumora, PPP).**

- **Base case.** Payment capacity is about 2.0x the PPA bill in the first ten years, with no gap.
- **Offtaker stress.** Collections fall 8 percentage points from COD, government transfers are cut 30%, and the retail tariff is frozen for 5 years. Payment capacity falls to zero within ten years, and the lifetime gap reaches about USD 5.5 bn in nominal terms. With the budget backstop on, fiscal NPV moves from about +USD 28 m to about −USD 1.24 bn.
- **FX step devaluation of 50% at COD.** With a USD-denominated PPA and local-currency retail tariffs, payment capacity falls to about 0.44x. The lifetime gap is about USD 1.17 bn, and fiscal NPV is about −USD 412 m.

**Interpretation (analyst inference).** In the fictional base case, the utility's cash margin before the new PPA is roughly 15–20% of collections. A permanent price shock, whether a tariff freeze or a devaluation without pass-through, compounds over a 30-year PPA. The project still looks fine to its own lenders, because the shortfall is paid by the state. This is the mechanism through which "bankable" projects create unsustainable liabilities.

> **In the model:** `11_OFFTAKER`, `12_UTILITY`, `16_REVENUE` (section C), stresses `st_offtaker`, `st_fx`; Gate 5.

## Chapter 9. Regulation as a bankability input

The model's Regulatory Bankability Matrix scores 16 items, each as READY, PARTIAL, GAP or CRITICAL GAP:

- electricity law
- generation licence
- water rights
- concession
- PPP law
- IPP framework
- PPA enforceability
- tariff regulation
- regulator independence
- grid access
- grid code
- environmental permits
- land rights
- FX convertibility
- tax regime
- repatriation

It is a **development-readiness screen, not legal advice**. Gate 6 converts the counts of GAP and CRITICAL GAP items into a status.

The case files show that governance and procurement failures stop more projects than technical failures do:

- On Gibe III, the no-bid contract led multilateral lenders to withdraw, and financing moved to ICBC [A1 S53–S55].
- Bujagali's first attempt collapsed after export-credit-agency withdrawal and corruption probes [A2 S48].
- The Batoka direct award was revoked and re-tendered [A2].

**Analyst inference.** Transparent, competitive procurement is itself a bankability condition.

> **In the model:** `13_REGULATION`; Gates 6 and 9.

## Chapter 10. The PPA: allocating hydrology, volume, currency and termination risk

### 10.1 The two-part tariff

A **capacity (availability) charge** in USD/kW-month pays for fixed costs, including debt service, as long as the plant is available. An **energy charge** in USD/MWh pays for delivered energy. The larger the capacity share, the less hydrology risk the IPP bears and the more the utility bears. Lumora's capacity share of lifetime billed revenue is about 71%.

### 10.2 Volume clauses

- **Deemed energy** pays for curtailment the seller did not cause (grid, transmission, demand).
- **Take-or-pay** sets a minimum annual payment.

Both turn system risk into utility risk.

### 10.3 Currency

A USD-denominated tariff transfers FX risk to a utility whose revenue is in local currency. The model's `lc_share` input lets the user denominate part of the tariff in local currency and index it to local CPI. Nachtigal's 21-year local-currency tranche, guaranteed by IBRD, shows that local-currency debt can lengthen tenor and reduce mismatch [SD PF-11; A2 S1–S6].

### 10.4 Termination

Termination payments for government default or political force majeure typically cover outstanding debt plus some equity compensation. In the model the exposure is debt outstanding plus unrecovered private equity × (1 + premium). This is usually the largest single contingent liability in an IPP: for Lumora under the PPP structure, roughly USD 0.96 bn at COD in the closed-form comparison.

> **In the model:** `14_PPA`, `15_TARIFF`, `16_REVENUE`, `23_GUARANTEES` (x_term).

---

# PART V: THE FINANCE LAYER

## Chapter 11. Project finance for hydro: sizing, sculpting and the lender case

### 11.1 Tenor is the strongest tariff lever

Brookings notes that debt tenors for African hydro are rarely longer than 15–18 years [SD PF-13]. Nachtigal's tranches ran 18 years (EUR) and 21 years (local currency), with about 6 years of grace [SD PF-11].

Bujagali's short original tenor front-loaded capacity charges. The 2018 refinancing extended maturity and cut tariffs, at the cost of a corporate-tax waiver [A2 S48–S54].

**Analyst inference.** For a 50–100-year asset, tenor matters more to the tariff than any other single financing lever.

### 11.2 Sculpting without circularity

The model sizes commercial debt by sculpting. Debt service in each year equals lender-case CFADS ÷ target DSCR, minus concessional debt service. Debt capacity is the present value of that stream at the commercial rate.

To avoid circular references:

- interest during construction, upfront fees and the initial DSRA are equity-funded;
- lender-case tax uses depreciation that excludes IDC and fees.

Both are documented simplifications. For stress testing, the user can **lock** the debt amount and switch to an annuity profile, as lenders do when a downside case is run against a fixed package.

### 11.3 Covenants

The only institutional covenant evidence found in our research is project-specific. Nachtigal's lenders' base case showed a minimum DSCR of 1.45x and an average of 1.53x, described as consistent with precedents [SD PF-11]. The model's sizing DSCRs (1.20x–1.35x by structure) and lock-up (1.10x) are therefore **user inputs**, not sourced norms.

### 11.4 Lumora results (PPP structure, base)

| Metric | Value |
|---|---|
| Plant CAPEX, nominal | about USD 1,110 m |
| Total uses | about USD 1,282 m |
| Senior debt | about USD 833 m (75% of the funding base) |
| Debt capacity | about USD 905 m |
| Minimum DSCR | 1.96x |
| LLCR | about 1.29x |
| Project IRR | 9.7% |
| Private equity IRR | 14.9% (vs a 15% target) |
| Financing gap | about USD 61 m (private equity required beyond the 20% available) |

> **In the model:** `17_PROJECT_FINANCE`, `18_DEBT`, `19_EQUITY`, `20_CASH_FLOW`, `21_TAX`; Gate 7.

## Chapter 12. Five structures, one project

`17A_STRUCTURES` holds five financing structures for the *same* plant:

1. **Public:** SOE, with debt borrowed by the sovereign.
2. **IPP:** private BOOT.
3. **PPP:** SOE plus private sponsor, backed by DFIs.
4. **Hybrid:** public civil works, with private E&M and O&M.
5. **Blended finance:** grants, concessional debt and private capital.

The closed-form screen and the full-engine snapshot (both in the model) show four things.

1. **The required tariff depends on the cost of capital.** In the closed-form screen, the levelised tariff needed to recover costs ranges from about USD 53/MWh (hybrid, with a 35% public capital contribution) through about USD 58/MWh (public) and about USD 69/MWh (PPP) to about USD 92/MWh (IPP).
2. **Gross public exposure at COD barely changes.** It is about USD 1.11–1.16 bn in every structure, roughly 3.2–3.3% of GDP. The public structure carries it as direct debt. The IPP carries it as a termination obligation plus PPA guarantee. The PPP and blended structures carry it as a mix of public capital, guaranteed debt and termination exposure.
3. **Grants without a tariff adjustment are a windfall.** In the full engine at the *same* PPA tariff, the hybrid structure's private equity IRR jumps to about 26%, while fiscal NPV falls to about −USD 294 m. A grant or VGF must be matched by a lower tariff, or by an explicit return cap, or it transfers public money to private equity.
4. **Public ownership at an IPP tariff is fiscally positive but costly to consumers.** The public structure's fiscal NPV is about +USD 416 m at the same tariff, because the state receives all equity returns. Consumers pay the IPP-level PPA tariff (blended about USD 109/MWh in operating year 2), roughly USD 50/MWh above the public structure's closed-form cost-recovery tariff.

**Analyst inference.** No structure is costless. The right question is not "PPP or public?" but "Which combination of tariff, public capital and risk transfer minimises total cost to consumers and taxpayers within acceptable fiscal exposure?"

> **In the model:** `17A_STRUCTURES` (library, closed-form comparison, full-engine snapshot); control switch `structure`.

---

# PART VI: THE PUBLIC-FINANCE LAYER

## Chapter 13. Direct support and contingent liabilities

### 13.1 Direct exposure

Direct exposure is cash the state actually spends:

- government equity;
- grants, VGF or public capital contributions;
- public transmission CAPEX and O&M;
- budget support to the utility to cover the offtaker gap.

### 13.2 Contingent liabilities

Contingent liabilities are payments the state may have to make:

- debt guarantees or counter-indemnities;
- sovereign PPA payment guarantees;
- termination payments;
- FX convertibility undertakings;
- minimum revenue guarantees.

MDB guarantees do not remove these exposures. An IBRD or IDA guarantee is backed by a sovereign indemnity. Bujagali's IDA PRG of up to USD 115 m came with a Uganda–IDA Indemnity Agreement dated 18 July 2007 [A2 S53]. Nachtigal's IBRD payment guarantee (EUR 86 m) and loan guarantee (EUR 171 m) [A2 S3] work the same way.

### 13.3 Three measures, kept separate

1. **Maximum simultaneous exposure** = MAX(termination; debt guarantee + PPA guarantee) + FX cover. Guarantees are not added on top of termination, because termination would replace them.
2. **Deterministic calls in the active scenario.** Guarantee and backstop payments the model actually computes under the chosen stress.
3. **Expected loss** = user-entered annual probabilities × exposure × loss given call. It is labelled "user judgement, not calibrated default probabilities". The model never presents an expected value as a forecast.

For calibration, the IMF dataset by Bova et al. puts the average fiscal cost of a realised contingent liability at about 6% of GDP. The breakdown by type, about 1.2% for PPPs and about 3% for SOEs, was seen only in a snippet [SD FR-13]. Between 24% and 41% of power PPP contracts are renegotiated [SD FR-17].

> **In the model:** `22_GOVERNMENT_SUPPORT`, `23_GUARANTEES`, `24_CONTINGENT_LIABILITIES`, `25_FISCAL_IMPACT`.

## Chapter 14. Project-level fiscal exposure screening

The IMF–World Bank LIC-DSF uses debt-carrying-capacity thresholds. Examples:

- PV of PPG external debt / GDP of 30/40/55%, and PV of total public debt / GDP benchmarks of 35/55/70% (weak/medium/strong) [SD FR-09].
- Contingent-liability stress shocks, including 2% of GDP for SOEs and 35% of the PPP capital stock where that stock exceeds 3% of GDP [SD FR-09].

PFRAM 2.0 is the standard tool for assessing the fiscal costs and risks of PPPs [SD FR-01–FR-03].

The book's screen **does not replace these tools**. It asks a narrower question: *does this single project add material fiscal pressure?* It reports:

- peak on-budget increment to debt/GDP (direct debt plus cumulative outlays);
- peak contingent exposure / GDP;
- peak annual government cash requirement / revenue;
- whether the project pushes public debt above the user's benchmark.

These are combined with the latest published DSA risk rating to give **LOW**, **MODERATE** or **HIGH** additional fiscal pressure. All thresholds are editable and labelled as screening conventions.

**Worked result.** In the base case, Lumora screens as MODERATE. Contingent exposure peaks at about 2.6% of GDP and the annual cash requirement at about 1.9% of revenue. The +27% CAPEX overrun, the low case and the offtaker and FX stresses all move the screen to HIGH.

> **In the model:** `26_DEBT_SUSTAINABILITY`; Gate 8.

---

# PART VII: DECISION

## Chapter 15. Risk allocation: who really bears what

`29_RISK_ALLOCATION` maps 16 risks across 8 parties:

- **Parties:** government, developer, EPC, lender, utility, consumer, insurer, DFI.
- **Risks:** hydrology, construction, cost overrun, delay, demand, offtaker, tariff, FX, interest rate, political, regulatory, transmission, grid, E&S, force majeure, termination.

For each risk, it asks whether the risk can be mitigated by contract, and links it to the model stress that quantifies it.

Mitigation instruments (descriptions from sources):

- MIGA non-honoring of sovereign financial obligations cover [SD PF-03];
- World Bank guarantees [SD PF-01, PF-02];
- the ATI Regional Liquidity Support Facility, up to 12 months of revenue (seen in snippet only) [SD PF-04];
- AfDB partial risk guarantees, e.g. Sahofika [SD PF-06].

Most of these move risk to the sovereign or to an MDB backed by the sovereign. The matrix counts how many risks the government bears as primary bearer.

## Chapter 16. The Hydropower Bankability Framework™

### 16.1 Design principles

1. **Explainable:** every test is a named metric with three visible thresholds.
2. **Auditable:** every metric links to a model cell.
3. **No hidden weights:** a gate takes the status of its weakest test.
4. **Editable:** thresholds are inputs, labelled illustrative.

### 16.2 The nine gates

| Gate | Tests |
|---|---|
| 1 Resource | Flow-record years; P90/P50; hydrology study maturity |
| 2 Demand | Bankable/contracted demand (worst of years 1–5); share of system peak |
| 3 Configuration | Unit CAPEX vs benchmark; capacity factor; feasibility maturity |
| 4 Transmission | Evacuation/installed at COD; transmission lag; transmission financing secured |
| 5 Offtaker/Utility | Payment capacity/PPA (worst of years 1–10); collection rate; payment-security months |
| 6 Regulation/PPA | CRITICAL GAP count; GAP count; fixed revenue share |
| 7 Financing | Minimum DSCR; financing gap/uses; equity IRR vs target |
| 8 Public finance | Peak cash need/revenue; peak contingent exposure/GDP; DSA rating |
| 9 E&S/Sustainability | ESIA/lender-standard compliance; RAP status; transboundary issues |

Statuses: **READY** (3), **CONDITIONAL** (2), **DEVELOPMENT GAP** (1), **CRITICAL GAP** (0). The overall verdict is:

- NOT BANKABLE, if any gate is at CRITICAL GAP;
- otherwise NOT YET BANKABLE, if any gate is at DEVELOPMENT GAP;
- otherwise BANKABLE SUBJECT TO CONDITIONS, if any gate is CONDITIONAL;
- otherwise READY FOR FINANCIAL CLOSE.

The dashboard ranks the gates and shows the **top 5 bankability gaps** and **top 5 actions before financial close**.

**Lumora base result.** NOT YET BANKABLE. Four gates are at DEVELOPMENT GAP:

- Gate 4: transmission financing not secured;
- Gate 5: utility collection rate (88%) and payment security (4 months) below the thresholds;
- Gate 6: four regulatory items at GAP (tariff pass-through, grid code, land, FX convertibility);
- Gate 8: peak contingent exposure about 2.6% of GDP and cash requirement about 1.9% of revenue.

The remaining gates are CONDITIONAL. Each gap comes with a specific pre-close action.

## Chapter 17. Ten rules for financial close without unsustainable liabilities

*(Analyst synthesis of the evidence in Chapters 1–16.)*

1. Size and price on P90 *and* test multi-year drought. Do not stop at single-year P90.
2. Budget against the reference class. A median overrun of +27% is a base expectation, not a stress [SD HY-08].
3. Finance the line with the plant: same close, same timetable, explicit deemed-energy allocation.
4. Compute the offtaker's maximum sustainable PPA payment before negotiating the tariff.
5. Match currency: local-currency tranches, partial local-currency tariffs, or explicit FX risk-sharing.
6. Treat every guarantee as public debt-in-waiting. Record it, cap it and disclose it [SD FR-04, FR-08].
7. Tie every grant or VGF to a tariff reduction or a return cap.
8. Aggregate across the whole PPA portfolio. One project may pass the screen while the portfolio fails it (the Lao lesson [INT S13]).
9. Make procurement transparent and competitive. It determines who will lend (Gibe III, Bujagali, Batoka).
10. Close only when no gate is at CRITICAL GAP and the fiscal screen has been signed off by the Ministry of Finance.

---

## Annex A. Case library summary

See `case_library/README.md` and `model/31_CASE_STUDY`. The full A–AD field files are in `research/case_studies/`.

## Annex B. Benchmark ranges

See `research/source_database.md`, section "BENCHMARK RANGES FOR MODEL DEFAULTS": 31 parameters, each with source ID and confidence level.

## Annex C. Glossary (selected)

| Term | Meaning |
|---|---|
| CFADS | Cash flow available for debt service |
| DSCR | CFADS ÷ senior debt service for the period |
| LLCR / PLCR | PV of CFADS over the loan life / project life ÷ debt outstanding |
| DSRA | Debt service reserve account |
| Deemed energy | Energy paid for but not delivered, because of curtailment not caused by the seller |
| PRG | Partial risk guarantee (e.g. IDA/IBRD, AfDB) |
| NHSFO | MIGA non-honoring of sovereign financial obligations cover |
| VGF | Viability gap funding |
| PFRAM | IMF/World Bank PPP Fiscal Risk Assessment Model |
| LIC-DSF | IMF/World Bank Debt Sustainability Framework for Low-Income Countries |
| Quasi-fiscal deficit | The gap between a utility's efficient cost recovery and its actual revenue, borne implicitly by the state [SD UT-02] |

## Annex D. Model map

See `manual/USER_MANUAL.md`, section 3.

---

*Disclaimer: This manuscript is for education and analysis. It is not investment, legal, tax or accounting advice. All Lumora/Navaria data are fictional. Case data are drawn from public sources as cited; where marked "snippet" or "PUBLIC DATA NOT FOUND", they should be verified before reliance.*
