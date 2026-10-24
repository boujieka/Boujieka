import { describe, expect, it } from "vitest";
import { allKeysTranslated, formatValue, t, translateMessage } from "./i18n";
import { niceTicks } from "./components/LineChart";
import { parseHash, href } from "./router";

// French rules as served by /engine/labels (Python regex syntax, groups written \1)
const RULES: [string, string][] = [
  ["^Derived DSCR falls to ([\\d.]+)x in a repayment year, below the ([\\d.]+)x target \\(the workbook has no DSCR covenant test\\)\\.$",
    "Le DSCR dérivé descend à \\1x une année de remboursement, sous la cible de \\2x (le classeur ne teste aucun covenant de DSCR)."],
  ["^(.*)Must be (.+)\\.$", "\\1Valeur attendue : \\2."],
];

describe("i18n", () => {
  it("translates every key in French and English", () => {
    expect(allKeysTranslated()).toBe(true);
    expect(t("calculate", "fr")).toBe("Calculer");
    expect(t("calculate", "en")).toBe("Calculate");
  });
  it("formats values per locale and unit", () => {
    expect(formatValue(0.126574, "%", "en")).toBe("12.66%");
    expect(formatValue(null, "%", "fr")).toBe("n/a");
    expect(formatValue(1234.5, "currency", "en")).toBe("1,235");
    expect(formatValue(1.2, "x", "en")).toBe("1.20 x");
  });
  it("applies the server's message rules", () => {
    expect(translateMessage("Derived DSCR falls to 0.37x in a repayment year, below the 1.20x target (the workbook has no DSCR covenant test).", RULES))
      .toBe("Le DSCR dérivé descend à 0.37x une année de remboursement, sous la cible de 1.20x (le classeur ne teste aucun covenant de DSCR).");
    expect(translateMessage("debt.drawdown: Must be 'Pari Passu' or 'Equity first'.; other", RULES))
      .toBe("debt.drawdown: Valeur attendue : 'Pari Passu' or 'Equity first'.; other");
    expect(translateMessage("unchanged", [])).toBe("unchanged");
  });
});

describe("chart axis", () => {
  it("always reaches the data maximum and includes zero", () => {
    for (const [lo, hi] of [[0, 4.33e6], [0, 1.2], [-3.8e6, 3.2e6], [0, 0], [0, 0.37]]) {
      const tk = niceTicks(Math.min(lo, 0), Math.max(hi, 0));
      expect(tk[0]).toBeLessThanOrEqual(lo);
      expect(tk[tk.length - 1]).toBeGreaterThanOrEqual(hi);
    }
  });
});

describe("router", () => {
  it("round-trips routes", () => {
    const r = parseHash(href("runs", "abc 1", { x: "1" }));
    expect(r.name).toBe("runs");
    expect(r.id).toBe("abc 1");
    expect(r.query.get("x")).toBe("1");
    expect(parseHash("").name).toBe("projects");
  });
});
