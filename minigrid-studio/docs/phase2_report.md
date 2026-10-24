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
| Tests | **88 tests pytest** (dont 22 d'API sur PostgreSQL, 15 d'exports), **7 tests vitest**, et un test **de bout en bout** (Playwright, Chromium) de 21 vérifications : création de projet et de version, calcul, infobulle, 3 exports téléchargés, révision (saisie à la française « 1,3 »), comparaison, lots, bascule EN, invitation et acceptation dans un autre navigateur, approbation par un réviseur, affichage mobile, aucune erreur de console. | `backend/tests/`, `frontend/src/i18n.test.ts`, `frontend/e2e/smoke.mjs` |
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

## 6. Vérification par deux relectures IA indépendantes (24 octobre 2026)

Chaque constat a été reproduit avant correction ; des tests de non-régression ont été ajoutés.

| Relecture | Constats confirmés | Suite donnée |
|---|---|---|
| Sécurité | **Élevé** : déni de service par expression régulière quadratique dans l'export CrossBoundary (un classeur piégé de quelques Ko occupait un processus plusieurs minutes). **Moyens** : injection de formules dans l'export Studio (un nom de lot `=HYPERLINK(…)` devenait une formule) ; un caractère de contrôle dans un nom cassait l'export pour tous. **Faibles** : classeur CrossBoundary corrompu par ces caractères ; nom de projet non latin → erreur 500 au téléchargement ; `NaN`/`Infinity` → erreur 500 ; messages d'erreur internes renvoyés. | Index des cellules en un seul passage (temps linéaire, testé) ; toute cellule non générée est forcée en texte ; caractères de contrôle refusés à la saisie et retirés à l'export ; noms de fichiers ASCII ; nombres finis exigés ; messages génériques. |
| Exactitude | Séparateur de milliers affiché en carré dans les PDF français ; tableau annuel illisible en monnaie locale ; saisie « 1 600,5 » ignorée silencieusement ; unités erronées dans les hypothèses du PDF ; graphique DSCR écrasé par une année à 29x ; libellés de la feuille Hypothèses (sous-champs monétaires, dates) ; traductions manquantes (DSCR négatif, « or », TRI par lot, « derived ») ; détails d'interface (TVA, surlignage des lots, noms en double dans la comparaison, « -0,00 »). Soupçon : séries comparées alignées par position. | Tout corrigé : espace simple ; montants en milliers au-delà de 10⁷ ; analyse des nombres FR/EN avec message d'erreur visible ; unités tirées des métadonnées ; axe du DSCR plafonné à 3 × la cible avec mention « hors échelle » (PDF et écran) ; feuille Hypothèses corrigée (cellule `I` pour la valeur en monnaie locale, dates au format date) ; règles de traduction complétées ; comparaison alignée par année civile. |

Constats non retenus : aucun. Non traité : les nombres restent écrits à l'anglaise (« 0.37x ») à l'intérieur des
messages du moteur traduits.

L'export CrossBoundary a été revérifié après correction par l'outil `tools/phase2/check_crossboundary_export.py`
(5 cas sur 5 identiques, 46 434 cellules, 0 écart) : journal local dans `work/` (non versionné).

## 7. Déploiement Netlify (24 octobre 2026)

Netlify n'exécutant ni Python ni PostgreSQL, le commanditaire a choisi une **démo dans le navigateur** : le moteur
Python tourne dans Pyodide (WebAssembly), les projets et calculs restent dans le navigateur. Publiée sur le site
existant `access360-africa` : https://access360-africa.netlify.app/app/ (lien depuis la page d'accueil).

| Vérification | Résultat |
|---|---|
| Égalité navigateur / serveur | Les 3 046 valeurs des séries annuelles du calcul de démonstration exportées par le navigateur sont **identiques** à celles du moteur serveur (écart nul). |
| Test de bout en bout sur le site en ligne | 12/12 : chargement du moteur (≈ 4,6 s), calcul (TRI 8,11 %), exports .xlsx et .csv, comparaison, conservation après rechargement, anglais, aucune erreur de console sous la politique de sécurité (CSP) de `/app/`. |
| Sécurité | CSP stricte : seulement le site lui-même, `'wasm-unsafe-eval'` requis par WebAssembly ; aucune ressource tierce. |

Limites de la démo : un seul utilisateur, pas de revue à plusieurs, pas d'import de classeur, pas d'export au format
CrossBoundary, PDF par l'impression du navigateur, 40 derniers calculs conservés. Les données sont perdues si le
navigateur efface son stockage.
