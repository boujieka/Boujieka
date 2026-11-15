# Clean Cooking Market Assessment: Six Central African Countries

**Cameroon · DR Congo · Republic of Congo · Chad · Burundi · São Tomé and Príncipe**
Comparing LPG, eCooking, bioethanol, biogas and carbon-linked models, with a focus on bundling eCooking into mini-grid and solar home system (SHS) business models.

*Prepared 15 November 2026. Desk study. No primary data collection, no interviews.*

---

## How to read this document

Every claim carries one of four labels:

| Label | Meaning |
|---|---|
| **[V]** Verified | Taken from a named source retrieved during this study (listed in §10). |
| **[I]** Inference | My reasoning from verified facts. The logic is shown. |
| **[A]** Assumption | An input I chose because no source was found. Change it and the result changes. |
| **[O]** Opinion | My analytical judgment, mainly the scores in §6. Others may reasonably disagree. |

Anything I could not verify is stated as such and not filled in.

---

## 1. Executive summary

1. **The access gap is very large and very uneven** [V]. Clean cooking access in 2024 (World Bank WDI): Republic of Congo 40%, Cameroon 32%, Chad 11%, São Tomé and Príncipe 7%, DRC 5%, Burundi 0% (rounded). Together that is roughly 155 million people without clean cooking [I: population × (1 − access rate)]. Most of them are in the DRC (about 107 million).

2. **LPG is the incumbent in the two "middle-access" markets (Cameroon, Republic of Congo)** [I]. In both, a state-fixed cylinder price is held up by subsidies and undermined by recurring shortages. LPG scales, but its affordability depends on fiscal support that the IMF has criticised [V]. Since mid-2026 it has also been exposed to the import price shock that followed the closure of the Strait of Hormuz [V, reported].

3. **eCooking has the strongest structural case wherever the electricity access rate is far above the clean cooking access rate.** That describes São Tomé and Príncipe (78% vs 7%), Cameroon (72% vs 32%) and urban eastern DRC [V for the rates, I for the conclusion]. The best evidence for the region comes from Goma, DRC. On the Virunga Energies hydro mini-grid, fully subsidised electric pressure cookers (EPCs) reduced charcoal use by about 30% and saved households more than $8/month. About 85% of households kept using them when the full equipment cost was covered [V].

4. **Bundling eCooking into mini-grids works commercially only when three conditions hold** [I, from the Tanzania and Goma evidence]:
   - the marginal tariff for cooking energy is far below the typical solar-hybrid mini-grid tariff;
   - cooking load fills spare capacity, as it does on hydro or oversized solar systems;
   - the appliance is financed or subsidised.

   Where these do not hold (for example a Tanzania pilot with mini-grid tariffs of $0.55–0.85/kWh), cooking fell off and the operator's finances were strained [V].

5. **Bundling eCooking into standard SHS is not viable at today's typical system sizes** [I]. Full EPC cooking needs roughly 1 kWh/day [A]. That implies about 300+ Wp of PV plus storage [I, engineering arithmetic], several times a typical PAYG SHS. I found no DRC SHS–EPC bundle on the market: Bboxx's DRC cooking offer is PAYG LPG, not electric [V].

6. **Bioethanol and biogas are niche in all six countries** [I]. I found one bioethanol initiative, a WESAF sugarcane pilot in South West Cameroon described only in company-sourced material [V], and no verifiable national biogas programme data for any of the six.

7. **Carbon finance is now a quality filter, not just a subsidy** [I]. The ICVCM has approved, with conditions, Gold Standard's *Metered & Measured Energy Cooking Devices* methodology [V]. This favours metered eCooking on mini-grids, where smart meters already exist. ICVCM conditions push fNRB values typically below 0.5, against a market average of 0.86 [V], which roughly halves per-stove credit volumes for many legacy biomass-stove projects [I]. Article 6.4 has issued its first credits, from a cookstove project in Myanmar [V]. Burundi has filed host-party participation paperwork listing clean cooking as eligible [V].

**Bottom-line ranking for investment readiness** [O]:
1. Cameroon
2. Republic of Congo (LPG) and DRC (eastern urban eCooking on mini-grids), roughly tied
3. São Tomé and Príncipe: an excellent ratio but a tiny market
4. Chad
5. Burundi

---

## 2. Baseline indicators (verified)

Source: World Bank World Development Indicators, retrieved via the World Bank API on 15 Nov 2026 (dataset last updated 11 Nov 2026) [V].

