import {
  type CorridorConfig, type CountryCode, type CurrencyCode, type FxRate, type StateChange, type TransferOrder, type TransferState,
  COUNTRIES, INITIAL_CORRIDORS, assertTransition, convertFloor, crossRate, divCeil, divFloor, findCorridor, isRateValid, referenceRates,
} from '@diasposwap/shared-types';
import { type AccountRef, Ledger } from '@diasposwap/ledger';
import { type Allocation, runMatching } from '@diasposwap/matching-engine';
import {
  type BeneficiaryProfile, type ComplianceResult, type CustomerProfile, type HistoryItem, evaluateTransfer,
} from '@diasposwap/compliance-engine';
import { type PaymentProvider, type ProviderOperation, defaultSimulatedProviders } from './providers';

/**
 * SwapSimulator: end-to-end orchestration of the DiaspoSwap flow IN SIMULATION MODE.
 * quote -> order -> compliance -> funding (simulated collection) -> matching -> local payouts -> ledger -> reconciliation.
 * No real money moves; every provider is a SimulatedProvider and every ledger entry is flagged `simulated`.
 */
export const SIMULATION_NOTICE_FR = 'Mode simulation — aucun argent réel';
export const SIMULATION_NOTICE_EN = 'Simulation mode — no real money';

export interface SimUser {
  profile: CustomerProfile;
  /** Masked funding source reference, e.g. "FR76 **** 1234". Never a real account. */
  fundingRef: string;
  history: HistoryItem[];
}

export interface Beneficiary extends BeneficiaryProfile {
  ownerId: string;
  /** Masked payout reference. Ending with "FAIL" makes simulated payouts fail. */
  accountRef: string;
  relationship?: string;
}

export interface Quote {
  id: string;
  userId: string;
  from: CountryCode;
  to: CountryCode;
  sendCurrency: CurrencyCode;
  receiveCurrency: CurrencyCode;
  principal: bigint;
  fee: bigint;
  total: bigint;
  rate: FxRate;
  estimatedReceive: bigint;
  createdAt: string;
  expiresAt: string;
}

export interface OrderRecord extends TransferOrder {
  quoteId: string;
  beneficiaryId: string;
  fee: bigint;
  complianceResult?: ComplianceResult;
  collectionRef?: string;
  refundRef?: string;
  refundedPrincipal: bigint;
  refundedFee: bigint;
}

export type PayoutStatus = 'PENDING' | 'SUCCEEDED' | 'FAILED' | 'EXCEPTION';

export interface PayoutRecord {
  id: string;
  allocationId: string;
  /** Order whose beneficiary receives this payout. */
  beneficiaryOrderId: string;
  /** Order whose funds pay it (the counterparty). */
  fundingOrderId: string;
  amount: bigint;
  currency: CurrencyCode;
  country: CountryCode;
  providerId: string;
  providerRef: string;
  attempts: number;
  status: PayoutStatus;
}

export interface SimulatorOptions {
  now?: () => Date;
  /** Commission in basis points (simulation hypothesis; default 0.75 %). */
  feeBps?: bigint;
  corridors?: readonly CorridorConfig[];
  providers?: PaymentProvider[];
  webhookSecret?: string;
  maxPayoutAttempts?: number;
  orderTtlHours?: number;
}

export class SimulationError extends Error {
  constructor(readonly code: string, message: string) { super(message); }
}

export class SwapSimulator {
  readonly ledger = new Ledger();
  readonly users = new Map<string, SimUser>();
  readonly beneficiaries = new Map<string, Beneficiary>();
  readonly quotes = new Map<string, Quote>();
  readonly orders = new Map<string, OrderRecord>();
  readonly allocations: Allocation[] = [];
  readonly payouts = new Map<string, PayoutRecord>();
  readonly audit: StateChange[] = [];
  readonly exceptions: { payoutId: string; reason: string; at: string }[] = [];
  readonly providers: PaymentProvider[];
  private readonly processedEvents = new Set<string>();
  private readonly idempotentOrders = new Map<string, string>();
  private readonly refOwner = new Map<string, { type: 'COLLECTION' | 'PAYOUT' | 'REFUND'; id: string }>();
  private readonly now: () => Date;
  private readonly feeBps: bigint;
  private readonly corridors: readonly CorridorConfig[];
  private readonly maxPayoutAttempts: number;
  private readonly orderTtlHours: number;
  private matchingLock = false;
  private seq = { q: 0, o: 0, p: 0, run: 0 };

