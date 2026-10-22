# AP²I — Administrator guide

## Roles
| Role | Can |
|---|---|
| Public visitor | Public pages, project registry, project pages, map, dashboards |
| Registered user | + assistant, CSV exports (1,000 rows), CSV reports |
| Professional subscriber | + field-level provenance, full exports, PDF/Excel reports, saved searches |
| Government analyst / DFI analyst | + private workspace read, Project Rescue (with an institutional plan) |
| Government / Institutional administrator | + private workspace write, manage their organization's users, thresholds |
| Data contributor | Upload official data (private to their organization until reviewed) |
| Data reviewer | Review queue, verification, duplicates/merges, alert review |
| AP²I super administrator | Everything: connectors, schedules, users, organizations, subscriptions, settings, audit |
Grant roles in Admin → Users (`PUT /api/v1/admin/users/{id}/roles`). Role changes revoke the user's sessions.

## Daily routine
1. **Connectors** (Admin → Connectors): check status, last success/failure, records requiring review. "Sync now"
   runs immediately; "background" queues it on the worker. Never mark a connector operational by hand: the
   status changes only after a successful run that persisted real records.
2. **Review queue** (Admin → Review): records with validation errors. Verify (source checked) or reject.
3. **Duplicates** (Admin → Matches): compare both projects (partners, dates, agencies). Accept only when they are
   the same physical project; choose the survivor. Wrong merge → Admin → Merges → Reverse.
4. **Alerts** (Performance): acknowledge / confirm / dismiss with a note. Alerts are verification prompts.
5. **Data quality**: watch missing information, outdated observations and failed imports.

## Importing official data (no API available)
1. Download the template (`data_templates/projects_import_template.csv` or `budget_lines_template.csv`, also
   `GET /api/v1/uploads/templates`).
2. One row per project/budget line, transcribed from an official document; `source_url` (or document reference)
   and `reporting_date` are mandatory; leave unknown values empty (never 0).
3. Upload in Admin → Uploads. Any invalid row rejects the whole file with row-level errors.
4. Contributor uploads stay private to the organization until a reviewer verifies them.

## Configuration
* Thresholds: `PUT /api/v1/admin/thresholds` (organization-specific for institutional admins; AP²I defaults for
  super admins).
* Schedules: cron per connector (`PATCH /api/v1/admin/connectors/{key}`), validated on save.
* Countries: `AP2I_ACTIVE_COUNTRIES` + `python -m app.cli activate-countries`.
* AI: `AP2I_LLM_PROVIDER` (`none` default). Secrets only through environment variables.
* Subscriptions: online payment is disabled; requests appear as notifications; grant with
  `POST /api/v1/admin/subscriptions`.

## Command line (`python -m app.cli`)
`seed`, `sync <keys>`, `post-sync`, `rates`, `dispatch`, `create-admin <email>`, `activate-countries`,
`check-country-sources`, `connector-report`, `migrate-mvp <db_url>`.
