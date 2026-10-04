# Collecte « admin » : limites administratives et localités du Cameroun

Prérequis : Python 3.11, `pip install geopandas shapely pyproj pyogrio osmium`.
Exécuter depuis la racine du dépôt, dans l'ordre :

```sh
python3 data/admin/scripts/01_telecharger.py        # sources brutes -> data/admin/.cache/ (non commité), sha256
python3 data/admin/scripts/02_limites.py            # limites_adm{0..3}.geojson + comparaison_ocha_geoboundaries.csv
python3 data/admin/scripts/03_localites.py          # localites_osm.geojson
python3 data/admin/scripts/04_tableau_et_manifest.py # unites_administratives.csv + manifest.json
```

Les sources « latest » (OSM, HDX) évoluent : une nouvelle exécution donnera des sha256 et des comptes différents.
Tout est documenté dans `../manifest.json`.