  constructor(opts: SimulatorOptions = {}) {
    this.now = opts.now ?? (() => new Date());
    this.feeBps = opts.feeBps ?? 75n;
    this.corridors = opts.corridors ?? INITIAL_CORRIDORS;
    this.providers = opts.providers ?? defaultSimulatedProviders(opts.webhookSecret ?? 'demo-webhook-secret-not-for-production');
    this.maxPayoutAttempts = opts.maxPayoutAttempts ?? 3;
    this.orderTtlHours = opts.orderTtlHours ?? 72;
  }

  // ---------- reference data ----------
  rates(): Record<CurrencyCode, FxRate> {
    return referenceRates(this.now().toISOString());
  }

  addUser(u: SimUser): void { this.users.set(u.profile.userId, u); }
  addBeneficiary(b: Beneficiary): void { this.beneficiaries.set(b.id, b); }

  providerFor(country: CountryCode): PaymentProvider {
    const p = this.providers.find((x) => x.countries.includes(country));
    if (!p) throw new SimulationError('NO_PROVIDER', `No provider available in ${country}`);
    return p;
  }

  // ---------- quote ----------
  quote(userId: string, from: CountryCode, to: CountryCode, principal: bigint): Quote {
    const user = this.mustUser(userId);
    if (principal <= 0n) throw new SimulationError('INVALID_AMOUNT', 'Amount must be positive');
    const corridor = findCorridor(from, to, this.corridors);
    if (!corridor || corridor.mode !== 'SIMULATION') throw new SimulationError('CORRIDOR_UNAVAILABLE', `Corridor ${from}-${to} unavailable`);
    if (user.profile.country !== from) throw new SimulationError('COUNTRY_MISMATCH', 'Sender must send from their country of residence');
    const sendCurrency = COUNTRIES[from].currency;
    const receiveCurrency = COUNTRIES[to].currency;
    const rate = crossRate(sendCurrency, receiveCurrency, this.rates());
    const fee = divCeil(principal * this.feeBps, 10_000n);
    const createdAt = this.now();
    const q: Quote = {
      id: `q_${(++this.seq.q).toString().padStart(6, '0')}`,
      userId, from, to, sendCurrency, receiveCurrency, principal, fee, total: principal + fee, rate,
      estimatedReceive: convertFloor(principal, rate),
      createdAt: createdAt.toISOString(),
      expiresAt: new Date(createdAt.getTime() + rate.validForSeconds * 1000).toISOString(),
    };
    this.quotes.set(q.id, q);
    return q;
  }

