/**
 * Dimensionnement du mix solaire-batterie-appoint à fiabilité cible fixée.
 *
 * Traduction du pseudo-code de référence (Logique algorithmique §2.3).
 * PV fixée par un facteur de surdimensionnement k appliqué à l'équilibre
 * énergétique annuel ; capacité batterie ajustée par dichotomie jusqu'à
 * atteindre la couverture cible ; k incrémenté si la cible reste hors
 * d'atteinte. Approche imbriquée, convergente et interprétable.
 *
 * L'architecture réserve l'extension vers l'optimisation économique : la
 * fonction `simulate` reste identique, seule la boucle de recherche change
 * (voir `simulation_method` dans le schéma et `optimizeEconomic` à venir).
 */

import { simulate, type BatteryParams, type SimulationResult } from "./energy-balance";
import { sizingBounds, technoEconomicDefaults } from "../config";

export interface SizingInput {
  /** Vecteur de charge horaire L[h] (kW ≡ kWh sur le pas). */
  load: readonly number[];
  /** Vecteur de productible y[h] (kWh par kWc et par pas). */
  yieldPerKwp: readonly number[];
  /** Taux de couverture cible R* imposé par l'utilisateur (ex. 0.95). */
  targetReliabilityRate: number;
  /** Paramètres physiques de la batterie. */
  battery: BatteryParams;
}

export interface SizingResult {
  pvSizeKwp: number;
  batterySizeKwh: number;
  /** Puissance d'appoint dimensionnée sur la pointe de déficit résiduel (kW). */
  backupSizeKw: number;
  /** Productible annuel du champ dimensionné (kWh/an). */
  annualYieldKwh: number;
  coverageRate: number;
  residualDeficitKwh: number;
  /** Coût annualisé de la fiabilité (stockage + appoint + OPEX associés). */
  reliabilityCost: number;
  /** Cible atteinte dans les bornes de recherche ? */
  targetReached: boolean;
  simulation: SimulationResult;
}

/** Facteur de recouvrement du capital (annuité) — CRF(taux, durée). */
export function capitalRecoveryFactor(rate: number, years: number): number {
  if (rate <= 0) return 1 / years;
  const f = Math.pow(1 + rate, years);
  return (rate * f) / (f - 1);
}

/**
 * Coût annualisé de la fiabilité : surcoût du stockage et de l'appoint
 * mobilisés pour atteindre la cible, incluant les OPEX associés.
 * cout_fiabilite = CAPEX_batterie_annualisé + CAPEX_appoint_annualisé + OPEX
 */
export function reliabilityCost(batterySizeKwh: number, backupSizeKw: number): number {
  const t = technoEconomicDefaults;
  const crf = capitalRecoveryFactor(t.discountRate, t.projectLifetimeYears);
  const batteryCapex = batterySizeKwh * t.batteryCapexPerKwh;
  const backupCapex = backupSizeKw * t.backupCapexPerKw;
  const annualizedCapex = (batteryCapex + backupCapex) * crf;
  const opex = (batteryCapex + backupCapex) * t.opexRateOfCapex;
  return annualizedCapex + opex;
}

/**
 * Dimensionne le mix pour atteindre `targetReliabilityRate`.
 * Fonction pure : ne dépend que de ses arguments et des bornes de config.
 */
export function sizeToTargetReliability(input: SizingInput): SizingResult {
  const { load, yieldPerKwp, targetReliabilityRate, battery } = input;

  const annualNeed = load.reduce((a, b) => a + b, 0);
  const unitYield = yieldPerKwp.reduce((a, b) => a + b, 0); // kWh par kWc et par an
  const meanLoad = annualNeed / Math.max(1, load.length);
  const eBattMax = sizingBounds.battMaxHoursOfMeanLoad * meanLoad;

  let best: { pv: number; e: number; sim: SimulationResult } | null = null;

  for (let k = 1.0; k <= sizingBounds.kMax + 1e-9; k += sizingBounds.kStep) {
    const pvSize = unitYield > 0 ? (k * annualNeed) / unitYield : 0;

    // Dichotomie sur la capacité batterie.
    let low = 0;
    let high = eBattMax;
    while (high - low > sizingBounds.battToleranceKwh) {
      const mid = (low + high) / 2;
      const { coverageRate } = simulate(pvSize, mid, load, yieldPerKwp, battery);
      if (coverageRate >= targetReliabilityRate) high = mid;
      else low = mid;
    }

    const sim = simulate(pvSize, high, load, yieldPerKwp, battery);
    best = { pv: pvSize, e: high, sim };

    if (sim.coverageRate >= targetReliabilityRate) {
      return finalize(pvSize, high, sim, unitYield, true);
    }
  }

  // Cible inatteignable dans les bornes : meilleur effort.
  const b = best!;
  return finalize(b.pv, b.e, b.sim, unitYield, false);
}

function finalize(
  pvSizeKwp: number,
  batterySizeKwh: number,
  sim: SimulationResult,
  unitYield: number,
  targetReached: boolean,
): SizingResult {
  const backupSizeKw = sim.peakResidualDeficitKw;
  return {
    pvSizeKwp,
    batterySizeKwh,
    backupSizeKw,
    annualYieldKwh: pvSizeKwp * unitYield,
    coverageRate: sim.coverageRate,
    residualDeficitKwh: sim.residualDeficitKwh,
    reliabilityCost: reliabilityCost(batterySizeKwh, backupSizeKw),
    targetReached,
    simulation: sim,
  };
}
