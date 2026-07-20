/**
 * Score de bancabilité — intègre explicitement une dimension de RÉSILIENCE
 * (sécurité d'approvisionnement), objectif stratégique d'ATEN au même titre
 * que la décarbonisation.
 *
 * Quatre composantes normalisées [0,1], agrégées en un score pondéré, puis
 * converties en notation synthétique A/B/C/D.
 */

export type LoadCriticality = "faible" | "moyenne" | "elevee" | "critique";
export type Rating = "A" | "B" | "C" | "D";

export interface BankabilityWeights {
  financial: number;
  technical: number;
  resilience: number;
  decarbonization: number;
}

export const bankabilityWeightsDefault: BankabilityWeights = {
  financial: 0.35,
  technical: 0.25,
  resilience: 0.25,
  decarbonization: 0.15,
};

export interface BankabilityInput {
  /** TRI du projet (ex. 0.14). Null si non rentable. */
  irr: number | null;
  /** Délai de retour (années). Null si jamais atteint. */
  paybackYears: number | null;
  /** Taux de couverture atteint ∈ [0,1]. */
  coverageRate: number;
  /** Cible de fiabilité atteinte dans les bornes ? */
  targetReached: boolean;
  /** Criticité de la charge du site. */
  loadCriticality: LoadCriticality;
  /** Heures d'indisponibilité réseau subies par an (exposition). */
  gridOutageHoursYear?: number | null;
  /** tCO₂ évitées par an. */
  annualCo2AvoidedTonnes: number;
  /** Facteur d'émission réseau du pays (tCO₂/MWh) — intensité carbone évitée. */
  emissionFactorTco2PerMwh: number;
  weights?: BankabilityWeights;
}

export interface BankabilityResult {
  financialScore: number;
  technicalScore: number;
  resilienceScore: number;
  decarbonizationScore: number;
  totalScore: number;
  rating: Rating;
}

const clamp01 = (x: number) => Math.max(0, Math.min(1, x));

const CRITICALITY_WEIGHT: Record<LoadCriticality, number> = {
  faible: 0.4,
  moyenne: 0.6,
  elevee: 0.8,
  critique: 1.0,
};

/** Financier : TRI (référence 20 %) et payback (référence 7 ans), à parts égales. */
export function financialScore(irr: number | null, paybackYears: number | null): number {
  const irrScore = irr === null ? 0 : clamp01(irr / 0.2);
  const paybackScore = paybackYears === null ? 0 : clamp01(1 - (paybackYears - 3) / 12);
  return clamp01(0.6 * irrScore + 0.4 * paybackScore);
}

/** Technique : couverture atteinte, bonifiée si la cible est tenue. */
export function technicalScore(coverageRate: number, targetReached: boolean): number {
  return clamp01(coverageRate * (targetReached ? 1 : 0.85));
}

/**
 * Résilience : sécurité d'approvisionnement. Combine la part de charge servie
 * en renouvelable et la criticité de la charge (plus la charge est critique,
 * plus la valeur de la résilience est élevée), avec un bonus lié à la
 * réduction de l'exposition aux coupures réseau.
 */
export function resilienceScore(
  coverageRate: number,
  loadCriticality: LoadCriticality,
  gridOutageHoursYear?: number | null,
): number {
  const criticality = CRITICALITY_WEIGHT[loadCriticality];
  // Exposition réseau normalisée : 0 h → 0, ≥ 500 h/an → 1 (fort besoin).
  const exposure = clamp01((gridOutageHoursYear ?? 0) / 500);
  const base = coverageRate * criticality;
  return clamp01(0.7 * base + 0.3 * (coverageRate * exposure) + 0.15 * criticality * coverageRate);
}

/** Climat : intensité de la décarbonisation (couverture × intensité réseau). */
export function decarbonizationScore(
  coverageRate: number,
  emissionFactorTco2PerMwh: number,
): number {
  // Réseau très carboné (≥ 0.8 tCO₂/MWh) → intensité 1 ; réseau propre → faible.
  const intensity = clamp01(emissionFactorTco2PerMwh / 0.8);
  return clamp01(coverageRate * (0.5 + 0.5 * intensity));
}

export function ratingFromScore(total: number): Rating {
  if (total >= 0.8) return "A";
  if (total >= 0.65) return "B";
  if (total >= 0.5) return "C";
  return "D";
}

export function computeBankability(input: BankabilityInput): BankabilityResult {
  const w = input.weights ?? bankabilityWeightsDefault;
  const financial = financialScore(input.irr, input.paybackYears);
  const technical = technicalScore(input.coverageRate, input.targetReached);
  const resilience = resilienceScore(
    input.coverageRate,
    input.loadCriticality,
    input.gridOutageHoursYear,
  );
  const decarbonization = decarbonizationScore(
    input.coverageRate,
    input.emissionFactorTco2PerMwh,
  );

  const total = clamp01(
    w.financial * financial +
      w.technical * technical +
      w.resilience * resilience +
      w.decarbonization * decarbonization,
  );

  return {
    financialScore: financial,
    technicalScore: technical,
    resilienceScore: resilience,
    decarbonizationScore: decarbonization,
    totalScore: total,
    rating: ratingFromScore(total),
  };
}
