import { SwapSimulator, seedDemo } from '@diasposwap/settlement-engine';

export const SIMULATOR = Symbol('SIMULATOR');
export const CONFIG = Symbol('CONFIG');

export interface ApiConfig {
  /** Admin API keys -> role. Loaded from env; never hard-code real secrets. */
  adminKeys: Record<string, 'ops' | 'compliance'>;
  webhookSecret: string;
  seedDemo: boolean;
}

export function loadConfig(env: NodeJS.ProcessEnv = process.env): ApiConfig {
  const adminKeys: ApiConfig['adminKeys'] = {};
  for (const pair of (env.DIASPOSWAP_ADMIN_KEYS ?? '').split(',').filter(Boolean)) {
    const [key, role] = pair.split(':');
    if (key && (role === 'ops' || role === 'compliance')) adminKeys[key] = role;
  }
  return {
    adminKeys,
    webhookSecret: env.DIASPOSWAP_WEBHOOK_SECRET ?? 'dev-only-webhook-secret',
    seedDemo: env.DIASPOSWAP_SEED_DEMO === 'true',
  };
}

export function createSimulator(cfg: ApiConfig, now?: () => Date): SwapSimulator {
  const sim = new SwapSimulator({ webhookSecret: cfg.webhookSecret, ...(now ? { now } : {}) });
  if (cfg.seedDemo) seedDemo(sim, { seed: 42 });
  return sim;
}
