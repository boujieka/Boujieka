## 1. Purpose of the model {#purpose}

The model follows a mini-grid developer from demand estimation to the financing request. It asks whether the project can become bankable, and with what mix of upfront capital grant, results-based financing (RBF), concessional debt, senior debt and equity.

Compared with the entry calculator, the Developer Edition adds:

* an hourly load profile per segment, which sets the night-time energy share and the peak ratio;
* an inventory of productive uses, which can drive the consumption of productive users;
* RBF that differs by customer segment, and an affordability test;
* exact calibration of the grant and RBF needed, without Excel's Goal Seek;
* two debt tranches, a debt service reserve account (DSRA) and tax loss carry-forward;
* three preset scenarios and a tornado sensitivity that recalculates live;
* impact and MRV indicators, and an automatically written financing note.

The model focuses on subsidy sizing, affordability and impact. It does not cover foreign exchange, VAT, working capital or full financial statements. If the file requires them, use it alongside a full project-finance model.

## 2. Getting started {#getting-started}

The workbook is an .xlsx file with no macros, compatible with Excel 2010 and later versions and with LibreOffice Calc. No sheet is protected. Work on a copy and keep the original intact.

| Appearance | Meaning |
|---|---|
| Blue text on yellow fill | Input |
| Black text | Formula, do not overwrite |
| Green text | Link from another sheet |

All amounts are in the currency named in "Currency label". The label performs no conversion.

Suggested sequence:

1. Section 1 of the "Inputs" sheet: project, rates, tax.
2. Customer segments: numbers, consumption, tariff, connection fee, RBF, monthly income.
3. The "Load Profile" and "Productive Use" sheets.
4. Sizing, CAPEX, OPEX.
5. Funding structure.
6. Read the "Dashboard", then the "Funding Gap & RBF" sheet.
7. Confirm that the "Checks" sheet shows "ALL OK".
8. Test scenarios and read the "Sensitivity" sheet.
9. Copy the paragraphs of the "Financing Request" sheet into your concept note.

## 3. Workbook structure {#structure}

| Sheet | Content |
|---|---|
| "Start Here" | Workflow, method, simplifications, disclaimer |
| "Inputs" | Project, scenarios, segments, technical, CAPEX, OPEX, funding, impact |
| "Load Profile" | Hourly profile per segment, night-time share, peak ratio |
| "Productive Use" | Inventory of productive appliances |
| "Dashboard" | Indicators, verdicts, affordability, charts |
| "Funding Gap & RBF" | Viability gap, grant and RBF needed, debt capacity, RBF timing |
| "Sensitivity" | Tornado and break-even indicators |
| "Impact & MRV" | Annual indicators and cost-effectiveness ratios |
| "Financing Request" | Written paragraphs, sources and uses, key metrics |
| "Cash Flow" | 20-year annual engine |
| "Checks" | Sixteen integrity checks |

The workbook also holds fourteen hidden sheets whose names start with S_. They are copies of the calculation engine used by the tornado. Do not edit them.

## 4. Entering the inputs {#inputs}

### 4.1 Project, rates and tax

The "Project hurdle rate (discount rate)" drives NPV, LCOE, the viability gap and the RBF calibration. Express it in nominal terms, like the cash flows. The "Target equity IRR" drives the equity verdict and the RBF needed from the shareholder's point of view. The "Minimum DSCR required by lenders" is the covenant from the term sheet.

### 4.2 Scenarios

The "Active scenario" is chosen from a list: Base, Conservative, Optimistic or Custom. Each scenario applies multipliers to tariff, consumption per customer, CAPEX, OPEX, collection rate and diesel price. The values supplied are examples. Adjust them to your own risk analysis.

Scenarios represent out-turn risk on a system already built. Sizing stays at the base case. A 15% lower demand therefore does not shrink the PV array; it reduces sales.

### 4.3 Segments, tariffs, RBF and affordability

For each segment, enter:

| Column | Comment |
|---|---|
| "Customers" | Target number once ramp-up is complete |
| "kWh/month (entered)" | Monthly consumption per customer. For productive users, the "kWh/month (used)" column can take the productive-use inventory instead |
| "Tariff per kWh" | Year 1 tariff, before escalation |
| "Connection fee" | Paid by the customer at connection |
| "RBF per new connection" | Amount set by the programme for this customer type |
| "Monthly income or revenue" | Household income or business revenue. Leave 0 for institutions |

