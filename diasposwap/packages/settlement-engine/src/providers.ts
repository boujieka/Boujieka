import type { CountryCode, CurrencyCode } from '@diasposwap/shared-types';
import { hmacHex, safeEqual } from './hmac';

/**
 * Abstract payment provider. Real adapters (SEPA, Interac, MTN MoMo, Orange Money, Airtel Money,
 * M-Pesa, banks, licensed PSPs) are NOT implemented: no partner has authorised DiaspoSwap's model.
 * Only the simulated adapters below exist; they move no money.
 */
export type ProviderOpStatus = 'PENDING' | 'SUCCEEDED' | 'FAILED';
export type ProviderOpKind = 'COLLECTION' | 'PAYOUT' | 'REFUND';

export interface ProviderOperation {
  providerRef: string;
  kind: ProviderOpKind;
  idempotencyKey: string;
  amount: bigint;
  currency: CurrencyCode;
  country: CountryCode;
  /** Opaque, masked account reference (never full bank details). */
  accountRef: string;
  status: ProviderOpStatus;
  failureReason?: string;
}

export interface ProviderOperationRequest {
  idempotencyKey: string;
  amount: bigint;
  currency: CurrencyCode;
  country: CountryCode;
  accountRef: string;
}

export interface WebhookEvent {
  eventId: string;
  providerRef: string;
  status: Exclude<ProviderOpStatus, 'PENDING'>;
  failureReason?: string;
}

export interface PaymentProvider {
  readonly id: string;
  readonly rail: 'SEPA' | 'INTERAC' | 'MOBILE_MONEY' | 'BANK' | 'PSP';
  readonly countries: readonly CountryCode[];
  readonly simulated: boolean;
  collect(req: ProviderOperationRequest): ProviderOperation;
  payout(req: ProviderOperationRequest): ProviderOperation;
  refund(req: ProviderOperationRequest): ProviderOperation;
  get(providerRef: string): ProviderOperation | undefined;
  all(): readonly ProviderOperation[];
  /** Verifies a webhook signature and parses it. Returns null if the signature is invalid. */
  parseWebhook(rawBody: string, signature: string): WebhookEvent | null;
}

/**
 * Simulated provider. Account references ending in "FAIL" make payouts fail (to test failure paths).
 * Operations are idempotent on `idempotencyKey`: retrying a request returns the same operation.
 */
export class SimulatedProvider implements PaymentProvider {
  readonly simulated = true;
  private readonly ops = new Map<string, ProviderOperation>();
  private readonly byKey = new Map<string, string>();
  private seq = 0;
  private eventSeq = 0;

  constructor(
    readonly id: string,
    readonly rail: PaymentProvider['rail'],
    readonly countries: readonly CountryCode[],
    private readonly webhookSecret: string,
  ) {}

  private create(kind: ProviderOpKind, req: ProviderOperationRequest): ProviderOperation {
    const k = `${kind}:${req.idempotencyKey}`;
    const existing = this.byKey.get(k);
    if (existing) return this.ops.get(existing) as ProviderOperation;
    if (!this.countries.includes(req.country)) throw new Error(`${this.id} does not operate in ${req.country}`);
    if (req.amount <= 0n) throw new Error('Amount must be positive');
    const op: ProviderOperation = {
      providerRef: `${this.id}_${(++this.seq).toString().padStart(6, '0')}`,
      kind, idempotencyKey: req.idempotencyKey, amount: req.amount, currency: req.currency,
      country: req.country, accountRef: req.accountRef, status: 'PENDING',
    };
    this.ops.set(op.providerRef, op);
    this.byKey.set(k, op.providerRef);
    return { ...op };
  }

  collect(req: ProviderOperationRequest) { return this.create('COLLECTION', req); }
  payout(req: ProviderOperationRequest) { return this.create('PAYOUT', req); }
  refund(req: ProviderOperationRequest) { return this.create('REFUND', req); }
  get(ref: string) { const o = this.ops.get(ref); return o ? { ...o } : undefined; }
  all() { return [...this.ops.values()].map((o) => ({ ...o })); }

  /** Simulates the provider finishing an operation and emitting a signed webhook. */
  complete(providerRef: string, forceStatus?: 'SUCCEEDED' | 'FAILED'): { rawBody: string; signature: string } {
    const op = this.ops.get(providerRef);
    if (!op) throw new Error(`Unknown op ${providerRef}`);
    const fail = forceStatus === 'FAILED' || (forceStatus === undefined && op.kind === 'PAYOUT' && op.accountRef.endsWith('FAIL'));
    op.status = fail ? 'FAILED' : 'SUCCEEDED';
    if (fail) op.failureReason = 'SIMULATED_BENEFICIARY_ACCOUNT_REJECTED';
    const event: WebhookEvent = {
      eventId: `${this.id}_evt_${(++this.eventSeq).toString().padStart(6, '0')}`,
      providerRef, status: op.status, ...(fail ? { failureReason: op.failureReason } : {}),
    };
    const rawBody = JSON.stringify(event);
    return { rawBody, signature: hmacHex(this.webhookSecret, rawBody) };
  }

  parseWebhook(rawBody: string, signature: string): WebhookEvent | null {
    if (!safeEqual(hmacHex(this.webhookSecret, rawBody), signature)) return null;
    try {
      const e = JSON.parse(rawBody) as WebhookEvent;
      if (typeof e.eventId !== 'string' || typeof e.providerRef !== 'string' || (e.status !== 'SUCCEEDED' && e.status !== 'FAILED')) return null;
      return e;
    } catch {
      return null;
    }
  }
}

/** Default simulated rails per country (names describe the rail type, not a real partner). */
export function defaultSimulatedProviders(secret: string): PaymentProvider[] {
  return [
    new SimulatedProvider('sim_sepa', 'SEPA', ['FR'], secret),
    new SimulatedProvider('sim_interac', 'INTERAC', ['CA'], secret),
    new SimulatedProvider('sim_bank_us', 'BANK', ['US'], secret),
    new SimulatedProvider('sim_bank_gb', 'BANK', ['GB'], secret),
    new SimulatedProvider('sim_bank_za', 'BANK', ['ZA'], secret),
    new SimulatedProvider('sim_momo_cemac', 'MOBILE_MONEY', ['CM', 'CG'], secret),
    new SimulatedProvider('sim_momo_umoa', 'MOBILE_MONEY', ['SN', 'CI'], secret),
    new SimulatedProvider('sim_bank_ng', 'BANK', ['NG'], secret),
  ];
}
