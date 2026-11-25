import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import pg from 'pg';

/**
 * Creates a throwaway database, applies the real migration files in order, and drops it afterwards.
 * TEST_DATABASE_URL must point to a role allowed to CREATE DATABASE (any existing db, e.g. .../postgres).
 */
export const TEST_DATABASE_URL = process.env.TEST_DATABASE_URL;
const MIGRATIONS = fileURLToPath(new URL('../prisma/migrations', import.meta.url));

/** In CI a missing database is an error, never a silent skip. */
export function requireDatabaseInCi(): void {
  if (!TEST_DATABASE_URL && process.env.CI) throw new Error('TEST_DATABASE_URL is required in CI');
}

export async function createTestDatabase(): Promise<{ url: string; drop: () => Promise<void> }> {
  if (!TEST_DATABASE_URL) throw new Error('TEST_DATABASE_URL is not set');
  const name = `ds_test_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  const admin = new pg.Client({ connectionString: TEST_DATABASE_URL });
  await admin.connect();
  await admin.query(`CREATE DATABASE "${name}"`);
  await admin.end();
  const url = new URL(TEST_DATABASE_URL);
  url.pathname = `/${name}`;
  const client = new pg.Client({ connectionString: url.toString() });
  await client.connect();
  for (const dir of readdirSync(MIGRATIONS).filter((d) => /^\d+_/.test(d)).sort()) {
    await client.query(readFileSync(join(MIGRATIONS, dir, 'migration.sql'), 'utf8'));
  }
  await client.end();
  return {
    url: url.toString(),
    drop: async () => {
      const a = new pg.Client({ connectionString: TEST_DATABASE_URL });
      await a.connect();
      await a.query(`DROP DATABASE IF EXISTS "${name}" WITH (FORCE)`);
      await a.end();
    },
  };
}
