"""Charge les données de data/ dans le schéma TasetyGrid (schema/schema_postgis.sql).

Chaque entité devient un `objet_spatial` + une `assertion` (statut IMPORTE : rien n'est
validé). Les limites ADM0-ADM3 alimentent `unite_territoriale`, la population par
arrondissement alimente `mesure` (est_estimation = vrai).

Usage : python3 data/scripts/charger_postgis.py "postgresql://user@host/base"
(le schéma doit déjà être créé avec schema/schema_postgis.sql)
"""
import csv
import gzip
import json
import sys
from datetime import date
from pathlib import Path

import psycopg
import yaml

RACINE = Path(__file__).resolve().parents[2]
DATA = RACINE / "data"

# Niveau de collecte selon la nature de la source (docs/04)
NIVEAUX = [
    ("OSM", "N0_DECLARATION"), ("HEALTHSITES", "N0_DECLARATION"), ("OURAIRPORTS", "N0_DECLARATION"),
    ("WORLDPOP", "N1_TELEDETECTION"), ("WORLDCOVER", "N1_TELEDETECTION"), ("GRIDFINDER", "N1_TELEDETECTION"),
    ("MINFOF", "N3_ADMINISTRATIF"), ("MAINA", "N3_ADMINISTRATIF"), ("OCHA", "N3_ADMINISTRATIF"),
    ("WPI", "N3_ADMINISTRATIF"), ("NGA", "N3_ADMINISTRATIF"),
]


def niveau(code):
    c = (code or "").upper()
    return next((n for k, n in NIVEAUX if k in c), "N0_DECLARATION")


def une_date(x):
    """AAAA-MM-JJ, AAAA-MM ou AAAA extraits d'un texte ; None si aucune date fiable."""
    import re
    m = re.search(r"(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?", str(x or ""))
    if not m:
        return None
    return f"{m.group(1)}-{m.group(2) or '01'}-{m.group(3) or '01'}"


def charger_json(p):
    b = p.read_bytes()
    return json.loads(gzip.decompress(b) if p.suffix == ".gz" else b)


def manifestes():
    for mp in sorted(DATA.glob("*/manifest.json")) + sorted(DATA.glob("*/*/manifest.json")):
        m = json.loads(mp.read_text(encoding="utf-8"))
        entrees = m if isinstance(m, list) else m.get("fichiers") or m.get("files") or [m]
        for e in entrees:
            nom = e.get("fichier")
            if not nom:
                continue
            p = next((c for c in (DATA / nom, mp.parent / nom, RACINE / nom) if c.exists()), None)
            if p:
                sc = e.get("source_code")
                if isinstance(sc, list):  # plusieurs sources combinées
                    e = {**e, "source_code": "+".join(map(str, sc))}
                yield mp, e, p


