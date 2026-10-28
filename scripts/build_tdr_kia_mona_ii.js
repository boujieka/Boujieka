const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, HeadingLevel,
  AlignmentType, WidthType, ShadingType, BorderStyle, LevelFormat, PageBreak,
  Header, Footer, PageNumber, TableOfContents, PageOrientation,
} = require('docx');

const FONT = 'Arial';
const W = 9638; // largeur utile A4 avec marges 2 cm (11906 - 2*1134)
const ACCENT = '1F4E79';
const LIGHT = 'DCE6F1';
const GREY = 'F2F2F2';

// ---------- helpers ----------
function runs(text, opts = {}) {
  // **gras** en ligne
  const parts = String(text).split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
  return parts.map(p => p.startsWith('**')
    ? new TextRun({ text: p.slice(2, -2), bold: true, font: FONT, size: opts.size || 20, color: opts.color })
    : new TextRun({ text: p, font: FONT, size: opts.size || 20, italics: opts.italics, color: opts.color, bold: opts.bold }));
}
const P = (t, o = {}) => new Paragraph({ children: runs(t, o), spacing: { after: 120, line: 276 }, alignment: o.align || AlignmentType.JUSTIFIED });
const Note = t => new Paragraph({ children: runs(t, { italics: true, size: 18, color: '404040' }), spacing: { after: 120 },
  border: { left: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 6 } }, indent: { left: 200 } });
const H1 = t => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun({ text: t })], pageBreakBefore: false });
const H2 = t => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: t })] });
const H3 = t => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun({ text: t })] });
const B = (t, lvl = 0) => new Paragraph({ numbering: { reference: 'bul', level: lvl }, children: runs(t), spacing: { after: 60 } });
const N = (t, ref = 'num') => new Paragraph({ numbering: { reference: ref, level: 0 }, children: runs(t), spacing: { after: 60 } });
const BR = () => new Paragraph({ children: [new PageBreak()] });

const border = { style: BorderStyle.SINGLE, size: 4, color: 'A6A6A6' };
const borders = { top: border, bottom: border, left: border, right: border };

function T(header, rows, widths, o = {}) {
  const total = widths.reduce((a, b) => a + b, 0);
  const scale = W / total;
  const cw = widths.map(w => Math.floor(w * scale));
  cw[cw.length - 1] += W - cw.reduce((a, b) => a + b, 0);
  const mk = (txt, i, head, shade) => new TableCell({
    width: { size: cw[i], type: WidthType.DXA }, borders,
    shading: head ? { fill: ACCENT, type: ShadingType.CLEAR, color: 'auto' } : (shade ? { fill: shade, type: ShadingType.CLEAR, color: 'auto' } : undefined),
    margins: { top: 60, bottom: 60, left: 90, right: 90 },
    children: String(txt).split('\n').map(line => new Paragraph({ children: runs(line, { size: 17, color: head ? 'FFFFFF' : undefined, bold: head }), spacing: { after: 20 } })),
  });
  const trs = [new TableRow({ tableHeader: true, children: header.map((h, i) => mk(h, i, true)) })];
  rows.forEach((r, ri) => {
    const isTotal = o.totalLast && ri === rows.length - 1;
    trs.push(new TableRow({ cantSplit: true, children: r.map((c, i) => mk(isTotal ? `**${c}**` : c, i, false, isTotal ? LIGHT : (ri % 2 ? GREY : undefined))) }));
  });
  return [new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cw, rows: trs }), new Paragraph({ spacing: { after: 120 }, children: [] })];
}

// ---------- contenu ----------
const C = [];
const add = (...x) => x.flat().forEach(e => C.push(e));

// Page de garde
add(
  new Paragraph({ spacing: { before: 1800, after: 200 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'RÉPUBLIQUE DÉMOCRATIQUE DU CONGO', font: FONT, size: 22, bold: true, color: '595959' })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 }, children: [new TextRun({ text: 'Protocole d’accord CSSPEVK – VIPRO S.A (version de juillet 2026)', font: FONT, size: 20, color: '595959' })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: 'TERMES DE RÉFÉRENCE', font: FONT, size: 44, bold: true, color: ACCENT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: 'Étude de faisabilité détaillée technique, financière, économique, environnementale et sociale', font: FONT, size: 28, bold: true })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 800 }, children: [new TextRun({ text: 'Système intégré de gestion des déchets solides municipaux et de valorisation énergétique « Kia Mona II » — Commune de Maluku, Ville de Kinshasa', font: FONT, size: 24 })] }),
  ...T(['Rubrique', 'Information'], [
    ['Statut du document', 'Version complète de travail (V1.0) — à valider par le Comité de Suivi CSSPEVK – VIPRO S.A avant toute consultation'],
    ['Date', '28 octobre 2026'],
    ['Base documentaire', 'Protocole d’accord CSSPEVK – VIPRO S.A, juillet 2026 (version révisée transmise) ; TdR de travail du 28 octobre 2026'],
    ['Mode de réalisation', 'Étude réalisée par Claude Code et un réseau d’agents IA ; contrôle qualité par des agents IA de revue, Gemini et ChatGPT ; travaux de terrain, signatures et validations indépendantes assurés par des personnes et organismes qualifiés (chapitres 6 et 18)'],
    ['Confidentialité', 'Document soumis aux articles 12 et 16 du Protocole et au NCNDA (Annexe B)'],
  ], [2600, 7000]),
  BR(),
);

// Mode d'emploi
add(
  H1('Mode de lecture et conventions'),
  P('Les présents Termes de Référence (TdR) distinguent systématiquement l’origine et le niveau de certitude de chaque élément. Les marqueurs suivants sont utilisés dans l’ensemble du document :'),
  ...T(['Marqueur', 'Signification', 'Conséquence pour l’étude'], [
    ['[P]', 'Élément tiré du Protocole d’accord (déclaratif, indicatif et non engageant selon l’article 4)', 'Doit être vérifié ; ne vaut pas donnée observée'],
    ['[TdR]', 'Exigence ou proposition introduite par les présents TdR', 'Opposable au Consultant une fois les TdR validés'],
    ['[Q]', 'Quantité minimale indicative (échantillons, sondages, hommes-mois)', 'À confirmer ou ajuster par le Consultant dans son offre technique, avec justification'],
    ['[V]', 'Point devant faire l’objet d’une validation indépendante', 'Ne peut être réceptionné sur la seule base du rapport du Consultant'],
  ], [1200, 5000, 3400]),
  P('Dans les présents TdR, le terme « Consultant » désigne le dispositif de réalisation de l’étude, c’est-à-dire le réseau d’agents IA piloté par Claude Code, ses responsables humains et ses prestataires de terrain, placé sous la responsabilité de VIPRO S.A (article 8 du Protocole).'),
  P('Trois modes d’exécution sont distingués pour chaque tâche :'),
  B('**Mode D — à distance** : travaux de bureau réalisables sans présence sur site (revue documentaire, SIG, modélisation, rédaction), exécutés par le réseau d’agents IA piloté par Claude Code.'),
  B('**Mode T — terrain obligatoire** : mesures, prélèvements, enquêtes, levés, sondages, consultations et entretiens qui ne peuvent être remplacés par une source secondaire ni par une estimation.'),
  B('**Mode V — validation indépendante** : contrôle par une entité distincte de l’auteur (laboratoire accrédité, ingénieur indépendant, auditeur de modèle, autorité compétente, gestionnaire de réseau).'),
  Note('Avertissement : les textes juridiques, statistiques de déchets, capacités et caractéristiques technologiques cités proviennent du Protocole et n’ont pas été vérifiés de manière indépendante pour la rédaction des présents TdR. Les ordres de grandeur numériques présentés au chapitre 11 sont des calculs illustratifs fondés sur des paramètres hypothétiques, non des données de conception.'),
  BR(),
  new Paragraph({ children: [new TextRun({ text: 'Sommaire', font: FONT, size: 28, bold: true, color: ACCENT })], spacing: { after: 200 } }),
  new TableOfContents('Sommaire', { hyperlink: true, headingStyleRange: '1-2' }),
  Note('Mettre à jour le sommaire dans Word : clic droit > Mettre à jour les champs.'),
  BR(),
);

// 1 Contexte
add(
  H1('1. Contexte et fondement documentaire'),
  P('Le Protocole d’accord conclu entre le Comité Stratégique pour la Supervision du Projet d’Extension de la Ville de Kinshasa (CSSPEVK) et la société VIPRO S.A établit un cadre de collaboration non engageant financièrement pour la préparation d’une Solution Intégrée de Gestion des Déchets couvrant la sensibilisation, la pré-collecte, le tri mécanique, le recyclage des matières valorisables et la Valorisation Énergétique de la seule fraction résiduelle non recyclable, au moyen de la technologie Biodrum [P].'),
  P('Les hypothèses de structuration retenues par le Protocole (article 4) sont reprises ci-dessous avec leur statut. Aucune n’est considérée comme acquise par les présents TdR.'),
  ...T(['Paramètre', 'Hypothèse du Protocole [P]', 'Statut [P]', 'Traitement par l’étude [TdR]'], [
    ['Capacité', '1 unité Biodrum de 16 MW (Jalon 1) ; 2e unité facultative de 16 MW (32 MW cumulés)', 'Provisoire, à valider en Phase 2', 'Trois scénarios : 16 MW, 32 MW, capacité optimisée (chapitre 11)'],
    ['Structure juridique', 'Concession BOT, loi n° 14/011 du 17 juin 2014', 'À confirmer en Phase 3', 'Volet 12 : vérification juridique et montage'],
    ['Acheteur d’énergie', 'CSSPEVK, contrepartie unique (PPA)', 'Hypothèse de travail', 'Vérification de capacité juridique et financière (volets 1, 8, 12)'],
    ['Redevances déchets', 'Tipping fees payées par le CSSPEVK', 'Hypothèse de travail', 'Analyse de solvabilité et de source de paiement'],
    ['Monnaie', 'Contrats libellés en euros', 'Principe directeur', 'Modèle en EUR avec analyse du risque CDF/convertibilité'],
    ['Financement', 'Fonds propres et dette senior VIPRO S.A et investisseurs, sans budget de l’État', 'Sous réserve du bouclage financier', 'Plan de financement et tests de bancabilité (volet 9)'],
    ['Durée', '25 ans à compter du bouclage financier, construction incluse', 'Ferme, à préciser', 'Voir incohérence n° 3 (chapitre 2)'],
    ['Site', 'Commune de Maluku ; site non encore alloué', '—', 'Identification et validation : préalable à l’ingénierie détaillée (volet 3)'],
  ], [1500, 3100, 1700, 3300]),
  P('Le Protocole prévoit également qu’une **étude de marché actualisée** soit réalisée et soumise au CSSPEVK et qu’elle conditionne le passage à la Phase 3 (article 3.1) [P]. Elle est intégrée au volet 8 des présents TdR.'),
);

