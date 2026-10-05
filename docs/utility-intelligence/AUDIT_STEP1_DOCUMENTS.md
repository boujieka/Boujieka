# Étape 1 : audit de disponibilité des documents publics (v0.1)

> Audit réalisé le 5 octobre 2026 par 8 agents de recherche (un par groupe de pays), suivi d’une contre-vérification indépendante. Il couvre **19 utilities dans 11 pays**, les exercices 2019 à 2025, et les 23 KPI du noyau MVP hors variables de contexte (voir `KPI_DICTIONARY.md`). Aucune valeur de KPI n’est relevée ici : l’audit dit seulement si les **données d’entrée** existent et où elles se trouvent.

## Conclusions principales

1. **Viabilité MVP** : 6 fortes, 6 utilisables, 6 faibles, 1 non viable. Les utilities cotées ou soumises à un auditeur public qui publie ses rapports (Kenya, Ghana pour GRIDCo, Afrique du Sud, Zambie) et Senelec forment le socle. **L’Afrique centrale francophone est le maillon faible** : E2C (Congo) ne publie rien en ligne ; SNEL (RDC) et SONABEL (Burkina) ne sont accessibles que via le régulateur ou les bailleurs.
2. **Le biais de transparence est confirmé.** Les utilities les moins transparentes ne pourraient pas être notées sur la finance. Elles seraient donc soit absentes, soit pénalisées par la seule dimension Gouvernance. Il faut afficher un **taux de couverture** et ne pas publier de classement agrégé pour elles.
3. **Les régulateurs et les bailleurs sont des sources de premier rang**, pas des compléments : rapports trimestriels NERC (Nigeria, par DisCo), statistiques EPRA (Kenya), Energy Commission et SIGA (Ghana, états financiers audités abrégés d’ECG et de VRA), ARSE (Burkina), ARSEL (Cameroun), CRSE (Sénégal), ARE (RDC), ERB (Zambie), documents Banque mondiale (PAD/ISR).
4. **KPI du noyau à reclasser** (voir le tableau ci-dessous) :
   - `NET_saidi_hours` : **0 calculable sur 19**, 10 « valeur publiée seule », avec des définitions incompatibles (heures annuelles ou mensuelles, avec ou sans délestage, TMC ou SAIDI). À garder en **valeur publiée avec drapeau de définition**, sans classement inter-utilities au MVP.
   - `GOV_audited_fs_publication_lag_months` : 1 seul calculable, car la date de mise en ligne est rarement déterminable et les re-téléversements faussent les dates de fichier. Utiliser la **date de signature du rapport d’audit** comme mesure principale.
   - `FIN_government_transfer_dependency` : 2 calculables, 12 partiels. Le traitement comptable des transferts varie trop (voir conclusion 5).
   - `NET_distribution_losses_pct` : surtout des valeurs publiées seules (6), rarement le bilan énergétique complet.
   - Les KPI financiers « durs » sont les plus disponibles : capex / amortissements (11 calculables), marge d’EBITDA (10), recouvrement des coûts (9), liquidité (8), délai des créances (7).
5. **Les compensations tarifaires sont comptabilisées de quatre façons** : dans le chiffre d’affaires (Senelec, « Écart sur RMA »), en subventions d’exploitation (ENEO), en autres produits (EKEDC, subvention FGN), ou en paiements directs de l’État aux producteurs (ECG, interrompus en FY2025). La règle d’extraction de `tariff_compensation_revenue_lcu_m` doit donc être documentée par utility. Sinon, l’EBITDA et le recouvrement des coûts ne sont pas comparables.
6. **Les périmètres bougent pendant la fenêtre MVP** : concession CIE (2021, la CIE ne comptabilise plus que sa rémunération) ; création de NISO au Nigeria (2024) ; filiale NTCSA d’Eskom (2025) ; filiales DisCo sous régulation de l’État de Lagos (2025) ; nationalisation d’ENEO (2026, selon la presse, décret non consulté) ; affermage E2C suspendu. Le modèle de données doit **dater le périmètre de chaque entité** (`entity_scope` par exercice).
7. **Extraction technique** : de nombreux PDF sont scannés (rapports ENEO 2020-2024, comptes EKEDC 2020-2023, états financiers ZESCO 2023 et 2025, pages d’audit kenyanes). Il faut de l’**OCR**, comme pour les rapports UMOA-Titres de Cartouche. Plusieurs sites bloquent les robots (ECG, E2C, SONABEL, Ikeja Electric). ANARE-CI exige une connexion SharePoint.
8. **La publication s’accélère** chez plusieurs utilities : Eskom FY2026 publié en août 2026, ZESCO FY2025 en mars 2026, GRIDCo FY2025 signé six mois après la clôture. L’exercice 2025, voire 2026, est donc déjà exploitable pour une partie de l’échantillon.

## Synthèse par utility

Légende des exercices 2019 → 2025. Rapport annuel : ● ouvert, ◐ lien vu mais non ouvert, ○ cité ailleurs seulement, · non trouvé, ? non vérifié. États financiers audités : ● complets avec notes, ◐ résumé ou extrait, u non audités, · non trouvé.

