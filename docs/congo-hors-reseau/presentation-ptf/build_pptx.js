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
pres.subject = "Préparation de 80 mini-réseaux verts et 9 concessions SSD – République du Congo";
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

// ============ SECTION 1 ============
const S1 = "Objet et Pacte";
{
  const s = newSlide("COVER", S1, null, null, "Ouverture. Objet : soumettre aux PTF les termes de référence (v1.0) de préparation bancable de la fenêtre hors réseau du PEZoR et recueillir leurs avis et intentions de financement. Les chiffres de portefeuille sont ceux de la pré-faisabilité PEZoR (août 2026) ; le budget de préparation (≈ 12,9 MUSD) est une estimation des TdR, non validée.");
  s._m = "COVER";
  s.addText("RÉPUBLIQUE DU CONGO · MINISTÈRE DE L’ÉNERGIE ET DE L’HYDRAULIQUE · ANER", { x: M, y: 0.7, w: CW, h: 0.35, fontSize: 12, bold: true, charSpacing: 2, color: C.accent2, margin: 0, isTextBox: true, objectName: "Surtitre" });
  s.addText("Électrification hors réseau : préparer 80 mini-réseaux verts et 9 concessions solaires bancables", { x: M, y: 1.2, w: 11.2, h: 1.9, fontSize: 36, bold: true, fontFace: THEME.headFontFace, color: C.background1, margin: 0, valign: "top", isTextBox: true, objectName: "Titre" });
  s.addText("Consultation des partenaires techniques et financiers sur les termes de référence de préparation des investissements du PEZoR, au service du Pacte National Énergétique (Mission 300)", { x: M, y: 3.2, w: 10.5, h: 1.0, fontSize: 16, color: HEX.onDarkMuted, margin: 0, valign: "top", isTextBox: true, objectName: "Sous-titre" });
  [["80", "mini-réseaux verts"], ["9", "concessions SSD"], ["80 322", "ménages ciblés"], ["≈ 12,9", "MUSD de préparation"]].forEach(([b, l], i) => stat(s, M + i * 2.45, 5.0, 2.3, b, l, 36));
  s.addText("Document de travail · novembre 2026\nVersion de consultation", { x: 10.0, y: 5.55, w: 2.73, h: 0.7, fontSize: 11, color: HEX.onDarkMuted, align: "right", margin: 0, isTextBox: true, objectName: "Date" });
}
{
  const s = newSlide("CONTENT", S1, "OBJET DE LA CONSULTATION", "Trois choses que nous attendons des partenaires aujourd’hui",
    "Cadrer la réunion : nous ne venons pas présenter un projet figé mais un projet de TdR à améliorer avec les PTF. Les trois attentes structurent la discussion finale.");
  const w = (CW - 0.6) / 3;
  [["1", "Valider l’approche", "Le périmètre aligné sur la pré-faisabilité, le découpage en trois missions et les gates d’investissement G0–G4."],
   ["2", "Financer la préparation", "≈ 12,9 MUSD de dons et d’avances de préparation : ESMAP, fonds gérés par la BAD dont le SEFA, avances adossées aux opérations, Basket Fund PEZoR, UE."],
   ["3", "Signaler les intentions d’investissement", "Positionnement sur le pilote (37 MRV, 6 concessions) et sur le Programme Cadre : prêts, dons, RBF, garanties."]]
    .forEach(([n, t, d], i) => card(s, M + i * (w + 0.3), 2.0, w, 3.3, [P(s, "num", n, { fontSize: 32 }), P(s, "title", t, { fontSize: 20 }), P(s, "text", d, { fontSize: 17 })]));
  lead(s, "Déroulé : contexte et portefeuille → diagnostic de bancabilité → réponse proposée → budget et financement → discussion.", 5.9);
}
{
  const s = newSlide("CONTENT", S1, "PACTE NATIONAL ÉNERGÉTIQUE · MISSION 300", "La cible rurale : de 1 % à 50 % d’accès en 2030",
    "Le Pacte mesure l’accès par les abonnés E2C (1,01 % en rural) ; les enquêtes WDI de la Banque mondiale donnent 19,4 % en 2024. La mission mesurera la situation de référence sur le terrain (MTF). Le point 90/10 est important : le PEZoR oriente beaucoup plus vers les mini-réseaux, ce qu’il faudra justifier par le moindre coût.");
  const w = (CW - 0.9) / 4;
  [["1,01 %", "accès rural de référence (abonnés E2C)"], ["50 %", "cible rurale 2030 (90 % en urbain, 81,3 % au niveau national)"], ["79 000", "nouveaux branchements ruraux, ≈ 500 000 personnes"], ["944 MUSD", "de besoins hors réseau : 606 pour les mini-réseaux, 338 pour les systèmes autonomes"]]
    .forEach(([b, t], i) => card(s, M + i * (w + 0.3), 2.0, w, 2.0, [P(s, "big", b, { fontSize: 30 }), P(s, "text", t)]));
  const w2 = (CW - 0.4) / 2;
  s.addText([P(s, "tag", "PRIORITÉ DU PACTE"), P(s, "text", "Les localités de plus de 1 000 habitants. Besoins financés à 50 % par le public et 50 % par le privé.", { fontSize: 15, color: C.text1 })], { x: M, y: 4.4, w: w2, h: 1.6, margin: 0, valign: "top", isTextBox: true });
  s.addText([P(s, "tag", "POINT À RÉCONCILIER"), P(s, "text", "Hypothèse du Pacte : 90 % de la hausse rurale par systèmes autonomes et 10 % par mini-réseaux, à confirmer par la Stratégie Nationale d’Électrification.", { fontSize: 15, color: C.text1 })], { x: M + w2 + 0.4, y: 4.4, w: w2, h: 1.6, margin: 0, valign: "top", isTextBox: true });
  src(s, "Sources : Pacte National Énergétique (approuvé en Conseil des ministres le 17/09/2025), mesure par les abonnés E2C ; enquêtes WDI : 19,4 % d’accès rural en 2024.");
}

