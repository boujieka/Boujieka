import { describe, expect, it } from "vitest";
import { toCSV } from "./exporters";

describe("CSV export", () => {
  it("quotes, keeps provenance, blanks missing values and guards formulas", () => {
    const s = toCSV(["a", "b"], [["x,y", null], ["=HYPERLINK(1)", 3]], ["AP²I snapshot"]);
    expect(s.split("\r\n")).toEqual(["# AP²I snapshot", "a,b", '"x,y",', "'=HYPERLINK(1),3"]);
  });
});
