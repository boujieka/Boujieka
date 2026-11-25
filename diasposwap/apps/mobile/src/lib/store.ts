import { create } from 'zustand';
import { type CountryCode, COUNTRIES, CURRENCIES, convertFloor, crossRate, pow10 } from '@diasposwap/shared-types';
import { type OrderRecord, type Quote, SwapSimulator, seedDemo } from '@diasposwap/settlement-engine';
import { clearSession, saveSession } from './session';

export interface DemoProfile { userId: string; name: string; country: CountryCode; kyc: 'BASIC' | 'VERIFIED' | 'ENHANCED'; pep?: boolean; note: string }

/** Fictional demo profiles. No real person. */
export const DEMO_PROFILES: DemoProfile[] = [
  { userId: 'demo_amina', name: 'Amina Mbarga', country: 'FR', kyc: 'VERIFIED', note: 'France → Cameroun' },
  { userId: 'demo_jean', name: 'Jean Essomba', country: 'CM', kyc: 'VERIFIED', note: 'Cameroun → France' },
  { userId: 'demo_fatou', name: 'Fatou Ndiaye', country: 'SN', kyc: 'ENHANCED', note: 'Sénégal → France' },
  { userId: 'demo_serge', name: 'Serge Bakala', country: 'CA', kyc: 'VERIFIED', pep: true, note: 'Canada → Congo (revue PEP)' },
];

function buildSimulator(): SwapSimulator {
  const sim = new SwapSimulator();
  // a small background community so matching and liquidity have something to work with
  seedDemo(sim, { seed: 42, users: 120, orders: 260 });
  sim.runMatching();
  sim.settleAllPending();
  for (const p of DEMO_PROFILES) {
    sim.addUser({
      profile: { userId: p.userId, fullName: p.name, country: p.country, kycLevel: p.kyc, emailVerified: true, phoneVerified: true, pep: !!p.pep },
      fundingRef: `SIM-${p.country}-****${p.userId.length}${p.userId.charCodeAt(5)}`,
      history: [],
    });
  }
  const ben = (id: string, owner: string, fullName: string, country: CountryCode, accountRef: string, relationship: string) =>
    sim.addBeneficiary({ id, ownerId: owner, fullName, country, verified: true, accountRef, relationship });
  ben('b_paul', 'demo_amina', 'Paul Mbarga', 'CM', 'SIM-MOMO-CM-****4521', 'Père');
  ben('b_mireille', 'demo_amina', 'Mireille Mbarga', 'CG', 'SIM-MOMO-CG-****1180', 'Sœur');
  ben('b_grace', 'demo_jean', 'Grace Essomba', 'FR', 'SIM-IBAN-FR-****2290', 'Fille étudiante');
  ben('b_moussa', 'demo_fatou', 'Moussa Ndiaye', 'FR', 'SIM-IBAN-FR-****7731', 'Frère');
  ben('b_lea', 'demo_serge', 'Léa Bakala', 'CG', 'SIM-MOMO-CG-****6602', 'Mère');
  return sim;
}

let counterpartySeq = 0;

interface AppState {
  sim: SwapSimulator;
  version: number;
  userId: string | null;
  onboarded: boolean;
  locale: 'fr' | 'en';
  bump: () => void;
  setOnboarded: () => void;
  setLocale: (l: 'fr' | 'en') => void;
  login: (userId: string) => Promise<void>;
  logout: () => Promise<void>;
  placeOrder: (quote: Quote, beneficiaryId: string, allowPartial: boolean, idempotencyKey: string) => OrderRecord;
  simulateCounterparty: (orderId: string, fraction: 1 | 0.5) => void;
  runMatching: () => number;
  settle: () => void;
  cancel: (orderId: string) => void;
  addBeneficiary: (b: { fullName: string; country: CountryCode; accountRef: string }) => void;
}

