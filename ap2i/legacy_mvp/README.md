# AP²I — MVP Cameroun (v0.1)

Prototype exécutable **sans données inventées**, avec registre de projets, fiches, engagements par bailleur, décaissements annuels, diagnostics déterministes, plans d'action, export et import CSV. API extensible par pays. Interface publique en français.

## Démarrer avec Docker

```bash
cp .env.example .env
# Modifier impérativement les deux secrets dans .env
 docker compose up --build
```

Ouvrir `http://localhost:8000` et `http://localhost:8000/docs`.

## Démarrer en local (SQLite, développement uniquement)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export AP2I_ADMIN_KEY='replace-with-a-long-random-secret'
uvicorn app:app --reload
```

## Importer les projets

Compléter `projects_template.csv` avec des projets **réels, documentés et une URL source par ligne**. Les colonnes `country_code,name,sector,source_url` sont obligatoires à l'import. Les coûts sont saisis dans leur devise d'origine.

```bash
curl -X POST http://localhost:8000/api/import.csv \
 -H "X-Admin-Key: $AP2I_ADMIN_KEY" \
 -F "file=@projects_template.csv"
```

Le CSV est validé en bloc : une ligne erronée annule tout l'import. Pour ajouter un pays : `POST /api/countries` avec code ISO3 et nom. Le Cameroun est initialisé par défaut.

## Limites importantes

- **Pas de connecteur automatique** Banque mondiale/BAD/IATI dans cette version ; les projets doivent être importés et contrôlés manuellement.
- **Pas de connexion utilisateur, ni abonnement, ni véritable isolation multi-tenant** : clé administrateur unique pour l'écriture. Ne pas exposer en production publique sans authentification robuste, RBAC, journal d'audit, contrôle des sources et migrations.
- Les montants ne sont **jamais agrégés entre devises**. Les financements et décaissements sont stockés séparément.
- Le diagnostic Project Rescue est fondé sur des règles simples et **n'est pas une analyse IA**.
- L'export CSV concerne les fiches projets et non encore les décaissements.
- L'interface de consultation fonctionne, mais l'édition et l'import se font via l'API `/docs`.
- L'année de début/fin est une approximation de la période d'activité, pas un historique vérifié des statuts annuels.
- Aucun jeu de données officiel n'est livré ; le tableau de bord initial est vide.

## Suite prioritaire

1. Modèle de données enrichi, Alembic et historiques annuels vérifiés.
2. Authentification, permissions, audit et validation humaine.
3. Connecteurs API vérifiés et provenance par observation.
4. Gestion d'avenants, coûts contractuels, devises et méthodologie de conversion.
5. Interface d'administration et indicateurs de qualité des données.
6. Tests de sécurité et déploiement institutionnel.