// ============ SECTION 2 ============
const S2 = "Portefeuille PEZoR";
{
  const s = newSlide("CONTENT_ALT", S2, "LE PORTEFEUILLE DE RÉFÉRENCE", "Le PEZoR : 242 localités, dont 80 en mini-réseau et 162 en solaire domestique",
    "Ces chiffres sont strictement ceux de la pré-faisabilité. Un ménage retenu en pré-faisabilité n’est pas encore une connexion vérifiée au sens de Mission 300.");
  const w = (CW - 0.6) / 3;
  [["MINI-RÉSEAUX VERTS (≥ 1 000 HAB.)", "80", "localités · 59 467 ménages · 42,95 MWc de PV · 178,40 MWh de stockage · CAPEX technique de 317,61 MUSD"],
   ["SYSTÈMES SOLAIRES DOMESTIQUES (< 1 000 HAB.)", "162", "localités · 20 855 ménages · CAPEX de 33,62 MUSD · regroupées en 9 concessions territoriales"],
   ["ENSEMBLE DU PROGRAMME CADRE", "80 322", "ménages, soit 381 110 habitants, en 10 lots MRV et 9 concessions SSD ; à comparer aux 79 000 branchements ruraux du Pacte"]]
    .forEach(([t, b, d], i) => card(s, M + i * (w + 0.3), 2.0, w, 2.85, [P(s, "tag", t), P(s, "big", b, { fontSize: 40 }), P(s, "text", d)]));
  lead(s, "La règle « 1 000 habitants et plus → mini-réseau » est une pré-orientation : la technologie est arrêtée site par site au moindre coût (gate G2). Les microcentrales hydroélectriques restent une alternative, jamais cumulée au solaire.", 5.2, 1.0, 15);
  src(s, "Source : PEZoR, étude de pré-faisabilité et Annexe A2 (août 2026). Totaux recalculés site par site : concordants.");
}
{
  const s = newSlide("CONTENT", S2, "SÉQUENCE", "Un pilote de 67 localités avant le Programme Cadre de 242",
    "Conséquence pour Mission 300 : seules les connexions du pilote ont une chance raisonnable d’être vérifiées avant fin 2030. La contribution du Programme Cadre à la cible 2030 est incertaine et doit être présentée comme telle.");
  table(s, [["Indicateur", "Phase pilote", "Programme Cadre"],
    ["Localités MRV / lots MRV", "37 / 7", "80 / 10"], ["Localités SSD / concessions", "30 / 6", "162 / 9"],
    ["Ménages MRV / SSD", "35 225 / 5 003", "59 467 / 20 855"], ["PV / stockage MRV", "25,44 MWc / 105,68 MWh", "42,95 MWc / 178,40 MWh"],
    ["CAPEX technique MRV + SSD", "186,92 + 8,24 MUSD", "317,61 + 33,62 MUSD"], ["Calendrier PEZoR", "Attribution 2028 S2, travaux 2029", "Appels d’offres 2030 S1"]],
    [4.5, 3.8, 3.833], 1.95, { right: [1, 2], fontSize: 14, rowH: 0.45 });
  lead(s, "Les 67 localités pilotes sont incluses dans les 242 : les colonnes ne s’additionnent pas. Le lancement du Programme Cadre est conditionné à l’évaluation indépendante du pilote.", 5.4, 0.8, 15);
  src(s, "Source : PEZoR, ProDoc et pré-faisabilité (août 2026) ; présentation PEZoR, diapositives 15, 16 et 19.");
}
{
  const s = newSlide("CONTENT_ALT", S2, "80 MINI-RÉSEAUX · 10 DÉPARTEMENTS = 10 LOTS", "Deux grappes, Niari et Cuvette-Ouest, portent 43 % du CAPEX",
    "Le pilote compte 37 MRV sur 5 départements (Cuvette-Ouest, Niari, Lékoumou, Sangha, Pool) pour 7 lots prévus : au moins deux grappes, vraisemblablement Lékoumou et Cuvette-Ouest, seront scindées.");
  hbar(s, { x: M, y: 1.9, w: 8.4, h: 4.75, labels: ["Niari (14 sites)", "Cuvette-Ouest (12)", "Lékoumou (14)", "Likouala (7)", "Pool (14)", "Cuvette (11)", "Sangha (3)", "Brazzaville (2)", "Kouilou (2)", "Bouenza (1)"],
    series: [{ name: "CAPEX technique (MUSD)", values: [69.32, 65.91, 40.21, 38.43, 31.66, 31.41, 30.90, 4.14, 3.71, 1.93] }], colors: [HEX.teal], title: "CAPEX technique par grappe (MUSD, total 317,61)", name: "CAPEX par grappe" });
  card(s, 9.4, 2.0, 3.333, 2.0, [P(s, "big", "43 %"), P(s, "text", "du CAPEX MRV dans les deux premières grappes (135,2 MUSD)")]);
  card(s, 9.4, 4.3, 3.333, 2.25, [P(s, "tag", "À REGROUPER"), P(s, "text", "Brazzaville, Kouilou et Bouenza : 5 sites, ≈ 10 MUSD, trop petits pour former des lots attractifs seuls")]);
  src(s, "Source : Annexe A2 du PEZoR, agrégée par département. Correspondance départements–lots : observation de l’auteur, à confirmer par la Mission A.");
}
{
  const s = newSlide("CONTENT", S2, "9 CONCESSIONS SSD · 9 DÉPARTEMENTS", "Des concessions solaires trop petites pour un opérateur PAYGo",
    "Un distributeur PAYGo doit amortir un réseau de vente et de SAV : quelques centaines de clients par territoire ne suffisent pas. Demander aux PTF leur retour d’expérience sur les concessions SSD.");
  table(s, [["Territoire", "Localités", "Ménages", "MUSD"], ["Pool", "54", "8 251", "12,80"], ["Bouenza", "24", "3 342", "5,40"], ["Kouilou", "31", "3 119", "4,64"],
    ["Cuvette", "25", "2 058", "3,86"], ["Niari", "15", "1 897", "3,19"], ["Lékoumou", "8", "1 495", "2,61"], ["Cuvette-Ouest", "3", "298", "0,56"],
    ["Brazzaville", "1", "214", "0,30"], ["Pointe-Noire", "1", "181", "0,26"], ["Total", "162", "20 855", "33,62"]],
    [2.6, 1.3, 1.5, 1.4], 1.9, { right: [1, 2, 3], fontSize: 12, rowH: 0.4, totalRow: true, w: 6.8 });
  const x = 7.8, w = W - M - x;
  stat(s, x, 2.0, w, "≈ 2 300", "ménages en moyenne par concession ; moins de 300 dans trois territoires", 34);
  s.addText([P(s, "tag", "VARIANTES À TESTER"), P(s, "text", "(a) Concession élargie à tous les ménages hors réseau du territoire ; (b) regroupement des petits territoires.", { fontSize: 14, color: C.text1 })], { x, y: 3.35, w, h: 1.4, margin: 0, valign: "top", isTextBox: true });
  s.addText([P(s, "tag", "NIVEAUX 4 ET 5 (5 219 MÉNAGES)"), P(s, "text", "800 à 2 000 Wc par ménage : plutôt des nano-réseaux que des kits.", { fontSize: 14, color: C.text1 })], { x, y: 4.85, w, h: 1.2, margin: 0, valign: "top", isTextBox: true });
  src(s, "Source : Annexe A2 du PEZoR ; segmentation par niveau de service (présentation PEZoR, diapositive 7 bis). Pilote : 30 localités SSD sur 6 départements, soit 6 concessions.");
}
{
  const s = newSlide("CONTENT_ALT", S2, "COMPOSANTE 2 DU PEZoR", "445 MUSD d’investissement, dont 29 % de provisions sur les mini-réseaux",
    "Ne pas traiter l’exonération comme acquise : elle reste à opérationnaliser (procédure DGD/DGID, liste positive). C’est une tâche de la Mission A.");
  const x0 = 3.4, sc = 8.0 / 445;
  const rows = [["MRV, coût technique", 0, 317.61, HEX.teal, "317,61"], ["Provisions MRV", 317.61, 92.11, HEX.grey, "+ 92,11"], ["SSD", 409.72, 33.62, HEX.grey, "+ 33,62"],
    ["Marge de programmation", 443.34, 1.66, HEX.grey, "+ 1,66"], ["Enveloppe C2", 0, 445, HEX.amber, "445,0"]];
  rows.forEach(([l, b, v, c, lab], i) => {
    const y = 2.0 + i * 0.58;
    txt(s, l, M, y, 2.7, 0.4, { bold: i === 4 });
    hrect(s, x0 + b * sc, y + 0.04, Math.max(v * sc, 0.04), 0.32, c, "Barre " + l);
    txt(s, lab, x0 + (b + v) * sc + 0.1, y, 1.0, 0.4, { bold: true });
  });
  const w2 = (CW - 0.4) / 2;
  s.addText([P(s, "tag", "DÉTAIL DES PROVISIONS (92,11 MUSD)"), P(s, "text", "Foncier 6,35 · taxes et douanes 25,41 · logistique 25,41 · E&S 6,35 · assurance 3,18 · contingence 25,41", { fontSize: 14, color: C.text1 })], { x: M, y: 5.1, w: w2, h: 1.4, margin: 0, valign: "top", isTextBox: true });
  s.addText([P(s, "tag", "GAIN POTENTIEL"), P(s, "text", "Les 25,4 MUSD de taxes sont provisionnés « sans exonération ». L’exonération promise par le Pacte les éviterait, à condition qu’elle devienne effective.", { fontSize: 14, color: C.text1 })], { x: M + w2 + 0.4, y: 5.1, w: w2, h: 1.4, margin: 0, valign: "top", isTextBox: true });
  src(s, "Source : présentation PEZoR (août 2026), diapositives 9 et 10. Montants en MUSD.");
}
{
  const s = newSlide("CONTENT", S2, "STRUCTURE DE FINANCEMENT DU PEZoR", "Le RBF couvre au plus 38,7 % de la C2 ; 50,5 MUSD non sécurisés",
    "Message clé : le Basket Fund est un levier, pas le budget. Le RBF seul ne rend pas les mini-réseaux viables ; il faut aussi une méthode tarifaire décentralisée.");
  const w = (CW - 0.9) / 4;
  [["180,5", "Basket Fund (PNUD) : 8,5 d’AT + 172,0 de RBF"], ["421,5", "Secteur privé : 273,0 sur la C2 + 148,5 sur la C3"], ["1,5", "Gouvernement : contrepartie"], ["603,5", "Total (MUSD) : 1,77 $ privé par $ concessionnel"]]
    .forEach(([b, t], i) => card(s, M + i * (w + 0.3), 2.0, w, 1.6, [P(s, "big", b, { fontSize: 30 }), P(s, "text", t)]));
  s.addText("RBF : PLAFOND THÉORIQUE ET RESSOURCES PROVISIONNÉES (MUSD)", { x: M, y: 3.95, w: CW, h: 0.3, fontSize: 11, bold: true, charSpacing: 1, color: C.accent1, margin: 0, isTextBox: true });
  const x0 = 3.4, sc = 7.5 / 222.5;
  [["Plafond de 50 % du CAPEX", 0, 222.5, HEX.grey, "222,5"], ["Provisionné", 0, 172.0, HEX.teal, "172,0"], ["Écart non sécurisé", 172.0, 50.5, HEX.amber, "50,5"]]
    .forEach(([l, b, v, c, lab], i) => { const y = 4.4 + i * 0.55; txt(s, l, M, y, 2.7, 0.4); hrect(s, x0 + b * sc, y + 0.04, v * sc, 0.32, c, "Barre " + l); txt(s, lab, x0 + (b + v) * sc + 0.1, y, 1.0, 0.4, { bold: true }); });
  src(s, "Source : présentation PEZoR, diapositives 20 à 22. Incohérence à corriger : le ProDoc donne 423,0 MUSD d’apport privé et une C3 de 153 MUSD.");
}

