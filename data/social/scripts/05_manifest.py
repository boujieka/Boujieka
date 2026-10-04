"""Écrit data/social/manifest.json (CONVENTIONS §4) à partir des fichiers produits et des contrôles."""
import hashlib
import json

import pandas as pd

from commun import (DATE_HS, DATE_MAINA, DATE_OSM, RAW, SOCIAL, SRC_HS, SRC_MAINA, SRC_OSM, TMP)

DATE_TELECHARGEMENT = "2026-10-04"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


C = json.load(open(TMP / "controles_couches.json"))
R = json.load(open(TMP / "controles_rapprochement.json"))
S = json.load(open(TMP / "controles_synthese.json"))

SHA = {"osm": sha256(RAW / "cameroon.osm.pbf"),
       "hs": sha256(RAW / "healthsites_cameroon.geojson"),
       "maina": sha256(RAW / "maina_figshare.xlsx"),
       "gb": sha256(RAW / "gb_cmr_adm3.geojson")}

OSM = {
    "source_code": SRC_OSM,
    "producteur": "Contributeurs OpenStreetMap, extrait Cameroun du miroir openstreetmap.fr",
    "url": "https://download.openstreetmap.fr/extracts/africa/cameroon.osm.pbf",
    "licence": "ODbL 1.0",
    "attribution": "© les contributeurs d'OpenStreetMap (openstreetmap.org/copyright)",
    "date_telechargement": DATE_TELECHARGEMENT,
    "date_situation": DATE_OSM,
    "sha256_source": SHA["osm"],
}
LIM_OSM = ("OSM n'est PAS exhaustif : couverture très inégale (forte en ville et dans les zones de "
           "projets de cartographie humanitaire, faible en zone rurale). Les absences ne signifient pas "
           "l'absence d'établissement. Surfaces converties en centroïdes. Les tags sont saisis par des "
           "bénévoles : erreurs de classification possibles. Noms tels que saisis (fautes, casse, "
           "mojibake éventuels conservés). Les noms d'établissements privés peuvent contenir un nom "
           "de personne (ex. « Clinique Dr ... ») : ce sont des raisons sociales publiques affichées, "
           "conservées telles quelles ; aucun autre attribut personnel n'est exporté.")
FILTRE_OSM = ("Filtre d'emprise : bbox lon 8,4-16,2 / lat 1,6-13,1 ET intersection stricte avec l'union "
              "des 360 polygones geoBoundaries CMR ADM3 (l'extrait OSM déborde sur les pays voisins).")
EXCLUS = ("Champs exclus : user, uid, phone, contact:*, email, addr:*, operator, website.")


def ctl_couche(nom):
    c = C[nom]
    return (f"Emprise : {json.dumps(c['emprise'], ensure_ascii=False)}. "
            f"Comptes par tg_type : {json.dumps(c['comptes_par_tg_type'], ensure_ascii=False)}. "
            f"Doublons internes suspects ({c['doublons_internes']['regle']}) : "
            f"{c['doublons_internes']['paires_suspectes']} paires, "
            f"{c['doublons_internes']['entites_concernees']} entités signalées dans le champ "
            f"doublon_interne_suspect (rien n'est supprimé).")


def entree(fichier, base, nom_ctl, methode, limites, controle_extra=""):
    p = SOCIAL / fichier
    e = {"fichier": fichier, **base, "sha256_fichier": sha256(p), "nb_entites": C[nom_ctl]["nb_entites"],
         "methode": methode, "limites": limites, "controle": ctl_couche(nom_ctl) + controle_extra}
    return e


import geopandas as gpd  # noqa: E402
_m = gpd.read_file(SOCIAL / "sante/etablissements_sante_publics_maina2019.geojson")
LLSRC = json.dumps({str(k): int(v) for k, v in _m["source_coordonnees"].value_counts().items()},
                   ensure_ascii=False)
