# AP²I — Database schema

PostgreSQL 16 with PostGIS. Migrations: `backend/alembic/versions` (`alembic upgrade head`). The ORM models in
`backend/app/models/` are the source of truth; `tests/test_migration.py` checks that migrations and models
match (Alembic autogenerate diff must be empty).

## Conventions
* Monetary values: `NUMERIC(24,4)` (never floats); exchange rates `NUMERIC(24,10)`; percentages `NUMERIC(7,3)`.
* Every amount has its currency next to it; nothing stores a pre-converted total.
* Provenance columns: `source_record_id` (FK → `source_records`) on every fact table; `data_nature`
  (`officially_reported | verified | calculated | estimated | ai_generated | missing | synthetic`) and
  `verification_status` (`unverified | needs_review | verified | rejected`).
* Tenant isolation: `tenant_id` (FK → `organizations`) on projects, agreements, documents, recovery plans and
  source records. `NULL` = public. Enforced by `security.deps.tenant_filter` on every query.
* History: source records are versioned (`is_latest`); observations are corrected by new rows
  (`supersedes_id`); project merges are recorded and reversible (`project_merges.moved`); status changes in
  `project_status_history`; annual snapshots are superseded, never deleted.
* Synthetic guard: CHECK `is_synthetic = false OR data_nature = 'synthetic'` on `projects`.
* PostGIS: `project_locations.geog geography(Point,4326)` is a generated column from latitude/longitude, with a
  GiST index (created by migration 0001 when the extension can be created).

## Entity map (required entities → tables)
| Master prompt entity | Table(s) |
|---|---|
| countries, regions | `countries`, `regions` (administrative divisions), `country_data_sources` |
| sectors, subsectors | `sectors`, `subsectors`, `sector_indicators` |
| organizations, users, roles, user_roles | `organizations`, `users`, `roles`, `user_roles`, `user_tokens`, `api_keys` |
| projects, project_aliases, project_locations, project_status_history, project_milestones | same names + `project_identifiers`, `id_sequences` |
| financing_agreements, financing_instruments, financing_partners, financing_commitments, disbursements | same names + `counterpart_financing` |
| annual_financial_snapshots | same |
| contracts, contract_amendments | same |
| implementation_progress, operational_status | same (`operational_status` = dated observations) |
| results_indicators, results_observations | same |
| project_risks, project_alerts | same + `alert_thresholds` |
| recovery_plans, recovery_actions | same |
| documents | same |
| source_connectors, source_records, source_observations, project_source_links | same + `sync_runs`, `match_candidates`, `project_merges` |
| data_validation, data_quality_assessments, ai_assessments | same |
| audit_logs, subscriptions, payments, reports, notifications, saved_searches | same + `plans`, `app_settings` |
| national budget | `budget_allocations` (appropriations ≠ commitments ≠ disbursements) |
| exchange rates | `exchange_rates` |

## Tables (generated from the models — `python backend/scripts/gen_schema_doc.py`)

### `countries`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `iso2` | VARCHAR(2) | no | unique |
| `iso3` | VARCHAR(3) | no | unique, indexed |
| `iso_numeric` | VARCHAR(3) | yes |  |
| `name_en` | VARCHAR(120) | no |  |
| `name_fr` | VARCHAR(120) | no |  |
| `region` | VARCHAR(40) | no |  |
| `subregion` | VARCHAR(40) | no |  |
| `currency` | VARCHAR(3) | no |  |
| `official_languages` | JSON | no |  |
| `is_active` | BOOLEAN | no |  |
| `reporting_config` | JSON | no |  |
| `reference_status` | VARCHAR(20) | no |  |
| `reference_note` | TEXT | yes |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `exchange_rates`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `base_currency` | VARCHAR(3) | no |  |
| `quote_currency` | VARCHAR(3) | no |  |
| `rate` | NUMERIC(24, 10) | no |  |
| `period` | VARCHAR(10) | no |  |
| `period_type` | VARCHAR(10) | no |  |
| `source` | VARCHAR(120) | no |  |
| `source_url` | TEXT | yes |  |
| `retrieved_at` | DATETIME | no |  |

Unique together: (base_currency, quote_currency, period, period_type, source)

### `financing_instruments`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `code` | VARCHAR(40) | no | unique |
| `name_en` | VARCHAR(120) | no |  |
| `name_fr` | VARCHAR(120) | no |  |

