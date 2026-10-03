"""Proposed official URLs for the source registry. UNCONFIRMED until an operator approves them.

Evidence was gathered on 2026-10-03:
  "http_200"   — fetched from our environment; HTTP 200 and the page <title> names the institution
                 (title quoted in `evidence`).
  "http_403"   — server answered but blocked automated access (bot protection); domain exists.
  "search_only"— our fetches failed (timeouts); the URL comes from web-search results citing the
                 institution. Lowest confidence: must be opened by a human before use.

These are stored in Source.crawl_config["candidates"]. Source.base_url stays NULL and the
source stays `pending_configuration` until an operator confirms a URL. A URL being reachable
proves the page exists, not that its content is complete, current or machine-readable.
"""

CHECKED_ON = "2026-10-03"

# source name (must match reference.SOURCES) -> candidate URLs, most useful first
CANDIDATES: dict[str, list[dict[str, str]]] = {
    "BEAC — government securities market": [
        {
            "url": "https://www.beac.int/m-des-titres-publics/annonces-et-communiques/",
            "purpose": "Auction announcements and result communiqués (CEMAC BTA/OTA)",
            "check": "http_200",
            "evidence": "title 'Annonces et Communiqués - BEAC'",
        },
        {
            "url": "https://www.beac.int/m-des-titres-publics/calendrier-trimestriel-demission-titres-publics-etats-de-cemac/",
            "purpose": "Quarterly issuance calendars of CEMAC states",
            "check": "http_200",
            "evidence": "title 'Calendriers trimestriels d'émissions des Titres Publics des États de la CEMAC - BEAC'",
        },
        {
            "url": "https://www.beac.int/m-des-titres-publics/programme-annuel-emissions-de-titres-publics-etats-de-cemac/",
            "purpose": "Annual issuance programmes",
            "check": "http_200",
            "evidence": "title 'Programme annuel des émissions de Titres Publics des Etats de la CEMAC - BEAC'",
        },
        {
            "url": "https://www.beac.int/m-des-titres-publics/bulletins-marche-titres-publics/",
            "purpose": "Public-securities market bulletins",
            "check": "http_200",
            "evidence": "title 'Bulletins du Marché des titres publics - BEAC'",
        },
        {
            "url": "https://www.beac.int/economie-stats/statistiques-titres-publics/",
            "purpose": "Public-securities statistics",
            "check": "http_200",
            "evidence": "title 'Statistiques des Titres Publics - BEAC'",
        },
    ],
    "BCEAO — publications": [
        {
            "url": "https://www.bceao.int/fr/appels-offres/appels-offres-marches-titres-publics-prives",
            "purpose": "Calls for tender for public securities (auction notices)",
            "check": "http_200",
            "evidence": "title 'Avis d'appel d'offres | BCEAO'",
        },
        {
            "url": "https://www.bceao.int/index.php/fr/publications/bulletins",
            "purpose": "Statistical bulletins",
            "check": "http_200",
            "evidence": "linked from BCEAO homepage; homepage title 'BCEAO | Banque Centrale des Etats de l'Afrique de l'Ouest'",
        },
    ],
    "UMOA-Titres — auction calendar and results": [
        {
            "url": "https://www.umoatitres.org/fr/calendrier-des-emissions-2/",
            "purpose": "Issuance calendar (WAEMU states)",
            "check": "http_200",
            "evidence": "title 'Calendrier des emissions – UMOA-Titres'",
        },
        {
            "url": "https://www.umoatitres.org/fr/emissions/",
            "purpose": "Issuance data table (results)",
            "check": "http_200",
            "evidence": "title 'Table des données – Particuliers – UMOA-Titres'",
        },
        {
            "url": "https://www.umoatitres.org/fr/category/publications/bulletin-statistiques/",
            "purpose": "Quarterly statistical bulletins",
            "check": "http_200",
            "evidence": "title 'Bulletins statistiques – UMOA-Titres'",
        },
        {
            "url": "https://www.umoatitres.org/fr/donnees-du-marche-secondaire/",
            "purpose": "Secondary-market data",
            "check": "http_200",
            "evidence": "title 'Données du marché secondaire – UMOA-Titres'",
        },
    ],
    "Central Bank of Kenya — auction results": [
        {
            "url": "https://www.centralbank.go.ke/securities/treasury-bills/",
            "purpose": "T-bill auction notices and results (PDFs)",
            "check": "http_200",
            "evidence": "title 'Treasury Bills | CBK'",
        },
        {
            "url": "https://www.centralbank.go.ke/securities/treasury-bonds/",
            "purpose": "T-bond prospectuses and results (PDFs)",
            "check": "http_200",
            "evidence": "title 'Treasury Bonds | CBK'",
        },
        {
            "url": "https://www.centralbank.go.ke/wp-content/uploads/2024/06/AuctionRulesGuidelines.pdf",
            "purpose": "Auction rules and guidelines (procedural; Phase 6)",
            "check": "http_200",
            "evidence": "PDF returned HTTP 200",
        },
        {
            "url": "https://www.centralbank.go.ke/releases/weekly-bulletin/",
            "purpose": "Weekly bulletin",
            "check": "http_200",
            "evidence": "linked from CBK homepage; homepage title 'CBK | Central Bank of Kenya'",
        },
    ],
    "Kenya — National Treasury": [
        {
            "url": "https://newsite.treasury.go.ke/directorate-public-debt-management",
            "purpose": "Public Debt Management directorate",
            "check": "http_200",
            "evidence": "title 'Directorate of Public Debt Management | The National Treasury'",
        },
        {
            "url": "https://www.treasury.go.ke/",
            "purpose": "Homepage",
            "check": "http_200",
            "evidence": "title 'Homepage | The National Treasury'",
        },
    ],
    "Cameroon — Ministry of Finance": [
        {
            "url": "https://minfi.gov.cm/dette-flottante-de-letat-du-cameroun/",
            "purpose": "State floating-debt page",
            "check": "http_200",
            "evidence": "title 'DETTE FLOTTANTE DE L'ETAT DU CAMEROUN – MINFI'",
        },
        {
            "url": "https://minfi.gov.cm/",
            "purpose": "Homepage",
            "check": "http_200",
            "evidence": "title 'MINFI – Site institutionnel du Ministère des Finances du Cameroun'",
        },
    ],
    "Cameroon — Direction Générale du Budget": [
        {
            "url": "https://www.dgb.cm/",
            "purpose": "Publishes monthly public-debt conjuncture reports (per search results)",
            "check": "http_200",
            "evidence": "title 'LA DIRECTION GENERALE DU BUDGET – Ministère des Finances du Cameroun'",
        },
    ],
    "Cameroon — Caisse Autonome d'Amortissement": [
        {
            "url": "https://www.caa.cm/",
            "purpose": "Debt-management office",
            "check": "search_only",
            "evidence": "web search cites www.caa.cm as the CAA site; our fetches timed out",
        },
    ],
    "Congo — Ministry of Finance": [
        {
            "url": "https://www.finances.gouv.cg/",
            "purpose": "Ministry homepage",
            "check": "http_403",
            "evidence": "server responded 403 Forbidden to automated access",
        },
    ],
    "Gabon — Direction Générale de la Dette": [
        {
            "url": "https://dette.ga/",
            "purpose": "Debt directorate; public-offering announcements",
            "check": "search_only",
            "evidence": "press coverage names dette.ga as the DGD site; HTTPS timed out, plain HTTP returned 503",
        },
    ],
    "Côte d'Ivoire — Direction Générale du Trésor": [
        {
            "url": "https://tresor.gouv.ci/tres/",
            "purpose": "Treasury (DGTCP); public-debt statistical bulletins",
            "check": "http_200",
            "evidence": "title 'DIRECTION GÉNÉRALE DU TRÉSOR ET DE LA COMPTABILITÉ PUBLIQUE'",
        },
    ],
    "Côte d'Ivoire — Ministry of Finance": [
        {
            "url": "https://finances.gouv.ci/",
            "purpose": "Ministry homepage",
            "check": "http_200",
            "evidence": "HTTP 200 (no <title> extracted)",
        },
    ],
    "Senegal — Ministry of Finance": [
        {
            "url": "https://www.finances.gouv.sn/",
            "purpose": "Ministry homepage",
            "check": "http_200",
            "evidence": "HTTP 200, title 'Accueil'; domain is the ministry's",
        },
    ],
    "BVMAC — listings": [
        {
            "url": "https://www.bvm-ac.org/",
            "purpose": "CEMAC regional exchange",
            "check": "http_200",
            "evidence": "title 'Accueil - BVMAC: Bourse des Valeurs Mobilières de l'Afrique Centrale'",
        },
        {
            "url": "https://www.bvmac.cm/",
            "purpose": "Alternate BVMAC domain (also live; operator to pick canonical)",
            "check": "http_200",
            "evidence": "title 'BVMAC: Bourse des Valeurs Mobilières de l'Afrique Centrale'",
        },
    ],
    "BRVM — listings": [
        {
            "url": "https://www.brvm.org/fr/bulletins-officiels-de-la-cote",
            "purpose": "Official daily price bulletins (incl. listed government bonds)",
            "check": "http_200",
            "evidence": "title 'Bulletins Officiels de la Cote | BRVM'",
        },
    ],
    "Nairobi Securities Exchange — bond listings": [
        {
            "url": "https://www.nse.co.ke/government-bonds/",
            "purpose": "Listed government bonds",
            "check": "http_200",
            "evidence": "title 'Government Bonds - Nairobi Securities Exchange PLC'",
        },
    ],
    "AfDB — African Financial Markets Initiative": [
        {
            "url": "https://www.afdb.org/en/topics-and-sectors/initiatives-partnerships/african-financial-markets-initiative-afmi",
            "purpose": "AFMI programme page (African Financial Markets Database)",
            "check": "http_403",
            "evidence": "appears in web search; server returned 403 bot challenge to our fetch",
        },
    ],
}
