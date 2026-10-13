# Public reference data: manifest

Bundled public data in `backend/app/public_data/`, loaded by `python -m app.ingest_public`. This file is generated from `backend/app/public_data/manifest.json` (the machine-readable record the ingestion checks SHA-256 values against).

* Retrieval date of every file: **2026-10-13**.
* Raw downloads are **not** committed. They were kept outside git; their SHA-256 values are recorded below so that a re-download can be checked.
* Every raw file was also checked against the git blob of the pinned commit (`git hash-object` equal to `git rev-parse <commit>:<path>`).
* Derived files are produced by `backend/scripts/derive_public_data.py` (needs `shapely>=2.1`, build time only). Running it twice gives byte-identical files.
* Polygon simplification: shapely 2.2 / GEOS 3.14 `coverage_simplify`, tolerance **0.005 degrees**, applied to the whole layer at once so that shared borders stay identical (no gaps or overlaps). The largest measured displacement (Hausdorff distance between an original and a simplified polygon) is given per file. Coordinates are rounded to 5 decimals. Points are not changed.
* Natural Earth licence file checked: https://raw.githubusercontent.com/nvkelso/natural-earth-vector/ca96624a56bd078437bca8184e78163e5039ad19/LICENSE.md (SHA-256 `2631b5b39b6d1acc56de75235109b5af2dbb4b0ac5a127b6f06185977247fd4b`).

## Summary

| Derived file | Bytes | SHA-256 | Source | Licence | Quality |
|---|---|---|---|---|---|
| `ne_admin0_africa.geojson` | 868,344 | `ad428d89866f02c90f4ff16fbacbbbe4e9bf2ead2978abb38f97c701fb3ee028` | Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors) | Public domain (Natural Earth LICENSE.md: "Everything here is public domain.") | verified_source |
| `ne_admin1_africa.geojson` | 2,857,573 | `c87545895ce0b89c5818673fcdce11155abad6bbfa1cec2abdfbb2ec1c379881` | Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors) | Public domain (Natural Earth LICENSE.md: "Everything here is public domain.") | verified_source |
| `ne_populated_places_africa.geojson` | 522,630 | `85162260e76a0de1e4670dc86565723d2b49bb9feebb58349db5f69f661c0451` | Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors) | Public domain (Natural Earth LICENSE.md: "Everything here is public domain.") | verified_source |
| `owid_energy_africa.csv` | 92,445 | `ffb05c91b17b4956779e8033b4f2d147fd84c46d64634acff1214fb19ab05eb2` | Our World in Data (Global Change Data Lab), compiling Ember and Energy Institute data | CC BY 4.0 for data produced by Our World in Data; third-party data keep the licence of their original authors (repository README) | secondary |
| `owid_energy_codebook_subset.csv` | 3,164 | `b4c2a291fc1735dc96488a42850c26e3a238bac28e68226233862ed08c3e46ab` | Our World in Data (Global Change Data Lab), compiling Ember and Energy Institute data | CC BY 4.0 for data produced by Our World in Data; third-party data keep the licence of their original authors (repository README) | secondary |
| `wdi_eg_elc_accs_zs_africa.csv` | 37,549 | `3e0750c3afa45b7038f8503f2dd5e5daef285872f6e6d053b2c3527ca6ef474e` | World Bank, World Development Indicators (copy maintained by the Datahub 'datasets' GitHub organisation) | CC-BY-4.0 (as stated in the mirror's datapackage.json) | secondary |

## Natural Earth Admin 0 - Countries 1:10m (Africa)

* Key: `ne_admin0_africa` (platform dataset in `datasets`)
* Source institution: Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors)
* Dataset title as published: Admin 0 - Countries, 1:10m (ne_10m_admin_0_countries.geojson)
* Version / commit: v5.1.2 (file identical to tag v5.1.2; repository commit ca96624a56bd078437bca8184e78163e5039ad19; VERSION file reads 5.2.0-pre)
* Publication date: 2022-05-12 (v5.1.2)
* Retrieval date: 2026-10-13
* Licence: Public domain (Natural Earth LICENSE.md: "Everything here is public domain.")
* Attribution text: Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com. (Credit is optional per the source: "No permission is needed to use Natural Earth. Crediting the authors is unnecessary.")
* Coverage: 54 African UN member states, plus Somaliland and Western Sahara as separate units as drawn by Natural Earth
* Resolution: 1:10m source; simplified, tolerance 0.005 deg, max displacement 0.007244 deg (~0.8 km)
* Quality class: `verified_source`
* Known limitations: Natural Earth shows de facto boundaries at cartographic scale and states that the authors are not responsible for accuracy; not a legal or cadastral boundary. Somaliland (NE code SOL) and Western Sahara (NE code SAH) are separate units in the source; they are kept as published with iso3 null and are not attributed to any of the 54 countries. Source files date from 2022 (release v5.1.2): later administrative reforms are not reflected.

