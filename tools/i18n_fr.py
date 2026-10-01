"""French dictionary for the workbook builders (exact-match translation of English strings)."""

SHEETS = {
    "Start Here": "Commencer ici",
    "Inputs": "Hypothèses",
    "Load Profile": "Courbe de charge",
    "Productive Use": "Usages productifs",
    "Dashboard": "Tableau de bord",
    "Funding Gap & RBF": "Déficit de financement & RBF",
    "Sensitivity": "Sensibilité",
    "Impact & MRV": "Impact & MRV",
    "Financing Request": "Demande de financement",
    "Cash Flow": "Flux de trésorerie",
    "Checks": "Contrôles",
}

SUFFIXES = {"  [B = NPV]": "  [B = VAN]"}

DICT = {
    # ------------------------------------------------------------------ common words / verdicts
    "YES": "OUI", "NO": "NON", "NO - ": "NON - ", "OK": "OK", "ALL OK": "TOUT OK", "CHECK": "À VÉRIFIER", "REVIEW": "À REVOIR",
    "n/a": "n.d.", "no debt": "pas de dette", "No debt": "Pas de dette", "> life": "> durée de vie",
    "NO - above threshold": "NON - au-dessus du seuil", "NO - gap remains": "NON - déficit restant",
    "NO - needs subsidy": "NON - subvention nécessaire", "NO - resize debt": "NON - redimensionner la dette",
    "NO - see RBF needed": "NON - voir RBF nécessaire", "NO - tariff below cost": "NON - tarif inférieur au coût",
    "Base": "Base", "Conservative": "Prudent", "Optimistic": "Optimiste", "Custom": "Personnalisé",
    "USD": "USD", "Currency": "Devise", "Invalid": "Valeur invalide",
    "Enter a value between 0% and 100%.": "Saisissez une valeur entre 0 % et 100 %.",
    "Project life must be 1-20 years.": "La durée de vie doit être comprise entre 1 et 20 ans.",
    "Select from the drop-down list.": "Choisir dans la liste déroulante.",
    "Total": "Total", "Year": "Année", "year": "année", "years": "ans", "Unit": "Unité", "Units": "Unités",
    "people": "personnes", "jobs": "emplois", "kW": "kW", "kWh": "kWh", "kWp": "kWc", "kWh/yr": "kWh/an",
    "kWh/kWp/yr": "kWh/kWc/an", "kWh/litre": "kWh/litre", "kgCO2/litre": "kgCO2/litre",
    "per connection": "par raccordement", "per kW": "par kW", "per kWh": "par kWh", "per kWp": "par kWc",
    "per kWh diesel": "par kWh diesel", "per litre": "par litre", "per year": "par an",
    "of hard CAPEX": "du CAPEX direct", "of hard CAPEX / yr": "du CAPEX direct / an", "of total CAPEX / yr": "du CAPEX total / an",
    "of revenue": "du chiffre d'affaires",
    "Example Energy Ltd": "Énergie Exemple SARL", "Example site": "Site exemple", "Example village mini-grid": "Mini-réseau villageois (exemple)",

    # ------------------------------------------------------------------ P1 Start Here
    "Mini-Grid Financial Feasibility Calculator": "Calculateur de faisabilité financière de mini-réseau",
    "Solar PV + Battery + Diesel hybrid  |  20-year annual model  |  Energy-access edition":
        "Hybride solaire PV + batterie + diesel  |  modèle annuel sur 20 ans  |  édition accès à l'énergie",
    "WHAT THIS TOOL ANSWERS": "À QUELLE QUESTION RÉPOND CET OUTIL",
    "Is this mini-grid financially viable, can it carry debt, and how much subsidy (grant / RBF) closes the gap?":
        "Ce mini-réseau est-il financièrement viable, peut-il supporter de la dette, et quelle subvention (grant / RBF) comble le déficit ?",
    "HOW TO USE IT (10 minutes)": "MODE D'EMPLOI (10 minutes)",
    "1. Go to 'Inputs'. Edit ONLY the yellow cells with blue text. Every other cell is a formula.":
        "1. Allez dans « Hypothèses ». Modifiez UNIQUEMENT les cellules jaunes à texte bleu. Toutes les autres cellules sont des formules.",
    "2. Enter your customer segments (households, productive users, commercial, institutions).":
        "2. Saisissez vos segments de clientèle (ménages, usagers productifs, commerces, institutions).",
    "3. Check the auto-sizing on 'Inputs' (PV, battery, diesel). Type a value in the Override column to force your own design.":
        "3. Vérifiez le dimensionnement automatique dans « Hypothèses » (PV, batterie, diesel). Saisissez une valeur dans la colonne Forçage pour imposer votre propre conception.",
    "4. Enter unit costs, operating costs and the financing structure (grant, RBF per connection, debt).":
        "4. Saisissez les coûts unitaires, les coûts d'exploitation et la structure de financement (grant, RBF par raccordement, dette).",
    "5. Read 'Dashboard': IRR, NPV, LCOE, DSCR, payback, and the viability gap (subsidy needed to reach your hurdle rate).":
        "5. Lisez le « Tableau de bord » : TRI, VAN, LCOE, DSCR, délai de récupération et déficit de viabilité (subvention nécessaire pour atteindre votre taux de rendement minimal).",
    "6. Use the Scenario levers on 'Inputs' (tariff, demand, CAPEX multipliers) to stress-test the project.":
        "6. Utilisez les leviers de scénario dans « Hypothèses » (multiplicateurs de tarif, demande, CAPEX) pour tester la résistance du projet.",
    "COLOUR LEGEND": "LÉGENDE DES COULEURS",
    "Blue text on yellow fill = input you may change   |   Black text = formula, do not overwrite   |   Green text = link to another sheet":
        "Texte bleu sur fond jaune = hypothèse modifiable   |   Texte noir = formule, ne pas écraser   |   Texte vert = lien vers un autre onglet",
    "SHEETS": "ONGLETS",
    "Inputs      - all assumptions, auto-sizing and scenario levers": "Hypothèses         - toutes les hypothèses, le dimensionnement automatique et les leviers de scénario",
    "Cash Flow   - 20-year annual engine: demand, generation, revenue, OPEX, tax, debt, CFADS, DSCR, project and equity cash flows":
        "Flux de trésorerie - moteur annuel sur 20 ans : demande, production, recettes, OPEX, impôt, dette, CFADS, DSCR, flux projet et fonds propres",
    "Dashboard   - KPIs, bankability checks, viability gap and charts": "Tableau de bord    - indicateurs clés, tests de bancabilité, déficit de viabilité et graphiques",
    "Checks      - integrity checks (should all read OK)": "Contrôles          - contrôles d'intégrité (tous doivent afficher OK)",
    "KEY SIMPLIFICATIONS (read before relying on results)": "PRINCIPALES SIMPLIFICATIONS (à lire avant d'utiliser les résultats)",
    "- Annual time step; construction in Year 0, operations from Year 1. No intra-year dispatch: solar share is capped by the target solar fraction (storage limit).":
        "- Pas de temps annuel ; construction en année 0, exploitation à partir de l'année 1. Pas de dispatch infra-annuel : la part solaire est plafonnée par la fraction solaire cible (limite du stockage).",
    "- Tax: flat rate on positive taxable profit, no loss carry-forward. RBF and grants are treated as non-taxable cash inflows. Check local tax treatment.":
        "- Impôt : taux unique sur le bénéfice imposable positif, sans report des pertes. Le RBF et les subventions sont traités comme des encaissements non imposables. Vérifiez le régime fiscal local.",
    "- Debt: single senior loan, annuity repayment after optional interest-only grace years. No DSRA, no fees, no refinancing.":
        "- Dette : un seul prêt senior, remboursement par annuités après d'éventuelles années de différé (intérêts seuls). Pas de DSRA, pas de frais, pas de refinancement.",
    "- PV and battery capacity are fixed after Year 0. If demand keeps growing, diesel fills the gap and fuel costs rise. Plan an expansion or cap growth.":
        "- Les capacités PV et batterie sont fixes après l'année 0. Si la demande continue de croître, le diesel comble l'écart et le coût du carburant augmente. Prévoyez une extension ou plafonnez la croissance.",
    "- Battery replacements create negative cash-flow years, so IRR can be misleading. Use NPV and the viability gap as the primary decision metrics.":
        "- Les remplacements de batteries créent des années de flux négatifs : le TRI peut donc être trompeur. Utilisez la VAN et le déficit de viabilité comme critères de décision principaux.",
    "- Viability gap = upfront subsidy that brings the pre-subsidy project NPV (at the hurdle rate) to zero.":
        "- Déficit de viabilité = subvention initiale qui ramène à zéro la VAN du projet avant subventions (au taux de rendement minimal).",
    "- The example values pre-filled are ILLUSTRATIVE ONLY. They are not market benchmarks. Replace them with your own project data and quotes.":
        "- Les valeurs d'exemple pré-remplies sont PUREMENT ILLUSTRATIVES. Ce ne sont pas des références de marché. Remplacez-les par vos propres données et devis.",
    "DISCLAIMER": "AVERTISSEMENT",
    "This workbook is a screening tool for educational and pre-feasibility purposes. It is not investment, legal, tax or engineering advice.":
        "Ce classeur est un outil de présélection à visée pédagogique et de préfaisabilité. Il ne constitue pas un conseil en investissement, juridique, fiscal ou d'ingénierie.",
    "Results depend entirely on the inputs you provide. Perform independent technical and financial due diligence before any investment decision.":
        "Les résultats dépendent entièrement des hypothèses saisies. Réalisez une due diligence technique et financière indépendante avant toute décision d'investissement.",
    "Licence: single user / single organisation. Do not resell or redistribute.":
        "Licence : un utilisateur / une organisation. Revente et redistribution interdites.",

    # ------------------------------------------------------------------ P2 Start Here
    "Energy Access Project Financial Model - Developer Edition": "Modèle financier de projet d'accès à l'énergie - Édition Développeur",
    "From community demand to a bankable funding request  |  Solar PV + battery + diesel mini-grids  |  20-year annual model":
        "De la demande communautaire à une demande de financement bancable  |  Mini-réseaux solaire PV + batterie + diesel  |  modèle annuel sur 20 ans",
    "THE QUESTION THIS MODEL ANSWERS": "LA QUESTION À LAQUELLE RÉPOND CE MODÈLE",
    "Can this energy-access project be made bankable, and what combination of grant, RBF, concessional debt, senior debt and equity does it need?":
        "Ce projet d'accès à l'énergie peut-il devenir bancable, et quelle combinaison de subvention, RBF, dette concessionnelle, dette senior et fonds propres lui faut-il ?",
    "WORKFLOW": "DÉMARCHE",
    "1. Inputs           - project, scenarios, customer segments (tariff, RBF, income), technical, CAPEX, OPEX, financing, impact.":
        "1. Hypothèses       - projet, scénarios, segments de clientèle (tarif, RBF, revenu), technique, CAPEX, OPEX, financement, impact.",
    "2. Load Profile     - hourly load shape per segment. Drives the night-time energy share (battery size) and the peak ratio (generator size).":
        "2. Courbe de charge - profil horaire par segment. Détermine la part d'énergie nocturne (taille de la batterie) et le ratio de pointe (taille du groupe).",
    "3. Productive Use   - appliance inventory (mills, welding, cold rooms, pumps...). Can drive productive users' consumption.":
        "3. Usages productifs - inventaire des équipements (moulins, soudure, chambres froides, pompes...). Peut déterminer la consommation des usagers productifs.",
    "4. Dashboard        - KPIs, bankability verdict, affordability by segment, charts.":
        "4. Tableau de bord  - indicateurs clés, verdict de bancabilité, capacité de paiement par segment, graphiques.",
    "5. Funding Gap & RBF - viability gap, grant needed, RBF per connection needed for the project hurdle and the equity target, debt capacity.":
        "5. Déficit de financement & RBF - déficit de viabilité, subvention nécessaire, RBF par raccordement nécessaire pour le taux minimal du projet et la cible des fonds propres, capacité d'endettement.",
    "6. Sensitivity      - live tornado: tariff, demand, CAPEX, OPEX, collection, diesel price, interest rate.":
        "6. Sensibilité      - tornado dynamique : tarif, demande, CAPEX, OPEX, recouvrement, prix du diesel, taux d'intérêt.",
    "7. Impact & MRV     - connections, people, productive users, energy, CO2, RBF disbursements, cost-effectiveness ratios.":
        "7. Impact & MRV     - raccordements, personnes, usagers productifs, énergie, CO2, décaissements RBF, ratios coût-efficacité.",
    "8. Financing Request - auto-written project summary, sources & uses, key metrics. Copy into your concept note.":
        "8. Demande de financement - résumé du projet rédigé automatiquement, emplois-ressources, indicateurs clés. À copier dans votre note conceptuelle.",
    "9. Cash Flow / Checks - the engine and the integrity checks (all should read OK).":
        "9. Flux de trésorerie / Contrôles - le moteur de calcul et les contrôles d'intégrité (tous doivent afficher OK).",
    "Blue text on yellow = input   |   Black = formula (do not overwrite)   |   Green = link from another sheet":
        "Texte bleu sur jaune = hypothèse   |   Noir = formule (ne pas écraser)   |   Vert = lien depuis un autre onglet",
    "METHOD AND SIMPLIFICATIONS": "MÉTHODE ET SIMPLIFICATIONS",
    "- Annual time step. Construction in Year 0, operation Years 1-20. No hourly dispatch: solar delivery is capped by the target solar fraction.":
        "- Pas de temps annuel. Construction en année 0, exploitation années 1 à 20. Pas de dispatch horaire : la production solaire livrée est plafonnée par la fraction solaire cible.",
    "- Sizing uses base inputs. Scenario and sensitivity levers model out-turn risk on the built system (the design does not change).":
        "- Le dimensionnement utilise les hypothèses de base. Les leviers de scénario et de sensibilité modélisent le risque de réalisation sur le système construit (la conception ne change pas).",
    "- PV and battery capacity are fixed after Year 0. If demand keeps growing, diesel covers the difference and fuel cost rises.":
        "- Les capacités PV et batterie sont fixes après l'année 0. Si la demande continue de croître, le diesel couvre la différence et le coût du carburant augmente.",
    "- Tax: flat rate with unlimited loss carry-forward. Grants and RBF are treated as non-taxable. Check local tax treatment.":
        "- Impôt : taux unique avec report illimité des pertes. Les subventions et le RBF sont traités comme non imposables. Vérifiez le régime fiscal local.",
    "- Debt: senior and concessional tranches, each an annuity after interest-only grace years. DSRA funded by equity. No fees, no sculpting.":
        "- Dette : tranches senior et concessionnelle, chacune remboursée par annuités après un différé (intérêts seuls). DSRA financé par les fonds propres. Pas de frais, pas de profil sculpté.",
    "- RBF is paid per verified new connection, by segment, with an optional verification lag. RBF is not a construction source: bridge it.":
        "- Le RBF est versé par nouveau raccordement vérifié, par segment, avec un délai de vérification optionnel. Le RBF ne finance pas la construction : il faut le préfinancer.",
    "- RBF and grant needs are solved in closed form (cash flows are linear in RBF), so no Goal Seek is required.":
        "- Les besoins en RBF et en subvention sont résolus analytiquement (les flux sont linéaires en RBF) : aucune « Valeur cible » n'est nécessaire.",
    "- Battery replacements create negative cash-flow years, so IRR can mislead. Use NPV and the funding-gap metrics as primary decision tools.":
        "- Les remplacements de batteries créent des années de flux négatifs : le TRI peut être trompeur. Utilisez la VAN et les indicateurs de déficit comme outils de décision principaux.",
    "- Pre-filled values are ILLUSTRATIVE ONLY, not market benchmarks. Replace them with your project data, quotes and programme rules.":
        "- Les valeurs pré-remplies sont PUREMENT ILLUSTRATIVES et ne sont pas des références de marché. Remplacez-les par vos données de projet, devis et règles de programme.",
    "DISCLAIMER & LICENCE": "AVERTISSEMENT & LICENCE",
    "Screening and pre-feasibility tool for educational and planning purposes. Not investment, legal, tax or engineering advice.":
        "Outil de présélection et de préfaisabilité à visée pédagogique et de planification. Ne constitue pas un conseil en investissement, juridique, fiscal ou d'ingénierie.",
    "Perform independent technical and financial due diligence before any investment decision. Licence: single user / single organisation. No resale.":
        "Réalisez une due diligence technique et financière indépendante avant toute décision d'investissement. Licence : un utilisateur / une organisation. Revente interdite.",

    # ------------------------------------------------------------------ Inputs
    "INPUTS": "HYPOTHÈSES",
    "Edit yellow cells only. Example values are illustrative, not benchmarks.":
        "Ne modifiez que les cellules jaunes. Les valeurs d'exemple sont illustratives et ne sont pas des références.",
    "1. PROJECT": "1. PROJET",
    "Project name": "Nom du projet", "Country / site": "Pays / site", "Developer / sponsor": "Développeur / promoteur",
    "Currency label": "Libellé de la devise",
    "Label only. All amounts must be entered in this currency.": "Libellé uniquement. Tous les montants doivent être saisis dans cette devise.",
    "Label only. Enter every amount in this currency.": "Libellé uniquement. Saisissez tous les montants dans cette devise.",
    "First operating year": "Première année d'exploitation", "Project life": "Durée de vie du projet",
    "Maximum 20. Cash flows after this year are zero.": "Maximum 20. Les flux au-delà de cette année sont nuls.",
    "1 to 20.": "De 1 à 20.",
    "Discount rate / hurdle rate (project)": "Taux d'actualisation / taux de rendement minimal (projet)",
    "Project hurdle rate (discount rate)": "Taux de rendement minimal du projet (taux d'actualisation)",
    "Used for NPV, LCOE and viability gap.": "Utilisé pour la VAN, le LCOE et le déficit de viabilité.",
    "Used for NPV, LCOE, viability gap and RBF calibration.": "Utilisé pour la VAN, le LCOE, le déficit de viabilité et le calibrage du RBF.",
    "Target equity IRR": "TRI cible des fonds propres",
    "Minimum DSCR required by lender": "DSCR minimum exigé par le prêteur", "Minimum DSCR required by lenders": "DSCR minimum exigé par les prêteurs",
    "Tariff escalation": "Indexation du tarif",
    "Cost escalation (OPEX, fuel)": "Indexation des coûts (OPEX, carburant)",
    "Cost escalation (OPEX, fuel, replacements)": "Indexation des coûts (OPEX, carburant, remplacements)",
    "Corporate tax rate": "Taux d'impôt sur les sociétés", "Tax depreciation period": "Durée d'amortissement fiscal",
    "Straight-line on total CAPEX.": "Linéaire sur le CAPEX total.",
    "2. SCENARIO LEVERS (1.00 = base case)": "2. LEVIERS DE SCÉNARIO (1,00 = cas de base)",
    "2. SCENARIOS (multipliers on the inputs below; 1.00 = as entered)": "2. SCÉNARIOS (multiplicateurs appliqués aux hypothèses ci-dessous ; 1,00 = tel que saisi)",
    "Tariff multiplier": "Multiplicateur de tarif", "Demand multiplier": "Multiplicateur de demande",
    "CAPEX multiplier": "Multiplicateur de CAPEX", "OPEX multiplier": "Multiplicateur d'OPEX",
    "Active scenario": "Scénario actif", "Lever": "Levier", "Active": "Actif",
    "Demand (consumption per customer)": "Demande (consommation par client)",
    "Collection lever multiplies the collection rate (capped at 100%). Scenario values are illustrative.":
        "Le levier de recouvrement multiplie le taux de recouvrement (plafonné à 100 %). Les valeurs des scénarios sont illustratives.",
    "Sensitivity range (+/- applied to each variable)": "Amplitude de sensibilité (+/- appliqué à chaque variable)",
    "Used by the tornado on the 'Sensitivity' sheet.": "Utilisé par le tornado de l'onglet « Sensibilité ».",
    "3. CUSTOMERS & DEMAND": "3. CLIENTS & DEMANDE",
    "3. CUSTOMER SEGMENTS, TARIFFS, RBF AND AFFORDABILITY": "3. SEGMENTS DE CLIENTÈLE, TARIFS, RBF ET CAPACITÉ DE PAIEMENT",
    "Segment": "Segment", "Customers": "Clients", "kWh / month": "kWh / mois", "Tariff /kWh": "Tarif /kWh", "Conn. fee": "Frais de racc.",
    "Monthly bill": "Facture mensuelle", "kWh/month (entered)": "kWh/mois (saisi)", "Tariff per kWh": "Tarif par kWh",
    "Connection fee": "Frais de raccordement", "RBF per new connection": "RBF par nouveau raccordement",
    "Monthly income or revenue": "Revenu ou chiffre d'affaires mensuel", "kWh/month (used)": "kWh/mois (utilisé)",
    "Monthly bill (Yr 1)": "Facture mensuelle (an 1)", "Bill as % of income": "Facture en % du revenu", "Affordable?": "Abordable ?",
    "Households": "Ménages", "Productive users (mills, welding, cold rooms)": "Usagers productifs (moulins, soudure, chambres froides)",
    "Commercial (shops, bars, kiosks)": "Commerces (boutiques, bars, kiosques)",
    "Institutions (health centre, school, water)": "Institutions (centre de santé, école, eau)", "Other / custom": "Autre / personnalisé",
    "Total / weighted average": "Total / moyenne pondérée",
    "Monthly income: household income, or business revenue for productive/commercial users. Leave 0 for institutions.":
        "Revenu mensuel : revenu du ménage, ou chiffre d'affaires pour les usagers productifs/commerciaux. Laisser 0 pour les institutions.",
    "Use 'Productive Use' sheet for productive users' kWh? (1 = yes)": "Utiliser l'onglet « Usages productifs » pour les kWh des usagers productifs ? (1 = oui)",
    "1 = kWh/month of productive users comes from the appliance inventory.": "1 = les kWh/mois des usagers productifs proviennent de l'inventaire des équipements.",
    "Affordability threshold (max bill as % of income)": "Seuil de capacité de paiement (facture max en % du revenu)",
    "Set to your programme's own definition. Example value only.": "À fixer selon la définition de votre programme. Valeur d'exemple uniquement.",
    "Connection ramp - Year 1 (% of customers connected)": "Montée en charge des raccordements - année 1 (% des clients raccordés)",
    "Connection ramp - Year 2": "Montée en charge des raccordements - année 2",
    "Connection ramp - Year 3 onwards": "Montée en charge des raccordements - année 3 et suivantes",
    "Annual growth in consumption per customer": "Croissance annuelle de la consommation par client",
    "Collection rate (share of bills actually paid)": "Taux de recouvrement (part des factures effectivement payées)",
    "Collection rate (share of bills paid)": "Taux de recouvrement (part des factures payées)",
    "4. TECHNICAL DESIGN & AUTO-SIZING": "4. CONCEPTION TECHNIQUE & DIMENSIONNEMENT AUTOMATIQUE",
    "PV specific yield": "Productible spécifique PV", "Use PVGIS or your design study for the site.": "Utilisez PVGIS ou votre étude de conception pour le site.",
    "PV degradation": "Dégradation PV", "Distribution & conversion losses": "Pertes de distribution et de conversion",
    "Energy generated vs energy sold.": "Énergie produite par rapport à l'énergie vendue.",
    "Target solar fraction (max share of generation from PV)": "Fraction solaire cible (part max de la production issue du PV)",
    "Storage-limited cap; the rest comes from diesel.": "Plafond lié au stockage ; le reste provient du diesel.",
    "Storage-limited cap. Diesel supplies the rest.": "Plafond lié au stockage. Le diesel fournit le reste.",
    "PV oversizing factor": "Facteur de surdimensionnement PV", "Margin for weather, curtailment and growth.": "Marge pour la météo, l'écrêtage et la croissance.",
    "Share of daily energy consumed at night": "Part de l'énergie journalière consommée la nuit",
    "Battery usable depth of discharge": "Profondeur de décharge utile de la batterie",
    "Peak-to-average load ratio": "Ratio charge de pointe / charge moyenne",
    "Diesel generator efficiency": "Rendement du groupe diesel", "Diesel price at Year 1": "Prix du diesel en année 1", "Diesel price, Year 1": "Prix du diesel, année 1",
    "Night-time share of daily energy (from Load Profile)": "Part nocturne de l'énergie journalière (courbe de charge)",
    "Peak-to-average load ratio (from Load Profile)": "Ratio pointe / moyenne (courbe de charge)",
    "Component": "Composant", "Auto-size": "Auto-dimensionné", "Override": "Forçage", "Used": "Retenu",
    "Design energy sold (Year 3, full connection)": "Énergie vendue de conception (année 3, raccordement complet)",
    "Design energy sold (Year 3, full connection, base inputs)": "Énergie vendue de conception (année 3, raccordement complet, hypothèses de base)",
    "Design generation (incl. losses)": "Production de conception (pertes incluses)",
    "PV array": "Champ PV", "Battery storage (usable basis -> nameplate)": "Stockage batterie (base utile -> nominale)",
    "Battery storage (nameplate)": "Stockage batterie (nominal)",
    "Diesel generator (backup, covers peak)": "Groupe diesel (secours, couvre la pointe)", "Diesel generator (covers peak)": "Groupe diesel (couvre la pointe)",
    "Leave Override blank to use the auto-size. Auto-sizing is a screening rule of thumb, not an engineering design (use HOMER or equivalent for final design).":
        "Laissez Forçage vide pour utiliser l'auto-dimensionnement. C'est une règle empirique de présélection, pas une conception d'ingénierie (utilisez HOMER ou équivalent pour la conception finale).",
    "Leave Override blank to use the auto-size. This is a screening rule of thumb, not an engineering design.":
        "Laissez Forçage vide pour utiliser l'auto-dimensionnement. C'est une règle empirique de présélection, pas une conception d'ingénierie.",
    "5. CAPEX (unit costs, Year 0)": "5. CAPEX (coûts unitaires, année 0)", "5. CAPEX (Year 0)": "5. CAPEX (année 0)",
    "PV modules, structures & inverters": "Modules PV, structures et onduleurs", "Battery storage system": "Système de stockage par batterie",
    "Diesel generator": "Groupe diesel", "Distribution network": "Réseau de distribution", "Smart meters & service drops": "Compteurs intelligents et branchements",
    "Powerhouse, BOS, civil works (lump sum)": "Local technique, BOS, génie civil (forfait)",
    "Productive-use equipment financed by the project": "Équipements d'usage productif financés par le projet",
    "Optional: appliances the developer buys and leases or sells to users.": "Optionnel : équipements achetés par le développeur et loués ou vendus aux usagers.",
    "Development costs (studies, permits, community)": "Coûts de développement (études, permis, communauté)",
    "Contingency": "Imprévus", "Battery life": "Durée de vie des batteries", "Battery replacement cost": "Coût de remplacement des batteries",
    "Battery replacement cost (Year-0 terms)": "Coût de remplacement des batteries (valeur année 0)",
    "In real terms at Year 0, escalated with cost escalation.": "En termes réels de l'année 0, indexé avec les coûts.",
    "Fund replacements via maintenance reserve? (1 = yes, 0 = no)": "Financer les remplacements via une réserve de maintenance ? (1 = oui, 0 = non)",
    "Fund replacements via maintenance reserve? (1 = yes)": "Financer les remplacements via une réserve de maintenance ? (1 = oui)",
    "1 = annual reserve contributions smooth the battery replacement in CFADS (lender practice).":
        "1 = des dotations annuelles à la réserve lissent le remplacement des batteries dans le CFADS (pratique des prêteurs).",
    "1 = reserve contributions smooth replacements in CFADS (lender practice).": "1 = les dotations à la réserve lissent les remplacements dans le CFADS (pratique des prêteurs).",
    "Hard CAPEX": "CAPEX direct", "TOTAL CAPEX": "CAPEX TOTAL", "CAPEX per connection": "CAPEX par raccordement",
    "Hard CAPEX (base, before scenario lever)": "CAPEX direct (base, avant levier de scénario)",
    "Total CAPEX (base, before scenario lever)": "CAPEX total (base, avant levier de scénario)",
    "6. OPEX (Year-1 values, escalated)": "6. OPEX (valeurs année 1, indexées)",
    "Fixed O&M": "Exploitation et maintenance fixes", "Local staff & operator": "Personnel local et opérateur", "Insurance": "Assurance",
    "Licences, land, regulatory fees": "Licences, foncier, redevances réglementaires", "Diesel generator O&M": "Maintenance du groupe diesel",
    "Customer management, mobile money fees": "Gestion clientèle, frais de mobile money",
    "Customer management & mobile money fees": "Gestion clientèle et frais de mobile money",
    "MRV & reporting costs (programme compliance)": "Coûts MRV et reporting (conformité au programme)",
    "Verification, data platform, audits.": "Vérification, plateforme de données, audits.",
    "7. FINANCING & SUBSIDIES": "7. FINANCEMENT & SUBVENTIONS", "7. FUNDING STRUCTURE": "7. STRUCTURE DE FINANCEMENT",
    "Upfront CAPEX grant": "Subvention d'investissement initiale", "Capital subsidy received in Year 0.": "Subvention d'investissement reçue en année 0.",
    "Paid in the year the connection is made (verified).": "Versé l'année où le raccordement est réalisé (et vérifié).",
    "RBF verification lag": "Délai de vérification du RBF", "0 = paid same year, 1 = paid next year.": "0 = payé la même année, 1 = payé l'année suivante.",
    "0 = paid in the year of connection, 1 = next year. RBF amounts per segment are in section 3.":
        "0 = payé l'année du raccordement, 1 = l'année suivante. Les montants RBF par segment sont en section 3.",
    "Debt share of CAPEX net of grant": "Part de dette dans le CAPEX net de subvention", "Interest rate": "Taux d'intérêt",
    "Loan tenor (incl. grace)": "Durée du prêt (différé inclus)", "Grace period (interest only)": "Différé (intérêts seuls)",
    "Debt amount": "Montant de la dette", "Equity amount": "Montant des fonds propres",
    "Senior debt - share of CAPEX net of grant": "Dette senior - part du CAPEX net de subvention",
    "Senior debt - interest rate": "Dette senior - taux d'intérêt", "Senior debt - tenor (incl. grace)": "Dette senior - durée (différé inclus)",
    "Senior debt - grace period (interest only)": "Dette senior - différé (intérêts seuls)",
    "Concessional debt - share of CAPEX net of grant": "Dette concessionnelle - part du CAPEX net de subvention",
    "For example a DFI or climate-fund loan.": "Par exemple un prêt d'IFD ou de fonds climat.",
    "Concessional debt - interest rate": "Dette concessionnelle - taux d'intérêt",
    "Concessional debt - tenor (incl. grace)": "Dette concessionnelle - durée (différé inclus)", "Concessional debt - grace period": "Dette concessionnelle - différé",
    "DSRA target (share of next year's debt service)": "Cible du DSRA (part du service de la dette de l'année suivante)",
    "0.5 = 6 months. Funded by equity, released when the debt is repaid.": "0,5 = 6 mois. Financé par les fonds propres, libéré au remboursement de la dette.",
    "8. IMPACT": "8. IMPACT", "8. IMPACT & MRV": "8. IMPACT & MRV",
    "CO2 emission factor of diesel": "Facteur d'émission CO2 du diesel", "Diesel CO2 emission factor": "Facteur d'émission CO2 du diesel",
    "Commonly used combustion factor for diesel; verify against the standard your funder uses.":
        "Facteur de combustion couramment utilisé pour le diesel ; à vérifier selon la norme de votre bailleur.",
    "Combustion factor. Verify against your funder's standard.": "Facteur de combustion. À vérifier selon la norme de votre bailleur.",
    "Average household size": "Taille moyenne des ménages", "Jobs supported per productive user connected": "Emplois soutenus par usager productif raccordé",
    "Use your own survey data. Example value only.": "Utilisez vos propres données d'enquête. Valeur d'exemple uniquement.",
    "Baseline: share of households' energy otherwise from diesel/kerosene": "Référence : part de l'énergie qui proviendrait sinon du diesel/kérosène",
    "1 = counterfactual is fully diesel-based supply.": "1 = le scénario contrefactuel est une alimentation entièrement au diesel.",

    # ------------------------------------------------------------------ Load profile / PUE
    "LOAD PROFILE (share of each segment's daily energy, by hour)": "COURBE DE CHARGE (part de l'énergie journalière de chaque segment, par heure)",
    "Each segment column must sum to 100%. Shapes are illustrative; replace them with metered data or survey results where you have them.":
        "Chaque colonne de segment doit totaliser 100 %. Les profils sont illustratifs ; remplacez-les par des données mesurées ou d'enquête si vous en disposez.",
    "Sunrise hour (PV starts)": "Heure du lever du soleil (début PV)", "Sunset hour (PV stops)": "Heure du coucher du soleil (fin PV)",
    "Hour": "Heure", "Weighted (all)": "Pondéré (total)", "Night hour?": "Heure de nuit ?",
    "Seg 1": "Seg. 1", "Seg 2": "Seg. 2", "Seg 3": "Seg. 3", "Seg 4": "Seg. 4", "Seg 5": "Seg. 5",
    "Night-time share of daily energy": "Part nocturne de l'énergie journalière",
    "Peak-to-average ratio (peak hour share x 24)": "Ratio pointe / moyenne (part de l'heure de pointe x 24)",
    "Segment totals check": "Contrôle des totaux par segment",
    "Weighted daily load shape": "Profil de charge journalier pondéré", "Share of daily energy": "Part de l'énergie journalière",
    "PRODUCTIVE USE OF ENERGY (appliance inventory)": "USAGES PRODUCTIFS DE L'ÉNERGIE (inventaire des équipements)",
    "Inventory of productive appliances expected in the community. Values are illustrative; use your demand survey.":
        "Inventaire des équipements productifs attendus dans la communauté. Valeurs illustratives ; utilisez votre enquête de demande.",
    "Appliance / activity": "Équipement / activité", "Rated kW": "Puissance (kW)", "Hours / day": "Heures / jour", "Days / month": "Jours / mois",
    "Load factor": "Facteur de charge", "Grain mill / huller": "Moulin à grains / décortiqueuse", "Welding workshop": "Atelier de soudure",
    "Cold room / commercial refrigeration": "Chambre froide / réfrigération commerciale", "Irrigation pump": "Pompe d'irrigation",
    "Tailoring (electric sewing machines)": "Couture (machines à coudre électriques)", "Hair salon / barber": "Salon de coiffure / barbier",
    "Carpentry tools": "Outils de menuiserie", "Total productive demand": "Demande productive totale",
    "Productive users (from Inputs, segment 2)": "Usagers productifs (Hypothèses, segment 2)",
    "kWh / month per productive user": "kWh / mois par usager productif",
    "Share of total demand from productive use (Year 3)": "Part de la demande totale issue des usages productifs (année 3)",
    "Why it matters: daytime productive load uses solar directly, improves the load factor and lowers LCOE. Funders often track it as an impact indicator.":
        "Pourquoi c'est important : la charge productive diurne utilise directement le solaire, améliore le facteur de charge et réduit le LCOE. Les bailleurs en font souvent un indicateur d'impact.",

    # ------------------------------------------------------------------ Engine
    "CASH FLOW ENGINE (annual, nominal)": "MOTEUR DE FLUX DE TRÉSORERIE (annuel, nominal)",
    "All cells are formulas. Column B = total or NPV where relevant.": "Toutes les cellules sont des formules. Colonne B = total ou VAN selon le cas.",
    "All cells are formulas. Column B = total, or NPV at the hurdle rate where marked [B = NPV].":
        "Toutes les cellules sont des formules. Colonne B = total, ou VAN au taux minimal lorsque la ligne est marquée [B = VAN].",
    "CASE LEVERS (relative to the active scenario)": "LEVIERS DU CAS (par rapport au scénario actif)",
    "Tariff": "Tarif", "Demand": "Demande", "CAPEX": "CAPEX", "OPEX": "OPEX", "Collection": "Recouvrement", "Diesel price": "Prix du diesel",
    "Interest rates": "Taux d'intérêt", "Collection rate": "Taux de recouvrement",
    "CASE SUMMARY": "SYNTHÈSE DU CAS", "Total CAPEX (case)": "CAPEX total (cas)", "Hard CAPEX (case)": "CAPEX direct (cas)",
    "Senior debt": "Dette senior", "Concessional debt": "Dette concessionnelle", "Equity at construction": "Fonds propres à la construction",
    "Initial DSRA funding (equity)": "Dotation initiale du DSRA (fonds propres)",
    "Project NPV before subsidies": "VAN du projet avant subventions", "Project NPV after subsidies": "VAN du projet après subventions",
    "Project IRR before subsidies": "TRI du projet avant subventions", "Project IRR after subsidies": "TRI du projet après subventions",
    "Viability gap (PV)": "Déficit de viabilité (VA)", "Equity IRR": "TRI des fonds propres",
    "Equity NPV at target equity IRR": "VAN des fonds propres au TRI cible", "Minimum DSCR": "DSCR minimum", "Average DSCR": "DSCR moyen",
    "LCOE": "LCOE", "Levelized collected revenue per kWh": "Recette encaissée actualisée par kWh",
    "PV of verified connections (hurdle)": "VA des raccordements vérifiés (taux minimal)", "PV of RBF received (hurdle)": "VA du RBF reçu (taux minimal)",
    "PV of verified connections (equity rate)": "VA des raccordements vérifiés (taux fonds propres)",
    "PV of RBF received (equity rate)": "VA du RBF reçu (taux fonds propres)",
    "Max senior debt at min DSCR (annuity)": "Dette senior max au DSCR minimum (annuités)", "Equity payback (years)": "Délai de récupération des fonds propres (ans)",
    "Project year": "Année du projet", "Total / NPV": "Total / VAN", "Calendar year": "Année civile", "Operating flag": "Indicateur d'exploitation",
    "Connection ramp": "Montée en charge des raccordements", "Tariff index": "Indice tarifaire", "Cost index": "Indice des coûts",
    "Consumption growth index": "Indice de croissance de la consommation", "Consumption index (growth x levers)": "Indice de consommation (croissance x leviers)",
    "DEMAND & CONNECTIONS": "DEMANDE & RACCORDEMENTS", "Connections - ": "Raccordements - ", "Total connections": "Total des raccordements",
    "New connections - ": "Nouveaux raccordements - ", "New connections in year": "Nouveaux raccordements de l'année",
    "Total new (verified) connections": "Total des nouveaux raccordements (vérifiés)",
    "Energy sold (kWh) - ": "Énergie vendue (kWh) - ", "Energy sold - ": "Énergie vendue - ", " (kWh)": " (kWh)",
    "Total energy sold (kWh)": "Énergie totale vendue (kWh)", "GENERATION MIX": "MIX DE PRODUCTION",
    "Gross generation required (kWh)": "Production brute nécessaire (kWh)", "PV energy available (kWh)": "Énergie PV disponible (kWh)",
    "Solar energy delivered (kWh)": "Énergie solaire livrée (kWh)", "Diesel energy delivered (kWh)": "Énergie diesel livrée (kWh)",
    "Actual solar fraction": "Fraction solaire effective", "Diesel consumed (litres)": "Diesel consommé (litres)",
    "REVENUE": "RECETTES", "Billed revenue - ": "Recettes facturées - ", "Total billed energy revenue": "Total des recettes d'énergie facturées",
    "Collected energy revenue": "Recettes d'énergie encaissées", "Connection fees": "Frais de raccordement",
    "TOTAL OPERATING REVENUE": "TOTAL DES RECETTES D'EXPLOITATION", "OPERATING COSTS": "COÛTS D'EXPLOITATION",
    "Staff & operator": "Personnel et opérateur", "Licences & fees": "Licences et redevances", "MRV & reporting": "MRV et reporting",
    "Customer management": "Gestion clientèle", "Diesel O&M": "Maintenance diesel", "Diesel fuel": "Carburant diesel", "TOTAL OPEX": "TOTAL OPEX",
    "EBITDA": "EBE", "EBITDA margin": "Marge d'EBE", "CAPEX, REPLACEMENTS & SUBSIDIES": "CAPEX, REMPLACEMENTS & SUBVENTIONS",
    "Initial CAPEX": "CAPEX initial", "Battery replacement": "Remplacement des batteries",
    "Maintenance reserve contribution (battery)": "Dotation à la réserve de maintenance (batteries)",
    "Maintenance reserve contribution": "Dotation à la réserve de maintenance",
    "Replacement cost charged to CFADS": "Coût de remplacement imputé au CFADS", "Upfront CAPEX grant received": "Subvention d'investissement reçue",
    "RBF received": "RBF reçu", "RBF earned (new connections x RBF by segment)": "RBF acquis (nouveaux raccordements x RBF par segment)",
    "RBF received (after verification lag)": "RBF reçu (après délai de vérification)",
    "Verified connections paid (after lag)": "Raccordements vérifiés payés (après délai)",
    "TAX (simplified)": "IMPÔT (simplifié)", "TAX (loss carry-forward)": "IMPÔT (report des pertes)", "Tax depreciation": "Amortissement fiscal",
    "Tax - unlevered (for project IRR)": "Impôt - hors dette (pour le TRI projet)", "Tax - levered (after interest)": "Impôt - avec dette (après intérêts)",
    "Taxable result before losses - unlevered (project IRR)": "Résultat imposable avant pertes - hors dette (TRI projet)",
    "Taxable result before losses - levered (after interest)": "Résultat imposable avant pertes - avec dette (après intérêts)",
    "  Tax losses brought forward": "  Pertes fiscales reportées (début)", "  Losses used": "  Pertes imputées",
    "  Tax losses carried forward": "  Pertes fiscales reportables (fin)",
    "Tax paid - unlevered (project IRR)": "Impôt payé - hors dette (TRI projet)", "Tax paid - levered (after interest)": "Impôt payé - avec dette (après intérêts)",
    "SENIOR DEBT": "DETTE SENIOR", "CONCESSIONAL DEBT": "DETTE CONCESSIONNELLE", "Opening balance": "Solde d'ouverture",
    "Drawdown": "Tirage", "Interest": "Intérêts", "Principal": "Principal", "Principal repayment": "Remboursement du principal",
    "Closing balance": "Solde de clôture", "Total debt service": "Service total de la dette", "TOTAL DEBT SERVICE": "SERVICE TOTAL DE LA DETTE",
    "Senior debt service per $1 of senior debt": "Service de la dette senior par unité de dette senior",
    "Max senior debt allowed by this year's CFADS at min DSCR": "Dette senior max permise par le CFADS de l'année au DSCR minimum",
    "DSRA target balance": "Solde cible du DSRA", "DSRA funding (+) / release (-)": "Dotation (+) / libération (-) du DSRA",
    "CASH FLOWS": "FLUX DE TRÉSORERIE",
    "Project cash flow BEFORE subsidies (unlevered)": "Flux du projet AVANT subventions (hors dette)",
    "Project cash flow AFTER subsidies (unlevered)": "Flux du projet APRÈS subventions (hors dette)",
    "Project cash flow BEFORE subsidies": "Flux du projet AVANT subventions", "Project cash flow AFTER subsidies": "Flux du projet APRÈS subventions",
    "CFADS (cash flow available for debt service)": "CFADS (flux disponible pour le service de la dette)", "CFADS": "CFADS", "DSCR": "DSCR",
    "Equity cash flow": "Flux des fonds propres", "Cumulative equity cash flow": "Flux cumulé des fonds propres",
    "LCOE INPUTS (discounted at hurdle rate)": "ÉLÉMENTS DU LCOE (actualisés au taux minimal)",
    "LEVELIZED METRICS INPUTS (discounted at hurdle)": "ÉLÉMENTS DES INDICATEURS ACTUALISÉS (au taux minimal)",
    "Lifecycle cost (CAPEX + OPEX + replacements)": "Coût sur le cycle de vie (CAPEX + OPEX + remplacements)",
    "Lifecycle cost (CAPEX + OPEX excl. revenue-linked + replacements)": "Coût sur le cycle de vie (CAPEX + OPEX hors coûts liés aux recettes + remplacements)",
    "Energy sold (kWh)": "Énergie vendue (kWh)",

    # ------------------------------------------------------------------ Dashboard
    "DASHBOARD - ": "TABLEAU DE BORD - ", "Model checks: ": "Contrôles du modèle : ",
    "  |  ": "  |  ", " customers  |  ": " clients  |  ", " kWp PV / ": " kWc PV / ", " kWh battery / ": " kWh batterie / ",
    " kW diesel  |  amounts in ": " kW diesel  |  montants en ", " kW diesel  |  scenario: ": " kW diesel  |  scénario : ",
    "PROJECT ECONOMICS": "ÉCONOMIE DU PROJET", "Total CAPEX": "CAPEX total",
    "Project IRR - before subsidies": "TRI du projet - avant subventions", "Project IRR - after subsidies": "TRI du projet - après subventions",
    "Project NPV @ hurdle - before subsidies": "VAN du projet au taux minimal - avant subventions",
    "Project NPV @ hurdle - after subsidies": "VAN du projet au taux minimal - après subventions",
    "LCOE (cost per kWh sold)": "LCOE (coût par kWh vendu)", "LCOE (per kWh sold)": "LCOE (par kWh vendu)", "LCOE (per kWh)": "LCOE (par kWh)",
    "Average tariff billed (weighted, Year 1)": "Tarif moyen facturé (pondéré, année 1)", "Average tariff billed, Year 1": "Tarif moyen facturé, année 1",
    "Year-1 EBITDA margin": "Marge d'EBE année 1", "Average solar fraction (life)": "Fraction solaire moyenne (durée de vie)",
    "FINANCING & BANKABILITY": "FINANCEMENT & BANCABILITÉ", "FUNDING & BANKABILITY": "FINANCEMENT & BANCABILITÉ",
    "Total subsidies (grant + RBF, nominal)": "Total des subventions (grant + RBF, nominal)", "Subsidy share of CAPEX": "Part des subventions dans le CAPEX",
    "Lifetime CO2 avoided vs diesel-only (tCO2)": "CO2 évité sur la durée de vie vs tout-diesel (tCO2)",
    "Total energy sold over life (MWh)": "Énergie totale vendue sur la durée de vie (MWh)",
    "Upfront grant": "Subvention initiale", "RBF received (nominal, life)": "RBF reçu (nominal, durée de vie)",
    "Equity (construction + initial DSRA)": "Fonds propres (construction + DSRA initial)",
    "Viability gap (PV, before subsidies)": "Déficit de viabilité (VA, avant subventions)",
    "VIABILITY GAP & BANKABILITY VERDICT": "DÉFICIT DE VIABILITÉ & VERDICT DE BANCABILITÉ", "BANKABILITY VERDICT": "VERDICT DE BANCABILITÉ",
    "Viability gap: upfront subsidy needed for NPV = 0 at hurdle": "Déficit de viabilité : subvention initiale nécessaire pour VAN = 0 au taux minimal",
    "Viability gap per connection": "Déficit de viabilité par raccordement",
    "Subsidies already planned (PV of grant + RBF at hurdle)": "Subventions déjà prévues (VA du grant + RBF au taux minimal)",
    "Remaining funding gap after planned subsidies": "Déficit restant après subventions prévues",
    "Commercially viable without subsidy?": "Viable commercialement sans subvention ?",
    "Viable at hurdle after planned subsidies?": "Viable au taux minimal après subventions prévues ?",
    "Project viable at hurdle after planned subsidies?": "Projet viable au taux minimal après subventions prévues ?",
    "Debt covenant met (min DSCR >= required)?": "Covenant de dette respecté (DSCR min >= exigé) ?",
    "Equity IRR meets target?": "TRI des fonds propres conforme à la cible ?", "Tariff covers LCOE?": "Le tarif couvre-t-il le LCOE ?",
    "Collected tariff covers LCOE?": "Le tarif encaissé couvre-t-il le LCOE ?", "Household bills affordable?": "Factures des ménages abordables ?",
    "Equity IRR test uses equity NPV at the target rate (robust when cash flows change sign).":
        "Le test du TRI des fonds propres utilise la VAN des fonds propres au taux cible (robuste quand les flux changent de signe).",
    "Viability gap uses the pre-subsidy project cash flow discounted at the hurdle rate. It is the minimum upfront subsidy in present-value terms; RBF paid later must be larger in nominal terms.":
        "Le déficit de viabilité utilise le flux du projet avant subventions actualisé au taux minimal. C'est la subvention initiale minimale en valeur actuelle ; un RBF versé plus tard doit être plus élevé en nominal.",
    "AFFORDABILITY BY SEGMENT (Year 1)": "CAPACITÉ DE PAIEMENT PAR SEGMENT (année 1)",
    "Segment  ->  bill as % of income": "Segment  ->  facture en % du revenu", "/month)": "/mois)", "Threshold: ": "Seuil : ", " of monthly income": " du revenu mensuel",
    "Chart data is linked from 'Cash Flow' (columns L-R).": "Les données des graphiques sont liées à « Flux de trésorerie » (colonnes L-R).",
    "Chart data (linked)": "Données des graphiques (liées)", "Chart data (linked from Cash Flow)": "Données des graphiques (liées au flux de trésorerie)",
    "Revenue": "Recettes", "Debt service": "Service de la dette", "Solar kWh": "kWh solaire", "Diesel kWh": "kWh diesel",
    "Sources of funds (construction)": "Ressources (construction)", "Grant": "Subvention", "Equity": "Fonds propres",
    "Revenue vs OPEX vs CFADS": "Recettes, OPEX et CFADS", "Revenue, OPEX, CFADS, debt service": "Recettes, OPEX, CFADS, service de la dette",
    "Generation mix (kWh)": "Mix de production (kWh)", "Sources of funds": "Ressources",

    # ------------------------------------------------------------------ Funding gap & RBF
    "FUNDING GAP & RBF CALIBRATION": "DÉFICIT DE FINANCEMENT & CALIBRAGE DU RBF",
    "Closed-form solutions: project and equity cash flows are linear in the RBF amount, so these results are exact. No Goal Seek is needed.":
        "Solutions analytiques : les flux du projet et des fonds propres sont linéaires en RBF, ces résultats sont donc exacts. Aucune « Valeur cible » n'est nécessaire.",
    "1. HOW BIG IS THE GAP?": "1. QUELLE EST L'AMPLEUR DU DÉFICIT ?",
    "Viability gap: PV subsidy needed for project NPV = 0 at the hurdle rate": "Déficit de viabilité : subvention en VA nécessaire pour VAN projet = 0 au taux minimal",
    "Present-value subsidy needed with no grant and no RBF.": "Subvention en valeur actuelle nécessaire sans grant ni RBF.",
    "Planned subsidies, PV at hurdle (grant + RBF)": "Subventions prévues, VA au taux minimal (grant + RBF)",
    "Remaining project-level gap": "Déficit restant au niveau du projet",
    "0 means the planned subsidies close the gap at the hurdle rate.": "0 signifie que les subventions prévues comblent le déficit au taux minimal.",
    "2. WHAT GRANT IS NEEDED? (given the planned RBF)": "2. QUELLE SUBVENTION FAUT-IL ? (compte tenu du RBF prévu)",
    "Upfront grant needed for project NPV = 0": "Subvention initiale nécessaire pour VAN projet = 0",
    "Compare with the grant entered on Inputs.": "À comparer avec la subvention saisie dans Hypothèses.",
    "Planned grant (Inputs)": "Subvention prévue (Hypothèses)", "Grant surplus (+) / shortfall (-)": "Excédent (+) / insuffisance (-) de subvention",
    "3. WHAT RBF IS NEEDED? (given the planned grant)": "3. QUEL RBF FAUT-IL ? (compte tenu de la subvention prévue)",
    "Uniform RBF per connection for project NPV = 0 at hurdle": "RBF uniforme par raccordement pour VAN projet = 0 au taux minimal",
    "Same amount for every segment, paid with the verification lag.": "Même montant pour tous les segments, versé avec le délai de vérification.",
    "Uniform RBF per connection for equity IRR = target": "RBF uniforme par raccordement pour TRI fonds propres = cible",
    "Developer's view: RBF needed for equity to earn its target return with the current debt.":
        "Point de vue du développeur : RBF nécessaire pour que les fonds propres atteignent leur rendement cible avec la dette actuelle.",
    "Planned RBF per connection (customer-weighted average)": "RBF prévu par raccordement (moyenne pondérée par client)",
    "Scale factor on planned RBF to reach the equity target": "Facteur multiplicatif du RBF prévu pour atteindre la cible des fonds propres",
    "Multiply every segment's RBF on Inputs by this factor.": "Multipliez le RBF de chaque segment dans Hypothèses par ce facteur.",
    "Total RBF budget at the equity-target level (nominal)": "Budget RBF total au niveau de la cible des fonds propres (nominal)",
    "Useful for a programme's budget envelope.": "Utile pour l'enveloppe budgétaire d'un programme.",
    "4. HOW MUCH DEBT CAN THE PROJECT CARRY?": "4. QUELLE DETTE LE PROJET PEUT-IL SUPPORTER ?",
    "Maximum senior debt sized on min DSCR (annuity, binding year)": "Dette senior maximale au DSCR minimum (annuités, année contraignante)",
    "Largest senior loan whose annuity keeps DSCR >= minimum in every year, given current CFADS and concessional debt service.":
        "Plus grand prêt senior dont l'annuité maintient le DSCR >= minimum chaque année, compte tenu du CFADS actuel et du service de la dette concessionnelle.",
    "Senior debt planned": "Dette senior prévue", "Headroom (+) / excess (-)": "Marge (+) / excès (-)",
    "Negative: reduce senior debt, extend tenor or grace, or add RBF/grant.": "Négatif : réduire la dette senior, allonger la durée ou le différé, ou ajouter du RBF/grant.",
    "Binding year (lowest DSCR)": "Année contraignante (DSCR le plus bas)",
    "Typical cause: RBF ends while principal repayments of both tranches overlap.":
        "Cause fréquente : le RBF s'arrête alors que les remboursements des deux tranches se chevauchent.",
    "5. RBF CASH TIMING (bridge requirement)": "5. CALENDRIER DU RBF (besoin de préfinancement)",
    "RBF received in Years 1-3 (nominal)": "RBF reçu les années 1 à 3 (nominal)",
    "RBF arrives after connections are verified. CAPEX is spent in Year 0, so this amount must be bridged.":
        "Le RBF arrive après vérification des raccordements. Le CAPEX est dépensé en année 0 : ce montant doit être préfinancé.",
    "RBF as share of total CAPEX": "RBF en part du CAPEX total",

    # ------------------------------------------------------------------ Sensitivity
    "SENSITIVITY ANALYSIS (live)": "ANALYSE DE SENSIBILITÉ (dynamique)",
    "Each variable is moved by -/+ ": "Chaque variable varie de -/+ ", " around the active scenario (": " autour du scénario actif (",
    "), one at a time. Computed by hidden copies of the cash-flow engine.": "), une à la fois. Calcul par des copies masquées du moteur de flux.",
    "Variable": "Variable", "NPV after subs. (low)": "VAN après subv. (bas)", "NPV after subs. (high)": "VAN après subv. (haut)",
    "Swing": "Amplitude", "Viability gap (low)": "Déficit de viabilité (bas)", "Viability gap (high)": "Déficit de viabilité (haut)",
    "Min DSCR (low)": "DSCR min (bas)", "Min DSCR (high)": "DSCR min (haut)", "Equity IRR (low)": "TRI fonds propres (bas)",
    "Equity IRR (high)": "TRI fonds propres (haut)", "Base case": "Cas de base",
    "Low = variable x (1 - range); High = variable x (1 + range). Collection rate is capped at 100%. Interest rates do not change project NPV (unlevered); see DSCR and equity IRR.":
        "Bas = variable x (1 - amplitude) ; Haut = variable x (1 + amplitude). Le taux de recouvrement est plafonné à 100 %. Les taux d'intérêt ne modifient pas la VAN du projet (hors dette) ; voir DSCR et TRI des fonds propres.",
    "TORNADO (chart order)": "TORNADO (ordre du graphique)", "Low vs base": "Bas vs base", "High vs base": "Haut vs base",
    "Change in project NPV after subsidies vs base": "Variation de la VAN du projet après subventions vs base",
    "BREAK-EVEN INDICATORS (approximate, linear interpolation)": "INDICATEURS DE POINT MORT (approximatifs, interpolation linéaire)",
    "Tariff multiplier for NPV before subsidies = 0": "Multiplicateur de tarif pour VAN avant subventions = 0",
    "Implied break-even average tariff (no subsidy), Year 1": "Tarif moyen d'équilibre implicite (sans subvention), année 1",
    "Approximation: tax and the solar/diesel split make NPV slightly non-linear in tariff. Confirm by entering the tariff on Inputs.":
        "Approximation : l'impôt et la répartition solaire/diesel rendent la VAN légèrement non linéaire en tarif. Confirmez en saisissant le tarif dans Hypothèses.",

    # ------------------------------------------------------------------ Impact & MRV
    "IMPACT & MRV INDICATORS": "INDICATEURS D'IMPACT & MRV",
    "Annual indicators for results verification and impact reporting. Adapt definitions to your programme's MRV framework.":
        "Indicateurs annuels pour la vérification des résultats et le reporting d'impact. Adaptez les définitions au cadre MRV de votre programme.",
    "Total / end": "Total / fin", "ACCESS": "ACCÈS", "Verified new connections - ": "Nouveaux raccordements vérifiés - ",
    "Customers connected (end of year)": "Clients raccordés (fin d'année)",
    "People with electricity access (households x household size)": "Personnes ayant accès à l'électricité (ménages x taille du ménage)",
    "Productive users connected": "Usagers productifs raccordés",
    "Jobs supported (productive users x jobs per user)": "Emplois soutenus (usagers productifs x emplois par usager)",
    "Public institutions connected": "Institutions publiques raccordées", "ENERGY & CLIMATE": "ÉNERGIE & CLIMAT",
    "Energy delivered (MWh)": "Énergie livrée (MWh)", "Energy to productive users (MWh)": "Énergie livrée aux usagers productifs (MWh)",
    "Renewable generation delivered (MWh)": "Production renouvelable livrée (MWh)", "Renewable share of generation": "Part renouvelable de la production",
    "CO2 avoided vs diesel baseline (tCO2)": "CO2 évité vs référence diesel (tCO2)", "RESULTS-BASED FINANCE": "FINANCEMENT BASÉ SUR LES RÉSULTATS",
    "RBF earned (verified)": "RBF acquis (vérifié)", "RBF disbursed (after lag)": "RBF décaissé (après délai)",
    "COST-EFFECTIVENESS (life of project)": "COÛT-EFFICACITÉ (durée de vie du projet)",
    "Public grant funding (grant + RBF, nominal)": "Financement public non remboursable (grant + RBF, nominal)",
    "Private capital mobilised (senior debt + equity incl. DSRA)": "Capitaux privés mobilisés (dette senior + fonds propres yc DSRA)",
    "Leverage: private capital per $ of public grant": "Effet de levier : capitaux privés par unité de subvention publique",
    "Public grant per connection": "Subvention publique par raccordement", "Public grant per person with access": "Subvention publique par personne desservie",
    "Public grant per tCO2 avoided": "Subvention publique par tCO2 évitée", "People with access (peak)": "Personnes desservies (pic)",
    "Lifetime CO2 avoided (tCO2)": "CO2 évité sur la durée de vie (tCO2)", "Jobs supported (peak)": "Emplois soutenus (pic)",

    # ------------------------------------------------------------------ Financing request
    "FINANCING REQUEST - ": "DEMANDE DE FINANCEMENT - ",
    "Auto-generated from the model. Copy the paragraphs into your concept note and edit the wording. Check every figure before submission.":
        "Généré automatiquement par le modèle. Copiez les paragraphes dans votre note conceptuelle et adaptez la rédaction. Vérifiez chaque chiffre avant soumission.",
    "PROJECT SUMMARY": "RÉSUMÉ DU PROJET", "TECHNICAL SOLUTION": "SOLUTION TECHNIQUE", "INVESTMENT AND FUNDING GAP": "INVESTISSEMENT ET DÉFICIT DE FINANCEMENT",
    "FUNDING REQUEST": "DEMANDE DE FINANCEMENT", "BANKABILITY": "BANCABILITÉ", "IMPACT": "IMPACT",
    " will build and operate a solar PV-battery-diesel mini-grid in ": " construira et exploitera un mini-réseau solaire PV-batterie-diesel à ",
    ", connecting ": ", raccordant ", " customers (": " clients (", " households, ": " ménages, ", " productive users, ": " usagers productifs, ",
    " businesses and ": " commerces et ", " public institutions) and giving about ": " institutions publiques) et donnant accès à l'électricité à environ ",
    " people access to electricity.": " personnes.",
    "The system combines ": "Le système associe ", " kWp of solar PV, ": " kWc de solaire PV, ",
    " kWh of battery storage and ": " kWh de stockage par batterie et ",
    " kW of backup diesel capacity. It delivers ": " kW de capacité diesel de secours. Il fournit ",
    "Battery round-trip efficiency": "Rendement aller-retour de la batterie",
    "Energy out / energy in. Applies to the solar energy stored for night-time use.": "Énergie restituée / énergie stockée. S'applique à l'énergie solaire stockée pour la nuit.",
    "Storage loss factor on solar energy": "Facteur de pertes de stockage sur l'énergie solaire",
    "PV must produce this much energy per kWh of solar delivered, because night-time solar passes through the battery.":
        "Énergie que le PV doit produire par kWh solaire livré, l'énergie solaire consommée la nuit transitant par la batterie.",
    "- Night-time solar energy passes through the battery: the round-trip efficiency loss is charged to PV production.":
        "- L'énergie solaire consommée la nuit transite par la batterie : la perte liée au rendement aller-retour est imputée à la production PV.",
    " MWh over its life with an average renewable share of ": " MWh sur sa durée de vie, avec une part renouvelable moyenne de ",
    "Total investment is ": "L'investissement total s'élève à ",
    " per connection). On tariff revenue alone the project NPV at ": " par raccordement). Avec les seules recettes tarifaires, la VAN du projet à ",
    " is ": " est de ", ", a viability gap of ": ", soit un déficit de viabilité de ", " in present-value terms (": " en valeur actuelle (",
    " per connection). The levelized cost of electricity is ": " par raccordement). Le coût actualisé de l'électricité (LCOE) est de ",
    "/kWh against an average tariff of ": "/kWh, pour un tarif moyen de ", "/kWh.": "/kWh.",
    "We request an upfront grant of ": "Nous sollicitons une subvention d'investissement de ",
    " and results-based financing averaging ": " et un financement basé sur les résultats (RBF) de ",
    " per verified connection (": " en moyenne par raccordement vérifié (", " in total), alongside ": " au total), ainsi que ",
    " of concessional debt. These leverage ": " de dette concessionnelle. Ces financements mobilisent ",
    " of senior debt and ": " de dette senior et ", " of sponsor equity.": " de fonds propres du promoteur.",
    "With this structure the project NPV after subsidies is ": "Avec cette structure, la VAN du projet après subventions est de ",
    ", the minimum DSCR is ": ", le DSCR minimum est de ", " (lender requirement ": " (exigence des prêteurs : ",
    "x) and the equity IRR is ": "x) et le TRI des fonds propres est de ", " (target ": " (cible : ",
    "Over its life the project avoids about ": "Sur sa durée de vie, le projet évite environ ",
    " tCO2 relative to diesel supply and supports about ": " tCO2 par rapport à une alimentation au diesel et soutient environ ",
    " jobs in productive enterprises. Public grant funding amounts to ": " emplois dans des activités productives. Les subventions publiques représentent ",
    " per connection.": " par raccordement.",
    "USES OF FUNDS": "EMPLOIS", "SOURCES OF FUNDS": "RESSOURCES", "Solar PV": "Solaire PV", "Battery storage": "Stockage par batterie",
    "Distribution network & meters": "Réseau de distribution et compteurs", "Powerhouse, BOS, civil works": "Local technique, BOS, génie civil",
    "Productive-use equipment": "Équipements d'usage productif", "Development costs": "Coûts de développement", "Initial DSRA funding": "Dotation initiale du DSRA",
    "Upfront grant ": "Subvention initiale ", "Sponsor equity (incl. DSRA)": "Fonds propres du promoteur (yc DSRA)",
    "TOTAL USES": "TOTAL EMPLOIS", "TOTAL SOURCES": "TOTAL RESSOURCES",
    "Plus RBF of ": "Plus un RBF de ", " received after verification (bridge required).": " reçu après vérification (préfinancement nécessaire).",
    "KEY METRICS": "INDICATEURS CLÉS", "Project IRR before / after subsidies": "TRI du projet avant / après subventions",
    "Uniform RBF needed for equity target (per connection)": "RBF uniforme nécessaire pour la cible des fonds propres (par raccordement)",

    # ------------------------------------------------------------------ Checks
    "INTEGRITY CHECKS": "CONTRÔLES D'INTÉGRITÉ", "OVERALL": "GLOBAL",
    "Sources = uses at Year 0 (grant + debt + equity = CAPEX)": "Ressources = emplois en année 0 (grant + dette + fonds propres = CAPEX)",
    "Sources = uses at construction": "Ressources = emplois à la construction",
    "Debt fully repaid by end of tenor": "Dette entièrement remboursée à l'échéance",
    "Senior debt repaid by end of tenor": "Dette senior remboursée à l'échéance", "Concessional debt repaid by end of tenor": "Dette concessionnelle remboursée à l'échéance",
    "Senior + concessional share <= 100%": "Part senior + concessionnelle <= 100 %",
    "Project life within modelled horizon": "Durée de vie dans l'horizon modélisé", "Tenor within project life": "Durée du prêt dans la durée de vie",
    "Debt tenors within project life": "Durées des prêts dans la durée de vie", "Grace shorter than tenor": "Différé plus court que la durée",
    "Grace periods shorter than tenors": "Différés plus courts que les durées",
    "Connection ramp percentages between 0 and 100%": "Pourcentages de montée en charge entre 0 et 100 %",
    "Energy balance: solar + diesel = generation": "Bilan énergétique : solaire + diesel = production",
    "At least one customer entered": "Au moins un client saisi", "At least one customer": "Au moins un client",
    "Maintenance reserve contributions = replacements (when reserve used)": "Dotations à la réserve = remplacements (si réserve utilisée)",
    "Maintenance reserve contributions = replacements (when used)": "Dotations à la réserve = remplacements (si utilisée)",
    "Load profile: each segment sums to 100%": "Courbe de charge : chaque segment totalise 100 %",
    "DSRA fully released at end": "DSRA entièrement libéré à la fin",
    "Subsidy identity: NPV after = NPV before + grant + PV(RBF)": "Identité des subventions : VAN après = VAN avant + grant + VA(RBF)",
    "RBF calibration reproduces equity target (identity check)": "Le calibrage du RBF reproduit la cible des fonds propres (contrôle d'identité)",
    "Tax losses never negative": "Pertes fiscales jamais négatives",
    "Sensitivity engines reproduce base at zero range (base row = Cash Flow)": "Les moteurs de sensibilité reproduisent la base (ligne de base = Flux de trésorerie)",
}