  // ---------- order ----------
  createOrder(input: { quoteId: string; beneficiaryId: string; allowPartial?: boolean; idempotencyKey: string }): OrderRecord {
    const existing = this.idempotentOrders.get(input.idempotencyKey);
    if (existing) return this.mustOrder(existing);
    const q = this.quotes.get(input.quoteId);
    if (!q) throw new SimulationError('UNKNOWN_QUOTE', 'Unknown quote');
    const now = this.now();
    if (Date.parse(q.expiresAt) < now.getTime() || !isRateValid(q.rate, now)) throw new SimulationError('QUOTE_EXPIRED', 'Quote expired');
    const user = this.mustUser(q.userId);
    const ben = this.beneficiaries.get(input.beneficiaryId);
    if (!ben || ben.ownerId !== q.userId) throw new SimulationError('UNKNOWN_BENEFICIARY', 'Unknown beneficiary');

    const o: OrderRecord = {
      id: `ord_${(++this.seq.o).toString().padStart(6, '0')}`,
      userId: q.userId, fromCountry: q.from, toCountry: q.to, sendCurrency: q.sendCurrency, receiveCurrency: q.receiveCurrency,
      principal: q.principal, remaining: q.principal, fee: q.fee,
      createdAt: now.toISOString(), expiresAt: new Date(now.getTime() + this.orderTtlHours * 3600_000).toISOString(),
      allowPartial: input.allowPartial ?? true, state: 'DRAFT', compliance: 'NOT_CHECKED',
      quoteId: q.id, beneficiaryId: ben.id, refundedPrincipal: 0n, refundedFee: 0n,
    };
    this.orders.set(o.id, o);
    this.idempotentOrders.set(input.idempotencyKey, o.id);
    this.setState(o, 'QUOTED', `quote ${q.id}`, 'user');
    this.setState(o, 'PENDING_VERIFICATION', 'compliance screening', 'system');

    const result = evaluateTransfer({
      customer: user.profile, beneficiary: ben,
      request: { amountMinor: q.principal, currency: q.sendCurrency, from: q.from, to: q.to },
      history: user.history, now, rates: this.rates(), corridors: this.corridors,
    });
    o.complianceResult = result;
    if (result.decision === 'BLOCK') {
      o.compliance = 'BLOCKED';
      this.setState(o, 'FAILED', `compliance BLOCK: ${result.reasons.join(',')}`, 'compliance');
    } else if (result.decision === 'REVIEW') {
      o.compliance = 'REVIEW'; // stays PENDING_VERIFICATION until a compliance officer decides
    } else {
      o.compliance = 'CLEARED';
      this.setState(o, 'PENDING_FUNDING', 'compliance ALLOW', 'compliance');
    }
    return o;
  }

  /** Manual compliance decision (four-eyes control is enforced by the API layer). */
  reviewDecision(orderId: string, approve: boolean, officer: string): OrderRecord {
    const o = this.mustOrder(orderId);
    if (o.state !== 'PENDING_VERIFICATION' || o.compliance !== 'REVIEW') throw new SimulationError('NOT_IN_REVIEW', 'Order is not under review');
    if (approve) { o.compliance = 'CLEARED'; this.setState(o, 'PENDING_FUNDING', 'compliance review approved', officer); }
    else { o.compliance = 'BLOCKED'; this.setState(o, 'FAILED', 'compliance review rejected', officer); }
    return o;
  }

  cancel(orderId: string, actor: string): OrderRecord {
    const o = this.mustOrder(orderId);
    if (['DRAFT', 'QUOTED', 'PENDING_VERIFICATION', 'PENDING_FUNDING'].includes(o.state)) {
      this.setState(o, 'CANCELLED', 'cancelled before funding', actor);
      return o;
    }
    if (o.state === 'QUEUED' && o.remaining === o.principal) {
      this.startRefund(o, 'cancelled by user while queued, nothing matched');
      return o;
    }
    throw new SimulationError('NOT_CANCELLABLE', `Order in state ${o.state} cannot be cancelled`);
  }

  // ---------- funding ----------
  fund(orderId: string): ProviderOperation {
    const o = this.mustOrder(orderId);
    if (o.state !== 'PENDING_FUNDING') throw new SimulationError('NOT_FUNDABLE', `Order in state ${o.state}`);
    if (o.compliance !== 'CLEARED') throw new SimulationError('COMPLIANCE', 'Compliance not cleared');
    const user = this.mustUser(o.userId);
    const p = this.providerFor(o.fromCountry);
    const op = p.collect({ idempotencyKey: `collect:${o.id}`, amount: o.principal + o.fee, currency: o.sendCurrency, country: o.fromCountry, accountRef: user.fundingRef });
    o.collectionRef = op.providerRef;
    this.refOwner.set(`${p.id}:${op.providerRef}`, { type: 'COLLECTION', id: o.id });
    return op;
  }