fichiers = []
fichiers.append(entree(
    "sante/etablissements_sante_osm.geojson", OSM, "sante_osm",
    "scripts/01_osm_extraire.py puis 02_couches.py. Objets OSM (noeuds, ways fermés, multipolygones) "
    "avec amenity in {hospital, clinic, doctors, pharmacy, dentist} ou healthcare=* (hors objets "
    "école/mairie/marché). Classement (champ classement_regle) : HOPITAL si amenity|healthcare=hospital ; "
    "PHARMACIE si pharmacy ; LABORATOIRE si healthcare=laboratory ; CENTRE si healthcare=centre ; "
    "clinic/doctors dont le nom contient centre de santé, CSI, CMA, centre médical, dispensaire, "
    "health centre... -> CENTRE (règle tag+nom) ; autre clinic -> CLINIQUE ; doctors, dentist et "
    "valeurs non reconnues -> tg_type null (valeurs brutes amenity/healthcare conservées). "
    + FILTRE_OSM + " " + EXCLUS,
    LIM_OSM + " La distinction CENTRE/CLINIQUE repose en partie sur le nom (règle tag+nom). Quelques "
    "objets sont des districts de santé (unités administratives) étiquetés comme établissements."))
fichiers.append(entree(
    "sante/etablissements_sante_healthsites.geojson",
    {"source_code": SRC_HS,
     "producteur": "healthsites.io (Global Healthsites Mapping Project), données issues d'OpenStreetMap, "
                   "publiées sur HDX par Open Healthsite Consulting",
     "url": "https://data.humdata.org/dataset/cameroon-healthsites (ressource cameroon.geojson)",
     "licence": "ODbL 1.0",
     "attribution": "healthsites.io ; © les contributeurs d'OpenStreetMap",
     "date_telechargement": DATE_TELECHARGEMENT,
     "date_situation": DATE_HS,
     "sha256_source": SHA["hs"]},
    "sante_healthsites",
    "scripts/02_couches.py. Export HDX lu tel quel ; polygones convertis en centroïdes ; source_id = "
    "osm_type/osm_id ; mêmes règles de classement que la couche OSM. Champs changeset_* non exportés "
    "(rattachables à un contributeur). Filtre d'emprise : bbox + limites ADM3 avec tolérance ~1 km "
    "(source déclarée Cameroun).",
    "healthsites.io est DÉRIVÉ d'OSM : ce n'est pas une source indépendante. Mêmes limites que la couche "
    "OSM ; décalage temporel (situation 2026-09-15 contre 2026-10-03 pour l'extrait OSM). "
    "Période HDX déclarée 2010-10-28 à 2026-09-15."))
fichiers.append(entree(
    "sante/etablissements_sante_publics_maina2019.geojson",
    {"source_code": SRC_MAINA,
     "producteur": "Maina J., Ouma P.O., Macharia P.M., Alegana V.A., Mitto B., Snow R.W. et al. "
                   "(KEMRI-Wellcome Trust Research Programme), 2019. « A spatial database of health "
                   "facilities managed by the public health sector in sub Saharan Africa », Scientific "
                   "Data 6:134, doi:10.1038/s41597-019-0142-2",
     "url": "https://doi.org/10.6084/m9.figshare.7725374.v1 (fichier https://ndownloader.figshare.com/files/14379593, "
            "« 00 SSA MFL (130219).xlsx », md5 3bf56fc31081c8fd798789a3d70564b8 vérifié)",
     "licence": "CC0 1.0 (licence déclarée sur figshare ; l'article est sous CC BY 4.0)",
     "attribution": "Maina et al. 2019, Scientific Data ; figshare doi:10.6084/m9.figshare.7725374.v1",
     "date_telechargement": DATE_TELECHARGEMENT,
     "date_situation": DATE_MAINA,
     "sha256_source": SHA["maina"]},
    "sante_maina",
    "scripts/02_couches.py. Feuille « SSA MFL », lignes Country = Cameroon ("
    f"{C['sante_maina']['lignes_cameroun_source']} lignes, dont "
    f"{C['sante_maina']['lignes_sans_coordonnees_exclues']} sans coordonnées exclues). source_id = numéro "
    "de ligne Excel (la source n'a pas d'identifiant). Classement depuis « Facility type » : Centre de Santé "
    "Intégré, Health Centre, Centre Médical d'Arrondissement, Dispensaire -> CENTRE ; Hôpital de "
    "District/Régional/Général/Centraux -> HOPITAL ; Clinic -> CLINIQUE. Valeur brute dans type_source. "
    "Filtre d'emprise : bbox + limites ADM3 avec tolérance ~1 km.",
    "Données de 2019 (situation antérieure, date exacte non publiée ; fichier daté 13/02/2019). Secteur "
    "PUBLIC uniquement (gestionnaire « MoH » ; inclut des structures confessionnelles intégrées au "
    "système public). Coordonnées arrondies à 4 décimales par les auteurs et souvent géocodées au "
    f"niveau du village (source_coordonnees : {LLSRC}) : "
    "écart médian ~0,9 km constaté avec les objets OSM de même nom. Doublons de noms possibles "
    "(même établissement à deux positions)."))
