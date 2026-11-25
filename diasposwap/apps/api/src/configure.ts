import type { INestApplication } from '@nestjs/common';

/** Shared HTTP hardening, applied identically in production bootstrap and in tests. */
export function configureApp(app: INestApplication): INestApplication {
  const http = app.getHttpAdapter().getInstance() as { disable?: (k: string) => void };
  http.disable?.('x-powered-by');
  app.use((_req: unknown, res: { setHeader: (k: string, v: string) => void }, next: () => void) => {
    res.setHeader('X-DiaspoSwap-Mode', 'SIMULATION');
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('Referrer-Policy', 'no-referrer');
    next();
  });
  return app;
}
