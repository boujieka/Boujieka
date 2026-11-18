# Déploiement — interface sur Netlify, API ailleurs

**État au 18/11/2026**

| Élément | État |
|---|---|
| Interface (React) | ✅ en ligne : https://georenew-africa.netlify.app (projet Netlify `georenew-africa`) |
| API FastAPI + PostGIS | ❌ **non déployée**. L'interface affiche « API GeoRenew non configurée » |

Netlify ne sert que des fichiers statiques et des fonctions JavaScript/Go : il ne peut pas exécuter
l'API Python ni la base PostGIS. Celles-ci doivent être hébergées ailleurs. Netlify relaie ensuite
`/api/*` vers elles, si bien que le navigateur ne parle qu'au domaine Netlify et qu'aucun réglage
CORS n'est nécessaire.

## ⚠ Avant de brancher une API publique

La version P1 **n'a pas d'authentification**. Une fois l'API branchée, **toute personne qui connaît
l'URL peut créer, modifier et supprimer** des projets, des données, des règles et des analyses.
Il faut donc soit ajouter l'authentification (première tâche prévue pour P2), soit restreindre
l'accès au site, par exemple avec la protection par mot de passe ou la connexion d'équipe de
Netlify. Ces fonctions dépendent du forfait Netlify, que je n'ai pas vérifié.

## Étapes pour brancher l'API

1. **Base de données.** PostgreSQL 16 avec l'extension PostGIS 3. La migration exécute
   `CREATE EXTENSION IF NOT EXISTS postgis` : l'hébergeur doit l'autoriser.
2. **API.** Déployer l'image construite par `GeoRenew_Africa/backend/Dockerfile`, avec
   `GeoRenew_Africa/` comme contexte de construction (le Dockerfile copie `backend/` et `examples/`),
   sur un hébergeur qui exécute des conteneurs Docker et expose un point HTTPS.
   - Variable obligatoire : `GEORENEW_DATABASE_URL=postgresql+psycopg://UTILISATEUR:MOT_DE_PASSE@HOTE:5432/BASE`.
     Elle se définit comme secret chez l'hébergeur, jamais dans le dépôt.
   - Au démarrage, le conteneur applique les migrations, charge le projet de démonstration FICTIF
     et écoute sur le port 8000.
   - Vérification : `https://VOTRE-API/api/v1/health` doit renvoyer `{"status":"ok",…}`.
3. **Netlify.** Dans le projet `georenew-africa`, définir la variable d'environnement
   `GEORENEW_API_ORIGIN=https://VOTRE-API`, sans chemin ni barre finale, puis relancer un déploiement.
   Le script `frontend/scripts/netlify-redirects.mjs` génère alors la règle
   `/api/*  https://VOTRE-API/api/:splat  200`.
4. **Contrôle.** Ouvrir https://georenew-africa.netlify.app : le portefeuille doit afficher le
   projet de démonstration. Le test de bout en bout peut aussi tourner contre le site :
   `GEORENEW_URL=https://georenew-africa.netlify.app node frontend/e2e/smoke.mjs`. Attention, ce test
   **crée des données** (un projet, un site, une règle) dans la base de production.

## Points non vérifiés

- Les limites du relais Netlify (durée maximale d'une requête relayée, taille des fichiers envoyés)
  n'ont pas été mesurées. Les imports volumineux (l'API accepte jusqu'à 50 Mo) pourraient dépasser
  ces limites ; il faudrait alors les tester.
- Aucun hébergeur d'API n'a été choisi ni testé : les étapes 1 et 2 sont génériques.

## Redéployer l'interface

Le site n'est pas relié au dépôt Git : chaque déploiement est manuel. Il a été fait par l'outil
Netlify de la session, qui téléverse `GeoRenew_Africa/frontend` sans `node_modules` ni `dist`, puis
construit sur Netlify avec `npm run build:netlify` (voir `frontend/netlify.toml`). Pour automatiser,
il faut relier le projet Netlify au dépôt GitHub avec le dossier de base `GeoRenew_Africa/frontend`.
