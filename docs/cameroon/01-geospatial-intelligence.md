# Module 01 — GEO-SPATIAL INTELLIGENCE · « From Satellite to Mineral Target »

**Africa Mineral Insights — édition Cameroun · Livrable : Mineral Target Map**

> Version de travail du 2026-10-08. Contenu rédigé à partir de sources publiques effectivement
> consultées (liste en section 10). Conventions utilisées dans tout le document :
> **[F]** fait vérifié (source citée) · **[I]** inférence (raisonnement à partir de faits vérifiés) ·
> **[H]** hypothèse (à tester) · **[?]** inconnue / non vérifié.
> Les statistiques notées « calcul AMI » ont été calculées par nous le 2026-10-08 à partir de
> données publiques ; la méthode est décrite pour qu'on puisse les refaire.
>
> **Avertissement.** Contenu d'information et de formation, **pas un conseil** (ni en
> investissement, ni juridique, ni technique pour une décision d'exploration). Une cible de
> télédétection est une hypothèse à vérifier sur le terrain : elle ne constitue ni une ressource ni
> une réserve.

---

## 1. Résumé

- **Le schéma du module tient**, mais le document de cadrage surestime les données « prêtes à
  l'emploi ». L'imagerie (Sentinel-2, Sentinel-1, Landsat, archive ASTER) et les MNT sont libres
  et faciles d'accès **[F]**. En revanche, **la couche d'occurrences USGS ne permet pas de faire un
  exercice de ciblage aurifère au Cameroun**. Le calcul AMI sur la base téléchargée donne pour le
  Cameroun 9 gisements (Al, Ga, Co, Fe), 13 sites d'exploration (dont 1 seul en or) et
  17 enregistrements d'installations, soit 13 installations distinctes (dont 1 point générique
  « orpaillage, région du Nord ») **[F]**. Les occurrences
  d'or doivent venir de la littérature scientifique. Exemple : jeu de données Tcholliré,
  CC BY 4.0 **[F]**.
- **Les cartes géologiques modernes (13,5 feuilles au 1/200 000, PRECASEM/BRGM) existent d'après
  le BRGM**, mais nous n'avons trouvé aucun accès public **[?]**. Ce qui est accessible
  aujourd'hui : la carte au 1/1 000 000 de Gazel (révisée en 1956, Atlas IRD), la carte
  continentale USGS (1997) et des feuilles de reconnaissance au 1/500 000 des années 1950,
  conservées en bibliothèque avec un accès restreint **[F]**.
- **Zones d'étude proposées** :
  - **Z1 Tcholliré–Rey Bouba (Nord)**, zone principale. Savane : 74 % d'arbustes et d'herbacées
    (calcul AMI, ESA WorldCover). Occurrences d'or publiées avec coordonnées, et études
    télédétection et aéromagnétisme déjà publiées.
  - **Z2 Bétaré-Oya (Est septentrional)**, zone de transition. 54 % d'arbres. District aurifère
    documenté, contrôle structural NE–SW publié.
  - **Z3 Batouri–Kambélé (Est)**, variante « forêt + latérite ». 87 % d'arbres, or sous plusieurs
    mètres de latérite **[F]**. Elle sert à l'exercice structural (MNT + Sentinel-1).
- **Fenêtre d'acquisition** : de novembre à février. Sur 2023–2024, les dates Sentinel-2 dont
  la tuile a moins de 10 % de nuages tombent presque toutes dans cette période, et il n'y en a
  aucune de juin à septembre dans les trois zones (calcul AMI, catalogue STAC).
- **Livrable** : un GeoPackage de 9 couches avec métadonnées et une classe de confiance par cible.
  Une couche « données insuffisantes » est obligatoire. Les cibles produites sont des **zones à
  vérifier**, pas des gisements.

---

## 2. Corrections au document de cadrage

