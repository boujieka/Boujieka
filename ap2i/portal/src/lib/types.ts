// Shapes of the public snapshot written by `python -m app.cli export-public-snapshot` (backend/app/publish/snapshot.py).
// Monetary values are decimal strings (exact, as stored); null means "not available", never zero.

export type Dec = string | null;

export interface ProjectRow {
  id: number;
  ref: string;
  title: string;
  country: string;
  sector: string | null;
  region: string | null;
  status: string;
  operational_status: string;
  verification: string;
  approval: string | null;
  start: string | null;
  planned_end: string | null;
  revised_end: string | null;
  actual_end: string | null;
  current_end: string | null;
  portfolio_end: string | null;
  agency: string | null;
  partners: string[];
  instruments: string[];
  alerts: Partial<Record<AlertLevel, number>>;
  physical_progress: Dec;
  original_cost: Dec;
  revised_cost: Dec;
  cost_currency: string | null;
  documents: number;
  results_indicators: number;
  latest_rating: { date: string | null; rating: string } | null;
  dq: { completeness: number; traceability: number; timeliness: number | null } | null;
  locations: { lat: string; lon: string; precision: string | null; place: string | null }[];
  last_source_update: string | null;
  commissioning?: string | null;
  status_source?: string | null;
}

export interface AgreementRow {
  id: number;
  project: number;
  source_identifier: string;
  partner: string | null;
  instrument: string | null;
  instrument_label: string | null;
  approval: string | null;
  closing_original: string | null;
  closing_current: string | null;
  status: string;
  currency: string | null;
  amount_original: Dec;
  committed: Dec;
  committed_basis: string | null;
  cancelled: Dec;
  disbursed: Dec;
  disbursed_basis: string | null;
  disbursed_as_of: string | null;
  undisbursed: Dec;
  is_guarantee: boolean;
  parent: string | null;
  committed_usd: Dec;
  committed_usd_note: string | null;
  source_record_id: number | null;
}

export interface FlowTable {
  kind: ("commitment" | "disbursement" | "expenditure")[];
  agreement: number[];
  date: (string | null)[];
  year: (number | null)[];
  amount: string[];
  currency: string[];
  usd: Dec[];
  rate_source: (string | null)[];
}

export type AlertLevel = "critical_attention" | "high_attention" | "watch" | "information";

export interface Country {
  iso3: string;
  iso2: string;
  name_en: string;
  name_fr: string;
  region: string;
  currency: string;
  is_active: boolean;
  documented_projects: number;
  data_coverage: string;
}

export interface Ref {
  countries: Country[];
  sectors: { code: string; name_en: string; name_fr: string }[];
  partners: { code: string; name: string; short_name: string; partner_type: string; website: string | null }[];
  instruments: { code: string; name_en: string; name_fr: string }[];
  methodology: Record<string, unknown>;
  alert_rules: { code: string; label: string; indicator: string; thresholds: Record<string, string> }[];
  rate_sources: string[];
}

export interface AlertItem {
  id: number;
  alert_id: string;
  rule_code: string;
  level: AlertLevel;
  triggering_indicator: string;
  observed_value: string;
  threshold: string;
  source: string;
  source_record_ids: number[];
  as_of: string;
  explanation: string;
  recommended_verification: string;
  review_status: string;
  project: { id: number; ap2i_id: string; title: string };
}

export interface Meta {
  snapshot_version: number;
  generated_at: string;
  countries: string[];
  years: [number, number];
  counts: { projects: number; agreements: number; transactions: number; alerts: number };
  latest_source_update: string | null;
  connectors: { key: string; name: string; status: string; last_success: string | null }[];
  reconciliation: { country: string; ok: boolean; check?: string; method?: string }[];
  scope: string;
  checksum: string;
}

export interface Snapshot {
  meta: Meta;
  ref: Ref;
  projects: ProjectRow[];
  agreements: AgreementRow[];
  flows: FlowTable;
  alerts: { total: number; items: AlertItem[]; summary_by_level: Record<string, number>; disclaimer: string };
  dataQuality: DataQuality;
  africa: { countries: AfricaCountry[] };
}

export interface AfricaCountry {
  iso3: string;
  has_data: boolean;
  documented_projects: number | null;
  last_update: string | null;
}

export interface DataQuality {
  projects: number;
  missing_information: Record<string, number>;
  average_scores: Record<string, number>;
  outdated_observations: number;
  potential_duplicates: number;
  records_requiring_review: number;
  connectors: { key: string; name: string; enabled: boolean; status: string; last_success_at: string | null; records_stored: number }[];
  coverage_warning: string;
}
