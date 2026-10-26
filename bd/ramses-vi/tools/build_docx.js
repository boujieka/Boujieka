// Génère les documents Word de la série à partir des fichiers Markdown.
// Usage : node build_docx.js bible|scenario
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, LevelFormat, PageBreak, Header, Footer, PageNumber,
  TableOfContents, ExternalHyperlink, TabStopType,
} = require('docx');

const ROOT = path.resolve(__dirname, '..');

const C = {
  nuit: '14213D',   // bleu nuit (plafond de Nout)
  or: 'B8860B',     // or
  ocre: 'A0522D',   // ocre rouge
  sable: 'F5EBD7',  // fond des en-têtes de tableau
  pale: 'FBF6EC',   // fond des encadrés
  gris: '5A5A5A',
};
const BODY_FONT = 'Calibri';
const HEAD_FONT = 'Cambria';

// Page A4, marges 2 cm
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1134;
const CONTENT_W = PAGE_W - 2 * MARGIN;

const CONFIGS = {
  bible: {
    out: 'Bible_Les_Mysteres_du_tombeau_de_Ramses_VI.docx',
    kicker: 'BIBLE DE LA SÉRIE',
    subtitle: 'Saison 1 — Le Livre de la Terre : le secret de la renaissance solaire',
    note: 'Référence historique sourcée, personnages, épisodes, édition',
    files: [
      'bible/00_index_et_corrections.md',
      'bible/01_reference_kv9.md',
      'bible/02_livre_de_la_terre.md',
      'bible/03_divinites_iconographie.md',
      'bible/04_histoire_ramses_v_vi.md',
      'bible/05_episodes_saison_1.md',
      'bible/06_edition_kdp_droits.md',
      'bible/07_bibliographie.md',
    ],
  },
  chatgpt: {
    out: 'Prompts_ChatGPT_Volume_1_Les_Mysteres_du_tombeau_de_Ramses_VI.docx',
    kicker: 'PROMPTS CHATGPT — VOLUME 1',
    subtitle: 'Le Livre de la Terre : le secret de la renaissance solaire',
    note: 'Mode d\'emploi et un prompt par planche, à coller dans ChatGPT',
    files: ['prompts_chatgpt/00_mode_d_emploi_chatgpt.md', 'prompts_chatgpt/01_chatgpt_couverture_prologue_ep01-03.md',
      'prompts_chatgpt/02_chatgpt_ep04-06.md', 'prompts_chatgpt/03_chatgpt_ep07-09.md', 'prompts_chatgpt/04_chatgpt_ep10-12.md'],
  },
  prompts: {
    out: 'Prompts_images_Volume_1_Les_Mysteres_du_tombeau_de_Ramses_VI.docx',
    kicker: "PROMPTS D'IMAGES — VOLUME 1",
    subtitle: 'Le Livre de la Terre : le secret de la renaissance solaire',
    note: 'Guide de style, fiches personnages et prompts case par case',
    files: ['prompts/00_guide_prompts.md', 'prompts/01_prompts_couverture_prologue.md',
      'prompts/02_prompts_ep01-03.md', 'prompts/03_prompts_ep04-06.md',
      'prompts/04_prompts_ep07-09.md', 'prompts/05_prompts_ep10-12.md'],
  },
  scenario: {
    out: 'Scenario_Volume_1_Les_Mysteres_du_tombeau_de_Ramses_VI.docx',
    kicker: 'SCÉNARIO — VOLUME 1',
    subtitle: 'Le Livre de la Terre : le secret de la renaissance solaire',
    note: 'Couverture, prologue et découpage des 12 épisodes',
    files: null, // déterminé à l'exécution : 01_… à 14_…
  },
};

