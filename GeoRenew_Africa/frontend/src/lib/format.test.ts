import { describe, expect, it } from "vitest";
import { errorMessage } from "./api";
import { formatHa, natureLabel, shortHash } from "./format";

describe("format", () => {
  it("convertit m² en ha au format français", () => {
    expect(formatHa(740000)).toBe("74,00 ha".replace(" ", " ").replace(" ha", " ha"));
    expect(formatHa(null)).toBe("—");
  });
  it("distingue les natures de valeur", () => {
    expect(natureLabel("calcule")).toBe("Calculé");
    expect(natureLabel("hypothetique")).toBe("Hypothétique");
    expect(natureLabel("inconnu")).toBe("Inconnu");
    expect(natureLabel("renseigne")).toBe("Renseigné");
  });
  it("raccourcit les empreintes", () => {
    expect(shortHash("abcdef0123456789")).toBe("abcdef012345");
  });
  it("lit les erreurs métier et de validation de l'API", () => {
    expect(errorMessage({ detail: { code: "x", message: "Refusé" } }, 422)).toEqual({ code: "x", message: "Refusé" });
    expect(errorMessage({ detail: [{ loc: ["body", "name"], msg: "trop court" }] }, 422).message).toBe("name : trop court");
    expect(errorMessage(null, 500).message).toBe("Erreur HTTP 500");
    expect(errorMessage({ detail: { code: "api_non_configuree", message: "API non configurée" } }, 503).code).toBe("api_non_configuree");
  });
});
