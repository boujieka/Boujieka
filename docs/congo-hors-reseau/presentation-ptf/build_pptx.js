const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/root/.claude/skills/synced/595554f7-3334-4cb8-90b6-40da4dcb6b84_e238fe12-8a4b-4490-8c46-5bf1323948af/pptx/scripts/apply_theme.js");

const THEME = {
  name: "PEZoR Hors Reseau",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2A24", lt1: "FFFEF9", dk2: "10261F", lt2: "F7F5EE",
    accent1: "1F6B5A", accent2: "E3A21A", accent3: "9FB0A6", accent4: "4A5A52",
    accent5: "2D5246", accent6: "ECEFE6", hlink: "1F6B5A", folHlink: "4A5A52",
  },
};
const HEX = { ink: "1B2A24", dark: "10261F", light: "F7F5EE", light2: "ECEFE6", teal: "1F6B5A", amber: "E3A21A", grey: "9FB0A6",
  muted: "4A5A52", line: "CBD3C6", card: "FFFEF9", cardDark: "17352C", lineDark: "2D5246", onDark: "E9EFE9", onDarkMuted: "B9CCC3", head: "DCE6DD" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5
pres.title = "PEZoR – Consultation des PTF : préparation bancable hors réseau";
pres.subject = "Préparation de 77 localités en mini-réseaux verts et 9 concessions SSD – République du Congo";
pres.author = "MEH / ANER – document de travail";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const M = 0.6, W = 13.333, CW = W - 2 * M;

function layout(name, bg, titleColor, numColor) {
  pres.defineSlideMaster({
    title: name,
    background: { color: bg },
    margin: [0.5, 0.6, 0.6, 0.6],
    slideNumber: { x: 12.25, y: 6.95, w: 0.5, h: 0.3, fontSize: 10, color: numColor, align: "right" },
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 0.78, w: CW, h: 1.0, fontSize: 30, bold: true, color: titleColor, valign: "top", align: "left", margin: 0, fontFace: THEME.headFontFace }, text: "" } },
    ],
  });
}
layout("CONTENT", C.background2, C.text2, C.accent4);
layout("CONTENT_ALT", C.accent6, C.text2, C.accent4);
layout("DARK", C.text2, C.background1, C.accent3);
layout("ACCENT", C.accent2, C.text2, C.text2);
pres.defineSlideMaster({ title: "COVER", background: { color: C.text2 }, objects: [] });

const dark = (m) => m === "DARK" || m === "COVER";
let curSection = null;
function newSlide(master, section, eyebrow, title, notes) {
  if (section !== curSection) { pres.addSection({ title: section }); curSection = section; }
  const s = pres.addSlide({ masterName: master, sectionTitle: section });
  if (eyebrow) s.addText(eyebrow, { x: M, y: 0.42, w: CW, h: 0.3, fontSize: 11, bold: true, charSpacing: 2, color: master === "DARK" ? C.accent2 : master === "ACCENT" ? C.text2 : C.accent1, margin: 0, isTextBox: true, objectName: "Surtitre" });
  if (title) s.addText(title, { placeholder: "title" });
  if (notes) s.addNotes(notes);
  s._m = master;
  return s;
}
function src(s, text) {
  s.addText(text, { x: M, y: 6.85, w: 11.4, h: 0.4, fontSize: 10, color: dark(s._m) ? HEX.onDarkMuted : C.accent4, margin: 0, valign: "top", isTextBox: true, objectName: "Source" });
}
function card(s, x, y, w, h, paras, opts = {}) {
  const d = dark(s._m);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12,
    fill: { color: d ? HEX.cardDark : HEX.card }, line: { color: opts.border || (d ? HEX.lineDark : HEX.line), width: opts.borderW || 1 }, objectName: opts.name || "Carte" });
  s.addText(paras, { x: x + 0.05, y: y + 0.05, w: w - 0.1, h: h - 0.1, margin: 0.18, valign: "top", isTextBox: true, objectName: (opts.name || "Carte") + " texte" });
}
// paragraph builders
function P(s, kind, text, extra = {}) {
  const d = dark(s._m);
  const st = {
    tag: { fontSize: 12, bold: true, color: d ? C.accent2 : C.accent1, charSpacing: 1, paraSpaceAfter: 4 },
    num: { fontSize: 24, bold: true, color: d ? C.accent2 : C.accent1, fontFace: THEME.headFontFace, paraSpaceAfter: 2 },
    big: { fontSize: 34, bold: true, color: d ? C.accent2 : C.accent1, fontFace: THEME.headFontFace, paraSpaceAfter: 2 },
    title: { fontSize: 18, bold: true, color: d ? C.background1 : C.text2, paraSpaceAfter: 4 },
    text: { fontSize: 15, color: d ? HEX.onDarkMuted : C.accent4, paraSpaceAfter: 4 },
  }[kind];
  return { text, options: { ...st, ...extra, breakLine: true } };
}
function lead(s, text, y, h = 0.6, size = 14) {
  s.addText(text, { x: M, y, w: CW, h, fontSize: size, color: dark(s._m) ? HEX.onDarkMuted : C.accent4, margin: 0, valign: "top", isTextBox: true, objectName: "Message" });
}
function stat(s, x, y, w, big, label, size = 30) {
  const d = dark(s._m);
  s.addText([
    { text: big, options: { fontSize: size, bold: true, color: d ? C.accent2 : C.accent1, fontFace: THEME.headFontFace, breakLine: true } },
    { text: label, options: { fontSize: 12, color: d ? HEX.onDarkMuted : C.accent4 } },
  ], { x, y, w, h: 1.05, margin: 0, valign: "top", isTextBox: true, objectName: "Chiffre clé" });
}
function table(s, rows, colW, y, opts = {}) {
  const fs = opts.fontSize || 13;
  const data = rows.map((r, i) => r.map((c, j) => ({ text: String(c), options: {
    bold: i === 0 || (opts.totalRow && i === rows.length - 1), fill: { color: i === 0 ? HEX.head : (opts.totalRow && i === rows.length - 1) ? "E6ECE3" : HEX.card },
    align: (opts.right || []).includes(j) ? "right" : "left", color: HEX.ink, fontSize: fs } })));
  s.addTable(data, { x: M, y, w: opts.w || CW, colW, border: { type: "solid", pt: 0.75, color: HEX.line }, margin: [0.05, 0.1, 0.05, 0.1], rowH: opts.rowH || 0.38, objectName: opts.name || "Tableau" });
}
function hbar(s, opts) {
  // horizontal bar chart (native)
  const data = opts.series.map((sr) => ({ name: sr.name, labels: opts.labels, values: sr.values }));
  s.addChart(pres.charts.BAR, data, {
    x: opts.x, y: opts.y, w: opts.w, h: opts.h, barDir: "bar", barGrouping: opts.stacked ? "stacked" : "clustered",
    catAxisOrientation: "maxMin", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
    catAxisLabelColor: HEX.ink, catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt", catAxisLineShow: false,
    chartColors: opts.colors, showValue: true, dataLabelPosition: opts.stacked ? "inEnd" : "outEnd", dataLabelColor: opts.labelColor || HEX.ink,
    dataLabelFontSize: 12, dataLabelFontFace: "+mn-lt", dataLabelFontBold: true, dataLabelFormatCode: opts.fmt || "#,##0.0",
    showLegend: !!opts.legend, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.ink,
    barGapWidthPct: 45, showTitle: !!opts.title, title: opts.title, titleFontSize: 13, titleColor: HEX.ink, titleFontFace: "+mn-lt",
    objectName: opts.name || "Graphique",
  });
}
function hrect(s, x, y, w, h, color, name) { s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color }, line: { color, width: 0 }, objectName: name || "Barre" }); }
function txt(s, text, x, y, w, h, o = {}) {
  s.addText(text, { x, y, w, h, margin: 0, valign: o.valign || "middle", fontSize: o.size || 13, bold: !!o.bold, color: o.color || (dark(s._m) ? HEX.onDark : HEX.ink), align: o.align || "left", isTextBox: true, objectName: o.name || "Texte" });
}