// 2 Incohérences
add(
  H1('2. Points du Protocole à clarifier avant ou au démarrage'),
  P('La lecture du Protocole fait apparaître des points qui affectent directement la conception de l’étude. Ils ne remettent pas en cause le Protocole mais doivent être tranchés par le Comité de Suivi, faute de quoi certains résultats de l’étude ne seraient pas interprétables.'),
  ...T(['N°', 'Constat (référence)', 'Effet sur l’étude', 'Décision attendue'], [
    ['1', 'Le préambule mentionne « environ 4 millions de tonnes » par an et « entre 7 000 et 9 000 tonnes par jour ». Or 7 000 à 9 000 t/j correspondent à environ 2,6 à 3,3 Mt/an, et 4 Mt/an à environ 11 000 t/j.', 'Le gisement de référence ne peut pas être tiré du Protocole.', 'Traiter ces chiffres comme non vérifiés ; le volet 2 établit le gisement par mesure.'],
    ['2', 'Le Protocole place l’IEE (M12–M15) après les études d’impact (M6–M12), alors qu’un examen initial précède usuellement une EIES.', 'Risque de séquence réglementaire inadaptée.', 'Faire confirmer la procédure et la séquence par l’ACE dès l’étape E0.'],
    ['3', 'Article 4 : concession de 25 ans à compter du bouclage financier, construction incluse. Annexe C : PPA de 25 ans à compter de la mise en service commerciale (COD).', 'La durée d’exploitation rémunérée diffère de la durée de la construction (environ 2 à 3 ans, à confirmer).', 'Arrêter une hypothèse de base ; le modèle testera les deux.'],
    ['4', 'Annexe C.2 : fourniture des déchets « par VIPRO S.A », contrat entre SPV et CSSPEVK, redevance payée par le CSSPEVK ; article 8 : VIPRO S.A assure l’approvisionnement.', 'Le débiteur de l’obligation de volume (put-or-pay) n’est pas identifiable ; le risque de volume ne peut pas être alloué.', 'Clarifier fournisseur, payeur et porteur du risque de volume.'],
    ['5', 'Article 9.1 (30 j, puis 8 j et 15 j d’escalade avant acceptation réputée) et article 10 (acceptation réputée à défaut d’observations sous 30 j) prévoient deux mécanismes différents.', 'Ambiguïté sur la date de réception des livrables.', 'Retenir un mécanisme unique (chapitre 17).'],
    ['6', 'L’APD figure à l’article 3.1 (études de faisabilité) et à la Phase 3 de l’article 6 (sous réserve de conclusions positives).', 'Ambiguïté sur le niveau d’ingénierie attendu de l’étude.', 'Proposition [TdR] : avant-projet sommaire dans l’étude ; APD en tranche conditionnelle après le jalon G4.'],
    ['7', 'Le Protocole a une durée de 12 mois, renouvelable automatiquement « conformément à la Loi Applicable » (article 17) ; l’étude dure environ 13 mois après mobilisation.', 'L’étude dépasse la durée initiale du Protocole.', 'Confirmer le renouvellement par écrit (article 24).'],
    ['8', 'L’étude est la propriété exclusive de VIPRO S.A, confidentielle et connue des seules Parties (article 12).', 'Un ingénieur indépendant, des prêteurs ou l’ACE doivent y accéder ; l’indépendance de l’étude n’est pas garantie par sa seule commande.', 'Autorisation écrite de VIPRO S.A définissant les droits d’accès des valideurs (chapitre 19).'],
    ['9', 'L’article 2 renvoie aux « Études visées à l’Article 2 » et l’article 5 au « chronogramme détaillé visé à l’Article 9 », que l’article 9 ne contient pas.', 'Renvois internes imprécis.', 'Correction de forme par avenant si nécessaire.'],
  ], [500, 3700, 2700, 2700]),
);

// 3 Objectifs
add(
  H1('3. Objectifs de l’étude et décisions attendues'),
  H2('3.1 Objectif général'),
  P('Établir, sur la base de données vérifiées, si la Solution Intégrée de Gestion des Déchets et sa composante de Valorisation Énergétique sont techniquement réalisables, juridiquement structurables, environnementalement et socialement acceptables, économiquement justifiées et finançables. L’étude doit permettre de déterminer la configuration, le site, le phasage et les conditions contractuelles qui offrent le meilleur rapport coût-bénéfice, conformément à l’article 8 du Protocole.'),
  H2('3.2 Objectifs spécifiques'),
  N('Quantifier et caractériser le gisement de déchets mobilisable, par saison et par origine, sur un horizon de 25 ans.'),
  N('Identifier, comparer et faire valider un site préférentiel et un site de repli dans la Commune de Maluku.'),
  N('Vérifier de manière indépendante la maturité, les performances et les garanties de la technologie Biodrum, et la comparer à des alternatives crédibles.'),
  N('Comparer trois scénarios de puissance (16 MW, 32 MW, capacité optimisée) et un scénario sans valorisation énergétique.'),
  N('Concevoir la chaîne complète : pré-collecte, collecte, transfert, tri, recyclage, traitement de la fraction organique, valorisation énergétique, gestion des résidus.'),
  N('Définir le raccordement électrique et sa faisabilité avec le gestionnaire de réseau.'),
  N('Produire un modèle financier ouvert et audité, une analyse économique coûts-avantages et une évaluation de la bancabilité.'),
  N('Préparer l’EIES et ses instruments selon la procédure de l’ACE.'),
  N('Proposer la structuration BOT/PPA/WSA, la matrice des risques et le plan de mise en œuvre.'),
  H2('3.3 Décision finale attendue'),
  P('L’étude se conclut par une recommandation motivée **GO / GO conditionnel / NO-GO** fondée sur les critères du chapitre 22, et non sur la seule rentabilité financière.'),
);

// 4 Périmètre
add(
  H1('4. Périmètre de l’étude'),
  H2('4.1 Périmètre fonctionnel : la chaîne complète'),
  ...T(['Maillon', 'Contenu minimal', 'Liens avec les autres maillons'], [
    ['1. Sensibilisation et pré-collecte', 'Tri à la source, conteneurisation, pré-collecte de proximité, intégration du secteur informel', 'Qualité du gisement, taux de captage'],
    ['2. Collecte et transport', 'Circuits, flotte, fréquences, coûts, stations de transfert', 'Coût à la tonne livrée, distance au site'],
    ['3. Réception et tri', 'Pesée, tri mécanique et manuel, refus', 'Bilan matière, fraction résiduelle'],
    ['4. Recyclage', 'Plastiques, métaux, verre, papier-carton : filières, débouchés et prix', 'Revenus matières, réduction du PCI résiduel'],
    ['5. Traitement de la fraction organique', 'Compostage, digestion anaérobie ou séchage : options à comparer', 'Humidité et PCI de la fraction énergétique'],
    ['6. Valorisation énergétique', 'Chaîne Biodrum complète : préparation, conversion, récupération d’énergie, épuration des fumées', 'Puissance nette, émissions'],
    ['7. Résidus et rejets', 'Mâchefers, cendres volantes, résidus d’épuration, lixiviats, effluents ; exutoires', 'Coûts, conformité, besoin de CET'],
    ['8. Évacuation de l’énergie', 'Poste de livraison, ligne, point de raccordement', 'Production livrable, revenus PPA'],
  ], [2300, 4300, 3000]),
  H2('4.2 Périmètre géographique'),
  B('Zone d’implantation : Commune de Maluku, périmètre du Projet d’Extension de la Ville de Kinshasa (Kia Mona) [P].'),
  B('Zone de gisement : communes de Kinshasa et zones de Kia Mona susceptibles d’alimenter l’Installation ; leur délimitation est un résultat du volet 2, fondé sur les coûts de transport.'),
  B('Corridors : accès routiers et couloirs de raccordement électrique.'),
  H2('4.3 Hors périmètre'),
  B('Déchets dangereux, médicaux non traités, radioactifs ou explosifs, sauf pour définir leur exclusion et leur gestion séparée.'),
  B('Les capacités supérieures à 32 MW sont étudiées comme variante analytique ; leur mise en œuvre sort du cadre contractuel actuel et nécessiterait un accord des Parties par avenant (article 24) [TdR].'),
  B('La négociation juridique des Documents Contractuels Définitifs (Phase 3 du Protocole) : l’étude prépare des term sheets indicatifs, elle ne négocie pas.'),
);

// 5 Modes
add(
  H1('5. Répartition des travaux : à distance, terrain, validation indépendante'),
  P('Le tableau suivant constitue la matrice de référence. Le Consultant la reprend dans son offre en précisant, pour chaque tâche, les moyens, les responsables et la durée.'),
  ...T(['Volet', 'Mode D — agents IA (Claude Code)', 'Mode T — terrain (prestataires humains)', 'Mode V — validation indépendante (humaine)'], [
    ['V1 Institutionnel et juridique', 'Revue des textes, cartographie des compétences, matrice des autorisations', 'Entretiens institutionnels, collecte des actes officiels', 'Avis juridique d’un cabinet congolais inscrit au barreau'],
    ['V2 Gisement et collecte', 'Revue des données existantes, SIG, modèle de projection, optimisation des circuits', 'Pesées, caractérisation, échantillonnage, comptages, enquêtes opérateurs', 'Laboratoire accrédité ISO/IEC 17025 ; revue statistique du plan'],
    ['V3 Site et foncier', 'Long-list SIG, contraintes, analyse multicritère préliminaire', 'Visites, topographie, géotechnique, hydrologie, enquête foncière, consultations', 'Vérification foncière auprès des services compétents ; rapport géotechnique signé'],
    ['V4 Technologie', 'Revue des références, comparaison des options, bilans', 'Visites de références, essais sur échantillons représentatifs', 'Ingénieur procédés indépendant du fournisseur'],
    ['V5 Dimensionnement', 'Bilans masse-énergie, simulations, P50/P90', '— (dépend des mesures V2 et V4)', 'Ingénieur indépendant'],
    ['V6 Ingénierie', 'Plans de principe, PFD, plan masse, estimation des coûts', 'Relevés des réseaux d’eau et routes, accès, utilités', 'Revue d’ingénierie indépendante'],
    ['V7 Raccordement', 'Études de répartition de charge et de court-circuit sur données fournies', 'Inspection des postes et lignes, réunions techniques', 'Avis écrit du gestionnaire de réseau'],
    ['V8 Marché et revenus', 'Analyse de prix, de la demande et de la concurrence', 'Entretiens recycleurs et acheteurs, relevés de prix, lettres d’intérêt', 'Triangulation des sources'],
    ['V9 Coûts et finance', 'Modèle financier, sensibilités, code de recalcul', 'Collecte de devis et de prix locaux', 'Audit du modèle par un auditeur indépendant'],
    ['V10 Économie', 'Analyse coûts-avantages, contrefactuel', 'Enquêtes ciblées ménages et entreprises', 'Revue par un économiste indépendant'],
    ['V11 Environnement et social', 'Cadrage, revue, modélisation de dispersion', 'État initial, recensement, consultations publiques', 'Approbation par l’ACE ; conformité aux normes des prêteurs'],
    ['V12 Structuration et mise en œuvre', 'Matrice des risques, term sheets, plan de mise en œuvre', 'Consultations prêteurs, assureurs, autorités', 'Revue par les conseils juridiques des Parties'],
  ], [1700, 2700, 2700, 2500]),
);

