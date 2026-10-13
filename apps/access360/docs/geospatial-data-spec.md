# ACCESS MAP: geospatial data specification

## 1. Dataset record (mandatory fields)

Every layer, whether uploaded by a tenant or provided by the platform, carries the fields below. The API rejects an upload (HTTP 422) if any field is missing.

| Field | Meaning |
|---|---|
| title | Dataset title as published |
| layer_type | boundaries, settlements, grid, substations, health, schools, markets, anchors, minigrids, constraints or other |
| source_institution | The publisher |
| publication_date | As published (free text, at least the year) |
| geographic_coverage | Area covered |
| resolution | Spatial resolution or scale |
| licence | Licence under which the data may be used |
| retrieval_date | Date the copy was obtained |
| quality | verified_source, secondary, user_assumption or synthetic_demo |
| limitations | Known limitations, in words |

## 2. Accepted formats

| Format | Rules |
|---|---|
| GeoJSON | A FeatureCollection with up to 50,000 features. Geometry types: Point, MultiPoint, LineString, MultiLineString, Polygon or MultiPolygon. Properties must be an object |
| CSV | UTF-8, with latitude and longitude columns (`lat`/`latitude`, `lon`/`lng`/`longitude`) in range. Other columns become properties |
| Size | Limited by `A360_MAX_UPLOAD_MB` (default 20) |

