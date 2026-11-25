import { type CurrencyCode, type FxRate, formatMoney, rateToDisplay } from '@diasposwap/shared-types';

export const fmt = (amount: bigint, currency: CurrencyCode, locale: 'fr' | 'en') => formatMoney({ amount, currency }, locale);

export function fmtRate(rate: FxRate, locale: 'fr' | 'en'): string {
  const v = rateToDisplay(rate, 4);
  return `1 ${rate.base} = ${locale === 'fr' ? v.replace('.', ',') : v} ${rate.quote}`;
}

export function fmtDate(iso: string, locale: 'fr' | 'en'): string {
  return new Date(iso).toLocaleString(locale === 'fr' ? 'fr-FR' : 'en-GB', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
}
