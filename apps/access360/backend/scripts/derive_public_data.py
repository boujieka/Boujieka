"""Derive the bundled public reference data (backend/app/public_data/) from the raw downloads.

This script is a build step, not part of the API. It needs `shapely>=2.1` (GEOS 3.12 or later, for
`coverage_simplify`), which is deliberately not a backend runtime dependency:

    python3.11 -m venv /tmp/dvenv && /tmp/dvenv/bin/pip install "shapely>=2.1"
    /tmp/dvenv/bin/python -I scripts/derive_public_data.py RAW_DIR app/public_data

RAW_DIR must hold the files exactly as downloaded (see docs/public-data-manifest.md for URLs and commits):
    ne/ne_10m_admin_0_countries.geojson, ne/ne_10m_admin_1_states_provinces.geojson,
    ne/ne_10m_populated_places_simple.geojson, owid/owid-energy-data.csv, owid/owid-energy-codebook.csv,
    wdi/data.csv

Rules: values are copied, never computed or filled in. Tabular rows are copied verbatim (same strings) after
filtering to the 54 African UN member states. Polygons are simplified with a documented tolerance and the
resulting maximum displacement (Hausdorff distance) is measured and written to the manifest.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import shapely
from shapely.geometry import mapping, shape

AFRICA54 = ("DZA AGO BEN BWA BFA BDI CPV CMR CAF TCD COM COG COD CIV DJI EGY GNQ ERI SWZ ETH GAB GMB GHA GIN GNB KEN LSO "
            "LBR LBY MDG MWI MLI MRT MUS MAR MOZ NAM NER NGA RWA STP SEN SYC SLE SOM ZAF SSD SDN TZA TGO TUN UGA ZMB ZWE").split()
# Natural Earth uses its own ADM0_A3 code "SDS" for South Sudan (ISO 3166-1 alpha-3: SSD).
NE_TO_ISO = {"SDS": "SSD"}
# Units that Natural Earth maps separately in Africa but that are not among the 54 UN member states.
NE_EXTRA_UNITS = {"SOL", "SAH"}

ADMIN_TOLERANCE_DEG = 0.005   # coverage_simplify tolerance (degrees), see manifest
COORD_DECIMALS = 5            # about 1.1 m at the equator; far below the 1:10m source accuracy
OWID_COLUMNS = ["electricity_generation", "per_capita_electricity", "renewables_share_elec", "solar_share_elec",
                "fossil_share_elec", "electricity_demand", "electricity_demand_per_capita"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iso_of(adm0_a3: str) -> str | None:
    code = NE_TO_ISO.get(adm0_a3, adm0_a3)
    return code if code in AFRICA54 else None


def rnd(geom: dict) -> dict:
    def r(c):
        if isinstance(c[0], (int, float)):
            return [round(c[0], COORD_DECIMALS), round(c[1], COORD_DECIMALS)]
        return [r(x) for x in c]
    return {"type": geom["type"], "coordinates": r(geom["coordinates"])}


def simplify_coverage(features: list[dict]) -> tuple[list[dict], float]:
    """Topology aware simplification of a polygon coverage (shared borders stay identical). Returns the new
    features and the largest Hausdorff distance (degrees) between an original and a simplified polygon."""
    geoms = [shape(f["geometry"]) for f in features]
    geoms = [g if g.is_valid else shapely.make_valid(g) for g in geoms]
    simp = shapely.coverage_simplify(geoms, ADMIN_TOLERANCE_DEG, simplify_boundary=True)
    out, worst = [], 0.0
    for f, g0, g1 in zip(features, geoms, simp):
        if not g1.is_valid:
            g1 = shapely.make_valid(g1)
        if g1.geom_type == "GeometryCollection":
            g1 = shapely.union_all([p for p in g1.geoms if p.geom_type in ("Polygon", "MultiPolygon")])
        worst = max(worst, g0.hausdorff_distance(g1))
        out.append({"type": "Feature", "properties": f["properties"], "geometry": rnd(mapping(g1))})
    return out, worst


def write_json(p: Path, obj) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main(raw: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    stats: dict[str, dict] = {}

    # 1. admin 0 (10m)
    src = json.loads((raw / "ne/ne_10m_admin_0_countries.geojson").read_text(encoding="utf-8"))
    feats = []
    for f in src["features"]:
        p = f["properties"]
        iso = p["ISO_A3_EH"] if p["ISO_A3_EH"] in AFRICA54 else None
        if iso is None and p["ADM0_A3"] not in NE_EXTRA_UNITS:
            continue
        feats.append({"type": "Feature", "geometry": f["geometry"], "properties": {
            "iso3": iso, "ne_adm0_a3": p["ADM0_A3"], "name": p["NAME"], "name_long": p["NAME_LONG"],
            "name_en": p["NAME_EN"], "name_fr": p["NAME_FR"], "ne_type": p["TYPE"],
            "un_member_54": iso is not None}})
    feats.sort(key=lambda f: f["properties"]["ne_adm0_a3"])
    feats, worst0 = simplify_coverage(feats)
    write_json(out / "ne_admin0_africa.geojson", {"type": "FeatureCollection", "features": feats})
    stats["ne_admin0_africa.geojson"] = {"features": len(feats), "max_hausdorff_deg": round(worst0, 6),
                                         "isos": sorted({f["properties"]["iso3"] for f in feats if f["properties"]["iso3"]})}

    # 2. admin 1 (10m)
    src = json.loads((raw / "ne/ne_10m_admin_1_states_provinces.geojson").read_text(encoding="utf-8"))
    feats = []
    for f in src["features"]:
        p = f["properties"]
        iso = iso_of(p["adm0_a3"])
        if iso is None and p["adm0_a3"] not in NE_EXTRA_UNITS:
            continue
        feats.append({"type": "Feature", "geometry": f["geometry"], "properties": {
            "iso3": iso, "ne_adm0_a3": p["adm0_a3"], "admin": p["admin"], "adm1_code": p["adm1_code"],
            "iso_3166_2": p["iso_3166_2"], "name": p["name"], "name_fr": p["name_fr"], "type_en": p["type_en"],
            "type_local": p["type"]}})
    feats.sort(key=lambda f: (f["properties"]["ne_adm0_a3"], f["properties"]["adm1_code"]))
    feats, worst1 = simplify_coverage(feats)
    write_json(out / "ne_admin1_africa.geojson", {"type": "FeatureCollection", "features": feats})
    stats["ne_admin1_africa.geojson"] = {"features": len(feats), "max_hausdorff_deg": round(worst1, 6),
                                         "isos": sorted({f["properties"]["iso3"] for f in feats if f["properties"]["iso3"]})}

    # 3. populated places (points: copied, not simplified or rounded)
    src = json.loads((raw / "ne/ne_10m_populated_places_simple.geojson").read_text(encoding="utf-8"))
    keep = ["name", "nameascii", "namealt", "featurecla", "adm0name", "adm0_a3", "adm1name", "adm0cap", "worldcity",
            "megacity", "pop_max", "pop_min", "pop_other", "latitude", "longitude", "ne_id"]
    feats = []
    for f in src["features"]:
        p = f["properties"]
        iso = iso_of(p["adm0_a3"])
        if iso is None:
            continue
        feats.append({"type": "Feature", "geometry": f["geometry"], "properties": {"iso3": iso, **{k: p.get(k) for k in keep}}})
    feats.sort(key=lambda f: (f["properties"]["iso3"], f["properties"]["ne_id"]))
    write_json(out / "ne_populated_places_africa.geojson", {"type": "FeatureCollection", "features": feats})
    stats["ne_populated_places_africa.geojson"] = {"features": len(feats)}

    # 4. OWID energy: verbatim rows of the 54 countries, selected columns, rows with at least one value
    with open(raw / "owid/owid-energy-data.csv", encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        cols = ["country", "year", "iso_code", *OWID_COLUMNS]
        rows = [{k: r[k] for k in cols} for r in rd if r["iso_code"] in AFRICA54 and any(r[c] != "" for c in OWID_COLUMNS)]
    with open(out / "owid_energy_africa.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    stats["owid_energy_africa.csv"] = {"rows": len(rows), "countries": len({r["iso_code"] for r in rows})}
    with open(raw / "owid/owid-energy-codebook.csv", encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        fields = rd.fieldnames
        cb = [r for r in rd if r["column"] in OWID_COLUMNS]
    with open(out / "owid_energy_codebook_subset.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(cb)
    stats["owid_energy_codebook_subset.csv"] = {"rows": len(cb)}

    # 5. WDI access to electricity: verbatim rows of the 54 countries
    with open(raw / "wdi/data.csv", encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        fields = rd.fieldnames
        rows = [r for r in rd if r["Country Code"] in AFRICA54]
    with open(out / "wdi_eg_elc_accs_zs_africa.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    stats["wdi_eg_elc_accs_zs_africa.csv"] = {"rows": len(rows), "countries": len({r["Country Code"] for r in rows})}

    raw_files = ["ne/ne_10m_admin_0_countries.geojson", "ne/ne_10m_admin_1_states_provinces.geojson",
                 "ne/ne_10m_populated_places_simple.geojson", "ne/LICENSE.md", "owid/owid-energy-data.csv",
                 "owid/owid-energy-codebook.csv", "owid/README.md", "wdi/data.csv", "wdi/datapackage.json"]
    for name in stats:
        stats[name]["sha256"] = sha256(out / name)
        stats[name]["bytes"] = (out / name).stat().st_size
    result = {"tolerance_deg": ADMIN_TOLERANCE_DEG, "coord_decimals": COORD_DECIMALS, "derived": stats,
              "raw": {f: {"sha256": sha256(raw / f), "bytes": (raw / f).stat().st_size} for f in raw_files}}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
