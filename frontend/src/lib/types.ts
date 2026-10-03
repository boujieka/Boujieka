// Mirrors backend/app/schemas.py. Decimal values arrive as strings to preserve precision.

export type Dec = string;
export type DataNature = "FACT" | "CALCULATION" | "ESTIMATE" | "AI_INTERPRETATION" | "SYNTHETIC";
export type FieldStatus = "not_disclosed" | "not_available" | "pending";
export type AuctionStatus = "announced" | "completed" | "cancelled" | "postponed";
export type InstrumentType =
  | "treasury_bill"
  | "treasury_bond"
  | "eurobond"
  | "infrastructure_bond"
  | "sukuk"
  | "regional_bond"
  | "other";

export interface SourceRef {
  source_id: number;
  name: string;
  institution: string;
  category: string;
  is_synthetic: boolean;
}

export interface Provenance {
  data_nature: DataNature;
  verification_status: string;
  confidence_score: Dec | null;
  is_synthetic: boolean;
  source: SourceRef | null;
  source_url: string | null;
  source_document_id: number | null;
  publication_date: string | null;
  extracted_at: string | null;
  notes: string | null;
}

export interface SourceCandidate {
  url: string;
  purpose: string;
  check: "http_200" | "http_403" | "search_only";
  evidence: string;
}

export interface SourceOut {
  source_id: number;
  name: string;
  institution: string;
  category: string;
  priority: number;
  country_id: number | null;
  base_url: string | null;
  status: string;
  last_checked_at: string | null;
  last_success_at: string | null;
  last_error: string | null;
  notes: string | null;
  is_synthetic: boolean;
  candidates: SourceCandidate[];
}

export interface Country {
  country_id: number;
  name: string;
  iso2: string;
  iso3: string;
  currency: string;
  monetary_zone: string;
  central_bank: string | null;
  debt_management_office: string | null;
  primary_market_structure: string | null;
  secondary_market_structure: string | null;
  tax_notes: string | null;
  capital_controls: string | null;
  market_access_notes: string | null;
  last_verified: string | null;
  field_status: Record<string, FieldStatus>;
  provenance: Provenance;
}

export interface CountryDetail extends Country {
  upcoming_auction_count: number;
  completed_auction_count: number;
  security_count: number;
  sources: SourceOut[];
}

export interface SecuritySummary {
  security_id: number;
  security_name: string;
  instrument_type: InstrumentType;
  tenor_days: number | null;
  maturity_date: string | null;
  currency: string;
  country_iso3: string;
  country_name: string;
  is_synthetic: boolean;
}

export interface Security extends SecuritySummary {
  isin: string | null;
  local_code: string | null;
  face_value: Dec | null;
  coupon_rate: Dec | null;
  coupon_frequency: string | null;
  issue_date: string | null;
  amortization: string | null;
  indexation: string | null;
  green_social_sustainability_flag: string | null;
  listing_status: string | null;
  minimum_denomination: Dec | null;
  field_status: Record<string, FieldStatus>;
  provenance: Provenance;
}

export interface SecurityDetail extends Security {
  auctions: Auction[];
}

export interface AuctionOfficial {
  amount_offered: Dec | null;
  amount_submitted: Dec | null;
  amount_allocated: Dec | null;
  minimum_bid: Dec | null;
  maximum_bid: Dec | null;
  cutoff_yield: Dec | null;
  weighted_average_yield: Dec | null;
  average_price: Dec | null;
  reported_bid_to_cover: Dec | null;
  number_of_bidders: number | null;
  number_of_successful_bidders: number | null;
  yield_convention: string | null;
}

export interface AuctionCalculated {
  data_nature: DataNature;
  bid_to_cover: Dec | null;
  bid_to_cover_definition: string;
  allocation_rate: Dec | null;
  allocation_rate_definition: string;
  acceptance_rate: Dec | null;
  acceptance_rate_definition: string;
}

export interface Auction {
  auction_id: number;
  status: AuctionStatus;
  auction_type: string;
  announcement_date: string | null;
  auction_date: string;
  settlement_date: string | null;
  security: SecuritySummary;
  official: AuctionOfficial;
  calculated: AuctionCalculated;
  field_status: Record<string, FieldStatus>;
  provenance: Provenance;
}