### `id_sequences`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `key` | VARCHAR(40) | no | PK |
| `value` | INTEGER | no |  |

### `plans`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `code` | VARCHAR(30) | no | unique |
| `name_en` | VARCHAR(80) | no |  |
| `name_fr` | VARCHAR(80) | no |  |
| `price_amount` | NUMERIC(24, 4) | yes |  |
| `price_currency` | VARCHAR(3) | yes |  |
| `billing_period` | VARCHAR(20) | yes |  |
| `features` | JSON | no |  |
| `is_public` | BOOLEAN | no |  |
| `sort_order` | INTEGER | no |  |

### `roles`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `code` | VARCHAR(40) | no | unique |
| `name_en` | VARCHAR(80) | no |  |
| `name_fr` | VARCHAR(80) | no |  |
| `permissions` | JSON | no |  |

### `sectors`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `code` | VARCHAR(30) | no | unique |
| `name_en` | VARCHAR(80) | no |  |
| `name_fr` | VARCHAR(80) | no |  |
| `sort_order` | INTEGER | no |  |

### `annual_financial_snapshots`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `country_id` | INTEGER | no | FK → `countries.id`, indexed |
| `year` | INTEGER | no | indexed |
| `computed_at` | DATETIME | no |  |
| `methodology_version` | VARCHAR(20) | no |  |
| `input_fingerprint` | VARCHAR(64) | no |  |
| `payload` | JSON | no |  |
| `is_current` | BOOLEAN | no |  |
| `note` | TEXT | yes |  |

Checks: `year >= 1950 AND year <= 2100`

### `country_data_sources`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `country_id` | INTEGER | no | FK → `countries.id`, indexed |
| `name` | VARCHAR(250) | no |  |
| `institution` | VARCHAR(250) | no |  |
| `category` | VARCHAR(60) | no |  |
| `url` | TEXT | yes |  |
| `access_method` | VARCHAR(40) | no |  |
| `reachability` | VARCHAR(20) | no |  |
| `last_checked_at` | VARCHAR(40) | yes |  |
| `notes` | TEXT | yes |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `organizations`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `name` | VARCHAR(250) | no |  |
| `short_name` | VARCHAR(60) | yes |  |
| `org_type` | VARCHAR(40) | no |  |
| `country_id` | INTEGER | yes | FK → `countries.id` |
| `iati_ref` | VARCHAR(80) | yes | indexed |
| `is_tenant` | BOOLEAN | no |  |
| `website` | TEXT | yes |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `regions`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `country_id` | INTEGER | no | FK → `countries.id`, indexed |
| `parent_id` | INTEGER | yes | FK → `regions.id` |
| `level` | INTEGER | no |  |
| `code` | VARCHAR(20) | no |  |
| `name_en` | VARCHAR(120) | no |  |
| `name_fr` | VARCHAR(120) | no |  |
| `division_type` | VARCHAR(40) | no |  |

Unique together: (country_id, code)

### `sector_indicators`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `sector_id` | INTEGER | no | FK → `sectors.id`, indexed |
| `code` | VARCHAR(60) | no |  |
| `name_en` | VARCHAR(160) | no |  |
| `name_fr` | VARCHAR(160) | no |  |
| `unit` | VARCHAR(40) | no |  |
| `kind` | VARCHAR(20) | no |  |

Unique together: (sector_id, code)

### `subsectors`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `sector_id` | INTEGER | no | FK → `sectors.id`, indexed |
| `code` | VARCHAR(40) | no |  |
| `name_en` | VARCHAR(120) | no |  |
| `name_fr` | VARCHAR(120) | no |  |

Unique together: (sector_id, code)

### `alert_thresholds`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `organization_id` | INTEGER | yes | FK → `organizations.id` |
| `rule_code` | VARCHAR(60) | no |  |
| `parameter` | VARCHAR(60) | no |  |
| `value` | NUMERIC(24, 4) | no |  |

Unique together: (organization_id, rule_code, parameter)

