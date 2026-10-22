import { en } from "./en";
import { fr, type Dict } from "./fr";
import type { Locale } from "@/lib/format";

export type { Dict };
export const LOCALES: Locale[] = ["fr", "en"];
export const DEFAULT_LOCALE: Locale = "fr";
export const LOCALE_COOKIE = "ap2i_locale";

export const dictionaries: Record<Locale, Dict> = { fr, en };

export function normalizeLocale(v: string | undefined | null): Locale {
  return v === "en" ? "en" : "fr";
}

/** Looks up a label in a code → label map, falling back to the raw code (never invents a value). */
export function label(map: Record<string, string>, code: string | null | undefined): string {
  if (code === null || code === undefined || code === "") return "";
  return map[code] ?? code.replace(/_/g, " ");
}

/** Replaces {name} placeholders. */
export function interpolate(s: string, vars: Record<string, string | number>): string {
  return s.replace(/\{(\w+)\}/g, (_, k: string) => String(vars[k] ?? `{${k}}`));
}

/** Flattens a nested dictionary into dotted keys (used by the key-parity test). */
export function flatKeys(obj: object, prefix = ""): string[] {
  return Object.entries(obj).flatMap(([k, v]) =>
    v && typeof v === "object" ? flatKeys(v as object, `${prefix}${k}.`) : [`${prefix}${k}`],
  );
}
