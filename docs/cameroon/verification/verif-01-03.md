# Contre-vérification des modules 01, 02 et 03 — édition Cameroun

Date : 2026-10-08. Vérificateur indépendant, en mode adversarial : l'objectif était de trouver des
erreurs, pas de confirmer le texte.

Périmètre : `01-geospatial-intelligence.md`, `02-mineral-potential.md`,
`03-mining-sector-intelligence.md`.

**Méthode**
- Réouverture des URL citées (WebFetch, ou curl quand WebFetch renvoyait 403).
- Re-téléchargement des PDF primaires : RNS Oriole 6596V, Rapport ITIE 2023, BRGM IGF 2018,
  Geophysica 2014.
- DOI contrôlés via api.crossref.org ; DataCite pour le jeu Mendeley.
- Recomptage des couches USGS sur `Africa_GIS.gdb` avec pyogrio.
- Recalcul des dates Sentinel-2 claires via le STAC Earth Search.
- Recherche web d'une seconde source pour 3 affirmations : Batouri, Sundance, Ahafo.

Légende des résultats : **Confirmé** · **Corrigé** (texte modifié) · **Rétrogradé** (statut
abaissé) · **Promu** (statut relevé après confirmation directe) · **Source inaccessible**.

## 1. Tableau des vérifications