fichiers.append(entree(
    "education/etablissements_education_osm.geojson", OSM, "education_osm",
    "scripts/01_osm_extraire.py puis 02_couches.py. amenity in {school, college, university, kindergarten}. "
    "Classement (champ classement_regle) : kindergarten -> MATERNELLE ; university -> SUPERIEUR ; sinon "
    "isced:level (0 MATERNELLE, 1 PRIMAIRE, 2 SECONDAIRE_1, 3 SECONDAIRE_2, 5-8 SUPERIEUR) ; sinon nom : "
    "université/faculté/institut supérieur/ENS -> SUPERIEUR ; maternelle/nursery -> MATERNELLE (PRIMAIRE "
    "si le nom mentionne aussi le primaire, règle tag+nom;multi_niveaux) ; lycée/collège technique, "
    "CETIC, CETI, SAR, GTHS -> TECHNIQUE ; lycée/high school/GBHS/GHS -> SECONDAIRE_2 ; collège/CES/CEG/"
    "secondary school/GSS -> SECONDAIRE_1 ; amenity=school + école primaire/école publique/EP/EPP/GS/"
    "primary school -> PRIMAIRE ; sinon tg_type null (valeur brute amenity conservée). "
    + FILTRE_OSM + " " + EXCLUS,
    LIM_OSM + f" Seulement {C['education_osm']['nb_entites']} objets : forte sous-représentation probable, "
    "surtout du primaire rural (aucun chiffre officiel n'a été téléchargé pour comparaison). "
    f"{round(100 * C['education_osm']['comptes_par_tg_type'].get('null', 0) / C['education_osm']['nb_entites'])} % "
    "des objets non classés (tg_type null). "
    "Un lycée camerounais couvre souvent les deux cycles du secondaire : SECONDAIRE_2 = « lycée » au "
    "sens du nom. Les « collèges » privés peuvent aussi couvrir les deux cycles. Certains objets "
    "university/college sont des bâtiments ou facultés d'un même campus (pas des établissements "
    "distincts). Classement par le nom = inférence, à valider."))
fichiers.append(entree(
    "services/mairies_osm.geojson", OSM, "mairies_osm",
    "scripts/01_osm_extraire.py puis 02_couches.py. amenity=townhall -> SOC.ADMIN.MAIRIE. " + FILTRE_OSM
    + " " + EXCLUS,
    LIM_OSM + f" {S['arrondissements_sans_mairie_osm']} arrondissements sur 360 n'ont aucun objet "
    "townhall dans OSM. "
    "amenity=townhall peut aussi désigner une salle communautaire ou une annexe."))
fichiers.append(entree(
    "services/marches_osm.geojson", OSM, "marches_osm",
    "scripts/01_osm_extraire.py puis 02_couches.py. amenity=marketplace -> ECO.MARCHE. " + FILTRE_OSM
    + " " + EXCLUS, LIM_OSM + " Les marchés périodiques ruraux sont très peu cartographiés."))

