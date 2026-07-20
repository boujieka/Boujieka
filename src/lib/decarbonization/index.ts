/**
 * Module de décarbonisation : tCO₂ évitées via le facteur d'émission réseau
 * du pays. La décarbonisation est une grandeur MESURÉE et stockée, non une
 * mention qualitative.
 *
 *   tCO₂ évitées/an = énergie renouvelable servie (MWh) × facteur (tCO₂/MWh)
 */

import { decarbonizationLifetimeYears } from "../config";

export interface DecarbonizationInput {
  /** Énergie renouvelable servie sur l'année (kWh) — sortie de la simulation. */
  servedRenewableKwh: number;
  /** Facteur d'émission du réseau du pays (tCO₂/MWh). */
  emissionFactorTco2PerMwh: number;
  /** Durée de vie pour le cumul (années). Défaut : config. */
  lifetimeYears?: number;
}

export interface DecarbonizationResult {
  annualCo2AvoidedTonnes: number;
  lifetimeCo2AvoidedTonnes: number;
}

export function computeDecarbonization(input: DecarbonizationInput): DecarbonizationResult {
  const mwh = input.servedRenewableKwh / 1000;
  const annual = mwh * input.emissionFactorTco2PerMwh;
  const years = input.lifetimeYears ?? decarbonizationLifetimeYears;
  return {
    annualCo2AvoidedTonnes: annual,
    lifetimeCo2AvoidedTonnes: annual * years,
  };
}

/**
 * Agrège un portefeuille d'opportunités : total annuel et cumulé de CO₂ évité.
 * Alimente le suivi portefeuille de décarbonisation.
 */
export function aggregatePortfolio(
  metrics: { annualCo2AvoidedTonnes: number; lifetimeCo2AvoidedTonnes: number }[],
): DecarbonizationResult {
  return metrics.reduce(
    (acc, m) => ({
      annualCo2AvoidedTonnes: acc.annualCo2AvoidedTonnes + m.annualCo2AvoidedTonnes,
      lifetimeCo2AvoidedTonnes: acc.lifetimeCo2AvoidedTonnes + m.lifetimeCo2AvoidedTonnes,
    }),
    { annualCo2AvoidedTonnes: 0, lifetimeCo2AvoidedTonnes: 0 },
  );
}
