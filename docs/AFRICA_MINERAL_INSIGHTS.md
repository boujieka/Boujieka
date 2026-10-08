# AFRICA MINERAL INSIGHTS

**From Satellite to Minerals — From Minerals to Market**

> Note de cadrage du concept (version de travail, 2026-10-08). Document de conception. Les sources
> citées ont été vérifiées à la date indiquée ; les cellules « … » des matrices sont à remplir avec
> des données sourcées, jamais avec des estimations non signalées.
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

| # | Composante | Étude de cas Cameroun | Livrable |
|---|---|---|---|
| 01 | Geo-Spatial Intelligence | From Satellite to Mineral Target | Mineral Target Map |
| 02 | Mineral Potential | Can we identify Cameroon's next gold target? | Cameroon Gold Prospectivity Map |
| 03 | Mining Sector Intelligence | Mapping the Cameroon Mining Ecosystem | Cameroon Mining Ecosystem Map |
| 04 | Legal & Regulatory Insights | Is Cameroon's mining framework investment-ready? | Mining Regulatory Gap Matrix |
| 05 | Mineral Products & Value Chains | From Cameroon Bauxite to Aluminium Value | Cameroon Mineral Value Chain Map |
| 06 | Market & Trade Intelligence | Where should Cameroon sell its minerals? | Market Attractiveness Matrix |
| 07 | Mineral Investment Intelligence | Build the Cameroon Mining Investment Pipeline | Top 10 Opportunities + Investment Opportunity Score |
| 08 | Mineral Financing Intelligence | How do we finance a Cameroon mining project? | Indicative Mining Financing Structure |
| 09 | Value Addition, Diversification & National Strategy | How can Cameroon capture more value from its minerals? | Cameroon National Mineral Value Strategy |

## Dépendances entre études de cas

L'enchaînement n'est pas strictement linéaire. Les flux réels :

| Module | Utilise les livrables de |
|---|---|
| 02 Mineral Potential | 01 |
| 03 Mining Ecosystem | 01, 02 |
| 04 Legal Framework | 03 (titres, statuts, titulaires) |
| 05 Value Chains | 03 (ressources, installations) |
| 06 Markets | 05 (produits à chaque étape de la chaîne) |
| 07 Investment Pipeline | 02, 03, 04, 05, 06 |
| 08 Financing | 04, 07 |
| 09 National Strategy | 01 à 08 |

Conséquence pédagogique : les modules 04, 05 et 06 peuvent être enseignés en parallèle ; 07, 08 et
09 sont des modules de synthèse et doivent venir en fin de parcours. Il faut prévoir un **jeu de
données de secours** par module, pour qu'un groupe dont le livrable précédent est faible puisse
continuer.

## Socle de données publiques (Cameroun)

| Source | Contenu | Utilisé en | Limites vérifiées |
|---|---|---|---|
| USGS — *Compilation of Geospatial Data (GIS) for the Mineral Industries and Related Infrastructure of Africa* (data release 2021 ; carte GeoPDF : Open-File Report 2024-1041) | Installations de production et de traitement, sites d'exploration et de développement, occurrences, ports d'exportation, voies ferrées, routes, centrales et lignes électriques, pipelines, terminaux GNL | 01, 03, 05, 07 | Année de référence **2018**. Les « undiscovered resource tracts » ne couvrent que le Gabon, la Mauritanie et certaines substances (potasse, platinoïdes, cuivre), pas une évaluation propre au Cameroun |
| Cadastre minier en ligne du MINMIDT (Flexicadastre) | Titres miniers, limites, statut, titulaires | 03, 04, 07 | Annoncé comme opérationnel en 2017 ; état actuel, couverture et conditions de réutilisation à vérifier |
| Système d'information géologique et minière (SIGM), financé par la Banque mondiale (PRECASEM) | Données géologiques et géochimiques (campagne citée : 18 000 échantillons, 300 sites) | 01, 02 | Une étude pour l'African Minerals Development Centre (UA) rapportée en 2025 juge les données en grande partie obsolètes et insuffisamment standardisées |
| Copernicus Sentinel-2, Sentinel-1 (radar), Landsat, MNT (SRTM / Copernicus DEM) | Imagerie optique, radar, relief | 01, 02 | Couverture nuageuse et végétation dense au sud et à l'est (voir module 01) |
| Code minier : loi n° 2023/014 du 19 décembre 2023 et décrets d'application | Cadre juridique | 04, 08 | Remplace le code de 2016 ; décrets d'application publiés progressivement depuis 2024 — inventaire à faire |
| Statistiques commerciales (UN Comtrade et équivalents), prix publics de référence | Exportations, importations, partenaires, prix | 06 | Sous-déclaration de l'or artisanal : croiser avec les statistiques miroirs des pays importateurs |

