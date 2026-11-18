import type { FeatureCollection, Geometry } from "geojson";

export type Nature = "renseigne" | "calcule" | "hypothetique" | "inconnu";

export interface Meta {
  version: string;
  engine_version: string;
  technologies: string[];
  dataset_categories: string[];
  data_natures: string[];
  rule_kinds: string[];
  justification_types: string[];
  land_statuses: string[];
  grid_statuses: string[];
  upload_extensions: string[];
  max_upload_mb: number;
}

export interface Project {
  id: number;
  name: string;
  country_iso3: string;
  technology: string;
  description: string;
  is_fictional: boolean;
  site_count: number;
  dataset_count: number;
  rule_count: number;
  created_at: string | null;
}

export interface DatasetVersion {
  id: number;
  version_no: number;
  sha256: string;
  original_filename: string;
  file_format: string;
  source_crs: string;
  crs_origin: string;
  feature_count: number;
  geometry_types: string[];
  bbox: number[] | null;
  warnings: string[];
  imported_at: string | null;
}

export interface Dataset {
  id: number;
  project_id: number;
  name: string;
  category: string;
  nature: string;
  source_name: string;
  source_url: string;
  licence: string;
  producer: string;
  reference_date: string | null;
  horizontal_accuracy_m: number | null;
  is_synthetic: boolean;
  notes: string;
  latest_version: DatasetVersion | null;
  version_count: number;
}

export interface Site {
  id: number;
  project_id: number;
  name: string;
  geometry: Geometry;
  bbox: [number, number, number, number];
  boundary_source: string;
  boundary_dataset_version_id: number | null;
  boundary_accuracy_m: number | null;
  land_status: string;
  land_evidence_dataset_id: number | null;
  grid_status: string;
  grid_evidence_dataset_id: number | null;
  analysis_count: number;
  warnings?: string[];
}

export interface Rule {
  id: number;
  project_id: number;
  dataset_id: number;
  dataset_name: string | null;
  name: string;
  kind: string;
  buffer_m: number;
  justification_type: string;
  justification: string;
  weight: number | null;
  active: boolean;
}

export interface AreaMetric {
  valeur_m2: number;
  valeur_ha: number;
  unite: string;
  nature: Nature;
  methode: string;
}

export interface ValueMetric {
  valeur: number | null;
  unite: string;
  nature: Nature;
  methode: string;
}

export interface IntervalMetric {
  bas_m2: number | null;
  haut_m2: number | null;
  nature: Nature;
  methode: string;
}

export interface RuleResult {
  regle_id: number;
  nom: string;
  type: string;
  buffer_m: number;
  justification: string;
  entites_retenues: number;
  surface_dans_site_m2: number;
  surface_dans_zone_amenageable_m2?: number;
  surface_dans_surface_nette_m2?: number;
}

export interface AnalysisResults {
  version_moteur: string;
  scr_calcul: string;
  scr_calcul_nom: string;
  niveau_etude: string;
  mention: string;
  indicateurs: Record<string, AreaMetric | ValueMetric | IntervalMetric>;
  par_regle: RuleResult[];
  controles: { nom: string; ok: boolean; detail: string }[];
  avertissements: string[];
  statuts: {
    foncier: string;
    foncier_libelle: string;
    raccordement: string;
    raccordement_libelle: string;
    capacite_reseau: string;
  };
  donnees_fictives: boolean;
}

export interface AnalysisRun {
  id: number;
  site_id: number;
  created_at: string | null;
  input_hash: string;
  software_version: string;
  engine_version: string;
  duration_ms: number;
  results: AnalysisResults;
  layers: { id: number; kind: string; rule_id: number | null; area_m2: number }[];
  reused?: boolean;
}

export interface AnalysisSummary {
  id: number;
  created_at: string | null;
  input_hash: string;
  surface_nette_ha: number;
  recul_m: number;
  regles: number;
  donnees_fictives: boolean;
}

export type GeoJSONFC = FeatureCollection;
