# 21 Review of the second client extraction of the Off-Grid Solar Market Trends Report 2024

Date: 4 October 2026. Input: the author's knowledge pack, stored as `volumes/02-solar-home-systems/sources/MTR2024_client_extraction_2026-10-04.txt`.

## 1. Status of the evidence

The pack is a client extraction of the report: a summary prepared by the author from the PDF. It is not the report itself.

* It gives page ranges by chapter (for example, Chapter 2 on pp. 29 to 49), but no page for any individual figure.
* The project still does not hold the PDF, and this environment cannot open esmap.org.

The E1 claims therefore stay **PENDING PRIMARY DOCUMENT**. The pack raises confidence in them: a second extraction made independently of the search snippets agrees with the first on every figure the book uses. It does not verify them.

## 2. Agreement with the register

| Register | First extraction (3 Oct) | Second extraction (4 Oct) | Result |
|---|---|---|---|
| E1-14 Average collection rate | About 62%, 2021 to 2023 | "Remained around 62% from 2021 to 2023" | Agrees. The book now says the rate stayed at about 62% from 2021 to 2023, which fits both the extractions and the earlier snippets ("62% in 2023, in line with 2021") |
| E1-15 Quartiles | 75 to 80%; below 50% | Same | Agrees |
| E1-16 Ratio band | Half of companies at 30 to 50% (18% in 2021) | Same | Agrees: the ratio concerns companies, not customers |
| E1-07, E1-08 Affordability | 5% and 10%; 22% and 27% | Same | Agrees (see the arithmetic in section 3) |
| E1-10 Sub-Saharan Africa | 16% and 46% | 16% and "an additional" 46% | Agrees; reads 46% as incremental, still to check |
| E1-12 Cost to serve | Up to 57%; USD 127 and 199 | Same | Agrees |
| E1-13 Cost of capital | 2 to 3 points, about 5% on price | Same | Agrees |
| E1-17 Investment | 773; 1,200 (746 and 425) | Same, plus the series 2017 to 2023 | Agrees |
| E1-19 Local currency | More than one third in 2023 | Same | Agrees |
| E1-23 RBF | 733 committed; about 350 disbursed | Same | Agrees |
| E1-24 Universal access | About USD 21bn; 398m people; 41% "of households" | About USD 21bn; 398m people; 41% of about 969m **people** | Register wording corrected from households to people |
| E1-25 Current trajectory | 216m (about 55%); USD 9bn | 216m; USD 9bn | Share corrected to about 54% (216 ÷ 398 = 54.3%) |
| E1-18, E1-21, E1-22 | 75% debt; more than 60%; about 14% | Not in the pack | Unchanged, still pending |

## 3. Arithmetic checks on the pack

| Item | Pack | Check | Finding |
|---|---|---|---|
| Tier 1 global | "51% are either affordable or affordable at a stretch; 49% are unaffordable" | 22% + 27% = 49% | **Slip in the pack.** Its own figures give 49% affordable or at a stretch and 51% not affordable, which is what the register holds |
| Universal access components | 6.4 + 4.3 + 1.5 + 9.2 = 21.3 | Sum is 21.4 | Rounding difference; recorded in E1-28 and in the book |
| Affordability gap population | 240m, "about 59%" of 398m | 60.3% | Minor rounding; recorded |
| Debt share of commercial need | About 60% | 6.4 ÷ 10.7 = 59.8% | Consistent |
| Public share | About half (first extraction) | (1.5 + 9.2) ÷ 21.3 = 50.2% | Consistent across the two extractions |
| Remote premium | 57% | 199 ÷ 127 = 1.567 | Consistent |
| Investment | 1.2bn; 773m; about 6% a year | 746 + 425 = 1,171; 316 + 457 = 773; (425 ÷ 307) to the power 1/6 = 5.6% | Consistent |
| Turnover | +32% (2022); about 3% lower (2023); about 15% above 2019 | 3.9 ÷ 2.9 = +34% (2021 "approximately"); (2.6%); +15.2% | Consistent within rounding |
| Remote and conflict | 82%; 31% (about 211m); three quarters (about 158m) | 562 ÷ 685 = 82%; 211 ÷ 685 = 31%; 158 ÷ 211 = 75% | Consistent |
| Total addressable investment | About USD 97bn | 21 + 74 + 2.4 = 97.4 | Consistent |
| World Bank lending, FY2024 | USD 660m and USD 626m in two sections | Internal conflict, flagged by the pack itself | E1-30, CONFLICTING SOURCES, not used |

