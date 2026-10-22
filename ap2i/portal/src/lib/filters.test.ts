import { describe, expect, it } from "vitest";
import { filterAgreements, filterProjects, parseFilters, toQuery } from "./filters";
import type { AgreementRow, ProjectRow } from "./types";

const P = (id: number, o: Partial<ProjectRow>) => ({ id, ref: `SYN-${id}`, title: `SYNTHETIC ${id}`, country: "CMR", sector: "ENERGY", region: null,
  status: "active", partners: ["WB"], instruments: [], alerts: {}, approval: "2015-01-01", agency: null, dq: { completeness: 0.5, traceability: 1, timeliness: null }, ...o }) as ProjectRow;

describe("URL filter state", () => {
  it("round-trips and rejects invalid values", () => {
    const f = parseFilters(new URLSearchParams("country=cmr&y0=2015&y1=2020&sector=ENERGY&status=active,closed&alert=watch"));
    expect(f).toEqual({ country: "CMR", y0: 2015, y1: 2020, sector: "ENERGY", status: ["active", "closed"], alert: "watch" });
    expect(parseFilters(new URLSearchParams(toQuery(f).slice(1)))).toEqual(f);
    const bad = parseFilters(new URLSearchParams("country=<script>&y0=abc&alert=boom&status=DROP TABLE&minusd=-5"));
    expect(bad).toEqual({});
  });
});

describe("project filters", () => {
  const ps = [P(1, {}), P(2, { sector: null, approval: null }), P(3, { partners: ["AFDB"], approval: "2021-05-01", status: "closed" }),
    P(4, { alerts: { high_attention: 1 }, title: "SYNTHETIC road Yaoundé" })];
  it("combines filters", () => {
    expect(filterProjects(ps, { partner: "AFDB" }).projects.map((p) => p.id)).toEqual([3]);
    expect(filterProjects(ps, { sector: "UNCLASSIFIED" }).projects.map((p) => p.id)).toEqual([2]);
    expect(filterProjects(ps, { alert: "any" }).projects.map((p) => p.id)).toEqual([4]);
    expect(filterProjects(ps, { q: "yaoundé" }).projects.map((p) => p.id)).toEqual([4]);
    expect(filterProjects(ps, { status: ["closed"], y0: 2020 }).projects.map((p) => p.id)).toEqual([3]);
  });
  it("year filter excludes undated projects and reports them", () => {
    const r = filterProjects(ps, { y0: 2010, y1: 2016 });
    expect(r.projects.map((p) => p.id)).toEqual([1, 4]);
    expect(r.undatedExcluded).toBe(1);
  });
  it("empty dataset gives empty results", () => {
    expect(filterProjects([], { sector: "ENERGY" }).projects).toEqual([]);
  });
  it("financial measures follow the institution filter at agreement level", () => {
    const a = [{ id: 1, project: 3, partner: "AFDB" }, { id: 2, project: 3, partner: "EU" }] as AgreementRow[];
    expect(filterAgreements(a, new Set([3]), { partner: "AFDB" }).map((x) => x.id)).toEqual([1]);
  });
});
