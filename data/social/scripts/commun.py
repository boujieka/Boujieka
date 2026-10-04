"""Paramètres et règles communes à la collecte « infrastructures sociales »."""
import json
import os
import re
import unicodedata
from pathlib import Path

import geopandas as gpd

SOCIAL = Path(__file__).resolve().parents[1]          # data/social
RAW = Path(os.environ.get("RAW", SOCIAL / "raw"))      # sources brutes, hors dépôt
TMP = Path(os.environ.get("TMP_SOCIAL", RAW / "tmp"))  # intermédiaires, hors dépôt

# Emprise de contrôle (data/CONVENTIONS.md §5)
BBOX = (8.4, 1.6, 16.2, 13.1)
# Tolérance (degrés) autour des limites geoBoundaries pour le filtre « dans le Cameroun ».
# - Couches OSM : 0 (l'extrait OSM déborde sur le Tchad, le Nigeria, le Congo : avec 1 km de
#   tolérance, Bongor, N'Djamena ou Gamboru passaient le filtre).
# - Sources déclarées « Cameroun » (healthsites, Maina) : ~1 km, pour absorber les imprécisions
#   du trait de côte et des frontières (ex. Bakassi, estuaire du Wouri).
TOL_FRONTIERE = 0.01

SRC_OSM = "OSM_OSMFR_2026-10-03"
SRC_HS = "HEALTHSITES_HDX_2026-09-29"
SRC_MAINA = "MAINA2019_FIGSHARE_7725374"

DATE_OSM = "2026-10-03"
DATE_HS = "2026-09-15"  # fin de la période couverte (HDX dataset_date) ; publication HDX 2026-09-29
DATE_MAINA = "2019"  # date exacte de situation non publiée (fichier daté 13/02/2019, publié 16/07/2019)


def charger_adm3():
    """Limites ADM3 geoBoundaries (non commitées). Corrige le mojibake UTF-8/Latin-1 des noms."""
    g = gpd.read_file(RAW / "gb_cmr_adm3.geojson")

    def fix(s):
        try:
            return s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return s

    g["arrondissement"] = g["shapeName"].map(fix)
    g = g.rename(columns={"shapeID": "gb_shape_id"})
    return g[["gb_shape_id", "arrondissement", "geometry"]]


def masque_cameroun(adm3, tolerance=TOL_FRONTIERE):
    u = adm3.geometry.union_all()
    return u.buffer(tolerance) if tolerance else u


def norm(s):
    """Minuscules, sans accents, ponctuation réduite à des espaces."""
    if s is None or (isinstance(s, float) and s != s):
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = s.replace("’", "'")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


# ---------------------------------------------------------------- Santé
RE_CENTRE = re.compile(
    r"\b(centre de sante|centre medical|center de sante|csi|cma|cmi|"
    r"health cent(er|re)|health post|dispensaire|poste de sante|case de sante|"
    r"integrated health)\b")


def _propre(tags):
    return {k: ("" if v is None or (isinstance(v, float) and v != v) else str(v))
            for k, v in tags.items()}


def classer_sante(tags):
    """Retourne (tg_type, regle). Règles documentées dans manifest.json."""
    tags = _propre(tags)
    a = tags.get("amenity", "")
    h = tags.get("healthcare", "")
    n = norm(tags.get("name", ""))
    if a == "hospital" or h == "hospital":
        return "SOC.SANTE.HOPITAL", "tag"
    if a == "pharmacy" or h == "pharmacy":
        return "SOC.SANTE.PHARMACIE", "tag"
    if h == "laboratory":
        return "SOC.SANTE.LABORATOIRE", "tag"
    if h == "centre":
        return "SOC.SANTE.CENTRE", "tag"
    if a in ("clinic", "doctors") or h in ("clinic", "doctor"):
        if RE_CENTRE.search(n):
            return "SOC.SANTE.CENTRE", "tag+nom"
        if a == "clinic" or h == "clinic":
            return "SOC.SANTE.CLINIQUE", "tag"
        return None, "non_classe"
    return None, "non_classe"