Caution for the reader: the Sub-Saharan Africa affordability total (16% + 46% = 62%) and the average collection rate (62%) are different measures that happen to be equal. Quoting either one needs its label.

## 4. Changes made

**Register** (`tools/source_register_data.py`; 04 rebuilt; Source_Register sheet in both workbooks rebuilt):
* five new claims, taking the register from 64 to 69: E1-26 (one customer in four facing payment difficulties), E1-27 (method assumptions: 20% deposit, two years, 40% a year), E1-28 (funding components), E1-29 (local currency debt about 20%, 2017 to 2023), E1-30 (World Bank 660 or 626, CONFLICTING SOURCES);
* corrections to E1-08, E1-10, E1-14, E1-16, E1-24 and E1-25, and book references updated;
* statuses: 8 VERIFIED, 5 VERIFIED (HISTORICAL), 44 PENDING PRIMARY DOCUMENT, 4 CONFLICTING SOURCES, 8 NOT USED.

**Book** (every addition is worded "is reported to" and cites Annex G, E1, to be checked):
* Ch 1.6 and 7.4: the 62% wording; Ch 7.4 adds one customer in four in difficulty.
* Ch 2.3: the method's assumptions and the Sub-Saharan Africa shares, with the point that the results depend on the contract assumed.
* Ch 5.6: the remote cost to serve premium.
* Ch 11.3: the local currency share.
* Ch 13.1: RBF committed against disbursed.
* Ch 13.7: new subsection "The gap at sector level", giving the funding components and the rounding difference.
* Annex G, E1: the row is rewritten.

**Model:** no calculation change. Only the lookup ranges in Market_Benchmark and Calibration grow to cover the longer register. Recalculated in LibreOffice: 0 errors in 101,589 formulas, master check OK, readiness 2 of 23 and 4 of 23 with STOP, unchanged. Calibration still uses VERIFIED claims only, so no E1 figure feeds a calculation.

## 5. Proposals from the pack not implemented

The pack recommends a customer segmentation (commercially viable, marginal, affordability gap, subsidy supported), C&I and productive use segments, impact linked finance and impact metrics. These are model design changes, not evidence. They are listed for the product plan (13) and are not made without the author's decision. Most of the pack's minimum list (collection rate, RAR30, write offs, FX, RBF, receivables facility, DSCR, minimum cash) already exists in MODEL 2.

## 6. What would close E1

Upload the PDF, or allow esmap.org in the environment's network policy. Each figure can then be checked on its page, and E1 claims moved to VERIFIED with page numbers.

## 7. Primary document search, 4 October 2026 (second pass)

* **Network:** esmap.org, openknowledge.worldbank.org, documents1.worldbank.org, gogla.org, Companies House and The Gazette were each tried again, both directly and through the web fetch tool. All were refused by the environment's egress policy.
* **Author's Google Drive:** searched for the missing documents. *Beyond Connections: Energy Access Redefined* (ESMAP, Technical Report 008/15, July 2015, 244 pages) was found and read. E3-01 to E3-03 are now VERIFIED:
  * PDF page 19 (report page 5): the seven attributes and the lowest tier rule;
  * PDF page 20 (report page 6), Table ES.1: the capacity and duration thresholds and the affordability test.
* **Correction found by reading the document:** the workbook described the capacity minimums as "3 W and 12 Wh/day". Table ES.1 gives "power capacity ratings (in W or daily Wh)", so the workbook now reads "or". Ch 2.6 now also states that the framework's affordability test (365 kWh a year below 5% of income) is a different measure from the PAYGo payment burden.
* **Not found in the Drive:** MTR 2024, GOGLA "After the Dip", M-KOPA Holdings group accounts and Gazette notice 4891954. The Drive holds the 2018 Market Trends Report, which is too old for the pending claims.
* **Register:** 71 claims: 11 VERIFIED, 5 VERIFIED (HISTORICAL), 43 PENDING PRIMARY DOCUMENT, 4 CONFLICTING SOURCES, 8 NOT USED.
* **Model:** 0 errors, master check OK, readiness unchanged.
