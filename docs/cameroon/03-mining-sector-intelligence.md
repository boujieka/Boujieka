# Module 03 — Mining Sector Intelligence · « Mapping the Cameroon Mining Ecosystem »

> Édition Cameroun — livrable : **Cameroon Mining Ecosystem Map**.
> Version de travail du 2026-10-08. Toutes les URL citées ont été consultées le **2026-10-08**, sauf
> mention contraire. Les données USGS ont été téléchargées depuis ScienceBase et analysées localement
> (comptages par couche ci-dessous). Les informations antérieures au 2024-10-08 (plus de 2 ans) sont
> signalées par **[ancien]**.
>
> **Avertissement.** Contenu d'information et de formation, **pas un conseil** (ni en
> investissement, ni juridique, ni fiscal). Les cartes et inventaires de ce module décrivent des
> informations publiques datées ; ils ne constituent ni une déclaration de ressources ni une
> évaluation de projet.
>
> Légende des statuts : **Fait vérifié** (source consultée, citée) · **Inférence** (déduction
> explicite à partir de faits vérifiés) · **Hypothèse** (proposition de travail à tester) ·
> **Inconnue** / **Non vérifié** (aucune source consultée ne l'établit).
>
> Limite de méthode : le quota de recherches web de la session a été épuisé en fin de travail. Les
> points qui n'ont pas pu être recherchés (diamant de Mobilong aujourd'hui, capacités cimentières
> 2025, actionnariat actuel de Camrail, Lom Pangar, etc.) sont marqués « Non vérifié » et listés en §11.

---

## 1. Résumé

1. **Le cadastre minier en ligne n'existe plus.** Le portail public Landfolio (ex-Flexicadastre) du
   MINMIDT, `https://portals.landfolio.com/Cameroon/`, affiche le 2026-10-08 : « Le Système de Cadastre
   Minier Landfolio du Cameroun a été mis hors service le 3 novembre 2025 ». Aucune plateforme de
   remplacement n'a été trouvée. Même quand il fonctionnait, le portail interdisait toute republication
   ou copie sans autorisation écrite de la Sous-Direction du Cadastre Minier (SDCM) et de Spatial
   Dimension, et ne permettait aucun export en format ouvert (constat du Rapport ITIE 2023). **Fait vérifié.**
2. **La source de titres miniers exploitable aujourd'hui est le Rapport ITIE 2023** (publié en décembre
   2025) et son classeur d'annexes : 261 titres miniers actifs au 31/12/2023 selon le tableau 31 du
   rapport, et un « répertoire minier reconstitué » (annexe 30, 274 lignes lues) **sans coordonnées
   géographiques**. La couche « permis » du livrable ne peut donc pas être un polygone officiel : ce
   sera une couche de **points approximatifs ou de centroïdes géocodés**, signalée comme telle. **Fait
   vérifié** (contenu du rapport) / **Inférence** (conséquence pour la carte).
3. **La base USGS Afrique est utile mais mince et datée pour le Cameroun** : 13 installations (17
   enregistrements, surtout cimenteries et champs gaziers), 9 gisements, 13 sites d'exploration, 1 seul
   port (Douala ; **Kribi absent** de la couche ports), 47 centrales, routes et rails issus
   d'OpenStreetMap extrait le 2020-04-30. Année de référence 2018 pour les installations, mais 2009 et
   2017 pour les gisements. Aucun titre minier. **Fait vérifié** (comptages faits sur `Africa_GIS.gdb`).
4. **Licence USGS à nuancer** : la page USGS affiche CC0, mais la géodatabase intègre des couches
   tierces sous leurs propres conditions : OpenStreetMap (ODbL), GADM (« Redistribution or commercial
   use is not allowed without prior permission ») et African Energy Live Data (republication autorisée
   par l'éditeur). **Fait vérifié.**
5. **Institutions** : la société nationale s'appelle **SONAMINES S.A.** (Société Nationale des Mines),
   créée par le décret n° 2020/749 du 14 décembre 2020. Le nom « SOCAMINES » n'apparaît dans aucune
   source consultée. Le **CAPAM** a cessé ses activités (date prévue : 16 octobre 2021). L'**ITIE**
   a suspendu le Cameroun le 29 février 2024 (Exigence 1.3, engagement de la société civile). **Fait
   vérifié.**
6. **Grands projets, octobre 2026** : aucun projet de fer n'a d'exportation confirmée dans les sources
   consultées. Kribi-Lobé est reporté à juillet 2027. Pour Mbalam, la première exportation était
   annoncée pour le T1 2026 et n'était toujours pas confirmée en avril 2026. Bipindi-Grand Zambi a été
   inauguré le 22/09/2025. Nkout n'a pas de permis d'exploitation. Côté bauxite, la première expédition
   de Minim-Martap via Douala, prévue initialement fin septembre 2026 puis au T4 2026, a été
   **reportée sans nouvelle date** après la suspension des tirages de la facilité AFG Bank le
   24/08/2026 (EcoMatin, 24/08/2026 ; AlCircle, 29/09/2026) ; aucune expédition confirmée au
   2026-10-08. À Nkamouna, le permis de Geovic a été retiré
   (décret 2025/040), Geovic le conteste et l'appel à partenaires de SONAMINES a été déclaré
   infructueux le 18/08/2026. **Fait vérifié** (sources datées en §5).

---

## 2. Corrections au document de cadrage

Le document visé est `docs/AFRICA_MINERAL_INSIGHTS.md` (socle de données, module 03, points ouverts).

| # | Affirmation du cadrage | Constat | Correction proposée | Statut |
|---|---|---|---|---|
| C1 | « Cadastre minier en ligne du MINMIDT (Flexicadastre) … état actuel, couverture et conditions de réutilisation à vérifier » ; « Données : couches USGS Afrique + cadastre minier en ligne » | Le portail (renommé Landfolio) a été **mis hors service le 3 novembre 2025** (message affiché sur `portals.landfolio.com/cameroon/`, qui redirige vers `eu.demo.landfolio.com/MaintenanceCameroon/`). Avant cela, il restait en ligne : captures Internet Archive de 2020 à octobre 2025. | Remplacer « cadastre minier en ligne » par « **Rapport ITIE 2023, annexes 4 et 30 (répertoire des titres au 31/12/2023)** + demande formelle de données à la SDCM/MINMIDT ». | Fait vérifié |
| C2 | (implicite) le cadastre en ligne permettrait d'extraire les titres | Le Rapport ITIE 2023 note l'« impossibilité d'extraire les données sous un format ouvert (Excel/CSV) » et l'absence des autorisations artisanales. L'avertissement du portail interdisait de republier, copier, reproduire ou modifier les données sans autorisation écrite de la SDCM et de Spatial Dimension. | Pour une archive éventuelle du portail : **usage interne seulement**, pas de redistribution dans le livrable. | Fait vérifié |
| C3 | « le cadastre reflète la date d'extraction » | Il n'y a plus d'extraction possible. La seule date de référence disponible est le **31/12/2023** (situation communiquée par la SDCM à l'ITIE). | Afficher « Titres : situation au 31/12/2023 (ITIE 2023, publié déc. 2025) ». | Inférence |
| C4 | USGS : « Année de référence **2018** » pour l'ensemble | Exact pour les installations (champ `DsgAttr06` = 2018) et l'énergie (African Energy 2018). Les **gisements** viennent de sources de 2009 (OFR 2005-1294) et 2017 (PP 1802). L'**exploration** couvre 2004-2018 (WMED). Les **routes et rails** viennent d'OSM au 2020-04-30. | Afficher la date **par couche** (voir §8), pas une date unique « 2018 ». | Fait vérifié |
| C5 | USGS « data release 2021 » | Publication le 2021-08-13 selon ScienceBase, le 2021-08-18 selon la page usgs.gov. DOI 10.5066/P97EQWXP. 24 classes d'entités dans la géodatabase, contre 20 « couches » annoncées sur la page. | Citer le DOI. Signaler l'écart 20/24 (des couches de ressources sont regroupées dans le texte). | Fait vérifié |
| C6 | Points ouverts §4 : « les données USGS sont en principe du domaine public » | La page USGS indique CC0, mais la géodatabase redistribue de l'**OSM (ODbL)**, du **GADM (usage non commercial, pas de redistribution sans permission)** et des données **Cross-border Information** (republication autorisée). | Nuancer : CC0 pour la production USGS ; licences tierces à respecter couche par couche. Pour les limites administratives, préférer une source non-GADM : **Hypothèse** à vérifier. | Fait vérifié |
| C7 | « undiscovered resource tracts … pas une évaluation propre au Cameroun » | Confirmé : 0 entité des couches Gabon, Mauritanie, cuivre, PGE et potasse n'intersecte le Cameroun. Seules 6 zones de charbon (« coal occurrence areas », 2008) l'intersectent. | Aucune correction. Ajouter la mention charbon. | Fait vérifié |
| C8 | (module 03) ports = Douala, Kribi | La couche **ports** USGS ne contient que **Douala** (4 enregistrements de produits). Kribi n'apparaît que via le FLNG *Hilli Episeyo* dans la couche GNL. | Ajouter Kribi depuis une autre source (OSM/Wikipédia/PAK) avec sa date. | Fait vérifié |
| C9 | « rôle de l'organisme public mandaté » (module 04) ; demande de vérifier « SONAMINES / SOCAMINES » | Le nom exact est **SONAMINES S.A.**, créée par le décret 2020/749 du 14/12/2020 (statuts : décret 2020/750). Elle assure l'achat et la commercialisation de l'or et du diamant à titre exclusif. | Utiliser « SONAMINES ». Supprimer « SOCAMINES ». | Fait vérifié |
| C10 | (implicite) CAPAM acteur actuel | Arrêt des activités du CAPAM prévu le 16/10/2021 (décision ministérielle du 05/07/2021). La collecte de l'or au titre de l'ISML est passée à SONAMINES. | Traiter le CAPAM comme une **institution historique**. | Fait vérifié [ancien] |
| C11 | SIGM : « campagne citée : 18 000 échantillons, 300 sites » ; étude AMDC « rapportée en 2025 » | L'article Financial Afrik du 10/07/2025 confirme l'étude AMDC (UA, financements EU-TAF/ZLECAf) et des « données jugées pour la plupart obsolètes ». Il parle d'un SIG « de 1929 à ce jour », mais **ne mentionne ni PRECASEM, ni 18 000 échantillons, ni 300 sites**. | Garder l'étude AMDC. Reprendre la formulation vérifiée des modules 01 (C4) et 02 (C1) : « Programme PRECASEM : campagne géochimique **prévue** d'environ 18 000 échantillons (objectif annoncé en janvier 2017, Business in Cameroon du 28/01/2017) ; 300 "nouveaux sites miniers" annoncés en juin 2019 pour 2014-2019 (Business in Cameroon du 17/06/2019) ; nombre d'échantillons réellement analysés non vérifié ». Les deux chiffres ne relèvent pas d'une même campagne. | Fait vérifié (partiel) ; chiffres vérifiés dans les modules 01 et 02 |

