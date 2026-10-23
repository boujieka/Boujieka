import { createContext, useContext, useMemo } from "react";
import { filterAgreements, filterProjects, toQuery, type Filters } from "./filters";
import { usdByProject } from "./agg";
import type { Snapshot } from "./types";
import type { Locale } from "./format";

const REGIONS_FR: Record<string, string> = { "Central Africa": "Afrique centrale", "West Africa": "Afrique de l'Ouest",
  "East Africa": "Afrique de l'Est", "North Africa": "Afrique du Nord", "Southern Africa": "Afrique australe" };

export const SnapCtx = createContext<Snapshot | null>(null);

export function useSnap(): Snapshot {
  const s = useContext(SnapCtx);
  if (!s) throw new Error("snapshot not loaded");
  return s;
}

/** Projects / agreements matching the global filters (memoised per filter state). */
export function useSelection(f: Filters) {
  const s = useSnap();
  const usd = useMemo(() => usdByProject(s.agreements), [s]);
  // keyed on the canonical query string: a new-but-equal filter object (every render, every hash change) reuses the result
  const key = toQuery(f);
  return useMemo(() => {
    const { projects, undatedExcluded } = filterProjects(s.projects, f, usd);
    const ids = new Set(projects.map((p) => p.id));
    const agreements = filterAgreements(s.agreements, ids, f);
    return { projects, undatedExcluded, ids, agreements, agreementIds: new Set(agreements.map((a) => a.id)), usd };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [s, key, usd]);
}

export function useNames(locale: Locale) {
  const s = useSnap();
  return useMemo(() => {
    const sectors = new Map(s.ref.sectors.map((x) => [x.code, locale === "fr" ? x.name_fr : x.name_en]));
    const partners = new Map(s.ref.partners.map((x) => [x.code, x.short_name]));
    const instruments = new Map(s.ref.instruments.map((x) => [x.code, locale === "fr" ? x.name_fr : x.name_en]));
    const countries = new Map(s.ref.countries.map((x) => [x.iso3, locale === "fr" ? x.name_fr : x.name_en]));
    return {
      sector: (c: string | null) => (c ? sectors.get(c) ?? c : locale === "fr" ? "Non classé" : "Unclassified"),
      partner: (c: string | null) => (c ? partners.get(c) ?? c : locale === "fr" ? "Non renseigné" : "Not reported"),
      instrument: (c: string | null) => (c ? instruments.get(c) ?? c : locale === "fr" ? "Non renseigné" : "Not reported"),
      country: (c: string | null) => (c ? countries.get(c) ?? c : "—"),
      region: (r: string) => (locale === "fr" ? REGIONS_FR[r] ?? r : r),
      sectors, partners, instruments, countries,
    };
  }, [s, locale]);
}