# placeholder labels later overwritten by formulas (kept translated for cleanliness)
for _i in range(1, 6):
    DICT[f"Connections - segment {_i}"] = f"Raccordements - segment {_i}"
    DICT[f"Energy sold - segment {_i} (kWh)"] = f"Énergie vendue - segment {_i} (kWh)"
    DICT[f"Billed revenue - segment {_i}"] = f"Recettes facturées - segment {_i}"

# ---------------------------------------------------------------------- P3 Fund Manager Edition
SHEETS.update({
    "Fund Parameters": "Paramètres du fonds",
    "Pipeline": "Pipeline de projets",
    "Eligibility & Scoring": "Éligibilité & notation",
    "Allocation": "Allocation",
    "Disbursements": "Décaissements",
    "MRV Tracker": "Suivi MRV",
    "Portfolio Dashboard": "Tableau de bord portefeuille",
})
DICT.update(SHEETS)
DICT.update({
    "Y": "O", "N": "N",
    # Start Here
    "Energy Access Fund Manager Model - RBF & Portfolio Edition": "Modèle du gestionnaire de fonds d'accès à l'énergie - Édition RBF & Portefeuille",
    "From funding to impact  |  Screen, score and allocate RBF and grant funding across an energy-access project pipeline":
        "Du financement à l'impact  |  Sélectionner, noter et allouer le RBF et les subventions sur un pipeline de projets d'accès à l'énergie",
    "Which projects should the fund support, with how much RBF and grant, and what portfolio of connections, impact, leverage and risk does that buy?":
        "Quels projets le fonds doit-il soutenir, avec quels montants de RBF et de subvention, et quel portefeuille de raccordements, d'impact, d'effet de levier et de risque cela permet-il d'obtenir ?",
    "1. Fund Parameters    - envelope, costs, fund profile (RBF rates, grant share, caps, tranches), eligibility rules, scoring weights, limits.":
        "1. Paramètres du fonds - enveloppe, coûts, profil du fonds (taux RBF, part de subvention, plafonds, tranches), règles d'éligibilité, pondérations, limites.",
    "2. Pipeline           - one row per applicant project. Outputs of the Developer Edition (CAPEX, viability gap, CO2) can be pasted here.":
        "2. Pipeline de projets - une ligne par projet candidat. Les résultats de l'Édition Développeur (CAPEX, déficit de viabilité, CO2) peuvent y être collés.",
    "3. Eligibility & Scoring - eligibility tests, maximum support, request, cost-effectiveness, leverage, additionality and weighted score.":
        "3. Éligibilité & notation - tests d'éligibilité, soutien maximal, demande, coût-efficacité, effet de levier, additionnalité et score pondéré.",
    "4. Allocation         - projects funded in rank order until the envelope is used, within project and country concentration limits.":
        "4. Allocation         - projets financés par ordre de rang jusqu'à épuisement de l'enveloppe, dans les limites de concentration par projet et par pays.",
    "5. Disbursements      - grant at commissioning, RBF by tranche as connections are verified, adjusted for expected delivery by risk rating.":
        "5. Décaissements      - subvention à la mise en service, RBF par tranches à mesure de la vérification des raccordements, ajusté du taux de réalisation attendu selon le risque.",
    "6. MRV Tracker        - verified connections to date against targets, RBF earned and outstanding, status per project.":
        "6. Suivi MRV          - raccordements vérifiés à date par rapport aux cibles, RBF acquis et restant dû, statut par projet.",
    "7. Portfolio Dashboard - commitments, disbursements, connections, people, CO2, leverage, cost per connection, concentration and risk.":
        "7. Tableau de bord portefeuille - engagements, décaissements, raccordements, personnes, CO2, effet de levier, coût par raccordement, concentration et risque.",
    "8. Checks             - integrity checks (all should read OK).": "8. Contrôles          - contrôles d'intégrité (tous doivent afficher OK).",
    "- Maximum support per project = RBF (connections x rate by customer type) + CAPEX grant, capped at a share of CAPEX, an amount per project and a share of the envelope.":
        "- Soutien maximal par projet = RBF (raccordements x taux par type de client) + subvention d'investissement, plafonné en part du CAPEX, en montant par projet et en part de l'enveloppe.",
    "- Eligibility is pass/fail on each active criterion. Only eligible projects are scored, ranked and funded.":
        "- L'éligibilité est binaire pour chaque critère actif. Seuls les projets éligibles sont notés, classés et financés.",
    "- Scores (0-100) are relative to the best eligible project for cost-effectiveness, leverage, productive use and CO2; absolute for readiness, track record and risk.":
        "- Les scores (0-100) sont relatifs au meilleur projet éligible pour le coût-efficacité, l'effet de levier, les usages productifs et le CO2 ; absolus pour la maturité, l'expérience et le risque.",
    "- Additionality: a request at or below the project's viability gap (+ tolerance) scores 100; above it scores 0; no viability-gap data scores 50.":
        "- Additionnalité : une demande inférieure ou égale au déficit de viabilité du projet (+ tolérance) obtient 100 ; au-dessus, 0 ; sans donnée de déficit, 50.",
    "- Allocation is greedy by rank. With partial funding off, a project that does not fit is skipped and the next one is tested.":
        "- L'allocation suit l'ordre de rang. Si le financement partiel est désactivé, un projet qui ne tient pas est sauté et le suivant est testé.",
    "- Disbursements: annual time step. Connections are verified over three years from commissioning; RBF is paid in two tranches.":
        "- Décaissements : pas de temps annuel. Les raccordements sont vérifiés sur trois ans à partir de la mise en service ; le RBF est versé en deux tranches.",
    "- Expected delivery by risk rating reduces RBF disbursements (connections not delivered are not paid). Grants are assumed paid in full at commissioning.":
        "- Le taux de réalisation attendu selon le risque réduit les décaissements RBF (les raccordements non réalisés ne sont pas payés). Les subventions sont supposées versées intégralement à la mise en service.",
    "- Impact and leverage of funded projects are attributed pro rata to the share of their request that the fund covers.":
        "- L'impact et l'effet de levier des projets financés sont attribués au prorata de la part de leur demande couverte par le fonds.",
    "- Pre-filled projects, countries and parameters are ILLUSTRATIVE ONLY. They do not describe any real fund, programme or project.":
        "- Les projets, pays et paramètres pré-remplis sont PUREMENT ILLUSTRATIFS. Ils ne décrivent aucun fonds, programme ou projet réel.",
    "Portfolio screening and planning tool. It does not replace a fund's investment committee, due diligence, procurement rules or legal documentation.":
        "Outil de sélection et de planification de portefeuille. Il ne remplace ni le comité d'investissement d'un fonds, ni la due diligence, ni les règles de passation, ni la documentation juridique.",
    "Not investment, legal or tax advice. Licence: single user / single organisation. No resale or redistribution.":
        "Ne constitue pas un conseil en investissement, juridique ou fiscal. Licence : un utilisateur / une organisation. Revente et redistribution interdites.",
    # Fund parameters
    "FUND PARAMETERS": "PARAMÈTRES DU FONDS",
    "Edit yellow cells only. All values are illustrative and do not describe any real fund.":
        "Ne modifiez que les cellules jaunes. Toutes les valeurs sont illustratives et ne décrivent aucun fonds réel.",
    "1. FUND": "1. FONDS", "Fund name": "Nom du fonds", "Fund manager": "Gestionnaire du fonds",
    "Example Energy Access Fund": "Fonds d'accès à l'énergie (exemple)", "Example Fund Manager": "Gestionnaire de fonds (exemple)",
    "First fund year (calendar)": "Première année du fonds (calendaire)", "Total fund size": "Taille totale du fonds",
    "Fund management & MRV costs": "Coûts de gestion du fonds et MRV", "Share of fund size.": "Part de la taille du fonds.",
    "Technical assistance window": "Guichet d'assistance technique", "Share of fund size, not allocated to projects.": "Part de la taille du fonds, non allouée aux projets.",
    "Funds available for project allocation": "Fonds disponibles pour l'allocation aux projets", "Over-commitment ratio": "Taux de surengagement",
    "Commit above available funds to offset expected under-delivery of connections.":
        "Engager au-delà des fonds disponibles pour compenser la sous-réalisation attendue des raccordements.",
    "Allocation envelope (commitment limit)": "Enveloppe d'allocation (plafond d'engagement)",
    "Allow partial funding of the marginal project? (1 = yes)": "Autoriser le financement partiel du projet marginal ? (1 = oui)",
    "Maximum share of the envelope per project": "Part maximale de l'enveloppe par projet",
    "Maximum share of the envelope per country": "Part maximale de l'enveloppe par pays",
    "Additionality tolerance above the viability gap": "Tolérance d'additionnalité au-delà du déficit de viabilité",
    "A request up to viability gap x (1 + tolerance) counts as additional.": "Une demande jusqu'à déficit de viabilité x (1 + tolérance) est considérée comme additionnelle.",
    "2. FUND PROFILE (support rules)": "2. PROFIL DU FONDS (règles de soutien)", "Active profile": "Profil actif", "Rule": "Règle",
    "Per-connection RBF": "RBF par raccordement", "Capex grant + RBF": "Subvention CAPEX + RBF", "Productive-use focus": "Priorité usages productifs",
    "Generic profiles. Configure 'Custom' to mirror a specific programme's published rules.":
        "Profils génériques. Configurez « Personnalisé » pour reproduire les règles publiées d'un programme donné.",
    "RBF per household connection": "RBF par raccordement de ménage", "RBF per productive-use connection": "RBF par raccordement d'usage productif",
    "RBF per commercial connection": "RBF par raccordement commercial", "RBF per institution connection": "RBF par raccordement d'institution",
    "CAPEX grant (share of project CAPEX)": "Subvention d'investissement (part du CAPEX du projet)",
    "Maximum public support (share of CAPEX, all sources)": "Soutien public maximal (part du CAPEX, toutes sources)",
    "Maximum support per project": "Soutien maximal par projet", "RBF tranche paid at verification": "Tranche RBF versée à la vérification",
    "RBF verification lag (years)": "Délai de vérification RBF (années)",
    "The remaining RBF tranche (1 - tranche at verification) is paid one year later, after a service-continuity check.":
        "La tranche RBF restante (1 - tranche à la vérification) est versée un an plus tard, après un contrôle de continuité de service.",
    "Connections verified in commissioning year (share of target)": "Raccordements vérifiés l'année de mise en service (part de la cible)",
    "Connections verified by end of the following year (cumulative)": "Raccordements vérifiés à la fin de l'année suivante (cumulé)",
    "The rest is verified in the third year.": "Le reste est vérifié la troisième année.",
    "3. ELIGIBILITY CRITERIA (1 = apply)": "3. CRITÈRES D'ÉLIGIBILITÉ (1 = appliquer)", "Criterion": "Critère", "Threshold": "Seuil", "Apply?": "Appliquer ?",
    "Minimum number of connections": "Nombre minimal de raccordements", "Maximum CAPEX per connection": "CAPEX maximal par raccordement",
    "Minimum renewable share of generation": "Part renouvelable minimale de la production",
    "Minimum private co-finance (equity + debt) / CAPEX": "Cofinancement privé minimal (fonds propres + dette) / CAPEX",
    "Minimum readiness stage (1-5)": "Stade de maturité minimal (1-5)", "Maximum average tariff per kWh (affordability)": "Tarif moyen maximal par kWh (capacité de paiement)",
    "Minimum productive-use share of connections": "Part minimale de raccordements d'usage productif",
    "Country must be listed as eligible (table below)": "Le pays doit être déclaré éligible (tableau ci-dessous)",
    "4. ELIGIBLE COUNTRIES": "4. PAYS ÉLIGIBLES", "Country": "Pays", "Eligible? (Y/N)": "Éligible ? (O/N)",
    "Country A": "Pays A", "Country B": "Pays B", "Country C": "Pays C", "Country D": "Pays D",
    "5. SCORING WEIGHTS (must total 100%)": "5. PONDÉRATIONS DE NOTATION (total = 100 %)", "Weight": "Pondération",
    "Cost-effectiveness (fund support per connection, lower is better)": "Coût-efficacité (soutien du fonds par raccordement, plus bas = mieux)",
    "Leverage (private capital per $ of fund support)": "Effet de levier (capitaux privés par unité de soutien du fonds)",
    "Productive-use share of connections": "Part de raccordements d'usage productif",
    "Climate (lifetime CO2 avoided per $ of fund support)": "Climat (CO2 évité sur la durée de vie par unité de soutien)",
    "Readiness stage": "Stade de maturité", "Developer track record": "Expérience du développeur", "Risk rating (lower risk is better)": "Notation de risque (plus bas = mieux)",
    "Additionality (request within viability gap)": "Additionnalité (demande dans la limite du déficit de viabilité)", "Total weights": "Total des pondérations",
    "6. EXPECTED DELIVERY BY RISK RATING": "6. TAUX DE RÉALISATION ATTENDU PAR NOTATION DE RISQUE", "Risk rating": "Notation de risque",
    "Expected share of target connections delivered": "Part attendue des raccordements cibles réalisés",
    "1 = lowest risk, 5 = highest. Calibrate on the fund's own delivery history where available.":
        "1 = risque le plus faible, 5 = le plus élevé. À calibrer sur l'historique de réalisation du fonds si disponible.",
    "Enter a whole number from 1 to 5.": "Saisissez un nombre entier de 1 à 5.",
    "Commissioning must be in fund years 1 to 7 so that RBF is paid within the fund life.":
        "La mise en service doit intervenir entre les années 1 et 7 du fonds pour que le RBF soit versé pendant sa durée de vie.",
    # Pipeline
    "PROJECT PIPELINE": "PIPELINE DE PROJETS",
    "One row per applicant. Projects and figures are illustrative. Paste CAPEX, viability gap and CO2 from the Developer Edition where available.":
        "Une ligne par candidat. Projets et chiffres illustratifs. Collez le CAPEX, le déficit de viabilité et le CO2 issus de l'Édition Développeur si disponibles.",
    "Viability gap and amount requested are optional: leave blank if unknown. Technology is descriptive only.":
        "Le déficit de viabilité et le montant demandé sont optionnels : laissez vide si inconnu. La technologie est purement descriptive.",
    "Project": "Projet", "Developer": "Développeur", "Technology": "Technologie", "Readiness (1-5)": "Maturité (1-5)",
    "Track record (1-5)": "Expérience (1-5)", "Risk rating (1-5)": "Risque (1-5)", "Commissioning (fund year)": "Mise en service (année du fonds)",
    "Household connections": "Raccordements ménages", "Productive-use connections": "Raccordements usages productifs",
    "Commercial connections": "Raccordements commerciaux", "Institution connections": "Raccordements institutions", "Project CAPEX": "CAPEX du projet",
    "Developer equity": "Fonds propres du développeur", "Debt secured": "Dette obtenue", "Other grants": "Autres subventions",
    "Average tariff per kWh": "Tarif moyen par kWh", "Renewable share": "Part renouvelable",
    "Viability gap (from Developer model)": "Déficit de viabilité (modèle Développeur)", "Amount requested (optional)": "Montant demandé (optionnel)",
    "Mini-grid": "Mini-réseau", "Hybrid": "Hybride", "Solar home systems": "Kits solaires domestiques", "Productive use": "Usage productif", "Other": "Autre",
    "Project A - Lake village cluster": "Projet A - Villages du lac", "Project B - River towns": "Projet B - Bourgs du fleuve",
    "Project C - Northern corridor": "Projet C - Corridor nord", "Project D - Island grids": "Projet D - Réseaux insulaires",
    "Project E - Highland villages": "Projet E - Villages des hauts plateaux", "Project F - Market towns": "Projet F - Bourgs marchands",
    "Project G - Remote valley": "Projet G - Vallée isolée", "Project H - Agro-processing hub": "Projet H - Pôle agro-transformation",
    "Project I - Fishing communities": "Projet I - Communautés de pêcheurs", "Project J - Health and schools first": "Projet J - Santé et écoles d'abord",
    "Project K - Peri-urban extension": "Projet K - Extension périurbaine", "Project L - Mining belt": "Projet L - Zone minière",
    "Project M - Small pilot": "Projet M - Petit pilote", "Project N - Lakeside expansion": "Projet N - Extension du littoral lacustre",
    # Eligibility & scoring
    "ELIGIBILITY & SCORING": "ÉLIGIBILITÉ & NOTATION",
    "All cells are formulas. 1 = criterion met. Only eligible projects receive a score, a rank and an allocation.":
        "Toutes les cellules sont des formules. 1 = critère respecté. Seuls les projets éligibles reçoivent un score, un rang et une allocation.",
    "ELIGIBILITY TESTS": "TESTS D'ÉLIGIBILITÉ", "Private co-finance / CAPEX": "Cofinancement privé / CAPEX", "Productive-use share": "Part d'usages productifs",
    "Min. connections": "Min. raccordements", "Max. CAPEX / connection": "Max. CAPEX / raccordement", "Min. renewable share": "Min. part renouvelable",
    "Min. private co-finance": "Min. cofinancement privé", "Min. readiness": "Min. maturité", "Max. tariff": "Max. tarif",
    "Min. productive use": "Min. usages productifs", "Eligible country": "Pays éligible", "ELIGIBLE": "ÉLIGIBLE", "Eligibility status": "Statut d'éligibilité",
    "Eligible": "Éligible", "Too few connections": "Trop peu de raccordements", "CAPEX per connection too high": "CAPEX par raccordement trop élevé",
    "Renewable share too low": "Part renouvelable trop faible", "Private co-finance too low": "Cofinancement privé trop faible",
    "Not ready enough": "Maturité insuffisante", "Tariff above cap": "Tarif au-dessus du plafond", "Productive use too low": "Usages productifs insuffisants",
    "Country not eligible": "Pays non éligible", "RBF at profile rates": "RBF aux taux du profil", "CAPEX grant at profile rate": "Subvention CAPEX au taux du profil",
    "Maximum support (after caps)": "Soutien maximal (après plafonds)", "Request considered": "Demande retenue", "RBF share of request": "Part RBF de la demande",
    "Fund support per connection": "Soutien du fonds par raccordement", "Leverage (private / fund)": "Effet de levier (privé / fonds)",
    "tCO2 per $1,000 of support": "tCO2 par 1 000 de soutien", "Additionality check": "Contrôle d'additionnalité",
    "Within viability gap": "Dans le déficit de viabilité", "Above viability gap": "Au-dessus du déficit de viabilité", "No viability-gap data": "Pas de donnée de déficit",
    "Score: cost-effectiveness": "Score : coût-efficacité", "Score: leverage": "Score : effet de levier", "Score: productive use": "Score : usages productifs",
    "Score: climate": "Score : climat", "Score: readiness": "Score : maturité", "Score: track record": "Score : expérience", "Score: risk": "Score : risque",
    "Score: additionality": "Score : additionnalité", "WEIGHTED SCORE": "SCORE PONDÉRÉ", "Rank key": "Clé de rang", "RANK": "RANG",
    "Allocated": "Alloué", "Share of request funded": "Part de la demande financée", "Allocation status": "Statut d'allocation",
    "Funded": "Financé", "Partially funded": "Partiellement financé", "Not funded": "Non financé",
    "helper: 1 / support per connection": "aide : 1 / soutien par raccordement", "helper: leverage": "aide : effet de levier",
    "helper: productive share": "aide : part productive", "helper: CO2 per $": "aide : CO2 par unité",
    # Allocation
    "ALLOCATION (in rank order)": "ALLOCATION (par ordre de rang)", "Envelope: ": "Enveloppe : ", "  |  Partial funding: ": "  |  Financement partiel : ",
    "allowed": "autorisé", "not allowed": "non autorisé", "  |  Max per country: ": "  |  Max par pays : ", " of envelope": " de l'enveloppe",
    "Each row only looks at the rows above it: the envelope and country limits are applied in rank order, without circular references.":
        "Chaque ligne ne consulte que les lignes au-dessus : l'enveloppe et les limites par pays s'appliquent par ordre de rang, sans référence circulaire.",
    "Rank": "Rang", "Score": "Score", "Request": "Demande", "Envelope remaining before": "Enveloppe restante avant",
    "Country room remaining": "Marge restante du pays", "ALLOCATED": "ALLOUÉ", "Status": "Statut", "Binding constraint": "Contrainte limitante",
    "Country limit": "Limite pays", "Envelope exhausted": "Enveloppe épuisée", "TOTAL": "TOTAL",
    # Disbursements
    "DISBURSEMENTS (expected, by fund year)": "DÉCAISSEMENTS (attendus, par année du fonds)",
    "Grant: paid at commissioning. RBF: paid as connections are verified (tranche at verification, balance one year later), scaled by expected delivery.":
        "Subvention : versée à la mise en service. RBF : versé à mesure de la vérification des raccordements (tranche à la vérification, solde un an plus tard), ajusté du taux de réalisation attendu.",
    "RBF DISBURSEMENTS": "DÉCAISSEMENTS RBF", "GRANT DISBURSEMENTS": "DÉCAISSEMENTS DE SUBVENTIONS", "TOTAL DISBURSEMENTS": "DÉCAISSEMENTS TOTAUX",
    "Allocated RBF": "RBF alloué", "Allocated grant": "Subvention allouée", "Expected delivery": "Réalisation attendue", "Expected total": "Total attendu",
    "FUND CASH POSITION": "TRÉSORERIE DU FONDS", "Expected disbursements": "Décaissements attendus", "Cumulative disbursements": "Décaissements cumulés",
    "Funds available for projects, remaining": "Fonds disponibles pour les projets, restants", "Undisbursed commitments": "Engagements non décaissés",
    "Expected decommitment (RBF not earned)": "Désengagement attendu (RBF non acquis)", "Lowest remaining balance over fund life": "Solde restant le plus bas sur la durée du fonds",
    # MRV
    "MRV TRACKER": "SUIVI MRV",
    "Enter verified connections and RBF paid to date (yellow). Status compares progress with the expected verification profile.":
        "Saisissez les raccordements vérifiés et le RBF payé à date (jaune). Le statut compare l'avancement au profil de vérification attendu.",
    "Reporting fund year": "Année de reporting du fonds", "= calendar year ": "= année civile ", "Target connections": "Raccordements cibles",
    "Verified connections to date": "Raccordements vérifiés à date", "Achieved": "Réalisé", "Expected by now": "Attendu à date",
    "RBF earned to date (all tranches)": "RBF acquis à date (toutes tranches)", "RBF paid to date": "RBF payé à date", "Outstanding RBF": "RBF restant dû",
    "Not started": "Non démarré", "On track": "Dans les temps", "Behind": "En retard", "Off track": "Hors trajectoire",
    "Outstanding RBF = RBF earned x tranche at verification - RBF paid. The balance tranche falls due after the service-continuity check.":
        "RBF restant dû = RBF acquis x tranche à la vérification - RBF payé. La tranche de solde est due après le contrôle de continuité de service.",
    # Dashboard
    "PORTFOLIO DASHBOARD - ": "TABLEAU DE BORD PORTEFEUILLE - ", "  |  profile: ": "  |  profil : ", "  |  fund size ": "  |  taille du fonds ",
    "COMMITMENTS": "ENGAGEMENTS", "Fund size": "Taille du fonds", "Available for projects (after management and TA)": "Disponible pour les projets (après gestion et AT)",
    "Allocation envelope (with over-commitment)": "Enveloppe d'allocation (avec surengagement)", "Requested by eligible projects": "Demandé par les projets éligibles",
    "Oversubscription (requested / envelope)": "Sursouscription (demandé / enveloppe)", "  of which RBF": "  dont RBF", "  of which CAPEX grants": "  dont subventions CAPEX",
    "Envelope used": "Enveloppe utilisée", "Expected disbursements (after delivery haircut)": "Décaissements attendus (après décote de réalisation)",
    "Lowest remaining fund balance": "Solde restant le plus bas du fonds",
    "Over-commitment covered by expected under-delivery (indicative)": "Surengagement couvert par la sous-réalisation attendue (indicatif)",
    "PIPELINE": "PIPELINE", "Projects in pipeline": "Projets dans le pipeline", "Eligible projects": "Projets éligibles",
    "Projects funded (fully or partly)": "Projets financés (totalement ou partiellement)", "Projects fully funded": "Projets entièrement financés",
    "Eligible projects not funded": "Projets éligibles non financés", "Projects above their viability gap (funded)": "Projets financés au-dessus de leur déficit de viabilité",
    "Average weighted score of funded projects": "Score pondéré moyen des projets financés",
    "IMPACT BOUGHT (pro rata to funding share)": "IMPACT FINANCÉ (au prorata de la part financée)", "Connections funded": "Raccordements financés",
    "  household connections": "  raccordements de ménages", "  productive-use connections": "  raccordements d'usages productifs",
    "  commercial and institution connections": "  raccordements commerciaux et institutionnels",
    "People with access (households x household size)": "Personnes desservies (ménages x taille du ménage)",
    "Verified connections to date (MRV Tracker)": "Raccordements vérifiés à date (Suivi MRV)",
    "LEVERAGE & COST-EFFECTIVENESS": "EFFET DE LEVIER & COÛT-EFFICACITÉ", "Total project investment mobilised": "Investissement total des projets mobilisé",
    "Private capital mobilised (equity + debt)": "Capitaux privés mobilisés (fonds propres + dette)",
    "Leverage: private capital per $ allocated": "Effet de levier : capitaux privés par unité allouée", "Investment per $ allocated": "Investissement par unité allouée",
    "Fund allocation per connection": "Allocation du fonds par raccordement", "Fund allocation per person with access": "Allocation du fonds par personne desservie",
    "Fund allocation per tCO2 avoided": "Allocation du fonds par tCO2 évitée", "RISK & CONCENTRATION": "RISQUE & CONCENTRATION",
    "Allocation-weighted risk rating (1-5)": "Notation de risque pondérée par l'allocation (1-5)", "Expected delivery of RBF connections": "Réalisation attendue des raccordements RBF",
    "Largest single project (share of allocation)": "Plus gros projet (part de l'allocation)", "Top 3 projects (share of allocation)": "3 premiers projets (part de l'allocation)",
    "Largest country (share of envelope)": "Premier pays (part de l'enveloppe)", "PORTFOLIO VERDICT": "VERDICT SUR LE PORTEFEUILLE",
    "Envelope at least 90% committed?": "Enveloppe engagée à 90 % au moins ?", "NO - pipeline too thin": "NON - pipeline trop mince",
    "Expected disbursements within available funds?": "Décaissements attendus dans la limite des fonds disponibles ?", "NO - reduce over-commitment": "NON - réduire le surengagement",
    "Country concentration within limit?": "Concentration par pays dans la limite ?", "NO - rebalance": "NON - rééquilibrer",
    "All funded projects within their viability gap?": "Tous les projets financés dans leur déficit de viabilité ?", "NO - review additionality": "NON - revoir l'additionnalité",
    "ALLOCATION BY COUNTRY": "ALLOCATION PAR PAYS", "Share of envelope": "Part de l'enveloppe", "Other / unlisted": "Autres / non listés",
    "Largest country allocation": "Allocation du premier pays", "Disbursement profile (linked)": "Profil de décaissement (lié)", "RBF": "RBF", "Grants": "Subventions",
    "Cumulative": "Cumulé", "Allocation by project (rank order)": "Allocation par projet (ordre de rang)",
    "Expected disbursements by year": "Décaissements attendus par année", "Allocation by country": "Allocation par pays",
    # Checks
    "Scoring weights total 100%": "Les pondérations totalisent 100 %", "Allocation within envelope": "Allocation dans la limite de l'enveloppe",
    "No allocation above a project's request": "Aucune allocation supérieure à la demande d'un projet", "No allocation to ineligible projects": "Aucune allocation à un projet non éligible",
    "Each eligible project ranked exactly once": "Chaque projet éligible classé une seule fois",
    "Country allocations add up to total allocation": "La somme des allocations par pays égale l'allocation totale", "Country limit respected": "Limite par pays respectée",
    "Expected disbursements by year = grants + RBF x expected delivery (all paid within the fund life)":
        "Décaissements attendus par année = subventions + RBF x réalisation attendue (tout versé pendant la durée du fonds)",
    "Expected disbursements do not exceed allocations": "Les décaissements attendus ne dépassent pas les allocations",
    "Verification profile valid (0 <= year 1 <= cumulative year 2 <= 100%)": "Profil de vérification valide (0 <= année 1 <= cumul année 2 <= 100 %)",
    "Management + TA below 100%": "Gestion + AT inférieures à 100 %", "At least one project in pipeline": "Au moins un projet dans le pipeline",
})
for _k in range(1, 11):
    DICT[f"Developer {_k}"] = f"Développeur {_k}"

DICT["By Emmanuel Boujieka Kamga"] = "Par Emmanuel Boujieka Kamga"
