"""How buyers can access government securities: procedural facts quoted from official pages.

Every route below is backed by a verbatim excerpt from the cited official page, retrieved on
VERIFIED_ON. Nothing here is advice, and access is never guaranteed. Fees and taxes are not
stated on these pages, so they are left empty ("Not available").

Coverage: CEMAC (BEAC), WAEMU (UMOA-Titres), Kenya (CBK), and since VERIFIED_ON_2: Nigeria (DMO),
Ghana (Bank of Ghana), South Africa (National Treasury), Tanzania (BoT), Uganda (BoU) and Rwanda
(BNR). Routes for the other countries are not yet documented. A route may carry its own
"verified_on" date; otherwise VERIFIED_ON applies.

Several of the newer sources are dated documents (calls for tender, prospectuses, guidelines):
the document is named in instrument_notes, and terms may change at each issue.
"""

from app.models.enums import InstrumentType, MonetaryZone

VERIFIED_ON = "2026-10-03"
VERIFIED_ON_2 = "2026-10-04"  # Nigeria, Ghana, South Africa, Tanzania, Uganda, Rwanda

BEAC_URL = "https://www.beac.int/m-des-titres-publics/presentation-generale/"
UMOA_MARKET_URL = "https://www.umoatitres.org/a-propos-des-titres-publics/le-marche/"
UMOA_RETAIL_URL = "https://www.umoatitres.org/fr/particuliers/"
CBK_BILLS_URL = "https://www.centralbank.go.ke/securities/treasury-bills/"

_BEAC_ACTORS = (
    "les Spécialistes en Valeurs du Trésor (SVT) qui sont les établissements de crédit agréés, "
    "comme teneurs du marché ; les Directions Nationales de la BEAC, en charge de l'organisation "
    "matérielle des adjudications ; les investisseurs : personnes physiques et morales résidentes et "
    "non résidentes ; la CRCT, en qualité de Dépositaire Central"
)
_BEAC_RETAIL = (
    "Permettre aux entreprises et aux particuliers de souscrire à des instruments financiers "
    "rentables, peu risqués et liquides par le canal des institutions habilités"
)
_UMOA_DIRECT = (
    "Les participants directs à ce jour sont les établissements de crédit, les SGI et les organismes "
    "financiers régionaux disposant d'un compte de règlement dans les livres de la Banque Centrale "
    "(article 4 du règlement n°06/2013/CM/UEMOA). Les autres investisseurs, personnes physiques ou "
    "morales peuvent souscrire par l'intermédiaire des établissements de crédit et des SGI de la zone UEMOA."
)
_UMOA_TARGETED = (
    "Tout investisseur qui souhaite acquérir le titre mis en adjudication peut souscrire par "
    "l'intermédiaire du SVT de l'Etat émetteur."
)
_CBK_DIRECT = (
    "Individuals and Corporate bodies can invest in Treasury bills without going through an "
    "intermediary by accessing https://dhowcsd.centralbank.go.ke/ and registering for CSD accounts. "
    "Investors inter alia individuals and corporates can equally invest via their respective Kenyan "
    "commercial banks and investment banks as custodials."
)
_CBK_MIN = (
    "The minimum face value purchase for Treasury bills and bonds is Kshs. 50,000.00 for "
    "non-competitive bids and Kshs. 2,000,000.00 for competitive bids, and must be invested in "
    "denominations of Kshs. 50,000.00."
)

