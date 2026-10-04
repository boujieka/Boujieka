# Case Data Audit: Book 7 benchmark cases

Audit date: 2026-10-04. Scope: every row of `CASES` in `model/build_model.py` and every case fact cited in `book7/src/*.md` and `book7/src/tech/*.md` with an `[A1:Sn]`, `[A2:Sn]` or `[INT:Sn]` ID.

Status key: CONFIRMED = read on the fetched page or PDF; CONFIRMED-SUMMARY = seen only in a search summary; CORRECTED = value, wording or citation changed (correct value and source given); NOT FOUND = no public figure found.

New sources added (existing numbers unchanged):
- africa_part2 **[S63]**: World Bank PAD, Nachtigal Hydropower Project, Report No. 122876-CM (P157734), https://ewsdata.rightsindevelopment.org/files/documents/34/WB-P157734_j0tmCq4.pdf
- africa_part2 **[S64]**: Cameroon Tribune, "Barrage de Nachtigal : à pleine puissance" (27 Mar 2025), https://cameroon-tribune.cm/article.html/69784/fr.html/details_2
- africa_part2 **[S65]**: The Citizen, "Julius Nyerere Hydropower Project reaches major milestone with full turbine activation" (5 Apr 2025), https://thecitizen.co.tz/tanzania/news/national/julius-nyerere-hydropower-project-reaches-major-milestone-with-full-turbine-activation-4991572
- international_benchmarks **[S24]**: EIB topical brief, "Nam Theun 2 hydropower project, Laos", https://www.eib.org/en/press/topical-briefs/all/nam-theun-2-hydropower-project-laos

Status markers changed from snippet to fetched: A2 S23, S29, S53; INT S19.

## Totals

102 facts checked: **CONFIRMED 88**, **CONFIRMED-SUMMARY 1**, **CORRECTED 11**, **NOT FOUND 2**.

## Fact table

"CASES" means the row in `model/build_model.py` (CASES list, lines 1523-1537).

