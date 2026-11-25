import type { CurrencyCode } from './money';

export type CountryCode = 'FR' | 'CM' | 'CG' | 'CA' | 'SN' | 'CI' | 'US' | 'GB' | 'NG' | 'ZA';

export interface CountryInfo {
  code: CountryCode;
  nameFr: string;
  nameEn: string;
  currency: CurrencyCode;
  flag: string;
  /** Monetary/regulatory zone, for compliance routing. */
  zone: 'EU' | 'CEMAC' | 'UMOA' | 'CANADA' | 'USA' | 'UK' | 'NIGERIA' | 'SACU';
}

export const COUNTRIES: Readonly<Record<CountryCode, CountryInfo>> = {
  FR: { code: 'FR', nameFr: 'France', nameEn: 'France', currency: 'EUR', flag: '🇫🇷', zone: 'EU' },
  CM: { code: 'CM', nameFr: 'Cameroun', nameEn: 'Cameroon', currency: 'XAF', flag: '🇨🇲', zone: 'CEMAC' },
  CG: { code: 'CG', nameFr: 'République du Congo', nameEn: 'Republic of the Congo', currency: 'XAF', flag: '🇨🇬', zone: 'CEMAC' },
  CA: { code: 'CA', nameFr: 'Canada', nameEn: 'Canada', currency: 'CAD', flag: '🇨🇦', zone: 'CANADA' },
  SN: { code: 'SN', nameFr: 'Sénégal', nameEn: 'Senegal', currency: 'XOF', flag: '🇸🇳', zone: 'UMOA' },
  CI: { code: 'CI', nameFr: "Côte d'Ivoire", nameEn: "Côte d'Ivoire", currency: 'XOF', flag: '🇨🇮', zone: 'UMOA' },
  US: { code: 'US', nameFr: 'États-Unis', nameEn: 'United States', currency: 'USD', flag: '🇺🇸', zone: 'USA' },
  GB: { code: 'GB', nameFr: 'Royaume-Uni', nameEn: 'United Kingdom', currency: 'GBP', flag: '🇬🇧', zone: 'UK' },
  NG: { code: 'NG', nameFr: 'Nigeria', nameEn: 'Nigeria', currency: 'NGN', flag: '🇳🇬', zone: 'NIGERIA' },
  ZA: { code: 'ZA', nameFr: 'Afrique du Sud', nameEn: 'South Africa', currency: 'ZAR', flag: '🇿🇦', zone: 'SACU' },
};

/** A corridor is an unordered pair of countries; flows go in both directions. */
export interface CorridorConfig {
  id: string;
  a: CountryCode;
  b: CountryCode;
  /** Simulation corridors are usable in demo mode only. */
  mode: 'SIMULATION' | 'DISABLED';
  /** Real operations require prior legal, regulatory and partner authorisation. Always false in this version. */
  liveAuthorised: false;
  /** Per-order ceiling expressed in EUR cents (simulation hypothesis, not a regulatory figure). */
  maxOrderEurCents: bigint;
  /** Smallest allocation the engine will create, in EUR cents (avoids dust). */
  minFillEurCents: bigint;
}

const mk = (a: CountryCode, b: CountryCode): CorridorConfig => ({
  id: `${a}-${b}`, a, b, mode: 'SIMULATION', liveAuthorised: false,
  maxOrderEurCents: 5_000_00n, minFillEurCents: 10_00n,
});

/** The 10 initial corridors, all in SIMULATION mode. */
export const INITIAL_CORRIDORS: readonly CorridorConfig[] = [
  mk('FR', 'CM'), mk('FR', 'CG'), mk('CA', 'CM'), mk('CA', 'CG'), mk('FR', 'SN'),
  mk('FR', 'CI'), mk('US', 'CM'), mk('GB', 'NG'), mk('ZA', 'CM'), mk('CG', 'CM'),
];

export function findCorridor(from: CountryCode, to: CountryCode, corridors: readonly CorridorConfig[] = INITIAL_CORRIDORS): CorridorConfig | undefined {
  return corridors.find((c) => (c.a === from && c.b === to) || (c.a === to && c.b === from));
}

/** Directed flow key, e.g. "FR>CM". */
export const flowKey = (from: CountryCode, to: CountryCode): string => `${from}>${to}`;