// ===================== slides =====================
const w3 = (CW - 0.6) / 3, w4 = (CW - 0.9) / 4, w5 = (CW - 1.0) / 5, w2 = (CW - 0.4) / 2;
function txtBlock(s, paras, x, y, w, h) { s.addText(paras, { x, y, w, h, margin: 0, valign: "top", isTextBox: true }); }
function missionStats(s, stats, y = 5.35) { stats.forEach(([b, l], i) => stat(s, M + i * (w3 + 0.3), y, w3, b, l, 26)); }
function bars(s, rows, x0, y0, step, scale, maxW, labelW = 2.7) {
  rows.forEach(([l, b, v, c, lab], i) => { const y = y0 + i * step; txt(s, l, M, y, labelW, 0.4); hrect(s, x0 + b * scale, y + 0.04, Math.max(v * scale, 0.04), 0.3, c, "Barre " + l); txt(s, lab, x0 + (b + v) * scale + 0.1, y, 2.6, 0.4, { bold: true }); });
}

// ---------- Section 1 ----------
const S1 = "Objet et Pacte";
{
  const s = newSlide("COVER", S1, null, null, "Ouverture. Objet : soumettre aux PTF les TdR de préparation bancable de la fenêtre hors réseau du PEZoR et recueillir leurs avis et intentions de financement. Portefeuille sans doublon ; budget de préparation ≈ 15,5 MUSD (plus 0,44 de provision), estimation non validée.");
  s._m = "COVER";
  s.addText("RÉPUBLIQUE DU CONGO · MINISTÈRE DE L’ÉNERGIE ET DE L’HYDRAULIQUE · ANER", { x: M, y: 0.7, w: CW, h: 0.35, fontSize: 12, bold: true, charSpacing: 2, color: C.accent2, margin: 0, isTextBox: true, objectName: "Surtitre" });
  s.addText("Électrification hors réseau : préparer des mini-réseaux verts et une filière solaire domestique bancables", { x: M, y: 1.2, w: 11.2, h: 1.9, fontSize: 36, bold: true, fontFace: THEME.headFontFace, color: C.background1, margin: 0, valign: "top", isTextBox: true, objectName: "Titre" });
  s.addText("Consultation des partenaires techniques et financiers sur les TdR de préparation des investissements du PEZoR, au service du Pacte National Énergétique (Mission 300)", { x: M, y: 3.2, w: 10.5, h: 1.0, fontSize: 16, color: HEX.onDarkMuted, margin: 0, valign: "top", isTextBox: true, objectName: "Sous-titre" });
  [["77", "localités en mini-réseau"], ["160", "localités solaire domestique"], ["78 293", "ménages potentiels"], ["≈ 15,5", "MUSD de préparation"]].forEach(([b, l], i) => stat(s, M + i * 2.45, 5.0, 2.3, b, l, 36));
  s.addText("Novembre 2026\nDocument de consultation", { x: 10.0, y: 5.55, w: 2.73, h: 0.7, fontSize: 11, color: HEX.onDarkMuted, align: "right", margin: 0, isTextBox: true, objectName: "Date" });
}
{
  const s = newSlide("CONTENT", S1, "OBJET DE LA CONSULTATION", "Trois choses que nous attendons des partenaires aujourd’hui",
    "Cadrer la réunion : nous ne venons pas présenter un projet figé mais un projet de TdR à améliorer avec les PTF.");
  [["1", "Valider l’approche", "La séquence par tranches (audit préalable, filière rapide SSD, mini-réseaux) et les gates G0 à G4, dont G3a et G3b."],
   ["2", "Financer la préparation", "≈ 15,5 MUSD de dons et d’avances : ESMAP, fonds BAD, avances de préparation, Basket Fund PEZoR, UE."],
   ["3", "Signaler les intentions d’investissement", "Filière SSD, pilote mini-réseaux et Programme Cadre : prêts, dons, RBF, garanties."]]
    .forEach(([n, t, d], i) => card(s, M + i * (w3 + 0.3), 2.0, w3, 3.3, [P(s, "num", n, { fontSize: 32 }), P(s, "title", t, { fontSize: 20 }), P(s, "text", d, { fontSize: 17 })]));
  lead(s, "Déroulé : Pacte et portefeuille → diagnostic → réponse → budget et financement → discussion.", 5.9);
}
{
  const s = newSlide("CONTENT", S1, "PACTE NATIONAL ÉNERGÉTIQUE · MISSION 300", "La cible rurale : de 1 % à 50 % d’accès en 2030",
    "Le Pacte mesure l’accès par les abonnés E2C (1,01 % en rural) ; WDI : 19,4 % en 2024. Le point 90/10 est à réconcilier : le PEZoR oriente beaucoup plus vers les mini-réseaux.");
  [["1,01 %", "accès rural de référence (abonnés E2C)"], ["50 %", "cible rurale 2030 (81,3 % au niveau national)"], ["79 000", "nouveaux branchements ruraux"], ["944 MUSD", "besoins hors réseau : 606 mini-réseaux, 338 systèmes autonomes"]]
    .forEach(([b, t], i) => card(s, M + i * (w4 + 0.3), 2.0, w4, 2.0, [P(s, "big", b, { fontSize: 30 }), P(s, "text", t)]));
  txtBlock(s, [P(s, "tag", "PRIORITÉ ET COMPTAGE"), P(s, "text", "Localités de plus de 1 000 habitants. Mission 300 ne compte que les nouveaux accès de niveau MTF 1 ou plus.", { fontSize: 15, color: C.text1 })], M, 4.4, w2, 1.6);
  txtBlock(s, [P(s, "tag", "POINT À RÉCONCILIER"), P(s, "text", "Hypothèse du Pacte : 90 % de la hausse rurale par systèmes autonomes, 10 % par mini-réseaux, à confirmer par la SEN.", { fontSize: 15, color: C.text1 })], M + w2 + 0.4, 4.4, w2, 1.6);
  src(s, "Source : Pacte National Énergétique (approuvé le 17/09/2025).");
}

