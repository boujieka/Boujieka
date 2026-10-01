## 1. Purpose of the model {#purpose}

The model is built for the manager of a grant or results-based financing (RBF) window for energy access. Starting from a pipeline of applicant projects, it answers one question: which projects should the fund support, with how much RBF and capital grant, and what portfolio of connections, impact, leverage and risk does that buy?

The workbook covers the full cycle of a call for proposals:

1. setting up the fund and its support rules;
2. eligibility screening, with the rejection reason for each project;
3. weighted scoring of eligible projects;
4. allocation of the envelope in rank order, within concentration limits;
5. projection of disbursements and of the fund's cash position;
6. tracking of verified results over the life of the fund.

The model supports decisions. It does not replace the investment committee, due diligence, procurement rules or the fund's legal documentation.

## 2. Getting started {#getting-started}

The workbook is an .xlsx file with no macros, compatible with Excel 2010 and later versions and with LibreOffice Calc. None of its functions requires a recent Excel version. No sheet is protected: work on a copy.

| Appearance | Meaning |
|---|---|
| Blue text on yellow fill | Input |
| Black text | Formula, do not overwrite |
| Green text | Link from another sheet |

Suggested sequence:

1. "Fund Parameters" sheet: envelope, profile, criteria, countries, weights, delivery rates.
2. "Pipeline" sheet: one row per applicant.
3. Read the "Eligibility & Scoring" sheet, then the "Allocation" sheet.
4. Read the "Portfolio Dashboard" and confirm the "Checks" sheet.
5. During the life of the fund, update the "MRV Tracker" sheet.

## 3. Workbook structure {#structure}

| Sheet | Content | Input |
|---|---|---|
| "Start Here" | Workflow, method, simplifications | No |
| "Fund Parameters" | Envelope, support profile, eligibility, countries, weights, delivery rates | Yes |
| "Pipeline" | Applicant project data, up to 25 | Yes |
| "Eligibility & Scoring" | Tests, maximum support, request, metrics, scores, rank | No |
| "Allocation" | Sequential allocation by rank | No |
| "Disbursements" | RBF, grants and fund cash position by year | No |
| "MRV Tracker" | Verified connections, RBF earned and outstanding | Yes |
| "Portfolio Dashboard" | Summary, verdicts, charts | No |
| "Checks" | Twelve integrity checks | No |

Project sheets share the same layout: a project sits on the same row in the pipeline, eligibility, disbursement and MRV sheets. This makes the formulas easier to audit.

## 4. Setting up the fund {#parameters}

### 4.1 Envelope and limits

| Parameter | Role |
|---|---|
| "Total fund size" | Total resources of the window |
| "Fund management & MRV costs" | Share of fund size not allocated to projects |
| "Technical assistance window" | Share reserved for technical assistance |
| "Over-commitment ratio" | Allows commitments above available funds, in anticipation that some connections will not be delivered |
| "Allow partial funding of the marginal project? (1 = yes)" | If 0, a project that does not fit in what is left is skipped and the next one is tested |
| "Maximum share of the envelope per project" | Concentration ceiling per project |
| "Maximum share of the envelope per country" | Concentration ceiling per country |
| "Additionality tolerance above the viability gap" | Margin allowed between the request and the project's viability gap |

The allocation envelope equals the funds available for projects times the over-commitment ratio. Over-commitment is prudent only if expected under-delivery covers it. Chapter 7 shows a case where it does not.

### 4.2 Support profile

The "Active profile" is chosen from three generic profiles and a "Custom" profile. Each profile sets:

* an RBF amount per connection for each customer type (household, productive use, commercial, institution);
* a capital grant as a share of project CAPEX;
* a ceiling on public support from all sources, as a share of CAPEX;
* a ceiling on support per project;
* the RBF tranche paid at verification and the verification lag.

The remaining tranche is paid one year later, after a service-continuity check. Part of the payment therefore depends on continued service as well as on the connection.

To reproduce the published rules of an existing programme, use the "Custom" profile. The generic profiles do not describe any real programme.

Two parameters describe how fast connections are verified: the share verified in the commissioning year and the cumulative share by the end of the following year. The balance is verified in the third year.

