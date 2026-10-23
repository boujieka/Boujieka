# Mini-Grid Financial Model Studio

Plateforme de préparation financière, contractuelle, ESG et pédagogique pour mini-réseaux africains, réalisée pour ACCESS360 Africa. Ce dossier est **indépendant** du produit Cartouche hébergé dans le même dépôt.

> **Statut : Phase 0 (audit) terminée, en attente de la décision S0.** Aucun moteur de calcul, API ni interface n'existe encore. Aucun résultat ne doit être présenté comme validé : le moteur web n'a passé aucun rapprochement avec le classeur Excel. Rien ici ne constitue une certification BAD, Banque mondiale ou CrossBoundary, ni un avis juridique.

## Contenu

| Chemin | Rôle |
|---|---|
| `docs/audit.md` | Rapport d'audit : inventaire, conventions, macros, cycles, fonctions délicates, observations, questions bloquantes. |
| `docs/variable_dictionary.csv` | Dictionnaire des entrées, sélecteurs, valeurs collées, lignes calculées et sorties du classeur. |
| `docs/formula_dependency_map.md` | Carte des dépendances et boucles rompues par macro. |
| `docs/row_dependencies.csv` | Lignes dont dépend chaque ligne de formules. |
| `docs/reference_scenarios.md` | Scénarios de référence, procédure des valeurs étalons Excel, tolérances. |
| `reference/MANIFEST.md` | Empreintes, provenance et droits des documents sources. Les sources ne sont **pas** versionnées. |
| `reference_values/` | Valeurs Excel de S1 ; valeurs LibreOffice provisoires de S1 à S5 (contrôle, pas étalon). |
| `tools/phase0/` | Scripts d'analyse statique et de recalcul de contrôle. |

## Reproduire la Phase 0

Prérequis : placer les sources dans `reference/` (voir le manifeste), Python 3.11 ou plus, et LibreOffice avec son pont UNO Python (pour le recalcul de contrôle uniquement).

```bash
python -m venv .venv && .venv/bin/pip install -r tools/phase0/requirements.txt
X=reference/CrossBoundary-Access-Open-Source-Model-1.0-October-2023.xlsm

# Macros : extraction statique, jamais d'exécution
.venv/bin/olevba --decode "$X"

# Dictionnaire, dépendances ligne à ligne, statistiques (écrit docs/*.csv et work/)
.venv/bin/python tools/phase0/inventory.py "$X" .

# Valeurs Excel en cache (S1)
.venv/bin/python tools/phase0/extract_cached.py "$X" reference_values/S1_base_excel_cached.json

# Recalcul de contrôle LibreOffice avec rejeu des macros en Python (S1 à S5)
python3 tools/phase0/lo_scenarios.py "$X" tools/phase0/scenarios.json work/lo_out
.venv/bin/python tools/phase0/compare_outputs.py reference_values/S1_base_excel_cached.json work/lo_out/S1_base_libreoffice.json
```

## Prochaine étape

Décision S0 : réponses aux questions de `docs/audit.md` §9 (droits, valeurs étalons Excel, cible de rapprochement, observations, lots, rémunération OSA). La Phase 1 (moteur, tests, API, PostgreSQL) ne démarrera qu'après cette décision.
