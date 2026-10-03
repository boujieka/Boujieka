// Builds the Bankable Hydro book (.docx) from book/build/manuscript_resolved.md
// Usage: node tools/book/build_docx.js <resolved.md> <out.docx> [toc.json]
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, ImageRun, Header, Footer, PageNumber, PageBreak,
  LevelFormat, TabStopType, VerticalAlign, PageOrientation,
} = require("docx");

const [, , SRC, OUT, TOCJSON] = process.argv;
const ROOT = path.resolve(__dirname, "../..");
const lines = fs.readFileSync(SRC, "utf8").split(/\r?\n/);
const toc = TOCJSON && fs.existsSync(TOCJSON) ? JSON.parse(fs.readFileSync(TOCJSON, "utf8")) : null;

// ---------- page geometry: 170 x 240 mm ----------
const MM = 56.6929; // DXA per mm
const PAGE_W = Math.round(170 * MM), PAGE_H = Math.round(240 * MM);
const M_IN = Math.round(22 * MM), M_OUT = Math.round(18 * MM), M_TOP = Math.round(20 * MM), M_BOT = Math.round(20 * MM);
const TEXT_W = PAGE_W - M_IN - M_OUT;

const SERIF = "Times New Roman", SANS = "Arial";
const INK = "1A1A1A", ACCENT = "1F3864", MUTED = "5A5A5A", RULE = "8EA3C2";