The model calculates the year 1 monthly bill and compares it with the "Affordability threshold (max bill as % of income)". There is no universal threshold: use your programme's definition or your market study.

The "Collection rate (share of bills paid)" applies to all energy revenue. With prepaid meters, energy is paid before it is used and the rate can be set at 100%.

### 4.4 Load profile

The "Load Profile" sheet holds, for each segment, the share of daily energy used in each hour. Each column must add up to 100%. The model weights these profiles by each segment's energy and derives two values:

* the night-time share, meaning energy used between sunset and sunrise, which sizes the battery;
* the peak ratio, equal to the share of the busiest hour times 24, which sizes the diesel generator.

The profiles supplied are illustrative. Replace them with metered or survey data as soon as possible. A household profile that is too concentrated in the evening oversizes the battery. A productive profile that is too flat understates the daytime peak.

### 4.5 Productive uses

The "Productive Use" sheet lists the expected appliances: grain mills, welding workshops, cold rooms, irrigation pumps, sewing machines, hair salons, carpentry tools. For each line, monthly consumption is:

units × rated power (kW) × hours per day × days per month × load factor
{: .formula}

The load factor reflects the fact that a motor rarely runs at full power. The total, divided by the number of productive users, gives consumption per user. When the related option on the "Inputs" sheet is set to 1, this value replaces the direct entry.

### 4.6 Technical design and sizing

| Component | Rule |
|---|---|
| PV array | Design generation × target solar fraction × storage loss factor ÷ specific yield × oversizing |
| Battery | Daily generation × night-time share ÷ depth of discharge |
| Diesel generator | Average load × peak ratio |

The "Battery round-trip efficiency" feeds the storage loss factor: solar energy used at night is stored, then discharged with a loss. The "Override" column lets you impose a design from a detailed study.

### 4.7 CAPEX and OPEX

CAPEX covers PV, battery, generator, distribution network, meters and service drops, powerhouse and civil works, any productive-use equipment financed by the project, and development costs and contingency as percentages of hard CAPEX. Batteries are replaced at the end of their life. With the maintenance reserve on, the cost is smoothed in CFADS through annual contributions.

OPEX covers fixed O&M, staff, insurance, licences and fees, MRV and reporting, customer management, generator maintenance and fuel. MRV costs deserve their own line: an RBF programme requires third-party verification and data tracking, which carry an annual cost.

### 4.8 Funding structure

| Source | Parameters | Treatment |
|---|---|---|
| Capital grant | Amount | Received in year 0 |
| RBF | Amount per segment, verification lag | Paid per verified new connection |
| Senior debt | Share of CAPEX net of grant, rate, tenor, grace | Interest only during grace, then annuities |
| Concessional debt | Same parameters | Same, on its own terms |
| DSRA | Share of next year's debt service | Funded by equity, released on repayment |
| Equity | Balance of the financing plan | Also funds the initial DSRA |

> RBF arrives after commissioning and connection verification. It does not fund construction. The "Funding Gap & RBF" sheet shows the amount received in years 1 to 3, which the developer must bridge.

## 5. Reading the results {#results}

### 5.1 Dashboard

The dashboard presents project economics (CAPEX, IRR and NPV before and after subsidies, LCOE, levelized collected revenue), financing and bankability (DSCR, equity IRR and NPV, payback), affordability by segment, and six verdicts.

The equity verdict uses equity NPV at the target rate rather than IRR. Battery replacements and the DSRA create cash flows that change sign, for which IRR can mislead or not exist.

### 5.2 Funding gap and RBF calibration

This is the core sheet of the model. It answers four questions.

#### Size of the gap

The viability gap is the present-value subsidy that brings pre-subsidy project NPV to zero. It is compared with the present value of planned subsidies.

#### Grant needed

Given the planned RBF: grant needed = viability gap − PV(planned RBF).

#### RBF needed

Given the planned grant, the model gives two answers. The first brings project NPV to zero at the hurdle rate. The second gives equity its target return with the debt in place, which is the developer's view. Both are expressed as a uniform amount per connection, then as a scale factor to apply to the amounts per segment.

