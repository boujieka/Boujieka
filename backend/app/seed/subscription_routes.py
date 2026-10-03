"""How buyers can access government securities: procedural facts quoted from official pages.

Every route below is backed by a verbatim excerpt from the cited official page, retrieved on
VERIFIED_ON. Nothing here is advice, and access is never guaranteed. Fees and taxes are not
stated on these pages, so they are left empty ("Not available").

Coverage: CEMAC (BEAC), WAEMU (UMOA-Titres) and Kenya (CBK). Routes for the other countries are
not yet documented.
"""

from app.models.enums import InstrumentType, MonetaryZone

VERIFIED_ON = "2026-10-03"

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
