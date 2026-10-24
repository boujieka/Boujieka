# Rapport Phase 2 — interface bilingue et exports

*24 octobre 2026. Demande du commanditaire : « Lancer la Phase 2 ». Périmètre du cahier des charges : « interface
bilingue FR/EN : création de projet, hypothèses, sites/lots, tableaux financiers, graphiques, comparaison de
scénarios, alertes, export Excel et PDF. Authentification, rôles et journal d'audit. »*

## 1. Terminé

| Élément | État | Preuve |
|---|---|---|
| Interface web FR/EN | Connexion, acceptation d'invitation, projets (création, archivage, restriction), versions (gabarit ou import `.xlsm`), éditeur d'hypothèses par groupe (146 champs, libellés FR/EN, unité, cellule du classeur, recherche, mise en évidence des modifications), sites et lots (1 à 6), options d'amélioration et solveur, calcul, résultats, comparaison, administration. Bascule FR/EN à tout moment. Mise en page mobile sans défilement horizontal. | `frontend/src/` |
| Résultats | Indicateurs clés, alertes (icône + libellé, jamais la couleur seule), 4 graphiques (survol et clavier, légende, libellés directs, vue tableau), tableaux annuels (exploitation, compte de résultat, trésorerie et dette, bilan) avec cellule source, tableau complet des indicateurs, contrôles du classeur. | `pages/Run.tsx`, `components/LineChart.tsx` |
| Comparaison | 2 à 4 calculs, écarts par rapport au premier (en points pour les taux), séries clés superposées, hypothèses qui diffèrent. | `POST /compare`, `pages/Compare.tsx` |
| Workflow et rôles | Soumission, revue (quatre yeux affichés à l'auteur et au soumetteur), statut des versions, profil investisseur limité aux versions approuvées, administration des membres, invitations (lien à usage unique), rôles, retrait, journal d'audit consultable. | `pages/Version.tsx`, `pages/Admin.tsx` |
| Export Excel « Studio » | Valeurs du moteur avec leur cellule source, et **formules Excel vivantes** qui recalculent les identités comptables, le DSCR, le TRI projet (`XIRR`) et la VAN (`XNPV`, taux lu dans la feuille des hypothèses), avec une colonne d'écart. Recalcul vérifié **sous LibreOffice** : écarts nuls (≤ 1,5×10⁻¹¹). | `app/exports/xlsx_studio.py`, `tests/test_exports.py` |
| Export au format CrossBoundary | L'utilisateur fournit **sa** copie du classeur ; seules les cellules d'hypothèses et les 4 valeurs collées sont réécrites dans le XML ; formules, graphiques, styles et macros sont conservés octet pour octet ; Excel recalcule à l'ouverture. Le fichier n'est pas stocké. Refus motivé si le scénario exige de changer des formules (base de change, TVA, lots hérités) ou si le calcul est une variante. | `app/exports/crossboundary.py` |
| Vérification de cet export | Démo fictive et S2 à S5 : classeur rempli, puis recalculé par LibreOffice **sans rejouer les macros** : 46 434 cellules comparées, **0 écart**, et les 4 contrôles de dimensionnement des macros valent 0 (les valeurs collées du moteur sont des points fixes acceptés par le classeur). Aller-retour des hypothèses : identique. | `tools/phase2/check_crossboundary_export.py`, `tests/test_exports.py` |
| Rapport PDF | FR/EN : identification et statut, alertes, indicateurs avec source, 4 graphiques, synthèse annuelle, contrôles, hypothèses principales, lots ; pagination. | `app/exports/pdf_report.py` |
| Libellés | Une seule source FR/EN côté serveur (`GET /engine/labels`), utilisée par l'interface et les exports ; messages du moteur traduits par règles. | `app/exports/labels.py` |
| Tests | **85 tests pytest** (dont 21 d'API sur PostgreSQL, 13 d'exports), **5 tests vitest**, et un test **de bout en bout** (Playwright, Chromium) de 21 vérifications : création de projet et de version, calcul, infobulle, 3 exports téléchargés, révision, comparaison, lots, bascule EN, invitation et acceptation dans un autre navigateur, approbation par un réviseur, affichage mobile, aucune erreur de console. | `backend/tests/`, `frontend/src/i18n.test.ts`, `frontend/e2e/smoke.mjs` |
| Intégration continue | Nouveau job `e2e` (PostgreSQL, API, Vite, Chromium). | `.github/workflows/minigrid-studio.yml` |

## 2. Non terminé

- **Validation sous Microsoft Excel** des deux exports : les formules du classeur Studio et le classeur CrossBoundary
  rempli n'ont été recalculés que par LibreOffice. Excel est le logiciel de référence ; à vérifier sur un poste Excel
  (ouvrir le fichier, constater les écarts nuls et les contrôles `Inputs!N292`, `N300`, `N344`, `E373` à 0).
- **Export DOCX** (cité dans le cahier des charges, section exports) : non fait ; PDF seulement.
- **Graphiques dans l'export Excel** : non ; les graphiques sont dans l'interface et le PDF.
- **Changer la base de change, la classe de TVA ou rétablir l'héritage d'un lot** dans le classeur CrossBoundary :
  refusé plutôt que deviné (il faudrait réécrire des formules).
- **Lots au-delà de 6** : non pris en charge (format du classeur, colonnes E à J).
- Contract Studio, Learning Academy, Investment Studio (Phases 3 à 5).

## 3. Hypothèses retenues

1. « Export Excel avec formules auditables » est servi de deux façons : (a) un classeur Studio dont les formules
   recalculent ce qui peut l'être à partir des séries exportées ; (b) le classeur CrossBoundary complet, rempli à partir
   d'une copie fournie par l'utilisateur, pour ne pas redistribuer nous-mêmes le fichier de CrossBoundary.
2. Le DSCR minimum et moyen n'ont pas de formule dans l'export Studio : ils dépendent d'un indicateur d'années de
   remboursement non exporté. Pas de formule plutôt qu'une formule fausse.
3. Les pourcentages sont saisis en fraction (0,45 = 45 %), comme dans le classeur ; l'éditeur affiche l'équivalent.
4. Le jeton de session reste dans `sessionStorage` (effacé à la fermeture de l'onglet).

## 4. Écarts au modèle Excel

Aucun nouvel écart : la Phase 2 n'a pas modifié les calculs. Trois séries ont été ajoutées aux résultats pour
permettre les formules d'audit (`period_end` = `Model!5`, `npv_cash_flow` = `Model!369`, `irr_cash_flow` = `Model!371`)
et une série dérivée (`debt_service`). Les calculs déjà enregistrés ne les contiennent pas : leur export Studio
omet simplement les formules correspondantes.

## 5. Risques

- Validation Excel des exports non faite (voir section 2).
- La limite de 6 lots peut être insuffisante pour de grands portefeuilles.
- Le test de bout en bout dépend d'un navigateur ; il n'a pas encore tourné dans GitHub Actions.
- Droits : inchangés (voir rapport de Phase 1, section 7). L'export CrossBoundary n'utilise que le fichier de
  l'utilisateur.
