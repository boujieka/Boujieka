// Synthetic fixtures (SYNTHETIC — test only). Real-data reconciliation is in reconcile.test.ts.
import { describe, expect, it } from "vitest";
import { annual, commitmentsOf, completionYear, disbursementRate, elapsedRatio, moneyBy, usdByProject } from "./agg";
import type { AgreementRow, FlowTable, ProjectRow } from "./types";

const agr = (o: Partial<AgreementRow>): AgreementRow => ({
  id: 1, project: 1, source_identifier: "SYN-1", partner: "WB", instrument: "LOAN", instrument_label: null, approval: "2015-01-01",
  closing_original: null, closing_current: null, status: "active", currency: "USD", amount_original: null, committed: "100", committed_basis: null,
  cancelled: "0", disbursed: null, disbursed_basis: null, disbursed_as_of: null, undisbursed: null, is_guarantee: false, parent: null,
  committed_usd: "100", committed_usd_note: null, source_record_id: null, ...o,
});
const proj = (o: Partial<ProjectRow>): ProjectRow => ({
  id: 1, ref: "SYN-P1", title: "SYNTHETIC", country: "CMR", sector: "ENERGY", region: null, status: "active", operational_status: "unknown",
  verification: "unverified", approval: "2015-01-01", start: null, planned_end: null, revised_end: null, actual_end: null, current_end: null,
  portfolio_end: null, agency: null, partners: ["WB"], instruments: ["LOAN"], alerts: {}, physical_progress: null, original_cost: null,
  revised_cost: null, cost_currency: null, documents: 0, results_indicators: 0, latest_rating: null, dq: null, locations: [], last_source_update: null, ...o,
});

describe("currency handling", () => {
  it("never adds currencies; unconverted amounts are kept apart", () => {
    const m = commitmentsOf([agr({ id: 1 }), agr({ id: 2, currency: "EUR", committed: "50", committed_usd: "55" }),
      agr({ id: 3, currency: "XDR", committed: "10", committed_usd: null })]);
    expect(m.usd).toBe(155);
    expect(m.byCurrency).toEqual({ USD: 100, EUR: 50, XDR: 10 });
    expect(m.unconverted).toEqual({ XDR: 10 });
  });
  it("empty selection is null (not available), not zero", () => {
    expect(commitmentsOf([]).usd).toBeNull();
    expect(commitmentsOf([agr({ committed: null, committed_usd: null })]).usd).toBeNull();
  });
  it("groups by institution with USD equivalents", () => {
    const g = moneyBy([agr({ id: 1 }), agr({ id: 2, partner: "AFDB", committed_usd: "300" })], (a) => a.partner);
    expect([...g.keys()]).toEqual(["AFDB", "WB"]);
  });
  it("usd per project is null when nothing is convertible", () => {
    const m = usdByProject([agr({ project: 7, committed_usd: null })]);
    expect(m.get(7)).toBeNull();
  });
});

describe("annual series", () => {
  const flows: FlowTable = {
    kind: ["commitment", "disbursement", "disbursement", "disbursement"], agreement: [1, 1, 1, 2],
    date: ["2015-03-01", "2016-01-01", null, "2016-05-01"], year: [2015, 2016, null, 2016],
    amount: ["100", "20", "5", "7"], currency: ["USD", "USD", "USD", "EUR"], usd: ["100", "20", "5", null], rate_source: [null, null, null, null],
  };
  it("separates commitments and disbursements, counts undated, keeps gaps as null", () => {
    const d = annual(flows, new Set([1, 2]), "disbursement", 2014, 2016);
    expect(d.years[2016].usd).toBe(20);
    expect(d.years[2016].unconverted).toEqual({ EUR: 7 });
    expect(d.years[2014].usd).toBeNull();
    expect(d.undated).toBe(1);
    expect(annual(flows, new Set([1]), "commitment", 2014, 2016).years[2015].usd).toBe(100);
  });
});

describe("indicators", () => {
  it("disbursement rate needs one currency and excludes guarantees", () => {
    expect(disbursementRate([agr({ disbursed: "25" })]).value).toBe(0.25);
    expect(disbursementRate([agr({ disbursed: "25" }), agr({ id: 2, currency: "EUR", disbursed: "1" })]).reason).toBe("multiple_currencies");
    expect(disbursementRate([agr({ disbursed: "25", is_guarantee: true })]).value).toBeNull();
    expect(disbursementRate([agr({})]).value).toBeNull(); // disbursed missing: not computed
  });
  it("elapsed share uses start (or approval) and current end; missing dates give null", () => {
    expect(elapsedRatio(proj({ start: "2020-01-01", current_end: "2022-01-01" }), new Date("2021-01-01"))).toBeCloseTo(0.5, 2);
    expect(elapsedRatio(proj({ current_end: null }), new Date())).toBeNull();
  });
  it("completion year: actual date, else closing date for closed projects only", () => {
    expect(completionYear(proj({ actual_end: "2019-06-30" }))).toEqual({ year: 2019, basis: "actual" });
    expect(completionYear(proj({ status: "closed", portfolio_end: "2018-12-31" }))).toEqual({ year: 2018, basis: "closing_date" });
    expect(completionYear(proj({ status: "active", portfolio_end: "2018-12-31" }))).toBeNull();
  });
});
