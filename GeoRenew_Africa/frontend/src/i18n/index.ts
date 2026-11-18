import { en } from "./en";
import { enumsFr, fr, type MessageKey } from "./fr";

export type Lang = "fr" | "en";

function readLang(): Lang {
  try {
    return localStorage.getItem("georenew.lang") === "en" ? "en" : "fr";
  } catch {
    return "fr";
  }
}

let current: Lang = typeof window === "undefined" ? "fr" : readLang();

export function setLang(lang: Lang): void {
  current = lang;
  try {
    localStorage.setItem("georenew.lang", lang);
  } catch {
    /* stockage indisponible : la langue n'est pas mémorisée */
  }
}

export function getLang(): Lang {
  return current;
}

export function t(key: MessageKey): string {
  return (current === "en" ? en : fr)[key];
}

/** Libellé d'une valeur d'énumération de l'API (les énumérations restent en français en P1). */
export function label(value: string | null | undefined): string {
  if (!value) return "—";
  return enumsFr[value] ?? value;
}
