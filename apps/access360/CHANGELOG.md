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
