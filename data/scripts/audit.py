"""Audit indépendant des données TasetyGrid (data/).

Vérifie, pour chaque fichier listé dans les manifest.json :
existence, sha256, nombre d'entités, emprise Cameroun, validité des géométries,
licence et champs de traçabilité, absence apparente de données personnelles.
Usage : python3 data/scripts/audit.py  -> écrit data/AUDIT.md
"""
import csv
import gzip
import hashlib
import json
import re
from pathlib import Path

from shapely.geometry import shape
from shapely.validation import explain_validity

DATA = Path(__file__).resolve().parent.parent
BBOX = (8.3, 1.5, 16.3, 13.2)  # emprise Cameroun, avec marge
CHAMPS_MANIFESTE = ["fichier", "licence", "url", "date_telechargement", "methode", "limites"]
LICENCES_OK = re.compile(r"CC[ -]?BY|CC0|ODbL|domaine public|public domain|Open Government|IGO", re.I)
PERSONNEL = re.compile(r"\b(phone|telephone|téléphone|contact:phone|email|e-mail|owner|proprietaire|propriétaire|operator:person|chef_nom)\b", re.I)


def charger(p):
    raw = p.read_bytes()
    if p.suffix == ".gz":
        raw = gzip.decompress(raw)
    return raw


def entrees_manifeste(m):
    if isinstance(m, list):
        return m
    for cle in ("fichiers", "files", "couches", "datasets", "entries"):
        if isinstance(m.get(cle), list):
            return m[cle]
    return [m] if "fichier" in m else []


def auditer_geojson(p):
    gj = json.loads(charger(p))
    feats = gj.get("features", [])
    hors, invalides, vides, perso = 0, 0, 0, set()
    for f in feats:
        g = f.get("geometry")
        if not g:
            vides += 1
            continue
        s = shape(g)
        if not s.is_valid:
            invalides += 1
        x0, y0, x1, y1 = s.bounds
        if x1 < BBOX[0] or x0 > BBOX[2] or y1 < BBOX[1] or y0 > BBOX[3]:
            hors += 1
        for k in (f.get("properties") or {}):
            if PERSONNEL.search(k):
                perso.add(k)
    return len(feats), hors, invalides, vides, sorted(perso)


def main():
    lignes, alertes, docs = [], [], []
    manifestes = sorted(DATA.glob("*/manifest.json")) + sorted(DATA.glob("*/*/manifest.json"))
    vus = set()
    for mp in manifestes:
        m = json.loads(mp.read_text(encoding="utf-8"))
        for e in entrees_manifeste(m):
            nom = e.get("fichier") or e.get("file") or e.get("path")
            if not nom:  # fiche de documentation (source non publiée, licence incompatible, inaccessible)
                docs.append(f"{mp.parent.name} : {e.get('source_code', '?')} — {str(e.get('limites', ''))[:160]}")
                continue
            candidats = [DATA / nom, mp.parent / nom, DATA.parent / nom]
            p = next((c for c in candidats if c.exists()), candidats[0])
            vus.add(p.resolve())
            manque = [c for c in CHAMPS_MANIFESTE if not e.get(c) and not e.get({"fichier": "file", "licence": "license"}.get(c, c))]
            lic = str(e.get("licence") or e.get("license") or "")
            statut = []
            if not p.exists():
                lignes.append((str(nom), "—", "—", "FICHIER ABSENT", lic))
                alertes.append(f"{nom} : fichier absent")
                continue
            sha = hashlib.sha256(p.read_bytes()).hexdigest()
            attendu = e.get("sha256_fichier") or e.get("sha256")
            if attendu and attendu != sha:
                statut.append("sha256 différent")
            if not attendu:
                statut.append("sha256 non déclaré")
            if not LICENCES_OK.search(lic):
                statut.append(f"licence à vérifier ({lic or 'absente'})")
            if manque:
                statut.append("manifeste incomplet : " + ", ".join(manque))
            n = "—"
            if p.name.endswith((".geojson", ".geojson.gz")):
                n, hors, inval, vides, perso = auditer_geojson(p)
                if hors:
                    statut.append(f"{hors} hors emprise")
                if inval:
                    statut.append(f"{inval} géométries invalides")
                if vides:
                    statut.append(f"{vides} sans géométrie")
                if perso:
                    statut.append("champs possiblement personnels : " + ", ".join(perso))
                declare = e.get("nb_entites")
                if isinstance(declare, int) and declare != n:
                    statut.append(f"nb_entites déclaré {declare} ≠ {n}")
            elif p.suffix == ".csv":
                with p.open(encoding="utf-8") as fh:
                    n = sum(1 for _ in csv.reader(fh)) - 1
            taille = f"{p.stat().st_size / 1e6:.1f} Mo"
            lignes.append((str(p.relative_to(DATA)), str(n), taille, "; ".join(statut) or "OK", lic))
            for s in statut:
                alertes.append(f"{p.relative_to(DATA)} : {s}")
    orphelins = [f for f in DATA.rglob("*") if f.is_file() and f.suffix in (".geojson", ".gz", ".csv")
                 and f.resolve() not in vus and "scripts" not in f.parts]
    with (DATA / "AUDIT.md").open("w", encoding="utf-8") as out:
        out.write("# Audit des données TasetyGrid\n\nGénéré par `data/scripts/audit.py`. "
                  "Contrôles : présence, sha256, comptes, emprise Cameroun, validité des géométries, licence, "
                  "champs de traçabilité, champs possiblement personnels.\n\n")
        out.write("| Fichier | Entités / lignes | Taille | Contrôles | Licence |\n|---|---|---|---|---|\n")
        for l in lignes:
            out.write("| " + " | ".join(x.replace("|", "/") for x in l) + " |\n")
        out.write("\n## Sources documentées mais non publiées\n\n")
        for d in docs:
            out.write(f"- {d}\n")
        out.write(f"\n**Fichiers de données non déclarés dans un manifeste : {len(orphelins)}**\n")
        for f in orphelins:
            out.write(f"- `{f.relative_to(DATA)}`\n")
    for d in docs:
        print(" · doc :", d)
    print(f"{len(lignes)} fichiers audités, {len(alertes)} alertes, {len(orphelins)} orphelins")
    for a in alertes:
        print(" -", a)
    for f in orphelins:
        print(" - orphelin :", f.relative_to(DATA))


if __name__ == "__main__":
    main()