Raw files downloaded:

| URL downloaded | Pinned URL | File last changed in commit | Bytes | SHA-256 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_0_countries.geojson | https://raw.githubusercontent.com/nvkelso/natural-earth-vector/ca96624a56bd078437bca8184e78163e5039ad19/geojson/ne_10m_admin_0_countries.geojson | `9380cca83db5` (2022-05-12) | 13,287,234 | `239eec57ac17f100a11e2536cffc56752c318b50ae765b0918ff7aab4ce8f255` |

Transformations:

1. kept features whose ISO_A3_EH is one of the 54 African UN member states, plus ADM0_A3 SOL and SAH
1. kept properties ISO_A3_EH (as iso3), ADM0_A3, NAME, NAME_LONG, NAME_EN, NAME_FR, TYPE
1. shapely 2.2 / GEOS 3.14 coverage_simplify (topology preserving, shared borders stay identical), tolerance 0.005 degrees
1. coordinates rounded to 5 decimals

Derived files:

* `ne_admin0_africa.geojson`: 868,344 bytes, SHA-256 `ad428d89866f02c90f4ff16fbacbbbe4e9bf2ead2978abb38f97c701fb3ee028`

## Natural Earth Admin 1 - States, Provinces 1:10m (Africa)

* Key: `ne_admin1_africa` (platform dataset in `datasets`)
* Source institution: Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors)
* Dataset title as published: Admin 1 - States, Provinces, 1:10m (ne_10m_admin_1_states_provinces.geojson)
* Version / commit: v5.1.2 (file identical to tag v5.1.2; repository commit ca96624a56bd078437bca8184e78163e5039ad19)
* Publication date: 2022-05-04 (v5.1.0-v5.1.2)
* Retrieval date: 2026-10-13
* Licence: Public domain (Natural Earth LICENSE.md: "Everything here is public domain.")
* Attribution text: Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com. (Credit is optional per the source: "No permission is needed to use Natural Earth. Crediting the authors is unnecessary.")
* Coverage: First-level administrative units of the 54 African UN member states (South Sudan: NE code SDS mapped to ISO SSD), plus Somaliland and Western Sahara units
* Resolution: 1:10m source; simplified, tolerance 0.005 deg, max displacement 0.007244 deg (~0.8 km)
* Quality class: `verified_source`
* Known limitations: Natural Earth shows de facto boundaries at cartographic scale and states that the authors are not responsible for accuracy; not a legal or cadastral boundary. Somaliland (NE code SOL) and Western Sahara (NE code SAH) are separate units in the source; they are kept as published with iso3 null and are not attributed to any of the 54 countries. Source files date from 2022 (release v5.1.2): later administrative reforms are not reflected. Admin 1 names and units follow Natural Earth, which may differ from current national gazetteers; for example Kenya appears as its 8 former provinces, not its 47 counties. Check against the national statistics office before operational use.

Raw files downloaded:

| URL downloaded | Pinned URL | File last changed in commit | Bytes | SHA-256 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_1_states_provinces.geojson | https://raw.githubusercontent.com/nvkelso/natural-earth-vector/ca96624a56bd078437bca8184e78163e5039ad19/geojson/ne_10m_admin_1_states_provinces.geojson | `117488dc884b` (2022-05-04) | 40,726,851 | `22d0e3ad85eb3e27f17cabf8ba2d50e554fbc27a87796ff891d958185da62fb5` |

Transformations:

1. kept features whose adm0_a3 (SDS mapped to SSD) is one of the 54 countries, plus SOL and SAH
1. kept properties adm0_a3, admin, adm1_code, iso_3166_2, name, name_fr, type_en, type; added iso3
1. coverage_simplify tolerance 0.005 degrees (same method as admin 0)
1. coordinates rounded to 5 decimals

Derived files:

* `ne_admin1_africa.geojson`: 2,857,573 bytes, SHA-256 `c87545895ce0b89c5818673fcdce11155abad6bbfa1cec2abdfbb2ec1c379881`

## Natural Earth Populated Places 1:10m (Africa)

* Key: `ne_populated_places_africa` (platform dataset in `datasets`)
* Source institution: Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors)
* Dataset title as published: Populated Places (simple), 1:10m (ne_10m_populated_places_simple.geojson)
* Version / commit: v5.1.2 (file identical to tag v5.1.2; repository commit ca96624a56bd078437bca8184e78163e5039ad19)
* Publication date: 2022-05-13 (v5.1.2)
* Retrieval date: 2026-10-13
* Licence: Public domain (Natural Earth LICENSE.md: "Everything here is public domain.")
* Attribution text: Made with Natural Earth. Free vector and raster map data @ naturalearthdata.com. (Credit is optional per the source: "No permission is needed to use Natural Earth. Crediting the authors is unnecessary.")
* Coverage: 1285 populated places in the 54 African UN member states selected for 1:10m cartography
* Resolution: Point locations at 1:10m cartographic scale (coordinates as published)
* Quality class: `verified_source`
* Known limitations: pop_max, pop_min and pop_other are population estimates as published by Natural Earth, not census counts, and no reference year is given per feature. Only places selected for small-scale cartography are included: most villages relevant to mini grids are absent, so this is not a settlement inventory. Places in Somaliland and Western Sahara (NE codes SOL, SAH) are excluded.

