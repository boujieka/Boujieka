import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import pg from 'pg';
import { type LedgerStore, InMemoryLedgerStore, LedgerError } from '@diasposwap/ledger';
import { PostgresLedger } from '../src/persistence/postgres-ledger';
import { createPrisma } from '../src/persistence/prisma';
import { TEST_DATABASE_URL, createTestDatabase, requireDatabaseInCi } from './pg-test-db';

requireDatabaseInCi();

const A = { type: 'COLLECTION', currency: 'EUR', scope: 'FR' } as const;
const L = { type: 'CUSTOMER_FUNDS', currency: 'EUR', scope: 'FR:o1' } as const;
const X = { type: 'COLLECTION', currency: 'XAF', scope: 'CM' } as const;
const XL = { type: 'CUSTOMER_FUNDS', currency: 'XAF', scope: 'CM:o2' } as const;
const at = '2026-11-25T10:00:00.000Z';
const entry = (key: string, amount: bigint, reference = 'r') => ({ idempotencyKey: key, at, description: 'd', reference, postings: [{ account: A, amount }, { account: L, amount: -amount }] });

type Ctx = { store: LedgerStore; cleanup: () => Promise<void>; url?: string };
const factories: [string, () => Promise<Ctx>][] = [
  ['in-memory', async () => ({ store: new InMemoryLedgerStore(), cleanup: async () => {} })],
];
if (TEST_DATABASE_URL) {
  factories.push(['postgres', async () => {
    const db = await createTestDatabase();
    const prisma = createPrisma(db.url);
    return { store: new PostgresLedger(prisma), url: db.url, cleanup: async () => { await prisma.$disconnect(); await db.drop(); } };
  }]);
} else {
  console.warn('TEST_DATABASE_URL not set: PostgreSQL ledger tests are not run locally');
}

describe.each(factories)('LedgerStore contract: %s', (_name, make) => {
  let ctx: Ctx;
  beforeEach(async () => { ctx = await make(); });
  afterEach(async () => { await ctx.cleanup(); });

  it('posts a balanced entry and computes balances', async () => {
    const e = await ctx.store.post(entry('k1', 100050n));
    expect(e.postings.map((p) => p.amount)).toEqual([100050n, -100050n]);
    expect(await ctx.store.balance(A)).toBe(100050n);
    expect(await ctx.store.balance(L)).toBe(-100050n);
  });

  it('keeps currencies separate in one entry (two balanced legs)', async () => {
    await ctx.store.post({ idempotencyKey: 'k', at, description: 'd', reference: 'r', postings: [
      { account: A, amount: 100000n }, { account: L, amount: -100000n }, { account: X, amount: 655957n }, { account: XL, amount: -655957n },
    ] });
    const tb = await ctx.store.trialBalance();
    expect(tb.get('EUR')).toBe(0n);
    expect(tb.get('XAF')).toBe(0n);
  });

  it('rejects unbalanced, zero and single-posting entries', async () => {
    await expect(ctx.store.post({ ...entry('u', 1n), postings: [{ account: A, amount: 100n }, { account: L, amount: -99n }] })).rejects.toThrow(LedgerError);
    await expect(ctx.store.post({ ...entry('c', 1n), postings: [{ account: A, amount: 100n }, { account: X, amount: -100n }] })).rejects.toThrow(LedgerError);
    await expect(ctx.store.post({ ...entry('z', 1n), postings: [{ account: A, amount: 0n }, { account: L, amount: 0n }] })).rejects.toThrow(LedgerError);
    await expect(ctx.store.post({ ...entry('s', 1n), postings: [{ account: A, amount: 0n }] })).rejects.toThrow(LedgerError);
    expect((await ctx.store.trialBalance()).size).toBe(0);
  });

  it('is idempotent on the key and refuses a key reused with other postings', async () => {
    const e1 = await ctx.store.post(entry('k1', 500n));
    const e2 = await ctx.store.post(entry('k1', 500n));
    expect(e2.id).toBe(e1.id);
    await expect(ctx.store.post(entry('k1', 501n))).rejects.toThrow(/reused/);
    expect(await ctx.store.balance(A)).toBe(500n);
  });

  it('corrects by reversal, only once, and never reverses a reversal', async () => {
    const e = await ctx.store.post(entry('k1', 700n, 'ord_1'));
    const rev = await ctx.store.reverse(e.id, at, 'test');
    expect(rev.reverses).toBe(e.id);
    expect(rev.postings.map((p) => p.amount)).toEqual([-700n, 700n]);
    expect(await ctx.store.balance(A)).toBe(0n);
    expect((await ctx.store.forReference('ord_1')).map((x) => x.id)).toEqual([e.id, rev.id]);
    await expect(ctx.store.reverse(e.id, at, 'again')).rejects.toThrow(/already reversed/);
    await expect(ctx.store.reverse(rev.id, at, 'rev of rev')).rejects.toThrow(/reversal/);
    await expect(ctx.store.reverse('999999', at, 'unknown')).rejects.toThrow(/Unknown/);
  });

  it('concurrent posts with the same idempotency key create exactly one entry', async () => {
    const results = await Promise.all(Array.from({ length: 8 }, () => ctx.store.post(entry('race', 300n))));
    expect(new Set(results.map((r) => r.id)).size).toBe(1);
    expect(await ctx.store.balance(A)).toBe(300n);
  });
});

