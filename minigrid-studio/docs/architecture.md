# Architecture — Mini-Grid Financial Model Studio (Phase 1)

```
                 ┌───────────────────────────── backend (Python 3.12+, FastAPI) ─────────────────────────────┐
 React/TS  ──►   │  app/api/*        REST /api/v1 (auth, orgs, projects, versions, runs, engine)              │
 (frontend/)     │  app/security.py  argon2 passwords · opaque bearer tokens (SHA-256 stored) · roles          │
                 │  app/services/    scenario versions · calculation runs · audit journal                      │
                 │  app/engine/      DETERMINISTIC ENGINE (pure Python, no I/O, no AI, no randomness)          │
                 │     assumptions.py  typed inputs, each field tied to its workbook cell                       │
                 │     loader.py       read inputs from a CrossBoundary-format .xlsm (data only, no macros)     │
                 │     prepare.py      Currency, Portfolio, Inputs-sheet calculations                          │
                 │     model.py        Model / Debt / FinStat timeline (69 annual columns)                     │
                 │     solver.py       replay of the 3 VBA macros (default) or exact fixed point (variant)      │
                 │     options.py      opt-in improvements (default = workbook behaviour)                       │
                 │     results.py      named KPIs/series with source cells · derived ratios · per-lot (exp.)    │
                 │     validation.py   blocking errors / warnings before a run                                 │
                 │     reconcile.py    cell-by-cell comparison with Excel or LibreOffice values                │
                 └──────────────┬──────────────────────────────────────────────────────────────────────────────┘
                                │ SQLAlchemy 2.0 · Alembic
                       PostgreSQL 16 (multi-tenant)
```

## Engine

* **Faithful by construction.** Each timeline series is stored under its workbook row
  (`Model!87` = revenue, `Debt!34` = senior debt balance…), so any figure can be traced to
  the Excel formula it reproduces. Calculation order follows the workbook's dependency graph
  (docs/formula_dependency_map.md): operations, then a financing pass year by year down to
  CFADS and debt sculpting, then a reserves pass (DSRA, MMRA, distributions), then returns
  and statements.
* **Excel semantics** are reproduced explicitly (`excel.py`): ROUND half away from zero on
  15 significant digits, ROUNDUP/ROUNDDOWN, EOMONTH with the 1900 date system, approximate
  LOOKUP (text keys skipped), OFFSET look-back windows including the row-total quirk, NPV,
  XNPV, XIRR and IRR (negative IRRs found as Excel does).
* **Circularities.** The workbook breaks four loops with values pasted by macros
  (funding, DSCR capacity, refinancing, DSRA). `solver.solve_excel_macros` replays
  `Debt_Sizing`, `Refi_Debt_Sizing` and `DSRA_resize_3` from the stored pasted values,
  with the same one-sided tolerance; `solve_exact` solves the fixed point exactly (variant).
* **Status of a result.** `reconciled-engine` = faithful options and macro solver (the code
  path verified against Excel); `variant` = any option or the exact solver. Derived
  indicators (DSCR series, LLCR, unlevered IRR) carry `derived=true`; per-lot IRRs carry
  `experimental=true`.
* **Units and currency.** Amounts are in the model currency chosen by `currency.case`
  (1 = USD, 2 = local currency), as in the workbook; every assumption field states its unit.

## Data model (PostgreSQL)

| Table | Content |
|---|---|
| organizations, users, memberships | tenants; role per organisation: admin, analyst, reviewer, investor |
| session_tokens | SHA-256 of bearer tokens, expiry, revocation |
| projects, project_members | projects per organisation; optional restriction to listed members |
| scenario_versions | **immutable** assumption sets (JSONB), options, solver, parent version, changes vs parent, provenance (template, upload SHA-256), status draft → submitted → approved/rejected |
| calculation_runs | engine version, input hash, full result (JSONB), duration, error |
| audit_events | **append-only** journal of every mutation |

Database triggers enforce that `audit_events` cannot be updated or deleted and that a
version's assumptions, options, solver and hash cannot be rewritten.

## Security

* Passwords: argon2id, minimum 12 characters. Tokens: 256-bit random, only their SHA-256 is stored, 12 h expiry, revocable.
* Authorisation: every query goes through the caller's memberships; resources of another
  organisation answer **404** (existence not revealed). Investors only see approved versions.
  Four-eyes rule: the author of a version cannot review it.
* Login attempts are rate-limited per e-mail and IP (in memory, per process).
* Uploads: size limit, extension and ZIP signature checks; workbooks are read as data with
  openpyxl, formulas are not evaluated and VBA is never executed.
* Security headers (nosniff, DENY framing, no-referrer, no-store). Secrets only from the environment (`.env.example`).
* Encryption at rest and TLS are provided by the deployment (managed PostgreSQL with
  encrypted storage, TLS-terminating proxy); they are not implemented in the application.
* No generative AI and no paid API are called by Phase 1.

## Not in Phase 1

Bilingual interface beyond the skeleton, Excel export with live formulas, PDF reports,
Contract Studio, Learning Academy, Investment Studio, ESG and Capital Connect (Phases 2–5).
