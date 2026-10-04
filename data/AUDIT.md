# Audit des données TasetyGrid

Généré par `data/scripts/audit.py`. Contrôles : présence, sha256, comptes, emprise Cameroun, validité des géométries, licence, champs de traçabilité, champs possiblement personnels.

| Fichier | Entités / lignes | Taille | Contrôles | Licence |
|---|---|---|---|---|
| admin/limites_adm0.geojson | 1 | 0.7 Mo | OK | Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO) |
| admin/limites_adm1.geojson | 10 | 1.4 Mo | OK | Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO) |
| admin/limites_adm2.geojson | 58 | 2.7 Mo | OK | Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO) |
| admin/limites_adm3.geojson | 360 | 4.8 Mo | OK | Creative Commons Attribution for Intergovernmental Organisations (CC BY-IGO) |
| admin/localites_osm.geojson | 12739 | 7.9 Mo | OK | ODbL 1.0 |
| admin/unites_administratives.csv | 429 | 0.0 Mo | manifeste incomplet : url | CC BY-IGO (limites OCHA) et ODbL 1.0 (comptes de localités dérivés d'OSM) |
| admin/comparaison_ocha_geoboundaries.csv | 430 | 0.0 Mo | manifeste incomplet : url, date_telechargement, limites | CC BY-IGO / CC BY 3.0 / CC BY 4.0 / ODbL 1.0 (noms et identifiants issus des deux sources) |
| infrastructures/routes_motorway.geojson | 110 | 0.1 Mo | OK | ODbL 1.0 |
| infrastructures/routes_trunk.geojson | 2841 | 2.2 Mo | OK | ODbL 1.0 |
| infrastructures/routes_primary.geojson | 2004 | 1.7 Mo | OK | ODbL 1.0 |
| infrastructures/routes_secondary.geojson | 3292 | 3.1 Mo | OK | ODbL 1.0 |
| infrastructures/routes_tertiary.geojson | 6938 | 6.5 Mo | OK | ODbL 1.0 |
| infrastructures/voies_ferrees.geojson | 476 | 0.3 Mo | OK | ODbL 1.0 |
| infrastructures/ponts_routes_principales.geojson | 885 | 0.4 Mo | OK | ODbL 1.0 |
| infrastructures/gares.geojson | 66 | 0.0 Mo | OK | ODbL 1.0 |
| infrastructures/ports_osm.geojson | 16 | 0.0 Mo | OK | ODbL 1.0 |
| infrastructures/aerodromes_osm.geojson | 30 | 0.0 Mo | OK | ODbL 1.0 |
| infrastructures/centrales_electriques.geojson | 34 | 0.0 Mo | OK | ODbL 1.0 |
| infrastructures/barrages.geojson | 68 | 0.0 Mo | OK | ODbL 1.0 |
| infrastructures/points_eau.geojson | 3108 | 1.6 Mo | OK | ODbL 1.0 |
| infrastructures/antennes_telecom.geojson | 290 | 0.1 Mo | OK | ODbL 1.0 |
| infrastructures/lignes_electriques.geojson | 101 | 0.1 Mo | OK | ODbL 1.0 |
| infrastructures/aeroports_ourairports.geojson | 47 | 0.0 Mo | OK | Domaine public (Public Domain Dedication, voir ourairports.com/data) |
| infrastructures/ports_wpi.geojson | 2 | 0.0 Mo | OK | Domaine public (œuvre du gouvernement fédéral des États-Unis) |
| infrastructures/synthese_par_arrondissement.csv | 360 | 0.0 Mo | OK | ODbL 1.0 (base de données dérivée d'OSM et de geoBoundaries CMR ADM3, elle-même sous ODbL) ; colonne Gridfinder : CC BY 4.0 |
| population/population_par_arrondissement.csv | 360 | 0.1 Mo | OK | CC BY 4.0 (WorldPop) ; noms et identifiants d'unités issus de geoBoundaries/OSM (ODbL 1.0) ; département/région issus du MINFOF/WRI (CC BY 4.0) |
| population/population_totaux_comparaison.csv | 2 | 0.0 Mo | OK | CC BY 4.0 (WorldPop) ; CC BY 3.0 IGO (ONU WPP 2024) |
| ressources/occupation_sol_par_arrondissement.csv | 360 | 0.1 Mo | OK | CC BY 4.0 (WorldCover) ; noms/identifiants geoBoundaries (ODbL 1.0) |
| ressources/foret_ufa_et_communales_minfof2018.geojson | 181 | 5.0 Mo | OK | CC BY 4.0 (champ licenseInfo de la fiche ArcGIS, modifiée le 2020-04-02) |
| ressources/foret_communautaire_minfof2018.geojson | 640 | 2.0 Mo | OK | CC BY 4.0 (champ licenseInfo de la fiche ArcGIS, modifiée le 2020-04-02) |
| ressources/aires_protegees_faune_minfof2018.geojson | 38 | 1.0 Mo | OK | CC BY 4.0 (champ licenseInfo de la fiche ArcGIS, modifiée le 2020-04-02) |
| ressources/permis_miniers_minfof2018.geojson | 167 | 0.1 Mo | OK | CC BY 4.0 (champ licenseInfo de la fiche ArcGIS, modifiée le 2020-04-02) |
| ressources/ressources_forestieres_minieres_par_arrondissement.csv | 360 | 0.1 Mo | OK | CC BY 4.0 (MINFOF/WRI) ; noms/identifiants geoBoundaries (ODbL 1.0) |
| ressources/synthese_par_arrondissement.csv | 360 | 0.1 Mo | manifeste incomplet : url | CC BY 4.0 (WorldPop, WorldCover, MINFOF/WRI) ; noms/identifiants geoBoundaries (ODbL 1.0) |
| social/sante/etablissements_sante_osm.geojson | 2106 | 1.1 Mo | OK | ODbL 1.0 |
| social/sante/etablissements_sante_healthsites.geojson | 1990 | 1.1 Mo | OK | ODbL 1.0 |
| social/sante/etablissements_sante_publics_maina2019.geojson | 3019 | 1.4 Mo | OK | CC0 1.0 (licence déclarée sur figshare ; l'article est sous CC BY 4.0) |
| social/education/etablissements_education_osm.geojson | 5011 | 2.5 Mo | OK | ODbL 1.0 |
| social/services/mairies_osm.geojson | 290 | 0.1 Mo | OK | ODbL 1.0 |
| social/services/marches_osm.geojson | 378 | 0.2 Mo | OK | ODbL 1.0 |
| social/sante/rapprochement_sources_sante.csv | 5101 | 0.8 Mo | manifeste incomplet : url | ODbL 1.0 (base dérivée d'OSM/healthsites ; Maina CC0 compatible) |
| social/synthese_par_arrondissement.csv | 8643 | 1.0 Mo | OK | ODbL 1.0 (comptes dérivés d'OSM ; limites geoBoundaries CMR ADM3 elles-mêmes sous ODbL 1.0, voir sources_documentees) |

## Sources documentées mais non publiées

- infrastructures : GRIDFINDER_ZENODO_3628142 — ESTIMATION PAR MODÈLE du réseau moyenne tension (et transport) à partir de lumières nocturnes VIIRS et d'OSM ; précision ~ 75 % selon les auteurs sur des pays d
- infrastructures : GEOBOUNDARIES_CMR_ADM3_9469f09 — Limites non officielles ; 360 unités (cohérent avec les 360 arrondissements).
- infrastructures : POSTES_ELECTRIQUES_OSM_NON_PUBLIES — Décision de prudence à confirmer par la gouvernance du projet (la donnée est publique dans OSM).
- infrastructures : TELECOM_SOURCES_NON_RETENUES — Couverture télécom réelle non représentée ; fibre optique (INF.TELECOM.FIBRE) non collectée faute de source ouverte identifiée.
- infrastructures : OSM_GEOFABRIK_INACCESSIBLE — L'extrait openstreetmap.fr est découpé avec une marge au-delà des frontières : objets hors Cameroun retirés par découpage au contour geoBoundaries + ~1 km.

**Fichiers de données non déclarés dans un manifeste : 0**