| Module | Affirmation | Source | Résultat | Commentaire |
|---|---|---|---|---|
| 01 | USGS Cameroun : 9 gisements, 13 sites d'exploration (1 en or), « 17 installations » | `Africa_GIS.gdb` (recompté) | Corrigé | 17 **enregistrements** pour 13 installations distinctes (CMR001 à CMR013). Le module 03 le disait déjà ; le module 01 était imprécis. |
| 01 | Nkamouna : 3,266/13,813 contre 2,533/14,817 ; Minim-Martap : 6,93/12,97 contre 6,425/13,242 | gdb | Confirmé | Écarts de 138 km et 64 km. |
| 01 | Point d'orpaillage « Mine in North Region… » à 8,386° N / 14,154° E ; site d'exploration « Southern Belt » | gdb | Confirmé | — |
| 01 | Data release : DOI 10.5066/P97EQWXP, CC0, GDB de 131,7 Mo | sciencebase.gov ; usgs.gov | Confirmé | ScienceBase indique le 2021-08-13 ; usgs.gov indique le 18/08/2021, CC0 et 20 couches. |
| 01 | OFR 2024-1041 : 1/38 504 000, référence 2018 | pubs.usgs.gov | Confirmé | Mis en ligne le 02/07/2024. |
| 01 | Sentinel-2 : depuis le 28/03/2017, revisite 5 j, QA60 masqué du 2022-01-25 au 2024-02-28, L2A 2017–2018 non global | Catalogue GEE | Confirmé | — |
| 01 | Cloud Score+ : seuil 0,50–0,65 | Catalogue GEE | Confirmé | Seuil donné dans un commentaire du script d'exemple. |
| 01 | Copernicus DEM = DSM, remplacé par GLO30_2024_1, 2010–2015, exclusion Arménie/Azerbaïdjan | Catalogue GEE | Confirmé | — |
| 01 | WorldCover v200 : 10 m, 11 classes, CC BY 4.0, classes 50 (bâti) et 80 (eau) | Catalogue GEE | Confirmé | Les pourcentages par zone n'ont pas été recalculés. |
| 01 | S1B : anomalie le 23/12/2021, fin de mission le 03/08/2022 | esa.int (lu par curl) | Confirmé | — |
| 01 | S1C lancé le 05/12/2024 (Partiel) | esa.int, communiqué n° 70–2024 (lu par curl) | Promu → Vérifié | « launched into orbit on 5 December… 22:20 CET ». |
| 01 | ASTER : AST_L1T gratuit depuis le 01/04/2016 ; SWIR inutilisable depuis avril 2008 | earthdata.nasa.gov ; asterweb.jpl.nasa.gov | Confirmé + précision | Le JPL signale aussi des saturations SWIR de fin mai 2007 à fin janvier 2008. Réserve ajoutée. |
| 01 | Programme 2017 : lancé le 24/01, 13 cartes au 1/200 000, 18 000 échantillons, BRGM-BEIG3-GTK, 4,5 Mds FCFA, 30 mois, 6 régions | businessincameroon.com (28/01/2017) | Confirmé | — |
| 01 | 300 nouveaux sites (2014–2019), 5 régions | businessincameroon.com (17/06/2019) | Confirmé | Annonce du ministre Dodo Ndocké. |
| 01 | Geotech, 2,1 Mds FCFA, 160 000 km², 6 régions | businessincameroon.com (23/01/2014) ; PANA | Confirmé | PANA : 80–120 m d'altitude, lignes espacées de 500 m. |
| 01 | « 13.5 new geological 1/200 000 », SIGM, GEO4CAM | BRGM IGF 2018 (PDF) | Confirmé | — |
| 01 | Levé 1970 : Survair, 235 m, lignes N–S à 750 m, Paterson et al. 1976 | Geophysica 2014 (PDF) | Confirmé | — |
| 01 | Étude AMDC : données « du SIGM » pour la plupart obsolètes | financialafrik.com | Rétrogradé (attribution) | L'article ne nomme ni le SIGM ni le PRECASEM. Il parle d'un « système d'information géologique et minérale » couvrant 1929 à aujourd'hui. Les modules 02 et 03 le notaient ; le module 01 ne le faisait pas. |
| 01 | P160917 clôturé le 01/12/2021 (Partiel) | API search.worldbank.org | Promu → Vérifié | Projet parent P122153. |
| 01 | Batouri : granitoïdes de 619–624 Ma (Non vérifié) | pure.kfupm.edu.sa (résumé d'Asaah et al.) | Promu → Vérifié | « concordant ages of 619 ± 2 and 624 ± 2 Ma ». |
| 01 | Batouri : or sous plusieurs mètres de latérite ; 119 ppb Au | rims.gov.bw | Confirmé | 119 ppb dans un horizon latéritique. |
| 01 | Tcholliré : Bougouma, Bandjoukri (primaires), Vaimba (alluvial), éluvial, altérations, ASD 350–2 500 nm, CC BY | PMC10823102 ; DataCite | Confirmé | — |
| 01 | Tcholliré 2022 : ASTER 07XT + Landsat 8 + aéromag ; linéaments NE–SW/ENE–WSW, E–W, N–S | Crossref (résumé gj.4513) | Confirmé | — |
| 01 | Bétaré-Oya : cisaillement NNE–SSW fragile-ductile, altérations | Crossref (résumé gj.3093) | Confirmé | — |
| 01 | Ngoura-Colomines : « Climatic conditions and vegetation constrain… » | Semantic Scholar (résumé 10.1016/j.oregeorev.2020.103530) | Confirmé | — |
| 01 | Dates S2 < 10 % : Z1 43/146 ; Z2 28/146 ; Z3 24/146 | STAC Earth Search (recalcul) | Confirmé / Corrigé (Z2) | Z1 et Z3 sont reproduits exactement. Z2 donne 28 au repère Bétaré-Oya, mais 32 au centre de l'emprise, alors que la méthode annonçait « point central ». Méthode et tableau précisés. |
| 01 | 9 DOI (Ore Geol. Rev. 2020, ASR 2024, JAES 2015, GJ 2022, Acta Geophys. 2023, GJ 2017, NRR 2020, GeoJournal 2019, RSE 2014) | api.crossref.org | Confirmé | van der Meer et al., RSE 148:124-133. |
| 01 | Coordonnées de Tcholliré, Bétaré-Oya et Batouri | API Wikipédia | Confirmé | — |
| 01 | Atlas IRD : PDF de 37 Mo | En-tête HTTP | Confirmé | 37 114 481 octets. |
| 02 | Mbe : 50,60 Mt à 1,02 g/t = 1,66 Moz Inferred ; MB01-S 40,10 Mt à 1,01 g/t = 1,30 Moz ; coupure 0,40 g/t ; 3 200 US$/oz | RNS 6596V (PDF re-téléchargé) | Confirmé | Calcul : 1,659 Moz et 1,302 Moz. |
| 02 | MB01-N : 10,50 Mt à 1,05 g/t = 360 koz | RNS 6596V | Confirmé + note | Le chiffre est dans la source, mais le calcul donne 354 koz : écart d'arrondi signalé. |
| 02 | Mbe : 312 km², « mainly in the Adamawa Region », dans l'Eastern CLP de 2 266 km² | RNS du 20/05/2026 ; RNS 6596V | Corrigé (précision) | Au 22/09/2026, l'Eastern CLP fait 1 954 km² (90 %) et Mbe est présenté séparément. |
| 02 | Mbe et Bibemi : Oriole 50 % / BCM 50 % | RNS 6596V | Confirmé | Au 23/09/2025, Oriole détenait 90 % de Bibemi : la date compte. |
| 02 | Mbe : de l'anomalie de sols à la ressource « entre 2021 et 2026 » | RNS du 20/05/2026 | Corrigé | La source dit « Since 2022 ». L'année 2021 n'était pas sourcée. |
| 02 | Bibemi : 6,96 Mt à 2,06 g/t ≈ 460 koz ; 100 koz Ind. et 360 koz Inf. ; 2 750 US$/oz ; JORC 2012 ; R. Davies | RNS du 23/09/2025 | Confirmé | Calcul : 461 koz. |
| 02 | Bibemi : PEA 89 koz à 2,20 g/t, 10 koz/an, 7 ans, VAN de 12,8 M US$ à 3 200 US$/oz, < 20 % des ressources | RNS 6596V ; share-talk.com | Confirmé | — |
| 02 | Bibemi : EIES approuvée | ecofinagency.com | Confirmé | Validée par le MINEPDED. |
| 02 | Bibemi dans la région du Nord ([F-e]) | ecomatin.net (03/04/2025), relu | Promu → [F] | — |
| 02 | Eastern CLP « Adamaoua/Nord » | RNS 6596V | Rétrogradé → [?] | La source dit seulement « contiguous with the Mbe licence ». |
| 02 | SONAMINES : 353,63 kg (2021) ; 859,92 kg (2022) ; 27,45 Mds FCFA ; 90 % hors circuits formels | ecomatin.net (26/03/2025) ; Rapport ITIE 2023 | Confirmé | Le chiffre de 2022 est recoupé par l'ITIE. |
| 02 | Batouri : 37,3 % (332,2 kg) | ecomatin.net | Confirmé + note | Incohérence interne de la source : 37,3 % de 859,92 kg font 320,8 kg. |
| 02 | 95 % artisanal ; 170,9 kg (2023) ; 420 kg (2023 + S1 2024) ; 122 permis et plus de 1 000 | financialafrik.com | Confirmé | — |
| 02 | P122153 : 30 M US$ ; P160917 : 26,9 M US$ ([F-e]) | API Banque mondiale | Promu → Vérifié | — |
| 02 | Lom : ≈ 310 °C, 6–9 km, mésozonal orogénique | OpenAlex (résumé [L6]) | Confirmé | Salinité d'environ 6,2 % pds éq. NaCl. |
| 02 | Ahafo : 76 % des occurrences dans 24 % de la surface | OpenAlex (résumé [M6]) | Confirmé | Modèle d'indexation multi-critères ; le modèle flou donne 74 % dans 26 %. |
| 02 | 29 DOI de la littérature et de la méthode | api.crossref.org | Confirmé | Titres, revues et années conformes. |
| 02 | Indice de couverture : une cellule sans géochimie ni géophysique plafonne à 0,65 | Calcul interne | Confirmé | 1 − 0,25 − 0,10 = 0,65. En forêt (E6 = 0), les poids ne somment qu'à 0,95 : à normaliser [I]. |
| 03 | Landfolio mis hors service le 03/11/2025 | portals.landfolio.com (redirection vers la page de maintenance) | Confirmé | Message bilingue. |
| 03 | 261 titres actifs (149/11/72/29) ; 952,77 kg d'or, 22,31 kg exportés, 3 305,78 ct | Rapport ITIE 2023 (PDF re-téléchargé) | Confirmé | — |
| 03 | Liste des PEMI : CIMENCAM « PEMI 00008 … arrêté 2023/129 » ; G STONES | Rapport ITIE 2023 | Corrigé | PEMI 00008 correspond à l'arrêté **2023/128**. L'arrêté 2023/129 est un second permis CIMENCAM non numéroté. G STONES est PEMI 00009 dans l'une des listes. |
| 03 | « Impossibilité d'extraire les données sous un format ouvert » | Rapport ITIE 2023 | Confirmé | — |
| 03 | ITIE : suspension par la décision 2024-17 du 29/02/2024, Exigence 1.3, score 53, validation à partir du 01/04/2027, mesure corrective 13 | api.eiti.org ; eiti.org | Confirmé | La page pays date le rapport 2023 au 30/12/2025 ; RFI parle du 10/12/2025. Les deux sont en décembre 2025. |
| 03 | SONAMINES : décret 2020/749 du 14/12/2020 ; statuts 2020/750 ; capital de 10 Mds FCFA ; État actionnaire unique ; exclusivité or et diamant | prc.cm ; osidimbea.cm ; sonamines.cm | Confirmé | Le capital n'apparaît que sur sonamines.cm. |
| 03 | CAPAM : arrêt le 16/10/2021, décision du 05/07/2021, lancé en 2003 | businessincameroon.com (09/07/2021) | Confirmé | — |
| 03 | Kribi-Lobé : juillet 2027 ; 120 sur 420 Mds FCFA ; 42 MW ; 632,8 Mt à 33 % ; 10 Mt/an pour ≈ 4 Mt de concentré ; permis du 01/07/2022 ; 132 km² | ecomatin.net (11/03/2026) | Confirmé | BIC (16/09/2024) donne bien « 1er juillet 2024 » : la discordance signalée est réelle. |
| 03 | Grand Zambi : inauguré le 22/09/2025 ; 6 Mt/an ; 150 Mt ; 600 000 t ; terminal à 14 puis 47,5 Mt/an | ecomatin.net (23/09/2025) | Confirmé | — |
| 03 | Nkamouna et Akonolinga : appels infructueux le 18/08/2026 ; décret 2025/040 du 12/02/2025 ; 121 Mt à 0,23 % Co | businessincameroon.com (21/08/2026) | Confirmé | — |
| 03 | Retrait d'Eramet d'Akonolinga en octobre 2023 (Non vérifié) | businessincameroon.com (21/08/2026) | Promu → Fait vérifié | — |
| 03 | Camalco : 7 locomotives CRRC, participation de 9,1 → 26,9 % (9,852 Mds FCFA), 1re expédition au T4 2026 via Douala, 35 000 t/mois | railwaygazette.com (15/07/2026) | Confirmé | Le chiffre de 35 000 t/mois figure dans Railway Gazette, alors que le module 03 le disait « Non vérifié ». |
| 03 | Mbalam : exportations annoncées pour le T1 2026, transport routier jusqu'en 2029, Lolabé ; aucune confirmation au 07/04/2026 | businessincameroon.com (13/12/2025) ; afrik.com | Confirmé | — |
| 03 | Sentence CCI d'environ 616 M$ en faveur de Sundance | discoveryalert.com ; Reuters via engineeringnews.co.za | Promu → Partiel | Reprise par Reuters d'après la déclaration de Sundance du 26/07/2026. Texte de la sentence non consulté. |
| 03 | Rail Mbalam-Kribi : « double voie » de 540 km ; 149 km au Congo ; paraphé le 25/02/2022 ; comité le 10/07/2025 | bougna.net | Corrigé | La source dit « voie à double sens ». La double voie n'est pas établie. |
| 03 | Colomine : environ 54,5 kg (02/2023–12/2025), extrapolés du prélèvement de 5 % | ecomatin.net (30/06/2026) | Confirmé | — |
| 03 | RFI : 15,2 t déclarées par les importateurs, environ 90 % EAU, 22,3 kg exportés | fr.allafrica.com | Confirmé | — |
| 03 | ZIP USGS de 138 Mo, support de 490 Mo | sciencebase.gov | Corrigé (précision) | ScienceBase affiche 131,74 MB et 467,21 MB. Les chiffres du module correspondent aux unités décimales. |
| 03 | Ports USGS : Douala seul (4 enregistrements, propriétaire ONPC) ; FLNG de Kribi typé « Refinery » ; routes ventilées en 1 716 / 1 632 / 2 884 | gdb | Confirmé | — |
| 03 | Nachtigal : 420 MW, 7 × 60 MW, 1er groupe le 10/05/2024, dernier le 18/03/2025, actionnariat ; Kribi : 35 km au sud, 2,719/9,864 | Wikipédia | Confirmé | Source tertiaire, statut « faible » conservé. |
| 03 | Étude AMDC : « données SIGM » obsolètes | financialafrik.com | Rétrogradé (attribution) | Même problème que dans le module 01. |
| 03 | Geofabrik : données jusqu'au 2026-10-06 | download.geofabrik.de | Source inaccessible | Connexion réinitialisée. |

## 2. Synthèse

**Volume** : 69 affirmations vérifiées (01 : 29 ; 02 : 18 ; 03 : 22).
- 51 confirmées, dont 4 avec une note sur une incohérence ou une précision de la source ;
- 7 corrigées ou précisées dans le texte ;
- 3 rétrogradées (attribution au SIGM dans les modules 01 et 03, région de l'Eastern CLP) ;
- 7 promues après confirmation directe (S1C, P160917, âges de Batouri, région de Bibemi, montants
  Banque mondiale, retrait d'Eramet, sentence Sundance passée en Partiel) ;
- 1 source inaccessible.

Aucun chiffre de ressource minérale, aucune date de statut de projet et aucun DOI ne s'est révélé
faux.

**Erreurs les plus significatives**
1. **Attribution au SIGM** (modules 01 et 03). L'étude AMDC, via Financial Afrik, ne nomme pas le
   SIGM. Présenter « données du SIGM obsolètes » comme fait vérifié était une sur-interprétation,
   alors que le module 02 avait correctement signalé la nuance.
2. **Liste des PEMI** (module 03) : l'arrêté 2023/129 était associé à tort au PEMI 00008, qui
   correspond à l'arrêté 2023/128.
3. **Mbe « depuis 2021 »** (module 02) : année non sourcée ; la source dit 2022.
4. **Eastern CLP** (module 02) : la surface de 2 266 km² est datée et dépassée (1 954 km² au
   22/09/2026). Sa localisation « Adamaoua/Nord » n'était pas sourcée.
5. **Méthode nuages** (module 01) : la zone Z2 n'a pas été calculée au « point central » annoncé.
   Le résultat (28 ou 32 dates sur 146) dépend du point choisi.
6. **Incohérence entre modules** : « 17 installations » (module 01) contre « 13 installations,
   17 enregistrements » (module 03) ; « double voie » sur-traduit (module 03).
7. **Incohérences dans les sources elles-mêmes**, signalées mais non corrigées : Batouri à 37,3 %
   pour 332,2 kg (Ecomatin) ; MB01-N à 360 koz pour un calcul de 354 koz (Oriole).

**Points restés non vérifiés**
- pourcentages WorldCover (pas de recalcul raster) ;
- ratios de Ketté ;
- résumés de [L1], [L2], [L5], [L7] et [L8] (DOI confirmés) ;
- sources Consensus sans DOI ;
- texte de la sentence Sundance.