// ============ SECTION 3 ============
const S3 = "Diagnostic de bancabilité";
{
  const s = newSlide("DARK", S3, "DIAGNOSTIC DE BANCABILITÉ", "Huit verrous à lever avant le premier appel d’offres",
    "Chaque verrou correspond à une tâche identifiée dans les TdR. Les verrous 1 et 2 sont liés : si la demande réelle est plus faible que supposé, un dimensionnement modulaire réduit le CAPEX par connexion.");
  const items = [["1 · Coût par connexion", "5 341 USD par ménage MRV (coût technique)"], ["2 · Demande", "0,72 kWc et ≈ 88 kWh/mois par ménage, non mesurés"], ["3 · Concentration", "10 sites = 47 % du CAPEX MRV"], ["4 · Tarif", "Le tarif national couvre ≈ 22 % du coût complet"],
    ["5 · Écart de RBF", "50,5 MUSD non sécurisés"], ["6 · Instruments juridiques", "Ni licence, ni concession, ni tarif, ni clause d’arrivée du réseau"], ["7 · Fiscalité", "25,4 MUSD de taxes, exonération non effective"], ["8 · Données", "Doublons, sites raccordés, capacité SSD à 31,4 ou 6,8 MWc"]];
  const w = (CW - 0.9) / 4, h = 2.15;
  items.forEach(([t, d], i) => card(s, M + (i % 4) * (w + 0.3), 2.0 + Math.floor(i / 4) * (h + 0.3), w, h, [P(s, "title", t, { fontSize: 20 }), P(s, "text", d, { fontSize: 17 })]));
  src(s, "Sources : pré-faisabilité et présentation PEZoR (août 2026) ; Pacte National Énergétique ; GET.transform (sept. 2026). Détail dans les TdR, § I.4.");
}
{
  const s = newSlide("CONTENT", S3, "VERROUS 1 ET 2 · COÛT PAR CONNEXION", "Un mini-réseau coûte 5 341 USD par ménage : plus de 2,5 fois le repère international",
    "Le repère international date de 2019 et provient d’une source secondaire ; la comparaison donne un ordre de grandeur, pas une conclusion. Les coûts congolais intègrent la logistique, le stockage d’une journée et ≈ 1 300 km de réseau BT, mais l’écart justifie une revue critique du dimensionnement.");
  hbar(s, { x: M, y: 1.95, w: 8.3, h: 3.4, stacked: true, legend: true, fmt: "#,##0;;", labelColor: HEX.ink,
    labels: ["Repère ESMAP 2019, bas", "Repère ESMAP 2019, haut", "SSD PEZoR (moyenne)", "MRV PEZoR, technique", "MRV PEZoR, rebasé"],
    series: [{ name: "Repère international", values: [1000, 2100, 0, 0, 0] }, { name: "PEZoR", values: [0, 0, 1612, 5341, 6890] }], colors: [HEX.grey, HEX.amber], name: "Coût par connexion" });
  card(s, 9.3, 2.0, 3.433, 1.6, [P(s, "big", "× 2,5"), P(s, "text", "au-dessus de la borne haute du repère (MRV, coût technique)")]);
  card(s, 9.3, 3.8, 3.433, 1.55, [P(s, "big", "0,72 kWc"), P(s, "text", "par ménage, sur une demande non mesurée")]);
  const w2 = (CW - 0.4) / 2;
  s.addText([P(s, "tag", "HYPOTHÈSE À TESTER"), P(s, "text", "0,72 kWc et ≈ 88 kWh/mois par ménage, dimensionnés sur une demande non mesurée.", { fontSize: 14, color: C.text1 })], { x: M, y: 5.6, w: w2, h: 1.1, margin: 0, valign: "top", isTextBox: true });
  s.addText([P(s, "tag", "RÉPONSE DES TdR"), P(s, "text", "Enquêtes de demande obligatoires, dimensionnement modulaire à 3 ans et cible de coût par connexion fixée au mois 6.", { fontSize: 14, color: C.text1 })], { x: M + w2 + 0.4, y: 5.6, w: w2, h: 1.1, margin: 0, valign: "top", isTextBox: true });
  src(s, "USD par ménage. Sources : Annexe A2 et pré-faisabilité PEZoR. Repère ESMAP 2019 : source secondaire (Power for All), à confirmer sur le rapport ESMAP 2022.");
}
{
  const s = newSlide("CONTENT_ALT", S3, "VERROU 4 · TARIF", "Au tarif national, le mini-réseau ne couvre que 22 % de son coût",
    "À 0,35 USD/kWh, le PEZoR estime que l’exploitation devient autonome, pour un prix inférieur d’un tiers au coût complet du diesel. La capacité de paiement des ménages n’a pas encore été mesurée : c’est l’objet des enquêtes de la Mission B.");
  hbar(s, { x: M, y: 1.95, w: 8.3, h: 4.6, fmt: "0.000", labels: ["Tarif national", "Tarif intermédiaire", "Tarif d’autonomie", "Diesel, prix à la pompe", "MRV, coût complet", "Diesel, coût complet rendu"],
    series: [{ name: "USD/kWh", values: [0.164, 0.25, 0.35, 0.55, 0.757, 1.05] }], colors: [HEX.teal], title: "USD/kWh (coût complet sur 20 ans)", name: "Tarifs et coûts" });
  card(s, 9.3, 2.0, 3.433, 1.45, [P(s, "big", "22 %"), P(s, "text", "du coût complet couvert par le tarif national (0,164 $)")]);
  card(s, 9.3, 3.65, 3.433, 1.45, [P(s, "big", "≈ 96 %"), P(s, "text", "de subvention du capital nécessaire à 0,25 $/kWh")]);
  card(s, 9.3, 5.3, 3.433, 1.3, [P(s, "big", "0,35 $", { fontSize: 28 }), P(s, "text", "exploitation autonome (81 % de subvention du capital)")]);
  src(s, "Source : présentation PEZoR, diapositive 25. Diesel complet ≈ 1,05 $ (≈ 0,55 $ à la pompe) : à confirmer par relevés de terrain. Le RBF plafonné à 50 % ne suffit pas sans méthode tarifaire décentralisée.");
}

