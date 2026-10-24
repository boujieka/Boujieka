# API — Mini-Grid Financial Model Studio (v1)

Base path `/api/v1`. Authentication: `Authorization: Bearer <token>` obtained from `POST /auth/login`.
The full machine-readable contract is `docs/openapi.json` (generated from the code); an interactive
explorer is served at `/docs` when the API runs.

| Method | Path | Purpose | Minimum role |
|---|---|---|---|
| POST | `/api/v1/auth/signup` | Create an organisation and its first administrator (disabled unless MGS_ALLOW_SIGNUP=true). | public (if MGS_ALLOW_SIGNUP) |
| POST | `/api/v1/auth/login` | Login | public |
| POST | `/api/v1/auth/logout` | Logout | any |
| GET | `/api/v1/auth/me` | Me | any |
| GET | `/api/v1/orgs/{org_id}/members` | Members | reviewer |
| POST | `/api/v1/orgs/{org_id}/members` | Add Member | admin |
| PUT | `/api/v1/orgs/{org_id}/members/{user_id}` | Set Role | admin |
| GET | `/api/v1/orgs/{org_id}/audit` | Audit Log | admin |
| GET | `/api/v1/projects` | List Projects | investor |
| POST | `/api/v1/projects` | Create Project | analyst |
| GET | `/api/v1/projects/{project_id}` | Get Project | investor |
| PATCH | `/api/v1/projects/{project_id}` | Patch Project | analyst |
| POST | `/api/v1/projects/{project_id}/members/{user_id}` | Add Project Member | admin |
| POST | `/api/v1/projects/{project_id}/versions` | Create Version | analyst |
| GET | `/api/v1/projects/{project_id}/versions` | List Versions | investor (approved only) |
| POST | `/api/v1/projects/{project_id}/versions/import-xlsm` | Read the assumptions of a workbook in the CrossBoundary format. The file | analyst |
| GET | `/api/v1/versions/{version_id}` | Get Version | investor (approved only) |
| POST | `/api/v1/versions/{version_id}/revise` | Revise | analyst |
| POST | `/api/v1/versions/{version_id}/submit` | Submit | analyst |
| POST | `/api/v1/versions/{version_id}/review` | Review | reviewer (not the author) |
| POST | `/api/v1/versions/{version_id}/runs` | Run | analyst |
| GET | `/api/v1/versions/{version_id}/runs` | List Runs | investor (approved only) |
| GET | `/api/v1/runs/{run_id}` | Get Run | investor (approved only) |
| GET | `/api/v1/runs/{run_id}/series.csv` | Annual series with their unit and workbook source row, one column per year. | investor (approved only) |
| GET | `/api/v1/engine/info` | Info | public |
| GET | `/api/v1/engine/options` | Options | public |
| GET | `/api/v1/engine/assumption-schema` | Assumption Schema | any |
| GET | `/api/v1/engine/templates` | Templates | public |
| GET | `/health` | Health | public |

## Typical sequence

1. `POST /auth/login` → token.
2. `POST /projects` with `org_id` and a name.
3. `POST /projects/{id}/versions` with `template` (`demo_fictitious` or `crossboundary_reference`), or a full
   `assumptions` object, or upload a CrossBoundary-format workbook to `/versions/import-xlsm`.
   `changes` accepts dotted paths (`"debt.sizing_method": "DSCR"`) or workbook cells (`"Inputs!E302": "DSCR"`).
   `options` enables improvements (see `/engine/options`); `solver_method` is `excel_macros` (default) or `exact`.
4. `POST /versions/{id}/runs` → result with `status` (`reconciled-engine` or `variant`), `kpis`, `series`,
   `checks`, `failed_checks`, `warnings`, `solver`, `pasted_values`. Each KPI and series names its workbook source.
5. `POST /versions/{id}/revise` to change assumptions (new immutable version), `submit`, then a reviewer `review`s.
6. `GET /runs/{id}/series.csv` exports the annual series with unit and source row.
