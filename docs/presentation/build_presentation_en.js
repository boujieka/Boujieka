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
pres.title = "Cameroon mineral flows 2000–2025";
pres.author = "Boujieka research";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const FOOT = "Cameroon mineral flows · 2000–2025 · mirror data and public sources";

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
const fr = (x, d = 1) => x.toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d });
const chartBase = () => ({
  catAxisLabelColor: H.dk2, valAxisLabelColor: H.dk2, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  catAxisLabelFontSize: 11, valAxisLabelFontSize: 11, dataLabelFontFace: "+mn-lt", dataLabelFontSize: 10, dataLabelColor: H.dk1,
  valGridLine: { color: "E2DDD4", size: 0.5 }, catGridLine: { style: "none" }, titleFontFace: "+mj-lt", titleColor: H.dk1, titleFontSize: 14,
  legendFontFace: "+mn-lt", legendFontSize: 11, legendColor: H.dk2,
});

// ===== 1. Titre
section("Introduction");
let s = pres.addSlide({ masterName: "TITRE_SOMBRE", sectionTitle: cur() });
s.addText("Where does Cameroon's gold go?", { placeholder: "title" });
s.addText("Declared and actual mineral flows, 2000–2025: gold, diamonds, cobalt, iron, manganese, bauxite", { placeholder: "body" });
s.addText("Desk research · version 2, revised after audit · data as of 31 October 2026", { x: 0.8, y: 6.5, w: 8, h: 0.4, fontSize: 14, color: C.accent4, margin: 0, isTextBox: true });
s.addNotes("Findings: UN Comtrade mirror analysis (all reporters) for gold; desk research for the five other minerals.");