// ---------- Section 2 ----------
const S2 = "Portefeuille PEZoR";
{
  const s = newSlide("CONTENT_ALT", S2, "LE PORTEFEUILLE DE RÉFÉRENCE", "Le PEZoR : 237 localités, dont 77 en mini-réseau et 160 en solaire domestique",
    "Un ménage potentiel n’est pas une connexion vérifiée.");
  [["MINI-RÉSEAUX VERTS (≥ 1 000 HAB.)", "77", "localités · 57 750 ménages · 41,71 MWc · 173,25 MWh · 308,83 MUSD"],
   ["SOLAIRE DOMESTIQUE (< 1 000 HAB.)", "160", "localités · 20 543 ménages · 33,12 MUSD"],
   ["MÉNAGES POTENTIELS", "78 293", "soit moins que les 79 000 branchements du Pacte"]]
    .forEach(([t, b, d], i) => card(s, M + i * (w3 + 0.3), 2.0, w3, 2.85, [P(s, "tag", t), P(s, "big", b, { fontSize: 40 }), P(s, "text", d)]));
  lead(s, "La règle « 1 000 habitants et plus → mini-réseau » est une pré-orientation : la technologie est arrêtée au moindre coût (G2). Les microcentrales restent une alternative.", 5.2, 1.0, 15);
  src(s, "Source : Annexe A2 du PEZoR (août 2026), sans doublon.");
}
{
  const s = newSlide("CONTENT", S2, "SÉQUENCE PEZoR", "Un pilote de 67 localités avant le Programme Cadre de 237",
    "Seules les connexions du pilote ont une chance raisonnable d’être vérifiées avant fin 2030.");
  table(s, [["Indicateur", "Phase pilote", "Programme Cadre"], ["Localités MRV / lots MRV", "37 / 7", "77 / 10"], ["Localités SSD / concessions", "30 / 6", "160 / 9"],
    ["Ménages MRV / SSD", "35 225 / 5 003", "57 750 / 20 543"], ["PV / stockage MRV", "25,44 MWc / 105,68 MWh", "41,71 MWc / 173,25 MWh"],
    ["CAPEX technique MRV + SSD", "186,92 + 8,24 MUSD", "308,83 + 33,12 MUSD"], ["Calendrier PEZoR", "Attribution 2028 S2, travaux 2029", "Appels d’offres 2030 S1"]],
    [4.5, 3.8, 3.833], 1.95, { right: [1, 2], fontSize: 14, rowH: 0.45 });
  lead(s, "Selon le PEZoR, le pilote est inclus dans le Programme Cadre ; 11 localités pilotes restent à rapprocher de la liste (Mission 0). Le Programme Cadre est conditionné à l’évaluation du pilote.", 5.4, 0.8, 15);
  src(s, "Source : PEZoR, ProDoc, pré-faisabilité et Annexe A2 (août 2026), sans doublon.");
}
{
  const s = newSlide("DARK", S2, "STATUT JURIDIQUE · VÉRIFIÉ", "Les 10 plus grands sites sont hors de la « zone rurale »",
    "Près de la moitié du CAPEX MRV porte sur des localités qui ne relèvent pas du régime rural. Leur régime juridique et leur statut électrique doivent être établis d’abord.");
  stat(s, M, 2.0, 5.0, "48,8 %", "du CAPEX des mini-réseaux, soit 150,6 MUSD, dans 10 sites", 44);
  txtBlock(s, [P(s, "text", "Décret 2017-250, article 1 : « la zone rurale est celle non comprise dans le périmètre des communes et des communautés urbaines ».", { fontSize: 15, color: HEX.onDark }),
    P(s, "text", "Le décret ne vise que le thermique de moins de 1 MW et l’hydraulique de moins de 5 MW ; le solaire n’y figure pas.", { fontSize: 14 })], M, 3.4, 5.4, 2.6);
  card(s, 6.6, 2.0, 6.133, 2.3, [P(s, "title", "Communes et communautés urbaines"), P(s, "text", "Communes : Ewo (loi 13-2017), Mossendjo (décret 2024-3). Communautés urbaines : Sembé, Souanké, Dongou, Loukolela, Etoumbi, Makabana, Komono, Epena (décrets 2020-125 et 2024-3)", { fontSize: 14 })]);
  card(s, 6.6, 4.5, 6.133, 1.7, [P(s, "title", "Conséquence"), P(s, "text", "Régime à établir (délégation, E2C ou modification des textes) avant les études détaillées", { fontSize: 14 })]);
  src(s, "Sources : décret 2017-250 (JO 30-2017) ; JO 2017-12, 2020-19, 2024-03 (sgg.cg). Traitement : Mission 0, puis Mission A.");
}
{
  const s = newSlide("CONTENT_ALT", S2, "77 LOCALITÉS MRV · 10 GRAPPES GÉOGRAPHIQUES INDICATIVES", "Deux grappes, Cuvette-Ouest et Niari, portent 41 % du CAPEX",
    "Le pilote compte 37 MRV sur 5 départements pour 7 lots prévus. L’allotissement définitif est arrêté par la Mission A.");
  hbar(s, { x: M, y: 1.9, w: 8.4, h: 4.75, labels: ["Cuvette-Ouest (11 sites)", "Niari (12)", "Lékoumou (14)", "Likouala (7)", "Pool (14)", "Cuvette (11)", "Sangha (3)", "Brazzaville (2)", "Kouilou (2)", "Bouenza (1)"],
    series: [{ name: "CAPEX technique (MUSD)", values: [64.64, 61.81, 40.21, 38.43, 31.66, 31.41, 30.90, 4.14, 3.71, 1.93] }], colors: [HEX.teal], title: "CAPEX technique par grappe (MUSD, total 308,83)", name: "CAPEX par grappe" });
  card(s, 9.4, 2.0, 3.333, 2.0, [P(s, "big", "41 %"), P(s, "text", "du CAPEX MRV dans les deux premières grappes")]);
  card(s, 9.4, 4.3, 3.333, 2.25, [P(s, "tag", "À REGROUPER"), P(s, "text", "Brazzaville, Kouilou et Bouenza : 5 sites, ≈ 10 MUSD, trop petits pour former des lots seuls")]);
  src(s, "Source : Annexe A2 du PEZoR, agrégée par département. Grappes indicatives, non des lots arrêtés.");
}
{
  const s = newSlide("CONTENT", S2, "160 LOCALITÉS SSD · 9 TERRITOIRES", "Neuf concessions solaires : un découpage à tester, pas à imposer",
    "Un distributeur PAYGo doit amortir un réseau de vente et de SAV. Demander aux PTF leur retour d’expérience sur les concessions et le RBF ouvert.");
  table(s, [["Territoire", "Localités", "Ménages", "MUSD"], ["Pool", "53", "8 027", "12,45"], ["Bouenza", "24", "3 342", "5,40"], ["Kouilou", "31", "3 119", "4,64"],
    ["Cuvette", "25", "2 058", "3,86"], ["Niari", "14", "1 809", "3,04"], ["Lékoumou", "8", "1 495", "2,61"], ["Cuvette-Ouest", "3", "298", "0,56"],
    ["Brazzaville", "1", "214", "0,30"], ["Pointe-Noire", "1", "181", "0,26"], ["Total", "160", "20 543", "33,12"]],
    [2.6, 1.3, 1.5, 1.4], 1.9, { right: [1, 2, 3], fontSize: 12, rowH: 0.4, totalRow: true, w: 6.8 });
  const x = 7.8, w = W - M - x;
  stat(s, x, 2.0, w, "2 283", "ménages en moyenne par territoire (médiane 1 809) ; trois territoires ne totalisent que 693 ménages", 34);
  txtBlock(s, [P(s, "tag", "QUATRE MODÈLES COMPARÉS (MISSION S)"), P(s, "text", "9 concessions · 3–4 zones · concession nationale · RBF ouvert à des opérateurs accrédités", { fontSize: 14, color: C.text1 })], x, 3.4, w, 1.4);
  txtBlock(s, [P(s, "tag", "CRITÈRE DE VIABILITÉ"), P(s, "text", "Clients actifs nécessaires = coûts fixes ÷ marge contributive par client", { fontSize: 14, color: C.text1 })], x, 4.9, w, 1.2);
  src(s, "Source : Annexe A2 du PEZoR ; segmentation par niveau de service (présentation PEZoR, diapositive 7 bis).");
}
{
  const s = newSlide("CONTENT_ALT", S2, "COMPOSANTE 2 · ENVELOPPE RECALCULÉE SANS DOUBLON", "≈ 431,5 MUSD d’investissement, dont 29 % de provisions sur les mini-réseaux",
    "Les provisions uniformes de 29 % sont remplacées par des coûts rendus site par site (Mission B). L’exonération n’est pas acquise.");
  bars(s, [["MRV, coût technique", 0, 308.83, HEX.teal, "308,83"], ["Provisions MRV", 308.83, 89.56, HEX.grey, "+ 89,56"], ["SSD", 398.39, 33.12, HEX.grey, "+ 33,12"],
    ["Enveloppe C2", 0, 431.51, HEX.amber, "431,5"]], 3.4, 2.0, 0.62, 8.0 / 431.51);
  txtBlock(s, [P(s, "tag", "DÉTAIL DES PROVISIONS (89,56 MUSD)"), P(s, "text", "Foncier 6,18 · taxes et douanes 24,71 · logistique 24,71 · E&S 6,18 · assurance 3,09 · contingence 24,71", { fontSize: 14, color: C.text1 })], M, 5.0, w2, 1.4);
  txtBlock(s, [P(s, "tag", "GAIN POTENTIEL"), P(s, "text", "24,7 MUSD de taxes provisionnés « sans exonération » : à éviter si l’exonération du Pacte devient effective.", { fontSize: 14, color: C.text1 })], M + w2 + 0.4, 5.0, w2, 1.4);
  src(s, "Méthode de la pré-faisabilité PEZoR (provisions de 29 % du coût technique MRV), appliquée aux 237 localités. Montants en MUSD.");
}
{
  const s = newSlide("CONTENT", S2, "STRUCTURE DE FINANCEMENT (RECALCULÉE)", "Le RBF couvre au plus 39,9 % de la C2 ; le privé n’est pas démontré",
    "L’écart au plafond n’est pas un déficit de viabilité. Le vrai déficit est calculé par lot par la Mission A.");
  [["180,5", "Basket Fund (PNUD) : 8,5 d’AT + 172,0 de RBF"], ["≈ 408,0", "Secteur privé : ≈ 259,5 sur la C2 + 148,5 sur la C3"], ["1,5", "Gouvernement : contrepartie"], ["≈ 590,0", "Total (MUSD)"]]
    .forEach(([b, t], i) => card(s, M + i * (w4 + 0.3), 2.0, w4, 1.6, [P(s, "big", b, { fontSize: 30 }), P(s, "text", t)]));
  s.addText("RBF : PLAFOND THÉORIQUE ET RESSOURCES PROVISIONNÉES (MUSD)", { x: M, y: 3.95, w: CW, h: 0.3, fontSize: 11, bold: true, charSpacing: 1, color: C.accent1, margin: 0, isTextBox: true });
  bars(s, [["Plafond de 50 % de la C2", 0, 215.8, HEX.grey, "215,8"], ["Provisionné", 0, 172.0, HEX.teal, "172,0"], ["Écart au plafond", 172.0, 43.8, HEX.amber, "43,8"]], 3.4, 4.4, 0.55, 7.5 / 215.8);
  src(s, "Cadre de résultats PEZoR : 319,0 MUSD privés (levier 1,77) ; structure recalculée : ≈ 408 MUSD (levier 2,26).");
}