| # | Claim | Where used | Source | URL | Supporting text (quote) | Status |
|---|---|---|---|---|---|---|
| 1 | Nachtigal 420 MW | CASES | A2:S63 | ewsdata …WB-P157734_j0tmCq4.pdf | "Power Plant Size 420 MW" | CONFIRMED |
| 2 | Nachtigal EUR 1.2bn | CASES | A2:S1 | blogs.worldbank.org/en/ppps/hydropower-cameroon-… | "The project cost is estimated at €1.2 billion with a five-year construction period." | CONFIRMED |
| 3 | Nachtigal US$1,383m per WB PAD (cost used) | CASES | A2:S63 (was cited as S1-S6) | as #1 | "total Project cost is expected to be approximately EUR 1,184 million (approximately US$ 1,383 million) including EUR 114 million of funded contingencies" | CONFIRMED (source ref added) |
| 4 | Nachtigal FC Nov 2018 | CASES | A2:S4 | renewableenergyworld.com/…nachtigal-hydropower-plant/ | signed "November 9, 2018" (research file said 8 Nov; fixed) | CONFIRMED |
| 5 | Nachtigal 5-year plan | CASES | A2:S1; A2:S63 | as #2; #1 | "five-year construction period"; PAD: "total duration of 57 months" | CONFIRMED |
| 6 | Nachtigal full COD "Dec 2024 / 2025" | CASES | A2:S64 | cameroon-tribune.cm/article.html/69784/… | "Cet ouvrage a atteint sa pleine capacité depuis le 27 février dernier, avec le couplage du septième et dernier groupe" | CORRECTED: full capacity 27 Feb 2025 |
| 7 | Nachtigal defects found by regulator 2023 | CASES | A2:S5 | businessincameroon.com/energy/2111-13531-… | ARSEL inspection 11 Aug 2023: "vertical cracks are visible between the joints of several blocks" | CONFIRMED |
| 8 | IBRD payment guarantee EUR 86m, loan guarantee EUR 171m | CASES | A2:S3 | ewsdata …WB-P157734.pdf | "IBRD payment guarantee in the amount of up to EUR 86 million … IBRD loan guarantee in the amount of up to EUR 171 million" | CONFIRMED |
| 9 | Nachtigal MIGA cover | CASES | A2:S3 | as #8 | "MIGA guarantees in the total amount of up to EUR 224.8 million (US$ 262.5 million equivalent)" | CONFIRMED |
| 10 | Nachtigal 75:25 debt:equity | CASES | A2:S63 (S4: "a quarter") | as #1 | "financed on a limited recourse basis with a 76:24 debt-to-equity ratio" | CORRECTED: 76:24 (PAD) |
| 11 | Cameroon backs IBRD guarantees by indemnity | ch08.md:40 | A2:S3 cited; text is in A2:S63 | as #1 | "The Member Country will reimburse and indemnify IBRD on demand … for all payments under the IBRD Guarantee"; "There will be a single Indemnity Agreement in respect of both IBRD Guarantees." S3 does not mention an indemnity | CORRECTED (citation) |
| 12 | Nachtigal debt from 11 DFIs and local banks, coordinated by IFC | ch13.md:11 | A2:S6 cited (HTTP 403); A2:S4 | as #4 | "11 development finance institutions and four local commercial banks"; IFC "global financing coordinator" | CORRECTED (citation to S4) |
| 13 | Bujagali 250 MW | CASES | A2:S49 | miga.org/project/bujagali-energy-ltd-4 | "a 250 megawatt, run-of-the-river hydropower plant" | CONFIRMED |
| 14 | Bujagali US$582m (2001) | CASES, ch10.md:45 | A2:S48 | documents1.worldbank.org/…/33722.pdf | "Total project costs were estimated at US$582 million." | CONFIRMED |
| 15 | Bujagali US$799m (2007) | CASES | A2:S49 | as #13 | "Total project cost is estimated at $799 million." | CONFIRMED |
| 16 | Bujagali US$862m (2012) | CASES, ch10.md:45 | A2:S52 | independent.co.ug/bujagali-power-expensive | "Bujagali power plant has so far cost $862 million according to Sithe Global Vice President" | CONFIRMED |
| 17 | +48% "driven by re-procurement and escalation" | CASES, ch10.md:45 | A2:S48; A2:S52 | as #14, #16 | 862/582 = 1.48 (arithmetic). Neither source gives a cause. The 2001 scope "included construction of a 100 kilometer transmission line", so it is not like-for-like | CORRECTED (wording) |
| 18 | IDA PRG up to US$115m, indemnity 2007 | CASES, ch08.md:40 | A2:S53 | documents1.worldbank.org/…/B01301UG1IA10CONFORMED.pdf | "INDEMNITY AGREEMENT, dated July 18, 2007 … loan to the Company of up to one hundred fifteen million United States Dollars (US$115,000,000)" | CONFIRMED |
| 19 | MIGA US$115m | CASES | A2:S49 | as #13 | "$115 million in guarantee coverage" against "breach of contract" for "up to 20 years" | CONFIRMED |
| 20 | 2018 refinancing in exchange for a tax waiver | CASES | A2:S51 | eagle.co.ug/2018/04/11/… | "a waiver of a 30 per cent corporation tax for Bujagali Energy Limited"; repayment extended to 2032 | CONFIRMED |
| 21 | First attempt collapsed after ECAs withdrew "and corruption investigations followed" | ch04.md:25 | A2:S48 | as #14 | "withdrawal of export credit agency support … in January 2002"; "Secondly, in parallel, there were ongoing investigations … concerning allegations of corruption involving one of the engineering/procurement/construction contractors" | CORRECTED (investigations ran in parallel and did not follow) |
| 22 | Bujagali c.2007-2012 | CASES | A2:S53; A2:S52 | as #18, #16 | Indemnity dated 18 Jul 2007; cost "so far" Mar 2012 | CONFIRMED |
| 23 | Bui 400 MW | CASES | A1:S38 | graphic.com.gh/features/opinion/the-power-of-bui-dam.html | "adding 400 megawatts" | CONFIRMED |
| 24 | Bui US$622m → 790m (2012), +168m, ~27% | CASES, ch01.md:61, ch10.md:45 | A1:S38 | as #23 | "The initial $622 million cost of the project" increased by $168 million in 2012 to $790 million (168/622 = 27%) | CONFIRMED |
| 25 | Bui COD Dec 2013 | CASES | A1:S38 | as #23 | "December 2013 inauguration" | CONFIRMED |
| 26 | China Exim loans secured on cocoa escrow | CASES | A1:S38 | as #23 | "Proceeds of 30,000 tonnes of cocoa per year exported to China is placed in an escrow account at the Exim Bank to serve as collateral." | CONFIRMED |
| 27 | ECG owed BPA ~US$612m, Mar 2023 | ch01.md:63, ch16.md:57 | A1:S40 | gna.org.gh/2023/03/ecg-owes-bpa-us612-million-… | headline "ECG owes BPA US$612 million"; dated 31 Mar 2023 | CONFIRMED |
| 28 | KGL 750 MW | CASES | A1:S58 | power-technology.com/projects/kafue-gorge-lower-… | "750MW (5 x 150MW)" | CONFIRMED |
| 29 | KGL US$2.0bn incl. US$312m capitalised interest | CASES, ch10.md:45 | book cites A1:S59; A1:S60. The breakdown is in A1:S58 | as #28 | "$2bn" … "Capitalised interest: $312m". S60 gives only the $2bn total ("some $300m less than the previously expected") | CORRECTED (citation) |
| 30 | KGL Nov 2015 → full COD Mar 2023 | CASES | A1:S58; A1:S57 | as #28; china.aiddata.org/projects/92289 | began "November 2015", completion "2020"; "On March 24, 2023, the fifth turbine was launched and the entire project was officially commissioned" | CONFIRMED |
| 31 | KGL from US$1.48bn | CASES | A1:S57 | as #30 | "cost of the EPC contract with Sinohydro … reportedly increased from $1.48 billion to $2 billion" | CONFIRMED |
| 32 | KGL ~3 years late | CASES, ch10.md:45 | A1:S57; A1:S58 | as #30 | scheduled 2020, fully commissioned 24 Mar 2023 | CONFIRMED |
| 33 | KGL sovereign guarantee | CASES | A1:S57 | as #30 | "Zambia's Ministry of Finance provided a sovereign guarantee in support of the loan" | CONFIRMED |
| 34 | ZESCO arrears in sovereign DSA | CASES | A1:S61 | documents1.worldbank.org/…BOSIB-e3b08a14….txt | DSA table row "ZESCO external IPP arrears 101"; "ZESCO's contingent risks to the sovereign" | CONFIRMED |
| 35 | Isimba 183 MW | CASES | A2:S34 | china.aiddata.org/projects/36216 | "183.2MW" | CONFIRMED |
| 36 | Isimba US$567.7m | CASES | A2:S34; A2:S35 | as #35; nsenergybusiness.com/projects/isimba-… | "$567,738,990.96"; "$567.7 million" | CONFIRMED |
| 37 | Isimba and Karuma 85% China Exim / 15% GoU | CASES, ch01.md:47, ch09.md:42 | A2:S34; A2:S40 | as #35; eagle.co.ug/2024/09/26/… | Isimba: Chinese loan "financing 85%"; Karuma: "China's Exim Bank funding 85% and Uganda's government providing 15%" | CONFIRMED |
| 38 | Isimba Apr 2015 → Mar 2019, ~7 months late | CASES | A2:S34 | as #35 | began "April 30, 2015"; target "August 30, 2018"; "officially commissioned on March 22, 2019" | CONFIRMED |
| 39 | Isimba ~700 defects "at handover" | CASES, ch09.md:42, ch11.md:33 | A2:S34 (S35 has no defect data) | as #35 | "By June 2021 … UEGCL leadership reported 'nearly 700 dam construction defects'" (commissioned Mar 2019) | CORRECTED (reported 2021, not at handover; drop S35) |
| 40 | Karuma 600 MW | CASES | A2:S40 | as #37 | "six vertical Francis turbine units, each producing 100MW" | CONFIRMED |
| 41 | Karuma US$1.7bn | CASES | A2:S40; A2:S41 | as #37; renewableenergyworld.com/news/600-mw-karuma-… | "$1.7 billion (Shs6.3 trillion)" | CONFIRMED |
| 42 | Karuma contracted 2013 for 5 years; COD Jun 2024; commissioned Sep 2024 | CASES, ch01.md:61, ch10.md:45 | A2:S40; A2:S41 | as #37 | contract "June 2013", "Five years (expected completion in 2018)", COD "June 12, 2024", commissioning "September 26, 2024" | CONFIRMED |
| 43 | Karuma contractor wants Shs148bn (~US$40m) for defects | ch09.md:42, ch11.md:33 | A2:S42 | monitor.co.ug/…shs148b-to-fix-defects-5570110 | "The cost of our proposal is about $40 million, about 3.4 percent of the contract cost ($1.4b)"; Shs147.9bn, for water weed/debris and cooling-water defects | CONFIRMED |
| 44 | JNHPP 2,115 MW | CASES | A2:S30; A2:S31 | enerdata.net/…julius-nyerere…; waterpowermagazine.com/news/tanzania-inaugurates-… | "2,115 MW Julius Nyerere Hydropower Project" | CONFIRMED |
| 45 | JNHPP TZS 7.45tn / US$2.8bn; US$2.9bn | CASES | A2:S30; A2:S31 | as #44 | "The TZS7.45tn (USD2.8bn) plant"; WPM "$2.9bn" | CONFIRMED |
| 46 | JNHPP TZS 6.5tn | CASES | A2:S65 (S32 page returns 403) | thecitizen.co.tz/…4991572 | "The project, with a cost of Sh6.5 trillion" | CONFIRMED |
| 47 | JNHPP 42-month EPC, award Dec 2018 | CASES | A2:S31 | as #44 | "42 months"; awarded December 2018 | CONFIRMED |
| 48 | JNHPP construction Jun 2019 → Mar 2025; inaugurated 22 Aug 2026; ~3 years late | CASES | A2:S30; A2:S31 | as #44 | "construction began in June 2019 and was completed in March 2025" | CONFIRMED |
| 49 | JNHPP funded from state budget | CASES, ch01.md:47 | ch01 cites A2:S30, which has no financing sentence; A2:S65 | as #46 | "99.5 percent of the project's funding came from domestic revenue"; "99.5 percent of its total funding already paid by the government" | CORRECTED (citation to S65) |
| 50 | Rusumo 80 MW | CASES | A2:S16 | documents1.worldbank.org/…/P075941-….pdf | "The RRFHP is a 80 MW run-of-…" | CONFIRMED |
| 51 | Rusumo US$468.9m | CASES | A2:S17 | ewsdata…/WB-P075941/pdf | "Project Cost (USD) $ 468.90 million" | CONFIRMED |
| 52 | Rusumo approval 2013 → COD Feb 2025 | CASES | A2:S16 | as #50 | approved "August 6, 2013"; "The COD was declared in mid February 2025." | CONFIRMED |
| 53 | Rusumo main civil works +47% | CASES, ch01.md:61, ch10.md:45 | A2:S16 | as #50 | "Increase in the CP1 contract price by about 47 percent … from USD 75,138,586 … to USD 110,412,615" | CONFIRMED |
| 54 | Rusumo "resettlement" / "land acquisition and livelihood restoration" cost doubled, US$18m → 38m | CASES, ch07.md:40, ch10.md:45 | A2:S16 | as #50 | "Increase in the livelihood restoration plan (LRP) and LADP [Local Area Development Plan] activities by USD 20 million (from USD18 million to about USD38 million) associated with repairs/construction of houses … damaged by excavation … and additional LADP activities (USD 15 million) requested by the governments" | CORRECTED (scope is livelihood restoration and local development, not land acquisition) |
| 55 | Rusumo IDA-financed; transmission AfDB/EU | CASES | A2:S16 | as #50 | "parallel financed by the African Development Bank (AfDB) and the European Union, who finance the transmission facilities" | CONFIRMED |
| 56 | Rusumo safeguards rating | annex_r.md:15 | A2:S16 | as #50 | "overall safeguards rating … updated to Moderately Satisfactory" | CONFIRMED |
| 57 | Rusumo sediment/organics in cooling water, shaft-seal wear | annex_r.md:73 | A2:S16 | as #50 | "accumulation of organic material …"; "abnormal wearing of the turbine shaft seals and higher outages" | CONFIRMED |
| 58 | Rusumo 580 structures (TZ), 80 households relocated (RW), decision 2023 | annex_r.md:85 | A2:S16 | as #50 | "repair and reconstruction works of 580 PAPs houses/structures"; "relocation … for 80 households"; decision made "late, only in 2023" | CONFIRMED |
| 59 | Rusumo closing date Dec 2020 → Jun 2025, three restructurings | annex_r.md:85 | A2:S16 | as #50 | "June 30, 2025 (having been extended from original closing date of December 31, 2020 in three project restructurings)" | CONFIRMED |
| 60 | Rusumo owned equally by three states | annex_r.md:101 | A2:S16 | as #50 | "Rusumo Power Company Limited (RPCL), a company that is owned equally by the three countries" | CONFIRMED |
| 61 | Rusumo livelihood programmes more than doubled | annex_r.md:85, 132 | A2:S16 | as #54 | as #54 | CONFIRMED (annex wording already correct) |
| 62 | Mpatamanga 358.5 MW | CASES | A2:S26 | disclosures.ifc.org/project-detail/ED/43014/mpatamanga | "358.5 MW dual-dam hydropower development" | CONFIRMED |
| 63 | Mpatamanga US$1.5bn / US$1,636m | CASES | A2:S28; A2:S27 | ippjournal.com/…mpatamanga…; ewsdata…p513960… | "exceeds US$1.5 billion"; "$ 1,636.00 million" | CONFIRMED |
| 64 | Mpatamanga earlier ~US$1bn | CASES | A2:S29 | enr.com/articles/54778-… | "$1-billion", 350 MW, 12 Sep 2022 | CONFIRMED (was snippet) |
| 65 | Mpatamanga 5-year build in 35-year PPA | CASES | A2:S27 | as #63 | "35 years, with five years construction and 30 years of operation" | CONFIRMED |
| 66 | Mpatamanga IDA PRG US$100m; MIGA US$180m; IDA grant US$350m | CASES | A2:S26 | as #62 | "IDA Partial Risk Guarantee: US$100 million"; "MIGA … up to US$180 million"; "IDA Grant … US$350 million" | CONFIRMED |
| 67 | Ruzizi III 206 MW | CASES, ch17.md:45 | A2:S22 | engineeringnews.co.za/…eib-reviews-financing-for-760m-… | "planned capacity of 206 megawatts" | CONFIRMED |
| 68 | Ruzizi III US$760m | CASES | A2:S22 | as #67 | "$760m hydro project" (EIB 2020 [S21]: EUR 728m for 147 MW, added) | CONFIRMED |
| 69 | Ruzizi III target 2030 | CASES | A2:S22 | as #67 | "aiming to operate by 2030" | CONFIRMED |
| 70 | Ruzizi III "stalled since c.2009" | CASES, ch01.md:59 | A2:S20 cited; A2:S21; A2:S22 | eib.org/en/press/all/2020-065-…; as #67 | EIB has supported Ruzizi III "since 2009"; "in planning for more than a decade". S20 gives no 2009 date | CORRECTED (in preparation since at least 2009, not stalled since then) |
| 71 | IFIs ~60%; EIB lead arranger | CASES | A2:S23; A2:S22 | power-technology.com/projects/ruzizi-iii-…; as #67 | "will fund 60% of the project cost"; EIB "the lead arranger" | CONFIRMED (S23 now fetched) |
| 72 | EIB reviewing financing in 2025 because of war | ch17.md:45 | A2:S22 | as #67 | "the Ruzizi III project site is within the conflict area"; "wait and see" | CONFIRMED |
| 73 | GERD 5,150 MW | CASES | A1:S1 | enr.com/articles/61317-… | "5,150 MW across 13 Francis turbines" | CONFIRMED |
| 74 | GERD ~US$5bn, budget US$4.8bn | CASES | A1:S1 | as #73 | "$5 billion" (initial budget $4.8 billion) | CONFIRMED |
| 75 | GERD 2011 → inauguration Sep 2025 | CASES | A1:S1 | as #73 | construction began 2011; "Inaugurated September 9, 2025" | CONFIRMED |
| 76 | GERD domestic finance, no MDB | CASES | A1:S1 | as #73 | "91% of the $5 billion cost was financed domestically through bonds, payroll contributions and public fundraising"; China Exim ~$1bn for turbines; "No multilateral bank funding" | CONFIRMED (Exim added) |
| 77 | GERD no binding operating agreement with Egypt/Sudan | ch07.md:46 | A1:S1 | as #73 | "no binding operating agreement has been established with Egypt and Sudan" | CONFIRMED |
| 78 | Gibe III 1,870 MW | CASES | A1:S55 | waterpowermagazine.com/news/gibe-iii-inaugurated-… | "1870MW" | CONFIRMED |
| 79 | Gibe III EUR 1.47-1.55bn | CASES | A1:S54; A1:S53; A1:S55 | china.aiddata.org/projects/105839; banktrack.org/news/gibe_3_…; as #78 | "EUR 1.47 billion"; "$2 billion (€1.55 billion)"; "€1.5 billion" | CONFIRMED |
| 80 | Gibe III inaugurated Dec 2016 | CASES | A1:S55 | as #78 | "mid December" 2016 | CONFIRMED |
| 81 | Gibe III no-bid civil works incompatible with WB policy; AfDB, EIB withdrew; E&M financed by ICBC | ch04.md:25, CASES | A1:S53; A1:S54 | as #79 | "no-bid contract with … Salini, violates international procurement standards"; WB said it conflicted with its procurement policy; "ICBC stepped into the breach when the EIB and the AFDB withdrew their support" | CONFIRMED |
| 82 | Gibe III overrun | CASES | — | — | BankTrack mentions "cost overruns" but gives no amount | NOT FOUND (kept "PUBLIC DATA NOT FOUND") |
| 83 | NT2 1,070 MW | CASES | INT:S10; INT:S24 | infrastructure.greenstreet.com/articles/23099/…; eib.org/…nam-theun-2… | "995MW – EGAT" and "75MW – EdL"; "installed generating capacity of 1,070 MWe" | CONFIRMED |
| 84 | NT2 US$1.25bn base + US$200m contingency | CASES | INT:S9 | miga.org/…/NT2.pdf | "total estimated base project cost of $1.25 billion"; "the additional $200 million of contingent costs" | CONFIRMED |
| 85 | NT2 FC Jun 2005 | CASES | INT:S10 | as #83 | "10 June 2005" | CONFIRMED |
| 86 | NT2 COD Apr 2010 | CASES | INT:S24 (new) | as #83 | "Since being commissioned in April 2010" | CONFIRMED (was snippet) |
| 87 | NT2 IDA, ADB, MIGA covering ~US$186m of debt | CASES | INT:S9 | as #84 | "debt guarantees from IDA, the Asian Development Bank and MIGA covering about $186 million of the debt financing" | CONFIRMED |
| 88 | NT2 turnkey price-capped EPC | CASES | INT:S9 | as #84 | "a turnkey, price-capped" contract | CONFIRMED |
| 89 | NT2 overrun | CASES | — | — | none found | NOT FOUND (kept) |
| 90 | UT-1 216 MW | CASES | INT:S17 | aiib.org/…PSI-P000085-…pdf | "216 mega-watt greenfield run-of-river hydropower plant" | CONFIRMED |
| 91 | UT-1 US$647.4m | CASES | INT:S17 | as #90 | "Total project cost: USD647.4 million" | CONFIRMED |
| 92 | UT-1 debt ~70% | CASES | INT:S17 | as #90 | "Debt: USD453.2 million" (453.2/647.4 = 70%) | CONFIRMED |
| 93 | UT-1 2024 → Dec 2026 | CASES | INT:S15; INT:S19 | ifc.org/en/pressroom/2019/…; andritz.com/hydro-en/hydronews/hn36/… | expected completion 2024 (IFC); "completion scheduled for December 2026" | CONFIRMED (S19 now fetched) |
| 94 | Reventazón 305.5 MW, US$1.4bn | CASES | INT:S20 | infrastructure.greenstreet.com/articles/127517/… | "$1.4 billion" … "305.5MW hydro power plant" | CONFIRMED |
| 95 | Reventazón FC Jan 2014 | CASES | INT:S20 | as #94 | closed "29 January 2014" | CONFIRMED |
| 96 | Reventazón inaugurated Sep 2016 | CASES | INT:S23 (403) | newenergyevents.com/… | search summary: "inaugurated on 16 September 2016" | CONFIRMED-SUMMARY |
| 97 | Reventazón post-COD spillway repairs ~US$15m | CASES, ch11.md:25 | INT:S22 | crhoy.com/nacionales/ice-asegura-… | "La intervención, en principio, estuvo fijada en $15 millones"; work on the "canal del vertedero" | CONFIRMED |
| 98 | Reventazón trust + lease; IDB A-loan; IFC; IG bond; local-currency debt | CASES | INT:S20 | as #94 | IADB A-loan $200m; IFC $100m; private placement $135m, Fitch "BBB-"; local bank $469m colón | CONFIRMED |
| 99 | Belo Monte 11,233 MW vs 4,571 MW assured | ch02.md:13 | INT:S8 | apublica.org/2017/11/belo-monte-… | "capacidade total de geração 11.233 megawatts (MW) e 4.571 MW de energia assegurada" | CONFIRMED |
| 100 | Nyagak III awarded by tender | ch04.md:15 | A2:S45 | ifc.org/…2016-uganda-nyagak-hydro-ppp-brief.pdf | "competitive tender process that resulted in the selection of a strategic partner" | CONFIRMED |
| 101 | Batoka: Zambia exited 2019 arrangement in 2023 over procurement | ch04.md:25 | A2:S57 | engineeringnews.co.za/article/batoka-gorge-…-2024-03-29 | "In June 2023 … would exit the 2019 contract with GE and Power China because proper procurement methods were not followed" | CONFIRMED |
| 102 | Multilateral guarantees backed by government indemnities | ch15.md:37 | A2:S53 | as #18 | Uganda–IDA Indemnity Agreement for the guaranteed loan | CONFIRMED |

