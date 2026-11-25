import { defineConfig } from 'prisma/config';

// DATABASE_URL is read from the environment (never committed). See ../../.env.example.
// `prisma generate` does not need a database, so a missing URL only fails commands that connect.
export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: { path: 'prisma/migrations' },
  datasource: { url: process.env.DATABASE_URL ?? 'postgresql://DATABASE_URL-is-not-set' },
});