  // ---------- webhooks ----------
  handleWebhook(providerId: string, rawBody: string, signature: string): { accepted: boolean; duplicate?: boolean; reason?: string } {
    const p = this.providers.find((x) => x.id === providerId);
    if (!p) return { accepted: false, reason: 'UNKNOWN_PROVIDER' };
    const ev = p.parseWebhook(rawBody, signature);
    if (!ev) return { accepted: false, reason: 'INVALID_SIGNATURE' };
    if (this.processedEvents.has(`${providerId}:${ev.eventId}`)) return { accepted: true, duplicate: true };
    const owner = this.refOwner.get(`${providerId}:${ev.providerRef}`);
    if (!owner) return { accepted: false, reason: 'UNKNOWN_REFERENCE' };
    const op = p.get(ev.providerRef);
    if (!op || op.status !== ev.status) return { accepted: false, reason: 'STATUS_MISMATCH' };
    this.processedEvents.add(`${providerId}:${ev.eventId}`);
    const at = this.now().toISOString();

    if (owner.type === 'COLLECTION') {
      const o = this.mustOrder(owner.id);
      if (o.state !== 'PENDING_FUNDING') return { accepted: true, duplicate: true };
      if (ev.status === 'FAILED') { this.setState(o, 'FAILED', 'collection failed', providerId); return { accepted: true }; }
      this.ledger.post({
        idempotencyKey: `collect:${providerId}:${ev.providerRef}`, at, reference: o.id,
        description: `Collecte simulée ${o.id}`,
        postings: [
          { account: this.acc('COLLECTION', o.sendCurrency, o.fromCountry), amount: o.principal + o.fee },
          { account: this.acc('CUSTOMER_FUNDS', o.sendCurrency, `${o.fromCountry}:${o.id}`), amount: -o.principal },
          { account: this.acc('FEE_REVENUE', o.sendCurrency, o.fromCountry), amount: -o.fee },
        ],
      });
      this.setState(o, 'FUNDED', 'collection confirmed', providerId);
      this.setState(o, 'QUEUED', 'waiting for a reciprocal order', 'system');
      return { accepted: true };
    }

    if (owner.type === 'PAYOUT') {
      const po = this.payouts.get(owner.id);
      if (!po || po.status !== 'PENDING' || po.providerRef !== ev.providerRef) return { accepted: true, duplicate: true };
      if (ev.status === 'SUCCEEDED') {
        po.status = 'SUCCEEDED';
        this.ledger.post({
          idempotencyKey: `payout:${providerId}:${ev.providerRef}`, at, reference: po.beneficiaryOrderId,
          description: `Paiement local simulé ${po.id}`,
          postings: [
            { account: this.acc('BENEFICIARY_PAYABLE', po.currency, `${po.country}:${po.beneficiaryOrderId}`), amount: po.amount },
            { account: this.acc('COLLECTION', po.currency, po.country), amount: -po.amount },
          ],
        });
        this.tryComplete(this.mustOrder(po.beneficiaryOrderId));
      } else {
        po.status = 'FAILED';
        if (po.attempts < this.maxPayoutAttempts) this.issuePayout(po);
        else {
          po.status = 'EXCEPTION';
          this.exceptions.push({ payoutId: po.id, reason: ev.failureReason ?? 'PAYOUT_FAILED', at });
          const o = this.mustOrder(po.beneficiaryOrderId);
          if (o.state === 'SETTLEMENT_PENDING') this.setState(o, 'DISPUTED', `payout ${po.id} failed ${po.attempts} times`, 'system');
        }
      }
      return { accepted: true };
    }

    // REFUND
    const o = this.mustOrder(owner.id);
    if (ev.status === 'FAILED') {
      this.exceptions.push({ payoutId: `refund:${o.id}`, reason: 'REFUND_FAILED', at });
      return { accepted: true };
    }
    this.ledger.post({
      idempotencyKey: `refund:${providerId}:${ev.providerRef}`, at, reference: o.id,
      description: `Remboursement simulé ${o.id}`,
      postings: [
        { account: this.acc('REFUND_PAYABLE', o.sendCurrency, `${o.fromCountry}:${o.id}`), amount: o.refundedPrincipal + o.refundedFee },
        { account: this.acc('COLLECTION', o.sendCurrency, o.fromCountry), amount: -(o.refundedPrincipal + o.refundedFee) },
      ],
    });
    if (o.state === 'REFUND_PENDING') this.setState(o, 'REFUNDED', 'refund confirmed', providerId);
    else this.tryComplete(o);
    return { accepted: true };
  }

