/**
 * Mode d'optimisation économique du mix solaire-batterie — EXTENSION.
 *
 * Réservé par l'architecture (schéma : `simulation_method`). La contrainte de
 * couverture est remplacée par la minimisation du coût actualisé de l'énergie
 * sur la durée de vie, la fiabilité devenant une contrainte souple valorisée
 * par le coût des coupures :
 *
 *     min  LCOE(P_pv, E_batt) + valeur_coupures(deficit_residuel)
 *
 * La fonction de simulation horaire `simulate` demeure IDENTIQUE ; seule la
 * boucle de recherche change. Ce module balaie l'espace (P_pv, E_batt) et
 * renvoie un résultat compatible avec `SizingResult`, de sorte que le module
 * de pré-faisabilité et le schéma restent inchangés (simulation_method passe
 * simplement à `optimisation_economique`).
 */

import { simulate, type BatteryParams, type SimulationResult } from "./energy-balance";
import { capitalRecoveryFactor } from "./sizing";
import type { SizingResult } from "./sizing";
import { technoEconomicDefaults } from "../config";

export interface EconomicOptimizationInput {
  load: readonly number[];
  yieldPerKwp: readonly number[];
  battery: BatteryParams;
  /** Coût d'une heure de coupure (devise/h) — valorise le déficit résiduel. */
  outageCostPerKwh: number;
  /** Nombre de pas de balayage par dimension (résolution de la grille). */
  gridSteps?: number;
}

/**
 * Balaye (P_pv, E_batt) et minimise le coût total annualisé, défaillances
 * comprises. Implémentation volontairement simple (grille) : elle prouve
 * l'extensibilité sans introduire de dépendance d'optimisation lourde.
 */
export function optimizeEconomicMix(input: EconomicOptimizationInput): SizingResult {
  const { load, yieldPerKwp, battery, outageCostPerKwh } = input;
  const steps = input.gridSteps ?? 12;
  const t = technoEconomicDefaults;
  const crf = capitalRecoveryFactor(t.discountRate, t.projectLifetimeYears);

  const annualNeed = load.reduce((a, b) => a + b, 0);
  const unitYield = yieldPerKwp.reduce((a, b) => a + b, 0);
  const meanLoad = annualNeed / Math.max(1, load.length);

  const pvMax = unitYield > 0 ? (2.5 * annualNeed) / unitYield : 0;
  const battMax = 48 * meanLoad;

  let bestCost = Infinity;
  let best: { pv: number; e: number; sim: SimulationResult } | null = null;

  for (let i = 1; i <= steps; i++) {
    const pv = (pvMax * i) / steps;
    for (let j = 0; j <= steps; j++) {
      const e = (battMax * j) / steps;
      const sim = simulate(pv, e, load, yieldPerKwp, battery);

      const pvCapex = pv * t.pvCapexPerKwp;
      const battCapex = e * t.batteryCapexPerKwh;
      const backupCapex = sim.peakResidualDeficitKw * t.backupCapexPerKw;
      const capex = pvCapex + battCapex + backupCapex;
      const annualized = capex * crf + capex * t.opexRateOfCapex;
      const outageValue = sim.residualDeficitKwh * outageCostPerKwh;
      const total = annualized + outageValue;

      if (total < bestCost) {
        bestCost = total;
        best = { pv, e, sim };
      }
    }
  }

  const b = best!;
  const backupSizeKw = b.sim.peakResidualDeficitKw;
  const capex =
    b.e * t.batteryCapexPerKwh + backupSizeKw * t.backupCapexPerKw;
  return {
    pvSizeKwp: b.pv,
    batterySizeKwh: b.e,
    backupSizeKw,
    annualYieldKwh: b.pv * unitYield,
    coverageRate: b.sim.coverageRate,
    residualDeficitKwh: b.sim.residualDeficitKwh,
    reliabilityCost: capex * crf + capex * t.opexRateOfCapex,
    targetReached: true,
    simulation: b.sim,
  };
}
