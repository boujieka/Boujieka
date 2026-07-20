import { describe, it, expect } from "vitest";
import { computeTechnoEconomic, internalRateOfReturn, npv } from "./techno-economic";
import { computeDecarbonization, aggregatePortfolio } from "./decarbonization";
import { computeBankability, ratingFromScore } from "./bankability";
import { irradianceToYield } from "./nasa-power";

describe("techno-économique", () => {
  it("TRI : NPV s'annule au taux renvoyé", () => {
    const cf = [-1000, 300, 300, 300, 300, 300];
    const irr = internalRateOfReturn(cf)!;
    expect(Math.abs(npv(irr, cf))).toBeLessThan(1e-3);
  });

  it("flux tous négatifs (aucun changement de signe) → TRI null", () => {
    expect(internalRateOfReturn([-1000, -10, -10, -10])).toBeNull();
  });

  it("calcule capex, ppa sous le tarif réseau, et économies positives", () => {
    const r = computeTechnoEconomic({
      pvSizeKwp: 1000,
      batterySizeKwh: 2000,
      backupSizeKw: 200,
      servedRenewableKwh: 1_800_000,
      currentGridTariff: 0.14,
    });
    expect(r.capex).toBeGreaterThan(0);
    expect(r.ppaTariff).toBeLessThan(0.14);
    expect(r.annualSavings).toBeGreaterThan(0);
    expect(r.opexAnnual).toBeGreaterThan(0);
  });
});

describe("décarbonisation", () => {
  it("tCO₂/an = MWh servis × facteur ; cumul = annuel × durée", () => {
    const r = computeDecarbonization({
      servedRenewableKwh: 1_000_000, // 1000 MWh
      emissionFactorTco2PerMwh: 0.5,
      lifetimeYears: 20,
    });
    expect(r.annualCo2AvoidedTonnes).toBeCloseTo(500, 3);
    expect(r.lifetimeCo2AvoidedTonnes).toBeCloseTo(10000, 3);
  });

  it("agrège un portefeuille", () => {
    const agg = aggregatePortfolio([
      { annualCo2AvoidedTonnes: 100, lifetimeCo2AvoidedTonnes: 2000 },
      { annualCo2AvoidedTonnes: 50, lifetimeCo2AvoidedTonnes: 1000 },
    ]);
    expect(agg.annualCo2AvoidedTonnes).toBe(150);
    expect(agg.lifetimeCo2AvoidedTonnes).toBe(3000);
  });
});

describe("bancabilité", () => {
  it("un projet critique bien couvert obtient un meilleur score de résilience", () => {
    const critique = computeBankability({
      irr: 0.15,
      paybackYears: 6,
      coverageRate: 0.95,
      targetReached: true,
      loadCriticality: "critique",
      gridOutageHoursYear: 400,
      annualCo2AvoidedTonnes: 500,
      emissionFactorTco2PerMwh: 0.6,
    });
    const faible = computeBankability({
      irr: 0.15,
      paybackYears: 6,
      coverageRate: 0.95,
      targetReached: true,
      loadCriticality: "faible",
      gridOutageHoursYear: 0,
      annualCo2AvoidedTonnes: 500,
      emissionFactorTco2PerMwh: 0.6,
    });
    expect(critique.resilienceScore).toBeGreaterThan(faible.resilienceScore);
    expect(["A", "B", "C", "D"]).toContain(critique.rating);
  });

  it("notation par paliers", () => {
    expect(ratingFromScore(0.85)).toBe("A");
    expect(ratingFromScore(0.7)).toBe("B");
    expect(ratingFromScore(0.55)).toBe("C");
    expect(ratingFromScore(0.3)).toBe("D");
  });
});

describe("nasa-power", () => {
  it("convertit l'irradiation en productible via le ratio de performance", () => {
    const y = irradianceToYield([1000, 500, 0], 0.8);
    expect(y[0]).toBeCloseTo(0.8, 5);
    expect(y[1]).toBeCloseTo(0.4, 5);
    expect(y[2]).toBe(0);
  });
});