// ---------- Section 3 ----------
const S3 = "Diagnostic de bancabilité";
{
  const s = newSlide("DARK", S3, "DIAGNOSTIC DE BANCABILITÉ", "Dix verrous à lever avant le premier appel d’offres",
    "Verrous 1 à 3 : Mission 0 ; 4 et 5 : Mission B ; 7 à 10 : Mission A ; solaire domestique : Mission S.");
  const items = [["1 · Données", "11 localités pilotes à rapprocher ; GPS manquants"], ["2 · Statut réseau", "7 chefs-lieux = 40,7 % du CAPEX MRV"], ["3 · Statut juridique", "10 plus grands sites hors « zone rurale »"], ["4 · Coût", "5 348 $ par ménage potentiel"], ["5 · Demande", "« 88 kWh/mois » = production répartie"],
    ["6 · Concentration", "10 sites = 48,8 % du CAPEX MRV"], ["7 · Viabilité", "Tarif = 22 % du coût ; privé non démontré"], ["8 · Instruments", "Ni régime, ni contrat type, ni tarif"], ["9 · Fiscalité", "25,4 MUSD de taxes provisionnés"], ["10 · Cohérence", "Privé : 319 ou ≈ 408 MUSD selon le document"]];
  const h = 2.15;
  items.forEach(([t, d], i) => card(s, M + (i % 5) * (w5 + 0.25), 2.0 + Math.floor(i / 5) * (h + 0.3), w5, h, [P(s, "title", t, { fontSize: 17 }), P(s, "text", d, { fontSize: 15 })]));
  src(s, "Sources : Annexe A2, pré-faisabilité et présentation PEZoR (août 2026) ; décret 2017-250 ; Pacte. Détail : TdR-cadre, § I.4.");
}
{
  const s = newSlide("CONTENT", S3, "VERROUS 4 ET 5 · COÛT ET DEMANDE", "Un mini-réseau coûte 5 348 USD par ménage : plus de 2,5 fois le repère international",
    "Le repère date de 2019 et provient d’une source secondaire : il doit être normalisé (année, kWc, kWh utile, réseau, logistique, fiscalité) avant toute conclusion.");
  hbar(s, { x: M, y: 1.95, w: 8.3, h: 3.4, stacked: true, legend: true, fmt: "#,##0;;", labels: ["Repère ESMAP 2019, bas", "Repère ESMAP 2019, haut", "SSD PEZoR (moyenne)", "MRV PEZoR, technique", "MRV PEZoR, avec provisions"],
    series: [{ name: "Repère international", values: [1000, 2100, 0, 0, 0] }, { name: "PEZoR", values: [0, 0, 1612, 5348, 6899] }], colors: [HEX.grey, HEX.amber], name: "Coût par connexion" });
  card(s, 9.3, 2.0, 3.433, 1.6, [P(s, "big", "× 2,5"), P(s, "text", "au-dessus de la borne haute du repère")]);
  card(s, 9.3, 3.8, 3.433, 1.55, [P(s, "big", "8 623 $"), P(s, "text", "par connexion réalisée si 80 % des ménages se raccordent")]);
  txtBlock(s, [P(s, "tag", "CONSTAT"), P(s, "text", "Les « 88 kWh/mois » sont la production répartie entre les ménages (60,9 GWh/an ÷ 57 750 ÷ 12), pas une demande mesurée.", { fontSize: 14, color: C.text1 })], M, 5.6, w2, 1.1);
  txtBlock(s, [P(s, "tag", "RÉPONSE"), P(s, "text", "Enquêtes stratifiées et comportements observés, dimensionnement modulaire à 3 ans, repère normalisé.", { fontSize: 14, color: C.text1 })], M + w2 + 0.4, 5.6, w2, 1.1);
  src(s, "USD par ménage. Sources : Annexe A2 et pré-faisabilité PEZoR ; repère ESMAP 2019 (source secondaire, Power for All).");
}
{
  const s = newSlide("CONTENT_ALT", S3, "VERROU 7 · TARIF", "Au tarif national, le mini-réseau ne couvre que 22 % de son coût",
    "À 0,35 USD/kWh, le PEZoR estime que l’exploitation devient autonome. La capacité de paiement n’est pas encore mesurée (Mission B).");
  hbar(s, { x: M, y: 1.95, w: 8.3, h: 4.6, fmt: "0.000", labels: ["Tarif national", "Tarif intermédiaire", "Tarif d’autonomie", "Diesel, combustible seul", "MRV, coût complet", "Diesel, coût complet rendu"],
    series: [{ name: "USD/kWh", values: [0.164, 0.25, 0.35, 0.55, 0.757, 1.05] }], colors: [HEX.teal], title: "USD/kWh (coût complet sur 20 ans)", name: "Tarifs et coûts" });
  card(s, 9.3, 2.0, 3.433, 1.45, [P(s, "big", "22 %"), P(s, "text", "du coût complet couvert par le tarif national")]);
  card(s, 9.3, 3.65, 3.433, 1.45, [P(s, "big", "≈ 96 %"), P(s, "text", "de subvention du capital à 0,25 $/kWh (PEZoR)")]);
  card(s, 9.3, 5.3, 3.433, 1.3, [P(s, "big", "0,35 $", { fontSize: 28 }), P(s, "text", "exploitation autonome (PEZoR)")]);
  src(s, "Source : présentation PEZoR, diapositive 25. Les pourcentages de subvention sont à recalculer à partir des flux de trésorerie (Mission A).");
}

