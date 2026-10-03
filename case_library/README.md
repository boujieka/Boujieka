# BANKABLE HYDRO: Case Study Library

The library has three parts:

1. **Field-by-field case files** in `research/case_studies/`. Fields A–AD cover:
   - size, capacity, generation and hydrology;
   - CAPEX, construction, overruns, financing, debt, equity, concessional finance, government contribution and guarantees;
   - PPA, offtaker and utility condition;
   - transmission, grid, demand, tariff and regulation;
   - PPP/IPP structure and FX, political, E&S and fiscal risk;
   - contingent liabilities, delays and restructuring;
   - lessons for financial close.

   Where no verified public source was found, the field reads **PUBLIC DATA NOT FOUND**.
2. **Benchmark table** in the model, sheet `31_CASE_STUDY`. It holds 15 cases plus the fictional reference project, with nominal, unadjusted USD/kW.
3. **One fictional reference project**, Lumora Falls (Navaria). It is the worked example throughout the model, book and course.

| File | Projects | Sources |
|---|---|---|
| `research/case_studies/africa_part1.md` | GERD; Inga I/II, Inga 3 and Grand Inga; Cahora Bassa; Kariba (incl. KDRP); Akosombo; Bui; Merowe; Gilgel Gibe I/II/III; Kafue Gorge Lower | S1–S61 |
| `research/case_studies/africa_part2.md` | Nachtigal; Lesotho Highlands (Muela, Phase II); Rusumo Falls; Ruzizi I/II/III; Mpatamanga; Julius Nyerere; Isimba; Karuma; Kiira/Nalubaale; Nyagak; Bujagali; Batoka Gorge | 62 sources |
| `research/case_studies/international_benchmarks.md` | Three Gorges; Itaipu; Belo Monte; Nam Theun 2; Xayaburi; Upper Trishuli-1; Reventazón | 23 sources |

**Not covered in v1.0:** Theun-Hinboun, Tala, Punatsangchhu, Teesta III and Chaglla. The research could not verify enough data for them.

## Data-quality flags (read before citing)

- **"(snippet)" / "search-result only".** The fact came from search-result text because the page itself could not be fetched. Re-verify before external publication.
- **Ranges.** Where sources disagree, the case file shows both figures with their sources. Examples:
  - GERD cost: USD 4–5 bn.
  - Ruzizi III capacity: 147 vs 206 MW.
  - Bujagali cost: USD 582 m, 799 m and 862 m at different dates.
- **Possible source errors** are flagged in `africa_part2.md`:
  - a World Bank blog's "€0.6/kWh", almost certainly €0.06;
  - a "16 km" Rusumo line, where the World Bank says 160 km;
  - Karuma's "original cost", which is likely the loan amount.

## Teaching map: case → lesson → model stress

| Theme | Case evidence | Model stress / sheet | Book chapter |
|---|---|---|---|
| Overrun and delay reference class | Bui +27%; Rusumo civil works +47%; Karuma ~5 yrs; KGL ~3 yrs | `st_capex`, `st_delay` | 4 |
| Utility arrears become sovereign debt | KGL / ZESCO (2024 DSA); Bui / ECG USD 612 m | `st_offtaker`, `12_UTILITY` | 1, 8 |
| Deemed energy and transmission lag | Uganda UETCL deemed energy; Rusumo parallel transmission | `st_trans`, `08`, `09` | 6 |
| Guarantees carry sovereign indemnities | Bujagali IDA PRG; Nachtigal IBRD guarantees | `23`, `24` | 13 |
| Tenor and tariff | Bujagali refinancing; Nachtigal 21-yr local-currency tranche | `str_nm`, `lc_share` | 10, 11 |
| Drought | Kariba 2024 allocation cut | `st_drought` | 3 |
| Building ahead of demand | Julius Nyerere / Tanzania surplus over peak | `st_demand`, `10` | 7 |
| Procurement governance | Gibe III; Bujagali first attempt; Batoka re-tender | `13`, Gate 6 | 9 |
| Portfolio fiscal risk | Lao PDR (Nam Theun 2 vs later EDL take-or-pay wave) | `26` (single project); portfolio sheet on roadmap | 14, 17 |
| Off-balance-sheet form vs substance | Reventazón trust and lease | `17A` | 2, 12 |

All lessons in the case files are labelled **Analyst inference**.
