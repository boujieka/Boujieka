# AFRICA MINERAL INSIGHTS

**From Satellite to Minerals — From Minerals to Market**

> Note de cadrage du concept (version 3, 2026-10-08, après contre-vérification croisée de l'édition
> Cameroun). Document de conception. Les faits cités renvoient aux modules détaillés
> (`docs/cameroon/01` à `09`) et aux rapports de vérification (`docs/cameroon/verification/`), qui
> portent les sources primaires. Les cellules « … » des matrices sont à remplir avec des données
> sourcées, jamais avec des estimations non signalées.
>
> Nom antérieur de travail : *Africa Mining Intelligence — From Satellite to Mine, From Mine Products
> to Market*. Le nom définitif reste à arrêter (voir « Points ouverts »).

## Principe

Chaque composante = **un module de formation + une étude de cas pratique sur données réelles et
publiques + un livrable d'intelligence exploitable**. Les études de cas s'enchaînent : le livrable
de chaque module est une donnée d'entrée des modules suivants. Projet final :

> *Take a mineral opportunity from satellite observation all the way to an investable, financeable
> and value-adding national development strategy.*

La formation n'est donc plus un pilier séparé : elle est intégrée dans chacune des 9 composantes.

## Description officielle

Africa Mineral Insights is a hybrid country platform that combines professional training and
actionable mineral intelligence. Each country edition is built around nine components — geospatial
intelligence, mineral potential, mining sector intelligence, legal and regulatory insights, mineral
products and value chains, market and trade intelligence, investment intelligence, financing
intelligence, and value addition and national strategy — each delivered as a practical case study
on real, public data.

The case studies are linked: each one produces an output that feeds the next, so that participants
take a mineral opportunity from satellite observation to an investable, financeable and
value-adding national strategy.

The platform answers six strategic questions: What does the country have? What can it develop?
Where are the markets? What prevents greater value creation? How can projects be financed? How can
the country capture more value from its mineral resources?

## Les 9 composantes et leurs études de cas — édition Cameroun

| # | Composante | Étude de cas Cameroun | Livrable | Module détaillé |
|---|---|---|---|---|
| 01 | Geo-Spatial Intelligence | From Satellite to Mineral Target | Mineral Target Map | `cameroon/01-geospatial-intelligence.md` |
| 02 | Mineral Potential | Can we identify Cameroon's next gold target? | Cameroon Gold Prospectivity Map | `cameroon/02-mineral-potential.md` |
| 03 | Mining Sector Intelligence | Mapping the Cameroon Mining Ecosystem | Cameroon Mining Ecosystem Map | `cameroon/03-mining-sector-intelligence.md` |
| 04 | Legal & Regulatory Insights | Is Cameroon's mining framework investment-ready? | Mining Regulatory Gap Matrix | `cameroon/04-legal-regulatory.md` |
| 05 | Mineral Products & Value Chains | From Cameroon Bauxite to Aluminium Value | Cameroon Mineral Value Chain Map | `cameroon/05-value-chains.md` |
| 06 | Market & Trade Intelligence | Where should Cameroon sell its minerals? | Market Attractiveness Matrix (par produit) | `cameroon/06-market-trade.md` |
| 07 | Mineral Investment Intelligence | Build the Cameroon Mining Investment Pipeline | Top 10 Opportunities + Investment Opportunity Score | `cameroon/07-investment-intelligence.md` |
| 08 | Mineral Financing Intelligence | How do we finance a Cameroon mining project? | Indicative Mining Financing Structure | `cameroon/08-financing-intelligence.md` |
| 09 | Value Addition, Diversification & National Strategy | How can Cameroon capture more value from its minerals? | Cameroon National Mineral Value Strategy (proposition) | `cameroon/09-value-strategy.md` |

## Dépendances entre études de cas

L'enchaînement n'est pas strictement linéaire. Les flux réels :