Raw files downloaded:

| URL downloaded | Pinned URL | File last changed in commit | Bytes | SHA-256 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_populated_places_simple.geojson | https://raw.githubusercontent.com/nvkelso/natural-earth-vector/ca96624a56bd078437bca8184e78163e5039ad19/geojson/ne_10m_populated_places_simple.geojson | `789c99040878` (2022-05-13) | 4,932,147 | `fd3fa867a320cbd5c5b6bb5bc550afeec2939fb2cef688e508007282a55ac42f` |

Transformations:

1. kept features whose adm0_a3 (SDS mapped to SSD) is one of the 54 countries
1. kept properties name, nameascii, namealt, featurecla, adm0name, adm0_a3, adm1name, adm0cap, worldcity, megacity, pop_max, pop_min, pop_other, latitude, longitude, ne_id; added iso3
1. geometry copied unchanged

Derived files:

* `ne_populated_places_africa.geojson`: 522,630 bytes, SHA-256 `85162260e76a0de1e4670dc86565723d2b49bb9feebb58349db5f69f661c0451`

## Our World in Data energy data (Africa, electricity indicators)

* Key: `owid_energy` (indicators in `country_profiles`)
* Source institution: Our World in Data (Global Change Data Lab), compiling Ember and Energy Institute data
* Dataset title as published: Data on Energy by Our World in Data, legacy release (owid-energy-data.csv, owid-energy-codebook.csv)
* Version / commit: repository commit f8de88a4f6f9cab44f1cf606047cbd6c4414042c; owid-energy-data.csv last changed in commit e7897aed55b514b8d16e0a3d8f1518789ac3de31 (2026-04-27)
* Publication date: 2026-04-27 (README changelog)
* Retrieval date: 2026-10-13
* Licence: CC BY 4.0 for data produced by Our World in Data; third-party data keep the licence of their original authors (repository README)
* Licence text quoted from the repository README: "All visualizations, data, and code produced by Our World in Data are completely open access under the Creative Commons BY license. You have the permission to use, distribute, and reproduce these in any medium, provided the source and authors are credited. The data produced by third parties and made available by Our World in Data is subject to the license terms from the original third-party authors. We will always indicate the original source of the data in our database, and you should always check the license of any such third-party data before use."
* Attribution text: Our World in Data, Data on Energy (github.com/owid/energy-data, commit f8de88a), based on Ember - Yearly Electricity Data (2026), Energy Institute - Statistical Review of World Energy (2025) and OWID population (2024). The README asks users to cite both Our World in Data and the underlying data source(s).
* Coverage: 54 African UN member states, national level
* Resolution: Country, annual
* Quality class: `secondary`
* Known limitations: The repository README states this legacy release 'is no longer updated' (a new methodology release exists on catalog.ourworldindata.org, which was not reachable from the build environment). Values are compiled by OWID from Ember and the Energy Institute; the licences of those third-party sources were not verified here. Latest available year differs by country and indicator.

Raw files downloaded:

| URL downloaded | Pinned URL | File last changed in commit | Bytes | SHA-256 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv | https://raw.githubusercontent.com/owid/energy-data/f8de88a4f6f9cab44f1cf606047cbd6c4414042c/owid-energy-data.csv | `e7897aed55b5` (2026-04-27) | 9,229,369 | `266f2e2baad7975351bc9bb4aa061d22b1da9fe4c47d51d2ac6071e01e171f76` |
| https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-codebook.csv | https://raw.githubusercontent.com/owid/energy-data/f8de88a4f6f9cab44f1cf606047cbd6c4414042c/owid-energy-codebook.csv | `7ae9b4864980` (2026-01-27) | 45,793 | `3cc9b7db0d921496e2988568ce3aee5ed41f50431dd234a0663b5f0a4b2e32bb` |
| https://raw.githubusercontent.com/owid/energy-data/master/README.md | https://raw.githubusercontent.com/owid/energy-data/f8de88a4f6f9cab44f1cf606047cbd6c4414042c/README.md | `e380ef0c3887` (2026-10-01) | 16,149 | `d014045a2eeb06343f9f107af80c2e86959df320525faf16cfb9155f9f3007d0` |

Transformations:

