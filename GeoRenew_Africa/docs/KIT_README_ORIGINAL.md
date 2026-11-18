> **Archive.** README du kit de démarrage v0.1, conservé à l'identique pour traçabilité. Le prototype qu'il décrit (`backend/app/geo_engine.py`, front Leaflet) a été **perdu et n'a jamais été reçu** ; la phase P1 a été reconstruite de zéro. État réel : voir `../README.md` et `P1_RAPPORT.md`.

# GeoRenew Africa — kit de démarrage pour Claude Code

**Version :** 0.1 · 18 novembre 2026  
**Origine :** descriptif fourni par l'utilisateur, *GIS Specialist – Renewable Energy Projects* (annonce localisée à Johannesburg, Afrique du Sud).  
**Cible proposée :** plateforme SIG et technico-économique multi-pays pour l'Afrique, avec méthodes configurables par pays et par projet.

## Ce qui est fourni

1. `PROMPT_CLAUDE_CODE.md` — prompt maître à transmettre à Claude Code.
2. `CLAUDE.md` — règles persistantes du projet pour Claude Code.
3. `docs/CAHIER_DES_CHARGES.md` — spécifications fonctionnelles et non fonctionnelles.
4. `docs/SOURCES_DONNEES.md` — catalogue de données et contraintes d'utilisation.
5. `docs/METHODES_ET_CALCULS.md` — spécifications calculatoires et règles de prudence.
6. `docs/BACKLOG_ET_RECETTE.md` — plan d'implémentation, tests et critères de recette.
7. `backend/` + `frontend/` + `examples/` — **MVP exécutable de screening géospatial** (pas une plateforme complète).

## Démarrer le MVP existant

Prérequis : Python 3.11+ et accès Internet pour charger les dépendances de carte du front-end (Leaflet) et, si souhaité, les tuiles de démonstration OSM.

```bash
cd GeoRenew_Africa_Claude_Code
python -m venv .venv
source .venv/bin/activate                  # Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --app-dir backend --reload --port 8000
```

Puis ouvrir `http://127.0.0.1:8000/`.

**Fonctions déjà implémentées :** import GeoJSON, affichage cartographique, tracé de polygones, exclusions dures / indicatives, buffer de recul de parcelle, calcul de surfaces en projection métrique UTM, estimation *strictement indicative* de MWp DC selon densité paramétrée, API FastAPI et tests.

**Fonctions non implémentées :** cadastre réel, analyse de relief sur MNT, accès automatique aux réseaux, téléchargement de données solaires, modèle PV horaire, modèle éolien, dispatch BESS, étude financière, PDF/Word/Excel, authentification, stockage PostGIS, géométrie de corridors, audit trail persistant. Ces fonctionnalités sont décrites pour construction par Claude Code.

### Tester le moteur actuel

```bash
cd backend
PYTHONPATH=. pytest -q
```

### Lancer Claude Code sur ce dossier

```bash
cd GeoRenew_Africa_Claude_Code
claude
```

Ouvrir `PROMPT_CLAUDE_CODE.md` et donner son contenu à Claude Code, ou demander :

> Lis CLAUDE.md, PROMPT_CLAUDE_CODE.md et tous les documents de `docs/`. Commence la phase P1 décrite dans le backlog, exécute les tests et documente ce qui fonctionne réellement.

## Conventions de qualité

- Chaque résultat doit mentionner **source, millésime, résolution spatiale, licence, projection, paramètres et niveau de confiance**.
- Aucun réseau, limite de parcelle ou statut environnemental fictif ne doit être affiché comme réel.
- L'application ne doit jamais assimiler un *screening* à une étude de faisabilité bancable.
- Les propriétés et parcelles ne doivent être déclarées vérifiées que sur preuves foncières officielles ou relevés qualifiés.
- Un jeu de données avec conditions d'utilisation restrictives n'est pas intégré au logiciel commercial sans permission/licence appropriée.

## Licence du kit

Les fichiers de code et documents créés pour ce kit sont fournis à l'utilisateur pour modification et adaptation. Les licences des bibliothèques et données externes restent régies par leurs propres conditions.