// ---------- Section 4 ----------
const S4 = "Réponse proposée";
{
  const s = newSlide("CONTENT_ALT", S4, "LA RÉPONSE · SÉQUENCE PAR TRANCHES", "D’abord fiabiliser, puis deux filières en parallèle",
    "La filière rapide SSD répond à deux constats : le Pacte attend 90 % de la hausse rurale des systèmes autonomes, et les mini-réseaux ne livreront qu’une partie de leurs connexions avant 2030.");
  [["TRANCHE 0 · T1 2027", "Audit préalable", "Contrôle des localités, GPS, statut réseau et juridique (Mission 0, 4 mois)"], ["TRANCHE 1A · DÈS 2027", "Filière rapide SSD", "Marché, RBF ouvert, accréditation, installations (Mission S)"],
   ["TRANCHE 1B · 2027–2028", "Mini-réseaux pilotes", "Sites revalidés : APD, E&S, financement, passation"], ["TRANCHE 2 · 2030", "Programme Cadre", "Si financement confirmé et résultats intermédiaires"], ["TRANCHE 3", "Mise à l’échelle", "Selon l’évaluation indépendante du pilote"]]
    .forEach(([t, h, d], i) => card(s, M + i * (w5 + 0.25), 2.0, w5, 3.3, [P(s, "tag", t), P(s, "title", h, { fontSize: 17 }), P(s, "text", d, { fontSize: 14 })], i === 1 ? { border: HEX.amber, borderW: 3 } : {}));
  lead(s, "Une localité peut sortir du portefeuille sans remplacement. Le succès se mesure en connexions vérifiées, pas en nombre d’APD.", 5.7, 0.7, 15);
}
{
  const s = newSlide("CONTENT", S4, "CONTRIBUTION À LA CIBLE 2030 DU PACTE", "Le pilote couvre au mieux la moitié des 79 000 branchements",
    "Scénarios illustratifs, non probabilisés. Le programme retient provisoirement la lecture (b), qui justifie la filière rapide SSD.");
  hbar(s, { x: M, y: 1.9, w: 7.6, h: 4.3, fmt: "#,##0", labels: ["Pilote réalisé à 50 %", "Pilote réalisé à 70 %", "Pilote réalisé à 85 %", "Pilote réalisé à 100 %", "Cible du Pacte"],
    series: [{ name: "Connexions", values: [20114, 28160, 34194, 40228, 79000] }], colors: [HEX.teal], title: "Connexions potentielles du pilote et cible 2030", name: "Trajectoire" });
  card(s, 8.6, 2.0, 4.133, 2.2, [P(s, "title", "Décision requise du MEH"), P(s, "text", "(a) Le PEZoR révise le scénario du Pacte (90 % SSD / 10 % MRV), ou (b) il n’en est qu’un sous-portefeuille.")]);
  card(s, 8.6, 4.4, 4.133, 1.8, [P(s, "title", "Levier pour 2030"), P(s, "text", "La filière rapide SSD, indépendante du calendrier des mini-réseaux")]);
  src(s, "Mission 300 ne compte que les nouveaux accès de niveau MTF 1 ou plus. Le cadre de résultats PEZoR doit être recalé sur 78 293 ménages potentiels.");
}
{
  const s = newSlide("DARK", S4, "LA RÉPONSE PROPOSÉE", "Cinq missions de préparation, plus deux contrôles indépendants",
    "Les conflits d’intérêts couvrent les entités liées, les sous-traitants et les experts clés. L’ANER conserve toutes les décisions.");
  [["MISSION 0 · 0,36 MUSD", "Audit préalable", "Données, statut réseau et juridique. 4 mois"], ["MISSION S · 1,21 MUSD", "Filière rapide SSD", "Modèle, RBF, accréditation. 12 mois"],
   ["MISSION A · 2,84 MUSD", "Régulation et transaction", "Tarif, déficit de viabilité, contrats, passation"], ["MISSION B · 8,87 MUSD", "Études et EIES", "Demande, APD, finance, E&S, genre"], ["MISSION C · 2,19 MUSD", "UGP et données", "Manuels, plateforme, vérification"]]
    .forEach(([t, h, d], i) => card(s, M + i * (w5 + 0.25), 2.0, w5, 3.3, [P(s, "tag", t), P(s, "title", h, { fontSize: 17 }), P(s, "text", d, { fontSize: 14 })]));
  lead(s, "Contrôles indépendants : IVA (connexions RBF) et revue technique des APD et modèles (gérée par la Mission C). Titulaires distincts.", 5.7, 0.7, 15);
}
function mission(master, eyebrow, title, notes, cards, stats, source) {
  const s = newSlide(master, S4, eyebrow, title, notes);
  cards.forEach(([t, d], i) => card(s, M + i * (w3 + 0.3), 2.0, w3, 3.05, [P(s, "tag", t), P(s, "text", d, { fontSize: 16 })]));
  missionStats(s, stats);
  src(s, source);
}
mission("CONTENT", "MISSION 0 · AUDIT PRÉALABLE · 4 MOIS · ≈ 0,36 MUSD", "Un portefeuille fiable avant toute étude détaillée", "La Mission 0 conditionne le périmètre des Missions B et S. Elle peut être financée sur des ressources légères.",
  [["DONNÉES", "Contrôle des 237 localités, rapprochement des 11 localités pilotes, coordonnées WGS84, identifiant permanent"], ["STATUT ÉLECTRIQUE", "Localités vierges, centres isolés E2C, partiellement desservies ou raccordées ; priorité aux 10 plus grands sites"], ["STATUT JURIDIQUE", "Commune, communauté urbaine ou zone rurale ; régime d’autorisation ou de concession ; qualification du PAYGo"]],
  [["M2", "registre contrôlé et géoréférencé"], ["M4", "gate G0 : portefeuille revalidé"], ["6 + 10", "hommes-mois internationaux + nationaux"]],
  "Sélection sur qualifications ou consultants individuels ; livrables publiés dans les dossiers des autres missions.");