// 6 IA
add(
  H1('6. Organisation de l’étude par agents IA et contrôle qualité multi-modèles'),
  P('L’étude est réalisée par **Claude Code et un réseau d’agents IA** qu’il orchestre. Le contrôle qualité est assuré par des **agents IA de revue, Gemini et ChatGPT**. Ce mode de réalisation couvre l’ensemble des travaux de mode D. Il ne couvre pas les travaux de mode T ni les validations de mode V, qui exigent une présence physique, une accréditation, une responsabilité professionnelle ou une compétence réglementaire qu’un système d’IA ne possède pas.'),
  H2('6.1 Architecture du réseau d’agents'),
  ...T(['Composant', 'Rôle', 'Produits'], [
    ['Orchestrateur (Claude Code)', 'Planifie les tâches, distribue le travail aux agents, intègre les résultats, tient le dépôt, le registre des variables et le journal', 'Plan de travail, dépôt versionné, livrables consolidés'],
    ['Agents de volet (un par volet V1 à V12)', 'Recherche documentaire, analyse, calculs, modélisation, rédaction pour leur volet', 'Notes, données traitées, code, chapitres de livrables'],
    ['Agent données et SIG', 'Ingestion des données de terrain, contrôles de cohérence, traitements spatiaux', 'Bases de données, cartes, contrôles automatiques'],
    ['Agent modèles', 'Bilans masse-énergie, modèle financier en code, sensibilités, tests', 'Code, résultats reproductibles, tests'],
    ['Agent rédaction', 'Mise en forme des livrables en français, tableaux des réserves', 'Livrables L0 à L10'],
    ['Agents de revue (Claude, distincts des agents producteurs)', 'Revue contradictoire de chaque livrable : cohérence, sources, calculs, conformité aux TdR', 'Rapports de revue'],
    ['Gemini et ChatGPT (revue croisée)', 'Contre-expertise indépendante du modèle producteur : recherche d’erreurs, d’hypothèses non étayées et de sources invérifiables', 'Rapports de revue croisée'],
  ], [2400, 4400, 2800]),
  H2('6.2 Trois niveaux de contrôle qualité'),
  ...T(['Niveau', 'Contrôleur', 'Contenu', 'Portée'], [
    ['N1 — automatique', 'Tests du dépôt', 'Tests unitaires, bouclage masse, énergie et trésorerie, contrôle des unités, comparaison tableur et code', 'Erreurs de calcul et d’intégrité'],
    ['N2 — revue multi-modèles', 'Agents de revue, Gemini, ChatGPT', 'Relecture contradictoire, vérification des sources citées, recalculs indépendants, recherche des contradictions', 'Contrôle qualité interne ; ne vaut pas validation'],
    ['N3 — validation indépendante', 'Personnes et organismes qualifiés (chapitre 18)', 'Validation technique, scientifique, juridique et réglementaire', 'Seul niveau opposable aux autorités, aux prêteurs et au Comité de Suivi'],
  ], [1700, 2200, 3700, 2000]),
  Note('Pourquoi le niveau N2 ne remplace pas le niveau N3 : des modèles d’IA différents peuvent partager les mêmes sources publiques et les mêmes erreurs. Leur accord ne prouve pas qu’une donnée est exacte. Aucun modèle ne peut constater un fait sur le terrain ni engager une responsabilité professionnelle.'),
  H2('6.3 Ce que le réseau d’agents ne peut pas faire'),
  B('Peser, trier ou prélever des déchets, réaliser des sondages, des levés, des mesures environnementales ou des essais : ces travaux sont confiés à des prestataires de terrain, dont les données brutes alimentent les agents.'),
  B('Conduire les consultations publiques et le recensement des personnes affectées, qui exigent des enquêteurs humains et le consentement éclairé des personnes.'),
  B('Signer un rapport géotechnique, un avis juridique, une EIES ou un avis d’ingénieur indépendant, ni répondre d’une faute professionnelle.'),
  B('Obtenir des données non publiques (réseau, foncier, tonnages) sans demande formelle d’une personne habilitée.'),
  B('Garantir que la procédure de l’ACE accepte une EIES produite par IA : le statut exigé de l’auteur (bureau d’études agréé ou non) est à vérifier auprès de l’ACE à l’étape E0.'),
  H2('6.4 Règles non négociables'),
  B('Toute sortie d’IA est une donnée de niveau C (chapitre 7) tant qu’elle n’est pas vérifiée sur une source primaire ou par une mesure.'),
  B('Il est interdit de créer, compléter ou « estimer » des résultats de laboratoire, des devis, des coordonnées de parcelles, des références industrielles, des citations ou des textes juridiques.'),
  B('Chaque référence citée est vérifiée sur la source primaire (lien, page, date de consultation), puis contrôlée en revue N2.'),
  B('Tout calcul clé (puissance nette, CAPEX, TRI, DSCR) est recalculé par une seconde méthode : tableur et code, et revue par un second modèle.'),
  B('Un agent de revue ne révise jamais son propre travail ; les désaccords entre modèles sont consignés et tranchés par le responsable humain de l’étude.'),
  B('Un **responsable humain de l’étude** désigné par VIPRO S.A répond des livrables devant le Comité de Suivi (chapitre 16).'),
  H2('6.5 Confidentialité et données'),
  P('Les informations échangées sont protégées par l’article 16 et le NCNDA (Annexe B), qui limite la divulgation aux dirigeants, employés, conseils, affiliés et partenaires liés par une confidentialité équivalente. L’envoi de documents vers des services d’IA hébergés par des tiers (Anthropic, Google, OpenAI) peut constituer une telle divulgation. En conséquence [TdR] :'),
  B('les Parties approuvent par écrit, avant le démarrage, la liste des outils, les offres utilisées (paramètres de conservation et d’entraînement sur les données) et les catégories d’informations autorisées pour chacun ;'),
  B('les données personnelles (enquêtes, recensement) sont pseudonymisées avant tout traitement par IA ;'),
  B('les informations protégées au titre de l’article 12 (technologie Biodrum, savoir-faire) ne sont pas transmises aux outils sans l’accord écrit de leur titulaire ; à défaut, la revue N2 de ces éléments est faite sur des extraits autorisés.'),
  H2('6.6 Traçabilité et reproductibilité'),
  B('Dépôt versionné (Git) : /data_raw (lecture seule, empreintes de contrôle), /data_processed, /src, /models, /tests, /gis, /reports, /docs, /ai_log, /reviews.'),
  B('Journal d’IA (/ai_log) : date, agent ou modèle et version, objet, résumé de la demande, sortie retenue, vérification, contrôleur (gabarit en Annexe G).'),
  B('Rapports de revue N2 archivés (/reviews) avec le statut de chaque observation : acceptée, rejetée avec motif, ou transmise au niveau N3.'),
  B('Environnement figé, scripts exécutables de bout en bout ; toute figure ou tout tableau de livrable est régénérable à partir du dépôt.'),
);

// 7 Données
add(
  H1('7. Qualité et provenance des données'),
  ...T(['Niveau', 'Définition', 'Usage autorisé'], [
    ['A', 'Mesure de terrain selon protocole validé ; analyse de laboratoire accrédité ; document officiel vérifié', 'Cas de base, après contrôle qualité'],
    ['B', 'Source secondaire corroborée, dont la date, le périmètre et la méthode sont connus', 'Cas de base avec sensibilité explicite'],
    ['C', 'Hypothèse non vérifiée, déclaration non documentée, sortie d’IA', 'Scénarios uniquement ; interdite comme donnée observée'],
  ], [900, 5500, 3200]),
  P('Le registre des variables (Annexe F) indique pour chaque variable : identifiant, libellé, unité, valeur, plage d’incertitude, date, géographie, source, droit d’usage, méthode, niveau A/B/C, responsable et version. **Seuil de réception [TdR]** : au jalon G4, les variables qui déterminent plus de 80 % de la variance du TRI projet doivent être de niveau A ou B.'),
);

