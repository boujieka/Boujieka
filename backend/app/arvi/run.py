"""ARVI pilot pipeline.

    python -m app.arvi.run fetch     # UN Comtrade -> var/arvi/flows.json (+ raw archive, manifest)
    python -m app.arvi.run compute   # flows.json -> var/arvi/indicators.json
    python -m app.arvi.run all

The manifest (URLs, SHA-256, fetch times, record counts; no trade values) is also copied to
app/arvi/data/manifest.json so a published release can be re-fetched and checked.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from app.arvi.comtrade import DATA_DIR, Archive, Comtrade, Flow, area_codes, normalise, partner_names
from app.arvi.mirror import CIF_FOB_BAND, build_cells, indicators, score_cells
from app.arvi.taxonomy import HUB_PARTNERS, LANDLOCKED, PILOT, RESOURCES, YEARS
from app.seed.africa import AFRICA

METHODOLOGY_VERSION = "0.1-pilot"
COMMITTED_MANIFEST = Path(__file__).resolve().parent / "data" / "manifest.json"


def fetch(root: Path = DATA_DIR) -> None:
    archive = Archive(root)
    api = Comtrade(archive)
    reporters, partners = api.reference("Reporters"), api.reference("partnerAreas")
    codes, iso_to_code = area_codes(reporters, partners)
    flows: dict[tuple, Flow] = {}
    for iso, res_keys in PILOT.items():
        hs = [c for k in res_keys for c in RESOURCES[k].hs_codes]
        code = iso_to_code[iso]
        for kind, kw in (("exports", {"flow": "X", "reporter": code}),
                         ("mirror", {"flow": "M", "partner": code})):
            rows = api.query(cmd=hs, years=YEARS, **kw)
            kept = 0
            for rec, sha in rows:
                f = normalise(rec, sha, codes)
                if f is None:
                    continue
                key = (f.reporter, f.partner, f.flow, f.hs, f.year)
                if key in flows:
                    raise RuntimeError(f"duplicate flow {key}")
                flows[key] = f
                kept += 1
            print(f"{iso} {kind}: {len(rows)} records, {kept} kept")
    (root / "flows.json").write_text(json.dumps([f.to_json() for f in flows.values()]))
    (root / "partners.json").write_text(json.dumps(partner_names(partners), ensure_ascii=False))
    COMMITTED_MANIFEST.parent.mkdir(exist_ok=True)
    shutil.copy(archive.manifest_path, COMMITTED_MANIFEST)
    print(f"{len(flows)} flows written")


def compute(root: Path = DATA_DIR) -> dict:
    flows = [Flow.from_json(d) for d in json.loads((root / "flows.json").read_text())]
    cells = build_cells(flows)
    score_cells(cells)
    names = {c.iso3: c.name_fr for c in AFRICA}
    manifest = json.loads((root / "manifest.json").read_text())
    result = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "methodology_version": METHODOLOGY_VERSION,
            "years": list(YEARS),
            "source": "UN Comtrade (Division de statistique des Nations unies), API publique, "
                      "données annuelles SH ; valeurs en USD courants, quantités en poids net.",
            "responses": len(manifest),
            "first_fetch": min(m["fetched_at"] for m in manifest),
            "last_fetch": max(m["fetched_at"] for m in manifest),
            "cif_fob_band": [str(b) for b in CIF_FOB_BAND],
            "hub_partners": sorted(HUB_PARTNERS), "landlocked": sorted(LANDLOCKED),
            "flows": len(flows), "cells": len(cells),
        },
        "countries": {iso: {"name_fr": names[iso], "resources": list(r)} for iso, r in PILOT.items()},
        "resources": {k: {"name_fr": r.name_fr, "family": r.family,
                          "stages": [{"order": s.order, "name_fr": s.name_fr, "hs": list(s.hs_codes)}
                                     for s in r.stages]}
                      for k, r in RESOURCES.items()},
        "partners": json.loads((root / "partners.json").read_text()),
        "results": indicators(cells),
    }
    (root / "indicators.json").write_text(json.dumps(result, ensure_ascii=False))
    print(f"{len(result['results'])} country-resource-year results from {len(cells)} cells")
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("step", choices=["fetch", "compute", "all"])
    args = p.parse_args()
    if args.step in ("fetch", "all"):
        fetch()
    if args.step in ("compute", "all"):
        compute()


if __name__ == "__main__":
    main()