mission("CONTENT_ALT", "MISSION A · RÉGULATION, FINANCEMENT, TRANSACTION · ≈ 2,84 MUSD", "Démontrer le déficit de viabilité, puis contractualiser", "Les 50,5 MUSD ne sont qu’un écart au plafond de RBF ; le vrai déficit est à calculer avant d’annoncer 273 MUSD de capitaux privés.",
  [["CADRE FAVORABLE", "Régime des sites ruraux et urbains · méthode tarifaire (ARSEL) · arrivée du réseau · exonérations · fin de vie des batteries"], ["DÉFICIT DE VIABILITÉ", "Subvention minimale sous contraintes de TRI, DSCR et trésorerie · cinq architectures : concession, EPC et O&M, affermage, hybride, disponibilité"], ["PASSATION", "Dialogue de marché (au moins 20 entreprises) · critères multicritères · clauses contre les offres anormalement basses"]],
  [["M11", "déficit de viabilité et architecture par lot"], ["M26", "contrats pilotes signés (cible)"], ["77 + 28", "hommes-mois internationaux + nationaux"]],
  "Inclut un tableau emplois-ressources unique et l’analyse des engagements budgétaires de l’État. TdR-cadre, Partie III.");
mission("CONTENT", "MISSION B · ÉTUDES DE FAISABILITÉ, APD, EIES ET GENRE · ≈ 8,87 MUSD", "Des sites revalidés, étudiés jusqu’à la bancabilité technique", "Les études des 10 grands sites urbains ne sont engagées qu’après décision sur leur régime. Les données SSD vont à la Mission S.",
  [["DEMANDE", "Enquête stratifiée (au moins 100 ménages par site) · mesures de charge, préinscriptions, expériences de choix"], ["COÛTS", "APD à ± 15 % défini (cotations, date des prix, risques) · coûts rendus site par site · stress combinés"], ["E&S ET GENRE", "Matrice de conformité · NIES par localité · inventaires en deux saisons · indicateurs d’écarts femmes-hommes"]],
  [["M10–12", "G3a de la Tranche 1"], ["M15–17", "certificats environnementaux (G3b)"], ["125 + 156", "hommes-mois internationaux + nationaux"]],
  "Contrat mixte. Provision de 0,44 MUSD pour les 5 % de frais administratifs (circulaire du 16/10/2026). TdR détaillés.");
mission("CONTENT_ALT", "MISSION C · UGP, DONNÉES, VÉRIFICATION, REVUE INDÉPENDANTE · ≈ 2,19 MUSD", "Des capacités fiduciaires et des résultats vérifiables", "La revue technique indépendante (≈ 0,35 MUSD) contrôle les APD et modèles des Missions A et B avant les gates G3a.",
  [["GOUVERNANCE", "Instances, RACI, UGP à l’ANER · appui résident 18 mois · gabarits communs validés par le maître d’ouvrage"], ["DONNÉES", "Registre : potentiels, contrats, installations, connexions admissibles, personnes · trajectoire 2030 recalée"], ["VÉRIFICATION", "Protocole Mission 300 · règle anti-double financement · TdR de l’IVA · revue technique indépendante"]],
  [["M3", "gabarits communs validés"], ["M8", "protocole de vérification"], ["M9", "cadre de résultats recalé"]],
  "Le Pacte reconnaît à l’ANER des « capacités et mandats limités ». TdR-cadre, Partie V.");
