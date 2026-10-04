#!/usr/bin/env bash
# Téléchargement des sources brutes (non commitées) dans $RAW (défaut : ./raw).
# Usage : RAW=/chemin/raw bash 01_telecharger.sh
set -euo pipefail
RAW="${RAW:-./raw}"
mkdir -p "$RAW"
cd "$RAW"

# 1. Extrait OSM Cameroun (miroir openstreetmap.fr ; download.geofabrik.de n'était pas joignable
#    depuis l'environnement de collecte le 2026-10-04).
curl -sS -D osm_headers.txt -o cameroon-latest.osm.pbf \
  https://download.openstreetmap.fr/extracts/africa/cameroon-latest.osm.pbf

# 2. OurAirports (domaine public)
curl -sS -o airports.csv https://davidmegginson.github.io/ourairports-data/airports.csv

# 3. geoBoundaries CMR ADM3 (version figée au commit 9469f09, gbOpen ; servie via Git LFS)
curl -sS -o adm3_meta.json https://www.geoboundaries.org/api/current/gbOpen/CMR/ADM3/
curl -sSL -o adm3.geojson \
  https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/9469f09/releaseData/gbOpen/CMR/ADM3/geoBoundaries-CMR-ADM3.geojson
# contrôle : sha256 attendu = oid LFS 9d0ff998057c3afe7f3a6334d71e9d7c353c64fe6e7c35b01fe14d804c97f04b

# 4. Gridfinder (Arderne et al. 2020, Zenodo 3628142, CC BY 4.0) — fichier mondial de ~725 Mo
curl -sSL -o grid.gpkg https://zenodo.org/api/records/3628142/files/grid.gpkg/content
# contrôle : md5 attendu (Zenodo) = e5d0e9bd8ce4de851e65c6adae1af386

# 5. World Port Index (NGA, Pub. 150, domaine public US) — croisement des ports
curl -sSL -o wpi.csv \
  "https://msi.nga.mil/api/publications/download?type=view&key=16920959/SFH00000/UpdatedPub150.csv" || echo "WPI inaccessible"

sha256sum cameroon-latest.osm.pbf airports.csv adm3.geojson grid.gpkg wpi.csv 2>/dev/null > sha256_sources.txt || true
md5sum grid.gpkg
cat sha256_sources.txt