// ============ SECTION 4 ============
const S4 = "Réponse proposée";
{
  const s = newSlide("DARK", S4, "LA RÉPONSE PROPOSÉE", "Trois missions de préparation, plus une vérification indépendante",
    "Pourquoi trois contrats plutôt qu’un : séparer le conseil transactionnel de l’ingénierie limite les conflits d’intérêts et le risque de capacité, et permet à chaque bailleur de financer la mission qui correspond à ses instruments.");
  const w = (CW - 0.9) / 4;
  [["MISSION A · ≈ 3,1 MUSD", "Conseil réglementaire, financier et transactionnel", "Cadre favorable, RBF, requêtes de dons, passation et bouclage financier du pilote. Composantes 1, 3 et 4."],
   ["MISSION B · ≈ 8,0 MUSD", "Ingénierie, faisabilité, APD, EIES", "80 MRV et 162 localités SSD amenés au gate G3, plus usages productifs et genre. Composantes 2 et 6."],
   ["MISSION C · ≈ 1,8 MUSD", "Gestion du programme et données", "UGP, manuels, plateforme géoréférencée, protocole de vérification. Composantes 5 et 7."],
   ["IVA · CONTRAT SÉPARÉ", "Vérification indépendante", "Vérifie les connexions qui déclenchent le RBF et le comptage Mission 300."]]
    .forEach(([t, h, d], i) => card(s, M + i * (w + 0.3), 2.0, w, 3.5, [P(s, "tag", t), P(s, "title", h, { fontSize: 19 }), P(s, "text", d, { fontSize: 16 })]));
  lead(s, "Conflits d’intérêts : A et B exclues des marchés en aval · A et B à des titulaires distincts · C distinct de l’IVA.", 5.85, 0.6, 15);
}
function missionSlide(master, eyebrow, title, notes, cards, stats, source) {
  const s = newSlide(master, S4, eyebrow, title, notes);
  const w = (CW - 0.6) / 3;
  cards.forEach(([t, h, d], i) => card(s, M + i * (w + 0.3), 2.0, w, 3.05, h ? [P(s, "tag", t), P(s, "title", h, { fontSize: 20 }), P(s, "text", d, { fontSize: 16 })] : [P(s, "tag", t), P(s, "text", d, { fontSize: 16 })]));
  stats.forEach(([b, l], i) => stat(s, M + i * (w + 0.3), 5.35, w, b, l, 26));
  src(s, source);
}
missionSlide("CONTENT", "MISSION A · CONSEIL RÉGLEMENTAIRE, FINANCIER ET TRANSACTIONNEL", "Rendre l’investissement privé possible, puis le contractualiser",
  "Hypothèses critiques que la Mission A doit tester : appétit réel des opérateurs, tarif approuvable et payable, suffisance du RBF lot par lot, viabilité des 9 concessions, choix du modèle contractuel.",
  [["ENVIRONNEMENT FAVORABLE", null, "Régime d’autorisation et de concession (décret 2017-250, article 51) · méthode tarifaire avec l’ARSEL · arrivée du réseau · exonérations · fin de vie des batteries · coordination avec GET.transform et PASEL"],
   ["FINANCEMENT", null, "Plan de financement par lot · manuel RBF (montant par connexion vérifiée) · requêtes ESMAP, BAD et autres · contributions aux documents de projet BM et BAD · garanties, change, carbone · table ronde"],
   ["PASSATION", null, "PPSD et plans de passation · dialogue de marché (au moins 20 entreprises) · DAO et contrat type · critère dominant : subvention par connexion · bouclage financier de 7 lots et 6 concessions"]],
  [["85 + 28", "hommes-mois internationaux + nationaux"], ["M24", "contrats pilotes signés (cible)"], ["M30", "DAO du Programme Cadre prêts à publier"]],
  "Paiement par livrable : 12 livrables (A0–A11), chacun avec un critère d’acceptation. Détail dans les TdR, Partie II.");