# Zone-level routes, expanded to every member country by the loader.
ZONE_ROUTES: list[dict] = [
    {
        "zone": MonetaryZone.CEMAC,
        "instrument_type": InstrumentType.TREASURY_BILL,
        "investor_type": "Personnes physiques et morales, résidentes et non résidentes",
        "eligibility": "Investisseurs personnes physiques et morales, résidents et non résidents.",
        "primary_dealer": "Spécialistes en Valeurs du Trésor (SVT) : établissements de crédit agréés.",
        "account_requirement": "Conservation auprès de la CRCT (dépositaire central), via un intermédiaire habilité.",
        "submission_method": "Souscription par le canal des institutions habilitées (SVT) ; adjudications organisées par les Directions Nationales de la BEAC.",
        "settlement_method": "Règlement-livraison par la CRCT.",
        "instrument_notes": "BTA : 13, 26 et 52 semaines ; valeur nominale 1 million de francs CFA ; intérêts précomptés.",
        "source_url": BEAC_URL,
        "quotes": [
            _BEAC_ACTORS,
            _BEAC_RETAIL,
            "les BTA, émis pour des durées de 13, 26 et 52 semaines, dont la valeur nominale est fixée à "
            "1 million de francs CFA et dont les intérêts sont précomptés",
        ],
    },
    {
        "zone": MonetaryZone.CEMAC,
        "instrument_type": InstrumentType.TREASURY_BOND,
        "investor_type": "Personnes physiques et morales, résidentes et non résidentes",
        "eligibility": "Investisseurs personnes physiques et morales, résidents et non résidents.",
        "primary_dealer": "Spécialistes en Valeurs du Trésor (SVT) : établissements de crédit agréés.",
        "account_requirement": "Conservation auprès de la CRCT (dépositaire central), via un intermédiaire habilité.",
        "submission_method": "Souscription par le canal des institutions habilitées (SVT) ; adjudications organisées par les Directions Nationales de la BEAC.",
        "settlement_method": "Règlement-livraison par la CRCT.",
        "instrument_notes": "OTA : durée de 2 ans ou plus ; valeur nominale 10 000 francs CFA ; intérêts annuels.",
        "source_url": BEAC_URL,
        "quotes": [
            _BEAC_ACTORS,
            "les OTA, émises pour des durées supérieures ou égales à deux ans, pour une valeur nominale de "
            "10 000 francs CFA et dont les intérêts sont payables annuellement",
        ],
    },
    {
        "zone": MonetaryZone.WAEMU,
        "instrument_type": InstrumentType.TREASURY_BILL,
        "investor_type": "Particuliers, entreprises et organisations (via intermédiaire)",
        "eligibility": "Participants directs : établissements de crédit, SGI, organismes financiers régionaux ayant un compte de règlement à la BCEAO. Autres investisseurs : via ces intermédiaires.",
        "primary_dealer": "SVT de l'État émetteur (obligatoire pour les adjudications ciblées).",
        "account_requirement": "Compte auprès d'un établissement de crédit ou d'une SGI de la zone UEMOA.",
        "submission_method": "Soumission par l'intermédiaire d'un établissement de crédit ou d'une SGI ; adjudications organisées par UMOA-Titres.",
        "settlement_method": None,
        "instrument_notes": "BAT : maturité inférieure à 2 ans ; intérêts précomptés.",
        "source_url": UMOA_MARKET_URL,
        "quotes": [
            _UMOA_DIRECT,
            _UMOA_TARGETED,
            "Les Bons Assimilables du trésor «BAT» sont des titres de créances à court terme émis par l'Etat "
            "par voie d'adjudication. Maturité du Titre : inférieure à 2 ans",
        ],
    },
    {
        "zone": MonetaryZone.WAEMU,
        "instrument_type": InstrumentType.TREASURY_BOND,
        "investor_type": "Particuliers, entreprises et organisations (via intermédiaire)",
        "eligibility": "Participants directs : établissements de crédit, SGI, organismes financiers régionaux ayant un compte de règlement à la BCEAO. Autres investisseurs : via ces intermédiaires.",
        "primary_dealer": "SVT de l'État émetteur (obligatoire pour les adjudications ciblées).",
        "account_requirement": "Compte auprès d'un établissement de crédit ou d'une SGI de la zone UEMOA.",
        "submission_method": "Soumission par l'intermédiaire d'un établissement de crédit ou d'une SGI ; adjudications organisées par UMOA-Titres.",
        "settlement_method": None,
        "instrument_notes": "OAT : maturité indiquée « supérieure à 3 ans » sur la page source.",
        "source_url": UMOA_MARKET_URL,
        "quotes": [
            _UMOA_DIRECT,
            "Les Obligations Assimilables du Trésor « OAT » sont des titres de créances à moyen et long terme, "
            "émis par l'Etat par voie d'adjudication. Maturité du Titre : supérieure à 3 ans",
        ],
    },
]

