"""Écrit data/ressources/manifest.json (métadonnées, contrôles, sha256 des fichiers produits).
Les sha256 des sources ont été relevés au téléchargement (01_telecharger.sh)."""
import hashlib
import json
import os

import pandas as pd

ICI = os.path.join(os.path.dirname(__file__), "..")


def sha(f):
    return hashlib.sha256(open(os.path.join(ICI, f), "rb").read()).hexdigest()


def n_entites(f):
    if f.endswith(".geojson"):
        return len(json.load(open(os.path.join(ICI, f), encoding="utf-8"))["features"])
    return sum(1 for _ in open(os.path.join(ICI, f), encoding="utf-8")) - 1


SHA_WC = {
    "N00E006": "1032240c983d7669aa6847d07b8780ce641ef707fb0f8d8bd3f8330097681309",
    "N00E009": "acd048ae58ebccec49533a7c7b079b7040cbb980e1f5cc97921bbcca50829fd6",
    "N00E012": "416cee7289679b7415620042eea3ea57130f267d22b04c9e602abbae5d8f0bb2",
    "N00E015": "89af6d334e58f8019cb64bb68cfd7ff1fb07c28540d6268eae9e78deae4b2e51",
    "N03E006": "3b968e9c4ca6e118a2b7b099d124e15fc549488c9bafbead5c15c501abbfd6c2",
    "N03E009": "1baef0e8d13e36d7aca5439787f7d65622259b5a31ce74f9b0ca72f0108dd25d",
    "N03E012": "0d71efac64cc67bccd04ddbb35e8be93af414e2ec37b1329ad4c32a330cae950",
    "N03E015": "10b427c26b1da109b08cbfc1a2f844b6e1e60727bfc443e5fffb6a562bf1bea3",
    "N06E006": "f5c33a6ab42afaffee0e96103e44dd236bf2678eb71b9e17b0a31e83dcac4630",
    "N06E009": "310d4bea0dc7ae5a93c249eeb3909b3596f0dc1ee60f1023ebb2dda081059a79",
    "N06E012": "eb2a742b935ee18c139de6045af5a60b5990dc3b0270629f3e52129701d16cc6",
    "N06E015": "80704616c5b2e90384ac04cd14d4e8e09dd3d2c55f94e50a9d41db2f4f0d8fca",
    "N09E006": "81038bd3e6701abeaa28d6030ee369cefcfa49df1d8d1e83f9fd305310ca3247",
    "N09E009": "437ab941804eee3eca9c485b4f055c02448b2ac59c84a96976e5c304c09374c3",
    "N09E012": "f0debd002fc9a6915302025fb9cb68700a7e97d565c696fdfa2dbc1b916cd463",
    "N09E015": "eb535de61289cee3d3fc191e0db9403cfa60aa0ee808d8a33eb9388a191eb3cd",
    "N12E006": "0c35200d666b1a38fc46a62dc5b61bafa2a0a3c30089a273ab2def857270e6d6",
    "N12E009": "f433e78038c3bc4a83aa35764fcff0526fd91e7ef4c69b202d123eac20c9e285",
    "N12E012": "873442291197a9e57434742e5986901114622c50a4008938ceb287fee3dcfb7f",
    "N12E015": "be072548a50b1a10499eff6ff15c411fe4d74a203d95bcea4d0d3980bed979a6",
}

