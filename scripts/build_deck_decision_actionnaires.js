const pptxgen = require('pptxgenjs');
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const md = require('react-icons/md');
const { applyTheme } = require('/root/.claude/skills/synced/595554f7-3334-4cb8-90b6-40da4dcb6b84_e238fe12-8a4b-4490-8c46-5bf1323948af/pptx/scripts/apply_theme.js');

const OUT = process.argv[2] || 'Kia_Mona_II_Decision_Actionnaires.pptx';

const THEME = {
  name: 'Kia Mona II',
  headFontFace: 'Cambria',
  bodyFontFace: 'Calibri',
  colors: {
    dk1: '1C2B28', lt1: 'FFFFFF', dk2: '173A33', lt2: 'EEF3F0',
    accent1: '1F6B5A', accent2: 'C98A0E', accent3: 'A63D33', accent4: '4F6D7A', accent5: '9FBFB2', accent6: '6E7573',
    hlink: '1F6B5A', folHlink: '4F6D7A',
  },
};
const HEX = THEME.colors;

// Chiffres repris des TdR V3.0 (13 novembre 2026)
const TR = { T1: 199600, T2: 571600, T3: 841800, T4: 294500, T5: 170500 };
const TOT = 1907500, LOW = 1430600, HIGH = 2575100, DISC = 381100;
const LOTS = [
  ['A', 'Direction, coordination, données', 261400], ['B', 'Gisement et laboratoires', 174800],
  ['C', 'Sites, sols, topographie, eau', 255500], ['D', 'Technologie et essais', 230000],
  ['E', 'Ingénierie et raccordement', 78700], ['F', 'Environnement et social', 245500],
  ['G', 'Finance, économie, juridique', 166200], ['H', 'Contrôles indépendants', 180000],
  ['I', 'Logistique, sécurité, assurances', 142000],
];
const fmt = n => Math.round(n).toLocaleString('fr-FR').replace(/ | /g, ' ');

