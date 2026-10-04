"""Source register for Book 2 (PAYGo Solar Finance) and MODEL 2: the single list from which the standalone register
(output/04_SOURCE_REGISTER_v1.0.xlsx) and the model's Source_Register sheet are both built.

Grade describes the source cited: A primary official, regulatory or audited; B authoritative institutional (including a
company's own unaudited disclosure); C reputable secondary; D unverified or informal.
Status describes what this project has verified in that source: VERIFIED; VERIFIED (HISTORICAL); PENDING PRIMARY DOCUMENT;
UNVERIFIED; CONFLICTING SOURCES; NOT USED. Only VERIFIED and VERIFIED (HISTORICAL) claims may feed a model calculation.
Pages are PDF page numbers of the file held by the project unless stated; "PAGE TO VERIFY" where the page has not been seen.
"""

VERIFIED = "VERIFIED"
HISTORICAL = "VERIFIED (HISTORICAL)"  # the brief writes "VERIFIED, HISTORICAL" with a dash; written without one per the house style
PENDING = "PENDING PRIMARY DOCUMENT"
UNVERIFIED = "UNVERIFIED"
CONFLICT = "CONFLICTING SOURCES"
NOT_USED = "NOT USED"
USABLE = (VERIFIED, HISTORICAL)
PTV = "PAGE TO VERIFY"

MTR = dict(source="Off-Grid Solar Market Trends Report 2024", publisher="ESMAP / World Bank, with GOGLA and Dalberg (as reported)",
           date="October 2024 (as reported in the client extractions; to verify)", document="MTR 2024 (primary PDF not held by the project)", page=PTV,
           url="https://www.esmap.org/sites/default/files/esmap-files/2024-Off-Grid-Solar-Market-Trends-Report.pdf (not opened from this environment)",
           evidence="Client extractions from the report, 3 Oct 2026 and 4 Oct 2026 (the second gives chapter page ranges only, not pages per figure); primary PDF not held", grade="B", status=PENDING)
PERF26 = dict(source="PAYGo PERFORM KPIs: Industry Standards for End-User Asset Financing, Technical Guide", publisher="GOGLA (PAYGo PERFORM initiative)",
              date="June 2026", document="617b6faf-PAYGo-PERFORM-KPIs_Technical-Guide_2026.pdf (42 pages)", url="Project file (uploaded 3 Oct 2026)",
              evidence="Industry standard, read in the project file", grade="B", status=VERIFIED)
PERF21 = dict(source="PAYGo PERFORM Technical Guide: Financial, Operational, and Portfolio Quality KPIs for the PAYGo solar industry",
              publisher="CGAP, GOGLA, IFC Lighting Global", date="July 2021", document="a30c1991-2021_07_Technical_Guide_PAYGo_PERFORM_KPI.pdf (85 pages)",
              url="Project file (uploaded 3 Oct 2026; a byte-identical second copy was also uploaded)", evidence="Industry standard (superseded), read in the project file",
              grade="B", status=HISTORICAL)
MKUK = dict(source="M-KOPA UK LIMITED, Annual Report and Accounts, year ended 31 December 2024", publisher="Companies House (company 10229661)",
            date="Approved 20 Jun 2025; filed 25 Sep 2025", document="245b3bf6-companies_house_document.pdf (34 pages, scanned)", url="Project file (uploaded 3 Oct 2026)",
            evidence="Audited statutory accounts (auditor KLSA LLP), read page by page", grade="A", status=VERIFIED)
BC = dict(source="Beyond Connections: Energy Access Redefined (Technical Report 008/15, conceptualization report)", publisher="ESMAP / World Bank",
          date="July 2015", document="BEYOND CONNECTIONS  Energy Access Redefined.pdf (244 pages; author's Google Drive, SHA-256 9d23881a...c1d26b)",
          url="Project file (retrieved from the author's Drive, 4 Oct 2026)", evidence="Read in the document", grade="B", status=VERIFIED)
TC = "https://techcabal.com/2025/10/07/m-kopa-turns-first-ever-profit-revenue-surges-66-416/"
KWS = "https://kenyanwallstreet.com/m-kopa-posts-first-ever-profit-bets-on-e-mobility-for-next-growth-phase/"


