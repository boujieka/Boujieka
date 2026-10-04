// Génère les icônes PNG de la PWA à partir des SVG de la marque.
// Usage : node brand/tools/render_icons.mjs   (nécessite Playwright + Chromium)
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ici = path.dirname(fileURLToPath(import.meta.url));
const logo = path.resolve(ici, '../logo');
const sortie = path.resolve(ici, '../../site/static/icons');
fs.mkdirSync(sortie, { recursive: true });
const svg = (f) => fs.readFileSync(path.join(logo, f), 'utf8');
const BLEU = '#1D3F8F';

// [fichier, taille, html]
const icones = [
  // « any » : icône arrondie, coins transparents
  ['icon-192.png', 192, svg('tasetygrid-icone.svg'), false],
  ['icon-512.png', 512, svg('tasetygrid-icone.svg'), false],
  // « maskable » et Apple : fond plein, symbole dans la zone sûre (80 %)
  ['maskable-512.png', 512, svg('tasetygrid-favicon.svg'), true],
  ['apple-touch-icon.png', 180, svg('tasetygrid-favicon.svg'), true],
];

const b = await chromium.launch();
const p = await b.newPage();
for (const [nom, t, contenu, plein] of icones) {
  const interieur = plein
    ? `<div style="width:${t}px;height:${t}px;background:${BLEU};display:grid;place-items:center">
         <div style="width:${t * 0.78}px;height:${t * 0.78}px">${contenu.replace('<svg ', '<svg width="100%" height="100%" ')}</div></div>`
    : `<div style="width:${t}px;height:${t}px">${contenu.replace('<svg ', '<svg width="100%" height="100%" ')}</div>`;
  await p.setViewportSize({ width: t, height: t });
  await p.setContent(`<html><body style="margin:0;background:transparent">${interieur}</body></html>`);
  await p.screenshot({ path: path.join(sortie, nom), omitBackground: !plein, clip: { x: 0, y: 0, width: t, height: t } });
  console.log('écrit', nom);
}
await b.close();
