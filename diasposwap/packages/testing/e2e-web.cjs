// Usage: node packages/testing/e2e-web.cjs apps/mobile/dist <screenshot-dir> [light|dark]
// Requires Playwright + Chromium available to Node (not a project dependency).
// Drives the exported web build through the France -> Cameroon vertical flow.
const { chromium } = require('playwright');
const http = require('http');
const fs = require('fs');
const path = require('path');

const [dist, outDir, scheme = 'light'] = process.argv.slice(2);
const types = { '.js': 'application/javascript', '.html': 'text/html', '.css': 'text/css', '.png': 'image/png', '.ico': 'image/x-icon', '.json': 'application/json', '.ttf': 'font/ttf' };
const server = http.createServer((req, res) => {
  let p = path.join(dist, decodeURIComponent(req.url.split('?')[0]));
  if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) p = path.join(dist, 'index.html');
  res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});

(async () => {
  await new Promise((r) => server.listen(8765, r));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, colorScheme: scheme, locale: 'fr-FR' });
  const errors = [];
  page.on('pageerror', (e) => errors.push(`pageerror: ${e.message}`));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(`console: ${m.text()}`); });
  const shot = async (name) => page.screenshot({ path: `${outDir}/${scheme}-${name}.png`, fullPage: true });
  const step = async (label, fn) => { process.stdout.write(`- ${label} ... `); await fn(); console.log('ok'); };

  await step('open app', async () => { await page.goto('http://localhost:8765/'); await page.getByText('Continuer').waitFor({ timeout: 30000 }); });
  await shot('01-onboarding');
  await step('onboarding', async () => { await page.getByText('Continuer').click(); await page.getByText('Continuer').click(); await page.getByTestId('start').click(); });
  await step('login as Amina (France)', async () => { await page.getByTestId('pin').fill('1234'); await shot('02-login'); await page.getByTestId('login').click(); await page.getByTestId('send-money').waitFor(); });
  await shot('03-dashboard');
  await step('new transfer 1000 EUR to Cameroon', async () => {
    await page.getByTestId('send-money').click();
    await page.getByTestId('amount').fill('1000');
    await page.getByText('655 957', { exact: false }).first().waitFor();
  });
  await shot('04-calculator');
  await step('review + confirm', async () => { await page.getByTestId('review').click(); await page.getByTestId('pay').waitFor(); await shot('05-confirm'); await page.getByTestId('pay').click(); });
  await step('order queued', async () => { await page.getByTestId('order-state').filter({ hasText: 'QUEUED' }).waitFor(); });
  await shot('06-queued');
  await step('simulate reciprocal order + run matching', async () => {
    await page.getByTestId('sim-counterparty').click();
    await page.getByTestId('run-matching').click();
    await page.getByTestId('order-state').filter({ hasText: 'SETTLEMENT_PENDING' }).waitFor();
  });
  await shot('07-matched');
  await step('confirm simulated local payouts', async () => { await page.getByTestId('settle').click(); await page.getByTestId('order-state').filter({ hasText: 'SETTLED' }).waitFor(); });
  await shot('08-settled');
  await step('receipt', async () => { await page.getByTestId('receipt').click(); await page.getByText('Document de simulation').waitFor(); });
  await shot('09-receipt');
  await step('history', async () => { await page.goBack(); await page.goBack(); await page.getByRole('tab', { name: /Historique/ }).click(); await page.getByText(/ord_/).first().waitFor(); });
  await shot('10-history');

  console.log(errors.length ? `ERRORS:\n${errors.join('\n')}` : 'no page/console errors');
  await browser.close();
  server.close();
  process.exit(errors.length ? 2 : 0);
})().catch(async (e) => { console.log(`\nFAILED: ${e.message}`); server.close(); process.exit(1); });
