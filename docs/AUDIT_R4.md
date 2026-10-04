# Audit R4: Annexes N to R (technical due-diligence reference)

Files: book7/src/tech/annex_n.md, annex_o.md, annex_p.md, annex_q.md, annex_r.md.
Method: every technical number grepped against local full texts (ifc.txt [DE:S1], esha.txt [LIT:S6], ag.txt [LIT:S7], esmap.txt [HY-06]); other IDs checked against research/source_database.md and research/hydro_development_evidence.md; all Kasiri arithmetic recomputed (Python).

## Summary counts

Citation claims audited: 214 (about 150 [DE:S1], 30 [LIT:S6], 14 [LIT:S7], 14 [HY-06], 6 others)

| Status | Count |
|---|---|
| CONFIRMED-FULLTEXT | 196 |
| CONFIRMED-PAGE | 11 (CL-04 re-read by R4; DE:S9, S12, S13, S16, S17, S47, S49, S51, S52, S40b by evidence-file record) |
| SUMMARY-ONLY | 5 (HY-15 x4 now partly backed by R4:S1; CL-03; HY-03; DE:S50 also backed by S49) |
| NOT SUPPORTED, corrected | 6 |

Kasiri arithmetic: 64 computations checked; 62 correct, 2 corrected (N.3 monthly-overestimate row, P.13 energy check); 2 wording errors in derivations corrected (O contingency sentence, O penstock limit).

## Audit table (selected; all others CONFIRMED-FULLTEXT on grep of the stated source)