| Country | Population (2025) | Clean cooking access (2024) | Electricity access (2024) | Rural electricity access (2024) | GDP per capita, current US$ (2025) | Electricity minus cooking gap (pp) [I] |
|---|---:|---:|---:|---:|---:|---:|
| Cameroon | 29.9 m | 32% | 72.0% | 42.7% | 1,972 | **40** |
| DR Congo | 112.8 m | 5% | 22.5% | 1.0% | 807 | 17.5 |
| Republic of Congo | 6.5 m | 40% | 53.0% | 19.4% | 2,515 | 13 |
| Chad | 21.0 m | 11% | 13.4% | *100% (data error, see below)* | 1,022 | 2.4 |
| Burundi | 14.4 m | 0% (rounded) | 20.1% | 3.6% | 234 | 20 |
| São Tomé and Príncipe | 0.24 m | 7% | 77.7% | 75.1% | 4,084 | **71** |

**Data-quality warnings** [V/I]:
- **Chad, rural electricity 100%.** This is almost certainly an error in the API record: national access is 13.4%, and Chad is majority rural. Do not use it.
- **Burundi, clean cooking 0%.** This is a rounded value (the indicator is published at 0 decimals). The true figure is probably below 0.5%, not literally zero. The SEforALL 2025 deep-dive snippet I retrieved mentions "Chad and Burundi (12 percent)". I could not see the full sentence, so its meaning (which indicator, which year) is unclear. Treat it as unreconciled.
- **Chad, clean cooking 11% vs 3%.** WDI gives 11%, but a WFP publication says "only 3%" [V]. They likely use different years or definitions. Unreconciled.
- **DRC, 5% vs 1%.** WDI gives 5% (all clean fuels). The Clean Cooking Alliance DRC dashboard says about 1% regularly use LPG or electric [V]. These can both be true if most "clean" users in WDI rely on other fuels or use them irregularly.

**Why the gap column matters** [I]: the electricity-minus-cooking gap is the share of the population that already has an electricity connection but still cooks with polluting fuels. That is the addressable base for eCooking without building new generation infrastructure. São Tomé and Príncipe and Cameroon stand out. In Chad the gap is near zero, so eCooking there means building electricity access first.

---

## 3. Technology-by-technology assessment

### 3.1 LPG

**Verified market facts**
- **Cameroon** [V]:
  - The official price of a 12.5 kg cylinder is 6,500 FCFA; one April 2025 report cites 6,697 FCFA.
  - The Hydrocarbon Price Stabilisation Fund (CSPH) absorbs an estimated real-cost gap of 3,500–4,500 FCFA per bottle.
  - LPG subsidies were 52.6 bn FCFA in 2024 and 48.96 bn FCFA budgeted for 2025, with 36.9 bn FCFA injected by 30 September 2025.
  - In late 2025, shortages linked to the distributor SCTM pushed parallel-market prices as high as 13,000 FCFA. In Kumba prices were 7,500–10,000 FCFA.
  - A new filling plant in Bamenda was reported to cut local prices by 18%.
  - Cameroon tendered for 60,000 t of LPG imports.
- **Republic of Congo** [V, secondary reporting]:
  - A regulated cylinder price of 6,400 FCFA, set by a 2018 order, is under pressure; distributors' costs reportedly imply about 8,300 FCFA.
  - Authorities sanctioned a distributor (FAAKI) for raising prices in January 2026.
  - Shortages were reported in September 2023 and January 2025.
  - The national refiner CORAF produces butane and supplies about 70% of national petroleum product demand.
  - In July 2025 the IMF criticised the country's petroleum subsidies as inefficient.
- **Chad** [V, partial]:
  - An ARSAT communiqué dated 15 December 2025 reportedly removed the subsidy on butane kits (cylinder and accessories) but kept refill prices fixed, at 1,000 FCFA for 3 kg. I saw only a snippet of this.
  - Subsidy costs for gas imports reportedly rose about elevenfold in ten years.
  - WFP and UNHCR introduced LPG to more than 5,000 refugee families in six eastern camps from 2022. WFP found that fuel supply and cost were the main barriers.
- **DRC** [V]: LPG consumption was about 25,000 t in 2025, very low for more than 100 million people. Bboxx has run PAYG smart-meter LPG pilots there.
- **Burundi** [V]: there is a chronic fuel crisis dating from late November 2023, driven by foreign-exchange shortages. Reserves were about $214 m (about 1.6 months of imports) at end-2025. Urban charcoal prices have doubled or tripled (FEWS NET, May 2026). I found no LPG price or volume data.
- **Global shock** [V, reported]: following the Strait of Hormuz closure (reported in May 2026), African LPG import prices were reported at 70–100% above their 2025 average in East and West Africa. Some East African users reportedly reverted to polluting fuels. I could not retrieve the full article text, so I cannot confirm country-specific effects for these six.