### `financing_partners`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `code` | VARCHAR(40) | no | unique |
| `name` | VARCHAR(250) | no |  |
| `short_name` | VARCHAR(40) | no |  |
| `partner_type` | VARCHAR(40) | no |  |
| `tier` | INTEGER | no |  |
| `organization_id` | INTEGER | yes | FK → `organizations.id` |
| `iati_org_refs` | JSON | no |  |
| `connector_key` | VARCHAR(60) | yes |  |
| `website` | TEXT | yes |  |
| `notes` | TEXT | yes |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `projects`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `ap2i_id` | VARCHAR(40) | no | unique, indexed |
| `country_id` | INTEGER | no | FK → `countries.id`, indexed |
| `tenant_id` | INTEGER | yes | FK → `organizations.id`, indexed |
| `title` | TEXT | no |  |
| `title_language` | VARCHAR(5) | yes |  |
| `description` | TEXT | yes |  |
| `objectives` | TEXT | yes |  |
| `sector_id` | INTEGER | yes | FK → `sectors.id`, indexed |
| `subsector_id` | INTEGER | yes | FK → `subsectors.id` |
| `region_id` | INTEGER | yes | FK → `regions.id` |
| `funding_type` | VARCHAR(40) | no |  |
| `executing_agency` | TEXT | yes |  |
| `supervising_ministry` | TEXT | yes |  |
| `implementing_agency` | TEXT | yes |  |
| `project_owner` | TEXT | yes |  |
| `original_estimated_cost` | NUMERIC(24, 4) | yes |  |
| `revised_estimated_cost` | NUMERIC(24, 4) | yes |  |
| `cost_currency` | VARCHAR(3) | yes |  |
| `original_approval_date` | DATE | yes | indexed |
| `implementation_start_date` | DATE | yes |  |
| `original_completion_date` | DATE | yes |  |
| `revised_completion_date` | DATE | yes |  |
| `actual_completion_date` | DATE | yes |  |
| `commissioning_date` | DATE | yes |  |
| `status` | VARCHAR(20) | no | indexed |
| `status_source` | VARCHAR(200) | yes |  |
| `physical_progress_pct` | NUMERIC(7, 3) | yes |  |
| `physical_progress_date` | DATE | yes |  |
| `operational_status` | VARCHAR(30) | no |  |
| `expected_beneficiaries` | TEXT | yes |  |
| `actual_beneficiaries` | TEXT | yes |  |
| `development_results` | TEXT | yes |  |
| `data_nature` | VARCHAR(30) | no |  |
| `verification_status` | VARCHAR(20) | no | indexed |
| `is_synthetic` | BOOLEAN | no |  |
| `last_verified_at` | DATETIME | yes |  |
| `last_source_update_at` | DATETIME | yes |  |
| `merged_into_id` | INTEGER | yes | FK → `projects.id`, indexed |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

Checks: `physical_progress_pct IS NULL OR (physical_progress_pct >= 0 AND physical_progress_pct <= 100)`; `is_synthetic = false OR data_nature = 'synthetic'`

### `users`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `email` | VARCHAR(254) | no | unique, indexed |
| `password_hash` | VARCHAR(255) | no |  |
| `full_name` | VARCHAR(200) | no |  |
| `organization_id` | INTEGER | yes | FK → `organizations.id`, indexed |
| `locale` | VARCHAR(5) | no |  |
| `is_active` | BOOLEAN | no |  |
| `email_verified_at` | DATETIME | yes |  |
| `mfa_secret` | VARCHAR(64) | yes |  |
| `mfa_enabled` | BOOLEAN | no |  |
| `failed_logins` | INTEGER | no |  |
| `locked_until` | DATETIME | yes |  |
| `last_login_at` | DATETIME | yes |  |
| `token_version` | INTEGER | no |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `ai_assessments`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | yes | FK → `projects.id`, indexed |
| `user_id` | INTEGER | yes | FK → `users.id` |
| `tenant_id` | INTEGER | yes | FK → `organizations.id` |
| `kind` | VARCHAR(40) | no |  |
| `provider` | VARCHAR(40) | no |  |
| `model` | VARCHAR(80) | yes |  |
| `question` | TEXT | yes |  |
| `output` | JSON | no |  |
| `citations` | JSON | no |  |
| `grounding_check` | JSON | no |  |
| `review_status` | VARCHAR(20) | no |  |
| `created_at` | DATETIME | no |  |

### `api_keys`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `user_id` | INTEGER | no | FK → `users.id`, indexed |
| `name` | VARCHAR(100) | no |  |
| `prefix` | VARCHAR(12) | no | indexed |
| `key_hash` | VARCHAR(64) | no | unique |
| `created_at` | DATETIME | no |  |
| `revoked_at` | DATETIME | yes |  |
| `last_used_at` | DATETIME | yes |  |