def main(dsn):
    with psycopg.connect(dsn, autocommit=False) as cx, cx.cursor() as cur:
        cur.execute("SET search_path = atlas, public")

        # 1. Nomenclatures
        objets = yaml.safe_load((RACINE / "nomenclatures/objets.yaml").read_text(encoding="utf-8"))
        mesures = yaml.safe_load((RACINE / "nomenclatures/mesures.yaml").read_text(encoding="utf-8"))
        lignes = [(c, "OBJET", v["fr"], v.get("en"), v.get("sensibilite", "S0_PUBLIC")) for c, v in objets.items()]
        lignes.append(("NON_CLASSE", "OBJET", "Objet non classé (type source conservé)", "Unclassified", "S0_PUBLIC"))
        lignes += [("MESURE." + c, "MESURE", v["fr"], None, "S0_PUBLIC") for c, v in mesures.items()]
        cur.executemany("""INSERT INTO nomenclature(code, domaine, libelle_fr, libelle_en, sensibilite_defaut)
                           VALUES (%s,%s,%s,%s,%s) ON CONFLICT (code) DO NOTHING""", lignes)
        connus = {c: s for c, _, _, _, s in lignes}

        # 2. Sources (une par fichier déclaré)
        sources = {}
        for mp, e, p in manifestes():
            code = (e.get("source_code") or p.stem)[:120] + "::" + p.name
            cur.execute("""INSERT INTO source(code, libelle, niveau, producteur, licence, date_reference, description)
                           VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (code) DO UPDATE SET licence = EXCLUDED.licence
                           RETURNING source_id""",
                        (code, p.name, niveau(e.get("source_code")), e.get("producteur"), e.get("licence"),
                         une_date(e.get("date_situation")) or une_date(e.get("date_telechargement")),
                         json.dumps({k: e.get(k) for k in ("url", "methode", "limites", "sha256_fichier")}, ensure_ascii=False)))
            sources[p.resolve()] = (cur.fetchone()[0], e)

        # 3. Référentiel territorial ADM0-ADM3
        types = {0: "PAYS", 1: "REGION", 2: "DEPARTEMENT", 3: "ARRONDISSEMENT"}
        ids = {}
        for n in range(4):
            p = DATA / f"admin/limites_adm{n}.geojson"
            src = sources.get(p.resolve(), (None,))[0]
            for f in charger_json(p)["features"]:
                pr = f["properties"]
                cur.execute("""INSERT INTO unite_territoriale(type, code_officiel, nom, parent_id, geom,
                                   version_referentiel, valide_depuis, officiel, source_id)
                               VALUES (%s,%s,%s,%s, ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(%s),4326)),
                                       'OCHA-COD-AB', %s, true, %s) RETURNING unite_id""",
                            (types[n], pr["code"], pr["nom"], ids.get(pr.get("parent_code")),
                             json.dumps(f["geometry"]), date.today(), src))
                ids[pr["code"]] = cur.fetchone()[0]

        # 4. Objets spatiaux + assertions
        bilan = {}
        for chemin, (src, e) in sources.items():
            if not chemin.name.endswith((".geojson", ".geojson.gz")) or "admin/limites_adm" in str(chemin):
                continue
            n = 0
            for f in charger_json(chemin)["features"]:
                if not f.get("geometry"):
                    continue
                pr = f.get("properties") or {}
                t = pr.get("tg_type") if pr.get("tg_type") in connus else "NON_CLASSE"
                cur.execute("""INSERT INTO objet_spatial(type_code, nom, geom, sensibilite)
                               VALUES (%s,%s, ST_SetSRID(ST_GeomFromGeoJSON(%s),4326), %s) RETURNING objet_id""",
                            (t, pr.get("nom"), json.dumps(f["geometry"]), connus[t]))
                oid = cur.fetchone()[0]
                if pr.get("source_id"):
                    cur.execute("""INSERT INTO identifiant_externe(objet_id, systeme, valeur, source_id)
                                   VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING""",
                                (oid, (pr.get("source") or e.get("source_code") or "SOURCE")[:60], str(pr["source_id"]), src))
                cur.execute("""INSERT INTO assertion(objet_id, attribut, valeur, statut, source_id, valide_depuis, sensibilite)
                               VALUES (%s,'existence',%s,'IMPORTE',%s,%s,%s)""",
                            (oid, json.dumps(pr, ensure_ascii=False, default=str), src,
                             une_date(pr.get("date_source")),
                             connus[t]))
                n += 1
            bilan[chemin.relative_to(DATA).as_posix()] = n

        # 5. Mesures : population estimée par arrondissement
        p = DATA / "population/population_par_arrondissement.csv"
        src = sources.get(p.resolve(), (None,))[0]
        import unicodedata

        import re

        ROMAINS = {"i": "1", "ii": "2", "iii": "3", "iv": "4", "v": "5", "vi": "6", "vii": "7"}

        def norm(x):
            x = unicodedata.normalize("NFKD", (x or "").lower())
            x = "".join(c for c in x if c.isalnum() or c in " -")
            # « Yaoundé I » (geoBoundaries) = « Yaoundé 1er » (OCHA) = « Bamenda 1st »
            x = re.sub(r"\b(\d+)\s*(er|re|e|eme|st|nd|rd|th)\b", r"\1", x)
            x = re.sub(r"\b(i{1,3}|iv|v|vi|vii)\b$", lambda m: ROMAINS[m.group(1)], x.strip())
            return "".join(c for c in x if c.isalnum())

        cur.execute("""SELECT a.unite_id, a.nom, d.nom FROM unite_territoriale a
                       JOIN unite_territoriale d ON d.unite_id = a.parent_id WHERE a.type='ARRONDISSEMENT'""")
        par_nom = {}
        for uid, nom, dep in cur.fetchall():
            par_nom.setdefault(norm(nom), []).append((uid, norm(dep)))
        nb_pop, non_rapproches = 0, []
        for r in csv.DictReader(p.open(encoding="utf-8")):
            cands = par_nom.get(norm(r["arrondissement_nom"])) or par_nom.get(norm(r.get("nom_minfof_2018"))) or []
            if len(cands) > 1:
                cands = [c for c in cands if c[1] == norm(r.get("departement"))] or []
            # Pas de rapprochement approché : il produit des erreurs (ex. Nkong-Zem ≠ Nkongni).
            # Les unités restantes viennent de versions de limites différentes (geoBoundaries vs OCHA) :
            # il faut recalculer la population sur les limites OCHA (zonal statistics), pas deviner.
            if len(cands) != 1 or not src or not r.get("pop_2025"):
                non_rapproches.append(r["arrondissement_nom"])
                continue
            cur.execute("""INSERT INTO mesure(unite_id, indicateur, valeur, est_estimation, date_reference, source_id)
                           VALUES (%s,'MESURE.POP_TOTALE',%s,true,'2025-07-01',%s)""", (cands[0][0], float(r["pop_2025"]), src))
            nb_pop += 1
        if non_rapproches:
            print(f"Arrondissements non rapprochés par le nom ({len(non_rapproches)}) : {', '.join(non_rapproches)}")
        cx.commit()
        for k, v in sorted(bilan.items()):
            print(f"{v:>7}  {k}")
        print(f"{len(ids):>7}  unités territoriales ; {nb_pop} mesures de population")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "postgresql://postgres@/tasetygrid")