### 4.3 Eligibility criteria

Eight criteria can be switched on or off individually:

| Criterion | Intent |
|---|---|
| Minimum number of connections | Screen out projects too small to justify verification costs |
| Maximum CAPEX per connection | Screen out projects with excessive unit cost |
| Minimum renewable share | Keep support low carbon |
| Minimum private co-finance | Require commitment from the developer and lenders |
| Minimum readiness stage | Reserve support for projects ready to build |
| Maximum average tariff | Protect customers' ability to pay |
| Minimum productive-use share | Favour projects that create economic activity |
| Eligible country | Respect the fund's geographic scope |

The country list sits in its own table, with Y for eligible and N for not eligible. The country name in the pipeline must match exactly, with no extra spaces.

### 4.4 Scoring weights

Eight scoring criteria carry weights. They must add up to 100%, which a check verifies. The weights supplied are examples: they should reflect the fund's policy and, ideally, be set before applications arrive.

### 4.5 Delivery rate by risk rating

The table links each risk rating, from 1 to 5, to the share of target connections the fund expects to see delivered. This rate reduces expected RBF disbursements. Calibrate it on the fund's own history or on comparable programmes.

## 5. Filling in the pipeline {#pipeline}

Each row describes one project: name, country, developer, technology, readiness, developer track record, risk rating, commissioning year, connections by type, CAPEX, developer equity, debt secured, other grants, average tariff, renewable share and lifetime CO2 avoided.

Two columns are optional:

* the "Viability gap (from Developer model)", which the Developer Edition calculates for each project. It feeds the additionality test;
* the "Amount requested (optional)". When filled in, the request considered is the lower of this amount and the maximum support.

"Commissioning (fund year)" must fall between years 1 and 7, so that all RBF is paid before the end of the ten-year horizon.

## 6. Reading the results {#results}

### 6.1 Eligibility and scoring

For each project, the sheet shows the result of each test (1 when the criterion is met), then the "Eligibility status". A rejected project shows the first criterion it fails, for example "Country not eligible" or "Renewable share too low".

A project's maximum support is the lowest of four amounts:

* RBF at profile rates plus capital grant;
* the public support ceiling as a share of CAPEX, less other grants;
* the per-project ceiling;
* the maximum share of the envelope per project.

Eight scores from 0 to 100 are then calculated. Cost-effectiveness, leverage, productive-use share and CO2 per unit of support are relative to the best eligible project. Readiness, track record and risk use an absolute scale. Additionality scores 100 if the request stays within the viability gap plus tolerance, 0 if it exceeds it, and 50 when no data is available.

### 6.2 Allocation

The "Allocation" sheet ranks eligible projects by descending score. Each row calculates the envelope and the country room left using only the rows above it, so the model contains no circular references. The "Binding constraint" column shows why a project is funded only partly or not at all: "Country limit" or "Envelope exhausted".

### 6.3 Disbursements and fund cash position

The capital grant is paid in the commissioning year. RBF in year t equals:

RBF allocated × delivery rate × [tranche A × share verified in (t − lag) + (1 − A) × share verified in (t − lag − 1)]
{: .formula}

The cash block tracks cumulative disbursements, remaining available funds and undisbursed commitments. A negative remaining balance means the over-commitment is not covered.

### 6.4 MRV tracking

During the life of the fund, enter in the "MRV Tracker" sheet the verified connections and RBF paid to date for each project. The model compares progress with the profile expected for the "Reporting fund year" and assigns a status:

| Status | Rule |
|---|---|
| "On track" | Progress at least 90% of expected |
| "Behind" | Between 60% and 90% of expected |
| "Off track" | Below 60% of expected |
| "Not started" | Commissioning after the reporting year |

"Outstanding RBF" is RBF earned times the tranche paid at verification, less payments already made. The second tranche falls due after the service-continuity check.

### 6.5 Portfolio dashboard

The dashboard groups commitments, the pipeline, impact bought, leverage, cost-effectiveness, risk and concentration, and four verdicts: envelope commitment, coverage of disbursements by available funds, country concentration, and additionality.

