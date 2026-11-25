import type { CurrencyCode } from '@diasposwap/shared-types';

/**
 * Double-entry ledger, append-only. SIMULATION ONLY: balances represent no real deposit.
 * Corrections are made with reversal entries, never by editing or deleting.
 */
export type AccountKind = 'ASSET' | 'LIABILITY' | 'REVENUE' | 'EXPENSE' | 'EQUITY';

export type AccountType =
  | 'COLLECTION'          // asset: funds held at the partner collecting locally
  | 'CUSTOMER_FUNDS'      // liability: funds received from a sender, not yet allocated
  | 'BENEFICIARY_PAYABLE' // liability: owed to a beneficiary after a match
  | 'FEE_REVENUE'         // revenue
  | 'REFUND_PAYABLE'      // liability: owed back to a sender
  | 'CLEARING'            // technical compensation account
  | 'RECONCILIATION'      // suspense for unexplained bank/provider differences
  | 'FX_DIFFERENCE';      // FX rounding/differences

const KIND: Record<AccountType, AccountKind> = {
  COLLECTION: 'ASSET', CUSTOMER_FUNDS: 'LIABILITY', BENEFICIARY_PAYABLE: 'LIABILITY', FEE_REVENUE: 'REVENUE',
  REFUND_PAYABLE: 'LIABILITY', CLEARING: 'ASSET', RECONCILIATION: 'ASSET', FX_DIFFERENCE: 'EXPENSE',
};

export interface AccountRef {
  type: AccountType;
  currency: CurrencyCode;
  /** Country / partner / user scoping, e.g. "FR" or "FR:user_1". */
  scope: string;
}

export const accountId = (a: AccountRef): string => `${a.type}:${a.currency}:${a.scope}`;
export const accountKind = (t: AccountType): AccountKind => KIND[t];

export interface Posting {
  account: AccountRef;
  /** Positive = debit, negative = credit. Minor units. */
  amount: bigint;
}

export interface JournalEntry {
  readonly id: string;
  readonly seq: number;
  readonly idempotencyKey: string;
  readonly at: string;
  readonly description: string;
  readonly reference: string;
  readonly postings: readonly Readonly<Posting>[];
  readonly reverses?: string;
  readonly simulated: true;
}

export class LedgerError extends Error {}

export interface PostInput {
  idempotencyKey: string;
  at: string;
  description: string;
  reference: string;
  postings: Posting[];
}

export class Ledger {
  private readonly entries: JournalEntry[] = [];
  private readonly byKey = new Map<string, JournalEntry>();
  private readonly reversed = new Set<string>();

  /** Posts a balanced entry. Re-posting the same idempotency key returns the original entry unchanged. */
  post(input: PostInput): JournalEntry {
    const existing = this.byKey.get(input.idempotencyKey);
    if (existing) {
      if (!samePostings(existing.postings, input.postings)) {
        throw new LedgerError(`Idempotency key ${input.idempotencyKey} reused with different postings`);
      }
      return existing;
    }
    validatePostings(input.postings);
    const seq = this.entries.length + 1;
    const entry: JournalEntry = deepFreeze({
      id: `je_${seq.toString().padStart(6, '0')}`,
      seq,
      idempotencyKey: input.idempotencyKey,
      at: input.at,
      description: input.description,
      reference: input.reference,
      postings: input.postings.map((p) => ({ account: { ...p.account }, amount: p.amount })),
      simulated: true as const,
    });
    this.entries.push(entry);
    this.byKey.set(entry.idempotencyKey, entry);
    return entry;
  }

  /** Reverses an entry with an opposite entry. An entry can be reversed only once. */
  reverse(entryId: string, at: string, reason: string): JournalEntry {
    const orig = this.entries.find((e) => e.id === entryId);
    if (!orig) throw new LedgerError(`Unknown entry ${entryId}`);
    if (orig.reverses) throw new LedgerError('Cannot reverse a reversal');
    if (this.reversed.has(entryId)) throw new LedgerError(`Entry ${entryId} already reversed`);
    const rev = this.post({
      idempotencyKey: `reversal:${entryId}`,
      at,
      description: `Contrepassation de ${entryId}: ${reason}`,
      reference: orig.reference,
      postings: orig.postings.map((p) => ({ account: p.account, amount: -p.amount })),
    });
    // attach the link (entry is frozen, so build a new frozen copy in place)
    const idx = this.entries.indexOf(rev);
    const linked = deepFreeze({ ...rev, reverses: entryId });
    this.entries[idx] = linked;
    this.byKey.set(linked.idempotencyKey, linked);
    this.reversed.add(entryId);
    return linked;
  }