## Les 9 composantes en détail

### 01 — GEO-SPATIAL INTELLIGENCE · « From Satellite to Mineral Target »

Les participants reçoivent une zone d'étude, avec Sentinel-2, Landsat, un MNT, la carte géologique,
les occurrences et, si disponible, la géochimie.

`Image satellite → indices spectraux → anomalies → structures → cible minérale`

Livrable : **Mineral Target Map**.

Choix de la zone d'étude (point critique) : en forêt dense et sous couvert latéritique (sud, est),
la télédétection optique ne voit pas les altérations hydrothermales, et les nuages limitent les
images exploitables. Deux options :
- une zone de savane (Adamaoua, Nord) pour l'exercice spectral ;
- ou une zone forestière en mettant l'accent sur l'analyse structurale (linéaments sur MNT et
  radar Sentinel-1) plutôt que sur les indices spectraux.

### 02 — MINERAL POTENTIAL · « Can we identify Cameroon's next gold target? »

`Géologie + Géochimie + Télédétection + Structures + Occurrences connues → matrice de prospectivité`

Livrable : **Cameroon Gold Prospectivity Map** (High / Medium / Low potential / Insufficient data).

Règles méthodologiques :
- l'objectif est de générer des cibles d'exploration à valider, pas d'annoncer un gisement ;
- **validation** : mettre de côté une partie des occurrences connues, construire le modèle sans
  elles, puis vérifier qu'il les retrouve ;
- ne pas confondre les zones d'orpaillage alluvionnaire (indices de surface) avec un potentiel de
  gisement primaire.

### 03 — MINING SECTOR INTELLIGENCE · « Mapping the Cameroon Mining Ecosystem »

`Mines + projets + permis + occurrences + routes + chemins de fer + énergie + ports`

Données : couches USGS Afrique + cadastre minier en ligne.

Livrable : **Cameroon Mining Ecosystem Map**, avec date et source affichées pour chaque couche (les
couches USGS reflètent 2018 ; le cadastre reflète la date d'extraction).

### 04 — LEGAL & REGULATORY INSIGHTS · « Is Cameroon's mining framework investment-ready? »

Texte de référence : **Code minier de 2023** (loi n° 2023/014) et ses décrets d'application, et non
le code de 2016.

Champs analysés : titres et permis, fiscalité, royalties, participation de l'État et rôle de
l'organisme public mandaté, contenu local, environnement, communautés, transformation locale,
exportation, stabilité fiscale, rapatriement des capitaux, fermeture et réhabilitation.

Comparaison avec 3 pays africains de référence, choisis à l'avance selon un critère explicite (par
exemple un pays de la CEMAC, un pays d'Afrique de l'Ouest, un pays réputé pour son attractivité
minière).

Livrable : **Mining Regulatory Gap Matrix**

