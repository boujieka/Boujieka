"""The 54 African UN member states — geographical reference data (Master prompt §6).

STATUS: compiled reference, UNVERIFIED against an official register at load time.
  * ISO 3166-1 alpha-2/alpha-3/numeric codes and names: cross-checked automatically by
    `tests/test_reference_live.py` against the World Bank country API (codes) and the Natural
    Earth/world-atlas dataset (numeric codes) when run with `-m live`.
  * region = African Union region; subregion = UN M49 geoscheme sub-region.
  * currency = ISO 4217. Points that change and need periodic checking: ZWE (ZWG, 2024),
    SLE (redenominated leone, 2022), STN, MRU.
  * official_languages: main official languages; may be incomplete.
The Sahrawi Arab Democratic Republic is an AU member but not a UN member state; it is not
included (54 = UN member states).

Geographical availability is NOT data coverage: a country listed here has no project data
until a connector has imported records for it.
"""

from typing import NamedTuple


class CountryRef(NamedTuple):
    iso3: str
    iso2: str
    numeric: str
    name_en: str
    name_fr: str
    region: str  # AU region
    subregion: str  # UN M49
    currency: str
    languages: tuple[str, ...]


N, W, C, E, S = "North Africa", "West Africa", "Central Africa", "East Africa", "Southern Africa"
NA, WA, MA, EA, SA = "Northern Africa", "Western Africa", "Middle Africa", "Eastern Africa", "Southern Africa"

COUNTRIES: list[CountryRef] = [
    CountryRef("DZA", "DZ", "012", "Algeria", "Algérie", N, NA, "DZD", ("ar", "ber")),
    CountryRef("EGY", "EG", "818", "Egypt", "Égypte", N, NA, "EGP", ("ar",)),
    CountryRef("LBY", "LY", "434", "Libya", "Libye", N, NA, "LYD", ("ar",)),
    CountryRef("MAR", "MA", "504", "Morocco", "Maroc", N, NA, "MAD", ("ar", "ber")),
    CountryRef("TUN", "TN", "788", "Tunisia", "Tunisie", N, NA, "TND", ("ar",)),
    CountryRef("MRT", "MR", "478", "Mauritania", "Mauritanie", N, WA, "MRU", ("ar",)),
    CountryRef("SDN", "SD", "729", "Sudan", "Soudan", E, NA, "SDG", ("ar", "en")),
    CountryRef("BEN", "BJ", "204", "Benin", "Bénin", W, WA, "XOF", ("fr",)),
    CountryRef("BFA", "BF", "854", "Burkina Faso", "Burkina Faso", W, WA, "XOF", ("fr",)),
    CountryRef("CPV", "CV", "132", "Cabo Verde", "Cap-Vert", W, WA, "CVE", ("pt",)),
    CountryRef("CIV", "CI", "384", "Côte d'Ivoire", "Côte d'Ivoire", W, WA, "XOF", ("fr",)),
    CountryRef("GMB", "GM", "270", "Gambia", "Gambie", W, WA, "GMD", ("en",)),
    CountryRef("GHA", "GH", "288", "Ghana", "Ghana", W, WA, "GHS", ("en",)),
    CountryRef("GIN", "GN", "324", "Guinea", "Guinée", W, WA, "GNF", ("fr",)),
    CountryRef("GNB", "GW", "624", "Guinea-Bissau", "Guinée-Bissau", W, WA, "XOF", ("pt",)),
    CountryRef("LBR", "LR", "430", "Liberia", "Liberia", W, WA, "LRD", ("en",)),
    CountryRef("MLI", "ML", "466", "Mali", "Mali", W, WA, "XOF", ("fr",)),
    CountryRef("NER", "NE", "562", "Niger", "Niger", W, WA, "XOF", ("fr",)),
    CountryRef("NGA", "NG", "566", "Nigeria", "Nigeria", W, WA, "NGN", ("en",)),
    CountryRef("SEN", "SN", "686", "Senegal", "Sénégal", W, WA, "XOF", ("fr",)),
    CountryRef("SLE", "SL", "694", "Sierra Leone", "Sierra Leone", W, WA, "SLE", ("en",)),
    CountryRef("TGO", "TG", "768", "Togo", "Togo", W, WA, "XOF", ("fr",)),
    CountryRef("CMR", "CM", "120", "Cameroon", "Cameroun", C, MA, "XAF", ("fr", "en")),
    CountryRef("CAF", "CF", "140", "Central African Republic", "République centrafricaine", C, MA, "XAF", ("fr", "sg")),
    CountryRef("TCD", "TD", "148", "Chad", "Tchad", C, MA, "XAF", ("fr", "ar")),
    CountryRef("COG", "CG", "178", "Republic of the Congo", "République du Congo", C, MA, "XAF", ("fr",)),
    CountryRef("COD", "CD", "180", "Democratic Republic of the Congo", "République démocratique du Congo", C, MA, "CDF", ("fr",)),
    CountryRef("GNQ", "GQ", "226", "Equatorial Guinea", "Guinée équatoriale", C, MA, "XAF", ("es", "fr", "pt")),
    CountryRef("GAB", "GA", "266", "Gabon", "Gabon", C, MA, "XAF", ("fr",)),
    CountryRef("STP", "ST", "678", "São Tomé and Príncipe", "Sao Tomé-et-Principe", C, MA, "STN", ("pt",)),
    CountryRef("BDI", "BI", "108", "Burundi", "Burundi", C, EA, "BIF", ("rn", "fr", "en")),
    CountryRef("AGO", "AO", "024", "Angola", "Angola", S, MA, "AOA", ("pt",)),
    CountryRef("KEN", "KE", "404", "Kenya", "Kenya", E, EA, "KES", ("sw", "en")),
    CountryRef("UGA", "UG", "800", "Uganda", "Ouganda", E, EA, "UGX", ("en", "sw")),
    CountryRef("TZA", "TZ", "834", "Tanzania", "Tanzanie", E, EA, "TZS", ("sw", "en")),
    CountryRef("RWA", "RW", "646", "Rwanda", "Rwanda", E, EA, "RWF", ("rw", "fr", "en", "sw")),
    CountryRef("ETH", "ET", "231", "Ethiopia", "Éthiopie", E, EA, "ETB", ("am",)),
    CountryRef("ERI", "ER", "232", "Eritrea", "Érythrée", E, EA, "ERN", ("ti", "ar", "en")),
    CountryRef("DJI", "DJ", "262", "Djibouti", "Djibouti", E, EA, "DJF", ("fr", "ar")),
    CountryRef("SOM", "SO", "706", "Somalia", "Somalie", E, EA, "SOS", ("so", "ar")),
    CountryRef("SSD", "SS", "728", "South Sudan", "Soudan du Sud", E, EA, "SSP", ("en",)),
    CountryRef("SYC", "SC", "690", "Seychelles", "Seychelles", E, EA, "SCR", ("en", "fr", "crs")),
    CountryRef("MUS", "MU", "480", "Mauritius", "Maurice", E, EA, "MUR", ("en", "fr")),
    CountryRef("COM", "KM", "174", "Comoros", "Comores", E, EA, "KMF", ("ar", "fr", "zdj")),
    CountryRef("MDG", "MG", "450", "Madagascar", "Madagascar", E, EA, "MGA", ("mg", "fr")),
    CountryRef("ZAF", "ZA", "710", "South Africa", "Afrique du Sud", S, SA, "ZAR", ("en", "af", "zu", "xh")),
    CountryRef("NAM", "NA", "516", "Namibia", "Namibie", S, SA, "NAD", ("en",)),
    CountryRef("LSO", "LS", "426", "Lesotho", "Lesotho", S, SA, "LSL", ("st", "en")),
    CountryRef("SWZ", "SZ", "748", "Eswatini", "Eswatini", S, SA, "SZL", ("ss", "en")),
    CountryRef("BWA", "BW", "072", "Botswana", "Botswana", S, SA, "BWP", ("en", "tn")),
    CountryRef("ZMB", "ZM", "894", "Zambia", "Zambie", S, EA, "ZMW", ("en",)),
    CountryRef("ZWE", "ZW", "716", "Zimbabwe", "Zimbabwe", S, EA, "ZWG", ("en", "sn", "nd")),
    CountryRef("MWI", "MW", "454", "Malawi", "Malawi", S, EA, "MWK", ("en", "ny")),
    CountryRef("MOZ", "MZ", "508", "Mozambique", "Mozambique", S, EA, "MZN", ("pt",)),
]

