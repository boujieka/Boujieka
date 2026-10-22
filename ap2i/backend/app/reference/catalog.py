"""Sectors, indicators, instruments, donor registry, roles and plans (reference catalogue)."""

# --- Sectors (Master prompt §18) -------------------------------------------------------------
SECTORS: list[tuple[str, str, str]] = [
    ("ENERGY", "Energy", "Énergie"),
    ("TRANSPORT", "Transport", "Transport"),
    ("WATER", "Water and Sanitation", "Eau et assainissement"),
    ("HEALTH", "Health", "Santé"),
    ("EDUCATION", "Education", "Éducation"),
    ("AGRICULTURE", "Agriculture", "Agriculture"),
    ("INDUSTRY", "Industry", "Industrie"),
    ("DIGITAL", "Digital Infrastructure", "Infrastructures numériques"),
    ("HOUSING", "Housing", "Logement"),
    ("URBAN", "Urban Development", "Développement urbain"),
    ("ENVIRONMENT", "Environment", "Environnement"),
    ("CLIMATE", "Climate", "Climat"),
    ("PUBADMIN", "Public Administration", "Administration publique"),
    ("MINING", "Mining", "Mines"),
    ("NATRES", "Natural Resources", "Ressources naturelles"),
    ("OTHER", "Other", "Autre"),
]

# Configurable sector indicators. (sector, code, name_en, name_fr, unit, kind)
SECTOR_INDICATORS: list[tuple[str, str, str, str, str, str]] = [
    ("ENERGY", "mw_installed", "MW installed", "MW installés", "MW", "output"),
    ("ENERGY", "mw_operational", "MW operational", "MW opérationnels", "MW", "operational"),
    ("ENERGY", "transmission_km", "Transmission lines built", "Lignes de transport construites", "km", "output"),
    ("ENERGY", "distribution_km", "Distribution lines built", "Lignes de distribution construites", "km", "output"),
    ("ENERGY", "new_connections", "New electricity connections", "Nouveaux branchements électriques", "connections", "output"),
    ("ENERGY", "access_beneficiaries", "People with new electricity access", "Bénéficiaires d'un nouvel accès à l'électricité", "people", "outcome"),
    ("TRANSPORT", "road_km_built", "Road kilometres constructed", "Kilomètres de routes construits", "km", "output"),
    ("TRANSPORT", "road_km_rehab", "Road kilometres rehabilitated", "Kilomètres de routes réhabilités", "km", "output"),
    ("TRANSPORT", "bridges_completed", "Bridges completed", "Ponts achevés", "bridges", "output"),
    ("TRANSPORT", "utilization", "Infrastructure utilization", "Utilisation de l'infrastructure", "vehicles/day", "operational"),
    ("WATER", "production_capacity", "Water production capacity", "Capacité de production d'eau", "m3/day", "output"),
    ("WATER", "connections", "Water connections delivered", "Branchements d'eau réalisés", "connections", "output"),
    ("WATER", "population_served", "Population served", "Population desservie", "people", "outcome"),
    ("WATER", "service_continuity", "Service continuity", "Continuité du service", "hours/day", "operational"),
    ("HEALTH", "hospitals_built", "Hospitals constructed", "Hôpitaux construits", "facilities", "output"),
    ("HEALTH", "hospitals_equipped", "Hospitals equipped", "Hôpitaux équipés", "facilities", "output"),
    ("HEALTH", "hospitals_operational", "Hospitals operational", "Hôpitaux fonctionnels", "facilities", "operational"),
    ("EDUCATION", "schools_built", "Schools constructed", "Écoles construites", "schools", "output"),
    ("EDUCATION", "classrooms", "Classrooms delivered", "Salles de classe livrées", "classrooms", "output"),
    ("EDUCATION", "schools_operational", "Schools operational", "Écoles fonctionnelles", "schools", "operational"),
    ("EDUCATION", "student_capacity", "Student capacity", "Capacité d'accueil", "students", "output"),
]

