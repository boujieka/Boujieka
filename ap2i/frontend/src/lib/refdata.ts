import "server-only";
import { apiGet } from "./api";
import type { Instrument, Partner, Sector } from "./types";
import type { Locale } from "./format";
import type { Dict } from "@/i18n";

/** Reference lists used by filter forms. */
export async function refData(locale: Locale) {
  const [sectors, partners, instruments] = await Promise.all([apiGet<Sector[]>("/sectors"), apiGet<Partner[]>("/partners"), apiGet<Instrument[]>("/instruments")]);
  return {
    sectors: sectors.ok ? sectors.data.map((s) => [s.code, locale === "fr" ? s.name_fr : s.name_en] as [string, string]) : [],
    partners: partners.ok ? partners.data.map((p) => [p.code, p.short_name || p.name] as [string, string]) : [],
    instruments: instruments.ok ? instruments.data.map((i) => [i.code, locale === "fr" ? i.name_fr : i.name_en] as [string, string]) : [],
    partnerById: partners.ok ? new Map(partners.data.map((p) => [p.id, p])) : new Map<number, Partner>(),
  };
}

export function statusOptions(d: Dict): [string, string][] {
  return Object.entries(d.projectStatus).filter(([k]) => k !== "unknown");
}
export function verificationOptions(d: Dict): [string, string][] {
  return Object.entries(d.verificationStatus);
}
