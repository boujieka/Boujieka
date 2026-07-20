# Déploiement — ATEN

Guide de mise en production de l'application complète (Next.js 14 + PostgreSQL + Prisma).
Trois voies au choix : **Vercel** (le plus simple), **Docker / Docker Compose**, ou **serveur (VPS) manuel**.

---

## 1. Pré-requis communs

- **Node.js 20+** (build & exécution)
- **PostgreSQL 14+** (base de données)
- Les **variables d'environnement** ci-dessous
- Facultatif : une **clé API Claude** (`ANTHROPIC_API_KEY`). Sans elle, les fonctions IA
  (qualification, notes de concept, explications de matching) basculent sur un **repli
  déterministe** — l'application reste pleinement fonctionnelle.

### Variables d'environnement

| Variable | Requis | Rôle |
|---|:---:|---|
| `DATABASE_URL` | ✅ | Chaîne de connexion PostgreSQL |
| `AUTH_SECRET` | ✅ | Secret de signature des sessions JWT — `openssl rand -base64 48` |
| `NEXT_PUBLIC_SITE_URL` | recommandé | URL publique du site (métadonnées Open Graph + image `/opengraph-image`) |
| `ANTHROPIC_API_KEY` | optionnel | Clé Claude — **serveur uniquement**, jamais exposée au client |
| `ANTHROPIC_MODEL_QUALIFICATION` / `_CONCEPT_NOTE` / `_MATCHING` | optionnel | Surcharge des modèles par tâche |
| `NASA_POWER_BASE_URL` | optionnel | Point d'accès NASA POWER (défaut public) |
| `ATEN_PERFORMANCE_RATIO`, `ATEN_BATTERY_ROUND_TRIP`, `ATEN_BATTERY_DOD`, `ATEN_BATTERY_C_RATE` | optionnel | Paramètres physiques par défaut de la simulation |

> ⚠️ **Sécurité** : `ANTHROPIC_API_KEY` et `AUTH_SECRET` sont des secrets **serveur**.
> Ne jamais les préfixer `NEXT_PUBLIC_`. Seul `NEXT_PUBLIC_SITE_URL` est exposé au client
> (c'est une URL publique, sans risque).

Partir de `.env.example` :

```bash
cp .env.example .env
# renseigner DATABASE_URL, AUTH_SECRET, NEXT_PUBLIC_SITE_URL, (ANTHROPIC_API_KEY)
```

---

## 2. Base de données — migrations & amorçage

Le schéma est versionné dans `prisma/migrations/`. En production, on **applique** les
migrations (jamais `migrate dev`) :

```bash
npx prisma migrate deploy      # crée/actualise les tables
npm run db:seed                # (optionnel) référentiels + démo + cas INDUCO
```

`db:seed` insère : les **facteurs d'émission** par pays (focus Afrique centrale), un jeu
de **démonstration** (offtaker / developer / admin) et le **cas d'usage INDUCO**.
Comptes de démo — mot de passe `demo1234` :
`offtaker@aten.demo` · `developer@aten.demo` · `admin@aten.demo` · `induco@aten.demo`

> À ne lancer qu'une fois sur une base de production réelle (le seed est idempotent mais
> crée des comptes de démonstration — à retirer pour un vrai lancement client).

---

## 3. Option A — Vercel (recommandé)

1. **Base managée** : créer une base PostgreSQL chez **Neon**, **Supabase** ou **Vercel Postgres**.
   Pour un runtime serverless, utiliser la **chaîne « pooled »** (PgBouncer/pooler) comme
   `DATABASE_URL` — voir §6 (pooling).
2. **Importer le dépôt** dans Vercel (framework détecté : Next.js).
   - *Build command* : `npm run build` (déjà `prisma generate && next build`).
   - *Install command* : `npm ci`.
3. **Variables d'environnement** (Project → Settings → Environment Variables) :
   `DATABASE_URL`, `AUTH_SECRET`, `NEXT_PUBLIC_SITE_URL` (= l'URL Vercel/domaine),
   et `ANTHROPIC_API_KEY` si utilisée.
4. **Migrations** : Vercel n'exécute pas les migrations au build. Deux approches :
   - **Recommandé** — les appliquer depuis votre poste ou la CI, en pointant sur la base de prod :
     ```bash
     DATABASE_URL="<url_prod_direct>" npx prisma migrate deploy
     ```
   - ou les intégrer au build : `"build": "prisma generate && prisma migrate deploy && next build"`
     (nécessite un accès DB au build — préférer une URL **directe**, non poolée, pour la migration).
5. **Déployer**. `/api/health` doit répondre `{"status":"ok"}`, et l'aperçu de lien afficher
   l'image Open Graph (`/opengraph-image`).

> L'image OG et les routes API fonctionnent nativement sur Vercel (runtime edge pour
> `/opengraph-image`, Node.js pour le reste).