Every dataset is also loaded into the PostGIS table `dataset_features` (geometries made valid, EPSG:4326, GIST index) by a database trigger. The API offers a project context (country, admin 1 region, nearest Natural Earth places, the organisation's layers within a radius) and radius screening of any visible dataset. Shapefile, GeoPackage and raster formats (for example GeoTIFF for solar resource or night lights) are not yet supported.

## 3. Rules

* An inferred electrification status is never shown as a verified connection. Layers derived from night lights or models must use quality `secondary` and say so in `limitations`.
* Where data is missing, the interface shows "Data unavailable". Authorised users may enter assumptions (quality `user_assumption`).
* Platform datasets (`org_id` NULL) are read-only for tenants. Tenant datasets are visible only to their organisation (row-level security).
* Only the public reference data listed in section 5 is bundled. Every other candidate layer needs a licence check before ingestion:
  * population and settlements (beyond the Natural Earth cartographic selection);
  * transmission and distribution networks;
  * electrification status at sub-national level;
  * night lights;
  * solar and wind resources;
  * facilities;
  * protected areas.
* Demo datasets are synthetic, flagged `synthetic_demo`, and placed at sea in the Gulf of Guinea on purpose, so that they cannot be mistaken for real settlements.

## 4. Countries and boundaries

The country selector lists the 54 UN member states in Africa (ISO 3166-1 alpha-3). Choosing a country fits the map to its Natural Earth admin 0 boundary, draws its admin 1 regions and the Natural Earth populated places, and opens the country profile.

* Admin 1 regions: from the bundled Natural Earth layer (section 5). Natural Earth admin 1 units can lag national reforms (for example Kenya is drawn as 8 former provinces, not 47 counties).
* Districts (admin 2) and settlements below that: "Data unavailable" until a tenant uploads a dataset. The Natural Earth populated places are a cartographic selection (36 places in Kenya, 1,285 in Africa), not a settlement inventory, and the interface says so.
* Somaliland and Western Sahara are separate units in Natural Earth. They are kept as published (iso3 null) in the platform layers and are not attributed to any of the 54 countries.

## 5. Bundled public reference data

Loaded by `python -m app.ingest_public` (owner role, idempotent, SHA-256 of each file checked against `backend/app/public_data/manifest.json`). Geographic layers become platform datasets (`datasets.org_id` NULL, `is_demo` false, read only for tenants through RLS). Indicators go to `country_profiles`; full source records to `reference_sources`. Both tables are SELECT only for the app role. Full hashes, URLs and transformations: `docs/public-data-manifest.md`.

| Key | Source institution | Dataset as published | Version or commit | Publication date | Licence (as stated) | Coverage and resolution | Quality |
|---|---|---|---|---|---|---|---|
| `ne_admin0_africa` | Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors) | Admin 0 - Countries, 1:10m (ne_10m_admin_0_countries.geojson) | v5.1.2 (file identical to tag v5.1.2; repository commit ca96624a56bd078437bca8184e78163e5039ad19; VERSION file reads 5.2.0-pre) | 2022-05-12 (v5.1.2) | Public domain (Natural Earth LICENSE.md: "Everything here is public domain.") | 54 African UN member states, plus Somaliland and Western Sahara as separate units as drawn by Natural Earth; 1:10m source; simplified, tolerance 0.005 deg, max displacement 0.007244 deg (~0.8 km) | verified_source |
| `ne_admin1_africa` | Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors) | Admin 1 - States, Provinces, 1:10m (ne_10m_admin_1_states_provinces.geojson) | v5.1.2 (file identical to tag v5.1.2; repository commit ca96624a56bd078437bca8184e78163e5039ad19) | 2022-05-04 (v5.1.0-v5.1.2) | Public domain (Natural Earth LICENSE.md: "Everything here is public domain.") | First-level administrative units of the 54 African UN member states (South Sudan: NE code SDS mapped to ISO SSD), plus Somaliland and Western Sahara units; 1:10m source; simplified, tolerance 0.005 deg, max displacement 0.007244 deg (~0.8 km) | verified_source |
| `ne_populated_places_africa` | Natural Earth (Tom Patterson, Nathaniel Vaughn Kelso and contributors) | Populated Places (simple), 1:10m (ne_10m_populated_places_simple.geojson) | v5.1.2 (file identical to tag v5.1.2; repository commit ca96624a56bd078437bca8184e78163e5039ad19) | 2022-05-13 (v5.1.2) | Public domain (Natural Earth LICENSE.md: "Everything here is public domain.") | 1285 populated places in the 54 African UN member states selected for 1:10m cartography; Point locations at 1:10m cartographic scale (coordinates as published) | verified_source |
| `owid_energy` | Our World in Data (Global Change Data Lab), compiling Ember and Energy Institute data | Data on Energy by Our World in Data, legacy release (owid-energy-data.csv, owid-energy-codebook.csv) | repository commit f8de88a4f6f9cab44f1cf606047cbd6c4414042c; owid-energy-data.csv last changed in commit e7897aed55b514b8d16e0a3d8f1518789ac3de31 (2026-04-27) | 2026-04-27 (README changelog) | CC BY 4.0 for data produced by Our World in Data; third-party data keep the licence of their original authors (repository README) | 54 African UN member states, national level; Country, annual | secondary |
| `wdi_eg_elc_accs_zs` | World Bank, World Development Indicators (copy maintained by the Datahub 'datasets' GitHub organisation) | Access to electricity (% of population) (indicators/eg.elc.accs.zs/data.csv) | datasets/world-development-indicators commit 4ebec5a2273f531ba238a34dbe440394dc5a6c4b (automated update of 2026-07-01) | 2026-07-01 (mirror update) | CC-BY-4.0 (as stated in the mirror's datapackage.json) | 54 African UN member states, national level; Country, annual | secondary |

Retrieval date for all files: 2026-10-13. All were downloaded from `raw.githubusercontent.com` at the commits shown.

Profile indicators (latest year with a published value, per indicator and country; the year is always shown; a missing value stays null and is displayed as "Data unavailable"):

| Indicator key | Column in source | Unit (from the source codebook or title) |
|---|---|---|
| access_to_electricity | WDI `EG.ELC.ACCS.ZS`, `Value` | % of population |
| electricity_generation | OWID `electricity_generation` | terawatt-hours (TWh) |
| per_capita_electricity | OWID `per_capita_electricity` | kilowatt-hours (kWh) |
| electricity_demand | OWID `electricity_demand` | terawatt-hours (TWh) |
| electricity_demand_per_capita | OWID `electricity_demand_per_capita` | kilowatt-hours (kWh) |
| renewables_share_elec | OWID `renewables_share_elec` | % |
| solar_share_elec | OWID `solar_share_elec` | % |
| fossil_share_elec | OWID `fossil_share_elec` | % |

Required attribution:

* Natural Earth: optional per the source ("Crediting the authors is unnecessary"); the platform shows "Made with Natural Earth."
* Our World in Data: cite both Our World in Data and the underlying sources (Ember, Energy Institute, OWID population), as the repository README asks. Third-party data inside the OWID file keep their own licences, which were not verified here.
* World Bank WDI: CC BY 4.0 as stated by the mirror; attribution "World Bank, World Development Indicators: Access to electricity (% of population), EG.ELC.ACCS.ZS". The copy is a mirror (`datasets/world-development-indicators`), so it is classed `secondary`.

API: `GET /api/countries` (adds `has_profile` and `bbox`), `GET /api/countries/{iso3}/profile`, `/boundary`, `/admin1`, `/places` (login required; features filtered by `iso3` in PostgreSQL).
