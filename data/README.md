# Données réelles TasetyGrid — Cameroun (collecte du 4 octobre 2026)

Collectées par quatre agents (une session par thème), puis **auditées et chargées indépendamment**
dans le schéma `schema/schema_postgis.sql`. Règles : [CONVENTIONS.md](CONVENTIONS.md) ·
Audit fichier par fichier : [AUDIT.md](AUDIT.md) · Sources et licences : `*/manifest.json`.

**Statut de toutes les données : `IMPORTE`** (aucune n'est validée par une administration).

## Contenu

| Thème | Couches | Entités | Sources principales (licence) |
|---|---|---|---|
| Limites | ADM0, 10 régions, 58 départements, 360 arrondissements | 429 | OCHA COD-AB (CC BY-IGO), comparé à geoBoundaries |
| Localités | villes, villages, quartiers | 12 739 | OpenStreetMap (ODbL) |
| Santé | 3 sources séparées + table de rapprochement | 2 106 / 1 990 / 3 019 | OSM (ODbL), healthsites.io, Maina et al. 2019 (CC0) |
| Éducation, services | écoles, mairies, marchés | 5 011 / 290 / 378 | OSM (ODbL) |
| Infrastructures | routes par classe, rail, gares, ponts, ports, aéroports, centrales, lignes, barrages, points d'eau, antennes | 21 107 | OSM (ODbL), OurAirports, World Port Index |
| Ressources | UFA et forêts communales, forêts communautaires, aires protégées, permis miniers | 1 026 | Atlas forestier MINFOF/WRI 2018 (CC BY 4.0) |
| Population | estimation par arrondissement 2025-2026 | 360 lignes | WorldPop R2025A (CC BY 4.0), comparée à l'ONU WPP 2024 |
| Occupation du sol | hectares par classe et par arrondissement | 360 lignes | ESA WorldCover 2021 (CC BY 4.0) |

## Contrôles passés
- 10 / 58 / 360 unités administratives ; superficie calculée 466 544 km² (identique à OCHA à 0,2 km² près).
- 0 objet à plus de 5 km hors des frontières ; géométries valides ; sha256 conformes aux manifestes.
- Population WorldPop 2025 : 29,5 millions, soit 1,3 % sous l'estimation ONU au 1er juillet 2025.
- Somme de l'occupation du sol = surface classée (466 372 km²).
- Aucun champ de données personnelles détecté ; postes électriques volontairement non publiés (prudence).

## Limites connues (à lire avant tout usage)
1. **Complétude OSM inégale** : ex. 0 établissement scolaire cartographié à Mfou ; le Nord-Ouest compte
   seulement 488 localités OSM contre 2 300 pour le Centre. L'absence d'un objet ne prouve pas son absence réelle.
2. **Doublons entre sources santé** : les trois couches se recouvrent ; utiliser `rapprochement_sources_sante.csv`
   avant de compter (ex. 91 objets santé à Garoua 1er, toutes sources confondues).
3. **Population = estimation modélisée**, pas un recensement ; les résultats du 4ᵉ RGPH 2026 ne sont pas publiés.
   16 arrondissements n'ont pas pu être rapprochés par le nom (limites geoBoundaries ≠ OCHA) : à recalculer
   par statistiques zonales sur les limites OCHA.
4. **Atlas forestier MINFOF 2018** : 7 à 8 ans d'ancienneté ; les permis miniers ont pu changer (Code minier 2023).
5. 2 573 objets sans code de nomenclature (type source conservé dans l'assertion).
6. Anomalie OSM signalée : une localité « Bamenda » marquée *city* près de Pitoa (Nord), à vérifier.

## Recharger
```bash
createdb tasetygrid && psql -d tasetygrid -f schema/schema_postgis.sql
pip install psycopg[binary] pyyaml shapely
python3 data/scripts/charger_postgis.py postgresql:///tasetygrid   # ~25 s, 46 867 objets
python3 data/scripts/audit.py                                      # régénère AUDIT.md
```
