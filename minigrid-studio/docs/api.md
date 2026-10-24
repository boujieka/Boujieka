# API — Mini-Grid Financial Model Studio (v1)

Base path `/api/v1`. Authentication: `Authorization: Bearer <token>` obtained from `POST /auth/login`.
The full machine-readable contract is `docs/openapi.json` (generated from the code); an interactive
explorer is served at `/docs` when the API runs with `MGS_EXPOSE_DOCS=true`.

| Method | Path | Purpose | Rôles autorisés (liste explicite, pas une hiérarchie) |
|---|---|---|---|
| POST | `/api/v1/auth/signup` | Create an organisation and its first administrator (disabled unless MGS_ALLOW_SIGNUP=true). | public (si MGS_ALLOW_SIGNUP=true) |
| POST | `/api/v1/auth/login` | Login | public |
| POST | `/api/v1/auth/logout` | Logout | tout utilisateur connecté |
| GET | `/api/v1/auth/me` | Me | tout utilisateur connecté |
| POST | `/api/v1/auth/accept-invitation` | New users set their own password here. Existing users must call this endpoint while signed in as the invited account (bearer token). | jeton d'invitation (+ session du compte s'il existe déjà) |
| GET | `/api/v1/orgs/{org_id}/members` | Members | admin, analyste, réviseur |
| POST | `/api/v1/orgs/{org_id}/invitations` | Create a single-use invitation. No account is created and no password is set by the admin; existing accounts are never attached without their consent. | admin |
| GET | `/api/v1/orgs/{org_id}/invitations` | Invitations | admin |
| DELETE | `/api/v1/orgs/{org_id}/members/{user_id}` | Remove a member; their project memberships in this organisation go too and all their sessions are revoked. | admin |
| PUT | `/api/v1/orgs/{org_id}/members/{user_id}` | Set Role | admin |
| GET | `/api/v1/orgs/{org_id}/audit` | Audit Log | admin |
| GET | `/api/v1/projects` | List Projects | admin, analyste, réviseur, investisseur |
| POST | `/api/v1/projects` | Create Project | admin, analyste |
| GET | `/api/v1/projects/{project_id}` | Get Project | admin, analyste, réviseur, investisseur |
| PATCH | `/api/v1/projects/{project_id}` | Patch Project | admin, analyste ; `restricted` et `archived` : admin seulement |
| POST | `/api/v1/projects/{project_id}/members/{user_id}` | Add Project Member | admin |
| DELETE | `/api/v1/projects/{project_id}/members/{user_id}` | Remove Project Member | admin |
| POST | `/api/v1/projects/{project_id}/versions` | Create Version | admin, analyste |
| GET | `/api/v1/projects/{project_id}/versions` | List Versions | admin, analyste, réviseur ; investisseur : versions approuvées seulement |
| POST | `/api/v1/projects/{project_id}/versions/import-xlsm` | Read the assumptions of a workbook in the CrossBoundary format. The file is parsed as data only: formulas are not evaluated and macros never run.… | admin, analyste |
| GET | `/api/v1/versions/{version_id}` | Get Version | admin, analyste, réviseur ; investisseur : versions approuvées seulement |
| POST | `/api/v1/versions/{version_id}/revise` | Revise | admin, analyste |
| POST | `/api/v1/versions/{version_id}/submit` | Submit | admin, analyste |
| POST | `/api/v1/versions/{version_id}/review` | Review | admin, réviseur (ni l'auteur ni le soumetteur) |
| POST | `/api/v1/versions/{version_id}/runs` | Run | admin, analyste |
| GET | `/api/v1/versions/{version_id}/runs` | List Runs | admin, analyste, réviseur ; investisseur : versions approuvées seulement |
| GET | `/api/v1/runs/{run_id}` | Get Run | admin, analyste, réviseur ; investisseur : versions approuvées seulement |
| GET | `/api/v1/runs/{run_id}/series.csv` | Annual series with their unit and workbook source row, one column per year. | admin, analyste, réviseur ; investisseur : versions approuvées seulement |
| GET | `/api/v1/engine/info` | Info | public |
| GET | `/api/v1/engine/options` | Options | public |
| GET | `/api/v1/engine/assumption-schema` | Assumption Schema | tout utilisateur connecté |
| GET | `/api/v1/engine/templates` | Templates | public |
| GET | `/health` | Health | public |

Un projet `restricted` n'est visible que de ses membres et des admins. Un projet archivé est en lecture seule.
Les membres sont ajoutés par **invitation** : l'admin reçoit un jeton à usage unique (7 jours) à transmettre hors bande ;
l'invité crée son compte avec `POST /auth/accept-invitation`, ou, s'il a déjà un compte, l'accepte connecté à ce compte.
La documentation interactive `/docs` n'est servie que si `MGS_EXPOSE_DOCS=true`.

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
