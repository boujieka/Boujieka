/**
 * Configuration centrale d'ATEN.
 *
 * Conformément aux notes pour Claude Code, les paramètres physiques de la
 * simulation et les poids du matching sont exposés ici comme configuration —
 * jamais codés en dur dans les algorithmes. Ils peuvent être surchargés par
 * variables d'environnement (paramètres physiques) et, à terme, par
 * l'opérateur de la plateforme (poids de matching).
 */

const num = (v: string | undefined, fallback: number): number => {
  const n = v === undefined ? NaN : Number(v);
  return Number.isFinite(n) ? n : fallback;
};

/** Nombre de pas horaires d'une année type. */
export const HOURS_PER_YEAR = 8760;

/** Paramètres physiques par défaut de la simulation énergétique. */
export interface PhysicalParams {
  /** Ratio de performance PV (pertes onduleur, température, câblage, salissure). */
  performanceRatio: number;
  /** Rendement aller-retour de la batterie (η_rt). */
  batteryRoundTrip: number;
  /** Profondeur de décharge admissible (DoD). */
  batteryDod: number;
  /** Limite de puissance de charge/décharge (fraction de la capacité par heure). */
  batteryCRate: number;
}

export const physicalDefaults: PhysicalParams = {
  performanceRatio: num(process.env.ATEN_PERFORMANCE_RATIO, 0.8),
  batteryRoundTrip: num(process.env.ATEN_BATTERY_ROUND_TRIP, 0.9),
  batteryDod: num(process.env.ATEN_BATTERY_DOD, 0.9),
  batteryCRate: num(process.env.ATEN_BATTERY_C_RATE, 0.5),
};

/** Bornes et pas de la boucle de dimensionnement à cible fixée. */
export const sizingBounds = {
  /** Facteur de surdimensionnement PV maximal. */
  kMax: 3.0,
  /** Incrément du facteur PV lorsque la cible reste hors d'atteinte. */
  kStep: 0.1,
  /** Capacité batterie maximale explorée, exprimée en heures de charge moyenne. */
  battMaxHoursOfMeanLoad: 72,
  /** Tolérance de la dichotomie sur la capacité batterie (kWh). */
  battToleranceKwh: 1,
};

/**
 * Poids par défaut du score de compatibilité du matching.
 * Leur somme vaut 1. L'opérateur peut les ajuster selon la stratégie.
 */
export interface MatchingWeights {
  geography: number;
  technology: number;
  size: number;
  bankability: number;
}

export const matchingWeightsDefault: MatchingWeights = {
  geography: 0.3,
  technology: 0.3,
  size: 0.2,
  bankability: 0.2,
};

/** Hypothèses technico-économiques par défaut (surchargeables par étude). */
export const technoEconomicDefaults = {
  /** CAPEX solaire par kWc installé (USD). */
  pvCapexPerKwp: 850,
  /** CAPEX stockage par kWh (USD). */
  batteryCapexPerKwh: 350,
  /** CAPEX groupe d'appoint par kW (USD). */
  backupCapexPerKw: 400,
  /** OPEX annuel en pourcentage du CAPEX. */
  opexRateOfCapex: 0.02,
  /** Durée de vie économique du projet (années). */
  projectLifetimeYears: 20,
  /** Taux d'actualisation pour le TRI / LCOE. */
  discountRate: 0.09,
  /** Facteur de dégradation annuelle du productible PV. */
  pvDegradationRate: 0.005,
  /** Marge PPA appliquée sous le tarif réseau actuel (ex. 0.85 = -15 %). */
  ppaDiscountToGrid: 0.85,
};

/** Durée de vie utilisée pour le cumul carbone (années). */
export const decarbonizationLifetimeYears = 20;

/** Modèles Claude par tâche (côté serveur uniquement). */
export const aiModels = {
  qualification: process.env.ANTHROPIC_MODEL_QUALIFICATION || "claude-opus-4-8",
  conceptNote: process.env.ANTHROPIC_MODEL_CONCEPT_NOTE || "claude-opus-4-8",
  matching: process.env.ANTHROPIC_MODEL_MATCHING || "claude-haiku-4-5-20251001",
};