  // ---------- matching ----------
  runMatching(): { runId: string; allocations: Allocation[] } {
    if (this.matchingLock) throw new SimulationError('MATCHING_IN_PROGRESS', 'A matching run is already in progress');
    this.matchingLock = true;
    try {
      const runId = `run_${(++this.seq.run).toString().padStart(5, '0')}`;
      const candidates = [...this.orders.values()].filter((o) => o.state === 'QUEUED' || o.state === 'PARTIALLY_MATCHED');
      const res = runMatching({ runId, orders: candidates, rates: this.rates(), now: this.now(), corridors: this.corridors });
      const at = this.now().toISOString();

      for (const a of res.allocations) {
        this.allocations.push(a);
        const t = this.mustOrder(a.takerOrderId);
        const m = this.mustOrder(a.makerOrderId);
        this.ledger.post({
          idempotencyKey: `alloc:${a.id}`, at, reference: a.id,
          description: `Compensation ${t.id} <-> ${m.id}`,
          postings: [
            { account: this.acc('CUSTOMER_FUNDS', a.takerCurrency, `${t.fromCountry}:${t.id}`), amount: a.takerAmount },
            { account: this.acc('BENEFICIARY_PAYABLE', a.takerCurrency, `${t.fromCountry}:${m.id}`), amount: -a.takerAmount },
            { account: this.acc('CUSTOMER_FUNDS', a.makerCurrency, `${m.fromCountry}:${m.id}`), amount: a.makerAmount },
            { account: this.acc('BENEFICIARY_PAYABLE', a.makerCurrency, `${m.fromCountry}:${t.id}`), amount: -a.makerAmount },
          ],
        });
        // taker's money pays the maker's beneficiary locally, and vice versa
        this.createPayout(a, m, t, a.takerAmount, a.takerCurrency, t.fromCountry);
        this.createPayout(a, t, m, a.makerAmount, a.makerCurrency, m.fromCountry);
      }

      for (const updated of res.orders) {
        const o = this.mustOrder(updated.id);
        o.remaining = updated.remaining;
        if (updated.state !== o.state) {
          if (updated.state === 'MATCHED') {
            this.setState(o, 'MATCHED', `fully matched in ${runId}`, 'swap-engine');
            this.setState(o, 'SETTLEMENT_PENDING', 'local payouts issued', 'system');
          } else if (updated.state === 'PARTIALLY_MATCHED') {
            this.setState(o, 'PARTIALLY_MATCHED', `partially matched in ${runId}`, 'swap-engine');
          }
        }
      }
      for (const d of res.dust) {
        const o = this.mustOrder(d.orderId);
        if (o.state === 'PARTIALLY_MATCHED') this.startRefund(o, 'remainder below minimum fill (dust)');
      }
      for (const id of res.expired) this.expire(this.mustOrder(id));
      return { runId, allocations: res.allocations };
    } finally {
      this.matchingLock = false;
    }
  }

  // ---------- refunds / expiry ----------
  private expire(o: OrderRecord): void {
    if (o.state === 'QUEUED' && o.remaining === o.principal) {
      this.setState(o, 'EXPIRED', 'no reciprocal order before expiry', 'system');
      this.startRefund(o, 'expired unmatched');
    } else if (o.state === 'PARTIALLY_MATCHED') {
      this.startRefund(o, 'expired with unmatched remainder');
    }
  }

  private startRefund(o: OrderRecord, reason: string): void {
    const remaining = o.remaining;
    if (remaining <= 0n) return;
    // fee refunded pro rata on the unmatched part (rounded down, in favour of no over-refund)
    const fee = divFloor(o.fee * remaining, o.principal);
    o.refundedPrincipal = remaining;
    o.refundedFee = fee;
    o.remaining = 0n;
    const at = this.now().toISOString();
    const postings = [
      { account: this.acc('CUSTOMER_FUNDS', o.sendCurrency, `${o.fromCountry}:${o.id}`), amount: remaining },
      { account: this.acc('REFUND_PAYABLE', o.sendCurrency, `${o.fromCountry}:${o.id}`), amount: -(remaining + fee) },
    ];
    if (fee > 0n) postings.push({ account: this.acc('FEE_REVENUE', o.sendCurrency, o.fromCountry), amount: fee });
    this.ledger.post({ idempotencyKey: `refund-init:${o.id}`, at, reference: o.id, description: `Remboursement initié ${o.id}: ${reason}`, postings });
    const unmatched = o.refundedPrincipal === o.principal;
    if (unmatched) this.setState(o, 'REFUND_PENDING', reason, 'system');
    else this.setState(o, 'SETTLEMENT_PENDING', `${reason}; remainder refunded`, 'system');
    const user = this.mustUser(o.userId);
    const p = this.providerFor(o.fromCountry);
    const op = p.refund({ idempotencyKey: `refund:${o.id}`, amount: remaining + fee, currency: o.sendCurrency, country: o.fromCountry, accountRef: user.fundingRef });
    o.refundRef = op.providerRef;
    this.refOwner.set(`${p.id}:${op.providerRef}`, { type: 'REFUND', id: o.id });
  }