// ---------- Inline : **gras**, *italique*, `code`, [lien](url) ----------
function inline(text, base = {}) {
  const runs = [];
  const re = /(\*\*([^*]+)\*\*|\*([^*]+)\*|`([^`]+)`|\[([^\]]+)\]\((https?:[^)]+)\))/g;
  let last = 0, m;
  const push = (t, extra = {}) => { if (t) runs.push(new TextRun({ text: t, ...base, ...extra })); };
  while ((m = re.exec(text)) !== null) {
    push(text.slice(last, m.index));
    if (m[2] !== undefined) push(m[2], { bold: true });
    else if (m[3] !== undefined) push(m[3], { italics: true });
    else if (m[4] !== undefined) push(m[4], { font: 'Consolas', size: (base.size || 21) - 2, color: C.ocre });
    else if (m[5] !== undefined) {
      runs.push(new ExternalHyperlink({
        link: m[6],
        children: [new TextRun({ text: m[5], ...base, style: 'Hyperlink' })],
      }));
    }
    last = m.index + m[0].length;
  }
  push(text.slice(last));
  return runs;
}

// Pour les URL nues dans les tableaux : texte brut, plus petit
function cellRuns(text, header) {
  const base = header ? { bold: true, color: C.nuit, size: 18 } : { size: 18 };
  return inline(text, base);
}

// ---------- Blocs ----------
function heading(text, level) {
  const map = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3 };
  return new Paragraph({ heading: map[level], children: inline(text) });
}

function para(text, opts = {}) {
  return new Paragraph({ spacing: { after: 120, line: 276 }, ...opts, children: inline(text, opts.run || {}) });
}

function quoteBlock(lines) {
  // Chaque élément de `lines` est un paragraphe de l'encadré
  return lines.map((t, i) => {
    const isSource = /^(Source|Rigueur|Statut|Note|Intention|Attention|Garde-fou|Remarque|Sources?|Note de)/.test(t.replace(/\*\*/g, ''));
    return new Paragraph({
      spacing: { before: i === 0 ? 60 : 0, after: i === lines.length - 1 ? 140 : 40, line: 264 },
      indent: { left: 340, right: 200 },
      shading: { type: ShadingType.CLEAR, fill: isSource ? 'F2F2F2' : C.pale, color: 'auto' },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: isSource ? '9E9E9E' : C.or, space: 8 } },
      children: inline(t, isSource ? { size: 18, color: C.gris } : { size: 21 }),
    });
  });
}

function table(rows) {
  const ncol = rows[0].length;
  // largeur proportionnelle à la longueur moyenne du texte, bornée
  const plain = t => (t || '').replace(/\*\*|`|\*/g, '');
  const mins = Array.from({ length: ncol }, (_, c) => Math.min(2600, 260 + 95 *
    Math.max(...rows.map(r => Math.max(0, ...plain(r[c]).split(/\s+/).map(w => w.length))))));
  const lens = Array.from({ length: ncol }, (_, c) =>
    Math.max(4, Math.min(80, rows.reduce((s, r) => s + plain(r[c]).length, 0) / rows.length)));
  const minTot = mins.reduce((a, b) => a + b, 0);
  const rest = Math.max(0, CONTENT_W - minTot);
  const tot = lens.reduce((a, b) => a + b, 0);
  let widths = minTot >= CONTENT_W
    ? mins.map(w => Math.floor(w * CONTENT_W / minTot))
    : lens.map((l, c) => mins[c] + Math.floor((l / tot) * rest));
  widths[widths.length - 1] += CONTENT_W - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: 'D6C7A8' };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      cantSplit: true,
      children: widths.map((w, ci) => new TableCell({
        width: { size: w, type: WidthType.DXA },
        borders,
        shading: ri === 0 ? { type: ShadingType.CLEAR, fill: C.sable, color: 'auto' }
          : (ri % 2 === 0 ? { type: ShadingType.CLEAR, fill: 'FDFBF6', color: 'auto' } : undefined),
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({ spacing: { after: 0, line: 240 }, children: cellRuns(r[ci] || '', ri === 0) })],
      })),
    })),
  });
}

function splitRow(line) {
  return line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(s => s.trim());
}

