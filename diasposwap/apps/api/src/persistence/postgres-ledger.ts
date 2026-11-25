import {
  type AccountRef, type AccountType, type JournalEntry, type LedgerStore, type PostInput,
  LedgerError, samePostings, validatePostings,
} from '@diasposwap/ledger';
import type { CurrencyCode } from '@diasposwap/shared-types';
import { Prisma, type PrismaClient } from '../generated/prisma/client';

/**
 * PostgreSQL implementation of LedgerStore.
 * The application validates first (clear errors); the database enforces the same rules again
 * (migration 20261125230000_ledger_integrity): balanced per currency at commit, append-only, no zero postings.
 */
type EntryRow = Prisma.LedgerEntryGetPayload<{ include: { postings: true } }>;

function toEntry(row: EntryRow): JournalEntry {
  return Object.freeze({
    id: row.id.toString(),
    seq: Number(row.id),
    idempotencyKey: row.idempotencyKey,
    at: row.at.toISOString(),
    description: row.description,
    reference: row.reference,
    postings: [...row.postings]
      .sort((a, b) => (a.id < b.id ? -1 : 1))
      .map((p) => Object.freeze({ account: { type: p.accountType as AccountType, currency: p.currency as CurrencyCode, scope: p.scope }, amount: p.amount })),
    ...(row.reversesId !== null ? { reverses: row.reversesId.toString() } : {}),
    simulated: true as const,
  });
}

const isUniqueViolation = (e: unknown) => e instanceof Prisma.PrismaClientKnownRequestError && e.code === 'P2002';

export class PostgresLedger implements LedgerStore {
  constructor(private readonly db: PrismaClient) {}

  async post(input: PostInput): Promise<JournalEntry> {
    return this.insert(input, null);
  }

  async reverse(entryId: string, at: string, reason: string): Promise<JournalEntry> {
    const id = parseId(entryId);
    const orig = await this.db.ledgerEntry.findUnique({ where: { id }, include: { postings: true, reversedBy: true } });
    if (!orig) throw new LedgerError(`Unknown entry ${entryId}`);
    if (orig.reversesId !== null) throw new LedgerError('Cannot reverse a reversal');
    if (orig.reversedBy) throw new LedgerError(`Entry ${entryId} already reversed`);
    const original = toEntry(orig);
    try {
      return await this.insert({
        idempotencyKey: `reversal:${entryId}`, at, reference: original.reference,
        description: `Contrepassation de ${entryId}: ${reason}`,
        postings: original.postings.map((p) => ({ account: p.account, amount: -p.amount })),
      }, id);
    } catch (e) {
      // a concurrent reversal won the UNIQUE("reversesId") race
      if (e instanceof LedgerError && /reused|already/.test(e.message)) throw new LedgerError(`Entry ${entryId} already reversed`);
      throw e;
    }
  }

  async balance(account: AccountRef): Promise<bigint> {
    const r = await this.db.ledgerPosting.aggregate({
      _sum: { amount: true },
      where: { accountType: account.type, currency: account.currency, scope: account.scope },
    });
    return r._sum.amount ?? 0n;
  }

  async forReference(reference: string): Promise<JournalEntry[]> {
    const rows = await this.db.ledgerEntry.findMany({ where: { reference }, include: { postings: true }, orderBy: { id: 'asc' } });
    return rows.map(toEntry);
  }

  async trialBalance(): Promise<Map<CurrencyCode, bigint>> {
    const rows = await this.db.ledgerPosting.groupBy({ by: ['currency'], _sum: { amount: true } });
    return new Map(rows.map((r) => [r.currency as CurrencyCode, r._sum.amount ?? 0n]));
  }

  private async insert(input: PostInput, reversesId: bigint | null): Promise<JournalEntry> {
    validatePostings(input.postings);
    const existing = await this.byKey(input.idempotencyKey);
    if (existing) return this.sameOrThrow(existing, input);
    try {
      const row = await this.db.$transaction(async (tx) => {
        const entry = await tx.ledgerEntry.create({
          data: { idempotencyKey: input.idempotencyKey, reference: input.reference, description: input.description, at: new Date(input.at || Date.now()), simulated: true, reversesId },
        });
        // one statement per posting keeps their order (ids ascend in insertion order)
        for (const p of input.postings) {
          await tx.ledgerPosting.create({ data: { entryId: entry.id, accountType: p.account.type, currency: p.account.currency, scope: p.account.scope, amount: p.amount } });
        }
        return tx.ledgerEntry.findUniqueOrThrow({ where: { id: entry.id }, include: { postings: true } });
      });
      return toEntry(row);
    } catch (e) {
      if (isUniqueViolation(e)) {
        // lost a race on the same idempotency key (or reversal): return the winner if it is the same posting set
        const winner = await this.byKey(input.idempotencyKey);
        if (winner) return this.sameOrThrow(winner, input);
        throw new LedgerError('Entry already reversed');
      }
      throw e;
    }
  }

  private async byKey(key: string): Promise<JournalEntry | null> {
    const row = await this.db.ledgerEntry.findUnique({ where: { idempotencyKey: key }, include: { postings: true } });
    return row ? toEntry(row) : null;
  }

  private sameOrThrow(existing: JournalEntry, input: PostInput): JournalEntry {
    if (!samePostings(existing.postings, input.postings)) {
      throw new LedgerError(`Idempotency key ${input.idempotencyKey} reused with different postings`);
    }
    return existing;
  }
}

function parseId(id: string): bigint {
  if (!/^\d+$/.test(id)) throw new LedgerError(`Unknown entry ${id}`);
  return BigInt(id);
}
