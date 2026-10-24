# Mini-Grid Financial Model Studio

Plateforme de préparation financière, contractuelle, ESG et pédagogique pour mini-réseaux africains (ACCESS360 Africa).
Dossier **indépendant** du produit Cartouche hébergé dans le même dépôt.

> **Statut : Phase 1 livrée (moteur, API, base de données).** Le moteur reproduit le classeur CrossBoundary Access
> Open Source Model 1.0 : 46 860 cellules et 920 cellules de tables égales aux valeurs Excel du cas publié (S1), à
> max(10⁻⁹ relatif, 10⁻⁶ absolu) près, et égalité avec les rejeux LibreOffice de S2 à S5 et de 10 scénarios
> fonctionnels, hors TRI glissants `Model!372/429` et trois dates `EOMONTH(0)` (voir `docs/phase1_report.md`).
> Page d'accueil : https://access360-africa.netlify.app Les valeurs étalons **Excel** de S2 à S5 restent à produire
> (`docs/reference_scenarios.md`). Rien ici n'est une certification BAD, Banque mondiale ou CrossBoundary, ni un avis
> juridique ou d'investissement.

## Contenu

| Chemin | Rôle |
|---|---|
| `backend/app/engine/` | Moteur déterministe : hypothèses typées tracées jusqu'aux cellules, calculs, rejeu des macros, options d'amélioration, résultats, rapprochement |
| `backend/app/` | API FastAPI, sécurité, services, modèles SQLAlchemy |
| `backend/alembic/` | Migrations PostgreSQL |
| `backend/tests/` | Tests unitaires, de rapprochement et d'intégration API |
| `frontend/` | Squelette React/TypeScript bilingue (Phase 2 à venir) |
| `docs/audit.md` | Audit Phase 0 du classeur |
| `docs/phase1_report.md` | **Rapport Phase 1** : terminé, non terminé, hypothèses, écarts, risques, prochaines étapes |
| `docs/architecture.md`, `docs/api.md`, `docs/openapi.json` | Architecture et contrat d'API |
| `docs/reference_scenarios.md` | Scénarios de référence et procédure des valeurs étalons Excel |
| `reference/MANIFEST.md` | Sources (non versionnées : droits non vérifiés), empreintes |
| `reference_values/` | Hypothèses et sorties Excel de S1 ; sorties LibreOffice de S1 à S5 |
| `tools/phase0/` | Outils d'audit statique et de rejeu LibreOffice |
| `tools/excel_benchmark/` | Pont Microsoft Excel (xlwings) : valeurs étalons et comparaison au moteur |
| `landing/` | Page d'accueil statique (Netlify) |

## Démarrer

```bash
cd minigrid-studio/backend
python -m venv .venv && .venv/bin/pip install -e '.[dev]'

# Calcul sans base de données
.venv/bin/python -m app.cli --template demo_fictitious --per-lot
.venv/bin/python -m app.cli --template crossboundary_reference --set Inputs!E302=DSCR
.venv/bin/python -m app.cli --template crossboundary_reference --option cap_principal_at_balance

# Si le classeur source est présent dans reference/ : rapprochement cellule par cellule
.venv/bin/python -m app.cli --xlsm ../reference/CrossBoundary-Access-Open-Source-Model-1.0-October-2023.xlsm --reconcile

# API + PostgreSQL (voir ../.env.example)
export MGS_DATABASE_URL=postgresql+psycopg://mgs:...@localhost:5432/mgs
.venv/bin/alembic upgrade head
MGS_DEMO_ADMIN_EMAIL=you@example.org MGS_DEMO_ADMIN_PASSWORD='a long passphrase' .venv/bin/python -m app.demo.seed
MGS_EXPOSE_DOCS=true .venv/bin/uvicorn app.main:app --port 8000   # documentation interactive : http://localhost:8000/docs

# Front-end (squelette)
cd ../frontend && npm install && npm run dev          # http://localhost:5173 (proxy /api vers :8000)
```

## Tests

```bash
cd minigrid-studio/backend
sudo scripts/test_db.sh                              # PostgreSQL 16 jetable sur le port 55432 (facultatif)
MGS_TEST_DATABASE_URL=postgresql+psycopg://mgs:mgs@127.0.0.1:55432/mgs_test .venv/bin/python -m pytest
cd ../frontend && npm test && npm run build
```

Sans `MGS_TEST_DATABASE_URL`, les tests d'API sont ignorés. Sans le classeur source dans `reference/` et sans les
exports LibreOffice de `work/` (non versionnés), les rapprochements cellule par cellule sont ignorés aussi ; le
rapprochement des indicateurs et séries, sur les valeurs versionnées dans `reference_values/`, s'exécute toujours.
L'intégration continue (`.github/workflows/minigrid-studio.yml`) lance pytest sur PostgreSQL 16, l'aller-retour
Alembic, vitest et le build.

## Principes

- **Fidèle par défaut.** Chaque amélioration (`/api/v1/engine/options`) est désactivée par défaut. L'activer marque le résultat `variant`.
- **Traçable.** Chaque indicateur et chaque série nomme sa cellule ou sa ligne Excel. Les indicateurs sans équivalent Excel sont marqués `derived`, le calcul par lot `experimental`.
- **Séparé de l'IA.** Le moteur n'appelle aucun service externe ni modèle génératif.