**Illustrative affordability** [A + I]
- **Assumption** [A]: a household using LPG as its main fuel consumes about one 12.5 kg cylinder per month. Real use varies with household size and fuel stacking.
- **Cameroon at the official price**: about 6,500 FCFA/month, or roughly $11/month [A: about 590 FCFA/USD; the FCFA is pegged to the euro, so the USD rate moves].
- **Cameroon at the parallel-market price**: about 13,000 FCFA, roughly $22/month, double the official cost.
- **Unsubsidised cost** [I]: official price plus the 3,500–4,500 FCFA gap, about 10,000–11,000 FCFA (about $17–19) per cylinder.
- **Implication** [I]: LPG affordability in Cameroon and the Republic of Congo is a policy artefact. Once subsidy is removed, or supply fails, the cost to households can roughly double.

**Assessment**
- **Affordability** [I]: medium where subsidised and in supply. Low and volatile otherwise.
- **Scalability** [I]: high in Cameroon and the Republic of Congo, which already have infrastructure, distributors and urban demand. Low in Chad, Burundi and the DRC interior, where import logistics, foreign exchange and the cost of cylinder deposits are the bottlenecks. In São Tomé and Príncipe everything is imported by sea in tiny volumes.
- **Investment readiness** [O]: Cameroon is the highest, with bankable filling-plant and distribution infrastructure, although subsidy arrears and price controls compress margins. The Republic of Congo has domestic butane supply from CORAF but price-control risk. Elsewhere readiness is low.
- **Main risks** [I]: fiscal subsidy reform, foreign-exchange shortages (acute in Burundi), import price shocks (2026), and the fact that regulated prices cap distributor margins.

### 3.2 eCooking (grid, mini-grid, SHS)

**Verified evidence**
- **Goma, DRC (Virunga Energies hydro mini-grid)** [V]:
  - A randomised trial started in July 2022, planned around 1,000 fully subsidised EPCs, with a pre-registered sample of 1,500 households. Some households also received a $5 electricity voucher.
  - Results: about 30% less charcoal, saving the average household more than $8/month. About 85% durable adoption when the equipment was fully paid for.
  - The free top-up raised early usage but not long-run usage.
  - 92% of Goma households cook mainly with charcoal. Virunga Energies built four hydro plants between 2014 and 2019.
  - A three-year follow-up has a pre-analysis plan dated January 2026.
- **Tanzania mini-grid pilot (A2EI, MECS, PowerGen, 2020–21)** [V]:
  - 100 EPC users at six sites.
  - Regulators blocked daily low-tariff cooking bundles and required per-kWh billing. That tariff did not cover costs, which strained the operator's finances, and cooking declined over the pilot.
- **Tariff economics (Tanzania review, 2023)** [V]:
  - Solar-hybrid mini-grid tariffs were $0.55–0.85/kWh in 2020, with a cost-viability gap of up to $11/month. 100% eCooking was not cost-effective at those tariffs.
  - Tariffs of $0.25–0.38/kWh were *projected* to make it viable for some peri-urban customers by 2025. That is a projection, not an observed outcome.
  - "Load factor ↑ = tariff ↓."
- **Network headroom** [V]: MECS modelling suggests about 15% of mini-grid households could move to a "clean stack" within typical load conditions.
- **Grid policy precedent** [V]: in 2022 Uganda introduced a cross-subsidised domestic eCooking tariff. It is a grid example, not one of the six countries, but it is a template regulators can copy.

**Illustrative mini-grid economics** [A + I]

Assumption [A]: an EPC-led household cooks with 0.6–1.2 kWh/day, about 18–36 kWh/month. Actual use depends on menu, household size and whether the EPC is used for staples like beans. Calibrate this against MECS cooking-diary data before using it in a model.

| Tariff ($/kWh) | Monthly cooking energy cost [I] | Compared with Goma's verified saving of >$8/month on charcoal |
|---|---:|---|
| 0.85 (high-end solar-hybrid mini-grid) | $15–31 | Clearly worse than charcoal |
| 0.55 | $10–20 | Worse |
| 0.38 | $7–14 | Roughly break-even |
| 0.25 | $4.5–9 | Better |
| 0.10 (hydro or cheap grid) | $1.8–3.6 | Much better |

**What follows from the table** [I]:
- eCooking on a mini-grid pays for the household only at a dedicated cooking tariff of roughly $0.25/kWh or less.
- That price is reachable when cooking uses energy that would otherwise be wasted: daytime solar surplus, run-of-river hydro, or spare capacity on oversized systems.
- At the typical solar-hybrid tariff it is not affordable.
- This is why hydro-based eastern DRC (Goma, and potentially Bukavu and Butembo, though I found no evidence for those two) is the strongest eCooking mini-grid niche in the region.