### `app_settings`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `key` | VARCHAR(80) | no | PK |
| `value` | JSON | no |  |
| `updated_at` | DATETIME | no |  |
| `updated_by` | INTEGER | yes | FK → `users.id` |

### `audit_logs`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `at` | DATETIME | no | indexed |
| `user_id` | INTEGER | yes | FK → `users.id`, indexed |
| `organization_id` | INTEGER | yes | FK → `organizations.id` |
| `action` | VARCHAR(80) | no | indexed |
| `entity_type` | VARCHAR(60) | yes |  |
| `entity_id` | VARCHAR(80) | yes |  |
| `method` | VARCHAR(8) | yes |  |
| `path` | VARCHAR(300) | yes |  |
| `status_code` | INTEGER | yes |  |
| `ip_truncated` | VARCHAR(64) | yes |  |
| `detail` | JSON | no |  |
| `note` | TEXT | yes |  |

### `data_quality_assessments`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `assessed_at` | DATETIME | no |  |
| `completeness` | FLOAT | no |  |
| `timeliness` | FLOAT | yes |  |
| `traceability` | FLOAT | no |  |
| `consistency` | FLOAT | yes |  |
| `source_reliability` | FLOAT | yes |  |
| `duplicate_risk` | FLOAT | yes |  |
| `missing_fields` | JSON | no |  |
| `detail` | JSON | no |  |
| `is_current` | BOOLEAN | no |  |

### `match_candidates`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_a_id` | INTEGER | no | FK → `projects.id`, indexed |
| `project_b_id` | INTEGER | no | FK → `projects.id`, indexed |
| `score` | FLOAT | no |  |
| `features` | JSON | no |  |
| `relation` | VARCHAR(30) | no |  |
| `status` | VARCHAR(20) | no | indexed |
| `created_at` | DATETIME | no |  |
| `reviewed_by` | INTEGER | yes | FK → `users.id` |
| `reviewed_at` | DATETIME | yes |  |
| `review_note` | TEXT | yes |  |

Unique together: (project_a_id, project_b_id)

### `notifications`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `user_id` | INTEGER | yes | FK → `users.id`, indexed |
| `organization_id` | INTEGER | yes | FK → `organizations.id` |
| `kind` | VARCHAR(40) | no |  |
| `title` | TEXT | no |  |
| `body` | TEXT | yes |  |
| `link` | TEXT | yes |  |
| `read_at` | DATETIME | yes |  |
| `created_at` | DATETIME | no |  |

### `project_alerts`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `alert_key` | VARCHAR(64) | no |  |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `rule_code` | VARCHAR(60) | no | indexed |
| `level` | VARCHAR(30) | no | indexed |
| `triggering_indicator` | VARCHAR(120) | no |  |
| `observed_value` | TEXT | yes |  |
| `threshold` | TEXT | yes |  |
| `source` | TEXT | yes |  |
| `source_record_ids` | JSON | no |  |
| `as_of` | DATE | no |  |
| `explanation` | TEXT | no |  |
| `recommended_verification` | TEXT | no |  |
| `review_status` | VARCHAR(20) | no | indexed |
| `reviewed_by` | INTEGER | yes | FK → `users.id` |
| `reviewed_at` | DATETIME | yes |  |
| `review_note` | TEXT | yes |  |
| `is_active` | BOOLEAN | no |  |
| `created_at` | DATETIME | no |  |

### `recovery_plans`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `tenant_id` | INTEGER | yes | FK → `organizations.id`, indexed |
| `title` | TEXT | no |  |
| `diagnosis` | JSON | no |  |
| `status` | VARCHAR(20) | no |  |
| `created_by` | INTEGER | yes | FK → `users.id` |
| `approved_by` | INTEGER | yes | FK → `users.id` |
| `approved_at` | DATETIME | yes |  |
| `method` | VARCHAR(40) | no |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `reports`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `report_uid` | VARCHAR(40) | no | unique |
| `report_type` | VARCHAR(40) | no |  |
| `title` | TEXT | no |  |
| `fmt` | VARCHAR(10) | no |  |
| `params` | JSON | no |  |
| `period` | VARCHAR(40) | yes |  |
| `generated_at` | DATETIME | no |  |
| `generated_by` | INTEGER | yes | FK → `users.id` |
| `tenant_id` | INTEGER | yes | FK → `organizations.id` |
| `sha256` | VARCHAR(64) | no |  |
| `size_bytes` | INTEGER | no |  |
| `storage_key` | TEXT | no |  |