// ===== 2. L'essentiel
s = content("Key message: gold is almost everything");
const stats = [
  ["138.5 t", "of unwrought gold (HS 7108) reported by partners as coming from Cameroon, 2000–2025; 2024–2025 partial (no UAE data)"],
  ["USD 6.58 bn", "declared value, ≈ FCFA 3,744 bn (World Bank exchange rates)"],
  ["FCFA 577.5 bn", "revenue shortfall 2021–2025 estimated by the Ministry of Mines: published figure, not independently verified"],
];
stats.forEach((st, i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.8, 3.3, "Key figure " + (i + 1));
  s.addText(st[0], { x: x + 0.3, y: 1.9, w: 3.2, h: 1.2, fontSize: 32, bold: true, color: i === 2 ? C.accent2 : C.accent5, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
  s.addText(st[1], { x: x + 0.3, y: 3.15, w: 3.2, h: 1.5, fontSize: 15, color: C.text1, margin: 0, valign: "top", isTextBox: true });
});
s.addText([
  { text: "Takeaway: ", options: { bold: true, color: C.accent2 } },
  { text: "Cameroon reports a few kilograms of gold exports per year while its partners report tonnes. Diamonds, cobalt, iron, manganese and bauxite show no comparable gap: flows are small or absent." },
], { x: 0.6, y: 5.2, w: 12.1, h: 1.1, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true });
caption(s, "Sources: UN Comtrade (HS 7108, partner Cameroon, 254 reporters, regional aggregates excluded); World Bank; MINMIDT via Sikafinance (07/2026). Line-by-line detail: annexes A1–A3.");

// ===== 3. Méthode
s = content("Method: compare what leaves with what arrives");
const steps = [
  ["What arrives", "Imports \"from Cameroon\" reported by 254 countries in UN Comtrade (mirror data)"],
  ["What leaves", "Exports reported by Cameroon itself (Comtrade, EITI, customs, Kimberley Process)"],
  ["The gap, costed", "Value in USD and FCFA, comparison with the world gold price, tax regime of each period"],
];
steps.forEach((st, i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.8, 2.9, "Step " + (i + 1));
  circleNum(s, i + 1, x + 0.3, 1.85, 0.7);
  s.addText(st[0], { x: x + 1.15, y: 1.85, w: 2.5, h: 0.7, fontSize: 20, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  s.addText(st[1], { x: x + 0.3, y: 2.75, w: 3.2, h: 1.6, fontSize: 15, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  if (i < 2) s.addShape(pres.shapes.CHEVRON, { x: x + 3.86, y: 2.9, w: 0.18, h: 0.32, fill: { color: C.accent1 }, line: { type: "none" }, objectName: "Arrow " + (i + 1) });
});
card(s, 0.6, 4.8, 12.1, 1.6, "Sources");
s.addText([
  { text: "Sources used: ", options: { bold: true } },
  { text: "UN Comtrade, World Bank (exchange rates, gold price), EITI Cameroon, MINMIDT, Sonamines, Kimberley Process, USGS, UN Panel of Experts, specialist press." , options: { breakLine: true } },
  { text: "Limitation: ", options: { bold: true, color: C.accent2 } },
  { text: "only gold could be analysed with the full Comtrade database; the other minerals rely on web search excerpts." },
], { x: 0.9, y: 4.95, w: 11.5, h: 1.35, fontSize: 15, color: C.text1, valign: "middle", margin: 0, isTextBox: true });

// ===== 4. Section or
section("Gold");
s = pres.addSlide({ masterName: "SECTION_SOMBRE", sectionTitle: cur() });
s.addText("Gold: 138 tonnes reported abroad", { placeholder: "title" });
s.addText("Charts: unwrought gold HS 7108 only. Scrap (HS 7112) and jewellery (HS 7113) are treated separately and never added", { placeholder: "body" });

// ===== 5. Volumes annuels
s = content("Volumes surge after 2009 and peak in 2023");
const yrs = years.filter(y => y >= 2000);
s.addChart(pres.charts.BAR, [
  { name: "Complete series", labels: yrs.map(String), values: yrs.map(y => y >= 2024 ? 0 : +(data[y].kg / 1000).toFixed(1)) },
  { name: "Partial: UAE not published", labels: yrs.map(String), values: yrs.map(y => y >= 2024 ? +(data[y].kg / 1000).toFixed(1) : 0) },
], {
  x: 0.6, y: 1.4, w: 8.4, h: 5.0, barDir: "col", barGrouping: "stacked", chartColors: [H.accent1, H.accent4], showLegend: true, legendPos: "b",
  showTitle: true, title: "Unwrought gold (HS 7108) reported \"from Cameroon\", tonnes",
  showValue: false, valAxisMinVal: 0, catAxisLabelRotate: -45, ...chartBase(), objectName: "Gold volumes chart",
});
card(s, 9.3, 1.4, 3.4, 5.0, "Volumes comment");
s.addText([
  { text: "2000–2008", options: { bold: true, breakLine: true } },
  { text: "Under 0.4 t per year", options: { breakLine: true } },
  { text: "2013–2019", options: { bold: true, breakLine: true } },
  { text: "≈ 10 to 11.7 t per year, almost all to the UAE", options: { breakLine: true } },
  { text: "2023", options: { bold: true, breakLine: true } },
  { text: "Record: 18.3 t, USD 1.15 bn", options: { breakLine: true } },
  { text: "2024–2025", options: { bold: true, color: C.accent2, breakLine: true } },
  { text: "Partial: UAE data not published (withdrawn from Comtrade, per SWISSAID). These are not totals." },
], { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 14, color: C.text1, valign: "top", margin: 0, paraSpaceAfter: 4, isTextBox: true });
caption(s, "Source: UN Comtrade, extracted 31/10/2026. Sum of rounded bars: 138.2 t; exact total: 138.5 t. Sonamines: ≈ 12.2 t in Dubai in 2024, unverified.");

// ===== 6. Destinations
s = content("UAE: 80.3% of recorded volumes (2024–25 incomplete)");
const dest = [["United Arab Emirates", 111.3], ["Rwanda", 16.0], ["Uganda", 7.7], ["Germany", 1.9], ["United States", 0.55], ["Belgium", 0.42], ["Switzerland", 0.31], ["South Korea", 0.22]].reverse();
s.addChart(pres.charts.BAR, [{ name: "Cumulative 2000–2025 (t)", labels: dest.map(d => d[0]), values: dest.map(d => d[1]) }], {
  x: 0.6, y: 1.4, w: 7.6, h: 5.0, barDir: "bar", chartColors: [H.accent5], showLegend: false,
  showTitle: true, title: "Gold reported as received from Cameroon, cumulative 2000–2025 (tonnes)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0", ...chartBase(), objectName: "Destinations chart",
});
const facts6 = [
  ["111.3 t", "UAE, 2004–2023 (USD 4.81 bn); series confirmed by Interpol for 2010–2018"],
  ["16.0 t", "Rwanda, 2019–2025: a new regional relay"],
  ["7.7 t", "Uganda, 2023–2025"],
];
facts6.forEach((f, i) => {
  const y = 1.5 + i * 1.6;
  card(s, 8.5, y, 4.2, 1.4, "Destination fact " + (i + 1));
  s.addText(f[0], { x: 8.75, y: y + 0.15, w: 3.8, h: 0.6, fontSize: 26, bold: true, color: C.accent5, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
  s.addText(f[1], { x: 8.75, y: y + 0.75, w: 3.8, h: 0.55, fontSize: 14, color: C.text1, margin: 0, isTextBox: true });
});
caption(s, "UN Comtrade, HS 7108. The 8 countries shown total 138.37 t; the remaining 0.13 t: Spain 0.11 t, Italy, Saudi Arabia, Israel, France, Türkiye… No regional aggregate included.");

// ===== 6b. Cameroon-UAE
s = content("Cameroon–UAE: twenty years of declared gold flows");
const uy = years.filter(y => y >= 2004 && y <= 2023);
s.addChart(pres.charts.BAR, [{ name: "UAE (t)", labels: uy.map(String), values: uy.map(y => +(decl[y].eau / 1000).toFixed(2)) }], {
  x: 0.6, y: 1.4, w: 7.9, h: 5.0, barDir: "col", chartColors: [H.accent5], showLegend: false,
  showTitle: true, title: "Unwrought gold imports reported by the UAE from Cameroon (t)",
  valAxisMinVal: 0, catAxisLabelRotate: -45, ...chartBase(), objectName: "UAE annual chart",
});
const per = [[2004, 2009], [2010, 2014], [2015, 2019], [2020, 2023]];
const phd = ["Period", "Reported by UAE"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const prow = per.map(([a, b]) => { let t = 0; for (let y = a; y <= b; y++) t += decl[y].eau; return [a + "–" + b, fr(t / 1000, 3) + " t"]; });
prow.push(["2004–2023", fr(111.273, 3) + " t"], ["2024–2025", "Not published"]);
s.addTable([phd, ...prow.map((r, i) => r.map(c => ({ text: c, options: { bold: i === 4, color: H.dk1 } })))], {
  x: 8.8, y: 1.5, w: 3.9, colW: [1.8, 2.1], fontSize: 14, fontFace: THEME.bodyFontFace, rowH: 0.5,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "UAE periods table",
});
s.addText("These are UAE import declarations, not documented purchases from Cameroonian producers.", { x: 8.8, y: 5.25, w: 3.9, h: 1.1, fontSize: 14, italic: true, color: C.text2, valign: "top", margin: 0, isTextBox: true });
caption(s, "Source: UN Comtrade, HS 7108, reporter 784 (UAE), partner 120 (Cameroon), net weight. Subtotals computed on unrounded values.");

// ===== 7. Ecart
s = content("A few kilograms declared out, tonnes declared in");
const hdr = ["Year", "Exported per Cameroon", "Received per partners", "Ratio"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const tbl = [
  ["2013", "214 kg", "11,490 kg", "× 54"],
  ["2018", "13 kg", "11,712 kg", "× 900"],
  ["2021", "40 kg (73 kg per EITI)", "5,602 kg", "× 140"],
  ["2022", "3.5 kg (47.9 kg per EITI)", "4,820 kg", "× 1,380"],
  ["2023", "22.3 kg (EITI); 20 kg to the UAE (WITS)", "18,255 kg (UAE only: 14,048 kg)", "× 820 (UAE: × 702)"],
];
s.addTable([hdr, ...tbl.map(r => r.map((c, j) => ({ text: c, options: { bold: j === 3, color: j === 3 ? H.accent2 : H.dk1 } })))], {
  x: 0.6, y: 1.5, w: 12.1, colW: [1.6, 4.3, 3.8, 2.4], fontSize: 16, fontFace: THEME.bodyFontFace, rowH: 0.62,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "Gap table",
});
card(s, 0.6, 5.4, 12.1, 1.0, "Gap reading");
s.addText("The \"received ÷ exported\" ratio runs into the hundreds: most of the gold leaves outside declared channels, or is attributed to Cameroon while originating elsewhere.", { x: 0.9, y: 5.45, w: 11.5, h: 0.9, fontSize: 15, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
caption(s, "Same HS code 7108 and same unit (net kg) on both sides. Sources: UN Comtrade/WITS (X and M flows), EITI 2021–2023 via the press. 2023 ratio based on EITI.");

// ===== 8. Recoupement ITIE
s = content("EITI and Comtrade match, once the scope is stated");
const itie = [
  ["2021", "5.6 t", "5.60 t", "UAE 4.81 t + Rwanda 0.79 t"],
  ["2022", "4.8 t", "4.82 t", "UAE 4.71 t + Rwanda 0.11 t"],
  ["2023", "15.2 t", "15.19 t", "Scope UAE 14.05 t + Uganda 1.14 t. All reporters: 18.26 t (slide 7), as Rwanda (3.06 t) is added"],
];
itie.forEach((r, i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.8, 4.6, "Cross-check " + r[0]);
  s.addText(r[0], { x: x + 0.3, y: 1.8, w: 3.2, h: 0.6, fontSize: 24, bold: true, color: C.text1, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
  s.addText("EITI", { x: x + 0.3, y: 2.55, w: 1.5, h: 0.35, fontSize: 13, color: C.accent4, margin: 0, isTextBox: true });
  s.addText(r[1], { x: x + 0.3, y: 2.9, w: 1.6, h: 0.7, fontSize: 30, bold: true, color: C.accent5, margin: 0, isTextBox: true });
  s.addText("Comtrade", { x: x + 2.0, y: 2.55, w: 1.6, h: 0.35, fontSize: 13, color: C.accent4, margin: 0, isTextBox: true });
  s.addText(r[2], { x: x + 2.0, y: 2.9, w: 1.6, h: 0.7, fontSize: 30, bold: true, color: C.accent3, margin: 0, isTextBox: true });
  s.addText(r[3], { x: x + 0.3, y: 3.9, w: 3.2, h: 2.1, fontSize: 15, color: C.text1, valign: "top", margin: 0, isTextBox: true });
});
caption(s, "The exact scope used by EITI is not published: the match is an inference. Uganda 2023: 1,144.7 net kg (Comtrade) vs 1,117 kg (WITS, quantity).");

// ===== 8b. Vérifications externes
s = content("What external checks confirm");
const ihd = ["Year", "Comtrade, UAE (t)", "Interpol 2021, UAE (t)"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const iy = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018];
const ivals = { 2010: "2.37", 2011: "3.53", 2012: "4.98", 2013: "9.57", 2014: "8.67", 2015: "10.42", 2016: "9.94", 2017: "10.90", 2018: "11.70" };
s.addTable([ihd, ...iy.map(y => [String(y), fr(decl[y].eau / 1000, 2), ivals[y]].map(c => ({ text: c, options: { color: H.dk1 } })))], {
  x: 0.6, y: 1.45, w: 6.0, colW: [1.4, 2.3, 2.3], fontSize: 14, fontFace: THEME.bodyFontFace, rowH: 0.48,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "Interpol table",
});
const vf = [
  ["Interpol 2021", "UAE series 2010–2018 identical to Comtrade, up to rounding. In 2017: 4 kg declared by Cameroon to the UAE vs 10.9 t received"],
  ["WITS 2023", "UAE 14,048 kg (USD 879.7 M), Rwanda 3,060 kg, Uganda 1,117 kg; Cameroon declares 20 kg to the UAE"],
  ["SWISSAID 2025", "UAE 2024 data were posted then withdrawn from Comtrade \"for verification\": 2024–2025 remain partial"],
];
vf.forEach((f, i) => {
  const y = 1.45 + i * 1.7;
  card(s, 6.9, y, 5.8, 1.55, "Check " + (i + 1));
  s.addText(f[0], { x: 7.15, y: y + 0.12, w: 5.3, h: 0.4, fontSize: 16, bold: true, color: C.accent3, margin: 0, isTextBox: true });
  s.addText(f[1], { x: 7.15, y: y + 0.52, w: 5.3, h: 0.95, fontSize: 13, color: C.text1, valign: "top", margin: 0, isTextBox: true });
});
caption(s, "Sources: INTERPOL, Illegal Gold Mining in Central Africa (2021); WITS/UN Comtrade (external check, 31/10/2026); SWISSAID press release of 04/11/2025 and Swissinfo.");

// ===== 9. Ecart au cours
s = content("Declared values track the world gold price");
const ey = years.filter(y => y >= 2005);
s.addChart(pres.charts.LINE, [{ name: "Gap (%)", labels: ey.map(String), values: ey.map(y => data[y].ecart) }], {
  x: 0.6, y: 1.4, w: 8.4, h: 5.0, chartColors: [H.accent2], lineSize: 2.5, lineDataSymbol: "circle", lineDataSymbolSize: 7,
  showLegend: false, showTitle: true, title: "Gap between declared value and weight × LBMA price (%)",
  valAxisMinVal: -20, valAxisMaxVal: 10, valAxisMajorUnit: 5, catAxisLabelRotate: -45, ...chartBase(), objectName: "Price gap chart",
});
card(s, 9.3, 1.4, 3.4, 5.0, "Gap comment");
s.addText([
  { text: "± 8%", options: { bold: true, fontSize: 26, color: C.accent5, breakLine: true } },
  { text: "Most years: declared weights are near-pure gold", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "–11 to –15%", options: { bold: true, fontSize: 26, color: C.accent2, breakLine: true } },
  { text: "2016–2020 and 2024–2025: doré declared at gross weight, or low Rwandan values (hypotheses)" },
], { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
caption(s, "Sources: UN Comtrade; World Bank Pink Sheet (LBMA PM average; spot price from June 2025).");

// ===== 10. Couts fiscaux
s = content("Tax losses: estimates, not demonstrated");
const fy = [2021, 2022, 2023, 2024, 2025];
const pub = { 2021: 52.81, 2022: 50.55, 2023: 161.79, 2024: 159.15, 2025: 153.2 };
const eiti = { 2021: 0, 2022: 0, 2023: 165, 2024: 0, 2025: 0 };
s.addChart(pres.charts.BAR, [
  { name: "Low scenario: ad valorem tax only", labels: fy.map(String), values: fy.map(y => +(data[y].lo / 1e9).toFixed(1)) },
  { name: "High scenario: ISML 25% + export duty", labels: fy.map(String), values: fy.map(y => +(data[y].hi / 1e9).toFixed(1)) },
  { name: "MINMIDT series 2021–2025 (577.5 total)", labels: fy.map(String), values: fy.map(y => pub[y]) },
  { name: "EITI estimate, 2023", labels: fy.map(String), values: fy.map(y => eiti[y]) },
], {
  x: 0.6, y: 1.4, w: 8.4, h: 5.0, barDir: "col", barGrouping: "clustered", chartColors: [H.accent6, H.accent1, H.accent2, H.accent3],
  showLegend: true, legendPos: "b", showTitle: true, title: "Potential revenue shortfall on unreconciled gold (FCFA bn)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0;-0;;", ...chartBase(), objectName: "Tax loss chart",
});
card(s, 9.3, 1.4, 3.4, 5.0, "Loss comment");
s.addText([
  { text: "A risk, not a proven loss", options: { bold: true, fontSize: 18, color: C.accent2, breakLine: true } },
  { text: "The high scenario assumes all the gold is Cameroonian and falls under the semi-mechanised regime (ISML: 25% in kind on gross output). Neither origin nor regime is established.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "Two distinct 2023 estimates: FCFA 161.8 bn (MINMIDT) and 165 bn (EITI). The MINMIDT web page of 24/07/2026 cites 557 bn instead of 577.5: to be reconciled.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true } },
  { text: "2024–2025: excluding the UAE", options: { italic: true } },
], { x: 9.55, y: 1.6, w: 2.95, h: 4.6, fontSize: 13, color: C.text1, valign: "top", margin: 0, isTextBox: true });
caption(s, "Distinguish unreconciled value, legally due levies, revenue collected and losses. Rates by period and legal texts: PERTES_FISCALES.md. Scenarios = author's calculations.");

// ===== 11. Section autres
section("Other minerals");
s = pres.addSlide({ masterName: "SECTION_SOMBRE", sectionTitle: cur() });
s.addText("Diamonds, cobalt, iron, manganese, bauxite", { placeholder: "title" });
s.addText("Small or absent flows; traceability and contract issues", { placeholder: "body" });

// ===== 12. Diamant
s = content("Diamonds: a traceability issue, not a revenue one");
const dy = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024];
const dv = [236, 156, 242, 179, 84, 274, 127, 92, 249, 117, 35, 16];
s.addChart(pres.charts.BAR, [{ name: "USD per carat", labels: dy.map(String), values: dv }], {
  x: 0.6, y: 1.4, w: 6.6, h: 5.0, barDir: "col", chartColors: [H.accent3], showLegend: false,
  showTitle: true, title: "Average price of exported diamonds (USD/carat, Kimberley)",
  showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0", ...chartBase(), objectName: "Diamond price chart",
});
const dfacts = [
  ["≤ USD 0.6 M", "of official exports per year"],
  ["140,000 ct", "smuggled out of the CAR after May 2013 (UN), all routes combined"],
  ["4,523 ct", "on a forged Cameroonian Kimberley certificate (2016)"],
  ["FCFA 25–175 M", "calculated tax loss per year"],
];
dfacts.forEach((f, i) => {
  const y = 1.4 + i * 1.27;
  card(s, 7.5, y, 5.2, 1.12, "Diamond fact " + (i + 1));
  s.addText(f[0], { x: 7.7, y: y + 0.1, w: 2.2, h: 0.92, fontSize: 20, bold: true, color: C.accent3, valign: "middle", margin: 0, isTextBox: true });
  s.addText(f[1], { x: 9.95, y: y + 0.1, w: 2.6, h: 0.92, fontSize: 13, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
});
caption(s, "Sources: Kimberley Process (excerpts), UN Panel of Experts S/2014/762, PAC/IMPACT 2016. 2024 price: column alignment uncertain.");

// ===== 13. Quatre minerais
s = content("Four minerals: no flows found, no proof of absence");
const four = [
  ["Cobalt", "Geovic at Nkamouna (Lomié) never mined; licence withdrawn in February 2025 and handed to Sonamines", "Mirror: ≈ USD 3,000 (China, 2023)"],
  ["Iron", "No confirmed exports; Grand Zambi opened in September 2025", "Mbalam arbitration: USD 616 M (≈ FCFA 355 bn) owed to Sundance"],
  ["Manganese", "By-product of Nkamouna, never mined; no known active licence", "No mirror flow found (web search only)"],
  ["Bauxite", "Minim-Martap (Canyon/Camalco): first export postponed, target withdrawn in August 2026", "Expected revenue: FCFA 9.5–16.6 bn/yr at 3 Mt"],
];
four.forEach((f, i) => {
  const x = 0.6 + (i % 2) * 6.15, y = 1.5 + Math.floor(i / 2) * 2.55;
  card(s, x, y, 5.95, 2.35, "Mineral " + f[0]);
  circleNum(s, i + 1, x + 0.25, y + 0.25, 0.55, C.accent3);
  s.addText(f[0], { x: x + 1.0, y: y + 0.25, w: 4.7, h: 0.55, fontSize: 20, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  s.addText(f[1], { x: x + 0.25, y: y + 0.95, w: 5.45, h: 0.8, fontSize: 14, color: C.text1, valign: "top", margin: 0, isTextBox: true });
  s.addText(f[2], { x: x + 0.25, y: y + 1.75, w: 5.45, h: 0.45, fontSize: 14, bold: true, color: C.accent2, valign: "top", margin: 0, isTextBox: true });
});
caption(s, "\"No flow found\" does not mean \"proven absence\": Comtrade could not be queried for these minerals. Sources: web excerpts (USGS, BGS, press, ASX, ICC award of 26/07/2026).");

// ===== 14. Comparatif
s = content("Six minerals: gold shows the best-documented gaps");
const ch = ["Mineral", "Official flows found", "Mirror flows found", "Estimated cost", "Reliability"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const comp = [
  ["Gold", "A few kg/yr", "5 to 18 t/yr (USD 280–1,145 M)", "Est. FCFA 51–162 bn/yr (MINMIDT)", "High (volumes)"],
  ["Diamonds", "250 to 18,000 ct/yr (≤ USD 0.6 M)", "Negligible in sources", "FCFA 0.03–0.2 bn/yr (calc.)", "Low"],
  ["Cobalt", "None", "≈ USD 3,000 (2023)", "Negligible", "Medium"],
  ["Iron", "None confirmed", "≈ 0", "Arbitration: ≈ FCFA 355 bn", "Medium"],
  ["Manganese", "None found", "Not queried in Comtrade", "–", "Low"],
  ["Bauxite", "None found", "Not queried in Comtrade", "–", "Low"],
];
s.addTable([ch, ...comp.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, color: (i === 0 && j === 3) ? H.accent2 : H.dk1, fill: { color: i === 0 ? "F6EED3" : H.lt1 } } })))], {
  x: 0.6, y: 1.45, w: 12.1, colW: [1.6, 2.9, 3.0, 3.1, 1.5], fontSize: 14, fontFace: THEME.bodyFontFace, rowH: 0.66,
  border: { type: "solid", pt: 0.75, color: "D9D3C8" }, valign: "middle", objectName: "Comparison table",
});
caption(s, "Reliability: high = full Comtrade database; medium = consistent sources; low = web search excerpts only.");

// ===== 15. Limites
section("Conclusion");
s = content("What these figures do not prove");
const lim = [
  ["Origin or provenance", "Part of the gold and diamonds may come from the Central African Republic or Chad and transit through Cameroon"],
  ["Gap or fraud", "Smuggling, under-declaration, hand-carry or country-code errors: the data cannot tell them apart"],
  ["Incomplete data", "2024–2025 without the UAE; Comtrade inaccessible for five minerals"],
  ["Uncertain tax regime", "Conflicting 2001–2015 rates (3% or 5%); export duty before 2020 not found"],
];
lim.forEach((l, i) => {
  const x = 0.6 + (i % 2) * 6.15, y = 1.5 + Math.floor(i / 2) * 2.45;
  card(s, x, y, 5.95, 2.2, "Limitation " + (i + 1));
  circleNum(s, "!", x + 0.25, y + 0.25, 0.55, C.accent2);
  s.addText(l[0], { x: x + 1.0, y: y + 0.25, w: 4.7, h: 0.55, fontSize: 20, bold: true, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
  s.addText(l[1], { x: x + 0.25, y: y + 0.95, w: 5.45, h: 1.1, fontSize: 15, color: C.text1, valign: "top", margin: 0, isTextBox: true });
});
caption(s, "Contradictions and sources are detailed in the per-mineral reports (docs/recherche-*-cameroun/RAPPORT.md, in French).");

// ===== 16. Conclusion
s = pres.addSlide({ masterName: "TITRE_SOMBRE", sectionTitle: cur() });
s.addText("Conclusions and next steps", { x: 0.8, y: 0.6, w: 11.7, h: 0.9, fontSize: 36, bold: true, color: C.background1, fontFace: THEME.headFontFace, margin: 0, isTextBox: true });
const concl = [
  "Documented fact: partners report gold imports attributed to Cameroon far above its official exports (Interpol, EITI, WITS)",
  "Hypothesis to investigate: much of the gap may stem from informal channels, smuggling or regional transit",
  "Still to establish: volumes of Cameroonian origin exported irregularly and the exact revenue lost",
];
const nexts = [
  "Compare Rwanda's and Uganda's exports to the UAE with their imports attributed to Cameroon; examine refiners and intermediaries",
  "Build a documented tax model by mining regime, with scenarios and legal texts",
  "Obtain UAE 2024–2025 data, check Rwanda and Uganda, query Comtrade for the other minerals",
];
s.addText("Conclusions", { x: 0.8, y: 1.7, w: 5.6, h: 0.5, fontSize: 20, bold: true, color: C.accent1, margin: 0, isTextBox: true });
s.addText("Next steps", { x: 6.9, y: 1.7, w: 5.6, h: 0.5, fontSize: 20, bold: true, color: C.accent1, margin: 0, isTextBox: true });
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
const ah = ["Year", "Total (kg)", "UAE (kg)", "Rwanda (kg)", "Uganda, net weight", "Uganda, quantity", "Other (kg)", "Value (USD M)"].map(t => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk2 } } }));
const fk = x => x ? Math.round(x).toLocaleString("en-US") : "–";
[[2000, 2012], [2013, 2025]].forEach(([a, b], k) => {
  s = content("Annex A" + (k + 1) + ": unwrought gold by reporter, " + a + "–" + b);
  const rr = [];
  for (let y = a; y <= b; y++) {
    const d = decl[y] || { eau: 0, rwa: 0, uga: 0, aut: 0 };
    rr.push([String(y) + (y >= 2024 ? " *" : ""), fk(data[y].kg), y >= 2024 ? "n/p" : fk(d.eau), fk(d.rwa), fk(d.uga), fk(ugaQty[y] || 0), fk(d.aut), fr(data[y].usd / 1e6, 1)].map(c => ({ text: c, options: { color: H.dk1 } })));
  }
  s.addTable([ah, ...rr], {
    x: 0.6, y: 1.4, w: 12.1, colW: [1.1, 1.55, 1.55, 1.45, 1.7, 1.7, 1.35, 1.7], fontSize: 14, fontFace: THEME.bodyFontFace, rowH: 0.34, align: "right",
    border: { type: "solid", pt: 0.5, color: "D9D3C8" }, fill: { color: H.lt1 }, valign: "middle", objectName: "Annexe table " + (k + 1),
  });
  caption(s, k ? "* Partial: UAE not published (n/p). Totals use net weight (netWgt); quantity (qty) differs materially only for Uganda. File: donnees_miroir_or_tous_declarants.csv." : "Source: UN Comtrade public preview API, flow M, partner 120 (Cameroon), extracted 31/10/2026. Net weight in kg, CIF values in USD.");
});
s = content("Annex A3: reproducibility and scope");
const meta = [
  ["Query", "comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=…&partnerCode=120&flowCode=M&cmdCode=7108 (then 7112, 7113)"],
  ["Reporters", "254 countries and territories queried (“Reporters” table, groups and regional aggregates excluded); 19 reported non-zero unwrought gold imports"],
  ["Requests", "5 batches of 44–57 codes × 26 years × 3 HS codes = 390 annual requests, plus retries after timeouts; 283 non-zero observations"],
  ["Checks", "No truncated response (“truncated” flag false, 500-row cap never reached); duplicates removed on the HS code × year × reporter key"],
  ["Period", "2000–2025, annual; extracted 31/10/2026; data subject to revision"],
  ["Conversions", "USD/XAF rate: World Bank PA.NUS.FCRF; gold price: World Bank Pink Sheet (LBMA PM)"],
];
meta.forEach((m, i) => {
  const y = 1.4 + i * 0.86;
  card(s, 0.6, y, 12.1, 0.76, "Meta " + (i + 1));
  s.addText(m[0], { x: 0.85, y: y + 0.06, w: 2.2, h: 0.64, fontSize: 15, bold: true, color: C.accent5, valign: "middle", margin: 0, isTextBox: true });
  s.addText(m[1], { x: 3.1, y: y + 0.06, w: 9.4, h: 0.64, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
});
caption(s, "GitHub repository boujieka/Boujieka, docs/ folder. Other minerals rely on web search excerpts, without Comtrade extraction.");

s = content("Annex A4: primary sources");
const srcs = [
  ["UN Comtrade", "Public preview API · comtradeapi.un.org/public/v1/preview/C/A/HS · HS 7108, 7112, 7113 · partner 120 · extracted 31/10/2026"],
  ["INTERPOL (2021)", "Illegal Gold Mining in Central Africa · interpol.int/content/download/16493 · UAE series 2008–2018"],
  ["EITI", "“Cameroon's gold gap” · eiti.org/impact-story/cameroons-gold-gap-how-eiti-data-driving-reforms · 2023 report presented 10/12/2025"],
  ["MINMIDT", "2021–2025 series (FCFA 577.51 bn) reported by sikafinance.com (07/2026); MINMIDT page of 24/07/2026 citing 557 bn: to be reconciled"],
  ["SWISSAID (2025)", "“United Arab Emirates: More Than Ever a Hub for Conflict Gold” · swissaid.ch · 04/11/2025 (UAE 2024 data withdrawn)"],
  ["World Bank", "PA.NUS.FCRF exchange rate · api.worldbank.org; gold price: annual Pink Sheet, CMO-Historical-Data-Annual.xlsx"],
];
srcs.forEach((m, i) => {
  const y = 1.4 + i * 0.86;
  card(s, 0.6, y, 12.1, 0.76, "Source " + (i + 1));
  s.addText(m[0], { x: 0.85, y: y + 0.06, w: 2.5, h: 0.64, fontSize: 14, bold: true, color: C.accent5, valign: "middle", margin: 0, isTextBox: true });
  s.addText(m[1], { x: 3.4, y: y + 0.06, w: 9.1, h: 0.64, fontSize: 13, color: C.text1, valign: "middle", margin: 0, isTextBox: true });
});
caption(s, "Full URL list in the per-mineral reports (repository boujieka/Boujieka, docs/ folder). WITS 2023: external check of 31/10/2026.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
