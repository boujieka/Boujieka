const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { applyTheme } = require("/root/.claude/skills/synced/595554f7-3334-4cb8-90b6-40da4dcb6b84_e238fe12-8a4b-4490-8c46-5bf1323948af/pptx/scripts/apply_theme.js");

const OUT = process.argv[2];
const CSV = "/home/user/Boujieka/docs/recherche-or-cameroun/tableau_annuel_consolide.csv";

const THEME = {
  name: "Flux mineraux Cameroun",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1C1A17", lt1: "FFFFFF", dk2: "4A3F35", lt2: "F1EEE8",
    accent1: "C9A227", accent2: "B85042", accent3: "2F6F73",
    accent4: "8C857B", accent5: "6B4F2A", accent6: "E3D08A",
    hlink: "2F6F73", folHlink: "6B4F2A",
  },
};
const H = THEME.colors;

// ---- data
const rows = fs.readFileSync(CSV, "utf8").trim().split("\n").slice(1).map(l => l.split(","));
const data = {};
for (const r of rows) data[+r[0]] = { kg: +r[1], usd: +r[2], xaf: +r[3], ecart: r[4] === "" ? null : +r[4], lo: +r[6], hi: +r[7] };
const M = fs.readFileSync("/home/user/Boujieka/docs/recherche-or-cameroun/donnees_miroir_or_tous_declarants.csv", "utf8").trim().split("\n").slice(1).map(l => l.split(",")).filter(r => r[0] === "7108");
const decl = {};
for (const r of M) { const y = +r[1]; decl[y] = decl[y] || { eau: 0, rwa: 0, uga: 0, aut: 0 }; const kg = +r[4] || 0; if (r[2] === "784") decl[y].eau += kg; else if (r[2] === "646") decl[y].rwa += kg; else if (r[2] === "800") decl[y].uga += kg; else decl[y].aut += kg; }
const years = Object.keys(data).map(Number).sort((a, b) => a - b);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "Flux minéraux du Cameroun 2000–2025";
pres.author = "Recherche Boujieka";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const FOOT = "Flux minéraux du Cameroun · 2000–2025 · données miroir et sources publiques";

pres.defineSlideMaster({
  title: "TITRE_SOMBRE",
  background: { color: C.text1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 11.7, h: 1.9, fontSize: 44, bold: true, color: C.background1, valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.1, w: 11.7, h: 1.4, fontSize: 20, color: C.accent6, valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "SECTION_SOMBRE",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.6, w: 11.7, h: 1.3, fontSize: 40, bold: true, color: C.background1, valign: "middle", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.0, w: 11.7, h: 1.0, fontSize: 18, color: C.accent6, valign: "top", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});
pres.defineSlideMaster({
  title: "CONTENU",
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 32, bold: true, color: C.text1, valign: "middle", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: 0.6, y: 7.05, w: 10, h: 0.3, fontSize: 10, color: C.accent4, margin: 0 } } },
  ],
  slideNumber: { x: 12.1, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: C.accent4, align: "right" },
});

const sections = [];
function section(t) { pres.addSection({ title: t }); sections.push(t); }
const cur = () => sections[sections.length - 1];
function content(title) {
  const s = pres.addSlide({ masterName: "CONTENU", sectionTitle: cur() });
  s.addText(title, { placeholder: "title" });
  return s;
}
function caption(s, t) {
  s.addText(t, { x: 0.6, y: 6.6, w: 12.1, h: 0.35, fontSize: 10, italic: true, color: C.accent4, margin: 0, isTextBox: true, objectName: "Source" });
}
function circleNum(s, n, x, y, d, fill) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill || C.accent1 }, line: { type: "none" }, objectName: "Pastille " + n });
  s.addText(String(n), { x, y, w: d, h: d, fontSize: d > 0.6 ? 20 : 14, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
}
function card(s, x, y, w, h, name) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.08, fill: { color: C.background2 }, line: { type: "none" }, objectName: name });
}
const fr = (x, d = 1) => x.toLocaleString("fr-FR", { minimumFractionDigits: d, maximumFractionDigits: d });
const chartBase = () => ({
  catAxisLabelColor: H.dk2, valAxisLabelColor: H.dk2, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 11, valAxisLabelFontSize: 11, dataLabelFontFace: "+mn-lt", dataLabelFontSize: 10, dataLabelColor: H.dk1,
  valGridLine: { color: "E2DDD4", size: 0.5 }, catGridLine: { style: "none" }, titleFontFace: "+mj-lt", titleColor: H.dk1, titleFontSize: 14,
  legendFontFace: "+mn-lt", legendFontSize: 11, legendColor: H.dk2,
});

// ===== 1. Titre
section("Introduction");
let s = pres.addSlide({ masterName: "TITRE_SOMBRE", sectionTitle: cur() });
s.addText("Où va l'or du Cameroun ?", { placeholder: "title" });
s.addText("Flux miniers déclarés et réels, 2000–2025 : or, diamant, cobalt, fer, manganèse, bauxite", { placeholder: "body" });
s.addText("Recherche documentaire · version 2 révisée après audit · données au 31 octobre 2026", { x: 0.8, y: 6.5, w: 8, h: 0.4, fontSize: 14, color: C.accent4, margin: 0, isTextBox: true });
s.addNotes("Présentation des résultats : analyse miroir UN Comtrade (tous déclarants) pour l'or, recherches documentaires pour les cinq autres minerais.");