// ---------- Markdown -> blocs ----------
function convert(md, { firstHeadingPageBreak }) {
  const out = [];
  md = md.replace(/\[`?([^\]`]+)`?\]\((?!https?:)[^)]+\)/g, '« $1 »');
  const lines = md.split('\n');
  let i = 0, firstH1 = true;
  const isBlockStart = l => /^(#{1,3} |\||> |- |\d+\. |```|---\s*$)/.test(l) || l.trim() === '';
  while (i < lines.length) {
    const l = lines[i];
    if (l.trim() === '') { i++; continue; }
    if (/^---\s*$/.test(l)) {
      out.push(new Paragraph({ spacing: { before: 120, after: 120 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'D6C7A8', space: 1 } }, children: [] }));
      i++; continue;
    }
    let m;
    if ((m = l.match(/^(#{1,3}) (.*)$/))) {
      const lvl = m[1].length;
      if (lvl === 1 && firstHeadingPageBreak && !firstH1) out.push(new Paragraph({ children: [new PageBreak()] }));
      if (lvl === 1 && firstHeadingPageBreak && firstH1) { out.push(new Paragraph({ children: [new PageBreak()] })); }
      if (lvl === 1) firstH1 = false;
      out.push(heading(m[2], lvl));
      i++; continue;
    }
    if (l.startsWith('```')) {
      i++; const code = [];
      while (i < lines.length && !lines[i].startsWith('```')) code.push(lines[i++]);
      i++;
      // bloc de texte (prompt) : lignes jointes par paragraphe, paragraphes séparés par une ligne vide
      const blocks = code.join('\n').split(/\n\s*\n/).map(t => t.split('\n').map(x => x.trim()).join(' ').trim()).filter(Boolean);
      blocks.forEach((t, k) => out.push(new Paragraph({
        spacing: { after: k === blocks.length - 1 ? 0 : 80, line: 252 }, indent: { left: 340, right: 200 },
        shading: { type: ShadingType.CLEAR, fill: 'F4F4F4', color: 'auto' },
        children: [new TextRun({ text: t, font: 'Consolas', size: 17 })],
      })));
      out.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
      continue;
    }
    if (l.startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].startsWith('|')) {
        if (!/^\|[\s\-:|]+\|?\s*$/.test(lines[i])) rows.push(splitRow(lines[i]));
        i++;
      }
      out.push(table(rows));
      out.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
      continue;
    }
    if (l.startsWith('>')) {
      const paras = [];
      while (i < lines.length && lines[i].startsWith('>')) {
        const t = lines[i].replace(/^>\s?/, '');
        const startsNew = paras.length === 0 || t === '' ||
          /^(\*\*|Cartouche|SFX|Source|Rigueur|Statut|Note|Intention|Attention|Garde-fou|Remarque|Option)/.test(t);
        if (t === '') { i++; continue; }
        if (startsNew) paras.push(t); else paras[paras.length - 1] += ' ' + t.trim();
        i++;
      }
      out.push(...quoteBlock(paras));
      continue;
    }
    if ((m = l.match(/^(\s*)(- |\d+\. )(.*)$/))) {
      const numbered = /\d/.test(m[2]);
      const ref = numbered ? 'num' : 'bullet';
      const instance = ++LIST_ID;
      while (i < lines.length && (m = lines[i].match(/^(\s*)(- |\d+\. )(.*)$/))) {
        const level = m[1].length >= 2 ? 1 : 0;
        let t = m[3]; i++;
        while (i < lines.length && /^\s{2,}\S/.test(lines[i]) && !/^\s*(- |\d+\. )/.test(lines[i])) t += ' ' + lines[i++].trim();
        out.push(new Paragraph({ numbering: { reference: ref, level, instance }, spacing: { after: 60, line: 264 }, children: inline(t) }));
      }
      out.push(new Paragraph({ spacing: { after: 60 }, children: [] }));
      continue;
    }
    // paragraphe (lignes de continuation jointes)
    let t = l.trim(); i++;
    while (i < lines.length && !isBlockStart(lines[i])) t += ' ' + lines[i++].trim();
    out.push(para(t));
  }
  return out;
}

// ---------- Page de titre ----------
function titlePage(cfg) {
  const center = (children, spacing = {}) => new Paragraph({ alignment: AlignmentType.CENTER, spacing, children });
  return [
    center([new TextRun({ text: ' ' })], { before: 2200 }),
    center([new TextRun({ text: cfg.kicker, font: HEAD_FONT, size: 22, color: C.or, bold: true, characterSpacing: 60 })], { after: 400 }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      border: { top: { style: BorderStyle.SINGLE, size: 12, color: C.or, space: 12 } }, children: [] }),
    center([new TextRun({ text: 'LES MYSTÈRES DU', font: HEAD_FONT, size: 44, color: C.nuit, bold: true })]),
    center([new TextRun({ text: 'TOMBEAU DE RAMSÈS VI', font: HEAD_FONT, size: 60, color: C.nuit, bold: true })], { after: 300 }),
    center([new TextRun({ text: cfg.subtitle, font: HEAD_FONT, size: 28, italics: true, color: C.ocre })], { after: 200 }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: C.or, space: 12 } }, children: [] }),
    center([new TextRun({ text: 'Une aventure archéologique du Dr Kerbu', size: 24, color: C.gris })], { after: 120 }),
    center([new TextRun({ text: cfg.note, size: 20, color: C.gris })], { after: 2400 }),
    center([new TextRun({ text: 'Balisage : [H] histoire documentée · [F] fiction · [S] symbolisme', size: 18, color: C.gris })]),
    center([new TextRun({ text: 'Statuts : V vérifié · C sources en désaccord · N non vérifié', size: 18, color: C.gris })]),
    center([new TextRun({ text: `Version du ${new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })} — document de travail`, size: 18, color: C.gris })], { before: 200 }),
    new Paragraph({ children: [new PageBreak()] }),
    new Paragraph({ spacing: { after: 240 }, border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: C.or, space: 6 } },
      children: [new TextRun({ text: 'Sommaire', font: HEAD_FONT, size: 36, bold: true, color: C.nuit })] }),
    ...TOC_ENTRIES.map(e => new Paragraph({
      spacing: { before: e.level === 1 ? 140 : 0, after: 30 },
      indent: { left: e.level === 1 ? 0 : 400 },
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W, leader: 'dot' }],
      children: [new TextRun({ text: e.text, bold: e.level === 1, color: e.level === 1 ? C.nuit : '333333',
        size: e.level === 1 ? 21 : 19, font: e.level === 1 ? HEAD_FONT : BODY_FONT }),
        new TextRun({ text: '\t' + (PAGES[e.key] || '00'), size: e.level === 1 ? 21 : 19 })],
    })),
  ];
}

