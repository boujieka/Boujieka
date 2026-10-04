"""Traductions anglaises de site/template.html.

Chaque clé est un fragment exact du gabarit français ; build.py remplace les clés
les plus longues en premier et échoue si une clé n'est pas trouvée.
Les fragments courts portent leur contexte (balises ou guillemets) pour ne pas
toucher d'autres textes. Les valeurs techniques (data-niveau="critique",
"alerte", "ok") ne sont pas traduites : la feuille de style s'en sert.
"""

EN = {
    # <head>
    '<title>TasetyGrid</title>': '<title>TasetyGrid</title>',
    "TasetyGrid, l'atlas des personnes, des terres et des ressources : savoir ce qui existe sur un territoire, où, dans quel état, et ce qui manque.":
        "TasetyGrid, the atlas of people, land and resources: know what exists across a territory, where it is, what condition it is in, and what is missing.",

    # En-tête
    'aria-label="TasetyGrid, accueil"': 'aria-label="TasetyGrid, home"',
    'aria-label="Navigation principale"': 'aria-label="Main navigation"',
    '>Fiche territoriale</a>': '>Area profile</a>',
    '>Méthode</a>': '>Method</a>',
    '>Confiance</a>': '>Trust</a>',
    '>Pilote</a>': '>Pilot</a>',
    '>Rejoindre le pilote</a>': '>Join the pilot</a>',

    # Hero
    '>Atlas des personnes, des terres et des ressources<': '>Atlas of people, land and resources<',
    'Savoir ce qui existe sur chaque territoire. <em>Et ce qui manque.</em>':
        'Know what exists in every territory. <em>And what is missing.</em>',
    "TasetyGrid réunit sur une seule carte la population, le foncier, les écoles, la santé, les routes,\n          l'énergie, les ressources et le patrimoine de chaque localité. Chaque chiffre affiche sa source et son niveau de vérification.":
        "TasetyGrid brings together, on a single map, the population, land, schools, health services, roads,\n          energy, resources and heritage of every locality. Every figure shows its source and how it was verified.",
    '>Voir une fiche territoriale<': '>See an area profile<',
    '>Rejoindre le pilote Cameroun<': '>Join the Cameroon pilot<',
    '<span>10 régions</span><span>58 départements</span><span>374 collectivités</span><span>Pays bilingue, plateforme bilingue</span>':
        '<span>10 regions</span><span>58 divisions</span><span>374 local councils</span><span>Bilingual country, bilingual platform</span>',
    "Symbole Kodya : une spirale de coquille d'escargot tracée sur une grille, prolongée par un cercle à quatre points":
        "Kodya symbol: a snail-shell spiral drawn on a grid, continued by a circle with four points",
    "KODYA · la coquille qui grandit jusqu'à devenir le cercle": "KODYA · the shell that grows until it becomes the circle",

    # Cinq questions
    '<b>Qui ?</b><span>Ménages et population, en agrégats protégés</span>':
        '<b>Who?</b><span>Households and population, as protected aggregates</span>',
    '<b>Quoi ?</b><span>Bâtiments, équipements, infrastructures, ressources</span>':
        '<b>What?</b><span>Buildings, facilities, infrastructure, resources</span>',
    "<b>À qui ?</b><span>Titres, concessions et permis, quand l'autorité les établit</span>":
        "<b>Whose?</b><span>Titles, concessions and permits, where the authority has issued them</span>",
    '<b>Quel état ?</b><span>Capacité, fonctionnement, date du dernier constat</span>':
        '<b>What condition?</b><span>Capacity, working status, date last checked</span>',
    '<b>Que manque-t-il ?</b><span>Déficits calculés selon les normes officielles</span>':
        '<b>What is missing?</b><span>Gaps calculated against official standards</span>',

    # Démonstration
    '>Démonstration<': '>Demo<',
    '>Une fiche pour chaque localité<': '>A profile for every locality<',
    'Choisissez un exemple. Les chiffres ci-dessous sont fictifs : ils montrent le format, pas une localité réelle.':
        'Pick an example. The figures below are fictional: they show the format, not a real place.',
    'aria-label="Exemples de localités"': 'aria-label="Example localities"',
    '>Village en zone forestière<': '>Forest-zone village<',
    '>Quartier périurbain<': '>Peri-urban neighbourhood<',
    '>Exemple fictif<': '>Fictional example<',
    '<span>● vérifié</span><span>◐ estimé ou partiel</span><span>○ déclaré</span><span>⚠ anomalie à vérifier</span>':
        '<span>● verified</span><span>◐ estimated or partial</span><span>○ reported</span><span>⚠ discrepancy to check</span>',
    '<h3>Ce qui manque</h3>': '<h3>What is missing</h3>',
    '>Score de confiance des données<': '>Data confidence score<',
    "Les besoins sont calculés à partir des normes fixées par chaque ministère, saisies dans la plateforme avec leur texte de référence. Aucune norme n'est inventée.":
        "Needs are calculated from the standards set by each ministry, entered in the platform with their reference text. No standard is made up.",

    # Données d'exemple (script)
    '"Village forestier (exemple)"': '"Forest village (example)"',
    '"Commune rurale · zone forestière · référentiel v2026.1"': '"Rural council · forest zone · reference v2026.1"',
    '"≈ 1 840 hab."': '"≈ 1,840 people"',
    '"intervalle 1 650 à 2 030 · estimation 2026"': '"range 1,650 to 2,030 · 2026 estimate"',
    '["Population",': '["Population",',
    '["Ménages",': '["Households",',
    '"recensement"': '"census"',
    '["Bâtiments",': '["Buildings",',
    '"381 détectés · 374 vérifiés"': '"381 detected · 374 verified"',
    '"imagerie 2025 · terrain"': '"2025 imagery · field check"',
    '["Surface",': '["Area",',
    '"agricole 630 · forêt 420 · autre 195"': '"farmland 630 · forest 420 · other 195"',
    '["Chefferie",': '["Chiefdom",',
    '"1 chefferie de 3ᵉ degré"': '"1 third-class chiefdom"',
    '"3 sites patrimoniaux, dont 1 protégé"': '"3 heritage sites, 1 of them protected"',
    '["Éducation",': '["Education",',
    '"1 école primaire · 1 collège"': '"1 primary school · 1 secondary school"',
    '"carte scolaire · terrain"': '"school map · field check"',
    '["Santé",': '["Health",',
    '"1 centre de santé, dégradé"': '"1 health centre, run-down"',
    '"terrain, mars 2026"': '"field check, March 2026"',
    '["Ressources",': '["Resources",',
    '"1 carrière ⚠ titre non trouvé"': '"1 quarry ⚠ no permit found"',
    '"observée, non rapprochée"': '"observed, not matched"',
    '["Routes",': '["Roads",',
    '"8,2 km · 3,1 km toute l\'année"': '"8.2 km · 3.1 km all-season"',
    '"terrain"': '"field check"',
    '["Couverture",': '["Coverage",',
    '["Accord",': '["Agreement",',
    '["Fraîcheur",': '["Freshness",',
    '["Vérification",': '["Verification",',
    '"Accès critique"': '"Critical access"',
    '"Centre de santé dégradé ; le suivant est à 14 km par une piste coupée en saison des pluies."':
        '"The health centre is run-down; the next one is 14 km away on a track cut off in the rainy season."',
    '["Éducation primaire",': '["Primary education",',
    '"4 salles manquantes"': '"4 classrooms short"',
    '"Calcul : enfants d\'âge scolaire estimés ÷ norme élèves par salle du ministère."':
        '"Calculation: estimated school-age children ÷ the ministry\'s pupils-per-classroom standard."',
    '["Électricité",': '["Electricity",',
    '"17 % des ménages"': '"17% of households"',
    '"Réseau moyenne tension à 6 km ; un mini-réseau solaire est à étudier."':
        '"Medium-voltage grid 6 km away; a solar mini-grid is worth studying."',
    '["Carrière",': '["Quarry",',
    '"Anomalie"': '"Discrepancy"',
    '"Exploitation observée sans titre correspondant au cadastre minier : vérification transmise."':
        '"Quarrying observed with no matching entry in the mining cadastre: referred for checking."',
    '"Quartier périurbain (exemple)"': '"Peri-urban neighbourhood (example)"',
    '"Commune d\'arrondissement · zone urbaine · référentiel v2026.1"': '"Sub-divisional council · urban zone · reference v2026.1"',
    '"≈ 12 600 hab."': '"≈ 12,600 people"',
    '"intervalle 11 400 à 13 900 · estimation 2026"': '"range 11,400 to 13,900 · 2026 estimate"',
    '"2 910"': '"2,910"',
    '"2 284 détectés · 1 240 vérifiés"': '"2,284 detected · 1,240 verified"',
    '"imagerie 2025 · terrain partiel"': '"2025 imagery · partial field check"',
    '"186 ha"': '"186 ha"',
    '"résidentiel 142 · commerce 21 · autre 23"': '"residential 142 · commercial 21 · other 23"',
    '["Foncier",': '["Land",',
    '"312 titres · 57 attestations"': '"312 titles · 57 certificates"',
    '"MINDCAF · registre des attestations"': '"MINDCAF · certificate register"',
    '"3 écoles primaires · 1 lycée"': '"3 primary schools · 1 high school"',
    '"carte scolaire"': '"school map"',
    '"1 CMA · 4 cliniques privées"': '"1 medical centre · 4 private clinics"',
    '"carte sanitaire · terrain"': '"health map · field check"',
    '["Économie",': '["Economy",',
    '"1 marché · 214 commerces"': '"1 market · 214 shops"',
    '"terrain, comptage agrégé"': '"field check, aggregate count"',
    '["Eau",': '["Water",',
    '"38 % raccordés"': '"38% connected"',
    '"enquête ménages"': '"household survey"',
    '["Eau potable",': '["Drinking water",',
    '"Extension du réseau prioritaire pour 1 800 ménages environ."': '"Network extension is a priority for about 1,800 households."',
    '"9 chevauchements"': '"9 overlaps"',
    '"Attestations qui recouvrent des titres existants : signalées au service des domaines."':
        '"Certificates overlapping existing land titles: reported to the lands office."',
    '"Effectifs élevés"': '"Overcrowded"',
    '"Classes au-dessus de la norme sectorielle dans 2 écoles sur 3."': '"Classes above the sector standard in 2 schools out of 3."',
    '"Couverture correcte"': '"Adequate coverage"',
    '"92 % des habitants à moins de 30 minutes d\'une formation sanitaire."': '"92% of residents within 30 minutes of a health facility."',
    '"vérifié"': '"verified"',
    '"estimé"': '"estimated"',
    '"déclaré"': '"reported"',
    '" / 100"': '" / 100"',

    # Modules
    '>La plateforme<': '>The platform<',
    '>Cinq modules, un seul référentiel territorial<': '>Five modules, one territorial reference<',
    '<h3>Population</h3><p>Habitat, ménages et dynamique démographique, publiés uniquement en agrégats.</p>':
        '<h3>Population</h3><p>Housing, households and population trends, published only as aggregates.</p>',
    '<h3>Foncier</h3><p>Occupation du sol, titres, attestations ARDFC/AJPTER, concessions et aires protégées.</p>':
        '<h3>Land</h3><p>Land use, titles, ARDFC/AJPTER certificates, concessions and protected areas.</p>',
    '<h3>Équipements</h3><p>Écoles, santé, routes, eau, énergie, télécoms, chefferies et patrimoine.</p>':
        '<h3>Facilities</h3><p>Schools, health, roads, water, energy, telecoms, chiefdoms and heritage.</p>',
    '<h3>Ressources</h3><p>Forêts, mines, carrières, eau, potentiel solaire et hydroélectrique, activités économiques.</p>':
        '<h3>Resources</h3><p>Forests, mines, quarries, water, solar and hydropower potential, economic activity.</p>',
    "<h3>Décision</h3><p>Rapprochement des sources, déficits, accessibilité et priorités d'investissement.</p>":
        "<h3>Decisions</h3><p>Source matching, gaps, accessibility and investment priorities.</p>",

    # Méthode
    '>Méthode<': '>Method<',
    '>Chaque information monte en preuve, étape par étape<': '>Every record gains proof, one step at a time<',
    "Un agent de terrain ne devient jamais une autorité juridique. Chaque donnée garde la trace de qui l'a fournie et de qui l'a validée.":
        "A field agent never becomes a legal authority. Every record keeps track of who supplied it and who validated it.",
    '<span class="num">Niveau 0</span><h3>Déclaration</h3><p>Chefs de village, communes et citoyens signalent ce qui manque ou a changé.</p><span class="statut">○ Déclaré</span>':
        '<span class="num">Level 0</span><h3>Reporting</h3><p>Village chiefs, councils and citizens report what is missing or has changed.</p><span class="statut">○ Reported</span>',
    '<span class="num">Niveau 1</span><h3>Imagerie</h3><p>Bâtiments, routes, forêts et plans d\'eau détectés par satellite.</p><span class="statut">◐ Détecté</span>':
        '<span class="num">Level 1</span><h3>Imagery</h3><p>Buildings, roads, forests and water bodies detected by satellite.</p><span class="statut">◐ Detected</span>',
    '<span class="num">Niveau 2</span><h3>Terrain</h3><p>Des agents vérifient l\'usage, l\'état et le fonctionnement, hors connexion si besoin.</p><span class="statut">● Observé</span>':
        '<span class="num">Level 2</span><h3>Field</h3><p>Agents check use, condition and working status, offline if needed.</p><span class="statut">● Observed</span>',
    '<span class="num">Niveau 3</span><h3>Administration</h3><p>Le ministère compétent valide titres, concessions, permis et licences.</p><span class="statut">● Validé</span>':
        '<span class="num">Level 3</span><h3>Administration</h3><p>The competent ministry validates titles, concessions, permits and licences.</p><span class="statut">● Validated</span>',

    # Sentinelle
    '>Le chef de village, sentinelle du territoire<': '>The village chief, watching over the territory<',
    '« Voici votre territoire. Dites-nous ce qui manque. »': '“Here is your territory. Tell us what is missing.”',
    'Une application à trois boutons, utilisable hors connexion. Les signalements orientent les vérifications ; ils ne remplacent pas les autorités compétentes.':
        'A three-button app that works offline. Reports guide where checks happen; they do not replace the competent authorities.',
    "Les signalements sensibles (conflit foncier, exploitation illégale) sont transmis à l'autorité sans être publiés.":
        "Sensitive reports (land disputes, illegal extraction) go to the authority without being published.",
    'Les attestations ARDFC et AJPTER délivrées par les chefs de 3ᵉ degré sont enregistrées comme attestations, jamais comme titres fonciers.':
        'ARDFC and AJPTER certificates issued by third-class chiefs are recorded as certificates, never as land titles.',
    'Chaque village reçoit sa fiche territoriale en retour.': 'Every village gets its area profile back.',
    "aria-label=\"Aperçu de l'application du chef de village\"": 'aria-label="Preview of the village chief app"',
    '<span class="titre">Votre territoire</span>': '<span class="titre">Your territory</span>',
    'Essayez : touchez une action.': 'Try it: tap an action.',
    'data-msg="Point placé sur la carte. Ajoutez une photo et une catégorie : maison, forage, école, piste…">Il manque quelque chose<small>Nouvelle maison, école, forage, route…</small>':
        'data-msg="Point placed on the map. Add a photo and a category: house, borehole, school, track…">Something is missing<small>New house, school, borehole, road…</small>',
    'data-msg="Objet sélectionné. Indiquez ce qui a changé : détruit, fermé, en travaux…">Ceci a changé<small>Disparu, fermé, agrandi</small>':
        'data-msg="Item selected. Say what has changed: destroyed, closed, under works…">This has changed<small>Gone, closed, extended</small>',
    "data-msg=\"Signalement non public, transmis à l'autorité compétente. Vous serez informé de la suite.\">Je signale un problème<small>Conflit, dégradation, risque</small>":
        'data-msg="Private report, sent to the competent authority. You will be told what happens next.">Report a problem<small>Dispute, damage, hazard</small>',

    # Confiance
    '>Confiance et souveraineté<': '>Trust and sovereignty<',
    '>Les données du pays restent au pays<': '>The country\'s data stays in the country<',
    'Une base qui relie personnes, terres et ressources doit protéger avant de montrer. TasetyGrid est conçu selon la loi n° 2024/017 sur la protection des données à caractère personnel.':
        'A database linking people, land and resources must protect before it shows. TasetyGrid is designed under Law No. 2024/017 on personal data protection.',
    "<b>L'État est propriétaire</b><p>Des données comme de l'hébergement. Formats ouverts et réversibilité garantis par contrat.</p>":
        "<b>The State owns it</b><p>Both the data and the hosting. Open formats and the right to take everything back are written into the contract.</p>",
    "<b>Le recensement reste secret</b><p>Les réponses individuelles restent chez l'institution de recensement. L'atlas ne reçoit que des agrégats.</p>":
        "<b>Census answers stay confidential</b><p>Individual responses stay with the census institution. The atlas only receives aggregates.</p>",
    "<b>Aucun droit créé</b><p>La plateforme référence les titres et concessions établis par l'autorité. Elle n'en délivre aucun.</p>":
        "<b>No rights created</b><p>The platform records titles and concessions issued by the authority. It issues none itself.</p>",
    "<b>Le patrimoine sacré est protégé</b><p>Forêts sacrées et sites rituels ne sont localisés publiquement qu'avec l'accord des communautés.</p>":
        "<b>Sacred heritage is protected</b><p>Sacred forests and ritual sites are only shown publicly with the community's consent.</p>",
    '<b>Chaque consultation est tracée</b><p>Un journal inaltérable des accès, audité par une instance indépendante.</p>':
        '<b>Every access is logged</b><p>A tamper-proof access log, audited by an independent body.</p>',
    '<b>Toute information est contestable</b><p>Une personne ou une communauté peut contester une donnée qui la concerne.</p>':
        '<b>Any record can be challenged</b><p>A person or community can challenge a record about them.</p>',
    'aria-label="Classes de sensibilité"': 'aria-label="Sensitivity classes"',
    '<span>S0 · Public</span><span>S1 · Restreint aux administrations</span><span>S2 · Confidentiel</span><span>S3 · Protégé culturel</span>':
        '<span>S0 · Public</span><span>S1 · Government only</span><span>S2 · Confidential</span><span>S3 · Culturally protected</span>',

    # Pilote
    '>Pilote Cameroun<': '>Cameroon pilot<',
    '>Commencer petit, mesurer, puis étendre<': '>Start small, measure, then scale<',
    '<span class="ph">Phase 0 · Cadrage</span><h3>Sources, droit et partenaires</h3><p>Inventaire des données existantes, revue juridique, accords avec les institutions propriétaires de chaque couche.</p>':
        '<span class="ph">Phase 0 · Scoping</span><h3>Sources, law and partners</h3><p>Inventory of existing data, legal review, agreements with the institutions that own each layer.</p>',
    '<span class="ph">Phase 1 · Socle national</span><h3>Le référentiel du pays</h3><p>Découpage administratif versionné, localités et bâtiments par imagerie, import des registres sectoriels.</p>':
        '<span class="ph">Phase 1 · National base</span><h3>The country\'s reference map</h3><p>Versioned administrative boundaries, settlements and buildings from imagery, import of sector registers.</p>',
    '<span class="ph">Phase 2 · Terrain</span><h3>Trois communes pilotes</h3><p>Une commune urbaine, une rurale agricole, une forestière ou minière : toutes les couches, du signalement à la validation.</p>':
        '<span class="ph">Phase 2 · Field</span><h3>Three pilot councils</h3><p>One urban, one rural farming, one forest or mining council: every layer, from report to validation.</p>',
    "<span class=\"ph\">Phase 3 · Évaluation</span><h3>Coûts et qualité mesurés</h3><p>Coût par bâtiment vérifié, taux d'erreur, délais de validation, usage réel dans les décisions.</p>":
        '<span class="ph">Phase 3 · Evaluation</span><h3>Cost and quality measured</h3><p>Cost per verified building, error rate, validation times, actual use in decisions.</p>',
    '<span class="ph">Phase 4 · Extension</span><h3>Par vagues régionales</h3><p>Imagerie et registres partout, terrain ciblé là où les sources se contredisent.</p>':
        '<span class="ph">Phase 4 · Roll-out</span><h3>In regional waves</h3><p>Imagery and registers everywhere, field checks where sources disagree.</p>',
    '<span class="ph">Phase 5 · Mise à jour continue</span><h3>Recensement intégré</h3><p>Intégration des résultats du 4ᵉ recensement général (RGPH/RGAE 2026) dès leur publication, puis mises à jour entre deux recensements.</p>':
        '<span class="ph">Phase 5 · Continuous updates</span><h3>Census built in</h3><p>Results of the 4th general census (RGPH/RGAE 2026) added as soon as they are published, then updates between censuses.</p>',
    '<h3>Ancré dans le cadre en vigueur</h3>': '<h3>Grounded in current law</h3>',
    '<li>Loi n° 2024/017 · données personnelles</li>': '<li>Law No. 2024/017 · personal data</li>',
    '<li>Loi n° 2020/010 · activité statistique</li>': '<li>Law No. 2020/010 · statistics</li>',
    '<li>Ordonnances n° 74-1 et 74-2 · foncier et domaines</li>': '<li>Ordinances No. 74-1 and 74-2 · land tenure and State lands</li>',
    '<li>Circulaire MINDCAF du 20 février 2026 · ARDFC et AJPTER</li>': '<li>MINDCAF circular of 20 February 2026 · ARDFC and AJPTER</li>',
    '<li>Loi n° 2019/024 · collectivités territoriales</li>': '<li>Law No. 2019/024 · local authorities</li>',
    '<li>Loi n° 2024/008 · forêts et faune</li>': '<li>Law No. 2024/008 · forestry and wildlife</li>',
    '<li>Loi n° 2023/014 · Code minier</li>': '<li>Law No. 2023/014 · Mining Code</li>',
    '<li>Loi n° 2013/003 · patrimoine culturel</li>': '<li>Law No. 2013/003 · cultural heritage</li>',
    'Au service de la Stratégie nationale de développement 2020-2030 et de la décentralisation.':
        'Supporting the 2020-2030 National Development Strategy and decentralisation.',

    # Nom
    "<small>tꜣ-stj · « le pays de l'arc »</small>": '<small>tꜣ-stj · “the land of the bow”</small>',
    "<b>Le nom</b><p>Ta-Sety est le nom que l'Égypte ancienne donnait à la Nubie. Grid, c'est la grille : la carte, la mesure, la donnée.</p>":
        "<b>The name</b><p>Ta-Sety is what ancient Egypt called Nubia. Grid is the map, the measurement, the data.</p>",
    "<b>La coquille</b><p>Dans la pensée kongo, la coquille d'escargot (kodya) évoque la vie qui grandit. La spirale du symbole est tracée sur une grille qui grandit avec elle.</p>":
        "<b>The shell</b><p>In Kongo thought, the snail shell (kodya) stands for growing life. The symbol's spiral is drawn on a grid that grows with it.</p>",
    '<b>Le cercle</b><p>Le cercle et ses quatre points reprennent le cosmogramme kongo : le cycle complet, comme la mise à jour continue du territoire.</p>':
        '<b>The circle</b><p>The circle and its four points echo the Kongo cosmogram: a full cycle, like the continuous updating of the territory.</p>',

    # Appel
    '>Rejoindre le pilote</p>': '>Join the pilot</p>',
    ">Construisons l'atlas avec ceux qui connaissent le terrain<": '>Let\'s build the atlas with the people who know the ground<',
    'Nous cherchons trois communes pilotes et les institutions qui détiennent les données de référence. Le projet est en phase de conception.':
        'We are looking for three pilot councils and the institutions that hold the reference data. The project is at the design stage.',
    'Adresse de contact publiée prochainement.': 'Contact address coming soon.',
    '<b>Communes</b><span>Inventaire de votre patrimoine et de vos besoins</span>': '<b>Councils</b><span>An inventory of your assets and needs</span>',
    '<b>Ministères</b><span>Vos cartes sectorielles, à jour et rapprochées</span>': '<b>Ministries</b><span>Your sector maps, up to date and cross-checked</span>',
    '<b>Chefferies</b><span>Votre territoire et votre patrimoine, documentés</span>': '<b>Chiefdoms</b><span>Your territory and heritage, documented</span>',
    '<b>Partenaires</b><span>Un ciblage des investissements fondé sur des preuves</span>': '<b>Partners</b><span>Evidence-based targeting of investment</span>',

    # Pied de page
    "TasetyGrid est un projet en conception. Ce n'est pas un service officiel de l'État camerounais et il n'est affilié à aucune administration citée.":
        "TasetyGrid is a project at the design stage. It is not an official service of the Cameroonian State and is not affiliated with any administration mentioned.",
}
