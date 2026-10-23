# Scénarios de référence et procédure des valeurs étalons (étape D)

## 1. Scénarios retenus

Chaque scénario active un chemin de calcul distinct du classeur. La définition exécutable est dans `tools/phase0/scenarios.json`.

| ID | Modifications par rapport au fichier publié | Chemins exercés | Valeurs étalons Excel | Valeurs LibreOffice (contrôle) |
|---|---|---|---|---|
| **S1_base** | Aucune | Gearing 50 %, DSRA, MMRA, taux fixe, cas de consommation 3, USD | **Oui** : valeurs mises en cache dans le fichier (`reference_values/S1_base_excel_cached.json`) | Oui, identiques à 6×10⁻¹⁵ près |
| **S2_dscr_sizing** | `Inputs!E302 = "DSCR"` | Dette dimensionnée sur le DSCR, boucle de la macro `Debt_Sizing` | **Non, à produire** | Provisoires |
| **S3_local_currency** | `Currency!F18 = 2` | Montants en LCY, indices de change, reconversion des TRI en USD, arrondi des macros à −7 | **Non, à produire** | Provisoires (11 tours de macros) |
| **S4_refinancing** | `Inputs!G336 = 1` (refinancement en 5ᵉ année de maturité) | Refinancement, macro `Refi_Debt_Sizing` | **Non, à produire** | Provisoires |
| **S5_phased_stress** | Construction sur 3 ans `Inputs!I135:K135 = 0,4 / 0,3 / 0,3` ; tarif −20 % `Inputs!G170 = −0,2` ; cas de consommation 1 (plateau) `Inputs!E432 = 1` | Achats étalés, tirages successifs, extension, diesel, pertes fiscales, injection de fonds propres | **Non, à produire** | Provisoires |

Fonctions **sans scénario** à ce stade : arrivée du réseau national, valeur de sortie, BFR, TVA non nulle, taux variable, lots désactivés, ordre de tirage « Equity first ». Elles ne pourront pas être publiées comme validées (protocole, étape F) tant qu'un scénario Excel ne les couvre pas.

## 2. Procédure de calcul des valeurs étalons sous Excel (environnement maîtrisé)

À faire exécuter par une personne habilitée, sur un poste Windows ou macOS avec Microsoft Excel de bureau, version à consigner.

1. Copier le fichier de référence. Vérifier son empreinte : `fe0ecb160b294120e3135dfce6bacf619246bff1ed85944e06b6c44c0c4bb33e` (SHA-256).
2. Ouvrir la copie avec les macros **désactivées**, puis vérifier dans *Fichier > Options > Formules* que le calcul est **automatique** et que le calcul itératif est **désactivé**.
3. Saisir les modifications du scénario (tableau ci-dessus), et elles seules.
4. Activer les macros pour **ce fichier uniquement**. Les seules macros présentes sont les 4 procédures auditées (`docs/audit.md`, section 1).
5. Exécuter la procédure du classeur :
   1. `Debt_Sizing` (bouton « Model Solver », `Inputs!I302`) ;
   2. si `Inputs!G336 = 1`, `Refi_Debt_Sizing` (bouton `Inputs!I346`) ;
   3. `DSRA_resize_3` (bouton « DSRA Size ») ;
   4. recommencer les étapes 1 à 3 jusqu'à ce que `Inputs!N292`, `N300`, `N344` et `E373` valent tous 0.

   Noter le nombre de tours. Si une macro ne s'arrête pas après 2 minutes, l'interrompre (Échap) et consigner la non-convergence.
6. Enregistrer sous `S<n>_<id>_excel.xlsx`, sans macros, puis calculer son SHA-256.
7. Extraire les valeurs avec `python tools/phase0/extract_cached.py S<n>_<id>_excel.xlsx reference_values/S<n>_<id>_excel.json S<n>_<id>`.
8. Consigner dans `reference_values/LOG.md` : opérateur, date, version d'Excel, nombre de tours, empreintes des fichiers d'entrée et de sortie.

Les valeurs collées (`G292`, `G300`, `G344`, `E372`) sont enregistrées dans chaque fichier de résultat (`pasted_values`). Le moteur web pourra ainsi être rapproché **à valeurs collées identiques**, ce qui neutralise la tolérance des macros (audit §4).

## 3. Rejeu de contrôle sous LibreOffice (déjà exécuté, non étalon)

```bash
python3 tools/phase0/lo_scenarios.py reference/CrossBoundary-Access-Open-Source-Model-1.0-October-2023.xlsm \
        tools/phase0/scenarios.json work/lo_out
python3 tools/phase0/compare_outputs.py reference_values/S1_base_excel_cached.json work/lo_out/S1_base_libreoffice.json
```

Le script :
- réécrit les `OFFSET` à largeur négative dans une copie de travail ;
- ouvre cette copie sans macros ;
- applique les modifications du scénario ;
- rejoue les macros en Python, à partir de leur source audité, jusqu'à ce que les contrôles de dimensionnement soient nuls ;
- extrait les sorties définies dans `tools/phase0/outputs_spec.json`.

Les résultats sont dans `reference_values/provisional_libreoffice/`. Ils servent à détecter un écart grossier entre Excel et LibreOffice quand les valeurs Excel arriveront. **Ils ne servent pas d'étalon.**

## 4. Tolérances de rapprochement proposées (à approuver en S0)

| Grandeur | Tolérance | Justification |
|---|---|---|
| Montants (flux, soldes, totaux) | 0,1 % relatif, ou 0,001 unité monétaire en absolu sous 1 unité | Cahier des charges §6 ; bruit flottant de l'ordre de 10⁻¹⁰ observé. |
| TRI, taux, ratios | 1×10⁻⁴ en absolu (0,01 point) | Le solveur XIRR diffère d'un logiciel à l'autre (écart observé de 2,4×10⁻⁹). |
| Drapeaux, contrôles, compteurs, délai de récupération | Égalité exacte | Valeurs discrètes. |
| Valeurs dépendant des macros (dette, financement, DSRA) | 0,1 % **à valeurs collées identiques**. En résolution exacte : écart documenté, jusqu'à 0,34 % observé sur la capacité DSCR. | Tolérance de convergence des macros : ±50 000 unités, asymétrique. |

`tools/phase0/compare_outputs.py` applique les trois premières lignes.

## 5. Ratios dérivés sans équivalent Excel

Le DSCR annuel effectif (CFADS ÷ service de la dette senior) **n'est pas calculé par le classeur**. Dérivé des séries de S1, il vaut :
- 0,83 en 2024 (année de grâce, écart couvert par la DSRA) ;
- 1,20 de 2025 à 2034 ;
- 1,47 en 2035 (dernière échéance).

Ces valeurs ne peuvent être « rapprochées » d'Excel. Seules leurs composantes, CFADS et service de la dette, le sont.
