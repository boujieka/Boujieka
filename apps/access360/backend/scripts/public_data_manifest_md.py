"""Regenerate docs/public-data-manifest.md from backend/app/public_data/manifest.json.

    python -I scripts/public_data_manifest_md.py app/public_data/manifest.json ../docs/public-data-manifest.md
"""
import json, sys
m = json.load(open(sys.argv[1]))
o = []
w = o.append
w("# Public reference data: manifest\n")
w("Bundled public data in `backend/app/public_data/`, loaded by `python -m app.ingest_public`. This file is generated from "
  "`backend/app/public_data/manifest.json` (the machine-readable record the ingestion checks SHA-256 values against).\n")
w(f"* Retrieval date of every file: **{m['retrieval_date']}**.")
w("* Raw downloads are **not** committed. They were kept outside git; their SHA-256 values are recorded below so that a re-download can be checked.")
w("* Every raw file was also checked against the git blob of the pinned commit (`git hash-object` equal to `git rev-parse <commit>:<path>`).")
w("* Derived files are produced by `backend/scripts/derive_public_data.py` (needs `shapely>=2.1`, build time only). Running it twice gives byte-identical files.")
w(f"* Polygon simplification: shapely 2.2 / GEOS 3.14 `coverage_simplify`, tolerance **{m['simplification_tolerance_deg']} degrees**, "
  "applied to the whole layer at once so that shared borders stay identical (no gaps or overlaps). The largest measured displacement "
  "(Hausdorff distance between an original and a simplified polygon) is given per file. Coordinates are rounded to 5 decimals. Points are not changed.")
w(f"* Natural Earth licence file checked: {m['licence_file']['url']} (SHA-256 `{m['licence_file']['sha256']}`).\n")
w("## Summary\n")
w("| Derived file | Bytes | SHA-256 | Source | Licence | Quality |")
w("|---|---|---|---|---|---|")
for s in m["sources"]:
    for d in s["derived"]:
        w(f"| `{d['file']}` | {d['bytes']:,} | `{d['sha256']}` | {s['source_institution']} | {s['licence']} | {s['quality']} |")
w("")
for s in m["sources"]:
    w(f"## {s['title']}\n")
    w(f"* Key: `{s['key']}` ({'platform dataset in `datasets`' if s['kind']=='dataset' else 'indicators in `country_profiles`'})")
    w(f"* Source institution: {s['source_institution']}")
    w(f"* Dataset title as published: {s['source_title']}")
    w(f"* Version / commit: {s['version']}")
    w(f"* Publication date: {s['publication_date']}")
    w(f"* Retrieval date: {s['retrieval_date']}")
    w(f"* Licence: {s['licence']}")
    if s.get("readme_licence_text"):
        w(f"* Licence text quoted from the repository README: \"{s['readme_licence_text']}\"")
    w(f"* Attribution text: {s['attribution']}")
    if s.get("provenance"):
        w(f"* Provenance stated by the mirror: {s['provenance']}")
    w(f"* Coverage: {s['geographic_coverage']}")
    w(f"* Resolution: {s['resolution']}")
    w(f"* Quality class: `{s['quality']}`")
    w(f"* Known limitations: {s['limitations']}\n")
    w("Raw files downloaded:\n")
    w("| URL downloaded | Pinned URL | File last changed in commit | Bytes | SHA-256 |")
    w("|---|---|---|---|---|")
    for r in s["raw"]:
        lc = f"`{r['file_last_commit'][:12]}` ({r.get('file_last_commit_date','')})" if r.get("file_last_commit") else "not recorded"
        w(f"| {r['url']} | {r.get('pinned_url', 'same')} | {lc} | {r['bytes']:,} | `{r['sha256']}` |")
    w("\nTransformations:\n")
    for t in s["transformations"]:
        w(f"1. {t}")
    w("\nDerived files:\n")
    for d in s["derived"]:
        w(f"* `{d['file']}`: {d['bytes']:,} bytes, SHA-256 `{d['sha256']}`")
    w("")
w("## Not ingested\n")
w("* World Bank API, Our World in Data catalogue, HDX, geoBoundaries: not reachable from the build environment (proxy 403). "
  "No value from them is used. The WDI access-to-electricity series comes from a mirror (see above) and is marked `secondary`.")
w("* The new OWID energy release (catalog.ourworldindata.org) was not reachable; the legacy GitHub release is used and its README says it is no longer updated.\n")
w("## How to refresh\n")
w("1. Download the raw files from the pinned URLs (or newer commits) into a scratch folder with the layout `ne/`, `owid/`, `wdi/`.")
w("2. Verify each file against its commit (`git hash-object`) and record the new commit in `scripts/derive_public_data.py` notes and the manifest.")
w("3. Run `python -I scripts/derive_public_data.py RAW_DIR app/public_data`, update `manifest.json` (hashes, dates, limitations) and regenerate this file (`python -I scripts/public_data_manifest_md.py app/public_data/manifest.json ../docs/public-data-manifest.md`).")
w("4. Run `python -m app.ingest_public`, then `python -m pytest tests/api/test_public_data.py` with `A360_PUBLIC_RAW_DIR=RAW_DIR` so profile values are compared with the raw CSVs.")
open(sys.argv[2], "w").write("\n".join(o) + "\n")