#### Debt capacity

Maximum senior debt is the largest loan whose annuities keep DSCR above the minimum in every year, given CFADS and concessional debt service. The model shows the binding year. Most often it is the year when RBF stops while both tranches are amortising.

### 5.3 Sensitivity

Each variable moves up and down by the chosen range (20% by default), one at a time, around the active scenario. The table gives NPV after subsidies, the viability gap, minimum DSCR and equity IRR for each case. The tornado ranks the variables by their effect on NPV.

Interest rates do not change project NPV, which is unlevered. Their effect shows in DSCR and equity IRR.

The sheet also gives a break-even average tariff without subsidy, obtained by linear interpolation. It is an approximation, because tax and the solar and diesel split make NPV slightly non-linear in tariff. Confirm it by entering that tariff in the inputs.

### 5.4 Impact and MRV

The "Impact & MRV" sheet shows, year by year, verified new connections by segment, people with access, productive users, jobs supported, energy delivered, renewable generation, CO2 avoided, RBF earned and RBF disbursed. Cost-effectiveness ratios relate public grant funding to connections, people with access and tonnes of CO2 avoided.

Avoided CO2 assumes that, without the project, the solar energy delivered would have been generated by diesel at the same efficiency. The baseline parameter lets you reduce this assumption if some customers used other sources.

### 5.5 Financing request

The sheet writes six paragraphs from the results: project summary, technical solution, investment and gap, funding request, bankability, impact. It also shows the sources and uses table and key metrics. Numbers display with the separators of the user's Excel language. Review and adapt the wording before sending anything.

## 6. Calculation method {#method}

### 6.1 Main formulas

Solar delivered = MIN(available PV energy ÷ storage loss factor ; gross generation × target solar fraction)
{: .formula}

CFADS = EBITDA − maintenance reserve contribution − tax after interest + RBF received
{: .formula}

Equity cash flow = CFADS − total debt service − change in DSRA
{: .formula}

Viability gap = MAX(0 ; − NPV of project cash flow before subsidies)
{: .formula}

Uniform RBF for NPV = 0 = (viability gap − grant) ÷ PV(verified connections paid)
{: .formula}

Uniform RBF for the equity target = − (equity NPV at target rate − PV of planned RBF at target rate) ÷ PV(connections) at target rate
{: .formula}

Maximum senior debt = MIN over years of (CFADS ÷ minimum DSCR − concessional debt service) ÷ senior debt service per unit of debt
{: .formula}

### 6.2 Why the calibration is exact

RBF enters project and equity cash flows linearly. It is not taxed in the model, and it changes neither the debt nor the DSRA. NPV is therefore an affine function of the RBF amount per connection, and the equation NPV = 0 can be solved directly. Two identity checks on the "Checks" sheet verify this at every recalculation. In testing, entering the calculated RBF gives zero project NPV and an equity IRR equal to the 15.0% target.

If RBF is taxable in your jurisdiction, the calibration understates the amount needed. For a profitable project, a first approximation is to divide the result by (1 − tax rate). For an exact result, RBF has to be added to taxable income in the engine.

### 6.3 Tax

Tax is calculated twice. The unlevered calculation feeds project IRR; the calculation after interest feeds CFADS. In both cases tax losses are carried forward without time limit and offset against later profits.

## 7. Worked example {#example}

The example is fictitious: 970 customers, including 800 households, 60 productive users, 100 commercial customers and 10 institutions.

| Item | Value |
|---|---|
| Night-time share and peak ratio from the load profile | 37.1% and 1.79 |
| Consumption per productive user from the inventory | 155 kWh per month |
| Sizing | 305 kWp PV, 540 kWh storage, 87 kW diesel generator |
| Total CAPEX | USD 1,162,734, or USD 1,199 per connection |
| Viability gap | USD 804,952, or USD 830 per connection |
| Planned subsidies | USD 600,000 upfront grant and USD 252,000 RBF, an average of USD 260 per connection |
| Project NPV after subsidies | positive, USD 12,968 |
| Senior and concessional debt | USD 112,547 each |
| Minimum DSCR | 1.34x against a 1.30x covenant, binding year 2036 |
| Maximum senior debt at minimum DSCR | USD 118,010 |
| Equity IRR | 10.1% against a 15% target |
| Uniform RBF needed for the equity target | USD 347 per connection |
| Break-even average tariff without subsidy | USD 0.60 per kWh, against an average billed tariff of USD 0.38 |

