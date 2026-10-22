// Reconciliation of the portal's client-side aggregations with the database engine, on the REAL exported snapshot
// (portal/public/data, produced by `python -m app.cli export-public-snapshot`). Skipped when no snapshot is present.
import { existsSync, readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { annual, commitmentsOf } from "./agg";
import { filterAgreements, filterProjects } from "./filters";

const dir = new URL("../../public/data/", import.meta.url);
const has = existsSync(new URL("meta.json", dir));
const load = (n: string) => JSON.parse(readFileSync(new URL(n, dir), "utf8"));

describe.skipIf(!has)("real snapshot reconciles with the backend", () => {
  const meta = has ? load("meta.json") : null;
  const projects = has ? load("projects.json") : [];
  const agreements = has ? load("agreements.json") : [];
  const flows = has ? load("flows.json") : null;
  for (const iso3 of meta?.countries ?? []) {
    it(`${iso3}: total commitments (USD eq.) = /africa/overview`, () => {
      const { projects: ps } = filterProjects(projects, { country: iso3 });
      const m = commitmentsOf(filterAgreements(agreements, new Set(ps.map((p: { id: number }) => p.id)), {}));
      const api = load("africa.json").countries.find((c: { iso3: string }) => c.iso3 === iso3).commitments_usd;
      expect(Math.round(m.usd!)).toBe(Number(api));
    });
    it(`${iso3}: annual commitments and disbursements = portfolio engine (2011–2026)`, () => {
      const { projects: ps } = filterProjects(projects, { country: iso3 });
      const ag = filterAgreements(agreements, new Set(ps.map((p: { id: number }) => p.id)), {});
      const ids = new Set(ag.map((a: { id: number }) => a.id));
      const portfolio = load(`country-${iso3}.json`).portfolio;
      const c = annual(flows, ids, "commitment", 2011, 2026).years;
      const d = annual(flows, ids, "disbursement", 2011, 2026).years;
      for (const y of portfolio.years) {
        for (const [mine, api] of [[c[y.year], y.commitments], [d[y.year], y.disbursements]]) {
          if (api.usd_equivalent === null) expect(mine.usd).toBeNull();
          else expect(mine.usd!.toFixed(2)).toBe(Number(api.usd_equivalent).toFixed(2));
          for (const [cur, v] of Object.entries(api.by_currency)) expect(mine.byCurrency[cur].toFixed(2)).toBe(Number(v).toFixed(2));
        }
      }
    });
  }
  it("no synthetic project is exported and every project has a provenance file", () => {
    expect(projects.every((p: { ref: string; title: string }) => !/SYNTHETIC/.test(p.title))).toBe(true);
    expect(projects.length).toBe(meta.counts.projects);
    expect(projects.every((p: { ref: string }) => existsSync(new URL(`p/${p.ref}.json`, dir)))).toBe(true);
  });
});