T = pd.read_csv(SOCIAL / "sante/rapprochement_sources_sante.csv")
sens = R["sensibilite_maina_vs_osm_hs_nb_paires"]
nM = C["sante_maina"]["nb_entites"]
fichiers.append({
    "fichier": "sante/rapprochement_sources_sante.csv",
    "source_code": f"{SRC_OSM};{SRC_HS};{SRC_MAINA}",
    "producteur": "Dérivé TasetyGrid des trois couches santé ci-dessus",
    "url": None,
    "licence": "ODbL 1.0 (base dérivée d'OSM/healthsites ; Maina CC0 compatible)",
    "attribution": "© les contributeurs d'OpenStreetMap ; healthsites.io ; Maina et al. 2019",
    "date_telechargement": DATE_TELECHARGEMENT,
    "date_situation": f"OSM {DATE_OSM} ; healthsites {DATE_HS} ; Maina {DATE_MAINA}",
    "sha256_source": {"osm": SHA["osm"], "healthsites": SHA["hs"], "maina": SHA["maina"]},
    "sha256_fichier": sha256(SOCIAL / "sante/rapprochement_sources_sante.csv"),
    "nb_entites": int(len(T)),
    "methode": "scripts/03_rapprochement_sante.py. Une ligne = un établissement présumé ; colonnes "
               "*_source_id renvoyant aux couches (aucune couche n'est modifiée). (1) OSM<->healthsites par "
               "identifiant OSM identique ; (2) résidus par distance < 500 m et similarité de nom >= 85 ; "
               "(3) Maina<->entités OSM/healthsites par distance < 500 m, similarité de nom >= 85 "
               "(moyenne token_set/token_sort rapidfuzz sur noms sans termes génériques ; noms vides ou "
               "purement génériques non appariables) et types compatibles (hôpital<->hôpital, "
               "centre<->clinique, null avec tout) ; appariement 1-1 glouton.",
    "limites": "Le seuil de 500 m imposé est très strict face à la précision des coordonnées Maina "
               "(géocodage au village) : le recouvrement Maina/OSM est donc SOUS-ESTIMÉ. Sensibilité "
               f"(paires Maina appariées) : {json.dumps(sens, ensure_ascii=False)} sur {nM} établissements "
               "Maina. Faux positifs résiduels repérés à la relecture : objets OSM « District de santé "
               "de X » appariés au CSI de X. Faux négatifs : noms très différents d'une source à l'autre, "
               "établissements renommés ou reclassés depuis 2019. Le recouvrement OSM/healthsites n'est pas "
               "une confirmation indépendante (healthsites dérive d'OSM).",
    "controle": f"Répartition : {json.dumps(R['repartition_par_combinaison_de_sources'], ensure_ascii=False)}. "
                f"OSM<->healthsites : {json.dumps(R['osm_healthsites'], ensure_ascii=False)} ; écart de "
                f"position sur les liens par identifiant : {json.dumps(R['ecart_position_liens_id_osm_m'])}. "
                f"Maina<->OSM/healthsites : {json.dumps(R['maina_vs_osm_healthsites'], ensure_ascii=False)}. "
                "Les 25 paires Maina retenues ont été relues une à une (voir limites).",
})

SY = pd.read_csv(SOCIAL / "synthese_par_arrondissement.csv")
fichiers.append({
    "fichier": "synthese_par_arrondissement.csv",
    "source_code": f"{SRC_OSM};{SRC_HS};{SRC_MAINA};GEOBOUNDARIES_CMR_ADM3_9469f09",
    "producteur": "Dérivé TasetyGrid ; limites geoBoundaries (Runfola et al. 2020, wmgeolab) utilisées "
                  "pour la jointure seulement",
    "url": "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/CMR/ADM3/"
           "geoBoundaries-CMR-ADM3.geojson (lu via media.githubusercontent.com, objet Git LFS)",
    "licence": "ODbL 1.0 (comptes dérivés d'OSM ; limites geoBoundaries CMR ADM3 elles-mêmes sous ODbL "
               "1.0, voir sources_documentees)",
    "attribution": "© les contributeurs d'OpenStreetMap ; healthsites.io ; Maina et al. 2019 ; geoBoundaries",
    "date_telechargement": DATE_TELECHARGEMENT,
    "date_situation": f"OSM {DATE_OSM} ; healthsites {DATE_HS} ; Maina {DATE_MAINA} ; limites : année "
                      "représentée 2017, mise à jour source 2023-01-19, build 2023-12-12",
    "sha256_source": {"osm": SHA["osm"], "healthsites": SHA["hs"], "maina": SHA["maina"],
                      "geoboundaries_cmr_adm3_geojson": SHA["gb"]},
    "sha256_fichier": sha256(SOCIAL / "synthese_par_arrondissement.csv"),
    "nb_entites": int(len(SY)),
    "methode": "scripts/04_synthese.py. Jointure point-dans-polygone (within) avec les 360 polygones ADM3 ; "
               "format long : gb_shape_id, arrondissement (shapeName, mojibake UTF-8/Latin-1 corrigé), "
               "source, couche, tg_type (vide = non classé), nombre. Toutes les combinaisons "
               "arrondissement x tg_type présentes dans une couche sont listées, zéros compris. "
               "gb_shape_id = HORS_LIMITES pour les points hors polygones (Maina, tolérance ~1 km).",
    "limites": "NE PAS additionner les trois sources santé (elles se recouvrent ; voir "
               "sante/rapprochement_sources_sante.csv). Un zéro signifie « rien dans la source », pas "
               "« aucun établissement ». Les limites geoBoundaries (OSM/Wambacher, année représentée 2017) "
               "ne sont pas officielles (boundaryCanonical = Unknown) ; le rattachement à un arrondissement "
               "peut différer du découpage administratif officiel près des limites.",
    "controle": f"{json.dumps(S, ensure_ascii=False)}. Contrôle de cohérence : pour chaque couche, la somme "
                "des nombres égale le nombre d'entités de la couche (assert dans le script). 360 "
                "arrondissements (= nombre officiel, docs CONVENTIONS §5).",
})