| Utility | Pays | Périmètre | Cadre | Rapport annuel | États fin. audités | KPI calculables / partiels / non applicables | Viabilité |
|---|---|---|---|---|---|---|---|
| Energie Electrique du Congo (E2C) | Republic of the Congo | intégrée | XAF. The framework is presum | `·······` | `·······` | 1 / 3 / 0 | **non viable** |
| Société Nationale d'Electricité (SNEL SA) | Democratic Republic of the Congo | intégrée | Unknown from primary sources | `○○··○○·` | `·······` | 2 / 2 / 0 | **faible** |
| ENEO Cameroon (now SOCADEL) | Cameroon | intégrée | XAF | `●●●●●●·` | `◐◐·◐···` | 6 / 13 / 0 | **utilisable** |
| SONATREL | Cameroon | transport | XAF | `·······` | `·····◐●` | 6 / 6 / 10 | **faible** |
| CIE (Compagnie Ivoirienne d'Electricité) | Côte d'Ivoire | autre | XOF/FCFA | `●●●●●··` | `◐◐◐◐◐◐◐` | 4 / 11 / 0 | **utilisable** |
| CI-ENERGIES (Société des Energies de Côte d'Ivoire) | Côte d'Ivoire | autre | XOF/FCFA | `··○●···` | `··◐◐◐◐·` | 6 / 12 / 1 | **faible** |
| Senelec | Senegal | intégrée | XOF | `●●●●●●·` | `◐◐◐◐◐◐·` | 9 / 13 / 0 | **fort** |
| SONABEL | Burkina Faso | intégrée | XOF | `○◐○○···` | `·······` | 2 / 5 / 0 | **faible** |
| GRIDCo (Ghana Grid Company) | Ghana | transport | GHS | `●●●●●●●` | `●●●●●●●` | 7 / 4 / 9 | **fort** |
| ECG (Electricity Company of Ghana) | Ghana | distribution | GHS | `◐·○○○○○` | `?·◐◐◐◐◐` | 2 / 11 / 1 | **utilisable** |
| VRA (Volta River Authority) | Ghana | production | GHS | `○·○○○○○` | `··◐◐◐◐◐` | 0 / 4 / 7 | **faible** |
| Kenya Power (KPLC) | Kenya | distribution | KES | `◐◐◐◐◐●●` | `???●●●●` | 16 / 5 / 0 | **fort** |
| KenGen | Kenya | production | KES | `◐◐◐◐◐◐●·` | `??????●◐` | 9 / 4 / 10 | **fort** |
| KETRACO | Kenya | transport | KES | `◐◐◐·●●◐` | `???·●●?` | 7 / 3 / 11 | **utilisable** |
| Transmission Company of Nigeria (TCN) | Nigeria | transport | NGN | `●●·····` | `●●·····` | 7 / 4 / 10 | **faible** |
| Ikeja Electric | Nigeria | distribution | NGN | `○◐·····` | `·●·····` | 5 / 6 / 3 | **utilisable** |
| Eko Electricity Distribution (EKEDC) | Nigeria | distribution | NGN | `●●●●●●·` | `●●●●●●·` | 14 / 5 / 3 | **fort** |
| ZESCO | Zambia | intégrée | ZMW | `◐●●●●●●` | `?●●●●●●` | 9 / 11 / 0 | **utilisable** |
| Eskom | South Africa | intégrée | ZAR | `●●●●●●●` | `●●●●●●●` | 15 / 7 / 0 | **fort** |

## Couverture par KPI du noyau (19 utilities)

| KPI | calculable | partiel | valeur publiée seule | absent des docs lus | non applicable |
|---|---|---|---|---|---|
| `FIN_average_revenue_per_kwh_billed` | 6 | 8 | 2 | 1 | 2 |
| `FIN_cost_recovery_ratio` | 9 | 4 | 3 | 3 | 0 |
| `FIN_current_ratio` | 8 | 5 | 2 | 4 | 0 |
| `FIN_ebitda_margin` | 10 | 3 | 0 | 6 | 0 |
| `FIN_government_transfer_dependency` | 2 | 12 | 0 | 5 | 0 |
| `FIN_power_purchase_payables_days` | 2 | 6 | 0 | 6 | 5 |
| `GEN_avg_power_purchase_cost` | 3 | 6 | 0 | 5 | 5 |
| `GEN_costly_thermal_share` | 2 | 8 | 0 | 3 | 6 |
| `GEN_purchased_energy_share` | 6 | 3 | 0 | 2 | 8 |
| `NET_distribution_losses_pct` | 4 | 3 | 6 | 0 | 6 |
| `NET_saidi_hours` | 0 | 0 | 10 | 6 | 3 |
| `NET_total_system_losses_pct` | 4 | 4 | 4 | 2 | 5 |
| `COM_cash_recovery_index` | 3 | 4 | 2 | 4 | 6 |
| `COM_collection_rate` | 4 | 5 | 4 | 6 | 0 |
| `COM_receivables_days` | 7 | 7 | 0 | 5 | 0 |
| `OPS_customers_per_employee` | 8 | 2 | 1 | 1 | 7 |
| `GOV_annual_reporting_disclosure_score` | 10 | 9 | 0 | 0 | 0 |
| `GOV_audit_opinion_code` | 8 | 4 | 0 | 7 | 0 |
| `GOV_audited_fs_publication_lag_months` | 1 | 12 | 0 | 6 | 0 |
| `GOV_regulatory_framework_score` | 8 | 11 | 0 | 0 | 0 |
| `INV_capex_to_depreciation` | 11 | 3 | 0 | 5 | 0 |
| `ACC_consumption_per_customer` | 7 | 3 | 0 | 3 | 6 |
| `ACC_new_connections` | 4 | 7 | 0 | 2 | 6 |

« Absent des docs lus » ne signifie pas que la donnée n’existe pas : seuls 1 ou 2 documents par utility ont été lus en profondeur.

## Recommandation d’échantillon MVP

Le périmètre doit rester un filtre strict pour les comparaisons. Les groupes proposés :

- **Intégrées** : Senelec (fort), Eskom (fort), ZESCO (utilisable), ENEO/SOCADEL (utilisable). SONABEL (via ARSE) et SNEL (via ARE et la Banque mondiale) peuvent être affichées en mode « valeurs publiées », sans score financier.
- **Distribution** : Kenya Power (fort), EKEDC (fort, avec les données opérationnelles NERC), Ikeja Electric (utilisable via NERC ; comptes audités introuvables), ECG (utilisable via SIGA, l’Energy Commission et le PURC). Pour la Côte d’Ivoire, le **secteur CIE + CI-ENERGIES** doit être traité comme une seule unité d’analyse.
- **Transport** : GRIDCo (fort), KETRACO (utilisable), SONATREL (faible, comptes FY2025 seulement), TCN (faible, comptes jusqu’en FY2020).
- **Production** : KenGen (fort), VRA (faible, via SIGA seulement).
- **Hors MVP pour l’instant** : E2C (Congo). Aucune donnée primaire n’existe en ligne. Elle pourrait figurer sur une page « transparence » avec un score de divulgation proche de zéro, mais il faut d’abord décider si c’est souhaitable (risque politique).

**Conséquence** : un groupe de pairs ne dépasse pas 4 à 6 utilities. Le score « ajusté aux pairs » ne sera statistiquement fragile qu’au MVP (comparaison descriptive plutôt que régression). Pour l’étoffer, il faut ajouter des utilities du même type : DisCos nigérianes via NERC, NEDCo (Ghana), ou d’autres utilities d’Afrique australe et de l’Est.

## Régulateurs et sources secondaires

| Pays | Organisme | Ce qui est publié (selon l’agent) | Consulté |
|---|---|---|---|
| Republic of the Congo | Agence de Régulation du Secteur de l'Electricité (ARSEL) | No public annual report, tariff decision or E2C performance data found online. It was created by law 16-2003. The WB PAD P501343 (2024) describes it as having 'limited capacity and mandates'. Tariffs are unchanged since 1994; tariff principles are set by decree 2017-252. | oui |
| Democratic Republic of the Congo | Autorité de Régulation du secteur de l'Electricité (ARE) | Annual reports for 2020 (published Mar 2021), 2021 (Jan/Feb 2023), 2022 (May 2023), 2023 (Jul 2024), 2024 (Mar/Apr 2025) and 2025 (announced 20 Aug 2026). They contain national production by year (12,460 GWh in 2020 to 13,625 GWh in 2024) and billed customers by voltage for 2020-2024 across all operators. They also publish tariff arrêtés (2018 arrêtés 009/013; 'Arrêté interministériel tarifs SNEL 2022', uploaded Aug 2026), tariff modelling directives, an 'Avis sur les tarifs' section and a 'Rapports des opérateurs' page, which only holds the Virunga Energies 2023 report. | oui |
| Cameroon | Agence de Régulation du Secteur de l'Electricité (ARSEL) | Annual activity reports listed at /index.php/rapports-annuels/: 2008, 2010-2021 and 2023-2025. No 2022 report in the listing. The 2025 report (181 pp, text, created Sep 2026) and the 2024 report (161 pp, text) were fetched. They cover ENEO financial analysis (2024 FS), national SAIDI/SAIFI, connections, customer counts, tariff compensation, SONATREL RMA, transported energy and transmission efficiency. Tariff decisions at /decision-tarifaire/ cover ENEO tariff compensation (2016-2019, 2021, 2022, FY2023 dated 14 Feb 2025), ENEO RMA (2022, FY2024 and FY2025 both dated 19 Dec 2025, provisional 2024 and 2025), tariff conditions 2021-2025, MT tariff tables 2023-2025, and SONATREL transport grids/RMA 2019-2025. Most decision PDFs are scanned images. | oui |
| Côte d'Ivoire | ANARE-CI (Autorité Nationale de Régulation du secteur de l'Electricité de Côte d'Ivoire) | Activity reports listed for 2019, 2020 (+résumé), 2021 (+résumé), 2022 (+résumé), 2023 (+résumé) and 2024, on the 'rapports-dactivites' download category. Also has 'Décisions', 'Avis/décisions/recommandations', 'Arrêtés' and laws/decrees sections. No report content was read: the download links (WP Download Manager) redirect to anareciv.sharepoint.com, which asks for a Microsoft sign-in (checked for 2023 and 2024). The 2019 link returned HTML, not a PDF. | oui |
| Senegal | Commission de Régulation du Secteur de l'Energie (CRSE) | Annual reports listed via the site's WordPress media API: 2013, 2014, 2015-16, 2017, 2018, 2019, 2020-2021, 2022-2023, 2024 and 2025 (2025 uploaded June and Sept 2026). Also 426 decisions, including Senelec revenue-cap (RMA) and tariff-compensation decisions, tariff grids (e.g. decision 2025-140 on the 2026 tariff cut), and public-consultation documents. The 2024 report has Senelec RMA 2024, the revenue gap 2020-2024, compensation 2019-2024 and SAIDI standards. | oui |
| Burkina Faso | Autorité de Régulation du Secteur de l'Energie (ARSE) | Rapport d'activités 2024 (PDF, Aug 2025) with SONABEL energy balance, distribution losses, SAIDI/SAIFI 2020-24, fuel subsidy 2020-24, and SONABEL net income, revenue, receivables and cash 2020-24 taken from SONABEL FS. The 2025 activity report was handed over 27 Jul 2026, with no PDF seen. The 2019 report is on ESMAP RISE. Decisions page shows opinions on SONABEL fuel-subsidy thresholds (2017-2019). Retail tariffs appear to be set by Government, with ARSE in an advisory role. | oui |
| Ghana | Public Utilities Regulatory Commission (PURC) | PURC annual reports (2018-2023 listed; 2019, 2020, 2021 as PDF attachments, 2022 and 2023 via news-det pages and docs.purc.com.gh links). Quarterly ECG/NEDCo 'Key Regulatory Indicators' (purchased and distributed GWh, technical and commercial losses, collection ratio, SAIFI/SAIDI/CAIDI, customers, employees), seen for Q4 2023 and Q1 2024. Tariff decision papers (interactive register at attachment74.github.io/TRDP2025), automatic adjustment notices, rate-setting guidelines, Cash Waterfall Mechanism (CWM) validation reports, Ghana Utilities Performance Index (GUPI) abridged reports 2021 and 2022, and a 'Comparative Analysis of DisCos Performance' report. | oui |
| Ghana | Energy Commission (Ghana) | National Energy Statistics, annual editions 2017-2026 downloadable at /index.php/planning/energy-statistics. The 2026 edition (PDF created 31 May 2026) covers 2000-2025: generation by hydro/thermal/RE, imports and exports, transmission losses, distribution utility purchases, sales and losses by ECG/NEDCo/EPC, customer population, reliability indices by DISCO and area, and average tariffs. Also Key Energy Statistics, Energy Outlook, and weekly wholesale market statistics. Direct /files/YYYY-energy-Statistics.pdf URLs work only for 2023; later editions are served through download IDs. | oui |
| Ghana | State Interests and Governance Authority (SIGA) - SOE oversight (not a regulator) | Annual State Ownership Reports. 2024 SOR (FY2024) and 2025 SOR (FY2025, with 5-year abridged audited FS 2021-2025, KPIs, auditor names and compliance table) for ECG, VRA, GRIDCo and NEDCo. Older editions are on the same page. | oui |
| Ghana | Ministry of Finance (MoF) | Budget statements, ESLA reports, and energy-sector shortfall figures (e.g. 2024 USD 2.2bn shortfall, ECG collecting 62% of purchased energy, per press). No dedicated utility-level energy sector report was fetched in this pass. | non |
| Ghana | Ghana Audit Service (Auditor-General) | Auditor-General reports on Public Boards, Corporations and Statutory Institutions (FY2022 report seen in search; 2024 report covered in press). Ghana Audit Service is the statutory auditor of ECG and VRA per SIGA. | non |
| Kenya | Energy and Petroleum Regulatory Authority (EPRA) | Energy & Petroleum Statistics Reports: calendar 2020, 2021, 2022 and Jan-Dec 2023; FY2023/24; FY ended June 2025 (PDF created 29 Sep 2025); and a 2026 report (posted 2026-09). Bi-annual statistics reports for 2024/25 and 2025/26. The FY2025 report has utility-level data: monthly system losses (annual average 23.36% vs allowable), SAIDI/SAIFI/CAIDI against tariff-control-period targets, new connections (395,490) and cumulative customers (10,045,775), off-grid consumption, and PPAs approved. EPRA Annual Reports FY2018/19 to FY2023/24 were all uploaded 2026-08. Tariff decisions and gazette notices were not fetched. | oui |
| Nigeria | Nigerian Electricity Regulatory Commission (NERC) | Quarterly reports with DisCo-level tables: energy offtake, energy accounting and billing efficiency, collection efficiency, ATC&C losses and revenue loss, GenCo invoice vs DRO (FGN subsidy by DisCo), remittances to NBET/MO, metering status by DisCo, meter deployment, complaints, TCN transmission loss factor, system collapses. Quarterlies seen in the 'NERC Reports' category listing: 2017Q3, 2017Q4, 2018Q1, 2018Q2, 2018Q3, 2018Q4, 2019Q1, 2019Q2, 2019Q3, 2019Q4, 2020Q1, 2020Q2, 2020Q4, 2021Q1, 2021Q2, 2021Q3, 2022Q1-Q4, 2023Q1-Q4, 2024Q1-Q4, 2025Q1-Q4, 2026Q1, 2026Q2. 2020Q3 and 2021Q4 were not in the listing. NERC Annual Report & Accounts seen for 2017, 2018, 2020, 2022, 2023, 2024 and 2025 (2019 and 2021 not in the listing). Also published: market competition reports for 2022 and 2023; MYTO and monthly supplementary tariff orders; monthly energy caps by DisCo (2024-2026); factsheets (commercial, operational, metering). Some old licensee financial statements from 2013-2015 are posted (Abuja DisCo, Afam, Ibom, North South). I fetched the 2019Q2 report, the 2025Q4 report and the 2025 Annual Report. The 2025 Annual Report records enforcement against TCN for non-submission of audited FS, and 2025 transfers of state oversight to state electricity regulatory commissions (SERCs). | oui |
| Nigeria | Lagos State Electricity Regulatory Commission (LASERC) | Not checked. Per NERC 2025 Annual Report Table 10, LASERC regulates Lagos, where the DisCos operating are Excel Electricity Distribution Ltd (EKEDC subsidiary) and IE Energy Lagos Ltd (Ikeja Electric subsidiary). Press reports a licensing ceremony on 2 October 2025. | non |
| Zambia | Energy Regulation Board (ERB) | Annual Energy Sector Reports (2015-2023 seen in search listings; the 2025 Energy Sector Report was posted 28/05/2026), statistical bulletins (e.g. statBullet2018.pdf), and the ERB Annual Report with audited FS (2025 report posted 21/04/2026). It approves ZESCO's tariffs, including the 5-year MYT 2023-2027 and the 2024 emergency tariff (per the ZESCO 2023 FS). Its reliability benchmarks (SAIDI ≤27h) are cited in the ZESCO 2025 IR. | oui |
| South Africa | National Energy Regulator of South Africa (NERSA) | Annual reports: 2022/23 fetched from the PMG mirror (204 pages, mentions the MYPD5 determination); 2018/19 and 2019/20 copies are on PMG and ESMAP. It publishes MYPD revenue applications and determinations: MYPD6 for FY2026-FY2028 was published for consultation 23 Sep 2024 and decided Jan 2025 at 12.74% for FY2026, and municipal distributor tariff approvals are made annually. The /annual-reports/ path on nersa.org.za returned 404; the homepage returned 200. | oui |

## Contre-vérification indépendante

32 documents déclarés « ouverts » ont été échantillonnés, et 30 ont été rouverts par un agent indépendant : **26 confirmés, 4 partiellement confirmés, 0 contredits, 0 inaccessibles**. Les écarts concernaient des opinions d’audit mal lues : KETRACO 2022/23 est en réalité **qualifiée**, EKEDC 2023 est non modifiée, et SONATREL 2025 n’a qu’un rapport sur projet d’états financiers. Ils ont été corrigés dans les données. Les deux documents Eskom FY2024 et FY2025 n’ont pas été rouverts.

**Limite connue** : le contrôle de sécurité automatique n’a pas pu relire le travail de l’agent Kenya (délai dépassé). Ses affirmations sur KPLC et KETRACO ont été partiellement recoupées par la contre-vérification, mais pas celles sur KenGen FY2026.

## Faits inattendus signalés par les agents

Ce sont des affirmations des agents, sourcées dans `audit_matrix.json`. Elles n’ont pas toutes été recoupées : à vérifier avant toute publication.

- **congo-rdc** : E2C is legally a transitional 'société de patrimoine' (asset company), a SAU created by decree 2018-295. The predecessor dissolved by law 22-2018 (13 June 2018) was the 'Société Nationale d'Electricité' (SNE), originally the 'Société Nationale d'Energie' (an EPIC created in 1967). As of 2024, E2C was still operating the system on a 'transitionary basis' more than 5 years later.
- **congo-rdc** : Republic of Congo is moving to a private distribution affermage: SENELEC (Senegal) was pre-selected as 'fermier' and a convention was signed in Dec 2024. The process is now suspended pending interministerial review, and the government asked to drop the related DPF prior action (WB Restructuring Paper P501343, Dec 2025). The entity scope of E2C may change within the MVP window.
- **congo-rdc** : E2C's website has a 'Téléchargements' page with no documents. No E2C financial statements for any year were found online.
- **congo-rdc** : WB ISR P173506 (Sep 2026) states that disclosure of SNEL audited financial statements, a commitment in the State-SNEL performance contract, has seen 'no progress'. The WB project will now finance the external auditors.
- **congo-rdc** : Press items labelled SNEL 'rapport annuel 2023' (ACP, Jan 2024) are year-end narrative communiqués, not annual reports with financial statements. SNEL's 2022 financial statements were 'transmitted to authorities' but not published.
- **congo-rdc** : SNEL collection by voltage reportedly deteriorated: the HV collection rate fell from a baseline of 84% (Oct 2024) to 60% (Jun/Sep 2026) per WB ISR.
- **congo-rdc** : The DRC regulator's real domain is are.gouv.cd (not are.cd). Its annual reports give national, all-operator customer counts that are easy to mistake for SNEL figures.
- **congo-rdc** : The WB PAD 2022 says SNEL was 'profitable over 2014-2019' per its annual financial statements, yet those statements 'do not provide a reliable picture' and auditors identified shortcomings.
- **cameroon** : ENEO is no longer Actis-controlled. The State bought Actis's 51% (agreement 19 Nov 2025, CFA 78 bn, paid 10 Feb 2026), and a presidential decree of 4 May 2026 reportedly converted ENEO into the state-owned 'Société Camerounaise d'Electricité' (SOCADEL). This comes from multiple press search results; the decree itself was not fetched.
- **cameroon** : ENEO has never published full audited financial statements with notes on its website in 2019-2024. Only the 2022 Annual Report carries a scanned FS extract, and its Deloitte art.715 report omits the opinion section. The 2023 and 2024 reports contain management accounts only.
- **cameroon** : The ARSEL 2025 report states that ENEO's financial statements were validated despite reservations the regulator sent to ENEO's statutory auditors. It also says the regulator was still awaiting ENEO's certified FY2025 statements.
- **cameroon** : ENEO's tariff compensation is booked as 'Operating Subsidies' in its SYSCOHADA P&L (2022 AR p.48; ARSEL 2025 p.28). This is key for the EBITDA-excluding-transfers KPI.
- **cameroon** : SONATREL's FS are published by the Ministry of Finance budget directorate (dgb.cm), not on its own website, which is unreachable. Its FY2025 receivables are about FCFA 314 bn net, 87% from ENEO, and SONATREL has taken ENEO to court (payment injunction of 22 Jan 2025, opposed by ENEO).
- **cameroon** : ENEO's annual report PDFs from 2020 onward mostly have no text layer: the 2023 report's text is converted to vector outlines and 2020/2024 are image-based. Automated extraction needs rendering and OCR.
- **cameroon** : SAIDI figures are inconsistent across definitions. The 2023 ENEO AR gives 46.14 h excluding scheduled works/force majeure versus 88.24 h 'global including exclusions'. ARSEL reports a national SAIDI of 147.83 h for 2025.
- **cameroon** : ARSEL migrated its site. Older /photo/*.pdf links returned by search engines now return 404, and documents now sit under /wp-content/uploads/2025/12/ and /2026/09/.
- **cameroon** : An automated WebFetch summary misidentified the SONATREL FY2025 PDF as 'CAMWATER 2021'. The document was verified by downloading and extracting it locally.
- **cote-divoire** : The CIE accounting perimeter changed with the new State–CIE concession agreement (2021-2032, signed 1 Oct 2020). CIE turnover went from about 723bn FCFA (2020, with full electricity sales) to about 232bn (2021, remuneration basis). Sector electricity sales (about 1,057bn FCFA in 2025) are now disclosed only in a supplementary 'Ventes d'énergie' table, and sector assets/liabilities sit in a 'gérés pour le compte de l'Autorité Concédante' memorandum balance sheet (about 1,470bn FCFA in 2025). A naive revenue time series breaks in 2021.
- **cote-divoire** : CIE is majority private (Eranove 54%, State 15%, float 26%, staff 5%), not a state utility. The state-owned counterpart CI-ENERGIES carries sector investments, IPP and gas purchases and debt, so neither entity alone is a full 'utility'.
- **cote-divoire** : CIE's sustainability ('Rapport DD') reports, which serve as its annual reports since 2018, are hosted on the parent Eranove's site, not cie.ci. The latest CIE-level one found is 2023; nothing for 2024 or 2025.
- **cote-divoire** : BRVM extracts state that the FS are 'certifiés' but never include the auditor's report, so the audit opinion type cannot be coded from public filings. The auditors (Ernst & Young, Forvis Mazars) are named only in the semi-annual limited-review attestations.
- **cote-divoire** : ANARE-CI activity reports are listed publicly for 2019-2024, but downloads redirect to a SharePoint tenant that requires sign-in, so they are effectively not machine-accessible.
- **cote-divoire** : The CI-ENERGIES 2022 management report shows sector stress: IPP and gas arrears of 231bn FCFA (about 4.2 months of invoices) at end-2022, EDM (Mali) export arrears of 78bn, a ~40bn State subsidy for the HVO surcharge, and a sector operating deficit of -54.7bn FCFA in 2022.
- **cote-divoire** : Two different interruption metrics are reported for 2022: TMC 28.93 h and SAIDI 19.60 h (CI-ENERGIES p.37), so SAIDI definitions must be harmonised.
- **senegal-burkina** : Senelec's annual reports reproduce the full statutory auditors' report only for FY2021 and FY2022; both are QUALIFIED. The qualification is that grid and generation assets legally transferred to the State (law 2002-01, confirmed by the 2021 Electricity Code) are still carried as Senelec's own assets. FY2023 and FY2024 reports omit the audit report.
- **senegal-burkina** : Senelec's 'Achats Energie' line changes scope across years: about 90-180 bn FCFA in AR2019-2021 versus 542.92 bn in AR2024, which is explicitly described as including IPP fuels and fixed premiums. A naive time series of power purchase cost would be inconsistent.
- **senegal-burkina** : Senelec's State tariff compensation is booked inside revenue (chiffre d'affaires) as 'Ecart sur RMA'. It ranges from about 61 bn (2020) to 333 bn FCFA (2022), so headline revenue overstates tariff revenue.
- **senegal-burkina** : Senelec exports grew strongly to NAWEC (Gambia) and imports from EDG (Guinea) started in 2024.
- **senegal-burkina** : Senelec moved into structured finance in 2025: FCTC SENELEC 2025-2030, a 120 bn FCFA green and sustainability-linked securitisation of unpaid receivables (including public-sector arrears) on BRVM. Press also reports a 108 bn FCFA securitisation listed in Luxembourg and a USD 200m hybrid green bond.
- **senegal-burkina** : Senelec's AR2024 was produced in Oct 2025 and AR2023 was uploaded around Apr 2025, a 10-16 month release lag. The search-indexed AR2024 URL is dead (404).
- **senegal-burkina** : The CRSE re-uploaded its whole archive of annual reports in March 2026, so upload dates do not reflect original publication dates.
- **senegal-burkina** : SONABEL's website is unreachable from non-local networks (TLS reset / 503). The ARSE annual report is the only accessible source of SONABEL financials; it shows SAIDI deteriorating sharply in 2024 versus 2023 and a fuel subsidy rising from 14.5 bn (2020) to 75 bn FCFA (2023-2024).
- **ghana** : ECG presented audited financial statements at its 28th AGM (reported 31 July 2026) for the first time since 2018. Even so, no ECG annual report or audited FS PDF was found online, and ecg.com.gh is entirely behind a captcha/bot wall.
- **ghana** : SIGA's 2025 State Ownership Report labels ECG FY2021-FY2025 and VRA FY2021-FY2025 figures as 'Audited' and names Ghana Audit Service as auditor for both. It is the only public source of audited ECG/VRA figures for the MVP years.
- **ghana** : ECG's FY2025 operating revenue fell sharply in the SIGA SOR because the Government grant (direct GoG payments to power producers and fuel suppliers on ECG's behalf, GHS17,035m in FY2024) was not recognised in FY2025. This is a major break in comparability for revenue, EBITDA and transfer-dependency KPIs.
- **ghana** : The VRA website's 'Annual Reports', 'Sustainability Reports' and 'Facts & Figures' pages all return 404. VRA has no publicly available annual report for 2019-2025.
- **ghana** : GRIDCo publishes every annual report from 2009 to 2025 with full audited IFRS statements and unqualified opinions. The FY2025 report was signed on 30 June 2026, down from about 15 months for FY2022.
- **ghana** : GRIDCo's FY2024 auditor's opinion references an 'IAS 29 directive issued by the Institute of Chartered Accountants Ghana', and FY2024 shows a large upward PPE revaluation (PPE rising from about GHS9.3bn to GHS24.3bn), so asset-based ratios need care.
- **ghana** : Energy Commission 2026 National Energy Statistics (Table 3.16) shows identical ECG and NEDCo reliability indices for 2024 and 2025, which looks like a carry-forward or copy error. Its customer population table covers all DISCOs, not ECG alone.
- **ghana** : PURC's 'Collection Ratio' is defined as Total Revenue/Total Sales in its quarterly ECG indicators, and its system SAIDI is quarterly. Annualisation and inclusion rules are not stated.
- **ghana** : Press (Citi Newsroom, Feb 2025) reports a PwC revenue audit finding that ECG under-declared about GH¢5.3bn of 2024 collections into the Cash Waterfall Mechanism. This affects the reliability of collection data from CWM sources.
- **kenya** : The two loss figures differ: KPLC reports FY2025 total system losses of 21.21% (IAR p259-260), while EPRA's FY2025 statistics report gives an annual average of 23.36%. 21.21% is EPRA's June 2025 monthly value. The definition or averaging must be checked before benchmarking.
- **kenya** : The connection counts differ: KPLC reports 401,848 new connections in FY2025, while EPRA reports 395,490.
- **kenya** : The Auditor-General said KPLC's system-generated SAIDI and CAIDI values could not be confirmed (KPLC FY2025 auditor report p12). The headline SAIDI of 113 hours is an annual total, while EPRA publishes monthly SAIDI of about 7-12 hours, so units and period must be harmonised.
- **kenya** : KPLC's FY2025 audit opinion was unmodified with emphasis of matter, and the going-concern material uncertainty from FY2024 does not appear in the FY2025 pages read. Net working capital improved from -74.8bn (2020) to -19.2bn (2025).
- **kenya** : KPLC has no tariff-compensation or operating-subsidy line. Government support runs through the Rural Electrification Scheme (RES): recharged power costs and a GoK RES receivable of about KShs 34.8bn.
- **kenya** : KenGen already published audited FY2025/26 results (PDF created 4 Sep 2026), so FY2026 data is available before the cut-off.
- **kenya** : KETRACO received a QUALIFIED Auditor-General opinion for FY2024, has negative equity, and books about 40% of its revenue as National Government grants.
- **kenya** : The FY2022 and FY2023 file timestamps on kplc.co.ke reflect a June 2024 re-upload, not the original release. The FY2019-FY2021 KPLC annual reports are no longer on the utility site.
- **kenya** : The KenGen and KETRACO reports were audited by the Auditor-General; KenGen's audit was delegated to Deloitte & Touche. In every IAR, the auditor report pages are scanned images, not text.
- **nigeria** : TCN has been unbundled. Under the Electricity Act 2023, NERC moved system operations into the Nigerian Independent System Operator (NISO) in 2024. TCN's FY2019 revenue included System Operator (N10.5bn) and Market Operator (N0.66bn) lines, so TCN revenue series break after 2024.
- **nigeria** : TCN's audited accounts are public only up to FY2020 (FY2018-2020 PDFs); the same URL pattern for 2021-2024 returns 404. The NERC 2025 Annual Report lists an enforcement order against TCN for 'non-submission of audited financial statement, annual uniform system of accounts'.
- **nigeria** : Lagos regulation has moved to the state. LASERC licensed Excel Electricity Distribution Ltd (100% EKEDC) and IE Energy Lagos Ltd (Ikeja Electric) in October 2025. NERC's 2025 report lists these, plus Ogun State entities (Olumo, Agbara), as the DisCos under state regulators. Entity boundaries for EKEDC and Ikeja Electric change from FY2025.
- **nigeria** : EKEDC, an unlisted Plc, posts audited accounts for every year FY2013-FY2024 on its website, but most are scanned images. Only FY2018, FY2019 and FY2024 have a text layer.
- **nigeria** : EKEDC FY2024: cost of sales (N468.0bn) exceeds revenue (N327.1bn). The company reports an operating profit only because of N230.8bn of FGN tariff-shortfall subsidy recognised as other income: since 2024, NBET invoices are issued net of the approved tariff. Treatment of transfers is therefore decisive for EBITDA and cost-recovery KPIs.
- **nigeria** : EKEDC's FY2019 accounts carried a going-concern material uncertainty (KPMG, signed 14 Oct 2021, about 21.5 months after FYE). By FY2023-FY2024 the auditor was PwC, and FY2024 was signed 4 Feb 2026 (about 13 months).
- **nigeria** : The EKEDC FY2024 accounts list four directors resigning and six being appointed on 30 December 2025, which suggests a governance or ownership change after year-end.
- **nigeria** : Ikeja Electric's website was unreachable (TCP reset/503), and the only public copy of its accounts found (FY2020, ESMAP RISE library) is behind a 403. Searches for 'Ikeja ... financial statements' mostly return Ikeja Hotel Plc, an unrelated NGX issuer.
- **nigeria** : No bond or commercial-paper issuance by Ikeja Electric or EKEDC was found. The FMDQ search returned only NBET Finance bonds.
- **zambia-southafrica** : Eskom has already published FY2026 results (FYE 31 Mar 2026; AFS approved 30 Aug 2026 and published 31 Aug 2026), earlier than in any prior year. FY2025 was published 30 Sep 2025, while FY2022 and FY2024 slipped to December.
- **zambia-southafrica** : Eskom has received a qualified audit opinion every year from FY2019 to FY2026, mainly over PFMA disclosures (irregular expenditure, losses due to criminal conduct), with a going-concern material uncertainty paragraph in FY2019 and FY2022-FY2026.
- **zambia-southafrica** : Eskom is being unbundled: the National Transmission Company South Africa (NTCSA) became operational as a separate subsidiary. The company-level AFS now show 'net internal energy costs' from NTCSA (note 34), so group and company figures diverge from FY2025.
- **zambia-southafrica** : Eskom's FY2025 profit before tax of R23.9bn was its first since 2017, and loadshedding fell to 13 days, against 329 in FY2024.
- **zambia-southafrica** : ZESCO's audit opinion improved from a disclaimer (FY2020, Deloitte) to qualified (FY2021-2022) and then unmodified with a going-concern material uncertainty (FY2023-2025, Grant Thornton). Deloitte resigned at the end of FY2021.
- **zambia-southafrica** : ZESCO published its FY2025 integrated report with full audited FS by about March 2026 (PDF created 30 Mar 2026). This is much faster than FY2022 (FS signed 4 Mar 2024) and FY2023 (signed 23 Dec 2024).
- **zambia-southafrica** : The FS sections of ZESCO's 2023 and 2025 integrated reports are scanned images with no text layer and need OCR, while the 2024 report is fully text-based.
- **zambia-southafrica** : ZESCO's reported annual-average headcount rose 54%, from 6,707 (2024) to 10,319 (2025), and the customer-per-employee ratio fell from 202 to 139. This may be a scope or definition change.
- **zambia-southafrica** : ZESCO's billing and collection figures (K6.79bn billed, 90% collected in 2025) cover only distribution/retail. Group revenue is K32.7bn, mostly mining and export customers who have been migrated to Power Supply Agreements.

## Détail par utility

### Energie Electrique du Congo (E2C) (Republic of the Congo)

- **Nom légal confirmé** : Energie Electrique du Congo (E2C), société anonyme unipersonnelle avec Conseil d'Administration (E2C SAU). It was created by decree n°2018-295 of 7 Aug 2018 as a 'société de patrimoine' after law n°22-2018 of 13 June 2018 dissolved the Société Nationale d'Electricité (SNE). Source: e2c.cg/a-propos (fetched), confirmed by the World Bank PAD P501343 (2024).
- **Actionnariat** : 100% state-owned SAU under the Ministry of Energy and Hydraulics (e2c.cg/a-propos; WB PAD P501343). Gas plants CEC and Aksa (50 MW) have private participation. A private distribution 'affermage' is planned: SENELEC was pre-selected and a convention was signed in Dec 2024, but it is suspended pending interministerial review (WB Restructuring Paper, Dec 2025).
- **Cadre comptable** : XAF. The framework is presumably SYSCOHADA (OHADA member), but no financial statements were seen, so this is unconfirmed. · clôture : Presumably 31 December (calendar year). Not confirmed from any E2C financial statement.
- **Site** : https://e2c.cg (Reachable with curl (HTTP 200) but returns 403 to WebFetch, with intermittent connection resets. The 'Téléchargements' page (https://e2c.cg/telechargements/) is empty: no documents are listed. The only PDFs found on the domain were the company statutes (wp-content/uploads/2022/10/statut-e2c.pdf, search result) and an April magazine (2022/12 upload). The WP REST media listing returned an empty array.)
- **Évaluation** : Not viable from utility sources. E2C publishes no annual report or financial statements online for 2019-2025; its downloads page is empty. The only data path is donor documents (WB PAD, PID and ISRs for P501343), which give single-year headline ratios (losses 42-45%, collection 73%, cost recovery 56%, customers per employee 117, SAIDI baseline) but not their inputs. Governance KPIs can be scored as non-disclosure. Ongoing reform (planned affermage, asset-company status) makes the entity scope unstable.
- **Accès** : e2c.cg returns 403 to WebFetch but loads with curl and a browser user agent, with intermittent connection resets through the proxy. The downloads page is empty. No ARSEL Congo website could be found (arsel.cg did not resolve through the proxy). All useful data comes from World Bank documents, which are text PDFs in English.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | not_found | not_found | not_visible | unknown |  |
| 2020 | not_found | not_found | not_visible | unknown |  |
| 2021 | not_found | not_found | not_visible | unknown |  |
| 2022 | not_found | not_found | not_visible | unknown |  |
| 2023 | not_found | not_found | not_visible | unknown |  |
| 2024 | not_found | not_found | not_visible | unknown |  |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **valeur publiée seule**. WB PAD P501343 (May 2024), p.15 para 10: average tariff of US$0.09/kWh against a cost of service of US$0.16/kWh. No revenue or billed-GWh inputs.
- `FIN_cost_recovery_ratio` : **valeur publiée seule**. WB PAD p.15: tariffs 'recover only 56 percent of the cost-of-service'. No financial statements, so no inputs.
- `FIN_current_ratio` : **absent des docs lus**. No E2C balance sheet found in any source.
- `FIN_ebitda_margin` : **absent des docs lus**. No income statement found.
- `FIN_government_transfer_dependency` : **absent des docs lus**. The PID mentions fuel subsidies (gas for CEC, about 1% of GDP per IMF/WB) but gives no E2C-level transfer data.
- `FIN_power_purchase_payables_days` : **absent des docs lus**. The PAD and PID say E2C has 'significant arrears with CEC' but give no amounts.
- `GEN_avg_power_purchase_cost` : **absent des docs lus**. No purchase cost data.
- `GEN_costly_thermal_share` : **partiel**. WB PAD p.13: 2021 production of 3,159 GWh, 69% from CEC (gas), the rest hydro. Gas is not liquid fuel. One year only, with no breakdown of liquid fuel or emergency power.
- `GEN_purchased_energy_share` : **partiel**. WB PAD p.13: 2021 production of 3,159 GWh with a 69% CEC (IPP-type concession) share. Imports from DRC are 'negligible'. One year only, from a donor document.
- `NET_distribution_losses_pct` : **valeur publiée seule**. WB PAD p.14 para 10: total distribution losses of 42%. WB ISR seq.5 (Jul 2026): baseline 42 (Nov 2023), actual 42.
- `NET_saidi_hours` : **valeur publiée seule**. WB ISR P501343 seq.5 (27 Jul 2026), PDO indicator SAIDI: baseline 2.00 h (Nov 2023), current 2, target 1.40. No definition of inclusion flags.
- `NET_total_system_losses_pct` : **valeur publiée seule**. WB PID (Nov 2023), para 6: 'Total network losses were at 45% in 2022'. No energy balance.
- `COM_cash_recovery_index` : **absent des docs lus**. Only the loss and collection percentages are available, from separate statements.
- `COM_collection_rate` : **valeur publiée seule**. WB PAD p.15: 'bill collection rate stands at a mere 73 percent'.
- `COM_receivables_days` : **absent des docs lus**. No receivables data. The PAD mentions about US$14m of LCDE arrears to E2C (para on the water sector).
- `OPS_customers_per_employee` : **valeur publiée seule**. WB PAD p.14: customers per employee of 117. Customers are 428,657 (Table 1, 2023 E2C data); the employee count is not given.
- `GOV_annual_reporting_disclosure_score` : **calculable**. Can be scored as near-zero: no annual report, financial statements or auditor report is on e2c.cg or anywhere found online (2019-2025).
- `GOV_audit_opinion_code` : **absent des docs lus**. No auditor report found.
- `GOV_audited_fs_publication_lag_months` : **absent des docs lus**. Financial statements are not published, so the lag cannot be determined beyond 'not released'.
- `GOV_regulatory_framework_score` : **partiel**. WB PAD p.15: ARSEL created by law 16-2003; tariff principles decree 2017-252; tariffs unchanged since 1994; ARSEL 'limited capacity and mandates'. No ARSEL website, annual report or tariff decisions were found.
- `INV_capex_to_depreciation` : **absent des docs lus**. No financial statements.
- `ACC_consumption_per_customer` : **absent des docs lus**. 428,657 customers (2023) are given, but billed GWh is not.
- `ACC_new_connections` : **absent des docs lus**. Only project targets (25,000 new customers) are given, not actuals.

</details>

### Société Nationale d'Electricité (SNEL SA) (Democratic Republic of the Congo)

- **Nom légal confirmé** : Société Nationale d'Electricité, SNEL SA (snel.cd homepage and Présentation page, fetched Oct 2026)
- **Actionnariat** : State-owned société anonyme. It is under a performance contract with the State and COPIREP involvement, per WB ISR P173506 (Sep 2026) and PAD (2022). It owns about 90% of national installed capacity (PAD P173506; ARE AR 2024).
- **Cadre comptable** : Unknown from primary sources. CDF with SYSCOHADA (DRC joined OHADA in 2012) is likely, but unconfirmed. WB documents quote SNEL revenue in USD (US$647m in 2020). · clôture : Presumably 31 December (calendar). Not confirmed from financial statements.
- **Site** : https://www.snel.cd (Reachable. It has no publications, annual report or financial statements section. It shows tariff grids (HT/MT/BT in USD/kWh) and an 'indicateurs-2025' page whose content did not render in fetched HTML (probably loaded by JavaScript).)
- **Évaluation** : Weak. SNEL does not publish annual reports or audited financial statements for 2019-2025; the World Bank (Sep 2026) confirms FS disclosure is delayed with no progress. The best data path combines World Bank PAD/ISR values (collection by voltage, losses, revenue 2020, billed customers) with the ARE annual reports (2020-2025, sector-level production and billed customers) and AfDB Compact figures. This supports a handful of reported ratios and governance/regulatory scores, but almost no computed financial KPIs.
- **Accès** : snel.cd is reachable but publishes no reports. ESMAP RISE and IFRI PDFs returned 403. are.gouv.cd is reachable, and its WP media API lists the PDFs; the 2024 annual report is 27.8 MB. The are.cd and are-rdc.cd domains were refused by the proxy (the real domain is are.gouv.cd).

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | referenced_only | not_found | not_visible | unknown |  |
| 2020 | referenced_only | not_found | not_visible | unknown |  |
| 2021 | not_found | not_found | not_visible | unknown |  |
| 2022 | not_found | not_found | not_visible | unknown | <https://www.forumdesas.cd/snel-sa-le-bilan-operationnel-2023-marque-par-lengagement-constant-envers-lexpansion-et-lefficacite> |
| 2023 | referenced_only | not_found | not_visible | unknown | <https://acp.cd/economie/energie-des-perspectives-prometteuses-pour-un-projet-industriel-au-service-de-la-clientele/> |
| 2024 | referenced_only | not_found | not_visible | unknown |  |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **valeur publiée seule**. WB PAD P173506 (2022), Table 1: average household tariff of US¢9/kWh. snel.cd lists HV reference tariffs by zone (USD/kWh). No billed GWh paired with revenue.
- `FIN_cost_recovery_ratio` : **absent des docs lus**. The PAD says tariffs are 'below cost recovery' and SNEL was 'profitable 2014-2019' per its financial statements, but no P&L lines were seen.
- `FIN_current_ratio` : **absent des docs lus**. No balance sheet seen. Government arrears of about US$110m (Mar 2020) are given in PAD Table 1.
- `FIN_ebitda_margin` : **absent des docs lus**. No income statement seen.
- `FIN_government_transfer_dependency` : **absent des docs lus**. No transfer or subsidy data seen.
- `FIN_power_purchase_payables_days` : **absent des docs lus**. Only CEC arrears figures from press (US$32.6m to US$4.3m) are available. The ISR notes no action on arrears for energy purchases.
- `GEN_avg_power_purchase_cost` : **absent des docs lus**. No purchase data seen.
- `GEN_costly_thermal_share` : **absent des docs lus**. The ARE AR 2024 gives the national production mix (about 99% renewable/hydro), but it is not SNEL-specific.
- `GEN_purchased_energy_share` : **absent des docs lus**. No SNEL energy balance seen.
- `NET_distribution_losses_pct` : **valeur publiée seule**. WB PAD P173506: 'about 40 percent in 2019' (para 10). Para 85: 57% of energy delivered to distribution was collected in 2019-2020, i.e. 43% commercial plus technical losses.
- `NET_saidi_hours` : **absent des docs lus**. No SAIDI found.
- `NET_total_system_losses_pct` : **valeur publiée seule**. Bankable.africa (Feb 2025, citing AfDB): technical plus non-technical losses estimated at 46% in 2022. This is a secondary source.
- `COM_cash_recovery_index` : **valeur publiée seule**. PAD para 85: 57% of energy delivered to distribution was collected (2019-2020). This is effectively a cash-recovery-type ratio, given without inputs.
- `COM_collection_rate` : **valeur publiée seule**. WB ISR P173506 (Sep 2026): SNEL bill collection rate 60% (Jun/Sep 2026); HV 84%→60%, MV 65%, LV 40% (baselines Sep/Oct 2024). PAD 2022: LV 51%. AfDB via Bankable: 61% in 2022.
- `COM_receivables_days` : **absent des docs lus**. No receivables balances seen.
- `OPS_customers_per_employee` : **partiel**. Billed customers: PAD Table 1 gives 778,171 (national utility). The ARE AR 2024 'Clients facturés' table covers all operators nationally (799,221 in 2020 to 1,075,511 in 2024), not SNEL alone. No employee count seen (press mentions 688 promotions only).
- `GOV_annual_reporting_disclosure_score` : **calculable**. Can be scored low: no annual report or financial statements published 2019-2025 on snel.cd or elsewhere found. WB ISR (Sep 2026) confirms audited financial statements are not disclosed.
- `GOV_audit_opinion_code` : **absent des docs lus**. PAD P173506 para 85 mentions 'shortcomings identified by the auditors' (2014-2019), suggesting a modified opinion, but no auditor report was seen.
- `GOV_audited_fs_publication_lag_months` : **absent des docs lus**. Financial statements are never publicly released (WB ISR Sep 2026).
- `GOV_regulatory_framework_score` : **calculable**. ARE was created by decree 16/013 (2016) under Electricity Law 14/011 (2014, amended by law 18/031). Tariffs are fixed by interministerial arrêté after ARE opinion (ARE AR 2024 §3.3, tariff procedure page). Published items include the 2018 tariff arrêtés 009/013, the 2022 SNEL tariff arrêté and tariff modelling directives (are.gouv.cd media). ARE annual reports exist for 2020-2025.
- `INV_capex_to_depreciation` : **absent des docs lus**. No financial statements.
- `ACC_consumption_per_customer` : **absent des docs lus**. No SNEL billed GWh seen. The 'about 10,000 GWh sold' figure is unverified.
- `ACC_new_connections` : **partiel**. The ARE AR 2024 gives billed customers 2020-2024 (all operators), so a national delta is possible. It is not SNEL-specific.

</details>

### ENEO Cameroon (now SOCADEL) (Cameroon)

- **Nom légal confirmé** : Energy of Cameroon S.A. (ENEO), per the Deloitte statutory auditors' report reproduced in the 2022 Annual Report, p.44. Search results only (CRTV, Cameroon Tribune, Business in Cameroon, Ecomatin; no official text fetched) say a presidential decree of 4 May 2026 turned it into 'Société Camerounaise d'Electricité' (SOCADEL), fully state-owned. The renaming is unconfirmed from a primary source.
- **Actionnariat** : 2019 AR (text, shareholders section): Actis 51%, State of Cameroon 44%, employees 5%. Per search results (Business in Cameroon, Ecofin, Financial Afrik), the State signed on 19 Nov 2025 to buy Actis's 51% for CFA 78 bn and paid on 10 Feb 2026. That gives the State about 95%, with 5% reserved for employees. Some sources call it the sole shareholder after the May 2026 SOCADEL decree. Now state-owned; not listed.
- **Cadre comptable** : XAF (FCFA); SYSCOHADA (OHADA), per the Deloitte report extract in the 2022 AR, p.44 · clôture : 31 December
- **Site** : https://eneocameroon.cm (reachable (eneocameroon.cm/index.php/en/...; annual report PDFs download with HTTP 200))
- **Évaluation** : Usable. ENEO has published an English annual report or review every year from 2019 to 2024 with rich operating KPIs (customers, headcount, connections, SAIDI, distribution efficiency, collections, generation/IPP mix, capex). Statutory SYSCOHADA statements appear only as an un-annotated extract in 2022, and FY2023-2025 audited FS are not public. Energy billed GWh is never published, so losses and collection metrics are reported values only. Best path: ENEO ARs for operations, plus ARSEL annual reports and tariff/compensation decisions for financials, energy balance and the regulator's view of the audited FS. The May 2026 renaming to SOCADEL needs watching for future publications.
- **Accès** : Site reachable, but the 2020, 2021 (mostly), 2023 and 2024 PDFs have no extractable text (images or outlined vectors), so OCR or page rendering is needed. Files are large (18-37 MB). No standalone audited FS with notes is published on the website. The 2022 FS extract is scanned and omits the opinion paragraph.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | found_fetched | summary_or_extract | not_visible | PDF CreationDate 30 Dec 2020 (pdfinfo) | <https://eneocameroon.cm/pdf/Eneo2019Annual_Report.pdf> |
| 2020 | found_fetched | summary_or_extract | not_visible | PDF CreationDate 30 Sep 2021 (pdfinfo) | <https://eneocameroon.cm/pdf/Eneo2020AnnualReport.pdf> |
| 2021 | found_fetched | not_found | not_visible | PDF ModDate 18 Oct 2022 (pdfinfo) | <https://eneocameroon.cm/pdf/2022/Annual_Review2021.pdf> |
| 2022 | found_fetched | summary_or_extract | not_visible | Deloitte art.715 report signed Douala 29 May 2023; AGM 26 June 2023; AR PDF ModDate 25 Oct 2023 | <https://eneocameroon.cm/docs/EneoAnnualReport2022_ENG.pdf> |
| 2023 | found_fetched | not_found | not_visible | PDF ModDate 21 Nov 2024 (pdfinfo) | <https://eneocameroon.cm/media/Eneo%202023%20Annual%20Report.pdf> |
| 2024 | found_fetched | not_found | not_visible | PDF ModDate 23 Dec 2025 (pdfinfo) | <https://eneocameroon.cm/media/2024-2025%20Eneo%20Highlights_compressed%20(1).pdf> |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **partiel**. Revenue: 2022 AR p.48 income statement ('Goods & Services sold'); 2023 AR p.43 management P&L. Energy billed GWh: not in 2022 or 2023 AR. 2023 AR p.43 gives only an average tariff of CFAF 76.6/kWh (reported value). 2019 AR appendix p.41 gives HV & MV energy injected, not billed.
- `FIN_cost_recovery_ratio` : **partiel**. 2022 AR p.48 (SYSCOHADA P&L): turnover, non-core revenue, operating subsidies, purchases, external services, taxes, personnel, D&A, provisions, financial expenses. Bad debt sits inside provisions with no notes. 2023 AR pp.43-45 management P&L: fixed costs, D&A, interests, provisions; bad-debt provision 14.47bn on p.31.
- `FIN_current_ratio` : **partiel**. 2022 AR pp.46-47: total current assets, current liabilities and bank overdrafts. Public-sector receivables are not split on the face of the balance sheet and no notes are published. 2023 AR p.47 text says only that State/council/SOE arrears rose.
- `FIN_ebitda_margin` : **calculable**. 2022 AR p.48: Turnover (goods & services sold + non-core revenue), 'Operating Subsidies' line (tariff compensation recorded as operating subsidy, per ARSEL 2025 report p.28), other incomes, and all opex lines to EBITDA. The 2023 AR (p.43) management P&L mixes tariff compensation into income, so 2023 is only partial.
- `FIN_government_transfer_dependency` : **partiel**. Operating subsidies line on 2022 AR p.48. 2023 AR p.37 shows tariff compensation collections and p.43 'Tariff compensation: budget increase of CFA 29.4bn'. Government-paid fuel/IPP costs on ENEO's behalf are not disclosed.
- `FIN_power_purchase_payables_days` : **partiel**. 2022 AR p.47: 'Suppliers and Account Payable' total only, not split by power-purchase/fuel. 2023 AR p.44 gives fuel and energy purchase costs; the energy purchase line includes transmission charges, per variance text p.44. ARSEL 2025 p.28 gives 2024 supplier payables total.
- `GEN_avg_power_purchase_cost` : **partiel**. 2023 AR p.44 'Energy purchase' cost (includes SONATREL transmission charges). 2023 AR p.27 IPP GWh by producer (Globeleq Kribi & Dibamba, Memve'ele/Mekin/Mbakaou/Lom Pangar, Aggreko/Guider/Scatec). No imports line.
- `GEN_costly_thermal_share` : **partiel**. 2023 AR p.27: ENEO thermal interconnected and remote thermal GWh shown separately. IPP rows mix fuel types (Kribi gas with Dibamba HFO; Aggreko LFO with Scatec solar), so liquid-fuel/emergency IPP energy cannot be isolated.
- `GEN_purchased_energy_share` : **calculable**. 2023 AR p.27 table: ENEO own generation (hydro, thermal) vs IPPs vs total generation, 2022 and 2023. No imports shown, so they are presumed nil.
- `NET_distribution_losses_pct` : **valeur publiée seule**. 2023 AR p.31 'Distribution Efficiency' 75.24% (2022 75.75%) with a 2014-2023 trend chart; 2024 Highlights p.32 gives 73.79%. Definition (billed/injected into distribution) is in 2022 AR text, but no injected or billed GWh are published.
- `NET_saidi_hours` : **valeur publiée seule**. 2023 AR p.29: SAIDI 46.14 h 'excluding scheduled works and force majeure', plus a 'SAIDI global including exclusions' 2014-2023 chart. p.30 has SAIDI by cause (incl. distribution works programme). 2019 AR p.42 splits distribution/generation/load shedding/transmission. Customer-hour inputs not given.
- `NET_total_system_losses_pct` : **partiel**. Total generation incl. IPPs on 2023 AR p.27, but energy billed GWh is not published in the 2022/2023 ARs. The ARSEL reports give transmission energy balance and transport efficiency (94-95%).
- `COM_cash_recovery_index` : **valeur publiée seule**. Only reported percentages: distribution efficiency and overall gross collections 87.6% (2023 AR p.31). Billed and injected GWh and revenue billed are not given.
- `COM_collection_rate` : **valeur publiée seule**. 2023 AR p.31: overall gross collections, private MV/LV and government cash collection. p.37: total collections CFAF 427.3bn by segment, but revenue billed is not stated ('only 87% of total volume billed collected'). 2019 AR p.43 gives collection rate by customer category.
- `COM_receivables_days` : **partiel**. 2022 AR p.46: 'Customers' gross/provision/net and 'Customers and related accounts', plus turnover on p.48. The tariff-compensation receivable is not separated (no notes). 2023 AR p.47 text gives only the increase in the tariff compensation receivable.
- `OPS_customers_per_employee` : **calculable**. 2023 AR p.7 key figures: active customers 2,029,656 and headcount 3,600. 2019 AR pp.41-43 gives customers by voltage and headcount 3,759.
- `GOV_annual_reporting_disclosure_score` : **partiel**. Annual reports published every year 2019-2024; FS extract only in 2022 (no notes); auditor report only partial (2022); operating stats yes; no energy balance in GWh billed; public-sector receivables only in narrative; board composition yes (2023 AR p.15); state transactions narrative only.
- `GOV_audit_opinion_code` : **partiel**. Auditor name visible: Deloitte & Touche Afrique Centrale + co-auditor Onambele Denis Roland (2022 AR p.45). The opinion paragraph is omitted from the extract, so the category and emphasis-of-matter flag are not visible. ARSEL 2025 report p.29 says ENEO's FS were validated despite reservations the regulator raised with the auditors.
- `GOV_audited_fs_publication_lag_months` : **partiel**. FY2022: art.715 report signed 29 May 2023; AR PDF ModDate 25 Oct 2023 (public release proxy). FY2023/FY2024: no FS published; AR PDFs dated Nov 2024 and Dec 2025.
- `GOV_regulatory_framework_score` : **calculable**. ARSEL is a separate regulator. arsel-cm.org/decision-tarifaire/ publishes tariff decisions, ENEO RMA/compensation decisions (2016-2025) and SONATREL transport grids. The 2021-2025 tariff conditions decision exists. Annual activity reports 2018-2021 and 2023-2025 are published.
- `INV_capex_to_depreciation` : **calculable**. 2023 AR p.47: Capex payments (cash out) and total closed capex (cwip to PPE + direct acquisitions). D&A on p.45 (management P&L). 2022 AR p.48: D&A on the income statement.
- `ACC_consumption_per_customer` : **partiel**. Customers on 2023 AR p.7, but energy billed GWh is not published (only prepaid consumption 606 GWh on p.37 / 704 GWh in 2024 Highlights p.32).
- `ACC_new_connections` : **calculable**. 2023 AR p.31: new connections executed 114,345 (2022: 130,297). p.7: active customers. 2019 AR p.42: new connections by region. Note: internal inconsistency, since key figures p.7 say 112,260 connections.

</details>

### SONATREL (Cameroon)

- **Nom légal confirmé** : Société Nationale de Transport de l'Electricité (SONATREL), per the KPMG report and FS cover, FY2025
- **Actionnariat** : State-owned public company, created by decree 2015/454 of 8 Oct 2015 (per search result). Share capital FCFA 10 bn (FS cover). Its FS are published by the Ministry of Finance Direction Générale du Budget (dgb.cm).
- **Cadre comptable** : XAF (FCFA); SYSCOHADA / AUDCIF (FY2025 KPMG report) · clôture : 31 December
- **Site** : https://sonatrel-cmr.cm/ (per search result; sonatrel.cm does not resolve) (down/unreachable (sonatrel-cmr.cm: CONNECT tunnel 502 via proxy; sonatrel.cm: DNS ENOTFOUND))
- **Évaluation** : Weak to usable for financial KPIs. The FY2025 SYSCOHADA FS with full notes, published by the DGB, are high quality and include FY2024 comparatives, but FY2019-2023 statements were not found publicly. Operating data (energy transported, efficiency) comes from ARSEL reports and decisions. Most distribution/commercial KPIs are not applicable. Next step: browse the dgb.cm SOE financial-statement listing directly for prior years.
- **Accès** : Company website sonatrel-cmr.cm is unreachable through the proxy (502) and sonatrel.cm does not resolve. dgb.cm reset the curl connection, but WebFetch retrieved the PDF. Only FY2025 FS found; earlier years not located on dgb.cm by search (the DGB may have a listing page not indexed).

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | not_found | not_found | not_visible | unknown |  |
| 2020 | not_found | not_found | not_visible | unknown |  |
| 2021 | not_found | not_found | not_visible | unknown |  |
| 2022 | not_found | not_found | not_visible | unknown |  |
| 2023 | not_found | not_found | not_visible | unknown |  |
| 2024 | not_found | summary_or_extract | not_visible | unknown | <https://www.dgb.cm/wp-content/uploads/2026/06/ETATS_FINANCIERS_SONATREL_EXERCICE_2025.pdf> |
| 2025 | not_found | full_with_notes | not_visible | KPMG art.715 report signed 22 Jun 2026; PDF ModDate 23 Jun 2026, uploaded under dgb.cm /2026/06/ | <https://www.dgb.cm/wp-content/uploads/2026/06/ETATS_FINANCIERS_SONATREL_EXERCICE_2025.pdf> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **partiel**. FY2025 FS note 21 (chiffre d'affaires). Energy transported GWh is not in the FS but is in ARSEL 2025 report p.26 (7,678 GWh estimate; average transport tariff 4.161 FCFA/kWh reported).
- `FIN_cost_recovery_ratio` : **calculable**. FY2025 P&L and notes 21-29: revenue, purchases, transport, external services, taxes, personnel, D&A and provisions (line RL), financial expenses (note 29).
- `FIN_current_ratio` : **calculable**. FY2025 balance sheet plus note 7 (clients, ENEO share) and note 8 (other receivables). Public-sector (ENEO) receivable is identifiable from the KPMG report and note 7.
- `FIN_ebitda_margin` : **calculable**. FY2025 P&L includes 'Subvention d'exploitation' (line TG), revenue and opex lines. Note 15A covers investment subsidies separately.
- `FIN_government_transfer_dependency` : **partiel**. Operating subsidy line (TG) in the P&L; no government-paid costs on behalf.
- `FIN_power_purchase_payables_days` : **non applicable**. Transmission-only; no power purchases (note 22 purchases are materials).
- `GEN_avg_power_purchase_cost` : **non applicable**. Transmission-only.
- `GEN_costly_thermal_share` : **non applicable**. Transmission-only.
- `GEN_purchased_energy_share` : **non applicable**. Transmission-only.
- `NET_distribution_losses_pct` : **non applicable**. Transmission-only.
- `NET_saidi_hours` : **absent des docs lus**. Not in FS. 2019 ENEO AR gives a 'SAIDI Transmission' component; ARSEL reports cover transmission availability.
- `NET_total_system_losses_pct` : **non applicable**. System-level losses belong to ENEO/sector. ARSEL 2025 report gives transmission efficiency 95.00% (2024) / 94.60% (2025).
- `COM_cash_recovery_index` : **non applicable**. Transmission-only; single main customer.
- `COM_collection_rate` : **partiel**. KPMG report: ENEO payments in period about FCFA 8 bn against receivables. Revenue in note 21; cash collected not explicitly stated.
- `COM_receivables_days` : **calculable**. Note 7 clients (gross/provisions) and note 21 revenue, FY2025 and FY2024.
- `OPS_customers_per_employee` : **non applicable**. Transmission-only. Employees are available (note 31: 452 average workers).
- `GOV_annual_reporting_disclosure_score` : **partiel**. FS with notes published by DGB for FY2025 only; no annual report or operating statistics found; company website unreachable.
- `GOV_audit_opinion_code` : **partiel**. KPMG art.715 report pp.3-6: intends to issue an unqualified opinion with an observation on note 7. The final opinion report was not seen. Auditor: KPMG Afrique Centrale.
- `GOV_audited_fs_publication_lag_months` : **partiel**. FYE 31 Dec 2025; art.715 report signed 22 Jun 2026; DGB PDF ModDate 23 Jun 2026.
- `GOV_regulatory_framework_score` : **calculable**. ARSEL publishes SONATREL transport tariff grids and RMA decisions 2019-2025 (arsel-cm.org/decision-tarifaire/).
- `INV_capex_to_depreciation` : **calculable**. Note 3A gross fixed assets with an 'Acquisitions' column; note 3C depreciation; P&L line RL.
- `ACC_consumption_per_customer` : **non applicable**. Transmission-only.
- `ACC_new_connections` : **non applicable**. Transmission-only.

</details>

### CIE (Compagnie Ivoirienne d'Electricité) (Côte d'Ivoire)

- **Nom légal confirmé** : Compagnie Ivoirienne d'Electricité (C.I.E.), Société Anonyme avec conseil d'administration, capital 14,000,000,000 FCFA, RCCM CI-ABJ-1990 B-149296 (header of the FY2025 BRVM FS filing)
- **Actionnariat** : Listed on BRVM since 1992 (30% float). Eranove 54%, State of Côte d'Ivoire 15%, other holders 26%, staff FCP 5% (CIE Rapport DD 2023, p.~7). Private concessionaire (operator/affermage) of the national power system under the State–CIE concession agreement 2021-2032, signed 1 Oct 2020. It runs distribution, transmission operation, retail and some state-owned generation (hydro plus Vridi thermal) for the State.
- **Cadre comptable** : XOF/FCFA (MFCFA); SYSCOHADA (separate) plus IFRS (separate and consolidated) published since about 2020; French · clôture : 31 December
- **Site** : https://www.cie.ci (down/unreachable during audit (WebFetch HTTP 503; curl connection reset). Filings came from BRVM and the Eranove parent site.)
- **Évaluation** : Usable but structurally special. CIE is a private, listed concessionaire whose own P&L since 2021 shows only its remuneration. Sector sales (MFCFA and GWh), customers and connections are in an annual table inside its BRVM FS, published every year 2019-2025 with a lag of about 4-5 months. Operating KPIs (losses, TMC/SAIDI, staff) are only reported values, in the Eranove-hosted DD reports through 2023. The best path is to combine the CIE BRVM filings with the CI-ENERGIES sector account and treat the power sector (CIE plus CI-ENERGIES) as the benchmarking unit.
- **Accès** : cie.ci unreachable (503 or connection reset). BRVM PDFs are open; several versions are scanned images with no text layer (FY2019 v1, FY2021 2022-06-03, FY2022 synthèse, FY2023 2024-06-06). BRVM extracts are 1-3 page summaries without notes or the auditor's report. DD reports are 30-40 MB but text-based.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | found_fetched | summary_or_extract | not_visible (the BRVM extract says 'Etats financiers certifiés par les Commissaires aux comptes', but the auditor's report is not included) | 2020-06-12 (BRVM listing date for the certified FS); a first version was posted 2020-05-19 | <https://www.brvm.org/sites/default/files/20200612_-_etats_financiers_certifies_-_exercice_2019_-_cie_ci.pdf> |
| 2020 | found_fetched | summary_or_extract | not_visible | 2021-06-04 (BRVM listing date) | <https://www.brvm.org/sites/default/files/20210604_-_etats_financiers_exercice_2020_-_cie_ci.pdf> |
| 2021 | found_fetched | summary_or_extract | not_visible | 2022-04-29 (BRVM listing of the SYSCOHADA and IFRS FS); another version was posted 2022-06-03 | <https://www.brvm.org/sites/default/files/20220429_-_etats_financiers_syscohada_exercice_2021_-_cie.pdf> |
| 2022 | found_fetched | summary_or_extract | not_visible | 2023-04-27 (BRVM listing date) | <https://www.brvm.org/sites/default/files/20230427_-_etats_financiers_syscohada_exercice_2022_-_cie_ci.pdf> |
| 2023 | found_fetched | summary_or_extract | not_visible | 2024-05-02 (BRVM listing of the SYSCOHADA FS); a second version was posted 2024-06-06 | <https://www.brvm.org/sites/default/files/20240502_-_etats_financiers_syscohada_-_exercice_2023_-_cie_ci.pdf> |
| 2024 | not_found | summary_or_extract | not_visible | 2025-04-30 (BRVM listing date) | <https://www.brvm.org/sites/default/files/20250430_-_etats_financiers_-_norme_syscohada_-_exercice_2024_-_cie_ci.pdf> |
| 2025 | not_found | summary_or_extract | not_visible | 2026-05-20 (BRVM listing date; PDF CreationDate 2026-05-20) | <https://www.brvm.org/sites/default/files/20260520_-_etats_financiers_syscohada_et_ifrs_-_exercice_2025_-_cie_ci.pdf> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **calculable**. FY2025 BRVM FS p.2, 'Evolution des ventes d'énergie': national and export energy sales in MFCFA plus national and export GWh, 2025 and 2024. These are SECTOR revenues collected for the State, not CIE's own revenue. The same table is in the FY2023 and FY2024 filings.
- `FIN_cost_recovery_ratio` : **partiel**. FY2025 SYSCOHADA P&L p.1 gives CIE's own revenue (services 261.9bn plus accessory 40.4bn), opex lines, 'Dotations aux amortissements, provisions' (combined) and finance costs. Bad debt is not separated. At sector level, costs (fuel, IPP, debt) are not in CIE's documents; they are in CI-ENERGIES' sector operating account.
- `FIN_current_ratio` : **partiel**. FY2025 IFRS consolidated balance sheet p.3 gives total current assets and liabilities. SYSCOHADA gives 'Créances et emplois assimilés' and 'Passif circulant'. Public-sector receivables are not separated.
- `FIN_ebitda_margin` : **partiel**. FY2025 SYSCOHADA P&L reports EBE (Excédent brut d'exploitation) and a 'Subvention d'exploitation' line (0). This is computable for CIE as concessionaire, but its revenue is remuneration, not electricity sales, so it does not measure the power sector.
- `FIN_government_transfer_dependency` : **absent des docs lus**. Not in CIE filings: the operating subsidy line is 0, and tariff compensation and state fuel payments sit at sector level. The CI-ENERGIES 2022 management report shows the State subsidy of 39.8bn in the sector account.
- `FIN_power_purchase_payables_days` : **absent des docs lus**. CIE does not buy IPP power on its own account. IPP and gas arrears are in the CI-ENERGIES Rapport de gestion 2022, p.77.
- `GEN_avg_power_purchase_cost` : **absent des docs lus**. No IPP purchase GWh or cost in the CIE FS or DD 2023.
- `GEN_costly_thermal_share` : **partiel**. DD 2023 annex p.88 gives CIE-operated thermal and hydro production (GWh), fuel volumes (gas, HVO, DDO, diesel) and ENV550 energy available. There is no IPP fuel-type or emergency-rental GWh split.
- `GEN_purchased_energy_share` : **partiel**. DD 2023 p.88 gives CIE-operated production (1,989 GWh in 2023) and energy available. Purchased IPP GWh and imports are not in CIE docs.
- `NET_distribution_losses_pct` : **valeur publiée seule**. DD 2023 p.48 reports 'rendement distribution' (2022 and 2023 %) and annex SOT241 'ratio de facturation'. No injected-energy GWh.
- `NET_saidi_hours` : **valeur publiée seule**. DD 2023 annex p.92, SOT201 'Temps moyen de coupure électricité' (HH:MM, 2021-2023). Definition and inclusion flags not stated.
- `NET_total_system_losses_pct` : **valeur publiée seule**. DD 2023 p.48 and annex ENV560 'Rendement global' %. Sales GWh are in the FS, but sent-out, import and export balance is not in CIE docs.
- `COM_cash_recovery_index` : **absent des docs lus**. No cash collections or injected energy in the CIE FS or DD 2023.
- `COM_collection_rate` : **absent des docs lus**. DD 2023 mentions 'taux de recouvrement' only qualitatively (e-billing section). No figure seen.
- `COM_receivables_days` : **partiel**. FY2025 IFRS 'Créances clients' (CIE's own). Sector receivables sit in 'Créances et emplois assimilés' of the assets managed for the concession authority, with no electricity or public-sector breakdown.
- `OPS_customers_per_employee` : **calculable**. FY2025 FS p.2 gives 'Nombre de clients'. DD 2023 p.32 gives staff (CDI 4,802, CDD 755, 2021-2023), and annex SOT101 gives customers. Employees are not in the FY2024 or FY2025 FS.
- `GOV_annual_reporting_disclosure_score` : **partiel**. FS extracts are published every year on BRVM, but without notes or the auditor's report. The DD reports carry operational, energy and governance data. No annual report or DD report found for 2024 or 2025.
- `GOV_audit_opinion_code` : **partiel**. Auditors are Ernst & Young and Forvis Mazars (H1 2025 attestation; 2018 annual report). The annual audit opinion text is not in the BRVM extracts; the FY2019 extract only states 'certifiés'.
- `GOV_audited_fs_publication_lag_months` : **partiel**. FY-end 31 Dec and BRVM posting dates are known (e.g. FY2025 on 2026-05-20, FY2024 on 2025-04-30). The audit report signing date was not seen.
- `GOV_regulatory_framework_score` : **partiel**. Country level: ANARE-CI exists and publishes activity reports 2019-2024 and a decisions page (listing seen). Tariff methodology was not read.
- `INV_capex_to_depreciation` : **partiel**. FY2025 SYSCOHADA cash flow gives acquisitions of intangible and tangible assets. Depreciation is combined with provisions in 'Dotations aux amortissements, provisions'. Covers CIE's own capex only; sector capex is by CI-ENERGIES.
- `ACC_consumption_per_customer` : **calculable**. FY2025 FS p.2: national sales GWh and number of customers (also FY2023 and FY2024 filings).
- `ACC_new_connections` : **calculable**. FY2025 FS p.2: 'Branchements BT ordinaires', 'Branchements BT PEPT', 'Raccordements HT' counts and customer totals.

</details>

### CI-ENERGIES (Société des Energies de Côte d'Ivoire) (Côte d'Ivoire)

- **Nom légal confirmé** : CI-ENERGIES (name as printed on the 2023 and 2024 published FS and the 2022 Rapport de gestion; the full legal expansion was not confirmed from a fetched source)
- **Actionnariat** : State-owned. The FY2024 FS were 'Approuvé par l'Actionnaire Unique' on 05 June 2025; capital 20bn FCFA (FY2024 FS balance sheet).
- **Cadre comptable** : XOF/FCFA; SYSCOHADA; French · clôture : 31 December
- **Site** : https://www.cinergies.ci (reachable (www.cinergies.ci; ci-energies.ci did not resolve via proxy))
- **Évaluation** : Usable as the sector-level complement to CIE. The 2022 Rapport de gestion is very rich: sector energy balance, SAIDI/SAIFI, the sector operating and cash accounts with State subsidy, IPP volumes, costs and arrears, and export receivables. Only one such report was found for 2019-2025. Own-entity SYSCOHADA FS extracts are public for 2023 and 2024 only, without the audit report. Best path: 2022 report plus Journal Officiel FS, filling other years from CIE BRVM sector tables and ANARE-CI activity reports (if they can be downloaded).
- **Accès** : No publications or annual-reports section on the site; documents were found only through the WordPress media API search. The 'Chiffres clés' page is image-only. ci-energies.ci did not resolve (proxy 502).

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | not_found | not_found | not_visible | unknown |  |
| 2020 | not_found | not_found | not_visible | unknown |  |
| 2021 | referenced_only | summary_or_extract | not_visible | unknown | <https://www.cinergies.ci/wp-content/uploads/2023/07/CI-ENERGIES_Rapport_Gestion_Exercice-2022-_final.pdf> |
| 2022 | found_fetched | summary_or_extract | not_visible | 2023-07-24 (WordPress media upload date and blog post date) | <https://www.cinergies.ci/wp-content/uploads/2023/07/CI-ENERGIES_Rapport_Gestion_Exercice-2022-_final.pdf> |
| 2023 | not_found | summary_or_extract | not_visible | 2024-06-27 (WordPress media upload date) | <https://www.cinergies.ci/wp-content/uploads/2024/06/PUBLICATION-JOURNAL-OFFICIEL-ETATS-FINANCIERS-2023.pdf> |
| 2024 | not_found | summary_or_extract | not_visible | 2025-06-16 (media upload date); FS approved by the sole shareholder on 2025-06-05 | <https://www.cinergies.ci/wp-content/uploads/2025/06/PUBLICATION-JOURNAL-OFFICIEL-ETATS-FINANCIERS-2024.pdf> |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **calculable**. Rapport de gestion 2022: p.75 sector 'Ventes nationales' and 'Ventes export' (MFCFA, 2021-2022); p.37 national sales GWh.
- `FIN_cost_recovery_ratio` : **partiel**. Sector operating account p.75: sales, other income, CIE remuneration, gas, liquid fuel, energy purchases, interest and operating charges. Sector depreciation and bad debt are not shown.
- `FIN_current_ratio` : **partiel**. CI-ENERGIES FY2024 FS balance sheet: actif circulant, passif circulant, trésorerie. No public-sector receivable split.
- `FIN_ebitda_margin` : **partiel**. FY2024 FS P&L has turnover, operating subsidies (TG), opex and EBE. At sector level, p.75 separates the 'Dotation et subvention Etat' line.
- `FIN_government_transfer_dependency` : **partiel**. p.75 'Dotation et subvention Etat' (3.9bn in 2021, 39.8bn in 2022); p.76 says the State's ~40bn covered the HVO surcharge. FY2023-2024 FS show operating subsidies. Govt-paid fuel on behalf is partly visible as the gas 'part Etat' on p.75.
- `FIN_power_purchase_payables_days` : **calculable**. p.77: monthly arrears by IPP and gas supplier in MFCFA, also expressed as months of invoices. p.75 gives purchase costs.
- `GEN_avg_power_purchase_cost` : **partiel**. Section 'Achat d'énergie aux PIE': 8,705 GWh bought from IPPs for 188.8bn FCFA in 2022; Soubré 1,356.8 GWh for 47.5bn. Import GWh are on p.37 but the import cost was not seen.
- `GEN_costly_thermal_share` : **partiel**. p.37 hydro vs thermal production GWh; liquid-fuel purchase cost on p.75. No GWh split for liquid fuel or emergency rental (Aggreko, Karpower) seen.
- `GEN_purchased_energy_share` : **calculable**. p.37 gross production and imports GWh; IPP purchases 8,705 GWh (IPP section).
- `NET_distribution_losses_pct` : **valeur publiée seule**. Report text: 'rendement distribution' 91.03% in 2022 vs 89.12% in 2021. Injected energy not given.
- `NET_saidi_hours` : **valeur publiée seule**. p.37 reports SAIDI (hours), SAIFI and TMC for 2021 and 2022. Inclusion flags not stated.
- `NET_total_system_losses_pct` : **calculable**. p.37 gross production, imports, exports, national sales GWh, and reported 'Rendement global'. Production is gross, not sent-out.
- `COM_cash_recovery_index` : **absent des docs lus**. Injected distribution energy not given.
- `COM_collection_rate` : **partiel**. p.76 cash account 'Encaissement vente nationale' and export receipts, against p.75 sales billed. Timing and arrears composition are unclear.
- `COM_receivables_days` : **partiel**. p.78 export receivables by client. National receivables not seen.
- `OPS_customers_per_employee` : **non applicable**. CI-ENERGIES is an asset holder and sector manager; customers are served by CIE. Sector customer counts are on p.37.
- `GOV_annual_reporting_disclosure_score` : **partiel**. Only one management report (2022) and FS extracts for 2023-2024 found. No notes or auditor's report.
- `GOV_audit_opinion_code` : **absent des docs lus**. No auditor's report or auditor name seen. An AMI for auditing project accounts for 2023/2024 exists on the site but was not read.
- `GOV_audited_fs_publication_lag_months` : **partiel**. FY2024 approval date 2025-06-05 and upload date 2025-06-16. The audit signing date was not seen.
- `GOV_regulatory_framework_score` : **partiel**. Country level; see ANARE-CI.
- `INV_capex_to_depreciation` : **calculable**. FY2024 FS cash flow: acquisitions of intangible and tangible assets (e.g. FG); P&L 'Dotations aux amortissements, provisions' (combined with provisions).
- `ACC_consumption_per_customer` : **calculable**. p.37 national sales GWh and number of customers (sector).
- `ACC_new_connections` : **partiel**. p.37 customer counts for 2021 and 2022 (connections derivable as net change). Explicit connection counts are in CIE filings.

</details>

### Senelec (Senegal)

- **Nom légal confirmé** : Société Nationale d'Electricité du Sénégal (SENELEC), as written in the statutory auditors' reports included in the FY2021 and FY2022 annual reports
- **Actionnariat** : State-owned SA. Capital social is 175.24 bn FCFA at 31/12/2024 (AR2024 p.47). The auditors' report is addressed to the shareholders ('Aux Actionnaires'). The shareholder split was not checked.
- **Cadre comptable** : XOF (FCFA); Système Comptable OHADA (SYSCOHADA), audited under ISA by joint auditors KPMG Sénégal and Mazars Sénégal · clôture : 31 December
- **Site** : https://www.senelec.sn (reachable. The /rapports/ page lists annual reports for 2019-2024 and all six PDFs downloaded with HTTP 200. One search-indexed URL under /assets/uploads/media-uploader/ returned 404.)
- **Évaluation** : Strong candidate. Consistent text-PDF annual reports exist for every FY2019-2024, with a rich energy balance, customers, staff, SAIDI, collection data and the tariff compensation line (Ecart sur RMA). The main gap is that full audited statements with notes and the auditor report appear only in AR2021 and AR2022 (both qualified on asset ownership), while AR2023 and AR2024 give summaries only. CRSE publishes RMA and compensation decisions and annual reports. Best path: annual reports plus CRSE reports, and seek the full FS for 2023-2025 (e.g. bond or securitisation documents).
- **Accès** : None significant. All PDFs are text-based French documents of 1-5 MB. A search-indexed URL for AR2024 (/assets/uploads/media-uploader/...) returns 404; the working path is /media/rapports/pdf/... . No bond prospectus was located on BRVM or AMF-UMOA within budget.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | found_fetched | summary_or_extract | not_visible | unknown; PDF CreationDate is 26 Feb 2021 (pdfinfo) | <https://www.senelec.sn/media/rapports/pdf/ras2019.pdf> |
| 2020 | found_fetched | summary_or_extract | not_visible | unknown; PDF CreationDate is 3 Mar 2022, and the filename timestamp shows a re-upload on 4 Sep 2023 | <https://www.senelec.sn/media/rapports/pdf/rapport-annuel-senelec-2020-ok1693835980.pdf> |
| 2021 | found_fetched | summary_or_extract | qualified | unknown; auditor report signed in Dakar on 20 June 2022; PDF CreationDate is 4 Nov 2022 | <https://www.senelec.sn/media/rapports/pdf/ras2021.pdf> |
| 2022 | found_fetched | summary_or_extract | qualified | unknown; auditor report signed in Dakar on 27 June 2023; PDF CreationDate is 14 Aug 2023, uploaded 4 Sep 2023 (filename timestamp) | <https://www.senelec.sn/media/rapports/pdf/rapport-annuel-senelec-2022-compressed1693835195.pdf> |
| 2023 | found_fetched | summary_or_extract | not_visible | unknown; PDF CreationDate is 6 Sep 2024; the filename timestamp suggests upload on 22 Apr 2025 | <https://www.senelec.sn/media/rapports/pdf/rapport-annuel-senelec-2023-vf-ok1745314522.pdf> |
| 2024 | found_fetched | summary_or_extract | not_visible | unknown; PDF CreationDate is 8 Oct 2025; filename timestamp 9 Oct 2025 | <https://www.senelec.sn/media/rapports/pdf/rapport-annuel-senelec-20241760024319_1.pdf> |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **calculable**. AR2024 pp.19 and 40-41: energy sales revenue excluding the tariff-freeze subsidy by voltage, and GWh billed by voltage. An average price is also reported.
- `FIN_cost_recovery_ratio` : **partiel**. AR2024 pp.44-47: product table (Ventes de produits finis, Ecart sur RMA, Travaux & services, Produits accessoires), current charges (raw materials, Achats Energie, Charges financières, personnel), and provisions for receivables in the text. Total opex and depreciation are not tabulated: EBE and résultat d'exploitation are given, so D&A is only derivable indirectly. AR2022 has account-level D&A.
- `FIN_current_ratio` : **partiel**. AR2024 p.47: Actifs Circulants, Passifs Circulants, Trésorerie actif/passif. Public-sector receivables gross come from the commercial receivables table (Administration) on p.43, which is a commercial basis, not the accounting basis.
- `FIN_ebitda_margin` : **calculable**. AR2024 p.45: EBE is reported, and products are split into energy sales and 'Ecart sur RMA' (the tariff compensation). EBITDA excluding transfers can be derived. Operating subsidies are visible only in the AR2022 account detail.
- `FIN_government_transfer_dependency` : **partiel**. 'Ecart sur RMA' (the State tariff compensation) appears every year 2019-2024 in the product tables. Operating subsidies appear in AR2022 detail. Government-paid fuel or IPP costs were not seen.
- `FIN_power_purchase_payables_days` : **partiel**. AR2022 detailed passif has 'Fournisseurs d'exploitation' (not split by power purchase or fuel). AR2024 text mentions the rise in operating supplier debt. Purchase costs are available.
- `GEN_avg_power_purchase_cost` : **calculable**. AR2024 p.46: 'Achats Energie' (described as purchases of energy, IPP fuels and fixed premiums). Pp.18-19 give purchased GWh by IPP, OMVS hydro and EDG imports. Caution: in AR2019-2021, 'Achats Energie' appears to have a narrower scope.
- `GEN_costly_thermal_share` : **partiel**. AR2024 pp.18-19: purchases by named IPP (Kounoune, ContourGlobal, Tobène, Malicounda, KPS powership, etc.) and own production by network. The fuel type per IPP and Senelec's own generation by fuel must be mapped. Fuel tonnages are on pp.30-32.
- `GEN_purchased_energy_share` : **calculable**. AR2024 pp.18-19: own production, total energy purchases, and total energy available.
- `NET_distribution_losses_pct` : **partiel**. Only 'Rendement brut' (overall efficiency) and a production-transport efficiency figure are given (AR2024 pp.19, 37, 42). Energy injected into distribution is not tabulated, so distribution losses must be derived.
- `NET_saidi_hours` : **valeur publiée seule**. AR2024 p.19 and the reliability section: SAIDI and SAIFI for 2022-2024. Inclusion of load shedding and planned outages is not explicit. The CRSE 2024 report has a SAIDI standard table.
- `NET_total_system_losses_pct` : **calculable**. AR2024 p.19: total energy available, energy sales (including exports), and rendement brut reported.
- `COM_cash_recovery_index` : **partiel**. Collection data is computable (p.42), but energy injected into distribution is missing.
- `COM_collection_rate` : **calculable**. AR2024 p.42: collection table with CAE brut and encaissements by management centre, plus a reported coverage rate.
- `COM_receivables_days` : **partiel**. AR2024 p.47: net customer receivables (créances nettes clients) and other receivables. P.43 gives commercial receivables by Particuliers/Administration/Ambassades. The tariff-compensation receivable ('ETAT, ECART SUR RMA A RECEVOIR') is visible only in the AR2022 detail.
- `OPS_customers_per_employee` : **calculable**. AR2024 pp.19, 40 and 48: customers by voltage and permanent staff (3,435).
- `GOV_annual_reporting_disclosure_score` : **partiel**. Annual reports 2019-2024 are published, with operational statistics, energy balance and receivables by category. Full audited statements with notes are not reproduced. The auditor report is included only in AR2021 and AR2022. Management and auditors are listed; board composition was not checked.
- `GOV_audit_opinion_code` : **partiel**. FY2021 and FY2022: qualified opinion (asset ownership), auditors KPMG Sénégal and Mazars Sénégal. FY2019, 2020, 2023 and 2024: opinion not visible.
- `GOV_audited_fs_publication_lag_months` : **partiel**. Audit signing dates: 20/06/2022 (FY21) and 27/06/2023 (FY22). Public release dates are only proxied by PDF metadata and filename timestamps.
- `GOV_regulatory_framework_score` : **calculable**. CRSE is a separate regulator. Its 2024 annual report (fetched) covers RMA/revenue-cap decisions, tariff compensation, quality-of-service standards (SAIDI) and public consultation documents. 426 decisions are published on crse.sn.
- `INV_capex_to_depreciation` : **partiel**. AR2022 detailed fixed-asset accounts allow additions to be inferred, and depreciation is given. AR2023/2024 give only the change in actif immobilisé. No cash-flow statement was seen.
- `ACC_consumption_per_customer` : **calculable**. AR2024 pp.19 and 40: GWh billed and customers by voltage.
- `ACC_new_connections` : **partiel**. Only the net increase in customers is given (+211,807 in 2024, p.40). A count of new connections (branchements) was not seen.

</details>

### SONABEL (Burkina Faso)

- **Nom légal confirmé** : Société Nationale d'Electricité du Burkina (SONABEL), as written on the cover of the World Bank-hosted PER-DN project audit report for FY2023 (fetched)
- **Actionnariat** : State-owned enterprise (société d'État). It is covered in the annual assemblée générale of Burkina sociétés d'État per Sidwaya press (search result, not fetched). Exact legal form was not confirmed from a fetched source.
- **Cadre comptable** : XOF (FCFA); SYSCOHADA presumed; not confirmed from SONABEL's own FS · clôture : 31 December (presumed; the ARSE report cites 'Etats financiers 2024 de la SONABEL' on a calendar-year basis)
- **Site** : https://www.sonabel.bf (blocked or unavailable from the audit environment. curl got a TLS 'connection reset by peer' after the proxy CONNECT succeeded, and WebFetch returned HTTP 503 for the home page, /nos-rapports/ and /nos-chiffres-cles/. A Wayback snapshot of /nos-rapports/ exists (16 Jul 2025) but web.archive.org could not be fetched.)
- **Évaluation** : Weak at present. SONABEL appears to publish activity reports (2014-2022 per the site listing), but none could be opened, and no audited FS or auditor opinion is public in sources reached. The best accessible data path is the ARSE annual activity report, which has energy balance, SAIDI, losses %, subsidy, revenue, net income, receivables and cash for 2020-2024, sourced from SONABEL's FS. This supports a handful of KPIs but not the financial core. Viability could rise to 'usable' if sonabel.bf reports are retrieved manually.
- **Accès** : sonabel.bf is unreachable from this environment (TLS connection reset, 503 via WebFetch), possibly due to geo-blocking or a firewall. The ESMAP RISE mirror returns 403. web.archive.org is not fetchable here. No SONABEL report could be opened. Recommended next step: retry sonabel.bf/nos-rapports/ from a browser or an African IP, or obtain the PDFs from the Wayback snapshot of 16 Jul 2025.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | referenced_only | not_found | not_visible | unknown | <https://www.sonabel.bf/nos-rapports/> |
| 2020 | found_link_not_fetched | not_found | not_visible | unknown | <https://rise.esmap.org/data/files/library/burkina-faso/Electricity Access/Burkina Faso_SONABEL_s activity report_2020.pdf> |
| 2021 | referenced_only | not_found | not_visible | unknown | <https://www.sonabel.bf/nos-rapports/> |
| 2022 | referenced_only | not_found | not_visible | unknown | <https://www.sonabel.bf/nos-rapports/> |
| 2023 | not_found | not_found | not_visible | unknown |  |
| 2024 | not_found | not_found | not_visible | unknown |  |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **absent des docs lus**. The ARSE 2024 report (p.49) gives total revenue but no GWh billed for SONABEL; no SONABEL report was read.
- `FIN_cost_recovery_ratio` : **absent des docs lus**. Only revenue and net income in ARSE 2024 p.49; the ARSE text gives cost of service per kWh with and without subsidy for 2022.
- `FIN_current_ratio` : **absent des docs lus**. Only cash (trésorerie) in ARSE 2024 p.50 table 24.
- `FIN_ebitda_margin` : **absent des docs lus**. No opex or EBE seen in documents read; EBE is mentioned only in press.
- `FIN_government_transfer_dependency` : **partiel**. ARSE 2024 table 21 (p.48): State fuel subsidy or compensation to SONABEL for 2020-2024, plus revenue for 2020-2024 (table 23).
- `FIN_power_purchase_payables_days` : **absent des docs lus**. No payables seen.
- `GEN_avg_power_purchase_cost` : **absent des docs lus**. ARSE 2024 has import volumes by interconnector but no purchase cost.
- `GEN_costly_thermal_share` : **partiel**. ARSE 2024 pp.42-43: SONABEL production and private thermal/solar production by plant, and imports (HTB/HTA from Côte d'Ivoire, Ghana and Togo). Fuel split of SONABEL's own thermal output was not confirmed.
- `GEN_purchased_energy_share` : **calculable**. ARSE 2024 p.43 table: total SONABEL production, national production including IPPs, total imports, and total produced plus imported, for 2023-2024.
- `NET_distribution_losses_pct` : **valeur publiée seule**. ARSE 2024 p.43: distribution losses (technical plus non-technical) in % for 2023-2024.
- `NET_saidi_hours` : **valeur publiée seule**. ARSE 2024 table 20 (p.46): SAIDI (hours) and SAIFI for 2020-2024; inclusion flags not stated.
- `NET_total_system_losses_pct` : **partiel**. ARSE 2024 p.43: production-transport efficiency (rendement) and distribution losses %; energy billed not seen.
- `COM_cash_recovery_index` : **absent des docs lus**. No billing or collection data seen.
- `COM_collection_rate` : **absent des docs lus**. The ARSE collection-rate table concerns ARSE's own levy, not SONABEL.
- `COM_receivables_days` : **partiel**. ARSE 2024 table 23 (p.49): SONABEL customer receivables (créances clients) and revenue for 2020-2024; no public-sector split.
- `OPS_customers_per_employee` : **absent des docs lus**. ARSE 2024 p.30 gives only projected subscribers (abonnés) for 2024; no SONABEL headcount seen.
- `GOV_annual_reporting_disclosure_score` : **partiel**. Activity reports exist (2014-2022 per the listing snippet, 2020 copy on RISE) but none could be opened, and no audited FS are public.
- `GOV_audit_opinion_code` : **absent des docs lus**. No entity audit report seen.
- `GOV_audited_fs_publication_lag_months` : **absent des docs lus**. No audited FS publication found.
- `GOV_regulatory_framework_score` : **calculable**. ARSE is a separate regulator with a published 2024 activity report and published opinion-type decisions (fuel subsidy trigger thresholds for SONABEL, 2017-2019). Tariff and fuel prices are validated with the Government; no published tariff methodology was seen.
- `INV_capex_to_depreciation` : **absent des docs lus**. Press (sirainfo) mentions 20.86% execution of the 2022 investment budget; no FS seen.
- `ACC_consumption_per_customer` : **absent des docs lus**. Not in ARSE 2024 for actuals.
- `ACC_new_connections` : **absent des docs lus**. Only a projection (+78,807 net subscribers expected in 2024) in ARSE 2024 p.30.

</details>

### GRIDCo (Ghana Grid Company) (Ghana)

- **Nom légal confirmé** : Ghana Grid Company Limited (auditor's report in 2024 AR addresses 'Ghana Grid Company LTD.')
- **Actionnariat** : State-owned, 100% Government of Ghana (2024 AR going-concern/directors' report: 'The Company is wholly owned by the Government of Ghana', represented by Ministry of Finance and Ministry of Energy; oversight by SIGA)
- **Cadre comptable** : GHS (GH¢'000), IFRS as issued by IASB, Companies Act 2019 (Act 992); 2024 opinion also cites 'the IAS 29 directive issued by the Institute of Chartered Accountants Ghana' · clôture : 31 December
- **Site** : https://gridcogh.com (reachable (annual-reports page https://gridcogh.com/annual-reports/ lists ARs 2009-2025; 2024 PDF is 43 MB so WebFetch failed on size, curl download worked))
- **Évaluation** : Strong. GRIDCo publishes full annual reports with audited IFRS statements for every MVP year 2019-2025 on its own site, all with unmodified opinions. Statements are text-based and detailed (related party revenue by utility, receivables by related party, transmission losses GWh). Distribution and generation KPIs do not apply. The audit lag fell from about 15 months (FY2022) to about 6 months (FY2025).
- **Accès** : None blocking. 2024 PDF is 43 MB (WebFetch size limit exceeded, curl fine). Non-ASCII en dash in 2024 filename. Older reports re-uploaded in 2025/06 folder, so upload folder does not show original publication date.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | found_fetched | full_with_notes | unmodified (true and fair, IFRS; key audit matter on trade receivables impairment; no emphasis of matter seen) | unknown; filename suggests finalised 26-07-2023; file sits in /2025/06/ upload folder | <https://gridcogh.com/wp-content/uploads/2025/06/2019_Annual-Report_Final_26-07-23.pdf> |
| 2020 | found_fetched | full_with_notes | unmodified (true and fair; no emphasis of matter seen) | unknown; filename dated 02-09-2022 | <https://gridcogh.com/wp-content/uploads/2025/06/2020-Annual-Report-02-09-2022.pdf> |
| 2021 | found_fetched | full_with_notes | unmodified ('our unqualified opinion') | unknown; filename 'Approved for printing 030723' (3 July 2023) | <https://gridcogh.com/wp-content/uploads/2025/06/2021-Annual-Report-Approved-for-printing-030723.pdf> |
| 2022 | found_fetched | full_with_notes | unmodified ('unqualified opinion') | auditor signing 18 March 2024 (seen in report); upload folder 2025/01; filename dated 5-12-24 | <https://gridcogh.com/wp-content/uploads/2025/01/GRIDCo_2022_Annual-Report_Final_5-12-24.pdf> |
| 2023 | found_fetched | full_with_notes | unmodified ('unqualified opinion'); joint auditors Deloitte & Touche and Opoku, Andoh & Co | auditor signing 8/10 October 2024; PDF created 5 Dec 2024 (pdfinfo); uploaded in 2025/01 folder | <https://gridcogh.com/wp-content/uploads/2025/01/GRIDCo_2023_Annual_Report_Final_5-12-24.pdf> |
| 2024 | found_fetched | full_with_notes | unmodified ('unqualified opinion'); joint auditors Deloitte & Touche and Opoku, Andoh & Co; no emphasis of matter or material uncertainty on going concern seen | auditor's report signed 3 November 2025; directors approved FS 22 October 2025; PDF creation 10 Dec 2025; uploaded in /2026/01/ folder (so public ~Jan 2026, inferred) | <https://gridcogh.com/wp-content/uploads/2026/01/FINAL-–-GRIDCo-AR-2024-FINAL-1.pdf> |
| 2025 | found_fetched | full_with_notes | unmodified ('unqualified opinion') | auditor signing 30 June 2026; uploaded in /2026/09/ folder | <https://gridcogh.com/wp-content/uploads/2026/09/2025_GRIDCo-_Annual_Report_.pdf> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **partiel**. 2024 AR note 8(a) p.~69: revenue from transmission services and total transmission GWh (23,692). This is a wholesale transmission charge, not retail energy billed.
- `FIN_cost_recovery_ratio` : **calculable**. 2024 AR statement of comprehensive income (p.~51): revenue, other income, direct costs, G&A, impairment loss on trade receivables, finance costs; depreciation and amortisation analysis in note 17.
- `FIN_current_ratio` : **calculable**. 2024 AR statement of financial position: total current assets / total current liabilities; note 21 'Trade receivables due from related parties' (gross) and impairment.
- `FIN_ebitda_margin` : **calculable**. Revenue (note 8), direct costs (note 9), G&A (note 13), D&A (note 17). No tariff compensation/subsidy line seen.
- `FIN_government_transfer_dependency` : **absent des docs lus**. No operating subsidy or tariff compensation line seen in 2024 AR; likely zero but not explicitly stated.
- `FIN_power_purchase_payables_days` : **non applicable**. Transmission company; no power purchase/fuel cost. 'Trade payables due to related parties' exist (note 28).
- `GEN_avg_power_purchase_cost` : **non applicable**. Transmission-only entity.
- `GEN_costly_thermal_share` : **non applicable**. Transmission-only entity (national mix available from Energy Commission).
- `GEN_purchased_energy_share` : **non applicable**. Transmission-only entity.
- `NET_distribution_losses_pct` : **non applicable**. Transmission-only entity.
- `NET_saidi_hours` : **absent des docs lus**. 2024 AR reports system/line availability (%) and transmission losses; no SAIDI/SAIFI found.
- `NET_total_system_losses_pct` : **partiel**. 2024 AR note 9: 'Transmission losses for the year ended 31 December 2024 was 951 GWh'; total transmitted GWh in note 8; operational review reports 4.1% threshold. Only transmission segment.
- `COM_cash_recovery_index` : **non applicable**. Distribution KPI.
- `COM_collection_rate` : **absent des docs lus**. No explicit cash collected or collection rate found; could be approximated from receivables movement and cash flow.
- `COM_receivables_days` : **calculable**. Note 21 trade receivables (related parties and third parties, gross and impairment) plus revenue note 8; related party note 30 gives revenue by counterpart (ECG, NEDCo, VRA, VALCO).
- `OPS_customers_per_employee` : **non applicable**. Bulk-customer transmission company; staff strength 879 reported in 2024 AR.
- `GOV_annual_reporting_disclosure_score` : **calculable**. AR published, full audited FS with notes, auditor's report, operational stats (GWh, losses, availability), board composition (p.16 Board of Directors), related-party/state transactions (note 30).
- `GOV_audit_opinion_code` : **calculable**. Independent auditors' report p.~48-50: unqualified opinion, Deloitte & Touche + Opoku, Andoh & Co, going concern no material uncertainty.
- `GOV_audited_fs_publication_lag_months` : **partiel**. Signing date 3 Nov 2025 seen; public release date only inferable from WordPress upload folder (2026/01) and PDF creation date.
- `GOV_regulatory_framework_score` : **partiel**. Country-level via PURC (tariff decision papers register, annual reports to 2023) and GRIDCo 2025-2029 tariff proposal published on gridcogh.com.
- `INV_capex_to_depreciation` : **calculable**. Cash flow 'Purchase of property, plant and equipment' and note 17 additions; total D&A charge note 17.
- `ACC_consumption_per_customer` : **non applicable**. Transmission entity.
- `ACC_new_connections` : **non applicable**. Transmission entity.

</details>

### ECG (Electricity Company of Ghana) (Ghana)

- **Nom légal confirmé** : Electricity Company of Ghana Limited (SIGA 2025 State Ownership Report: 'a limited liability company wholly owned by the Government of Ghana', incorporated Feb 1997; GRIDCo 2024 AR note 30 'Electricity Company of Ghana Limited')
- **Actionnariat** : State-owned, 100% Government of Ghana (SIGA 2025 SOR, state shareholding 100.0%)
- **Cadre comptable** : GHS; framework presumed IFRS but not confirmed from a fetched ECG document · clôture : 31 December
- **Site** : https://www.ecg.com.gh (blocked: every request returns a SiteGround captcha / Incapsula challenge page (HTTP 202 redirect to /.well-known/sgcaptcha/), so no publications page was reachable)
- **Évaluation** : Weak at utility level, usable with secondary sources. ECG's own disclosures cannot be reached, and audited accounts were presented to an AGM only in July 2026, for the first time since 2018. The best data path is: (1) SIGA State Ownership Reports for audited abridged FS 2021-2025; (2) Energy Commission National Energy Statistics for the energy balance and losses back to 2000; (3) PURC quarterly key regulatory indicators for collection, SAIDI, customers and employees. Audit opinion and full notes need an offline request.
- **Accès** : ecg.com.gh is fully behind a captcha/bot challenge (SiteGround sgcaptcha plus Incapsula) for both curl and WebFetch. The ESMAP copy of the 2019 FS returns 403. No full ECG annual report or audited FS for 2019-2025 was found publicly online.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | found_link_not_fetched | not_checked | not_visible | unknown | <https://rise.esmap.org/data/files/library/ghana/Electricity Access/Ghana_ECG Financial Report_2019.pdf> |
| 2020 | not_found | not_found | not_visible | unknown |  |
| 2021 | referenced_only | summary_or_extract | not_visible | unknown | <https://siga.gov.gh/resource-category/state-ownership-reports/> |
| 2022 | referenced_only | summary_or_extract | not_visible | unknown | <https://siga.gov.gh/resource-category/state-ownership-reports/> |
| 2023 | referenced_only | summary_or_extract | not_visible | unknown | <https://siga.gov.gh/resource-category/state-ownership-reports/> |
| 2024 | referenced_only | summary_or_extract | not_visible | Audited accounts presented at the 28th AGM, reported 31 July 2026 (GNA, Graphic); no public PDF found | <https://gna.org.gh/2026/07/ecg-slashes-annual-loss-from-ghs8-3bn-to-ghs2-5bn-amid-revenue-surge/> |
| 2025 | referenced_only | summary_or_extract | not_visible | Presented at AGM reported 31 July 2026; SIGA 2025 SOR includes FY2025 'Audited' abridged FS | <https://siga.gov.gh/resource-category/state-ownership-reports/> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **partiel**. Operating revenue in the SIGA 2025 SOR ECG abridged FS (p.64-65) combined with ECG sales GWh in Energy Commission 2026 Statistics Table 3.11. Electricity-sales revenue is not separated from other revenue or grants.
- `FIN_cost_recovery_ratio` : **valeur publiée seule**. SIGA 2025 SOR ECG KPI table reports 'Cost Recovery %' for 2021-2025 without the input breakdown.
- `FIN_current_ratio` : **valeur publiée seule**. SIGA SOR reports the current ratio; current assets/liabilities are not shown separately in the abridged table.
- `FIN_ebitda_margin` : **absent des docs lus**. SOR gives EBIT only; no D&A.
- `FIN_government_transfer_dependency` : **partiel**. SIGA SOR p.65 text: 'Government grant to ECG (GHS17,035million in FY2024)... direct payments to Power Producers and Fuel Companies'. FY2025 grant reportedly not recognised. No full series.
- `FIN_power_purchase_payables_days` : **partiel**. SOR debt table: 'Trade & Other Payables' total only. No IPP/VRA payables split or power purchase cost.
- `GEN_avg_power_purchase_cost` : **partiel**. Energy purchased GWh available (EC Table 3.11; PURC quarterly 'Total Electricity Purchased'). Power purchase cost not in documents read.
- `GEN_costly_thermal_share` : **absent des docs lus**. Supply mix by source for ECG purchases not seen. National hydro/thermal split is in EC Table 3.7 but not by fuel type.
- `GEN_purchased_energy_share` : **non applicable**. Distribution-only. All energy is purchased.
- `NET_distribution_losses_pct` : **calculable**. Energy Commission 2026 National Energy Statistics Table 3.11: ECG purchase, sales and losses GWh and % for 2000-2025. PURC quarterly sheets split technical and commercial losses.
- `NET_saidi_hours` : **valeur publiée seule**. PURC quarterly key regulatory indicators give system SAIDI hours per customer and metro/urban/rural values. EC Table 3.16 gives annual SAIDI by operational area only. Inclusion of planned outages and load shedding not stated.
- `NET_total_system_losses_pct` : **partiel**. PURC 'System Losses %' reported quarterly. Purchases and sales in EC Table 3.11. No export or HV-direct split.
- `COM_cash_recovery_index` : **partiel**. PURC quarterly 'Collection Ratio (Total Revenue/Total Sales)' plus loss %. Cash and billed amounts in GHS not seen.
- `COM_collection_rate` : **valeur publiée seule**. PURC quarterly collection ratio (Q4 2023, Q1 2024 sheets).
- `COM_receivables_days` : **absent des docs lus**. No receivables breakdown in documents read.
- `OPS_customers_per_employee` : **calculable**. PURC quarterly sheets: 'No. of Customers (Incl. Inactive)', 'No. of Employees', and the ratio. SIGA SOR also gives employee count.
- `GOV_annual_reporting_disclosure_score` : **partiel**. No ECG annual report found online. Score can be assigned as low or partial from the absence of a report plus the SOR abridged FS.
- `GOV_audit_opinion_code` : **absent des docs lus**. SOR names the auditor (Ghana Audit Service). Opinion type not seen.
- `GOV_audited_fs_publication_lag_months` : **absent des docs lus**. No signing date seen. AGM in July 2026 per press.
- `GOV_regulatory_framework_score` : **partiel**. PURC tariff decisions register, rate-setting guidelines, PURC annual reports (2019-2023 listed), CWM reports and GUPI exist on purc.com.gh.
- `INV_capex_to_depreciation` : **partiel**. SOR gives net investing cash flow only. No depreciation.
- `ACC_consumption_per_customer` : **partiel**. ECG sales GWh in EC Table 3.11. ECG customer count from PURC quarterly sheets (EC Table 3.13 customer population is national, all DISCOs).
- `ACC_new_connections` : **partiel**. PURC 'Customer Growth Rate %' and customer counts by quarter. No explicit new-connections count.

</details>

### VRA (Volta River Authority) (Ghana)

- **Nom légal confirmé** : Volta River Authority (VRA), statutory authority established 26 April 1961 (SIGA 2025 SOR VRA profile)
- **Actionnariat** : State-owned statutory corporation (SIGA 2025 SOR; auditor Ghana Audit Service). NEDCo is listed as a separate specified entity by SIGA.
- **Cadre comptable** : GHS; framework not confirmed from a fetched document · clôture : 31 December (SOR uses FY2021-FY2025 calendar years)
- **Site** : https://www.vra.com (homepage reachable. The 'Annual Reports' page (resources/annual_reports.php), sustainability-reports.php and facts.php all return 404 (broken links).)
- **Évaluation** : Weak. VRA publishes no annual report or audited FS online in 2019-2025. The only audited-figure source is SIGA's State Ownership Report (abridged FS and ratios), which is enough for a few reported ratios but not the input-level KPIs. The tariff proposal to PURC adds some operational and fuel data. Full statements would need a request to VRA or the Ghana Audit Service.
- **Accès** : The vra.com 'Annual Reports' and 'Sustainability Reports' menu links return 404. No VRA annual report PDF for any MVP year was found. Only the abridged SIGA figures and a tariff proposal are public.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | referenced_only | not_found | not_visible | unknown |  |
| 2020 | not_found | not_found | not_visible | unknown |  |
| 2021 | referenced_only | summary_or_extract | not_visible | unknown | <https://siga.gov.gh/resource-category/state-ownership-reports/> |
| 2022 | referenced_only | summary_or_extract | not_visible | unknown | <https://siga.gov.gh/resource-category/state-ownership-reports/> |
| 2023 | referenced_only | summary_or_extract | not_visible | unknown | <https://siga.gov.gh/resource-category/state-ownership-reports/> |
| 2024 | referenced_only | summary_or_extract | not_visible | unknown | <https://siga.gov.gh/resource-category/state-ownership-reports/> |
| 2025 | referenced_only | summary_or_extract | not_visible | unknown | <https://siga.gov.gh/resource-category/state-ownership-reports/> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **partiel**. SOR operating revenue. VRA sales GWh not in documents read (generation totals in press and EC national tables only).
- `FIN_cost_recovery_ratio` : **valeur publiée seule**. SIGA 2025 SOR VRA KPI table 'Cost Recovery %' 2021-2025.
- `FIN_current_ratio` : **valeur publiée seule**. SOR current ratio 2021-2025.
- `FIN_ebitda_margin` : **absent des docs lus**. Only EBIT margin in SOR.
- `FIN_government_transfer_dependency` : **absent des docs lus**. Not seen.
- `FIN_power_purchase_payables_days` : **absent des docs lus**. No payables or fuel cost split.
- `GEN_avg_power_purchase_cost` : **absent des docs lus**. VRA is mainly a generator. Purchases not seen.
- `GEN_costly_thermal_share` : **partiel**. VRA 2025 Tariff Proposal to PURC section 3.3 'Generation on Liquid Fuel' table (DFO/LCO volumes and MWh from liquid fuel by year). Total sent-out not confirmed.
- `GEN_purchased_energy_share` : **absent des docs lus**. Not seen.
- `NET_distribution_losses_pct` : **non applicable**. Generation entity.
- `NET_saidi_hours` : **non applicable**. Generation entity.
- `NET_total_system_losses_pct` : **non applicable**. Generation entity.
- `COM_cash_recovery_index` : **non applicable**. Distribution KPI.
- `COM_collection_rate` : **absent des docs lus**. Tariff proposal notes payment by ECG and NEDCo 'continues to be a challenge'. No figures for amounts collected and billed.
- `COM_receivables_days` : **absent des docs lus**. Not in SOR abridged table.
- `OPS_customers_per_employee` : **non applicable**. Generator with few bulk customers.
- `GOV_annual_reporting_disclosure_score` : **partiel**. No AR online (annual reports page 404). Scorable as low from absence plus the SOR abridged FS.
- `GOV_audit_opinion_code` : **absent des docs lus**. Auditor Ghana Audit Service per SOR. Opinion not seen.
- `GOV_audited_fs_publication_lag_months` : **absent des docs lus**. No signing date seen.
- `GOV_regulatory_framework_score` : **partiel**. PURC publishes tariff decisions. VRA tariff proposal 2025 is published on vra.com.
- `INV_capex_to_depreciation` : **absent des docs lus**. SOR shows cash flow aggregates only.
- `ACC_consumption_per_customer` : **non applicable**. Generation entity.
- `ACC_new_connections` : **non applicable**. Generation entity.

</details>

### Kenya Power (KPLC) (Kenya)

- **Nom légal confirmé** : The Kenya Power and Lighting Company PLC (FY2025 Integrated Annual Report cover and Auditor-General report title, p122)
- **Actionnariat** : Listed on NSE. Government of Kenya holds 50.1% (FY2025 IAR p14, p136, Note 38 p225).
- **Cadre comptable** : KES (Shs'000), IFRS + Companies Act 2015 + PFM Act 2012 · clôture : 30 June
- **Site** : https://kplc.co.ke/annual-reports (reachable. The annual-reports page lists FY2022-FY2025 only. The old investor-relations URL returns 404.)
- **Évaluation** : Strong. The FY2025 and FY2024 IARs are text PDFs with full IFRS notes, power purchases by producer (GWh and cost), a 5-year energy balance, customers, staff and 10-year financial tables, so nearly all core KPIs can be computed. Gaps: there is no cash-collection figure and no separate distribution-loss split, SAIDI is reported only as a headline (and the auditor questions it), and the FY2019-FY2021 ARs are not on the utility website (use the Parliament IR and the 10-year tables).
- **Accès** : The old investor-relations URL returns 404. kplc.co.ke only hosts FY2022 onward, and the 2022 and 2023 files were re-uploaded in June 2024. africanfinancials.com, sustainabilityreports.com and the ESMAP RISE copy return 403. Parliament IR PDFs are very large (166-397 MB). In the IARs, the Auditor-General report pages are scanned images, not text; the rest is a text PDF.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2018/19 | found_link_not_fetched | not_checked | not_visible | Auditor-General report dated 2020 per Parliament IR metadata. News (the-star.co.ke, 2020-09-07) says audited results were released late, in Sept 2020. | <https://libraryir.parliament.go.ke/bitstreams/8ec3266c-a583-485c-9410-fc6f1016cc16/download> |
| 2019/20 | found_link_not_fetched | not_checked | not_visible | unknown | <https://libraryir.parliament.go.ke/items/6ce3e960-e40e-4d33-b50d-c4d1106793e8> |
| 2020/21 | found_link_not_fetched | not_checked | not_visible | sustainabilityreports.com snippet says published 3 Dec 2021 (not verified) | <https://rise.esmap.org/data/files/library/kenya/Electricity Access/Kenya_KPLC Annual Report and Financial Statements_2021.pdf> |
| 2021/22 | found_link_not_fetched | full_with_notes | not_visible | Parliament IR date issued 2023-04-26. The ID of the copy on kplc.co.ke decodes to an upload of 2024-06-26, which looks like a site migration and is not the original release date. | <https://kplc.co.ke/storage/01J199X5D4WQQ1XEK07HM6WJYZ.pdf> |
| 2022/23 | found_link_not_fetched | full_with_notes | not_visible | unknown. The kplc.co.ke upload ID decodes to 2024-06-26 (site migration). | <https://kplc.co.ke/storage/01J1AF61SZX223MXPQ13RNFBKY.pdf> |
| 2023/24 | found_fetched | full_with_notes | unmodified, with a Material Uncertainty relating to going concern (FY2025 IAR Annex I, p234). The preamble on p134 is consistent with an unmodified opinion. | IAR PDF created 2024-11-27. The kplc.co.ke upload ID decodes to 2024-11-28. Audited results PDF ID decodes to 2024-10-29. | <https://kplc.co.ke/storage/01JDRPZS8NZ473CWE2XCSQ1REJ.pdf> |
| 2024/25 | found_fetched | full_with_notes | unmodified_with_emphasis. Auditor-General (FCPA Nancy Gathungu). Emphasis of Matter: land without ownership documents, IPP cost disparity, and variances with County Government receivables. No going-concern material uncertainty was seen in the pages read (p122-124, 128-129). | Auditor's report signed 06 Oct 2025. Board approval 6 Oct 2025. Audited results PDF upload ID decodes to 2025-10-07. IAR PDF created 2025-11-24, upload ID 2025-11-28. | <https://kplc.co.ke/storage/01KB4JTB49DXJ81DG79JVEE0M3.pdf> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **calculable**. FY2025 IAR Note 7(a) p167: electricity sales split into post-paid, prepaid, forex adjustment and fuel cost charge. Note 7(b) p167: unit sales GWh by category (11,403 total; KPLC 10,643 after RES). Ten-year table p254 gives average yield per unit.
- `FIN_cost_recovery_ratio` : **calculable**. P&L p131 (revenue, cost of sales, network/commercial/admin opex, ECL, finance costs). Other income in Note 7(c) p168. Depreciation is 17,592,961k in the ten-year record p254. Bad debt is the ECL line, Note 9(d).
- `FIN_current_ratio` : **calculable**. SoFP p132-133: current assets 98,217,033k, current liabilities 117,426,250k. Public-sector receivables: Note 22(b) p194 gives GoK RES recurrent losses 34.77bn and GoK 0.48bn. County Government debt of KShs 5.68bn appears only in the Auditor-General report p123.
- `FIN_ebitda_margin` : **calculable**. Revenue, other income and opex as for cost recovery. There is no explicit tariff-compensation revenue or operating subsidy line: transfers are 0 or implicit. Government-funded RES cost is netted, as 'Recharged to RES' in Note 8 p171-172 and 'Revenue apportioned to RES' in Note 7(a).
- `FIN_government_transfer_dependency` : **partiel**. No tariff compensation or operating subsidy lines exist. RES costs are recharged to the Government: KShs 8.52bn renewable plus 1.85bn thermal (Note 8). The GoK RES recurrent-loss receivable is in Note 22(b). Government grants policy is at p150. No govt-paid fuel/IPP on-behalf figure was found.
- `FIN_power_purchase_payables_days` : **calculable**. Note 29(b) p206: payables to KenGen 17.71bn and other electricity suppliers 32.57bn. Power purchase cost is cost of sales 144.66bn (Note 8). Fuel is a pass-through: 23.48bn (Note 8(b) p172).
- `GEN_avg_power_purchase_cost` : **calculable**. Note 8 p169-172 gives GWh and cost (energy, capacity, fuel, forex, steam) per producer. Imports are shown separately: 1,534 GWh, KShs 14.76bn (p171). Table 1 p256-259 gives energy purchased by plant for 5 years.
- `GEN_costly_thermal_share` : **calculable**. Note 8(b) p172 gives thermal GWh: KenGen Kipevu III and Muhoroni GT 476; IPP HFO 771; off-grid diesel 88. Table 1 p256-259 covers 5 years. No emergency or rental power is listed for FY2025.
- `GEN_purchased_energy_share` : **calculable**. KPLC has no own grid generation. All supply is purchased: system total 14,472 GWh, including imports of 1,534 (Table 1 p259). The only own operation is off-grid diesel/solar, 88 GWh.
- `NET_distribution_losses_pct` : **partiel**. Only total system losses (transmission plus distribution) are reported: 21.21% (p259-260). Energy injected into distribution is not reported. Sales by voltage level (66, 132 and 220 kV in Tables 14-16 p263-264) allow HV-direct sales to be estimated.
- `NET_saidi_hours` : **valeur publiée seule**. FY2025 IAR p39: SAIDI improved from 120.6 to 113 hours; SAIFI 47.00 to 44.07. Inclusion flags are not stated. The Auditor-General (report p12, AR p128) says the system-generated SAIDI/CAIDI values could not be confirmed. EPRA reports a different monthly SAIDI series.
- `NET_total_system_losses_pct` : **calculable**. Table 1 p259-260: energy purchased 14,472 GWh, total sales 11,403 GWh including exports (Uganda 42, TANESCO 30.16), losses 3,069 GWh, reported 21.21%. Five-year history is given.
- `COM_cash_recovery_index` : **partiel**. Billing efficiency can be computed from purchased vs sold (p259). No cash-collected amount or collection rate was found. Only 'cash generated from operations' 48.2bn is available (p135).
- `COM_collection_rate` : **absent des docs lus**. No collection rate or cash collected figure in the FY2025 IAR. Text mentions only 'higher collections' (p9, p50).
- `COM_receivables_days` : **calculable**. Note 22(b)-(c) p194-195: electricity receivables gross 39.03bn, provision 13.33bn. GoK RES receivable 34.77bn. Revenue from Note 7(a).
- `OPS_customers_per_employee` : **calculable**. Customers 10,045,978 (Table 20 p265: KPLC 7,538,127 plus REP 2,507,851). Staff 10,582 (p99, p267). The reported ratio is 951 (p255).
- `GOV_annual_reporting_disclosure_score` : **calculable**. AR, full audited FS with notes, auditor report, operational statistics (Tables 1-22), energy balance and losses, public-sector receivables (Note 22, Note 38), board composition (p18-19), and state transactions (Note 38 p225) are all present.
- `GOV_audit_opinion_code` : **calculable**. Auditor-General report p122-129 (scanned): unmodified opinion with 3 Emphasis of Matter paragraphs. Auditor is the Auditor-General, FCPA Nancy Gathungu. The FY2024 report had a going-concern Material Uncertainty (Annex I p234).
- `GOV_audited_fs_publication_lag_months` : **partiel**. FYE 30 Jun 2025. Audit report signed 06 Oct 2025 (p129). The public release date is not printed. File IDs on kplc.co.ke decode to 2025-10-07 for the audited results and 2025-11-28 for the IAR.
- `GOV_regulatory_framework_score` : **partiel**. EPRA is a separate regulator that approves tariffs and PPAs (EPRA Statistics Report FY2025 p26). A tariff control period is referenced, with loss and reliability targets (EPRA p22-24). The tariff methodology document and consultation records were not fetched.
- `INV_capex_to_depreciation` : **calculable**. Cash flow p135: purchase of property and equipment 29,512,680k. PPE note p188 shows the same WIP additions. Depreciation is 17,592,961k (p254).
- `ACC_consumption_per_customer` : **calculable**. Units sold (Note 7(b), Tables 3-4 p261) and customers by category and region (Tables 20-21 p265-266).
- `ACC_new_connections` : **calculable**. 401,848 new connections in FY2025 (p40, p81). Customer totals are in Table 20. EPRA reports 395,490 for the same period (EPRA Stats FY2025 p17).

</details>

### KenGen (Kenya)

- **Nom légal confirmé** : Kenya Electricity Generating Company PLC (FY2025 IAR p128 auditor's report, and the FY2026 audited results header)
- **Actionnariat** : Listed on NSE. Government of Kenya holds 70% (stated in the KETRACO FY2024 AR related-party note p110). Not separately confirmed in the KenGen report read.
- **Cadre comptable** : KES (Shs'000), IFRS + PFM Act 2012 + Companies Act 2015 · clôture : 30 June
- **Site** : https://www.kengen.co.ke/investor-relations/financial-information/ (reachable. The old /index.php/investor-relations/annual-reports.html URL returns 404. Downloads use the WordPress Download Manager.)
- **Évaluation** : Strong for a generation company. Annual IARs for FY2019-FY2025 are all listed on the official site, and FY2025 is a text PDF with full notes, a ten-year financial review and station-level sent-out statistics. Network, commercial and access KPIs do not apply. Financial, audit and capex KPIs can be computed.
- **Accès** : Download links are WordPress Download Manager pages. A direct PDF needs the ?wpdmdl=<id> parameter from each download page. The year-to-slug mapping for FY2019-FY2022 is ambiguous (generic slugs -2, -3, -4). africanfinancials and sustainabilityreports return 403. The auditor report pages are scanned images.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2018/19 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.kengen.co.ke/investor-relations/financial-information/> |
| 2019/20 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.kengen.co.ke/investor-relations/financial-information/> |
| 2020/21 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.kengen.co.ke/download/final-results-2021/> |
| 2021/22 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.kengen.co.ke/investor-relations/financial-information/> |
| 2022/23 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.kengen.co.ke/download/2023-integrated-annual-report-financial-statement/> |
| 2023/24 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.kengen.co.ke/images/2024/new/KenGen-Integrated-Annual-Report--Accounts-2024.pdf> |
| 2024/25 | found_fetched | full_with_notes | unmodified_with_emphasis. Auditor-General, with Deloitte & Touche as delegated auditor. Emphasis of Matter: change in depreciation (10% residual value). | Auditor's report signed 30 Oct 2025 (p135). Board approval 30 Oct 2025 (p138). IAR PDF created 2025-11-25. | <https://www.kengen.co.ke/download/kengen-integrated-annual-report-financial-statement-2025/?wpdmdl=4037> |
| 2025/26 (outside MVP) | not_found | summary_or_extract | not_visible | PDF created 2026-09-04 | <https://www.kengen.co.ke/download/kengen-full-year-financial-results-2025-2026/?wpdmdl=7868> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **calculable**. P&L p136 gives electricity revenue 40.41bn (plus steam, fuel and water charges). Units sold 8,482 GWh (p12, p117). This is a wholesale yield.
- `FIN_cost_recovery_ratio` : **calculable**. P&L p136: revenue, reimbursable fuel/water costs, depreciation 14.48bn, employee, steam, O&M and other expenses, ECL 0.76bn, finance costs 2.25bn.
- `FIN_current_ratio` : **calculable**. SoFP p138: current assets 53.49bn, current liabilities 20.39bn. Trade receivables are all from Kenya Power (16.65bn, Note 21 / p221).
- `FIN_ebitda_margin` : **calculable**. P&L p136. No tariff compensation or subsidies. Grants appear only as deferred capital grants (Note 32).
- `FIN_government_transfer_dependency` : **partiel**. There is no operating subsidy line. Capital grants are in Note 32 (1.95bn non-current), and the grant policy is at p147. On-lent government loans are in Note 28.
- `FIN_power_purchase_payables_days` : **non applicable**. KenGen is a generator. Fuel costs are reimbursable pass-through (Note 7). Payables are in Note 33 (8.33bn) but are not split by fuel.
- `GEN_avg_power_purchase_cost` : **non applicable**. KenGen does not purchase power.
- `GEN_costly_thermal_share` : **calculable**. Units sent out by station are in the statistics section p249-251 (including Kipevu III and Muhoroni GT). The KPLC FY2025 Table 1 shows KenGen thermal at 476 GWh out of 8,482.
- `GEN_purchased_energy_share` : **non applicable**. Generation-only company.
- `NET_distribution_losses_pct` : **non applicable**. Generation-only company.
- `NET_saidi_hours` : **non applicable**. Generation-only company.
- `NET_total_system_losses_pct` : **non applicable**. Generation-only company.
- `COM_cash_recovery_index` : **non applicable**. Single off-taker (KPLC).
- `COM_collection_rate` : **partiel**. Revenue (p136) and the change in trade receivables (cash flow p207) allow a derived collection rate. No reported rate was found.
- `COM_receivables_days` : **calculable**. Trade receivables from KPLC 16,646,382k (Note 21 p183, p221) and revenue 56.10bn (p136). A ten-year receivables history is on p242.
- `OPS_customers_per_employee` : **non applicable**. No retail customers. Employees: 2,425 in FY2025, with a ten-year series on p241.
- `GOV_annual_reporting_disclosure_score` : **calculable**. The IAR contains full audited FS, the auditor report, generation statistics, board profiles (p44-55) and related-party notes. Energy balance is not applicable.
- `GOV_audit_opinion_code` : **calculable**. Auditor's report p127-135 (scanned): unmodified with an Emphasis of Matter on the depreciation estimate change. Auditor-General, with Deloitte & Touche delegated (p15, p128). No going-concern MU was seen.
- `GOV_audited_fs_publication_lag_months` : **partiel**. FYE 30 Jun 2025. Signed 30 Oct 2025. The IAR PDF was created 25 Nov 2025. The exact public release date is not shown.
- `GOV_regulatory_framework_score` : **partiel**. Country-level, same as KPLC: EPRA approves PPAs, including the 3rd supplemental KPLC-KenGen PPA (EPRA Stats FY2025 p26).
- `INV_capex_to_depreciation` : **calculable**. Cash flow p140: purchase of PPE 13,592,324k. PPE additions are in Note 15(a) p172. Depreciation and amortisation is 14,484,645k (p136).
- `ACC_consumption_per_customer` : **non applicable**. Generation-only company.
- `ACC_new_connections` : **non applicable**. Generation-only company.

</details>

### KETRACO (Kenya)

- **Nom légal confirmé** : Kenya Electricity Transmission Company Limited (FY2024 AR footer, and the Auditor-General report title p61)
- **Actionnariat** : State-owned, not listed (FY2024 AR related-party note p110). The exact % was not captured.
- **Cadre comptable** : KES (KShs'000), IFRS · clôture : 30 June
- **Site** : https://www.ketraco.co.ke/information-center/publications/financial-reports (reachable. The /publications URL returns 404, but /information-center/publications works.)
- **Évaluation** : Usable for financial and governance KPIs. Full IFRS FS for FY2019-FY2021, FY2023 and FY2024 are on the official site, and the FY2025 Auditor-General report is on the Parliament IR. As a grant-funded transmission company it has no customer, loss or energy-balance data, so most network and commercial KPIs are not applicable.
- **Accès** : The /publications URL returns 404 (use /information-center/publications/financial-reports). The FY2022 AR is missing from the site. FY2025 is only on the Parliament IR (74 MB). The auditor report pages are scanned images.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2018/19 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.ketraco.co.ke/sites/default/files/publications/Annual%20Report%202018-2019_0.pdf> |
| 2019/20 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.ketraco.co.ke/sites/default/files/publications/2019-2020%20ANNUAL%20REPORT%20FINAL.pdf> |
| 2020/21 | found_link_not_fetched | not_checked | not_visible | unknown | <https://www.ketraco.co.ke/sites/default/files/publications/2020-2021-%20Ketraco%20annual%20report-%20FINAL%20FOR%20PRINTING%20-June%2026.pdf> |
| 2021/22 | not_found | not_found | not_visible | unknown |  |
| 2022/23 | found_fetched | full_with_notes | qualified | PDF created 2025-05-22, which suggests web posting about May 2025. | <https://www.ketraco.co.ke/sites/default/files/publications/2022-2023%20ANNUAL%20REPORT.pdf> |
| 2023/24 | found_fetched | full_with_notes | qualified. The Auditor-General preamble p61 states 'A Qualified Opinion is issued...'. The specific qualification bases were not read. | Auditor's report signed 31 Dec 2024 (p71). PDF created 2025-05-22. | <https://www.ketraco.co.ke/sites/default/files/publications/2023-2024%20KETRACO%20Annual%20Financial%20Report%20%28For%20Web%29.pdf> |
| 2024/25 | found_link_not_fetched | not_checked | not_visible | Auditor-General report issued 12 Mar 2026; added to the Parliament IR 7 Apr 2026 (IR metadata). | <https://libraryir.parliament.go.ke/bitstreams/33e179d0-459a-4c59-8c4d-c1ca875e2e88/download> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **non applicable**. Transmission-only. Revenue is wheeling (KShs 5.50bn, P&L p74). No GWh wheeled was found in the text.
- `FIN_cost_recovery_ratio` : **calculable**. FY2024 P&L p74: revenue from contracts 5.50bn, grants 4.29bn, other income 0.87bn, admin and distribution costs, ECL, depreciation 4.61bn, finance costs 0.04bn.
- `FIN_current_ratio` : **calculable**. SoFP p75: current assets 19.73bn. Current liabilities include borrowings, deferred grant income and related-party amounts (continued on p76). Related-party receivables 3.36bn (Note 22(a)).
- `FIN_ebitda_margin` : **calculable**. P&L p74 shows 'Grants from National Government' (4.29bn) as a separate revenue line, so it can be excluded.
- `FIN_government_transfer_dependency` : **calculable**. Grants from National Government of 4,291,028k (Note 4(a)) against total revenue of 10,656,309k (p74). Deferred grant income is in Note 21(c).
- `FIN_power_purchase_payables_days` : **non applicable**. No power purchases.
- `GEN_avg_power_purchase_cost` : **non applicable**. Transmission-only.
- `GEN_costly_thermal_share` : **non applicable**. Transmission-only.
- `GEN_purchased_energy_share` : **non applicable**. Transmission-only.
- `NET_distribution_losses_pct` : **non applicable**. Transmission-only.
- `NET_saidi_hours` : **non applicable**. Transmission-only. No transmission reliability index found.
- `NET_total_system_losses_pct` : **absent des docs lus**. Transmission losses are mentioned qualitatively (p24). No GWh energy balance was found.
- `COM_cash_recovery_index` : **non applicable**. No retail billing.
- `COM_collection_rate` : **absent des docs lus**. No collection data found.
- `COM_receivables_days` : **partiel**. Trade and other receivables 8.26bn (Note 16(a)) and wheeling revenue 5.50bn. KPLC owes KETRACO 1.72bn (KPLC Note 22(b)) and has wheeling payables of 2.68bn (KPLC Note 29(b)).
- `OPS_customers_per_employee` : **non applicable**. No customers. Staff count is 516 (p41).
- `GOV_annual_reporting_disclosure_score` : **calculable**. AR with full FS and notes, the scanned auditor report, board list (p4), and related parties (p110). Energy and operational stats are limited.
- `GOV_audit_opinion_code` : **calculable**. FY2024: qualified, from the Auditor-General preamble p61. Prior-year going-concern MU and EoM are listed in Appendix 1 p128.
- `GOV_audited_fs_publication_lag_months` : **partiel**. Signed 31 Dec 2024. The web PDF was created 22 May 2025. The exact posting date is unknown.
- `GOV_regulatory_framework_score` : **partiel**. Country-level (EPRA). EPRA approved the KETRACO-TANESCO wheeling agreement (EPRA Stats FY2025 p26).
- `INV_capex_to_depreciation` : **calculable**. Cash flow p78: purchase of property and equipment, with 9,716,568k and 15,005,828k shown in the columns. PPE additions are in Note 13 p100-102. Depreciation 4,608,952k (p74).
- `ACC_consumption_per_customer` : **non applicable**. Transmission-only.
- `ACC_new_connections` : **non applicable**. Transmission-only.

</details>

### Transmission Company of Nigeria (TCN) (Nigeria)

- **Nom légal confirmé** : Transmission Company of Nigeria Plc (RC 639052), per the cover and corporate information of its audited accounts for FY2019 and FY2020
- **Actionnariat** : State-owned (Federal Government of Nigeria). The FY2019 accounts note 5.14 says capital contributions come from the owners, 'in this case, the Federal Government'. Its principal banker is the Central Bank of Nigeria. System operations were split out into the Nigerian Independent System Operator (NISO) in 2024 under the Electricity Act 2023 (NERC order; press coverage seen in search results).
- **Cadre comptable** : NGN (N'000); IFRS, plus CAMA 2020 and FRC Act 2011 · clôture : 31 December
- **Site** : https://www.tcn.org.ng (Partly reachable. The homepage returned HTTP 406 to curl, and the /repository/annualfinancialstatements/ directory returned 403 to WebFetch. Direct PDF links work: SIGNED_AFS_2019.pdf and SIGNED_AFS_2020.pdf returned 200. The same URL pattern for 2021-2024 returned 404.)
- **Évaluation** : Weak. Audited accounts exist publicly only for FY2018-FY2020 (FY2019-2020 are in the MVP window), and FY2020 needs OCR. NERC took enforcement action over TCN's non-submission of audited accounts, which suggests FY2021+ accounts are not public. For later years, use NERC quarterly and annual reports for TLF and grid reliability, and possibly donor (World Bank/AfDB) project documents for financials. The 2024 NISO carve-out breaks revenue comparability.
- **Accès** : The website homepage returned 406 and the repository directory returned 403. Only the 2018-2020 AFS PDFs exist under the known URL pattern; 2021-2024 return 404. The FY2020 PDF is fully scanned. In the FY2019 PDF, the auditor's report and statement of financial position are image pages.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | found_fetched | full_with_notes | unmodified (Ahmed Zakari & Co; no emphasis of matter or going-concern paragraph seen on the opinion page; Key Audit Matter on ECL for trade receivables) | unknown. The audit report is signed 7 June 2021 (scanned page 11) and the PDF CreationDate is 30 June 2021, so it was posted no earlier than that. | <https://www.tcn.org.ng/repository/annualfinancialstatements/SIGNED_AFS_2019.pdf> |
| 2020 | found_fetched | full_with_notes | unmodified (Ahmed Zakari & Co; KAM on ECL: gross trade receivables N317.63bn, allowance N283.84bn) | unknown. The audit report is signed 29 December 2021, and management certifications are dated 26 and 31 January 2022, so it was released after January 2022. | <https://www.tcn.org.ng/repository/annualfinancialstatements/SIGNED_AFS_2020.pdf> |
| 2021 | not_found | not_found | not_visible | unknown |  |
| 2022 | not_found | not_found | not_visible | unknown |  |
| 2023 | not_found | not_found | not_visible | unknown |  |
| 2024 | not_found | not_found | not_visible | unknown |  |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **non applicable**. Transmission-only company. Revenue is wheeling charges (FY2019 note 7: TSP/SO/MO), and energy wheeled in kWh is not given in the accounts.
- `FIN_cost_recovery_ratio` : **calculable**. FY2019 accounts: revenue (note 7), other income (note 9), cost of sales including depreciation (note 8), administrative expenses including impairment of receivables and depreciation (note 10), and net finance cost (note 12; P&L p.13). Depreciation is also in the cash flow adjustments.
- `FIN_current_ratio` : **partiel**. Current assets and current liabilities are in the FY2019 five-year summary (p.48). The statement of financial position (p.12) is an image. Receivables are owed by market operators and DisCos, with no public-sector split.
- `FIN_ebitda_margin` : **calculable**. FY2019 revenue, other income, operating expenses, and depreciation (notes 8 and 10). No tariff compensation or operating subsidy lines were seen. FGN funding goes through equity as 'capital contribution' (note 14.1/25).
- `FIN_government_transfer_dependency` : **partiel**. FY2019: FGN capital contributions recorded in equity (N17.4bn in 2019, N24.4bn in 2018; cash flow statement). No operating subsidies or costs paid on TCN's behalf were seen. FGN-guaranteed foreign borrowings appear in note 26.
- `FIN_power_purchase_payables_days` : **non applicable**. TCN does not buy power.
- `GEN_avg_power_purchase_cost` : **non applicable**. Transmission only.
- `GEN_costly_thermal_share` : **non applicable**. Transmission only.
- `GEN_purchased_energy_share` : **non applicable**. Transmission only.
- `NET_distribution_losses_pct` : **non applicable**. Transmission only.
- `NET_saidi_hours` : **absent des docs lus**. Not in the FY2019 accounts. The NERC Q4 2025 report gives system collapses (Table 3) but no SAIDI.
- `NET_total_system_losses_pct` : **valeur publiée seule**. The NERC Q4 2025 quarterly report section 2.2.1 and Figure 5 give the actual TLF (%) against the MYTO target. Energy inputs are not in TCN's accounts.
- `COM_cash_recovery_index` : **non applicable**. No retail billing.
- `COM_collection_rate` : **partiel**. NERC quarterly reports carry DisCo remittances to the Market Operator (Q4 2025 Table 11), which include TCN charges. TCN's own collections are not disclosed in the FY2019 accounts.
- `COM_receivables_days` : **calculable**. FY2019 note on trade receivables: gross N276.7bn, impairment N254.9bn (vs N241.5bn/N222.5bn in 2018), plus revenue from note 7.
- `OPS_customers_per_employee` : **non applicable**. No end customers. Employees are disclosed (FY2019 note 15.2.2: 3,768).
- `GOV_annual_reporting_disclosure_score` : **calculable**. Full audited accounts with notes and auditor's report for FY2019 and FY2020. No operational statistics or energy balance. Board listed in corporate information. Related-party and FGN transactions in notes 14.1 and 18. Nothing published after FY2020.
- `GOV_audit_opinion_code` : **calculable**. FY2019 and FY2020: unmodified opinions by Ahmed Zakari & Co (scanned pages 8-11). No going-concern material uncertainty paragraph was seen.
- `GOV_audited_fs_publication_lag_months` : **partiel**. Signing dates are known (7 June 2021 for FY2019; 29 December 2021 for FY2020). The public release date is not shown. The FY2019 PDF was created 30 June 2021.
- `GOV_regulatory_framework_score` : **calculable**. Country-level: NERC publishes MYTO orders, monthly supplementary tariff orders, quarterly and annual reports, and holds public consultations (NERC 2025 Annual Report, ch. 4-6).
- `INV_capex_to_depreciation` : **calculable**. FY2019 cash flow: purchases of PPE N29.25bn; PPE additions in note 16; depreciation N16.93bn.
- `ACC_consumption_per_customer` : **non applicable**. Transmission only.
- `ACC_new_connections` : **non applicable**. Transmission only.

</details>

### Ikeja Electric (Nigeria)

- **Nom légal confirmé** : Ikeja Electric Plc. The NERC Q4 2025 Quarterly Report abbreviation list gives 'IE - Ikeja Electric Plc', and NERC energy-cap documents use 'Ikeja Electricity Distribution Plc'. NERC 2025 Annual Report Table 10 lists the subsidiary 'IE Energy Lagos Limited' under the Lagos State Electricity Regulatory Commission.
- **Actionnariat** : Privatised DisCo (core investor holds a majority since November 2013; FGN keeps a minority through BPE/MOFI). The exact split was not confirmed from a fetched Ikeja Electric document. The Electricity Act 2023 context suggests the FGN 40% stake may be transferred (stated in EKEDC's FY2024 directors' report for DisCos generally).
- **Cadre comptable** : NGN; IFRS presumed (not confirmed from a fetched document) · clôture : 31 December (search snippet of the FY2020 report: 'year ended 31 December 2020')
- **Site** : https://www.ikejaelectric.com (down/blocked: connection reset by peer (curl, repeatedly); WebFetch returned 503)
- **Évaluation** : Weak for financial KPIs: no audited accounts could be opened, and only an FY2020 report is known publicly (third-party host). Operational and commercial KPIs (billing, collection, ATC&C, customers, metering, subsidy share) are well covered quarterly by NERC reports from 2019 to 2026. Best path: NERC quarterly reports for operations, plus a request to the company or NERC (USoA filings) for audited accounts. Retry the ESMAP link from another network.
- **Accès** : The company website was unreachable (TCP reset, 503). The only known audited-FS copy (FY2020, on ESMAP) returned 403. The Wayback Machine could not be reached either (connection reset, and WebFetch blocks web.archive.org). No bond or commercial paper issuance was found.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | referenced_only | not_found | not_visible | unknown |  |
| 2020 | found_link_not_fetched | full_with_notes | not_visible | unknown | <https://rise.esmap.org/data/files/library/nigeria/Electricity Access/Nigeria_Ikeja Electric_Report 2020.pdf> |
| 2021 | not_found | not_found | not_visible | unknown |  |
| 2022 | not_found | not_found | not_visible | unknown |  |
| 2023 | not_found | not_found | not_visible | unknown |  |
| 2024 | not_found | not_found | not_visible | unknown |  |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **partiel**. Not from the accounts. NERC Q4 2025 Tables 4-8 give DisCo-level energy received and billed and revenue billed. Using the NERC billing figure gives a tariff proxy.
- `FIN_cost_recovery_ratio` : **absent des docs lus**. No accounts read (FY2020 report blocked).
- `FIN_current_ratio` : **absent des docs lus**. No accounts read.
- `FIN_ebitda_margin` : **absent des docs lus**. No accounts read.
- `FIN_government_transfer_dependency` : **partiel**. NERC Q4 2025 Table 10 gives the total GenCo invoice against each DisCo's DRO-adjusted final obligation, i.e. the FGN subsidy by DisCo.
- `FIN_power_purchase_payables_days` : **absent des docs lus**. No accounts. NERC Table 11 gives remittance % to NBET/MO only.
- `GEN_avg_power_purchase_cost` : **partiel**. NERC Q4 2025 Table 10 (invoice and DRO) and Table 4 (energy offtake), for the DisCo.
- `GEN_costly_thermal_share` : **non applicable**. Distribution-only DisCo.
- `GEN_purchased_energy_share` : **non applicable**. All energy is purchased.
- `NET_distribution_losses_pct` : **calculable**. NERC Q4 2025 Table 6 (energy received vs billed, billing efficiency; Ikeja row) and Table 9 (ATC&C). No HV-direct split.
- `NET_saidi_hours` : **absent des docs lus**. NERC quarterly reports carry complaint categories (interruption, load shedding) but no SAIDI.
- `NET_total_system_losses_pct` : **non applicable**. Distribution only. Use distribution losses.
- `COM_cash_recovery_index` : **calculable**. NERC Q4 2025 Table 7 (billing efficiency) and Table 8 (collection efficiency), Ikeja row; ATC&C in Table 9.
- `COM_collection_rate` : **calculable**. NERC Q4 2025 Table 8: total billings, revenue collected, collection %.
- `COM_receivables_days` : **absent des docs lus**. No accounts read.
- `OPS_customers_per_employee` : **partiel**. Customers: NERC Q4 2025 Table 18 (registered and metered customers; Ikeja row 1,308,042 / 1,130,213). Employee count not found.
- `GOV_annual_reporting_disclosure_score` : **partiel**. Only the FY2020 report is known to exist publicly (third-party host). No company-hosted publication page could be reached.
- `GOV_audit_opinion_code` : **absent des docs lus**. FY2020 report not opened.
- `GOV_audited_fs_publication_lag_months` : **absent des docs lus**. No signing dates seen.
- `GOV_regulatory_framework_score` : **calculable**. Country-level, from NERC (MYTO orders, monthly tariff orders, quarterly and annual reports). From 2025 Lagos has LASERC as state regulator (NERC 2025 AR Table 10).
- `INV_capex_to_depreciation` : **absent des docs lus**. No accounts read.
- `ACC_consumption_per_customer` : **calculable**. NERC quarterly energy billed (Table 6) and customer counts (Table 18).
- `ACC_new_connections` : **partiel**. NERC Q4 2025 Table 19 gives meter deployment by DisCo (meters, not new connections). Customer stock is in Table 18, so year-over-year differences can be derived.

</details>

### Eko Electricity Distribution (EKEDC) (Nigeria)

- **Nom légal confirmé** : Eko Electricity Distribution Plc (Registration number 638862), per the FY2024 financial statements cover; brand EKEDC/EKEDP
- **Actionnariat** : Mixed: West Power and Gas Limited 60%, Bureau of Public Enterprises 32%, Ministry of Finance Incorporated 8% (FY2024 directors' report, shareholding structure, p.4). Not listed on any exchange.
- **Cadre comptable** : NGN (N'000); IFRS Accounting Standards plus CAMA 2020 and FRC Act 2023 · clôture : 31 December
- **Site** : https://ekedp.com (Financial Report page: https://ekedp.com/financial-report) (reachable (200). The PDFs are hosted on ekostore.fra1.digitaloceanspaces.com and all downloaded fine.)
- **Évaluation** : Strong. Audited financial statements with notes are publicly posted for every MVP year from FY2019 to FY2024, with auditor's reports (KPMG, then PwC). The FY2024 accounts separate the FGN tariff-shortfall subsidy, MDA receivables, NBET payables and capex, so the financial KPIs can be computed. Operational inputs (energy billed, collections, customers, ATC&C) come from NERC quarterly reports. FY2020-2023 need OCR. The FY2025 Lagos carve-out into Excel Electricity Distribution Ltd will need consolidation handling.
- **Accès** : No blocks. Most PDFs are scanned images with no text layer: FY2013-2017, FY2020, FY2021 (except the P&L page), FY2022 and FY2023. FY2018, FY2019 and FY2024 are text. The FY2024 statement of financial position page is an image. The listing page gives no year labels or upload dates; years had to be identified from the covers. No bond issuance was found.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | found_fetched | full_with_notes | unmodified_with_emphasis (KPMG Professional Services; separate 'Material Uncertainty Related to Going Concern' paragraph referring to Note 32) | unknown. The audit report is signed 14 October 2021 and the PDF CreationDate is 14 October 2021. | <https://ekostore.fra1.digitaloceanspaces.com/report/SyNUmk4oCLvFvzDPV362piZ0nC2tpqaFsDEFEYV4.pdf> |
| 2020 | found_fetched | full_with_notes | not_visible | unknown (PDF CreationDate 4 May 2022) | <https://ekostore.fra1.digitaloceanspaces.com/report/lhW8wNYTjkua6ur1XJhdHieeMG3s3Bfqdfew4ow4.pdf> |
| 2021 | found_fetched | full_with_notes | not_visible | unknown. The text layer shows '05 April 2023' (probably the signing date, not verified). PDF CreationDate is 28 April 2023. | <https://ekostore.fra1.digitaloceanspaces.com/report/j9OoCG0BYJHcFqhcLK4AW3Zi8owqLwEzm1JHRelI.pdf> |
| 2022 | found_fetched | full_with_notes | not_visible | unknown (PDF CreationDate 7 August 2023) | <https://ekostore.fra1.digitaloceanspaces.com/report/lV5TEjvBM8fY4oh5qkA2Pv3sHeN7nfAWqS4CDUit.pdf> |
| 2023 | found_fetched | full_with_notes | unmodified | unknown | <https://ekostore.fra1.digitaloceanspaces.com/report/Nxy1yKA5Fl4BN5kfxlZ4ShltnUIcx3x6S73lEfwW.pdf> |
| 2024 | found_fetched | full_with_notes | unmodified (PricewaterhouseCoopers; KAM on impairment of trade receivables; no going-concern paragraph seen; unqualified ICFR assurance report) | unknown. The audit report and ICFR report are signed 04 February 2026, so publication is after that date. | <https://ekostore.fra1.digitaloceanspaces.com/report/rLs177snOb8Tk3GP1lpNn2jOgq3w9lFy3sBzxNC0.pdf> |
| 2025 | not_found | not_found | not_visible | unknown |  |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **partiel**. Revenue in FY2024 note 10 (by band, prepaid/postpaid). Energy billed in GWh is not in the accounts, but NERC quarterly reports give Eko's energy received/billed (Q4 2025 Tables 4-6). Combining sources makes it computable.
- `FIN_cost_recovery_ratio` : **calculable**. FY2024: revenue (note 10), other income (note 14, incl. tariff shortfall), cost of sales including cost of energy and depreciation (note 11), operating expenses (note 13), net impairment (note 12), depreciation and amortisation (cash flow; notes 18-20), finance costs (note 16).
- `FIN_current_ratio` : **calculable**. Current assets and liabilities in the FY2024 five-year summary (p.66; the statement of financial position on p.22 is an image). Public-sector receivables: note 9 credit risk table gives 'Non Key Client Group (NKCG)', described as MDAs, with gross carrying amount and loss allowance.
- `FIN_ebitda_margin` : **calculable**. FY2024 note 14: tariff shortfall (FGN subsidy) N230.8bn shown separately from revenue (note 10). Government grant amortisation is in note 14/30. Operating expenses are in notes 11 and 13 with depreciation separable.
- `FIN_government_transfer_dependency` : **calculable**. FY2024 note 14 and note 8: since 2024, NBET invoices are issued net of the approved tariff and the subsidy is recognised as tariff shortfall income. This combines tariff compensation and costs paid by government on the DisCo's behalf. Note 22 gives the tariff shortfall receivable (2023).
- `FIN_power_purchase_payables_days` : **partiel**. FY2024 note 26: trade payables (NBET 'and other suppliers' combined) plus interest payables to NBET/ONEM; cost of energy is in note 11. The NBET-only payable is not separated.
- `GEN_avg_power_purchase_cost` : **partiel**. Cost of energy (FY2024 note 11) and energy received (NERC quarterly Table 4). The NERC subsidy table (Table 10) gives invoice vs DRO by DisCo.
- `GEN_costly_thermal_share` : **non applicable**. Distribution-only DisCo.
- `GEN_purchased_energy_share` : **non applicable**. All energy is purchased from NBET/market.
- `NET_distribution_losses_pct` : **calculable**. NERC Q4 2025 Table 6 (energy received vs billed, billing efficiency) and Table 9 (ATC&C), Eko row. Not in the accounts. No HV-direct split.
- `NET_saidi_hours` : **absent des docs lus**. Neither the FY2024 accounts nor the NERC quarterly report gives SAIDI.
- `NET_total_system_losses_pct` : **non applicable**. Distribution only.
- `COM_cash_recovery_index` : **calculable**. NERC quarterly billing efficiency (Table 6/7) and collection efficiency (Table 8), Eko row.
- `COM_collection_rate` : **calculable**. NERC Q4 2025 Table 8 (billings, collections, %). Accounts give receivables movement only.
- `COM_receivables_days` : **calculable**. FY2024 note 22: gross trade receivables N185.7bn, ECL; tariff shortfall receivables (nil in 2024, N64.3bn in 2023); revenue in note 10.
- `OPS_customers_per_employee` : **calculable**. Employees: FY2024 note 37.3 (average full-time 1,982). Customers: NERC Q4 2025 Table 18 (Eko registered 641,411, metered 550,764).
- `GOV_annual_reporting_disclosure_score` : **calculable**. Full audited accounts with auditor's report, corporate governance and audit committee reports, board list, related parties (note 36), MDA receivables (note 9). No operational statistics or energy balance in the accounts.
- `GOV_audit_opinion_code` : **calculable**. FY2024: unmodified (PwC, 4 Feb 2026). FY2019: unmodified with going-concern material uncertainty (KPMG, 14 Oct 2021).
- `GOV_audited_fs_publication_lag_months` : **partiel**. Signing dates seen for FY2019 (14 Oct 2021), FY2023 (about 25 Jul 2024, from scan) and FY2024 (4 Feb 2026). The website does not date its uploads. PDF CreationDate metadata is a proxy for some years.
- `GOV_regulatory_framework_score` : **calculable**. Country-level, from NERC (MYTO 2024, monthly supplementary orders, consultations, annual report). Lagos SERC (LASERC) took over oversight in 2025.
- `INV_capex_to_depreciation` : **calculable**. FY2024 cash flow: purchase of PPE N25.25bn and intangibles N10.13bn; depreciation, amortisation and right-of-use depreciation listed. Customer-granted assets are also in note 14.
- `ACC_consumption_per_customer` : **calculable**. NERC quarterly energy billed and customer count (Tables 6 and 18).
- `ACC_new_connections` : **partiel**. NERC Table 19 gives meter deployment, not connections. Service connection fees are in FY2024 note 14. Customer stock deltas can be derived from Table 18.

</details>

### ZESCO (Zambia)

- **Nom légal confirmé** : ZESCO Limited (confirmed on the zesco.co.zm homepage and in the auditor's reports in the 2023 and 2025 integrated reports, 'TO THE MEMBERS OF ZESCO LIMITED')
- **Actionnariat** : State-owned. The 2025 IR corporate governance statement says the Board is appointed by the Industrial Development Corporation (IDC), the state holding company. The Government of the Republic of Zambia issued a letter of support (2024 and 2025 auditor's reports).
- **Cadre comptable** : ZMW (Kwacha, K'000 in FS); IFRS Accounting Standards (IASB) and the Companies Act 2017 (per the auditor's opinion in the 2024 and 2025 IRs) · clôture : 31 December
- **Site** : https://www.zesco.co.zm (Reachable but flaky. The homepage fetched; investments.php returned HTTP 503; curl to the bare zesco.co.zm host failed on a TLS certificate mismatch, while www.zesco.co.zm worked. PDFs are hosted under /assets/documents/annual_reports/.)
- **Évaluation** : Usable to strong for the MVP. Integrated reports with full audited FS are public for 2020-2025, and FY2025 was already out by about March 2026. Financial KPIs are best taken from the text-based 2024 FS; 2023 and 2025 need OCR. Distribution losses, collection, customers and headcount are well covered in the 2025 IR. Supply-mix GWh (purchases, imports, emergency power) and total system losses are missing and should be sourced from ERB Energy Sector Reports.
- **Accès** : zesco.co.zm investments.php returned 503. The bare zesco.co.zm host has a TLS certificate mismatch (use www.). The PDFs are large (up to 31MB). The FS in the 2023 and 2025 IRs are scanned images (the 2025 ones at 72 dpi) and need OCR; the 2020-2022 and 2024 FS are text. The 2019 report is only found on ESMAP and returned 403. PDF creation dates (often 2025) look like re-uploads and are unreliable proxies for publication.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 | found_link_not_fetched | not_checked | not_visible | unknown | <https://rise.esmap.org/data/files/library/zambia/Electricity Access/Zambia_ZESCO Integrated Report 2019.pdf> |
| 2020 | found_fetched | full_with_notes | disclaimer | unknown (PDF CreationDate 18 Aug 2022, which may be a re-upload date; file name timestamp 20220818) | <https://www.zesco.co.zm/assets/documents/annual_reports/ZESCOIntegratedReport2020-20220818113110.pdf> |
| 2021 | found_fetched | full_with_notes | qualified (with material uncertainty related to going concern) | unknown (PDF CreationDate Jan 2025, probably a re-upload) | <https://www.zesco.co.zm/assets/documents/annual_reports/2021_Integrated_Report_ZESCO.pdf> |
| 2022 | found_fetched | full_with_notes | qualified (with material uncertainty related to going concern) | unknown; FS signed 4 March 2024 ('Signed at Lusaka on 4th March 2024'); PDF CreationDate 2 Oct 2025 | <https://www.zesco.co.zm/assets/documents/annual_reports/ZESCO-Integrated-Report-2022.pdf> |
| 2023 | found_fetched | full_with_notes | unmodified_with_emphasis (material uncertainty related to going concern; 'Our opinion is not further modified') | unknown; directors' statement signed at Lusaka on 23 December 2024; PDF CreationDate 25 Oct 2025 | <https://zesco.co.zm/assets/documents/annual_reports/ZESCO_Integrated_Report-2023.pdf> |
| 2024 | found_fetched | full_with_notes | unmodified_with_emphasis (material uncertainty related to going concern; 'Our opinion is not modified in respect of this matter') | unknown; PDF CreationDate 27 Oct 2025; auditor signing date not extractable | <https://zesco.co.zm/assets/documents/annual_reports/2024_Integrated_Report_ZESCO.pdf> |
| 2025 | found_fetched | full_with_notes | unmodified_with_emphasis (material uncertainty related to going concern; Grant Thornton) | unknown; PDF CreationDate 30 Mar 2026 (an upper-bound proxy; the release date was not stated) | <https://www.zesco.co.zm/assets/documents/annual_reports/2025_ZESCO_Integrated_Report_Digital.pdf> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **partiel**. The 2024 IR Finance Director's report has revenue by category (Mining 22,621; Residential 1,901; Industrial & Agricultural 3,356; Exports 7,238; Commercial; Total K30,844m), and the FS revenue note is in the text-based 2024 FS. Energy billed (GWh) appears only for the distribution/retail segment (2025 IR 'Distribution System Performance': sales 5,498.90 GWh in 2025, 5,969.82 in 2024). Group sales GWh including mining and exports was not seen.
- `FIN_cost_recovery_ratio` : **calculable**. 2024 IR FS (text): income statement with revenue, cost of sales, administrative expenses, impairment provisions, other losses, finance costs (2,352), and depreciation and amortisation (EBITDA reconciliation, p.14-20 of the FD report). Bad debt or ECL is in the impairment lines and the trade receivables notes.
- `FIN_current_ratio` : **calculable**. 2024 IR statement of financial position (text, e.g. trade and other receivables 9,661,983). The current ratio is also reported: 0.21x (2024) and 0.26x (2025) in the highlights pages. Public-sector receivables are only partially identified (related parties and water utilities are mentioned).
- `FIN_ebitda_margin` : **partiel**. The FS give revenue and opex excluding depreciation (2024 IR FD report EBITDA reconciliation; 2025 IR reports an EBITDA margin of 70% in the narrative). No tariff compensation revenue line exists. Government support for emergency power (USD 39m in 2024; K533m in 2025) is disclosed in the narrative, but its accounting treatment was not confirmed.
- `FIN_government_transfer_dependency` : **partiel**. 2024 IR FD report: 'Government provided support of USD 39 million towards emergency power'. 2025 IR: 'Secured K533 million in Government financial support to ease pressures related to power purchase obligations'. This is narrative only; no tariff-compensation line was found in the FS.
- `FIN_power_purchase_payables_days` : **partiel**. The cost-of-sales table in the 2024 IR FD report gives Local Purchases (IPP) 11,585 and Power Imports 9,701 (K'm). Payables appear only as total trade and other payables (2025 FS financial instruments note 26: 63,206,790 Group). IPP debt is given in USD in the narrative (USD 187m in 2025). No separate payables line for power purchases was seen.
- `GEN_avg_power_purchase_cost` : **partiel**. Costs are available (local purchases, power imports, wheeling: 2024 IR cost-of-sales table). Purchased or imported GWh was not found in the 2024 or 2025 IR text; only own generation is given (8,738.4 GWh in 2025; 7,524.5 GWh in 2024).
- `GEN_costly_thermal_share` : **absent des docs lus**. Emergency power imports are described in money terms (cost of sales), but no GWh split of emergency, rental or liquid-fuel supply was found in the 2024 or 2025 IR.
- `GEN_purchased_energy_share` : **partiel**. Own generation GWh is in the 2025 IR generation section. Purchased domestic and imported GWh were not seen. Distribution 'energy purchase' (6,074.79 GWh) is the distribution input, not the generation-level supply mix.
- `NET_distribution_losses_pct` : **calculable**. 2025 IR 'Distribution System Performance' table: Energy Purchase 6,074.79 / 6,714.68 GWh, Energy Sales 5,498.90 / 5,969.82 GWh, Loss 575.89 / 744.87 GWh, % Loss 9.48 / 11.26 (2025 / 2024).
- `NET_saidi_hours` : **valeur publiée seule**. 2025 IR: 'SAIFI was 11 times ... SAIDI was 184hrs against ERB requirement of 27hrs or less'; the system was affected by load management. Inclusion and exclusion rules (load shedding, planned outages) are not stated. The 2024 IR only says 'SAIDI and SAIFI continued to improve' without values in the text.
- `NET_total_system_losses_pct` : **absent des docs lus**. Only distribution losses are reported. No transmission losses or full energy balance (sent out + purchases + imports - exports - billed) was found in the 2024 or 2025 IR text.
- `COM_cash_recovery_index` : **calculable**. 2025 IR 'Billing Vs Collection' table: billing K6.79bn / K4.81bn, collection K6.11bn / K3.5bn, collection rate 90% / 72%, together with the distribution purchase and sales GWh table. Scope appears to be retail distribution only; mining PSA customers seem excluded, since group revenue is K32.7bn.
- `COM_collection_rate` : **calculable**. 2025 IR Distribution System Performance: billing and collection in K bn plus a reported collection rate of 90% (2025) and 72% (2024). Retail scope only.
- `COM_receivables_days` : **partiel**. Trade and other receivables (2024 FS statement of financial position; 2025 FS note 26: 13,881,651 Group) and revenue are available. A gross versus net split of electricity trade receivables requires the receivables note; the 2025 notes are scanned. There is no tariff-compensation receivable. The 2025 chairperson's statement mentions debtor days qualitatively.
- `OPS_customers_per_employee` : **calculable**. 2025 IR highlights: customer base 1,438,153 (2024: 1,357,021), head count (annual average) 10,319 (2024: 6,707), and a reported customer/employee ratio of 139 (2024: 202). Monthly employee counts are in the directors' report (scanned).
- `GOV_annual_reporting_disclosure_score` : **calculable**. Integrated reports with full audited FS and auditor's report, a corporate governance statement with board composition and attendance, operational statistics (generation, distribution losses, SAIDI/SAIFI) and related-party notes were seen in the 2023-2025 IRs. Public-sector receivables are not clearly separated.
- `GOV_audit_opinion_code` : **calculable**. Auditor's reports seen: 2020 disclaimer (Deloitte); 2021 and 2022 qualified with going-concern material uncertainty (Grant Thornton); 2023, 2024 and 2025 unmodified with going-concern material uncertainty (Grant Thornton).
- `GOV_audited_fs_publication_lag_months` : **partiel**. Signing dates: FY2022 FS signed 4 March 2024; FY2023 directors' statement signed 23 Dec 2024. FY2024 and FY2025 signing dates were not extracted (FY2025 is scanned). Public release dates are not stated; PDF creation dates were used as proxies only.
- `GOV_regulatory_framework_score` : **partiel**. The ERB is a separate regulator. The 2023 FS directors' report states that the ERB approved a 5-year Multi Year Tariff (2023-2027) effective 1 May 2023, plus an emergency tariff in 2024. The ERB publishes Energy Sector Reports and its own annual reports. Tariff methodology and consultation documents were not fetched.
- `INV_capex_to_depreciation` : **calculable**. 2024 IR FS PPE note 'Additions' lines (text) plus depreciation and amortisation in the EBITDA reconciliation. The 2025 directors' report (scanned) states the Group invested K7.1bn in PPE (2024: K7.6bn).
- `ACC_consumption_per_customer` : **partiel**. Distribution energy sales of 5,498.90 GWh and the customer base of 1,438,153 are in the 2025 IR. Group-wide billed GWh including mining and export customers was not seen.
- `ACC_new_connections` : **partiel**. 2025 IR mentions '18,257 new connections' (stakeholder section) and 15,306 LTDRP last-mile connections, with a connections backlog of 19,806. These are not presented as a clean annual KPI table.

</details>

### Eskom (South Africa)

- **Nom légal confirmé** : Eskom Holdings SOC Ltd (confirmed from the FY2025 annual financial statements)
- **Actionnariat** : State-owned (Government of South Africa as shareholder). Government support under the Eskom Debt Relief Act (R230bn, of which R180bn drawn by 2025, per the FY2025 auditor's report). Eskom has JSE-listed debt but no listed equity.
- **Cadre comptable** : ZAR (Rm); IFRS, Companies Act 71 of 2008 and PFMA · clôture : 31 March
- **Site** : https://www.eskom.co.za (Reachable. The integrated results page and all PDFs returned HTTP 200.)
- **Évaluation** : Strong. Full audited AFS and integrated reports exist for every year FY2019-FY2025, plus FY2026, all text PDFs. The AFS state approval and publication dates, and the IR has 5-year technical statistics (energy balance, IPP and imports GWh, losses, SAIDI, customers, debtors days). Gaps are a cash-collected figure, a payables split for power purchases, and an emergency or IPP OCGT GWh split. From FY2025 the figures should be treated at consolidated group level, since NTCSA is now a separate subsidiary.
- **Accès** : None. All PDFs are text-based, in English, and openable (AFS about 2MB, IR about 12MB). The FY2019 and FY2020 files sit under 2021 upload paths after a site migration, so URL dates do not indicate publication dates.

| Exercice | Rapport annuel | États fin. | Opinion | Publication | URL |
|---|---|---|---|---|---|
| 2019 (FYE 31 Mar 2019) | found_fetched | full_with_notes | qualified (material uncertainty related to going concern also present) | 30 July 2019 (AFS text: approved by the board 18 July 2019, 'published on 30 July 2019') | <https://www.eskom.co.za/wp-content/uploads/2021/02/0004EskomAFS2019singles.pdf> |
| 2020 | found_fetched | full_with_notes | qualified | 30 October 2020 (approved by the board 28 Oct 2020) | <https://www.eskom.co.za/wp-content/uploads/2021/06/0005_Eskom-AFS-2020.pdf> |
| 2021 | found_fetched | full_with_notes | qualified | 31 August 2021 (approved by the board 23 Aug 2021) | <https://www.eskom.co.za/wp-content/uploads/2021/08/AFS2021.pdf> |
| 2022 | found_fetched | full_with_notes | qualified (with material uncertainty related to going concern) | 23 December 2022 (approved by the board 16 Dec 2022) | <https://www.eskom.co.za/wp-content/uploads/2022/12/2022_annual_financial_statements.pdf> |
| 2023 | found_fetched | full_with_notes | qualified (with material uncertainty related to going concern) | 31 October 2023 (approved by the board 30 Oct 2023) | <https://www.eskom.co.za/wp-content/uploads/2023/10/Eskom_annual_financial_statements_2023.pdf> |
| 2024 | found_fetched | full_with_notes | qualified (with material uncertainty related to going concern) | 19 December 2024 (approved for issue by the board 18 Dec 2024) | <https://www.eskom.co.za/wp-content/uploads/2024/12/Eskom-annual-financial-statements-2024.pdf> |
| 2025 | found_fetched | full_with_notes | qualified (irregular expenditure and losses due to criminal conduct under PFMA disclosures, notes 51.1 and 51.3) with material uncertainty related to going concern | 30 September 2025 (approved by the board 29 Sep 2025; AFS text says 'published on 30 September 2025') | <https://www.eskom.co.za/wp-content/uploads/2025/09/Eskom-annual-financial-statements-2025-1.pdf> |

<details><summary>Couverture des KPI (preuves)</summary>

- `FIN_average_revenue_per_kwh_billed` : **calculable**. AFS 2025 note 32 Revenue (total electricity sales R338,901m by customer category) and IR 2025 Technical statistics p.140 (Total sales 189,723 GWh; electricity revenue R338,901m; 5-year series).
- `FIN_cost_recovery_ratio` : **calculable**. AFS 2025: note 32 revenue, note 33 other income (3,265), note 34 primary energy (150,207), note 35 employee benefits (43,160), other expenses, note 36 impairment of financial assets (7,317), depreciation and amortisation (31,764) and finance cost (39,932) in the segment table and income statement.
- `FIN_current_ratio` : **calculable**. AFS 2025 statement of financial position (current trade and other receivables 41,923; trade and other payables 54,040, etc.). Public-sector receivables are covered by municipal arrear debt (R94.6bn, IR) and the note 20 receivables analysis.
- `FIN_ebitda_margin` : **calculable**. The AFS 2025 segment note reports EBITDA (99,038) and its components. No tariff compensation or operating subsidy lines exist; government support comes through equity and debt relief.
- `FIN_government_transfer_dependency` : **partiel**. IR 2025: 'R64 billion Government support (2024: R76 billion)' (Debt Relief Act equity, not operating revenue) and 'R2.4 billion Electrification spend funded by Government'. There is no tariff compensation or operating subsidy line, so the KPI is mostly near-zero or not applicable on an operating basis.
- `FIN_power_purchase_payables_days` : **partiel**. Note 34 gives IPP purchases (45,642) and international purchases (6,554), and own generation costs include fuel (98,011). Payables are only given as total trade and other payables (note 30); no IPP-specific payable was seen in the sections read.
- `GEN_avg_power_purchase_cost` : **calculable**. AFS note 34 (IPP R45,642m; international purchases R6,554m) and IR Technical statistics (IPP purchases 19,365 GWh; imports from SADC 7,570 GWh).
- `GEN_costly_thermal_share` : **partiel**. IR Technical statistics: gas turbine stations 2,176 GWh (Eskom diesel OCGTs), diesel and kerosene usage 679.1 Ml, and Power sent out 195,702 GWh. IPP OCGT or emergency purchases are not split out of 'IPP purchases' in the tables read.
- `GEN_purchased_energy_share` : **calculable**. IR Technical statistics: Power sent out by Eskom 195,702 GWh, IPP purchases 19,365 GWh, imports 7,570 GWh, wheeling 2,028 GWh.
- `NET_distribution_losses_pct` : **partiel**. IR Technical statistics: Distribution energy losses 10.4% (reasonable assurance); AFS directors' report says 20,525 GWh (2024: 19,166), with non-technical losses of 14,881 GWh. Injected-to-distribution GWh is not shown directly but can be derived from losses GWh and the percentage.
- `NET_saidi_hours` : **valeur publiée seule**. IR Technical statistics: SAIDI 34.9 hours (reasonable assurance), reported after exclusions defined in the National Regulated Standards (footnote 2). Whether load shedding is included is not stated beyond that.
- `NET_total_system_losses_pct` : **calculable**. IR Technical statistics: total available for distribution 218,601 GWh, total sales 189,723 GWh, international sales 14,532 GWh, technical and other losses 25,339 GWh, and reported total energy losses of 12.3% (transmission 2.4%, distribution 10.4%).
- `COM_cash_recovery_index` : **partiel**. Billed revenue is in note 32 ('Invoiced to customers' versus 'Amounts not meeting collectability criteria' and 'Recognised on a cash received basis'). Cash collected is not given as a single figure in the sections read; collection is reported via arrear debt % of revenue (6.28%) and debtors days.
- `COM_collection_rate` : **partiel**. No explicit collection rate was seen. Proxies: debtors days by segment (municipalities 215.7 days), arrear debt as % of revenue (6.28%), and municipal arrear debt of R94.6bn (IR p.140 Customer statistics). The cash-flow statement may give receipts from customers (not checked).
- `COM_receivables_days` : **calculable**. AFS note 20 trade and other receivables plus note 32 revenue. The IR also reports debtors days by customer segment. There is no tariff-compensation receivable (not applicable).
- `OPS_customers_per_employee` : **calculable**. IR Technical statistics: number of customers 7,120,090. IR human capital section: 'Group headcount increased to 42 030 employees'. Note that customers are direct customers only; municipal end users are excluded.
- `GOV_annual_reporting_disclosure_score` : **calculable**. Integrated report, full AFS with notes, auditor's report, 5-year technical statistics with energy balance and losses, municipal debt disclosures, board composition, and PFMA and related-party disclosures were all seen in FY2025.
- `GOV_audit_opinion_code` : **calculable**. FY2019-FY2025 (and FY2026) auditor's reports are all qualified, with a going-concern material uncertainty paragraph in FY2019 and FY2022-FY2026. Auditors were SNG Grant Thornton (FY2019-FY2021) and Deloitte & Touche (FY2022 onward).
- `GOV_audited_fs_publication_lag_months` : **calculable**. Each AFS states its board approval and publication dates: FY2019 Jul 2019; FY2020 Oct 2020; FY2021 Aug 2021; FY2022 Dec 2022; FY2023 Oct 2023; FY2024 Dec 2024; FY2025 Sep 2025.
- `GOV_regulatory_framework_score` : **partiel**. NERSA is a separate regulator using the MYPD methodology. MYPD6 (FY2026-FY2028) was decided in Jan 2025, and the application was published for public consultation (search results; Eskom news page). NERSA annual reports exist (2022/23 fetched via PMG). The methodology document itself was not fetched.
- `INV_capex_to_depreciation` : **calculable**. AFS segment note: additions to PPE and intangibles 41,414 and depreciation and amortisation 31,764. IR: capital expenditure of R41.1bn excluding capitalised borrowing costs.
- `ACC_consumption_per_customer` : **calculable**. IR: total sales 189,723 GWh and 7,120,090 customers. The figure is distorted because sales include redistributors and international sales, so segment-level sales should be used.
- `ACC_new_connections` : **calculable**. IR 2025: '83 031 Electrification connections (2024: 114 800)' plus the customer count.

</details>