Reading. The project cannot be financed from its own revenue. The planned grant and RBF close the gap at project level, and the debt meets the covenant with a thin margin (planned senior debt is about 5% below the maximum the project can carry). Equity does not reach its target. RBF would need to rise from USD 260 to USD 347 per connection on average, which means an RBF budget about one third larger.

The tornado brings a less intuitive result. A 20% increase in consumption per customer lowers NPV, just as a 20% decrease does. The system is sized for base demand, so the extra kWh are produced by the diesel generator at a fuel and maintenance cost above the collected tariff. Demand growth without an extension of the PV array therefore worsens project economics.

## 8. Integrity checks and troubleshooting {#checks}

| Check | Meaning of an alert | Action |
|---|---|---|
| "Sources = uses at construction" | Unbalanced financing plan | Check debt shares and the grant |
| "Senior + concessional share <= 100%" | Debt shares too high | Reduce one of the two shares |
| "Senior debt repaid by end of tenor" | Inconsistent grace or tenor | Grace must be shorter than tenor |
| "Load profile: each segment sums to 100%" | Incomplete hourly profile | Correct the column concerned |
| "Energy balance: solar + diesel = generation" | A formula was overwritten | Restore the engine from a clean copy |
| "DSRA fully released at end" | Loan tenor beyond the horizon | Shorten the loan |
| "Subsidy identity: NPV after = NPV before + grant + PV(RBF)" | A formula was changed in the engine | Restore the engine |
| "RBF calibration reproduces equity target (identity check)" | A formula was changed | Restore the engine |
| "Sensitivity engines reproduce base at zero range (base row = Cash Flow)" | A hidden sheet was changed | Restore the file |

## 9. Limits of use {#limits}

These limits come from a critical review of the model. Read them before presenting a result to an investment committee.

1. Annual time step with no hourly dispatch. The solar and diesel split comes from a solar fraction ceiling. For an investment file, confirm it with an hourly simulation.
2. Fixed capacity. Without a PV extension, demand above forecast is served by diesel (see chapter 7).
3. Sizing on the base case. Scenarios and the tornado do not resize the system.
4. Diesel generator sized on the weighted peak, with no reserve margin and no motor starting constraint. Add a margin in the "Override" column if needed.
5. Simplified tax. Flat rate, depreciation on total CAPEX, non-taxable grants and RBF.
6. Annuity debt with no fees or sculpting. Maximum senior debt is calculated on current CFADS, whose tax depends on interest: a good approximation, not an optimisation.
7. Single currency. The exchange risk between hard-currency debt and local-currency revenue is not modelled.
8. Simplified impact measures. People with access only count connected households. Jobs supported rely on a user-entered ratio, which a survey should support.

## 10. Glossary {#glossary}

| Term | Definition |
|---|---|
| CFADS | Cash flow available for debt service |
| DSCR | CFADS divided by debt service for the year |
| DSRA | Debt service reserve account |
| Maintenance reserve | Annual contributions that fund battery replacement |
| Viability gap | Present-value subsidy that brings pre-subsidy NPV to zero |
| RBF | Results-based financing, paid per verified connection |
| Grace period | Period during which only interest is paid |
| Concessional debt | Loan on better than market terms, often from a development finance institution |
| LCOE | Levelized cost of electricity over the lifecycle, per kWh sold |
| Night-time share | Share of daily energy used between sunset and sunrise |
| Peak ratio | Load in the busiest hour divided by average load |
| Load factor | Average power actually drawn by an appliance divided by its rated power |
| MRV | Measurement, reporting and verification of results |

## 11. Disclaimer and licence {#licence}

The model is a screening and pre-feasibility tool. It is not investment, legal, tax or engineering advice and does not replace independent due diligence. Example data are fictitious and do not describe any existing project, developer or programme.

The licence covers one user or one organisation. Resale, redistribution and publication of the file or of this manual are not permitted.