missionSlide("CONTENT_ALT", "MISSION B · INGÉNIERIE, FAISABILITÉ, APD, EIES", "Des sites prêts à être financés, en deux vagues",
  "Règle d’alignement : un site écarté au G0 (doublon, raccordement au réseau) est remplacé par un site de réserve validé par le comité de pilotage, pour maintenir 80 MRV et 162 localités SSD. Sinon, révision formelle de la cible.",
  [["VAGUE 1 · PILOTE · M1–M10", "37 MRV et 30 localités SSD", "Contrôle G0 et liste de réserve · enquêtes de demande et MTF · moindre coût · APD à ± 15 % · modèles financiers · PGES"],
   ["VAGUE 2 · CADRE · M11–M22", "43 MRV et 132 localités SSD", "Mêmes livrables, avec les configurations types et les enseignements de la vague 1"],
   ["TRANSVERSAL", "E&S et inclusion", "Instruments E&S cadres communs BM/BAD · usages productifs · câblage intérieur · plus de 51 % de femmes"]],
  [["123 + 120", "hommes-mois internationaux + nationaux"], ["≥ 100", "ménages enquêtés par site MRV"], ["≥ 12", "MRV de réserve pour maintenir la cible de 80"]],
  "Option : deux lots géographiques, Sud et Nord, avec une méthode commune. Détail dans les TdR, Partie III.");
