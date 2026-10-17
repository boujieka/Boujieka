"""Fusionne les résultats des agents de recherche et leur vérification automatique.

    python import_research.py <dossier_brut>

Lit <dossier>/*.json (une tranche par fichier) et <dossier>/verif_*.json (sortie de
verify_citations.py), puis écrit recherche/donnees.json : chaque enregistrement porte son
statut de vérification et sa catégorie d'usage :
  retenu      chiffre retrouvé dans la citation, citation retrouvée dans la source (exacte ou ≥ 85 %)
  qualitatif  valeur textuelle dont la citation est retrouvée dans la source
  a_revoir    citation absente, valeur non citée telle quelle (dérivée, additionnée) ou source inaccessible
build_workbook.py lit ce fichier pour remplir les onglets Recherche_retenue et Recherche_a_revoir.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

OUT = Path(__file__).with_name("recherche") / "donnees.json"
USAGE = {"confirmé": "retenu", "citation_partielle": "retenu", "qualitatif_citation_ok": "qualitatif"}


def main(folder: str) -> None:
    src = Path(folder)
    rows, conflits, non_trouve = [], [], []
    for f in sorted(src.glob("*.json")):
        if f.name.startswith("verif_") or f.name == "IRENA.json":
            continue
        data = json.loads(f.read_text())
        vf = src / f"verif_{f.name}"
        verif = {v["index"]: v for v in json.loads(vf.read_text())} if vf.exists() else {}
        tranche = f.stem
        for i, rec in enumerate(data.get("records", [])):
            v = verif.get(i, {"statut": "non_verifie"})
            rows.append({"tranche": tranche, **rec, "verification": v["statut"],
                         "usage": USAGE.get(v["statut"], "a_revoir")})
        conflits += [{"tranche": tranche, "conflit": c} for c in data.get("conflits", [])]
        non_trouve += [{"tranche": tranche, "element": n} for n in data.get("non_trouve", [])]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"records": rows, "conflits": conflits, "non_trouve": non_trouve},
                              ensure_ascii=False, indent=1))
    print(len(rows), "enregistrements ;", Counter(r["usage"] for r in rows))
    for t, n in sorted(Counter((r["tranche"], r["usage"]) for r in rows).items()):
        print(" ", t, n)


if __name__ == "__main__":
    main(sys.argv[1])
