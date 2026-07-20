import { describe, it, expect } from "vitest";
import { simulate } from "./energy-balance";
import { sizeToTargetReliability } from "./sizing";
import { optimizeEconomicMix } from "./economic-optimization";

const battery = { roundTrip: 0.9, dod: 0.9, cRate: 0.5 };

/** Productible synthétique : cloche diurne (0 la nuit, pic à midi). */
function syntheticYield(hours = 8760): number[] {
  const y = new Array(hours);
  for (let h = 0; h < hours; h++) {
    const hod = h % 24;
    // profil solaire simple : sinus positif entre 6h et 18h
    const x = (hod - 6) / 12;
    y[h] = x > 0 && x < 1 ? Math.sin(Math.PI * x) * 0.6 : 0; // kWh/kWc/h
  }
  return y;
}

/** Charge plate (industrie continue). */
function flatLoad(kw: number, hours = 8760): number[] {
  return new Array(hours).fill(kw);
}

describe("simulate — bilan énergétique horaire", () => {
  it("sans solaire ni batterie, couverture nulle et déficit = charge totale", () => {
    const load = flatLoad(100);
    const y = syntheticYield();
    const r = simulate(0, 0, load, y, battery);
    expect(r.coverageRate).toBe(0);
    expect(r.residualDeficitKwh).toBeCloseTo(100 * 8760, 0);
    expect(r.peakResidualDeficitKw).toBeCloseTo(100, 5);
  });

  it("couverture croît de façon monotone avec la capacité batterie (PV fixe)", () => {
    const load = flatLoad(100);
    const y = syntheticYield();
    const pv = 400;
    const cov = [0, 200, 500, 1000, 2000].map(
      (e) => simulate(pv, e, load, y, battery).coverageRate,
    );
    for (let i = 1; i < cov.length; i++) {
      expect(cov[i]).toBeGreaterThanOrEqual(cov[i - 1] - 1e-9);
    }
  });

  it("couverture ∈ [0,1] et bilan cohérent (servi + déficit = charge)", () => {
    const load = flatLoad(100);
    const y = syntheticYield();
    const r = simulate(500, 1500, load, y, battery);
    expect(r.coverageRate).toBeGreaterThan(0);
    expect(r.coverageRate).toBeLessThanOrEqual(1);
    expect(r.servedRenewableKwh + r.residualDeficitKwh).toBeCloseTo(r.totalLoadKwh, 3);
  });

  it("écrête le surplus quand la batterie est pleine (PV très surdimensionné)", () => {
    const load = flatLoad(10);
    const y = syntheticYield();
    const r = simulate(1000, 50, load, y, battery);
    expect(r.curtailedKwh).toBeGreaterThan(0);
  });
});

describe("sizeToTargetReliability — dimensionnement à cible fixée", () => {
  it("atteint la couverture cible et renseigne les sorties attendues", () => {
    const load = flatLoad(100);
    const y = syntheticYield();
    const target = 0.9;
    const r = sizeToTargetReliability({
      load,
      yieldPerKwp: y,
      targetReliabilityRate: target,
      battery,
    });
    expect(r.targetReached).toBe(true);
    expect(r.coverageRate).toBeGreaterThanOrEqual(target - 1e-6);
    expect(r.pvSizeKwp).toBeGreaterThan(0);
    expect(r.batterySizeKwh).toBeGreaterThan(0);
    expect(r.backupSizeKw).toBeGreaterThanOrEqual(0);
    expect(r.annualYieldKwh).toBeGreaterThan(0);
    expect(r.reliabilityCost).toBeGreaterThan(0);
  });

  it("une cible plus haute exige davantage de stockage", () => {
    const load = flatLoad(100);
    const y = syntheticYield();
    const low = sizeToTargetReliability({ load, yieldPerKwp: y, targetReliabilityRate: 0.7, battery });
    const high = sizeToTargetReliability({ load, yieldPerKwp: y, targetReliabilityRate: 0.95, battery });
    expect(high.batterySizeKwh).toBeGreaterThanOrEqual(low.batterySizeKwh);
  });
});

describe("optimizeEconomicMix — extension réservée", () => {
  it("renvoie un résultat compatible SizingResult sans contrainte dure de couverture", () => {
    const load = flatLoad(100);
    const y = syntheticYield();
    const r = optimizeEconomicMix({
      load,
      yieldPerKwp: y,
      battery,
      outageCostPerKwh: 0.5,
      gridSteps: 6,
    });
    expect(r.pvSizeKwp).toBeGreaterThanOrEqual(0);
    expect(r.coverageRate).toBeGreaterThanOrEqual(0);
    expect(r.coverageRate).toBeLessThanOrEqual(1);
  });
});