Not in scope: citations with other prefixes (DE:, CL-, HY-, LIT:) such as Kariba, Ngonye and Kikagati.

## Changes made to CASES (`model/build_model.py`)

- **Nachtigal:** reported cost now "EUR 1,184m (~US$1,383m) per World Bank PAD". Timeline now "FC Nov 2018; 57-month build planned, COD 2023; 7th unit coupled 27 Feb 2025". Overrun now "Full capacity ~2 yrs late; defects found by regulator (ARSEL) Aug 2023". Credit support now includes the sovereign indemnity and MIGA up to EUR 224.8m, with "76:24 debt:equity (PAD)". Refs now "africa_part2 S1-S5, S63-S64".
- **Bujagali:** costs are labelled as estimates or "so far". Overrun now reads "+48% vs cancelled 2001 design; not like-for-like (2001 scope incl. 100 km line)". Refs now S48-S53.
- **Rusumo:** overrun now "CP1 civil contract +47%; livelihood restoration/local development US$18m → ~38m".
- **Mpatamanga:** "(snippet)" replaced by "(ENR, Sep 2022)".
- **Ruzizi III:** cost now notes EUR 728m for the 147 MW design in 2020. Overrun now "In preparation since at least 2009; no financial close".
- **GERD:** credit support now "91% domestic (bonds, payroll, public); China Exim ~US$1bn for E&M; no MDB finance".
- **Julius Nyerere:** credit support now "None (budget-funded; 99.5% domestic revenue)". Refs gain S65.
- **Isimba:** refs note that defects were reported in 2021.
- **Nam Theun 2:** timeline now "commissioned Apr 2010". Refs gain S24.
- **Upper Trishuli-1:** "(snippet)" replaced by "(scheduled)".
- **Reventazón:** "(snippet)" replaced by "(search summary)".
- No cost-used numbers changed.