// Sommaire statique : entrées collectées dans les titres, numéros de page lus dans un rendu PDF
// (fichier pages.json produit par paginate.py) ; « 00 » au premier passage.
const TOC_ENTRIES = [];
let LIST_ID = 0;
let PAGES = {};
const strip = t => t.replace(/\*\*|\*|`/g, '');

function build(which) {
  const cfg = CONFIGS[which];
  let files = cfg.files;
  if (!files) {
    files = fs.readdirSync(ROOT).filter(f => /^\d\d_.*\.md$/.test(f)).sort();
  }
  const pj = path.join(__dirname, `pages_${which}.json`);
  if (fs.existsSync(pj)) PAGES = JSON.parse(fs.readFileSync(pj, 'utf8'));
  for (const f of files) {
    for (const line of fs.readFileSync(path.join(ROOT, f), 'utf8').split('\n')) {
      const m = line.match(/^(#{1,2}) (.*)$/);
      if (m) TOC_ENTRIES.push({ level: m[1].length, text: strip(m[2]), key: `${f}#${strip(m[2])}` });
    }
  }
  fs.writeFileSync(path.join(__dirname, `toc_${which}.json`), JSON.stringify(TOC_ENTRIES, null, 1));
  const body = [];
  for (const f of files) {
    const md = fs.readFileSync(path.join(ROOT, f), 'utf8');
    body.push(...convert(md, { firstHeadingPageBreak: true }));
  }
  const doc = new Document({
    creator: 'Les Mystères du tombeau de Ramsès VI',
    title: `Les Mystères du tombeau de Ramsès VI — ${cfg.kicker}`,
    features: { updateFields: true },
    styles: {
      default: { document: { run: { font: BODY_FONT, size: 21 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { font: HEAD_FONT, size: 36, bold: true, color: C.nuit },
          paragraph: { spacing: { before: 120, after: 240 }, outlineLevel: 0,
            border: { bottom: { style: BorderStyle.SINGLE, size: 10, color: C.or, space: 6 } } } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { font: HEAD_FONT, size: 28, bold: true, color: C.ocre },
          paragraph: { spacing: { before: 320, after: 140 }, outlineLevel: 1, keepNext: true } },
        { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { font: HEAD_FONT, size: 24, bold: true, color: C.nuit },
          paragraph: { spacing: { before: 220, after: 100 }, outlineLevel: 2, keepNext: true } },
      ],
    },
    numbering: {
      config: [
        { reference: 'bullet', levels: [
          { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 500, hanging: 280 } } } },
          { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 900, hanging: 280 } } } } ] },
        { reference: 'num', levels: [
          { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 500, hanging: 320 } } } },
          { level: 1, format: LevelFormat.LOWER_LETTER, text: '%2)', alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 900, hanging: 320 } } } } ] },
      ],
    },
    sections: [{
      properties: {
        page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } },
        titlePage: true,
      },
      headers: {
        default: new Header({ children: [new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W }],
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D6C7A8', space: 4 } },
          children: [
            new TextRun({ text: 'Les Mystères du tombeau de Ramsès VI', font: HEAD_FONT, size: 16, color: C.nuit }),
            new TextRun({ text: `\t${cfg.kicker}`, size: 16, color: C.or }),
          ] })] }),
        first: new Header({ children: [new Paragraph({ children: [] })] }),
      },
      footers: {
        default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: ['— ', PageNumber.CURRENT, ' —'], size: 16, color: C.gris })] })] }),
        first: new Footer({ children: [new Paragraph({ children: [] })] }),
      },
      children: [...titlePage(cfg), ...body],
    }],
  });
  return Packer.toBuffer(doc).then(buf => {
    const outPath = process.env.DOCX_OUT || path.join(ROOT, cfg.out);
    fs.writeFileSync(outPath, buf);
    console.log('écrit :', outPath);
  });
}

build(process.argv[2] || 'bible');
