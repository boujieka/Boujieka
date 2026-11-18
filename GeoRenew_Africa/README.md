# GeoRenew Africa — phase P1

Plateforme web de **screening géospatial préliminaire** pour projets solaires PV, éoliens et BESS en
Afrique. **Résultats indicatifs, non bancables.**

> **Origine.** Le kit de démarrage (v0.1, 18/11/2026) comportait un prototype (`geo_engine.py`, front
> Leaflet) et quatre documents (`CAHIER_DES_CHARGES`, `SOURCES_DONNEES`, `METHODES_ET_CALCULS`,
> `BACKLOG_ET_RECETTE`). **Ils n'ont pas été reçus et le prototype est déclaré perdu par le
> propriétaire.** P1 a été reconstruite de zéro à partir de `PROMPT_CLAUDE_CODE.md` et `CLAUDE.md`.
> Aucun calcul de l'ancien prototype n'a donc pu être comparé ni préservé.

État détaillé, tableau de conformité et limites : [`docs/P1_RAPPORT.md`](docs/P1_RAPPORT.md).
Méthode de calcul : [`docs/METHODES_P1.md`](docs/METHODES_P1.md).
Choix d'architecture : [`docs/adr/0001-architecture-p1.md`](docs/adr/0001-architecture-p1.md).

## En ligne

Interface : https://georenew-africa.netlify.app — **API pas encore branchée** (voir
[`docs/DEPLOIEMENT.md`](docs/DEPLOIEMENT.md)).

## Démarrer — commande unique (Docker Compose)

```bash
cd GeoRenew_Africa
docker compose up --build
```

- Interface : http://localhost:8080
- API et documentation OpenAPI : http://localhost:8001/docs
- Base : PostgreSQL 16 + PostGIS 3.4 (volume `pgdata`). Au démarrage, l'API applique les migrations
  et charge le **projet de démonstration (DONNÉES FICTIVES)**.

Derrière un proxy TLS d'entreprise, fournir son certificat à la construction :
`docker build --secret id=extra_ca,src=chemin/ca.crt …` (voir les `Dockerfile`).

## Option locale Python (sans Docker, sans serveur de base de données)

Prérequis : Python 3.11+ (testé en 3.13), Node 20+ (testé en 22).

```bash
cd GeoRenew_Africa
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements-dev.txt

# Tests backend (SQLite temporaire, aucun service externe)
cd backend && PYTHONPATH=. pytest -q && cd ..

# Front : dépendances, contrôle de types, tests unitaires, build
cd frontend && npm ci && npm run typecheck && npm test && npm run build && cd ..

# Application complète servie par FastAPI (SQLite dans backend/var/)
cd backend
alembic upgrade head
python -m app.demo load              # projet de démonstration FICTIF (facultatif)
uvicorn app.main:app --port 8000     # http://127.0.0.1:8000 (front construit inclus)
```

Développement du front avec rechargement : `cd frontend && npm run dev` (port 5173, `/api` relayé
vers le port 8000).

Tests sur PostGIS plutôt que SQLite (base dédiée, vidée à chaque test) :
`GEORENEW_TEST_DATABASE_URL=postgresql+psycopg://user@host/base_test PYTHONPATH=. pytest -q`

Test de bout en bout (navigateur, Playwright) contre une instance en marche avec la démo chargée :
`cd frontend && GEORENEW_URL=http://127.0.0.1:8000 node e2e/smoke.mjs`

## Structure

```
backend/   FastAPI, SQLAlchemy 2, Alembic, Shapely/pyproj/pyogrio (GDAL)
  app/geo/       moteur de screening, SCR, validation, import de fichiers
  app/api/v1.py  API REST /api/v1
  alembic/       migrations (PostGIS + index GiST ; compatibles SQLite)
  tests/         moteur (cas de référence), import, API, stockage, démo
frontend/  React 18 + TypeScript + Vite + MapLibre GL + React Query ; e2e/ (Playwright)
examples/demo_fictive/  GeoJSON FICTIFS de la démonstration
docs/      rapport P1, méthode, ADR, inventaire P0, README d'origine archivé
```

## Règles de prudence appliquées

- Surfaces et longueurs mesurées en UTM (WGS 84), jamais en EPSG:4326/3857 ; contrôle géodésique.
- Chaque valeur est étiquetée **renseigné / calculé / hypothétique / inconnu** ; aucune valeur inventée.
- Aucun buffer « réglementaire » fourni par le logiciel : chaque buffer exige une justification de
  l'utilisateur, conservée dans l'analyse.
- « Foncier vérifié » et « raccordement confirmé » exigent une pièce du bon type, non fictive.
- Chaque analyse conserve l'instantané de ses entrées, leur empreinte SHA-256, les versions des
  données et du moteur ; une relance identique réutilise le résultat (idempotence).
- L'**authentification n'est pas implémentée** : ne pas exposer cette version hors d'un poste local.
