/** Shapes returned by the AP²I API (see backend app/api/*.py). Decimals are strings; dates are ISO strings. */
export type Money = Record<string, string>;

export interface Me {
  id: number;
  email: string;
  full_name: string;
  locale: string;
  email_verified: boolean;
  mfa_enabled: boolean;
  organization: { id: number; name: string } | null;
  roles: string[];
  permissions: string[] | null;
  features: string[] | null;
}

export interface Country {
  iso2: string;
  iso3: string;
  iso_numeric: string;
  name_en: string;
  name_fr: string;
  region: string | null;
  subregion: string | null;
  currency: string | null;
  official_languages: string[] | null;
  is_active: boolean;
  reference_status: string | null;
  documented_projects: number;
  data_coverage: string;
}

export interface OverviewCountry {
  iso3: string;
  iso2: string;
  iso_numeric: string;
  name_en: string;
  name_fr: string;
  is_active: boolean;
  has_data: boolean;
  documented_projects: number | null;
  commitments_usd: string | null;
  commitments_usd_note?: string;
  commitments_by_currency: Money | null;
  disbursements_by_currency?: Money | null;
  disbursements_usd?: string | null;
  under_implementation: number | null;
  completed: number | null;
  operational: number | null;
  operational_unknown?: number | null;
  requiring_attention: number | null;
  last_update: string | null;
  data_coverage: string;
}

export interface Overview {
  countries: OverviewCountry[];
  filters: Record<string, string | number | null>;
}

export interface SectorRef { code: string; name_en: string; name_fr: string }

export interface ProjectSummary {
  id: number;
  ap2i_id: string;
  title: string;
  status: string;
  operational_status: string | null;
  verification_status: string | null;
  data_nature: string | null;
  original_approval_date: string | null;
  implementation_start_date: string | null;
  original_completion_date: string | null;
  actual_completion_date: string | null;
  executing_agency: string | null;
  last_source_update_at: string | null;
  country: string | null;
  sector: SectorRef | null;
  region: { code: string; name_fr: string; name_en: string } | null;
  partners: string[];
  private: boolean;
  active_alerts?: number;
  committed_by_currency?: Money;
}

export interface ProjectList { total: number; limit: number; offset: number; items: ProjectSummary[] }

export interface Indicator {
  code: string;
  label: string;
  value: string | number | null;
  unit: string;
  formula: string;
  inputs: { name: string; value: unknown; currency?: string | null; basis?: string }[];
  as_of: string | null;
  limitations: string[];
  missing_inputs: string[];
  data_nature: string;
}

export interface Alert {
  id: number;
  alert_id: string;
  rule_code: string;
  level: string;
  triggering_indicator: string | null;
  observed_value: string | null;
  threshold: string | null;
  source: string | null;
  source_record_ids: number[] | null;
  as_of: string | null;
  explanation: string | null;
  recommended_verification: string | null;
  review_status: string;
  review_note?: string | null;
  project?: { id: number; ap2i_id: string; title: string };
}

export interface Agreement {
  id: number;
  source_identifier: string | null;
  name: string | null;
  instrument_label: string | null;
  approval_date: string | null;
  signature_date: string | null;
  closing_date_original: string | null;
  closing_date_current: string | null;
  status: string | null;
  currency: string | null;
  amount_original: string | null;
  amount_label: string | null;
  reported_current_commitment: string | null;
  reported_cumulative_disbursed: string | null;
  reported_undisbursed: string | null;
  reported_cumulative_as_of: string | null;
  reported_cumulative_label: string | null;
  parent_source_identifier: string | null;
  data_nature: string | null;
  verification_status: string | null;
  partner: { code: string; name: string } | null;
  instrument: string | null;
  source: { record_id: number; url: string | null; connector: string; retrieved_at: string | null } | null;
  commitments: { commitment_type: string; amount: string | null; currency: string | null; value_date: string | null; is_counted: boolean; counting_note: string | null; source_record_id: number | null }[];
  flows_count: number;
}