  // ---------- payouts ----------
  private createPayout(a: Allocation, beneficiaryOrder: OrderRecord, fundingOrder: OrderRecord, amount: bigint, currency: CurrencyCode, country: CountryCode): void {
    const ben = this.beneficiaries.get(beneficiaryOrder.beneficiaryId);
    if (!ben) throw new SimulationError('UNKNOWN_BENEFICIARY', 'Beneficiary missing');
    if (ben.country !== country) throw new SimulationError('BENEFICIARY_COUNTRY', 'Beneficiary country mismatch');
    const p = this.providerFor(country);
    const po: PayoutRecord = {
      id: `po_${(++this.seq.p).toString().padStart(6, '0')}`, allocationId: a.id,
      beneficiaryOrderId: beneficiaryOrder.id, fundingOrderId: fundingOrder.id,
      amount, currency, country, providerId: p.id, providerRef: '', attempts: 0, status: 'PENDING',
    };
    this.payouts.set(po.id, po);
    this.issuePayout(po);
  }

  private issuePayout(po: PayoutRecord): void {
    const ben = this.beneficiaries.get(this.mustOrder(po.beneficiaryOrderId).beneficiaryId) as Beneficiary;
    const p = this.providerFor(po.country);
    po.attempts += 1;
    const op = p.payout({ idempotencyKey: `${po.id}:attempt${po.attempts}`, amount: po.amount, currency: po.currency, country: po.country, accountRef: ben.accountRef });
    po.providerRef = op.providerRef;
    po.status = 'PENDING';
    this.refOwner.set(`${p.id}:${op.providerRef}`, { type: 'PAYOUT', id: po.id });
  }

  /** Operator fix after an exception: update the beneficiary account and retry (simulation). */
  resolvePayoutException(payoutId: string, newAccountRef: string): void {
    const po = this.payouts.get(payoutId);
    if (!po || po.status !== 'EXCEPTION') throw new SimulationError('NO_EXCEPTION', 'No exception for this payout');
    const ben = this.beneficiaries.get(this.mustOrder(po.beneficiaryOrderId).beneficiaryId) as Beneficiary;
    ben.accountRef = newAccountRef;
    this.issuePayout(po);
  }

  private tryComplete(o: OrderRecord): void {
    if (o.state !== 'SETTLEMENT_PENDING' && o.state !== 'DISPUTED') return;
    if (o.remaining !== 0n) return;
    const pays = [...this.payouts.values()].filter((p) => p.beneficiaryOrderId === o.id);
    if (pays.some((p) => p.status !== 'SUCCEEDED')) return;
    if (o.refundRef) {
      const p = this.providerFor(o.fromCountry).get(o.refundRef);
      if (!p || p.status !== 'SUCCEEDED') return;
    }
    if (pays.length === 0) return;
    // settlement is declared only after the ledger shows nothing left owed to this beneficiary
    const owed = this.ledger.naturalBalance(this.acc('BENEFICIARY_PAYABLE', o.receiveCurrency, `${o.toCountry}:${o.id}`));
    if (owed !== 0n) return;
    this.setState(o, 'SETTLED', 'all local payouts confirmed and reconciled', 'system');
  }

