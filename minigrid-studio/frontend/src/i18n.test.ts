import { describe, expect, it } from "vitest";
import { allKeysTranslated, formatValue, t } from "./i18n";

describe("i18n", () => {
  it("translates every key in French and English", () => {
    expect(allKeysTranslated()).toBe(true);
    expect(t("run", "fr")).toBe("Calculer");
    expect(t("run", "en")).toBe("Calculate");
  });
  it("formats values per locale and unit", () => {
    expect(formatValue(0.126574, "%", "en")).toBe("12.66%");
    expect(formatValue(null, "%", "fr")).toBe("n/a");
    expect(formatValue(1234.5, "currency", "en")).toBe("1,234.5");
  });
});
