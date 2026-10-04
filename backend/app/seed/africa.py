"""The 54 African UN member states — reference identity data.

STATUS: UNVERIFIED (see app.seed.reference.UNVERIFIED_NOTE). Compiled from general knowledge:
ISO 3166 codes, ISO 4217 currency, monetary arrangement and central bank. Points most likely to
need checking against an official source:
  * ZWE currency (ZWG, "Zimbabwe Gold", introduced 2024) and SLE (redenominated leone, 2022).
  * WAEMU membership of Burkina Faso, Mali and Niger after their 2025 exit from ECOWAS
    (ECOWAS and WAEMU are distinct; this file assumes WAEMU membership continues).
  * Exact official names of central banks.
The Sahrawi Arab Democratic Republic is an African Union member but not a UN member state
and is not included.

`tile` is (column, row) on a simplified tile-grid map of Africa used by the UI. It is a
layout aid, not geography.
"""

from typing import NamedTuple

from app.models.enums import MonetaryZone


class AfricanCountry(NamedTuple):
    iso3: str
    iso2: str
    name: str
    name_fr: str
    currency: str
    zone: MonetaryZone
    central_bank: str
    region: str  # north | west | central | east | southern
    tile: tuple[int, int]


BEAC = "Banque des États de l'Afrique Centrale (BEAC)"
BCEAO = "Banque Centrale des États de l'Afrique de l'Ouest (BCEAO)"
Z = MonetaryZone