### `saved_searches`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `user_id` | INTEGER | no | FK → `users.id`, indexed |
| `name` | VARCHAR(120) | no |  |
| `query` | JSON | no |  |
| `created_at` | DATETIME | no |  |

### `source_connectors`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `key` | VARCHAR(60) | no | unique |
| `name` | VARCHAR(200) | no |  |
| `partner_id` | INTEGER | yes | FK → `financing_partners.id` |
| `tier` | INTEGER | no |  |
| `enabled` | BOOLEAN | no |  |
| `status` | VARCHAR(20) | no |  |
| `status_evidence` | TEXT | yes |  |
| `access_method` | VARCHAR(60) | no |  |
| `base_url` | TEXT | yes |  |
| `documentation_url` | TEXT | yes |  |
| `usage_terms` | TEXT | yes |  |
| `update_frequency` | VARCHAR(80) | yes |  |
| `config` | JSON | no |  |
| `schedule_cron` | VARCHAR(60) | yes |  |
| `last_success_at` | DATETIME | yes |  |
| `last_failure_at` | DATETIME | yes |  |
| `last_error` | TEXT | yes |  |
| `cursor` | JSON | no |  |
| `notes` | TEXT | yes |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `subscriptions`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `plan_id` | INTEGER | no | FK → `plans.id` |
| `user_id` | INTEGER | yes | FK → `users.id`, indexed |
| `organization_id` | INTEGER | yes | FK → `organizations.id`, indexed |
| `status` | VARCHAR(20) | no |  |
| `starts_on` | DATE | yes |  |
| `ends_on` | DATE | yes |  |
| `seats` | INTEGER | yes |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `user_roles`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `user_id` | INTEGER | no | FK → `users.id`, indexed |
| `role_id` | INTEGER | no | FK → `roles.id` |
| `organization_id` | INTEGER | yes | FK → `organizations.id` |
| `granted_at` | DATETIME | no |  |

Unique together: (user_id, role_id, organization_id)

### `user_tokens`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `user_id` | INTEGER | no | FK → `users.id`, indexed |
| `purpose` | VARCHAR(30) | no |  |
| `token_hash` | VARCHAR(64) | no | unique |
| `expires_at` | DATETIME | no |  |
| `used_at` | DATETIME | yes |  |
| `created_at` | DATETIME | no |  |

### `payments`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `subscription_id` | INTEGER | no | FK → `subscriptions.id`, indexed |
| `provider` | VARCHAR(40) | no |  |
| `provider_reference` | VARCHAR(200) | yes |  |
| `amount` | NUMERIC(24, 4) | no |  |
| `currency` | VARCHAR(3) | no |  |
| `status` | VARCHAR(20) | no |  |
| `created_at` | DATETIME | no |  |

### `project_merges`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `survivor_id` | INTEGER | no | FK → `projects.id`, indexed |
| `merged_id` | INTEGER | no | FK → `projects.id`, indexed |
| `match_candidate_id` | INTEGER | yes | FK → `match_candidates.id` |
| `merged_by` | INTEGER | yes | FK → `users.id` |
| `merged_at` | DATETIME | no |  |
| `reason` | TEXT | yes |  |
| `moved` | JSON | no |  |
| `reversed_at` | DATETIME | yes |  |
| `reversed_by` | INTEGER | yes | FK → `users.id` |