| # | Affirmation du cadrage | Constat | Source |
|---|---|---|---|
| C1 | Couche USGS « occurrences » utilisée en 01 | Pour le Cameroun, la couche « Mineral occurrence sites and deposits » ne contient que **9 gisements** : Nkamouna (Co), bauxites/Ga de l'Adamaoua et de l'Ouest, Les Mamelles (Fe). **Aucune occurrence d'or.** Ses sources sont des synthèses de gisements majeurs (USGS PP1802, OFR 2005-1294), pas un inventaire d'indices. Pour l'or, il n'y a qu'un site d'exploration (« Southern Belt », Est) et un point générique d'orpaillage (« Mine in North Region and various other locations », 8,386° N / 14,154° E). **La couche ne suffit pas pour un exercice de ciblage aurifère.** | Calcul AMI sur `Africa_GIS.gdb` (ScienceBase, DOI 10.5066/P97EQWXP) et métadonnées FGDC `Africa_GIS_Metadata.xml` (champ InfSource1 de la couche Deposits) |
| C2 | « Année de référence 2018 » | **Partiel.** L'OFR 2024-1041 indique bien 2018 comme année de référence. Les métadonnées du jeu de données donnent cependant une période de **2008 à 2019** : installations 2018 (Minerals Yearbook), sites d'exploration 2014–2018, et des sources de gisements plus anciennes. Il faut afficher la date de chaque couche. | pubs.usgs.gov/publication/ofr20241041 ; métadonnées FGDC (timeperd 2008–2019) |
| C3 | (implicite) Les coordonnées USGS sont utilisables telles quelles | **Incohérences entre couches.** Nkamouna : 3,266° N / 13,813° E dans la couche Deposits, mais 2,533° N / 14,817° E dans la couche Exploration (environ 1° d'écart). Minim-Martap : 6,93° N / 12,97° E contre 6,425° N / 13,242° E. **Contrôle qualité obligatoire avant usage.** | Calcul AMI sur `Africa_GIS.gdb` |
| C4 | Le SIGM fournit « données géologiques et géochimiques (campagne citée : 18 000 échantillons, 300 sites) » | **Partiel / amalgame.** Les « 18 000 échantillons » sont un **objectif** annoncé en janvier 2017 pour le programme de cartographie (consortium BRGM, BEIG3, GTK ; 13 cartes au 1/200 000 ; 30 mois). Les « 300 sites » sont un **bilan** ministériel de juin 2019 (300 nouveaux sites minéralisés découverts entre 2014 et 2019). Il s'agit de deux chiffres différents. **Accès public au SIGM : non trouvé.** | businessincameroon.com (28/01/2017 ; 17/06/2019) ; BRGM, présentation IGF 2018 |
| C5 | Les participants reçoivent « la carte géologique » | **À préciser.** Les cartes PRECASEM au 1/200 000 (« 13.5 new geological 1/200 000 » selon le BRGM) ne sont pas accessibles en ligne d'après nos recherches. On dispose en accès ouvert de la carte au 1/1 000 000 (Gazel, révisée en 1956, notice dans l'Atlas du Cameroun IRD) et de la carte géologique de l'Afrique USGS OFR 97-470-A. Les feuilles au 1/500 000 (par exemple Ngaoundéré-O, 1955) sont en bibliothèque, avec consultation des métadonnées seulement. **L'échelle utilisable ne permet qu'un contexte régional.** | IRD Horizon (Atlas du Cameroun) ; pubs.usgs.gov/publication/ofr97470A ; ITÜ Library |
| C6 | « …et, si disponible, la géochimie » | **Aucune géochimie publique trouvée** pour les zones proposées. La géochimie PRECASEM n'est pas accessible. Ce qui existe : des données pétrographiques et spectrales d'échantillons (Tcholliré, Mendeley Data, CC BY 4.0), qui ne sont pas de la géochimie sol/sédiments. | DataCite 10.17632/p99227dppc.2 ; PMC10823102 |
| C7 | « En forêt dense et sous couvert latéritique (sud, est), la télédétection optique **ne voit pas** les altérations hydrothermales » | **Trop absolu.** La littérature parle de **contrainte**, pas d'impossibilité : « Climatic conditions and vegetation constrain the use of optical satellite imagery » (Ngoura-Colomines, Est). Des altérations ont été cartographiées puis validées sur le terrain dans l'Est (Ngoura-Colomines 2020 ; Borongo-Mborguene 2024, en « mixed-type vegetated terrain »). La limite réelle est forte sous **latérite épaisse**, comme à Batouri : or sous « several-m-thick lateritic cover ». Formulation proposée : « fortement dégradée, et à valider systématiquement sur le terrain ». | Ore Geol. Rev. 2020 (DOI 10.1016/j.oregeorev.2020.103530) ; Adv. Space Res. 2024 (DOI 10.1016/j.asr.2024.07.026) ; J. Afr. Earth Sci. 2015 (DOI 10.1016/j.jafrearsci.2015.07.010) |
| C8 | Zone de savane « Adamaoua, Nord » | **Confirmé**, et chiffré. Fenêtre autour de Ngaoundéré : 74 % d'arbustes et d'herbacées, 16 % d'arbres. Z1 Nord : 74 % d'arbustes et d'herbacées, 20 % d'arbres. À compléter : l'**Est septentrional** (Bétaré-Oya) est intermédiaire, avec 54 % d'arbres. | Calcul AMI, ESA WorldCover 2021 v200 |
| C9 | « les nuages limitent les images exploitables » (au sud et à l'est) | **Vrai partout, pas seulement au sud et à l'est.** Même au Nord (Z1), aucune date à moins de 10 % de nuages de juin à septembre (2023–2024). La différence entre zones est de degré : 43 dates claires sur 146 en Z1, 28 en Z2, 24 en Z3. **La fenêtre de novembre à février est déterminante.** | Calcul AMI, catalogue STAC Earth Search (Sentinel-2 L2A) |
| C10 | MNT « SRTM / Copernicus DEM » pour les structures | Le **Copernicus DEM est un modèle numérique de surface (DSM)** : il inclut le couvert, bâtiments compris. En forêt (Z3), il représente le toit de la canopée ; c'est un biais pour les linéaments. La version GLO30 de Google Earth Engine est remplacée par `COPERNICUS/DEM/GLO30_2024_1`. | developers.google.com (catalogue COPERNICUS_DEM_GLO30) |
| C11 | Sentinel-1 pour l'option forestière | **Valable**, mais la constellation n'a eu qu'un seul satellite de fin 2021 à fin 2024. Sentinel-1B est en panne depuis le 23/12/2021 et sa fin de mission a été déclarée le 03/08/2022. Sentinel-1C a été lancé le 05/12/2024 (communiqué de presse ESA n° 70–2024, consulté lors de la contre-vérification). Les séries temporelles 2022–2024 sont donc moins denses. | esa.int (fin de mission S1B ; communiqué S1C) |
| C12 | Landsat (sous-entendu : SWIR utilisable) ; ASTER non mentionné | À ajouter : **l'archive ASTER antérieure à avril 2008** est la seule source multispectrale libre avec **6 bandes SWIR**, utile pour distinguer les argiles. Le SWIR d'ASTER est inutilisable depuis avril 2008. Les produits AST_L1T sont gratuits depuis le 01/04/2016. | earthdata.nasa.gov (ASTER SWIR Anomaly ; ASTER Data Available at No Charge) ; asterweb.jpl.nasa.gov |
| C13 | Géophysique aéroportée (non mentionnée en 01) | Il existe **deux levés**, mais nous n'avons trouvé aucun accès public : (a) levé aéromagnétique de **1970** (Survair, coopération canadienne ; altitude 235 m, lignes N–S espacées de 750 m ; rapport Paterson, Grant & Watson 1976) ; (b) levé **PRECASEM de 2014–2015**, environ 160 000 km² dans 6 régions (contrat Geotech Airborne, 2,1 milliards de FCFA). Des chercheurs ont utilisé des données aéromagnétiques sur Tcholliré (2022, 2023). | Geophysica 2014 ; businessincameroon.com (22 et 23/01/2014) ; Crossref (gj.4513, s11600-023-01166-6) |

---

## 3. Inventaire des données

| Donnée | Contenu / résolution | URL d'accès | Accès | Licence | Limites (vérifiées sauf mention) | Statut |
|---|---|---|---|---|---|---|
| **Sentinel-2 L2A** (`COPERNICUS/S2_SR_HARMONIZED`) | 13 bandes. B2, B3, B4, B8 à 10 m ; B8A, B11 (≈ 1 610 nm), B12 (≈ 2 190 nm) à 20 m. Revisite de 5 jours. Depuis le 28/03/2017. | https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED · https://dataspace.copernicus.eu | Libre. Inscription requise au Copernicus Data Space ; GEE requiert un compte. | Copernicus : « free, full and open » (Legal Notice) | Couverture L2A 2017–2018 non globale. Bande QA60 vide entre 2022-01-25 et 2024-02-28 : utiliser Cloud Score+. Seulement 2 bandes SWIR, donc pas de discrimination fine des argiles [I]. | Vérifié |
| **Cloud Score+** (`GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED`) | Score de clarté 0–1 à 10 m (`cs`, `cs_cdf`) | https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_CLOUD_SCORE_PLUS_V1_S2_HARMONIZED | Via GEE | Voir la page du catalogue | Seuil conseillé entre 0,50 et 0,65 | Vérifié |
| **Sentinel-1 GRD** (`COPERNICUS/S1_GRD`) | Radar en bande C. Modes IW, EW, SM. Polarisations VV+VH ou HH+HV. Pixel de 10 m. Prétraitements : bruit thermique, calibration, correction de terrain (SRTM 30), conversion en dB. Depuis le 03/10/2014. | https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD | Libre | Copernicus Sentinel T&C | Un seul satellite du 23/12/2021 jusqu'à l'arrivée de S1C (lancé le 05/12/2024). Distorsions géométriques en relief : ombre et repliement [I]. | Vérifié |
| **Landsat 8/9 C2 L2** (`LANDSAT/LC09/C02/T1_L2`, LC08 équivalent) | 30 m. SR_B6 de 1,566 à 1,651 µm ; SR_B7 de 2,107 à 2,294 µm. Revisite de 16 jours par satellite. | https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2 · EarthExplorer (inscription USGS : Non vérifié) | Libre | **Domaine public** (crédit USGS demandé) | Résolution 30 m ; même limite SWIR que Sentinel-2 [I] | Vérifié |
| **ASTER L1T** (archive) | VNIR 15 m, SWIR 30 m (6 bandes), TIR 90 m (résolutions : Non vérifié dans les pages consultées) | https://www.earthdata.nasa.gov/news/aster-data-available-no-charge | Gratuit depuis le 01/04/2016. Compte NASA Earthdata (Non vérifié). | NASA/METI (conditions détaillées : Non vérifié) | **SWIR inutilisable après avril 2008** (saturation, rayures). Le JPL signale aussi des saturations possibles sur les données SWIR de fin mai 2007 à fin janvier 2008 (asterweb.jpl.nasa.gov). Il faut des scènes antérieures à 2008 et peu nuageuses ; leur disponibilité sur Z1, Z2 et Z3 est inconnue [?]. | Vérifié (accès + panne SWIR) |
| **Copernicus DEM GLO-30** (`COPERNICUS/DEM/GLO30`, remplacé par `GLO30_2024_1`) | Modèle de surface (DSM) à 30 m, acquisitions 2010–2015 | https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30 | Libre (sauf Arménie et Azerbaïdjan) | Licence Copernicus DEM, © DLR / Airbus | **DSM** : la canopée biaise les linéaments en forêt | Vérifié |
| **SRTM GL1 v3** (`USGS/SRTMGL1_003`) | 1 seconde d'arc (≈ 30 m), comblé des vides, acquis en février 2000 | https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003 | Libre | Politique JPL/NASA (« any purpose ») | Date de 2000 ; nature surface ou sol sous forêt non précisée dans la page consultée [?] | Vérifié |
| **ESA WorldCover 2021 v200** | Occupation du sol à 10 m, 11 classes | https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200 · tuiles COG `esa-worldcover.s3.eu-central-1.amazonaws.com` | Libre | **CC BY 4.0** | Une seule année (2021) | Vérifié |
| **USGS Africa GIS compilation** | 20 couches : installations, gisements, exploration, infrastructures | https://www.sciencebase.gov/catalog/item/607611a9d34e018b3201cbbf (DOI 10.5066/P97EQWXP) | Libre (GDB de 131,7 Mo) | **CC0 1.0** | Cameroun : 9 gisements, 13 sites d'exploration, 17 enregistrements d'installations (13 identifiants) ; or quasi absent ; incohérences de coordonnées (C1 à C3) | Vérifié (calcul AMI) |
| **USGS OFR 2024-1041** | Carte GeoPDF au 1/38 504 000 | https://pubs.usgs.gov/publication/ofr20241041 | Libre | Domaine public USGS [I] | Échelle continentale ; référence 2018 | Vérifié |
| **USGS MRDS** | Base mondiale d'indices et gisements | https://mrdata.usgs.gov/mrds/ | Libre (WFS) | Non vérifié | **Plus mise à jour systématiquement depuis 2011.** Requête WFS : environ 10 enregistrements camerounais (Al, Fe, Ti), **aucun or**. | Vérifié |
| **Carte géologique de l'Afrique** (USGS OFR 97-470-A, Persits et al. 1997) | Géologie continentale (vecteur et PDF) | https://pubs.usgs.gov/publication/ofr97470A | Libre | Domaine public USGS [I] | Échelle non indiquée sur la page ; usage régional seulement | Vérifié |
| **Carte géologique du Cameroun au 1/1 000 000** (Gazel, Hourcq, Nickles ; révisée en 1956) | 2 feuilles (Nord, Sud). Notice dans l'Atlas du Cameroun (IRCAM) | https://horizon.documentation.ird.fr/exl-doc/pleins_textes/2022-03/17164-17170.pdf | PDF libre (37 Mo, 82 p.) | Non vérifié | Fond topographique ancien (« croquis provisoire au 1/200 000 de l'IGN ») ; présence des planches couleur dans le PDF : Partiel | Partiel |
| **Feuilles de reconnaissance au 1/500 000** (par ex. Ngaoundéré-O, Guiraudie 1955 ; Banyo 1952 ; Yaoundé-O 1957) | Cartes papier | https://dijitalkoleksiyonlar.kutuphane.itu.edu.tr/cdm/compoundobject/collection/itumapsAll/id/2049/rec/1 | **Métadonnées seulement** (ITÜ) | « All rights reserved » | Pas de scan public trouvé pour Z1, Z2 ou Z3 | Vérifié (notice) |
| **Cartes PRECASEM au 1/200 000** + géochimie + SIGM | 13,5 feuilles, prospection géochimique, SIG | (aucune URL publique trouvée) | MINMIDT (procédure : Non vérifié) | Non vérifié | Une étude AMDC/UA de 2025 juge « pour la plupart obsolètes » les données du « système d'information géologique et minérale » (l'article ne nomme ni le SIGM ni le PRECASEM) | Non vérifié (accès) |
| **Aéromagnétisme 1970** (Survair / Paterson, Grant & Watson 1976) | Lignes N–S espacées de 750 m, altitude 235 m | (aucune URL publique) | Non vérifié | Non vérifié | Couverture de Z1, Z2 et Z3 : Non vérifié | Vérifié (existence) |
| **Aéromagnétisme / radiométrie PRECASEM 2014–2015** | Environ 160 000 km², 6 régions | (aucune URL publique) | Non vérifié | Non vérifié | Paramètres contradictoires selon la presse (80 m ou 80–120 m ; lignes à 500 m) | Partiel |
| **Données Tcholliré (Mendeley Data)** | Descriptions d'échantillons avec coordonnées, spectres ASD (350–2 500 nm), lames minces | https://data.mendeley.com/datasets/p99227dppc/2 | Libre | **CC BY 4.0** | Échantillonnage orienté vers les cibles, donc biaisé ; ce ne sont pas des teneurs en or | Vérifié |

