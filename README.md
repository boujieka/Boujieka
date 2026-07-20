# ATEN — Le disque solaire

**Plateforme web à deux faces d'origination et de mise en relation pour projets d'énergie renouvelable C&I** (Commercial & Industrial), centrée sur deux objectifs **mesurés** :

- 🌱 **Décarbonisation** — tonnes de CO₂ évitées via le facteur d'émission réseau par pays ;
- 🔌 **Sécurité d'approvisionnement** — taux de couverture de charge, déficit résiduel et coût de la fiabilité, issus d'une simulation horaire.

Auteur du cahier des charges : Emmanuel Boujieka Kamga · Charte visuelle **navy / or / vert**.

---

## Stack technique

| Couche | Choix |
|---|---|
| Framework | **Next.js 14** (App Router, Server Actions, Route Handlers) |
| Langage | **TypeScript** strict |
| Base de données | **PostgreSQL** via **Prisma** (migrations + client typé) |
| Authentification | Sessions **JWT** (`jose`) en cookie httpOnly, mots de passe **bcrypt**, **rôles** offtaker / developer / admin |
| IA | **API Claude** appelée **côté serveur uniquement** (clé en variable d'environnement) |
| Tests | **Vitest** (algorithmes purs) |

## Démarrage

```bash
# 1. Dépendances
npm install

# 2. Variables d'environnement
cp .env.example .env      # renseigner DATABASE_URL, AUTH_SECRET, ANTHROPIC_API_KEY

# 3. Base de données (PostgreSQL requis)
npx prisma migrate deploy   # applique prisma/migrations
npm run db:seed             # facteurs d'émission + jeu de démonstration

# 4. Développement
npm run dev                 # http://localhost:3000
```

Comptes de démonstration (mot de passe `demo1234`) :
`offtaker@aten.demo` · `developer@aten.demo` · `admin@aten.demo`

### Scripts

| Commande | Rôle |
|---|---|
| `npm run dev` / `build` / `start` | cycle Next.js |
| `npm run typecheck` | `tsc --noEmit` |
| `npm test` | suite Vitest |
| `npm run prisma:migrate` | migration de développement |
| `npm run db:seed` | amorçage |

## Déploiement

Voir **[`DEPLOYMENT.md`](DEPLOYMENT.md)** — mise en production sur **Vercel**, **Docker /
Docker Compose** (`Dockerfile`, `docker-compose.yml`) ou **serveur manuel**, avec la liste
des variables d'environnement, l'application des migrations (`prisma migrate deploy`) et le
pooling de connexions Prisma en serverless.

## Architecture des rôles

Trois rôles applicatifs, un middleware d'accès (`src/middleware.ts`) et des garde-fous serveur (`src/lib/auth/guards.ts`) :

- **offtaker** — entreprise consommatrice : sites, courbes de charge, opportunités, pré-faisabilité, suivi CO₂ ;
- **developer** — firme de développement : profil (zones, technologies, taille, track record), appariements, expression d'intérêt ;
- **admin** — opérateur de la plateforme (Aigle Group) : supervision du pipeline et **validation des mises en relation** (modèle intermédié).

La plateforme est **à deux faces sur une même architecture** : offtakers et développeurs partagent les tables `organizations` / `users`, distingués par le rôle.

## Modèle de données

Sept domaines fonctionnels (`prisma/schema.prisma`), fidèles au schéma de référence :

1. **Identité & accès** — `organizations`, `users`
2. **Offtaker** — `sites`, `load_profiles` (8760 pas, stockés en JSONB)
3. **Développeur** — `developer_profiles`, `developer_zones`, `developer_technologies`
4. **Origination** — `opportunities` (pipeline : identifiée → qualifiée → term sheet → mandat → bouclage financier → réalisée / abandonnée)
5. **Analyse** — `prefeasibility_studies`, `techno_economic_models`, `grid_emission_factors`, `decarbonization_metrics`, `bankability_scores`
6. **Mise en relation** — `matches`, `expressions_of_interest`, `messages`
7. **Référence & IA** — `concept_notes`, `ai_interactions`

Conventions : PK UUID, `created_at` / `updated_at`, suppression logique par `deleted_at` sur les entités métier.

## Modules (9)

| # | Module | Emplacement |
|---|---|---|
| 1 | Profils offtakers & sites (charge horaire, criticité, coût des coupures, pipeline) | `app/(app)/sites`, `lib/load-profiles` |
| 2 | Profils développeurs (zones, technologies, taille, track record) | `app/(app)/developers` |
| 3 | **Pré-faisabilité** (productible NASA POWER, simulation horaire, dimensionnement à fiabilité cible) | `lib/simulation`, `lib/nasa-power`, `lib/analysis/run-prefeasibility.ts` |
| 4 | Modèle technico-économique (CAPEX, PPA, TRI, payback) | `lib/techno-economic` |
| 5 | Décarbonisation (tCO₂ évitées, suivi portefeuille) | `lib/decarbonization`, `app/(app)/decarbonization` |
| 6 | Score de bancabilité (avec dimension **résilience**) | `lib/bankability` |
| 7 | **Moteur de matching** pondéré (géographie, taille, hybride, score) | `lib/matching`, `lib/analysis/run-matching.ts` |
| 8 | Expression d'intérêt & messagerie | `lib/actions/interactions.ts` |
| 9 | **API Claude** (qualification, notes de concept chiffrées, explication du matching) | `lib/ai/claude.ts` |

## Les deux algorithmes centraux

Spécifiés dans le document *Logique algorithmique* et implémentés comme **fonctions pures et testées**.

### Dimensionnement à fiabilité cible fixée — `src/lib/simulation`

- `simulate()` : bilan énergétique horaire sur 8760 pas (état de charge batterie, dispatch surplus/déficit, écrêtage). **Fonction pure, réutilisable par les deux régimes de dimensionnement.**
- `sizeToTargetReliability()` : PV fixée par facteur de surdimensionnement *k*, capacité batterie ajustée par **dichotomie** jusqu'à la couverture cible ; *k* incrémenté sinon. Sorties : taux de couverture, déficit résiduel, appoint, **coût de la fiabilité**.
- **Extension réservée** : `optimizeEconomicMix()` (`economic-optimization.ts`) minimise le coût actualisé + valeur des coupures en réutilisant `simulate()` — le champ `simulation_method` distingue les deux régimes **sans modification du schéma**.

### Score de compatibilité du matching — `src/lib/matching`

Quatre dimensions pondérées (géo 0.30, techno 0.30, taille 0.20, bancabilité 0.20) ∈ [0, 1], avec **filtres durs appliqués avant tout calcul pondéré** : hors zone géographique, ou hybride requis sans capacité de stockage → compatibilité nulle.

Les paramètres physiques (ratio de performance, rendement, DoD, C-rate) et les poids de matching sont exposés comme **configuration** (`src/lib/config.ts`), jamais codés en dur.

## API Claude — côté serveur uniquement

La clé `ANTHROPIC_API_KEY` n'est lue que dans `src/lib/ai/claude.ts` (marqué `server-only`), jamais exposée au client. Chaque appel est **journalisé dans `ai_interactions`** (traçabilité et maîtrise des coûts). En l'absence de clé, chaque fonction produit un **repli déterministe** à partir des chiffres déjà calculés — la plateforme reste fonctionnelle.

Trois tâches : qualification d'opportunité, génération de note de concept chiffrée (économie + CO₂ évité + fiabilité), explication des recommandations de matching.

## API REST (extrait)

| Méthode | Route | Effet |
|---|---|---|
| `GET` | `/api/health` | état du service |
| `POST` | `/api/opportunities/:id/prefeasibility` | lance la chaîne de pré-faisabilité |
| `POST` | `/api/opportunities/:id/matching` | exécute le moteur de matching |
| `GET` | `/api/opportunities/:id/matching` | matches classés par score |

## Tests

```bash
npm test
```

Couvrent la simulation horaire (monotonie, bilan, écrêtage), le dimensionnement à cible fixée, l'optimisation économique, le score de matching (filtres durs, sous-scores, classement), le TRI, la décarbonisation et la bancabilité.
