// Records the DiaspoSwap web build (simulation) with step markers for the demo video.
// Usage (from diasposwap/): node video/record-demo.cjs apps/mobile/dist <outDir>   -> <outDir>/capture.webm + marks.json
const { chromium } = require('playwright');
const http = require('http'); const fs = require('fs'); const path = require('path');
const [dist, outDir] = process.argv.slice(2);
const types = { '.js': 'application/javascript', '.html': 'text/html', '.css': 'text/css', '.png': 'image/png', '.ico': 'image/x-icon', '.json': 'application/json', '.ttf': 'font/ttf' };
const server = http.createServer((req, res) => {
  let p = path.join(dist, decodeURIComponent(req.url.split('?')[0]));
  if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) p = path.join(dist, 'index.html');
  res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
});
(async () => {
  await new Promise((r) => server.listen(8766, r));
  const browser = await chromium.launch();
  const t0 = Date.now();
  const ctx = await browser.newContext({ recordVideo: { dir: outDir, size: { width: 780, height: 1688 } }, viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, colorScheme: 'light', locale: 'fr-FR' });
  const page = await ctx.newPage(); page.setDefaultTimeout(30000);
  const marks = {}; const mark = (k) => { marks[k] = (Date.now() - t0) / 1000; };
  const hold = (ms) => page.waitForTimeout(ms);
  await page.goto('http://localhost:8766/'); await page.getByText('Continuer').waitFor(); await hold(500); mark('onboarding');
  await hold(2500); await page.getByText('Continuer').click(); await hold(1800); await page.getByText('Continuer').click(); await hold(1800);
  await page.getByTestId('start').click(); await page.getByTestId('pin').waitFor(); mark('login'); await hold(1500);
  await page.getByTestId('pin').pressSequentially('1234', { delay: 150 }); await hold(600);
  await page.getByTestId('login').click(); await page.getByTestId('send-money').waitFor(); mark('dashboard'); await hold(2500);
  await page.getByTestId('send-money').click(); await page.getByTestId('amount').waitFor(); mark('calculator'); await hold(1200);
  await page.getByTestId('amount').fill(''); await page.getByTestId('amount').pressSequentially('1000', { delay: 250 });
  await page.getByText('655 957', { exact: false }).first().waitFor(); mark('calc_filled'); await hold(6000);
  await page.getByTestId('review').click(); await page.getByTestId('pay').waitFor(); mark('confirm'); await hold(2500);
  await page.getByTestId('pay').click(); await page.getByTestId('order-state').filter({ hasText: 'QUEUED' }).waitFor(); mark('queued'); await hold(2500);
  await page.getByTestId('sim-counterparty').click(); mark('sim'); await hold(1500);
  await page.getByTestId('run-matching').click(); await page.getByTestId('order-state').filter({ hasText: 'SETTLEMENT_PENDING' }).waitFor(); mark('matched'); await hold(2500);
  await page.getByTestId('settle').click(); await page.getByTestId('order-state').filter({ hasText: 'SETTLED' }).waitFor(); mark('settled'); await hold(2500);
  await page.getByTestId('receipt').click(); await page.getByText('Document de simulation').waitFor(); mark('receipt'); await hold(2500);
  await page.goBack(); await page.goBack(); await page.getByRole('tab', { name: /Historique/ }).click(); await page.getByText(/ord_/).first().waitFor(); mark('history'); await hold(3000);
  mark('end');
  const v = page.video(); await ctx.close(); await browser.close(); server.close();
  fs.renameSync(await v.path(), path.join(outDir, 'capture.webm'));
  fs.writeFileSync(path.join(outDir, 'marks.json'), JSON.stringify(marks, null, 1));
  console.log(JSON.stringify(marks));
})().catch((e) => { console.log('FAILED', e.message); server.close(); process.exit(1); });
