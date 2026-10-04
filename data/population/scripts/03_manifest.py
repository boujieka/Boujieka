"""Écrit data/population/manifest.json (métadonnées + sha256 des fichiers produits).
Les sha256 des sources ont été relevés au téléchargement (01_telecharger.sh)."""
import hashlib
import json
import os

ICI = os.path.join(os.path.dirname(__file__), "..")


def sha(f):
    return hashlib.sha256(open(os.path.join(ICI, f), "rb").read()).hexdigest()


def nlignes(f):
    return sum(1 for _ in open(os.path.join(ICI, f), encoding="utf-8")) - 1


WORLDPOP = {
    "source_code": "WORLDPOP_R2025A_CN_100M",
    "producteur": "WorldPop, University of Southampton (Global2 R2025A v1, Bondarenko M. et al. 2025)",
    "url": "https://hub.worldpop.org/geodata/summary?id=72799",
    "url_fichiers": [
        "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2025/CMR/v1/100m/constrained/cmr_pop_2025_CN_100m_R2025A_v1.tif",
        "https://data.worldpop.org/GIS/Population/Global_2015_2030/R2025A/2026/CMR/v1/100m/constrained/cmr_pop_2026_CN_100m_R2025A_v1.tif"],
    "doi": "10.5258/SOTON/WP00839",
    "licence": "CC BY 4.0 (https://hub.worldpop.org/data/licence.txt)",
    "attribution": "WorldPop (www.worldpop.org), University of Southampton. Bondarenko M., Priyatikanto R., Tejedor-Garavito N., Zhang W., McKeen T., Cunningham A., Woods T., Hilton J., Cihan D., Nosatiuk B., Brinkhoff T., Tatem A., Sorichetta A. (2025). Constrained estimates of 2015-2030 total number of people per grid square, 3 arc-sec (~100 m), R2025A v1. DOI:10.5258/SOTON/WP00839",
    "produit": "Global2 R2025A v1 « Individual countries 2015-2030 (100 m) », méthode CONTRAINTE (population répartie uniquement sur les cellules bâties), redistribution dasymétrique par forêt aléatoire ; produit publié le 2025-09-01, qualifié « alpha » par WorldPop (susceptible de changer)",
    "resolution": "3 secondes d'arc (~100 m à l'équateur), WGS84",
    "sha256_source": {
        "cmr_pop_2025_CN_100m_R2025A_v1.tif": "4112e3fe949a447f36cc1998b915f6b7fdbc5a357135c3d58c9ec47c1f878f03",
        "cmr_pop_2026_CN_100m_R2025A_v1.tif": "f9f125aeca9a89fc463cfc645b21a27dfd213fcb049f6a781bfdcc2c8f235b72"},
    "commite": False,
}
GEOB = {
    "source_code": "GEOBOUNDARIES_CMR_ADM3_9469f09",
    "producteur": "geoBoundaries (William & Mary geoLab), boundaryID CMR-ADM3-9386221, source OpenStreetMap / Wambacher, année représentée 2017, build 2023-12-12",
    "url": "https://www.geoboundaries.org/api/current/gbOpen/CMR/ADM3/",
    "url_fichier": "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/9469f09/releaseData/gbOpen/CMR/ADM3/geoBoundaries-CMR-ADM3.geojson",
    "licence": "ODbL 1.0 (déclarée par l'API geoBoundaries pour CMR ADM3, car dérivée d'OSM) — et NON CC BY 4.0 comme supposé dans la demande initiale",
    "attribution": "geoBoundaries (Runfola et al. 2020) ; © les contributeurs d'OpenStreetMap",
    "sha256_source": "9d0ff998057c3afe7f3a6334d71e9d7c353c64fe6e7c35b01fe14d804c97f04b",
    "commite": False,
    "note": "Téléchargé pour le calcul uniquement ; les géométries ne sont pas commitées. Les CSV n'en reprennent que l'identifiant shapeID, le nom et la surface calculée.",
}
WPP = {
    "source_code": "ONU_WPP2024_MEDIUM",
    "producteur": "Nations unies, DESA, Division de la population — World Population Prospects 2024, variante moyenne",
    "url": "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz",
    "licence": "CC BY 3.0 IGO",
    "attribution": "United Nations, Department of Economic and Social Affairs, Population Division (2024). World Population Prospects 2024.",
    "sha256_source": "286ac36bb1415e2e1ade03acfef0a29f0e4c087e2f78e38c48f50c5df89082bc",
    "commite": False,
}
BM = {
    "source_code": "BANQUE_MONDIALE_WDI_2026-07",
    "producteur": "Banque mondiale, World Development Indicators (mise à jour 2026-07-13), indicateurs SP.POP.TOTL, AG.SRF.TOTL.K2, AG.LND.TOTL.K2",
    "url": "https://api.worldbank.org/v2/country/CMR/indicator/AG.SRF.TOTL.K2;AG.LND.TOTL.K2?source=2&format=json&date=2020:2024",
    "licence": "CC BY 4.0",
    "usage": "contrôle de cohérence uniquement (superficie 2023 : 475 440 km² totale, 472 710 km² terres ; population 2025 : 29 879 337)",
}
MINFOF = {
    "source_code": "MINFOF_WRI_ATLAS_FORESTIER_SIG_2018",
    "producteur": "MINFOF / World Resources Institute — Atlas forestier interactif du Cameroun, « Cameroun données SIG sans documents (2018) », couche arrondissements",
    "url": "https://www.arcgis.com/home/item.html?id=7e8925d7feb9439ca3f5754759f226ba",
    "licence": "CC BY 4.0 (champ licenseInfo de la fiche ArcGIS)",
    "sha256_source": "97278249253665d320da0bd2f6585c5510c4f46ac130f6aca35f36969bdc5ec3",
    "usage": "uniquement pour rattacher chaque arrondissement geoBoundaries à un département et une région (recouvrement maximal) et donner le nom MINFOF en regard",
}