missionSlide("CONTENT", "MISSION C · GESTION DU PROGRAMME, DONNÉES, VÉRIFICATION", "Des capacités fiduciaires et des résultats vérifiables",
  "Le protocole de vérification est la base du RBF et du comptage Mission 300 : un ménage retenu en pré-faisabilité n’est pas une connexion vérifiée.",
  [["GOUVERNANCE", null, "Comité de pilotage, comité technique et d’investissement, UGP à l’ANER articulée avec l’UGPNE · évaluations des capacités et plans d’action · appui résident pendant 18 mois"],
   ["MANUELS ET RAPPORTS", null, "Manuel d’exécution · procédures financières et comptables · manuel E&S · PTBA · rapports aux formats des bailleurs · TdR des audits"],
   ["DONNÉES ET VÉRIFICATION", null, "Plateforme géoréférencée des 242 localités · interfaces avec la télésurveillance et le PAYGo · définition de la connexion vérifiée · TdR de l’IVA"]],
  [["28 + 66", "hommes-mois internationaux + nationaux"], ["M6", "manuels soumis à non-objection"], ["M9", "protocole de vérification validé"]],
  "Le Pacte reconnaît à l’ANER des « capacités et mandats limités » : l’appui de la Mission C conditionne l’exécution. Détail dans les TdR, Partie IV.");
{
  const s = newSlide("CONTENT_ALT", S4, "GATES D’INVESTISSEMENT (PEZoR)", "Aucun engagement avant le gate G3",
    "Le gate G3 est le moment où les PTF émettent leur non-objection : c’est le point de rendez-vous de cette consultation.");
  const w = (CW - 1.0) / 5;
  [["G0", "Éligibilité", "Ni doublon, ni site raccordé ; remplacement par la réserve", "Comité de pilotage"], ["G1", "Terrain", "Foncier, coordonnées, engagement des communautés", "Comité technique"],
   ["G2", "Moindre coût", "Technologie et niveau de service arrêtés, site par site", "Comité d’investissement"], ["G3", "Bancabilité", "APD, modèle financier, E&S, régime réglementaire, contrat type", "Non-objection des PTF"],
   ["G4", "Engagement", "Financement, autorisations, contrats signés", "Gouvernement et PTF"]]
    .forEach(([g, t, d, who], i) => card(s, M + i * (w + 0.25), 2.0, w, 3.2, [P(s, "num", g), P(s, "title", t), P(s, "text", d), P(s, "tag", who)], i === 3 ? { border: HEX.amber, borderW: 3, name: "Carte G3" } : {}));
  lead(s, "Les gates s’alignent sur le cycle de projet des bailleurs : identification, préparation et évaluation pour la BAD ; note conceptuelle, évaluation et Conseil pour la BM. Aujourd’hui, les 242 sites sont tous au gate G0.", 5.5, 0.9, 15);
  src(s, "Source : PEZoR, gates G0 à G7 (G5 à G7 : construction, mise en service, performance). Les MCHE suivent leurs propres gates, H0 à H6.");
}
{
  const s = newSlide("CONTENT", S4, "CALENDRIER INTÉGRÉ", "Démarrage au premier trimestre 2027, contrats pilotes en 2028 S2",
    "Un retard au démarrage (financement de la préparation non disponible au premier trimestre 2027) décale mécaniquement l’ensemble et réduit encore la contribution à la cible 2030.");
  table(s, [["Période", "Mission B", "Mission A", "Gate"], ["M1–M2", "G0, liste de réserve", "Diagnostic juridique, dialogue de marché", "G0"], ["M3–M7", "Enquêtes vague 1, E&S cadres", "Architecture fiduciaire, textes, tarif", "G1–G2 pilote"],
    ["M8–M10", "APD vague 1", "RBF, requêtes de dons", "G3 pilote"], ["M11–M18", "Enquêtes vague 2", "DAO, préqualification, évaluation", "–"], ["M19–M24", "APD vague 2", "Négociation, bouclage financier du pilote", "G4 pilote, G3 Cadre"], ["M25–M30", "Rapport final", "Dossiers du Programme Cadre", "–"]],
    [1.8, 3.4, 4.4, 2.533], 1.95, { fontSize: 13, rowH: 0.42 });
  const w = (CW - 0.6) / 3;
  [["2029", "Travaux du pilote ; évaluation indépendante"], ["2030 S1", "Appels d’offres du Programme Cadre"], ["2030 S2 – 2031", "Travaux et mises en service"]]
    .forEach(([t, d], i) => s.addText([P(s, "tag", t), P(s, "text", d, { fontSize: 14, color: C.text1 })], { x: M + i * (w + 0.3), y: 5.25, w, h: 1.0, margin: 0, valign: "top", isTextBox: true }));
  src(s, "Mission C : continue sur toute la période (instances au M2, manuels au M6, vérification au M9). Calendrier aligné sur la présentation PEZoR, diapositive 19.");
}