export interface HistoricalComparison {
  data_nature: DataNature;
  peer_definition: string;
  previous_auction_id: number | null;
  yield_change_bps: Dec | null;
  yield_change_definition: string;
  peer_average_bid_to_cover: Dec | null;
  peer_count: number;
  caveat: string | null;
}

export interface AuctionDetail extends Auction {
  comparison: HistoricalComparison;
  peers: Auction[];
}

export interface Page<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

export interface YieldCurvePoint {
  tenor_days: number;
  instrument_type: InstrumentType;
  weighted_average_yield: Dec;
  auction_id: number;
  auction_date: string;
  yield_convention: string | null;
  is_synthetic: boolean;
}

export interface YieldCurve {
  country_iso3: string;
  as_of: string;
  lookback_days: number;
  method: string;
  caveat: string;
  points: YieldCurvePoint[];
}

export interface DashboardSummary {
  as_of: string;
  countries_monitored: number;
  upcoming_auctions_7d: number;
  upcoming_auctions_30d: number;
  results_last_7d: number;
  announced_issuance_by_currency: { currency: string; amount: Dec }[];
  cancelled_or_postponed: number;
  sources_pending_configuration: number;
  synthetic_records_present: boolean;
  new_opportunities: number;
  alerts: number | null;
}

export interface MissingFieldStat {
  field: string;
  missing: number;
  not_disclosed: number;
  pending: number;
  total: number;
}

export interface DataQualityReport {
  as_of: string;
  sources_total: number;
  sources_pending_configuration: SourceOut[];
  sources_stale: SourceOut[];
  sources_failing: SourceOut[];
  auction_missing_fields: MissingFieldStat[];
  low_confidence_records: number;
  unverified_records: number;
  synthetic_auctions: number;
  synthetic_securities: number;
  duplicate_candidates: number;
  duplicate_definition: string;
}

export interface PassportFact {
  label: string;
  value: string | null;
  unit?: string;
  auction_id?: number;
  auction_date?: string;
  field?: string;
  data_nature: DataNature | string;
  source?: string | null;
  source_url?: string | null;
  security_ids?: number[];
}

export interface Passport {
  facts: PassportFact[];
  calculation: { formula: string; inputs?: Record<string, unknown>; result: string | number; unit?: string } | null;
  rule: { description: string; threshold?: string | number };
  invalidated_if: string;
  caveats: string[];
  rules_version?: string;
  as_of?: string;
}

export interface Opportunity {
  opportunity_id: number;
  opportunity_type: string;
  label: string;
  country_iso3: string;
  country_name: string;
  currency: string | null;
  security: SecuritySummary | null;
  auction_id: number | null;
  auction_date: string | null;
  yield_pct: Dec | null;
  maturity: string | null;
  strength: Dec | null;
  strength_definition: string;
  explanation: string | null;
  evidence: Passport;
  risk_flags: string[];
  data_confidence: Dec | null;
  is_synthetic: boolean;
  as_of: string;
  is_active: boolean;
  matches_criteria: boolean | null;
  criteria_unmet: string[];
}

export interface OpportunityPage {
  items: Opportunity[];
  total: number;
  by_type: Record<string, number>;
  by_country: Record<string, number>;
  criteria: Record<string, string>;
  disclaimer: string;
}

export interface HeatCell {
  bucket: string;
  tenor_days: number;
  instrument_type: InstrumentType;
  auction_id: number;
  auction_date: string;
  weighted_average_yield: Dec | null;
  bid_to_cover: Dec | null;
  demand_z: Dec | null;
  demand_peer_count: number;
  yield_change_bps: Dec | null;
  is_synthetic: boolean;
}

export interface HeatGrid {
  as_of: string;
  buckets: string[];
  rows: { country_iso3: string; country_name: string; currency: string; active_opportunities: number; cells: HeatCell[] }[];
  method: string;
  caveat: string;
}

export interface MaturityWall {
  country_iso3: string;
  currency: string;
  as_of: string;
  total: Dec;
  months: { month: string; amount: Dec; securities: number; share_pct: Dec | null }[];
  data_nature: DataNature;
  caveat: string;
}