def r(ref, claim, value, unit, period, base=None, **kw):
    d = dict(base or {})
    d.update(ref=ref, claim=claim, value=value, unit=unit, period=period)
    d.update(kw)
    for k in ("source", "publisher", "date", "document", "page", "section", "url", "evidence", "grade", "status", "book", "model", "notes", "key", "legacy"):
        d.setdefault(k, "")
    return d


REGISTER = [
    # ---------------------------------------------------------------- E1: ESMAP MTR 2024 (client extraction, pages to verify)
    r("E1-01", "Off-grid solar products sold in 2022-2023 exceed 50 million, above the previous record of 47 million in 2019", ">50", "million units", "2022-2023", MTR,
      book="Planned: Ch 1, 11 (market context)", model="None"),
    r("E1-02", "Global off-grid solar sector turnover", 3.9, "USD bn", "2022", MTR, book="Planned: Ch 1", model="None"),
    r("E1-03", "Global off-grid solar sector turnover", 3.8, "USD bn", "2023", MTR, book="Planned: Ch 1", model="None",
      notes="Reported as about 15% above the pre-COVID level despite inflation, currency depreciation and lower purchasing power."),
    r("E1-04", "Share of off-grid solar products sold by GOGLA affiliates on PAYGo terms", 0.39, "%", "2023 (24% in 2018)", MTR, book="Planned: Ch 1", model="None"),
    r("E1-05", "Share of small SHS sold on PAYGo terms", 0.67, "%", "2023 (year to verify)", MTR, book="Planned: Ch 1", model="None"),
    r("E1-06", "Share of large SHS sold on PAYGo terms", 0.96, "%", "2023 (year to verify)", MTR, book="Planned: Ch 1", model="None"),
    r("E1-07", "Affordability convention: monthly payment of at most 5% of household income is affordable; up to 10% is affordable 'at a stretch'",
      "5% / 10%", "share of income", "Methodology", MTR, book="Planned: Ch 2.3, 13.7", model="Context for Consumer_Risk threshold (model threshold stays a model policy assumption)",
      notes="A methodological convention of the report, not a regulation or a universal empirical limit. The model's default 10% corresponds to the upper bound of 'at a stretch'."),
    r("E1-08", "Population without access for whom a PAYGo Tier 1 product is affordable / at a stretch / not affordable (global)", "22% / 27% / 51%", "% of population", "Report year", MTR,
      book="Ch 2.3", model="None",
      notes="The second client extraction states 51% affordable or at a stretch and 49% unaffordable, which does not follow from its own figures (22% + 27% = 49%). The register keeps 51% not affordable; check against the report."),
    r("E1-09", "Same measure for a Tier 2 product (global)", "1% / 2% / 97%", "% of population", "Report year", MTR, book="Planned: Ch 2", model="None"),
    r("E1-10", "Sub-Saharan Africa: share of the population without access for whom PAYGo Tier 1 is affordable; share for whom it is affordable at a stretch", "16% / 46%",
      "% of population", "Report year", MTR, book="Ch 2.3", model="None",
      notes="DEFINITION TO VERIFY: the global split (22% + 27% = 49%) is incremental. The second client extraction reads 46% as additional to 16% (62% in total); to check in the report. Not to be confused with the 62% average collection rate (E1-14)."),
    r("E1-11", "Share of people without access living in low-density rural, remote or conflict-affected areas", 0.82, "%", "Report year", MTR, book="Planned: Ch 5", model="None"),
    r("E1-12", "Cost of supplying a product in hard-to-reach areas: up to 57% higher; Tier 1 PAYGo example about USD 127 on average against about USD 199", "up to 57%",
      "% / USD", "Report year", MTR, book="Ch 5.6", model="Candidate for a remote-area cost-to-serve lever (not implemented)"),
    r("E1-13", "An increase of 2 to 3 percentage points in the cost of capital can raise the end-user price by about 5% in some contexts", "about 5%", "% of price",
      "Report year", MTR, book="Planned: Ch 4, 11", model="Candidate link from cost of funds to price (not implemented)"),
    r("E1-14", "Average PAYGo collection rate across reporting companies", 0.62, "%", "2021-2023 (reported as stable at about 62% over the period)", MTR,
      book="Ch 1.6, 7.4, 15, 16 (as about 62% from 2021 to 2023, reported)", model="Calibration reference (credit), suspended until VERIFIED",
      notes="Both client extractions give the average as about 62% across 2021 to 2023; earlier search snippets gave 62% in 2023, in line with 2021. The book says the rate stayed at about 62% over 2021 to 2023, which fits both readings. Reported definition: payments received over payments expected in the period. A collection rate, not the PAYGo PERFORM 2026 Repayment Rate. Definition (numerator, denominator, deposits, weighting) to verify before any comparison with the model's operational collection rate.",
      key="ESMAP / World Bank|Sector PAYGo collection rate", legacy="SR19"),
    r("E1-15", "Collection rate by quartile: top quartile 75-80%; bottom quartile below 50%", "75-80% / <50%", "%", "2021-2023", MTR, book="Ch 1.6, 7.4", model="None"),
    r("E1-16", "Share of companies with write-off ratio plus RAR30 between 30% and 50%", "about 50% (18% in 2021)", "% of companies", "2023 vs 2021", MTR,
      book="Ch 1.6, 15 (as half of companies, reported)", model="None",
      notes="Both client extractions concern half of companies within a ratio band, not half of customers; the earlier book wording about customers has been withdrawn. RAR30 and write-off ratio are 2021 PERFORM portfolio quality metrics (E2a-03, E2a-04)."),
    r("E1-17", "Off-grid solar investment", "773 / 1,200 (746 in 2022; 425 in 2023)", "USD m", "2020-2021 / 2022-2023", MTR, book="Planned: Ch 11", model="None",
      notes="Large single transactions drive the annual figures. Internal consistency check: 746 + 425 = 1,171, about USD 1.2bn."),
    r("E1-18", "Debt share of off-grid solar investment, excluding one large Sun King equity transaction", 0.75, "%", "2021-2023", MTR, book="Planned: Ch 11", model="None"),
    r("E1-19", "Share of 2023 investment in local currency", "more than one third", "% of investment", "2023", MTR, book="Ch 11.3", model="None"),
    r("E1-20", "Off-balance-sheet financing, including local-currency securitisations matched to receivables currency, became a significant source of funding", "qualitative",
      "text", "Report period", MTR, book="Planned: Ch 12", model="None"),
    r("E1-21", "Share of small and medium off-grid solar companies citing access to finance as a significant challenge", "more than 60%", "% of companies", "Report period", MTR,
      book="Planned: Ch 11", model="None"),
    r("E1-22", "Cost of financing as a share of total costs of off-grid solar companies in low-income markets", "about 14%", "% of total costs", "Report period", MTR,
      book="Planned: Ch 9, 11", model="None"),
    r("E1-23", "Results-based financing committed since 2018; disbursed", "733 / about 350", "USD m", "2018 to report date", MTR, book="Ch 13.1", model="None"),
    r("E1-24", "Financing need to serve, by 2030, the 398 million people for whom off-grid solar is the least-cost option (about 41% of the about 969 million people to be electrified)",
      "about 21", "USD bn", "To 2030", MTR, book="Ch 13.7", model="None",
      notes="About half public, half private; public funding from about USD 1bn in 2025 to about USD 2.1bn a year in 2028-2030; governments about 30-40% of total cost (client extraction). The register previously read 41% of households; the second extraction gives 41% of people."),
    r("E1-25", "People reached by off-grid solar on the current trajectory, of the 398 million least-cost population", "216 million (about 54%), about USD 9bn", "people / USD",
      "To 2030", MTR, book="Planned: Ch 1, 13", model="None"),
    r("E1-26", "Share of PAYGo customers facing payment difficulties", "about 1 in 4 (fewer than 1 in 5 about four years earlier)", "share of customers", "2023", MTR,
      book="Ch 7.4", model="None", notes="Second client extraction, 4 Oct 2026. Definition of payment difficulty to verify."),
    r("E1-27", "Affordability method assumptions for a Tier 1 PAYGo product: 20% deposit, 2 year repayment, 40% annual interest", "20% / 2 years / 40%", "assumptions",
      "Methodology", MTR, book="Ch 2.3", model="None",
      notes="Assumptions of the report's method, not market evidence. Reported cash prices of USD 71.61 (urban) and USD 198.75 (rural), 2017 PPP dollars, and USD 465 for Tier 2, to verify."),
    r("E1-28", "Composition of the about USD 21.3bn universal access need: debt, equity, grants, affordability gap (the gap associated with about 240 million people)",
      "6.4 / 4.3 / 1.5 / 9.2", "USD bn", "2025-2030", MTR, book="Ch 13.7", model="None",
      notes="Internal check: the components add to USD 21.4bn against a stated USD 21.3bn (rounding to verify); 240 of 398 million is about 60%, stated as about 59%."),
    r("E1-29", "Local currency debt financing as a share of off-grid solar investment, 2017-2023 average", "about 20%", "% of investment", "2017-2023", MTR,
      book="Ch 11.3", model="None"),
    r("E1-30", "World Bank lending to governments for off-grid solar, FY2024", "about 660 or 626", "USD m", "FY2024", MTR, status=CONFLICT, book="None", model="None",
      notes="The second client extraction reports both figures in different sections of the report. Not used until checked in the document."),
    # ---------------------------------------------------------------- E2: PERFORM 2026 (current standard)
    r("E2-01", "The PAYGo PERFORM KPIs are five: RR Paid vs Plan (PvP); RR Paid vs Financed (PvFin); RR PvP @90 Days; RR PvP @2x; Ownership Rate @2x", "5 KPIs", "text",
      "Current", PERF26, page="8", section="Summary Guide: KPI Definitions, Formulas & Key Calculation Rules", book="Ch 7 (to be restructured), Annex A", model="Planned PERFORM 2026 block (change M3)"),
    r("E2-02", "Collection Rate and other substitute metrics must not be used in place of the Repayment Rate calculation; the only accepted alternative basis is cumulative arrears",
      "rule", "text", "Current", PERF26, page="10", section="Repayment Rate: Core Calculation Rules, rule 3A and 3B", book="Ch 7", model="KPIs labels (change M3)"),
    r("E2-03", "Repayment Rate rules: excludes deposits and prepayments; includes arrears payments and write-offs; cumulative since contract start after any free-use period; instalments normalised to daily equivalents; payments recognised pro rata when applied to due instalments",
      "rules", "text", "Current", PERF26, page="9-10", section="Repayment Rate: Definition, Formula; Core Calculation Rules", book="Ch 6, 7", model="Planned PERFORM 2026 block (change M3)"),
    r("E2-04", "Ownership Rate @2x: proportion of contracts fully paid as of twice the contract term, among contracts that have reached at least 2x", "definition", "text", "Current",
      PERF26, page="8; 16-18", section="Ownership Rate", book="Ch 7, 13", model="Vintage_Dashboard, RBF_Engine (ownership-linked RBF)"),
    r("E2-05", "At a Glance companion: core RR calculation rules (1) exclude deposits (2) exclude prepayments (3) include arrears payments (4) include write-offs (5) cumulative since contract start",
      "rules", "text", "Current", dict(PERF26, source="PAYGo PERFORM KPIs, At a Glance", document="70d4c519-PAYGo-PERFORM-KPIs_At-A-Glance_2026.pdf (12 pages)"),
      page="5", book="Ch 7", model="None"),
    r("E2-06", "PAYGo PERFORM framework attributed to CGAP, GOGLA and Lighting Global with collection rate and receivables at risk as framework KPIs", "framework", "text", "2021",
      dict(PERF21), page="Front matter", status=HISTORICAL, book="Ch 7.1", model="Previous register entry (SR21) replaced by E2-01 to E2-05 and E2a",
      legacy="SR21", notes="The 2021 framing is historical; the current standard is E2 (June 2026)."),
    # ---------------------------------------------------------------- E2a: PERFORM 2021 (historical)
    r("E2a-01", "Collection Rate: collected receivables payments over receivables payments due for the period, excluding deposits", "definition", "text", "2021", PERF21,
      page="18-19", section="Portfolio Quality Indicators, 1.3 Collection Rate", book="Ch 7.2", model="KPIs (operational collection rate), Covenants"),
    r("E2a-02", "Receivables at Risk by consecutive days unpaid, RAR(CDU): gross outstanding receivables more than X consecutive days unpaid over gross outstanding receivables; suggested ageing RAR30, 90, 120, 180, 365",
      "definition", "text", "2021", PERF21, page="21-23", section="1.4a Receivables at Risk using Consecutive Days Unpaid", book="Ch 7.2", model="KPIs (model RaR is a curve-based proxy, not this definition)"),
    r("E2a-03", "Receivables at Risk by collection-rate threshold: gross outstanding receivables of customers with collection rate below Y%", "definition", "text", "2021", PERF21,
      page="24", section="1.4b", book="None", model="None"),
    r("E2a-04", "Write-off Ratio: outstanding receivables of contracts written off in the period over average outstanding receivables", "definition", "text", "2021", PERF21,
      page="27-28", section="Write-off Ratio", book="Ch 7.2", model="KPIs write-off rate (model definition differs: missed instalments written off as due)"),
    # ---------------------------------------------------------------- Other PERFORM documents held
    r("E2b-01", "PAYGo Accounting Brief: revenue recognition (IFRS 15), write-off and provisioning (IFRS 9) practice for PAYGo", "reference", "text", "2021",
      source="PAYGo Accounting Brief", publisher="PAYGo PERFORM initiative (CGAP, GOGLA, IFC Lighting Global); authored by MFR", date="October 2021",
      document="7d89d499-PAYGo-PERFORM-Accounting-Brief.pdf (67 pages)", page=PTV, section="Revenue recognition; Write-off and provisioning policy",
      url="Project file", evidence="Practitioner guidance, held; not an accounting standard", grade="B", status=NOT_USED, book="Planned: Ch 8 (context only)", model="None"),
    r("E2c-01", "Guidance for Company Analysis, v3 Beta", "reference", "text", "2025", source="PAYGo PERFORM: Guidance for Company Analysis, v3 Beta",
      publisher="GOGLA (PAYGo PERFORM)", date="July 2025", document="bb716947-PAYGo-PERFORM_Guidance-for-Company-Analysis_v3-beta.pdf (63 pages)", page=PTV,
      url="Project file", evidence="Beta guidance, held", grade="B", status=NOT_USED, book="Planned: Ch 15 (beta status to be stated)", model="None"),
    r("E2d-01", "Guidance for PAYGo RBF Funds: metrics and incentives for sustained energy access", "reference", "text", "2026", source="Guidance for PAYGo RBF Funds",
      publisher="PAYGo PERFORM initiative", date="April 2026", document="833f21cf-Guidance-for-PAYGo-RBFs-Metrics-Incentives-for-Sustained-Energy-Access.pdf (27 pages)",
      page=PTV, url="Project file", evidence="Institutional guidance, held", grade="B", status=NOT_USED, book="Planned: Ch 13", model="Planned: RBF_Engine review (change M11)",
      legacy="SR22", notes="Replaces the SR22 list item for this document. The other GOGLA publications listed in SR22 are not held."),
    # ---------------------------------------------------------------- E3: MTF
    r("E3-01", "Multi-Tier Framework household electricity supply, capacity: Tier 1 min 3 W or 12 Wh a day; Tier 2 min 50 W or 200 Wh; Tier 3 min 200 W or 1.0 kWh; Tier 4 min 800 W or 3.4 kWh; Tier 5 min 2 kW or 8.2 kWh",
      "T1-T5", "text", "2015", BC, page="20 (report page 6)", section="Table ES.1, Multi-tier Matrix for Measuring Access to Household Electricity Supply",
      book="Ch 2.6", model="Products tier labels (capacity attribute only)", legacy="SR20"),
    r("E3-02", "Household electricity attributes are capacity, duration (daily and evening supply), reliability, quality, affordability, legality, and health and safety; the lowest tier among all attributes determines the household's overall tier",
      "rule", "text", "2015", BC, page="19 (report page 5)", section="Executive Summary", book="Ch 2.6", model="None"),
    r("E3-03", "Duration thresholds: Tier 1 min 4 hours a day and 1 evening hour; Tier 2 min 4 hours and 2 evening hours; affordability attribute met when a standard package of 365 kWh a year costs less than 5% of household income",
      "thresholds", "text", "2015", BC, page="20 (report page 6)", section="Table ES.1", book="Ch 2.6", model="None",
      notes="The MTF affordability test prices a standard consumption package, not a PAYGo instalment; it is a different measure from the payment burden in Ch 2.3."),
    # ---------------------------------------------------------------- E4: M-KOPA
    r("E4-01", "M-KOPA UK LIMITED revenue (sales of carbon credits)", 1712776, "GBP", "FY2024 (FY2023: 718,100)", MKUK, page="10 (filing page 8); 18 (filing page 16, note 2.1)",
      section="Statement of profit or loss; note 2.1 Sale of carbon credits", book="Planned: Ch 15 (as an illustration of entity checking)",
      model="Not used: different entity and activity; not a PAYGo benchmark",
      notes="UK research and development subsidiary; no employees; functional currency sterling; IFRS as adopted in the UK; not consolidated."),
    r("E4-02", "M-KOPA UK LIMITED profit for the year", 1040472, "GBP", "FY2024 (FY2023: 497,346)", MKUK, page="10 (filing page 8)", section="Statement of profit or loss",
      book="None", model="Not used"),
    r("E4-03", "M-KOPA UK LIMITED parent and ultimate parent: M-Kopa LLC (Delaware); M-Kopa Holdings Limited (London)", "text", "text", "FY2024", MKUK,
      page="3 (filing page 1)", section="Company information", book="Planned: Ch 15", model="None",
      notes="The project's benchmark files attribute the group figures to M-KOPA Holdings Ltd, Companies House 10891868. That number has not been checked against the register."),
    r("E4-04", "M-KOPA group revenue FY2024", 416, "USD m", "FY2024", source="News article citing 'UK filings'", publisher="TechCabal", date="7 Oct 2025", document="Web article",
      page=PTV, url=TC, evidence="Secondary report; entity and revenue line not identified", grade="C", status=CONFLICT,
      book="Ch 15 (presented as conflicting)", model="Market_Benchmark and Calibration: suspended", key="M-KOPA|Revenue", legacy="SR01",
      notes="Conflicts with E4-05 (USD 253.5m). Not supported by E4-01 (different entity). Resolvable only with the consolidated accounts of the reporting group entity."),
    r("E4-05", "M-KOPA group revenue FY2024", 253.5, "USD m", "FY2024", source="News article", publisher="Kenyan Wall Street", date="2025", document="Web article", page=PTV, url=KWS,
      evidence="Secondary report; may be a different revenue line", grade="C", status=CONFLICT, book="Ch 15 (presented as conflicting)", model="Not used"),
    r("E4-06", "M-KOPA group revenue growth", 0.66, "%", "FY2024 vs FY2023", source="News articles", publisher="TechCabal; Kenyan Wall Street", date="Oct 2025", document="Web articles",
      page=PTV, url=TC, evidence="Secondary report", grade="C", status=PENDING, book="None", model="Calibration growth reference: suspended", key="M-KOPA|Revenue growth", legacy="SR02"),
    r("E4-07", "M-KOPA group net profit", 9.2, "USD m", "FY2024", source="News article", publisher="TechCabal", date="7 Oct 2025", document="Web article", page=PTV, url=TC,
      evidence="Secondary report", grade="C", status=PENDING, book="Ch 15", model="Calibration net margin reference: suspended", key="M-KOPA|Net profit", legacy="SR03"),
    r("E4-08", "M-KOPA group net result, prior year", "-24.7 (or -20.6)", "USD m", "FY2023", source="News articles", publisher="TechCabal; Kenyan Wall Street", date="2025",
      document="Web articles", page=PTV, url=TC, evidence="Secondary reports that conflict", grade="C", status=CONFLICT, book="Ch 15", model="Not used", legacy="SR04"),
    # ---------------------------------------------------------------- E5, E6: Sun King, d.light
    r("E5-01", "Sun King cumulative solar loans", 1300, "USD m", "Cumulative to Jul 2025", source="Citi press release on the Sun King securitisation", publisher="Citigroup",
      date="2025", document="Press release (not read in this project)", page=PTV,
      url="https://www.citigroup.com/global/news/press-release/2025/citi-sun-king-securitization-deliver-solar-million-kenyans", evidence="Company disclosure recorded from earlier research",
      grade="B", status=PENDING, book="Ch 12, 15", model="Market_Benchmark (shown, flagged)", key="Sun King|Cumulative solar loans", legacy="SR05"),
    r("E5-02", "Sun King cumulative loan customers (cumulative, not active)", 10, "million", "Cumulative to Jul 2025", source="Citi press release", publisher="Citigroup", date="2025",
      document="Press release (not read)", page=PTV, url="https://www.citigroup.com/global/news/press-release/2025/citi-sun-king-securitization-deliver-solar-million-kenyans",
      evidence="Company disclosure recorded from earlier research", grade="B", status=PENDING, book="Ch 12, 15", model="Market_Benchmark (shown, flagged)",
      key="Sun King|Cumulative loan customers", legacy="SR06"),
    r("E5-03", "Sun King local-currency securitisation in Kenya", 130, "USD m", "May 2023", source="Sun King news release", publisher="Sun King", date="2023",
      document="News release (not read)", page=PTV,
      url="https://sunking.com/news-blog/sun-king-and-citi-close-first-130-million-securitisation-to-broaden-access-to-finance-for-off-grid-solar-in-kenya/",
      evidence="Company disclosure recorded from earlier research", grade="B", status=PENDING, book="Ch 3.11, 11, 12", model="None", legacy="SR07"),
    r("E5-04", "Sun King local-currency securitisation in Kenya (KES 20.1bn)", 156, "USD m", "Jul 2025", source="Citi release; trade press", publisher="Citigroup; pv magazine",
      date="29 Jul 2025", document="Release and article (not read)", page=PTV, url="https://www.pv-magazine.com/2025/07/29/sun-king-closes-156m-off-grid-solar-deal-in-kenya/",
      evidence="Company disclosure and secondary report recorded from earlier research", grade="B", status=PENDING, book="Ch 3.11, 11, 12", model="Market_Benchmark (shown, flagged)",
      key="Sun King|Securitisation 2025", legacy="SR08"),
    r("E5-05", "Sun King MSME bond", 6.5, "USD m", "2024", source="None found", publisher="", date="", document="", page="", url="", evidence="No public source found",
      grade="D", status=NOT_USED, book="None", model="Excluded", legacy="SR09"),
    r("E6-01", "d.light securitisation purchasing capacity since 2020 (five facilities; purchasing capacity, not debt raised)", 718, "USD m", "2020 to Jul 2024",
      source="News article", publisher="Techpoint Africa", date="17 Jul 2024", document="Web article", page=PTV, url="https://techpoint.africa/2024/07/17/d-light-raises-176m/",
      evidence="Secondary report", grade="C", status=PENDING, book="Ch 3.11, 11, 12, 15", model="Market_Benchmark (shown, flagged)",
      key="d.light|Securitisation purchasing capacity since 2020", legacy="SR10"),
    r("E6-02", "d.light multi-currency securitisation facility", 176, "USD m", "Jul 2024", source="News articles", publisher="Techpoint Africa; WeeTracker", date="17 Jul 2024",
      document="Web articles", page=PTV, url="https://techpoint.africa/2024/07/17/d-light-raises-176m/", evidence="Secondary report", grade="C", status=PENDING,
      book="Ch 12", model="Market_Benchmark (shown, flagged)", key="d.light|Securitisation facility 2024", legacy="SR11"),
    r("E6-03", "d.light revenue growth", 0.41, "%", "H1 2023 vs H1 2022", source="d.light press release", publisher="d.light via PR Newswire", date="Sep 2023",
      document="Press release (not read)", page=PTV,
      url="https://www.prnewswire.co.uk/news-releases/dlight-revenues-surge-by-41-percent-in-first-six-months-of-2023-driven-by-143-percent-growth-in-nigeria-301919233.html",
      evidence="Company disclosure recorded from earlier research", grade="B", status=PENDING, book="None", model="Market_Benchmark (shown, flagged)",
      key="d.light|Revenue growth", legacy="SR12"),
    r("E6-04", "d.light revenue (third-party estimate)", 301.2, "USD m", "2023", source="Company database", publisher="bitscale.ai", date="n/d", document="Web page", page="",
      url="https://www.bitscale.ai/directory/dlight", evidence="Third-party estimate, method not stated", grade="D", status=NOT_USED, book="None", model="Excluded", legacy="SR13"),
    # ---------------------------------------------------------------- E7: BBOXX
    r("E7-01", "BBOXX LTD (07177839): appointment of administrators", "19 May 2025", "date", "2025", source="Notice of appointment of administrators",
      publisher="The Gazette", date="2025 (to verify)", document="Gazette notice 4891954 (not held)", page="Notice", url="https://www.thegazette.co.uk/notice/4891954 (not opened from this environment)",
      evidence="Date recorded from earlier research (Gazette and administrator's announcement); notice not read in this project", grade="A", status=PENDING,
      book="Ch 1.6, 14", model="Company_Cases text", legacy="SR15",
      notes="The date must be the date of appointment stated in the formal notice, not a petition, hearing, publication or creditors' meeting date."),
    r("E7-02", "BBOXX LTD (07177839): latest filed accounts made up to 31 Dec 2022; FY2023 accounts overdue; status in administration", "text", "text", "2025",
      source="Companies House register", publisher="Companies House", date="2025 (to verify)", document="Register entry (not opened)", page="",
      url="https://find-and-update.company-information.service.gov.uk/company/07177839 (not opened from this environment)",
      evidence="Recorded from earlier research", grade="A", status=PENDING, book="Ch 1.6", model="Company_Cases text", legacy="SR14"),
    # ---------------------------------------------------------------- E8 to E10 and others
    r("E8-01", "Off-grid solar investment in 2024, down about 30%", 299, "USD m", "2024", source="GOGLA investment data (as reported)", publisher="GOGLA", date="2025 (to verify)",
      document="Not held", page=PTV, url="", evidence="Secondary report", grade="B", status=PENDING, book="Ch 11.1, 14", model="None",
      notes="Consistency only, not verification: E1-17 gives USD 425m for 2023, and 425 x 0.7 is about 298."),
    r("E9-01", "ZOLA Electric financing round (USD 45m equity, USD 45m debt)", 90, "USD m", "Sep 2021", source="News article", publisher="TechCrunch", date="23 Sep 2021",
      document="Web article", page=PTV, url="https://techcrunch.com/2021/09/23/zola-electric-closes-90m-funding-round-to-scale-technology-and-enter-new-markets",
      evidence="Secondary report", grade="C", status=PENDING, book="None", model="Market_Benchmark (shown, flagged)", key="ZOLA Electric|Financing round", legacy="SR18"),
    r("E10-01", "SEforALL Universal Energy Facility pays results-based finance per verified connection", "qualitative", "text", "n/a", source="SEforALL (as reported)",
      publisher="SEforALL", date="to verify", document="Not held", page=PTV, url="", evidence="Secondary description", grade="B", status=PENDING, book="Ch 13.2", model="None"),
    r("X-01", "Pawame SHS financed", 18700, "units", "n/a", source="None found", evidence="No public source found", grade="D", status=NOT_USED, book="None", model="Excluded",
      key="Pawame|SHS financed", legacy="SR16"),
    r("X-02", "Pawame active customers", 16000, "customers", "n/a", source="None found", evidence="No public source found", grade="D", status=NOT_USED, book="None", model="Excluded",
      key="Pawame|Active customers", legacy="SR17"),
    r("X-03", "IFC / AFC material on PAYGo receivables financing", "reference", "text", "various", source="Not identified", evidence="Listed for retrieval", grade="D", status=NOT_USED,
      book="None", model="None", legacy="SR23"),
]


