# Rapport Phase 1 — moteur, API, base de données

*24 octobre 2026. Décision du commanditaire (23/10) : « Reproduire le modèle tel quel en l'améliorant, puis lancer la Phase 1 ». Interprétation retenue : reproduction fidèle par défaut ; chaque amélioration est une option explicite, désactivée par défaut, et tout résultat qui en utilise une est marqué `variant`.*

## 1. Terminé

| Élément | État | Preuve |
|---|---|---|
| Moteur déterministe (Python) | Reproduit les feuilles Currency, Portfolio, Inputs, Model, Debt et FinStat ligne à ligne, ainsi que les indicateurs du tableau de bord. | `backend/app/engine/` |
| Rapprochement avec Excel (S1) | **46 860 cellules calculées et 920 cellules de tables égales aux valeurs Excel** mises en cache dans le classeur publié (écart relatif ≤ 1×10⁻⁹). Toutes les lignes de calcul de la chronologie et tous les résultats sont couverts. Seuls les libellés, recopies de paramètres et lignes de la feuille Graph ne le sont pas. | `tests/test_reconcile_workbook.py`, `python -m app.cli --xlsm … --reconcile` |
| Rapprochement S2 à S5 | Égalité cellule par cellule avec les exports LibreOffice. **Les macros rejouées convergent vers les mêmes valeurs collées** que le rejeu LibreOffice. Écarts exclus et documentés : TRI glissants négatifs (LibreOffice renvoie 0) et `Inputs!J364` (date « 0 » lue différemment par LibreOffice). | `tests/test_engine_fixtures.py`, `tests/test_reconcile_workbook.py` |
| Solveur | Rejeu des macros `Debt_Sizing`, `Refi_Debt_Sizing` et `DSRA_resize_3` (par défaut), ou point fixe exact (variante). | `solver.py` |
| Améliorations (options) | 5 options, chacune testée : date de début d'exploitation, taux fixe par année de maturité, taux de base « 2023+ », principal plafonné au solde, coût de racking des extensions. | `options.py`, `tests/test_options_and_solver.py` |
| Sorties complémentaires | DSCR annuel, DSCR minimum, moyen et en période de grâce, LLCR, TRI non endetté avant impôt (avec et sans subvention), alerte de covenant. Marqués `derived`. | `results.py` |
| Calcul par lot | TRI projet de chaque lot calculé seul, comme le demande le PSA « Asset Transfer ». Marqué `experimental` : aucune référence Excel. | `results.lot_irrs` |
| Validation des saisies | Erreurs bloquantes là où le classeur afficherait `#DIV/0!` ou `#N/A`, et avertissements. | `validation.py` |
| API FastAPI | Authentification ; organisations et rôles (admin, analyste, réviseur, investisseur) ; projets ; versions immuables avec parent et changements ; règle des quatre yeux ; calculs ; export CSV ; import `.xlsm` sans exécution de macros ; journal d'audit. | `docs/api.md`, `docs/openapi.json` |
| PostgreSQL | Schéma multi-organisations ; migration Alembic testée dans les deux sens ; triggers rendant le journal d'audit en ajout seul et les versions non réécrivables. | `alembic/versions/0001_initial_schema.py` |
| Tests | **43 tests pytest**, dont 11 d'intégration API sur PostgreSQL 16 réel (isolation entre organisations, rôles, quatre yeux, immuabilité, upload, limitation des connexions), et 2 tests vitest. Tous passent. | `backend/tests/`, `frontend/src/i18n.test.ts` |
| Données de démonstration | Portefeuille **fictif** « Fictitia » (valeurs inventées). Aucun mot de passe par défaut. | `app/demo/templates/demo_fictitious.json`, `python -m app.demo.seed` |
| Squelette web React/TS | Connexion, projets, versions, calcul, indicateurs avec leur source et leur statut, alertes ; FR/EN. | `frontend/` |

## 2. Non terminé (prévu)

- **Interface Phase 2** : saisie structurée des hypothèses, sites et lots, tableaux et graphiques, comparaison de scénarios, export Excel avec formules auditables et PDF. Le squelette actuel n'est qu'un point d'entrée.
- **Valeurs étalons Excel pour S2 à S5** : elles exigent la procédure de `docs/reference_scenarios.md` sous Microsoft Excel. Elles n'ont pas été produites, faute d'Excel dans cet environnement.
- **Intégration continue** : non configurée, pour ne pas toucher la configuration partagée du dépôt. Les tests se lancent localement (voir le README).
- Contract Studio, Learning Academy, Investment Studio, ESG et Capital Connect (Phases 3 à 5).