mission("CONTENT", "MISSION S · FILIÈRE RAPIDE SOLAIRE DOMESTIQUE · 12 MOIS · ≈ 1,21 MUSD", "Des connexions solaires vérifiables avant 2030", "Les données des localités SSD viennent des enquêtes de la Mission B ; la Mission S les complète par une étude de marché.",
  [["MARCHÉ ET DEMANDE", "Opérateurs, prix rendus, mobile money ; moteur de coûts SSD reconstruit (31,4 ou 6,8 MWc à trancher)"], ["MODÈLE", "Quatre options : 9 concessions, 3–4 zones, concession nationale, RBF ouvert à des opérateurs accrédités"], ["RBF ET ACCRÉDITATION", "Montant par connexion et par niveau, primes territoriales et sociales, vérification, premières conventions"]],
  [["M5", "modèle de distribution recommandé"], ["M7", "manuel RBF et vérification"], ["M12", "premières conventions signées"]],
  "Le titulaire ne peut pas être accrédité comme opérateur. TdR-cadre, Partie VI.");
{
  const s = newSlide("CONTENT_ALT", S4, "GATES D’INVESTISSEMENT", "Bancabilité technique et autorisation d’engagement sont distinctes",
    "La bancabilité technique (G3a) précède l’autorisation d’engagement (G3b), qui suppose les certificats environnementaux et les non-objections.");
  const w6 = (CW - 1.25) / 6;
  [["G0", "Éligibilité", "Unique, géoréférencée ; statut réseau et juridique"], ["G1", "Terrain", "Foncier, données, communautés"], ["G2", "Moindre coût", "Technologie et niveau de service"],
   ["G3a", "Bancabilité", "APD, déficit de viabilité, EIES déposées"], ["G3b", "Engagement", "Certificats, non-objections, régime adopté"], ["G4", "Contrats", "Financement et contrats signés"]]
    .forEach(([g, t, d], i) => card(s, M + i * (w6 + 0.25), 2.0, w6, 3.0, [P(s, "num", g), P(s, "title", t, { fontSize: 16 }), P(s, "text", d, { fontSize: 14 })], (i === 3 || i === 4) ? { border: HEX.amber, borderW: 3 } : {}));
  lead(s, "Quatre étapes distinctes : acceptation technique du livrable (paiement du consultant), validation administrative, non-objection du bailleur, autorisation d’engagement.", 5.4, 0.9, 15);
  src(s, "Gates PEZoR, G3 scindé. G5 à G7 : construction, mise en service, performance.");
}
{
  const s = newSlide("CONTENT", S4, "CALENDRIER INTÉGRÉ · DÉMARRAGE CIBLE T1 2027", "Un audit de 4 mois, puis deux filières en parallèle",
    "Un retard de financement de la Mission 0 décale l’ensemble. La filière SSD est la seule à produire des connexions vérifiables dès 2028.");
  table(s, [["Période", "Mission 0", "Mission S", "Mission B", "Mission A"], ["M1–M4", "Audit, revalidation (G0)", "Marché (dès M3)", "Démarrage (M3), inventaires saison 1", "Diagnostic, emplois-ressources"],
    ["M5–M8", "–", "Modèle, RBF, protocole", "Enquêtes vague 1, E&S cadres", "Dialogue de marché, tarif, textes"], ["M9–M14", "–", "Accréditation, conventions", "APD, NIES : G3a (M12–14)", "Déficit de viabilité, DAO"],
    ["M15–M20", "–", "Installations vérifiées", "Certificats (G3b), vague 2", "Passation du pilote"], ["M21–M30", "–", "–", "Vague 2, rapport final", "Contrats pilotes (M26)"]],
    [1.4, 2.4, 2.6, 3.0, 2.733], 1.95, { fontSize: 13, rowH: 0.5 });
  lead(s, "Mission C en continu. Programme Cadre : appels d’offres en 2030 ; travaux 2030–2031.", 5.4, 0.5, 15);
  src(s, "Missions B et S démarrent au mois 3 sur les résultats intermédiaires de la Mission 0, pour ne pas perdre une saison sèche d’inventaires.");
}

// ---------- Section 5 ----------
const S5 = "Budget et financement";
{
  const s = newSlide("CONTENT_ALT", S5, "BUDGET DE LA PRÉPARATION", "≈ 15,5 MUSD, soit 3,6 % de l’enveloppe d’investissement",
    "Le ratio de 3,6 % n’est pas excessif pour un portefeuille dispersé, mais ne démontre pas l’efficience. Les postes de terrain sont des dépenses remboursables, sans double imputation.");
  hbar(s, { x: M, y: 1.9, w: 7.6, h: 3.0, fmt: "0.00", labels: ["Mission B", "Mission A", "Mission C", "Mission S", "Mission 0", "Provision 5 % (à confirmer)"],
    series: [{ name: "MUSD", values: [8.870, 2.839, 2.191, 1.211, 0.363, 0.444] }], colors: [HEX.teal], title: "MUSD, imprévus de 10 % inclus", name: "Budget par mission" });
  card(s, 8.6, 2.0, 4.133, 1.4, [P(s, "big", "≈ 15,9", { fontSize: 28 }), P(s, "text", "MUSD avec la provision")]);
  card(s, 8.6, 3.6, 4.133, 1.3, [P(s, "big", "265 + 278", { fontSize: 28 }), P(s, "text", "hommes-mois internationaux + nationaux")]);
  lead(s, "La Mission B (enquêtes, APD, EIES sur 77 localités MRV et 160 localités SSD) représente plus de la moitié du budget.", 5.2, 0.9, 14);
  src(s, "Estimation ascendante de l’auteur (TdR-cadre, § VII.5) : 25 000 $/mois international, 7 000 $/mois national ; non issue d’une cotation.");
}
{
  const s = newSlide("CONTENT", S5, "FINANCEMENT DE LA PRÉPARATION · SCÉNARIO À INSTRUIRE", "Scénario bas : un déficit d’environ 7,6 MUSD",
    "La séquence par tranches permet d’engager les missions au fur et à mesure : Mission 0 sur ressources légères, puis S et B (Tranche 1), puis B (Tranche 2).");
  table(s, [["Source", "MUSD", "Probabilité", "Prochaine décision"], ["BM / ESMAP (don)", "1,5 – 3,0", "Moyenne", "Équipe pays : fenêtre et mode d’exécution"],
    ["BAD / SEFA", "0 (base)", "Faible", "Fonds « à pleine capacité » : confirmation écrite"], ["Autres fonds BAD (AT, KOAFEC, facilité FAD)", "0,5 – 1,5", "Moyenne", "Requête formelle ; éligibilité à confirmer"],
    ["Avance de préparation BM", "jusqu’à 6", "Moyenne", "Opération identifiée (note conceptuelle)"], ["Basket Fund PEZoR (AT)", "1 – 2,5", "Moyenne", "Comité du fonds"],
    ["UE, FVC, FEM, AFD, OPEC Fund, IFC, PIDG, GEAPP", "0,3 – 1,5+", "À évaluer", "Prises de contact"]],
    [4.2, 1.5, 1.6, 4.833], 1.95, { right: [1], fontSize: 13, rowH: 0.5 });
  src(s, "Avances BM : 6 MUSD par opération, 10 pour certains projets (directive OPS5.03-DIR.117, 2023). Fourchette identifiée : 8,3 à 17,5 MUSD pour un besoin d’≈ 15,9 MUSD.");
}
{
  const s = newSlide("CONTENT_ALT", S5, "ARCHITECTURE FIDUCIAIRE · RECOMMANDATION PROVISOIRE", "Une architecture hybride : circuits distincts, règles communes",
    "Question directe aux PTF : cette architecture hybride est-elle recevable pour vos politiques de passation, de gestion financière et de sauvegardes ?");
  [["CIRCUITS DISTINCTS", "Chaque bailleur selon ses règles", "Opération BM · opération BAD · Basket Fund PNUD pour l’AT et les subventions autorisées"],
   ["ÉLÉMENTS COMMUNS", "Un seul programme", "Registre national, critères techniques, cadre de résultats, protocole de vérification"],
   ["GARDE-FOU", "Pas de double financement", "Aucune connexion financée par deux guichets RBF ; le manuel commun ne modifie pas les accords"]]
    .forEach(([t, h, d], i) => card(s, M + i * (w3 + 0.3), 2.0, w3, 3.3, [P(s, "tag", t), P(s, "title", h, { fontSize: 19 }), P(s, "text", d, { fontSize: 16 })]));
  lead(s, "À confirmer par des positions écrites de la BM, de la BAD et du PNUD (livrable A2, mois 3).", 5.7, 0.5, 15);
  src(s, "Écartés à ce stade : fonds commun intégral (négociations longues) ; cofinancement parallèle pur (coordination plus faible).");
}
{
  const s = newSlide("DARK", S5, "CE QUE NOUS DEMANDONS AUX PARTENAIRES", "Des demandes précises, partenaire par partenaire",
    "Aucune demande ne présume une réponse : il s’agit de recueillir des positions pour finaliser les TdR et le plan de financement.");
  const h = 2.15;
  [["Banque mondiale", "ESMAP pour les Missions 0 et S ; avance de préparation ; articulation avec PASEL ; règles Mission 300 pour le SSD"], ["BAD", "Voie recevable (SEFA ou autre fonds) ; facilité de préparation ; RBF au-delà de 50 % si le déficit est démontré ?"],
   ["PNUD", "Basket Fund pour la Mission 0 et l’AT ; acceptation de l’architecture hybride"], ["Union européenne", "GET.transform (régimes, tarif) ; Global Gateway pour la filière SSD"],
   ["Fonds climat, DFI, fondations", "FVC, FEM, AFD, OPEC Fund, IFC, PIDG, GEAPP : RBF SSD, usages productifs, garanties"], ["Tous", "Retours d’expérience ; revue E&S harmonisée ; financement anticipé d’une fenêtre SSD"]]
    .forEach(([t, d], i) => card(s, M + (i % 3) * (w3 + 0.3), 2.0 + Math.floor(i / 3) * (h + 0.3), w3, h, [P(s, "title", t, { fontSize: 19 }), P(s, "text", d, { fontSize: 15 })]));
}
{
  const s = newSlide("CONTENT", S5, "ENGAGEMENTS DU GOUVERNEMENT", "Huit décisions préalables, sans attendre le bouclage financier",
    "Le Gouvernement peut prendre ces décisions immédiatement, sans dépendre d’un financement.");
  const items = [["Trancher la réconciliation avec le Pacte", "Révision ou sous-portefeuille · mois 1"], ["Lancer la Mission 0", "Désigner récipiendaire et UGP · immédiat"], ["Revalider la liste", "Sur la base de la Mission 0 · mois 4"],
    ["Statuer sur le régime des 10 grands sites", "Communes et communautés urbaines · mois 4"], ["Saisir l’ARSEL", "Tarif hors réseau · mois 1"], ["Rendre l’exonération effective", "DGD, DGID · mois 3"],
    ["Évaluer l’espace budgétaire", "Avances, RBF, garanties · mois 3"], ["Décider du câblage intérieur", "≈ 150 $ par ménage · mois 6"]];
  const w = (CW - 0.5) / 2;
  items.forEach(([t, d], i) => {
    const x = M + (i % 2) * (w + 0.5), y = 1.95 + Math.floor(i / 2) * 1.12;
    s.addShape(pres.shapes.OVAL, { x, y: y + 0.05, w: 0.62, h: 0.62, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, objectName: "Pastille " + (i + 1) });
    s.addText(String(i + 1), { x, y: y + 0.05, w: 0.62, h: 0.62, align: "center", valign: "middle", fontSize: 18, bold: true, color: C.background1, margin: 0, isTextBox: true });
    txtBlock(s, [P(s, "title", t, { fontSize: 16 }), P(s, "text", d, { fontSize: 13 })], x + 0.8, y, w - 0.8, 0.95);
  });
  src(s, "Source : TdR-cadre, § I.7.");
}