COUNTRY_ROUTES: list[dict] = [
    {
        "iso3": "KEN",
        "instrument_type": instrument,
        "investor_type": "Particuliers et entreprises (en direct ou via une banque)",
        "eligibility": "Particuliers et entreprises : en direct sans intermédiaire, ou via une banque commerciale ou une banque d'investissement kényane.",
        "primary_dealer": "Aucun intermédiaire obligatoire ; banques commerciales et banques d'investissement kényanes possibles comme dépositaires.",
        "account_requirement": "Compte CSD ouvert sur le portail DhowCSD de la Banque centrale du Kenya.",
        "submission_method": "Offres via l'application mobile ou le portail DhowCSD. Minimum : 50 000 KES (non compétitif) ou 2 000 000 KES (compétitif), par tranches de 50 000 KES.",
        "settlement_method": None,
        "instrument_notes": "Minimum de valeur faciale : 50 000 KES (offre non compétitive), 2 000 000 KES (offre compétitive).",
        "source_url": CBK_BILLS_URL,
        "quotes": [_CBK_DIRECT, _CBK_MIN],
    }
    for instrument in (InstrumentType.TREASURY_BILL, InstrumentType.TREASURY_BOND)
]

# --- Added on VERIFIED_ON_2: English-language official sources (quotes kept verbatim). ---

DMO_FGN_URL = "https://www.dmo.gov.ng/fgn-bonds"
BOG_GUIDE_URL = "https://www.bog.gov.gh/wp-content/uploads/2020/12/Primary-Dealers-and-Bond-Market-Specialists-Guidelines-1.pdf"
RSA_RETAIL_URL = "https://www.rsaretailbonds.gov.za/assets/docs/2023_RSA_RSB_Pamphlet_Fixed_Rate_Bond_Final.pdf"
BOT_BILL_URL = "https://www.bot.go.tz/Adverts/TBills/en/2026100209430069.pdf"
BOT_BOND_URL = "https://www.bot.go.tz/Adverts/TBonds/en/2026092414085433.pdf"
BOU_BILL_URL = "https://bou.or.ug/uploads/Invitation_to_Tender_for_Treasury_Bills_Issue_No_1235_Auction_scheduled_for_30_Sep_2026_71dcc6c2d4.pdf"
BOU_BOND_URL = "https://bou.or.ug/uploads/General_Prospectus_for_Bond_Issuances_2025_a0ad4f614e.pdf"
BNR_BOND_URL = "https://www.bnr.rw/documents/PROSPECTUS_OF_15-YEAR_BOND-REOPEN_ON_MARCH_16th_2026.pdf"

_BOT_CDP = (
    "Bids will be submitted online through Central Depository Participants (CDPs), and the process "
    "will be closed at 11.00 a.m. on the auction date"
)
_BOT_COMMON = {
    "iso3": "TZA",
    "investor_type": "Tous investisseurs, y compris étrangers (via un CDP)",
    "eligibility": "Tous les investisseurs, y compris les ressortissants étrangers.",
    "primary_dealer": "Central Depository Participants (CDP) : les offres passent par un CDP.",
    "account_requirement": None,
    "submission_method": "Offres soumises en ligne par l'intermédiaire d'un CDP, avant 11 h le jour de l'adjudication.",
    "settlement_method": None,
    "verified_on": VERIFIED_ON_2,
}
_BOG_COMMON = {
    "iso3": "GHA",
    "investor_type": "Investisseurs (via un PD, un BMS ou un dépositaire accrédité)",
    "account_requirement": None,
    "settlement_method": None,
    "source_url": BOG_GUIDE_URL,
    "verified_on": VERIFIED_ON_2,
}