**SHS feasibility** [I, engineering arithmetic]
- PV needed ≈ 1 kWh/day ÷ (about 4.5 peak-sun-hours × about 70% system efficiency) ≈ 320 Wp. Battery storage of about 1 kWh or more is needed if cooking happens in the evening.
- That is several times a typical PAYG SHS (tens of Wp to roughly 100–200 Wp) [A, general market knowledge, not verified here].
- **Conclusion**: SHS + EPC is a premium, high-upfront-cost product. It suits peri-urban, salaried or commercial customers, not mass-market rural households.
- **More realistic SHS bundle**: a partial-cooking appliance (a small EPC used for one or two dishes a day, or an efficient induction plate used at midday) plus LPG or an improved stove as the backup "stack".

**Country fit**
- **São Tomé and Príncipe**: about 78% of people already have electricity, so eCooking needs no new connections. But I believe generation is largely diesel [A, not verified in this study], so the utility's marginal cost may be high. The business case depends on solar additions and tariff policy.
- **Cameroon**: 72% electricity access and 43% rural access give a large addressable base. Grid reliability data was not retrieved, so this is an unknown.
- **Republic of Congo**: a moderate electricity-minus-cooking gap of 13 points. Subsidised LPG competes directly.
- **DRC**: the gap of 17.5 points is concentrated in a few cities. Rural electricity access is 1%. Eastern hydro mini-grids are the strongest niche.
- **Burundi**: there is a 20-point gap, but low incomes (GDP per capita $234) make appliance finance the binding constraint.
- **Chad**: there is almost no gap, so eCooking requires building new access first.

### 3.3 Bioethanol

- **Verified** [V]:
  - WESAF Energy runs a sugarcane-ethanol pilot at Inokun, Manyu Division, South West Cameroon.
  - It has a larger 322 ha plan with $38 m capex, aimed mainly at sustainable aviation fuel (SAF). It plans to dedicate 5–10% of output to cooking fuel.
  - These are company claims; I found no independent evaluation.
  - FAO and the Global Bioenergy Partnership (GBEP) caution that domestic bioethanol for cooking "is neither feasible nor appropriate in all contexts."
- **Not found**: any bioethanol cooking programme in the DRC, Republic of Congo, Chad, Burundi or São Tomé and Príncipe.
- **Assessment** [I]:
  - **Affordability and supply**: unproven. The fuel competes with higher-value uses (SAF, beverages, industry).
  - **Scalability**: low in the near term.
  - **Investment readiness**: very low.
  - **Possible exception**: Cameroon, if a sugar producer builds a dedicated cooking-ethanol line. Candidates would be the existing sugar estates; I did not verify which firms or their interest.

### 3.4 Biogas

- **Verified**: nothing specific to these six countries was found in this study.
- **Background, not verified here**: domestic biogas typically requires households with several cattle kept in stalls and reliable water access, which limits it to a small agrarian segment.
- **Assessment** [I/O]:
  - It is a niche fit for institutional uses (schools, prisons, abattoirs, agro-processors), not mass-market household cooking.
  - It may fit parts of Burundi's dense smallholder livestock areas and Cameroon's Western Highlands, but this is a hypothesis to test, not a finding.
  - **Investment readiness**: low.

### 3.5 Carbon-linked models

**Verified facts**
- **ICVCM CCP approvals (2025)** [V]:
  - Gold Standard's *Metered & Measured Energy Cooking Devices* methodology (v1–1.2) was approved with conditions.
  - Gold Standard's TPDDTEC methodology was approved for v4 in February 2025 and for v2, 3 and 3.1 in June 2025.
  - Two improved-cookstove methodologies were rejected for weak quantification.
  - Conditions require fuel-use testing (KPT or CCT, or defaults with cross-checks). They also bring fNRB typically below 0.5, compared with a market average of 0.86.
  - Credits under approved methods were under 3% of available cookstove credits at end-2024.
- **Article 6.4 (UN Paris Agreement Crediting Mechanism)** [V]: its first issuance was 60,000 credits from a cookstove project in Myanmar, reported in February 2026.
- **Burundi** [V]:
  - It has filed an A6.4 host-party form. The designated national authority is IGEBU, and clean cooking (including improved biomass and LPG stoves) is listed as eligible.
  - In June 2025 a consultancy announced it was seeking a partner for a Burundi clean cooking project billed as the "world's largest ever carbon finance project". I found no follow-up.
- **Prices**: I found no cookstove-specific CCP price data. Analysts say high-integrity credits sell at a premium of at least double the market average [V, MSCI via secondary source]. No dollar figure is given here because none was verified.

**Implications** [I]
- **Metered eCooking on mini-grids fits the new integrity regime naturally.** Smart meters measure the energy used directly, so there is no reliance on contested fNRB-based fuel-saving estimates. A mini-grid operator can generate monitoring data at near-zero marginal cost.
- **Legacy improved-biomass-stove carbon models face lower volumes and higher costs of monitoring, reporting and verification (MRV).** Under the conditions, lower fNRB means fewer credits per stove, roughly halving volumes when fNRB falls from 0.86 to under 0.5.
- **LPG carbon projects** depend on the baseline and methodology. Without a retrieved methodology decision for LPG under the CCP or Article 6.4, I cannot say whether LPG credits would get the CCP label.
- **Article 6 adds sovereign risk and opportunity.** It requires host-country authorisation and corresponding adjustments. Burundi is visibly preparing; I found no equivalent evidence for the other five, which does not mean they have not.