---

## 3. Sources de données

| Source | Contenu utile pour le Cameroun | URL | Accès | Licence / conditions | Date de référence (date de publication) |
|---|---|---|---|---|---|
| USGS — *Compilation of Geospatial Data (GIS) for the Mineral Industries and Related Infrastructure of Africa* (Padilla et al., 2021) | Géodatabase `Africa_GIS.gdb`, 24 classes d'entités. Cameroun : 17 enregistrements d'installations (13 identifiants), 9 gisements, 13 sites d'exploration, 4 enregistrements au port de Douala, 1 terminal GNL, 47 centrales, 445 segments de rail et 6 695 de routes (attribut pays), 94 lignes électriques et 3 pipelines (par intersection) | https://doi.org/10.5066/P97EQWXP ; https://www.sciencebase.gov/catalog/item/607611a9d34e018b3201cbbf | Libre, sans compte. ZIP affiché à 131,74 MB par ScienceBase (≈ 138 Mo en unités décimales) ; données de support 467,21 MB (≈ 490 Mo) | CC0 (page USGS) ; métadonnées « Use constraints: None » ; couches tierces sous ODbL (OSM), GADM (non commercial) et African Energy (republication autorisée) | Installations 2018 ; exploration 2004-2018 ; gisements 2009/2017 ; énergie 2018 ; routes et rails OSM 2020-04-30 (publiée le 2021-08-13 ; métadonnées mises à jour le 2026-01-09) **[ancien]** |
| USGS OFR 2024-1041 (carte GeoPDF) | Représentation partielle : 12 classes d'entités, échelle 1:38 504 000 | https://pubs.usgs.gov/publication/ofr20241041 | Libre | Domaine public USGS (Non vérifié pour la carte elle-même) | Référence 2018 (publiée le 2024-07-02) |
| Portail cadastre Landfolio (ex-Flexicadastre), MINMIDT/SDCM + Spatial Dimension | Avant fermeture : couches « Licences », « Applications », « Administration » ; titre « Cameroon EITI Compliant Mining Cadastre Map Portal » | https://portals.landfolio.com/Cameroon/en/ (aujourd'hui : page de mise hors service) | **Hors service depuis le 2025-11-03** | « Material from this website may not be republished… without prior written permission from both SDCM and Spatial Dimension » | Champ de configuration `DateUpdated` = « 6 October 2016 » (capture Internet Archive du 2025-10-11) |
| Rapport ITIE 2023 — Cameroun (Comité ITIE, administrateur indépendant Enerteam) | Cadre légal ; cadastre (§2.3.2) ; 261 titres actifs au 31/12/2023 ; 11 permis d'exploitation (liste) ; production 2023 (or, diamant, matériaux) ; participations de l'État | https://eiti.org/documents/cameroon-2023-eiti-report (PDF : https://eiti.org/document/25588) | Libre | Non précisé dans le document (Non vérifié) | Exercice 2023 (publié en décembre 2025) |
| Annexes du Rapport ITIE 2023 (XLSX) | Annexe 4 : transactions sur titres 2023 ; annexe 13 : production de carrières par société ; annexe 30 : répertoire minier reconstitué (titulaire, région, nom du permis, arrêté, dates, superficie, substances ; **pas de coordonnées**) ; annexe 34 : bénéficiaires effectifs | https://eiti.org/document/25589 | Libre | Non précisé (Non vérifié) | 31/12/2023 (publiées en décembre 2025) |
| Page pays ITIE (international) | Statut (suspendu), validation 2024 (score 53), liste des rapports | https://eiti.org/countries/cameroon | Libre | — | Consultée le 2026-10-08 |
| Site national ITIE | `eiticameroon.org` redirige vers `itie.cm`, qui renvoie HTTP 503 le 2026-10-08 | http://itie.cm/ | **Indisponible** au test | — | — |
| OpenStreetMap via Geofabrik | Routes, rail, ports, lignes électriques, centrales (complétude variable) | https://download.geofabrik.de/africa/cameroon.html | Libre (PBF 213 Mo, SHP 655 Mo, GPKG 668 Mo) | **ODbL 1.0** (attribution, partage à l'identique des bases dérivées) | Données jusqu'au 2026-10-06T20:21Z |
| GADM 3.6 (inclus dans l'USGS) | Limites administratives ADM0/ADM1 | https://gadm.org/license.html | Libre | « Redistribution or commercial use is not allowed without prior permission » | 2018 (via l'USGS) |
| SONAMINES (site officiel) | Projets publics (Nkamouna, rutile d'Akonolinga), participations (COMINCOR SA, CAMALCO MINING SA), actualités | https://sonamines.cm/ | Libre | Non précisé | Actualités jusqu'au 2026-08-19 |
| Ancien site MINMIDT | Page « Cadastre minier du Cameroun » (organisation, types de titres) | https://www.minmidt.net/fr/secteurs-cibles/secteur-minier/cadastre-minier-du-cameroun.html | Libre | — | Contenu ≈ 2016 (Inférence d'après la dernière actualité datée du 23/09/2016) **[ancien]** |
| Brochure PRECASEM « cadastre » (MINMIDT / Banque mondiale) | Rôle du cadastre informatisé, procédures (Code minier 2016) | https://precasem.cm/wp-content/uploads/2021/03/Plaquette-cadastre-_cimec_mise-a-jour.pdf | Libre | — | PDF créé le 2021-03-09 **[ancien]** |
| Presse économique (Business in Cameroon, EcoMatin, Investir au Cameroun, Afrik.com, Railway Gazette, etc.) | Statuts récents des projets | URL citées en §5 et §12 | Libre (parfois payant) | Droit d'auteur : citer, ne pas reproduire | 2024-2026 |

---

## 4. Institutions du secteur

| Institution | Rôle (sourcé) | Statut / date | Source |
|---|---|---|---|
| **MINMIDT** — Ministère des Mines, de l'Industrie et du Développement Technologique | Tutelle. Instruit les demandes de titres et tient le registre des titres miniers via la **Sous-Direction du Cadastre Minier (SDCM)**, rattachée à la Direction des Mines. Le droit camerounais parle de « conservateur des titres miniers » plutôt que de « cadastre » | Ancien site `minmidt.net` en ligne. `minmidt.gov.cm` injoignable ou en 503 depuis l'environnement de test le 2026-10-08 (non concluant) | minmidt.net (page cadastre, ≈ 2016 **[ancien]**) ; Rapport ITIE 2023, §2.3.2 |
| **SDCM** (au sein du MINMIDT) | Gestion du cadastre et des titres ; instruction des demandes d'octroi et de renouvellement ; titulaire des droits de propriété intellectuelle sur les données du portail | Le portail Landfolio a été arrêté le 2025-11-03 | Rapport ITIE 2023 ; avertissement du portail (capture Internet Archive 2025-10-11) ; page de maintenance Landfolio |
| **SONAMINES S.A.** — Société Nationale des Mines | Créée par le décret n° 2020/749 du 14/12/2020 (statuts : décret 2020/750). Mission : « développer et promouvoir le secteur minier au Cameroun à l'exception des hydrocarbures et des substances de carrières » et gérer les intérêts de l'État. **Exclusivité** de l'achat et de la commercialisation de l'or (et du diamant selon les modalités réglementaires). Capital : 10 Mds FCFA ; l'État est actionnaire unique. Annonce avoir intégré le capital de COMINCOR SA et CAMALCO MINING SA. A repris les sites de Nkamouna-Lomié et du rutile d'Akonolinga | Appels à partenaires déclarés infructueux le 18/08/2026 ; négociations directes ouvertes. Offre de China Eximbank (21/03/2026), projets non précisés | sonamines.cm ; osidimbea.cm ; businessincameroon.com (15/12/2020 **[ancien]** et 21/08/2026) |
| **CAPAM** — programme d'appui à l'artisanat minier, lancé en 2003 | Encadrement de l'artisanat ; collecte de l'or au titre de l'ISML | Mise à l'arrêt des activités prévue le **16/10/2021** (décision du 05/07/2021). Fonctionnaires réaffectés au MINMIDT ; autres agents redéployés à SONAMINES selon les besoins | businessincameroon.com (09/07/2021) **[ancien]**. Développement exact du sigle : **Non vérifié** (les sources diffèrent) |
| **Comité ITIE Cameroun** (présidé par le ministre des Mines) | Rapports ITIE (17 rapports à ce jour selon la presse ; non recoupé) ; le rapport 2023 a été publié en décembre 2025 | **Suspendu** par le Conseil d'administration de l'ITIE (décision 2024-17 du 29/02/2024) pour respect partiel de l'Exigence 1.3. Score 53. Prochaine validation à partir du 01/04/2027. Mesure corrective 13 : rendre publiques les coordonnées de toutes les licences actives | eiti.org/countries/cameroon ; api.eiti.org/fr/board-decision/2024-17 **[ancien, Feb. 2024]** ; eiti.org (rapport 2023) |
| **SNH** — Société Nationale des Hydrocarbures | Hors périmètre minier (hydrocarbures). Fournisseur de gaz potentiel pour Lobé (discussions en cours) | — | ecomatin.net (11/03/2026) |
| **Communes** | Compétentes pour les carrières (exclues du mandat de SONAMINES) | — | businessincameroon.com (15/12/2020) **[ancien]** |

**Données ITIE 2023 utiles pour la carte (Fait vérifié, Rapport ITIE 2023, tableaux 7, 31 et 43) :**
- Production déclarée en 2023 : **952,77 kg d'or** (artisanal), dont **22,31 kg exportés** ; **3 305,78
  carats de diamant**. Pas de production minière industrielle.
- Titres actifs au 31/12/2023 : 149 permis de recherche, 11 permis d'exploitation, 72 permis
  d'exploitation de carrière industrielle et 29 autorisations de carrière d'intérêt public (total 261).
  Le tableau 31 présente aussi des lignes non lisibles dans l'extraction texte ; le total de 261 est
  cité dans le texte du rapport.
- Liste des permis d'exploitation (PEMI) : CIMENCAM (PEMI 00008 Biou Sud, arrêté 2023/128 du
  10/02/2023 ; un second permis, arrêté 2023/129 de la même date, numéro et localisation « non
  précisés » ; PEMI 00002 Figuil, 30/09/2004), G STONES (arrêté 2022/524, 29/11/2022 ; numéroté
  PEMI 00009 dans l'une des deux listes du rapport, « non précisé » dans l'autre), Cameroon Mining
  Company (PEMI 00007 Mbalam, 17/08/2022), Sinosteel Cam (PEMI 00006 Lobé-Kribi, 01/07/2022), C&K
  Mining (PEMI 00005 Mobilong, 16/12/2010), Rocaglia (PEMI 00003 Bidzar et PEMI 00004 Biou Nord,
  31/05/2005), Geovic (PEMI 00001 Lomié, 11/03/2003), et la petite mine CODIAS (n° 000317, 14/09/2022).
