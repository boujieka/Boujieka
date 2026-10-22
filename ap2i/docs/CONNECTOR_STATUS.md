# AP²I — Connector status report

Generated 2026-10-22T12:39Z from the local AP²I database with `python -m app.cli connector-report`. Source details and blockers: [DATA_SOURCES.md](DATA_SOURCES.md).

| Connector | Tier | Status | Enabled | Records stored | Last success | Evidence / blocker |
|---|---|---|---|---|---|---|
| `afd_iati` | 1 | operational | True | 306 | 2026-10-22 | Run #4 (2026-10-22 12:17 UTC): 306 real records retrieved, 306 imported; 306 records persisted in total. |
| `afd_opendata` | 1 | blocked | False | 0 | — | opendata.afd.fr reset the connection from the AP²I environment on 2026-10-22 and afd.fr was in maintenance (HTTP 503). AFD project data is ingested through AFD's own IATI publication (connector afd_iati). |
| `afdb_iati` | 1 | operational | True | 105 | 2026-10-22 | Run #3 (2026-10-22 12:17 UTC): 105 real records retrieved, 105 imported; 105 records persisted in total. |
| `afdb_portal` | 1 | blocked | False | 0 | — | projectsportal.afdb.org was unreachable from the AP²I environment on 2026-10-22 (proxy CONNECT 502) and no documented public API was identified. AfDB project data is ingested through AfDB's own IATI publication (connecto |
| `iati_generic` | 1 | not_tested | False | 0 | — |  |
| `manual_upload` | 1 | manual | False | 0 | — |  |
| `worldbank_iati` | 1 | operational | True | 46 | 2026-10-22 | Run #2 (2026-10-22 12:17 UTC): 46 real records retrieved, 46 imported; 46 records persisted in total. |
| `worldbank_projects` | 1 | operational | True | 159 | 2026-10-22 | Run #1 (2026-10-22 12:16 UTC): 159 real records retrieved, 159 imported; 159 records persisted in total. |
| `eib_iati` | 2 | operational | True | 10 | 2026-10-22 | Run #5 (2026-10-22 12:27 UTC): 10 real records retrieved, 10 imported; 10 records persisted in total. |
| `eu_intpa_iati` | 2 | operational | True | 182 | 2026-10-22 | Run #6 (2026-10-22 12:27 UTC): 182 real records retrieved, 182 imported; 182 records persisted in total. |
| `gcf` | 2 | not_implemented | False | 0 | — | GCF open data not yet assessed; manual import workflow. |
| `gef` | 2 | not_implemented | False | 0 | — | GEF project database not yet assessed; GEF-funded UNDP activities appear in undp_iati. |
| `isdb` | 2 | not_implemented | False | 0 | — | No IsDB IATI publication observed for Cameroon; official project pages need a source-specific connector. |
| `jica` | 2 | not_implemented | False | 0 | — | No JICA IATI publication observed for Cameroon; manual import workflow. |
| `kfw` | 2 | not_implemented | False | 0 | — | KfW is not a separate IATI reporting organisation for Cameroon (German flows appear under DE-1/BMZ). |
| `adfd` | 3 | not_implemented | False | 0 | — | No machine-readable source identified; manual import workflow. |
| `badea` | 3 | not_implemented | False | 0 | — | No machine-readable source identified; manual import workflow. |
| `bmz_iati` | 3 | not_tested | False | 0 | — |  |
| `fao_iati` | 3 | not_tested | False | 0 | — |  |
| `ifad_iati` | 3 | operational | True | 12 | 2026-10-22 | Run #7 (2026-10-22 12:27 UTC): 12 real records retrieved, 12 imported; 12 records persisted in total. |
| `kfaed` | 3 | not_implemented | False | 0 | — | No machine-readable source identified; manual import workflow. |
| `sfd` | 3 | not_implemented | False | 0 | — | No machine-readable source identified; manual import workflow. |
| `undp_iati` | 3 | not_tested | False | 0 | — |  |
| `unicef_iati` | 3 | not_tested | False | 0 | — |  |
| `unido_iati` | 3 | not_tested | False | 0 | — |  |