---

## 4. Bundling eCooking into mini-grid and SHS business models

### 4.1 Why bundle (the operator's view) [I]
- **Load factor.** Cooking adds kWh, often at midday and in the evening. For solar mini-grids with daytime surplus, a midday-cooking load lowers average cost per kWh. The Tanzania review states the relationship directly: load factor up, tariff down [V].
- **Average revenue per user (ARPU).** Household consumption on African mini-grids is typically low [A, general sector knowledge]. Cooking at 18–36 kWh/month [A] can multiply a household's consumption.
- **Carbon revenue.** Metered cooking kWh can be turned into credits under the CCP-approved metered methodology [V/I].
- **Churn and retention.** A household that cooks on the grid has a stronger reason to stay connected and pay [I, hypothesis].

### 4.2 Why bundles fail (verified failure mode) [V]
- In Tanzania, the regulator required per-kWh billing in place of cooking bundles. The tariff was not cost-reflective, cooking usage fell, and the operator's finances were strained.
- **Lesson** [I]: tariff design and regulatory approval are preconditions, not afterthoughts.

### 4.3 Bundle archetypes ranked for these six countries [O]

| Archetype | Description | Best fit | Key condition |
|---|---|---|---|
| **A. Hydro mini-grid + subsidised EPC + cooking tariff** | Operator distributes EPCs (subsidised by grants or carbon revenue) and offers a low marginal-kWh cooking tariff | Eastern DRC (Goma model), potentially hydro sites in Cameroon and Burundi | Spare hydro capacity; regulator accepts the tariff |
| **B. Solar-hybrid mini-grid + midday cooking tariff** | Time-of-use tariff steers EPC use into solar hours; carbon revenue co-finances the appliance | Cameroon rural mini-grids, São Tomé and Príncipe, Republic of Congo | Time-of-use metering; cooking behaviour shifts to midday (unproven) |
| **C. Utility grid + PAYG EPC + cooking tariff** | Appliance financier plus utility or regulator cooking tariff (Uganda-style) | São Tomé and Príncipe, urban Cameroon, Brazzaville | Grid reliability; utility cost of supply |
| **D. SHS + small EPC + LPG backup ("hybrid stack")** | Larger SHS (300 Wp or more) with partial eCooking, LPG for the rest | Peri-urban DRC, Cameroon | Customer credit; foreign-exchange risk on imported hardware |
| **E. Standard SHS + EPC** | Typical PAYG SHS with an EPC | Not recommended | Undersized systems [I] |

### 4.4 Indicative unit economics to model (inputs to calibrate, not results) [A]
- **Appliance cost**: EPC price landed in-country. Not verified in this study, so get local quotes.
- **Subsidy needed to reach about 85% adoption**: Goma covered the full equipment cost [V].
- **Cooking kWh per household per month**: 18–36 [A].
- **Marginal cost of supply**: hydro near zero (spilled water); solar during daytime surplus near zero; diesel at the generator's marginal cost.
- **Carbon revenue**: metered kWh × emission factor × credit price. Do not assume a price; get quotes from buyers of CCP-labelled credits.
- **Regulatory approval of a cooking tariff**: this is the gating item.

---

## 5. Country profiles

### Cameroon
- **Verified**:
  - 32% clean cooking, 72% electricity (42.7% rural), 29.9 m people.
  - Heavy LPG subsidy (48.96 bn FCFA in 2025) with chronic shortages and parallel-market prices up to 2×.
  - A Mission 300 compact endorsed in September 2025, with a reported 100% electricity-access target for 2030.
  - The WESAF ethanol pilot.
- **Inference**:
  - The largest absolute eCooking opportunity among grid-connected households in the group: a 40-point gap, about 12 m people [I].
  - Fiscal pressure on the LPG subsidy strengthens the policy case for eCooking as a hedge.
- **Unknowns**: grid reliability (outage frequency), the residential tariff, mini-grid regulation and the national clean cooking target. None were retrieved.

### DR Congo
- **Verified**:
  - 5% clean cooking (about 1% regular modern-fuel use per the Clean Cooking Alliance).
  - 22.5% electricity, 1% rural. 112.8 m people.
  - LPG consumption about 25,000 t (2025).
  - The Goma EPC trial results. Bboxx operates PAYG SHS and an LPG pilot.
  - A national clean cooking strategy was expected by end-2025, emphasising LPG, improved stoves and eCooking; I could not confirm that it was published.
  - The Mission 300 compact reportedly targets 62% electricity access by 2030.