---

## 4. Zones d'étude proposées

Méthode de comparaison (calcul AMI, reproductible) :

- **Occupation du sol** : ESA WorldCover 2021 v200, lu dans les tuiles COG publiques sur l'emprise
  de chaque zone, avec un pixel sur 10 (échantillonnage à environ 100 m).
- **Nuages** : catalogue STAC Earth Search (`sentinel-2-l2a`), requête sur un point de
  chaque zone (centre de l'emprise pour Z1 et Z3 ; repère de la ville de Bétaré-Oya pour Z2, voir le tableau) du 01/01/2023 au 31/12/2024, en retenant par date la plus faible valeur
  `eo:cloud_cover`.
- **Limite de cet indicateur** : `eo:cloud_cover` est calculé sur la **tuile entière**
  (100 × 100 km). Ce n'est pas une mesure au pixel.

| | **Z1 Tcholliré–Rey Bouba** (Nord) | **Z2 Bétaré-Oya** (Est septentrional) | **Z3 Batouri–Kambélé** (Est) |
|---|---|---|---|
| Emprise (WGS84) | 13,85–14,40° E ; 8,10–8,70° N (≈ 60 × 66 km) | 13,85–14,35° E ; 5,40–5,85° N (≈ 55 × 50 km) | 14,20–14,55° E ; 4,25–4,60° N (≈ 39 × 39 km) |
| Repère | Tcholliré 8,400° N / 14,167° E (Wikipedia) | Bétaré-Oya 5,600° N / 14,083° E (Wikipedia) | Batouri 4,435° N / 14,362° E (Wikipedia) |
| Projection de travail | UTM 33N (EPSG:32633) [I] | UTM 33N [I] | UTM 33N [I] |
| Occupation du sol (WorldCover 2021) | Arbustes 53,5 %, herbacées 20,3 %, arbres 19,5 %, cultures 6,5 % | Arbres 53,8 %, arbustes 35,0 %, herbacées 9,6 %, eau 1,2 % | **Arbres 87,2 %**, herbacées 7,8 %, arbustes 4,1 % |
| Dates S2 avec tuile < 10 % de nuages (2023–2024) | **43 / 146** (8 par mois de novembre à février ; 0 de juin à septembre) | 28 / 146 (de 4 à 9 par mois de novembre à février ; 0 de juin à octobre), calculé au repère Bétaré-Oya. Au centre géométrique de l'emprise (14,10° E ; 5,625° N), on obtient 32 / 146 : l'indicateur dépend des tuiles couvrant le point | 24 / 146 (de 2 à 7 par mois de novembre à février ; 1 en août) |
| Contexte géologique publié | Shear zone Tcholliré–Banyo. Gneiss, orthogneiss, granodiorite, métabasites, granites mylonitisés. Linéaments NE–SW/ENE–WSW, E–W, N–S. | Shear zone de Bétaré-Oya NNE–SSW, fragile-ductile. Veines quartz-sulfures dans des métasédiments, près de petits granites. Les linéaments NE–SW contrôlent l'or. | Domaine Adamaoua-Yadé. Granitoïdes aurifères d'environ 620 Ma. Or primaire sous plusieurs mètres de latérite. |
| Occurrences documentées | Sites primaires Bougouma et Bandjoukri (veines de quartz aurifère) ; alluvions à Vaimba ; un site éluvial. Coordonnées des échantillons publiées (CC BY 4.0). Point USGS d'orpaillage du Nord situé dans l'emprise. | District aurifère (orpaillage depuis 1934 environ, semi-mécanisé depuis 2004 environ, selon l'abstract GeoJournal 2019 cité via la recherche : Partiel). Gisements « spatially clustered » (NRR 2020). Coordonnées : dans les articles payants [?]. | Prospect Kambélé. Anomalie géochimique sol (119 ppb Au dans un horizon latéritique). Coordonnées : non publiques [?]. |
| Altérations attendues (publiées) | Kaolinite, montmorillonite, muscovite/séricite, calcite, chlorite, épidote ; altérations propylitique et phyllique | Silicification, sulfuration, séricitisation, altération potassique, hématitisation, carbonatation | Non documenté dans les sources consultées [?] |
| Géophysique publique | Études aéromagnétiques publiées (2022, 2023) ; « Poli et Tchamba » cités dans la zone du levé de 2014 (couverture exacte : Non vérifié) | Non vérifié | Non vérifié |
| **Usage pédagogique** | **Exercice spectral complet** (zone principale) | Exercice spectral **avec masquage végétation poussé** | **Variante structurale** (MNT + Sentinel-1), sans indices spectraux concluants |
| Statut | Recommandée | Recommandée en second | Optionnelle (groupe avancé ou comparaison) |

**Justification du choix de Z1 comme zone principale** [I] :

1. C'est la zone la moins végétalisée des trois et celle qui a le plus de dates claires.
2. Des occurrences primaires sont publiées avec coordonnées et licence ouverte, ce qui rend la
   **validation** possible, comme le module 02 l'exige.
3. Une étude publiée (Anaba Fotze et al., 2022) a déjà appliqué ASTER, Landsat 8 et
   l'aéromagnétisme sur la même zone. Elle sert de **référence de correction** pour les
   formateurs.

**Risques** [H] :

- Le dataset Tcholliré échantillonne des zones déjà ciblées par télédétection. Il y a donc un
  risque de circularité dans la validation.
- L'accès terrain et la sécurité dans le Mayo-Rey ne sont pas évalués ici [?].

### Zone et projection communes (modules 01, 02 et 03) [H : proposition d'harmonisation du 2026-10-08]

Ce module produit les couches d'évidence reprises par les modules 02 et 03 : il doit partager leur SCR et leur district de zoom. Proposition commune, identique dans les trois modules :

| Élément | Proposition commune | Justification |
|---|---|---|
| SCR d'échange et de stockage | WGS 84 géographique (**EPSG:4326**) | Système des sources (USGS, OSM, coordonnées des RNS) ; déjà retenu pour l'échange par le module 02 (§ 8) |
| SCR de calcul (distances, surfaces, rasters, densités) | **WGS 84 / UTM 33N (EPSG:32633)**, pour les trois modules | Les trois zones du module 01 (13,85° à 14,55° E, § 4 du module 01) sont entièrement dans le fuseau UTM 33 (12° à 18° E) ; le module 01 l'utilise déjà. Un SCR de calcul unique évite des reprojections entre livrables et des écarts de surface d'un module à l'autre [I] |
| Projets et ports à l'ouest de 12° E (fuseau 32 : Kribi, Douala) | Garder EPSG:32633 pour les distances du module 03 (étape 6) | Le port en eau profonde de Kribi (9,864° E, module 03 § 6.1) est à environ 5,1° du méridien central de 15° E : facteur d'échelle d'environ 1,0036, soit une erreur d'environ 0,4 % sur une distance, négligeable pour des distances au port exprimées en km [I : calcul k ≈ 0,9996 × (1 + (Δλ·cos φ)²/2)]. L'UTM 32N (EPSG:32632) n'est plus utilisé |
| Emprise nationale | Limite ADM0 du Cameroun (couche `adm0_adm1` du module 03) | Échelle de la carte nationale du module 02 (1 km) et de la carte de l'écosystème du module 03 |
| District commun (zoom) | **Z2 Bétaré-Oya : 13,85–14,35° E ; 5,40–5,85° N** (emprise du module 01, § 4) | Seule zone commune aux modules 01 (Z2, « recommandée en second ») et 02 (district « Bétaré-Oya / Lom », littérature la plus dense). Le module 03 y rattache Mborguéné (« Bétaré-Oya / Garoua-Boulaï ») ; son inclusion dans l'emprise reste à vérifier au géocodage [?]. Z1 Tcholliré reste la zone principale de l'exercice spectral du module 01 ; Mbe (Adamaoua) et Bibemi (Nord) restent hors district et servent à la rétro-prédiction nationale du module 02 |
| Résolution de référence | National : 1 km ; district : 100 m (module 02 § 8) ; produits Sentinel-2 : 10-20 m (module 01) | Les rasters du module 01 sont rééchantillonnés à 100 m avant d'entrer dans le modèle de district du module 02 [H] |

---

## 5. Déroulé de l'étude de cas

Durée totale indicative : **3 jours (environ 20 h)**, dont 6 h de théorie. Outils :
**Google Earth Engine** (Code Editor, compte requis ; conditions d'usage commercial : Non
vérifié) pour le prétraitement, et **QGIS** (version LTR ; outils natifs : calculatrice raster,
ombrage GDAL, densité de lignes) pour l'interprétation et la mise en page.

Chaîne : `Image → masques → indices → anomalies → structures → intégration → cibles + confiance`

### Étape 0 — Cadrage et données (1 h)

Charger l'emprise de la zone, les couches USGS (filtre `Country = 'Cameroon'`) et le tableau
d'échantillons Mendeley (Z1). Faire le **contrôle qualité des occurrences** (C3) et ajouter à
chaque point un champ `type` (primaire / éluvial / alluvial) et un champ `precision`.

### Étape 1 — Composite Sentinel-2 de saison sèche (2 h, GEE)

```javascript
// Z1 — adapter l'emprise pour Z2/Z3
var zone = ee.Geometry.Rectangle([13.85, 8.10, 14.40, 8.70]);
var csPlus = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(zone)
  .filter(ee.Filter.or(
    ee.Filter.date('2023-11-01', '2024-03-01'),
    ee.Filter.date('2024-11-01', '2025-03-01')))
  .linkCollection(csPlus, ['cs_cdf'])
  .map(function (img) {
    return img.updateMask(img.select('cs_cdf').gte(0.60));  // seuil 0.50–0.65 selon la doc
  });
var comp = s2.median().select(['B2','B3','B4','B8','B8A','B11','B12'])
  .divide(10000).clip(zone);
```

- Le seuil de 0,60 et la plage 0,50–0,65 viennent du catalogue GEE Cloud Score+ **[F]**.
- La fenêtre de novembre à février vient du calcul AMI (section 4) **[F]**.
- Exporter `comp` (GeoTIFF, EPSG:32633, 20 m) vers QGIS.

### Étape 2 — Masques (1 h 30)

- **Végétation** : `ndvi = comp.normalizedDifference(['B8','B4'])`. Masquer les pixels où
  `ndvi > seuil`. Le seuil est à **calibrer par zone** à partir de l'histogramme ; la valeur
  de départ 0,35 est une **hypothèse [H]**.
- **Eau** : WorldCover classe 80.
- **Bâti** : WorldCover classe 50.
- **Feux de brousse et cicatrices de brûlis** en saison sèche : risque de faux signaux
  d'oxydes de fer [H]. À contrôler visuellement sur la composition colorée.
- Produire une couche `masque_qualite` où chaque pixel exclu porte son motif d'exclusion.

### Étape 3 — Indices spectraux (2 h)

| Indice | Sentinel-2 | Landsat 8/9 | ASTER (avant 2008) | Cible |
|---|---|---|---|---|
| Oxydes de fer ferriques | B4/B2 | B4/B2 | B2/B1 | Hématite, goethite (chapeaux de fer, latérite) |
| Hydroxyles, argiles, carbonates | B11/B12 | B6/B7 | (B4+B6)/B5 pour Al-OH ; (B7+B9)/B8 pour Mg-OH et carbonates | Séricite, kaolinite, chlorite, épidote, calcite |
| ACP orientée (Crósta) | B2, B4, B11, B12 | B2, B4, B6, B7 | B1, B3, B4, B6 | Isoler les composantes « fer » et « OH » |

- **Statut des formules [I]** : il s'agit de ratios d'usage courant. Le rapport 4/2 et le
  rapport 6/7 pour Landsat sont rapportés pour le champ aurifère de Ketté (Est), mais la notice
  n'a pas été consultée directement. Les ratios ASTER, l'ACP de Crósta et l'article de référence
  van der Meer et al. 2014 (*Potential of ESA's Sentinel-2 for geological applications*,
  RSE 148:124-133, **DOI vérifié via Crossref, contenu non consulté**) sont à valider par le
  formateur.
- **Base physique [I]** : B12 (≈ 2 190 nm) et SR_B7 (2,107–2,294 µm) couvrent la zone
  d'absorption des hydroxyles et des carbonates (≈ 2,2–2,35 µm). Avec une seule bande dans cette
  zone, **on ne peut pas distinguer kaolinite, séricite et chlorite**. Seul l'ASTER SWIR
  antérieur à 2008 le permet, et seulement partiellement.
- **Fait vérifié** : des études camerounaises ont cartographié oxydes de fer et hydroxyles par
  ratios de bandes et ACP, puis les ont validés sur le terrain (Ngoura-Colomines 2020 ;
  Tcholliré 2022 ; Borongo-Mborguene 2024).

### Étape 4 — Anomalies (1 h)

- Sur les pixels non masqués, calculer le seuil `moyenne + 2σ`, puis `+ 1,5σ` en test de
  sensibilité [H]. Utiliser `reduceRegion` dans GEE ou les statistiques de couche dans QGIS.
- Vectoriser les anomalies et supprimer les polygones de moins de 4 pixels.
- Superposer avec les rivières (couche USGS ou OSM). **Une anomalie de fer alignée sur un
  talweg peut être une latérite alluviale ou colluviale, pas une altération** [I].

### Étape 5 — Linéaments (3 h)

- **MNT** : `COPERNICUS/DEM/GLO30_2024_1`, avec 4 ombrages (azimuts 0°, 45°, 90°, 135° ;
  élévation 30°), plus la pente et la courbure.
  - Un seul azimut favorise les linéaments perpendiculaires à l'éclairage [I].
  - En Z3, il faut garder en tête que le MNT est un DSM **[F]** : des limites de parcelles
    forestières peuvent apparaître comme de faux linéaments [I].
- **Sentinel-1** : médiane VV et VH (mode IW) en orbite **ascendante et descendante séparément**,
  en saison sèche, pour limiter l'effet de l'humidité [H]. Appliquer un filtre de speckle (par
  exemple une médiane 3×3), puis des filtres directionnels.
- **Extraction** : numérisation manuelle dans QGIS (référence). L'extraction automatique (filtres
  de Sobel, PCI LINE, etc.) est optionnelle ; les études de Ketté et de Tcholliré utilisent des
  approches semi-automatiques. **Chaque linéament porte les attributs** `source` (DEM ou S1),
  `azimut`, `longueur_m` et `confiance`.
- **Analyse** : rosace des directions, puis carte de **densité de linéaments** (QGIS, outil
  « densité de lignes », rayon de 1 à 2 km [H]).
- **Comparer avec les directions publiées** : NE–SW, ENE–WSW, E–W et N–S en Z1 ; NE–SW et NNE–SSW
  en Z2 **[F]**. Un écart important doit être expliqué.

### Étape 6 — Intégration et cibles (3 h)

Méthode recommandée : **indexation booléenne puis pondérée, transparente**. La logique floue
et l'apprentissage automatique sont réservés au module 02.

| Évidence | Règle (exemple, à ajuster [H]) | Poids indicatif [H] |
|---|---|---|
| Anomalie hydroxyles (OH) | ≥ moyenne + 2σ | 2 |
| Anomalie oxydes de fer | ≥ moyenne + 2σ, hors talweg | 1 |
| Densité de linéaments | Quintile supérieur | 2 |
| Proximité d'un linéament NE–SW (Z1, Z2) | ≤ 500 m | 1 |
| Lithologie favorable | Contact granite / métasédiments ou métabasites, d'après la carte disponible | 1 |
| Occurrence connue | ≤ 2 km | Non intégrée au score : sert à la **validation** |

- **Validation** (règle du module 02 appliquée dès le 01) : mettre de côté environ 30 % des
  occurrences primaires et contrôler qu'elles tombent dans les classes hautes. Les occurrences
  **alluviales sont exclues** du score et de la validation, conformément au cadrage.
- **Sortie** : polygones de cibles avec un score et une **classe de confiance** (voir 6.3).

### Étape 7 — Mise en forme, revue croisée et restitution (2 h + 1 h 30)

Chaque groupe présente 3 cibles maximum et défend les évidences et les limites de chacune.
Un autre groupe joue le rôle de critique.

### Limites de la télédétection en zone tropicale et sous latérite

1. **Végétation** : la chlorophylle et l'eau foliaire masquent les signatures minérales
   (« constrain », Ngoura-Colomines **[F]**). En Z3, 87 % de couvert arboré **[F]** signifie que
   les indices spectraux ne s'appliquent qu'aux clairières, routes et chantiers d'orpaillage.
   Ce sont des surfaces **déjà perturbées** [I].
2. **Latérite et cuirasse** : l'or est sous plusieurs mètres de latérite à Batouri **[F]**. Le
   signal fer de surface traduit l'altération supergène, pas l'hydrothermalisme [I]. **Un
   indice fer positif sur un plateau cuirassé n'est pas une cible.**
3. **Nuages** : aucune image claire de juin à septembre, même au Nord **[F]**. Les composites
   multi-dates mélangent des états de végétation différents [I].
4. **Résolution spectrale** : deux bandes SWIR (Sentinel-2, Landsat), donc pas de minéralogie
   fine. L'ASTER SWIR est figé avant 2008 **[F]**.
5. **Orpaillage** : les chantiers créent des anomalies (sols nus, argiles remaniées) qui sont des
   **conséquences** de l'or connu, pas des **indices** indépendants [I]. Il faut les masquer ou
   les signaler, sinon le résultat est circulaire.
6. **MNT** : le DSM représente la canopée en forêt **[F]**. SRTM date de 2000 **[F]**.
7. **Absence de géochimie publique** : sans elle, aucune cible ne dépasse la classe « B »
   (section 6.3) [I].

---

## 6. Spécification du livrable — *Mineral Target Map*

### 6.1 Format

- **GeoPackage** `AMI_CM_M01_<zone>_<groupe>_<AAAAMMJJ>.gpkg`, en EPSG:32633 (SCR de calcul commun aux
  modules 01, 02 et 03 ; copie d'échange en EPSG:4326 : voir « Zone et projection communes », § 4).
- Une **carte PDF** au format A3 à l'échelle 1/100 000 [H].
- Un **fichier de métadonnées** (Markdown ou YAML).

### 6.2 Couches

| Couche | Type | Attributs obligatoires |
|---|---|---|
| `zone_etude` | Polygone | nom, emprise, date |
| `masque_qualite` | Raster | 0 = valide ; 1 = nuage ; 2 = végétation ; 3 = eau ; 4 = bâti ; 5 = orpaillage ou perturbation |
| `anomalie_fe` / `anomalie_oh` | Polygone | capteur, ratio, seuil (σ), dates des scènes |
| `lineaments` | Ligne | source (DEM ou S1), azimut, longueur_m, confiance (1–3), opérateur |
| `densite_lineaments` | Raster | rayon, unité |
| `lithologie` | Polygone | unité, **carte source + échelle + année** |
| `occurrences` | Point | nom, substance, type (primaire / éluvial / alluvial), source (URL ou DOI), précision, `jeu` (calibration ou validation) |
| `cibles` | Polygone | id, score, classe de confiance, liste des évidences, évidences contraires, recommandation terrain |
| `donnees_insuffisantes` | Polygone | motif (nuage, couvert, latérite, absence de carte) |

### 6.3 Classes de confiance [H : grille proposée, à valider avec le module 02]

- **A — forte** : au moins 3 évidences indépendantes concordantes (spectral + structural +
  lithologie), une occurrence primaire validée à proximité **et** des données géochimiques. Cette
  classe est **inaccessible** sans géochimie publique.
- **B — moyenne** : au moins 3 évidences concordantes, sans géochimie. C'est la classe maximale
  atteignable dans ce module.
- **C — faible** : 2 évidences, ou évidences dans une zone partiellement masquée.
- **D — données insuffisantes** : couvert, nuages ou latérite empêchent l'évaluation.
  **Ce n'est pas une absence de potentiel.**

### 6.4 Métadonnées minimales

- Identifiants et dates des scènes, seuils (Cloud Score+, NDVI, σ), versions des collections GEE
  et de QGIS.
- Sources avec URL, licence et date d'extraction.
- Opérateur, et limites connues de la zone.
- Mention : « Cible d'exploration à vérifier — ne constitue pas une ressource ni une réserve ».

---

## 7. Sorties vers les autres modules

| Vers | Ce qui est transmis | Usage |
|---|---|---|
| **02 Mineral Potential** | `cibles`, `anomalie_fe`, `anomalie_oh`, `densite_lineaments`, `lineaments`, `occurrences` (avec le champ `jeu` et le `type`), `donnees_insuffisantes` | Couches d'évidence pour la matrice de prospectivité. Le jeu de validation est déjà séparé. La catégorie « Insufficient data » est alimentée directement. |
| **03 Mining Ecosystem** | Occurrences consolidées et corrigées ; note de contrôle qualité sur les coordonnées USGS (C1 à C3) | Couche « occurrences » de l'écosystème, avec source et date |
| **07 Investment Pipeline** | Fiche synthétique des cibles de classe B (localisation, évidences, limites) | Critère « Geology » : niveau « cible télédétection non vérifiée » |
| **09 National Strategy** | Inventaire des lacunes de données (cartes au 1/200 000, géochimie, aéromagnétisme non publics) | Volet « Enable : données » de la stratégie |
| **Jeu de secours** | Composite Sentinel-2, linéaments de référence et cibles du corrigé formateur (Z1) | Permet à un groupe dont le livrable est faible de poursuivre en 02 |

---

## 8. Tableau de vérification

| Affirmation | Source | Statut |
|---|---|---|
| Données USGS Africa publiées le 18/08/2021, DOI 10.5066/P97EQWXP, licence CC0 | usgs.gov/data/... ; sciencebase.gov | Vérifié |
| Tracts non découverts : Gabon, Mauritanie ; potasse, platinoïdes, cuivre | usgs.gov/data/... (métadonnées) | Vérifié |
| Référence 2018 (OFR 2024-1041) ; période des métadonnées 2008–2019 | pubs.usgs.gov/publication/ofr20241041 ; FGDC XML | Vérifié |
| Cameroun dans USGS : 9 gisements, 13 sites d'exploration, 17 enregistrements d'installations (13 installations) ; 1 site d'exploration aurifère | Calcul AMI sur `Africa_GIS.gdb` | Vérifié |
| Coordonnées incohérentes pour Nkamouna et Minim-Martap | Calcul AMI | Vérifié |
| MRDS non mis à jour systématiquement depuis 2011 ; aucun or au Cameroun | mrdata.usgs.gov/mrds ; requête WFS | Vérifié |
| Programme de cartographie lancé le 24/01/2017 : 13 cartes au 1/200 000, 18 000 échantillons, BRGM-BEIG3-GTK, 4,5 milliards de FCFA, 30 mois | businessincameroon.com (28/01/2017) | Vérifié (annonce) |
| « 13.5 new geological 1/200 000 », SIGM, lithothèque (projet GEO4CAM) | igfmining.org (BRGM, 2018) | Vérifié |
| 300 nouveaux sites 2014–2019 (or, zinc, terres rares, U, Ni, rutile, Mn) | businessincameroon.com (17/06/2019) | Vérifié (déclaration) |
| Cartes PRECASEM et SIGM accessibles publiquement | — | Non vérifié |
| Étude AMDC/UA (2025) : données du « système d'information géologique et minérale » « pour la plupart obsolètes » (le lien avec le SIGM du PRECASEM n'est pas établi par l'article) | financialafrik.com (10/07/2025) | Vérifié (via la presse) ; attribution au SIGM : Partiel |
| Levé aéroporté 2014–2015, environ 160 000 km², 6 régions, Geotech, 2,1 milliards de FCFA | businessincameroon.com (22 et 23/01/2014) ; africainharlem.nyc (PANA) | Partiel (paramètres contradictoires) |
| Aéromagnétisme 1970 : Survair, altitude 235 m, lignes N–S à 750 m ; Paterson et al. 1976 | archive.geophysica.fi (Bikoro et al. 2014) | Vérifié (source secondaire) |
| Projet Banque mondiale P122153 ; financement additionnel P160917, clôturé le 01/12/2021 | API projets de la Banque mondiale (search.worldbank.org/api/v3/projects, consultée le 2026-10-08 : P160917, parent P122153, clôture 2021-12-01) | Vérifié |
| Carte au 1/1 000 000 (Gazel, Hourcq, Nickles ; révisée en 1956 ; 2 feuilles) | IRD Horizon (Atlas du Cameroun) | Vérifié |
| Feuille Ngaoundéré-O au 1/500 000 (1955), métadonnées seulement | ITÜ Library | Vérifié |
| USGS OFR 97-470-A, géologie de l'Afrique, 1997 | pubs.usgs.gov/publication/ofr97470A | Vérifié |
| Bandes, résolutions, revisite et masque QA60 de Sentinel-2 | Catalogue GEE COPERNICUS_S2_SR_HARMONIZED | Vérifié |
| Cloud Score+ : seuil de 0,50 à 0,65 | Catalogue GEE | Vérifié |
| Accès Copernicus gratuit avec inscription (« free, full and open ») | dataspace.copernicus.eu/terms-and-conditions | Vérifié |
| Libellé d'attribution exact Copernicus | — | Non vérifié |
| Sentinel-1B : anomalie le 23/12/2021, fin le 03/08/2022 | esa.int | Vérifié |
| Sentinel-1C lancé le 05/12/2024 | esa.int, communiqué n° 70–2024 (lu par curl lors de la contre-vérification) | Vérifié |
| Landsat C2 dans le domaine public ; bandes SWIR | Catalogue GEE LC09 | Vérifié |
| ASTER SWIR inutilisable depuis avril 2008 ; AST_L1T gratuit depuis le 01/04/2016 | earthdata.nasa.gov ; asterweb.jpl.nasa.gov | Vérifié |
| Copernicus DEM = DSM, licence libre, remplacé par GLO30_2024_1 | Catalogue GEE | Vérifié |
| SRTM GL1 v3 à 30 m, février 2000 | Catalogue GEE | Vérifié |
| WorldCover 2021 v200, CC BY 4.0 | Catalogue GEE | Vérifié |
| Occupation du sol Z1, Z2, Z3 et Adamaoua (%) | Calcul AMI (WorldCover) | Vérifié (calcul reproductible) |
| Dates à moins de 10 % de nuages par zone et par mois | Calcul AMI (STAC Earth Search) | Vérifié (indicateur par tuile) |
| Tcholliré : occurrences, altérations, coordonnées des échantillons, CC BY 4.0 | PMC10823102 ; DataCite | Vérifié |
| Tcholliré : ASTER 07XT, Landsat 8 et aéromagnétisme ; linéaments NE–SW/ENE–WSW, E–W, N–S | Crossref (10.1002/gj.4513, abstract) | Vérifié |
| Bétaré-Oya : shear zone NNE–SSW, altérations | Crossref (10.1002/gj.3093, abstract) | Vérifié |
| Bétaré-Oya : gisements regroupés, contrôle NE–SW | Crossref (titre) + résultat de recherche (abstract) | Partiel |
| Bétaré-Oya : orpaillage depuis 1934 environ, semi-mécanisé depuis 2004 environ | Résultat de recherche (GeoJournal 2019) | Partiel |
| Batouri : or sous plusieurs mètres de latérite ; 119 ppb Au | rims.gov.bw (abstract JAES 2015) | Vérifié |
| Batouri : granitoïdes aurifères de 619–624 Ma | Résumé d'Asaah et al. (DOI 10.1080/00206814.2014.951003) sur pure.kfupm.edu.sa : « concordant ages of 619 ± 2 and 624 ± 2 Ma » | Vérifié (résumé) |
| Ngoura-Colomines : « vegetation constrain » ; méthodes et validation | authors.library.caltech.edu | Vérifié |
| Borongo-Mborguene : Landsat-8, ASTER, SRTM, 5 prospects | authors.library.caltech.edu | Vérifié |
| Ketté : ratios 4/2, 6/5 et 6/7 | Résultat de recherche (page source en 403) | Non vérifié |
| Coordonnées des villes (Tcholliré, Bétaré-Oya, Batouri) | en.wikipedia.org | Vérifié |
| Ratios ASTER, ACP de Crósta, contenu de van der Meer 2014 | — (DOI vérifié seulement) | Non vérifié |
| Couverture de Z1, Z2 et Z3 par les levés aéroportés | — | Non vérifié |

---

## 9. Inconnues et questions ouvertes

1. **Accès aux cartes PRECASEM au 1/200 000, à la géochimie et au SIGM** : existe-t-il une
   procédure d'accès (MINMIDT, Direction de la Géologie) ? Quelles sont les conditions de
   réutilisation pédagogique et commerciale ? *Priorité 1 : cela détermine si la classe de
   confiance « A » est atteignable.*
2. **Aéromagnétisme de 1970 et de 2014–2015** : couverture effective de Z1, Z2 et Z3, format
   (grilles ou cartes), droits d'usage.
3. **Scènes ASTER antérieures à 2008** peu nuageuses sur Z1 et Z2 : nombre et qualité (requête
   LP DAAC ou GEE à faire).
4. **Coordonnées des occurrences** de Bétaré-Oya et de Batouri : elles sont dans des articles
   payants. Faut-il demander l'autorisation aux auteurs, ou numériser à partir des figures (avec
   une précision dégradée) ?
5. **Seuils** (NDVI, σ, poids) : à calibrer sur Z1 lors d'un essai à blanc par le formateur avant
   la session.
6. **Effet des feux de saison sèche** sur les indices de fer en Z1 : à tester (hypothèse non
   vérifiée).
7. **Sécurité et accès terrain** (Mayo-Rey, Lom-et-Djerem) si une vérification terrain est
   envisagée : non évalués.
8. **Conditions Google Earth Engine** pour un usage dans une formation payante : non vérifiées.
   Prévoir une alternative en QGIS seul, avec téléchargement depuis le Copernicus Data Space.
9. **Limite de cette vérification** : le quota de recherches web a été atteint pendant le
   travail. Les points marqués « Partiel » ou « Non vérifié » ci-dessus (Ketté, contenu de
   van der Meer 2014) restent à confirmer par consultation directe. S1C, les granitoïdes de
   Batouri et P160917 ont été confirmés lors de la contre-vérification (voir la dernière section).

---

## 10. Sources (URL consultées)

**USGS / données d'occurrences**
- https://www.usgs.gov/data/compilation-geospatial-data-gis-mineral-industries-and-related-infrastructure-africa
- https://www.sciencebase.gov/catalog/item/607611a9d34e018b3201cbbf (dont `Africa_GIS_Metadata.xml` et `Africa_GIS.gdb.zip`, téléchargés et analysés)
- https://pubs.usgs.gov/publication/ofr20241041
- https://pubs.usgs.gov/publication/ofr97470A
- https://mrdata.usgs.gov/mrds/ et le service WFS https://mrdata.usgs.gov/services/wfs/mrds

**Imagerie et MNT**
- https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED
- https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_CLOUD_SCORE_PLUS_V1_S2_HARMONIZED
- https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD
- https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2
- https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30
- https://developers.google.com/earth-engine/datasets/catalog/USGS_SRTMGL1_003
- https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200
- https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ (tuiles N03E012 et N06E012, lues pour le calcul AMI)
- https://earth-search.aws.element84.com/v1/search (catalogue STAC, calcul AMI des nuages)
- https://dataspace.copernicus.eu/terms-and-conditions
- https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-1/Mission_ends_for_Copernicus_Sentinel-1B_satellite
- https://www.esa.int/Newsroom/Press_Releases/Double_win_for_Europe_Sentinel-1C_and_Vega-C_take_to_the_skies (403 via WebFetch lors de la rédaction ; lu par curl lors de la contre-vérification du 2026-10-08)
- https://www.earthdata.nasa.gov/data/alerts-outages/aster-swir-anomaly
- https://www.earthdata.nasa.gov/news/aster-data-available-no-charge
- https://asterweb.jpl.nasa.gov/swir-alert.asp

**Cartes géologiques, PRECASEM, géophysique**
- https://horizon.documentation.ird.fr/exl-doc/pleins_textes/2022-03/17164-17170.pdf
- https://dijitalkoleksiyonlar.kutuphane.itu.edu.tr/cdm/compoundobject/collection/itumapsAll/id/2049/rec/1
- https://www.igfmining.org/wp-content/uploads/2018/11/Session-4-_-Geological-Information-_-2.pdf
- https://www.businessincameroon.com/mining/2801-6852-cameroon-launches-new-prospection-campaign-of-mining-sites-in-six-regions-of-the-country
- https://www.businessincameroon.com/mining/2201-4595-cameroon-starts-inventory-of-mining-potential-in-160-000-km2-area
- https://www.businessincameroon.com/mining/2301-4596-geotech-airbone-signs-2-1-billion-fcfa-contract-to-inventory-cameroon-s-mining-potential
- https://www.businessincameroon.com/index.php/mining/1706-9219-cameroon-300-new-mining-sites-discovered-in-5-regions-in-2014-2019-in-the-framework-of-world-bank-backed-programme-precasem
- https://africainharlem.nyc/en/cameroon-cameroon-to-conduct-aerial-geophysical-survey-le-cameroun-va-lancer-ce-mois-une-campagne-de-levee-geophysique-aeroportee/
- https://www.financialafrik.com/2025/07/10/au-cameroun-lurgence-dactualiser-le-potentiel-minier-pour-ameliorer-les-recettes-etude
- https://projects.worldbank.org/en/projects-operations/project-detail/P122153
- https://archive.geophysica.fi/pdf/geophysica_2014_50_1_011_bikoro.pdf

**Littérature sur les zones d'étude**
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10823102/ (Tcholliré, Data in Brief 2024)
- https://api.datacite.org/dois/10.17632/p99227dppc.2 → https://data.mendeley.com/datasets/p99227dppc/2
- https://api.crossref.org/works/10.1002/gj.4513 (Tcholliré, Geological Journal 2022)
- https://api.crossref.org/works/10.1007/s11600-023-01166-6 (Tcholliré, Acta Geophysica 2023)
- https://api.crossref.org/works/10.1002/gj.3093 (Bétaré-Oya, Geological Journal)
- https://api.crossref.org/works/10.1007/s11053-020-09695-3 (Bétaré-Oya, Natural Resources Research 2020)
- https://api.crossref.org/works/10.1007/s10708-019-10002-8 (Bétaré-Oya, Ngoura, Batouri — GeoJournal 2019)
- https://api.crossref.org/works/10.1016/j.rse.2014.03.022 (van der Meer et al. 2014 — métadonnées seulement)
- https://authors.library.caltech.edu/records/4b9as-90f26 (Ngoura-Colomines, Ore Geology Reviews 2020)
- https://authors.library.caltech.edu/records/n15cn-83v72 (Borongo-Mborguene, Advances in Space Research 2024)
- https://www.rims.gov.bw/converis/portal/detail/Publication/5379808?lang=en_GB (Batouri, J. Afr. Earth Sci. 2015)
- https://en.wikipedia.org/wiki/Bétaré-Oya · https://en.wikipedia.org/wiki/Batouri · https://en.wikipedia.org/wiki/Tcholliré

---

## Contre-vérification (2026-10-08)

Revue indépendante (rapport détaillé : `verification/verif-01-03.md`). Sources rouvertes le 2026-10-08.

**Confirmé** : comptages USGS refaits sur `Africa_GIS.gdb` (24 classes d'entités ; Cameroun :
9 gisements, 13 sites d'exploration dont 1 en or, 17 enregistrements d'installations) ;
incohérences Nkamouna (≈ 138 km) et Minim-Martap (≈ 64 km) ; ScienceBase (131,74 MB, publié le
2021-08-13) ; page usgs.gov (CC0, 18/08/2021, 20 couches) ; OFR 2024-1041 (1:38 504 000,
référence 2018, 02/07/2024) ; catalogue GEE Sentinel-2 (28/03/2017, 5 jours, QA60 masqué du
2022-01-25 au 2024-02-28, couverture 2017–2018 non globale), Cloud Score+ (0,50–0,65),
Copernicus DEM (DSM, remplacé par `GLO30_2024_1`), WorldCover (10 m, 11 classes, CC BY 4.0,
classes 50 et 80) ; ESA (S1B : anomalie 23/12/2021, fin 03/08/2022) ; NASA (AST_L1T gratuit
depuis le 01/04/2016 ; SWIR inutilisable depuis avril 2008) ; Business in Cameroon (28/01/2017,
23/01/2014, 17/06/2019) ; BRGM IGF 2018 (« 13.5 new geological 1/200 000 », SIGM) ; Geophysica 2014
(levé 1970 Survair, 235 m, 750 m) ; PANA (160 000 km², 80–120 m, 500 m) ; PMC10823102 et DataCite
(CC BY 4.0) ; 9 DOI via Crossref ; coordonnées Wikipédia ; dates claires Sentinel-2 recalculées
(Z1 : 43/146 ; Z3 : 24/146).

**Modifié** :
- « 17 installations » → « 17 enregistrements (13 installations) » (§1, §3, §8).
- Étude AMDC : l'article Financial Afrik ne nomme pas le SIGM ; attribution rétrogradée en Partiel.
- Z2 : 28/146 obtenu au repère Bétaré-Oya, 32/146 au centre de l'emprise ; méthode précisée.
- Sentinel-1C (05/12/2024) : Partiel → Vérifié (communiqué ESA lu directement).
- P160917 (clôture 01/12/2021) : Partiel → Vérifié (API Banque mondiale).
- Granitoïdes de Batouri (619 ± 2 et 624 ± 2 Ma) : Non vérifié → Vérifié (résumé, pure.kfupm.edu.sa).
- ASTER : ajout de la réserve du JPL sur les saturations SWIR de mai 2007 à janvier 2008.

**Non revérifié** : pourcentages WorldCover (calcul raster non refait) ; ratios de Ketté ; contenu
de van der Meer 2014 (DOI et pagination confirmés : RSE 148:124-133).

**Harmonisation inter-modules (2026-10-08)** : ajout de l'avertissement « information et formation, pas un conseil » (en-tête) ; ajout de la section « Zone et projection communes » (§ 4 : stockage EPSG:4326, calcul EPSG:32633, district commun Z2 Bétaré-Oya) ; § 6.1 renvoie à cette convention. Journal : `verification/harmonisation.md`.
