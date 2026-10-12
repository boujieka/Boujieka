# ACCESS MAP: geospatial data specification

## 1. Dataset record (mandatory fields)

Every layer, whether uploaded by a tenant or provided by the platform, carries the fields below. The API rejects an upload (HTTP 422) if any field is missing.

| Field | Meaning |
|---|---|
| title | Dataset title as published |
| layer_type | settlements, grid, substations, health, schools, markets, anchors, minigrids, constraints or other |
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

Shapefile, GeoPackage and raster formats (for example GeoTIFF for solar resource or night lights) are planned with the PostGIS, GeoPandas and Rasterio ingestion in Phase 2.

## 3. Rules

* An inferred electrification status is never shown as a verified connection. Layers derived from night lights or models must use quality `secondary` and say so in `limitations`.
* Where data is missing, the interface shows "Data unavailable". Authorised users may enter assumptions (quality `user_assumption`).
* Platform datasets (`org_id` NULL) are read-only for tenants. Tenant datasets are visible only to their organisation (row-level security).
* No third-party dataset is bundled with the MVP. Each candidate layer listed in the brief needs a licence check before ingestion:
  * population and settlements;
  * transmission and distribution networks;
  * electrification status;
  * night lights;
  * solar and wind resources;
  * facilities;
  * protected areas.
* Demo datasets are synthetic, flagged `synthetic_demo`, and placed at sea in the Gulf of Guinea on purpose, so that they cannot be mistaken for real settlements.

## 4. Countries and boundaries

The country selector lists the 54 UN member states in Africa (ISO 3166-1 alpha-3). Administrative regions, districts and settlements require a boundary dataset uploaded by the user, or licensed by the platform. Until then the interface shows "Data unavailable".
