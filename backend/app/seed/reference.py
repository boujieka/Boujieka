"""Reference data for the MVP countries and the official-source registry.

STATUS: UNVERIFIED. Compiled from general knowledge, not from a retrieved
official document. Every row is stored with verification_status=unverified and
no confidence score; an operator must confirm each field against the official
source before it is marked verified.

Deliberately left empty (rendered as "Not available"): tax notes, capital
controls, market-access notes and every source URL. We do not guess URLs —
crawlers stay in `pending_configuration` until an operator supplies them.
"""

from app.models.enums import MonetaryZone, SourceCategory

UNVERIFIED_NOTE = (
    "Reference seed compiled from general knowledge, not from a retrieved official "
    "document. Verify against the official source before relying on it."
)

COUNTRIES: list[dict] = [
    {
        "name": "Cameroon",
        "iso2": "CM",
        "iso3": "CMR",
        "currency": "XAF",
        "monetary_zone": MonetaryZone.CEMAC,
        "central_bank": "Banque des États de l'Afrique Centrale (BEAC)",
        "debt_management_office": "Caisse Autonome d'Amortissement (CAA)",
        "primary_market_structure": (
            "CEMAC regional public-securities market: Treasury bills (BTA) and Treasury "
            "bonds (OTA) issued by auction through BEAC; bids via approved primary dealers."
        ),
        "secondary_market_structure": "BVMAC (regional exchange, CEMAC); OTC between dealers.",
    },
    {
        "name": "Republic of the Congo",
        "iso2": "CG",
        "iso3": "COG",
        "currency": "XAF",
        "monetary_zone": MonetaryZone.CEMAC,
        "central_bank": "Banque des États de l'Afrique Centrale (BEAC)",
        "debt_management_office": "Caisse Congolaise d'Amortissement (CCA)",
        "primary_market_structure": (
            "CEMAC regional public-securities market: BTA and OTA issued by auction through "
            "BEAC; bids via approved primary dealers."
        ),
        "secondary_market_structure": "BVMAC (regional exchange, CEMAC); OTC between dealers.",
    },
    {
        "name": "Gabon",
        "iso2": "GA",
        "iso3": "GAB",
        "currency": "XAF",
        "monetary_zone": MonetaryZone.CEMAC,
        "central_bank": "Banque des États de l'Afrique Centrale (BEAC)",
        "debt_management_office": None,
        "primary_market_structure": (
            "CEMAC regional public-securities market: BTA and OTA issued by auction through "
            "BEAC; bids via approved primary dealers."
        ),
        "secondary_market_structure": "BVMAC (regional exchange, CEMAC); OTC between dealers.",
    },
    {
        "name": "Côte d'Ivoire",
        "iso2": "CI",
        "iso3": "CIV",
        "currency": "XOF",
        "monetary_zone": MonetaryZone.WAEMU,
        "central_bank": "Banque Centrale des États de l'Afrique de l'Ouest (BCEAO)",
        "debt_management_office": None,
        "primary_market_structure": (
            "WAEMU regional market: Treasury bills (BAT) and bonds (OAT) issued by auction "
            "organised by UMOA-Titres with BCEAO; bids via primary dealers (SVT) and banks. "
            "Public offerings (APE) also used."
        ),
        "secondary_market_structure": "BRVM (regional exchange, WAEMU); OTC between dealers.",
    },
    {
        "name": "Senegal",
        "iso2": "SN",
        "iso3": "SEN",
        "currency": "XOF",
        "monetary_zone": MonetaryZone.WAEMU,
        "central_bank": "Banque Centrale des États de l'Afrique de l'Ouest (BCEAO)",
        "debt_management_office": None,
        "primary_market_structure": (
            "WAEMU regional market: BAT and OAT issued by auction organised by UMOA-Titres "
            "with BCEAO; bids via primary dealers (SVT) and banks. Public offerings (APE) "
            "also used."
        ),
        "secondary_market_structure": "BRVM (regional exchange, WAEMU); OTC between dealers.",
    },
    {
        "name": "Kenya",
        "iso2": "KE",
        "iso3": "KEN",
        "currency": "KES",
        "monetary_zone": MonetaryZone.NONE,
        "central_bank": "Central Bank of Kenya (CBK)",
        "debt_management_office": "Public Debt Management Office, The National Treasury",
        "primary_market_structure": (
            "CBK auctions 91-, 182- and 364-day Treasury bills and Treasury bonds as fiscal "
            "agent for the National Treasury."
        ),
        "secondary_market_structure": "Treasury bonds trade on the Nairobi Securities Exchange.",
    },
]