WC = {
    "source_code": "ESA_WORLDCOVER_2021_V200",
    "producteur": "Agence spatiale européenne (ESA) / consortium WorldCover — ESA WorldCover 10 m 2021 v200",
    "url": "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/",
    "doi": "10.5281/zenodo.7254221",
    "licence": "CC BY 4.0 (vérifiée sur la notice Zenodo 7254221)",
    "attribution": "© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium. Zanaga D. et al. (2022) ESA WorldCover 10 m 2021 v200. DOI:10.5281/zenodo.7254221",
    "sha256_source": SHA_WC,
    "commite": False,
}
GEOB = {
    "source_code": "GEOBOUNDARIES_CMR_ADM3_9469f09",
    "url": "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/9469f09/releaseData/gbOpen/CMR/ADM3/geoBoundaries-CMR-ADM3.geojson",
    "licence": "ODbL 1.0 (dérivé d'OSM)",
    "sha256_source": "9d0ff998057c3afe7f3a6334d71e9d7c353c64fe6e7c35b01fe14d804c97f04b",
    "commite": False,
    "note": "voir data/population/manifest.json",
}
FA = {
    "source_code": "MINFOF_WRI_ATLAS_FORESTIER_SIG_2018",
    "producteur": "Ministère des Forêts et de la Faune (MINFOF) / World Resources Institute (WRI) — Atlas forestier interactif du Cameroun, paquet « Cameroun données SIG sans documents (2018) » (donnees_ouverts_fr.gdb)",
    "url": "https://www.arcgis.com/home/item.html?id=7e8925d7feb9439ca3f5754759f226ba",
    "url_fichier": "http://wri-sites.s3.amazonaws.com/forest-atlas.org/cmr.forest-atlas.org/resources/gdbs/cmr_data_sans_documents_2018.rar",
    "licence": "CC BY 4.0 (champ licenseInfo de la fiche ArcGIS, modifiée le 2020-04-02)",
    "attribution": "MINFOF / World Resources Institute, Atlas forestier interactif du Cameroun (cmr-data.forest-atlas.org), données SIG 2018, CC BY 4.0",
    "sha256_source": "97278249253665d320da0bd2f6585c5510c4f46ac130f6aca35f36969bdc5ec3",
    "date_situation": "archive datée du 2019-03-25 (Last-Modified HTTP) ; dates de dernière édition des entités 2015-06 à 2019-03",
}
NON_RETENUS = [
    {
        "source": "Couches actuelles de l'Atlas forestier (services ArcGIS MINFOF : UFA/Forêts de production, forets_communautaires, Aires_protegées_de_la_faune, Réserves_forestier, ventes de coupe, AAC…) et paquets « cmr data sans documents 2025.gdb », « Cameroun données SIG sans documents » 2019 à 2024",
        "url": "https://cmr-data.forest-atlas.org/",
        "licence": "AUCUNE licence déclarée (licenseInfo vide, ou texte « La qualité de ces données peut varier en fonction des sources » pour Forêts de production) — vérifié le 2026-10-04",
        "decision": "NON copiées : licence introuvable, redistribution non autorisée explicitement. Seuls des comptes d'entités ont été relevés pour mesurer l'obsolescence du paquet 2018 : UFA 198 (contre 181 UFA + forêts communales en 2018 — périmètre de couche peut différer), forêts communautaires 762 (contre 640), aires protégées de la faune 37 (contre 38).",
    },
    {
        "source": "World Database on Protected Areas (WDPA, UNEP-WCMC/IUCN)",
        "url": "https://www.protectedplanet.net/",
        "licence": "Conditions WDPA : redistribution interdite",
        "decision": "NON utilisée. Les aires protégées proviennent de la couche MINFOF 2018 (CC BY 4.0) ; le champ wdpaid n'est qu'un identifiant de renvoi. Le recours à OSM (boundary=protected_area) n'a pas été nécessaire.",
    },
    {
        "source": "Permis miniers actuels (cadastre minier)",
        "url": "",
        "licence": "inconnue",
        "decision": "Aucune source ouverte à jour trouvée pendant cette collecte ; seule la couche permis_miniers du paquet MINFOF 2018 (entités éditées 2015-2016) est fournie.",
    },
]

LIM_FA = ("Données ANCIENNES (situation 2015-2019) : attributions, classements et permis ont pu changer depuis ; "
          "ne pas utiliser comme situation actuelle. Champs nominatifs supprimés (attributaire, exploitant, société titulaire, partenaire, "
          "comptes d'édition). Reprojetées d'EPSG:4034 (Clarke 1880) vers EPSG:4326, géométries rendues valides (make_valid). "
          "Les tg_type sont une proposition de correspondance avec nomenclatures/objets.yaml (UFA et permis → FON.CONCESSION ; "
          "forêts communales/communautaires → RES.FORET ; aires protégées → FON.AIRE_PROTEGEE) et regime_tg avec usages_et_regimes.yaml.")