---

## 4. Option B — Docker / Docker Compose

Fichiers fournis : `Dockerfile`, `.dockerignore`, `docker-compose.yml`.

### Pile complète (app + PostgreSQL) en une commande

```bash
echo "AUTH_SECRET=$(openssl rand -base64 48)" >> .env
# (optionnel) echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
docker compose up --build            # app sur http://localhost:3000
docker compose run --rm seed         # (optionnel) amorçage démo + INDUCO
```

L'application applique les migrations au démarrage (`prisma migrate deploy`) puis démarre.
La base est persistée dans le volume `aten_pgdata`.

### Image seule (base gérée ailleurs)

```bash
docker build -t aten .
docker run -p 3000:3000 --env-file .env aten
```

---

## 5. Option C — Serveur (VPS) manuel

```bash
# 1. Pré-requis : Node 20+, PostgreSQL 14+
# 2. Récupérer le code et installer
npm ci

# 3. Configurer
cp .env.example .env      # renseigner les valeurs de prod

# 4. Base
npx prisma migrate deploy
npm run db:seed           # optionnel

# 5. Build + démarrage
npm run build
npm run start             # écoute sur $PORT (3000 par défaut)
```

Mettre derrière un **reverse proxy** (Nginx/Caddy) pour le TLS, et un **gestionnaire de
processus** (systemd ou pm2) pour la résilience :

```bash
pm2 start "npm run start" --name aten
pm2 save && pm2 startup
```

Exemple Nginx (extrait) :
```nginx
location / {
  proxy_pass http://127.0.0.1:3000;
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## 6. Prisma en serverless — pooling de connexions

Sur Vercel (ou tout runtime serverless), chaque invocation peut ouvrir une connexion :
sans pooling, on épuise vite les connexions PostgreSQL. Recommandations :

- Utiliser la **chaîne poolée** du fournisseur pour `DATABASE_URL`
  (ex. Neon *pooled*, ou PgBouncer en mode *transaction*), avec `?pgbouncer=true&connection_limit=1`.
- Pour les **migrations**, une **URL directe** (non poolée) est préférable. On peut, si besoin,
  ajouter un `directUrl` au bloc `datasource` de `prisma/schema.prisma` :
  ```prisma
  datasource db {
    provider  = "postgresql"
    url       = env("DATABASE_URL")   // poolée (runtime)
    directUrl = env("DIRECT_URL")     // directe (migrations)
  }
  ```
  (non activé par défaut pour ne pas alourdir le flux local ; à ajouter selon l'hébergeur.)

---

## 7. Checklist post-déploiement

- [ ] `GET /api/health` → `{"status":"ok","aiConfigured":true|false}`
- [ ] Page d'accueil `/` en 200, image OG visible au partage du lien
- [ ] Inscription puis connexion (offtaker et developer) fonctionnelles
- [ ] Création d'un site + génération d'un profil-type → **lancer la pré-faisabilité**
      (vérifie l'accès sortant à NASA POWER ; repli synthétique sinon)
- [ ] `ANTHROPIC_API_KEY` posée → qualification/note de concept en IA (sinon repli déterministe)
- [ ] `NEXT_PUBLIC_SITE_URL` = domaine réel (aperçus de lien corrects)
- [ ] Pour un vrai lancement : **retirer les comptes de démonstration** créés par le seed

---

## 8. Notes d'exploitation

- **Sauvegardes** : planifier `pg_dump` régulier de la base.
- **Réseau sortant** : la pré-faisabilité appelle `power.larc.nasa.gov` (NASA POWER) et,
  si configurée, l'API Claude. Autoriser ces sorties ; à défaut, la simulation utilise un
  productible synthétique de repli.
- **Journalisation IA** : chaque appel Claude est tracé dans `ai_interactions`
  (traçabilité et maîtrise des coûts).
- **Montée de version du schéma** : créer une migration (`prisma migrate dev` en local),
  la committer, puis `prisma migrate deploy` en production.