  /** Signed balance (debits positive). */
  balance(account: AccountRef): bigint {
    const id = accountId(account);
    let total = 0n;
    for (const e of this.entries) for (const p of e.postings) if (accountId(p.account) === id) total += p.amount;
    return total;
  }

  /** Balance in the account's natural sign (liabilities/revenue shown positive when credited). */
  naturalBalance(account: AccountRef): bigint {
    const b = this.balance(account);
    const k = accountKind(account.type);
    return k === 'ASSET' || k === 'EXPENSE' ? b : -b;
  }

  /** Every balance, keyed by account id. */
  balances(): Map<string, { account: AccountRef; balance: bigint }> {
    const m = new Map<string, { account: AccountRef; balance: bigint }>();
    for (const e of this.entries) {
      for (const p of e.postings) {
        const id = accountId(p.account);
        const cur = m.get(id) ?? { account: p.account, balance: 0n };
        cur.balance += p.amount;
        m.set(id, cur);
      }
    }
    return m;
  }

  all(): readonly JournalEntry[] {
    return this.entries;
  }

  forReference(reference: string): JournalEntry[] {
    return this.entries.filter((e) => e.reference === reference);
  }

  /** Global integrity check: each entry balances per currency, so the trial balance is zero per currency. */
  trialBalance(): Map<CurrencyCode, bigint> {
    const t = new Map<CurrencyCode, bigint>();
    for (const e of this.entries) for (const p of e.postings) t.set(p.account.currency, (t.get(p.account.currency) ?? 0n) + p.amount);
    return t;
  }

  isBalanced(): boolean {
    for (const v of this.trialBalance().values()) if (v !== 0n) return false;
    return true;
  }
}

/** Shared validation used by every LedgerStore implementation. */
export function validatePostings(postings: readonly Posting[]): void {
  if (postings.length < 2) throw new LedgerError('An entry needs at least two postings');
  const perCurrency = new Map<CurrencyCode, bigint>();
  for (const p of postings) {
    if (typeof p.amount !== 'bigint') throw new LedgerError('Amounts must be bigint minor units');
    if (p.amount === 0n) throw new LedgerError('Zero postings are not allowed');
    perCurrency.set(p.account.currency, (perCurrency.get(p.account.currency) ?? 0n) + p.amount);
  }
  for (const [c, v] of perCurrency) if (v !== 0n) throw new LedgerError(`Unbalanced entry in ${c}: ${v}`);
}

export function samePostings(a: readonly Posting[], b: readonly Posting[]): boolean {
  if (a.length !== b.length) return false;
  return a.every((p, i) => {
    const q = b[i];
    return q !== undefined && accountId(p.account) === accountId(q.account) && p.amount === q.amount;
  });
}

function deepFreeze<T>(o: T): T {
  if (o && typeof o === 'object') {
    Object.freeze(o);
    for (const v of Object.values(o as object)) if (v && typeof v === 'object' && !Object.isFrozen(v)) deepFreeze(v);
  }
  return o;
}

/**
 * Async ledger contract, implemented in memory (InMemoryLedgerStore) and in PostgreSQL (apps/api PostgresLedger).
 * Same semantics everywhere: balanced per currency, idempotent by key, append-only, one reversal per entry.
 */
export interface LedgerStore {
  post(input: PostInput): Promise<JournalEntry>;
  reverse(entryId: string, at: string, reason: string): Promise<JournalEntry>;
  balance(account: AccountRef): Promise<bigint>;
  forReference(reference: string): Promise<JournalEntry[]>;
  trialBalance(): Promise<Map<CurrencyCode, bigint>>;
}

export class InMemoryLedgerStore implements LedgerStore {
  constructor(readonly ledger: Ledger = new Ledger()) {}
  async post(input: PostInput) { return this.ledger.post(input); }
  async reverse(entryId: string, at: string, reason: string) { return this.ledger.reverse(entryId, at, reason); }
  async balance(account: AccountRef) { return this.ledger.balance(account); }
  async forReference(reference: string) { return this.ledger.forReference(reference); }
  async trialBalance() { return this.ledger.trialBalance(); }
}
