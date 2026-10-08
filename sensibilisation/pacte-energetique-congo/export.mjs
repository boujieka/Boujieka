// Exporte chaque planche en PNG (1080 px) et l'album complet en PDF.
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
const page = await browser.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
await page.setContent(html, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

// PNG : chaque planche seule, 1080 x 1080
const n = await page.locator('figure.planche').count();
await page.addStyleTag({ content: 'body{padding:0!important;margin:0} .wrap{max-width:none!important;gap:0!important} figure.planche{gap:0} figcaption, header.intro, section.block{display:none!important} figure.planche svg{width:1080px!important;border-radius:0!important;box-shadow:none!important}' });
for (let i = 0; i < n; i++) {
  await page.locator(`#planche-${i} svg`).screenshot({ path: path.join(out, `planche-${String(i).padStart(2, '0')}.png`) });
}

// PDF : une planche par page A4 avec sa note, puis questions et sources
const pdf = await browser.newPage();
await pdf.setContent(html, { waitUntil: 'networkidle' });
await pdf.evaluate(() => document.fonts.ready);
await pdf.addStyleTag({ content: '@page{size:A4;margin:12mm} body{padding:0!important;font-size:13px} .wrap{max-width:none!important} figure.planche{break-after:page} figure.planche svg{box-shadow:none!important} section.block{break-inside:avoid}' });
await pdf.emulateMedia({ media: 'print', colorScheme: 'light' });
await pdf.pdf({ path: path.join(out, 'pacte-energetique-congo-bd.pdf'), format: 'A4', printBackground: true });
await browser.close();
console.log(`${n} planches exportées dans ${out}`);