def main():
    o = pd.read_csv(os.path.join(ICI, "occupation_sol_par_arrondissement.csv"))
    r = pd.read_csv(os.path.join(ICI, "ressources_forestieres_minieres_par_arrondissement.csv"))
    classes = [c for c in o.columns if c.endswith("_ha") and c not in ("surface_classee_ha", "non_classe_nodata_ha")]
    nat = {c: int(round(o[c].sum())) for c in classes}
    tot = int(round(o.surface_classee_ha.sum()))
    pct = {c: round(100 * v / tot, 2) for c, v in nat.items()}
    res_nat = {c: int(round(r[c].sum())) for c in r.columns if c.endswith("_ha")}

    fichiers = [{
        "fichier": "ressources/occupation_sol_par_arrondissement.csv",
        "source_code": WC["source_code"], "sources_secondaires": [GEOB["source_code"]],
        "producteur": WC["producteur"], "url": WC["url"], "licence": "CC BY 4.0 (WorldCover) ; noms/identifiants geoBoundaries (ODbL 1.0)",
        "attribution": WC["attribution"] + " ; geoBoundaries / © contributeurs OpenStreetMap",
        "date_telechargement": "2026-10-04", "date_situation": "2021 (imagerie Sentinel-1/2 de 2021)",
        "sha256_source": WC["sha256_source"], "sha256_fichier": sha("occupation_sol_par_arrondissement.csv"),
        "nb_entites": n_entites("occupation_sol_par_arrondissement.csv"),
        "methode": "scripts/02_occupation_sol.py : 20 tuiles 3°x3° ; rasterisation des polygones ADM3 par bandes de 600 lignes sur la grille 10 m (centre du pixel) ; comptage par (arrondissement, classe) ; conversion en ha par l'aire géodésique WGS84 d'un pixel au centre de chaque bande. Correspondance : 10 forêt (couvert arboré), 20 arbustes, 30 prairie/savane herbacée, 40 cultures, 50 bâti, 60 sol nu, 80 eau permanente, 90 zone humide herbacée, 95 mangroves.",
        "limites": "Carte de 2021, issue d'une classification automatique (précision variable selon les classes, voir le rapport de validation ESA WorldCover_PVR_V2.0). « Couvert arboré » (classe 10) ≠ forêt au sens juridique ou du MINFOF : il inclut savanes boisées, plantations arborées et agroforêts ; les petites cultures sous couvert ou en mosaïque forestière sont souvent classées en arbres (cultures probablement sous-estimées en zone forestière, ex. Mbonge : 2 ha de cultures). Pas de distinction prairie/savane : « savane » = classes 20+30 dans la synthèse. Surfaces limitées aux polygones geoBoundaries (surface totale inférieure de 1,9 % à la superficie Banque mondiale).",
        "controle": f"Somme des classes = {tot} ha = {tot/100:.0f} km², égale à la surface géodésique des 360 polygones (466 372,5 km²) ; 0 ha sans donnée ; aucune classe inattendue. Répartition nationale (%) : {pct}. Hectares : {nat}.",
    }]
    for f, cat in [("foret_ufa_et_communales_minfof2018.geojson", "UFA (117) et forêts communales (64)"),
                   ("foret_communautaire_minfof2018.geojson", "forêts communautaires (640, dont 3 libellées « Forets communautiares » et 1 « Vente de coupe » dans la source)"),
                   ("aires_protegees_faune_minfof2018.geojson", "aires protégées de la faune (27 parcs nationaux, 6 sanctuaires, 5 réserves ; 28 créées, 9 proposées, 1 sans statut)"),
                   ("permis_miniers_minfof2018.geojson", "permis miniers (163 de recherche, 4 d'exploitation)")]:
        fichiers.append({
            "fichier": f"ressources/{f}", "source_code": FA["source_code"], "producteur": FA["producteur"],
            "url": FA["url"], "licence": FA["licence"], "attribution": FA["attribution"],
            "date_telechargement": "2026-10-04", "date_situation": FA["date_situation"],
            "sha256_source": FA["sha256_source"], "sha256_fichier": sha(f), "nb_entites": n_entites(f),
            "methode": "scripts/03_atlas_forestier.py : lecture de donnees_ouverts_fr.gdb (GDAL OpenFileGDB), sélection des champs non nominatifs, ajout des champs TasetyGrid, export GeoJSON RFC 7946, 6 décimales.",
            "limites": LIM_FA + (" Les dates d'expiration (date_expr) de nombreux permis de recherche sont antérieures à 2026 : vérifier leur validité." if "permis" in f else "")
                       + (" Une partie des aires protégées (≈ 326 600 ha, zones marines/côtières ou hors limites geoBoundaries) n'est pas affectée aux arrondissements." if "aires" in f else ""),
            "controle": f"Contenu : {cat}. 0 doublon d'identifiant ; emprises toutes dans lon 8,4-16,2 / lat 1,6-13,1 ; 2 géométries en double dans les forêts communautaires (signalées, non supprimées).",
        })
    fichiers.append({
        "fichier": "ressources/ressources_forestieres_minieres_par_arrondissement.csv",
        "source_code": FA["source_code"], "sources_secondaires": [GEOB["source_code"]], "producteur": FA["producteur"],
        "url": FA["url"], "licence": "CC BY 4.0 (MINFOF/WRI) ; noms/identifiants geoBoundaries (ODbL 1.0)", "attribution": FA["attribution"],
        "date_telechargement": "2026-10-04", "date_situation": FA["date_situation"],
        "sha256_source": FA["sha256_source"], "sha256_fichier": sha("ressources_forestieres_minieres_par_arrondissement.csv"),
        "nb_entites": n_entites("ressources_forestieres_minieres_par_arrondissement.csv"),
        "methode": "scripts/03_atlas_forestier.py : union des polygones par catégorie (pas de double compte des chevauchements internes), intersection avec les arrondissements en projection équivalente EPSG:6933, surfaces en ha ; *_nb = nombre d'entités qui touchent l'arrondissement (une entité à cheval est comptée dans chaque arrondissement).",
        "limites": LIM_FA + " Les catégories peuvent se chevaucher entre elles (ex. permis de recherche sur UFA ou aire protégée) : ne pas additionner les colonnes.",
        "controle": f"Totaux affectés aux arrondissements (ha) : {res_nat}. Unions nationales (ha) : aires protégées 4 773 718 (dont 4 447 139 dans les arrondissements), UFA 6 824 954, forêts communales 1 819 196, forêts communautaires 2 191 263, permis de recherche 13 035 383, permis d'exploitation 187 930.",
    })
    fichiers.append({
        "fichier": "ressources/synthese_par_arrondissement.csv",
        "source_code": "SYNTHESE_TASETYGRID",
        "sources_secondaires": ["WORLDPOP_R2025A_CN_100M", WC["source_code"], FA["source_code"], GEOB["source_code"]],
        "producteur": "TasetyGrid (calcul) à partir des sources citées",
        "url": "", "licence": "CC BY 4.0 (WorldPop, WorldCover, MINFOF/WRI) ; noms/identifiants geoBoundaries (ODbL 1.0)",
        "attribution": "WorldPop (2025) ; ESA WorldCover 2021 ; MINFOF/WRI Atlas forestier interactif du Cameroun ; geoBoundaries / © contributeurs OpenStreetMap",
        "date_telechargement": "2026-10-04",
        "date_situation": "millésimes HÉTÉROGÈNES : population 2025 (estimation), occupation du sol 2021, atlas forestier 2015-2019",
        "sha256_source": "voir les fichiers d'entrée", "sha256_fichier": sha("synthese_par_arrondissement.csv"),
        "nb_entites": n_entites("synthese_par_arrondissement.csv"),
        "methode": "scripts/04_synthese.py : jointure 1:1 sur arrondissement_id (shapeID geoBoundaries) de population/population_par_arrondissement.csv, occupation_sol_par_arrondissement.csv et ressources_forestieres_minieres_par_arrondissement.csv ; ratios simples (ha par habitant, part de la surface).",
        "limites": "Croise des millésimes différents ; population = estimation modélisée (pas un recensement) ; surfaces de ressources anciennes (2015-2019). Les ratios par habitant n'ont de sens qu'à titre indicatif.",
        "controle": "360 lignes, jointures 1:1 validées, aucune valeur manquante ; population totale 29 479 666 (= somme du fichier population).",
    })
    m = {
        "theme": "ressources",
        "date_collecte": "2026-10-04",
        "sources": [WC, GEOB, FA],
        "sources_non_retenues": NON_RETENUS,
        "fichiers": fichiers,
        "non_commite": ["20 tuiles raster ESA WorldCover (~1,6 Go)", "géométries geoBoundaries ADM3", "géodatabase MINFOF complète (les autres couches ne sont pas reprises)"],
    }
    with open(os.path.join(ICI, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"pct": pct, "tot": tot, "res": res_nat}, ensure_ascii=False))


if __name__ == "__main__":
    main()