export const useApp = create<AppState>((set, get) => ({
  sim: buildSimulator(),
  version: 0,
  userId: null,
  onboarded: false,
  locale: 'fr',
  bump: () => set((s) => ({ version: s.version + 1 })),
  setOnboarded: () => set({ onboarded: true }),
  setLocale: (locale) => set({ locale }),
  login: async (userId) => { await saveSession(userId); set({ userId }); },
  logout: async () => { await clearSession(); set({ userId: null }); },

  placeOrder: (quote, beneficiaryId, allowPartial, idempotencyKey) => {
    const { sim } = get();
    const o = sim.createOrder({ quoteId: quote.id, beneficiaryId, allowPartial, idempotencyKey });
    if (o.state === 'PENDING_FUNDING') {
      sim.fund(o.id);
      sim.settleAllPending(); // simulated collection confirmed by a signed webhook
    }
    get().bump();
    return o;
  },

  /** Creates a fictional reciprocal order (opposite direction) worth `fraction` of the remaining amount. */
  simulateCounterparty: (orderId, fraction) => {
    const { sim } = get();
    const o = sim.mustOrder(orderId);
    const id = `cp_${++counterpartySeq}`;
    sim.addUser({
      profile: { userId: id, fullName: `Contrepartie fictive ${counterpartySeq}`, country: o.toCountry, kycLevel: 'VERIFIED', emailVerified: true, phoneVerified: true, pep: false },
      fundingRef: `SIM-${o.toCountry}-****CP${counterpartySeq}`, history: [],
    });
    sim.addBeneficiary({ id: `${id}_ben`, ownerId: id, fullName: `Bénéficiaire fictif ${counterpartySeq}`, country: o.fromCountry, verified: true, accountRef: `SIM-${o.fromCountry}-****B${counterpartySeq}` });
    const rate = crossRate(o.sendCurrency, o.receiveCurrency, sim.rates());
    let amount = convertFloor(o.remaining, rate);
    if (fraction === 0.5) amount = amount / 2n;
    // round up slightly so the opposite order fully absorbs ours (the remainder becomes a refundable rounding dust on its side)
    amount += pow10(CURRENCIES[o.receiveCurrency].exponent);
    const q = sim.quote(id, o.toCountry, o.fromCountry, amount);
    const c = sim.createOrder({ quoteId: q.id, beneficiaryId: `${id}_ben`, idempotencyKey: `cp:${id}` });
    if (c.state === 'PENDING_FUNDING') sim.fund(c.id);
    sim.settleAllPending();
    get().bump();
  },

  runMatching: () => {
    const n = get().sim.runMatching().allocations.length;
    get().bump();
    return n;
  },
  settle: () => { get().sim.settleAllPending(); get().bump(); },
  cancel: (orderId) => {
    const { sim, userId } = get();
    sim.cancel(orderId, userId ?? 'user');
    sim.settleAllPending();
    get().bump();
  },
  addBeneficiary: (b) => {
    const { sim, userId } = get();
    if (!userId) return;
    const id = `b_${userId}_${sim.beneficiaries.size + 1}`;
    // simulated verification: accepted immediately in demo mode, flagged as such in the UI
    sim.addBeneficiary({ id, ownerId: userId, fullName: b.fullName, country: b.country, accountRef: b.accountRef, verified: true });
    get().bump();
  },
}));

/** Re-render on every simulator change. */
export function useSimVersion(): number {
  return useApp((s) => s.version);
}

export function useCurrentUser() {
  const { sim, userId } = useApp();
  useSimVersion();
  return userId ? sim.users.get(userId) ?? null : null;
}

export function userOrders(sim: SwapSimulator, userId: string): OrderRecord[] {
  return [...sim.orders.values()].filter((o) => o.userId === userId).sort((a, b) => (a.createdAt < b.createdAt ? 1 : -1));
}

export const countryName = (c: CountryCode, locale: 'fr' | 'en') => (locale === 'fr' ? COUNTRIES[c].nameFr : COUNTRIES[c].nameEn);