# --- Sector mapping from source classifications -----------------------------------------------
# OECD-DAC CRS purpose codes (3-digit category) -> AP²I sector. Documented in DATA_GOVERNANCE.md.
DAC3_TO_SECTOR: dict[str, str] = {
    "111": "EDUCATION", "112": "EDUCATION", "113": "EDUCATION", "114": "EDUCATION",
    "121": "HEALTH", "122": "HEALTH", "123": "HEALTH", "130": "HEALTH",
    "140": "WATER",
    "151": "PUBADMIN", "152": "PUBADMIN",
    "160": "OTHER",
    "210": "TRANSPORT",
    "220": "DIGITAL",
    "230": "ENERGY", "231": "ENERGY", "232": "ENERGY", "233": "ENERGY", "234": "ENERGY",
    "235": "ENERGY", "236": "ENERGY",
    "240": "OTHER", "250": "OTHER",
    "311": "AGRICULTURE", "312": "NATRES", "313": "AGRICULTURE",
    "321": "INDUSTRY", "322": "MINING", "323": "URBAN",
    "331": "OTHER", "332": "OTHER",
    "410": "ENVIRONMENT",
    "430": "OTHER",
    "510": "PUBADMIN", "520": "AGRICULTURE", "530": "OTHER", "600": "OTHER",
    "720": "OTHER", "730": "OTHER", "740": "OTHER", "910": "OTHER", "930": "OTHER", "998": "OTHER",
}
# 5-digit refinements that override the 3-digit category.
DAC5_TO_SECTOR: dict[str, str] = {
    "16030": "HOUSING", "16040": "HOUSING",
    "43030": "URBAN", "43040": "AGRICULTURE",
    "41030": "ENVIRONMENT",
}

# World Bank major sector names (as published in the Projects API `mjsector_namecode`).
WB_MAJOR_SECTOR_TO_SECTOR: dict[str, str] = {
    "energy and extractives": "ENERGY",
    "transportation": "TRANSPORT",
    "water, sanitation and waste management": "WATER",
    "water/sanit/waste": "WATER",
    "health": "HEALTH",
    "health and other social services": "HEALTH",
    "education": "EDUCATION",
    "agriculture, fishing and forestry": "AGRICULTURE",
    "agriculture": "AGRICULTURE",
    "industry, trade and services": "INDUSTRY",
    "industry and trade": "INDUSTRY",
    "information and communications technologies": "DIGITAL",
    "information and communications": "DIGITAL",
    "public administration": "PUBADMIN",
    "public administration, law, and justice": "PUBADMIN",
    "social protection": "OTHER",
    "financial sector": "OTHER",
    "finance": "OTHER",
}

# --- Financing instruments ---------------------------------------------------------------------
INSTRUMENTS: list[tuple[str, str, str]] = [
    ("LOAN", "Loan", "Prêt"),
    ("CONCESSIONAL_LOAN", "Concessional loan", "Prêt concessionnel"),
    ("GRANT", "Grant", "Don"),
    ("CREDIT", "Credit (IDA)", "Crédit (IDA)"),
    ("GUARANTEE", "Guarantee", "Garantie"),
    ("EQUITY", "Equity", "Prise de participation"),
    ("BUDGET_SUPPORT", "Budget support", "Appui budgétaire"),
    ("PROGRAM_FOR_RESULTS", "Program-for-Results", "Programme pour les résultats"),
    ("DEVELOPMENT_POLICY", "Development policy financing", "Financement de politique de développement"),
    ("TECHNICAL_ASSISTANCE", "Technical assistance", "Assistance technique"),
    ("GOVERNMENT_BUDGET", "Government budget", "Budget de l'État"),
    ("OTHER", "Other / not stated", "Autre / non précisé"),
]

# IATI finance-type codes -> instrument
IATI_FINANCE_TYPE_TO_INSTRUMENT = {
    "110": "GRANT", "111": "GRANT",
    "410": "LOAN", "411": "LOAN", "412": "LOAN", "413": "LOAN", "414": "LOAN",
    "421": "LOAN", "422": "LOAN", "423": "LOAN", "424": "LOAN", "425": "LOAN",
    "510": "EQUITY", "520": "EQUITY", "530": "EQUITY",
    "1100": "GUARANTEE",
}

