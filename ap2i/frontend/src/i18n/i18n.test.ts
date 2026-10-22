import { describe, expect, it } from "vitest";
import { en } from "./en";
import { fr } from "./fr";
import { flatKeys, interpolate, label } from "./index";

describe("dictionaries", () => {
  it("fr and en have identical keys", () => {
    const f = flatKeys(fr).sort();
    const e = flatKeys(en).sort();
    expect(e).toEqual(f);
    expect(f.length).toBeGreaterThan(300);
  });
  it("no empty strings", () => {
    for (const dict of [fr, en]) {
      const walk = (o: object): void => {
        for (const v of Object.values(o)) {
          if (typeof v === "string") expect(v.trim().length).toBeGreaterThan(0);
          else walk(v as object);
        }
      };
      walk(dict);
    }
  });
  it("missing values are labelled, never zero", () => {
    expect(fr.common.na).toBe("Non disponible");
    expect(en.common.na).toBe("Not available");
  });
  it("label falls back to the code; interpolate fills placeholders", () => {
    expect(label(fr.projectStatus, "active")).toBe("En cours");
    expect(label(fr.projectStatus, "weird_code")).toBe("weird code");
    expect(interpolate(en.pricing.requestRecorded, { id: 7 })).toContain("reference 7");
  });
});