| Claim | File:line | Source | Evidence | Status | Action |
|---|---|---|---|---|---|
| Energy "one of the most important determinants"; hydrology highest risk | N:5 | DE:S1 | "one of the most important determinants of HPP viability"; "Hydrology. Poses the highest risk" | CONFIRMED-FULLTEXT | none |
| Climate change makes rigorous assessment necessary | N:5 | HY-06 | "making rigorous assessment necessary, especially due to the risks of climate change" | CONFIRMED-FULLTEXT | none |
| At least 15 years of record | N:21 | DE:S1 | "no less than 15 years, preferably consecutive" | CONFIRMED-FULLTEXT | none |
| Five dry, five average, five wet measurements | N:25 | DE:S1 | "at least five dry-period, five average-period, and five wet-period" | CONFIRMED-FULLTEXT | none |
| Manning n 0.035, 0.001 error = 3% | N:15 | LIT:S6 | "about 0.035, an error in n of 0.001 gives an error in discharge of 3 per cent" | CONFIRMED-FULLTEXT | none |
| Qm = AARD x area / 31,536 | N:31 | LIT:S6 | "Qm = (AARD x AREA) / 31536" | CONFIRMED-FULLTEXT | none |
| Monthly data overestimate energy 10% or more | N:37 | DE:S1 | "can overestimate energy generation by 10 percent or more" | CONFIRMED-FULLTEXT | Table N.3 value corrected 263 to 266 GWh (292.2/1.10) |
| Level of use 1.0 to 1.5; design flow 100 to 120 days | N:58 | DE:S1 | "usually ranges from 1.0-1.5"; "available 100 to 120 days a year or about 30 percent" | CONFIRMED-FULLTEXT | none |
| Optimum design flow "significantly larger than" mean less reserved | N:58 | LIT:S6 | quoted verbatim | CONFIRMED-FULLTEXT | none |
| Min flow IFC Francis 40, Kaplan 20 to 40, Pelton 10 to 20; ESHA 50/15/10/30/20/75 | N:60, P Table P.2 | DE:S1; LIT:S6 | IFC 4.2 list; ESHA Table 3-2 | CONFIRMED-FULLTEXT | none |
| 8.5 x Q x H at 87%; generator 90 to 98%, transformer 98 to 99.5% | N:76 | DE:S1 | Table 7-2 and rough-estimation formula | CONFIRMED-FULLTEXT | none |
| ESHA example 1.52 m losses, 1.8% power loss, 3 m3/s, 85 m | N:78 | LIT:S6 | "1,29 m friction loss plus 0,23 m ... loss of power of 1,8%" | CONFIRMED-FULLTEXT | none |
| Availability 95% (11 + 7 days), 97 to 98% after three years | N:82, P, Q | DE:S1 | quoted | CONFIRMED-FULLTEXT | none |
| Auxiliary demand 0.5 to 3.0% | N:83 | DE:S1 | "0.5-3.0 percent of annual energy generation" | CONFIRMED-FULLTEXT | none |
| Run-of-river capacity factor 40 to 70% | N:99, P | DE:S1 | Box 7-2 | CONFIRMED-FULLTEXT | none |
| Firm energy 90 to 95% certainty | N:118 | LIT:S6 | ESHA 3.7 | CONFIRMED-FULLTEXT | none |
| IFC firm capacity 11 MW vs 23 MW; Nov flow ten times Feb | N:118 | DE:S1 | Section 7.4 | CONFIRMED-FULLTEXT | none |
| P75 dry year, P95 very dry year; DSCR > 1 in worst-case hydrology | N:122 | DE:S1 | lines on P75/P95 and DSCR | CONFIRMED-FULLTEXT | none |
| Kariba 2024 allocation cut about 47% | N:144, R:109 | CL-04 | "by 47 per cent to 16 billion cubic metres (BCM), down from 30 BCM" | CONFIRMED-PAGE (R4 re-read) | removed "(search summary only)" in R; added 30 to 16 bcm |
| Design flood table; lognormal 83 vs LP3 103 m3/s; 9.6% over 10 years | N:150-158, O:86, O:100 | LIT:S6 | Tables 3-3, 3-4; flood example | CONFIRMED-FULLTEXT | none |
| 0.2 mm above 100 m, 0.3 mm lower heads | N:170, O, P | DE:S1 | "if the head is higher than 100 m, all particles larger than 0.2 mm" | CONFIRMED-FULLTEXT | none |
| Francis repair 6 to 7 / 3 to 4 / 1 to 2 years | N:170, P | LIT:S6 | quoted | CONFIRMED-FULLTEXT | none |
| Storage lost to sedimentation exceeds storage added | N:172 | HY-06 | quoted | CONFIRMED-FULLTEXT | none |
| Concurrent drought risk from basin concentration | N:176, R | CL-03 | title and DB snippet | SUMMARY-ONLY | wording matches title; left |
| Pumped storage over 90%, 160 GW 2021; inertia, frequency | O:17-20 | HY-06 | quoted | CONFIRMED-FULLTEXT | none |
| Canal 1.0 to 1.5 m/s, freeboard 10/15 cm; tunnel below 3 to 4 m/s; concrete penstock 15 bar | O:31-33 | DE:S1 | quoted | CONFIRMED-FULLTEXT | none |
| ICOLD large dam; ESHA small dam | O:45 | DE:S1; LIT:S6 | quoted | CONFIRMED-FULLTEXT | none |
| Civil 33.2 to 76.5%, median 55.2, middle half 47 to 61; contingency 9.1 avg / 9.8 median; 15% / 7.5 to 10% | O:104-106, Q | DE:S1 | Table 13-4 and text | CONFIRMED-FULLTEXT | none |
| Large-dam overrun median 27, mean 96; schedule 27/44 | O:108, Q | HY-08 | DB record (F) | CONFIRMED-FULLTEXT | none |
| DFIs finance access roads and grid links | O:114 | HY-06 | ESMAP mentions DFI financing of "project transmission lines" only | NOT SUPPORTED | reworded to transmission lines |
| Dam safety note: panels, hydrological and seismic risk | O:88, N:158, R:15, R:25, R:93 | HY-15 | DB status S; R4:S1 page confirms technical notes on hydrological and seismic risk | SUMMARY-ONLY, now partly CONFIRMED-PAGE | O.7 and R.7 re-cited [HY-15; R4:S1], wording narrowed |
| GBR "sole source..." (Emerald Book) | O:80 | DE:S47 | evidence file quote | CONFIRMED-PAGE | none |
| E&M 30.3% of "total project cost" | P:5 | DE:S1 | Table 13-4 is "share of main cost groups in total plant costs"; average 30.3, median 29.2 | NOT SUPPORTED (wrong base) | changed to total plant cost, added median |
| Medium head class "should not be quoted" | P:14 | DE:S1 | IFC 4.2.2 gives scheme classes H > 100, 30 to 100, < 30 m; misprint is only in turbine list | NOT SUPPORTED (incomplete) | rewritten to quote the scheme classes |
| Two 30 MW units allow 20% instead of 40% | P:70 | DE:S1 | footnote 5 | CONFIRMED-FULLTEXT | none |
| Overhaul 7 to 12 years, 4 to 6 weeks > 20 MW | P:71, Q | DE:S1 | quoted | CONFIRMED-FULLTEXT | none |
| Water hammer 25 to 50% reaction; t_h 3 s / 6 s | P:100-104 | LIT:S6 | quoted | CONFIRMED-FULLTEXT | none |
| Generator approaches 98% above 1 MW; switchyard above 100-year flood | P:98, P:108 | DE:S1 | quoted | CONFIRMED-FULLTEXT | none |
| E&M payments 30/50/20; civil 10/80/10 | P:134, Q:30 | DE:S1 | Table 9-1 | CONFIRMED-FULLTEXT | none |
| Spares 2.5 to 3.0% FOB; E&M maintenance 2.0 to 2.5%, 60% reserve; civil 0.4 to 0.6% | P:136, Q:115 | DE:S1 | quoted | CONFIRMED-FULLTEXT | none |
| "In Africa" transmission barrier to COD | Q:13 | HY-06 | ESMAP statement is general, not Africa-specific | NOT SUPPORTED (scope) | "In Africa" removed |
| Tendering up to 18 months, BOO two years; construction 9 to 18 months / up to four years | Q Table Q.1 | DE:S1 | quoted | CONFIRMED-FULLTEXT | none |
| Nyamwamba II about 29 months | Q Table Q.1 | DE:S12 | construction Oct 2019, COD 17 Mar 2022 | CONFIRMED-PAGE | none |
| Large hydro 8 to 10 years initiation to COD | Q Table Q.1 | HY-06 | "beyond eight to ten years from project initiation" | CONFIRMED-FULLTEXT | none |
| O&M 1 to 4%; IEA 2.2%; USD 45/52 per kW-yr | Q:115 | DE:S1 | quoted | CONFIRMED-FULLTEXT | none |
| Africa refurbishment 60%, USD 6.8bn, 14.7 GW; equipment rehab at 45 to 60 years | Q:112, Q:137 | HY-06 | quoted | CONFIRMED-FULLTEXT | none |
| Nachtigal BOT, transfer after 35 years | Q:135 | LIT:S7 | "its ownership after a period of 35 years" | CONFIRMED-FULLTEXT | none |
| Private stakeholders prefer minimal resettlement, community support, IFC standards | R:5 | HY-06 | quoted | CONFIRMED-FULLTEXT | none |
| World Bank "recommends governments prepare basin plans ... before procurement" | R:40 | HY-06 | ESMAP: DFI support could include preparing pre-feasibility studies including basin plans and CIAs; nothing on "before procurement" | NOT SUPPORTED | reworded |
| CBI criteria "test greenhouse gas intensity" | R:77 | HY-06 | "Key elements ... low greenhouse gas (GHG)-generating infrastructure" | NOT SUPPORTED (overstated) | reworded |
| Green bond index: HSAP 3+ or eight PS | R:105 | HY-06 | Bloomberg Barclays MSCI index quoted | CONFIRMED-FULLTEXT | none |
| Dibwangui 11 of 12 criteria | R:105 | LIT:S7 | quoted | CONFIRMED-FULLTEXT | none |
| Kariba 2015 drought load shedding | R:109 | LIT:S7 | "A severe drought in 2015 led to months of declining power generation at the Kariba dam resulting in ... load shedding" | CONFIRMED-FULLTEXT | none |
| EP4 1 Oct 2020, USD 10m, non-designated countries | R:13 | DE:S49; DE:S50 | evidence file | CONFIRMED-PAGE (S50 snippet) | none |
| Kakono USD 4.8m; Mutunguru USD 992k | R:130 | DE:S16; DE:S17 | evidence file table | CONFIRMED-PAGE | none |
| Jordan one year; Mozambique fee 0.2% | R:9 | DE:S1 | quoted | CONFIRMED-FULLTEXT | none |