WB_LENDING_INSTRUMENT_TO_INSTRUMENT = {
    "investment project financing": "LOAN",
    "program-for-results financing": "PROGRAM_FOR_RESULTS",
    "development policy lending": "DEVELOPMENT_POLICY",
    "specific investment loan": "LOAN",
    "sector investment and maintenance loan": "LOAN",
    "technical assistance loan": "TECHNICAL_ASSISTANCE",
    "structural adjustment loan": "DEVELOPMENT_POLICY",
    "emergency recovery loan": "LOAN",
    "adaptable program loan": "LOAN",
    "learning and innovation loan": "LOAN",
    "financial intermediary loan": "LOAN",
    "sector adjustment loan": "DEVELOPMENT_POLICY",
    "poverty reduction support credit": "DEVELOPMENT_POLICY",
}

# --- Donor registry (Master prompt §8) ----------------------------------------------------------
# iati_org_refs: ONLY references observed as `reporting-org/@ref` in real IATI data for Cameroon
# (checked 2026-10-22 against datastore.codeforiati.org; see docs/DATA_SOURCES.md). Empty list =
# not verified; such donors need a source-specific connector or the manual import workflow.
DONORS: list[dict] = [
    # Tier 1
    {"code": "WB", "name": "World Bank Group (IBRD/IDA)", "short_name": "World Bank", "partner_type": "multilateral",
     "tier": 1, "iati_org_refs": ["44000"], "connector_key": "worldbank_projects", "website": "https://projects.worldbank.org"},
    {"code": "AFDB", "name": "African Development Bank Group", "short_name": "AfDB", "partner_type": "multilateral",
     "tier": 1, "iati_org_refs": ["XM-DAC-46002"], "connector_key": "afdb_iati", "website": "https://www.afdb.org"},
    {"code": "IATI", "name": "International Aid Transparency Initiative (all publishers)", "short_name": "IATI",
     "partner_type": "data_standard", "tier": 1, "iati_org_refs": [], "connector_key": "iati_generic",
     "website": "https://iatistandard.org"},
    {"code": "AFD", "name": "Agence Française de Développement", "short_name": "AFD", "partner_type": "bilateral",
     "tier": 1, "iati_org_refs": ["FR-3"], "connector_key": "afd_iati", "website": "https://www.afd.fr"},
    # Tier 2
    {"code": "EIB", "name": "European Investment Bank", "short_name": "EIB", "partner_type": "multilateral",
     "tier": 2, "iati_org_refs": ["XM-DAC-918-3"], "connector_key": "eib_iati", "website": "https://www.eib.org"},
    {"code": "EU", "name": "European Union — DG International Partnerships", "short_name": "EU", "partner_type": "multilateral",
     "tier": 2, "iati_org_refs": ["XI-IATI-EC_INTPA"], "connector_key": "eu_intpa_iati", "website": "https://international-partnerships.ec.europa.eu"},
    {"code": "ISDB", "name": "Islamic Development Bank", "short_name": "IsDB", "partner_type": "multilateral",
     "tier": 2, "iati_org_refs": [], "connector_key": None, "website": "https://www.isdb.org"},
    {"code": "KFW", "name": "KfW Development Bank", "short_name": "KfW", "partner_type": "bilateral",
     "tier": 2, "iati_org_refs": [], "connector_key": None, "website": "https://www.kfw-entwicklungsbank.de",
     "notes": "Not observed as a separate IATI reporting-org for Cameroon; German official flows appear under DE-1 (BMZ)."},
    {"code": "JICA", "name": "Japan International Cooperation Agency", "short_name": "JICA", "partner_type": "bilateral",
     "tier": 2, "iati_org_refs": [], "connector_key": None, "website": "https://www.jica.go.jp"},
    {"code": "GEF", "name": "Global Environment Facility", "short_name": "GEF", "partner_type": "fund",
     "tier": 2, "iati_org_refs": [], "connector_key": None, "website": "https://www.thegef.org"},
    {"code": "GCF", "name": "Green Climate Fund", "short_name": "GCF", "partner_type": "fund",
     "tier": 2, "iati_org_refs": [], "connector_key": None, "website": "https://www.greenclimate.fund"},
    # Tier 3
    {"code": "BADEA", "name": "Arab Bank for Economic Development in Africa", "short_name": "BADEA", "partner_type": "multilateral",
     "tier": 3, "iati_org_refs": [], "connector_key": None, "website": "https://www.badea.org"},
    {"code": "SFD", "name": "Saudi Fund for Development", "short_name": "SFD", "partner_type": "bilateral",
     "tier": 3, "iati_org_refs": [], "connector_key": None, "website": "https://www.sfd.gov.sa"},
    {"code": "KFAED", "name": "Kuwait Fund for Arab Economic Development", "short_name": "Kuwait Fund", "partner_type": "bilateral",
     "tier": 3, "iati_org_refs": [], "connector_key": None, "website": "https://www.kuwait-fund.org"},
    {"code": "ADFD", "name": "Abu Dhabi Fund for Development", "short_name": "ADFD", "partner_type": "bilateral",
     "tier": 3, "iati_org_refs": [], "connector_key": None, "website": "https://www.adfd.ae"},
    {"code": "IFAD", "name": "International Fund for Agricultural Development", "short_name": "IFAD", "partner_type": "un_agency",
     "tier": 3, "iati_org_refs": ["XM-DAC-41108"], "connector_key": "ifad_iati", "website": "https://www.ifad.org"},
    {"code": "UNDP", "name": "United Nations Development Programme", "short_name": "UNDP", "partner_type": "un_agency",
     "tier": 3, "iati_org_refs": ["XM-DAC-41114"], "connector_key": "undp_iati", "website": "https://www.undp.org"},
    {"code": "UNICEF", "name": "UNICEF", "short_name": "UNICEF", "partner_type": "un_agency",
     "tier": 3, "iati_org_refs": ["XM-DAC-41122"], "connector_key": "unicef_iati", "website": "https://www.unicef.org"},
    {"code": "FAO", "name": "Food and Agriculture Organization", "short_name": "FAO", "partner_type": "un_agency",
     "tier": 3, "iati_org_refs": ["XM-DAC-41301"], "connector_key": "fao_iati", "website": "https://www.fao.org"},
    {"code": "UNIDO", "name": "United Nations Industrial Development Organization", "short_name": "UNIDO", "partner_type": "un_agency",
     "tier": 3, "iati_org_refs": ["XM-DAC-41123"], "connector_key": "unido_iati", "website": "https://www.unido.org"},
    {"code": "BMZ", "name": "German Federal Ministry for Economic Cooperation and Development", "short_name": "BMZ",
     "partner_type": "bilateral", "tier": 3, "iati_org_refs": ["DE-1"], "connector_key": "bmz_iati", "website": "https://www.bmz.de"},
    {"code": "GOV", "name": "National government (own resources)", "short_name": "Government", "partner_type": "government",
     "tier": 1, "iati_org_refs": [], "connector_key": "national_budget_upload", "website": None},
]