## Required book text corrections (not applied; book7/src not edited)

1. **book7/src/ch01.md:59**
   - Old: `Ruzizi III, a regional public-private partnership, has been stalled since about 2009 [A2:S20].`
   - New: `Ruzizi III, a regional public-private partnership, has been in preparation since at least 2009 without reaching financial close [A2:S21; A2:S22].`
2. **book7/src/ch01.md:47**
   - Old: `Julius Nyerere in Tanzania was funded from the state budget [A2:S30].`
   - New: `Julius Nyerere in Tanzania was funded from the state budget [A2:S65].`
3. **book7/src/ch04.md:25**
   - Old: `The first attempt at Bujagali collapsed after export credit agencies withdrew and corruption investigations followed [A2:S48].`
   - New: `The first attempt at Bujagali collapsed after export credit agencies withdrew, amid corruption investigations involving one of the construction contractors [A2:S48].`
4. **book7/src/ch07.md:40**
   - Old: `At Rusumo Falls, land acquisition and livelihood restoration costs roughly doubled during implementation, from about USD 18 million to about USD 38 million [A2:S16].`
   - New: `At Rusumo Falls, livelihood restoration and local development costs roughly doubled during implementation, from about USD 18 million to about USD 38 million, largely to repair houses damaged by construction blasting and to fund extra local works requested by the governments [A2:S16].`