[A1], [A2], [INT] citations (Rusumo in R) were not re-verified, as instructed.

## Kasiri arithmetic check (all recomputed)

Correct: mean flow 37.83; usable 33.08 m3/s; 1.061 MW per m3/s; 60.5 MW; 307.6 and 292.2 GWh; CF 55.6%; Table N.1 power column and both exceedance columns; f_a 1.51; 22.8 m3/s Francis minimum and 13.6% energy loss; 8.1 GWh per extra 1 m3/s; aux 290.7 to 283.4; availability 298 to 301; 10% flow cut 264 GWh (9.7%); P-values 262/236/220/190/274/268/281/268; SE 4.3%; flood risks 14%, 3%, 25%, 27%, 6%; tunnel 14.3 to 19.0 m2 and 4.3 to 4.9 m; canal 38 to 57 m2; pondage 0.59 million m3; civil 43%/54%; contingency 13.4 to 14.4; overruns 18.4/65.3; Table P.4 specific speeds (all rows); Table P.5 months; E&M 26%/33%, USD 550/kW; Q.4 schedule 46/52 months, advances, maintenance, USD 2.7m/yr; R.2 shares; release cost 32 GWh (10.8%); 8,016 h; E&S 3.2%.

Corrected or clarified:
- N Table N.3: a 10% monthly overestimate means daily = monthly / 1.10 = 266 GWh, not 263.
- P.13: "60.5 MW x 8,760 x 0.56 = 297 GWh" mixed the 60.5 MW hydraulic power with a CF defined on 60 MW; replaced by the consistent statement 292 / (60 x 8.76) = 55.6%.
- O Table O.4: 120 m net head plus 25 to 50% water hammer exceeds, not "approaches", the 150 m concrete-penstock limit.
- O.11: "On the works alone, the case's contingency would be 10 percent" was circular; now: 10% on the six base lines = USD 12.7m, below the 13.4 to 14.4 practice range.
- N: added note that 60.5 MW at 57 m3/s exceeds the 60 MW rating (cap costs about 0.3 GWh).
- N.7: firm capacity 17 MW is before outages; added the 16 MW after-availability figure used in Chapter 3.

