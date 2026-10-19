"""Consolide les registres de sources et les indicateurs par domaine, et contrôle leur cohérence.

python3 cameroun/models/build_registers.py
Entrées  : sources/registre_<domaine>.csv, data/raw/indicateurs_<domaine>.csv, data/clean/wdi_cmr.csv
Sorties  : sources/registre_sources.csv, data/clean/indicateurs_consolides.csv,
           outputs/controle_registres.txt (anomalies : colonnes manquantes, source_id orphelins, doublons d'URL)
"""
import collections
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC_COLS = ["source_id", "titre", "organisme", "type_source", "url", "localisation_dans_doc", "annee_observee",
            "date_publication", "date_consultation", "domaine", "niveau_acces", "notes"]
IND_COLS = ["indicateur", "valeur", "unite", "annee_observee", "perimetre", "statut", "source_id",
            "localisation", "remarque"]


STATUS_MAP = [  # (préfixe du statut brut, statut normalisé) ; l'ordre compte
    ("observ", "observe"), ("estimation", "estimation"), ("prévision", "prevision"), ("prevision", "prevision"),
    ("cible", "cible"), ("budget_vote", "budget_vote"), ("budget", "budget_annonce"),
    ("financement approuvé", "financement_approuve"), ("annonce", "annonce"),
    ("resultat", "resultat"), ("résultat", "resultat"), ("decision", "decision"), ("décision", "decision"),
]


def normalize_status(raw):
    s = raw.strip().lower()
    for prefix, norm in STATUS_MAP:
        if s.startswith(prefix):
            return norm
    return "a_classer"


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    issues, sources = [], []
    for p in sorted((ROOT / "sources").glob("registre_*.csv")):
        if p.name == "registre_sources.csv":
            continue
        rows = read(p)
        missing = set(SRC_COLS) - set(rows[0].keys() if rows else SRC_COLS)
        if missing:
            issues.append(f"{p.name}: colonnes manquantes {sorted(missing)}")
        for r in rows:
            r["fichier"] = p.name
            sources.append(r)

    # Source WDI (une ligne par indicateur téléchargé par fetch_wdi.py)
    wdi = read(ROOT / "data/clean/wdi_cmr.csv")
    seen = {}
    for r in wdi:
        seen.setdefault(r["code"], r)
    for i, (code, r) in enumerate(sorted(seen.items()), 1):
        years = sorted(x["annee"] for x in wdi if x["code"] == code)
        sources.append({
            "source_id": f"WDI-{i:03d}", "titre": f"World Development Indicators — {r['libelle_bm']} ({code})",
            "organisme": "Banque mondiale", "type_source": "internationale", "url": r["source_url"],
            "localisation_dans_doc": f"API {r['api_url']}", "annee_observee": f"{years[0]}-{years[-1]}",
            "date_publication": "base WDI (mise à jour continue)", "date_consultation": r["date_consultation"],
            "domaine": "transversal", "niveau_acces": "lu_document",
            "notes": "Série compilée ; vérifier la métadonnée (estimations modélisées possibles)", "fichier": "wdi"})

    ids = collections.Counter(r["source_id"] for r in sources)
    for k, n in ids.items():
        if n > 1:
            issues.append(f"source_id dupliqué : {k} ({n})")
    urls = collections.defaultdict(list)
    for r in sources:
        if r.get("url"):
            urls[r["url"].strip()].append(r["source_id"])
    for u, l in urls.items():
        if len(l) > 1:
            issues.append(f"même URL dans plusieurs entrées (à fusionner ?) : {u} -> {l}")

    with open(ROOT / "sources/registre_sources.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=SRC_COLS + ["fichier"], extrasaction="ignore")
        w.writeheader()
        w.writerows(sources)

    inds = []
    for p in sorted((ROOT / "data/raw").glob("indicateurs_*.csv")):
        for r in read(p):
            r["fichier"] = p.name
            r["statut_brut"] = r.get("statut", "")
            r["statut"] = normalize_status(r["statut_brut"])
            inds.append(r)
            for sid in (r.get("source_id") or "").replace(";", " ").split():
                if sid not in ids:
                    issues.append(f"{p.name}: source_id inconnu '{sid}' pour « {r.get('indicateur')} »")
    with open(ROOT / "data/clean/indicateurs_consolides.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=IND_COLS + ["statut_brut", "fichier"], extrasaction="ignore")
        w.writeheader()
        w.writerows(inds)

    # Références du registre des problèmes
    prob = ROOT / "analyses/registre_problemes.csv"
    if prob.exists():
        for r in read(prob):
            for sid in r["sources"].replace(";", " ").split():
                if not sid.startswith("WDI") and sid not in ids:
                    issues.append(f"registre_problemes {r['id']}: source_id inconnu '{sid}'")

    acc = collections.Counter(r.get("niveau_acces", "") for r in sources)
    typ = collections.Counter(r.get("type_source", "") for r in sources)
    stat = collections.Counter(r.get("statut", "") for r in inds)
    report = [f"Sources : {len(sources)}", f"  par niveau d'accès : {dict(acc)}", f"  par type : {dict(typ)}",
              f"Indicateurs (hors WDI) : {len(inds)}", f"  par statut : {dict(stat)}",
              f"Anomalies : {len(issues)}"] + ["  - " + i for i in issues]
    (ROOT / "outputs/controle_registres.txt").write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report[:6]))


if __name__ == "__main__":
    main()