// 8 Volets
add(H1('8. Description détaillée des volets d’études'));
const volets = [
  ['V1 — Cadre institutionnel, juridique et réglementaire', 'Établir les compétences, autorisations et conditions juridiques préalables.', [
    'Cartographier les compétences effectives du CSSPEVK, de la Ville-Province, de la REGEDEK, de la Commission Permanente sur l’Électricité, de l’ARE, de l’ACE, de l’ANAPI, de la DGI et de la DGDA.',
    'Vérifier les textes cités par le Protocole (Code des investissements, loi n° 14/011, décrets relatifs au CSSPEVK, arrêté n° 043/CAB-MIN/RHE/ASM/2026) dans leur version en vigueur.',
    'Analyser la capacité juridique du CSSPEVK à conclure un PPA, à payer des redevances et à consentir des droits fonciers ; identifier la source de ses ressources.',
    'Établir le calendrier et le chemin critique des autorisations (EIES, licence ou concession de production, foncier, construction).',
    'Examiner l’éligibilité au régime du Code des investissements et les incidences fiscales.',
  ], 'Matrice de conformité ; calendrier des autorisations ; avis juridique ; liste des conditions préalables contractuelles.', 'Avis signé par un cabinet d’avocats congolais ; copies certifiées des actes.'],
  ['V2 — Gisement de déchets et chaîne de collecte', 'Mesurer le gisement mobilisable et concevoir la chaîne de collecte.', [
    'Revue des données disponibles (REGEDEK, programmes provinciaux, études antérieures dont celle de VIPRO S.A).',
    'Campagnes de mesure selon le plan d’échantillonnage du chapitre 9 et de l’Annexe B.',
    'Bilan matière : déchets générés, collectés, captables, recyclables, organiques, résiduels, refus.',
    'Projection sur 25 ans : démographie, urbanisation de Kia Mona, revenu, effets des programmes de tri.',
    'Conception de la chaîne : pré-collecte, circuits, flotte, stations de transfert ; coût complet à la tonne livrée.',
    'Analyse du secteur informel (récupérateurs) : effectifs, revenus, risques de déplacement économique.',
  ], 'Base de données géoréférencée ; rapport de caractérisation ; bilan matière ; prévisions P50/P90 ; plan de collecte.', 'Laboratoire accrédité ; revue statistique indépendante de la représentativité.'],
  ['V3 — Identification, sélection et validation du site (préalable)', 'Sécuriser un site préférentiel et un site de repli avant toute ingénierie détaillée.', [
    'Procédure en quatre étapes décrite au chapitre 10 : long-list, exclusions, short-list, validation.',
    'Investigations de terrain sur la short-list (topographie, géotechnique de reconnaissance, hydrologie, foncier).',
    'Investigations complètes sur le site retenu (Annexe C).',
  ], 'Carte SIG ; analyse multicritère ; note de sélection ; dossier foncier ; plan de sécurisation.', 'Vérification foncière auprès des services compétents ; validation du site par le Comité de Suivi (jalon G2).'],
  ['V4 — Technologie Biodrum et alternatives', 'Vérifier que la technologie est adaptée aux déchets caractérisés et capable d’atteindre les performances annoncées.', [
    'Décrire la chaîne Biodrum complète et le principe de conversion (à documenter par le fournisseur : nature du procédé, étapes, conditions de fonctionnement).',
    'Établir la liste des références commerciales : capacité, type de déchet, date de mise en service, heures de fonctionnement, disponibilité mesurée, contact de l’exploitant.',
    'Visiter au moins deux références en exploitation [Q], dont une traitant des déchets de composition proche.',
    'Réaliser des essais de traitement sur échantillons représentatifs de Kinshasa (saison sèche et saison des pluies).',
    'Comparer avec au moins trois alternatives : incinération à grille, production de CSR, digestion anaérobie et compostage, et une option sans valorisation énergétique (tri et compostage avec enfouissement contrôlé).',
    'Examiner les garanties constructeur, la disponibilité des pièces, les besoins de formation et les conditions de la propriété intellectuelle (article 12).',
  ], 'Rapport technologique ; matrice de maturité technologique (TRL) ; bilans masse-énergie ; comparaison des options.', 'Ingénieur procédés indépendant du fournisseur ; données d’exploitation certifiées par les exploitants de référence.'],
  ['V5 — Dimensionnement et production électrique', 'Déterminer la puissance nette soutenable et comparer les scénarios.', [
    'Calculer la production nette à partir du flux résiduel garanti, du PCI mesuré, du rendement, de la disponibilité, de l’autoconsommation et de la saisonnalité.',
    'Appliquer la méthode des scénarios de puissance du chapitre 11.',
    'Établir les bilans mensuels et annuels, P50/P90 si les données le justifient.',
  ], 'Note de dimensionnement ; enveloppes de conception ; seuils de viabilité.', 'Ingénieur indépendant.'],
  ['V6 — Ingénierie des infrastructures', 'Définir les ouvrages au niveau avant-projet sommaire (APS).', [
    'Schémas de procédé (PFD), principes de P&ID, liste des équipements principaux.',
    'Plan masse, voiries, stockage, fosse de réception, gestion des eaux pluviales et des effluents, sécurité incendie.',
    'Utilités : eau de process et de refroidissement, électricité de chantier, carburants.',
    'Estimation CAPEX par lot (classe de précision à déclarer, par exemple selon la classification AACE) et OPEX ; calendrier EPC ; stratégie O&M.',
  ], 'Dossier APS ; nomenclatures ; estimation des coûts ; matrice des interfaces.', 'Revue d’ingénierie indépendante.'],
  ['V7 — Raccordement électrique', 'Démontrer la faisabilité de l’évacuation de l’énergie.', [
    'Demande formelle de données au gestionnaire de réseau concerné (SNEL ou autre entité compétente, à confirmer en V1).',
    'Étude d’au moins deux points de raccordement [Q] : tension, longueur, capacité d’accueil, contraintes.',
    'Études de répartition de charge, de court-circuit et de stabilité selon les données fournies ; examen du mode îloté.',
    'Estimation du coût, du délai et du porteur du raccordement.',
  ], 'Dossier de raccordement ; schéma unifilaire ; coûts et calendrier.', 'Avis technique écrit du gestionnaire de réseau.'],
  ['V8 — Étude de marché actualisée et revenus', 'Satisfaire l’exigence de l’article 3.1 et fonder les revenus.', [
    'Actualiser l’étude de marché antérieure de VIPRO S.A : collecte, tri, recyclage, valorisation énergétique, demande d’électricité.',
    'Revenus : redevances de traitement, électricité, matières recyclées, compost, crédits carbone (en scénario séparé).',
    'Éviter le double comptage entre matières recyclées et combustible.',
    'Analyser la solvabilité des contreparties et la source de paiement des redevances.',
  ], 'Étude de marché actualisée ; projections prix et volumes ; stratégie commerciale.', 'Triangulation d’au moins trois sources par prix clé lorsque c’est possible.'],
  ['V9 — Coûts, modèle financier et bancabilité', 'Évaluer la rentabilité et la finançabilité de la SPV.', [
    'CAPEX et OPEX ascendants, renouvellements, fonds de roulement, fiscalité, inflation, change.',
    'Modèle financier conforme au chapitre 12.',
    'Plan de financement, tests de ratios et de liquidité, tarifs d’équilibre.',
  ], 'Modèle financier tableur et code de recalcul ; rapport financier ; analyse de bancabilité.', 'Audit du modèle par un auditeur indépendant.'],
  ['V10 — Analyse économique coûts-avantages', 'Mesurer la valeur du projet pour la collectivité.', [
    'Contrefactuel réaliste sans projet.',
    'Avantages : salubrité, santé, drainage et inondations, émissions évitées, matériaux, énergie ; coûts économiques complets.',
    'Prix de référence, taux d’actualisation social justifié, analyse distributive et impacts budgétaires.',
  ], 'VAN économique, TRE, ratio avantages-coûts, analyse distributive.', 'Revue par un économiste indépendant.'],
  ['V11 — Environnement, social, climat, santé et sécurité', 'Produire l’EIES et ses instruments selon la procédure de l’ACE.', [
    'Faire approuver les TdR de l’EIES par l’ACE (article 8) avant les campagnes d’état initial.',
    'État initial sur deux saisons (Annexe C), modélisation de la dispersion atmosphérique, du bruit et des odeurs.',
    'Analyse sociale : recensement des personnes affectées, secteur informel, genre, groupes vulnérables.',
    'Plan de mobilisation des parties prenantes, mécanisme de gestion des plaintes, PGES ; plan de réinstallation si requis.',
    'Conformité au droit congolais et aux normes de performance de la SFI, habituellement exigées par les prêteurs (Annexe D du Protocole).',
  ], 'EIES, PGES, PAR le cas échéant, plan de mobilisation des parties prenantes.', 'Approbation de l’ACE ; revue environnementale et sociale indépendante.'],
  ['V12 — Structuration BOT/PPA/WSA, risques et mise en œuvre', 'Préparer la Phase 3 du Protocole.', [
    'Tester le montage et l’allocation des risques sur la base des Annexes C et D du Protocole.',
    'Proposer des term sheets indicatifs (concession, PPA, WSA) et une stratégie graduée de garanties (Annexe C.3).',
    'Plan de mise en œuvre : EPC, O&M, contenu local, formation, chemin critique, transfert en fin de concession.',
  ], 'Matrice des risques ; term sheets indicatifs ; plan de mise en œuvre et de passation des marchés.', 'Revue par les conseils juridiques des deux Parties.'],
];
volets.forEach(([title, obj, tasks, deliv, valid]) => {
  add(H2(title), P(`**Objectif** : ${obj}`), P('**Tâches minimales** :'));
  tasks.forEach(t => add(B(t)));
  add(P(`**Livrables** : ${deliv}`), P(`**Validation indépendante [V]** : ${valid}`));
});