const nb = t => typeof t === 'string' ? t.replace(/(\d) (?=\d{3}\b)/g, '$1\u00a0').replace(/ (€|%|HT\b)/g, '\u00a0$1') : Array.isArray(t) ? t.map(r => Object.assign({}, r, { text: nb(r.text) })) : t;
async function icon(Comp, color = 'FFFFFF') {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Comp, { color: '#' + color, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return 'image/png;base64,' + buf.toString('base64');
}

(async () => {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';
  pres.author = 'VIPRO S.A';
  pres.company = 'VIPRO S.A';
  pres.title = 'Kia Mona II, décision du Comité d’investissement';
  pres.subject = 'Tranche T1 de l’étude de faisabilité';
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  const _add = pres.addSlide.bind(pres);
  pres.addSlide = o => { const sl = _add(o); const at = sl.addText.bind(sl); sl.addText = (t, op) => at(nb(t), op); return sl; };

  const FOOT = 'VIPRO S.A  |  Kia Mona II  |  Comité d’investissement  |  Document interne et confidentiel';

  pres.defineSlideMaster({
    title: 'COUVERTURE',
    background: { color: C.text2 },
    objects: [
      { placeholder: { options: { name: 'title', type: 'title', x: 0.8, y: 2.1, w: 11.7, h: 1.6, fontFace: THEME.headFontFace, fontSize: 44, bold: true, color: C.background1, valign: 'bottom', align: 'left', margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'body', type: 'body', x: 0.8, y: 3.95, w: 11.7, h: 1.4, fontFace: THEME.bodyFontFace, fontSize: 20, color: C.accent5, valign: 'top', align: 'left', margin: 0 }, text: '' } },
      { text: { text: 'VIPRO S.A  |  Document interne et confidentiel', options: { x: 0.8, y: 6.7, w: 11.7, h: 0.3, fontSize: 11, color: C.accent5, margin: 0 } } },
    ],
  });
  pres.defineSlideMaster({
    title: 'CONTENU',
    background: { color: C.background1 },
    margin: [0.5, 0.6, 0.6, 0.6],
    objects: [
      { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.35, w: 12.1, h: 0.75, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: C.text1, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'body', type: 'body', x: 0.6, y: 1.1, w: 12.1, h: 0.45, fontFace: THEME.bodyFontFace, fontSize: 16, color: C.accent6, valign: 'top', align: 'left', margin: 0 }, text: '' } },
      { text: { text: FOOT, options: { x: 0.6, y: 7.05, w: 10.5, h: 0.25, fontSize: 10, color: C.accent6, margin: 0 } } },
    ],
    slideNumber: { x: 12.2, y: 7.05, w: 0.5, h: 0.25, fontSize: 10, color: C.accent6, align: 'right' },
  });
  pres.defineSlideMaster({
    title: 'CLOTURE',
    background: { color: C.text2 },
    objects: [
      { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.35, w: 12.1, h: 0.75, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: C.background1, valign: 'middle', align: 'left', margin: 0 }, text: '' } },
      { text: { text: FOOT, options: { x: 0.6, y: 7.05, w: 10.5, h: 0.25, fontSize: 10, color: C.accent5, margin: 0 } } },
    ],
    slideNumber: { x: 12.2, y: 7.05, w: 0.5, h: 0.25, fontSize: 10, color: C.accent5, align: 'right' },
  });

  const card = (s, name, x, y, w, h, fill = C.background2) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.08, objectName: name });
  const txt = (s, name, t, o) => s.addText(t, Object.assign({ isTextBox: true, objectName: name, fontSize: 14, color: C.text1, margin: 0, valign: 'top' }, o));
  const circle = (s, name, x, y, d, fill) => s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: name });

  // ---------- 1. Couverture
  pres.addSection({ title: 'Décision' });
  let s = pres.addSlide({ masterName: 'COUVERTURE', sectionTitle: 'Décision' });
  s.addText('Kia Mona II : engager la première tranche d’étude', { placeholder: 'title' });
  s.addText('Comité d’investissement de VIPRO S.A, séance de novembre 2026\nDécision demandée : tranche T1, plafonnée à 199 600 € HT', { placeholder: 'body' });
  s.addNotes('Ce support résume les termes de référence V3.0 du 13 novembre 2026. Il ne demande qu’une seule décision : autoriser la première tranche de l’étude. Tout le reste sera soumis au Comité plus tard, jalon par jalon.');

  // ---------- 2. La décision demandée
  s = pres.addSlide({ masterName: 'CONTENU', sectionTitle: 'Décision' });
  s.addText('Ce que nous vous demandons de décider', { placeholder: 'title' });
  s.addText('Un engagement limité, réversible et assorti de conditions', { placeholder: 'body' });
  card(s, 'Montant', 0.6, 1.8, 4.6, 3.6, C.text2);
  txt(s, 'Montant chiffre', '199 600 €', { x: 0.9, y: 2.1, w: 4.0, h: 1.1, fontSize: 60, bold: true, color: C.accent2, fontFace: THEME.headFontFace, valign: 'middle' });
  txt(s, 'Montant libellé', 'hors taxes, pour la tranche T1, sur une enveloppe d’étude de 1 907 500 € HT engagée tranche par tranche', { x: 0.9, y: 3.3, w: 4.0, h: 1.0, fontSize: 15, color: C.background1 });
  txt(s, 'Montant part', 'Soit 10 % de l’enveloppe totale', { x: 0.9, y: 4.6, w: 4.0, h: 0.5, fontSize: 15, bold: true, color: C.accent5 });
  txt(s, 'Reco titre', 'Recommandation : approuver T1 sous quatre conditions', { x: 5.6, y: 1.8, w: 7.1, h: 0.45, fontSize: 18, bold: true, fontFace: THEME.headFontFace, color: C.accent1 });
  txt(s, 'Reco liste', [
    { text: 'Nommer un Directeur d’étude, responsable et signataire des livrables.', options: { bullet: { type: 'number' }, breakLine: true } },
    { text: 'Ne lancer la tranche T2 qu’après la revue du jalon G1, au troisième ou quatrième mois.', options: { bullet: { type: 'number' }, breakLine: true } },
    { text: 'Confier les contrôles à un ingénieur et à un auditeur indépendants, sous contrats distincts.', options: { bullet: { type: 'number' }, breakLine: true } },
    { text: 'N’engager ni contrat de construction, ni dette, ni garantie avant le jalon G4.', options: { bullet: { type: 'number' } } },
  ], { x: 5.6, y: 2.5, w: 7.1, h: 2.9, fontSize: 16, paraSpaceAfter: 10 });
  const tiles = [
    ['Le vote engage', '199 600 € HT et trois à quatre mois de travail'],
    ['Le vote n’engage pas', 'La puissance, les tarifs, la construction, la dette, une garantie de l’État'],
    ['Prochain rendez-vous', 'Jalon G1, avec les premiers résultats et la demande de T2'],
  ];
  tiles.forEach(([h, b], i) => {
    const x = 0.6 + i * 4.1;
    card(s, 'Tuile ' + (i + 1), x, 5.75, 3.9, 1.05);
    txt(s, 'Tuile titre ' + (i + 1), h, { x: x + 0.2, y: 5.85, w: 3.5, h: 0.3, fontSize: 14, bold: true, color: C.accent1 });
    txt(s, 'Tuile texte ' + (i + 1), b, { x: x + 0.2, y: 6.17, w: 3.5, h: 0.6, fontSize: 14 });
  });
  s.addNotes('La décision est volontairement étroite. Nous n’arrêtons ni la puissance de la centrale, ni les prix, ni le financement. Si le Comité approuve, il reverra le dossier au jalon G1 avant toute nouvelle dépense.');

  // ---------- 3. Pourquoi étudier d'abord
  pres.addSection({ title: 'Analyse' });
  s = pres.addSlide({ masterName: 'CONTENU', sectionTitle: 'Analyse' });
  s.addText('Quatre incertitudes imposent d’étudier avant d’investir', { placeholder: 'title' });
  s.addText('Le protocole d’accord fixe une ambition, mais aucune de ses données clés n’a encore été vérifiée', { placeholder: 'body' });
  const facts = [
    [md.MdTerrain, 'Le terrain n’est pas attribué', 'Aucun site n’est alloué à ce jour. Il doit être identifié, visité et sécurisé avant toute ingénierie.'],
    [md.MdScale, 'Les tonnages ne concordent pas', 'Le protocole cite 4 millions de tonnes par an, puis 7 000 à 9 000 tonnes par jour, soit 2,6 à 3,3 millions. Le gisement doit être mesuré.'],
    [md.MdAccountBalance, 'Un acheteur unique, non vérifié', 'Le CSSPEVK achèterait l’électricité et paierait les redevances. Sa capacité juridique et financière reste à démontrer.'],
    [md.MdPrecisionManufacturing, 'La technologie n’est pas auditée', 'Les performances de Biodrum doivent être prouvées sur des déchets de Kinshasa et sur des installations de référence visitées.'],
  ];
  for (let i = 0; i < facts.length; i++) {
    const [I, h, b] = facts[i];
    const x = 0.6 + (i % 2) * 6.15, y = 1.85 + Math.floor(i / 2) * 2.2;
    card(s, 'Constat ' + (i + 1), x, y, 5.95, 2.0);
    circle(s, 'Pastille ' + (i + 1), x + 0.3, y + 0.3, 0.75, C.accent1);
    s.addImage({ data: await icon(I), x: x + 0.45, y: y + 0.45, w: 0.45, h: 0.45, altText: h, objectName: 'Icône ' + (i + 1) });
    txt(s, 'Constat titre ' + (i + 1), h, { x: x + 1.3, y: y + 0.3, w: 4.4, h: 0.4, fontSize: 18, bold: true, fontFace: THEME.headFontFace });
    txt(s, 'Constat texte ' + (i + 1), b, { x: x + 1.3, y: y + 0.8, w: 4.4, h: 1.1, fontSize: 14 });
  }
  txt(s, 'Rappel protocole', 'À noter : le protocole met l’intégralité des frais d’étude à la charge de VIPRO S.A (articles 8 et 11) ; les études restent sa propriété (article 12).', { x: 0.6, y: 6.35, w: 12.1, h: 0.5, fontSize: 14, italic: true, color: C.accent6 });
  s.addNotes('Ces quatre points ne sont pas des objections au projet. Ils expliquent pourquoi il serait imprudent de décider d’une centrale avant d’avoir mesuré les déchets, trouvé un terrain, vérifié le payeur et audité la technologie.');

  // ---------- 4. Options
  s = pres.addSlide({ masterName: 'CONTENU', sectionTitle: 'Analyse' });
  s.addText('Trois options s’offrent au Comité', { placeholder: 'title' });
  s.addText('Nous recommandons l’option A, qui conserve la faculté d’arrêter à faible coût', { placeholder: 'body' });
  const opts = [
    ['A', 'Approuver T1', 'Recommandée', C.accent1, [
      ['Engagement', '199 600 € HT'],
      ['Ce que l’on obtient', 'Diagnostic juridique, campagne pilote, premiers sites, seuils exigés par les banques, en trois à quatre mois'],
      ['Risque principal', 'Perdre cette dépense si un motif d’arrêt apparaît dès G1'],
    ]],
    ['B', 'Reporter', 'Non recommandée', C.accent6, [
      ['Engagement', 'Aucun'],
      ['Ce que l’on obtient', 'Du temps pour réunir d’autres informations, sans données nouvelles sur le projet'],
      ['Risque principal', 'Le calendrier du protocole continue de courir ; une saison manquée peut décaler les mesures de plusieurs mois'],
    ]],
    ['C', 'Renoncer', 'À écarter à ce stade', C.accent3, [
      ['Engagement', 'Aucun'],
      ['Ce que l’on obtient', 'Une sortie sans indemnité, après concertation avec le CSSPEVK (article 18)'],
      ['Risque principal', 'Abandonner le projet sans savoir s’il était viable'],
    ]],
  ];
  opts.forEach(([L, h, tag, col, rows], i) => {
    const x = 0.6 + i * 4.1;
    card(s, 'Option ' + L, x, 1.8, 3.9, 5.0);
    circle(s, 'Option lettre fond ' + L, x + 0.25, 2.0, 0.65, col);
    txt(s, 'Option lettre ' + L, L, { x: x + 0.25, y: 2.0, w: 0.65, h: 0.65, fontSize: 24, bold: true, color: C.background1, align: 'center', valign: 'middle', fontFace: THEME.headFontFace });
    txt(s, 'Option titre ' + L, h, { x: x + 1.05, y: 2.0, w: 2.7, h: 0.38, fontSize: 20, bold: true, fontFace: THEME.headFontFace });
    txt(s, 'Option statut ' + L, tag, { x: x + 1.05, y: 2.38, w: 2.7, h: 0.3, fontSize: 14, color: col, bold: true });
    let y = 2.95;
    rows.forEach(([k, v], j) => {
      txt(s, `Option ${L} rubrique ${j + 1}`, [{ text: k, options: { bold: true, color: C.accent6, breakLine: true } }, { text: v }], { x: x + 0.25, y, w: 3.4, h: j === 0 ? 0.6 : 1.25, fontSize: 14 });
      y += j === 0 ? 0.7 : 1.3;
    });
  });
  s.addNotes('Reporter n’est pas une option neutre : les campagnes de mesure doivent couvrir une saison sèche et une saison des pluies, et le protocole a une durée initiale de douze mois. Renoncer reste possible à tout moment, y compris après T1.');

  // ---------- 5. Exposition cumulée
  s = pres.addSlide({ masterName: 'CONTENU', sectionTitle: 'Analyse' });
  s.addText('La perte maximale reste limitée à chaque étape', { placeholder: 'title' });
  s.addText('Dépense cumulée si le Comité arrête l’étude au jalon indiqué, en milliers d’euros hors taxes', { placeholder: 'body' });
  const cum = [TR.T1, TR.T1 + TR.T2, TR.T1 + TR.T2 + TR.T3, TOT, TOT + TR.T5].map(v => Math.round(v / 1000));
  s.addChart(pres.charts.BAR, [{ name: 'Dépense cumulée', labels: ['Arrêt à G1', 'Arrêt à G2', 'Arrêt à G3', 'Fin d’étude (G4)', 'Avec APD (T5)'], values: cum }], {
    x: 0.6, y: 1.75, w: 7.6, h: 5.0, barDir: 'col', chartColors: [HEX.accent1, HEX.accent1, HEX.accent1, HEX.accent1, HEX.accent5],
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0', dataLabelFontSize: 13, dataLabelColor: HEX.dk1, dataLabelFontFace: '+mn-lt',
    catAxisLabelColor: HEX.dk1, catAxisLabelFontSize: 13, catAxisLabelFontFace: '+mn-lt', valAxisHidden: true,
    valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false, barGapWidthPct: 60, objectName: 'Graphique exposition',
  });
  const callouts = [
    ['10 %', 'de l’enveloppe est engagé si l’on s’arrête au premier jalon'],
    ['60 %', 'du budget n’est dépensé qu’après la validation du terrain, au jalon G2'],
    ['0 €', 'd’investissement industriel avant la décision finale du jalon G4'],
  ];
  callouts.forEach(([n, l], i) => {
    const y = 1.85 + i * 1.65;
    card(s, 'Repère ' + (i + 1), 8.6, y, 4.1, 1.45);
    txt(s, 'Repère chiffre ' + (i + 1), n, { x: 8.85, y: y + 0.15, w: 3.6, h: 0.6, fontSize: 32, bold: true, color: C.accent2, fontFace: THEME.headFontFace });
    txt(s, 'Repère texte ' + (i + 1), l, { x: 8.85, y: y + 0.78, w: 3.6, h: 0.6, fontSize: 14 });
  });
  s.addNotes('C’est l’argument central : l’étude est découpée pour que l’argent engagé suive les preuves obtenues. Si le terrain ou le gisement font défaut, l’arrêt intervient avant les dépenses les plus lourdes.');

  // ---------- 6. Jalons
  pres.addSection({ title: 'Gouvernance' });
  s = pres.addSlide({ masterName: 'CONTENU', sectionTitle: 'Gouvernance' });
  s.addText('Chaque jalon pose au Comité une question précise', { placeholder: 'title' });
  s.addText('Aucune tranche n’est lancée sans la décision du jalon qui la précède ; les délais restent indicatifs', { placeholder: 'body' });
  const head = ['Jalon', 'Mois', 'Question posée au Comité', 'Preuves à présenter', 'Ce que la décision débloque'];
  const gates = [
    ['G0', '0 à 1', 'L’étude est-elle bien cadrée ?', 'Directeur nommé, accès aux données, règles de confidentialité, exigences de l’ACE', 'Déjà couvert par T1'],
    ['G1', '2 à 4', 'Les hypothèses justifient-elles des mesures complètes ?', 'Diagnostic juridique, campagne pilote, plan d’échantillonnage validé, seuils des banques', `T2 : ${fmt(TR.T2)} €`],
    ['G2', '4 à 7', 'Le terrain et les déchets sont-ils assurés ?', 'Site et site de repli validés, premières mesures saisonnières, preuves technologiques', `T3 : ${fmt(TR.T3)} €`],
    ['G3', '7 à 11', 'Le projet est-il finançable ?', 'Avant-projet, raccordement, étude de marché, modèle financier, cadrage environnemental', `T4 : ${fmt(TR.T4)} €`],
    ['G4', '11 à 14', 'Faut-il investir ?', 'Audit indépendant, rapport final, revue des sept motifs d’arrêt', `Si GO, T5 (APD) : ${fmt(TR.T5)} €`],
  ];
  const hdr = head.map(h => ({ text: h, options: { bold: true, color: C.background1, fill: { color: C.text2 }, fontSize: 14 } }));
  const rows = gates.map((r, i) => r.map((c, j) => ({ text: c, options: { fontSize: 14, bold: j === 0, color: j === 0 ? C.accent1 : C.text1, fill: { color: i % 2 ? C.background1 : C.background2 } } })));
  s.addTable([hdr, ...rows], { x: 0.6, y: 1.8, w: 12.1, colW: [0.9, 1.0, 3.2, 4.6, 2.4], border: { type: 'solid', pt: 0.5, color: HEX.accent5 }, margin: 0.08, valign: 'middle', rowH: [0.45, 0.9, 0.9, 0.9, 0.9, 0.9], objectName: 'Tableau des jalons' });
  s.addNotes('Le Comité reste maître du rythme. À chaque jalon, il reçoit une fiche de décision et choisit entre poursuivre, poursuivre sous conditions ou arrêter.');

  // ---------- 7. Motifs d'arrêt
  s = pres.addSlide({ masterName: 'CONTENU', sectionTitle: 'Gouvernance' });
  s.addText('Sept motifs d’arrêt, vérifiés au bon moment', { placeholder: 'title' });
  s.addText('Un échec démontré arrête le projet ; une preuve encore manquante peut justifier une poursuite sous conditions écrites', { placeholder: 'body' });
  const stops = [
    ['X1', 'Terrain', 'Pas de droit foncier sûr, ni de moyen crédible de l’obtenir', 'G2'],
    ['X2', 'Déchets', 'Gisement mesuré insuffisant pour la capacité visée', 'G2, G3'],
    ['X3', 'Environnement', 'Exigences environnementales ou sociales impossibles à tenir', 'G3'],
    ['X4', 'Électricité', 'Pas de raccordement ni d’acheteur viables', 'G3'],
    ['X5', 'Technologie', 'Performances non garanties ou risque inacceptable', 'G2, G3'],
    ['X6', 'Payeur', 'Payeur incapable de payer, sans garantie crédible', 'G3'],
    ['X7', 'Rentabilité', 'Projet non viable dans les scénarios défavorables', 'G3, G4'],
  ];
  stops.forEach(([c, h, b, g], i) => {
    const col = i % 4, row = Math.floor(i / 4);
    const x = 0.6 + col * 3.07, y = 1.85 + row * 2.45;
    card(s, 'Motif ' + c, x, y, 2.87, 2.25);
    txt(s, 'Motif code ' + c, c, { x: x + 0.2, y: y + 0.15, w: 0.9, h: 0.5, fontSize: 24, bold: true, color: C.accent3, fontFace: THEME.headFontFace });
    txt(s, 'Motif titre ' + c, h, { x: x + 1.05, y: y + 0.2, w: 1.7, h: 0.45, fontSize: 16, bold: true, valign: 'middle' });
    txt(s, 'Motif texte ' + c, b, { x: x + 0.2, y: y + 0.75, w: 2.5, h: 0.95, fontSize: 14 });
    txt(s, 'Motif jalon ' + c, 'Vérifié à ' + g, { x: x + 0.2, y: y + 1.8, w: 2.5, h: 0.3, fontSize: 13, italic: true, color: C.accent6 });
  });
  const lx = 0.6 + 3 * 3.07, ly = 1.85 + 2.45;
  card(s, 'Règle', lx, ly, 2.87, 2.25, C.text2);
  txt(s, 'Règle texte', [{ text: 'Règle de décision', options: { bold: true, color: C.accent2, breakLine: true } }, { text: 'Les seuils financiers sont fixés avec les banques au jalon G1, et non par nous.', options: { color: C.background1 } }], { x: lx + 0.2, y: ly + 0.2, w: 2.5, h: 1.9, fontSize: 14 });
  s.addNotes('Ces sept motifs sont la protection principale des actionnaires. Ils sont vérifiés au moment où la preuve devient disponible, et non tous à la fin.');

  // ---------- 8. Budget
  s = pres.addSlide({ masterName: 'CONTENU', sectionTitle: 'Gouvernance' });
  s.addText('Ce que coûte l’étude, et la fiabilité du chiffre', { placeholder: 'title' });
  s.addText('Montants hors taxes en milliers d’euros, avant la provision pour aléas de 10 %', { placeholder: 'body' });
  s.addChart(pres.charts.BAR, [{ name: 'Montant', labels: LOTS.map(l => l[1]), values: LOTS.map(l => Math.round(l[2] / 1000)) }], {
    x: 0.6, y: 1.7, w: 7.4, h: 5.15, barDir: 'bar', chartColors: [HEX.accent1], catAxisOrientation: 'maxMin',
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0', dataLabelFontSize: 13, dataLabelColor: HEX.dk1, dataLabelFontFace: '+mn-lt',
    catAxisLabelColor: HEX.dk1, catAxisLabelFontSize: 13, catAxisLabelFontFace: '+mn-lt', valAxisHidden: true,
    valGridLine: { style: 'none' }, catGridLine: { style: 'none' }, showLegend: false, barGapWidthPct: 45, objectName: 'Graphique budget',
  });
  card(s, 'Total', 8.4, 1.8, 4.3, 1.55, C.text2);
  txt(s, 'Total chiffre', fmt(TOT) + ' €', { x: 8.65, y: 1.92, w: 3.8, h: 0.65, fontSize: 32, bold: true, color: C.accent2, fontFace: THEME.headFontFace });
  txt(s, 'Total texte', 'Tranches T1 à T4, aléas compris. Fourchette : 1,43 à 2,58 millions d’euros', { x: 8.65, y: 2.6, w: 3.8, h: 0.7, fontSize: 14, color: C.background1 });
  txt(s, 'Fiabilité', [
    { text: 'Estimation établie sans devis ; elle sera recalée au jalon G0 sur trois devis pour chaque sous-traitance de plus de 20 000 €.', options: { bullet: true, breakLine: true } },
    { text: 'Les travaux d’analyse au bureau sont valorisés à 50 % du tarif du marché, soit une réduction de 381 100 €.', options: { bullet: true, breakLine: true } },
    { text: 'Postes les plus incertains : essais technologiques, recensement des riverains, sondages.', options: { bullet: true, breakLine: true } },
    { text: 'Non compris : TVA, redevances administratives, douane, sécurité des équipes.', options: { bullet: true } },
  ], { x: 8.4, y: 3.6, w: 4.3, h: 3.25, fontSize: 14, paraSpaceAfter: 8 });
  s.addNotes('Le chiffre est un ordre de grandeur. Les références publiques utilisées sont le barème des Nations unies pour les consultants internationaux et des tarifs de laboratoire publiés. Il faut aussi conserver factures et feuilles de temps : en cas de demande de remboursement au titre de l’article 12, seuls les coûts réellement engagés comptent.');

  // ---------- 9. Livrables T1
  s = pres.addSlide({ masterName: 'CONTENU', sectionTitle: 'Gouvernance' });
  s.addText('Ce que la tranche T1 vous apportera au jalon G1', { placeholder: 'title' });
  s.addText('Trois livrables en trois à quatre mois, et une décision éclairée sur la suite', { placeholder: 'body' });
  const del = [
    ['Mois 1', 'Plan de travail', 'Équipe, données à obtenir, règles de qualité, de sécurité et de confidentialité'],
    ['Mois 3', 'Préfaisabilité et diagnostic juridique', 'Compétences des autorités, capacité du payeur, premiers sites possibles, revue de la technologie'],
    ['Mois 3', 'Campagne pilote de déchets', 'Premières pesées et analyses, plan d’échantillonnage validé par un statisticien'],
  ];
  del.forEach(([m, h, b], i) => {
    const x = 0.6 + i * 2.75;
    circle(s, 'Étape ' + (i + 1), x + 0.2, 2.1, 0.5, C.accent1);
    txt(s, 'Étape numéro ' + (i + 1), 'L' + i, { x: x + 0.2, y: 2.1, w: 0.5, h: 0.5, fontSize: 14, bold: true, color: C.background1, align: 'center', valign: 'middle' });
    txt(s, 'Étape mois ' + (i + 1), m, { x: x + 0.85, y: 2.17, w: 1.6, h: 0.35, fontSize: 14, bold: true, color: C.accent1 });
    card(s, 'Livrable ' + (i + 1), x, 2.9, 2.55, 3.9);
    txt(s, 'Livrable titre ' + (i + 1), h, { x: x + 0.2, y: 3.05, w: 2.15, h: 0.95, fontSize: 16, bold: true, fontFace: THEME.headFontFace });
    txt(s, 'Livrable texte ' + (i + 1), b, { x: x + 0.2, y: 3.9, w: 2.15, h: 2.75, fontSize: 14 });
  });
  card(s, 'Questions G1', 8.95, 1.85, 3.75, 4.95, C.text2);
  txt(s, 'Questions G1 texte', [
    { text: 'Au jalon G1, vous saurez :', options: { bold: true, color: C.accent2, breakLine: true } },
    { text: 'si le CSSPEVK peut juridiquement acheter et payer ;', options: { bullet: true, breakLine: true } },
    { text: 'si des terrains crédibles existent à Maluku ;', options: { bullet: true, breakLine: true } },
    { text: 'si la composition des déchets laisse espérer une valorisation ;', options: { bullet: true, breakLine: true } },
    { text: 'quels ratios les banques exigeront.', options: { bullet: true } },
  ], { x: 9.2, y: 2.05, w: 3.3, h: 4.6, fontSize: 15, color: C.background1, paraSpaceAfter: 10 });
  s.addNotes('C’est ce que le Comité achète avec 199 600 euros : les réponses aux questions qui peuvent arrêter le projet le plus tôt et au moindre coût.');

  // ---------- 10. Résolution
  pres.addSection({ title: 'Résolution' });
  s = pres.addSlide({ masterName: 'CLOTURE', sectionTitle: 'Résolution' });
  s.addText('Projet de résolution soumis au vote', { placeholder: 'title' });
  txt(s, 'Résolution', [
    { text: 'Le Comité d’investissement de VIPRO S.A, après examen des termes de référence V3.0 du 13 novembre 2026 :', options: { breakLine: true, bold: true } },
    { text: 'approuve la tranche T1 de l’étude de faisabilité Kia Mona II, plafonnée à 199 600 € HT ;', options: { bullet: { type: 'number' }, breakLine: true } },
    { text: 'désigne M. ou Mme ........................................ comme Directeur d’étude ;', options: { bullet: { type: 'number' }, breakLine: true } },
    { text: 'subordonne le lancement de la tranche T2 à la revue du jalon G1 ;', options: { bullet: { type: 'number' }, breakLine: true } },
    { text: 'décide qu’aucun contrat de construction, aucune dette et aucune garantie ne seront engagés avant le jalon G4 ;', options: { bullet: { type: 'number' }, breakLine: true } },
    { text: 'demande la conservation des factures et des feuilles de temps justifiant les coûts engagés.', options: { bullet: { type: 'number' } } },
  ], { x: 0.6, y: 1.4, w: 7.6, h: 5.3, fontSize: 16, color: C.background1, paraSpaceAfter: 10 });
  card(s, 'Bulletin', 8.6, 1.4, 4.1, 5.3, C.background1);
  txt(s, 'Bulletin titre', 'Vote', { x: 8.9, y: 1.6, w: 3.5, h: 0.5, fontSize: 22, bold: true, fontFace: THEME.headFontFace, color: C.text2 });
  ['Pour', 'Contre', 'Abstention'].forEach((v, i) => {
    s.addShape(pres.shapes.RECTANGLE, { x: 8.9, y: 2.35 + i * 0.6, w: 0.32, h: 0.32, fill: { color: C.background1 }, line: { color: HEX.dk2, width: 1.25 }, objectName: 'Case ' + v });
    txt(s, 'Libellé ' + v, v, { x: 9.4, y: 2.33 + i * 0.6, w: 2.8, h: 0.36, fontSize: 16, color: C.text2, valign: 'middle' });
  });
  txt(s, 'Bulletin date', 'Date : ....................................', { x: 8.9, y: 4.4, w: 3.5, h: 0.4, fontSize: 14, color: C.text2 });
  txt(s, 'Bulletin signature', 'Nom et signature :', { x: 8.9, y: 5.0, w: 3.5, h: 0.4, fontSize: 14, color: C.text2 });
  s.addNotes('La résolution reprend mot pour mot les quatre conditions présentées au début. Le nom du Directeur d’étude est à compléter en séance.');

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log('written', OUT);
})();
