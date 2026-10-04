#!/usr/bin/env bash
# Téléchargement des sources brutes (NON commitées) dans $RAW (défaut : ./raw_population).
# Usage : RAW=/chemin/temp bash data/population/scripts/01_telecharger.sh
set -euo pipefail
RAW="${RAW:-./raw_population}"; mkdir -p "$RAW"; cd "$RAW"

# 1. WorldPop Global2 R2025A v1, constrained, 100 m (CC BY 4.0) — métadonnées via l'API REST
curl -sS -o worldpop_R25A_100m_CMR.json "https://hub.worldpop.org/rest/data/pop/G2_CN_POP_R25A_100m?iso3=CMR"
curl -sS -o worldpop_licence.txt "https://hub.worldpop.org/data/licence.txt"
for y in 2025 2026; do
  curl -sS -O "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/$y/CMR/v1/100m/constrained/cmr_pop_${y}_CN_100m_R2025A_v1.tif"
done

# 2. geoBoundaries gbOpen CMR ADM3 (commit 9469f09) — limites des arrondissements (ODbL 1.0, dérivé d'OSM)
curl -sS -o api_ADM3.json "https://www.geoboundaries.org/api/current/gbOpen/CMR/ADM3/"
curl -sSL -o gb_adm3.geojson "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/9469f09/releaseData/gbOpen/CMR/ADM3/geoBoundaries-CMR-ADM3.geojson"

# 3. Seconde source pour le total national : ONU, World Population Prospects 2024 (CC BY 3.0 IGO)
curl -sS -o wpp2024_demo.csv.gz "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz"

# 4. Atlas forestier interactif du Cameroun (MINFOF/WRI), paquet SIG 2018 (CC BY 4.0) :
#    sert uniquement à rattacher chaque arrondissement à son département et sa région.
curl -sS -O "http://wri-sites.s3.amazonaws.com/forest-atlas.org/cmr.forest-atlas.org/resources/gdbs/cmr_data_sans_documents_2018.rar"
unrar x -o+ cmr_data_sans_documents_2018.rar >/dev/null

sha256sum *.tif gb_adm3.geojson wpp2024_demo.csv.gz cmr_data_sans_documents_2018.rar