// 9 Echantillonnage
add(
  H1('9. Protocole de caractérisation des déchets (plan d’échantillonnage)'),
  P('Le plan ci-dessous fixe des **minimums [Q]**. Le Consultant le complète, recalcule les effectifs après une campagne pilote et le fait valider par le Comité de Suivi avant les campagnes principales (jalon G1).'),
  H2('9.1 Méthode de référence'),
  B('Tri et composition : méthode inspirée de la norme ASTM D5231 (composition des déchets municipaux non traités) ou méthode équivalente justifiée.'),
  B('Analyses de combustible : normes ISO/EN applicables aux combustibles solides de récupération, à préciser par le laboratoire.'),
  B('Laboratoire accrédité ISO/IEC 17025 pour les paramètres concernés ; chaîne de garde documentée pour chaque échantillon.'),
  H2('9.2 Stratification'),
  ...T(['Strate', 'Description', 'Unité d’échantillonnage'], [
    ['S1', 'Ménages — quartiers à revenu élevé', 'Ménage'],
    ['S2', 'Ménages — quartiers à revenu intermédiaire', 'Ménage'],
    ['S3', 'Ménages — quartiers populaires', 'Ménage'],
    ['S4', 'Marchés', 'Marché / benne'],
    ['S5', 'Commerces, bureaux, institutions, hôtellerie', 'Établissement'],
    ['S6', 'Flux collectés existants (points de transfert, dépôts, décharge)', 'Camion entrant'],
    ['S7', 'Zone de Kia Mona et Maluku (gisement local actuel et futur)', 'Ménage / établissement'],
  ], [900, 6000, 2700]),
  P('Les communes échantillonnées (au moins six [Q], plus Maluku) sont choisies selon des critères explicites : population, niveau de revenu, distance au site et existence de collecte.'),
  H2('9.3 Quantités minimales par campagne saisonnière'),
  ...T(['Mesure', 'Minimum par saison [Q]', 'Total (2 saisons)'], [
    ['Panel de pesée des ménages (S1, S2, S3, S7)', '50 ménages par strate, 8 jours consécutifs (le 1er jour n’est pas exploité)', '400 ménages-campagnes'],
    ['Pesée des producteurs non ménagers (S4, S5)', '15 producteurs par strate, 7 jours', '60 producteurs-campagnes'],
    ['Comptage et pesée des camions entrants (S6)', '14 jours consécutifs sur chaque site d’apport principal', '28 jours par site'],
    ['Tris de composition (≥ 100 kg par échantillon)', '10 échantillons par strate (7 strates)', '140 échantillons'],
    ['Échantillons composites pour laboratoire', '3 par strate', '42 + 10 % de doublons'],
    ['Essais de traitement sur échantillons représentatifs (V4)', '1 essai par saison sur un mélange représentatif de la fraction résiduelle', '2 essais'],
  ], [3400, 4100, 2100]),
  P('Effectif statistique : pour chaque fraction principale, n = (t × s / (e × x̄))², avec t la valeur de Student au niveau de confiance retenu, s l’écart-type, x̄ la moyenne et e la précision relative visée. **Objectif [TdR]** : précision de ±10 % à 90 % de confiance sur les fractions déterminantes (organique, plastiques, fines, inertes) et sur le PCI.'),
  H2('9.4 Paramètres à analyser'),
  B('Composition : organiques, papier-carton, plastiques (films, rigides), textiles, bois, verre, métaux, inertes, fines (< 10 mm ou maille à justifier), déchets dangereux ménagers.'),
  B('Physico-chimie : masse volumique, humidité totale, cendres, matières volatiles, carbone fixe, PCS et PCI (sur brut et sur sec), C, H, N, S, O, chlore, fluor.'),
  B('Métaux et contaminants : Hg, Cd, Pb, As, Cr, Ni, Cu, Zn et tout autre paramètre exigé par le fournisseur de technologie ou par l’EIES.'),
  H2('9.5 Saisons et contrôle qualité'),
  B('Au moins une campagne en saison sèche et une en saison des pluies, dates justifiées par les données climatiques ; une campagne pilote de quelques jours précède la première campagne.'),
  B('Étalonnage quotidien des balances, doublons de tri et de laboratoire (≥ 10 %), échantillons de contrôle, photographies datées et géolocalisées.'),
  B('Aucune campagne n’est réputée complète si la représentativité n’est pas démontrée statistiquement.'),
);

// 10 Site
add(
  H1('10. Procédure d’identification et de validation du site'),
  P('Le site n’étant pas attribué, sa validation est une **condition préalable à l’ingénierie détaillée** : aucun travail d’ingénierie au niveau APS ne commence avant le jalon G2, hormis les études génériques indépendantes du site.'),
  ...T(['Étape', 'Contenu', 'Résultat'], [
    ['1. Long-list (mode D)', 'Identification SIG d’au moins 8 sites candidats [Q] sur la base du plan directeur de Kia Mona, du cadastre disponible et des contraintes', 'Liste et fiches sommaires'],
    ['2. Exclusions', 'Zones inondables (crue de référence à définir), zones protégées, habitat dense, servitudes, pentes excessives, conflits fonciers connus, distance excessive au réseau', 'Sites éliminés et motifs'],
    ['3. Short-list (modes D et T)', 'Visites et reconnaissance sur au moins 3 sites [Q] ; analyse multicritère pondérée', 'Classement et analyse de sensibilité des pondérations'],
    ['4. Validation (modes T et V)', 'Investigations complètes du site préférentiel ; reconnaissance du site de repli ; vérification foncière ; consultation des riverains', 'Note de sélection validée au jalon G2'],
  ], [2200, 5000, 2400]),
  H2('10.1 Critères de l’analyse multicritère (pondérations indicatives à valider)'),
  ...T(['Critère', 'Pondération indicative [TdR]'], [
    ['Disponibilité et sécurité foncière', '20 %'],
    ['Distance et coût de transport depuis le gisement', '15 %'],
    ['Accès routier et logistique', '10 %'],
    ['Distance et capacité du point de raccordement électrique', '15 %'],
    ['Conditions géotechniques et hydrologiques', '10 %'],
    ['Sensibilité environnementale et sociale (riverains, réinstallation)', '15 %'],
    ['Accès à l’eau et exutoires des effluents et résidus', '5 %'],
    ['Compatibilité urbanistique et potentiel d’extension (32 MW et plus)', '10 %'],
  ], [7000, 2600], {}),
);

// 11 Puissance
add(
  H1('11. Scénarios de puissance et exigences de modélisation technique'),
  H2('11.1 Ordre de grandeur illustratif'),
  P('Pour situer l’enjeu du gisement, le débit de fraction résiduelle entrant au procédé, en fonctionnement, se déduit de : débit (t/j) = P (MW) ÷ [η × PCI (MJ/kg)] × 86,4, où η est le rendement électrique net. Le tableau ci-dessous applique cette formule à des valeurs **hypothétiques** de PCI et de rendement, qui devront être remplacées par les mesures (V2, V4).'),
  ...T(['Puissance nette', 'PCI 5 MJ/kg, η 20 %', 'PCI 7 MJ/kg, η 20 %', 'PCI 9 MJ/kg, η 20 %', 'PCI 7 MJ/kg, η 15 %', 'PCI 7 MJ/kg, η 25 %'], [
    ['16 MW', '≈ 1 380 t/j', '≈ 990 t/j', '≈ 770 t/j', '≈ 1 320 t/j', '≈ 790 t/j'],
    ['32 MW', '≈ 2 760 t/j', '≈ 1 980 t/j', '≈ 1 540 t/j', '≈ 2 630 t/j', '≈ 1 580 t/j'],
    ['48 MW (exemple > 32 MW)', '≈ 4 150 t/j', '≈ 2 960 t/j', '≈ 2 300 t/j', '≈ 3 950 t/j', '≈ 2 370 t/j'],
  ], [2000, 1520, 1520, 1520, 1520, 1520]),
  Note('Lecture : ces débits portent sur la seule fraction résiduelle après tri et recyclage, pendant les heures de fonctionnement. Le gisement brut à collecter est donc supérieur. Ces valeurs ne constituent ni une hypothèse de conception ni une donnée sur la technologie Biodrum.'),
  H2('11.2 Définition des scénarios'),
  ...T(['Scénario', 'Définition', 'Conditions d’examen'], [
    ['S0 — Sans valorisation énergétique', 'Tri, recyclage, compostage et enfouissement contrôlé des refus', 'Contrefactuel technique et économique obligatoire'],
    ['S16 — 16 MW', 'Unité du Jalon 1 [P]', 'Cas de base contractuel'],
    ['S32 — 32 MW', 'Deux unités, en une phase ou en deux phases', 'Phasage et déclencheurs de la 2e unité à définir'],
    ['SOPT — Capacité optimisée', 'Capacité maximisant la VAN économique et la VAN projet sous contraintes', 'Contraintes : gisement résiduel P90 contractualisable, capacité d’accueil du réseau, emprise du site, DSCR minimal, acceptabilité environnementale et sociale ; si la capacité optimale est inférieure à 16 MW, le signaler explicitement'],
  ], [2300, 3300, 4000]),
  H2('11.3 Exigences de modélisation technique'),
  B('Bilan matière et bilan énergétique mensuels, bouclés à ±2 % [TdR], du gisement brut jusqu’aux résidus ultimes.'),
  B('Paramètres explicites : PCI par saison, rendement brut et net, autoconsommation, disponibilité (heures par an), arrêts programmés, dégradation, capacité de stockage tampon.'),
  B('Simulation de la variabilité saisonnière et d’interruptions d’approvisionnement ; P50 et P90 lorsque les données le permettent.'),
  B('Modélisation de la dispersion atmosphérique et de l’impact sonore pour les scénarios retenus.'),
  B('Code documenté et testé dans le dépôt ; résultats reproduits par l’ingénieur indépendant sur un échantillon de cas.'),
);

// 12 Finance
add(
  H1('12. Exigences de modélisation financière et économique'),
  H2('12.1 Structure du modèle financier'),
  B('Feuilles séparées : hypothèses (une seule source par entrée, avec niveau A/B/C), calculs, construction, exploitation, financement, fiscalité, états financiers, ratios, sensibilités, contrôles.'),
  B('Pas de formules masquées, de macros indispensables ni de valeurs saisies dans les calculs ; contrôles d’équilibre (bilan, trésorerie, sources et emplois) visibles.'),
  B('Pas de temps : trimestriel en construction et semestriel ou annuel en exploitation ; monnaie de référence EUR ; CDF traité pour les coûts locaux et le risque de change.'),
  B('Deux hypothèses de durée testées : 25 ans depuis le bouclage financier (construction incluse) et 25 ans d’exploitation depuis la COD (voir chapitre 2).'),
  B('Modèle de recalcul indépendant en code (Claude Code) reproduisant les flux de trésorerie et les ratios avec une tolérance définie.'),
  H2('12.2 Indicateurs obligatoires'),
  B('VAN et TRI du projet et des fonds propres ; délai de récupération.'),
  B('DSCR annuel, moyen et minimal ; LLCR ; PLCR ; besoins de comptes de réserve.'),
  B('Tarif d’équilibre de l’électricité et redevance d’équilibre à la tonne pour un TRI fonds propres cible et un DSCR cible.'),
  B('Coût actualisé de l’électricité (LCOE) et coût net de traitement par tonne.'),
  H2('12.3 Sensibilités obligatoires'),
  ...T(['Famille', 'Variations minimales [TdR]'], [
    ['Gisement', 'Volumes mobilisables −20 % et −40 % ; saisonnalité ; PCI ±20 %'],
    ['Technique', 'Rendement net, disponibilité, autoconsommation ; retard de mise en service de 6 et 12 mois'],
    ['Coûts', 'CAPEX +20 % et +40 % ; OPEX +20 % et +40 % ; coût de collecte et de transport'],
    ['Revenus', 'Tarif PPA et redevance ±20 % ; impayés et retards de paiement de 90 et 180 jours ; arrêt de l’indexation'],
    ['Réseau', 'Coût et délai du raccordement ; écrêtement (curtailment)'],
    ['Financier', 'Taux d’intérêt +200 points de base ; maturité de la dette ; ratio dette/fonds propres ; change EUR/CDF'],
    ['Carbone', 'Cas de base sans revenus carbone ; revenus carbone en scénario séparé uniquement'],
    ['Combinés', 'Au moins deux scénarios défavorables combinés ; seuils de rupture (DSCR = 1,0) par variable'],
  ], [2000, 7600]),
  H2('12.4 Analyse économique'),
  B('Conversion des prix financiers en prix économiques (taxes, transferts, prix de référence) ; taux d’actualisation social justifié par une source citée.'),
  B('Pas de double comptage entre avantages sanitaires, avantages liés au drainage et coûts évités de collecte.'),
);