manifest = {
    "theme": "social",
    "description": "Infrastructures sociales du Cameroun : santé (3 sources), éducation, mairies, marchés.",
    "date_collecte": DATE_TELECHARGEMENT,
    "scripts": ["scripts/00_telecharger.sh", "scripts/commun.py", "scripts/01_osm_extraire.py",
                "scripts/02_couches.py", "scripts/03_rapprochement_sante.py", "scripts/04_synthese.py",
                "scripts/05_manifest.py"],
    "avertissement_completude": (
        "Aucune de ces couches n'est exhaustive. OpenStreetMap dépend de contributions bénévoles : de "
        f"nombreux arrondissements n'ont aucun établissement de santé ({S['arrondissements_sans_aucun_etablissement_osm_sante']}/360) "
        f"ou aucune école ({S['arrondissements_sans_aucune_ecole_osm']}/360) dans OSM. La base Maina 2019 "
        "ne couvre que le secteur public et date de 2019. Ces données sont des assertions importées "
        "(statut IMPORTE), à confronter aux listes officielles (MINSANTE, MINEDUB, MINESEC, MINESUP, "
        "MINDDEVEL) avant tout usage décisionnel."),
    "fichiers": fichiers,
    "sources_documentees": [
        {"source": "Geofabrik — https://download.geofabrik.de/africa/cameroon-latest.osm.pbf",
         "statut": "NON UTILISÉE : inaccessible depuis l'environnement de collecte (connexion réinitialisée "
                   "par le proxy de sortie, 2026-10-04). Remplacée par le miroir openstreetmap.fr (mêmes "
                   "données OSM, même licence ODbL)."},
        {"source": "Overpass API — overpass-api.de, overpass.kumi.systems, overpass.private.coffee, maps.mail.ru",
         "statut": "NON UTILISÉE : inaccessible ou hors délai depuis l'environnement de collecte (2026-10-04)."},
        {"source": "HOT Export Tool / HDX hotosm_cmr_health_facilities, hotosm_cmr_education_facilities (ODbL)",
         "statut": "NON UTILISÉE : simple autre extraction d'OSM, redondante avec l'extrait complet utilisé."},
        {"source": "geoBoundaries gbOpen CMR ADM3, boundaryID CMR-ADM3-9386221, commit 9469f09 "
                   "(https://www.geoboundaries.org/api/current/gbOpen/CMR/ADM3/)",
         "statut": "UTILISÉE pour la jointure spatiale et le filtre d'emprise, NON COMMITÉE (un autre agent "
                   "s'en charge). ATTENTION : la consigne la supposait sous CC BY 4.0 ; les métadonnées "
                   "geoBoundaries indiquent « Open Data Commons Open Database License 1.0 » (source "
                   "OpenStreetMap, Wambacher). Année représentée 2017, mise à jour source 2023-01-19, build "
                   "2023-12-12, 360 unités. Les noms (shapeName) contiennent du mojibake (ex. « MÃ©long ») "
                   "corrigé à la lecture.",
         "sha256": SHA["gb"]},
        {"source": "HDX health-facilities-in-sub-saharan-africa (copie Maina et al., CC BY)",
         "statut": "NON UTILISÉE : la version d'origine figshare (CC0) a été préférée."},
    ],
}
with open(SOCIAL / "manifest.json", "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print("manifest écrit :", len(fichiers), "fichiers")