5. **book7/src/ch08.md:40**
   - Old: `Cameroon backs the IBRD guarantees for Nachtigal through a similar indemnity [A2:S3].`
   - New: `Cameroon backs the IBRD guarantees for Nachtigal through a similar indemnity [A2:S63].`
6. **book7/src/ch10.md:45** (Bujagali)
   - Old: `Bujagali in Uganda cost about USD 862 million against about USD 582 million for the 2001 design, an increase of about 48 percent driven by re-procurement and escalation [A2:S48; A2:S52].`
   - New: `Bujagali in Uganda was reported in 2012 to have cost about USD 862 million, against about USD 582 million estimated for the cancelled 2001 design, about 48 percent more; the 2001 scope also included a 100 km transmission line, so the gap is not a like-for-like overrun [A2:S48; A2:S52].`
7. **book7/src/ch10.md:45** (Rusumo)
   - Old: `the civil works rose by about 47 percent and the cost of resettlement doubled [A2:S16]`
   - New: `the main civil works contract rose by about 47 percent and livelihood restoration and local development costs doubled [A2:S16]`
8. **book7/src/ch10.md:45** (Kafue Gorge Lower citation)
   - Old: `with about USD 312 million of capitalised interest in a total cost of about USD 2.0 billion [A1:S59; A1:S60]`
   - New: `with about USD 312 million of capitalised interest in a total cost of about USD 2.0 billion [A1:S57; A1:S58; A1:S60]`
9. **book7/src/ch11.md:33**
   - Old: `Uganda's Isimba plant was reported to have about 700 defects at handover [A2:S34; A2:S35]`
   - New: `Uganda's Isimba plant was reported in 2021, two years after commissioning, to have nearly 700 unrepaired defects [A2:S34]`
10. **book7/src/ch13.md:11**
    - Old: `Nachtigal's debt came from eleven development finance institutions and local banks, coordinated by IFC [A2:S6].`
    - New: `Nachtigal's debt came from eleven development finance institutions and four local banks, coordinated by IFC [A2:S4].`

Optional, not an error: ch09.md:42 says "several hundred defects were reported after commissioning". That is accurate. Adding "(nearly 700, by 2021)" would make it more precise.