LIMITES_COMMUNES = (
    "ESTIMATIONS MODÉLISÉES, PAS DES RÉSULTATS DE RECENSEMENT : les résultats du 4e RGPH (2026) ne sont pas publiés. "
    "WorldPop R2025A répartit un total national exogène : "
    "le total du raster 2025 (29 499 946) est EXACTEMENT égal à la population ONU WPP 2024 au 1er janvier 2025, "
    "et celui de 2026 (30 258 728) à celle du 1er janvier 2026 — la comparaison avec l'ONU n'est donc pas une validation indépendante. "
    "Écart avec la population ONU au 1er juillet : -1,27 % (2025), -1,25 % (2026), dû à la date de référence. "
    "Produit WorldPop qualifié « alpha » ; méthode contrainte = population nulle hors bâti détecté (bâti non détecté → population sous-estimée localement). "
    "Les limites geoBoundaries ADM3 (OSM, situation 2017) ne sont pas des limites officielles : surface totale 466 372 km² contre 475 440 km² "
    "(superficie totale, Banque mondiale AG.SRF.TOTL.K2) et 472 710 km² (terres émergées, AG.LND.TOTL.K2), soit -1,9 % et -1,3 % ; "
    "les densités dépendent de ces surfaces. 20 280 personnes (0,07 %) tombent dans des pixels hors des polygones (côte, frontières) et ne sont affectées à aucun arrondissement. "
    "69 noms geoBoundaries comportaient un défaut d'encodage (UTF-8 lu en Latin-1) réparé automatiquement ; plusieurs graphies diffèrent "
    "de celles du MINFOF (ex. Tabati/Tibati, Mouloundou/Moloundou, Ouli/Mbotoro) : voir la colonne nom_minfof_2018. "
    "Rattachement département/région par recouvrement avec la couche MINFOF 2018 : recouvrement minimal 0,538, 2 arrondissements < 0,8.")