COUNTRY_ROUTES += [
    {
        "iso3": "NGA",
        "instrument_type": InstrumentType.TREASURY_BOND,
        "investor_type": "Investisseurs (via un PDMM)",
        "eligibility": "Clients des PDMM : les PDMM soumettent les offres pour leur propre compte et pour le compte de leurs clients.",
        "primary_dealer": "Primary Dealer Market Makers (PDMM) désignés par le DMO.",
        "account_requirement": None,
        "submission_method": "Formulaire de souscription (auprès d'un PDMM ou téléchargé sur le site du DMO) remis à un PDMM ; adjudications mensuelles du DMO. Minimum : 50 001 000 NGN, puis multiples de 1 000 NGN.",
        "settlement_method": "Inscription électronique dans le système de règlement de titres dématérialisés de la Banque centrale du Nigeria, ou certificat si requis.",
        "instrument_notes": "Obligations FGN : adjudications mensuelles ; minimum 50 001 000 NGN puis multiples de 1 000 NGN ; intérêts semestriels.",
        "source_url": DMO_FGN_URL,
        "verified_on": VERIFIED_ON_2,
        "quotes": [
            "FGN Bonds Auctions Exercise is carried out by the DMO on a monthly basis. Primary Dealer Market "
            "Makers (PDMMs) empaneled by the DMO in 2006 are responsible for submitting bids for themselves "
            "and on behalf of their clients at the Auctions.",
            "Application forms can be obtained from any of the authorized dealers (PDMMs), or download from "
            "the DMO's website",
            "Complete the application forms and submit through any of the PDMMs.",
            "Minimum of N50,001,000.00 and multiple of N1,000.00, thereafter.",
            "FGN bonds purchase is confirmed by electronic registration in the Central Bank of Nigeria’s "
            "Scripless Securities Settlement System or by issue of certificates, where required.",
            "Interest is paid semi-annually until the maturity date when the principal amount is repaid.",
        ],
    },
    {
        **_BOG_COMMON,
        "instrument_type": InstrumentType.TREASURY_BILL,
        "eligibility": "Adjudication de gros réservée aux Primary Dealers agréés ; les autres investisseurs achètent et vendent sur le marché secondaire via des participants dépositaires accrédités.",
        "primary_dealer": "Primary Dealers (PD) : institutions financières agréées par la Bank of Ghana.",
        "submission_method": "Achat ou vente sur le marché secondaire par l'intermédiaire d'un participant dépositaire accrédité.",
        "instrument_notes": "Bons du Trésor : adjudication de gros réservée aux PD, qui achètent pour leur propre compte (lignes directrices de mars 2020).",
        "quotes": [
            "The Wholesale auction is the primary market for the issuance of GOG and BOG securities, and it "
            "is opened to only authorised dealers - Primary Dealers.",
            "Interested investors can buy or sell securities in the secondary market through accredited "
            "depository participants.",
            "Only financial institutions authorised by the BOG shall be eligible to participate in the "
            "wholesale auction as Primary Dealers.",
            "All PDs must participate in the primary auction of Treasury bills by purchasing bills for their "
            "own accounts and for their trading books.",
        ],
    },
    {
        **_BOG_COMMON,
        "instrument_type": InstrumentType.TREASURY_BOND,
        "eligibility": "Notes et obligations : les PD qui ne sont pas BMS, les autres entreprises et les particuliers passent leurs ordres par un Bond Market Specialist (BMS).",
        "primary_dealer": "Bond Market Specialists (BMS).",
        "submission_method": "Ordres transmis à un Bond Market Specialist (BMS).",
        "instrument_notes": "Notes et obligations : émises avec les Bond Market Specialists, qui remplacent les chefs de file (JBR) (lignes directrices de mars 2020).",
        "quotes": [
            "PDs that are not BMS, and other non-PD firms and individuals, are expected to place their orders "
            "through the BMS.",
            "The GOG by this guideline, replaces the JBRs with Bond Market Specialists (BMS) in the auction of "
            "GOG notes and bonds.",
        ],
    },
    {
        "iso3": "ZAF",
        "instrument_type": InstrumentType.TREASURY_BOND,
        "investor_type": "Particuliers : citoyens et résidents permanents sud-africains",
        "eligibility": "Citoyens sud-africains et résidents permanents titulaires d'un numéro d'identité sud-africain valide et d'un compte bancaire en Afrique du Sud ; pour un mineur, formulaire contresigné par un parent ou tuteur.",
        "primary_dealer": "Achat direct auprès du National Treasury (en ligne, au centre d'accueil ou par téléphone).",
        "account_requirement": "Compte bancaire dans une banque sud-africaine ; inscription auprès du National Treasury avec pièces justificatives.",
        "submission_method": "Inscription puis demande en ligne (secure.rsaretailbonds.gov.za), au centre d'accueil du National Treasury (40 Church Square, Pretoria) ou par téléphone pour les investisseurs déjà inscrits. Minimum : 1 000 ZAR par obligation.",
        "settlement_method": None,
        "instrument_notes": "Obligations d'épargne à taux fixe (Fixed Rate RSA Retail Savings Bonds) : 2, 3 ou 5 ans ; minimum 1 000 ZAR ; la brochure (2023) indique qu'aucun frais ni commission n'est payable.",
        "source_url": RSA_RETAIL_URL,
        "verified_on": VERIFIED_ON_2,
        "quotes": [
            "Any person with a valid South African identity number and a bank account at a South African bank "
            "can invest in the Fixed Rate RSA Retail Savings Bonds.",
            "Only South African citizens and permanent residents of the Republic who are in possession of a "
            "valid South African identity document, and who hold bank accounts with financial institutions in "
            "the Republic, shall be entitled to acquire RSA Retail Savings Bonds in terms hereof.",
            "If a minor (a person younger than eighteen years of age) applies for an investment, the "
            "application form must be countersigned by a parent or legal guardian.",
            "The minimum Capital Amount that may be invested at any time is an amount equal to R1, 000.00 "
            "(one thousand Rand) in respect of each RSA Retail Savings Bond.",
            "Visit website on https://secure.rsaretailbonds.gov.za and click register",
            "Visit the National Treasury, walk in centre in, 40 Church Square, Pretoria",
            "Telephonically (Only applicable to persons 18 years and older) who are existing investors and "
            "have already submitted their supporting documents",
            "What you see is what you get - no hidden costs, fees or commissions are payable.",
            "Investment terms: 2 years 3 years 5 years",
        ],
    },
    {
        **_BOT_COMMON,
        "instrument_type": InstrumentType.TREASURY_BILL,
        "instrument_notes": "Bons du Trésor : offre minimale 500 000 TZS, par multiples de 10 000 TZS ; intérêts soumis à une retenue à la source de 10 % (appel d'offres n°1208 du 7 octobre 2026).",
        "source_url": BOT_BILL_URL,
        "quotes": [
            "invites applications through Central Depository Participant (CDP) to tender for Treasury Bills",
            _BOT_CDP,
            "All investors, including foreign nationals, are eligible to participate.",
            "Minimum bid size TZS 500,000 in multiples of TZS 10,000",
            "Interest income is subject to 10% withholding tax.",
        ],
    },
    {
        **_BOT_COMMON,
        "instrument_type": InstrumentType.TREASURY_BOND,
        "instrument_notes": "Obligations du Trésor : offre minimale 1 000 000 TZS, par multiples de 100 000 TZS ; intérêts exonérés de retenue à la source ; cotation à la Bourse de Dar es Salaam (adjudication du 30 septembre 2026, obligation à 15 ans n°696).",
        "source_url": BOT_BOND_URL,
        "quotes": [
            _BOT_CDP,
            "All investors, including foreign nationals are eligible to participate.",
            "Minimum bid size TZS 1,000,000 in multiples of TZS 100,000",
            "Interest income is exempt from withholding tax",
            "The bonds will be listed on the Dar es Salaam Stock Exchange",
        ],
    },
    {
        "iso3": "UGA",
        "instrument_type": InstrumentType.TREASURY_BILL,
        "investor_type": "Investisseurs (via une banque commerciale)",
        "eligibility": "Offres non compétitives : via toute banque commerciale ; offres compétitives : réservées aux banques Primary Dealers.",
        "primary_dealer": "Banques Primary Dealers (offres compétitives) et autres banques commerciales.",
        "account_requirement": None,
        "submission_method": "Les banques soumettent les offres à la Bank of Uganda via le Central Securities Depository (CSD). Minimum non compétitif : 100 000 UGX ; compétitif : 200 100 000 UGX.",
        "settlement_method": None,
        "instrument_notes": "Bons du Trésor : minimum 100 000 UGX (non compétitif, via toute banque commerciale) ; offres non compétitives servies en totalité jusqu'à 200 000 000 UGX par échéance (appel d'offres n°1235 du 30 septembre 2026).",
        "source_url": BOU_BILL_URL,
        "verified_on": VERIFIED_ON_2,
        "quotes": [
            "Primary Dealer Banks (PDs) and other commercial banks should submit all bids to Bank of Uganda "
            "through the Central Securities Depository (CSD) by 10.00am, Wednesday September 30, 2026.",
            "Minimum Non-Competitive Bid Amount (THROUGH ANY COMMERCIAL BANK): 100,000/=",
            "Minimum Competitive Bid Amount (ONLY BY PRIMARY DEALER BANKS): 200,100,000/=",
            "PLEASE NOTE THAT ONLY PRIMARY DEALER BANKS ARE ALLOWED TO SUBMIT COMPETITIVE BIDS INTO THE AUCTION.",
            "Non-Competitive Bids: Accepted in full at the cut-off price up to 200,000,000/= per maturity",
        ],
    },
    {
        "iso3": "UGA",
        "instrument_type": InstrumentType.TREASURY_BOND,
        "investor_type": "Investisseurs (via une banque commerciale)",
        "eligibility": "Investisseurs résidents et non résidents ayant ouvert un compte CSD à la Bank of Uganda.",
        "primary_dealer": "Primary Dealers désignés dans le prospectus général (huit banques).",
        "account_requirement": "Compte CSD à la Bank of Uganda.",
        "submission_method": "Formulaire 1 (offre compétitive au-delà de 200 millions UGX, ou non compétitive) soumis via un Primary Dealer.",
        "settlement_method": "Règlement à T+1 ; les Primary Dealers règlent les offres des clients non bancaires soumises par leur intermédiaire.",
        "instrument_notes": "Obligations du Trésor : 2, 3, 5, 10, 15, 20 et 25 ans ; minimum 100 000 UGX (prospectus général de juillet 2025).",
        "source_url": BOU_BOND_URL,
        "verified_on": VERIFIED_ON_2,
        "quotes": [
            "Eligibility: Resident and non-resident investors who have opened up CSD accounts at the Bank of Uganda",
            "All bids must be submitted to the Bank of Uganda through one of the following Primary Dealers: "
            "ABSA Bank (U) Ltd., Centenary Bank, Citi Bank (U) Ltd., DFCU Bank (U) Ltd., Equity bank (U) Ltd., "
            "Housing Finance Bank Ltd., Stanbic Bank (U) Ltd., and Standard Chartered Bank (U) Ltd.",
            "Investors are invited to complete Form 1, the bid form for either competitive bids (bids in excess "
            "of Shs. 200 million which will be priced by the bidders) or non-competitive bids (bids that have a "
            "value of 200 million or less).",
            "13. Minimum bid amount: UGX 100,000= 14. Day count convention: Actual/364",
            "Tenors 2 Years, 3 Years, 5 Years, 10 Years, 15 Years, 20 Years and 25 Years",
            "All successful bids will be settled on a T+1 basis (by 12.00PM unless advised otherwise).",
            "Primary Dealers will be responsible for settling their own successful bids and the successful "
            "bids of non-commercial bank bidders submitted through them.",
        ],
    },
    {
        "iso3": "RWA",
        "instrument_type": InstrumentType.TREASURY_BOND,
        "investor_type": "Investisseurs résidents et non résidents (compte CSD)",
        "eligibility": "Résidents et non-résidents ayant ouvert un compte CSD via une banque commerciale agréée ou un intermédiaire de marché des capitaux.",
        "primary_dealer": "Banques commerciales agréées ou intermédiaires de marché des capitaux (placing agents).",
        "account_requirement": "Compte CSD ouvert via une banque commerciale agréée ou un intermédiaire de marché des capitaux.",
        "submission_method": "Formulaire de souscription (site de la BNR) remis via une banque commerciale agréée ou un intermédiaire de marché des capitaux. Minimum : 100 000 RWF (non compétitif), 50 millions RWF (compétitif).",
        "settlement_method": "Les banques commerciales règlent leurs offres et celles de leurs clients.",
        "instrument_notes": "Obligations du Trésor (book building) : minimum 100 000 RWF (offre non compétitive), 50 millions RWF (offre compétitive) ; retenue à la source de 5 % sur les intérêts (prospectus du 26 février 2026).",
        "source_url": BNR_BOND_URL,
        "verified_on": VERIFIED_ON_2,
        "quotes": [
            "Resident and non-resident who have opened a CSD account through Licensed commercial banks or "
            "Capital Market Intermediaries.",
            "All bids must be submitted to the National Bank of Rwanda through any of the licensed commercial "
            "banks or Capital Market intermediaries.",
            "All investors are required to complete bond application forms available on National Bank of "
            "Rwanda website: www.bnr.rw",
            "Minimum amount for: - Competitive bids………………………………. FRW 50 million - Non-competitive "
            "bids …………………………. FRW 100,000",
            "Commercial banks are responsible for settling their own successful bids and their clients’ bids.",
            "Interest will be subject to withholding tax at the rate of 5%",
        ],
    },
]
