import { describe, expect, it } from "vitest";
import { currencyEntries, fmtAmount, fmtNumber, fmtPct, toNumber } from "./format";

describe("format", () => {
  it("never turns missing values into 0", () => {
    expect(toNumber(null)).toBeNull();
    expect(toNumber("")).toBeNull();
    expect(fmtAmount(null, "USD", "en")).toBeNull();
    expect(fmtNumber(undefined, "fr")).toBeNull();
    expect(fmtPct(null, "en")).toBeNull();
  });
  it("keeps real zeros", () => {
    expect(fmtNumber("0", "en")).toBe("0");
  });
  it("formats per currency without summing", () => {
    expect(fmtAmount("300000000.0000", "USD", "en")).toBe("300,000,000 USD");
    expect(currencyEntries({ XDR: "1", EUR: "2" })).toEqual([["EUR", "2"], ["XDR", "1"]]);
    expect(currencyEntries(null)).toEqual([]);
  });
  it("percent", () => {
    expect(fmtPct("0.1776", "en")).toBe("17.8%");
  });
});