export interface AgreementPosition {
  agreement_id: number;
  partner: string | null;
  source_identifier: string | null;
  currency: string | null;
  committed: string | null;
  committed_basis: string | null;
  cancelled: string | null;
  disbursed: string | null;
  disbursed_basis: string | null;
  disbursed_as_of: string | null;
  undisbursed: string | null;
  expenditure: string | null;
  source_record_ids: number[];
}

export interface ProjectDetail extends ProjectSummary {
  description: string | null;
  objectives: string | null;
  funding_type: string | null;
  supervising_ministry: string | null;
  implementing_agency: string | null;
  project_owner: string | null;
  original_estimated_cost: string | null;
  revised_estimated_cost: string | null;
  cost_currency: string | null;
  revised_completion_date: string | null;
  commissioning_date: string | null;
  physical_progress_pct: string | null;
  physical_progress_date: string | null;
  expected_beneficiaries: string | null;
  actual_beneficiaries: string | null;
  development_results: string | null;
  status_source: string | null;
  last_verified_at: string | null;
  created_at: string | null;
  aliases: { alias: string; language: string | null }[];
  identifiers: { scheme: string; identifier: string }[];
  agreements: Agreement[];
  financials: { agreements: AgreementPosition[]; totals_by_currency: Record<string, Record<string, string | null>>; indicators: Indicator[]; note: string };
  annual_flows: { year: number; currency: string; flow: string; amount: string }[];
  sources: { record_id: number; connector: string; connector_name: string; source_identifier: string; url: string | null; retrieved_at: string | null; source_last_updated: string | null; link_type: string; match_rule: string | null; is_latest: boolean }[];
  documents: { id: number; title: string | null; doc_type: string | null; url: string | null; language: string | null; published_date: string | null }[];
  locations: { place_name: string | null; latitude: string | null; longitude: string | null; precision: string | null; region: number | null }[];
  status_history: { status: string; previous_status: string | null; effective_date: string | null; recorded_at: string | null; note: string | null; source_record_id: number | null }[];
  alerts: Alert[];
  results: { name: string; unit: string | null; measure: string | null; baseline_value: string | null; target_value: string | null; target_date: string | null; observations: { value: string | null; value_text: string | null; period_end: string | null; data_nature: string | null }[] }[];
  implementation_progress: {
    report_date: string | null; physical_progress_pct: string | null; financial_progress_pct: string | null; narrative: string | null;
    rating: string | null; data_nature: string; verification_status: string; source_record_id: number | null;
    document: { id: number; title: string; doc_type: string | null; url: string | null } | null;
  }[];
  data_quality: { completeness: number | null; timeliness: number | null; traceability: number | null; consistency: number | null; source_reliability: number | null; duplicate_risk: number | null; missing_fields: string[]; assessed_at: string | null } | null;
  validation_issues: { rule: string; severity: string; message: string; status: string }[];
  pending_match_candidates: number;
  observations: { field: string; source_field: string | null; value_text: string | null; value_numeric: string | null; value_date: string | null; currency: string | null; reporting_date: string | null; extracted_at: string | null; data_nature: string | null; verification_status: string | null; source_record_id: number | null }[] | null;
  observations_note?: string;
}

export interface FlowSlot {
  by_currency: Money;
  usd_equivalent: string | null;
  usd_complete: boolean;
  unconverted: Record<string, unknown>;
  rate_sources: string[];
  usd_by_sector: Money;
  usd_by_partner: Money;
  transactions: number;
  projects: number;
}

export interface PortfolioYear {
  year: number;
  counts: { approved: number | null; active: number | null; completed: number | null; completed_closing_date_proxy?: number | null; commissioned: number | null; suspended: number | null; cancelled: number | null; undated_projects_excluded?: number | null };
  commitments: FlowSlot;
  disbursements: FlowSlot;
  expenditures: FlowSlot;
}