| Domaine | Cameroun | Benchmark | Gap | Impact | Réforme proposée |
|---|---|---|---|---|---|
| Permis de recherche | … | … | … | … | … |
| Fiscalité et royalties | … | … | … | … | … |
| Participation de l'État | … | … | … | … | … |
| Contenu local | … | … | … | … | … |
| Transformation locale | … | … | … | … | … |
| Cadastre et transparence des titres | … | … | … | … | … |
| Environnement et fermeture | … | … | … | … | … |
| Exploitation artisanale | … | … | … | … | … |

Compétence visée : évaluer l'effet de la loi sur l'investissement et la création de valeur, pas
seulement la connaître.

### 05 — MINERAL PRODUCTS & VALUE CHAINS · « From Cameroon Bauxite to Aluminium Value »

Cas principal :
`Bauxite → concassage/lavage → alumine → aluminium → semi-produits → produits industriels`

Question : où se trouve la plus grande création de valeur, et quelle étape est réaliste pour le
Cameroun ? Pour chaque étape, identifier les intrants critiques (énergie, réactifs, eau), l'échelle
minimale et le capex indicatif sourcé. Point à documenter : l'existence d'une capacité
d'électrolyse d'aluminium dans le pays (Edéa) et son approvisionnement en alumine, à vérifier sur
sources primaires avant usage.

Mini-cas :
`Minerai de fer → concentré → pellet → DRI → acier → produits sidérurgiques`
(intrant clé du DRI : gaz naturel ou hydrogène ; à relier aux données énergie du module 03).

Livrable : **Cameroon Mineral Value Chain Map**.

### 06 — MARKET & TRADE INTELLIGENCE · « Where should Cameroon sell its minerals? »

Par minerai et par étape de la chaîne (livrable 05) : demande mondiale et africaine, producteurs et
importateurs principaux, prix, croissance, concurrence, transport, ports, marchés régionaux.

Livrable : **Market Attractiveness Matrix**

| Marché | Demande | Prix | Distance / logistique | Concurrence | Barrières (normes, droits) | Attractivité |
|---|---|---|---|---|---|---|
| Cameroun | … | … | … | … | … | … |
| CEMAC | … | … | … | … | … | … |
| Afrique (ZLECAf) | … | … | … | … | … | … |
| Europe | … | … | … | … | … | … |
| Asie | … | … | … | … | … | … |

Règle : publier la grille de notation (échelle, pondérations) avant de remplir la matrice.

### 07 — MINERAL INVESTMENT INTELLIGENCE · « Build the Cameroon Mining Investment Pipeline »

10 opportunités, une fiche chacune : minerai, localisation, niveau d'exploration, ressources connues
(avec le code de déclaration ou la mention « non conforme »), infrastructure, marché, capex
indicatif, risques, cadre réglementaire, potentiel de transformation.

**Investment Opportunity Score** : Geology — Resource — Infrastructure — Market — Regulation —
Economics — Risk.

Livrable : **Top 10 Cameroon Mineral Investment Opportunities**.

Règle : chaque chiffre porte sa source et sa date ; à défaut, la mention « estimation du
participant » ou « non disponible ». Les capex publics sont rares : c'est une limite à afficher,
pas à combler.

### 08 — MINERAL FINANCING INTELLIGENCE · « How do we finance a Cameroon mining project? »