describe.runIf(!!TEST_DATABASE_URL)('PostgreSQL enforces ledger rules even when bypassing the application', () => {
  let db: Awaited<ReturnType<typeof createTestDatabase>>;
  let c: pg.Client;
  beforeEach(async () => {
    db = await createTestDatabase();
    c = new pg.Client({ connectionString: db.url });
    await c.connect();
  });
  afterEach(async () => { await c.end(); await db.drop(); });

  const insertEntry = async (key: string) =>
    (await c.query(`INSERT INTO "LedgerEntry" ("idempotencyKey","reference","description") VALUES ($1,'r','d') RETURNING id`, [key])).rows[0].id as string;
  const insertPosting = (entryId: string, cur: string, amount: number) =>
    c.query(`INSERT INTO "LedgerPosting" ("entryId","accountType","currency","scope","amount") VALUES ($1,'COLLECTION',$2,'FR',$3)`, [entryId, cur, amount]);

  async function commitBalanced(key: string) {
    await c.query('BEGIN');
    const id = await insertEntry(key);
    await insertPosting(id, 'EUR', 100);
    await insertPosting(id, 'EUR', -100);
    await c.query('COMMIT');
    return id;
  }

  it('rejects an unbalanced entry at COMMIT', async () => {
    await c.query('BEGIN');
    const id = await insertEntry('u');
    await insertPosting(id, 'EUR', 100);
    await insertPosting(id, 'EUR', -99);
    await expect(c.query('COMMIT')).rejects.toThrow(/unbalanced/);
  });

  it('rejects an entry unbalanced in one currency even if the grand total is zero', async () => {
    await c.query('BEGIN');
    const id = await insertEntry('x');
    await insertPosting(id, 'EUR', 100);
    await insertPosting(id, 'XAF', -100);
    await expect(c.query('COMMIT')).rejects.toThrow(/unbalanced/);
  });

  it('rejects an entry without postings and a zero posting', async () => {
    await c.query('BEGIN');
    await insertEntry('empty');
    await expect(c.query('COMMIT')).rejects.toThrow(/no postings/);
    await c.query('BEGIN');
    const id = await insertEntry('zero');
    await expect(insertPosting(id, 'EUR', 0)).rejects.toThrow(/nonzero/);
    await c.query('ROLLBACK');
  });

  it('refuses UPDATE, DELETE and TRUNCATE on committed history', async () => {
    const id = await commitBalanced('ok');
    await expect(c.query(`UPDATE "LedgerPosting" SET amount = 1 WHERE "entryId" = $1`, [id])).rejects.toThrow(/append-only/);
    await expect(c.query(`UPDATE "LedgerEntry" SET description = 'x' WHERE id = $1`, [id])).rejects.toThrow(/append-only/);
    await expect(c.query(`DELETE FROM "LedgerPosting" WHERE "entryId" = $1`, [id])).rejects.toThrow(/append-only/);
    await expect(c.query(`DELETE FROM "LedgerEntry" WHERE id = $1`, [id])).rejects.toThrow(/append-only/);
    await expect(c.query(`TRUNCATE "LedgerPosting", "LedgerEntry"`)).rejects.toThrow(/append-only/);
  });

  it('refuses adding postings to an entry committed earlier, even balanced ones', async () => {
    const id = await commitBalanced('old');
    await c.query('BEGIN');
    await expect(insertPosting(id, 'EUR', 50)).rejects.toThrow(/transaction that created it/);
    await c.query('ROLLBACK');
  });
});