// ---------- Section 6 ----------
const S6 = "Discussion";
{
  const s = newSlide("CONTENT_ALT", S6, "RISQUES DE LA PRÉPARATION", "Les principaux risques et leurs parades",
    "Trois risques se renforcent mutuellement : demande surestimée, tarif non approuvé et déficit de viabilité.");
  table(s, [["Risque", "Niveau", "Atténuation"], ["Statut urbain des 10 plus grands sites", "Certain", "Régime à établir (Mission 0, puis A) avant études"], ["Demande solvable surestimée", "Élevé", "Enquêtes stratifiées, mesures, conception modulaire"],
    ["Déficit de viabilité supérieur au RBF", "Élevé", "Calcul par lot ; architectures publiques ou hybrides"], ["Financement de la préparation tardif", "Élevé", "Mission 0 légère ; tranches conditionnelles"],
    ["Retards EIES (deux saisons, délais)", "Élevé", "Démarrage au M3 ; NIES par localité"], ["Capacités de l’ANER", "Élevé", "Appui résident ; évaluations des capacités"],
    ["Espace budgétaire et dette publique", "À confirmer", "Analyse avec les Finances"], ["Sécurité, logistique fluviale", "Élevé", "Plans HSE, évacuation, coûts rendus site"]],
    [4.6, 1.5, 6.033], 1.95, { fontSize: 13, rowH: 0.48 });
  src(s, "Registre complet : TdR-cadre, § VII.8 (16 risques).");
}
{
  const s = newSlide("ACCENT", S6, "QUESTIONS POUR LA DISCUSSION", "Six questions sur lesquelles nous attendons vos positions",
    "Recueillir les réponses dans une matrice qui distingue positions de principe, intentions et engagements.");
  const qs = ["La séquence (Mission 0, filière SSD, mini-réseaux) et les gates G3a / G3b conviennent-elles à vos procédures ?", "Quels dons et avances de préparation pouvez-vous mobiliser, et quand ?",
    "L’architecture fiduciaire hybride est-elle recevable pour vous ?", "Le RBF peut-il dépasser 50 % du CAPEX lorsque le déficit de viabilité est démontré ?",
    "Quelles règles Mission 300 pour le SSD et les centres E2C réhabilités ?", "Une fenêtre SSD peut-elle être financée avant la fin des études mini-réseaux ?"];
  const w = (CW - 0.6) / 2;
  qs.forEach((q, i) => s.addText([{ text: (i + 1) + ".  ", options: { bold: true } }, { text: q }], { x: M + (i % 2) * (w + 0.6), y: 2.05 + Math.floor(i / 2) * 1.45, w, h: 1.2, fontSize: 17, color: C.text2, margin: 0, valign: "top", isTextBox: true, objectName: "Question " + (i + 1) }));
}
{
  const s = newSlide("DARK", S6, "PROCHAINES ÉTAPES", "De la consultation au lancement des missions",
    "Les délais sont des propositions. La Mission 0 peut démarrer avant le bouclage de tous les financements.");
  [["IMMÉDIAT", "Mission 0", "Financement léger et lancement de l’audit préalable"], ["+ 2 SEMAINES", "Commentaires écrits", "Observations des PTF sur les TdR"],
   ["+ 2 MOIS", "Financements", "Requêtes déposées ; décision sur les avances de préparation"], ["MOIS 3–4", "Lancement S et B", "Sur la base des résultats de la Mission 0"]]
    .forEach(([t, h, d], i) => card(s, M + i * (w4 + 0.3), 2.1, w4, 2.9, [P(s, "tag", t), P(s, "title", h, { fontSize: 20 }), P(s, "text", d, { fontSize: 17 })]));
  lead(s, "Documents : TdR-cadre, TdR d’études, liste des sites et points à traiter, budget détaillé.", 5.5, 0.6, 15);
}

(async () => {
  const out = process.argv[2];
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("written", out);
})();
