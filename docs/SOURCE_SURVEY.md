# Official sources outside WAEMU: survey of 2026-10-04

Three read-only surveys checked which official sources publish government-securities auction results and whether they are reachable from the platform. Each survey also recorded:

- the format and the history available;
- the fields printed;
- whether the documents are text or scanned;
- the exact terms of use.

The detailed results, with URLs, quoted terms and notes per source, are in `docs/source_survey/{cemac,west_north,east_south}.json`. Only URLs and facts that were actually fetched are recorded.

## Terms of use: the deciding constraint

The platform is commercial (paid report and data licence), so the reuse terms decide what may be published.

| Category | Sources |
|---|---|
| Open licence | **Rwanda (BNR): CC BY 4.0**, "personal, commercial, academic, or research purposes" |
| Copyright notice / disclaimer only, no reuse clause found | Kenya (CBK), Tanzania (BoT), South Africa (National Treasury; *not* SARB), Nigeria (CBN: none found; DMO: copyright), The Gambia (CBG), Ghana (BoG: disclaimer + "All rights reserved"), Uganda (BoU: download and copy "for User use") |
| Non-commercial / no reproduction without permission | **BEAC, BVMAC** ("usage personnel, à des fins non commerciales… sans… droit de reproduire… à des fins de revente ou de rediffusion"), Zambia (BoZ), Morocco (Bank Al-Maghrib), Tunisia (BCT), Sierra Leone (BSL), DR Congo (BCC), NSE Kenya, NGX |
| **UMOA-Titres (already published)** | https://www.umoatitres.org/mentions-legales/: « Toute reproduction, représentation, modification, publication, adaptation de tout ou partie des éléments du site … est interdite, sauf autorisation écrite préalable, de l'UMOA-Titres. Après l'obtention de l'accord de l'UT, les utilisateurs … peuvent disposer librement des informations … : elles doivent apparaître avec exactitude et l'UT doit être mentionnée comme source ; toute modification des informations … doit être mentionnée explicitement. » |

A "copyright only" notice does not grant reuse rights. Whether published figures are protected at all varies by jurisdiction. **This is not legal advice.**

## Technical feasibility (priority sources)

| Region | Usable now (text or structured) | Needs OCR | Not usable / unreachable |
|---|---|---|---|
| CEMAC | BVMAC daily price list (BOC): text, ISIN, 2019→2026; Congo debt bulletin | BEAC auction results (992 notices 2019→Sep 2026, all scanned); BEAC weekly reports | BEAC yield curves (charts only since 2017); minfi.gov.cm, dette.ga, caa.cm unreachable |
| East / Southern | KEN (text PDFs, 2007/2014→2026); TZA (JSON, 2012→2026); RWA (XLSX, 2008/2012→2026); ZAF NT (XLS, FY2010→2026); ZMB (JSON:API); MOZ, NAM, BWA, MUS, SYC, MWI, ETH, BDI | Uganda's 2026 PDFs (2017–2024 are text) | JSE, LuSE, BoM, Somalia blocked or JavaScript-only |
| West / North | NGA (CBN JSON API 2002→2026; DMO PDFs); GMB (XLSX 2017→2026); MAR (CSV 2003→2026); GHA (rates table + PDFs); EGY (MoF yields only); SLE, BDI | none | CBE blocked; TUN current data JavaScript-only; LBR stale; GIN, CPV, MRT, LBY not found |
