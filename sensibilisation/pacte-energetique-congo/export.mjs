// Exporte chaque page de la BD en PNG (format A4, 1240 x 1754 px) et l'album en PDF A4.
// Usage : node export.mjs   (nécessite Playwright et Chromium)
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { execSync } from 'node:child_process';

// Playwright local au projet, sinon installation globale
const { chromium } = await import('playwright').catch(() =>
  import(path.join(execSync('npm root -g').toString().trim(), 'playwright', 'index.mjs')));

const dir = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(dir, 'export');
mkdirSync(out, { recursive: true });
const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>${readFileSync(path.join(dir, 'index.html'), 'utf8')}</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1240, height: 1754 } });
const errors = [];
page.on('pageerror', e => errors.push(e.message));
await page.setContent(html, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
if (errors.length) { console.error(errors.join('\n')); process.exit(1); }

await page.addStyleTag({ content: 'body{padding:0!important;margin:0} .wrap{max-width:none!important;gap:0!important} #album{gap:0!important} header.intro, section.block{display:none!important} #album svg.page{width:1240px!important;box-shadow:none!important}' });
const ids = await page.$$eval('svg.page', els => els.map(e => e.id));
for (const id of ids) await page.locator(`#${id}`).screenshot({ path: path.join(out, `${id}.png`) });

await page.addStyleTag({ content: '@page{size:A4;margin:0} #album svg.page{width:210mm!important;height:297mm!important;break-after:page}' });
await page.emulateMedia({ media: 'print', colorScheme: 'light' });
await page.pdf({ path: path.join(out, 'le-courant-pour-tous-bd.pdf'), format: 'A4', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await browser.close();
console.log(`${ids.length} pages exportées dans ${out}`);
