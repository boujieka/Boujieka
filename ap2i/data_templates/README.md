# Import templates

Use these templates only to transcribe **official documents** (finance law annexes, budget execution reports,
donor project documents, implementation reports). One row per project (or budget line).

* `projects_import_template.csv` — required: `country_iso3`, `source_project_id`, `title`, `source_url`,
  `reporting_date` (YYYY-MM-DD). Amounts in their original currency with the currency code. `funder_code` uses
  the donor registry codes (`WB`, `AFDB`, `AFD`, `EIB`, `EU`, `ISDB`, `KFW`, `JICA`, `GEF`, `GCF`, `BADEA`,
  `SFD`, `KFAED`, `ADFD`, `IFAD`, `UNDP`, `UNICEF`, `FAO`, `UNIDO`, `BMZ`, `GOV` for national resources).
  `status`: pipeline | approved | active | completed | closed | suspended | cancelled | dropped | unknown.
  `operational_status`: operational | partially_operational | not_operational | unknown.
* `budget_lines_template.csv` — required: `country_iso3`, `budget_year`, `budget_line_code`, `currency`,
  `source_url`, `reporting_date`. Appropriations are **not** commitments or disbursements.

Leave unknown values empty — never 0. CSV in UTF-8 (`,` or `;`), or `.xlsx` with the same header row.
Upload: Admin → Uploads, or `POST /api/v1/uploads/projects` / `POST /api/v1/uploads/budget-lines`.
