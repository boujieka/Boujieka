// Global filter state, kept in the URL hash (shareable links): #/<route>?country=CMR&sector=ENERGY&y0=2015...
import type { AgreementRow, AlertLevel, ProjectRow } from "./types";

export interface Filters {
  country?: string;
  y0?: number;
  y1?: number;
  sector?: string;
  partner?: string;
  instrument?: string;
  status?: string[];
  region?: string;
  q?: string;
  alert?: AlertLevel | "any";
  minusd?: number;
  dq?: number; // minimum completeness score (0–1)
}

export const LEVELS: AlertLevel[] = ["critical_attention", "high_attention", "watch", "information"];
const KEYS = ["country", "y0", "y1", "sector", "partner", "instrument", "status", "region", "q", "alert", "minusd", "dq"] as const;

export function parseFilters(qs: URLSearchParams): Filters {
  const f: Filters = {};
  const num = (k: string, min: number, max: number) => {
    const v = Number(qs.get(k));
    return qs.get(k) !== null && qs.get(k) !== "" && Number.isFinite(v) && v >= min && v <= max ? v : undefined;
  };
  const code = (k: string) => {
    const v = qs.get(k);
    return v && /^[A-Za-z0-9_\-]{1,40}$/.test(v) ? v : undefined; // validated: identifiers only
  };
  f.country = code("country")?.toUpperCase();
  f.y0 = num("y0", 1950, 2100);
  f.y1 = num("y1", 1950, 2100);
  f.sector = code("sector");
  f.partner = code("partner")?.toUpperCase();
  f.instrument = code("instrument");
  const st = qs.get("status");
  f.status = st ? st.split(",").filter((s) => /^[a-z_]{1,20}$/.test(s)) : undefined;
  if (f.status && !f.status.length) f.status = undefined;
  f.region = code("region");
  const q = qs.get("q");
  f.q = q ? q.slice(0, 100) : undefined;
  const al = qs.get("alert");
  f.alert = al === "any" || LEVELS.includes(al as AlertLevel) ? (al as Filters["alert"]) : undefined;
  f.minusd = num("minusd", 0, 1e13);
  f.dq = num("dq", 0, 1);
  for (const k of KEYS) if (f[k] === undefined) delete f[k];
  return f;
}

export function toQuery(f: Filters): string {
  const qs = new URLSearchParams();
  for (const k of KEYS) {
    const v = f[k];
    if (v === undefined || v === "" || (Array.isArray(v) && !v.length)) continue;
    qs.set(k, Array.isArray(v) ? v.join(",") : String(v));
  }
  const s = qs.toString();
  return s ? `?${s}` : "";
}

export const year = (d: string | null | undefined): number | null => (d ? Number(d.slice(0, 4)) : null);

/** Project-level filters. The year range applies to the approval year (projects without an approval date are
 * excluded while a year filter is active and are counted separately). */
export function filterProjects(projects: ProjectRow[], f: Filters, usdByProject?: Map<number, number | null>) {
  let undatedExcluded = 0;
  const q = f.q?.toLowerCase().trim();
  const out = projects.filter((p) => {
    if (f.country && p.country !== f.country) return false;
    if (f.sector && (f.sector === "UNCLASSIFIED" ? p.sector !== null : p.sector !== f.sector)) return false;
    if (f.partner && !p.partners.includes(f.partner)) return false;
    if (f.instrument && !p.instruments.includes(f.instrument)) return false;
    if (f.status && !f.status.includes(p.status)) return false;
    if (f.region && p.region !== f.region) return false;
    if (f.alert) {
      const lv = LEVELS.filter((l) => (p.alerts[l] ?? 0) > 0);
      if (f.alert === "any" ? !lv.length : !lv.includes(f.alert)) return false;
    }
    if (f.dq !== undefined && (p.dq === null || p.dq.completeness < f.dq)) return false;
    if (f.minusd !== undefined) {
      const v = usdByProject?.get(p.id);
      if (v === null || v === undefined || v < f.minusd) return false;
    }
    if (q && !(p.title.toLowerCase().includes(q) || p.ref.toLowerCase().includes(q) || (p.agency ?? "").toLowerCase().includes(q))) return false;
    if (f.y0 !== undefined || f.y1 !== undefined) {
      const y = year(p.approval);
      if (y === null) {
        undatedExcluded++;
        return false;
      }
      if (f.y0 !== undefined && y < f.y0) return false;
      if (f.y1 !== undefined && y > f.y1) return false;
    }
    return true;
  });
  return { projects: out, undatedExcluded };
}

/** Agreement-level selection for financial measures: agreements of the selected projects, restricted to the
 * selected financing institution / instrument when those filters are set. */
export function filterAgreements(agreements: AgreementRow[], projectIds: Set<number>, f: Filters): AgreementRow[] {
  return agreements.filter((a) => projectIds.has(a.project) && (!f.partner || a.partner === f.partner) &&
    (!f.instrument || a.instrument === f.instrument));
}

export function withoutYears(f: Filters): Filters {
  const { y0: _a, y1: _b, ...rest } = f;
  return rest;
}
