const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { applyTheme } = require("/root/.claude/skills/synced/595554f7-3334-4cb8-90b6-40da4dcb6b84_e238fe12-8a4b-4490-8c46-5bf1323948af/pptx/scripts/apply_theme.js");
const OUT = process.argv[2];
const DIR = "/home/user/Boujieka/docs/recherche-or-cameroun/";

const THEME = {
  name: "Flux mineraux Cameroun",
  headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: "1C1A17", lt1: "FFFFFF", dk2: "4A3F35", lt2: "F1EEE8", accent1: "C9A227", accent2: "B85042", accent3: "2F6F73", accent4: "8C857B", accent5: "6B4F2A", accent6: "E3D08A", hlink: "2F6F73", folHlink: "6B4F2A" },
};
const H = THEME.colors;

// ---------- data
const csv = f => fs.readFileSync(DIR + f, "utf8").trim().split("\n").slice(1).map(l => l.split(","));
const rate = {}; for (const r of csv("valeurs_annuelles_or.csv")) rate[+r[0]] = +r[5];
const M = csv("donnees_miroir_or_tous_declarants.csv").filter(r => r[0] === "7108");
const YRS = []; for (let y = 2000; y <= 2025; y++) YRS.push(y);
const G = {}; YRS.forEach(y => G[y] = { kg: 0, usd: 0, eau: [0, 0], rwa: [0, 0], uga: [0, 0], aut: [0, 0] });
for (const r of M) {
  const y = +r[1], kg = +r[4] || 0, v = +r[5]; const g = G[y]; g.kg += kg; g.usd += v;
  const k = r[2] === "784" ? "eau" : r[2] === "646" ? "rwa" : r[2] === "800" ? "uga" : "aut"; g[k][0] += kg; g[k][1] += v;
}
const xaf = (usd, y) => usd * rate[y];
// Cameroon declared exports (UN Comtrade, reporter 120, flow X, HS 7108)
const CMR = { 2012: [184, 5390006], 2013: [214, 6850944], 2014: [78, 2359106], 2015: [10, 234967], 2016: [9, 202888], 2017: [5.02, 175399], 2018: [13, 519071], 2019: [82.4, 2708882], 2020: [5.32, 162247], 2021: [39.8, 783448], 2022: [3.45, 99108], 2023: [null, 674906] };
// Kimberley Process, Cameroon exports (ct, USD)
const KP = { 2013: [2420.88, 570357], 2014: [3600.15, 562923], 2015: [1723.29, 416871], 2016: [1807.41, 379040], 2017: [1294.63, 109001], 2018: [1261.91, 345784], 2019: [654.89, 83030], 2020: [788.14, 72428], 2021: [251.44, 62723], 2022: [421.76, 49339], 2023: [4840.36, 168871], 2024: [18002.56, 283887], 2025: [14646.99, 240244] };
const KPP = { 2013: 2721.94, 2014: 3718.16, 2015: 2244.61, 2016: 993.59, 2017: 1757.45, 2018: 1805.31, 2019: 1736.52, 2020: 2438.71, 2021: 2667.83, 2022: 2431.16, 2023: 3305.79, 2024: 11219.81, 2025: 15382.37 };
const PUB = { 2021: 52.81, 2022: 50.55, 2023: 161.79, 2024: 159.15, 2025: 153.20 };

// ---------- formatting
const nf = (x, d = 0) => x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d }).replace(/ /g, " ");
const musd = v => nf(v / 1e6, 1);           // M USD
const mdx = v => nf(v / 1e9, 1);            // Md FCFA
const t3 = kg => nf(kg / 1000, 1);

// ---------- deck
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Où va l'or du Cameroun ? Flux miniers 2000–2025";
pres.author = "Recherche Boujieka";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;
const FOOT = "Flux miniers du Cameroun 2000–2025 · statistiques douanières et sources publiques";
pres.defineSlideMaster({ title: "TITRE_SOMBRE", background: { color: C.text1 }, objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 11.7, h: 1.9, fontSize: 44, bold: true, color: C.background1, valign: "bottom", margin: 0 }, text: "" } },
  { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.1, w: 11.7, h: 1.4, fontSize: 20, color: C.accent6, valign: "top", margin: 0 }, text: "" } }] });
pres.defineSlideMaster({ title: "SECTION_SOMBRE", background: { color: C.text2 }, objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.6, w: 11.7, h: 1.3, fontSize: 40, bold: true, color: C.background1, valign: "middle", margin: 0 }, text: "" } },
  { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.0, w: 11.7, h: 1.0, fontSize: 18, color: C.accent6, valign: "top", margin: 0 }, text: "" } }],
  slideNumber: { x: 12.3, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: C.accent6, align: "right" } });
pres.defineSlideMaster({ title: "CONTENU", background: { color: C.background1 }, objects: [
  { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 30, bold: true, color: C.text1, valign: "middle", margin: 0 }, text: "" } },
  { text: { text: FOOT, options: { x: 0.6, y: 7.05, w: 10, h: 0.3, fontSize: 10, color: C.accent4, margin: 0 } } }],
  slideNumber: { x: 12.1, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: C.accent4, align: "right" } });