# --- Roles & permissions (Master prompt §25) ---------------------------------------------------
P_READ_PUBLIC = "read:public"
P_READ_DETAIL = "read:detail"
P_EXPORT = "export"
P_ANALYTICS = "analytics:advanced"
P_TENANT_READ = "tenant:read"
P_TENANT_WRITE = "tenant:write"
P_RESCUE = "rescue:use"
P_CONTRIBUTE = "data:contribute"
P_REVIEW = "data:review"
P_ADMIN_ORG = "admin:organization"
P_ADMIN_ALL = "admin:all"
P_ASSISTANT = "assistant:use"

ROLES: list[tuple[str, str, str, list[str]]] = [
    ("public_visitor", "Public visitor", "Visiteur public", [P_READ_PUBLIC]),
    ("registered_user", "Registered user", "Utilisateur inscrit", [P_READ_PUBLIC, P_ASSISTANT]),
    ("professional_subscriber", "Professional subscriber", "Abonné professionnel",
     [P_READ_PUBLIC, P_READ_DETAIL, P_EXPORT, P_ANALYTICS, P_ASSISTANT]),
    ("government_analyst", "Government analyst", "Analyste gouvernemental",
     [P_READ_PUBLIC, P_READ_DETAIL, P_EXPORT, P_ANALYTICS, P_TENANT_READ, P_RESCUE, P_ASSISTANT]),
    ("government_administrator", "Government administrator", "Administrateur gouvernemental",
     [P_READ_PUBLIC, P_READ_DETAIL, P_EXPORT, P_ANALYTICS, P_TENANT_READ, P_TENANT_WRITE, P_RESCUE, P_ADMIN_ORG, P_ASSISTANT]),
    ("dfi_analyst", "DFI analyst", "Analyste IFD",
     [P_READ_PUBLIC, P_READ_DETAIL, P_EXPORT, P_ANALYTICS, P_TENANT_READ, P_RESCUE, P_ASSISTANT]),
    ("institutional_administrator", "Institutional administrator", "Administrateur institutionnel",
     [P_READ_PUBLIC, P_READ_DETAIL, P_EXPORT, P_ANALYTICS, P_TENANT_READ, P_TENANT_WRITE, P_RESCUE, P_ADMIN_ORG, P_ASSISTANT]),
    ("data_contributor", "Data contributor", "Contributeur de données",
     [P_READ_PUBLIC, P_READ_DETAIL, P_CONTRIBUTE, P_TENANT_READ, P_TENANT_WRITE]),
    ("data_reviewer", "Data reviewer", "Réviseur de données",
     [P_READ_PUBLIC, P_READ_DETAIL, P_EXPORT, P_CONTRIBUTE, P_REVIEW, P_TENANT_READ]),
    ("ap2i_super_admin", "AP²I super administrator", "Super-administrateur AP²I",
     [P_READ_PUBLIC, P_READ_DETAIL, P_EXPORT, P_ANALYTICS, P_TENANT_READ, P_TENANT_WRITE, P_RESCUE,
      P_CONTRIBUTE, P_REVIEW, P_ADMIN_ORG, P_ADMIN_ALL, P_ASSISTANT]),
]

