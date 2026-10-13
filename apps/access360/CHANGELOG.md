# Changelog

## 0.1.0 (development, 12 October 2026)

* ACCESS FINANCE engine 0.1.0:
  * quarterly mini grid project finance (demand, energy balance, revenue, opex, capex, battery replacement with maintenance reserve, LCY and USD debt with DSRA and lock up, grants and RBF with deferred income, grid arrival treatments, tax);
  * three statements; metrics;
  * 18 sensitivity cases and tornado chart;
  * minimum capital grant solver;
  * integrity checks with fault injection;
  * status rules.
* ACCESS OPTIMIZER 0.1.0: options A to G, feasibility gates, weighted score, Pareto flag, explanation.
* Backend API:
  * authentication with cookie sessions, CSRF header and TOTP MFA;
  * organisations and roles; PostgreSQL row level security;
  * projects, inputs, runs, sensitivity, subsidy solver and milestones;
  * Excel and teaser exports with run stamps;
  * map datasets with mandatory metadata;
  * dashboard separating demo and real data;
  * accreditation workflow; audit log; demo seed.
* Documentation: architecture, ADR 0001, engine specification, geospatial specification, test strategy, deployment, guides, limitations, risks, roadmap.
* CI workflow for backend tests.
* Independent engine review (21 findings): critical and major findings fixed; 12 kinds of recomputation check; mutation tests; minor and design findings fixed or documented (docs/reviews).
* Frontend: Next.js 16, Tailwind 4, Recharts, MapLibre 6, EN/FR; dashboard, projects (inputs, results, sensitivity, subsidy, milestones, exports), optimizer, explore, reports, administration, planned module pages; Playwright end to end test.
* Fix: the W_REVIEW warning had its label and status fields swapped; warning texts now use the project currency code.

## 0.2.0 (development, 13 October 2026): milestone 2

* Owner review recorded (docs/reviews).
* Engine:
  * receivable and payable days;
  * one LCY tranche can be sculpted so that total debt service is CFADS divided by the target DSCR (fixed point, converged flag);
  * the DSRA is drawn before equity support;
  * new recomputation checks.
* Live formula Excel export, verified against the engine after LibreOffice recalculation.
* Three page project summary (PDF). Negatives are shown in parentheses in the exports.
* Public reference data:
  * Natural Earth boundaries and places (public domain);
  * OWID energy indicators (CC BY 4.0; third party licences not verified);
  * WDI access to electricity through the Datahub mirror (CC BY 4.0 as stated).

  Every file is in a manifest with its SHA-256.
* PostGIS 3.4 (migration 0004): feature table, project context and radius screening.
* Security:
  * MFA secrets encrypted at rest;
  * Redis rate limits;
  * password reset and change;
  * log out everywhere;
  * the SMTP sender must be set explicitly.
* Phase 2:
  * project gates;
  * Electrification Acceleration Score with explanations;
  * portfolios with ranking and separate real and demo totals;
  * interface pages and end to end tests.
* Fix: a project whose latest run uses illustrative inputs now counts as demo in the dashboard and portfolio totals.
