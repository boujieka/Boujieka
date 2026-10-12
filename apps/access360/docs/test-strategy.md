# Test strategy

| Level | Location | What it proves | Run |
|---|---|---|---|
| Engine unit and reconciliation | `backend/tests/engine/test_engine.py` | Hand-calculated revenue, opex, EBITDA and project IRR (checked against numpy-financial); straight-line depreciation; LCY annuity schedule; USD translation and FX loss; USD capex at the spend rate; battery replacement timing and cost; the maintenance reserve; RBF lag and cap; grant milestones and deferred income; the liquidity effect of subsidy delay; equity support on negative cash; the DSCR definition; capacity limits; all three grid treatments reconcile; every sensitivity case reconciles and moves in the expected direction; the minimum grant solver meets its threshold and the grant is minimal; status rules (never validated without review; demo never validated; incomplete inputs) | `pytest tests/engine` |
| Fault injection | same file | Each planted fault (balance sheet, cash, fixed assets, deferred grant, DSRA, maintenance reserve, negative cash, energy, collections, RBF, debt roll forward, sources and uses) is detected by its check | same |
| Optimizer | `backend/tests/engine/test_optimizer.py` | Infeasible options never ranked; unknown grid distance blocks grid options; least cost equals minimum LCOE; Pareto flags; the anchor option needs an anchor and reduces storage; weights change the ranking, not the costs | same |
| API and security | `backend/tests/api/test_api.py` (needs PostgreSQL) | Registration, login and logout; password policy; CSRF header; full project workflow (inputs, run, sensitivity, minimum subsidy, milestones, XLSX and PDF exports stamped with run and inputs hash); cross-tenant blocking at the API; row-level security in the database with the app role (no context gives no rows; another tenant's context gives no rows; a cross-tenant insert is refused); roles; MFA required for privileged actions; accreditation needs a superadmin with MFA; dataset validation for GeoJSON and CSV; optimizer endpoint; demo seed with separate demo and real aggregates | `pytest tests/api` |
| End to end (browser) | `frontend/e2e` | Register, project, demo inputs, run, results, sensitivity, teaser download, French labels, optimizer, map page | see frontend README |

**Rules:**
* A model is never labelled VALIDATED because it ran.
* Monte Carlo will only be added after the deterministic engine has passed an independent review.
* CI runs the backend suites on every change under `apps/access360/` (`.github/workflows/access360.yml`).