| Module | Utilise | Remarque |
|---|---|---|
| 02 Mineral Potential | 01 ; occurrences et projets de base (USGS, rapports d'entreprises) | Retour vers 01 : les zones à fort potentiel orientent de nouvelles analyses satellitaires |
| 03 Mining Ecosystem | 01, 02 | Même emprise et même système de coordonnées que 01 et 02 |
| 04 Legal Framework | 03 (titres, statuts, titulaires) ; sources externes (BEAC, ITIE) | L'exercice 3 utilise les paramètres du projet stylisé de 08, à fournir dès le module 04 |
| 05 Value Chains | 03 (ressources, installations) | |
| 06 Markets | 05 (produits à chaque étape de la chaîne) | |
| 07 Investment Pipeline | 02, 03, 04, 05, 06 | Jeu de secours pour les substances non couvertes par 02, 05 et 06 (cobalt-nickel-manganèse, rutile, calcaire) |
| 08 Financing | 04, 07 ; 05 et 06 (prix, fret, étape de transformation) | |
| 09 National Strategy | 01 à 08 | Renvoie aux livrables au lieu de réécrire les faits |

Conséquence pédagogique : les modules 04, 05 et 06 peuvent être enseignés en parallèle ; 07, 08 et
09 sont des modules de synthèse et doivent venir en fin de parcours. Il faut prévoir un **jeu de
données de secours** par module, pour qu'un groupe dont le livrable précédent est faible puisse
continuer.

## Socle de données publiques (Cameroun)

| Source | Contenu | Utilisé en | Limites vérifiées |
|---|---|---|---|
| USGS — *Compilation of Geospatial Data (GIS) for the Mineral Industries and Related Infrastructure of Africa* (DOI 10.5066/P97EQWXP ; carte GeoPDF : Open-File Report 2024-1041) | Installations, gisements, sites d'exploration, ports, rail, routes, énergie | 01, 03, 05, 07 | Année de référence **variable selon la couche** : installations 2018 ; gisements 2009 et 2017 ; exploration 2004-2018 ; routes et rails OpenStreetMap au 30/04/2020. Pour le Cameroun : 9 gisements, 13 sites d'exploration (1 seul en or), aucune occurrence d'or, **Kribi absent** de la couche ports ; coordonnées incohérentes entre couches pour Nkamouna et Minim-Martap. Licence CC0 pour la production USGS seulement : couches OSM sous ODbL, limites GADM sans usage commercial ni redistribution sans permission |
| Portail cadastral Landfolio (ex-Flexicadastre) du MINMIDT | Titres miniers | 03, 04, 07 | **Hors service depuis le 03/11/2025.** Avant sa fermeture : republication interdite sans autorisation écrite, aucun export ouvert |
| **Rapport ITIE 2023** (publié en décembre 2025) et annexes XLSX | Titres (annexe 30 : 261 titres actifs au 31/12/2023, **sans coordonnées**), production, exportations d'or, recettes | 03, 04, 06, 09 | Source de remplacement du cadastre. Le Cameroun est **suspendu de l'ITIE** par la décision 2024-17 du **29/02/2024** (score de 53) ; prochaine Validation à partir du 01/04/2027. Licence de réutilisation non précisée |
| PRECASEM (Banque mondiale, P122153 et P160917, **clos le 01/12/2021**) et SIGM | Données géologiques et géochimiques | 01, 02 | Campagne géochimique **prévue** d'environ 18 000 échantillons (annonce de janvier 2017) ; 300 nouveaux sites minéralisés annoncés en juin 2019 pour 2014-2019. SIGM conçu dans ce cadre (présentation BRGM, 2018). **Accès public non trouvé** au SIGM, à la géochimie, aux cartes au 1/200 000 et aux levés aéroportés |
| Cartes géologiques accessibles | Contexte régional | 01, 02 | Carte au 1/1 000 000 (Gazel, révisée en 1956, Atlas IRD) et carte géologique de l'Afrique USGS (1997) : contexte régional seulement. Feuilles au 1/500 000 des années 1950 : métadonnées seulement |
| Copernicus Sentinel-2, Sentinel-1 (radar), Landsat, MNT (SRTM, Copernicus DEM) | Imagerie optique, radar, relief | 01, 02 | Nuages : fenêtre utile de **novembre à février**, y compris au Nord. Le Copernicus DEM est un modèle de surface : en forêt, il représente la canopée. Sentinel-1 n'a eu qu'un satellite de fin 2021 à fin 2024 |
| Code minier : loi n° 2023/014 du 19/12/2023 (abroge la loi n° 2016/017, art. 200) | Cadre juridique | 04, 07, 08 | **Huit décrets d'application** signés les 18 et 19/11/2024 (n° 2024/05061/PM, 05062, 05248, 05249, 05250, 05251, 05252, 05253). Arrêté du 09/06/2025 et décrets du 25/06/2025 rapportés par la presse, textes non consultés. Copie de travail : FAOLEX ; la transcription AMLA présente des décalages de numérotation. À comparer au Journal officiel |
| Statistiques commerciales : UN Comtrade (déclarant Cameroun jusqu'en 2023), INS *Le Commerce extérieur en 2024*, Pink Sheet de la Banque mondiale | Exportations, importations, partenaires, prix | 05, 06 | Les statistiques miroirs sont une borne indicative : l'origine déclarée est incertaine (Rwanda, Ouganda), avec des délais de publication et des révisions |

## Les 9 composantes en détail

### 01 — GEO-SPATIAL INTELLIGENCE · « From Satellite to Mineral Target »

Les participants reçoivent une zone d'étude, avec Sentinel-2, Landsat, un MNT, la carte géologique,
les occurrences et, si disponible, la géochimie.

`Image satellite → indices spectraux → anomalies → structures → cible minérale`

Livrable : **Mineral Target Map**.

Choix de la zone d'étude : en forêt dense et sous couvert latéritique (sud, est), la télédétection
optique est **fortement dégradée** et doit être validée systématiquement sur le terrain. Les nuages
limitent les images partout, y compris au Nord. Zones proposées par le module 01 :
- **Z1 Tcholliré–Rey Bouba (Nord)**, zone principale : savane, occurrences d'or publiées avec
  coordonnées ;
- Z2 Bétaré-Oya (Est septentrional), zone intermédiaire ;
- Z3 Batouri (Est), variante structurale (linéaments sur MNT et radar Sentinel-1) pour l'or sous
  latérite.

La couche USGS ne permet pas de cibler l'or au Cameroun : elle ne contient qu'un site d'exploration
d'or.

Convention commune aux modules 01, 02 et 03 :
- stockage en WGS 84 (EPSG:4326) et calculs en UTM 33N (EPSG:32633) ;
- district de zoom commun : **Z2 Bétaré-Oya**, la seule zone partagée par les modules 01 et 02 ;
- Z1 reste la zone de l'exercice spectral du module 01.

### 02 — MINERAL POTENTIAL · « Can we identify Cameroon's next gold target? »

`Géologie + Structures + Géochimie + Géophysique + Télédétection (savane) → modèle → carte`

Les occurrences connues servent à **entraîner et valider** le modèle, pas comme couche d'entrée.
Sinon la validation est circulaire.

Livrable : **Cameroon Gold Prospectivity Map** (High / Medium / Low potential / Insufficient data).
La classe « Insufficient data » repose sur un indice de couverture des données, pas sur le score.

Règles méthodologiques :
- l'objectif est de générer des cibles d'exploration à valider, pas d'annoncer un gisement ;
- **validation par blocs spatiaux ou par districts entiers** (les occurrences sont groupées : un
  retrait aléatoire de points est trop faible), avec courbes de succès et de prédiction ;
- test central : construire le modèle sans les données des projets Mbe et Bibemi, puis vérifier
  s'il les classe en High ou Medium ;
- distinguer l'or primaire, éluvial et alluvial.

Seules ressources aurifères déclarées selon un code reconnu (JORC 2012), d'après le rapport
d'Oriole Resources du 22/09/2026 : Mbe (1,66 Moz, catégorie Inferred) et Bibemi (environ 460 koz).
Aucune ressource déclarée trouvée pour les districts de l'Est (Batouri, Kambélé).

### 03 — MINING SECTOR INTELLIGENCE · « Mapping the Cameroon Mining Ecosystem »

`Mines + projets + titres + occurrences + routes + chemins de fer + énergie + ports`

Données : couches USGS Afrique (date affichée par couche) + Rapport ITIE 2023, annexe 30 (titres au
31/12/2023) + OpenStreetMap. Afficher sur la carte : « Titres : situation au 31/12/2023 ; portail
cadastral hors service depuis le 03/11/2025 ». Les titres sont des points approximatifs, pas des
polygones cadastraux. Une demande formelle à la Sous-Direction du Cadastre Minier est à prévoir.

Livrable : **Cameroon Mining Ecosystem Map**.

### 04 — LEGAL & REGULATORY INSIGHTS · « Is Cameroon's mining framework investment-ready? »

Textes de référence : **Code minier de 2023** (loi n° 2023/014) et ses huit décrets d'application
de novembre 2024, et non le code de 2016.

Dispositions clés relevées par le module 04 (articles du Code 2023) :
- participation de l'État : 10 % gratuits et non diluables, plus jusqu'à 25 % **à titre onéreux**
  en mine industrielle (art. 47) ;
- partage de production : 1 à 5 % (substances précieuses) ou 2 à 15 % (autres) (art. 48) ;
- taxe ad valorem : 8 % pierres précieuses, 5 % métaux précieux, 3 % métaux de base, 10 %
  substances radioactives (art. 132) ;
- transformation locale : au moins 15 % de la production (art. 40(4)) ; or exporté affiné
  (art. 117(3)) ;
- stabilité fiscale limitée à un TRI de 15 % et à 15 ans au plus (art. 149) ;
- fonds de fermeture en séquestre à la Banque centrale (art. 192) ;
- arbitrage possible, sans institution désignée (art. 188-189).

Organisme public mandaté : **SONAMINES** (Société Nationale des Mines, décret n° 2020/749 du
14/12/2020), désignée par les décrets 2024/05061 et 05062. Elle a l'exclusivité de l'achat et de la
commercialisation de l'or et du diamant.

Benchmark : **Gabon** (pair CEMAC), **Côte d'Ivoire** (1re d'Afrique de l'Ouest, classement Fraser
2025), **Botswana** (1er en Afrique, classement Fraser 2025).

Livrable : **Mining Regulatory Gap Matrix**

| Domaine | Cameroun | Benchmark | Gap | Impact | Note | Réforme proposée |
|---|---|---|---|---|---|---|
| Permis de recherche | … | … | … | … | … | … |
| Fiscalité et royalties | … | … | … | … | … | … |
| Participation de l'État | … | … | … | … | … | … |
| Contenu local | … | … | … | … | … | … |
| Transformation locale | … | … | … | … | … | … |
| Cadastre et transparence des titres | … | … | … | … | … | … |
| Stabilité fiscale et juridique | … | … | … | … | … | … |
| Change et rapatriement | … | … | … | … | … | … |
| Commercialisation de l'or et du diamant | … | … | … | … | … | … |
| Gouvernance et transparence (ITIE) | … | … | … | … | … | … |
| Communautés | … | … | … | … | … | … |
| Environnement et fermeture | … | … | … | … | … | … |
| Exploitation artisanale | … | … | … | … | … | … |
| Règlement des différends | … | … | … | … | … | … |

Compétence visée : évaluer l'effet de la loi sur l'investissement et la création de valeur, pas
seulement la connaître. Ce module ne constitue pas un avis juridique.

### 05 — MINERAL PRODUCTS & VALUE CHAINS · « From Cameroon Bauxite to Aluminium Value »

Cas principal :
`Bauxite → concassage/criblage (lavage selon le gisement) → alumine → aluminium → semi-produits → produits industriels`

Situation vérifiée :
- **Électrolyse :** le Cameroun dispose d'une capacité de 100 kt/an nominaux à Edéa (Alucam). Elle
  est très sous-utilisée (34 à 74 kt/an de 2017 à 2022 ; 53 675 t en 2025) et en crise technique
  et financière depuis 2024.
- **Alumine :** il n'existe **aucune raffinerie d'alumine** dans le pays. L'alumine est entièrement
  importée : 135 347 t en 2023, dont 76 655 t de Guinée (UN Comtrade). La chaîne nationale est
  donc **discontinue**.
- **Bauxite :** Minim-Martap a des réserves JORC 2012 de 144 Mt. La première expédition, prévue au
  T4 2026, est **reportée sans nouvelle date** depuis la suspension des tirages de la facilité AFG
  Bank le 24/08/2026.
- **Aval :** une capacité existe déjà (laminage) et un projet de bobines et câbles est annoncé.

Question pour les participants : où se trouve la plus grande création de valeur (réponse
documentée : à l'électrolyse, qui consomme environ 13 à 15 MWh/t), et quelle étape manquante est
réaliste pour le Cameroun ?

Mini-cas :
`Minerai de fer → concentré → pellet → DRI → acier → produits sidérurgiques`
Le DRI exige un pellet de qualité DR (environ 67,5 % Fe, SiO₂ + Al₂O₃ ≤ 2,5 %). Or les concentrés
annoncés titrent environ 60 % Fe, et il n'existe au Cameroun aucune usine de pellets ni de DRI.
Aucun projet de fer n'exporte encore.

Livrable : **Cameroon Mineral Value Chain Map**.

### 06 — MARKET & TRADE INTELLIGENCE · « Where should Cameroon sell its minerals? »

Une matrice **par produit** (au minimum : aluminium brut, or, bauxite, minerai de fer,
ciment/clinker), avec les marchés en lignes selon le produit : Cameroun, CEMAC, Nigeria, Europe,
Chine, Japon/Corée, Émirats arabes unis, Turquie, États-Unis. La ZLECAf (ratifiée par le Cameroun
le 01/12/2020) est un régime d'accès : elle relève de la colonne « Barrières », pas d'une ligne de
marché.

Livrable : **Market Attractiveness Matrix**

| Marché | Demande | Prix net réalisable | Distance / logistique | Concurrence | Barrières (normes, droits, ZLECAf) | Attractivité |
|---|---|---|---|---|---|---|
| … | … | … | … | … | … | … |

Faits structurants (module 06) :
- **Aluminium brut :** 43 916 t exportées en 2023, dont 94,5 % vers l'UE **en valeur** (88,3 % en
  volume).
- **Or :** 22,31 kg d'exportations déclarées en 2023, contre 15 195 kg déclarés par les pays
  importateurs. Le vrai sujet est la formalisation et la traçabilité, pas la recherche de marchés.
- **Clinker :** il relève de la substitution aux importations, pas de l'exportation.

Règle : publier la grille de notation (échelle, pondérations) avant de remplir la matrice.

### 07 — MINERAL INVESTMENT INTELLIGENCE · « Build the Cameroon Mining Investment Pipeline »

10 opportunités, une fiche chacune :
- minerai, localisation, **titulaire**, **statut du titre**, **litiges**, **participation de
  l'État** ;
- niveau d'exploration ;
- **statut de la ressource** : conforme actuel / historique / non conforme / non disponible, en
  distinguant ressource et réserve ;
- infrastructure, marché, capex indicatif (en précisant sa nature), risques, cadre réglementaire,
  potentiel de transformation ;
- **date de la dernière information**.

**Investment Opportunity Score** : Geology — Resource — Infrastructure — Market — Regulation —
Economics — Risk, chacun noté de 0 à 5. Pondérations proposées par le module 07 : 15 / 20 / 20 / 10
/ 10 / 15 / 10. Un **indice de confiance** est affiché à côté du score, et un test à poids égaux
est fait. La note Market se déduit de la matrice du module 06 selon une règle de conversion
explicite.

Livrable : **Top 10 Cameroon Mineral Investment Opportunities**.

Constat de la contre-vérification : à ce jour, aucun grand projet ne prouve d'exportation. Seuls
Canyon (bauxite) et Oriole (or) publient des ressources JORC 2012 actuelles.

Règle : chaque chiffre porte sa source et sa date ; à défaut, la mention « estimation du
participant » ou « non disponible ». Ce n'est pas un conseil en investissement.

### 08 — MINERAL FINANCING INTELLIGENCE · « How do we finance a Cameroon mining project? »

Projet au stade pré-développement : **projet stylisé « Bauxite-Nord »**, explicitement fictif,
paramétré sur des ordres de grandeur publics de Minim-Martap. Ses paramètres sont fournis dès le
module 04.

`Sponsor Equity + Strategic Investor + DFI Debt + Commercial Debt + Dette bancaire locale/régionale en FCFA (refinancement BEAC) + Offtake/Prepayment + Royalty/Streaming (+ Blended Finance) → Financial Close`

Constat : aucune mine camerounaise financée par une institution de développement, une agence de
crédit export occidentale ou une garantie MIGA n'a été trouvée. Les financements documentés sont
des **prêts de banques locales en FCFA** (par exemple AFG Bank pour Minim-Martap, tirages suspendus
le 24/08/2026). Le financement par une institution de développement est donc présenté comme une
**cible**, pas comme la norme.

Sous-module ajouté : **contrôle des changes et architecture des comptes**. Contenu :
- réglementation de change CEMAC applicable au secteur extractif ;
- obligation de rapatriement de 35 %, portée à 50 % en 2027 puis 70 % en 2028 selon l'instruction
  BEAC 001/GR/2026. Le terme exact et les sanctions restent à arbitrer sur le texte officiel ;
- fonds de restauration en séquestre à la Banque centrale (art. 192) ;
- participation de l'État (art. 47) et son financement.

Modèle financier fourni (code Python, recalculé par le vérificateur). Ratios : DSCR, LLCR, part de
dette, TRI des fonds propres, sensibilités. Résultat illustratif : le DSCR minimum passe de 1,46 en
base à 0,87 si le prix baisse de 10 %. Les réserves de modélisation sont listées dans le module 08.

Livrable : **Indicative Mining Financing Structure** + tableau des risques et de leurs porteurs. Ce
n'est pas un conseil en investissement.

### 09 — VALUE ADDITION, DIVERSIFICATION & NATIONAL STRATEGY · « How can Cameroon capture more value from its minerals? »

Synthèse des 8 livrables : ressources prioritaires, chaînes de valeur prioritaires, transformations
réalisables localement, infrastructures nécessaires, investisseurs potentiels, financements
nécessaires, réformes réglementaires, marchés cibles.

Cadre existant :
- **SND30 (2020-2030)** : orientations minières, mais aucun objectif minier chiffré ;
- **Code minier 2023** : il impose déjà de la transformation locale (art. 40, 117) ;
- plan directeur d'industrialisation (texte non consulté).

Aucune politique minière nationale adoptée n'a été trouvée. Les horizons Develop et Transform
dépassent tout cadre officiel existant. Les horizons se chevauchent : des projets « Develop » sont
déjà en cours et une capacité « Transform » existe déjà (électrolyse à Edéa).

Livrable : **Cameroon National Mineral Value Strategy (proposition)**

| Horizon | Phase | Contenu |
|---|---|---|
| 2027–2030 | Enable | Données (accès SIGM, cadastre public), exploration, application de la réglementation, transparence (sortie de la suspension ITIE), cadre de financement |
| 2030–2035 | Develop | Mines, traitement, concentrateurs, transformation primaire, bouclage financier des projets prioritaires |
| 2035–2040+ | Transform | Industrialisation, manufacturing, exportation de produits à plus forte valeur ajoutée |

Règle : présenter la stratégie comme une proposition d'analystes, pas comme la stratégie de l'État.
L'enjeu central est l'**application** des obligations déjà prévues par le Code.

## Réplicabilité

L'architecture (9 composantes, 9 cas, mêmes livrables) est reproductible pour d'autres pays (RDC,
Guinée, Congo, Zambie, Ghana, Mali, Tanzanie…). La profondeur de chaque édition dépendra en revanche
des données disponibles : qualité du cadastre, accessibilité des données géologiques, publication
des contrats. L'édition Cameroun le montre : le cadastre en ligne est fermé et les données du SIGM
ne sont pas accessibles. Chaque édition commence donc par un **inventaire des données** qui fixe le
niveau de détail réaliste de chaque module.

## Points ouverts

1. **Nom** : « Africa Mineral Insights » ou « Africa Mining Intelligence ». À arrêter, après
   vérification de disponibilité (marque, domaine).
2. **Formation contre intelligence** : les livrables produits par les participants ne sont pas
   publiables tels quels. Il faut une revue par des experts avant toute diffusion ou vente, et
   des règles claires sur la propriété intellectuelle des travaux.
3. **Projet réel au module 08** : risques de confidentialité et de réputation. Par défaut, utiliser
   le projet stylisé.
4. **Conditions de réutilisation des données** :
   - USGS : CC0 pour la production USGS, mais licences tierces par couche (OSM ODbL, GADM non
     commercial) ;
   - cadastre : portail fermé, et sa republication était déjà interdite ;
   - SIGM : accès non établi ;
   - ITIE : licence non précisée.
   À régler avant toute exploitation commerciale.
5. **Scores composites** : publier la méthode, les pondérations et les sources ; distinguer données
   vérifiées, estimations et jugements d'experts.
6. **Arbitrages nécessitant une nouvelle source** (rapport de cohérence, priorité 2) :
   - libellé exact de l'instruction BEAC 001/GR/2026 ;
   - séries d'exportation d'or (gouvernement contre DGD/ITIE) ;
   - ressource de Minim-Martap (1 102 ou 1 027 Mt) et montant tiré sur la facilité AFG ;
   - capacité de Grand Zambi ;
   - part de l'État dans Alucam ;
   - ressources de Nkamouna.
7. **Homogénéité des modules** : adopter une convention unique de statuts de vérification, de
   format de sources et de dates (rapport de cohérence, section 5).

## Sources principales (vérifiées le 2026-10-08)

Les sources détaillées sont dans chaque module et dans `docs/cameroon/verification/`.

- USGS, *Compilation of Geospatial Data (GIS) for the Mineral Industries and Related Infrastructure
  of Africa* (DOI 10.5066/P97EQWXP): https://www.usgs.gov/data/compilation-geospatial-data-gis-mineral-industries-and-related-infrastructure-africa
- USGS, Open-File Report 2024-1041 (carte GeoPDF): https://pubs.usgs.gov/publication/ofr20241041
- Portail Landfolio Cameroun (avis de mise hors service): https://portals.landfolio.com/cameroon/
- Cameroon Tribune, annonce du Flexicadastre (2017 ; portail fermé depuis le 03/11/2025): https://www.cameroon-tribune.cm/article.html/9048/en.html/details_2
- ITIE, Rapport 2023 du Cameroun: https://eiti.org/document/25589
- ITIE, décision 2024-17 du 29/02/2024: https://api.eiti.org/fr/board-decision/2024-17
- Financial Afrik (10/07/2025), étude AMDC sur le potentiel minier (ne cite ni le SIGM, ni le
  PRECASEM, ni les chiffres 18 000 / 300): https://www.financialafrik.com/2025/07/10/au-cameroun-lurgence-dactualiser-le-potentiel-minier-pour-ameliorer-les-recettes-etude
- Code minier 2023, copie FAOLEX: https://faolex.fao.org/docs/pdf/cmr223180.pdf
- Code minier 2023, transcription AMLA (numérotation à contrôler): https://www.a-mla.org/en/country/pdf/2229
- Décrets d'application de novembre 2024: https://dgb.cm/?p=28315
- Décret n° 2020/749 portant création de SONAMINES: https://prc.cm/en/news/the-acts/decrees/4784-decree-no-2020-749-of-14-december-2020-to-set-up-the-national-mining-corporation-2

## Avertissement

Contenu d'information, de formation et d'analyse. Ne constitue ni un conseil en investissement, ni
un conseil juridique ou fiscal.
