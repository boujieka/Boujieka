import { type CountryCode, COUNTRIES, INITIAL_CORRIDORS, pow10, CURRENCIES } from '@diasposwap/shared-types';
import type { KycLevel } from '@diasposwap/compliance-engine';
import { type SwapSimulator, SimulationError } from './simulator';

/** Seeded PRNG (mulberry32) so demo data is reproducible. */
export function prng(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const FIRST = ['Amina', 'Jean', 'Fatou', 'Paul', 'Aïcha', 'Emmanuel', 'Mariam', 'Serge', 'Grace', 'Ibrahima', 'Clarisse', 'Kofi', 'Ngozi', 'Thabo', 'Brice', 'Estelle'];
const LAST = ['Mbarga', 'Ndiaye', 'Kouassi', 'Okafor', 'Nkosi', 'Moukoko', 'Diallo', 'Bakala', 'Essomba', 'Traoré', 'Adeyemi', 'Mabiala', 'Tchoumi', 'Koné'];

export interface DemoSeedOptions { seed?: number; users?: number; orders?: number; settle?: boolean }

/**
 * Populates a simulator with fictional, reproducible data. All names are generated; no real person,
 * bank account or phone number is used. Amounts follow a log-uniform-ish distribution (10..2000 EUR equivalent).
 */
export function seedDemo(sim: SwapSimulator, opts: DemoSeedOptions = {}): { users: string[]; orders: string[]; failedCreates: number } {
  const rnd = prng(opts.seed ?? 42);
  const pick = <T>(xs: readonly T[]): T => xs[Math.floor(rnd() * xs.length)] as T;
  const countries = [...new Set(INITIAL_CORRIDORS.flatMap((c) => [c.a, c.b]))] as CountryCode[];
  const users: string[] = [];
  const nUsers = opts.users ?? 1000;
  for (let i = 0; i < nUsers; i++) {
    const id = `user_${(i + 1).toString().padStart(4, '0')}`;
    const country = pick(countries);
    const r = rnd();
    const kyc: KycLevel = r < 0.05 ? 'BASIC' : r < 0.9 ? 'VERIFIED' : 'ENHANCED';
    sim.addUser({
      profile: { userId: id, fullName: `${pick(FIRST)} ${pick(LAST)}`, country, kycLevel: kyc, emailVerified: true, phoneVerified: true, pep: rnd() < 0.01 },
      fundingRef: `SIM-${country}-****${String(i).padStart(4, '0')}`,
      history: [],
    });
    users.push(id);
  }
  const orders: string[] = [];
  let failedCreates = 0;
  const nOrders = opts.orders ?? 5000;
  for (let i = 0; i < nOrders; i++) {
    const uid = pick(users);
    const user = sim.users.get(uid);
    if (!user) continue;
    const from = user.profile.country;
    const options = INITIAL_CORRIDORS.filter((c) => c.a === from || c.b === from).map((c) => (c.a === from ? c.b : c.a));
    if (options.length === 0) continue;
    const to = pick(options);
    const benId = `ben_${uid}_${to}`;
    if (!sim.beneficiaries.has(benId)) {
      sim.addBeneficiary({
        id: benId, ownerId: uid, fullName: `${pick(FIRST)} ${pick(LAST)}`, country: to, verified: rnd() > 0.03,
        accountRef: `SIM-${to}-****${String(i).padStart(4, '0')}${rnd() < 0.01 ? '-FAIL' : ''}`,
      });
    }
    const eurAmount = BigInt(Math.round(10 * Math.pow(200, rnd()))); // 10..2000 EUR
    const cur = COUNTRIES[from].currency;
    const rate = sim.rates()[cur];
    const principal = (eurAmount * rate.num * pow10(CURRENCIES[cur].exponent)) / rate.den;
    try {
      const q = sim.quote(uid, from, to, principal > 0n ? principal : 1n);
      const o = sim.createOrder({ quoteId: q.id, beneficiaryId: benId, allowPartial: rnd() > 0.1, idempotencyKey: `seed-${i}` });
      if (o.state === 'PENDING_FUNDING') sim.fund(o.id);
      orders.push(o.id);
    } catch (e) {
      if (e instanceof SimulationError) { failedCreates++; continue; }
      throw e;
    }
  }
  if (opts.settle !== false) sim.settleAllPending();
  return { users, orders, failedCreates };
}