# --- Subscription plans (Master prompt §26). Prices are configuration: NULL = on request. ------
PLANS: list[dict] = [
    {"code": "public", "name_en": "Public", "name_fr": "Public", "price_amount": None, "price_currency": None,
     "billing_period": None, "sort_order": 0,
     "features": ["basic_search", "country_summaries", "public_dashboards"]},
    {"code": "professional", "name_en": "Professional", "name_fr": "Professionnel", "price_amount": None,
     "price_currency": "EUR", "billing_period": "month", "sort_order": 1,
     "features": ["basic_search", "country_summaries", "public_dashboards", "advanced_analytics",
                  "project_details", "custom_filters", "exports", "saved_searches"]},
    {"code": "institutional", "name_en": "Institutional", "name_fr": "Institutionnel", "price_amount": None,
     "price_currency": "EUR", "billing_period": "year", "sort_order": 2,
     "features": ["basic_search", "country_summaries", "public_dashboards", "advanced_analytics",
                  "project_details", "custom_filters", "exports", "saved_searches", "private_portfolios",
                  "project_rescue", "team_collaboration", "advanced_reports", "institutional_imports"]},
    {"code": "enterprise", "name_en": "Enterprise", "name_fr": "Entreprise", "price_amount": None,
     "price_currency": "EUR", "billing_period": "year", "sort_order": 3,
     "features": ["basic_search", "country_summaries", "public_dashboards", "advanced_analytics",
                  "project_details", "custom_filters", "exports", "saved_searches", "private_portfolios",
                  "project_rescue", "team_collaboration", "advanced_reports", "institutional_imports",
                  "api_access", "custom_integrations", "dedicated_workspace"]},
]