1. kept rows whose iso_code is one of the 54 countries and that have at least one value in the kept columns
1. kept columns country, year, iso_code, electricity_generation, per_capita_electricity, renewables_share_elec, solar_share_elec, fossil_share_elec, electricity_demand, electricity_demand_per_capita
1. cell values copied verbatim (no rounding, no gap filling)
1. codebook rows for the kept columns copied verbatim

Derived files:

* `owid_energy_africa.csv`: 92,445 bytes, SHA-256 `ffb05c91b17b4956779e8033b4f2d147fd84c46d64634acff1214fb19ab05eb2`
* `owid_energy_codebook_subset.csv`: 3,164 bytes, SHA-256 `b4c2a291fc1735dc96488a42850c26e3a238bac28e68226233862ed08c3e46ab`

## Access to electricity (% of population), WDI EG.ELC.ACCS.ZS (Africa)

* Key: `wdi_eg_elc_accs_zs` (indicators in `country_profiles`)
* Source institution: World Bank, World Development Indicators (copy maintained by the Datahub 'datasets' GitHub organisation)
* Dataset title as published: Access to electricity (% of population) (indicators/eg.elc.accs.zs/data.csv)
* Version / commit: datasets/world-development-indicators commit 4ebec5a2273f531ba238a34dbe440394dc5a6c4b (automated update of 2026-07-01)
* Publication date: 2026-07-01 (mirror update)
* Retrieval date: 2026-10-13
* Licence: CC-BY-4.0 (as stated in the mirror's datapackage.json)
* Attribution text: World Bank, World Development Indicators: Access to electricity (% of population), EG.ELC.ACCS.ZS. Licence CC BY 4.0. Retrieved via github.com/datasets/world-development-indicators (commit 4ebec5a).
* Provenance stated by the mirror: The mirror's scripts/get.py downloads https://api.worldbank.org/v2/en/indicator/<code>?downloadformat=csv and the indicator metadata from https://api.worldbank.org/v2/indicator/<code>; a monthly GitHub Action (.github/workflows/update.yml) runs scripts/extractFeaturedWorldBankDatasets.py and commits changes.
* Coverage: 54 African UN member states, national level
* Resolution: Country, annual
* Quality class: `secondary`
* Known limitations: Secondary copy: the World Bank API (api.worldbank.org) was not reachable from the build environment, so values were not checked against the publisher. The World Bank's own source notes and methodology fields were not retrieved; the mirror's description reads: 'Electrification data are collected from industry, national surveys and international sources.' Values carry float precision artefacts as published (for example 99.1536560058594).

Raw files downloaded:

| URL downloaded | Pinned URL | File last changed in commit | Bytes | SHA-256 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/datasets/world-development-indicators/4ebec5a2273f531ba238a34dbe440394dc5a6c4b/indicators/eg.elc.accs.zs/data.csv | same | `4ebec5a2273f` (2026-07-01) | 238,876 | `6c3c4dcbbe6d2a0fada0d38acd24fad17e45288b36a7f78419eb73eb7124568a` |
| https://raw.githubusercontent.com/datasets/world-development-indicators/4ebec5a2273f531ba238a34dbe440394dc5a6c4b/indicators/eg.elc.accs.zs/datapackage.json | same | not recorded | 1,468 | `ff3c2176bd46f3d9c8396f8589ef57efd366dab2897ea15bffed1d7791799103` |

Transformations:

1. kept rows whose Country Code is one of the 54 countries
1. values copied verbatim

Derived files:

* `wdi_eg_elc_accs_zs_africa.csv`: 37,549 bytes, SHA-256 `3e0750c3afa45b7038f8503f2dd5e5daef285872f6e6d053b2c3527ca6ef474e`

## Not ingested

* World Bank API, Our World in Data catalogue, HDX, geoBoundaries: not reachable from the build environment (proxy 403). No value from them is used. The WDI access-to-electricity series comes from a mirror (see above) and is marked `secondary`.
* The new OWID energy release (catalog.ourworldindata.org) was not reachable; the legacy GitHub release is used and its README says it is no longer updated.

## How to refresh

1. Download the raw files from the pinned URLs (or newer commits) into a scratch folder with the layout `ne/`, `owid/`, `wdi/`.
2. Verify each file against its commit (`git hash-object`) and record the new commit in `scripts/derive_public_data.py` notes and the manifest.
3. Run `python -I scripts/derive_public_data.py RAW_DIR app/public_data`, update `manifest.json` (hashes, dates, limitations) and regenerate this file (`python -I scripts/public_data_manifest_md.py app/public_data/manifest.json ../docs/public-data-manifest.md`).
4. Run `python -m app.ingest_public`, then `python -m pytest tests/api/test_public_data.py` with `A360_PUBLIC_RAW_DIR=RAW_DIR` so profile values are compared with the raw CSVs.
