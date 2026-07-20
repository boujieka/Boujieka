/**
 * Simulation horaire du bilan énergétique — fonction PURE.
 *
 * Traduction directe du pseudo-code de référence (Logique algorithmique §2.2).
 * Prend les vecteurs de charge et de productible et renvoie couverture et
 * déficit, afin d'être réutilisable par les DEUX régimes de dimensionnement
 * (cible fixée aujourd'hui, optimisation économique demain).
 *
 * Aucune dépendance à la base ni à la configuration : tous les paramètres
 * physiques sont passés en argument.
 */

export interface BatteryParams {
  /** Rendement aller-retour (η_rt), ex. 0.90. */
  roundTrip: number;
  /** Profondeur de décharge admissible (DoD), ex. 0.90. */
  dod: number;
  /** Limite de puissance de charge/décharge (fraction de la capacité/h), ex. 0.50. */
  cRate: number;
}

export interface SimulationResult {
  /** Taux de couverture atteint ∈ [0, 1] (servi renouvelable / charge totale). */
  coverageRate: number;
  /** Énergie de charge servie par le renouvelable (kWh/an). */
  servedRenewableKwh: number;
  /** Charge totale annuelle (kWh). */
  totalLoadKwh: number;
  /** Déficit résiduel annuel non servi par le renouvelable (kWh). */
  residualDeficitKwh: number;
  /** Pointe horaire de déficit résiduel → dimensionne l'appoint (kW). */
  peakResidualDeficitKw: number;
  /** Surplus solaire écrêté faute de capacité/puissance batterie (kWh/an). */
  curtailedKwh: number;
  /** Productible solaire total mobilisé pour cette puissance PV (kWh/an). */
  pvGenerationKwh: number;
}

/**
 * Simule le bilan énergétique horaire pour un couple (P_pv, E_batt) donné.
 *
 * @param pvSizeKwp     Puissance solaire installée (kWc).
 * @param batterySizeKwh Capacité batterie nominale (kWh).
 * @param load          Vecteur de charge horaire L[h] (kW ≡ kWh sur le pas).
 * @param yieldPerKwp   Vecteur de productible y[h] (kWh par kWc et par pas).
 * @param params        Paramètres physiques de la batterie.
 */
export function simulate(
  pvSizeKwp: number,
  batterySizeKwh: number,
  load: readonly number[],
  yieldPerKwp: readonly number[],
  params: BatteryParams,
): SimulationResult {
  const n = Math.min(load.length, yieldPerKwp.length);
  const usableCapacity = batterySizeKwh * params.dod; // capacité utile
  const pMax = batterySizeKwh * params.cRate; // puissance charge/décharge max
  let soc = usableCapacity; // batterie pleine au départ

  let servedRenewable = 0;
  let totalLoad = 0;
  let curtailed = 0;
  let pvGeneration = 0;
  let peakResidualDeficit = 0;

  for (let h = 0; h < n; h++) {
    const L = load[h];
    totalLoad += L;
    const S = pvSizeKwp * yieldPerKwp[h];
    pvGeneration += S;
    const net = S - L;

    if (net >= 0) {
      // Surplus solaire : la charge est servie directement, le reste recharge.
      servedRenewable += L;
      const room = usableCapacity - soc;
      const charge = Math.min(net * params.roundTrip, room, pMax);
      soc += charge;
      // Excédent au-delà de la capacité/puissance : écrêté.
      curtailed += net - charge / params.roundTrip;
    } else {
      // Déficit : le solaire couvre S, la batterie prend le relais.
      servedRenewable += S;
      const deficit = -net;
      const available = Math.min(soc, pMax) * params.roundTrip;
      const supplied = Math.min(deficit, available);
      soc -= supplied / params.roundTrip;
      servedRenewable += supplied;
      const unmet = deficit - supplied; // reporté sur appoint / réseau
      if (unmet > peakResidualDeficit) peakResidualDeficit = unmet;
    }
  }

  const coverageRate = totalLoad > 0 ? servedRenewable / totalLoad : 0;

  return {
    coverageRate,
    servedRenewableKwh: servedRenewable,
    totalLoadKwh: totalLoad,
    residualDeficitKwh: totalLoad - servedRenewable,
    peakResidualDeficitKw: peakResidualDeficit,
    curtailedKwh: curtailed,
    pvGenerationKwh: pvGeneration,
  };
}
