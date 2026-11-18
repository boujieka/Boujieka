# GeoRenew Africa — état P0 (inventaire)

**Date :** 18 novembre 2026
**Emplacement :** sous-dossier `GeoRenew_Africa/` du dépôt `boujieka/Boujieka` (option b choisie par
le propriétaire). Ce sous-dossier est indépendant du projet Cartouche situé à la racine du dépôt :
aucun code, document ni donnée n'est partagé entre les deux.

## Fichiers reçus (copiés à l'identique)

| Fichier | SHA-256 |
|---|---|
| `README.md` | `4078b7b48527b03d83c5d909a0bdfb80477e91886a90c5542bcad5a946a59450` |
| `PROMPT_CLAUDE_CODE.md` | `a9faa4326813a0a1c4c796cfe28af3d3389a87276fe9d20f94e70bea827975af` |
| `CLAUDE.md` | `bd7dec82ded2527e270d3d1819ffd184855b14ab18994fe4881143c16f8538ac` |

## Fichiers cités par le kit mais NON reçus

| Fichier / dossier | Rôle | Conséquence |
|---|---|---|
| `docs/CAHIER_DES_CHARGES.md` | Périmètre produit | Périmètre P1 connu seulement par le résumé du prompt maître |
| `docs/SOURCES_DONNEES.md` | Sources, licences | Aucun connecteur de données ne peut être cadré |
| `docs/METHODES_ET_CALCULS.md` | Formules et contrôles | Aucune formule ne peut être implémentée « conforme » |
| `docs/BACKLOG_ET_RECETTE.md` | Phases, tests, recette | Critères de recette P1 détaillés inconnus |
| `backend/` (dont `app/geo_engine.py` et ses tests) | Calculateur validé à préserver | **Bloquant** : impossible de garantir la préservation des calculs |
| `frontend/` | UI Leaflet du MVP | Inventaire UI impossible |
| `examples/` | Jeux de démonstration | Tests de référence indisponibles |

## Matrice existant / manquant

| Fonctionnalité (selon README du kit) | Déclarée dans le kit | Présente dans ce dépôt | Testée ici |
|---|---|---|---|
| Import GeoJSON | implémentée | non (code non reçu) | non |
| Carte et tracé de polygones | implémentée | non | non |
| Exclusions dures / indicatives | implémentée | non | non |
| Buffer de recul de parcelle | implémenté | non | non |
| Surfaces en projection UTM | implémentées | non | non |
| MWp DC indicatif (densité paramétrée) | implémenté | non | non |
| API FastAPI + tests | implémentés | non | non |
| Tout le périmètre P1 (PostGIS, multi-projets, import multi-format, persistance, exports, React) | à construire | non | non |

## Prochaine étape

Dès réception de l'archive complète du kit :
1. copier `docs/`, `backend/`, `frontend/`, `examples/` dans ce sous-dossier en vérifiant les empreintes ;
2. exécuter `PYTHONPATH=. pytest -q` dans `backend/` et enregistrer les résultats comme tests de référence ;
3. démarrer P1 en refactorisant `geo_engine.py` sans modifier ses résultats.