- Écart mesuré par la presse (RFI repris par AllAfrica, 19/12/2025) : les pays importateurs déclarent
  15,2 t d'or d'origine camerounaise (environ 90 % aux Émirats arabes unis), contre 22,3 kg d'exports
  officiels.

---

## 5. Inventaire des mines et projets

Colonnes : **Date info** = date de la source la plus récente consultée pour le statut. Coordonnées :
celles de l'USGS quand elles existent (précision variable), sinon « à géocoder ».

| # | Projet / site | Substance | Région | Titulaire (selon source) | Titre (ITIE 2023, annexe 30 / liste PEMI) | Stade | Statut récent | Date info | Sources | Statut |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Mbalam** (côté Cameroun du système Mbalam-Nabeba) | Fer | Est | « Cameroon Mining Company » (ITIE) / « Cameroon Mining Corporation » (BIC), liée au consortium Bestway Finance | PEMI 00007, 17/08/2022, 768,54 km², échéance 2042-08-16 | Construction / pré-production | Exportations annoncées pour le T1 2026, par la route jusqu'à Kribi jusqu'en 2029 (BIC 13/12/2025). Au **7/04/2026, aucune confirmation officielle** d'expédition (Afrik). Le tribunal CCI aurait accordé environ **616 M$** à Sundance/Cam Iron contre le Cameroun (Discovery Alert, 27/07/2026, source secondaire) ; BIC (25/03/2026) attendait une décision fin 2026 | 2026-07-27 | ITIE annexe 30 ; businessincameroon.com (13/12/2025, 25/03/2026) ; afrik.com (07/04/2026) ; discoveryalert.com (27/07/2026) | Fait vérifié (titre, report) ; **Inconnue** (exportation effective) ; sentence arbitrale : **Partiel**, confirmée par Reuters (via Engineering News, 27/07/2026) qui rapporte la déclaration de Sundance ; texte de la sentence non consulté |
| 2 | Nabeba (Congo, transfrontalier) | Fer | Sangha (RC) | Sangha Mining Development (filiale Bestway) | Hors Cameroun | — | Le CCI a rejeté les demandes de Sundance contre le Congo ; recours à Londres (selon le résumé de recherche, non ouvert) | 2026 | afrik.com (07/04/2026) | Fait vérifié (titulaire) ; recours Londres : Non vérifié |
| 3 | **Kribi-Lobé** | Fer (magnétite) | Sud | Sinosteel Cam SA (partenaire JiuJiang) | PEMI 00006, 01/07/2022 (ITIE). BIC (16/09/2024) indique « 1er juillet 2024 » : **discordance** ; EcoMatin (2026) confirme 2022. Superficie : 138 km² (annexe 30) contre 132 km² (EcoMatin) | Construction | **Premières exportations reportées à juillet 2027**. 120 Mds FCFA investis sur environ 420 Mds. Centrale thermique de 42 MW sur site. Ressource de 632,8 Mt à 33 % Fe ; objectif 10 Mt/an de brut, soit environ 4 Mt de concentré | 2026-03-11 | ecomatin.net (11/03/2026) ; ITIE 2023 | Fait vérifié |
| 4 | **Bipindi-Grand Zambi** (permis « Akom II ») | Fer | Sud | G-Stones (Resources), groupe BOCOM | Arrêté 2022/524, 29/11/2022, 498,6 km² (ITIE) | Mine ouverte, pré-exportation | **Inaugurée le 22/09/2025** par le Premier ministre. 600 000 t de minerai stockées au T1 2025 ; objectif de 6 Mt/an de concentré ; réserves d'environ 150 Mt. Exportation prévue par camion vers Kribi. **Aucune exportation confirmée** dans les sources consultées | 2025-09-23 | ecomatin.net (23/09/2025) ; pak.cm (17/01/2025) ; ITIE 2023 | Fait vérifié ; Inconnue (exportation 2026) |
| 5 | **Nkout** (près de Djoum) | Fer | Sud | Caminex (Libyan Foreign Bank) ; consortium mené par Delta Resources (Fomento, KIOCL, VPR Mining) | **Aucun permis d'exploitation** ; convention et permis en attente, dossier « à la Présidence » | Exploration avancée / négociation | Démarrage visé début 2027 ; 1 à 2 Mt/an de minerai à environ 65 % Fe ; transport par camion vers Kribi | 2026-04-06 | ecomatin.net (06/04/2026) ; USGS WMED (« Reserves Development », 2014 **[ancien]**) | Fait vérifié |
| 6 | Ngovayang / « Ngoyang » (près d'Eséka, Bipindi) | Fer | Centre / Sud | CAMINA SA (permis de recherche Ngoyang, Ngoyang II et III, renouvelés le 23/09/2022, échéance 22/09/2024) | Permis de recherche | Exploration | Statut après septembre 2024 : **Inconnu** | 2023-12-31 | ITIE annexe 30 ; USGS WMED (2012) **[ancien]** | Fait vérifié (titre 2022) |
| 7 | Autres permis de recherche de fer (Sud) | Fer | Sud | Prometal Mining, Stone Mining, Biltmore Stones, Perlis, AUCAM, Geocam Mining (« Bipindi Sud »), G-Mining, etc. | 17 lignes « FER » dans l'annexe 30 | Exploration | Statut après 2023 : Inconnu | 2023-12-31 | ITIE annexe 30 | Fait vérifié |
| 8 | **Minim-Martap** | Bauxite | Adamaoua | Camalco Cameroon SA (filiale de Canyon Resources). SONAMINES dit avoir intégré « CAMALCO MINING SA » (lien entre les deux entités : **Non vérifié**) | Permis d'exploitation signé le 02/09/2024 et remis le 13/09/2024 ; convention minière de juillet 2024 | Construction | **1re expédition via le port de Douala prévue initialement fin septembre 2026 (AlCircle, 18/06/2026) puis au T4 2026 (Railway Gazette, 15/07/2026) ; reportée sans nouvelle date après la suspension des tirages de la facilité AFG Bank le 24/08/2026 (EcoMatin, 24/08/2026 ; AlCircle, 29/09/2026)**. Aucune expédition confirmée au 2026-10-08. 7 locomotives CRRC livrées fin juin 2026. Camalco porte sa part dans Camrail de 9,1 % à 26,9 % (mai 2026) | 2026-09-29 | railwaygazette.com (15/07/2026) ; globenewswire.com (11/05/2026) ; businessincameroon.com (16/09/2024) ; sonamines.cm ; ecomatin.net (24/08/2026) ; alcircle.com (18/06/2026 ; 29/09/2026) | Fait vérifié (report : source secondaire, reprise des modules 05, 06 et 07) |
| 9 | Ngaoundal / Makan | Bauxite | Adamaoua | Camalco (permis de recherche) ; MoU SONAMINES/CREC 5 annulé par le ministre | Permis de recherche (extensions de 2022) | Exploration | Non recoupé par une source ouverte | 2022 | Résumé de recherche (alcircle, rapports ASX) : **non ouvert** | **Non vérifié** |
| 10 | Autres bauxites (Fongo-Tongo, Bamboutos, Foumban, Mbouda, Tibati) | Bauxite (Ga) | Ouest / Adamaoua | West Afric Exploration, Highcountry, GM International, Cameroon Golding Wrapper (permis de recherche) | 7 lignes « BAUXITE » dans l'annexe 30 | Exploration | — | 2023-12-31 | ITIE annexe 30 ; USGS gisements (Ga dans bauxite, PP 1802, 2017 **[ancien]**) | Fait vérifié |
| 11 | **Nkamouna-Lomié** | Cobalt-nickel-manganèse | Est | **Litigieux** : permis n° 33 de Geovic (2003) **retiré par le décret n° 2025/040 du 12/02/2025** ; périmètre réattribué à SONAMINES. Geovic conteste (notice du 16/01/2026) | L'annexe 30 au 31/12/2023 liste encore GEOVIC (478 km², échéance 2028) | Relance / contentieux | Appel à partenaires de SONAMINES **infructueux (18/08/2026)** ; négociations directes. Ressources mesurées et indiquées d'environ 121 Mt à 0,23 % Co, 0,65 % Ni, 1,35 % Mn (selon BIC) | 2026-08-21 | businessincameroon.com (21/08/2026, 21/01/2026) ; sonamines.cm | Fait vérifié |
| 12 | Autres Co-Ni (Est) | Co-Ni | Est | Technology Minerals Cameroon, Eramet Exploration (Ngato), Cameroon Mining Corporation (Messok Est) | 8 lignes « COBALT/NICKEL » (annexe 30) | Exploration | Inconnu après 2023 | 2023-12-31 | ITIE annexe 30 | Fait vérifié |
| 13 | **Rutile d'Akonolinga** | Rutile | Centre | SONAMINES (après le retrait d'Eramet) | — | Relance | Appel à partenaires **infructueux (18/08/2026)** ; négociations directes | 2026-08-21 | businessincameroon.com (21/08/2026) ; sonamines.cm | Fait vérifié. Retrait d'Eramet en octobre 2023 : Fait vérifié (businessincameroon.com, 21/08/2026). Chiffres de ressources : non repris ici |
| 14 | Permis de rutile (Centre, Littoral, Sud) | Rutile (± zircon, ilménite) | Centre / Littoral / Sud | Eramet Sanaga Minerals, Eramet Simban Minerals, Nyong Mining, Minta Resources, Heritage Mining, Rhino Resources, BWA Resources, etc. | 50 lignes « RUTILE » dans l'annexe 30 | Exploration | Inconnu après 2023 | 2023-12-31 | ITIE annexe 30 | Fait vérifié |
| 15 | **Colomine** (Ngoura) | Or (petite mine semi-mécanisée) | Est | Codias SA (lien avec COMINCOR selon le tableau 43 de l'ITIE) | Permis petite mine n° 000317, 14/09/2022 | Production | **Environ 54,5 kg d'or entre 02/2023 et 12/2025**, extrapolés des prélèvements de 5 % de SONAMINES | 2026-06-30 | ecomatin.net (30/06/2026) ; ITIE 2023 | Fait vérifié |
| 16 | Mborguéné (Bétaré-Oya / Garoua-Boulaï) | Or | Est | Caminco | Permis petite mine (arrêté du 18/08/2025 selon EcoMatin) | Pré-production | — | 2025 | Résumé de recherche (ecomatin), **non ouvert** ; le tableau 43 de l'ITIE cite « CAMINCO, Code 2023 » | Partiellement vérifié |
| 17 | Orpaillage artisanal et semi-mécanisé | Or | Est, Adamaoua | Artisans ; achat exclusif par SONAMINES | 66 lignes « OR » (permis de recherche) dans l'annexe 30 | Production artisanale | 952,77 kg produits en 2023 ; 22,31 kg exportés | 2025-12 | ITIE 2023 ; AllAfrica/RFI (19/12/2025) | Fait vérifié |
| 18 | **Mobilong** | Diamant | Est | C&K Mining | PEMI 00005, 16/12/2010, 236,25 km², échéance 2035 | Inconnu | Production industrielle : **Non vérifié**. Diamant artisanal 2023 : 3 306 ct | 2023-12-31 | ITIE 2023 ; USGS WMED (« Pre-Production », 2013 **[ancien]**) | Titre : Fait vérifié ; statut : Non vérifié |
| 19 | Figuil / Biou Sud / Biou Nord / Bidzar | Calcaire, marbre, argile (cimenterie) | Nord | CIMENCAM (PEMI 00002, 00008 et arrêté 2023/129) ; Rocaglia (PEMI 00003, 00004) | Permis d'exploitation | Production | Production 2023 (annexe 13) : CIMENCAM 2 099 m³ d'argile ; Rocaglia 1 349 m³ de calcaire et marbre (Nord) | 2023 | ITIE 2023 ; USGS (Figuil, 2018 **[ancien]**) | Fait vérifié |
| 20 | Cimenteries de Douala et Limbé | Ciment, clinker importé, pouzzolane | Littoral, Sud-Ouest | CIMENCAM Bonabéri (1 600 kt/an), Dangote Douala (1 500 kt), CIMAF Bonabéri (500 kt), Medcem Douala (600 kt) ; Dangote Limbé et MIRA (pouzzolane) | — | Production | Capacités de 2018 (USGS) ; capacités 2025 : **Non vérifié** | 2018 / 2023 | USGS MYB 2018 ; ITIE 2023 annexe 13 | Fait vérifié **[ancien]** |
| 21 | Alucam, Edéa | Aluminium (électrolyse) | Littoral | Alucam (État 93,4 % selon l'USGS 2018) | — | Production (sous-utilisée) | *Harmonisation du 2026-10-08 (modules 05, 06 et 07)* : capacité nominale de **100 kt/an** (USGS MYB 2017-18 ; ASI 2024) ; 53 675 t produites en 2025 (Chambre des comptes via Business in Cameroon, 14/07/2026) ; alumine **importée**, aucune raffinerie d'alumine au Cameroun ; importations d'alumine 2023 : 135 347 t, dont 76 655 t de Guinée (UN Comtrade) | 2026-07-14 | USGS 2018 ; modules 05 [S1], [S6], [S12] et 07 [S8] | Fait vérifié (repris des modules 05, 06 et 07) ; part de l'État : **à arbitrer** (93,4 % selon l'USGS 2018 ; autres répartitions dans le module 05) |
| 22 | Lolodorf | Uranium | Sud | Mega Uranium (2007) | — | Exploration (2007) | Inconnu | 2007 | USGS WMED **[ancien]** | Ancien |
| 23 | Les Mamelles (Kribi) | Fer | Sud | — | — | Gisement (OFR 2005-1294) | Inconnu | 2009 | USGS gisements **[ancien]** | Ancien |
| 24 | **Mbe** | Or | Adamaoua (« mainly in the Adamawa Region ») | Oriole Resources 50 % / BCM International 50 % | Licence d'exploration de 312 km² (échéance non publiée) | Exploration avancée | Ressource JORC 2012 **présumée** de 50,60 Mt à 1,02 g/t = 1,66 Moz (coupure 0,40 g/t ; fosse à 3 200 US$/oz) | 2026-09-22 | RNS Oriole 6596V (22/09/2026) ; RNS Oriole (23/07/2026) — modules 02 [S13] et 07 [S28] | Fait vérifié (repris des modules 02 et 07) |
| 25 | **Bibemi** (Bakassi Zone 1) | Or | Nord | Oriole Resources 50 % / BCM International 50 % | Licence de 177 km² ; demande de permis d'exploitation **en cours** au 22/09/2026 ; EIES validée (novembre 2025) | Demande de permis d'exploitation | Ressource JORC 2012 de 6,96 Mt à 2,06 g/t ≈ 460 koz (100 koz indiquées, 360 koz présumées ; fosse à 2 750 US$/oz, mai 2025 ; personne compétente R. Davies). PEA interne de décembre 2025 : ~89 koz in situ à 2,20 g/t, 10 koz/an sur 7 ans, VAN après impôt de 12,8 M US$ à 3 200 US$/oz | 2026-09-22 | RNS Oriole (23/09/2025 ; 22/09/2026) ; Share Talk (16/12/2025) ; Ecofin (21/11/2025) ; EcoMatin (03/04/2025, région) — module 02 [S10], [S11], [S13], [S14] ; module 07 [S28] | Fait vérifié (repris du module 02) |
| 26 | **Wapouzé** | Calcaire / marbre (qualité cimentière) | Adamaoua | Oriole Resources | Licence convertie de l'or au calcaire en 2023, renouvelée pour 2 ans en janvier 2025 (échéance probable vers janvier 2027 : Inférence du module 07) | Exploration (premier forage) | Premier forage terminé (21 trous, 1 053,8 m), annoncé le 22/07/2026 ; > 50 % CaO selon un pXRF préliminaire ; première estimation de ressource attendue fin T3 2026, **non trouvée** au 2026-10-08 | 2026-07-22 | RNS Oriole « Completion of Maiden Drilling at Wapouzé » — module 07 [S34] | Fait vérifié (repris du module 07) |
| 27 | **Kambélé** (Batouri) | Or | Est | Zone réservée aux artisans ; sondages historiques d'African Aura Resources (article non daté) | **Arrêté du 13/08/2025 interdisant l'exploitation industrielle** | Artisanal | Aucune ressource conforme trouvée ; site fermé depuis neuf mois selon un article de 2025 | 2025-08-13 | EcoMatin (Kambélé) — module 07 [S39] ; Northern Miner, Cameroun24 — module 02 [S15], [S16] | Fait vérifié (arrêté, repris du module 07) ; opérateur industriel actuel : Inconnue |

**Contrôles qualité USGS à faire faire aux participants (Fait vérifié, extraits de la géodatabase) :**
- **Nkamouna** a des coordonnées incompatibles entre deux couches : gisements (3,266 N ; 13,813 E) et
  exploration (2,533 N ; 14,817 E), soit environ 138 km d'écart (Inférence : calcul géodésique
  approché).
- Pour **Mbalam** (couche exploration), le champ `MemoLoc` indique « Sangha, Rep. of the Congo ; 35 km SW
  of Souanke » alors que le pays saisi est Cameroon / Est. Les deux gisements sont mélangés.
- Les installations « Mine in East Region and various other locations » (diamant) et « Mine in North
  Region… » (or) sont des **points symboliques** (« Location provided is for one mine in the specified
  area »). Il ne faut pas les cartographier comme des mines réelles.
- Le FLNG de Kribi est typé « Refinery » dans la couche GNL.

---

## 6. Infrastructures

### 6.1 Ports
| Élément | Faits | Source (date) | Statut |
|---|---|---|---|
| Port de Douala (PAD) | Seul port camerounais de la couche USGS : produits aluminium, clinker, GPL et bitume, soude caustique ; propriétaire « Office National des Ports du Cameroun » (attribut de 2019, aujourd'hui `pad.cm`) | USGS (WPI 2019) **[ancien]** ; redirection observée vers https://www.pad.cm/ (2026-10-08) | Fait vérifié |
| Port de Douala, bauxite | Port d'exportation prévu pour la bauxite de Minim-Martap ; terrassements en cours | railwaygazette.com (15/07/2026) ; globenewswire (11/05/2026) | Fait vérifié |
| Port en eau profonde de Kribi (Mboro, environ 35 km au sud de Kribi ; 2,719 N, 9,864 E) | Premiers navires en 2014 ; absent de la couche ports USGS | en.wikipedia.org/wiki/Kribi_Deepwater_Port (source tertiaire) | Fait vérifié (faible) |
| Terminal minéralier de Kribi | Première pierre posée le **22/09/2025**, confié à Sinosteel Cameroun SA ; 14 Mt/an au départ, 47,5 Mt/an à long terme | ecomatin.net (23/09/2025) | Fait vérifié |
| Jetée minéralière de Lolabé | Prévue comme installation dédiée de long terme pour Mbalam | businessincameroon.com (13/12/2025) | Fait vérifié (projet) |
| Kribi FLNG *Hilli Episeyo* | Liquéfaction, 2,4 (Mt/an selon l'IGU 2019), actif en 2018 | USGS GNL **[ancien]** | Ancien |

### 6.2 Chemin de fer
| Élément | Faits | Source (date) | Statut |
|---|---|---|---|
| Réseau Camrail | Voie métrique (1 000 mm) d'environ 1 000 km (l'infobox et le texte divergent : 1 104 km en 1995) ; lignes Douala-Yaoundé, Yaoundé-Ngaoundéré (Transcamerounais), Douala-Kumba ; concession de 1999 ; voie appartenant à l'État, matériel roulant à Camrail | en.wikipedia.org/wiki/Camrail (tertiaire) **[ancien]** | Faible. Actionnariat actuel : **Non vérifié** |
| Camalco / Camrail | Camalco porte sa participation de 9,1 % à 26,9 % (CFA 9,852 Mds, mai 2026) ; flotte initiale de 7 locomotives et 160 wagons ; environ 35 000 t humides/mois en phase 1 | railwaygazette.com (15/07/2026) ; résumé alcircle (capacité, non ouvert) | Fait vérifié (participation ; capacité de 35 000 t/mois confirmée dans Railway Gazette lors de la contre-vérification) |
| Chemin de fer Mbalam-Kribi | Contrat de PPP sur 50 ans entre l'État et le consortium Bestway/AustSino ; voie « à double sens » (formulation de la source ; double voie non établie) de **540 km côté Cameroun** et 149 km côté Congo ; contrat paraphé le 25/02/2022 ; 1re session du comité de suivi le **10/07/2025** ; conditions suspensives encore à lever | bougna.net (14/07/2025) | Fait vérifié. Début des travaux : **Inconnu** |
| Rail USGS | 445 segments au Cameroun, issus d'OSM au 2020-04-30 | USGS **[ancien]** | Fait vérifié |

### 6.3 Énergie
| Élément | Faits | Source (date) | Statut |
|---|---|---|---|
| Centrales USGS (2018) | 47 enregistrements « Cameroon » : Song Loulou 384 MW, Edéa 276 MW, Kribi Gas 216 MW, Dibamba 88 MW (fioul lourd), Limbé 85 MW, Lagdo 72 MW, etc. Propriétaires de 2018 : Eneo (État 44 %, Actis 56 %), Globeleq, EDC | USGS / African Energy Live Data 2018 **[ancien]** | Fait vérifié (2018) |
| Nachtigal (Sanaga) | 420 MW au fil de l'eau (7 × 60 MW) ; 1er groupe le 10/05/2024 ; dernier groupe le **18/03/2025** ; NHPC (EDF 40 %, IFC 20 %, État 15 %, Africa50 15 %, Stoa 10 %) ; 4,351 N, 11,633 E | en.wikipedia.org (tertiaire) | Fait vérifié (faible) ; **absent de l'USGS** |
| Memve'ele (Ntem) | 211 MW ; premiers 80 MW en avril 2019 ; achèvement lié à la ligne 225 kV vers Yaoundé (date « attendue » de décembre 2022) ; État / EDC ; 2,396 N, 10,399 E | en.wikipedia.org (tertiaire) | Fait vérifié (faible) ; mise en service complète : **Non vérifié** |
| Lom Pangar | Page Wikipédia introuvable (404) ; pas d'autre source consultée | — | **Non vérifié** |
| Centrale captive de Lobé | 42 MW thermique ; discussions avec la SNH pour du gaz | ecomatin.net (11/03/2026) | Fait vérifié |
| Lignes de transport (USGS) | 94 segments intersectant le Cameroun (African Energy 2018) | USGS **[ancien]** | Fait vérifié |
| Gaz | Champs de Logbaba et Matanda (Gaz du Cameroun), Sanaga, Yoyo (2018) ; 3 pipelines intersectant le pays | USGS **[ancien]** | Fait vérifié |

### 6.4 Routes
| Élément | Faits | Source | Statut |
|---|---|---|---|
| Routes USGS | 6 695 segments « Cameroon » (OSM au 2020-04-30) : tronc 1 716, primaire 1 632, secondaire 2 884 (+ bretelles) | USGS **[ancien]** | Fait vérifié |
| OSM à jour | Extrait Geofabrik avec données jusqu'au 2026-10-06 (ODbL) | download.geofabrik.de | Fait vérifié |
| Transport minier par route | Mbalam vers Kribi par camions jusqu'en 2029 ; Grand Zambi vers Kribi par camion (plus de 50 km) ; Nkout vers Kribi par camion | BIC (13/12/2025) ; EcoMatin (23/09/2025 ; 06/04/2026) | Fait vérifié (plans annoncés) |

### 6.5 Sources recommandées pour les couches SIG d'infrastructure
- **OSM (Geofabrik GPKG)** : routes (`highway` trunk/primary/secondary), rail (`railway=rail`), ports
  (`landuse=port`, `harbour`), lignes (`power=line`) et centrales (`power=plant`), avec la date
  d'extraction affichée. Licence ODbL : attribution « © OpenStreetMap contributors ».
- **USGS** : couche de référence 2018, pour comparer 2018 et l'extraction OSM de 2026 et montrer ce qui
  a changé (Nachtigal, Memve'ele, terminal de Kribi). **Hypothèse pédagogique.**
- Points ajoutés à la main (Nachtigal, terminal minéralier de Kribi, jetée de Lolabé, terminal
  ferroviaire de Camalco) : chaque point porte sa source et sa date dans les attributs.

---

## 7. Déroulé de l'étude de cas (QGIS)

Durée indicative : 1 journée (6 h). Logiciel : QGIS 3.x LTR. Système de coordonnées : stockage en
WGS 84 (EPSG:4326), calcul des distances en WGS 84 / UTM 33N (EPSG:32633), conformément à la
convention commune aux modules 01, 02 et 03 (voir « Zone et projection communes » ci-dessous ; l'UTM 32N
initialement proposé est abandonné). Stockage dans un GeoPackage unique, `cmr_ecosystem_YYYYMMDD.gpkg`.

| Étape | Action | Données | Résultat attendu |
|---|---|---|---|
| 0. Cadrage (20 min) | Présenter les 6 constats du §1, en particulier la fermeture du cadastre et ses conséquences | Ce document | Les participants savent quelles données sont officielles, datées ou manquantes |
| 1. Import USGS (40 min) | Ouvrir `Africa_GIS.gdb` et filtrer `"Country" = 'Cameroon'` pour les couches qui ont ce champ. Pour les autres (lignes électriques, pipelines, charbon), faire une sélection par intersection avec ADM0 Cameroon | USGS 2021 | 10 couches nettoyées ; table des effectifs à comparer au §3 |
| 2. Audit qualité USGS (40 min) | Repérer les incohérences du §5 (Nkamouna, Mbalam, points symboliques, typage du FLNG). Créer un champ `qc_flag` | USGS | Liste d'anomalies documentée (exercice d'esprit critique) |
| 3. Titres miniers (60 min) | Importer l'annexe 30 de l'ITIE (XLSX) et normaliser titulaire, type, substance et dates. Géocoder **le nom du permis ou de la localité** (OSM Nominatim ou GeoNames) pour créer des **points approximatifs** avec `loc_precision = "localité"`. Ajouter les 11 permis d'exploitation de la liste ITIE | ITIE 2023 (situation au 31/12/2023) | Couche `titres_2023_pts`, explicitement **non cadastrale** |
| 4. Projets (45 min) | Créer la couche `projets_2026` à partir du tableau du §5 (y compris Mbe, Bibemi, Wapouzé et Kambélé, lignes 24 à 27, reprises des modules 02 et 07) : stade, statut, date de l'information, URL de la source, statut de vérification | §5 | 15 à 20 points |
| 5. Infrastructures (60 min) | Extraire d'OSM (Geofabrik) les routes principales, le rail, les ports, les lignes et les centrales. Ajouter les points manuels (Nachtigal, terminal de Kribi, Lolabé) et le tracé **projeté** Mbalam-Kribi en pointillés, avec `statut = "projet"` | OSM 2026-10 ; §6 | Couches d'infrastructure datées |
| 6. Analyse de proximité (45 min) | Pour chaque projet : distance au port d'export le plus proche, à la voie ferrée, à la ligne électrique et à la centrale, avec l'outil « Distance au plus proche (hub) » | Couches des étapes 4 et 5 | Table `projets_access` (km) pour le module 07 |
| 7. Mise en page (40 min) | Mise en page A3 avec un cartouche « Source — date » **par couche**, un encadré « Limites » (cadastre fermé, USGS 2018, points approximatifs) et les crédits de licence (OSM ODbL, USGS CC0, GADM non commercial ou remplacé) | — | `Cameroon_Mining_Ecosystem_Map.pdf` |
| 8. Restitution (30 min) | Chaque groupe présente 3 constats et 3 inconnues | — | Alimente les §9 et §11 |

**Jeu de données de secours** (exigé par le cadrage) : un GeoPackage préparé par l'équipe pédagogique
avec les couches des étapes 1 à 5 déjà construites. **Hypothèse** : à produire avant la session.

### Zone et projection communes (modules 01, 02 et 03) [H : proposition d'harmonisation du 2026-10-08]

La carte de l'écosystème importe les couches des modules 01 (occurrences, cibles) et 02 (polygones de prospectivité) : elle doit utiliser le même SCR et la même emprise de zoom. Proposition commune, identique dans les trois modules :

| Élément | Proposition commune | Justification |
|---|---|---|
| SCR d'échange et de stockage | WGS 84 géographique (**EPSG:4326**) | Système des sources (USGS, OSM, coordonnées des RNS) ; déjà retenu pour l'échange par le module 02 (§ 8) |
| SCR de calcul (distances, surfaces, rasters, densités) | **WGS 84 / UTM 33N (EPSG:32633)**, pour les trois modules | Les trois zones du module 01 (13,85° à 14,55° E, § 4 du module 01) sont entièrement dans le fuseau UTM 33 (12° à 18° E) ; le module 01 l'utilise déjà. Un SCR de calcul unique évite des reprojections entre livrables et des écarts de surface d'un module à l'autre [I] |
| Projets et ports à l'ouest de 12° E (fuseau 32 : Kribi, Douala) | Garder EPSG:32633 pour les distances du module 03 (étape 6) | Le port en eau profonde de Kribi (9,864° E, module 03 § 6.1) est à environ 5,1° du méridien central de 15° E : facteur d'échelle d'environ 1,0036, soit une erreur d'environ 0,4 % sur une distance, négligeable pour des distances au port exprimées en km [I : calcul k ≈ 0,9996 × (1 + (Δλ·cos φ)²/2)]. L'UTM 32N (EPSG:32632) n'est plus utilisé |
| Emprise nationale | Limite ADM0 du Cameroun (couche `adm0_adm1` du module 03) | Échelle de la carte nationale du module 02 (1 km) et de la carte de l'écosystème du module 03 |
| District commun (zoom) | **Z2 Bétaré-Oya : 13,85–14,35° E ; 5,40–5,85° N** (emprise du module 01, § 4) | Seule zone commune aux modules 01 (Z2, « recommandée en second ») et 02 (district « Bétaré-Oya / Lom », littérature la plus dense). Le module 03 y rattache Mborguéné (« Bétaré-Oya / Garoua-Boulaï ») ; son inclusion dans l'emprise reste à vérifier au géocodage [?]. Z1 Tcholliré reste la zone principale de l'exercice spectral du module 01 ; Mbe (Adamaoua) et Bibemi (Nord) restent hors district et servent à la rétro-prédiction nationale du module 02 |
| Résolution de référence | National : 1 km ; district : 100 m (module 02 § 8) ; produits Sentinel-2 : 10-20 m (module 01) | Les rasters du module 01 sont rééchantillonnés à 100 m avant d'entrer dans le modèle de district du module 02 [H] |

---

## 8. Spécification du livrable — *Cameroon Mining Ecosystem Map*

**Format** : GeoPackage, projet QGIS (`.qgz`), PDF A3 et tableau CSV des projets.
**Règle** : chaque couche porte dans ses métadonnées et sur la carte : `source`, `url`, `date_reference`,
`date_extraction`, `licence`, `precision`.

| Couche | Géométrie | Source | Date de référence | Date d'extraction | Licence | Champs obligatoires |
|---|---|---|---|---|---|---|
| `adm0_adm1` | Polygone | USGS (GADM 3.6) ; **ou** autre source à licence ouverte (Hypothèse : geoBoundaries, non vérifiée) | 2018 | 2026-10-08 | GADM : non commercial / à remplacer | nom, code |
| `usgs_installations` | Point | USGS MYB 2018 | 2018 | 2026-10-08 | CC0 | uid, nom, type, substance, exploitant, capacité, `qc_flag` |
| `usgs_gisements` | Point | USGS (OFR 2005-1294 ; PP 1802) | 2009 / 2017 | 2026-10-08 | CC0 | nom, substance, type de gîte |
| `usgs_exploration` | Point | USGS WMED | 2004-2018 | 2026-10-08 | CC0 | nom, stade, année |
| `titres_2023_pts` | Point (approximatif) | ITIE 2023, annexe 30 + liste PEMI | **31/12/2023** | 2026-10-08 | Non précisée (Non vérifié) | titulaire, type, substance, n° d'arrêté, date d'attribution, date de fin, superficie, `loc_precision` |
| `projets_2026` | Point | §5 (presse, sites officiels, ITIE) | Variable, par ligne | 2026-10-08 | Faits seulement (pas de reproduction de texte) | projet, substance, titulaire, stade, statut, `date_info`, `source_url`, `statut_verif` |
| `ports` | Point | OSM + USGS + ajouts manuels | 2026-10-06 (OSM) / 2019 (USGS WPI) | 2026-10-08 | ODbL / CC0 | nom, type, vrac minéral (o/n), statut |
| `rail_existant` | Ligne | OSM | 2026-10-06 | 2026-10-08 | ODbL | nom, opérateur, écartement |
| `rail_projete` | Ligne (schématique) | Tracé indicatif (bougna.net 2025 ; BIC 2025) | 2025 | 2026-10-08 | — | nom, longueur annoncée, statut = « projet » |
| `routes_principales` | Ligne | OSM | 2026-10-06 | 2026-10-08 | ODbL | classe, réf. |
| `centrales` | Point | OSM + USGS 2018 + ajouts (Nachtigal) | 2026 / 2018 | 2026-10-08 | ODbL / CC0 | nom, type, MW, mise en service, source |
| `lignes_electriques` | Ligne | OSM (USGS 2018 en comparaison) | 2026-10-06 | 2026-10-08 | ODbL | tension |
| `charbon_usgs` | Polygone | USGS (2008) | 2008 | 2026-10-08 | CC0 | — |

**Mentions obligatoires sur la carte** :
- « Titres miniers : situation au 31/12/2023 (Rapport ITIE 2023, publié en décembre 2025). Points
  approximatifs, non issus du cadastre officiel. Le portail cadastral du MINMIDT est hors service
  depuis le 03/11/2025. »
- « Installations USGS : année de référence 2018. »
- « © OpenStreetMap contributors, ODbL. »

---

## 9. Sorties vers les autres modules

| Module | Sortie du module 03 | Contenu | Statut des données |
|---|---|---|---|
| **04 — Legal & Regulatory** | `titres_2023` (table) + tableau des participations de l'État | Pour chaque permis : régime applicable (Code 2001, 2016 ou 2023, d'après le tableau 43 de l'ITIE), participation attendue (10 % gratuite selon le Code 2016) et participation déclarée (« NC » = écart) ; cas litigieux : Nkamouna (retrait par décret contre notice de Geovic), Mbalam (arbitrage CCI) ; pas de publication des coordonnées des licences (mesure corrective 13 de l'ITIE) | Fait vérifié (situation 2023) |
| **05 — Value Chains** | `projets_2026` + `usgs_installations` + infrastructures | Chaîne de la bauxite : Minim-Martap → rail Camrail → Douala (export) ; smelter Alucam d'Edéa (2018, statut actuel non vérifié). Projet d'alumine annoncé pour 2027 (BIC 16/09/2024, déclaration de l'entreprise : **Non vérifié** depuis). Fer : concentrés de Lobé, Grand Zambi et Mbalam → Kribi ; complexe sidérurgique de Kribi (Cameroon Steel, mentionné par bougna.net 2025 : **Non vérifié** autrement) ; ciment : clinker importé via Douala (USGS 2018) | Mixte |
| **07 — Investment Pipeline** | `projets_access` (distances) + stade + statut + date | Pour le score : stade (titre, construction, production), accès aux infrastructures (km), risque juridique (contentieux), date de l'information. Premier tri possible : Minim-Martap (titre, rail en cours) ; Lobé (titre, export 2027) ; Grand Zambi (inauguré, export non confirmé) ; Mbalam (titre, arbitrage) ; Nkout (pas de titre) ; Nkamouna et Akonolinga (pas de partenaire) | Inférence (classement indicatif, à scorer en 07) |
| 01/02 (retour) | Gisements et exploration USGS ; permis de recherche d'or (66) et de rutile (50) | Validation des cibles et contrôle « occurrence contre titre » | Fait vérifié |

---

## 10. Tableau de vérification

| Affirmation | Source | Statut |
|---|---|---|
| La base USGS Afrique a été publiée en 2021 (DOI 10.5066/P97EQWXP), sous licence CC0 | usgs.gov (page data release) ; ScienceBase JSON | Fait vérifié |
| L'année de référence des installations USGS est 2018 | `DsgAttr06` = 2018 ; OFR 2024-1041 | Fait vérifié |
| Les gisements USGS datent de 2009 et 2017 ; les routes et rails d'OSM au 2020-04-30 | Métadonnées FGDC `Africa_GIS_Metadata.xml` | Fait vérifié |
| L'USGS compte 17 enregistrements d'installations (13 identifiants), 9 gisements, 13 sites d'exploration, 1 port et 47 centrales au Cameroun | Comptage sur `Africa_GIS.gdb` | Fait vérifié |
| Kribi est absent de la couche ports USGS | Comptage sur `Africa_GIS.gdb` | Fait vérifié |
| La géodatabase USGS contient des couches OSM (ODbL) et GADM (non commercial) | Métadonnées FGDC ; gadm.org/license.html | Fait vérifié |
| Les « undiscovered tracts » ne concernent pas le Cameroun | Intersection : 0 entité | Fait vérifié |
| Flexicadastre a été annoncé comme opérationnel pour juillet 2017 | cameroon-tribune.cm (02/06/2017) | Fait vérifié [ancien] |
| Le portail cadastral Landfolio du Cameroun a été mis hors service le 03/11/2025 | portals.landfolio.com/cameroon (page de maintenance) | Fait vérifié |
| Le portail interdisait la republication sans autorisation écrite | Avertissement du portail (capture Internet Archive du 2025-10-11) | Fait vérifié |
| Le cadastre en ligne ne permettait pas d'export ouvert ni n'incluait les autorisations artisanales | Rapport ITIE 2023, §2.3.2 | Fait vérifié |
| Un portail cadastral a remplacé Landfolio | — | **Inconnue** |
| 261 titres miniers étaient actifs au 31/12/2023 | Rapport ITIE 2023, tableau 31 | Fait vérifié |
| Production 2023 : 952,77 kg d'or, 22,31 kg exportés, 3 305,78 ct de diamant | Rapport ITIE 2023, tableau 7 | Fait vérifié |
| La société nationale s'appelle SONAMINES, créée par le décret 2020/749 du 14/12/2020 | sonamines.cm ; prc.cm ; osidimbea.cm | Fait vérifié |
| Le nom « SOCAMINES » existe | Aucune source | Non vérifié (probablement erroné) |
| Le CAPAM a cessé ses activités (prévu le 16/10/2021) | businessincameroon.com (09/07/2021) | Fait vérifié [ancien] |
| Le Cameroun est suspendu de l'ITIE depuis le 29/02/2024 (Exigence 1.3) | eiti.org ; décision 2024-17 | Fait vérifié |
| Le Rapport ITIE 2023 a été publié en décembre 2025 | eiti.org (page du document) ; AllAfrica (19/12/2025) | Fait vérifié |
| Le site national ITIE (itie.cm) est accessible | Test HTTP du 2026-10-08 : 503 | Non vérifié (indisponible) |
| Mbalam : PEMI 00007 du 17/08/2022 attribué à Cameroon Mining Company | ITIE 2023 | Fait vérifié |
| Mbalam a déjà exporté | Afrik (07/04/2026) : aucune confirmation | **Inconnue** |
| Sentence CCI d'environ 616 M$ en faveur de Sundance contre le Cameroun | discoveryalert.com (27/07/2026) ; Reuters via engineeringnews.co.za (27/07/2026), d'après la déclaration de Sundance | Partiel (déclaration de la société, recoupée par Reuters ; sentence non consultée) |
| Les exportations de Kribi-Lobé sont reportées à juillet 2027 | ecomatin.net (11/03/2026) | Fait vérifié |
| Le permis de Lobé date du 01/07/2022 (et non de 2024) | ITIE 2023 ; EcoMatin (2026) contre BIC (2024) | Fait vérifié (discordance signalée) |
| Grand Zambi a été inauguré le 22/09/2025 | ecomatin.net (23/09/2025) | Fait vérifié |
| Nkout n'a pas de permis d'exploitation (avril 2026) | ecomatin.net (06/04/2026) | Fait vérifié |
| Minim-Martap : permis signé le 02/09/2024 ; 1re expédition prévue initialement fin septembre / T4 2026 via Douala, reportée sans nouvelle date après la suspension des tirages AFG Bank le 24/08/2026 | BIC (16/09/2024) ; AlCircle (18/06/2026) ; Railway Gazette (15/07/2026) ; EcoMatin (24/08/2026) ; AlCircle (29/09/2026) | Fait vérifié (report : source secondaire) |
| Le permis de Nkamouna a été retiré par le décret 2025/040 du 12/02/2025 ; Geovic conteste | BIC (21/08/2026 ; 21/01/2026) | Fait vérifié |
| Appels SONAMINES pour Nkamouna et Akonolinga infructueux le 18/08/2026 | BIC (21/08/2026) | Fait vérifié |
| Colomine : environ 54,5 kg d'or entre 2023 et 2025 | ecomatin.net (30/06/2026) | Fait vérifié |
| Statut actuel de Mobilong (C&K Mining) | — | Non vérifié |
| Nachtigal (420 MW) entièrement en service le 18/03/2025 | Wikipédia (tertiaire) | Fait vérifié (faible) |
| PPP ferroviaire Mbalam-Kribi : 540 km côté Cameroun, comité installé le 10/07/2025 | bougna.net (14/07/2025) | Fait vérifié |
| Première pierre du terminal minéralier de Kribi (Sinosteel) le 22/09/2025 | ecomatin.net (23/09/2025) | Fait vérifié |
| PRECASEM : 18 000 échantillons = objectif annoncé en janvier 2017 ; 300 nouveaux sites = bilan 2014-2019 annoncé en juin 2019 (chiffres absents de Financial Afrik du 10/07/2025) | Business in Cameroon (28/01/2017 ; 17/06/2019), vérifiés dans les modules 01 et 02 | Fait vérifié (annonces) ; échantillons réellement analysés : Non vérifié |
| Étude AMDC : données du « système d'information géologique et minérale » « pour la plupart obsolètes » (l'article ne nomme pas le SIGM) | financialafrik.com (10/07/2025) | Fait vérifié (attribution au SIGM : non établie) |

---

## 11. Inconnues

1. **Le système cadastral qui a remplacé Landfolio après le 03/11/2025** : nouveau logiciel, accès
   public ou non. Action : demande écrite à la SDCM/MINMIDT.
2. **Les polygones officiels des titres** : aucune source ouverte ne publie les coordonnées. L'ITIE
   l'exige (mesure corrective 13).
3. Les titres attribués, renouvelés ou expirés **après le 31/12/2023** : nombreux permis de recherche
   arrivés à échéance en 2024-2026 (annexe 30).
4. La **première exportation effective** de Mbalam et de Grand Zambi (2026).
5. La sentence CCI Sundance contre le Cameroun : à confirmer dans le texte primaire (annonce ASX de
   Sundance).
6. Le lien juridique entre « Camalco Cameroon SA » (Canyon) et « CAMALCO MINING SA » (participation
   SONAMINES).
7. Le statut actuel de Mobilong (diamant), l'état des cuves d'Alucam (Edéa ; capacité et production : module 05), des capacités cimentières 2025 et de
   l'actionnariat de Camrail (non recherchés faute de quota).
8. Lom Pangar et Memve'ele : capacité et date de mise en service complète, à documenter par une source
   primaire (EDC, Eneo).
9. Le statut juridique final de Nkamouna (contentieux Geovic, éventuel nouveau permis).
10. La licence de réutilisation des données ITIE (rapport et annexes) : non précisée dans les
    documents consultés.
11. La disponibilité du site national ITIE (`itie.cm`, HTTP 503 le 2026-10-08) et du site
    `minmidt.gov.cm`. Ces tests depuis un environnement proxy ne sont pas concluants.

---

## 12. Sources

Toutes consultées le **2026-10-08** ; la date entre parenthèses est la date de publication.

**Données et documents officiels**
- USGS, Padilla et al. (2021-08-13/18), *Compilation of Geospatial Data (GIS) for the Mineral Industries and Related Infrastructure of Africa*, DOI : https://doi.org/10.5066/P97EQWXP — page : https://www.usgs.gov/data/compilation-geospatial-data-gis-mineral-industries-and-related-infrastructure-africa — ScienceBase : https://www.sciencebase.gov/catalog/item/607611a9d34e018b3201cbbf (fichiers `Africa_GIS.gdb.zip` et `Africa_GIS_Metadata.xml` téléchargés et analysés)
- USGS, Neustaedter et al. (2024-07-02), OFR 2024-1041 : https://pubs.usgs.gov/publication/ofr20241041/full
- Landfolio, page de mise hors service du portail du Cameroun : https://portals.landfolio.com/cameroon/ → https://eu.demo.landfolio.com/MaintenanceCameroon/
- Internet Archive, capture du portail du 2025-10-11 : https://web.archive.org/web/20251011124601/https://portals.landfolio.com/Cameroon/en/ (récupérée par curl ; avertissement et configuration lus)
- Comité ITIE Cameroun (décembre 2025), *Rapport ITIE 2023* : https://eiti.org/documents/cameroon-2023-eiti-report — PDF : https://eiti.org/document/25588 — Annexes XLSX : https://eiti.org/document/25589
- EITI, page pays Cameroun : https://eiti.org/countries/cameroon
- EITI, décision du Conseil 2024-17 (2024-02-29) : https://api.eiti.org/fr/board-decision/2024-17
- MINMIDT (ancien site, ≈ 2016), page cadastre minier : https://www.minmidt.net/fr/secteurs-cibles/secteur-minier/cadastre-minier-du-cameroun.html
- PRECASEM/MINMIDT (2021-03-09), brochure cadastre : https://precasem.cm/wp-content/uploads/2021/03/Plaquette-cadastre-_cimec_mise-a-jour.pdf
- SONAMINES, site officiel : https://sonamines.cm/
- Présidence de la République, décret 2020/749 (résumé) : https://prc.cm/en/news/the-acts/decrees/4784-decree-no-2020-749-of-14-december-2020-to-set-up-the-national-mining-corporation-2
- Osidimbea (fiche SONAMINES) : https://www.osidimbea.cm/entreprises/a-capitaux-publics/sonamines/
- Geofabrik, extrait OSM du Cameroun : https://download.geofabrik.de/africa/cameroon.html
- GADM, licence : https://gadm.org/license.html

**Presse et sources secondaires**
- Cameroon Tribune (2017-06-02), Flexicadastre : https://www.cameroon-tribune.cm/article.html/9048/en.html/details_2
- Business in Cameroon (2020-12-15), création de SONAMINES : https://www.businessincameroon.com/mining/1512-11136-cameroon-establishes-sonamines-a-national-mining-company
- Business in Cameroon (2021-07-09), arrêt du CAPAM : https://www.businessincameroon.com/mining/0907-11757-cameroon-government-program-capam-to-soon-cease-operations
- Business in Cameroon (2024-09-16), permis de Minim-Martap : https://www.businessincameroon.com/mining/1609-14144-cameroon-grants-4th-solid-mining-permit-to-canyon-resources
- Business in Cameroon (2025-12-13), report des exportations de Mbalam : https://www.businessincameroon.com/public-management/1312-15495-mbalam-iron-ore-mine-delays-first-exports-to-early-2026
- Business in Cameroon (2026-01-21), contestation de Geovic : https://www.businessincameroon.com/mining/2101-15632-geovic-disputes-loss-of-nkamouna-permit-warns-cameroon-of-arbitration
- Business in Cameroon (2026-03-25), arbitrage Mbalam : https://www.businessincameroon.com/mining/2503-15932-mbalam-iron-dispute-drags-on-as-arbitration-ruling-delayed-to-2026
- Business in Cameroon (2026-08-21), Nkamouna et Akonolinga : https://www.businessincameroon.com/mining/2108-16603-sonamines-opens-talks-on-nkamouna-akonolinga-after-two-failed-tenders
- Afrik.com (2026-04-07), Mbalam-Nabeba : https://www.afrik.com/mbalam-nabeba-production-de-fer-lancee-exportations-retardees-en-2026-au-cameroun-congo
- Discovery Alert (2026-07-27), sentence Sundance : https://discoveryalert.com/sundance-cameroon-arbitration-african-mining-iron-ore-2026/
- EcoMatin (2025-09-23), inauguration de Grand Zambi : https://ecomatin.net/grand-zambi-le-cameroun-inaugure-sa-premiere-mine-de-fer-valorisee-a-333-milliards
- EcoMatin (2026-03-11), Kribi-Lobé reporté à 2027 : https://ecomatin.net/cameroun-sinosteel-reporte-les-exportations-du-fer-de-kribi-lobe-a-2027-malgre-120-milliards-fcfa-deja-investis
- EcoMatin (2026-04-06), Nkout : https://ecomatin.net/cameroun-pres-de-120-milliards-fcfa-pour-lancer-lexploitation-du-fer-de-nkout-des-2027
- EcoMatin (2026-06-30), Colomine : https://ecomatin.net/cameroun-54-kg-dor-extraits-a-colomine-en-trois-ans-loin-des-objectifs-initiaux
- Port Autonome de Kribi (2025-01-17), Grand Zambi : https://pak.cm/en/grand-zambi-iron-from-bipindi-driving-the-growth-of-the-port-of-kribi/
- GlobeNewswire / Canyon Resources (2026-05-11), point d'avancement de Minim-Martap : https://www.globenewswire.com/news-release/2026/05/11/3291534/0/en/Minim-Martap-Project-Development-Update.html
- AlCircle (2026-06-18), objectif de première cargaison de Minim-Martap fin septembre 2026 (cité par le module 06) : https://www.alcircle.com/news/cameroons-minim-martap-project-targets-first-bauxite-shipment-by-september-2026-119967
- EcoMatin (2026-08-24), premières exportations de bauxite de Minim-Martap reportées sine die (cité par les modules 05 et 06) : https://ecomatin.net/cameroun-les-premieres-exportations-de-bauxite-de-minim-martap-reportees-sine-die
- AlCircle (2026-09-29), Minim-Martap sans date de première expédition (cité par les modules 07 et 09) : https://www.alcircle.com/news/canyon-resources-minim-martap-bauxite-project-faces-fresh-uncertainty-over-funding-and-first-shipment-121352
- Oriole Resources, RNS 6596V (2026-09-22), Mbe et Bibemi (module 02 [S13]) : https://www.directorstalkinterviews.com/wp-content/uploads/2026/09/ORR-News-1.pdf
- Oriole Resources, Interim Results (RNS, 2025-09-23), ressource de Bibemi (module 02 [S11]) : https://www.investegate.co.uk/announcement/rns/oriole-resources--orr/interim-results/9124477
- Oriole Resources, RNS (2026-07-23), ressource de Mbe (module 07 [S28]) : https://www.investegate.co.uk/announcement/rns/oriole-resources--orr/resources-at-mbe-increased-to-1-66m-oz-gold-/9682976
- Oriole Resources, RNS « Completion of Maiden Drilling at Wapouzé » (module 07 [S34]) : https://www.investegate.co.uk/announcement/rns/oriole-resources--orr/completion-of-maiden-drilling-at-wapouz-/9680681
- Share Talk (2025-12-16), PEA de Bibemi (module 02 [S14]) : https://www.share-talk.com/oriole-resources-confirms-bibemi-gold-project-potential-with-preliminary-economic-assessment/
- Ecofin Agency (2025-11-21), EIES de Bibemi (module 02 [S10]) : https://www.ecofinagency.com/news-industry/2111-50708-oriole-eyes-mid-2026-permit-for-cameroon-s-bibemi-gold-project
- EcoMatin, Kambélé, fin des recherches industrielles (module 07 [S39]) : https://ecomatin.net/or-de-kambele-yaounde-met-fin-aux-recherches-industrielles-et-autorise-lexploitation-artisanale
- Railway Gazette (2026-07-15), locomotives de Camalco : https://www.railwaygazette.com/cameroon/2026/07/15/locomotives-delivered-for-cameroon-bauxite-mining-project/
- Bougna.net (2025-07-14), comité de suivi du rail Mbalam-Kribi : https://bougna.net/2025/07/14/routes/chemin-de-fer/chemin-de-fer-mbalam-port-de-kribi-le-comite-de-suivi-tient-sa-premiere-session/
- AllAfrica / Daba Finance (2026-02-14), plan fer 2026-2030 : https://allafrica.com/stories/202602160017.html
- AllAfrica / RFI (2025-12-19), or et rapport ITIE 2023 : https://fr.allafrica.com/stories/202512190205.html
- Financial Afrik (2025-07-10), étude AMDC et SIGM : https://www.financialafrik.com/2025/07/10/au-cameroun-lurgence-dactualiser-le-potentiel-minier-pour-ameliorer-les-recettes-etude
- Wikipédia (tertiaire) : https://en.wikipedia.org/wiki/Nachtigal_Hydroelectric_Power_Station ; https://en.wikipedia.org/wiki/Memve%27ele_Hydroelectric_Power_Station ; https://en.wikipedia.org/wiki/Kribi_Deepwater_Port ; https://en.wikipedia.org/wiki/Camrail

---

## Contre-vérification (2026-10-08)

Revue indépendante (rapport détaillé : `verification/verif-01-03.md`). Sources rouvertes le 2026-10-08.

**Confirmé** : page de mise hors service Landfolio (03/11/2025) ; comptages USGS refaits (17/13
installations, 9 gisements, 13 exploration, 4 enregistrements au port de Douala, Kribi absent,
FLNG typé « Refinery », 47 centrales, 445 segments de rail, 6 695 de routes avec la ventilation
annoncée) ; distance Nkamouna ≈ 138 km ; Rapport ITIE 2023 re-téléchargé (261 titres, ventilation
149/11/72/29, 952,77 kg d'or, 22,31 kg exportés, 3 305,78 ct, liste des PEMI, « impossibilité
d'extraire les données sous un format ouvert ») ; EITI (suspension, décision 2024-17 du 29/02/2024,
Exigence 1.3, score 53, validation à partir du 01/04/2027, mesure corrective 13) ; décret 2020/749
(prc.cm, osidimbea.cm) ; capital de 10 Mds FCFA et actionnaire unique (sonamines.cm) ; CAPAM ;
Kribi-Lobé (juillet 2027, 120/420 Mds FCFA, 42 MW, 632,8 Mt à 33 %, 132 km²) ; Grand Zambi
(22/09/2025, 6 Mt/an, 150 Mt, 600 000 t) ; terminal minéralier (14 et 47,5 Mt/an) ; Nkamouna et
Akonolinga (18/08/2026, décret 2025/040, 121 Mt) ; Railway Gazette (7 locomotives, 9,1 → 26,9 %,
T4 2026, 35 000 t/mois) ; Afrik (aucune exportation confirmée au 07/04/2026) ; BIC Mbalam et
Minim-Martap ; bougna.net (540/149 km, 25/02/2022, 10/07/2025) ; Colomine (54,5 kg) ; RFI/AllAfrica
(15,2 t, ≈ 90 % EAU, 22,3 kg) ; Wikipédia (Nachtigal, Kribi).

**Modifié** :
- Taille du ZIP USGS : 131,74 MB affichés par ScienceBase (138 Mo correspond aux unités décimales).
- Liste PEMI : CIMENCAM PEMI 00008 = arrêté 2023/128 (et non 2023/129, qui est un second permis
  non numéroté) ; G STONES = PEMI 00009 dans l'une des listes.
- Sentence CCI Sundance (≈ 616 M$) : recoupée par Reuters (https://www.engineeringnews.co.za/article/sundance-resources-says-it-has-won-616m-cameroon-arbitration-over-iron-ore-project-2026-07-27),
  d'après la déclaration de la société → Partiel (sentence elle-même non consultée).
- Retrait d'Eramet d'Akonolinga en octobre 2023 : Non vérifié → Fait vérifié (BIC 21/08/2026).
- Rail Mbalam-Kribi : « double voie » → voie « à double sens » (formulation de la source).
- Étude AMDC : l'article ne nomme pas le SIGM (§10).
- Capacité Camalco de 35 000 t/mois : Non vérifié → Fait vérifié (Railway Gazette, 15/07/2026).

**Non revérifié / inaccessible** : Geofabrik (connexion réinitialisée) ; GlobeNewswire ; capture
Internet Archive du portail ; Discovery Alert ne cite pas de source primaire.

**Harmonisation inter-modules (2026-10-08)** : avertissement « pas un conseil » ajouté ; Minim-Martap : formulation commune du calendrier (prévue fin septembre / T4 2026, reportée sans nouvelle date après la suspension des tirages AFG Bank le 24/08/2026 ; EcoMatin, AlCircle) ; « 18 000 / 300 » réattribués (objectif de janvier 2017 ; bilan 2014-2019 annoncé en juin 2019) ; Mbe, Bibemi, Wapouzé et Kambélé ajoutés à l'inventaire (lignes 24-27, sources des modules 02 et 07) ; ligne Alucam alignée sur les modules 05-07 ; section « Zone et projection communes » ajoutée (§ 7, l'UTM 32N est abandonné pour EPSG:32633). Journal : `verification/harmonisation.md`.