### `recovery_actions`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `plan_id` | INTEGER | no | FK → `recovery_plans.id`, indexed |
| `problem` | TEXT | no |  |
| `evidence` | JSON | no |  |
| `contributing_factors` | TEXT | no |  |
| `recommended_action` | TEXT | no |  |
| `responsible_institution` | TEXT | yes |  |
| `priority` | VARCHAR(20) | no |  |
| `estimated_timeframe` | VARCHAR(120) | yes |  |
| `indicative_budget` | NUMERIC(24, 4) | yes |  |
| `budget_currency` | VARCHAR(3) | yes |  |
| `dependencies` | TEXT | yes |  |
| `expected_result` | TEXT | yes |  |
| `monitoring_indicator` | TEXT | yes |  |
| `origin` | VARCHAR(20) | no |  |
| `data_nature` | VARCHAR(30) | no |  |
| `approval_status` | VARCHAR(20) | no |  |
| `implementation_status` | VARCHAR(20) | no |  |
| `assigned_to` | TEXT | yes |  |
| `due_date` | DATE | yes |  |
| `progress_note` | TEXT | yes |  |
| `decided_by` | INTEGER | yes | FK → `users.id` |
| `decided_at` | DATETIME | yes |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `sync_runs`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `connector_id` | INTEGER | no | FK → `source_connectors.id`, indexed |
| `trigger` | VARCHAR(20) | no |  |
| `started_at` | DATETIME | no |  |
| `finished_at` | DATETIME | yes |  |
| `status` | VARCHAR(20) | no |  |
| `params` | JSON | no |  |
| `attempts` | INTEGER | no |  |
| `records_retrieved` | INTEGER | no |  |
| `records_new` | INTEGER | no |  |
| `records_unchanged` | INTEGER | no |  |
| `records_imported` | INTEGER | no |  |
| `records_review` | INTEGER | no |  |
| `records_failed` | INTEGER | no |  |
| `errors` | JSON | no |  |
| `log` | TEXT | yes |  |

### `source_records`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `connector_id` | INTEGER | no | FK → `source_connectors.id`, indexed |
| `sync_run_id` | INTEGER | yes | FK → `sync_runs.id` |
| `source_identifier` | VARCHAR(200) | no | indexed |
| `record_type` | VARCHAR(40) | no |  |
| `country_iso3` | VARCHAR(3) | yes | indexed |
| `payload` | JSON | no |  |
| `payload_format` | VARCHAR(10) | no |  |
| `raw_text` | TEXT | yes |  |
| `payload_sha256` | VARCHAR(64) | no |  |
| `source_url` | TEXT | yes |  |
| `source_last_updated` | VARCHAR(40) | yes |  |
| `retrieved_at` | DATETIME | no |  |
| `is_latest` | BOOLEAN | no | indexed |
| `processing_status` | VARCHAR(20) | no |  |
| `processing_note` | TEXT | yes |  |
| `verification_status` | VARCHAR(20) | no |  |
| `tenant_id` | INTEGER | yes | FK → `organizations.id` |

Unique together: (connector_id, source_identifier, payload_sha256)

### `budget_allocations`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `country_id` | INTEGER | no | FK → `countries.id`, indexed |
| `project_id` | INTEGER | yes | FK → `projects.id`, indexed |
| `budget_year` | INTEGER | no | indexed |
| `budget_line_code` | VARCHAR(80) | no |  |
| `project_identifier` | VARCHAR(120) | yes |  |
| `project_label` | TEXT | yes |  |
| `administrative_classification` | TEXT | yes |  |
| `program_classification` | TEXT | yes |  |
| `funding_source` | TEXT | yes |  |
| `funding_type` | VARCHAR(40) | no |  |
| `currency` | VARCHAR(3) | no |  |
| `approved_appropriation` | NUMERIC(24, 4) | yes |  |
| `revised_appropriation` | NUMERIC(24, 4) | yes |  |
| `commitment` | NUMERIC(24, 4) | yes |  |
| `payment` | NUMERIC(24, 4) | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |

Unique together: (country_id, budget_year, budget_line_code, source_record_id)

### `contracts`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `reference` | VARCHAR(120) | yes |  |
| `title` | TEXT | no |  |
| `contractor` | TEXT | yes |  |
| `procurement_method` | VARCHAR(80) | yes |  |
| `signature_date` | DATE | yes |  |
| `original_amount` | NUMERIC(24, 4) | yes |  |
| `currency` | VARCHAR(3) | yes |  |
| `original_end_date` | DATE | yes |  |
| `paid_to_date` | NUMERIC(24, 4) | yes |  |
| `paid_as_of` | DATE | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `counterpart_financing`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `financier_type` | VARCHAR(30) | no |  |
| `financier_name` | TEXT | yes |  |
| `amount` | NUMERIC(24, 4) | yes |  |
| `currency` | VARCHAR(3) | yes |  |
| `as_of` | DATE | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |

### `data_validation`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `source_record_id` | INTEGER | yes | FK → `source_records.id`, indexed |
| `project_id` | INTEGER | yes | FK → `projects.id`, indexed |
| `rule` | VARCHAR(80) | no |  |
| `severity` | VARCHAR(10) | no |  |
| `message` | TEXT | no |  |
| `status` | VARCHAR(20) | no |  |
| `created_at` | DATETIME | no |  |
| `resolved_by` | INTEGER | yes | FK → `users.id` |
| `resolved_at` | DATETIME | yes |  |

### `documents`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | yes | FK → `projects.id`, indexed |
| `tenant_id` | INTEGER | yes | FK → `organizations.id`, indexed |
| `title` | TEXT | no |  |
| `doc_type` | VARCHAR(80) | yes |  |
| `url` | TEXT | yes |  |
| `language` | VARCHAR(5) | yes |  |
| `published_date` | DATE | yes |  |
| `storage_key` | TEXT | yes |  |
| `sha256` | VARCHAR(64) | yes | indexed |
| `mime_type` | VARCHAR(100) | yes |  |
| `size_bytes` | INTEGER | yes |  |
| `extracted_text` | TEXT | yes |  |
| `injection_flags` | JSON | no |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `financing_agreements`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `partner_id` | INTEGER | yes | FK → `financing_partners.id`, indexed |
| `instrument_id` | INTEGER | yes | FK → `financing_instruments.id` |
| `tenant_id` | INTEGER | yes | FK → `organizations.id`, indexed |
| `source_identifier` | VARCHAR(120) | no |  |
| `name` | TEXT | yes |  |
| `instrument_label` | VARCHAR(200) | yes |  |
| `approval_date` | DATE | yes | indexed |
| `signature_date` | DATE | yes |  |
| `effectiveness_date` | DATE | yes |  |
| `closing_date_original` | DATE | yes |  |
| `closing_date_current` | DATE | yes |  |
| `status` | VARCHAR(20) | no |  |
| `currency` | VARCHAR(3) | yes |  |
| `amount_original` | NUMERIC(24, 4) | yes |  |
| `amount_label` | VARCHAR(200) | yes |  |
| `reported_current_commitment` | NUMERIC(24, 4) | yes |  |
| `reported_cumulative_disbursed` | NUMERIC(24, 4) | yes |  |
| `reported_undisbursed` | NUMERIC(24, 4) | yes |  |
| `reported_cumulative_as_of` | DATE | yes |  |
| `reported_cumulative_label` | VARCHAR(300) | yes |  |
| `parent_source_identifier` | VARCHAR(120) | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |
| `verification_status` | VARCHAR(20) | no |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

Unique together: (partner_id, source_identifier)

### `project_aliases`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `alias` | TEXT | no |  |
| `language` | VARCHAR(5) | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |

Unique together: (project_id, alias)

### `project_identifiers`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `scheme` | VARCHAR(30) | no |  |
| `identifier` | VARCHAR(200) | no | indexed |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `created_at` | DATETIME | no |  |

Unique together: (scheme, identifier)

### `project_locations`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `region_id` | INTEGER | yes | FK → `regions.id` |
| `place_name` | TEXT | yes |  |
| `latitude` | NUMERIC(9, 6) | yes |  |
| `longitude` | NUMERIC(9, 6) | yes |  |
| `precision` | VARCHAR(40) | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |

### `project_milestones`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `name` | TEXT | no |  |
| `planned_date` | DATE | yes |  |
| `revised_date` | DATE | yes |  |
| `actual_date` | DATE | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |

### `project_risks`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `category` | VARCHAR(60) | no |  |
| `description` | TEXT | no |  |
| `rating` | VARCHAR(30) | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |
| `created_at` | DATETIME | no |  |
| `updated_at` | DATETIME | no |  |

### `project_source_links`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `source_record_id` | INTEGER | no | FK → `source_records.id`, indexed |
| `link_type` | VARCHAR(30) | no |  |
| `match_rule` | VARCHAR(120) | yes |  |
| `match_score` | FLOAT | yes |  |
| `linked_by` | INTEGER | yes | FK → `users.id` |
| `linked_at` | DATETIME | no |  |
| `active` | BOOLEAN | no |  |

Unique together: (project_id, source_record_id)