// ---------- inline formatting ----------
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\^[^^]+\^|~[^~]+~)/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(...runs(t.slice(2, -2), { ...base, bold: true }));
    else if (t.startsWith("*")) out.push(...runs(t.slice(1, -1), { ...base, italics: true }));
    else if (t.startsWith("`")) out.push(new TextRun({ text: t.slice(1, -1), ...base, font: "Courier New", size: (base.size || 21) - 3 }));
    else if (t.startsWith("^")) out.push(new TextRun({ text: t.slice(1, -1), ...base, superScript: true }));
    else out.push(new TextRun({ text: t.slice(1, -1), ...base, subScript: true }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

const body = (text, opts = {}) => new Paragraph({
  children: runs(text), alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 0, line: 276 }, indent: opts.noIndent ? undefined : { firstLine: Math.round(5 * MM) },
  ...opts.p,
});

// ---------- tables ----------
const STATUS_FILL = { R: "C6EFCE", C: "FFF2B3", D: "F8CBAD", X: "F08080" };
function makeTable(rows, caption, note) {
  const header = rows[0];
  const data = rows.slice(1);
  const n = header.length;
  // column widths proportional to max content length (bounded)
  const lens = header.map((h, i) => {
    const all = [h, ...data.map(r => r[i] || "")].map(s => s.replace(/\*|`/g, "").length);
    return Math.min(Math.max(...all.map(l => Math.min(l, 60))), 60) + 4;
  });
  const sum = lens.reduce((a, b) => a + b, 0);
  let widths = lens.map((l, i) => Math.max(Math.round(TEXT_W * l / sum), Math.min(1300, 140 * (header[i].replace(/\*/g, "").split(" ").reduce((a, w) => Math.max(a, w.length), 0) + 1))));
  let tot = widths.reduce((a, b) => a + b, 0);
  if (tot > TEXT_W) widths = widths.map(w => Math.floor(w * TEXT_W / tot));
  const diff = TEXT_W - widths.reduce((a, b) => a + b, 0);
  widths[widths.indexOf(Math.max(...widths))] += diff;
  const fs = n >= 8 ? 13 : n >= 6 ? 15 : n >= 5 ? 16 : 17;
  const border = { style: BorderStyle.SINGLE, size: 4, color: "BFBFBF" };
  const noB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  const mk = (txt, i, isHead, rIdx) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: isHead ? { fill: ACCENT, type: ShadingType.CLEAR, color: "auto" } : (STATUS_FILL[txt.trim()] ? { fill: STATUS_FILL[txt.trim()], type: ShadingType.CLEAR, color: "auto" } : (rIdx % 2 ? { fill: "F3F5F9", type: ShadingType.CLEAR, color: "auto" } : undefined)),
    margins: { top: 50, bottom: 50, left: 80, right: 80 },
    verticalAlign: VerticalAlign.TOP,
    borders: { top: isHead ? noB : border, bottom: border, left: noB, right: noB },
    children: [new Paragraph({
      alignment: (!isHead && n > 2 && i > 0 && /^[-−(]?[0-9$€£.,%x+ ()-]+$/.test(txt.trim()) && txt.trim().length < 14) ? AlignmentType.RIGHT : ((!isHead && /^[RCDX]$/.test(txt.trim())) ? AlignmentType.CENTER : AlignmentType.LEFT),
      spacing: { before: 0, after: 0, line: 240 },
      children: runs(txt.trim(), { size: fs, font: isHead ? SANS : SERIF, color: isHead ? "FFFFFF" : INK, bold: isHead ? true : undefined }),
    })],
  });
  const out = [];
  if (caption) out.push(new Paragraph({ keepNext: true, spacing: { before: 200, after: 80 }, children: runs(caption, { font: SANS, size: 17, bold: true, color: ACCENT }) }));
  out.push(new Table({
    width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: header.map((h, i) => mk(h, i, true, 0)) }),
      ...data.map((r, ri) => new TableRow({ cantSplit: true, children: header.map((_, i) => mk(r[i] || "", i, false, ri)) }))],
  }));
  out.push(new Paragraph({ spacing: { before: 60, after: 160 }, children: note ? runs(note, { size: 15, italics: true, color: MUTED, font: SERIF }) : [] }));
  return out;
}

// ---------- figure ----------
function makeFigure(file, caption) {
  const p = path.join(ROOT, file);
  const buf = fs.readFileSync(p);
  // read PNG size
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  const maxWpx = TEXT_W / 1440 * 96;
  const scale = maxWpx / w;
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 200, after: 60 },
      children: [new ImageRun({ type: "png", data: buf, transformation: { width: Math.round(w * scale), height: Math.round(h * scale) },
        altText: { title: caption.slice(0, 60), description: caption, name: path.basename(file) } })] }),
    new Paragraph({ spacing: { before: 0, after: 200 }, children: runs(caption, { font: SANS, size: 16, color: MUTED }) }),
  ];
}

// ---------- document assembly ----------
const children = [];
let para = [];
let i = 0;
let firstAfterHeading = true;
let chapterTitle = "";
const flushPara = () => {
  if (para.length) {
    children.push(body(para.join(" "), { noIndent: firstAfterHeading, p: { spacing: { after: 0, line: 276 } } }));
    firstAfterHeading = false;
    para = [];
  }
};

function titlePage(meta) {
  const t = [];
  t.push(new Paragraph({ spacing: { before: Math.round(45 * MM) }, children: [] }));
  t.push(new Paragraph({ alignment: AlignmentType.LEFT, children: [new TextRun({ text: meta.series, font: SANS, size: 18, color: MUTED, allCaps: true, characterSpacing: 40 })] }));
  t.push(new Paragraph({ spacing: { before: 400 }, border: { top: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 12 } }, children: [new TextRun({ text: meta.title, font: SANS, size: 64, bold: true, color: ACCENT })] }));
  t.push(new Paragraph({ spacing: { before: 200, after: 600 }, children: [new TextRun({ text: meta.subtitle, font: SERIF, size: 30, italics: true, color: INK })] }));
  t.push(new Paragraph({ spacing: { before: Math.round(60 * MM) }, children: [new TextRun({ text: meta.edition, font: SANS, size: 18, color: MUTED })] }));
  t.push(new Paragraph({ children: [new PageBreak()] }));
  return t;
}

const tocEntries = [];
let listCounter = 0;
while (i < lines.length) {
  let L = lines[i];
  if (L.startsWith("%%TITLE")) {
    const meta = JSON.parse(L.slice(7));
    children.push(...titlePage(meta));
    i++; continue;
  }
  if (L.startsWith("%%TOC")) {
    flushPara();
    children.push(new Paragraph({ spacing: { after: 300 }, children: [new TextRun({ text: "Contents", font: SANS, size: 36, bold: true, color: ACCENT })] }));
    if (toc) {
      for (const e of toc) {
        const lvl = e.level;
        children.push(new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: TEXT_W, leader: lvl === 0 ? "none" : "dot" }],
          spacing: { before: lvl === 0 ? 180 : 30, after: 20 },
          indent: { left: lvl === 2 ? Math.round(6 * MM) : 0 },
          children: [new TextRun({ text: e.text, font: lvl === 0 ? SANS : SERIF, size: lvl === 0 ? 17 : (lvl === 1 ? 20 : 18), bold: lvl < 2, color: lvl === 0 ? ACCENT : INK, allCaps: lvl === 0 }),
            ...(lvl === 0 ? [] : [new TextRun({ text: "\t" + (e.page || ""), font: SERIF, size: lvl === 1 ? 20 : 18 })])],
        }));
      }
    } else {
      children.push(body("[contents generated on second pass]", { noIndent: true }));
    }
    children.push(new Paragraph({ children: [new PageBreak()] }));
    i++; continue;
  }
  if (L.trim() === "") { flushPara(); i++; continue; }
  if (L.startsWith("%%PB")) { flushPara(); children.push(new Paragraph({ children: [new PageBreak()] })); i++; continue; }
  if (L.startsWith("# ")) { // PART
    flushPara();
    const txt = L.slice(2).trim();
    children.push(new Paragraph({ pageBreakBefore: true, spacing: { before: Math.round(70 * MM), after: 200 }, children: [new TextRun({ text: txt.split("|")[0].trim(), font: SANS, size: 22, color: MUTED, allCaps: true, characterSpacing: 60 })] }));
    if (txt.includes("|")) children.push(new Paragraph({ border: { top: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 10 } }, children: [new TextRun({ text: txt.split("|")[1].trim(), font: SANS, size: 44, bold: true, color: ACCENT })] }));
    children.push(new Paragraph({ children: [new PageBreak()] }));
    tocEntries.push({ level: 0, text: txt.split("|").map(s => s.trim()).join(": ") });
    i++; continue;
  }
  if (L.startsWith("## ")) { // CHAPTER
    flushPara();
    const txt = L.slice(3).trim();
    chapterTitle = txt;
    const m = txt.match(/^(Chapter \d+|Annex [A-Z]|Preface|References|Abbreviations|Foreword)\.?\s*(.*)$/);
    children.push(new Paragraph({ pageBreakBefore: true, spacing: { before: Math.round(25 * MM), after: 60 },
      children: [new TextRun({ text: m ? m[1] : "", font: SANS, size: 20, color: MUTED, allCaps: true, characterSpacing: 40 })] }));
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 0, after: 360 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RULE, space: 8 } },
      children: [new TextRun({ text: m && m[2] ? m[2] : txt, font: SANS, size: 38, bold: true, color: ACCENT })] }));
    tocEntries.push({ level: 1, text: txt });
    firstAfterHeading = true;
    i++; continue;
  }
  if (L.startsWith("### ")) {
    flushPara();
    const txt = L.slice(4).trim();
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, keepNext: true, spacing: { before: 320, after: 120 }, children: [new TextRun({ text: txt, font: SANS, size: 24, bold: true, color: ACCENT })] }));
    tocEntries.push({ level: 2, text: txt });
    firstAfterHeading = true;
    i++; continue;
  }
  if (L.startsWith("#### ")) {
    flushPara();
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, keepNext: true, spacing: { before: 220, after: 80 }, children: [new TextRun({ text: L.slice(5).trim(), font: SANS, size: 21, bold: true, italics: true, color: INK })] }));
    firstAfterHeading = true;
    i++; continue;
  }
  if (L.startsWith("!fig|")) {
    flushPara();
    const [, file, cap] = L.split("|");
    children.push(...makeFigure(file.trim(), cap.trim()));
    i++; continue;
  }
  if (L.startsWith("$$")) { // display equation: $$ text $$ (n)
    flushPara();
    const m = L.match(/^\$\$\s*(.*?)\s*\$\$\s*(\(.*\))?\s*$/);
    children.push(new Paragraph({
      tabStops: [{ type: TabStopType.CENTER, position: Math.round(TEXT_W / 2) }, { type: TabStopType.RIGHT, position: TEXT_W }],
      spacing: { before: 140, after: 140 },
      children: [new TextRun({ text: "\t" }), ...runs(m[1], { font: "Cambria Math", size: 21 }), new TextRun({ text: "\t" + (m[2] || ""), font: SERIF, size: 20 })],
    }));
    i++; continue;
  }
  if (L.startsWith("> ")) { // boxed note
    flushPara();
    const buf = [];
    while (i < lines.length && lines[i].startsWith("> ")) { buf.push(lines[i].slice(2)); i++; }
    const paras = buf.join("\n").split(/\n\s*\n/);
    paras.forEach((p, k) => children.push(new Paragraph({
      shading: { fill: "EEF2F8", type: ShadingType.CLEAR, color: "auto" },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 8 } },
      indent: { left: 200, right: 200 }, spacing: { before: k === 0 ? 200 : 0, after: k === paras.length - 1 ? 200 : 60, line: 264 },
      children: runs(p.replace(/\n/g, " "), { size: 19, font: SERIF }),
    })));
    firstAfterHeading = true;
    continue;
  }
  if (L.startsWith("Table: ") || L.startsWith("|")) {
    flushPara();
    let caption = null, note = null;
    if (L.startsWith("Table: ")) { caption = L.slice(7).trim(); i++; }
    const rows = [];
    while (i < lines.length && lines[i].startsWith("|")) {
      const cells = lines[i].trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map(s => s.trim());
      if (!cells.every(c => /^:?-{2,}:?$/.test(c))) rows.push(cells);
      i++;
    }
    if (i < lines.length && lines[i].startsWith("Note: ")) { note = lines[i]; i++; }
    children.push(...makeTable(rows, caption, note));
    firstAfterHeading = true;
    continue;
  }
  if (/^(- |\d+\. )/.test(L)) {
    flushPara();
    listCounter++;
    while (i < lines.length && /^(- |\d+\. )/.test(lines[i])) {
      const numbered = /^\d+\. /.test(lines[i]);
      let txt = lines[i].replace(/^(- |\d+\. )/, "");
      i++;
      while (i < lines.length && /^ {2,}\S/.test(lines[i])) { txt += " " + lines[i].trim(); i++; }
      children.push(new Paragraph({
        numbering: { reference: numbered ? "nums" : "bullets", level: 0, instance: numbered ? listCounter : undefined },
        spacing: { before: 40, after: 40, line: 264 }, alignment: AlignmentType.LEFT, children: runs(txt),
      }));
    }
    firstAfterHeading = true;
    continue;
  }
  if (L.startsWith("REF|")) { // bibliography entry: REF|n|text
    flushPara();
    const [, n, txt] = L.split("|");
    children.push(new Paragraph({ indent: { left: 520, hanging: 520 }, spacing: { after: 70, line: 240 },
      children: [new TextRun({ text: `[${n}]\t`, font: SERIF, size: 17 }), ...runs(txt, { size: 17 })],
      tabStops: [{ type: TabStopType.LEFT, position: 520 }] }));
    i++; continue;
  }
  para.push(L.trim());
  i++;
}
flushPara();

const doc = new Document({
  creator: "Bankable Hydro", lastModifiedBy: "Bankable Hydro", title: "Bankable Hydro", description: "Structuring hydropower projects without creating unsustainable public liabilities",
  styles: {
    default: { document: { run: { font: SERIF, size: 21, color: INK } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: SANS, size: 38, bold: true, color: ACCENT }, paragraph: { outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: SANS, size: 24, bold: true, color: ACCENT }, paragraph: { outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { font: SANS, size: 21, bold: true }, paragraph: { outlineLevel: 2 } },
    ],
  },
  numbering: { config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 440, hanging: 260 } } } }] },
    { reference: "nums", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 440, hanging: 300 } } } }] },
  ] },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: M_TOP, bottom: M_BOT, left: M_IN, right: M_OUT, header: Math.round(10 * MM), footer: Math.round(10 * MM), gutter: 0 } }, titlePage: true },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "Bankable Hydro", font: SANS, size: 15, color: MUTED, smallCaps: true })] })] }),
      first: new Header({ children: [new Paragraph({ children: [] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], font: SERIF, size: 18, color: MUTED })] })] }),
      first: new Footer({ children: [new Paragraph({ children: [] })] }) },
    children,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); fs.writeFileSync(OUT.replace(/\.docx$/, ".tocentries.json"), JSON.stringify(tocEntries, null, 1)); console.log("wrote", OUT, children.length, "blocks"); });
