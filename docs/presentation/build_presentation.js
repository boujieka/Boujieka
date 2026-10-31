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
s.addText("Recherche documentaire · données au 31 octobre 2026", { x: 0.8, y: 6.5, w: 8, h: 0.4, fontSize: 14, color: C.accent4, margin: 0, isTextBox: true });
s.addNotes("Présentation des résultats : analyse miroir UN Comtrade (tous déclarants) pour l'or, recherches documentaires pour les cinq autres minerais.");

// ===== 2. L'essentiel
s = content("L'essentiel : l'or pèse presque tout");
const stats = [
  ["138,5 t", "d'or déclarées à l'arrivée par les pays partenaires comme venant du Cameroun, 2000–2025"],
  ["6,58 Md USD", "de valeur déclarée, soit ≈ 3 744 Md FCFA (taux Banque mondiale)"],
  ["577,5 Md FCFA", "de pertes fiscales sur 2021–2025 selon le ministère des Mines"],
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
caption(s, "Sources : UN Comtrade (SH 7108, partenaire Cameroun, 254 déclarants) ; Banque mondiale ; MINMIDT via Sikafinance (juillet 2026).");

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
s.addText("Analyse miroir complète, 254 pays déclarants, codes SH 7108, 7112 et 7113", { placeholder: "body" });

// ===== 5. Volumes annuels
s = content("Les volumes explosent après 2009 et culminent en 2023");
const yrs = years.filter(y => y >= 2000);
s.addChart(pres.charts.BAR, [{ name: "Or déclaré par les partenaires (t)", labels: yrs.map(String), values: yrs.map(y => +(data[y].kg / 1000).toFixed(1)) }], {
  x: 0.6, y: 1.4, w: 8.4, h: 5.0, barDir: "col", chartColors: [H.accent1], showLegend: false,
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
  { text: "Sans les EAU, non publiés : sous-estimé" },
], { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 14, color: C.text1, valign: "top", margin: 0, paraSpaceAfter: 4, isTextBox: true });
caption(s, "Source : UN Comtrade, aperçu public de l'API, extrait le 31/10/2026. Sonamines : ≈ 12,2 t enregistrées à Dubaï en 2024 (non vérifié dans Comtrade).");

// ===== 6. Destinations
s = content("Les Émirats arabes unis reçoivent 80 % de l'or");
const dest = [["Émirats arabes unis", 111.3], ["Rwanda", 16.0], ["Ouganda", 7.7], ["Allemagne", 1.9], ["États-Unis", 0.55], ["Belgique", 0.42], ["Suisse", 0.31], ["Corée du Sud", 0.22]].reverse();
s.addChart(pres.charts.BAR, [{ name: "Cumul 2000–2025 (t)", labels: dest.map(d => d[0]), values: dest.map(d => d[1]) }], {
  x: 0.6, y: 1.4, w: 7.6, h: 5.0, barDir: "bar", chartColors: [H.accent5], showLegend: false,
  showTitle: true, title: "Or déclaré reçu du Cameroun, cumul 2000–2025 (tonnes)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", ...chartBase(), objectName: "Graphique destinations",
});
const facts6 = [
  ["111,3 t", "EAU, 2004–2023, pour 4,81 Md USD"],
  ["16,0 t", "Rwanda, 2019–2025 : nouveau relais régional"],
  ["7,7 t", "Ouganda, 2023–2025"],
];
facts6.forEach((f, i) => {
  const y = 1.5 + i * 1.6;
  card(s, 8.5, y, 4.2, 1.4, "Fait destination " + (i + 1));
  s.addText(f[0], { x: 8.75, y: y + 0.15, w: 3.8, h: 0.6, fontSize: 26, bold: true, color: C.accent5, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
  s.addText(f[1], { x: 8.75, y: y + 0.75, w: 3.8, h: 0.55, fontSize: 14, color: C.text1, margin: 0, isTextBox: true });
});
caption(s, "Source : UN Comtrade, SH 7108. Le Rwanda et l'Ouganda pourraient servir de transit vers Dubaï : hypothèse non vérifiée.");

// ===== 7. Ecart
s = content("Quelques kilos déclarés au départ, des tonnes à l'arrivée");
const hdr = ["Année", "Exporté selon le Cameroun", "Reçu selon les partenaires", "Rapport"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const tbl = [
  ["2013", "214 kg", "11 490 kg", "× 54"],
  ["2018", "13 kg", "11 712 kg", "× 900"],
  ["2021", "40 kg (73 kg selon l'ITIE)", "5 602 kg", "× 140"],
  ["2022", "3,5 kg (47,9 kg selon l'ITIE)", "4 820 kg", "× 1 380"],
  ["2023", "22,3 kg (ITIE)", "18 255 kg", "× 820"],
];
s.addTable([hdr, ...tbl.map(r => r.map((c, j) => ({ text: c, options: { bold: j === 3, color: j === 3 ? H.accent2 : H.dk1 } })))], {
  x: 0.6, y: 1.5, w: 12.1, colW: [1.6, 4.3, 3.8, 2.4], fontSize: 16, fontFace: THEME.bodyFontFace, rowH: 0.62,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "Tableau écart",
});
card(s, 0.6, 5.4, 12.1, 1.0, "Lecture écart");
s.addText("Le rapport « Reçu ÷ Exporté » atteint plusieurs centaines : l'essentiel de l'or quitte le pays hors des circuits déclarés, ou est attribué au Cameroun alors qu'il vient d'ailleurs.", { x: 0.9, y: 5.45, w: 11.5, h: 0.9, fontSize: 15, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
caption(s, "Sources : UN Comtrade (flux X et M), rapports ITIE Cameroun 2021–2023 via la presse. Rapport calculé sur les chiffres Comtrade, sauf 2023 (ITIE).");

// ===== 8. Recoupement ITIE
s = content("Nos chiffres recoupent presque exactement l'ITIE");
const itie = [
  ["2021", "5,6 t", "5,60 t", "EAU 4,81 t + Rwanda 0,79 t"],
  ["2022", "4,8 t", "4,82 t", "EAU 4,71 t + Rwanda 0,11 t"],
  ["2023", "15,2 t", "15,19 t", "EAU 14,05 t + Ouganda 1,14 t ; le Rwanda (3,06 t) n'est pas compté"],
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
caption(s, "L'écart de 2023 suggère que l'ITIE n'a pas intégré l'enregistrement rwandais, peut-être publié plus tard : inférence non vérifiée.");

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
s = content("Le coût fiscal atteint 50 à 165 Md FCFA par an depuis 2021");
const fy = [2021, 2022, 2023, 2024, 2025];
const pub = { 2021: 52.8, 2022: 50.6, 2023: 165, 2024: 159.2, 2025: 153.2 };
s.addChart(pres.charts.BAR, [
  { name: "Calcul, taux bas", labels: fy.map(String), values: fy.map(y => +(data[y].lo / 1e9).toFixed(1)) },
  { name: "Calcul, taux haut", labels: fy.map(String), values: fy.map(y => +(data[y].hi / 1e9).toFixed(1)) },
  { name: "Publié (ITIE 2023, MINMIDT)", labels: fy.map(String), values: fy.map(y => pub[y]) },
], {
  x: 0.6, y: 1.4, w: 8.4, h: 5.0, barDir: "col", barGrouping: "clustered", chartColors: [H.accent6, H.accent1, H.accent2],
  showLegend: true, legendPos: "b", showTitle: true, title: "Perte fiscale sur l'or non déclaré (Md FCFA)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0", ...chartBase(), objectName: "Graphique pertes fiscales",
});
card(s, 9.3, 1.4, 3.4, 5.0, "Commentaire pertes");
s.addText([
  { text: "164 à 835 Md FCFA", options: { bold: true, fontSize: 22, color: C.accent2, breakLine: true } },
  { text: "de perte calculée sur 2000–2025", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "Pourquoi la hausse ?", options: { bold: true, breakLine: true } },
  { text: "3 % de taxe avant 2014, puis prélèvement de 15 % (2014), impôt de 25 % sur le semi-mécanisé (2017), droit de sortie (2020)", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "2024–2025 : calcul sans les EAU, donc minoré", options: { italic: true } },
], { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 13, color: C.text1, valign: "top", margin: 0, isTextBox: true });
caption(s, "Calcul : valeur non déclarée × taux × taux de change Banque mondiale ; il suppose que tout l'or est camerounais. Publié : ITIE 2023 (165), MINMIDT 2021–2025 (577,5 au total).");

// ===== 11. Section autres
section("Les autres minerais");
s = pres.addSlide({ masterName: "SECTION_SOMBRE", sectionTitle: cur() });
s.addText("Diamant, cobalt, fer, manganèse, bauxite", { placeholder: "title" });
s.addText("Des flux faibles ou inexistants, des enjeux de traçabilité et de contrats", { placeholder: "body" });

// ===== 12. Diamant
s = content("Diamant : un enjeu de traçabilité, pas de recettes");
const dy = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
const dv = [236, 156, 242, 179, 84, 274, 127, 92, 249, 117, 35, 15];
s.addChart(pres.charts.BAR, [{ name: "USD par carat", labels: dy.map(String), values: dv }], {
  x: 0.6, y: 1.4, w: 6.6, h: 5.0, barDir: "col", chartColors: [H.accent3], showLegend: false,
  showTitle: true, title: "Prix moyen des diamants exportés (USD/carat, Kimberley)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0", ...chartBase(), objectName: "Graphique diamant prix",
});
const dfacts = [
  ["≤ 0,6 M USD", "d'exportations officielles par an"],
  ["140 000 ct", "de diamants centrafricains vendus illégalement via la frontière (ONU, 2013–2014)"],
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
s = content("Cobalt, fer, manganèse, bauxite : des projets, pas de flux");
const four = [
  ["Cobalt", "Geovic à Nkamouna (Lomié) jamais exploité ; permis retiré en février 2025 et confié à la Sonamines", "Miroir : ≈ 3 000 USD (Chine, 2023)"],
  ["Fer", "Aucune exportation confirmée ; Grand Zambi inaugurée en septembre 2025", "Arbitrage Mbalam : 616 M USD (≈ 355 Md FCFA) dus à Sundance"],
  ["Manganèse", "Coproduit de Nkamouna, jamais exploité ; aucun permis actif connu", "Aucun flux miroir trouvé"],
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
caption(s, "Sources : extraits de recherche web (USGS, BGS, presse, communiqués ASX, sentence CCI du 26/07/2026 via la presse). Aucune extraction Comtrade possible pour ces minerais.");

// ===== 14. Comparatif
s = content("Six minerais, un seul vrai écart : l'or");
const ch = ["Minerai", "Flux officiels", "Flux miroir", "Coût estimé", "Fiabilité"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const comp = [
  ["Or", "Quelques kg/an", "5 à 18 t/an (280–1 145 M USD)", "50–165 Md FCFA/an (2021–2025)", "Élevée"],
  ["Diamant", "250 à 18 000 ct/an (≤ 0,6 M USD)", "Négligeable dans les sources", "0,03–0,2 Md FCFA/an (calcul)", "Faible"],
  ["Cobalt", "Aucun", "≈ 3 000 USD (2023)", "Négligeable", "Moyenne"],
  ["Fer", "Aucun confirmé", "≈ 0", "Arbitrage : ≈ 355 Md FCFA", "Moyenne"],
  ["Manganèse", "Aucun", "Rien trouvé", "–", "Faible"],
  ["Bauxite", "Aucun", "Rien trouvé", "–", "Faible"],
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
  "L'or est le seul flux massif : ≈ 138 t et 6,6 Md USD déclarés à l'étranger sur 2000–2025",
  "Le manque à gagner fiscal récent atteint ≈ 50–165 Md FCFA par an",
  "Les autres minerais posent des questions de traçabilité (diamant) et de contrats (fer, bauxite, cobalt)",
];
const nexts = [
  "Ouvrir l'accès à UN Comtrade pour refaire l'analyse miroir des cinq autres minerais",
  "Obtenir les données 2024–2025 des EAU et vérifier le Rwanda et l'Ouganda",
  "Lire les textes originaux : Journal officiel, ITIE, rapports de l'ONU et de Kimberley",
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

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
