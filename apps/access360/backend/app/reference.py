"""Bundled public reference data: the country list, the indicator definitions and the readers of the derived files
in app/public_data/. Nothing here computes or fills in a value: indicator values are the latest non-empty value
of each source column, with the year it refers to. Provenance is in app/public_data/manifest.json and
docs/public-data-manifest.md."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "public_data"

# The 54 UN member states in Africa (ISO 3166-1 alpha-3), used for the country selector and as the ingestion filter.
AFRICA = [("DZA", "Algeria"), ("AGO", "Angola"), ("BEN", "Benin"), ("BWA", "Botswana"), ("BFA", "Burkina Faso"),
          ("BDI", "Burundi"), ("CPV", "Cabo Verde"), ("CMR", "Cameroon"), ("CAF", "Central African Republic"), ("TCD", "Chad"),
          ("COM", "Comoros"), ("COG", "Congo"), ("COD", "Democratic Republic of the Congo"), ("CIV", "Côte d'Ivoire"),
          ("DJI", "Djibouti"), ("EGY", "Egypt"), ("GNQ", "Equatorial Guinea"), ("ERI", "Eritrea"), ("SWZ", "Eswatini"),
          ("ETH", "Ethiopia"), ("GAB", "Gabon"), ("GMB", "Gambia"), ("GHA", "Ghana"), ("GIN", "Guinea"), ("GNB", "Guinea-Bissau"),
          ("KEN", "Kenya"), ("LSO", "Lesotho"), ("LBR", "Liberia"), ("LBY", "Libya"), ("MDG", "Madagascar"), ("MWI", "Malawi"),
          ("MLI", "Mali"), ("MRT", "Mauritania"), ("MUS", "Mauritius"), ("MAR", "Morocco"), ("MOZ", "Mozambique"),
          ("NAM", "Namibia"), ("NER", "Niger"), ("NGA", "Nigeria"), ("RWA", "Rwanda"), ("STP", "Sao Tome and Principe"),
          ("SEN", "Senegal"), ("SYC", "Seychelles"), ("SLE", "Sierra Leone"), ("SOM", "Somalia"), ("ZAF", "South Africa"),
          ("SSD", "South Sudan"), ("SDN", "Sudan"), ("TZA", "United Republic of Tanzania"), ("TGO", "Togo"), ("TUN", "Tunisia"),
          ("UGA", "Uganda"), ("ZMB", "Zambia"), ("ZWE", "Zimbabwe")]
AFRICA_ISO = {a for a, _ in AFRICA}

# OWID columns shown in the country profile, in display order (titles, units and sources come from the codebook)
OWID_COLUMNS = ["electricity_generation", "per_capita_electricity", "electricity_demand", "electricity_demand_per_capita",
                "renewables_share_elec", "solar_share_elec", "fossil_share_elec"]
WDI_KEY = "access_to_electricity"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest() -> dict:
    return json.loads((DATA_DIR / "manifest.json").read_text(encoding="utf-8"))


def source(key: str, man: dict | None = None) -> dict:
    return next(s for s in (man or manifest())["sources"] if s["key"] == key)


def latest(rows: list[dict], code_col: str, iso3: str, value_col: str, year_col: str) -> tuple[float | None, int | None]:
    """Latest year with a non-empty value for one country and one column; (None, None) if there is none."""
    best: tuple[int, str] | None = None
    for r in rows:
        if r[code_col] != iso3 or r[value_col] in ("", None):
            continue
        y = int(r[year_col])
        if best is None or y > best[0]:
            best = (y, r[value_col])
    return (float(best[1]), best[0]) if best else (None, None)


def read_csv(name: str) -> list[dict]:
    with open(DATA_DIR / name, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def indicator_definitions(man: dict | None = None) -> list[dict]:
    """Definitions in display order: access to electricity (WDI) first, then the OWID electricity columns."""
    man = man or manifest()
    wdi = source("wdi_eg_elc_accs_zs", man)
    owid = source("owid_energy", man)
    defs = [{"key": WDI_KEY, "column": "Value", "title": "Access to electricity (% of population)", "unit": "% of population",
             "description": "Access to electricity is the percentage of population with access to electricity. Electrification "
                            "data are collected from industry, national surveys and international sources.",
             "source": "World Bank, World Development Indicators (EG.ELC.ACCS.ZS)", "source_key": wdi["key"],
             "licence": wdi["licence"], "attribution": wdi["attribution"], "quality": wdi["quality"]}]
    codebook = {r["column"]: r for r in read_csv(owid["codebook_file"])}
    for c in OWID_COLUMNS:
        cb = codebook[c]
        defs.append({"key": c, "column": c, "title": cb["title"], "unit": cb["unit"], "description": cb["description"],
                     "source": cb["source"], "source_key": owid["key"], "licence": owid["licence"],
                     "attribution": owid["attribution"], "quality": owid["quality"]})
    return defs


def country_indicators(iso3: str, man: dict | None = None, owid_rows: list[dict] | None = None,
                       wdi_rows: list[dict] | None = None) -> list[dict]:
    man = man or manifest()
    owid_rows = owid_rows if owid_rows is not None else read_csv(source("owid_energy", man)["file"])
    wdi_rows = wdi_rows if wdi_rows is not None else read_csv(source("wdi_eg_elc_accs_zs", man)["file"])
    out = []
    for d in indicator_definitions(man):
        if d["key"] == WDI_KEY:
            v, y = latest(wdi_rows, "Country Code", iso3, "Value", "Year")
        else:
            v, y = latest(owid_rows, "iso_code", iso3, d["column"], "year")
        out.append({k: d[k] for k in d if k != "column"} | {"value": v, "year": y})
    return out