BY_ISO3 = {c.iso3: c for c in COUNTRIES}
BY_ISO2 = {c.iso2: c for c in COUNTRIES}

# First-level administrative divisions. Only Cameroon is loaded for the initial deployment;
# other countries' divisions are added through data import, not invented here.
# Cameroon: the 10 regions (ISO 3166-2:CM).
ADMIN_DIVISIONS: dict[str, list[tuple[str, str, str]]] = {
    "CMR": [
        ("CM-AD", "Adamawa", "Adamaoua"),
        ("CM-CE", "Centre", "Centre"),
        ("CM-ES", "East", "Est"),
        ("CM-EN", "Far North", "Extrême-Nord"),
        ("CM-LT", "Littoral", "Littoral"),
        ("CM-NO", "North", "Nord"),
        ("CM-NW", "North-West", "Nord-Ouest"),
        ("CM-OU", "West", "Ouest"),
        ("CM-SU", "South", "Sud"),
        ("CM-SW", "South-West", "Sud-Ouest"),
    ],
}

# Country-specific official sources for national public-investment data (Master prompt §13).
# These are candidate sources for the documented manual-import workflow. Reachability is
# checked at runtime (`python -m app.cli check-country-sources`); nothing here is asserted
# to contain machine-readable data.
COUNTRY_SOURCES: dict[str, list[dict]] = {
    "CMR": [
        {"name": "Lois de finances et documents budgétaires", "institution": "Ministère des Finances (MINFI)",
         "category": "finance_law", "url": "https://www.minfi.gov.cm"},
        {"name": "Budget d'investissement public (BIP) et programmation", "institution":
         "Ministère de l'Économie, de la Planification et de l'Aménagement du Territoire (MINEPAT)",
         "category": "budget", "url": "https://www.minepat.gov.cm"},
        {"name": "Rapports d'exécution budgétaire", "institution": "Ministère des Finances (MINFI)",
         "category": "budget_execution", "url": "https://www.minfi.gov.cm"},
        {"name": "Marchés publics", "institution": "Agence de Régulation des Marchés Publics (ARMP)",
         "category": "procurement", "url": "https://armp.cm"},
        {"name": "Rapports de contrôle des comptes publics", "institution": "Chambre des Comptes de la Cour Suprême",
         "category": "audit", "url": None},
        {"name": "Statistiques nationales", "institution": "Institut National de la Statistique (INS)",
         "category": "statistics", "url": "https://ins-cameroun.cm"},
    ],
}
