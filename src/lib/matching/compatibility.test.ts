import { describe, it, expect } from "vitest";
import {
  computeCompatibility,
  geographyScore,
  sizeScore,
  technologyScore,
  rankDevelopers,
  type OpportunityForMatch,
  type DeveloperForMatch,
} from "./compatibility";

const baseOpp: OpportunityForMatch = {
  country: "CM",
  region: "Littoral",
  projectSizeKw: 1000,
  requiredTechnologies: ["solaire", "stockage", "hybride"],
  rating: "B",
};

const baseDev: DeveloperForMatch = {
  zones: [{ country: "CM", region: "Littoral" }],
  technologies: ["solaire", "stockage", "hybride"],
  minProjectSizeKw: 200,
  maxProjectSizeKw: 5000,
  financingCapacity: "mixte",
};

describe("filtres durs", () => {
  it("annule la compatibilité hors zone géographique", () => {
    const dev = { ...baseDev, zones: [{ country: "GA" }] };
    const r = computeCompatibility(baseOpp, dev);
    expect(r.hardFiltered).toBe(true);
    expect(r.hardFilterReason).toBe("geographie");
    expect(r.compatibilityScore).toBe(0);
  });

  it("annule la compatibilité si hybride requis mais stockage absent", () => {
    const dev = { ...baseDev, technologies: ["solaire"] as const };
    const r = computeCompatibility(baseOpp, dev as unknown as DeveloperForMatch);
    expect(r.hardFiltered).toBe(true);
    expect(r.hardFilterReason).toBe("technologie");
    expect(r.compatibilityScore).toBe(0);
  });

  it("hybride satisfait par solaire + stockage même sans techno 'hybride' explicite", () => {
    const dev = { ...baseDev, technologies: ["solaire", "stockage"] as const };
    const r = computeCompatibility(baseOpp, dev as unknown as DeveloperForMatch);
    expect(r.hardFiltered).toBe(false);
    expect(r.technologyScore).toBeGreaterThan(0);
  });
});

describe("sous-scores", () => {
  it("géographie : pays+région = 1.0, pays seul = 0.6, sinon 0", () => {
    expect(geographyScore(baseOpp, baseDev)).toBe(1.0);
    expect(geographyScore(baseOpp, { ...baseDev, zones: [{ country: "CM", region: "Centre" }] })).toBe(0.6);
    expect(geographyScore(baseOpp, { ...baseDev, zones: [{ country: "SN" }] })).toBe(0.0);
  });

  it("taille : 1.0 dans la fourchette, décroissance de part et d'autre", () => {
    expect(sizeScore({ ...baseOpp, projectSizeKw: 1000 }, baseDev)).toBe(1.0);
    expect(sizeScore({ ...baseOpp, projectSizeKw: 100 }, baseDev)).toBeCloseTo(1 - (200 - 100) / 200, 5);
    expect(sizeScore({ ...baseOpp, projectSizeKw: 10000 }, baseDev)).toBe(0);
  });

  it("technologie : part des capacités requises détenues", () => {
    const opp: OpportunityForMatch = { ...baseOpp, requiredTechnologies: ["solaire", "stockage"] };
    const dev: DeveloperForMatch = { ...baseDev, technologies: ["solaire"] };
    expect(technologyScore(opp, dev)).toBe(0.5);
  });
});

describe("agrégation et classement", () => {
  it("score parfait quand tout est aligné", () => {
    const r = computeCompatibility(baseOpp, baseDev);
    expect(r.compatibilityScore).toBeCloseTo(0.3 * 1 + 0.3 * 1 + 0.2 * 1 + 0.2 * Math.min(1, 0.75 + 0.15), 5);
  });

  it("classe les développeurs par score décroissant et exclut les incompatibles", () => {
    const good = baseDev;
    const partial = { ...baseDev, zones: [{ country: "CM", region: "Centre" }] }; // géo 0.6
    const incompatible = { ...baseDev, zones: [{ country: "SN" }] }; // filtré
    const ranked = rankDevelopers(baseOpp, [partial, good, incompatible]);
    expect(ranked).toHaveLength(2);
    expect(ranked[0].developer).toBe(good);
    expect(ranked[0].result.compatibilityScore).toBeGreaterThan(ranked[1].result.compatibilityScore);
  });
});
