import { describe, expect, it } from "vitest";

import { addDays, emptyLabel, formatAmount, formatBps, formatDate, formatPct, formatRatio, formatShare, formatTenor } from "./format";

describe("empty-field labels", () => {
  it("distinguishes not disclosed / not available / pending", () => {
    expect(emptyLabel("not_disclosed")).toBe("Not disclosed");
    expect(emptyLabel("pending")).toBe("Pending");
    expect(emptyLabel("not_available")).toBe("Not available");
  });
  it("defaults an unexplained null to Not available, never to a value", () => {
    expect(emptyLabel(undefined)).toBe("Not available");
  });
});

describe("number formatting", () => {
  it("never drops the currency and never invents a value", () => {
    expect(formatAmount("23446000000.0000", "XAF")).toBe("23.45bn XAF");
    expect(formatAmount("4000000000", "KES")).toBe("4.00bn KES");
    expect(formatAmount("1500000", "XOF")).toBe("1.50m XOF");
    expect(formatAmount(null, "XAF")).toBeNull();
  });
  it("formats yields, ratios, shares and bps", () => {
    expect(formatPct("5.801300")).toBe("5.801%");
    expect(formatRatio("2.2100")).toBe("2.21×");
    expect(formatShare("0.9")).toBe("90.0%");
    expect(formatBps("25.00")).toBe("+25.0 bp");
    expect(formatBps("-3.5")).toBe("-3.5 bp");
    expect(formatPct(null)).toBeNull();
  });
});

describe("dates and tenors", () => {
  it("does not shift calendar dates across timezones", () => {
    expect(formatDate("2026-10-03")).toBe("03 Oct 2026");
    expect(formatDate(null)).toBeNull();
  });
  it("adds days across month ends", () => {
    expect(addDays("2026-09-28", 7)).toBe("2026-10-05");
    expect(addDays("2026-10-03", -6)).toBe("2026-09-27");
  });
  it("labels tenors", () => {
    expect(formatTenor(91)).toBe("13W");
    expect(formatTenor(182)).toBe("26W");
    expect(formatTenor(364)).toBe("52W");
    expect(formatTenor(1095)).toBe("3Y");
    expect(formatTenor(100)).toBe("100D");
  });
});
