import type { Locale, LocaleBundle } from "../types";
import { en } from "./en";
import { fr } from "./fr";

export const bundles: Record<Locale, LocaleBundle> = { en, fr };

export const getBundle = (locale: Locale): LocaleBundle => bundles[locale];