// 13 Bancabilité
add(
  H1('13. Critères de bancabilité'),
  P('L’étude évalue chaque critère comme **satisfait / satisfait sous conditions / non satisfait**, avec les preuves correspondantes. Les seuils chiffrés sont confirmés auprès d’au moins deux prêteurs ou IFD potentiels [TdR] ; à défaut, les résultats sont présentés pour plusieurs seuils (par exemple DSCR minimal de 1,20, 1,30 et 1,40).'),
  ...T(['N°', 'Critère', 'Preuve attendue'], [
    ['B1', 'Gisement résiduel P90 couvrant le besoin nominal avec une marge sur la durée du contrat', 'Rapport V2 ; WSA indicatif avec engagement de volume et contrepartie identifiée'],
    ['B2', 'Technologie éprouvée à l’échelle commerciale sur des déchets comparables', 'Références auditées ; rapport de l’ingénieur indépendant'],
    ['B3', 'Contrat EPC clé en main à prix forfaitaire, garanties de performance et pénalités', 'Offre ou lettre d’engagement d’un contractant qualifié'],
    ['B4', 'Opérateur O&M expérimenté', 'Références et proposition d’O&M'],
    ['B5', 'PPA avec production réputée en cas d’indisponibilité du réseau et acheteur solvable ou garanti', 'Analyse de solvabilité ; instruments de l’Annexe C.3'],
    ['B6', 'Sécurité de paiement des redevances de traitement', 'Source de paiement identifiée ; compte séquestre ou équivalent'],
    ['B7', 'Droits fonciers sécurisés pour la durée de la concession', 'Titre ou engagement foncier ; absence de litige'],
    ['B8', 'EIES approuvée et conformité aux normes des prêteurs', 'Certificat ou avis de l’ACE ; revue E&S indépendante'],
    ['B9', 'Raccordement faisable, financé et planifié', 'Avis du gestionnaire de réseau'],
    ['B10', 'Ratios financiers robustes en cas défavorable', 'Modèle audité ; sensibilités du chapitre 12'],
    ['B11', 'Risques de change, de convertibilité et de transfert traités', 'Mécanisme contractuel ; assurance risque politique'],
    ['B12', 'Stabilisation juridique, droits de substitution des prêteurs, accord direct, arbitrage', 'Term sheets V12'],
    ['B13', 'Capacité du promoteur à apporter les fonds propres et références des partenaires', 'Preuves de capacité financière et d’expérience de VIPRO S.A et de ses partenaires'],
  ], [700, 4900, 4000]),
);

// 14 Calendrier
add(
  H1('14. Phasage, calendrier et jalons de décision'),
  P('Pour éviter toute confusion avec les Phases 1 à 4 de l’article 6 du Protocole, les étapes de l’étude sont numérotées E0 à E5. Le mois 1 de l’étude est supposé correspondre au mois M2 du calendrier du Protocole (après la mise en place du Comité de Suivi) ; ce calage est à confirmer.'),
  ...T(['Étape', 'Mois de l’étude', 'Mois du Protocole (indicatif)', 'Contenu principal', 'Jalon de décision'], [
    ['E0 Mobilisation', 'S1–S2', 'M2', 'Plans qualité, données, terrain, HSE ; approbation des outils d’IA ; demandes de données', 'G0 : rapport de démarrage accepté'],
    ['E1 Diagnostic et préfaisabilité', 'M1–M3', 'M2–M4', 'Revue documentaire, long-list des sites, campagne pilote, TdR de l’EIES soumis à l’ACE', 'G1 : plan d’échantillonnage et short-list validés ; GO terrain'],
    ['E2 Investigations de terrain', 'M2–M7', 'M3–M8', 'Campagnes saisonnières, sondages, levés, état initial, essais', 'G2 (M5) : site préférentiel validé — préalable à l’ingénierie'],
    ['E3 Faisabilité détaillée', 'M5–M10', 'M6–M11', 'Technologie, dimensionnement, APS, raccordement, marché, finance, économie, EIES', 'G3 (M7) : technologie et capacité retenues ; G4 (M10) : faisabilité et bancabilité'],
    ['E4 Structuration', 'M9–M12', 'M10–M13', 'Matrice des risques, term sheets, plan de mise en œuvre, data room', '—'],
    ['E5 Audit et clôture', 'M12–M13', 'M13–M14', 'Audit indépendant, corrections, rapport final', 'G5 : recommandation GO / GO conditionnel / NO-GO'],
  ], [1700, 1200, 1400, 3200, 2100]),
  Note('La seconde campagne saisonnière peut repousser la clôture si la première campagne ne tombe pas dans la saison attendue. L’approbation de l’EIES dépend des délais de l’ACE et n’est pas maîtrisée par le Consultant. La tranche conditionnelle APD (après G4) correspond à la fenêtre M12–M15 du Protocole.'),
);

// 15 Livrables
add(
  H1('15. Livrables contractuels'),
  ...T(['Code', 'Livrable', 'Échéance', 'Critères d’acceptation minimaux'], [
    ['L0', 'Rapport de démarrage : méthodologie, plans qualité, données, terrain, HSE, IA', 'S2', 'Matrice D/T/V complète ; outils d’IA approuvés'],
    ['L1', 'Diagnostic documentaire, analyse des lacunes, préfaisabilité, long-list des sites', 'M2', 'Registre des variables initialisé'],
    ['L2', 'Rapport sur le gisement, la caractérisation, le laboratoire et la logistique', 'M5 (saison 1) ; M7 (consolidé)', 'Représentativité démontrée ; rapports de laboratoire originaux'],
    ['L3', 'Étude comparative des sites et note de sélection', 'M5', 'Validation au jalon G2'],
    ['L4', 'Rapport technologique, essais et bilans masse-énergie', 'M7', 'Avis de l’ingénieur indépendant'],
    ['L5', 'Faisabilité technique et avant-projet sommaire, dont le raccordement', 'M9', 'Avis du gestionnaire de réseau ; revue d’ingénierie'],
    ['L6', 'Étude de marché actualisée, analyse économique, modèle financier', 'M10', 'Modèle recalculé ; audit engagé'],
    ['L7', 'EIES, PGES et instruments connexes', 'Selon procédure ACE', 'Conformité aux TdR approuvés par l’ACE'],
    ['L8', 'Rapport de structuration BOT/PPA/WSA et matrice des risques', 'M11', 'Revue des conseils des Parties'],
    ['L9', 'Dossier consolidé, registre des risques, data room', 'M12', 'Index complet et traçable'],
    ['L10', 'Rapport d’audit indépendant et version finale corrigée', 'M13', 'Réponses traçables à toutes les observations'],
  ], [700, 4200, 1800, 2900]),
  P('Chaque livrable est remis en français (articles 22 et 25 du Protocole), en version éditable et PDF, avec un résumé exécutif, les données et le code correspondants, ainsi qu’un tableau des réserves et des hypothèses de niveau C.'),
);

// 16 Équipe
const team = [
  ['H1', 'Responsable de l’étude (ingénieur déchets-énergie)', 'Répond des livrables ; arbitre les désaccords entre modèles ; 15 ans d’expérience', 6],
  ['H2', 'Expert déchets, signataire du plan d’échantillonnage', 'Supervise les campagnes de terrain ; 10 ans', 3],
  ['H3', 'Ingénieur procédés WtE, indépendant du fournisseur', 'Signe l’analyse technologique ; 12 ans', 3],
  ['H4', 'Ingénieur électricien, réseaux', 'Interface avec le gestionnaire de réseau ; 10 ans', 1.5],
  ['H5', 'Géotechnicien signataire', 'Signe le rapport géotechnique ; 10 ans', 1],
  ['H6', 'Expert financement de projets', 'Revue du modèle et contacts prêteurs ; 12 ans', 2],
  ['H7', 'Spécialiste environnement (statut requis par l’ACE)', 'Signe l’EIES si la procédure l’exige ; 10 ans', 3],
  ['H8', 'Spécialiste social et réinstallation', 'Supervise le recensement et les consultations ; 10 ans', 3],
  ['H9', 'Juriste PPP, énergie et déchets (droit congolais)', 'Avis juridique ; inscrit au barreau en RDC', 2],
  ['H10', 'Coordinateur terrain, qualité et HSE (Kinshasa)', 'Logistique, sécurité, chaîne de garde ; 8 ans', 6],
];
const tot = team.reduce((a, r) => a + r[3], 0);
add(
  H1('16. Dispositif de réalisation : agents IA, responsables humains et prestataires'),
  H2('16.1 Réseau d’agents IA'),
  P('Le réseau d’agents décrit au chapitre 6 réalise les travaux de mode D. Son coût correspond aux abonnements, à la consommation des services d’IA et à l’infrastructure de calcul et de stockage (Annexe D, poste 1).'),
  H2('16.2 Responsables humains (hommes-mois indicatifs)'),
  P('Les hommes-mois ci-dessous sont une **estimation de travail [Q]**. Ils couvrent la supervision, les signatures, les interfaces avec les autorités et l’arbitrage, et non la production courante, confiée aux agents. Ils sont recalculés après validation du plan d’échantillonnage, du nombre de sites et des exigences de l’ACE.'),
  ...T(['Code', 'Poste', 'Rôle et expérience minimale [TdR]', 'H-m [Q]'],
    [...team.map(r => [r[0], r[1], r[2], String(r[3]).replace('.', ',')]), ['', 'Total responsables humains', '', String(tot).replace('.', ',')]],
    [700, 3600, 4300, 1000], { totalLast: true }),
  H2('16.3 Prestataires de terrain sous-traités'),
  B('Équipes de pesée et de tri, enquêteurs (chiffrés en hommes-jours).'),
  B('Laboratoire accrédité ISO/IEC 17025.'),
  B('Entreprise de sondages géotechniques et topographe.'),
  B('Bureau de mesures environnementales (air, bruit, eau, sols) et inventaires de biodiversité.'),
  P('Les prestataires remettent leurs données brutes dans les formats définis par l’agent données (gabarits de l’Annexe B) ; les agents ne modifient jamais ces données.'),
  H2('16.4 Valideurs indépendants'),
  P('L’ingénieur indépendant, l’auditeur du modèle financier et les autres valideurs du chapitre 18 font l’objet de contrats distincts, non soumis au dispositif de réalisation, afin de préserver leur indépendance.'),
);

