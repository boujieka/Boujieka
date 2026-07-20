/**
 * Score de compatibilité du matching — fonction PURE.
 *
 * Traduction du pseudo-code de référence (Logique algorithmique §3).
 * Quatre dimensions agrégées en un score pondéré ∈ [0, 1]. Deux filtres
 * DURS s'appliquent AVANT tout calcul pondéré :
 *   1. absence de couverture géographique → compatibilité nulle ;
 *   2. hybride requis mais stockage absent chez le développeur → nulle.
 */

import { matchingWeightsDefault, type MatchingWeights } from "../config";

export type Technology = "solaire" | "stockage" | "hybride" | "groupe_backup";
export type Rating = "A" | "B" | "C" | "D";
export type FinancingCapacity = "equity" | "dette" | "mixte" | "aucune";

export interface OpportunityForMatch {
  country: string;
  region?: string | null;
  /** Puissance du projet (kWc dimensionnés en pré-faisabilité). */
  projectSizeKw: number;
  /** Capacités technologiques requises par la solution dimensionnée. */
  requiredTechnologies: Technology[];
  /** Notation de bancabilité (A/B/C/D). Optionnelle si non encore calculée. */
  rating?: Rating | null;
}

export interface DeveloperForMatch {
  zones: { country: string; region?: string | null }[];
  technologies: Technology[];
  minProjectSizeKw: number;
  maxProjectSizeKw: number;
  financingCapacity: FinancingCapacity;
}

export interface CompatibilityResult {
  geographyScore: number;
  technologyScore: number;
  sizeScore: number;
  bankabilityAlignment: number;
  compatibilityScore: number;
  /** True si un filtre dur a annulé la compatibilité. */
  hardFiltered: boolean;
  hardFilterReason?: "geographie" | "technologie";
}

const RATING_NUM: Record<Rating, number> = { A: 1.0, B: 0.75, C: 0.5, D: 0.25 };
const FINANCING_TOLERANCE: Record<FinancingCapacity, number> = {
  equity: 0.2,
  mixte: 0.15,
  dette: 0.1,
  aucune: 0.0,
};

/** Géographie : pays+région → 1.0 ; pays seul → 0.6 ; sinon 0.0 (filtre dur). */
export function geographyScore(opp: OpportunityForMatch, dev: DeveloperForMatch): number {
  let countryCovered = false;
  for (const z of dev.zones) {
    if (z.country !== opp.country) continue;
    countryCovered = true;
    // Région couverte : zone sans région précise = couverture nationale.
    if (!opp.region || !z.region || z.region === opp.region) return 1.0;
  }
  return countryCovered ? 0.6 : 0.0;
}

/** Taille : 1.0 dans la fourchette, décroissance linéaire de part et d'autre. */
export function sizeScore(opp: OpportunityForMatch, dev: DeveloperForMatch): number {
  const p = opp.projectSizeKw;
  const { minProjectSizeKw: min, maxProjectSizeKw: max } = dev;
  if (p >= min && p <= max) return 1.0;
  if (p < min) return Math.max(0, 1 - (min - p) / min);
  return Math.max(0, 1 - (p - max) / max);
}

/**
 * Technologie : part des capacités requises détenues. L'hybride impose la
 * présence SIMULTANÉE du solaire et du stockage (filtre dur si absent).
 */
export function technologyScore(opp: OpportunityForMatch, dev: DeveloperForMatch): number {
  const required = opp.requiredTechnologies;
  if (required.length === 0) return 1.0;
  const owned = new Set(dev.technologies);

  const hybridRequired = required.includes("hybride");
  if (hybridRequired) {
    const hasHybridCapability =
      owned.has("hybride") || (owned.has("solaire") && owned.has("stockage"));
    if (!hasHybridCapability) return 0.0; // filtre dur
  }

  let held = 0;
  for (const tech of required) {
    if (tech === "hybride") {
      if (owned.has("hybride") || (owned.has("solaire") && owned.has("stockage"))) held++;
    } else if (owned.has(tech)) {
      held++;
    }
  }
  return held / required.length;
}

/** Bancabilité : min(1, note_num + tolérance(capacité de financement)). */
export function bankabilityAlignment(opp: OpportunityForMatch, dev: DeveloperForMatch): number {
  const noteNum = opp.rating ? RATING_NUM[opp.rating] : 0.5; // défaut neutre si non noté
  return Math.min(1.0, noteNum + FINANCING_TOLERANCE[dev.financingCapacity]);
}

/**
 * Compatibilité globale. Applique les filtres durs AVANT la pondération.
 * Un score nul signale une incompatibilité structurelle, non un désavantage.
 */
export function computeCompatibility(
  opp: OpportunityForMatch,
  dev: DeveloperForMatch,
  weights: MatchingWeights = matchingWeightsDefault,
): CompatibilityResult {
  const geo = geographyScore(opp, dev);
  if (geo === 0) {
    return {
      geographyScore: 0,
      technologyScore: 0,
      sizeScore: 0,
      bankabilityAlignment: 0,
      compatibilityScore: 0,
      hardFiltered: true,
      hardFilterReason: "geographie",
    };
  }

  const tech = technologyScore(opp, dev);
  if (tech === 0) {
    return {
      geographyScore: geo,
      technologyScore: 0,
      sizeScore: 0,
      bankabilityAlignment: 0,
      compatibilityScore: 0,
      hardFiltered: true,
      hardFilterReason: "technologie",
    };
  }

  const size = sizeScore(opp, dev);
  const banc = bankabilityAlignment(opp, dev);

  const compatibilityScore =
    weights.geography * geo +
    weights.technology * tech +
    weights.size * size +
    weights.bankability * banc;

  return {
    geographyScore: geo,
    technologyScore: tech,
    sizeScore: size,
    bankabilityAlignment: banc,
    compatibilityScore,
    hardFiltered: false,
  };
}

export interface RankedMatch<D> {
  developer: D;
  result: CompatibilityResult;
}

/**
 * Classe une liste de développeurs pour une opportunité, par score décroissant.
 * Les incompatibilités structurelles (score 0) sont exclues du classement.
 */
export function rankDevelopers<D extends DeveloperForMatch>(
  opp: OpportunityForMatch,
  developers: D[],
  weights: MatchingWeights = matchingWeightsDefault,
): RankedMatch<D>[] {
  return developers
    .map((developer) => ({ developer, result: computeCompatibility(opp, developer, weights) }))
    .filter((m) => !m.result.hardFiltered && m.result.compatibilityScore > 0)
    .sort((a, b) => b.result.compatibilityScore - a.result.compatibilityScore);
}