def by_key():
    return {d["key"]: d for d in REGISTER if d["key"]}


BOOK_CLAIM_CHECKS = [
    ("Ch 1.6, 7.4, 15, 16", "Sector PAYGo collection rate stayed at about 62% from 2021 to 2023", "E1-14", PENDING,
     "Two client extractions agree on the 2021-2023 period; the pages and definition must still be checked against the report."),
    ("Ch 1.6, 7.4, 15", "About half of PAYGo customers had been written off or were more than 30 days late", "E1-16", CONFLICT,
     "The client extraction concerns about half of companies with write-off ratio plus RAR30 between 30% and 50%. Withdraw the book's wording."),
    ("Ch 15", "M-KOPA FY2024 revenue USD 416m or USD 253.5m; net profit USD 9.2m", "E4-01 to E4-08", CONFLICT,
     "The primary filing held is a UK subsidiary (GBP 1.7m revenue from carbon credits). Remove the '6.1 times' diagnostic; keep the conflict as an illustration of entity checking."),
    ("Ch 1.6, 14", "BBOXX LTD entered administration on 19 May 2025", "E7-01", PENDING, "Keep with the pending caveat until the Gazette notice is read."),
    ("Ch 11.1, 14", "GOGLA: off-grid solar investment about USD 299m in 2024, down about 30%", "E8-01", PENDING, "Keep with the secondary caveat."),
    ("Ch 7.1", "PERFORM standardises collection rate, receivables at risk and write offs, later adding repayment and ownership rates", "E2-01, E2-06", HISTORICAL,
     "Restructure Chapter 7 on the 2026 standard (change B4)."),
]