// 17 Gouvernance
add(
  H1('17. Gouvernance, revue et réception'),
  B('Comité de Suivi (article 10) : au moins une réunion par trimestre, avec des revues supplémentaires à chaque jalon G0 à G5.'),
  B('Points focaux désignés par chaque Partie ; secrétariat technique tenu par le Consultant.'),
  B('Registre des observations : chaque commentaire reçoit un numéro, une réponse, une modification tracée et un statut.'),
  P('**Procédure de réception proposée [TdR]** : observations écrites et motivées du CSSPEVK sous 30 jours calendaires (articles 9.1 et 10) ; à défaut, escalade aux instances dirigeantes (8 jours puis 15 jours, article 9.1) avant toute acceptation réputée. L’acceptation réputée vaut uniquement autorisation de poursuivre l’étape suivante. Elle ne vaut ni validation scientifique, ni approbation réglementaire, ni avis de l’ingénieur indépendant, conformément à la réserve de l’article 10 (« sans préjudice des vérifications pouvant être requises par les autorités compétentes »).'),
);

// 18 Validation indépendante
add(
  H1('18. Dispositif de validation indépendante'),
  ...T(['Valideur', 'Objet', 'Moment'], [
    ['Laboratoire accrédité ISO/IEC 17025', 'Analyses des déchets, de l’air, de l’eau et des sols', 'E2'],
    ['Ingénieur indépendant (profil de conseiller technique des prêteurs)', 'Technologie, dimensionnement, APS, coûts', 'G3, G4'],
    ['Auditeur de modèle financier', 'Intégrité arithmétique, logique, conformité aux hypothèses', 'E5'],
    ['Gestionnaire de réseau', 'Faisabilité et conditions du raccordement', 'E3'],
    ['ACE', 'TdR de l’EIES puis EIES et PGES', 'E1, puis selon la procédure'],
    ['Cabinet d’avocats congolais', 'Avis juridique sur les compétences, le foncier et la structuration', 'E1, E4'],
    ['Statisticien', 'Plan d’échantillonnage et représentativité', 'G1, E2'],
  ], [3200, 4400, 2000]),
  P('La revue multi-modèles (agents IA, Gemini, ChatGPT) relève du contrôle qualité interne de niveau N2 et ne figure pas dans ce tableau : elle ne remplace aucun des valideurs ci-dessus.'),
  P('Les valideurs déclarent l’absence de conflit d’intérêts avec VIPRO S.A, le fournisseur de la technologie et le Consultant. Leurs droits d’accès aux études sont accordés par écrit par VIPRO S.A conformément à l’article 12.'),
);

// 19 Confidentialité
add(
  H1('19. Propriété intellectuelle, confidentialité et données'),
  B('Les Études sont la propriété de VIPRO S.A ; le CSSPEVK dispose d’une licence d’utilisation limitée (article 12) [P].'),
  B('Avant G0, VIPRO S.A remet une autorisation écrite précisant l’accès des valideurs, de l’ACE, des prêteurs et des assureurs [TdR].'),
  B('Les données de terrain brutes, les jeux de données SIG et le code sont livrés avec la licence et les conditions d’usage applicables.'),
  B('Protection des données personnelles : consentement éclairé, pseudonymisation, accès restreint et durée de conservation définie.'),
);

// 20 HSE
add(
  H1('20. Hygiène, sécurité, assurances et éthique de terrain'),
  B('Plan HSE soumis à G0 : manipulation des déchets (équipements de protection, vaccinations recommandées par un médecin du travail), sécurité routière, sondages, sécurité des équipes.'),
  B('Assurance responsabilité civile couvrant les prospections et les relevés (article 19.3).'),
  B('Code de conduite des enquêteurs ; prévention des abus et du harcèlement ; respect des engagements anticorruption (articles 3.2 et 26).'),
  B('Aucune promesse d’emploi, d’indemnisation ou de réinstallation n’est faite aux populations pendant l’étude.'),
);

// 21 Risques étude
add(
  H1('21. Risques de l’étude et mesures d’atténuation'),
  ...T(['Risque', 'Effet', 'Mesure'], [
    ['Retard d’attribution du site', 'Blocage de l’ingénierie', 'Travaux génériques en parallèle ; jalon G2 ferme ; site de repli'],
    ['Accès limité aux données de l’opérateur de réseau ou de la REGEDEK', 'Hypothèses de niveau C', 'Demandes formelles via le CSSPEVK (article 7) ; scénarios'],
    ['Accès refusé aux références Biodrum', 'Technologie non démontrée', 'Critère B2 non satisfait ; option alternative évaluée'],
    ['Campagne saisonnière décalée', 'Allongement du calendrier', 'Campagne pilote ; planification sur le calendrier climatique'],
    ['Délais de l’ACE', 'Report de L7', 'TdR de l’EIES soumis dès E1'],
    ['Conflit d’intérêts perçu (étude financée par le promoteur)', 'Faible crédibilité auprès des prêteurs', 'Valideurs indépendants sous contrats distincts ; accès complet des valideurs aux hypothèses'],
    ['Erreurs ou sources inventées par un agent IA', 'Données fausses dans les livrables', 'Règles du chapitre 6 ; vérification sur source primaire ; revue N2 ; journal d’IA'],
    ['Erreurs partagées par plusieurs modèles', 'Fausse assurance donnée par la revue croisée', 'Niveau N3 humain ; priorité aux mesures de terrain'],
    ['Refus d’une EIES ou d’un rapport produit par IA', 'Report de L7 ou rejet par les prêteurs', 'Vérifier les exigences de l’ACE à E0 ; signataires humains (H5, H7)'],
    ['Fuite d’informations vers les services d’IA', 'Manquement au NCNDA', 'Outils approuvés par écrit ; pseudonymisation ; informations protégées exclues'],
  ], [3000, 2600, 4000]),
);

// 22 Décision
add(
  H1('22. Critères de décision'),
  ...T(['Décision', 'Conditions'], [
    ['GO', 'Critères B1 à B13 satisfaits ou satisfaits sous des conditions mineures et datées ; EIES sans impact résiduel majeur non maîtrisé ; VAN économique positive'],
    ['GO conditionnel', 'Lacunes limitées, mesurables et remédiables avant le bouclage financier, avec un plan, un coût et un responsable pour chacune'],
    ['NO-GO', 'Gisement non soutenable ou non contractualisable ; technologie non démontrée sans alternative viable ; impacts non maîtrisables ; risque de paiement non finançable ; VAN économique négative dans le cas de base'],
  ], [2000, 7600]),
  P('La recommandation peut porter sur une configuration différente de celle du Protocole (par exemple une capacité inférieure à 16 MW, un phasage différent ou une option sans valorisation énergétique). Toute modification de cette nature exige un accord écrit des Parties (article 24).'),
);

// 23 Questions ouvertes
add(
  H1('23. Questions à résoudre au démarrage'),
  N('Les décisions sur les neuf points du chapitre 2.', 'num2'),
  N('L’identité du maître d’ouvrage de l’étude et du Consultant, et son mode de sélection.', 'num2'),
  N('La mise à disposition du plan directeur géoréférencé de Kia Mona et du périmètre foncier de recherche.', 'num2'),
  N('La communication de l’étude de marché antérieure de VIPRO S.A et de toute étude antérieure du CSSPEVK.', 'num2'),
  N('L’accès aux références industrielles et aux données d’exploitation de la technologie Biodrum, ainsi que l’identité du fournisseur ou du partenaire technologique (article 14).', 'num2'),
  N('La personne morale habilitée à signer et à honorer le PPA et le WSA, et la source de ses paiements.', 'num2'),
  N('La procédure de l’ACE applicable (catégorie du projet, séquence IEE/EIES, consultations).', 'num2'),
  N('Le budget de l’étude, à établir après chiffrage du bordereau des prix (Annexe D).', 'num2'),
  BR(),
);