manifest = {
    "theme": "population",
    "date_collecte": "2026-10-04",
    "avertissement": "Toutes les populations sont des ESTIMATIONS modélisées (WorldPop), pas des résultats de recensement.",
    "sources": [WORLDPOP, GEOB, WPP, BM, MINFOF],
    "fichiers": [
        {
            "fichier": "population/population_par_arrondissement.csv",
            "source_code": "WORLDPOP_R2025A_CN_100M",
            "sources_secondaires": ["GEOBOUNDARIES_CMR_ADM3_9469f09", "MINFOF_WRI_ATLAS_FORESTIER_SIG_2018"],
            "producteur": WORLDPOP["producteur"],
            "url": WORLDPOP["url"],
            "licence": "CC BY 4.0 (WorldPop) ; noms et identifiants d'unités issus de geoBoundaries/OSM (ODbL 1.0) ; département/région issus du MINFOF/WRI (CC BY 4.0)",
            "attribution": "WorldPop (2025) DOI:10.5258/SOTON/WP00839 ; geoBoundaries / © contributeurs OpenStreetMap ; MINFOF/WRI Atlas forestier interactif du Cameroun",
            "date_telechargement": "2026-10-04",
            "date_situation": "estimations pour 2025 et 2026 (produit R2025A publié le 2025-09-01)",
            "sha256_source": WORLDPOP["sha256_source"],
            "sha256_fichier": sha("population_par_arrondissement.csv"),
            "nb_entites": nlignes("population_par_arrondissement.csv"),
            "mesures": {"pop_2025": "POP_TOTALE", "pop_2026": "POP_TOTALE", "densite_2025_hab_km2": "DENSITE", "densite_2026_hab_km2": "DENSITE"},
            "methode": "scripts/01_telecharger.sh puis scripts/02_population_par_arrondissement.py : rasterisation des 360 polygones ADM3 sur la grille WorldPop (pixel affecté à l'unité contenant son centre, aucun double compte), somme des pixels (nodata = 0), surface géodésique WGS84 des polygones (pyproj.Geod), densité = population / surface.",
            "limites": LIMITES_COMMUNES,
            "controle": "360 arrondissements (attendu 360), 0 nom dupliqué, 10 régions et 58 départements rattachés (attendu 10 et 58), aucun arrondissement à population nulle (min 1 693 Afanloum, max 1 282 931 Douala III) ; emprise lon 8,499-16,192 / lat 1,655-13,083 (dans l'emprise Cameroun) ; somme 2025 = 29 479 666 sur un total raster de 29 499 946.",
        },
        {
            "fichier": "population/population_totaux_comparaison.csv",
            "source_code": "WORLDPOP_R2025A_CN_100M",
            "sources_secondaires": ["ONU_WPP2024_MEDIUM"],
            "producteur": "WorldPop ; Nations unies DESA/Division de la population",
            "url": WPP["url"],
            "licence": "CC BY 4.0 (WorldPop) ; CC BY 3.0 IGO (ONU WPP 2024)",
            "attribution": WORLDPOP["attribution"] + " ; " + WPP["attribution"],
            "date_telechargement": "2026-10-04",
            "date_situation": "2025 et 2026 (1er janvier et 1er juillet pour l'ONU)",
            "sha256_source": {"WorldPop": WORLDPOP["sha256_source"], "WPP2024_Demographic_Indicators_Medium.csv.gz": WPP["sha256_source"]},
            "sha256_fichier": sha("population_totaux_comparaison.csv"),
            "nb_entites": nlignes("population_totaux_comparaison.csv"),
            "methode": "Total du raster WorldPop, somme par arrondissement, reliquat hors polygones ; colonnes TPopulation1Jan et TPopulation1July (milliers × 1000) de WPP 2024 pour ISO3=CMR.",
            "limites": "WorldPop R2025A est calé sur l'ONU WPP 2024 (égalité exacte au 1er janvier) : ce n'est PAS une seconde source indépendante. Aucune projection INS/BUCREP téléchargeable et sous licence explicite n'a été trouvée pendant cette collecte ; à ajouter si l'INS publie une série ouverte. Chiffre de contexte : Banque mondiale SP.POP.TOTL 2025 = 29 879 337 (identique à l'ONU au 1er juillet, car issu de WPP).",
            "controle": "Écart WorldPop - ONU au 1er janvier : 0 (2025 et 2026). Écart au 1er juillet : -379 391 (-1,27 %) en 2025, -382 089 (-1,25 %) en 2026.",
        },
    ],
    "non_commite": ["rasters WorldPop (≈26 Mo chacun)", "géométries geoBoundaries ADM3", "fichier WPP complet"],
}
with open(os.path.join(ICI, "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("manifest population écrit")