- **Inference**:
  - The largest absolute market and the strongest eCooking evidence base, concentrated in the hydro-powered eastern cities.
  - Rural DRC is effectively unreachable by eCooking in the medium term.
- **Risks**: conflict in the east (Goma). The security situation directly affects operator assets; the current status was not assessed in this study. Also currency risk and governance.

### Republic of Congo
- **Verified**:
  - 40% clean cooking (the highest of the six), 53% electricity, 6.5 m people.
  - A regulated LPG price of 6,400 FCFA (2018 order) under cost pressure.
  - Domestic butane from CORAF.
  - IMF criticism of the subsidies.
- **Inference**: an LPG-led market. Its main opportunity is LPG distribution efficiency and the cylinder recirculation business. eCooking competes against subsidised LPG and needs a tariff signal.

### Chad
- **Verified**:
  - 11% clean cooking by WDI (3% by WFP), 13.4% electricity, 21 m people.
  - Removal of the butane-kit subsidy with refill prices kept fixed (December 2025, partially verified).
  - The WFP/UNHCR refugee LPG programme. A Mission 300 compact centred on decentralised renewables.
- **Inference**:
  - The humanitarian channel (refugee camps) is the most investable entry point. Institutional procurement reduces collection risk.
  - Mass-market eCooking requires new generation first.
  - LPG is the realistic near-term fuel, subject to import logistics (Chad is landlocked).

### Burundi
- **Verified**:
  - About 0% clean cooking (rounded), 20.1% electricity (3.6% rural), 14.4 m people, GDP per capita $234 (the lowest of the six).
  - A fuel crisis since late 2023, foreign-exchange reserves of about 1.6 months of imports, and urban charcoal prices up 2–3×.
  - An Article 6.4 host-party form filed. A Mission 300 compact endorsed in September 2025.
- **Inference**:
  - Imported fuels are structurally disadvantaged because of foreign-exchange scarcity.
  - Local-resource options (hydro-based eCooking, efficient biomass) plus carbon finance are the only scalable path. Even these need heavy grant or results-based finance because of very low purchasing power.
  - The charcoal price spike improves the relative economics of any alternative.

### São Tomé and Príncipe
- **Verified**:
  - 7% clean cooking (some sources: 4.6% in 2023), 77.7% electricity (75.1% rural), 0.24 m people.
  - A Mission 300 compact that includes clean cooking as a pillar; I could not retrieve its specific targets.
- **Inference**:
  - The best ratio for eCooking in the region: 71 points of the population are connected but do not cook cleanly.
  - The market is tiny, about 170,000 people [I]. It suits a utility- or donor-led national programme more than a venture-scale private business.
  - The economics depend on the utility's cost of generation [A: believed diesel-heavy, not verified].

---

## 6. Comparative scoring (opinion)

Scale: 1 = weak, 5 = strong. These are my judgments built from the evidence above, not measured values. Weights are not applied. Readers should weight the dimensions to fit their investment thesis.

### 6.1 Technology × dimension (regional view)

| Technology | Affordability | Scalability | Investment readiness | Comment |
|---|:-:|:-:|:-:|---|
| LPG | 3 | 4 | 3 | Proven, but subsidy- and import-dependent; 2026 price shock |
| eCooking: grid | 3 | 3 | 2 | Strong where the gap is large; needs a cooking tariff and reliability |
| eCooking: mini-grid bundle | 2 (3 on hydro) | 2 | 3 | Best evidence (Goma); tariff is the gating item |
| eCooking: SHS bundle | 1 | 2 | 2 | Undersized systems; premium niche only |
| Bioethanol | 2 | 1 | 1 | Single unproven pilot (Cameroon) |
| Biogas | 2 | 1 | 1 | Institutional niche |
| Carbon-linked (as enabler) | +1 to the technology it supports | — | 3 for metered eCooking, 2 for legacy biomass stoves | Integrity rules favour metered devices |

### 6.2 Country × technology (best-fit model per country)

| Country | Best near-term model [O] | Second model [O] | Readiness [O] |
|---|---|---|:-:|
| Cameroon | LPG distribution efficiency + grid eCooking pilots | Mini-grid eCooking bundles in rural concessions | 4 |
| DRC | Hydro mini-grid eCooking (east) | PAYG LPG (Kinshasa, Lubumbashi) | 3 |
| Republic of Congo | LPG (cylinder recirculation, distribution) | Urban grid eCooking | 3 |
| São Tomé and Príncipe | National grid eCooking programme | LPG import optimisation | 3 (small market) |
| Chad | Humanitarian LPG | Solar mini-grid with midday cooking (long-term) | 2 |
| Burundi | Carbon-financed efficient biomass + hydro eCooking pilots | Institutional biogas | 1–2 |