### `project_status_history`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `status` | VARCHAR(20) | no |  |
| `previous_status` | VARCHAR(20) | yes |  |
| `effective_date` | DATE | yes |  |
| `recorded_at` | DATETIME | no |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `note` | TEXT | yes |  |

### `results_indicators`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `sector_indicator_id` | INTEGER | yes | FK → `sector_indicators.id` |
| `name` | TEXT | no |  |
| `unit` | VARCHAR(60) | yes |  |
| `measure` | VARCHAR(20) | yes |  |
| `baseline_value` | NUMERIC(24, 4) | yes |  |
| `baseline_date` | DATE | yes |  |
| `target_value` | NUMERIC(24, 4) | yes |  |
| `target_date` | DATE | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |

### `source_observations`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `source_record_id` | INTEGER | no | FK → `source_records.id`, indexed |
| `project_id` | INTEGER | yes | FK → `projects.id`, indexed |
| `field` | VARCHAR(80) | no |  |
| `source_field` | VARCHAR(200) | yes |  |
| `value_text` | TEXT | yes |  |
| `value_numeric` | NUMERIC(24, 4) | yes |  |
| `value_date` | DATE | yes |  |
| `currency` | VARCHAR(3) | yes |  |
| `reporting_date` | DATE | yes |  |
| `extracted_at` | DATETIME | no |  |
| `data_nature` | VARCHAR(30) | no |  |
| `verification_status` | VARCHAR(20) | no |  |
| `supersedes_id` | INTEGER | yes | FK → `source_observations.id` |
| `correction_note` | TEXT | yes |  |

### `contract_amendments`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `contract_id` | INTEGER | no | FK → `contracts.id`, indexed |
| `amendment_date` | DATE | yes |  |
| `amount_change` | NUMERIC(24, 4) | yes |  |
| `currency` | VARCHAR(3) | yes |  |
| `new_end_date` | DATE | yes |  |
| `reason` | TEXT | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |

### `disbursements`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `agreement_id` | INTEGER | no | FK → `financing_agreements.id`, indexed |
| `flow_type` | VARCHAR(20) | no |  |
| `amount` | NUMERIC(24, 4) | no |  |
| `currency` | VARCHAR(3) | no |  |
| `value_date` | DATE | yes | indexed |
| `period_year` | INTEGER | yes | indexed |
| `transaction_key` | VARCHAR(200) | no |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |
| `is_counted` | BOOLEAN | no |  |
| `counting_note` | TEXT | yes |  |

Unique together: (agreement_id, transaction_key)

### `financing_commitments`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `agreement_id` | INTEGER | no | FK → `financing_agreements.id`, indexed |
| `commitment_type` | VARCHAR(20) | no |  |
| `amount` | NUMERIC(24, 4) | no |  |
| `currency` | VARCHAR(3) | no |  |
| `value_date` | DATE | yes | indexed |
| `transaction_key` | VARCHAR(200) | no |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |
| `is_counted` | BOOLEAN | no |  |
| `counting_note` | TEXT | yes |  |

Unique together: (agreement_id, transaction_key)

### `implementation_progress`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `report_date` | DATE | no |  |
| `physical_progress_pct` | NUMERIC(7, 3) | yes |  |
| `financial_progress_pct` | NUMERIC(7, 3) | yes |  |
| `narrative` | TEXT | yes |  |
| `rating` | VARCHAR(60) | yes |  |
| `document_id` | INTEGER | yes | FK → `documents.id` |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |
| `verification_status` | VARCHAR(20) | no |  |

### `operational_status`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `project_id` | INTEGER | no | FK → `projects.id`, indexed |
| `status` | VARCHAR(30) | no |  |
| `observed_date` | DATE | no |  |
| `evidence` | TEXT | yes |  |
| `document_id` | INTEGER | yes | FK → `documents.id` |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `verification_status` | VARCHAR(20) | no |  |

### `results_observations`

| Column | Type | Null | Key / reference |
|---|---|---|---|
| `id` | INTEGER | no | PK |
| `indicator_id` | INTEGER | no | FK → `results_indicators.id`, indexed |
| `value` | NUMERIC(24, 4) | yes |  |
| `value_text` | TEXT | yes |  |
| `period_start` | DATE | yes |  |
| `period_end` | DATE | yes |  |
| `source_record_id` | INTEGER | yes | FK → `source_records.id` |
| `data_nature` | VARCHAR(30) | no |  |