AFRICA: list[AfricanCountry] = [
    # North
    AfricanCountry("DZA", "DZ", "Algeria", "Algérie", "DZD", Z.NONE, "Banque d'Algérie", "north", (4, 0)),
    AfricanCountry("EGY", "EG", "Egypt", "Égypte", "EGP", Z.NONE, "Central Bank of Egypt", "north", (7, 0)),
    AfricanCountry("LBY", "LY", "Libya", "Libye", "LYD", Z.NONE, "Central Bank of Libya", "north", (6, 0)),
    AfricanCountry("MAR", "MA", "Morocco", "Maroc", "MAD", Z.NONE, "Bank Al-Maghrib", "north", (3, 0)),
    AfricanCountry("TUN", "TN", "Tunisia", "Tunisie", "TND", Z.NONE, "Banque Centrale de Tunisie", "north", (5, 0)),
    AfricanCountry("SDN", "SD", "Sudan", "Soudan", "SDG", Z.NONE, "Central Bank of Sudan", "north", (6, 1)),
    AfricanCountry("MRT", "MR", "Mauritania", "Mauritanie", "MRU", Z.NONE, "Banque Centrale de Mauritanie", "north", (2, 1)),
    # West
    AfricanCountry("BEN", "BJ", "Benin", "Bénin", "XOF", Z.WAEMU, BCEAO, "west", (4, 3)),
    AfricanCountry("BFA", "BF", "Burkina Faso", "Burkina Faso", "XOF", Z.WAEMU, BCEAO, "west", (3, 2)),
    AfricanCountry("CPV", "CV", "Cabo Verde", "Cap-Vert", "CVE", Z.NONE, "Banco de Cabo Verde", "west", (0, 2)),
    AfricanCountry("CIV", "CI", "Côte d'Ivoire", "Côte d'Ivoire", "XOF", Z.WAEMU, BCEAO, "west", (2, 4)),
    AfricanCountry("GMB", "GM", "Gambia", "Gambie", "GMD", Z.NONE, "Central Bank of The Gambia", "west", (2, 2)),
    AfricanCountry("GHA", "GH", "Ghana", "Ghana", "GHS", Z.NONE, "Bank of Ghana", "west", (3, 3)),
    AfricanCountry("GIN", "GN", "Guinea", "Guinée", "GNF", Z.NONE, "Banque Centrale de la République de Guinée", "west", (2, 3)),
    AfricanCountry("GNB", "GW", "Guinea-Bissau", "Guinée-Bissau", "XOF", Z.WAEMU, BCEAO, "west", (1, 3)),
    AfricanCountry("LBR", "LR", "Liberia", "Liberia", "LRD", Z.NONE, "Central Bank of Liberia", "west", (1, 5)),
    AfricanCountry("MLI", "ML", "Mali", "Mali", "XOF", Z.WAEMU, BCEAO, "west", (3, 1)),
    AfricanCountry("NER", "NE", "Niger", "Niger", "XOF", Z.WAEMU, BCEAO, "west", (4, 1)),
    AfricanCountry("NGA", "NG", "Nigeria", "Nigeria", "NGN", Z.NONE, "Central Bank of Nigeria", "west", (4, 2)),
    AfricanCountry("SEN", "SN", "Senegal", "Sénégal", "XOF", Z.WAEMU, BCEAO, "west", (1, 2)),
    AfricanCountry("SLE", "SL", "Sierra Leone", "Sierra Leone", "SLE", Z.NONE, "Bank of Sierra Leone", "west", (1, 4)),
    AfricanCountry("TGO", "TG", "Togo", "Togo", "XOF", Z.WAEMU, BCEAO, "west", (3, 4)),
    # Central
    AfricanCountry("CMR", "CM", "Cameroon", "Cameroun", "XAF", Z.CEMAC, BEAC, "central", (5, 3)),
    AfricanCountry("CAF", "CF", "Central African Republic", "République centrafricaine", "XAF", Z.CEMAC, BEAC, "central", (5, 2)),
    AfricanCountry("TCD", "TD", "Chad", "Tchad", "XAF", Z.CEMAC, BEAC, "central", (5, 1)),
    AfricanCountry("COG", "CG", "Republic of the Congo", "République du Congo", "XAF", Z.CEMAC, BEAC, "central", (4, 5)),
    AfricanCountry("GNQ", "GQ", "Equatorial Guinea", "Guinée équatoriale", "XAF", Z.CEMAC, BEAC, "central", (4, 4)),
    AfricanCountry("GAB", "GA", "Gabon", "Gabon", "XAF", Z.CEMAC, BEAC, "central", (5, 4)),
    AfricanCountry("COD", "CD", "Democratic Republic of the Congo", "République démocratique du Congo", "CDF", Z.NONE, "Banque Centrale du Congo", "central", (5, 5)),
    AfricanCountry("STP", "ST", "São Tomé and Príncipe", "Sao Tomé-et-Principe", "STN", Z.NONE, "Banco Central de São Tomé e Príncipe", "central", (3, 5)),
    AfricanCountry("AGO", "AO", "Angola", "Angola", "AOA", Z.NONE, "Banco Nacional de Angola", "central", (4, 6)),
    AfricanCountry("BDI", "BI", "Burundi", "Burundi", "BIF", Z.NONE, "Banque de la République du Burundi", "central", (6, 5)),
    AfricanCountry("RWA", "RW", "Rwanda", "Rwanda", "RWF", Z.NONE, "National Bank of Rwanda", "central", (6, 4)),
    # East
    AfricanCountry("KEN", "KE", "Kenya", "Kenya", "KES", Z.NONE, "Central Bank of Kenya (CBK)", "east", (7, 3)),
    AfricanCountry("UGA", "UG", "Uganda", "Ouganda", "UGX", Z.NONE, "Bank of Uganda", "east", (6, 3)),
    AfricanCountry("TZA", "TZ", "Tanzania", "Tanzanie", "TZS", Z.NONE, "Bank of Tanzania", "east", (7, 4)),
    AfricanCountry("ETH", "ET", "Ethiopia", "Éthiopie", "ETB", Z.NONE, "National Bank of Ethiopia", "east", (7, 2)),
    AfricanCountry("ERI", "ER", "Eritrea", "Érythrée", "ERN", Z.NONE, "Bank of Eritrea", "east", (7, 1)),
    AfricanCountry("DJI", "DJ", "Djibouti", "Djibouti", "DJF", Z.NONE, "Banque Centrale de Djibouti", "east", (8, 2)),
    AfricanCountry("SOM", "SO", "Somalia", "Somalie", "SOS", Z.NONE, "Central Bank of Somalia", "east", (8, 3)),
    AfricanCountry("SSD", "SS", "South Sudan", "Soudan du Sud", "SSP", Z.NONE, "Bank of South Sudan", "east", (6, 2)),
    AfricanCountry("SYC", "SC", "Seychelles", "Seychelles", "SCR", Z.NONE, "Central Bank of Seychelles", "east", (9, 4)),
    AfricanCountry("MUS", "MU", "Mauritius", "Maurice", "MUR", Z.NONE, "Bank of Mauritius", "east", (9, 6)),
    AfricanCountry("COM", "KM", "Comoros", "Comores", "KMF", Z.NONE, "Banque Centrale des Comores", "east", (8, 5)),
    AfricanCountry("MDG", "MG", "Madagascar", "Madagascar", "MGA", Z.NONE, "Banque Centrale de Madagascar", "east", (8, 6)),
    # Southern
    AfricanCountry("ZAF", "ZA", "South Africa", "Afrique du Sud", "ZAR", Z.CMA, "South African Reserve Bank", "southern", (5, 8)),
    AfricanCountry("NAM", "NA", "Namibia", "Namibie", "NAD", Z.CMA, "Bank of Namibia", "southern", (4, 7)),
    AfricanCountry("LSO", "LS", "Lesotho", "Lesotho", "LSL", Z.CMA, "Central Bank of Lesotho", "southern", (5, 9)),
    AfricanCountry("SWZ", "SZ", "Eswatini", "Eswatini", "SZL", Z.CMA, "Central Bank of Eswatini", "southern", (6, 8)),
    AfricanCountry("BWA", "BW", "Botswana", "Botswana", "BWP", Z.NONE, "Bank of Botswana", "southern", (5, 7)),
    AfricanCountry("ZMB", "ZM", "Zambia", "Zambie", "ZMW", Z.NONE, "Bank of Zambia", "southern", (5, 6)),
    AfricanCountry("ZWE", "ZW", "Zimbabwe", "Zimbabwe", "ZWG", Z.NONE, "Reserve Bank of Zimbabwe", "southern", (6, 7)),
    AfricanCountry("MWI", "MW", "Malawi", "Malawi", "MWK", Z.NONE, "Reserve Bank of Malawi", "southern", (7, 5)),
    AfricanCountry("MOZ", "MZ", "Mozambique", "Mozambique", "MZN", Z.NONE, "Banco de Moçambique", "southern", (7, 6)),
]

BY_ISO3: dict[str, AfricanCountry] = {c.iso3: c for c in AFRICA}