---

## 7. Key risks across the portfolio [I]

1. **Tariff and regulatory risk.** Cooking tariffs need regulator approval, and the Tanzania precedent shows bundles can be blocked [V].
2. **Subsidy reform risk for LPG.** It cuts both ways: removing the subsidy improves the relative economics of eCooking, but can push households back to charcoal.
3. **Foreign-exchange and import risk.** Acute in Burundi, significant elsewhere. EPCs, PV and LPG are all imported.
4. **Carbon market risk.** Price and volume uncertainty, ICVCM eligibility of legacy credits (more than 28 m cookstove credits under older Gold Standard versions were still pending [V]), and Article 6 authorisation timelines.
5. **Security risk.** Eastern DRC (the best eCooking evidence site) and eastern Chad.
6. **Data risk.** Baseline indicators conflict across sources (see §2). Market sizing should use ranges, not point estimates.

---

## 8. Recommendations [O]

1. **Lead with Cameroon and eastern DRC** for eCooking–mini-grid bundling pilots. Structure each pilot as: subsidised EPC (carbon-financed under the metered methodology) + regulator-approved cooking tariff + smart-meter MRV.
2. **Treat LPG as the backbone of the urban "stack"** in Cameroon and the Republic of Congo. Invest in supply security (filling plants, cylinder recirculation) rather than in price.
3. **Do not launch mass-market SHS + EPC bundles.** If SHS companies participate, offer premium systems of 300 Wp or more as a hybrid stack with LPG backup.
4. **In São Tomé and Príncipe, approach the utility and government** with a national eCooking programme, not a standalone private venture.
5. **In Burundi and Chad, use results-based and humanitarian finance channels.** Commercial readiness is low.
6. **Price carbon conservatively.** Model with fNRB below 0.5 for biomass projects and base metered eCooking revenue on measured kWh only.

---

## 9. What this study did not do and what would change its conclusions

**Not done**
- No primary surveys or interviews.
- No in-country price checks.
- National Energy Compacts were not read in full (clean cooking targets not retrieved).
- No grid reliability or tariff data.
- No EPC landed-cost quotes.
- No carbon credit price quotes.
- No security assessment.

**Would change the conclusions**
- **Measured cooking energy per household** (the key assumption [A]). If it is well below 0.6 kWh/day, SHS bundling becomes more feasible and mini-grid economics improve.
- **Actual mini-grid tariffs and the regulator's stance on cooking tariffs** in Cameroon and the DRC.
- **Grid reliability** in Cameroon and São Tomé and Príncipe. Frequent outages would undermine grid eCooking.
- **LPG subsidy reform** decisions in Cameroon or the Republic of Congo, and the duration of the 2026 LPG import price shock.
- **Carbon prices for CCP-labelled cookstove credits**, and whether the six countries authorise Article 6 transfers.
- **The security situation** in Goma and eastern DRC.

**Network note**: in this session, direct access to api.worldbank.org, mecs.org.uk and african.business was blocked. World Bank and some article data were retrieved through an intermediary scraping service. The MECS DRC eCooking Market Assessment PDF returned 404 at its previously indexed address, so its detailed DRC tariff findings are **not** included.

---

## 10. Sources

**Data**
- World Bank WDI via API: EG.CFT.ACCS.ZS, EG.ELC.ACCS.ZS, EG.ELC.ACCS.RU.ZS, SP.POP.TOTL, NY.GDP.PCAP.CD. https://api.worldbank.org/v2/ (retrieved 15 Nov 2026)
- SEforALL, Tracking SDG7 2025 deep dive: https://www.seforall.org/system/files/2025-12/SEforALL%20SDG7_TRACKING_2025-data_analysis.pdf
- Clean Cooking Alliance, DRC dashboard: https://cleancooking.org/market-intelligence-hub/national-markets-intelligence-dashboard/congo-democratic-republic/
- IndexMundi, São Tomé and Príncipe access to clean fuels: https://www.indexmundi.com/facts/s%C3%A3o-tom%C3%A9-and-principe/access-to-clean-fuels

**LPG**
- Cameroon:
  - https://ecomatin.net/cameroun-37-milliards-fcfa-mobilises-en-neuf-mois-pour-contenir-les-prix-du-gaz-domestique
  - https://cameroun24.net/article/75769-crise-du-gaz-au-cameroun-la-sctm-au-bord-du-gouffre-la-bouteille-de-12-5-kg-flambe-jusqua-13-000-fcfa.html
  - https://www.cameroononline.org/new-gas-filling-plant-in-bamenda-cuts-domestic-lpg-prices-by-18
  - https://mimimefoinfos.com/domestic-gas-access-to-expand-with-kumba-lpg-centre-launch/amp
  - https://africtelegraph.com/blog/le-cameroun-lance-un-appel-doffres-pour-60-000-tonnes-de-gpl/