The impact and leverage of a partly funded project are attributed pro rata to the share of its request that the fund covers.

## 7. Worked example {#example}

The example is entirely fictitious: fund, countries and projects.

| Item | Value |
|---|---|
| Fund size | USD 3,000,000 |
| Available after management (7%) and technical assistance (8%) | USD 2,550,000 |
| Envelope with 110% over-commitment | USD 2,805,000 |
| Applicants and eligible projects | 14 applicants, 8 eligible |
| Requests from eligible projects | USD 3,247,750, an oversubscription of 1.16 |
| Allocation | USD 2,805,000, of which USD 823,388 RBF and USD 1,981,612 grants |
| Connections funded | about 8,010, serving 32,400 people |
| Lifetime CO2 avoided | about 50,750 tCO2 |
| Private capital mobilised | USD 4,392,509, or 1.57 per unit allocated |
| Allocation per connection | USD 350 |

Six applicants are rejected, each with its reason: country not eligible, renewable share too low, not ready enough, CAPEX per connection too high, too few connections, productive use too low.

Two projects are only partly funded. Project N is limited by the country ceiling: Country B reaches exactly 50% of the envelope. Project I is limited because the envelope runs out.

The cash verdict is negative, and it is the most useful lesson in the example. With 110% over-commitment, expected disbursements (USD 2,756,447) exceed available funds (USD 2,550,000). The reason lies in the support mix: 71% of the allocation is capital grants, paid in full at commissioning. Only RBF is haircut for delivery risk. Expected under-delivery therefore covers an over-commitment of only about 1.02. There are two fixes: bring the over-commitment ratio down towards 1.02, or choose a profile where RBF carries more weight.

## 8. Integrity checks {#checks}

| Check | Meaning of an alert |
|---|---|
| "Scoring weights total 100%" | Weights need correcting |
| "Allocation within envelope" | Allocation formula changed |
| "No allocation to ineligible projects" | Eligibility formula changed |
| "Each eligible project ranked exactly once" | Rank formula changed |
| "Country limit respected" | Allocation formula changed |
| "Expected disbursements by year = grants + RBF x expected delivery (all paid within the fund life)" | Commissioning too late or verification lag too long |
| "Verification profile valid (0 <= year 1 <= cumulative year 2 <= 100%)" | Inconsistent verification parameters |

If an alert points to a changed formula, restore the file from a clean copy.

## 9. Limits of use {#limits}

These limits come from a critical review of the model.

1. Relative normalisation. Several scores are relative to the best eligible project. Adding or removing an applicant therefore changes the scores of the others and can, at the margin, swap two ranks. Freeze the pipeline before final scoring.
2. Greedy allocation. Funding follows score order. It is not a constrained optimisation: another combination of projects could deliver more connections for the same envelope.
3. Grants assumed paid in full. The risk that a project is never completed is not modelled for the capital grant.
4. One verification profile, over three years, for all projects.
5. Pro rata attribution. The impact of a partly funded project is attributed to the fund in proportion to its share. Funders use other attribution conventions as well.
6. No foreign exchange, no reflows, no financial return: the model handles a grant and RBF fund, not a lending fund.
7. Self-reported data. Pipeline data come from applicants. Their reliability depends on due diligence.

## 10. Glossary {#glossary}

| Term | Definition |
|---|---|
| Allocation envelope | Commitment ceiling, equal to available funds times the over-commitment ratio |
| Over-commitment | Committing beyond available funds in anticipation of under-delivery |
| Decommitment | Share of commitments that will not be disbursed for lack of results |
| Additionality | Support does not exceed what the project needs to be viable |
| Leverage | Private capital mobilised per unit of fund support |
| Delivery rate | Share of target connections actually delivered and verified |
| Verification tranche | Share of RBF paid as soon as a connection is verified |
| MRV | Measurement, reporting and verification of results |
| Oversubscription | Eligible requests divided by the envelope |

## 11. Disclaimer and licence {#licence}

The model is a portfolio screening and planning tool. It is not investment, legal or tax advice. The fund, countries and projects in the example are fictitious.

The licence covers one user or one organisation. Resale, redistribution and publication of the file or of this manual are not permitted.
