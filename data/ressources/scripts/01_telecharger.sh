#!/usr/bin/env bash
# Téléchargement des sources brutes (NON commitées) dans $RAW (défaut : ./raw_ressources).
# Usage : RAW=/chemin/temp bash data/ressources/scripts/01_telecharger.sh
set -euo pipefail
RAW="${RAW:-./raw_ressources}"; mkdir -p "$RAW/wc"; cd "$RAW"

# 1. Limites des arrondissements : geoBoundaries gbOpen CMR ADM3 (commit 9469f09, ODbL 1.0)
curl -sSL -o gb_adm3.geojson "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/9469f09/releaseData/gbOpen/CMR/ADM3/geoBoundaries-CMR-ADM3.geojson"

# 2. ESA WorldCover 10 m 2021 v200 (CC BY 4.0) — 20 tuiles de 3°x3° couvrant le Cameroun (~1,6 Go)
for la in N00 N03 N06 N09 N12; do for lo in E006 E009 E012 E015; do
  f=ESA_WorldCover_10m_2021_v200_${la}${lo}_Map.tif
  curl -sS -o "wc/$f" "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/$f"
done; done

# 3. Atlas forestier interactif du Cameroun (MINFOF/WRI) : paquet « Cameroun données SIG sans
#    documents (2018) », dernier paquet complet publié avec une licence explicite (CC BY 4.0).
#    Fiche : https://www.arcgis.com/home/item.html?id=7e8925d7feb9439ca3f5754759f226ba
curl -sS -o item_fa_2018.json "https://www.arcgis.com/sharing/rest/content/items/7e8925d7feb9439ca3f5754759f226ba?f=json"
curl -sS -O "http://wri-sites.s3.amazonaws.com/forest-atlas.org/cmr.forest-atlas.org/resources/gdbs/cmr_data_sans_documents_2018.rar"
unrar x -o+ cmr_data_sans_documents_2018.rar >/dev/null

sha256sum gb_adm3.geojson cmr_data_sans_documents_2018.rar wc/*.tif > sha256_sources.txt