- Republic of Congo:
  - https://fr.allafrica.com/stories/202601140230.html
  - https://blog.iambeezy.app/fr/prix-gaz-butane-brazzaville-bouteille-12-kg-hausse/
  - https://www.imf.org/-/media/files/publications/tar/2025/english/tarea2025074-source-pdf.pdf
  - https://ecomatin.net/hydrocarbures-le-fmi-denonce-linefficacite-des-subventions-publiques-au-congo
  - https://www.capmad.com/post/congo-coraf-boosts-refining-and-lifts-quarterly-sales-to-nearly-70-billion-cfa-francs
- Chad:
  - https://ecomatin.net/tchad-la-facture-des-subventions-a-limportation-de-gaz-domestique-multipliee-par-onze-en-dix-ans
  - https://wfp.org/publications/tea-sahel-clean-cooking-chads-refugee-settlements
  - https://www.wfp.org/stories/empowering-refugees-chad-el-salvador-wfp-fires-clean-cooking
- 2026 price shock:
  - https://african.business/2026/05/energy-resources/lpg-prices-spike-as-strait-of-hormuz-remains-closed
  - https://guardian.ng/?p=2948456
- DRC LPG and Bboxx:
  - https://african.business/2025/10/long-reads/us-firms-target-african-liquefied-petroleum-gas-bonanza
  - https://www.bboxx.com/news/bboxx-partners-with-uncdf-to-scale-clean-cooking-access-in-the-drc/
  - https://www.bboxx.com/news/bboxx-cook-overcoming-the-global-challenge-of-clean-cooking/

**eCooking**
- Goma trial:
  - https://www.socialscienceregistry.org/trials/10099
  - https://app.inrae.fr/en/breves/ecooker-the-promise-of-ecooking-electric-cooking-and-sustainable-development/
  - https://benin.afd.fr/sites/default/files/2025-02-11-02-07/QDD85_VA_WEB%20V3%20BAT.pdf
  - https://sun-connect.org/mini-grids-can-supply-electricity-but-what-about-demand-a-private-drc-project-shows-how-it-can-work/
- Tanzania pilot and tariff review:
  - https://sun-connect.org/wpcont/uploads/A2EI_Clean_Cooking_Data_Release_Report_Nov2021.pdf
  - https://www.mdpi.com/1996-1073/15/24/9549
  - https://microgridnews.com/wp-content/uploads/2023/07/Leary-Jon.pdf
- MECS modelling: https://mecs.org.uk/wp-content/uploads/2021/05/Modelling-the-costs-and-benefits-of-moving-to-Modern-Energy-Cooking-Services-–-methods-application-to-three-case-studies.pdf
- MECS DRC eCooking Market Assessment (cited but not retrievable, 404): https://mecs.org.uk/wp-content/uploads/2023/03/DRCongo-eCooking-Market-Assessment-28.02.23.pdf

**Bioethanol**
- https://www.biofuelsdigest.com/bdigest/2016/11/07/wesaf-energy-launches-cane-ethanol-pilot-project-with-eye-on-cooking-stove-market/
- https://green.simpliflying.com/p/could-cameroon-become-central-africas
- https://www.fao.org/in-action/global-bioenergy-partnership/news-and-events/news/news-detail/new-report-explores-the-bioethanol-potential-to-improve-clean-cooking-access-in-africa/en

**Carbon**
- ICVCM:
  - https://icvcm.org/integrity-council-approves-three-cookstove-methodologies/
  - https://www.goldstandard.org/news/integrity-council-approves-adipic-acid-and-further-clean-cookstove-methodology-versions
- Article 6.4: https://climatechangenews.com/2026/02/26/uns-new-carbon-market-delivers-first-credits-through-myanmar-cookstove-project/
- Burundi:
  - https://unfccc.int/sites/default/files/resource/A6.4-FORM-GOV-001%20_Burundi.pdf
  - https://carbon-pulse.com/407036/

**Burundi context**
- https://fews.net/east-africa/burundi/key-message-update/may-2026
- https://en.abpinfo.bi/?p=3377
- https://citizen.digital/article/regional-fuel-crisis-deepens-as-mozambique-ethiopia-and-burundi-report-shortages-long-queues-n383313

**Policy (Mission 300)**
- https://www.worldbank.org/en/news/press-release/2025/09/24/17-countries-commit-to-concrete-plans-to-scale-up-electricity-access-as-mission-300-expands
- https://www.worldbank.org/ext/en/energizingafrica/national-energy-compacts
- https://africa-energy-portal.org/reports/central-africa-compact-commitments
- https://thedocs.worldbank.org/en/doc/680a427c0554b887598d86080fdcc775-0010012025/original/Sao-Tome-National-Energy-Compact-Mission-300.pdf
