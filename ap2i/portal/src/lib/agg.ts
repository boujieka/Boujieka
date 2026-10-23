// Aggregations over the snapshot. Rules (AP²I methodology):
//  * amounts in different currencies are never added; USD equivalents use the annual average rate of the
//    transaction year (commitments of an agreement: its approval year), as computed by the backend;
//  * amounts whose USD equivalent is missing are reported per original currency as "not converted";
//  * commitments, disbursements and expenditures are separate measures;
//  * an empty selection gives `null` (not available), never 0.
import type { AgreementRow, FlowTable, ProjectRow } from "./types";
import { year } from "./filters";

export interface Money {
  usd: number | null; // null = no amount in the selection
  byCurrency: Record<string, number>;
  unconverted: Record<string, number>;
  n: number;
}

export const emptyMoney = (): Money => ({ usd: null, byCurrency: {}, unconverted: {}, n: 0 });

export function addMoney(m: Money, amount: number, currency: string, usd: number | null) {
  m.n++;
  m.byCurrency[currency] = (m.byCurrency[currency] ?? 0) + amount;
  if (usd === null) m.unconverted[currency] = (m.unconverted[currency] ?? 0) + amount;
  else m.usd = (m.usd ?? 0) + usd;
}

export const isComplete = (m: Money) => Object.keys(m.unconverted).length === 0;
const num = (v: string | null) => (v === null ? null : Number(v));

export function commitmentsOf(agreements: AgreementRow[]): Money {
  const m = emptyMoney();
  for (const a of agreements) {
    if (a.committed === null || !a.currency) continue;
    addMoney(m, Number(a.committed), a.currency, num(a.committed_usd));
  }
  return m;
}

/** Cumulative disbursed as published, per original currency (dated series are in `annual`). No USD sum: the
 * cumulative figures have no single date to choose a rate from. */
export function disbursedByCurrency(agreements: AgreementRow[]): Record<string, number> {
  const out: Record<string, number> = {};
  for (const a of agreements) if (a.disbursed !== null && a.currency) out[a.currency] = (out[a.currency] ?? 0) + Number(a.disbursed);
  return out;
}

export type FlowKind = FlowTable["kind"][number];

/** Dated transactions per year, for the selected agreements. */
export function annual(flows: FlowTable, agreementIds: Set<number>, kind: FlowKind, y0: number, y1: number) {
  const years: Record<number, Money> = {};
  for (let y = y0; y <= y1; y++) years[y] = emptyMoney();
  let undated = 0;
  for (let i = 0; i < flows.kind.length; i++) {
    if (flows.kind[i] !== kind || !agreementIds.has(flows.agreement[i])) continue;
    const y = flows.year[i];
    if (y === null) {
      undated++;
      continue;
    }
    if (y < y0 || y > y1) continue;
    addMoney(years[y], Number(flows.amount[i]), flows.currency[i], num(flows.usd[i]));
  }
  return { years, undated };
}

export function transactionsOf(flows: FlowTable, agreementId: number) {
  const out = [];
  for (let i = 0; i < flows.kind.length; i++) {
    if (flows.agreement[i] !== agreementId) continue;
    out.push({ i, kind: flows.kind[i], date: flows.date[i], year: flows.year[i], amount: flows.amount[i], currency: flows.currency[i],
      usd: flows.usd[i], rate_source: flows.rate_source[i] });
  }
  return out;
}

export function countBy<T>(items: T[], key: (t: T) => string | string[] | null | undefined, missing = "—"): Map<string, number> {
  const m = new Map<string, number>();
  for (const it of items) {
    let k = key(it);
    if (k === null || k === undefined || (Array.isArray(k) && !k.length)) k = missing;
    for (const kk of Array.isArray(k) ? k : [k]) m.set(kk, (m.get(kk) ?? 0) + 1);
  }
  return new Map([...m.entries()].sort((a, b) => b[1] - a[1]));
}

export function moneyBy(agreements: AgreementRow[], key: (a: AgreementRow) => string | null, missing = "—"): Map<string, Money> {
  const m = new Map<string, Money>();
  for (const a of agreements) {
    if (a.committed === null || !a.currency) continue;
    const k = key(a) ?? missing;
    if (!m.has(k)) m.set(k, emptyMoney());
    addMoney(m.get(k)!, Number(a.committed), a.currency, num(a.committed_usd));
  }
  return new Map([...m.entries()].sort((a, b) => (b[1].usd ?? 0) - (a[1].usd ?? 0)));
}

/** Committed USD per project (null when nothing convertible). */
export function usdByProject(agreements: AgreementRow[]): Map<number, number | null> {
  const m = new Map<number, number | null>();
  for (const a of agreements) {
    if (!m.has(a.project)) m.set(a.project, null);
    if (a.committed_usd !== null) m.set(a.project, (m.get(a.project) ?? 0) + Number(a.committed_usd));
  }
  return m;
}

/** Disbursement rate of a project: only when all its non-guarantee agreements with both figures share one
 * currency (same rule as the backend indicator: disbursed / net commitment, same currency). */
export function disbursementRate(agreements: AgreementRow[]): { value: number | null; reason: string | null } {
  const usable = agreements.filter((a) => !a.is_guarantee && a.committed !== null && a.disbursed !== null && a.currency && Number(a.committed) > 0);
  if (!usable.length) return { value: null, reason: "missing_inputs" };
  const curs = new Set(usable.map((a) => a.currency));
  if (curs.size > 1) return { value: null, reason: "multiple_currencies" };
  const c = usable.reduce((s, a) => s + Number(a.committed), 0);
  const d = usable.reduce((s, a) => s + Number(a.disbursed), 0);
  return { value: d / c, reason: null };
}

/** Share of the planned implementation period elapsed (backend formula: (min(today, end) - start) / (end - start)). */
export function elapsedRatio(p: ProjectRow, today: Date): number | null {
  const start = p.start ?? p.approval;
  const end = p.current_end;
  if (!start || !end) return null;
  const s = Date.parse(start), e = Date.parse(end);
  if (!(e > s)) return null;
  return (Math.min(today.getTime(), e) - s) / (e - s);
}

export function slippageDays(p: ProjectRow): number | null {
  if (!p.planned_end || !p.revised_end) return null;
  return Math.round((Date.parse(p.revised_end) - Date.parse(p.planned_end)) / 86400000);
}

export function maxLevel(p: ProjectRow) {
  for (const l of ["critical_attention", "high_attention", "watch", "information"] as const) if ((p.alerts[l] ?? 0) > 0) return l;
  return null;
}

/** Completion year of a closed/completed project. Active projects are never counted, even when the source publishes an
 * "actual" end date (some publishers fill it with the planned date); an actual date equal to the planned one is
 * treated as the proxy, not as an observed completion. */
export function completionYear(p: ProjectRow): { year: number; basis: "actual" | "closing_date" } | null {
  if (p.status !== "completed" && p.status !== "closed") return null;
  if (p.actual_end && p.actual_end !== p.planned_end) return { year: year(p.actual_end)!, basis: "actual" };
  const end = p.actual_end ?? p.portfolio_end;
  return end ? { year: year(end)!, basis: "closing_date" } : null;
}

/** Year flags for annual charts: the current (partial) year and years with unconverted amounts. */
export function yearFlags(years: number[], series: Money[][], generatedAt: string) {
  const current = Number(generatedAt.slice(0, 4));
  return years.map((y, i) => ({
    partial: y === current,
    incomplete: series.some((s) => Object.keys(s[i]?.unconverted ?? {}).length > 0),
  }));
}
