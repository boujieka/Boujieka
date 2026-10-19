// Convertit une note Markdown simple (titres #/##, listes numérotées et à puces, gras **…**) en .docx A4.
// Usage : node cameroun/models/md_to_docx.js <entree.md> <sortie.docx>
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat, Footer, PageNumber, BorderStyle,
} = require("docx");

const [, , input, output] = process.argv;
const lines = fs.readFileSync(input, "utf8").split(/\r?\n/);

// Découpe une ligne en runs, en gérant **gras** et `code`.
function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const t = m[0];
    if (t.startsWith("**")) out.push(new TextRun({ text: t.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: t.slice(1, -1), font: "Consolas", size: 18, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

const children = [];
let numberedInstance = 0;
let inNumbered = false;
let para = null; // paragraphe de continuation (ligne indentée suivant une puce)

for (const raw of lines) {
  const line = raw.replace(/\s+$/, "");
  if (!line.trim()) { inNumbered = false; para = null; continue; }
  let m;
  if ((m = line.match(/^# (.*)/))) {
    children.push(new Paragraph({ heading: HeadingLevel.TITLE, children: runs(m[1]) }));
  } else if ((m = line.match(/^## (.*)/))) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: runs(m[1]) }));
  } else if ((m = line.match(/^\d+\. (.*)/))) {
    if (!inNumbered) { numberedInstance++; inNumbered = true; }
    para = { kind: "num", text: m[1], instance: numberedInstance, level: 0 };
    children.push(para);
  } else if ((m = line.match(/^(\s*)- (.*)/))) {
    para = { kind: "bullet", text: m[2], level: m[1].length >= 2 ? 1 : 0 };
    children.push(para);
  } else if (para && (/^\s+/.test(raw) || para.kind === "p")) {
    // ligne de continuation : indentée sous une puce, ou suite d'un paragraphe ordinaire
    para.text += " " + line.trim();
  } else {
    para = { kind: "p", text: line.trim() };
    children.push(para);
  }
}

const body = children.map((c) => {
  if (c instanceof Paragraph) return c;
  if (c.kind === "num")
    return new Paragraph({ numbering: { reference: "num", level: 0, instance: c.instance }, spacing: { after: 80 }, children: runs(c.text) });
  if (c.kind === "bullet")
    return new Paragraph({ numbering: { reference: "puces", level: c.level }, spacing: { after: 60 }, children: runs(c.text) });
  return new Paragraph({ spacing: { after: 120 }, children: runs(c.text) });
});

const doc = new Document({
  creator: "Équipe d'analyse indépendante",
  title: "Note au décideur — Diagnostic national du Cameroun",
  styles: {
    default: { document: { run: { font: "Calibri", size: 21 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", run: { size: 32, bold: true, color: "1F3864" },
        paragraph: { spacing: { after: 160 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: "1F3864", space: 4 } } } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, color: "1F3864" }, paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 0 } },
    ],
  },
  numbering: {
    config: [
      { reference: "num", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 360, hanging: 360 } } } }] },
      { reference: "puces", levels: [
          { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        ] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1247, right: 1247 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "Analyse indépendante — sans mandat officiel — page ", size: 16, color: "808080" }),
                 new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "808080" })] })] }) },
    children: body,
  }],
});

Packer.toBuffer(doc).then((b) => { fs.writeFileSync(output, b); console.log("écrit :", output); });
