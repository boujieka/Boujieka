/**
 * Modèle technico-économique : CAPEX, tarif PPA, TRI, payback, économies.
 *
 * Point de vue projet : le développeur investit le CAPEX et vend l'énergie
 * renouvelable servie au tarif PPA ; l'offtaker économise l'écart avec le
 * tarif réseau. Le TRI est calculé sur les flux nets sur la durée de vie,
 * dégradation du productible incluse.
 */

import { technoEconomicDefaults } from "../config";

export interface TechnoEconomicInput {
  pvSizeKwp: number;
  batterySizeKwh: number;
  backupSizeKw: number;
  /** Énergie renouvelable servie la 1re année (kWh) — sortie de la simulation. */
  servedRenewableKwh: number;
  /** Tarif réseau actuel du site (devise/kWh). */
  currentGridTariff: number;
  currency?: string;
  /** Surcharges optionnelles des hypothèses par défaut. */
  overrides?: Partial<typeof technoEconomicDefaults>;
}

export interface TechnoEconomicResult {
  capex: number;
  opexAnnual: number;
  ppaTariff: number;
  irr: number | null;
  paybackYears: number | null;
  annualSavings: number;
  currency: string;
}

/** Valeur actuelle nette d'une série de flux au taux donné. */
export function npv(rate: number, cashflows: number[]): number {
  return cashflows.reduce((acc, cf, t) => acc + cf / Math.pow(1 + rate, t), 0);
}

/**
 * TRI par bissection sur [−0.9, 1.5]. Renvoie null si aucun changement de
 * signe (projet jamais rentable) sur l'intervalle.
 */
export function internalRateOfReturn(cashflows: number[]): number | null {
  let lo = -0.9;
  let hi = 1.5;
  let fLo = npv(lo, cashflows);
  let fHi = npv(hi, cashflows);
  if (fLo * fHi > 0) return null;

  for (let i = 0; i < 200; i++) {
    const mid = (lo + hi) / 2;
    const fMid = npv(mid, cashflows);
    if (Math.abs(fMid) < 1e-6) return mid;
    if (fLo * fMid < 0) {
      hi = mid;
      fHi = fMid;
    } else {
      lo = mid;
      fLo = fMid;
    }
  }
  return (lo + hi) / 2;
}

export function computeTechnoEconomic(input: TechnoEconomicInput): TechnoEconomicResult {
  const t = { ...technoEconomicDefaults, ...input.overrides };

  const capex =
    input.pvSizeKwp * t.pvCapexPerKwp +
    input.batterySizeKwh * t.batteryCapexPerKwh +
    input.backupSizeKw * t.backupCapexPerKw;

  const opexAnnual = capex * t.opexRateOfCapex;
  const ppaTariff = input.currentGridTariff * t.ppaDiscountToGrid;

  // Flux nets du projet (développeur) : revenu PPA − OPEX, énergie dégradée.
  const cashflows: number[] = [-capex];
  let cumulative = -capex;
  let paybackYears: number | null = null;
  for (let year = 1; year <= t.projectLifetimeYears; year++) {
    const degradation = Math.pow(1 - t.pvDegradationRate, year - 1);
    const energy = input.servedRenewableKwh * degradation;
    const revenue = energy * ppaTariff;
    const net = revenue - opexAnnual;
    cashflows.push(net);
    if (paybackYears === null) {
      const prev = cumulative;
      cumulative += net;
      if (cumulative >= 0 && net > 0) {
        // Interpolation linéaire dans l'année de bascule.
        paybackYears = year - 1 + -prev / net;
      }
    }
  }

  const irr = internalRateOfReturn(cashflows);

  // Économie annuelle de l'offtaker : écart tarif réseau − PPA sur l'énergie servie.
  const annualSavings = input.servedRenewableKwh * (input.currentGridTariff - ppaTariff);

  return {
    capex,
    opexAnnual,
    ppaTariff,
    irr,
    paybackYears,
    annualSavings,
    currency: input.currency ?? "USD",
  };
}