// ============ SECTION 5 ============
const S5 = "Budget et financement";
{
  const s = newSlide("CONTENT_ALT", S5, "BUDGET DE LA PRÉPARATION", "≈ 12,9 MUSD, soit 2,9 % de l’enveloppe d’investissement",
    "Le terrain de la Mission B (enquêtes de 80 MRV et 162 localités SSD, levés, logistique fluviale) est le premier poste. Une réduction passe par la sous-traitance nationale des enquêtes et le découpage en deux lots géographiques.");
  hbar(s, { x: M, y: 1.9, w: 7.6, h: 2.5, fmt: "0.00", labels: ["Mission B", "Mission A", "Mission C"], series: [{ name: "MUSD", values: [7.965, 3.114, 1.806] }], colors: [HEX.teal], title: "MUSD, imprévus de 10 % inclus", name: "Budget par mission" });
  s.addText([P(s, "tag", "PÉRIMÈTRE"), P(s, "text", "Hors IVA en exploitation, ingénieur-conseil de supervision des travaux et fonctionnement de l’UGP au-delà de 18 mois.", { fontSize: 14, color: C.text1 })], { x: 8.6, y: 2.0, w: 4.133, h: 2.2, margin: 0, valign: "top", isTextBox: true });
  const w = (CW - 0.6) / 3;
  [["236", "hommes-mois internationaux, à 25 000 USD par mois (hypothèse)"], ["214", "hommes-mois nationaux, à 7 000 USD par mois (hypothèse)"], ["≈ 3,3", "MUSD de coûts de terrain : enquêtes, levés, logistique"]]
    .forEach(([b, t], i) => card(s, M + i * (w + 0.3), 4.65, w, 1.6, [P(s, "big", b, { fontSize: 28 }), P(s, "text", t)]));
  src(s, "MUSD. Estimation ascendante des TdR v1.0 (§ V.5) : hypothèses de l’auteur, non issues d’une cotation. Le client doit établir une estimation confidentielle.");
}
{
  const s = newSlide("CONTENT", S5, "FINANCEMENT DE LA PRÉPARATION · SCÉNARIO À INSTRUIRE", "Les dons ne suffiront pas : la Mission B dépend d’avances de préparation",
    "Message clé : sans décision sur une avance de préparation adossée à une opération d’investissement, la Mission B (≈ 8 MUSD) ne peut pas être financée intégralement. Les dons ESMAP et SEFA servent au mieux l’environnement favorable, le RBF, les données et une partie de la vague 1.");
  table(s, [["Source", "Missions visées", "MUSD", "Point à confirmer"], ["BM / ESMAP (don)", "A (cadre), C, B (vague 1)", "1,5 – 3,0", "Fenêtre, mode d’exécution"],
    ["BAD / SEFA (don)", "A, B (usages productifs)", "0 – 1,0", "Se déclarait « à pleine capacité » (nov. 2026)"], ["Autres fonds gérés par la BAD", "A, B", "0,5 – 1,5", "Précédent de 1,5 MUSD en 2025"],
    ["Avances de préparation BM et BAD", "B, A (passation), C", "5 – 8", "Décision d’engager une opération"], ["Basket Fund PEZoR (AT)", "C, A", "1 – 2,5", "Éviter le double financement"],
    ["UE, SEforALL, FEM, FVC", "A, B", "0,3 – 1,5", "GET.transform : appui en nature"], ["Gouvernement", "Personnel, locaux", "En nature", "À formaliser"]],
    [3.6, 2.9, 1.5, 4.133], 1.95, { right: [2], fontSize: 13, rowH: 0.48 });
  src(s, "Aucun montant n’est confirmé. Sources : page SEFA de la BAD (consultée en nov. 2026) ; communiqué BAD de février 2025 ; TdR v1.0, § V.5.3.");
}
{
  const s = newSlide("CONTENT_ALT", S5, "ARCHITECTURE FIDUCIAIRE · À ARBITRER AU MOIS 3", "Comment articuler le Basket Fund du PNUD et les opérations BAD et BM ?",
    "Question directe aux PTF : quelles options sont compatibles avec vos politiques (passation, gestion financière, sauvegardes) ? Leur réponse conditionne l’option retenue.");
  const w = (CW - 0.6) / 3;
  [["1", "Cofinancement parallèle", "Chaque bailleur finance des lots identifiés selon ses règles, sur un cadre de résultats, un manuel et une vérification communs.", "Simple pour chaque bailleur ; coordination exigeante"],
   ["2", "Guichet RBF national", "Une facilité unique de subvention au résultat, logée au FDSEL ou à l’ANER ou confiée à un gestionnaire indépendant, alimentée par plusieurs bailleurs.", "Lisible pour les opérateurs ; capacités à bâtir"],
   ["3", "Combinaison", "Le Basket Fund reçoit les dons et l’AT ; les prêts BAD et BM restent hors du fonds.", "Valorise l’existant ; deux circuits à gérer"]]
    .forEach(([n, t, d, k], i) => card(s, M + i * (w + 0.3), 2.0, w, 3.6, [P(s, "num", n), P(s, "title", t, { fontSize: 20 }), P(s, "text", d, { fontSize: 16 }), P(s, "tag", k)]));
  lead(s, "Acquis PEZoR : chaque contributeur garde la non-objection sur ses seules ressources. Ce n’est pas un droit de veto général.", 5.9, 0.6, 15);
  src(s, "Livrable A2 des TdR : note d’options validée par le comité de pilotage, avec avis écrits de la BAD et de la BM.");
}
{
  const s = newSlide("DARK", S5, "CE QUE NOUS DEMANDONS AUX PARTENAIRES", "Des demandes précises, partenaire par partenaire",
    "Aucune de ces demandes ne présume une réponse : il s’agit de recueillir des positions pour finaliser les TdR et le plan de financement.");
  const w = (CW - 0.6) / 3, h = 2.15;
  [["Banque mondiale", "Don ESMAP pour l’environnement favorable et les données ; avance de préparation ; articulation avec PASEL (SEN, plan au moindre coût)"],
   ["BAD", "Recevabilité du SEFA ou autre fonds d’AT ; facilité de préparation ; intérêt pour des lots pilotes ; garanties partielles"],
   ["PNUD", "Articulation du Basket Fund (8,5 MUSD d’AT, 172 MUSD de RBF) avec les opérations BAD et BM"],
   ["Union européenne", "Coordination GET.transform sur la réglementation et la tarification ; financements Global Gateway"],
   ["Fonds climat et fondations", "FVC, FEM, SEforALL, GEAPP : RBF, usages productifs, réduction des risques"],
   ["Tous", "Retours d’expérience sur les concessions et le RBF ; harmonisation E&S et de la vérification"]]
    .forEach(([t, d], i) => card(s, M + (i % 3) * (w + 0.3), 2.0 + Math.floor(i / 3) * (h + 0.3), w, h, [P(s, "title", t, { fontSize: 20 }), P(s, "text", d, { fontSize: 16 })]));
}
{
  const s = newSlide("CONTENT", S5, "ENGAGEMENTS DU GOUVERNEMENT", "Six décisions préalables, sans attendre le bouclage financier",
    "Signal fort pour les PTF : le Gouvernement peut prendre ces décisions immédiatement, sans dépendre d’un financement.");
  const items = [["Revalider la liste des 242 localités", "Résoudre les 10 doublons signalés · avant le mois 2"], ["Désigner le récipiendaire et l’UGP", "ANER, en lien avec l’UGPNE · avant le mois 1"],
    ["Saisir l’ARSEL sur le tarif hors réseau", "Méthode tarifaire décentralisée · mois 1"], ["Rendre l’exonération effective", "Mandat aux Finances (DGD, DGID) · mois 3"],
    ["Décider du câblage intérieur", "≈ 150 USD par ménage, barrière d’accès · mois 6"], ["Autoriser le dialogue de marché", "Consultation des opérateurs · mois 2"]];
  const w = (CW - 0.5) / 2;
  items.forEach(([t, d], i) => {
    const x = M + (i % 2) * (w + 0.5), y = 2.0 + Math.floor(i / 2) * 1.2;
    s.addShape(pres.shapes.OVAL, { x, y: y + 0.05, w: 0.7, h: 0.7, fill: { color: C.accent1 }, line: { color: C.accent1, width: 0 }, objectName: "Pastille " + (i + 1) });
    s.addText(String(i + 1), { x, y: y + 0.05, w: 0.7, h: 0.7, align: "center", valign: "middle", fontSize: 20, bold: true, color: C.background1, margin: 0, isTextBox: true });
    s.addText([P(s, "title", t), P(s, "text", d, { fontSize: 14 })], { x: x + 0.9, y, w: w - 0.9, h: 1.0, margin: 0, valign: "top", isTextBox: true, objectName: "Décision " + (i + 1) });
  });
  lead(s, "Ces décisions montrent l’engagement du pays et conditionnent le calendrier de toutes les missions.", 5.75, 0.5, 15);
  src(s, "Source : TdR v1.0, § I.7 ; décisions à valider avec l’ANER (présentation PEZoR, annexe).");
}