# ------------------------------------------------------------ Éducation
RE_TECH = re.compile(
    r"\b(technique|technical|techniques|professionnel|professionnelle|cetic|ceti|cetif|"
    r"sar|lycee technique|gths|gtc)\b")
RE_LYCEE = re.compile(r"\b(lycee|high school|ghs|gbhs|bilingual high)\b")
RE_COLLEGE = re.compile(r"\b(college|ces|ceg|cetic|secondary school|gss|comprehensive)\b")
RE_PRIMAIRE = re.compile(r"\b(ecole primaire|primary school|ep|epp|epb|gs|ecole publique)\b")
RE_MATERNELLE = re.compile(r"\b(maternelle|nursery|creche|jardin d enfants)\b")
RE_SUP = re.compile(r"\b(universite|university|faculte|faculty|ecole normale superieure|"
                    r"ens|enset|institut superieur|higher institute|iut|ecole superieure)\b")

ISCED = {"0": "SOC.EDU.MATERNELLE", "1": "SOC.EDU.PRIMAIRE",
         "2": "SOC.EDU.SECONDAIRE_1", "3": "SOC.EDU.SECONDAIRE_2"}


def classer_education(tags):
    """Retourne (tg_type, regle). Priorité : tag amenity non ambigu > isced:level > nom."""
    tags = _propre(tags)
    a = tags.get("amenity", "")
    n = norm(tags.get("name", ""))
    if a == "kindergarten":
        return "SOC.EDU.MATERNELLE", "tag"
    if a == "university":
        return "SOC.EDU.SUPERIEUR", "tag"
    isced = tags.get("isced:level", "").strip()
    if isced in ISCED and ";" not in isced:
        return ISCED[isced], "isced"
    if isced and isced.split(";")[0].strip() in ("5", "6", "7", "8"):
        return "SOC.EDU.SUPERIEUR", "isced"
    if not n:
        return None, "non_classe"
    if RE_SUP.search(n):
        return "SOC.EDU.SUPERIEUR", "tag+nom"
    if RE_MATERNELLE.search(n):
        # « école maternelle et primaire » : on retient le niveau primaire, signalé multi-niveaux
        if RE_PRIMAIRE.search(n) or "primary" in n or "primaire" in n:
            return "SOC.EDU.PRIMAIRE", "tag+nom;multi_niveaux"
        return "SOC.EDU.MATERNELLE", "tag+nom"
    # Techniques avant lycées/collèges (ex. « lycée technique », « CETIC »)
    if RE_TECH.search(n) and (RE_LYCEE.search(n) or RE_COLLEGE.search(n)
                              or re.search(r"\b(cetic|ceti|cetif|sar|gths|gtc)\b", n)):
        return "SOC.EDU.TECHNIQUE", "tag+nom"
    if RE_LYCEE.search(n):
        return "SOC.EDU.SECONDAIRE_2", "tag+nom"
    if RE_COLLEGE.search(n):
        return "SOC.EDU.SECONDAIRE_1", "tag+nom"
    if a == "school" and RE_PRIMAIRE.search(n):
        return "SOC.EDU.PRIMAIRE", "tag+nom"
    return None, "non_classe"


def ecrire_geojson(gdf, chemin):
    """GeoJSON EPSG:4326, 6 décimales max (CONVENTIONS §2)."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    gdf = gdf.to_crs(4326)
    fc = json.loads(gdf.to_json(drop_id=True, na="null"))
    for f in fc["features"]:
        x, y = f["geometry"]["coordinates"]
        f["geometry"]["coordinates"] = [round(x, 6), round(y, 6)]
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write('{"type":"FeatureCollection","features":[\n')
        fh.write(",\n".join(json.dumps(f, ensure_ascii=False, separators=(",", ":"))
                            for f in fc["features"]))
        fh.write("\n]}\n")