## 3. Hypothèses retenues

1. La cible de rapprochement est l'état Excel **avec** la tolérance des macros (même procédure, mêmes valeurs collées de départ). Le solveur exact est une variante.
2. Les droits de réutilisation commerciale des documents CrossBoundary ne sont toujours pas vérifiés. Le gabarit `crossboundary_reference` (hypothèses du cas publié) est fourni pour le rapprochement, avec une mention dans l'API. Le gabarit par défaut est fictif.
3. Le calcul par lot fait tourner le modèle sur le lot seul, financement redimensionné compris. C'est **une** façon de définir un « TRI par lot » ; elle reste à valider.
4. Le DSCR dérivé rapporte le CFADS (`Model!291`) au service de la dette senior et refinancée (`Model!305:311`).

## 4. Écarts au modèle Excel

Avec les options par défaut et le solveur des macros, il n'y a **aucun écart** sur les cellules couvertes de S1. L'égalité avec LibreOffice tient sur S2 à S5, aux deux exclusions documentées près. Les écarts n'apparaissent que si l'on active une option ou le solveur exact : le résultat porte alors le statut `variant` et la liste des options activées.

**Observations nouvelles relevées en reproduisant le classeur** (elles complètent `docs/audit.md`, section 7) :

| Cellule | Constat | Vérifié par |
|---|---|---|
| `Debt!43` | Le taux fixe est recherché avec le drapeau de maturité, qui vaut toujours 1. Seul le taux de la période 1 s'applique, même si l'on saisit des taux par période. | Test (`test_fixed_rate_by_year`) |
| `Debt!32` | Le principal n'est pas plafonné au solde. Avec un DSCR cible de 0,6, le solde senior tombe à −7,36 M. | Test (`test_principal_cap_prevents_negative_debt`) |
| `Debt!102` | Le principal maximal du refinancement n'a pas de plancher à 0 (pas de `MAX(…, 0)`, contrairement à `Debt!60`). | Lecture de formule |
| `Dashboard!K52` | Le contrôle « MMRA end balance » lit la colonne V (2035) codée en dur. Il ne suit pas la maturité saisie. | Lecture de formule |
| `Model!37` | La consommation propre « kWh/grid/day » est multipliée par le nombre de modules (kW de PV ÷ taille d'un module d'extension), pas par le nombre de réseaux. | Lecture de formule |
| `Model!645` | La ligne racking du coût d'extension est vide, alors que `Inputs!E120` (2 500 par module) entre dans le total affiché `Inputs!E122`. | Test (option `include_expansion_racking`) |
| `Debt!139` | L'interrupteur MMRA ne s'applique au solde minimal que dans la première colonne. | Lecture de formule |
| Démo fictive | Le DSCR dérivé descend à 0,37 x une année de remboursement en mode gearing. Le classeur n'a aucun test de covenant ; le moteur émet désormais une alerte. | Calcul |

## 5. Risques

- **Fidélité ≠ justesse.** Le moteur reproduit aussi les anomalies du classeur (section 4). Les options correctives doivent être revues par un expert financier avant usage décisionnel.
- **Validation Excel incomplète** : seul S1 est rapproché d'Excel lui-même ; S2 à S5 ne le sont que de LibreOffice.
- **Droits** sur les gabarits et données CrossBoundary : non clarifiés.
- **Limitation des connexions en mémoire** : elle ne couvre qu'un processus. En déploiement multi-instance, il faudra une limitation partagée.
- **Chiffrement au repos et TLS** : ils relèvent de l'infrastructure de déploiement, qui n'est pas encore définie.

## 6. Prochaines étapes

1. Produire les valeurs étalons Excel de S2 à S5 (procédure prête), puis les verser dans `reference_values/`.
2. Arbitrer chaque option d'amélioration : rester variante ou devenir le comportement par défaut d'un « modèle v2 ».
3. Valider ou modifier la définition du TRI par lot et du DSCR dérivé.
4. Phase 2 : interface bilingue complète, exports Excel avec formules et PDF.
5. Mettre en place l'intégration continue (pytest sur PostgreSQL, vitest, build) quand la configuration partagée du dépôt pourra être modifiée.
