import { defineConfig } from 'vitest/config';
import { fileURLToPath } from 'node:url';

const pkg = (name: string) => fileURLToPath(new URL(`./packages/${name}/src/index.ts`, import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      '@diasposwap/shared-types': pkg('shared-types'),
      '@diasposwap/ledger': pkg('ledger'),
      '@diasposwap/matching-engine': pkg('matching-engine'),
      '@diasposwap/compliance-engine': pkg('compliance-engine'),
      '@diasposwap/settlement-engine': pkg('settlement-engine'),
      '@diasposwap/liquidity': pkg('liquidity'),
    },
  },
  // legacy decorators for the NestJS API (explicit @Inject tokens are used, so metadata is not required)
  oxc: { decorator: { legacy: true, emitDecoratorMetadata: true } } as never,
  test: {
    include: ['packages/*/test/**/*.test.ts', 'apps/api/test/**/*.test.ts'],
    setupFiles: [],
  },
});