  // ---------- reconciliation ----------
  reconcile(): { ok: boolean; issues: string[] } {
    const issues: string[] = [];
    if (!this.ledger.isBalanced()) issues.push('Ledger trial balance is not zero');
    const expected = new Map<string, bigint>();
    for (const p of this.providers) {
      for (const op of p.all()) {
        if (op.status !== 'SUCCEEDED') continue;
        const k = `${op.currency}:${op.country}`;
        const sign = op.kind === 'COLLECTION' ? 1n : -1n;
        expected.set(k, (expected.get(k) ?? 0n) + sign * op.amount);
        const key = `${op.kind === 'COLLECTION' ? 'collect' : op.kind === 'PAYOUT' ? 'payout' : 'refund'}:${p.id}:${op.providerRef}`;
        if (!this.ledger.all().some((e) => e.idempotencyKey === key)) issues.push(`Provider op ${p.id}:${op.providerRef} has no ledger entry`);
      }
    }
    for (const [id, { account, balance }] of this.ledger.balances()) {
      if (account.type !== 'COLLECTION') continue;
      const k = `${account.currency}:${account.scope}`;
      if ((expected.get(k) ?? 0n) !== balance) issues.push(`${id}: ledger ${balance} vs provider ${expected.get(k) ?? 0n}`);
      expected.delete(k);
    }
    for (const [k, v] of expected) if (v !== 0n) issues.push(`Provider balance ${k}=${v} missing in ledger`);
    return { ok: issues.length === 0, issues };
  }

  // ---------- views ----------
  /** What a user may see about an order: never the counterparty identity or account details. */
  userView(orderId: string) {
    const o = this.mustOrder(orderId);
    const received = [...this.payouts.values()].filter((p) => p.beneficiaryOrderId === o.id);
    return {
      id: o.id, state: o.state, fromCountry: o.fromCountry, toCountry: o.toCountry,
      sendCurrency: o.sendCurrency, receiveCurrency: o.receiveCurrency,
      principal: o.principal, fee: o.fee, matched: o.principal - o.remaining - o.refundedPrincipal,
      refunded: o.refundedPrincipal + o.refundedFee,
      beneficiaryReceived: received.filter((p) => p.status === 'SUCCEEDED').reduce((s, p) => s + p.amount, 0n),
      beneficiaryPending: received.filter((p) => p.status !== 'SUCCEEDED').reduce((s, p) => s + p.amount, 0n),
      matchCount: received.length,
      history: this.audit.filter((a) => a.orderId === o.id).map((a) => ({ to: a.to, at: a.at, reason: a.reason })),
      simulated: true as const,
    };
  }

  // ---------- helpers ----------
  private acc(type: AccountRef['type'], currency: CurrencyCode, scope: string): AccountRef {
    return { type, currency, scope };
  }

  private setState(o: OrderRecord, to: TransferState, reason: string, actor: string): void {
    if (o.state === to) return;
    assertTransition(o.state, to);
    this.audit.push({ orderId: o.id, from: o.state, to, at: this.now().toISOString(), reason, actor });
    o.state = to;
  }

  mustOrder(id: string): OrderRecord {
    const o = this.orders.get(id);
    if (!o) throw new SimulationError('UNKNOWN_ORDER', `Unknown order ${id}`);
    return o;
  }

  private mustUser(id: string): SimUser {
    const u = this.users.get(id);
    if (!u) throw new SimulationError('UNKNOWN_USER', `Unknown user ${id}`);
    return u;
  }

  /** Test/demo helper: complete every pending simulated provider operation and deliver its webhook. */
  settleAllPending(force?: 'SUCCEEDED' | 'FAILED'): number {
    let n = 0;
    for (let guard = 0; guard < 50; guard++) {
      let progressed = false;
      for (const p of this.providers) {
        const sp = p as PaymentProvider & { complete?: (ref: string, f?: 'SUCCEEDED' | 'FAILED') => { rawBody: string; signature: string } };
        if (!sp.complete) continue;
        for (const op of p.all()) {
          if (op.status !== 'PENDING') continue;
          const wh = sp.complete(op.providerRef, force);
          this.handleWebhook(p.id, wh.rawBody, wh.signature);
          n++; progressed = true;
        }
      }
      if (!progressed) break;
    }
    return n;
  }
}
