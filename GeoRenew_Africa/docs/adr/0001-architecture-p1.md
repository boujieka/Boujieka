# ADR 0001 — Architecture de la phase P1

**Date :** 18/11/2026 · **Statut :** accepté pour P1

## Contexte

Le prototype d'origine et quatre documents de spécification ont été perdus (voir `docs/STATUT_P0.md`).
P1 est construite à partir de `PROMPT_CLAUDE_CODE.md` §III–V et de `CLAUDE.md` §11, qui
recommandent FastAPI, PostGIS, Shapely/pyproj/GDAL, React/TypeScript/MapLibre/React Query, Alembic,
pytest et Playwright, ainsi qu'une option Python locale pour les tests.

## Décisions

1. **Calculs dans Python (Shapely/pyproj), stockage dans PostGIS.** Le moteur est une fonction pure
   (`app.geo.engine.screen_site`), testable sans base et identique quel que soit le stockage. PostGIS
   sert au stockage typé (`geometry(Geometry, 4326)`) et aux index GiST. Il servira aussi aux
   requêtes spatiales à venir (préfiltrage `ST_DWithin` des grandes couches, prévu en P2).
   *Conséquence :* toutes les entités d'une couche sont chargées en mémoire pour chaque analyse ; une
   couche est limitée à 50 000 entités.

2. **SQLite comme option locale.** Le type `GeomType` stocke les géométries en EWKB sous PostGIS et
   en WKB hexadécimal sous SQLite. La même migration Alembic sert aux deux bases. La suite de tests
   tourne par défaut sur SQLite (aucun service externe) et, sur demande, sur PostGIS : elle a été
   exécutée sur les deux pour cette livraison.

3. **Lecture des fichiers par pyogrio (GDAL embarqué dans la roue)** plutôt que par GeoPandas ou
   Fiona : moins de dépendances, et GDAL disponible sans installation système. Le CSV est lu avec le
   module `csv` pour contrôler explicitement les colonnes et le SCR.

4. **Pas de file de tâches (Celery/RQ) en P1.** Les analyses durent quelques millisecondes à
   quelques secondes sur des couches de taille raisonnable. Elles sont synchrones et idempotentes
   (empreinte des entrées). La file sera nécessaire en P2 pour les rasters (MNT, ressources).

5. **Pas d'authentification en P1.** Les tables `organizations` et `users` existent, mais aucun
   contrôle d'accès n'est appliqué. L'en-tête `X-Actor` sert seulement à l'audit, de façon
   déclarative. **La version P1 ne doit pas être exposée hors d'un poste local.** Le Compose publie
   les ports sur 127.0.0.1 uniquement.

6. **Fond de carte OSM tuilé (tile.openstreetmap.org)** pour la démonstration seulement. Il est
   soumis à la politique d'usage d'OSMF, désactivable dans la légende et ne porte aucune donnée
   métier. Un usage en production nécessite un fournisseur de tuiles approprié.

7. **Interface en français par défaut, anglais préparé.** Les libellés d'interface sont dans
   `src/i18n/` ; les valeurs d'énumération de l'API restent en français en P1.

## Écarts par rapport au prompt maître

- Aucun stockage objet S3 en P1 : les fichiers importés ne sont pas conservés, seuls leurs entités,
  leur SHA-256 et leurs métadonnées le sont. Il faudra le faire en P2 si l'archivage des fichiers
  sources est requis.
- Exports GeoPackage et PDF non faits en P1 : le prompt les place en II.2 et II.11, P1 n'exigeant
  que GeoJSON et CSV.
