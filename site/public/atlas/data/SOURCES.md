# Sources des données SIG

- Source : Natural Earth, jeux vectoriels 1:10m (https://www.naturalearthdata.com/).
- Téléchargement : https://naciscdn.org/naturalearth/10m/ (cultural : admin_0_countries, admin_1_states_provinces, airports, ports, railroads, roads, populated_places_simple ; physical : lakes).
- Licence : domaine public (https://www.naturalearthdata.com/about/terms-of-use/). Attribution non requise, citée par courtoisie.
- Version des fichiers (admin_0_countries) : 5.1.1
- Généré le : 2026-10-04 par site/gis_build.py.
- Traitement : rattachement par intersection spatiale avec la frontière (marge 0,1 degré pour les points), lignes découpées à la frontière, longueurs géodésiques WGS84, coordonnées arrondies à 3 décimales, géométries simplifiées.

## Limites

- Échelle 1:10m : généralisation forte, les tracés ne conviennent pas à la mesure précise ni à la navigation.
- Couverture inégale selon les pays et les couches (routes et chemins de fer = réseaux principaux seulement ; certains pays n'ont aucune entité sur une couche).
- Aucune garantie de données récentes : Natural Earth est mis à jour de façon irrégulière.
- Les longueurs sont celles des tracés généralisés, pas des réseaux réels.
- Les frontières suivent les choix cartographiques de Natural Earth (de facto), sans portée juridique.
- Pour les grands pays, des villes peu peuplées peuvent être omises pour respecter le budget de taille ; le compteur "cities" indique le nombre total.