## Edits made (old to new, short)

annex_n.md
1. Table N.1 note: added 60.5 MW vs 60 MW rating sentence.
2. Table N.3: "Monthly data overestimate of 10% ... 263 GWh" to "(292.2 / 1.10) ... 266 GWh".
3. N.7: firm capacity qualified "before outages", added "about 16 MW after 95% availability, the figure Chapter 3 uses".
4. N.8: serial-correlation formula and following prose were on one line; split into formula and paragraph.
5. Table N.4: "10-year" to "ten-year" in three row labels (book term "ten-year P90").

annex_o.md
6. O.7: HY-15 sentence narrowed to sample panel-of-experts TOR and technical notes on hydrological and seismic risk; re-cited [HY-15; R4:S1].
7. O.10: "DFIs can help by financing access roads and grid links" to "DFIs can support governments by financing project transmission lines [HY-06]; access roads need the same early funding."
8. Table O.4 penstock row: "approaches the limit" to "exceeds 150 m", with water hammer allowance cited [LIT:S6].
9. O.11 cost: circular contingency sentence replaced by USD 12.7m comparison.

annex_p.md
10. P.1: "total project cost" to "total plant cost (median 29.2%)".
11. P.2: head classes rewritten to quote IFC scheme classes (>100, 30 to 100, <30 m).
12. P.13: energy check sentence replaced (CF 55.6% on 60 MW).

annex_q.md
13. Q.2: removed "In Africa," before the ESMAP transmission statement.
14. Q.13: three-unit overhaul illustration replaced with Annex P's two-unit base case (one 28.5 m3/s unit passes February's 16 m3/s, above its 11.4 m3/s minimum).

annex_r.md
15. R.3: World Bank basin-plan sentence corrected to what ESMAP says.
16. R.4: "10.5 percent of mean flow" to "10.6 percent" (matches N.5; 4/37.83).
17. R.4: CBI "test greenhouse gas intensity" to "require low greenhouse gas infrastructure".
18. R.7: normal operation flood "often a 100-year event" to "defined by a return period such as 100 years"; HY-15 sentence re-cited [HY-15; R4:S1].
19. R.11: "(search summary only)" removed after page re-read; added "from 30 to 16 billion m3".

New file: research/audit_sources_R4.md ([R4:S1]).

## Open issues for the author

1. Contingency inconsistency in the book (outside my files): Chapter 3 (resolved line 384) says Kasiri's 10% contingency "follows the IFC's median of 9.8 percent of total plant cost", while Annex O argues it is too low on the works. Both can stand, but Chapter 3 should acknowledge the industry-practice comparison.
2. Firm output: Chapter 3 uses 16 MW (after availability); Annex N now gives both. Check Chapter 3 states "after availability" (it does).
3. 60.5 MW vs 60 MW: the model appears to run May at 60.5 MW. If the model does not cap at installed capacity, the P50 is overstated by about 0.3 GWh; trivial but an engineer will notice.
4. The P50 of 292 GWh is a monthly, no-minimum-flow, no-auxiliary figure (Annex N says so). A single-Francis configuration would cut it to about 252 GWh; the model does not define unit count. Consider fixing two units as a case fact.
5. HY-15 remains SUMMARY-ONLY in the source DB; the primary PDF (documents.worldbank.org, 2021) was not reachable (404 on the WB topic page). Worth obtaining and upgrading.
6. CL-03 still SUMMARY-ONLY (abstract snippet); wording kept close to the article title.
7. Annex N Table N.4 shows two different 268 GWh routes; the note explains this, but the author may prefer to show the combined figure (about 263 GWh with both serial correlation and mean uncertainty) for completeness.
8. Rebuild book7_resolved.md (tools/book7/prepare7.py) to pick up these edits.