# (name, institution, category, country iso3 or None for regional)
SOURCES: list[tuple[str, str, SourceCategory, str | None]] = [
    ("BEAC — government securities market", "BEAC", SourceCategory.CENTRAL_BANK, None),
    ("BCEAO — publications", "BCEAO", SourceCategory.CENTRAL_BANK, None),
    ("Central Bank of Kenya — auction results", "Central Bank of Kenya",
     SourceCategory.CENTRAL_BANK, "KEN"),
    ("UMOA-Titres — auction calendar and results", "UMOA-Titres",
     SourceCategory.AUCTION_PLATFORM, None),
    ("Cameroon — Ministry of Finance", "Ministry of Finance (Cameroon)",
     SourceCategory.MINISTRY_OF_FINANCE, "CMR"),
    ("Cameroon — Caisse Autonome d'Amortissement", "CAA",
     SourceCategory.DEBT_MANAGEMENT_OFFICE, "CMR"),
    ("Cameroon — Direction Générale du Budget", "Direction Générale du Budget (Cameroon)",
     SourceCategory.MINISTRY_OF_FINANCE, "CMR"),
    ("Congo — Ministry of Finance", "Ministry of Finance (Republic of the Congo)",
     SourceCategory.MINISTRY_OF_FINANCE, "COG"),
    ("Gabon — Ministry of Economy and Finance", "Ministry of Economy (Gabon)",
     SourceCategory.MINISTRY_OF_FINANCE, "GAB"),
    ("Gabon — Direction Générale de la Dette", "Direction Générale de la Dette (Gabon)",
     SourceCategory.DEBT_MANAGEMENT_OFFICE, "GAB"),
    ("Côte d'Ivoire — Ministry of Finance", "Ministry of Finance (Côte d'Ivoire)",
     SourceCategory.MINISTRY_OF_FINANCE, "CIV"),
    ("Côte d'Ivoire — Direction Générale du Trésor",
     "Direction Générale du Trésor et de la Comptabilité Publique (Côte d'Ivoire)",
     SourceCategory.DEBT_MANAGEMENT_OFFICE, "CIV"),
    ("Senegal — Ministry of Finance", "Ministry of Finance (Senegal)",
     SourceCategory.MINISTRY_OF_FINANCE, "SEN"),
    # Created by decree in June 2026 per press reports; no official website found yet.
    ("Senegal — Direction Générale du Financement et de la Dette",
     "Direction Générale du Financement et de la Dette (Senegal)",
     SourceCategory.DEBT_MANAGEMENT_OFFICE, "SEN"),
    ("Kenya — National Treasury", "The National Treasury (Kenya)",
     SourceCategory.MINISTRY_OF_FINANCE, "KEN"),
    ("BVMAC — listings", "BVMAC", SourceCategory.STOCK_EXCHANGE, None),
    ("BRVM — listings", "BRVM", SourceCategory.STOCK_EXCHANGE, None),
    ("Nairobi Securities Exchange — bond listings", "Nairobi Securities Exchange",
     SourceCategory.STOCK_EXCHANGE, "KEN"),
    ("AfDB — African Financial Markets Initiative", "African Development Bank",
     SourceCategory.REGIONAL_INSTITUTION, None),
]
