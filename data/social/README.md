# Infrastructures sociales — Cameroun

Collecte du 2026-10-04. Toutes les entités ont `statut = IMPORTE` : ce sont des assertions
de sources publiques, **non validées**. Traçabilité complète (URL, licence, sha256, méthode,
limites, contrôles) dans [`manifest.json`](manifest.json).

| Fichier | Source | Licence | Entités |
|---|---|---|---|
| `sante/etablissements_sante_osm.geojson` | OpenStreetMap (extrait openstreetmap.fr, 2026-10-03) | ODbL 1.0 | 2 106 |
| `sante/etablissements_sante_healthsites.geojson` | healthsites.io via HDX (dérivé d'OSM, 2026-09-15) | ODbL 1.0 | 1 990 |
| `sante/etablissements_sante_publics_maina2019.geojson` | Maina et al. 2019, figshare (secteur public) | CC0 1.0 | 3 019 |
| `sante/rapprochement_sources_sante.csv` | dérivé des 3 couches santé | ODbL 1.0 | 5 101 lignes |
| `education/etablissements_education_osm.geojson` | OpenStreetMap | ODbL 1.0 | 5 011 |
| `services/mairies_osm.geojson` | OpenStreetMap | ODbL 1.0 | 290 |
| `services/marches_osm.geojson` | OpenStreetMap | ODbL 1.0 | 378 |
| `synthese_par_arrondissement.csv` | comptes par arrondissement (geoBoundaries ADM3) | ODbL 1.0 | 8 643 lignes |

Attribution : © les contributeurs d'OpenStreetMap ; healthsites.io ; Maina J. et al. (2019),
*Scientific Data* 6:134 ; geoBoundaries (wmgeolab).

## Mises en garde
- **Aucune couche n'est exhaustive.** Dans OSM, 176 arrondissements sur 360 n'ont aucun
  établissement de santé et 120 aucune école. Un zéro veut dire « rien dans la source ».
- **Ne pas additionner les sources santé** : elles se recouvrent. healthsites.io est une copie
  d'OSM (99,9 % de ses entrées ont le même identifiant OSM) : ce n'est pas une confirmation indépendante.
- Maina 2019 : secteur public seulement, situation 2019, coordonnées souvent au niveau du village.
  Avec le seuil imposé de 500 m, seuls 25 de ses établissements sont retrouvés dans OSM ; à 2 km,
  161 le sont (voir `manifest.json`) : le recouvrement réel est sous-estimé.
- Classement `tg_type` : en partie déduit du nom (champ `classement_regle` = `tag+nom`) ;
  `null` quand rien ne permet de classer (valeurs brutes conservées).
- Doublons internes **signalés** (champ `doublon_interne_suspect`), jamais supprimés.
- Les limites ADM3 geoBoundaries ne sont pas commitées ici. Leur licence est **ODbL 1.0**
  (et non CC BY 4.0).

## Reproduire
```bash
pip install geopandas pyogrio shapely osmium rapidfuzz pyarrow openpyxl
export RAW=/chemin/hors/depot
bash scripts/00_telecharger.sh
cd scripts && for s in 01_osm_extraire 02_couches 03_rapprochement_sante 04_synthese 05_manifest; do python3 $s.py; done
```
Un nouveau téléchargement donnera un extrait OSM plus récent, donc des comptes différents.
