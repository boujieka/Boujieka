#!/usr/bin/env bash
# Téléchargement des sources brutes (non commitées) dans $RAW.
# Usage : RAW=/chemin/vers/raw bash 00_telecharger.sh
set -euo pipefail
RAW="${RAW:-./raw}"
mkdir -p "$RAW"
cd "$RAW"

# 1. Extrait OpenStreetMap du Cameroun (miroir openstreetmap.fr ; ODbL 1.0).
#    download.geofabrik.de était inaccessible depuis l'environnement de collecte
#    (connexion réinitialisée), d'où l'usage de ce miroir.
OSMFR=https://download.openstreetmap.fr/extracts/africa
curl -sS "$OSMFR/cameroon.state.txt" -o cameroon.state.txt
curl -sS "$OSMFR/cameroon.osm.pbf.md5" -o cameroon.osm.pbf.md5
curl -sS "$OSMFR/cameroon.osm.pbf" -o cameroon.osm.pbf
md5sum -c cameroon.osm.pbf.md5

# 2. healthsites.io — export Cameroun publié sur HDX (ODbL).
curl -sSL -o healthsites_cameroon.geojson \
  https://data.humdata.org/dataset/e4ef8126-9d18-48b1-8063-80e924ebbd9f/resource/ac6c9905-e1e9-4be0-b921-e43baa669e25/download/cameroon.geojson
curl -sS -o healthsites_hdx_package.json \
  "https://data.humdata.org/api/3/action/package_show?id=cameroon-healthsites"

# 3. Maina et al. 2019 — établissements de santé publics d'Afrique subsaharienne
#    (figshare 10.6084/m9.figshare.7725374.v1, licence CC0).
curl -sSL -o maina_figshare.xlsx https://ndownloader.figshare.com/files/14379593
curl -sS -o maina_figshare_article.json https://api.figshare.com/v2/articles/7725374
echo "3bf56fc31081c8fd798789a3d70564b8  maina_figshare.xlsx" | md5sum -c

# 4. geoBoundaries CMR ADM3 (gbOpen, commit 9469f09) — utilisé seulement pour la
#    jointure spatiale et le filtre d'emprise ; NON commité.
curl -sS -o gb_meta.json "https://www.geoboundaries.org/api/current/gbOpen/CMR/ADM3/"
# raw.githubusercontent / github.com renvoient vers Git LFS : on lit l'objet LFS.
curl -sSL -o gb_cmr_adm3.geojson \
  https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/9469f09/releaseData/gbOpen/CMR/ADM3/geoBoundaries-CMR-ADM3.geojson

sha256sum cameroon.osm.pbf healthsites_cameroon.geojson maina_figshare.xlsx gb_cmr_adm3.geojson | tee sha256_sources.txt