// ============ SECTION 6 ============
const S6 = "Discussion";
{
  const s = newSlide("CONTENT_ALT", S6, "RISQUES DE LA PRÉPARATION", "Les principaux risques et leurs parades",
    "Trois risques se renforcent mutuellement : coût par connexion élevé, tarif non approuvé et écart de RBF. Ensemble, ils déterminent l’appétit du secteur privé.");
  table(s, [["Risque", "Niveau", "Atténuation"], ["Financement de la préparation insuffisant", "Élevé", "Plusieurs sources, vagues, avances de préparation"],
    ["Textes non adoptés avant les DAO", "Élevé", "Démarrage au M1, coordination avec GET.transform, DAO conditionnels"], ["Coût par connexion trop élevé, faible appétit privé", "Élevé", "Ingénierie de la valeur, modèle hybride (distribution publique)"],
    ["Capacités limitées de l’ANER", "Élevé", "Appui résident, plans d’action, dispositions fiduciaires adaptées"], ["Extension du réseau vers des sites retenus", "Moyen", "Gate G0, liste de réserve, clause d’arrivée du réseau"],
    ["Exigences BM et BAD divergentes", "Moyen", "Instruments communs, norme la plus exigeante, revues conjointes"], ["Règle « ≥ 1 000 hab. » contestée face au 90/10 du Pacte", "Moyen", "Notes de moindre coût par site, réconciliation avec la SEN"]],
    [4.6, 1.2, 6.333], 1.95, { fontSize: 13, rowH: 0.5 });
  src(s, "Source : TdR v1.0, § V.8. Boko et Louingui (MRV du pilote) raccordées au réseau selon la presse de juillet 2026 : à confirmer au gate G0.");
}
{
  const s = newSlide("ACCENT", S6, "QUESTIONS POUR LA DISCUSSION", "Six questions sur lesquelles nous attendons vos positions",
    "Recueillir les réponses dans une matrice qui distingue positions de principe, intentions et engagements. Elles alimenteront la version finale des TdR et la table ronde des bailleurs.");
  const qs = ["Le périmètre (80 MRV, 9 concessions) et les gates conviennent-ils à vos procédures d’évaluation ?", "Quelles sources de don et d’avance de préparation pouvez-vous mobiliser, et dans quels délais ?",
    "Quelle option fiduciaire est compatible avec vos politiques ?", "Quel montant de RBF par connexion et quelle dégressivité jugez-vous défendables ?",
    "Quel modèle contractuel privilégier : concession privée, conception-construction-exploitation ou hybride ?", "Quels lots du pilote ou du Programme Cadre souhaitez-vous financer ?"];
  const w = (CW - 0.6) / 2;
  qs.forEach((q, i) => s.addText([{ text: (i + 1) + ".  ", options: { bold: true } }, { text: q }], { x: M + (i % 2) * (w + 0.6), y: 2.05 + Math.floor(i / 2) * 1.45, w, h: 1.2, fontSize: 17, color: C.text2, margin: 0, valign: "top", isTextBox: true, objectName: "Question " + (i + 1) }));
}
{
  const s = newSlide("DARK", S6, "PROCHAINES ÉTAPES", "De la consultation au lancement des missions",
    "Les délais sont des propositions de calendrier, à ajuster avec les PTF. Le démarrage au premier trimestre 2027 est nécessaire pour tenir le calendrier PEZoR (contrats pilotes en 2028 S2).");
  const w = (CW - 0.9) / 4;
  [["+ 2 SEMAINES", "Commentaires écrits", "Les PTF transmettent leurs observations sur les TdR v1.0"], ["+ 1 MOIS", "TdR finaux", "Version consolidée et plan de financement de la préparation"],
   ["+ 2 MOIS", "Accords de don", "Requêtes ESMAP, BAD et autres déposées ; décision sur les avances de préparation"], ["T1 2027", "Lancement", "Sélection et démarrage des Missions B et C, puis de la Mission A"]]
    .forEach(([t, h, d], i) => card(s, M + i * (w + 0.3), 2.1, w, 2.9, [P(s, "tag", t), P(s, "title", h, { fontSize: 20 }), P(s, "text", d, { fontSize: 17 })]));
  lead(s, "Documents disponibles : TdR v1.0, liste des 80 MRV avec alertes, budget détaillé, cadre de résultats de la préparation.", 5.5, 0.6, 15);
}

(async () => {
  const out = process.argv[2];
  await pres.writeFile({ fileName: out });
  await applyTheme(out, THEME);
  console.log("written", out);
})();