export interface Portfolio {
  country: string;
  first_year: number;
  last_year: number;
  methodology_version: string;
  projects_in_scope: number;
  has_data?: boolean;
  years: PortfolioYear[];
  coverage_note: string;
}

export interface Dashboard {
  country: { iso3: string; name_en: string; name_fr: string; currency: string | null; is_active: boolean };
  documented_projects: number;
  by_status: Record<string, number>;
  by_sector: { code: string; name_en: string; name_fr: string; projects: number; active: number; committed_usd: string }[];
  by_partner: { partner: string; code: string | null; agreements: number; committed_by_currency: Money; disbursed_by_currency: Money; committed_usd: string }[];
  alerts_by_level: Record<string, number>;
  data_gaps: Record<string, number>;
  average_quality: Record<string, number | null>;
  usd_method: string;
  coverage_warning: string;
}

export interface CountryDetail {
  iso2: string; iso3: string; iso_numeric: string; name_en: string; name_fr: string; region: string | null; subregion: string | null;
  currency: string | null; official_languages: string[] | null; is_active: boolean; reference_status: string | null; reference_note: string | null;
  admin_divisions: { code: string; name_en: string; name_fr: string; level: number; division_type: string }[];
  data_sources: { name: string; institution: string; category: string; url: string | null; access_method: string; reachability: string; last_checked_at: string | null; notes: string | null }[];
}

export interface Sector extends SectorRef { id: number; indicators: { code: string; name_en: string; name_fr: string; unit: string; kind: string }[] }

export interface Partner { id: number; code: string; name: string; short_name: string; partner_type: string; tier: number; connector: { key: string; status: string; enabled: boolean } | null }

export interface Instrument { code: string; name_en: string; name_fr: string }

export interface ConnectorStatus {
  key: string; name: string; tier: number; enabled: boolean; status: string; last_success_at: string | null; last_failure_at: string | null; last_error: string | null; records_stored: number;
  last_run: { id: number; status: string; retrieved: number; imported: number; review: number; failed: number; finished_at: string | null } | null;
}

export interface DataQuality {
  projects: number;
  verification: Record<string, number>;
  verified_records: number;
  unverified_records: number;
  records_requiring_review: number;
  missing_information: Record<string, number>;
  outdated_observations: number;
  potential_duplicates: number;
  failed_imports: number;
  average_scores: Record<string, number | null>;
  connectors: ConnectorStatus[];
  coverage_warning?: string;
}

export interface AssistantAnswer {
  question: string;
  parsed: { intent: string; [k: string]: unknown };
  facts: Record<string, unknown>[];
  calculations: Record<string, unknown>[];
  interpretations: string[];
  recommendations: string[];
  missing_information: string[];
  citations: { ap2i_id: string; project_id: number; title: string; sources: string[] }[];
  narrative: string | null;
  provider: string;
  grounding: { passed?: boolean; numbers_in_narrative?: number; unsupported_numbers?: string[]; error?: string; [k: string]: unknown };
  data_nature: Record<string, string | null>;
  disclaimer: string;
}

export interface RescueAction {
  id: number; problem: string; evidence: Record<string, unknown>[] | null; contributing_factors: unknown; recommended_action: string | null;
  responsible_institution: string | null; priority: string | null; estimated_timeframe: string | null; indicative_budget: string | null;
  budget_currency: string | null; dependencies: unknown; expected_result: string | null; monitoring_indicator: string | null; origin: string;
  data_nature: string | null; approval_status: string; implementation_status: string; assigned_to: string | null; due_date: string | null;
  progress_note: string | null; decided_at: string | null;
}

export interface RescuePlan {
  id: number; title: string; status: string; method: string | null; created_at: string; updated_at: string; approved_at: string | null;
  diagnosis: Record<string, unknown> | null; project: { id: number; ap2i_id: string; title: string }; private: boolean;
  summary: { actions: number; approved: number; done: number; by_status: Record<string, number>; completion_rate: number | null };
  actions: RescueAction[];
}
