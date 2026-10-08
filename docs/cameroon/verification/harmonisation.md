# Journal d'harmonisation inter-modules — Africa Mineral Insights, édition Cameroun

Date : 2026-10-08. Périmètre : modules 01 à 09 de `docs/cameroon/`. Base : `coherence.md` (§ 2, 3, 5
et 6) et rapports `verif-01-03.md`, `verif-04-06.md`, `verif-07-09.md`. Corrections appliquées :
**priorité 1** et **priorité 3** de `coherence.md` § 6. Aucun fait nouveau : chaque correction reprend
un fait déjà vérifié dans un module ou dans un rapport de vérification. Fichiers non modifiés :
`docs/AFRICA_MINERAL_INSIGHTS.md` et les rapports de vérification.

Formulation commune retenue pour Minim-Martap : « Première expédition prévue initialement fin
septembre 2026 (AlCircle, 18/06/2026) puis au T4 2026 (Railway Gazette, 15/07/2026 ; EcoMatin,
24/08/2026) ; reportée sans nouvelle date après la suspension des tirages de la facilité AFG Bank le
24/08/2026 (EcoMatin, 24/08/2026 ; AlCircle, 29/09/2026) ; aucune expédition confirmée au
2026-10-08. »

## 1. Journal des modifications

| Module | Passage | Avant | Après | Justification |
|---|---|---|---|---|
| 01 | En-tête | Pas d'avertissement « pas un conseil » | Avertissement « information et formation, pas un conseil » ajouté | coherence § 5.5 ; consigne |
| 01 | § 4, nouvelle sous-section | — | « Zone et projection communes » : stockage EPSG:4326 ; calcul EPSG:32633 ; emprise nationale ADM0 ; district commun Z2 Bétaré-Oya (13,85–14,35° E ; 5,40–5,85° N) | coherence R1, R2 (priorité 3, n° 10) |
| 01 | § 6.1 Format | « en EPSG:32633 » | Idem + renvoi à la convention commune et copie d'échange en EPSG:4326 | coherence R2 |
| 02 | § 5, ligne Cadastre | « À vérifier (module 03) » [?] | Portail Landfolio hors service depuis le 03/11/2025 ; titres au 31/12/2023 (ITIE, annexe 30) [F, module 03] | coherence G7 ; verif-01-03 (Landfolio confirmé) |
| 02 | § 4.2, Kambélé | Opérateur actuel « non vérifié » | Ajout de l'arrêté du 13/08/2025 interdisant l'exploitation industrielle (module 07, X2, [S39]) | coherence P24 ; fait déjà vérifié en M07 |
| 02 | § 7, choix du district | « Bétaré-Oya / Lom ou Borongo–Mborguéné … cohérente avec l'exercice spectral du module 01 » | District commun retenu = Bétaré-Oya / Lom (Z2 du module 01) ; Borongo–Mborguéné = variante, signalée hors zones du module 01 | coherence R1 (mention erronée) |
| 02 | § 7, nouvelle sous-section | — | « Zone et projection communes » (texte identique aux modules 01 et 03) | coherence R1, R2 |
| 02 | § 8, Projection | « calculs en UTM (fuseaux 32N et 33N) ou projection équivalente » | Échange EPSG:4326 ; calcul EPSG:32633 commun aux modules 01-03 | coherence R2 |
| 03 | En-tête | Pas d'avertissement « pas un conseil » | Avertissement ajouté | coherence § 5.5 ; consigne |
| 03 | § 1, point 6 | « première expédition … visée au T4 2026 » | Formulation commune (fin septembre / T4 2026, reportée sans nouvelle date après le 24/08/2026) | coherence P1 (priorité 1, n° 1) |
| 03 | § 4 (C11) | « 18 000 échantillons / 300 sites » : Non vérifié | Objectif de janvier 2017 (BIC 28/01/2017) ; bilan 2014-2019 annoncé en juin 2019 (BIC 17/06/2019) ; échantillons analysés non vérifiés | coherence G11 ; verif-01-03 (BIC 2017 et 2019 confirmés) |
| 03 | § 5, ligne 8 Minim-Martap | « 1re expédition visée au T4 2026 via Douala » ; date info 2026-07-15 | Formulation commune ; date info 2026-09-29 ; sources EcoMatin et AlCircle ajoutées | coherence P1 |
| 03 | § 5, ligne 21 Alucam | « Statut et capacité actuels : Non vérifié » (USGS 2018) | 100 kt/an (USGS MYB, ASI) ; 53 675 t (2025) ; alumine importée, aucune raffinerie ; Comtrade 2023 : 135 347 t dont 76 655 t de Guinée ; part de l'État « à arbitrer » | coherence A1, A4 ; verif-04-06 |
| 03 | § 5, lignes 24-27 | Absentes | Mbe, Bibemi, Wapouzé, Kambélé ajoutés avec les sources des modules 02 et 07 | coherence R7 (priorité 3, n° 11) |
| 03 | § 7, SCR | « WGS 84 / UTM 32N (EPSG:32632) … à valider » | Stockage EPSG:4326, calcul EPSG:32633 ; UTM 32N abandonné | coherence R2 |
| 03 | § 7, étape 4 | Couche `projets_2026` sans mention des nouvelles lignes | Inclut les lignes 24-27 | coherence R7 |
| 03 | § 7, nouvelle sous-section | — | « Zone et projection communes » | coherence R1, R2 |
| 03 | § 10 Vérification | Minim-Martap « T4 2026 » ; « 18 000 / 300 » Non vérifié | Formulation commune ; chiffres attribués | coherence P1, G11 |
| 03 | § 11, inconnue 7 | « statut actuel … d'Alucam » | « état des cuves d'Alucam (capacité et production : module 05) » | coherence A1 |
| 03 | § 12 Sources | — | AlCircle (18/06 et 29/09/2026), EcoMatin (24/08/2026), RNS Oriole, Share Talk, Ecofin, EcoMatin Kambélé | sources déjà citées dans les modules 02, 05, 06, 07 |
| 04 | § 2, C4 | Cadastre : « Inconnue (état en ligne actuel) » | Portail Landfolio hors service depuis le 03/11/2025 (module 03) ; publication en ligne non obligatoire (décret 05061, art. 110) | coherence G7 |
| 04 | § 9, V32 | « Rapporté ; état actuel inconnu » | Portail hors service depuis le 03/11/2025 (module 03) | coherence G7 |
| 04 | § 10, inconnue 5 | « existence et contenu actuels d'un portail en ligne » | Portail hors service ; reste inconnu : le système de remplacement | coherence G7 |
| 04 | § 11 Sources | — | Page de maintenance Landfolio | source du module 03 |
| 05 | § 1, point 3 ; § 3.2 ; § 8 | « prévues au T4 2026, reportées sine die (24 août 2026) » | Formulation commune ; [S15b] AlCircle 29/09/2026 ajoutée | coherence P1 |
| 06 | § 1, point 4 ; § 5.2 ; § 7.4 ; V21 ; inconnue 2 | « visée fin septembre … reportées sine die » | Formulation commune ; AlCircle 29/09/2026 ajoutée aux sources | coherence P1 |
| 06 | § 2, C7 | « sections 04 et 05 absentes du cadrage » | Supprimé (ligne marquée « supprimé lors de l'harmonisation ») | coherence R13 (affirmation fausse) ; consigne |
| 06 | § 10, V30 | « Incohérent : section 05 absente du cadrage » | Supprimé | coherence R13 |
| 06 | § 9, sortie vers 07 | Notes transmises sans règle de conversion | Règle : M (07) = note 06 arrondie à l'entier ; même note pour un même produit × marché ; B = 1 → M ≤ 2 ; ND ou produit non couvert → jeu de secours du 07 ; conversions listées (bauxite 3, fer 3, aluminium 4, ciment 4, or 5) | coherence R14 (priorité 3, n° 12) |
| 07 | § 2, C9 | Cadastre « en cours d'établissement » (Chambers) ; aucune URL | Portail Landfolio hors service depuis le 03/11/2025 (module 03) ; Chambers conservé comme contexte | coherence G7 |
| 07 | § 2, C10 | « origine de l'alumine : non vérifiée » | 100 kt/an ; alumine importée ; aucune raffinerie ; Comtrade 2023 : 135 347 t dont 76 655 t de Guinée | coherence A1, A4 (priorité 1, n° 2) |
| 07 | § 2, C11 | « cinq décrets (05062, 05248, 05249, 05252, 05253) » | Huit décrets des 18-19/11/2024 (inventaire du module 04) ; art. 47(4) rappelé | coherence G4, G5 |
| 07 | § 3.3 | Aucune règle de conversion M06 → M | Règle de conversion ajoutée et appliquée | coherence R14 |
| 07 | § 3.6 | Règle d'import de l'IOS par le 08 | + score de finançabilité du 08 distinct, affiché à côté de l'IOS, jamais intégré | coherence R20 |
| 07 | O1, Stade | « Calendrier de première expédition retiré sans nouvelle date (septembre 2026) » | Formulation commune (S1, S41, S5) | coherence P1 |
| 07 | O1, Marché et Capex | Clause de 30 % ; divergence 57 / 75 M$ | Marqués « à arbitrer » (priorité 2) | coherence P3, P6 ; consigne |
| 07 | O2, Titulaire | Part de l'État « non vérifiée » | Part « à arbitrer » avec les deux répartitions du module 05 | coherence A3 (priorité 2) |
| 07 | O2, Stade et Ressources | Capacité « non indiquée » ; alumine « non vérifiée » | 100 kt/an (S44, S45) ; alumine importée, aucune raffinerie, Comtrade 2023 (S46) | coherence A1, A4 |
| 07 | O2, Marché ; § 5.2 | M = 3 ; IOS 52 | M = 4 (aluminium → UE 4,2) ; IOS = 180 / 325 × 100 = **55** | coherence R14 (règle de conversion) |
| 07 | O3, Marché ; § 5.1 | M = 4 ; IOS 42 ; poids égaux 43 | M = 3 (fer → Chine 2,85, comme O4 et O5) ; IOS = 200 / 5 = **40** ; poids égaux **40** ; rang 9 inchangé | coherence R14 (même note pour un même produit) |
| 07 | O8, Ressources | « Bibemi : 460 000 oz (indiquées + présumées) » | + 100 koz indiquées / 360 koz présumées, mai 2025, R. Davies | coherence O8 |
| 07 | O8, Capex public | « Non publié (pas de PEA/PFS publiée) » | PEA interne de décembre 2025 (89 koz à 2,20 g/t ; 10 koz/an sur 7 ans ; VAN 12,8 M$ à 3 200 $/oz) [S42, S43] ; capex non repris | coherence P23 (priorité 1, n° 4) ; module 02 § 4.1 ; verif-01-03 |
| 07 | § 5.1, O8 | E = 1 (ND) ; IOS 57 ; poids égaux 60 ; IC 5 ; rang 2= | E = 3 (« Scoping/PEA ») ; IOS = 315 / 5 = **63** ; poids égaux 23 / 35 = **66** ; IC **6** ; rang **2** seul (O9 passe 3ᵉ) | coherence P23 ; calcul affiché dans le module |
| 07 | § 5.3 Lecture | « O8 serait 2ᵉ seul (63) si une PEA… » ; « O1 atteint 6/7 » | Effet de la PEA décrit ; O1 et O8 à 6/7 ; robustesse revérifiée (aucun rang ne bouge de plus de 2 places) | cohérence interne après recalcul |
| 07 | § 7, vers 08 | Pas de mention du retour | Retour = score de finançabilité distinct, jamais intégré à l'IOS | coherence R20 |
| 07 | § 8, V27, V28 ; V31-V33 | 5 décrets ; cadastre « contredit / non confirmé » | 8 décrets ; portail hors service ; nouvelles lignes PEA Bibemi, Alucam, Minim-Martap | coherence G4, G7, P23, A1, A4, P1 |
| 07 | § 9, inconnues 3 et 15 | Origine de l'alumine et capacité d'Alucam inconnues | Origine 2024-2025 et état des cuves seulement ; part de l'État « à arbitrer » | coherence A1, A3, A4 |
| 07 | § 10 Sources | S1-S40 | S41-S46 ajoutées (sources des modules 02 et 05) | traçabilité |
| 08 | § 1, contrainte 3 ; § 2, n° 3 ; § 5 | « option de 25 % supplémentaires » ; « +25 % » | « jusqu'à 25 % supplémentaires, à titre onéreux et d'accord parties (art. 47(4)) » | coherence G5 (priorité 1, n° 5) ; texte du module 04 |
| 08 | § 2, n° 8 | « Décrets … listés par l'USGS (source secondaire, non lus) » | Huit décrets lus par le module 04 (§ 3) | coherence G4, R21 |
| 08 | § 5 | Pas de référence à l'IOS | IOS 69 et IC 6/7 d'O1 importés comme contexte, non re-notés | coherence R20 (a) |
| 08 | § 7, ligne Construction | « 1re expédition prévue au S1 2026, puis au T3, puis au T4 2026, date retirée » | Formulation commune ; « S1 2026 » **conservé** car sourcé par [2] (Business in Cameroon, 26/08/2026), confirmé par verif-07-09 ; sources [44], [45] ajoutées | coherence P1 (la suppression n'était prévue que si la mention n'était pas sourcée) |
| 08 | § 10, retour vers 07 | « score de finançabilité à intégrer à l'IOS » | Score distinct, affiché à côté de l'IOS et de l'IC, jamais intégré ; dépendance à l'infrastructure laissée au critère I du 07 | coherence R20 (b) ; règle 3.6 du module 07 |
| 08 | § 10, retour vers 04 ; § 12, inconnue 6 | « décrets de 2024 » ; « décrets d'application de 2024 non lus » | Décrets lus par le module 04 ; numérotation art. 47 / « Section 59 » « à arbitrer » | coherence G4, G5 |
| 09 | § 2, C3 | Edéa 100 kt/an « selon des listes secondaires » | 100 kt/an vérifiée (USGS MYB, ASI ; module 05) ; alumine importée, aucune raffinerie | coherence A1, A4, R23 |
| 09 | § 2, C7 | « 18 000 échantillons » non vérifié | Objectif de janvier 2017 ; bilan 2014-2019 annoncé en juin 2019 | coherence G11, R23 |
| 09 | § 3.1, textes d'application | « inventaire complet [?] » | 8 décrets des 18-19/11/2024 (module 04) + textes 2025-2026 rapportés | coherence G4, R23 |
| 09 | § 4, Statut ITIE | « suspension annoncée le 1/03/2024 » | Décision 2024-17 du 29/02/2024 (annoncée le 01/03/2024) ; validation à partir du 01/04/2027 | coherence G1 |
| 09 | § 8, indicateur textes d'application | « Inventaire à faire (module 04) » | 8 décrets + arrêté du 15/04/2026 | coherence G4 |
| 09 | § 10 Vérification | 18 000 non vérifié ; Minim-Martap (AlCircle seul) ; Edéa non vérifié | Lignes alignées ; ligne alumine ajoutée | coherence G11, P1, A1, A4 |
| 09 | § 11, inconnues 5-7 | Cadastre, décrets, alumine d'Alucam inconnus | Portail hors service (module 03) ; textes postérieurs aux 8 décrets ; production 2023-2024 et origine 2024-2025 seulement | coherence G4, G7, A2, A4 |
| 09 | § 12 Sources | — | EcoMatin (24/08/2026), BIC (28/01/2017), USGS MYB, ASI, Comtrade | sources des modules 01, 02, 05, 06 |
| 01 à 09 | Section « Contre-vérification (2026-10-08) » | — | Ligne « Harmonisation inter-modules » ajoutée | consigne |

## 2. Points laissés « à arbitrer » (priorité 2 : nouvelle source nécessaire)

- Minim-Martap : ressource (1 102 ou 1 027 Mt), clause de 15 % ou 30 % (marquée en M07, O1), montant
  tiré sur la facilité AFG (57 ou 75 M$, marqué en M07, O1) — P2, P3, P6.
- Part de l'État dans Alucam (marquée en M03 et M07) — A3 ; production d'Alucam 2023-2024 en tonnes — A2.
- Numérotation de l'art. 47 (« Section 59 » dans la DFS ; marquée en M08) — G5.
- Instruction BEAC 001/GR/2026 (« rapatriement » ou « rétrocession »), sanction de 150 %, numéro du
  règlement de 2021 — G9, G10 : non modifiés.
- Exportations d'or (1,897 t contre séries DGD/ITIE) et production industrielle 2023 — O2, O3 : non
  modifiés.
- Grand Zambi (6 ou 1,3 Mt/an), clinker de Figuil, ressources de Nkamouna et date du décret — P14,
  P25, P17, P18 : non modifiés.

## 3. Points de priorité 3 non traités ici

Hors consigne : table de passage des classes de confiance A-D / High-Low (R3), validation par blocs
dès M01 (R4), convention de nommage commune (R5), import des couches 01-02 dans M03 (R6), fiche de
paramètres pour M04 (R9), renvois de M09 vers les livrables au lieu de réécrire les faits (R23, R24,
traités seulement pour les faits de priorité 1). Le cadrage (`AFRICA_MINERAL_INSIGHTS.md`) n'a pas
été modifié.