Projet au stade pré-développement, de préférence **un projet stylisé construit à partir de données
publiques** (voir « Points ouverts » pour le cas d'un projet réel).

`Sponsor Equity + Strategic Investor + DFI Debt + Commercial Debt + Offtake Financing (+ Blended Finance) → Financial Close`

Les participants déterminent : qui finance quoi, à quel stade, quel risque, quelles garanties, quel
niveau de fonds propres, quelles conditions, quel mécanisme d'offtake, quelle structure de
remboursement.

Ajout recommandé : un **modèle financier simplifié** fourni (capex, opex, prix, production), pour
que la structure soit testée sur les ratios utilisés par les prêteurs : ratio de couverture du
service de la dette (DSCR), ratio de couverture sur la durée du prêt (LLCR), part de dette, TRI des
fonds propres, sensibilité au prix et aux retards de construction. Aspects spécifiques à couvrir :
risque de change (franc CFA BEAC / dollar), participation de l'État et son financement, normes
environnementales et sociales exigées par les prêteurs.

Livrable : **Indicative Mining Financing Structure** + tableau des risques et de leurs porteurs.

### 09 — VALUE ADDITION, DIVERSIFICATION & NATIONAL STRATEGY · « How can Cameroon capture more value from its minerals? »

Synthèse des 8 livrables : ressources prioritaires, chaînes de valeur prioritaires, transformations
réalisables localement, infrastructures nécessaires, investisseurs potentiels, financements
nécessaires, réformes réglementaires, marchés cibles.

Livrable : **Cameroon National Mineral Value Strategy (proposition)**

| Horizon | Phase | Contenu |
|---|---|---|
| 2027–2030 | Enable | Données, exploration, réglementation, cadastre, infrastructures, cadre de financement |
| 2030–2035 | Develop | Mines, traitement, concentrateurs, transformation primaire, bouclage financier des projets prioritaires |
| 2035–2040+ | Transform | Industrialisation, manufacturing, exportation de produits à plus forte valeur ajoutée |

Règle : situer la proposition par rapport aux documents de stratégie existants du pays (stratégie
nationale de développement, politiques sectorielles), et la présenter comme une proposition
d'analystes, pas comme la stratégie de l'État.

## Réplicabilité

L'architecture (9 composantes, 9 cas, mêmes livrables) est reproductible pour d'autres pays (RDC,
Guinée, Congo, Zambie, Ghana, Mali, Tanzanie…). La profondeur de chaque édition dépendra en revanche
des données disponibles : qualité du cadastre, accessibilité des données géologiques, publication
des contrats. Chaque édition commence donc par un **inventaire des données** qui fixe le niveau
de détail réaliste de chaque module.

## Points ouverts

1. **Nom** : « Africa Mineral Insights » ou « Africa Mining Intelligence ». À arrêter, après
   vérification de disponibilité (marque, domaine).
2. **Formation contre intelligence** : les livrables produits par les participants ne sont pas
   publiables tels quels. Il faut une revue par des experts avant toute diffusion ou vente, et
   des règles claires sur la propriété intellectuelle des travaux.
3. **Projet réel au module 08** : risques de confidentialité et de réputation. Par défaut, utiliser
   un projet stylisé.
4. **Conditions de réutilisation des données** : les données USGS sont en principe du domaine
   public ; celles du cadastre et du SIGM doivent être vérifiées avant toute exploitation commerciale.
5. **Scores composites** : publier la méthode, les pondérations et les sources ; distinguer données
   vérifiées, estimations et jugements d'experts.

## Sources vérifiées (2026-10-08)

- USGS, *Compilation of Geospatial Data (GIS) for the Mineral Industries and Related Infrastructure
  of Africa*: https://www.usgs.gov/data/compilation-geospatial-data-gis-mineral-industries-and-related-infrastructure-africa
- USGS, Open-File Report 2024-1041 (carte GeoPDF): https://pubs.usgs.gov/publication/ofr20241041
- Cameroon Tribune, Flexicadastre: https://www.cameroon-tribune.cm/article.html/9048/en.html/details_2
- Financial Afrik (2025), étude sur le potentiel minier et le SIGM: https://www.financialafrik.com/2025/07/10/au-cameroun-lurgence-dactualiser-le-potentiel-minier-pour-ameliorer-les-recettes-etude
- Loi n° 2023/014 du 19 décembre 2023 portant Code minier (UNEP LEAP): https://leap.unep.org/en/countries/cm/national-legislation/loi-ndeg-2023-014-du-19-decembre-2023-portant-code-minier
- Texte du code (AMLA): https://www.a-mla.org/en/country/pdf/2229

## Avertissement

Contenu d'information, de formation et d'analyse. Ne constitue ni un conseil en investissement, ni
un conseil juridique ou fiscal.