// ===== 2. L'essentiel
s = content("L'essentiel : l'or pèse presque tout");
const stats = [
  ["138,5 t", "d'or brut (SH 7108) déclarées par les partenaires comme venant du Cameroun, 2000–2025 ; 2024–2025 partiels (sans les EAU)"],
  ["6,58 Md USD", "de valeur déclarée, soit ≈ 3 744 Md FCFA (taux Banque mondiale)"],
  ["577,5 Md FCFA", "de manque à gagner 2021–2025 estimé par le ministère des Mines : chiffre publié, non vérifié de façon indépendante"],
];
stats.forEach((st, i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.8, 3.3, "Chiffre clé " + (i + 1));
  s.addText(st[0], { x: x + 0.3, y: 1.9, w: 3.2, h: 1.2, fontSize: 32, bold: true, color: i === 2 ? C.accent2 : C.accent5, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
  s.addText(st[1], { x: x + 0.3, y: 3.15, w: 3.2, h: 1.5, fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true });
});
s.addText([
  { text: "À retenir : ", options: { bold: true, color: C.accent2 } },
  { text: "le Cameroun déclare quelques kilos d'or exportés par an quand ses partenaires en déclarent des tonnes. Diamant, cobalt, fer, manganèse et bauxite ne présentent pas d'écart comparable : flux faibles ou inexistants." },
], { x: 0.6, y: 5.2, w: 12.1, h: 1.1, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
caption(s, "Sources : UN Comtrade (SH 7108, partenaire Cameroun, 254 déclarants, agrégats régionaux exclus) ; Banque mondiale ; MINMIDT via Sikafinance (07/2026). Détail ligne à ligne : annexes A1–A3.");

// ===== 3. Méthode
s = content("Méthode : comparer ce qui part et ce qui arrive");
const steps = [
  ["Ce qui arrive", "Importations « en provenance du Cameroun » déclarées par 254 pays dans UN Comtrade (données miroir)"],
  ["Ce qui part", "Exportations déclarées par le Cameroun lui-même (Comtrade, ITIE, douanes, Processus de Kimberley)"],
  ["L'écart, en coûts", "Valeur en USD et en FCFA, comparaison au cours mondial, application du régime fiscal de chaque période"],
];
steps.forEach((st, i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.8, 2.9, "Étape " + (i + 1));
  circleNum(s, i + 1, x + 0.3, 1.85, 0.7);
  s.addText(st[0], { x: x + 1.15, y: 1.85, w: 2.5, h: 0.7, fontSize: 20, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  s.addText(st[1], { x: x + 0.3, y: 2.75, w: 3.2, h: 1.6, fontSize: 15, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  if (i < 2) s.addShape(pres.shapes.CHEVRON, { x: x + 3.86, y: 2.9, w: 0.18, h: 0.32, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "Flèche " + (i + 1) });
});
card(s, 0.6, 4.8, 12.1, 1.6, "Sources");
s.addText([
  { text: "Sources mobilisées : ", options: { bold: true } },
  { text: "UN Comtrade, Banque mondiale (taux de change, cours de l'or), ITIE Cameroun, MINMIDT, Sonamines, Processus de Kimberley, USGS, Panel d'experts de l'ONU, presse spécialisée." , options: { breakLine: true } },
  { text: "Limite : ", options: { bold: true, color: C.accent2 } },
  { text: "seul l'or a pu être analysé avec la base Comtrade complète ; les autres minerais reposent sur des extraits de recherche web." },
], { x: 0.9, y: 4.95, w: 11.5, h: 1.35, fontSize: 15, color: C.text1, valign: "middle", margin: 0, isTextBox: true });

// ===== 4. Section or
section("L'or");
s = pres.addSlide({ masterName: "SECTION_SOMBRE", sectionTitle: cur() });
s.addText("L'or : 138 tonnes déclarées à l'étranger", { placeholder: "title" });
s.addText("Graphiques : or brut SH 7108 uniquement. Déchets (SH 7112) et bijouterie (SH 7113) sont traités à part et ne sont pas additionnés", { placeholder: "body" });

// ===== 5. Volumes annuels
s = content("Les volumes explosent après 2009 et culminent en 2023");
const yrs = years.filter(y => y >= 2000);
s.addChart(pres.charts.BAR, [
  { name: "Séries complètes", labels: yrs.map(String), values: yrs.map(y => y >= 2024 ? 0 : +(data[y].kg / 1000).toFixed(1)) },
  { name: "Partiel : EAU non publiés", labels: yrs.map(String), values: yrs.map(y => y >= 2024 ? +(data[y].kg / 1000).toFixed(1) : 0) },
], {
  x: 0.6, y: 1.4, w: 8.4, h: 5.0, barDir: "col", barGrouping: "stacked", chartColors: [H.accent1, H.accent4], showLegend: true, legendPos: "b",
  showTitle: true, title: "Or brut (SH 7108) déclaré « en provenance du Cameroun », en tonnes",
  showValue: false, valAxisMinVal: 0, catAxisLabelRotate: -45, ...chartBase(), objectName: "Graphique volumes or",
});
card(s, 9.3, 1.4, 3.4, 5.0, "Commentaire volumes");
s.addText([
  { text: "2000–2008", options: { bold: true, breakLine: true } },
  { text: "Moins de 0,4 t par an", options: { breakLine: true } },
  { text: "2013–2019", options: { bold: true, breakLine: true } },
  { text: "≈ 10 à 11,7 t par an, presque tout vers les EAU", options: { breakLine: true } },
  { text: "2023", options: { bold: true, breakLine: true } },
  { text: "Record : 18,3 t, 1,15 Md USD", options: { breakLine: true } },
  { text: "2024–2025", options: { bold: true, color: C.accent2, breakLine: true } },
  { text: "Partiels : données des EAU non publiées (retirées de Comtrade selon SWISSAID). Ce ne sont pas des totaux." },
], { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 14, color: C.text1, valign: "top", margin: 0, paraSpaceAfter: 4, isTextBox: true });
caption(s, "Source : UN Comtrade, extrait le 31/10/2026. Somme des barres arrondies : 138,2 t ; total exact : 138,5 t. Sonamines : ≈ 12,2 t à Dubaï en 2024, non vérifié.");

// ===== 6. Destinations
s = content("EAU : 80,3 % des volumes recensés (2024–2025 incomplets)");
const dest = [["Émirats arabes unis", 111.3], ["Rwanda", 16.0], ["Ouganda", 7.7], ["Allemagne", 1.9], ["États-Unis", 0.55], ["Belgique", 0.42], ["Suisse", 0.31], ["Corée du Sud", 0.22]].reverse();
s.addChart(pres.charts.BAR, [{ name: "Cumul 2000–2025 (t)", labels: dest.map(d => d[0]), values: dest.map(d => d[1]) }], {
  x: 0.6, y: 1.4, w: 7.6, h: 5.0, barDir: "bar", chartColors: [H.accent5], showLegend: false,
  showTitle: true, title: "Or déclaré reçu du Cameroun, cumul 2000–2025 (tonnes)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", ...chartBase(), objectName: "Graphique destinations",
});
const facts6 = [
  ["111,3 t", "EAU, 2004–2023 (4,81 Md USD) ; série confirmée par Interpol pour 2010–2018"],
  ["16,0 t", "Rwanda, 2019–2025 : nouveau relais régional"],
  ["7,7 t", "Ouganda, 2023–2025"],
];
facts6.forEach((f, i) => {
  const y = 1.5 + i * 1.6;
  card(s, 8.5, y, 4.2, 1.4, "Fait destination " + (i + 1));
  s.addText(f[0], { x: 8.75, y: y + 0.15, w: 3.8, h: 0.6, fontSize: 26, bold: true, color: C.accent5, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
  s.addText(f[1], { x: 8.75, y: y + 0.75, w: 3.8, h: 0.55, fontSize: 14, color: C.text1, margin: 0, isTextBox: true });
});
caption(s, "UN Comtrade, SH 7108. Les 8 pays affichés font 138,37 t ; les 0,13 t restantes : Espagne 0,11 t, Italie, Arabie saoudite, Israël, France, Turquie… Pas d'agrégat régional inclus.");

// ===== 6b. Cameroun-EAU
s = content("Cameroun–EAU : vingt ans de flux aurifères déclarés");
const uy = years.filter(y => y >= 2004 && y <= 2023);
s.addChart(pres.charts.BAR, [{ name: "EAU (t)", labels: uy.map(String), values: uy.map(y => +(decl[y].eau / 1000).toFixed(2)) }], {
  x: 0.6, y: 1.4, w: 7.9, h: 5.0, barDir: "col", chartColors: [H.accent5], showLegend: false,
  showTitle: true, title: "Importations d'or brut déclarées par les EAU en provenance du Cameroun (t)",
  valAxisMinVal: 0, catAxisLabelRotate: -45, ...chartBase(), objectName: "Graphique EAU annuel",
});
const per = [[2004, 2009], [2010, 2014], [2015, 2019], [2020, 2023]];
const phd = ["Période", "Déclaré par les EAU"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const prow = per.map(([a, b]) => { let t = 0; for (let y = a; y <= b; y++) t += decl[y].eau; return [a + "–" + b, fr(t / 1000, 3) + " t"]; });
prow.push(["2004–2023", fr(111.273, 3) + " t"], ["2024–2025", "Non publiées"]);
s.addTable([phd, ...prow.map((r, i) => r.map(c => ({ text: c, options: { bold: i === 4, color: H.dk1 } })))], {
  x: 8.8, y: 1.5, w: 3.9, colW: [1.8, 2.1], fontSize: 14, fontFace: THEME.bodyFontFace, rowH: 0.5,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "Tableau périodes EAU",
});
s.addText("Ce sont des déclarations d'importations des EAU, pas des achats documentés auprès de producteurs camerounais.", { x: 8.8, y: 5.25, w: 3.9, h: 1.1, fontSize: 14, italic: true, color: C.text2, valign: "top", margin: 0, isTextBox: true });
caption(s, "Source : UN Comtrade, SH 7108, déclarant 784 (EAU), partenaire 120 (Cameroun), poids nets. Sous-totaux calculés sur les valeurs non arrondies.");

// ===== 7. Ecart
s = content("Quelques kilos déclarés au départ, des tonnes à l'arrivée");
const hdr = ["Année", "Exporté selon le Cameroun", "Reçu selon les partenaires", "Rapport"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const tbl = [
  ["2013", "214 kg", "11 490 kg", "× 54"],
  ["2018", "13 kg", "11 712 kg", "× 900"],
  ["2021", "40 kg (73 kg selon l'ITIE)", "5 602 kg", "× 140"],
  ["2022", "3,5 kg (47,9 kg selon l'ITIE)", "4 820 kg", "× 1 380"],
  ["2023", "22,3 kg (ITIE) ; 20 kg vers les EAU (WITS)", "18 255 kg (EAU seuls : 14 048 kg)", "× 820 (EAU : × 702)"],
];
s.addTable([hdr, ...tbl.map(r => r.map((c, j) => ({ text: c, options: { bold: j === 3, color: j === 3 ? H.accent2 : H.dk1 } })))], {
  x: 0.6, y: 1.5, w: 12.1, colW: [1.6, 4.3, 3.8, 2.4], fontSize: 16, fontFace: THEME.bodyFontFace, rowH: 0.62,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "Tableau écart",
});
card(s, 0.6, 5.4, 12.1, 1.0, "Lecture écart");
s.addText("Le rapport « Reçu ÷ Exporté » atteint plusieurs centaines : l'essentiel de l'or quitte le pays hors des circuits déclarés, ou est attribué au Cameroun alors qu'il vient d'ailleurs.", { x: 0.9, y: 5.45, w: 11.5, h: 0.9, fontSize: 15, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
caption(s, "Même code SH 7108 et même unité (kg nets) des deux côtés. Sources : UN Comtrade/WITS (flux X et M), ITIE 2021–2023 via la presse. 2023 : rapport sur la base ITIE.");

// ===== 8. Recoupement ITIE
s = content("ITIE et Comtrade concordent, à périmètre précisé");
const itie = [
  ["2021", "5,6 t", "5,60 t", "EAU 4,81 t + Rwanda 0,79 t"],
  ["2022", "4,8 t", "4,82 t", "EAU 4,71 t + Rwanda 0,11 t"],
  ["2023", "15,2 t", "15,19 t", "Périmètre EAU 14,05 t + Ouganda 1,14 t. Tous déclarants : 18,26 t (diapo 7), car le Rwanda (3,06 t) s'ajoute"],
];
itie.forEach((r, i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.8, 4.6, "Recoupement " + r[0]);
  s.addText(r[0], { x: x + 0.3, y: 1.8, w: 3.2, h: 0.6, fontSize: 24, bold: true, color: C.text1, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
  s.addText("ITIE", { x: x + 0.3, y: 2.55, w: 1.5, h: 0.35, fontSize: 13, color: C.accent4, margin: 0, isTextBox: true });
  s.addText(r[1], { x: x + 0.3, y: 2.9, w: 1.6, h: 0.7, fontSize: 30, bold: true, color: C.accent5, margin: 0, isTextBox: true });
  s.addText("Comtrade", { x: x + 2.0, y: 2.55, w: 1.6, h: 0.35, fontSize: 13, color: C.accent4, margin: 0, isTextBox: true });
  s.addText(r[2], { x: x + 2.0, y: 2.9, w: 1.6, h: 0.7, fontSize: 30, bold: true, color: C.accent3, margin: 0, isTextBox: true });
  s.addText(r[3], { x: x + 0.3, y: 3.9, w: 3.2, h: 2.1, fontSize: 15, color: C.text1, valign: "top", margin: 0, isTextBox: true });
});
caption(s, "Le périmètre exact retenu par l'ITIE n'est pas publié : la correspondance est une inférence. Ouganda 2023 : 1 144,7 kg nets (Comtrade) contre 1 117 kg (WITS, quantité).");

// ===== 8b. Vérifications externes
s = content("Ce que les vérifications externes confirment");
const ihd = ["Année", "Comtrade, EAU (t)", "Interpol 2021, EAU (t)"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const iy = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018];
const ivals = { 2010: "2,37", 2011: "3,53", 2012: "4,98", 2013: "9,57", 2014: "8,67", 2015: "10,42", 2016: "9,94", 2017: "10,90", 2018: "11,70" };
s.addTable([ihd, ...iy.map(y => [String(y), fr(decl[y].eau / 1000, 2), ivals[y]].map(c => ({ text: c, options: { color: H.dk1 } })))], {
  x: 0.6, y: 1.45, w: 6.0, colW: [1.4, 2.3, 2.3], fontSize: 14, fontFace: THEME.bodyFontFace, rowH: 0.48,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "Tableau Interpol",
});
const vf = [
  ["Interpol 2021", "Série EAU 2010–2018 identique à Comtrade, à l'arrondi près. En 2017 : 4 kg déclarés par le Cameroun vers les EAU contre 10,9 t reçues"],
  ["WITS 2023", "EAU 14 048 kg (879,7 M USD), Rwanda 3 060 kg, Ouganda 1 117 kg ; le Cameroun déclare 20 kg vers les EAU"],
  ["SWISSAID 2025", "Les données 2024 des EAU, mises en ligne puis retirées de Comtrade « pour vérification » : 2024–2025 restent partiels"],
];
vf.forEach((f, i) => {
  const y = 1.45 + i * 1.7;
  card(s, 6.9, y, 5.8, 1.55, "Vérification " + (i + 1));
  s.addText(f[0], { x: 7.15, y: y + 0.12, w: 5.3, h: 0.4, fontSize: 16, bold: true, color: C.accent3, margin: 0, isTextBox: true });
  s.addText(f[1], { x: 7.15, y: y + 0.52, w: 5.3, h: 0.95, fontSize: 13, color: C.text1, valign: "top", margin: 0, isTextBox: true });
});
caption(s, "Sources : INTERPOL, Illegal Gold Mining in Central Africa (2021) ; WITS/UN Comtrade (vérification externe du 31/10/2026) ; SWISSAID, communiqué du 04/11/2025 et Swissinfo.");

// ===== 9. Ecart au cours
s = content("Les valeurs déclarées suivent le cours mondial de l'or");
const ey = years.filter(y => y >= 2005);
s.addChart(pres.charts.LINE, [{ name: "Écart (%)", labels: ey.map(String), values: ey.map(y => data[y].ecart) }], {
  x: 0.6, y: 1.4, w: 8.4, h: 5.0, chartColors: [H.accent2], lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 7,
  showLegend: false, showTitle: true, title: "Écart entre valeur déclarée et poids × cours LBMA (%)",
  valAxisMinVal: -20, valAxisMaxVal: 10, valAxisMajorUnit: 5, catAxisLabelRotate: -45, ...chartBase(), objectName: "Graphique écart cours",
});
card(s, 9.3, 1.4, 3.4, 5.0, "Commentaire écart");
s.addText([
  { text: "± 8 %", options: { bold: true, fontSize: 26, color: C.accent5, breakLine: true } },
  { text: "La plupart des années : les poids déclarés sont de l'or presque pur", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "– 11 à – 15 %", options: { bold: true, fontSize: 26, color: C.accent2, breakLine: true } },
  { text: "2016–2020 et 2024–2025 : or doré déclaré au poids brut, ou valeurs rwandaises basses (hypothèses)" },
], { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
caption(s, "Sources : UN Comtrade ; Banque mondiale, Pink Sheet (moyenne LBMA PM ; cours spot à partir de juin 2025).");

// ===== 10. Couts fiscaux
s = content("Pertes fiscales : des estimations, non démontrées");
const fy = [2021, 2022, 2023, 2024, 2025];
const pub = { 2021: 52.81, 2022: 50.55, 2023: 161.79, 2024: 159.15, 2025: 153.2 };
const eiti = { 2021: 0, 2022: 0, 2023: 165, 2024: 0, 2025: 0 };
s.addChart(pres.charts.BAR, [
  { name: "Scénario bas : taxe ad valorem seule", labels: fy.map(String), values: fy.map(y => +(data[y].lo / 1e9).toFixed(1)) },
  { name: "Scénario haut : ISML 25 % + droit de sortie", labels: fy.map(String), values: fy.map(y => +(data[y].hi / 1e9).toFixed(1)) },
  { name: "MINMIDT, série 2021–2025 (577,5 au total)", labels: fy.map(String), values: fy.map(y => pub[y]) },
  { name: "ITIE, estimation 2023", labels: fy.map(String), values: fy.map(y => eiti[y]) },
], {
  x: 0.6, y: 1.4, w: 8.4, h: 5.0, barDir: "col", barGrouping: "clustered", chartColors: [H.accent6, H.accent1, H.accent2, H.accent3],
  showLegend: true, legendPos: "b", showTitle: true, title: "Manque à gagner potentiel sur l'or non réconcilié (Md FCFA)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0;-0;;", ...chartBase(), objectName: "Graphique pertes fiscales",
});
card(s, 9.3, 1.4, 3.4, 5.0, "Commentaire pertes");
s.addText([
  { text: "Risque, pas perte établie", options: { bold: true, fontSize: 18, color: C.accent2, breakLine: true } },
  { text: "Le scénario haut suppose que tout l'or est camerounais et relève du régime semi-mécanisé (ISML de 25 % en nature sur la production brute). Ni l'origine ni le régime ne sont établis.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "Deux estimations distinctes pour 2023 : 161,8 Md (MINMIDT) et 165 Md (ITIE). Le texte de la page MINMIDT du 24/07/2026 cite 557 Md au lieu de 577,5 : à réconcilier.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "2024–2025 : sans les EAU", options: { italic: true } },
], { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 13, color: C.text1, valign: "top", margin: 0, isTextBox: true });
caption(s, "Il faut distinguer valeur non réconciliée, prélèvements légalement exigibles, recettes perçues et pertes. Taux par période et textes : PERTES_FISCALES.md. Scénarios = calculs de l'auteur.");

// ===== 11. Section autres
section("Les autres minerais");
s = pres.addSlide({ masterName: "SECTION_SOMBRE", sectionTitle: cur() });
s.addText("Diamant, cobalt, fer, manganèse, bauxite", { placeholder: "title" });
s.addText("Des flux faibles ou inexistants, des enjeux de traçabilité et de contrats", { placeholder: "body" });

// ===== 12. Diamant
s = content("Diamant : un enjeu de traçabilité, pas de recettes");
const dy = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
const dv = [236, 156, 242, 179, 84, 274, 127, 92, 249, 117, 35, 16];
s.addChart(pres.charts.BAR, [{ name: "USD par carat", labels: dy.map(String), values: dv }], {
  x: 0.6, y: 1.4, w: 6.6, h: 5.0, barDir: "col", chartColors: [H.accent3], showLegend: false,
  showTitle: true, title: "Prix moyen des diamants exportés (USD/carat, Kimberley)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0", ...chartBase(), objectName: "Graphique diamant prix",
});
const dfacts = [
  ["≤ 0,6 M USD", "d'exportations officielles par an"],
  ["140 000 ct", "sortis clandestinement de RCA après mai 2013 (ONU), tous corridors confondus"],
  ["4 523 ct", "sur un faux certificat Kimberley camerounais (2016)"],
  ["25–175 M FCFA", "de perte fiscale calculée par an"],
];
dfacts.forEach((f, i) => {
  const y = 1.4 + i * 1.27;
  card(s, 7.5, y, 5.2, 1.12, "Fait diamant " + (i + 1));
  s.addText(f[0], { x: 7.7, y: y + 0.1, w: 2.2, h: 0.92, fontSize: 20, bold: true, color: C.accent3, valign: "middle", margin: 0, isTextBox: true });
  s.addText(f[1], { x: 9.95, y: y + 0.1, w: 2.6, h: 0.92, fontSize: 13, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
});
caption(s, "Sources : Processus de Kimberley (extraits), Panel d'experts ONU S/2014/762, PAC/IMPACT 2016. Prix 2024 : alignement des colonnes incertain.");

// ===== 13. Quatre minerais
s = content("Quatre minerais : aucun flux trouvé, sans preuve d'absence");
const four = [
  ["Cobalt", "Geovic à Nkamouna (Lomié) jamais exploité ; permis retiré en février 2025 et confié à la Sonamines", "Miroir : ≈ 3 000 USD (Chine, 2023)"],
  ["Fer", "Aucune exportation confirmée ; Grand Zambi inaugurée en septembre 2025", "Arbitrage Mbalam : 616 M USD (≈ 355 Md FCFA) dus à Sundance"],
  ["Manganèse", "Coproduit de Nkamouna, jamais exploité ; aucun permis actif connu", "Aucun flux miroir trouvé (recherche web seulement)"],
  ["Bauxite", "Minim-Martap (Canyon/Camalco) : première exportation repoussée, objectif retiré en août 2026", "Recettes attendues : 9,5–16,6 Md FCFA/an à 3 Mt"],
];
four.forEach((f, i) => {
  const x = 0.6 + (i % 2) * 6.15, y = 1.5 + Math.floor(i / 2) * 2.55;
  card(s, x, y, 5.95, 2.35, "Minerai " + f[0]);
  circleNum(s, i + 1, x + 0.25, y + 0.25, 0.55, C.accent3);
  s.addText(f[0], { x: x + 1.0, y: y + 0.25, w: 4.7, h: 0.55, fontSize: 20, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  s.addText(f[1], { x: x + 0.25, y: y + 0.95, w: 5.45, h: 0.8, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  s.addText(f[2], { x: x + 0.25, y: y + 1.75, w: 5.45, h: 0.45, fontSize: 14, bold: true, color: C.accent2, valign: "top", margin: 0, isTextBox: true });
});
caption(s, "« Aucun flux trouvé » ne signifie pas « absence prouvée » : Comtrade n'a pas pu être interrogé pour ces minerais. Sources : extraits web (USGS, BGS, presse, ASX, sentence CCI du 26/07/2026).");

// ===== 14. Comparatif
s = content("Six minerais : l'or a les divergences les mieux documentées");
const ch = ["Minerai", "Flux officiels trouvés", "Flux miroir trouvés", "Coût estimé", "Fiabilité"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const comp = [
  ["Or", "Quelques kg/an", "5 à 18 t/an (280–1 145 M USD)", "Estimé 51–162 Md FCFA/an (MINMIDT)", "Élevée (volumes)"],
  ["Diamant", "250 à 18 000 ct/an (≤ 0,6 M USD)", "Négligeable dans les sources", "0,03–0,2 Md FCFA/an (calcul)", "Faible"],
  ["Cobalt", "Aucun", "≈ 3 000 USD (2023)", "Négligeable", "Moyenne"],
  ["Fer", "Aucun confirmé", "≈ 0", "Arbitrage : ≈ 355 Md FCFA", "Moyenne"],
  ["Manganèse", "Aucun trouvé", "Non interrogé dans Comtrade", "–", "Faible"],
  ["Bauxite", "Aucun trouvé", "Non interrogé dans Comtrade", "–", "Faible"],
];
s.addTable([ch, ...comp.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, color: (i === 0 && j === 3) ? H.accent2 : H.dk1, fill: { color: i === 0 ? "F6EED3" : H.lt1 } } })))], {
  x: 0.6, y: 1.45, w: 12.1, colW: [1.6, 2.9, 3.0, 3.1, 1.5], fontSize: 14, fontFace: THEME.bodyFontFace, rowH: 0.66,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, valign: "middle", objectName: "Tableau comparatif",
});
caption(s, "Fiabilité : élevée = base Comtrade complète ; moyenne = sources concordantes ; faible = extraits de recherche web seulement.");

// ===== 15. Limites
section("Conclusion");
s = content("Ce que ces chiffres ne prouvent pas");
const lim = [
  ["Origine ou provenance", "Une partie de l'or et des diamants peut venir de Centrafrique ou du Tchad et transiter par le Cameroun"],
  ["Écart ou fraude", "Contrebande, sous-déclaration, transport en bagage à main ou erreurs de code pays : les données ne les distinguent pas"],
  ["Données incomplètes", "2024–2025 sans les EAU ; Comtrade inaccessible pour cinq minerais"],
  ["Fiscalité incertaine", "Taux de 2001–2015 contradictoires (3 % ou 5 %) ; droit de sortie avant 2020 non trouvé"],
];
lim.forEach((l, i) => {
  const x = 0.6 + (i % 2) * 6.15, y = 1.5 + Math.floor(i / 2) * 2.45;
  card(s, x, y, 5.95, 2.2, "Limite " + (i + 1));
  circleNum(s, "!", x + 0.25, y + 0.25, 0.55, C.accent2);
  s.addText(l[0], { x: x + 1.0, y: y + 0.25, w: 4.7, h: 0.55, fontSize: 20, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  s.addText(l[1], { x: x + 0.25, y: y + 0.95, w: 5.45, h: 1.1, fontSize: 15, color: C.text1, valign: "top", margin: 0, isTextBox: true });
});
caption(s, "Le détail des contradictions et des sources figure dans les rapports par minerai (docs/recherche-*-cameroun/RAPPORT.md).");

// ===== 16. Conclusion
s = pres.addSlide({ masterName: "TITRE_SOMBRE", sectionTitle: cur() });
s.addText("Conclusions et prochaines étapes", { x: 0.8, y: 0.6, w: 11.7, h: 0.9, fontSize: 36, bold: true, color: C.background1, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
const concl = [
  "Fait documenté : les partenaires déclarent des importations d'or attribuées au Cameroun très supérieures à ses exportations officielles (Interpol, ITIE, WITS)",
  "Hypothèse à investiguer : une part importante de l'écart pourrait venir de circuits informels, de contrebande ou de transit régional",
  "Résultat à établir : volumes d'origine camerounaise exportés irrégulièrement et montant exact des recettes perdues",
];
const nexts = [
  "Comparer les exportations du Rwanda et de l'Ouganda vers les EAU à leurs importations attribuées au Cameroun ; examiner raffineries et intermédiaires",
  "Construire un modèle fiscal documenté par régime d'exploitation, avec scénarios et textes juridiques",
  "Obtenir les données EAU 2024–2025, vérifier Rwanda et Ouganda, interroger Comtrade pour les autres minerais",
];
s.addText("Conclusions", { x: 0.8, y: 1.7, w: 5.6, h: 0.5, fontSize: 20, bold: true, color: C.accent1, margin: 0, isTextBox: true });
s.addText("Prochaines étapes", { x: 6.9, y: 1.7, w: 5.6, h: 0.5, fontSize: 20, bold: true, color: C.accent1, margin: 0, isTextBox: true });
concl.forEach((t, i) => {
  circleNum(s, i + 1, 0.8, 2.4 + i * 1.4, 0.55);
  s.addText(t, { x: 1.55, y: 2.35 + i * 1.4, w: 4.9, h: 1.2, fontSize: 15, color: C.background1, valign: "top", margin: 0, isTextBox: true });
});
nexts.forEach((t, i) => {
  circleNum(s, i + 1, 6.9, 2.4 + i * 1.4, 0.55, C.accent3);
  s.addText(t, { x: 7.65, y: 2.35 + i * 1.4, w: 4.9, h: 1.2, fontSize: 15, color: C.background1, valign: "top", margin: 0, isTextBox: true });
});

// ===== Annexes
section("Annexes");
const ugaQty = { 2023: 1116.8, 2024: 3175.4, 2025: 3321.0 };
const ah = ["Année", "Total (kg)", "EAU (kg)", "Rwanda (kg)", "Ouganda, poids net", "Ouganda, quantité", "Autres (kg)", "Valeur (M USD)"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const fk = x => x ? Math.round(x).toLocaleString("fr-FR") : "–";
[[2000, 2012], [2013, 2025]].forEach(([a, b], k) => {
  s = content("Annexe A" + (k + 1) + " : or brut par déclarant, " + a + "–" + b);
  const rr = [];
  for (let y = a; y <= b; y++) {
    const d = decl[y] || { eau: 0, rwa: 0, uga: 0, aut: 0 };
    rr.push([String(y) + (y >= 2024 ? " *" : ""), fk(data[y].kg), y >= 2024 ? "n. p." : fk(d.eau), fk(d.rwa), fk(d.uga), fk(ugaQty[y] || 0), fk(d.aut), fr(data[y].usd / 1e6, 1)].map(c => ({ text: c, options: { color: H.dk1 } })));
  }
  s.addTable([ah, ...rr], {
    x: 0.6, y: 1.4, w: 12.1, colW: [1.1, 1.55, 1.55, 1.45, 1.7, 1.7, 1.35, 1.7], fontSize: 14, fontFace: THEME.bodyFontFace, rowH: 0.34, align: "right",
    border: { type: "solid", pt: 0.5, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "Annexe table " + (k + 1),
  });
  caption(s, k ? "* Partiel : EAU non publiés (n. p.). Totaux en poids net (netWgt) ; la quantité (qty) ne diffère notablement que pour l'Ouganda. Fichier : donnees_miroir_or_tous_declarants.csv." : "Source : UN Comtrade, aperçu public de l'API, flux M, partenaire 120 (Cameroun), extrait le 31/10/2026. Poids nets en kg, valeurs CIF en USD.");
});
s = content("Annexe A3 : reproductibilité et périmètre");
const meta = [
  ["Requête", "comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=…&partnerCode=120&flowCode=M&cmdCode=7108 (puis 7112, 7113)"],
  ["Déclarants", "254 pays et territoires interrogés (table « Reporters », groupes et agrégats régionaux exclus) ; 19 ont déclaré des importations d'or brut non nulles"],
  ["Requêtes", "5 lots de 44 à 57 codes × 26 années × 3 codes SH = 390 requêtes annuelles, plus relances après délai dépassé ; 283 observations non nulles"],
  ["Contrôles", "Aucune réponse tronquée (indicateur « truncated » faux, plafond de 500 jamais atteint) ; doublons éliminés sur la clé code SH × année × déclarant"],
  ["Période", "2000–2025, fréquence annuelle ; extraction du 31/10/2026 ; données révisables"],
  ["Conversions", "Taux USD/XAF : Banque mondiale PA.NUS.FCRF ; cours de l'or : Banque mondiale Pink Sheet (LBMA PM)"],
];
meta.forEach((m, i) => {
  const y = 1.4 + i * 0.86;
  card(s, 0.6, y, 12.1, 0.76, "Méta " + (i + 1));
  s.addText(m[0], { x: 0.85, y: y + 0.06, w: 2.2, h: 0.64, fontSize: 15, bold: true, color: C.accent5, valign: "middle", margin: 0, isTextBox: true });
  s.addText(m[1], { x: 3.1, y: y + 0.06, w: 9.4, h: 0.64, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
});
caption(s, "Dépôt GitHub boujieka/Boujieka, dossier docs/. Les autres minerais reposent sur des extraits de recherche web, sans extraction Comtrade.");

s = content("Annexe A4 : sources primaires");
const srcs = [
  ["UN Comtrade", "API publique preview · comtradeapi.un.org/public/v1/preview/C/A/HS · SH 7108, 7112, 7113 · partenaire 120 · extrait le 31/10/2026"],
  ["INTERPOL (2021)", "Illegal Gold Mining in Central Africa · interpol.int/content/download/16493 · séries EAU 2008–2018"],
  ["ITIE / EITI", "« Cameroon's gold gap » · eiti.org/impact-story/cameroons-gold-gap-how-eiti-data-driving-reforms · rapport 2023 présenté le 10/12/2025"],
  ["MINMIDT", "Série 2021–2025 (577,51 Md FCFA) relayée par sikafinance.com (07/2026) ; page MINMIDT du 24/07/2026 citant 557 Md : à réconcilier"],
  ["SWISSAID (2025)", "« United Arab Emirates: More Than Ever a Hub for Conflict Gold » · swissaid.ch · 04/11/2025 (retrait des données EAU 2024)"],
  ["Banque mondiale", "Taux PA.NUS.FCRF · api.worldbank.org ; cours de l'or : Pink Sheet annuel, CMO-Historical-Data-Annual.xlsx"],
];
srcs.forEach((m, i) => {
  const y = 1.4 + i * 0.86;
  card(s, 0.6, y, 12.1, 0.76, "Source " + (i + 1));
  s.addText(m[0], { x: 0.85, y: y + 0.06, w: 2.5, h: 0.64, fontSize: 14, bold: true, color: C.accent5, valign: "middle", margin: 0, isTextBox: true });
  s.addText(m[1], { x: 3.4, y: y + 0.06, w: 9.1, h: 0.64, fontSize: 13, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
});
caption(s, "Liste complète des URL dans les rapports par minerai (dépôt boujieka/Boujieka, dossier docs/). WITS 2023 : vérification externe du 31/10/2026.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