const sections = []; const section = t => { pres.addSection({ title: t }); sections.push(t); }; const cur = () => sections[sections.length - 1];
const content = t => { const s = pres.addSlide({ masterName: "CONTENU", sectionTitle: cur() }); s.addText(t, { placeholder: "title" }); return s; };
const divider = (t, b) => { const s = pres.addSlide({ masterName: "SECTION_SOMBRE", sectionTitle: cur() }); s.addText(t, { placeholder: "title" }); s.addText(b, { placeholder: "body" }); return s; };
const caption = (s, t) => s.addText(t, { x: 0.6, y: 6.6, w: 12.1, h: 0.35, fontSize: 10, italic: true, color: C.accent4, margin: 0, isTextBox: true, objectName: "Source" });
const card = (s, x, y, w, h, n) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: C.background2 }, line: { type: "none" }, objectName: n });
const tx = (s, t, o) => s.addText(t, Object.assign({ margin: 0, isTextBox: true, color: C.text1, valign: "top" }, o));
const HDR = cols => cols.map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 }, align: "center" } }));
const cell = (t, o = {}) => ({ text: t, options: Object.assign({ color: H.dk1 }, o) });
const tbl = (s, rows, o) => s.addTable(rows, Object.assign({ fontFace: THEME.bodyFontFace, fontSize: 14, border: { type: "solid", pt: 0.5, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle" }, o));
const chartBase = () => ({ catAxisLabelColor: H.dk2, valAxisLabelColor: H.dk2, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  dataLabelFontFace: "+mn-lt", dataLabelFontSize: 10, dataLabelColor: H.dk1, valGridLine: { color: "E2DDD4", size: 0.5 }, catGridLine: { style: "none" }, titleFontFace: "+mj-lt", titleColor: H.dk1, titleFontSize: 14, legendFontFace: "+mn-lt", legendFontSize: 11, legendColor: H.dk2 });
function kpi(s, x, y, w, h, big, l1, l2, color, name) {
  card(s, x, y, w, h, name);
  tx(s, big, { x: x + 0.25, y: y + 0.2, w: w - 0.5, h: 0.7, fontSize: 26, bold: true, color: color || C.accent5, fontFace: THEME.headFontFace });
  tx(s, l1, { x: x + 0.25, y: y + 0.9, w: w - 0.5, h: 0.7, fontSize: 14, bold: true, color: C.accent3 });
  tx(s, l2, { x: x + 0.25, y: y + 1.6, w: w - 0.5, h: h - 1.7, fontSize: 14 });
}

// totals
let T = { kg: 0, usd: 0, x: 0 }, E = { kg: 0, usd: 0, x: 0 };
YRS.forEach(y => { T.kg += G[y].kg; T.usd += G[y].usd; T.x += xaf(G[y].usd, y); E.kg += G[y].eau[0]; E.usd += G[y].eau[1]; E.x += xaf(G[y].eau[1], y); });
let CE = { kg: 0, usd: 0, x: 0 }; for (const y in CMR) { CE.kg += CMR[y][0] || 0; CE.usd += CMR[y][1]; CE.x += xaf(CMR[y][1], +y); }
let PU = 0, PX = 0; for (const y in PUB) { PX += PUB[y]; PU += PUB[y] * 1e9 / rate[y]; }

// ===== 1. Titre
section("Synthèse");
let s = pres.addSlide({ masterName: "TITRE_SOMBRE", sectionTitle: cur() });
s.addText("Où va l'or du Cameroun ?", { placeholder: "title" });
s.addText("Flux miniers déclarés par le Cameroun et par ses partenaires commerciaux, 2000–2025 : volumes et valeurs en dollars et en francs CFA", { placeholder: "body" });
tx(s, "Note d'analyse · données au 31 octobre 2026 · version 6", { x: 0.8, y: 6.5, w: 8, h: 0.4, fontSize: 14, color: C.accent4 });

// ===== 2. Synthèse chiffrée
s = content("Synthèse : l'essentiel en quatre chiffres");
kpi(s, 0.6, 1.5, 2.9, 3.6, t3(T.kg) + " t", musd(T.usd) + " M USD · " + mdx(T.x) + " Md FCFA", "Or déclaré à l'importation depuis le Cameroun par ses partenaires, 2000–2025", null, "KPI total");
kpi(s, 3.67, 1.5, 2.9, 3.6, t3(E.kg) + " t", musd(E.usd) + " M USD · " + mdx(E.x) + " Md FCFA", "dont Émirats arabes unis, 2004–2023 (80,3 % des volumes)", null, "KPI EAU");
kpi(s, 6.74, 1.5, 2.9, 3.6, nf(CE.kg) + " kg", musd(CE.usd) + " M USD · " + mdx(CE.x) + " Md FCFA", "Or déclaré à l'exportation par le Cameroun, 2012–2023", C.accent3, "KPI Cameroun");
kpi(s, 9.81, 1.5, 2.9, 3.6, nf(PX, 1) + " Md FCFA", "≈ " + nf(PU / 1e6, 0) + " M USD", "Manque à gagner fiscal 2021–2025 estimé par le ministère des Mines", C.accent2, "KPI fiscal");
tx(s, [{ text: "Constat principal : ", options: { bold: true, color: C.accent2 } }, { text: "sur 2012–2023, les partenaires du Cameroun déclarent avoir reçu de lui environ " + nf(Math.round([2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023].reduce((a, y) => a + G[y].kg, 0) / CE.kg / 10) * 10) + " fois plus d'or, en poids, que ce que le Cameroun déclare avoir exporté." }],
  { x: 0.6, y: 5.35, w: 12.1, h: 0.9, fontSize: 16 });
caption(s, "Sources : UN Comtrade (SH 7108) ; Banque mondiale (taux de change annuels) ; MINMIDT (juillet 2026). Précisions : annexes B1–B4 ; méthode : annexe C1.");

// ===== 3. Méthode
s = content("Méthode : comparer les deux déclarations d'un même flux");
const steps = [["Déclarations des partenaires", "Importations d'or (SH 7108) « en provenance du Cameroun » déclarées par 254 pays et territoires dans UN Comtrade"],
  ["Déclarations du Cameroun", "Exportations déclarées par le Cameroun (UN Comtrade, ITIE) et statistiques du Processus de Kimberley pour le diamant"],
  ["Valorisation", "Valeurs déclarées en dollars, converties en francs CFA au taux de change moyen de chaque année (Banque mondiale)"]];
steps.forEach((st, i) => {
  const x = 0.6 + i * 4.1; card(s, x, 1.6, 3.8, 3.2, "Étape " + (i + 1));
  s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: 1.85, w: 0.65, h: 0.65, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "Pastille " + (i + 1) });
  tx(s, String(i + 1), { x: x + 0.3, y: 1.85, w: 0.65, h: 0.65, fontSize: 20, bold: true, color: C.background1, align: "center", valign: "middle" });
  tx(s, st[0], { x: x + 1.1, y: 1.85, w: 2.5, h: 0.65, fontSize: 18, bold: true, valign: "middle" });
  tx(s, st[1], { x: x + 0.3, y: 2.75, w: 3.2, h: 1.9, fontSize: 15 });
});
card(s, 0.6, 5.05, 12.1, 1.3, "Périmètre");
tx(s, [{ text: "Périmètre : ", options: { bold: true } }, { text: "or 2000–2025, analyse sur la base Comtrade complète ; diamant 2013–2025, statistiques officielles du Processus de Kimberley ; cobalt, fer, manganèse et bauxite, revue documentaire des projets." }],
  { x: 0.9, y: 5.15, w: 11.5, h: 1.1, fontSize: 15, valign: "middle" });
caption(s, "Détails de l'extraction, contrôles et reproductibilité : annexe C1.");

// ===== Section or
section("L'or");
divider("L'or : " + t3(T.kg) + " tonnes déclarées à l'étranger", musd(T.usd) + " millions USD, soit " + mdx(T.x) + " milliards FCFA, sur 2000–2025");

// ===== 5. Valeur annuelle
s = content("Flux d'or déclarés : plus de 250 M USD par an depuis 2012");
s.addChart(pres.charts.BAR, [
  { name: "Valeur déclarée (M USD)", labels: YRS.map(String), values: YRS.map(y => y >= 2024 ? 0 : +(G[y].usd / 1e6).toFixed(1)) },
  { name: "Hors EAU, non publiés (M USD)", labels: YRS.map(String), values: YRS.map(y => y >= 2024 ? +(G[y].usd / 1e6).toFixed(1) : 0) }],
  { x: 0.6, y: 1.4, w: 8.4, h: 5.0, barDir: "col", barGrouping: "stacked", chartColors: [H.accent1, H.accent4], showLegend: true, legendPos: "b",
    showTitle: true, title: "Or déclaré « en provenance du Cameroun », valeur en millions USD", valAxisMinVal: 0, catAxisLabelRotate: -45, ...chartBase(), objectName: "Graphique valeur or" });
card(s, 9.3, 1.4, 3.4, 5.0, "Repères valeur");
const rp = [[2013, "2013"], [2018, "2018"], [2023, "2023 (record)"]];
tx(s, rp.flatMap(([y, l]) => [{ text: l, options: { bold: true, breakLine: true } },
  { text: t3(G[y].kg) + " t · " + musd(G[y].usd) + " M USD", options: { breakLine: true } },
  { text: mdx(xaf(G[y].usd, y)) + " Md FCFA", options: { color: C.accent5, breakLine: true } }, { text: " ", options: { breakLine: true } }]).concat([
  { text: "2024–2025", options: { bold: true, breakLine: true } }, { text: "Rwanda et Ouganda : " + musd(G[2024].usd + G[2025].usd) + " M USD" }]),
  { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 14 });
caption(s, "Source : UN Comtrade, SH 7108, valeurs CIF déclarées par les importateurs ; conversion au taux moyen annuel (Banque mondiale). Séries annuelles : annexe A1.");

// ===== 6. Destinations
s = content("Les Émirats arabes unis concentrent 80 % des volumes recensés");
const dests = [["Émirats arabes unis", "eau", "2004–2023"], ["Rwanda", "rwa", "2019–2025"], ["Ouganda", "uga", "2023–2025"], ["Autres pays (16)", "aut", "2001–2023"]];
const drow = dests.map(([n, k, p]) => { let kg = 0, u = 0, x = 0; YRS.forEach(y => { kg += G[y][k][0]; u += G[y][k][1]; x += xaf(G[y][k][1], y); }); return [n, p, nf(kg / 1000, 1), musd(u), mdx(x), nf(kg / T.kg * 100, 1) + " %"]; });
drow.push(["Total", "2000–2025", nf(T.kg / 1000, 1), musd(T.usd), mdx(T.x), "100 %"]);
tbl(s, [HDR(["Pays déclarant", "Période", "Tonnes", "M USD", "Md FCFA", "Part"]), ...drow.map((r, i) => r.map((c, j) => cell(c, { bold: i === 4 || j === 0, align: j >= 2 ? "right" : "left" })))],
  { x: 0.6, y: 1.5, w: 12.1, colW: [3.3, 1.9, 1.6, 1.8, 1.9, 1.6], rowH: 0.62, fontSize: 16, objectName: "Tableau destinations" });
tx(s, "Les Émirats arabes unis ont déclaré 4,8 milliards USD d'or importé du Cameroun en vingt ans ; le Rwanda et l'Ouganda apparaissent comme destinations à partir de 2019 et 2023.", { x: 0.6, y: 5.5, w: 12.1, h: 0.9, fontSize: 16 });
caption(s, "Source : UN Comtrade, SH 7108, poids nets ; Banque mondiale. Liste complète des déclarants : fichier de données du dépôt (annexe C1).");

// ===== 7. Cameroun-EAU
s = content("Cameroun–Émirats : vingt ans de flux d'or déclarés");
const uy = YRS.filter(y => y >= 2004 && y <= 2023);
s.addChart(pres.charts.BAR, [{ name: "EAU (t)", labels: uy.map(String), values: uy.map(y => +(G[y].eau[0] / 1000).toFixed(2)) }], {
  x: 0.6, y: 1.4, w: 6.9, h: 5.0, barDir: "col", chartColors: [H.accent5], showLegend: false, showTitle: true,
  title: "Importations déclarées par les EAU en provenance du Cameroun (t)", valAxisMinVal: 0, catAxisLabelRotate: -45, ...chartBase(), objectName: "Graphique EAU" });
const per = [[2004, 2009], [2010, 2014], [2015, 2019], [2020, 2023]];
const prow = per.map(([a, b]) => { let k = 0, u = 0, x = 0; for (let y = a; y <= b; y++) { k += G[y].eau[0]; u += G[y].eau[1]; x += xaf(G[y].eau[1], y); } return [a + "–" + b, nf(k / 1000, 1), musd(u), mdx(x)]; });
prow.push(["2004–2023", nf(E.kg / 1000, 1), musd(E.usd), mdx(E.x)]);
tbl(s, [HDR(["Période", "t", "M USD", "Md FCFA"]), ...prow.map((r, i) => r.map((c, j) => cell(c, { bold: i === 4, align: j ? "right" : "left" })))],
  { x: 7.8, y: 1.5, w: 4.9, colW: [1.5, 0.9, 1.25, 1.25], rowH: 0.55, objectName: "Tableau EAU périodes" });
caption(s, "Source : UN Comtrade, déclarant 784 (EAU), partenaire 120 (Cameroun), SH 7108 ; série corroborée par INTERPOL (2021) pour 2010–2018.");

// ===== 8. Ecart officiel vs miroir
s = content("Exporté selon le Cameroun, reçu selon ses partenaires");
const ey = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023];
const erows = ey.map(y => [String(y), CMR[y][0] == null ? "n. d." : nf(CMR[y][0], CMR[y][0] < 10 ? 1 : 0), nf(CMR[y][1] / 1e6, 2), nf(G[y].kg, 0), musd(G[y].usd), mdx(xaf(G[y].usd, y))]);
erows.push(["2012–2023", nf(CE.kg, 0), nf(CE.usd / 1e6, 1), nf(ey.reduce((a, y) => a + G[y].kg, 0), 0), musd(ey.reduce((a, y) => a + G[y].usd, 0)), mdx(ey.reduce((a, y) => a + xaf(G[y].usd, y), 0))]);
tbl(s, [[{ text: "", options: { fill: { color: H.lt1 } } }, { text: "Déclaré par le Cameroun", options: { colspan: 2, bold: true, color: H.lt1, fill: { color: H.accent3 }, align: "center" } }, { text: "Déclaré par les partenaires", options: { colspan: 3, bold: true, color: H.lt1, fill: { color: H.accent5 }, align: "center" } }],
  HDR(["Année", "kg", "M USD", "kg", "M USD", "Md FCFA"]), ...erows.map((r, i) => r.map((c, j) => cell(c, { bold: i === 12, align: j ? "right" : "left" })))],
  { x: 0.6, y: 1.35, w: 12.1, colW: [2.0, 1.9, 1.9, 2.1, 2.1, 2.1], rowH: 0.34, fontSize: 13, objectName: "Tableau écart" });
caption(s, "Source : UN Comtrade, SH 7108 : exportations déclarées par le Cameroun (flux X) et importations des partenaires (flux M), poids nets ; conversion Banque mondiale.");

// ===== 9. Deux cas documentés
s = content("Deux années documentées par des sources indépendantes");
const cases = [
  ["2017 · INTERPOL", "4 kg", "déclarés par le Cameroun vers les EAU", nf(10.9, 1) + " t", "déclarées par les EAU depuis le Cameroun, soit " + musd(G[2017].eau[1]) + " M USD et " + mdx(xaf(G[2017].eau[1], 2017)) + " Md FCFA"],
  ["2023 · WITS / UN Comtrade", "20 kg", "déclarés par le Cameroun vers les EAU", nf(14.048, 3) + " t", "déclarées par les EAU depuis le Cameroun, soit " + musd(G[2023].eau[1]) + " M USD et " + mdx(xaf(G[2023].eau[1], 2023)) + " Md FCFA"]];
cases.forEach((c, i) => {
  const x = 0.6 + i * 6.15; card(s, x, 1.5, 5.95, 4.8, "Cas " + c[0]);
  tx(s, c[0], { x: x + 0.3, y: 1.7, w: 5.3, h: 0.5, fontSize: 18, bold: true });
  tx(s, c[1], { x: x + 0.3, y: 2.35, w: 2.3, h: 0.8, fontSize: 34, bold: true, color: C.accent3, fontFace: THEME.headFontFace });
  tx(s, c[2], { x: x + 0.3, y: 3.15, w: 2.4, h: 1.0, fontSize: 14 });
  tx(s, c[3], { x: x + 2.95, y: 2.35, w: 2.8, h: 0.8, fontSize: 34, bold: true, color: C.accent5, fontFace: THEME.headFontFace });
  tx(s, c[4], { x: x + 2.95, y: 3.15, w: 2.75, h: 1.6, fontSize: 14 });
  tx(s, i === 0 ? "Rapport des volumes : environ 2 700 pour 1" : "Rapport des volumes : environ 700 pour 1", { x: x + 0.3, y: 5.3, w: 5.3, h: 0.6, fontSize: 16, bold: true, color: C.accent2 });
});
caption(s, "Sources : INTERPOL, Illegal Gold Mining in Central Africa (2021) ; WITS/UN Comtrade 2023 ; valeurs : UN Comtrade et Banque mondiale.");

// ===== 10. 2023-2025 par partenaire
s = content("2023–2025 : le Rwanda et l'Ouganda s'ajoutent aux Émirats");
const pr = []; [2023, 2024, 2025].forEach(y => [["Émirats arabes unis", "eau"], ["Rwanda", "rwa"], ["Ouganda", "uga"]].forEach(([n, k]) => {
  if (y >= 2024 && k === "eau") { pr.push([String(y), n, "non publié", "–", "–"]); return; }
  pr.push([String(y), n, nf(G[y][k][0], 0), musd(G[y][k][1]), mdx(xaf(G[y][k][1], y))]);
}));
tbl(s, [HDR(["Année", "Pays déclarant", "kg", "M USD", "Md FCFA"]), ...pr.map(r => r.map((c, j) => cell(c, { align: j >= 2 ? "right" : "left" })))],
  { x: 0.6, y: 1.45, w: 8.0, colW: [1.2, 2.6, 1.4, 1.4, 1.4], rowH: 0.48, objectName: "Tableau partenaires" });
kpi(s, 8.9, 1.45, 3.8, 2.3, musd(G[2024].rwa[1] + G[2025].rwa[1]) + " M USD", "Rwanda 2024–2025", t3(G[2024].rwa[0] + G[2025].rwa[0]) + " t · " + mdx(xaf(G[2024].rwa[1], 2024) + xaf(G[2025].rwa[1], 2025)) + " Md FCFA", null, "KPI Rwanda");
kpi(s, 8.9, 3.95, 3.8, 2.3, musd(G[2024].uga[1] + G[2025].uga[1]) + " M USD", "Ouganda 2024–2025", t3(G[2024].uga[0] + G[2025].uga[0]) + " t · " + mdx(xaf(G[2024].uga[1], 2024) + xaf(G[2025].uga[1], 2025)) + " Md FCFA", null, "KPI Ouganda");
caption(s, "Source : UN Comtrade, SH 7108, poids nets ; Banque mondiale. Statut des données 2024–2025 des EAU : annexe B1.");

// ===== 11. Fiscalité
s = content("Manque à gagner fiscal : les estimations officielles");
const fy = [2021, 2022, 2023, 2024, 2025];
s.addChart(pres.charts.BAR, [{ name: "MINMIDT (Md FCFA)", labels: fy.map(String), values: fy.map(y => PUB[y]) }], {
  x: 0.6, y: 1.4, w: 6.6, h: 5.0, barDir: "col", chartColors: [H.accent2], showLegend: false, showTitle: true, title: "Recettes fiscales et douanières non perçues sur l'or, Md FCFA (MINMIDT)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", valAxisMinVal: 0, ...chartBase(), objectName: "Graphique fiscal" });
const frows = fy.map(y => [String(y), nf(PUB[y], 2), nf(PUB[y] * 1e3 / rate[y], 1)]);
frows.push(["2021–2025", nf(PX, 2), nf(PU / 1e6, 1)]);
tbl(s, [HDR(["Année", "Md FCFA", "M USD"]), ...frows.map((r, i) => r.map((c, j) => cell(c, { bold: i === 5, align: j ? "right" : "left" })))],
  { x: 7.5, y: 1.5, w: 5.2, colW: [1.8, 1.7, 1.7], rowH: 0.5, objectName: "Tableau fiscal" });
tx(s, "L'ITIE estime de son côté à 165 Md FCFA (≈ " + nf(165e9 / rate[2023] / 1e6, 0) + " M USD) les pertes potentielles de la seule année 2023.", { x: 7.5, y: 5.2, w: 5.2, h: 1.1, fontSize: 14 });
caption(s, "Sources : MINMIDT, tableau 2021–2025 (juillet 2026, via la presse) ; ITIE, avril 2026. Conversion en USD au taux moyen annuel. Réconciliation des montants : annexe B2.");

// ===== Section autres minerais
section("Autres minerais");
divider("Diamant, cobalt, fer, manganèse, bauxite", "Des flux officiels faibles, des projets à fort enjeu financier");

// ===== 13. Diamant
s = content("Diamant : 51 700 carats exportés officiellement depuis 2013");
const ky = Object.keys(KP).map(Number);
let KC = 0, KU = 0, KX = 0; ky.forEach(y => { KC += KP[y][0]; KU += KP[y][1]; KX += xaf(KP[y][1], y); });
s.addChart(pres.charts.BAR, [{ name: "Valeur (milliers USD)", labels: ky.map(String), values: ky.map(y => +(KP[y][1] / 1e3).toFixed(0)) }], {
  x: 0.6, y: 1.4, w: 7.4, h: 5.0, barDir: "col", chartColors: [H.accent3], showLegend: false, showTitle: true, title: "Exportations officielles de diamants bruts, valeur en milliers USD",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0", valAxisMinVal: 0, ...chartBase(), objectName: "Graphique diamant" });
kpi(s, 8.3, 1.4, 4.4, 2.35, nf(KC, 0) + " ct", nf(KU / 1e6, 2) + " M USD · " + nf(KX / 1e9, 2) + " Md FCFA", "Exportations certifiées 2013–2025", C.accent3, "KPI diamant");
kpi(s, 8.3, 4.0, 4.4, 2.35, nf(KP[2024][0], 0) + " ct", nf(KP[2024][1] / 1e3, 0) + " k USD · " + nf(xaf(KP[2024][1], 2024) / 1e6, 0) + " M FCFA", "2024 : record de volume, à " + nf(KP[2024][1] / KP[2024][0], 1) + " USD par carat", C.accent3, "KPI diamant 2024");
caption(s, "Source : Processus de Kimberley, statistiques du Cameroun (exportations certifiées) ; conversion Banque mondiale. Tableau annuel : annexe A3.");

// ===== 14. Diamant contexte
s = content("Diamant : un enjeu régional de traçabilité");
const dc = [["140 000 ct", "≈ 24 M USD · ≈ " + nf(24e6 * rate[2014] / 1e9, 1) + " Md FCFA", "sortis clandestinement de République centrafricaine entre mai 2013 et octobre 2014, tous itinéraires confondus (Groupe d'experts de l'ONU)"],
  ["4 523 ct", "certificat Kimberley camerounais falsifié", "présenté à l'étranger en 2016, selon Partnership Africa Canada / IMPACT"],
  ["≈ 5 000 ct/an", "≈ " + nf(5000 * 113.9 / 1e3, 0) + " k USD par an au prix moyen centrafricain", "produits à la frontière RCA hors du Processus de Kimberley, selon le secrétariat national"]];
dc.forEach((d, i) => {
  const x = 0.6 + i * 4.1; card(s, x, 1.5, 3.8, 4.8, "Diamant contexte " + (i + 1));
  tx(s, d[0], { x: x + 0.3, y: 1.75, w: 3.2, h: 0.8, fontSize: 30, bold: true, color: C.accent3, fontFace: THEME.headFontFace });
  tx(s, d[1], { x: x + 0.3, y: 2.6, w: 3.2, h: 0.9, fontSize: 15, bold: true, color: C.accent5 });
  tx(s, d[2], { x: x + 0.3, y: 3.6, w: 3.2, h: 2.5, fontSize: 15 });
});
caption(s, "Sources : ONU S/2014/762 ; PAC/IMPACT, From Conflict to Illicit (2016) ; Business in Cameroon (2019). Prix RCA : Processus de Kimberley.");

// ===== 15. Projets
s = content("Autres minerais : des projets à fort enjeu financier");
const pj = [["Cobalt et manganèse · Nkamouna", "617 M USD", "≈ " + mdx(617e6 * rate[2011]) + " Md FCFA d'investissement prévu (étude 2011) ; permis de Geovic retiré par le décret n° 2025/040 du 12 février 2025"],
  ["Fer · Mbalam", "616 M USD", "≈ " + mdx(616e6 * rate[2025]) + " Md FCFA : sentence arbitrale CCI du 26/07/2026 en faveur de Sundance contre l'État"],
  ["Fer · Lobé", "22,9 Md FCFA/an", "≈ " + nf(22.9e9 / rate[2025] / 1e6, 1) + " M USD de recettes annuelles attendues pour l'État (Sinosteel, première exportation prévue en 2027)"],
  ["Bauxite · Minim-Martap", "9,5–16,6 Md FCFA/an", "≈ " + nf(9.5e9 / rate[2025] / 1e6, 0) + "–" + nf(16.6e9 / rate[2025] / 1e6, 0) + " M USD de recettes attendues pour 3 Mt/an ; réserves JORC de 144 Mt à 51,2 % d'alumine"]];
pj.forEach((p, i) => {
  const x = 0.6 + (i % 2) * 6.15, y = 1.45 + Math.floor(i / 2) * 2.5; card(s, x, y, 5.95, 2.3, "Projet " + (i + 1));
  tx(s, p[0], { x: x + 0.3, y: y + 0.18, w: 5.4, h: 0.45, fontSize: 16, bold: true, color: C.accent3 });
  tx(s, p[1], { x: x + 0.3, y: y + 0.65, w: 5.4, h: 0.65, fontSize: 26, bold: true, color: C.accent5, fontFace: THEME.headFontFace });
  tx(s, p[2], { x: x + 0.3, y: y + 1.35, w: 5.4, h: 0.85, fontSize: 14 });
});
caption(s, "Sources : Geovic (étude 2011) ; Présidence, décret 2025/040 ; Sundance et Reuters (27/07/2026) ; MINMIDT ; LeFisk ; Canyon (25/06/2026). Conversion : taux moyen de l'année.");

// ===== 16. Comparatif
s = content("Six minerais : synthèse des flux et des montants");
const cp = [["Or", "≈ 0,6 t (2012–2023)", t3(T.kg) + " t (2000–2025)", musd(T.usd) + " M USD · " + mdx(T.x) + " Md FCFA"],
  ["Diamant", nf(KC, 0) + " ct (2013–2025)", "Volumes marginaux", nf(KU / 1e6, 2) + " M USD · " + nf(KX / 1e9, 2) + " Md FCFA"],
  ["Cobalt", "Aucune exportation recensée", "≈ 3 000 USD (Chine, 2023)", "Projet Nkamouna : 617 M USD prévus"],
  ["Fer", "Aucune exportation recensée", "Non significatif", "Arbitrage Mbalam : 616 M USD"],
  ["Manganèse", "Aucune exportation recensée", "Non recensé", "Coproduit de Nkamouna"],
  ["Bauxite", "Aucune exportation recensée", "Non recensé", "Recettes attendues : 9,5–16,6 Md FCFA/an"]];
tbl(s, [HDR(["Minerai", "Exportations déclarées", "Importations des partenaires", "Valeurs en jeu"]), ...cp.map((r, i) => r.map((c, j) => cell(c, { bold: j === 0, fill: { color: i === 0 ? "F6EED3" : H.lt1 } })))],
  { x: 0.6, y: 1.45, w: 12.1, colW: [1.7, 3.1, 3.2, 4.1], rowH: 0.7, fontSize: 15, objectName: "Tableau comparatif" });
caption(s, "Sources : UN Comtrade ; Processus de Kimberley ; documents de projets. Couverture des recherches par minerai : annexe B4.");

// ===== 17. Conclusions
section("Conclusions");
s = pres.addSlide({ masterName: "TITRE_SOMBRE", sectionTitle: cur() });
tx(s, "Conclusions et recommandations", { x: 0.8, y: 0.6, w: 11.7, h: 0.9, fontSize: 36, bold: true, color: C.background1, fontFace: THEME.headFontFace });
const concl = ["Sur 2012–2023, les partenaires déclarent " + nf(ey.reduce((a, y) => a + G[y].kg, 0) / 1000, 1) + " t d'or importé du Cameroun (" + nf(ey.reduce((a, y) => a + G[y].usd, 0) / 1e9, 2) + " Md USD), contre " + nf(CE.kg, 0) + " kg déclarés à l'exportation",
  "Les Émirats arabes unis en sont la destination principale, avec " + nf(E.usd / 1e9, 2) + " Md USD (" + nf(E.x / 1e9, 0) + " Md FCFA) sur 2004–2023",
  "Le ministère des Mines estime à " + nf(PX, 1) + " Md FCFA le manque à gagner fiscal sur 2021–2025"];
const recs = ["Rapprocher statistiques douanières, production déclarée et collectes de la Sonamines",
  "Obtenir les statistiques émiriennes 2024–2025 et coopérer avec le Rwanda et l'Ouganda sur l'origine de l'or",
  "Renforcer la traçabilité à l'exportation (or et diamant) et le contrôle des comptoirs"];
tx(s, "Constats", { x: 0.8, y: 1.7, w: 5.6, h: 0.5, fontSize: 20, bold: true, color: C.accent1 });
tx(s, "Recommandations", { x: 6.9, y: 1.7, w: 5.6, h: 0.5, fontSize: 20, bold: true, color: C.accent1 });
[concl, recs].forEach((L, c) => L.forEach((t, i) => {
  const x = c ? 6.9 : 0.8, y = 2.4 + i * 1.45;
  s.addShape(pres.shapes.OVAL, { x, y, w: 0.55, h: 0.55, fill: { color: c ? C.accent3 : C.accent1 }, line: { type: "none" }, objectName: "Pastille c" + c + i });
  tx(s, String(i + 1), { x, y, w: 0.55, h: 0.55, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle" });
  tx(s, t, { x: x + 0.75, y: y - 0.05, w: 4.85, h: 1.3, fontSize: 15, color: C.background1 });
}));

// ===== Annexes A : données
section("Annexes A · Données");
divider("Annexes A · Données détaillées", "Séries annuelles en volume, en dollars et en francs CFA");
[[2000, 2012], [2013, 2025]].forEach(([a, b], k) => {
  s = content("Annexe A" + (k + 1) + " · Or déclaré par les partenaires, " + a + "–" + b);
  const rr = []; for (let y = a; y <= b; y++) {
    const g = G[y]; rr.push([String(y) + (y >= 2024 ? " *" : ""), nf(g.kg, 0), y >= 2024 ? "n. p." : nf(g.eau[0], 0), nf(g.rwa[0] + g.uga[0], 0), nf(g.aut[0], 0), musd(g.usd), mdx(xaf(g.usd, y)), nf(rate[y], 1)]);
  }
  tbl(s, [HDR(["Année", "Total (kg)", "EAU (kg)", "Rwanda + Ouganda (kg)", "Autres (kg)", "M USD", "Md FCFA", "FCFA / USD"]), ...rr.map(r => r.map((c, j) => cell(c, { align: j ? "right" : "left" })))],
    { x: 0.6, y: 1.35, w: 12.1, colW: [1.2, 1.5, 1.5, 2.2, 1.4, 1.4, 1.4, 1.5], rowH: 0.36, objectName: "Annexe or " + (k + 1) });
  caption(s, k ? "* EAU non publiés (n. p.) : totaux partiels. Source : UN Comtrade, SH 7108, flux M, partenaire 120, poids nets, valeurs CIF ; taux : Banque mondiale PA.NUS.FCRF." : "Source : UN Comtrade, SH 7108, flux M, partenaire 120 (Cameroun), poids nets, valeurs CIF ; taux de change : Banque mondiale PA.NUS.FCRF.");
});
s = content("Annexe A3 · Diamants : production et exportations");
const kr = ky.map(y => [String(y), nf(KPP[y], 0), nf(KP[y][0], 0), nf(KP[y][1], 0), nf(KP[y][1] / KP[y][0], 1), nf(xaf(KP[y][1], y) / 1e6, 1)]);
kr.push(["2013–2025", nf(ky.reduce((a, y) => a + KPP[y], 0), 0), nf(KC, 0), nf(KU, 0), nf(KU / KC, 1), nf(KX / 1e6, 1)]);
tbl(s, [HDR(["Année", "Production (ct)", "Exportations (ct)", "Exportations (USD)", "USD par carat", "M FCFA"]), ...kr.map((r, i) => r.map((c, j) => cell(c, { bold: i === 13, align: j ? "right" : "left" })))],
  { x: 0.6, y: 1.35, w: 12.1, colW: [1.7, 2.1, 2.1, 2.3, 1.8, 2.1], rowH: 0.34, fontSize: 13, objectName: "Annexe diamant" });
caption(s, "Source : Processus de Kimberley, statistiques du Cameroun (page pays) ; conversion au taux moyen annuel (Banque mondiale). Divergences entre publications KP : annexe B3.");

// ===== Annexes B : points à clarifier
section("Annexes B · Points à clarifier");
divider("Annexes B · Points à clarifier", "Limites des données, divergences entre sources et hypothèses à vérifier");
const clar = (title, items, src) => {
  s = content(title);
  items.forEach((it, i) => {
    const y = 1.4 + i * (5.1 / items.length);
    const h = 5.1 / items.length - 0.15;
    card(s, 0.6, y, 12.1, h, "Point " + (i + 1));
    tx(s, it[0], { x: 0.85, y: y + 0.1, w: 3.1, h: h - 0.2, fontSize: 15, bold: true, color: C.accent5, valign: "middle" });
    tx(s, it[1], { x: 4.1, y: y + 0.1, w: 8.4, h: h - 0.2, fontSize: 14, valign: "middle" });
  });
  caption(s, src);
};
clar("Annexe B1 · Couverture et qualité des données sur l'or", [
  ["Données des EAU 2024–2025", "Non publiées dans UN Comtrade : les données 2024 ont été mises en ligne puis retirées « pour vérification » (SWISSAID, 04/11/2025). Les totaux 2024–2025 sont partiels. La Sonamines évoque ≈ 12,2 t enregistrées à Dubaï en 2024, chiffre non vérifié."],
  ["Poids net, quantité, arrondis", "Totaux en poids net. Le champ « quantité » de WITS diffère surtout pour l'Ouganda (1 117 contre 1 145 kg en 2023) : en quantité, 2023 totalise 18 227 kg (dont Portugal et Pérou, 1 kg chacun). En 2024–2025, la somme des composantes arrondies dépasse le total de 1 kg (arrondis)."],
  ["Valeurs déclarées", "Valeurs CIF déclarées par les importateurs. Elles s'écartent du cours mondial de −11 à −15 % en 2016–2020 et en 2024–2025 (or doré non affiné ? sous-évaluation ?), et de ±8 % les autres années."],
  ["Exportations du Cameroun", "Comtrade et ITIE divergent : 2021, 40 kg contre 73 kg ; 2022, 3,5 kg contre 47,9 kg ; 2023, poids non renseigné dans Comtrade (22,3 kg selon l'ITIE)."]],
  "Sources : UN Comtrade ; SWISSAID ; Sonamines ; ITIE ; Banque mondiale (Pink Sheet).");
clar("Annexe B2 · Estimations fiscales à réconcilier", [
  ["Trois montants publiés", "Gouvernement : 577,51 Md FCFA sur 2021–2025 (série annuelle relayée par Business in Cameroon et Sikafinance) ; index de la page MINMIDT du 24/07/2026 : 557 Md. ITIE : 165 Md ; période ambiguë (2023 selon le contexte du rapport, « annuelle » selon la lecture de l'article ITIE ; le MINMIDT donne 161,79 Md pour 2023)."],
  ["Valeur et recette", "La valeur de l'or non déclaré n'est pas une recette perdue : il faut établir la part d'origine camerounaise, le régime applicable (artisanal ou semi-mécanisé), l'assiette et les montants déjà acquittés."],
  ["Régime fiscal", "ISML de 25 % (semi-mécanisé, depuis 2017) ; droit de sortie de 10 % (2020) puis 5 % FOB (2023) ; taxe ad valorem de 3 % ou 5 % avant 2016 selon les sources (contradiction non résolue)."],
  ["Calcul indépendant", "Nos scénarios (164 à 835 Md FCFA sur 2000–2025) supposent que tout l'or est camerounais et taxable : ce sont des ordres de grandeur, pas des pertes établies."]],
  "Sources : MINMIDT ; ITIE ; codes miniers 2016 et 2023 ; lois de finances 2020 et 2023 ; calculs de l'auteur (dossier docs/recherche-or-cameroun/PERTES_FISCALES.md).");
clar("Annexe B3 · Origine des flux et diamant", [
  ["Provenance ou origine", "Le pays « en provenance de » déclaré par l'importateur n'établit pas le lieu d'extraction : une partie de l'or et des diamants peut venir de RCA ou du Tchad et transiter par le Cameroun."],
  ["Écart et fraude", "Contrebande, sous-déclaration, transport en bagage à main ou erreurs de codification : les statistiques ne permettent pas de les distinguer."],
  ["Rwanda et Ouganda", "Leur rôle éventuel de réexportation vers les EAU n'est pas démontré ; à vérifier par leurs exportations vers les EAU, les raffineries et les pays d'origine déclarés."],
  ["Diamant, sources KP", "Exportations supérieures à la production déclarée en 2016, 2023 et 2024 (bilan des stocks à établir). Publications KP divergentes en 2016, 2020 et 2024. Les 140 000 ct de l'ONU concernent toute la RCA, pas le seul corridor camerounais."]],
  "Sources : INTERPOL (2021) ; ONU S/2014/762 ; Processus de Kimberley (résumés globaux et page pays).");
clar("Annexe B4 · Couverture des autres minerais", [
  ["Méthode", "Cobalt, fer, manganèse et bauxite : revue documentaire uniquement. UN Comtrade n'a pas été interrogé pour ces codes SH (2605, 2601, 2602, 2606) : l'absence de flux n'est pas démontrée."],
  ["Cobalt et manganèse", "Décret n° 2025/040 du 12/02/2025 (site de la Présidence) : il retire le permis n° 33 de Geovic mais ne renseigne ni tonnages ni exportations ; une extraction douanière dédiée reste nécessaire."],
  ["Fer", "Démarrage des exportations de Mbalam annoncé en 2026 sans confirmation officielle ; recours éventuels contre la sentence CCI non documentés."],
  ["Bauxite", "Canyon visait en juin 2026 un minage d'essai au T3 et un premier envoi au T4 2026 (≈ 35 000 t humides/mois) ; selon la presse, cet objectif a été retiré en août 2026. Aucune expédition confirmée."]],
  "Sources : USGS ; BGS ; Présidence de la République ; Sundance Resources ; Canyon Resources ; presse spécialisée.");

// ===== Annexes C : méthode et sources
section("Annexes C · Méthode et sources");
s = content("Annexe C1 · Méthode et reproductibilité");
const meta = [["Requêtes", "UN Comtrade, API publique preview : C/A/HS, partenaire 120, flux M, SH 7108, 7112, 7113 ; 2000–2025 ; extraction du 31/10/2026"],
  ["Déclarants", "254 pays et territoires interrogés, groupes régionaux exclus ; 19 déclarent des importations d'or (SH 7108) non nulles"],
  ["Contrôles", "390 requêtes annuelles, relances après délai ; aucune réponse tronquée ; doublons éliminés (code SH × année × déclarant)"],
  ["Conversions", "Taux USD/XAF : Banque mondiale PA.NUS.FCRF (moyenne annuelle) ; cours de l'or : Pink Sheet de la Banque mondiale"],
  ["Données", "Dépôt boujieka/Boujieka, dossier docs/ : fichiers CSV par déclarant et par année, rapports par minerai, script de génération"]];
meta.forEach((m, i) => { const y = 1.4 + i * 1.0; card(s, 0.6, y, 12.1, 0.88, "Méta " + i);
  tx(s, m[0], { x: 0.85, y: y + 0.08, w: 2.3, h: 0.72, fontSize: 15, bold: true, color: C.accent5, valign: "middle" });
  tx(s, m[1], { x: 3.2, y: y + 0.08, w: 9.3, h: 0.72, fontSize: 14, valign: "middle" }); });
caption(s, "Les montants en FCFA sont convertis au taux moyen de l'année de chaque flux ; les cumuls additionnent ces montants annuels.");
s = content("Annexe C2 · Sources primaires");
const srcs = [["UN Comtrade / WITS", "comtradeapi.un.org · wits.worldbank.org : SH 7108, partenaire Cameroun, 2000–2025"],
  ["INTERPOL (2021)", "Illegal Gold Mining in Central Africa · interpol.int/content/download/16493"],
  ["ITIE / EITI", "« Cameroon's gold gap » · eiti.org/impact-story/cameroons-gold-gap-how-eiti-data-driving-reforms"],
  ["MINMIDT", "Tableau des exploitations d'or 2021–2025 · minmidt.cm (24/07/2026)"],
  ["Processus de Kimberley", "kimberleyprocess.com/participants/cameroon · résumés statistiques annuels"],
  ["ONU", "Groupe d'experts sur la RCA, S/2014/762 (29/10/2014)"],
  ["SWISSAID (2025)", "« United Arab Emirates: More Than Ever a Hub for Conflict Gold » (04/11/2025)"],
  ["Projets", "prc.cm, décret 2025/040 (12/02/2025) · Reuters (27/07/2026), sentence Sundance · GlobeNewswire, Canyon (26/06/2026)"],
  ["Banque mondiale", "api.worldbank.org (PA.NUS.FCRF) · Pink Sheet, CMO-Historical-Data-Annual.xlsx"]];
tbl(s, [HDR(["Source", "Référence"]), ...srcs.map(r => [cell(r[0], { bold: true }), cell(r[1])])], { x: 0.6, y: 1.4, w: 12.1, colW: [3.0, 9.1], rowH: 0.47, objectName: "Sources" });
caption(s, "Liste complète des URL dans les rapports par minerai du dépôt (docs/recherche-*-cameroun/RAPPORT.md).");

(async () => { await pres.writeFile({ fileName: OUT }); await applyTheme(OUT, THEME); console.log("written", OUT); })();
