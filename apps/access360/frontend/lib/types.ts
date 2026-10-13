// Shapes returned by the ACCESS360 API (see apps/access360/docs/openapi.json and the backend routers).

export type Role = "owner" | "admin" | "analyst" | "viewer";

export interface OrgMembership {
  id: string;
  name: string;
  kind: string;
  role: Role;
  plan: string | null;
  accreditation_status: string;
  is_demo: boolean;
}

export interface Me {
  id: string;
  email: string;
  full_name: string;
  locale: "en" | "fr";
  mfa_enabled: boolean;
  is_superadmin: boolean;
  organizations: OrgMembership[];
  session_mfa: boolean;
}

export type RunStatus = "validated" | "warning" | "failed_checks" | "incomplete_inputs";

export interface RunKey {
  capex_total_usd: number | null;
  connections_target: number | null;
  project_irr_post_subsidy: number | null;
  equity_irr: number | null;
  dscr_min: number | null;
  lcoe_per_kwh_sold_usd: number | null;
  viability_gap_per_connection: number | null;
}

export interface RunSummary {
  id: string;
  status: RunStatus;
  created_at: string;
  engine_version: string;
  inputs_version: number;
  is_demo: boolean;
  key: RunKey;
}

export interface Check {
  code: string;
  label: unknown;
  passed: unknown;
  detail: unknown;
}

export interface RunDetail extends RunSummary {
  metrics: Record<string, number | null>;
  checks: Check[];
  warnings: Check[];
  missing_inputs: string[];
  annual: Record<string, (number | null)[]>;
  quarterly: { date: string[] } & Record<string, (number | null)[] | string[]>;
  sources_uses: Record<string, number | null>;
  inputs_sha256: string;
}

export interface Project {
  id: string;
  name: string;
  country: string;
  technology: string;
  stage: string;
  latitude: number | null;
  longitude: number | null;
  geometry: unknown;
  is_demo: boolean;
  inputs_version: number;
  has_inputs: boolean;
  updated_at: string;
  latest_run: RunSummary | null;
  inputs?: ProjectInputs | null;
}

export interface Country {
  iso3: string;
  name: string;
  has_profile?: boolean;
  /** [west, south, east, north] of the Natural Earth admin 0 boundary, or null */
  bbox?: [number, number, number, number] | null;
}

export interface CountryIndicator {
  key: string;
  title: string;
  unit: string;
  description: string;
  value: number | null;
  year: number | null;
  source: string;
  source_key: string;
  licence: string;
  attribution: string;
  quality: string;
}

export interface ReferenceSource {
  key: string;
  kind: "dataset" | "indicators";
  title: string;
  source_institution: string;
  source_title: string | null;
  version: string | null;
  publication_date: string | null;
  retrieval_date: string;
  licence: string;
  attribution: string;
  quality: string;
  limitations: string | null;
  urls: string[];
}

export interface CountryProfile {
  iso3: string;
  name: string;
  bbox: [number, number, number, number] | null;
  indicators: CountryIndicator[];
  admin1_count: number;
  places_count: number;
  sources: ReferenceSource[];
}

export interface Milestone {
  id: string;
  title: string;
  category: string;
  due_date: string | null;
  status: "open" | "in_progress" | "done" | "blocked";
  owner_name: string | null;
}

export interface DocumentRow {
  id: string;
  project_id: string;
  run_id: string;
  kind: string;
  engine_version: string;
  inputs_sha256: string;
  file_sha256: string;
  created_at: string;
}

export interface DashAgg {
  projects: number;
  projects_modelled: number;
  pipeline_capex_usd: number;
  planned_connections: number;
  viability_gap_usd: number;
  status_counts: Record<string, number>;
  stage_counts: Record<string, number>;
  country_counts: Record<string, number>;
}

export interface Dashboard {
  real: DashAgg;
  demo: DashAgg;
  milestones: { project: string; title: string; due_date: string | null; status: string; due_soon: boolean }[];
  alerts: { level: "info" | "warning" | "critical"; project: string; text: string }[];
  note: string;
}

export interface DatasetMeta {
  id: string;
  title: string;
  layer_type: string;
  source_institution: string;
  publication_date: string;
  geographic_coverage: string;
  resolution: string;
  licence: string;
  quality: string;
  limitations: string;
  feature_count: number;
  is_demo: boolean;
  retrieval_date: string;
  scope: "platform" | "organisation";
  source_key?: string | null;
  source_url?: string | null;
  source_version?: string | null;
  attribution?: string | null;
}

export interface GeoJSONFeatureCollection {
  type: "FeatureCollection";
  features: { type: "Feature"; geometry: { type: string; coordinates: unknown }; properties: Record<string, unknown> | null }[];
}

