"use client";

import { createContext, useContext } from "react";
import type { Dict } from "@/i18n";
import type { Locale } from "@/lib/format";

const Ctx = createContext<{ locale: Locale; d: Dict } | null>(null);

export function I18nProvider({ locale, d, children }: { locale: Locale; d: Dict; children: React.ReactNode }) {
  return <Ctx.Provider value={{ locale, d }}>{children}</Ctx.Provider>;
}

export function useI18n() {
  const v = useContext(Ctx);
  if (!v) throw new Error("useI18n outside I18nProvider");
  return v;
}