// Annexes
add(
  H1('Annexe A — Matrice D/T/V par livrable'),
  ...T(['Livrable', 'Part principalement à distance (D)', 'Terrain (T)', 'Validation (V)'], [
    ['L0', 'Oui', 'Visite de démarrage', 'Comité de Suivi'],
    ['L1', 'Oui', 'Entretiens institutionnels', 'Comité de Suivi'],
    ['L2', 'Analyse et modélisation', 'Oui, déterminant', 'Laboratoire, statisticien'],
    ['L3', 'SIG, analyse multicritère', 'Oui, déterminant', 'Comité de Suivi, services fonciers'],
    ['L4', 'Comparaisons, bilans', 'Visites de références, essais', 'Ingénieur indépendant'],
    ['L5', 'Conception, estimations', 'Relevés complémentaires', 'Ingénieur indépendant, gestionnaire de réseau'],
    ['L6', 'Modèles', 'Devis et prix locaux, enquêtes', 'Auditeur de modèle'],
    ['L7', 'Rédaction, modélisation', 'Oui, déterminant', 'ACE'],
    ['L8', 'Oui', 'Consultations prêteurs et autorités', 'Conseils des Parties'],
    ['L9', 'Oui', '—', 'Comité de Suivi'],
    ['L10', 'Oui', '—', 'Auditeur indépendant'],
  ], [1000, 3000, 2800, 2800]),

  H1('Annexe B — Fiche de terrain type pour les tris de composition'),
  ...T(['Champ', 'Contenu'], [
    ['Identifiant', 'Code unique : saison-strate-commune-date-numéro'],
    ['Localisation', 'Coordonnées GPS (WGS84), adresse, photographie datée'],
    ['Origine', 'Strate, type de producteur, mode de collecte'],
    ['Masse', 'Masse brute, tare, masse nette ; numéro et date d’étalonnage de la balance'],
    ['Fractions', 'Masse par fraction (liste du § 9.4), refus, fines'],
    ['Conditions', 'Météo du jour et de la veille (pluie), heure, durée de stockage avant tri'],
    ['Prélèvement laboratoire', 'Numéro d’échantillon, masse, conditionnement, signature de la chaîne de garde'],
    ['Contrôle', 'Nom du trieur, nom du superviseur, doublon (oui ou non)'],
  ], [2600, 7000]),

  H1('Annexe C — Quantités minimales indicatives des investigations de terrain'),
  P('Les quantités ci-dessous sont des **minimums [Q]** à confirmer par le géotechnicien, l’hydrologue et le spécialiste environnement en fonction de l’implantation des ouvrages et des premiers résultats (approche progressive de l’Eurocode 7 ou d’un référentiel équivalent).'),
  ...T(['Investigation', 'Sites de la short-list (chacun)', 'Site préférentiel'], [
    ['Levé topographique', 'Levé de reconnaissance, MNT à partir de données disponibles', 'Levé à l’échelle 1/500 de l’emprise et de ses abords ; corridors de raccordement et d’accès à l’échelle 1/2 000 (bande de 100 m)'],
    ['Sondages', '3 sondages de reconnaissance d’au moins 15 m', 'Au moins 1 sondage carotté par ouvrage lourd (chaudière ou four, turbine, cheminée, fosse), d’au moins 25 m ou jusqu’au substratum'],
    ['Essais in situ', '3 essais pénétrométriques', 'Essais CPT ou SPT selon un maillage de 30 à 50 m sur les zones bâties'],
    ['Fosses de reconnaissance', '4', '10'],
    ['Piézomètres', '1', '3 au moins, suivis sur deux saisons'],
    ['Essais de laboratoire sur sols', 'Identification', 'Granulométrie, limites d’Atterberg, compressibilité, cisaillement, agressivité chimique'],
    ['Géophysique (résistivité)', '—', '2 profils au moins (mise à la terre, hétérogénéités)'],
    ['Hydrologie', 'Repérage des zones inondables', 'Étude de crue et de drainage ; niveau de la plateforme'],
    ['Qualité de l’air', '—', '4 stations au moins, 2 campagnes saisonnières (PM10, PM2,5, NO2, SO2, CO et autres paramètres de l’EIES)'],
    ['Bruit', '—', '6 points au moins, de jour et de nuit'],
    ['Eaux de surface et souterraines', '—', '4 points de surface et les piézomètres, 2 campagnes'],
    ['Sols (pollution)', '—', 'Échantillons composites sur l’emprise'],
    ['Biodiversité', 'Reconnaissance', 'Inventaires sur 2 saisons'],
    ['Social', 'Entretiens avec les autorités locales et coutumières', 'Recensement exhaustif des personnes affectées par l’emprise et les corridors ; enquête socio-économique par échantillon'],
  ], [2200, 3000, 4400]),

  H1('Annexe D — Bordereau des prix (cadre à compléter par le Consultant)'),
  P('Les prix unitaires et totaux sont laissés vides : ils relèvent de l’offre financière. Les quantités renvoient aux minimums des chapitres 9 et 16 et de l’Annexe C.'),
  ...T(['N°', 'Désignation', 'Unité', 'Qté indicative', 'PU (EUR)', 'Total (EUR)'], [
    ['1', 'Services d’IA (abonnements, consommation Claude, Gemini, ChatGPT) et infrastructure de calcul et de stockage', 'forfait', '1', '', ''],
    ['1 bis', 'Honoraires des responsables humains H1 à H10', 'h-m', String(tot).replace('.', ','), '', ''],
    ['2', 'Personnel d’appui terrain (enquêteurs, trieurs)', 'h-j', 'À chiffrer', '', ''],
    ['3', 'Panels de pesée des ménages', 'ménage-campagne', '400', '', ''],
    ['4', 'Pesées des producteurs non ménagers', 'producteur-campagne', '60', '', ''],
    ['5', 'Tris de composition', 'échantillon', '140', '', ''],
    ['6', 'Analyses de laboratoire (lot de paramètres du § 9.4)', 'échantillon', '47', '', ''],
    ['7', 'Essais de traitement de la technologie', 'essai', '2', '', ''],
    ['8', 'Visites de références industrielles', 'visite', '2', '', ''],
    ['9', 'Levés topographiques', 'forfait par site', '3 + 1', '', ''],
    ['10', 'Sondages géotechniques', 'mètre linéaire', 'À chiffrer', '', ''],
    ['11', 'Essais in situ et de laboratoire géotechniques', 'unité', 'À chiffrer', '', ''],
    ['12', 'Piézomètres et suivi', 'unité', '6', '', ''],
    ['13', 'Campagnes d’état initial (air, bruit, eau, sols, biodiversité)', 'campagne', '2', '', ''],
    ['14', 'Recensement et enquêtes socio-économiques', 'forfait', '1', '', ''],
    ['15', 'Consultations publiques', 'réunion', 'À chiffrer', '', ''],
    ['16', 'Logistique, transport et hébergement', 'forfait', '1', '', ''],
    ['17', 'Licences logicielles et infrastructure de données', 'forfait', '1', '', ''],
    ['18', 'Assurances et HSE', 'forfait', '1', '', ''],
    ['19', 'Tranche conditionnelle APD (après G4)', 'forfait', '1', '', ''],
    ['', 'Hors marché du Consultant : ingénieur indépendant, auditeur de modèle (contrats distincts)', 'pour mémoire', '—', '—', '—'],
    ['', 'Total hors taxes', '', '', '', ''],
  ], [600, 4200, 1500, 1300, 1000, 1000], { totalLast: true }),

  H1('Annexe E — Liste initiale des données à demander'),
  B('CSSPEVK : plan directeur géoréférencé de Kia Mona, périmètre foncier, études antérieures, documents institutionnels.'),
  B('Ville-Province et REGEDEK : tonnages collectés, sites de dépôt, contrats de collecte, flotte, coûts.'),
  B('Gestionnaire de réseau : schéma du réseau, postes, charges, projets de renforcement, conditions de raccordement.'),
  B('ACE : procédure, catégorie du projet, modèle de TdR de l’EIES.'),
  B('VIPRO S.A : étude de marché antérieure, données sur la technologie, références, partenaires.'),
  B('Services météorologiques : précipitations et températures pluriannuelles.'),
  B('Institut national de la statistique et autres sources : démographie par commune.'),

  H1('Annexe F — Gabarit du registre des variables'),
  ...T(['ID', 'Libellé', 'Unité', 'Valeur', 'Plage', 'Source', 'Date', 'Niveau', 'Responsable', 'Version'], [
    ['G-001', 'Production de déchets ménagers, strate S2', 'kg/hab/j', '', '', '', '', 'A/B/C', '', ''],
    ['T-010', 'PCI de la fraction résiduelle, saison des pluies', 'MJ/kg brut', '', '', '', '', 'A/B/C', '', ''],
  ], [700, 2000, 900, 700, 700, 1100, 700, 700, 1100, 800]),

  H1('Annexe G — Gabarit du journal d’utilisation de l’IA'),
  ...T(['Date', 'Outil et version', 'Livrable', 'Objet de la demande', 'Sortie retenue', 'Vérification', 'Vérificateur'], [
    ['', 'Agent V2 (Claude Code)', 'L2', '', '', 'Source primaire, test N1', ''],
    ['', 'Gemini / ChatGPT (revue N2)', 'L2', '', '', 'Observation acceptée, rejetée ou transmise au N3', ''],
  ], [900, 1400, 900, 1800, 1700, 1700, 1200]),

  H1('Annexe H — Abréviations'),
  ...T(['Sigle', 'Signification'], [
    ['ACE', 'Agence Congolaise de l’Environnement'], ['APD / APS', 'Avant-projet détaillé / sommaire'],
    ['ARE', 'Autorité de Régulation de l’Électricité'], ['BOT', 'Construction-exploitation-transfert'],
    ['COD', 'Date de mise en service commerciale'], ['CSR', 'Combustible solide de récupération'],
    ['DSCR', 'Ratio de couverture du service de la dette'], ['EIES', 'Étude d’impact environnemental et social'],
    ['IEE', 'Évaluation environnementale initiale'], ['IFD', 'Institution financière de développement'],
    ['LLCR / PLCR', 'Ratio de couverture sur la durée du prêt / du projet'], ['PAR', 'Plan d’action de réinstallation'],
    ['PCI / PCS', 'Pouvoir calorifique inférieur / supérieur'], ['PGES', 'Plan de gestion environnementale et sociale'],
    ['PPA', 'Contrat d’achat d’électricité'], ['SFI', 'Société financière internationale'],
    ['SPV', 'Société de projet'], ['TRE / TRI', 'Taux de rentabilité économique / interne'],
    ['VAN', 'Valeur actuelle nette'], ['WSA', 'Contrat d’approvisionnement en déchets'],
  ], [2000, 7600]),
);

const doc = new Document({
  creator: 'CSSPEVK – VIPRO S.A (projet de TdR)',
  title: 'TdR – Étude de faisabilité détaillée Kia Mona II',
  styles: {
    default: { document: { run: { font: FONT, size: 20 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 28, bold: true, font: FONT, color: ACCENT }, paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0, keepNext: true } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 23, bold: true, font: FONT, color: '2E75B6' }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1, keepNext: true } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 21, bold: true, font: FONT }, paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2, keepNext: true } },
    ],
  },
  numbering: { config: [
    { reference: 'bul', levels: [
      { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 280 } } } },
      { level: 1, format: LevelFormat.BULLET, text: '–', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1000, hanging: 280 } } } } ] },
    { reference: 'num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 320 } } } }] },
    { reference: 'num2', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 320 } } } }] },
  ] },
  features: { updateFields: true },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: 'TdR — Étude de faisabilité détaillée Kia Mona II — Version de travail V1.0', font: FONT, size: 16, color: '808080' })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: 'Confidentiel — Protocole CSSPEVK – VIPRO S.A, art. 12 et 16 — Page ', font: FONT, size: 16, color: '808080' }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16, color: '808080' }),
      new TextRun({ text: ' / ', font: FONT, size: 16, color: '808080' }),
      new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 16, color: '808080' }) ] })] }) },
    children: C,
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(process.argv[2], b); console.log('written', process.argv[2]); });