export interface DatasetDetail extends DatasetMeta {
  geojson: GeoJSONFeatureCollection;
}

export interface SensitivityRow {
  group: string;
  case: string;
  checks_passed: boolean;
  project_irr_post_subsidy: number | null;
  equity_irr: number | null;
  project_npv_post_subsidy: number | null;
  dscr_min: number | null;
  lcoe_per_kwh_sold: number | null;
  equity_support_total: number | null;
}

export interface TornadoRow {
  group: string;
  low: number | null;
  high: number | null;
  base: number | null;
  swing: number | null;
}

export interface Sensitivity {
  rows: SensitivityRow[];
  tornado_npv: TornadoRow[];
  tornado_equity_irr: TornadoRow[];
  note: string;
}

export interface SubsidyResult {
  feasible: boolean;
  grant: number | null;
  grant_per_connection: number | null;
  dscr_min: number | null;
  equity_irr: number | null;
  reason: string;
  monotone?: boolean;
}

export interface OptimizerOption {
  code: string;
  name: string;
  feasible: boolean;
  gates_failed: string[];
  capex: number | null;
  lcoe: number | null;
  cost_per_connection: number | null;
  service_tier: number | null;
  months_to_electrify: number | null;
  subsidy_per_connection: number | null;
  bill_to_income: number | null;
  co2_t_pa: number | null;
  score: number | null;
  pareto_efficient: boolean;
  connections: number | null;
  unserved_share: number | null;
}

export interface CompareResult {
  settlement: string;
  options: OptimizerOption[];
  least_cost: string | null;
  recommended: string | null;
  explanation: string;
  method_note: string;
}

export type Json = string | number | boolean | null | Json[] | { [k: string]: Json };

// ProjectInputs is edited as a loosely typed tree; the backend validates it (422 on error).
export type ProjectInputs = { [k: string]: Json };

export interface AuditRow {
  at: string;
  action: string;
  entity: string;
  entity_id: string | null;
  user_id: string | null;
  detail: unknown;
}

export interface Member {
  user_id: string;
  email: string;
  full_name: string;
  role: Role;
  mfa_enabled: boolean;
}

export interface AdminOrg {
  id: string;
  name: string;
  kind: string;
  accreditation_status: string;
  plan: string | null;
  is_demo: boolean;
  created_at: string;
}

// Phase 2: Electrification Acceleration Score and portfolios
export type GateState = "met" | "not_met" | "unknown";
export type Decision = "eligible" | "review_required" | "excluded";
export const USER_GATES = ["land_rights", "permits", "technical_feasibility", "environmental_social", "regulatory"] as const;
export type UserGate = (typeof USER_GATES)[number];
export const CRITERIA = ["access_impact", "financial_efficiency", "readiness", "speed", "productive_use", "equity"] as const;
export type Criterion = (typeof CRITERIA)[number];
export type ScoreWeights = Record<Criterion, number>;
export const DEFAULT_WEIGHTS: ScoreWeights = {
  access_impact: 0.2,
  financial_efficiency: 0.2,
  readiness: 0.15,
  speed: 0.15,
  productive_use: 0.15,
  equity: 0.15,
};

export interface ScorePart {
  criterion: Criterion | string;
  label: string;
  weight: number;
  raw: Json;
  normalised: number | null;
  points: number | null;
  explanation: string;
}

export interface GateRow {
  gate: string;
  label: string;
  state: GateState;
}

export interface ScoreCore {
  project_id: string;
  project_name: string;
  score: number;
  score_is_partial: boolean;
  missing_criteria: string[];
  parts: ScorePart[];
  gates: GateRow[];
  decision: Decision;
  decision_explanation: string;
  note: string;
  sources: Record<string, string>;
  is_demo: boolean;
}

export interface ScoreResult extends ScoreCore {
  readiness_categories?: string[];
}

export interface PortfolioSummary {
  id: string;
  name: string;
  description: string;
  projects: number;
  created_at: string;
}

export interface RankingRow extends ScoreCore {
  rank: number | null;
  country: string;
  stage: string;
  run_status: RunStatus | null;
  capex_usd: number | null;
  connections: number | null;
  viability_gap_usd: number | null;
  subsidy_usd: number | null;
}

export interface PortfolioTotals {
  projects: number;
  modelled: number;
  capex_usd: number;
  connections: number;
  viability_gap_usd: number;
  subsidy_usd: number;
  eligible: number;
  review_required: number;
  excluded: number;
}

export interface PortfolioAnalysis {
  portfolio: { id: string; name: string; description: string };
  ranking: RankingRow[];
  totals_real: PortfolioTotals;
  totals_demo: PortfolioTotals;
  weights: ScoreWeights;
  scales: Record<string, number>;
  note: string;
}
