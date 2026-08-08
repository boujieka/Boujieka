import { describe, expect, it } from "vitest";
import { buildSystemPrompt } from "@/services/ai/prompt";

describe("buildSystemPrompt", () => {
  it("includes the pedagogical method and safety rules unconditionally", () => {
    const prompt = buildSystemPrompt({});
    expect(prompt).toContain("MÉTHODE");
    expect(prompt).toContain("Donne un indice");
    expect(prompt).toContain("solution guidée");
    expect(prompt).toContain("N'invente jamais");
    expect(prompt).toContain("mineur");
  });

  it("includes provided context labels", () => {
    const prompt = buildSystemPrompt({
      programName: "Terminale C",
      subjectName: "Mathématiques",
      topicTitle: "Probabilités",
    });
    expect(prompt).toContain("Terminale C");
    expect(prompt).toContain("Mathématiques");
    expect(prompt).toContain("Probabilités");
  });

  it("only grounds on lesson/exercise content when explicitly provided (i.e. published)", () => {
    const withoutGrounding = buildSystemPrompt({ skillTitle: "Vocabulaire des probabilités" });
    expect(withoutGrounding).not.toContain("Leçon associée");

    const withGrounding = buildSystemPrompt({
      skillTitle: "Vocabulaire des probabilités",
      lessonContent: "Contenu de la leçon publiée.",
    });
    expect(withGrounding).toContain("Leçon associée (publiée)");
    expect(withGrounding).toContain("Contenu de la leçon publiée.");
  });

  it("handles no context at all without throwing", () => {
    expect(() => buildSystemPrompt({})).not.toThrow();
  });
});
