# Dictionnaire de KPI : Africa Utility Intelligence (v0.1, brouillon)

> **Statut : brouillon de travail destiné à une revue experte.** Les KPI n’ont pas encore été confrontés aux documents réellement publiés : c’est l’objet de l’étape 1 (audit de disponibilité). Le dictionnaire ne contient **aucune valeur de référence ni aucun seuil**, par choix : les benchmarks viendront des données extraites, pas d’hypothèses.

## Résumé

- **75 entrées** : 49 KPI notés, 24 indicateurs de contexte ou descriptifs (non notés) et 2 indicateurs dérivés affichés seulement.
- **Noyau MVP : 28 entrées**, soit 19 KPI notés, 4 indicateurs descriptifs (affichés, non notés) et 5 variables de contexte pour les groupes de pairs. Disponibilité attendue des KPI notés du noyau : 2 élevée, 14 moyenne, 3 faible. Ces niveaux sont une estimation d’experts, pas un constat.
- Les autres entrées forment le palier **étendu** : elles seront collectées quand elles sont disponibles, mais ne sont pas requises pour le score MVP.
- 4 doublons ont été supprimés et environ 20 noms de données brutes harmonisés. Les erreurs de formule relevées en revue ont été corrigées (voir « Méthode et corrections »).

## Méthode et corrections

Le dictionnaire a été produit en trois temps :

1. **Rédaction** : 8 agents spécialisés, un par dimension, ont rédigé chacun une section. Consigne : aucune statistique, aucun seuil, aucune URL inventés ; une référence n’est marquée « vérifiée » que si l’URL a réellement été consultée.
2. **Revue adversariale** : un agent critique a relu l’ensemble pour relever doublons, erreurs de formule, noms incohérents, disponibilités trop optimistes, KPI manquants et références douteuses.
3. **Consolidation** : les corrections du critique ont été vérifiées contre les formules brutes, puis appliquées.

**Corrections principales :**

- **Quasi-fiscal deficit** : la formule comptait les pertes deux fois. Le coût unitaire étant calculé par kWh facturé, l’écart de tarif représente déjà la totalité de l’écart coût–recette. Le titre est désormais (Coût − Recette) + défaut de recouvrement.
- **Bilan énergétique** : les importations étaient comptées deux fois (incluses dans les achats côté GEN, puis rajoutées côté NET). Les achats sont désormais scindés en `energy_purchased_domestic_gwh` + `energy_imported_gwh`, et `energy_purchased_total_gwh` n’est que leur somme dérivée.
- **Pont NET/COM** : une donnée canonique unique, `energy_billed_distribution_gwh`, garantit que « efficacité de facturation = 100 − pertes de distribution ». Seules les pertes sont notées ; l’efficacité de facturation est seulement affichée.
- **Couverture du service de la dette (DSCR)** : le numérateur est désormais le flux de trésorerie d’exploitation avant intérêts (l’EBITDA surestime la trésorerie quand les créances gonflent), et le principal des loyers est ajouté au service de la dette.
- **Dette nette / EBITDA** : la version classée exclut les loyers, pour ne pas biaiser la comparaison entre IFRS 16 et SYSCOHADA.
- **Coût O&M par km** : la conversion en USD a été corrigée (la division par km manquait).
- **Opinion d’audit** : « non publié » sort de l’échelle ordinale. La non-publication est déjà mesurée par le délai de publication.
- **Taux de recouvrement** : il est plafonné à 100 % dans l’indice de recouvrement de trésorerie classé (au-delà, il s’agit de récupération d’arriérés).
- **Références** : 4 références marquées « vérifiées » ont été rétrogradées (lecture d’un résumé seulement, ou site revendeur au lieu de l’éditeur de la norme).

Les **fiches détaillées** ci-dessous gardent les définitions techniques en anglais, telles que rédigées, avec un nom en français pour chaque KPI. La version lisible par machine est `kpi_dictionary.json`, qui contient aussi le glossaire complet des données brutes.

## Vue d’ensemble : noyau MVP

| ID | KPI | Dimension | Sens | Disponibilité attendue | Statut |
|---|---|---|---|---|---|
| `FIN_average_revenue_per_kwh_billed` | Recette moyenne par kWh facturé | FIN | contexte (non noté) | moyenne | contexte |
| `FIN_cost_recovery_ratio` | Taux de recouvrement des coûts (tarif moyen / coût du service) | FIN | plus haut = mieux | moyenne | noté |
| `FIN_current_ratio` | Ratio de liquidité générale | FIN | plus haut = mieux | moyenne | noté |
| `FIN_ebitda_margin` | Marge d'EBITDA (EBE / chiffre d'affaires) | FIN | plus haut = mieux | moyenne | noté |
| `FIN_government_transfer_dependency` | Dépendance aux transferts publics d'exploitation | FIN | plus bas = mieux | faible | noté |
| `FIN_power_purchase_payables_days` | Délai de paiement des achats d’énergie et de combustible | FIN | plus bas = mieux | moyenne | noté |
| `GEN_avg_power_purchase_cost` | Coût moyen d'achat d'énergie par kWh acheté | GEN | plus bas = mieux | moyenne | noté |
| `GEN_costly_thermal_share` | Part de l'énergie d'origine thermique coûteuse (fioul/diesel/location d'urgence) | GEN | plus bas = mieux | moyenne | noté |
| `GEN_purchased_energy_share` | Part de l'énergie achetée (IPP, importations) dans l'approvisionnement | GEN | contexte (non noté) | moyenne | contexte |
| `NET_distribution_losses_pct` | Pertes de distribution | NET | plus bas = mieux | moyenne | noté |
| `NET_saidi_hours` | Durée moyenne d'interruption par client (SAIDI) | NET | plus bas = mieux | faible | noté |
| `NET_total_system_losses_pct` | Pertes totales du système (transport + distribution) | NET | plus bas = mieux | élevée | noté |
| `COM_cash_recovery_index` | Indice de recouvrement de trésorerie (CRI) | COM | plus haut = mieux | faible | noté |
| `COM_collection_rate` | Taux de recouvrement | COM | plus haut = mieux | moyenne | noté |
| `COM_receivables_days` | Délai moyen de recouvrement des créances clients (DSO) | COM | plus bas = mieux | moyenne | noté |
| `OPS_customers_per_employee` | Clients par employé | OPS | plus haut = mieux | moyenne | noté |
| `GOV_annual_reporting_disclosure_score` | Score de divulgation du rapport annuel | GOV | plus haut = mieux | élevée | noté |
| `GOV_audit_opinion_code` | Type d'opinion d'audit (code ordinal) | GOV | plus haut = mieux | moyenne | noté |
| `GOV_audited_fs_publication_lag_months` | Délai de publication des états financiers audités | GOV | plus bas = mieux | moyenne | noté |
| `GOV_regulatory_framework_score` | Score du cadre de régulation et de tarification | GOV | plus haut = mieux | moyenne | noté |
| `INV_capex_to_depreciation` | Ratio de renouvellement des actifs (Capex / dotations aux amortissements) | INV | contexte (non noté) | moyenne | contexte |
| `ACC_consumption_per_customer` | Consommation moyenne par client | ACC | contexte (non noté) | élevée | contexte |
| `ACC_new_connections` | Nouveaux raccordements réalisés dans l'année | ACC | plus haut = mieux | moyenne | noté |
| `CTX_customer_base_size` | Taille du portefeuille clients | CTX | contexte (non noté) | élevée | contexte |
| `CTX_gdp_per_capita_usd` | PIB par habitant (USD courants) | CTX | contexte (non noté) | élevée | contexte |
| `CTX_market_structure` | Structure de marché et périmètre d'activité de l'entité | CTX | contexte (non noté) | élevée | contexte |
| `CTX_national_access_rate` | Taux d'accès national à l'électricité | CTX | contexte (non noté) | élevée | contexte |
| `CTX_ownership_type` | Type d'actionnariat et de contrôle | CTX | contexte (non noté) | élevée | contexte |

## Vue d’ensemble : palier étendu

| ID | KPI | Dimension | Disponibilité attendue | Statut |
|---|---|---|---|---|
| `FIN_controllable_opex_per_kwh_billed` | Charges contrôlables par kWh facturé | FIN | moyenne | noté |
| `FIN_debt_service_coverage_ratio` | Ratio de couverture du service de la dette | FIN | moyenne | noté |
| `FIN_equity_to_assets` | Fonds propres / actif total | FIN | moyenne | noté |
| `FIN_fx_debt_share` | Part de la dette en devises | FIN | moyenne | noté |
| `FIN_interest_coverage_ratio` | Couverture des intérêts | FIN | moyenne | noté |
| `FIN_net_debt_to_ebitda` | Dette nette / EBITDA | FIN | moyenne | noté |
| `FIN_quasi_fiscal_deficit_pct_gdp` | Déficit quasi-budgétaire du secteur électrique (% du PIB) | FIN | faible | noté |
| `FIN_unit_cost_of_service_per_kwh_billed` | Coût unitaire du service par kWh facturé | FIN | moyenne | noté |
| `GEN_available_capacity_ratio` | Taux de disponibilité de la capacité installée (puissance disponible / puissance installée) | GEN | faible | noté |
| `GEN_equivalent_availability_factor` | Facteur de disponibilité équivalente (EAF) du parc propre | GEN | faible | noté |
| `GEN_fuel_cost_per_kwh_thermal` | Coût du combustible par kWh produit (parc thermique propre) | GEN | faible | noté |
| `GEN_net_capacity_factor` | Facteur de charge net (facteur d'utilisation) du parc propre | GEN | moyenne | contexte |
| `GEN_reserve_margin` | Marge de réserve de capacité par rapport à la pointe | GEN | faible | noté |
| `NET_customers_per_network_km` | Densité de clients par km de réseau de distribution | NET | moyenne | contexte |
| `NET_energy_not_supplied_pct` | Énergie non distribuée (END) en % de la demande servie | NET | faible | noté |
| `NET_hours_of_supply_per_day` | Heures de fourniture par jour | NET | faible | noté |
| `NET_non_technical_losses_pct` | Pertes non techniques (commerciales) | NET | faible | noté |
| `NET_om_cost_per_network_km` | Coût d'exploitation et de maintenance du réseau par km de ligne | NET | faible | contexte |
| `NET_saifi_count` | Fréquence moyenne d'interruption par client (SAIFI) | NET | moyenne | noté |
| `NET_transmission_losses_pct` | Pertes de transport | NET | moyenne | noté |
| `COM_bad_debt_expense_pct_revenue` | Dotations pour créances douteuses / chiffre d’affaires | COM | moyenne | noté |
| `COM_billing_efficiency` | Taux de facturation (efficacité de facturation) | COM | moyenne | dérivé, affiché seulement |
| `COM_metering_coverage` | Taux de comptage des clients | COM | moyenne | noté |
| `COM_prepaid_share` | Part des clients prépayés | COM | moyenne | contexte |
| `COM_public_sector_receivables_share` | Part des créances publiques | COM | moyenne | noté |
| `COM_receivables_days_public_sector` | Délai de recouvrement des créances sur le secteur public (administrations, entreprises publiques, collectivités) | COM | faible | noté |
| `COM_revenue_per_customer` | Revenu moyen par client | COM | élevée | contexte |
| `GOV_board_independence_ratio` | Taux d'administrateurs indépendants | GOV | faible | noté |
| `GOV_performance_contract_score` | Score du contrat de performance avec l'État | GOV | faible | noté |
| `GOV_procurement_transparency_score` | Score de transparence des achats et contrats | GOV | moyenne | noté |
| `GOV_regulatory_reporting_compliance_code` | Conformité aux obligations de reporting réglementaire | GOV | moyenne | noté |
| `INV_asset_base_growth` | Croissance de la base d'actifs (immobilisations corporelles nettes) | INV | élevée | contexte |
| `INV_capex_execution_rate` | Taux d'execution du budget d'investissement | INV | faible | noté |
| `INV_capex_per_new_connection` | Capex de distribution par nouveau raccordement | INV | faible | contexte |
| `INV_capex_to_revenue` | Intensite d'investissement (Capex / chiffre d'affaires) | INV | moyenne | contexte |
| `INV_commissioning_delay` | Retard de mise en service des projets majeurs | INV | faible | noté |
| `INV_cwip_to_gross_ppe` | Part des immobilisations en cours | INV | moyenne | noté |
| `INV_external_financing_share` | Part du financement concessionnel / bailleurs dans l'investissement | INV | faible | contexte |
| `ACC_complaints_per_1000_customers` | Taux de réclamations pour 1 000 clients | ACC | faible | noté |
| `ACC_connection_time_days` | Délai moyen de raccordement | ACC | faible | noté |
| `ACC_customer_growth_rate` | Taux de croissance annuel du nombre de clients | ACC | élevée | contexte |
| `ACC_lifeline_tariff_coverage` | Couverture du tarif social (tranche sociale) | ACC | faible | contexte |
| `ACC_residential_share` | Part des clients résidentiels | ACC | moyenne | contexte |
| `CTX_average_tariff_usd` | Tarif moyen effectif (USD/kWh) | CTX | moyenne | dérivé, affiché seulement |
| `CTX_currency_accounting_regime` | Régime de change et référentiel comptable | CTX | élevée | contexte |
| `CTX_fcv_status` | Statut de fragilité, conflit et violence (FCV) | CTX | élevée | contexte |
| `CTX_supply_mix` | Mix d'approvisionnement (production propre, achats, importations) | CTX | moyenne | contexte |

## Règles transversales

- **Unités** : énergie en GWh ; montants en millions de monnaie locale (`_lcu_m`) de l’exercice ; LCU m / GWh = LCU/kWh. Conversion en USD au cours moyen annuel (`fx_lcu_per_usd_avg`), en montrant aussi la série en LCU (les dévaluations de 2019-2025 au Nigeria, au Ghana et en Zambie dominent sinon les tendances).
- **Valeurs absentes** : *Non publié* (la source ne donne pas l’information), *Non disponible* (aucune source trouvée), *Non trouvé*. Une valeur absente n’est jamais déduite.
- **Variantes** : chaque KPI garde la valeur publiée par l’utility (`reported_*`) à côté de la valeur recalculée, avec son dénominateur déclaré.
- **Comparabilité** : on ne classe jamais ensemble des utilities de périmètres différents (intégrée, distribution, production ou transport seuls).
- **Transferts** : les transferts d’investissement ne comptent que dans INV, les transferts d’exploitation que dans FIN.
- **Comptabilité** : SYSCOHADA et IFRS demandent une table de correspondance explicite des postes (EBE, subventions d’exploitation, trésorerie-passif, IFRS 16).

## FIN : Soutenabilité financière

*Financial sustainability is the binding constraint for most Sub-Saharan African power utilities. Tariffs below cost, high losses, poor collection (especially public-sector arrears), IPP take-or-pay obligations, emergency or diesel generation, and FX-denominated debt together produce operating deficits that governments cover through explicit subsidies, tariff compensation, debt assumption or tolerated arrears. These transfers form a quasi-fiscal deficit. This dimension measures whether a utility earns enough from tariffs to cover its cost of service, generates operating cash (EBITDA), can meet short-term obligations and debt service, and how much it depends on government transfers. Most inputs come from audited financial statements: IFRS for anglophone utilities, SYSCOHADA for most francophone ones, where 'Excédent brut d'exploitation (EBE)' is the nearest equivalent to EBITDA. These statements are the most consistently published documents for African utilities, which suits a source-first platform. Receivables days and collection efficiency belong to the COM dimension and are not duplicated here. Two conventions apply to every KPI. First, a value in LCU millions divided by GWh gives LCU per kWh directly (10^6 LCU / 10^6 kWh). Second, all money items are in nominal local currency for the reporting fiscal year, so ratios can be compared across countries but absolute amounts need FX/PPP conversion before comparison.*

### `FIN_average_revenue_per_kwh_billed` : Recette moyenne par kWh facturé
*Average revenue (effective tariff) per kWh billed* · palier **noyau MVP** · contexte · contexte (non noté) · unité : LCU/kWh (convert to USD/kWh at the annual average FX rate for cross-country views)

- **Définition** : Electricity sales revenue, excluding subsidies, tariff compensation, connection fees and other non-energy revenue, divided by energy billed to final customers (and to bulk/export customers if their revenue is included; the scope must match). Measures the effective average tariff actually applied, including the effect of customer mix, lifeline tariffs and fixed charges.
- **Formule** : `revenue_electricity_sales_lcu_m / energy_billed_gwh   (result in LCU per kWh)`
- **Données brutes** : `revenue_electricity_sales_lcu_m`, `energy_billed_gwh`, `fx_lcu_per_usd_avg`
- **Sources typiques** : audited financial statements; utility annual report (sales statistics section); regulator annual report / tariff decisions; ministry energy statistics
- **Disponibilité attendue** : moyenne. Revenue is always reported, and billed GWh is usually given in the annual report's operational statistics or in regulator reports, though sometimes only as GWh 'sold' with unclear treatment of exports and own use. [Review downgrade from high: The revenue and GWh scopes must match: exports, bulk sales, levies and compensation all have to be excluded. This is often impossible from summary reports. Suggested: medium.]
- **Pièges de comparaison** : Not a performance indicator in itself, since a higher tariff is not 'better'. Interpret it only against FIN_unit_cost_of_service_per_kwh_billed. Pitfalls: (1) exports and bulk sales to other utilities (low tariffs) dilute the average, so the revenue and GWh scope must match; (2) prepaid vending revenue may be recorded net of vendor commissions; (3) VAT and levies (e.g. rural electrification or TV levies collected on bills) must be excluded; (4) estimated billing for unmetered postpaid customers inflates billed GWh; (5) FX conversion during devaluations (Nigeria, Ghana, Zambia in 2019-2025) can dominate USD trends, so also show values in LCU and in real terms.

### `FIN_cost_recovery_ratio` : Taux de recouvrement des coûts (tarif moyen / coût du service)
*Cost recovery ratio (average tariff vs cost of service)* · palier **noyau MVP** · noté · plus haut = mieux · unité : ratio (dimensionless)

- **Définition** : Billed electricity sales revenue (excluding subsidies and tariff compensation) divided by the full accounting cost of service: cash operating costs (including fuel and power purchases), depreciation and finance costs. A value of 1 means billed tariffs would cover the full cost of service if every bill were collected. Equivalent to the average effective tariff per kWh billed divided by the unit cost of service per kWh billed. Billed basis only: collection shortfalls are captured by COM KPIs and by FIN_quasi_fiscal_deficit_pct_gdp.
- **Formule** : `(revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m) / (operating_expenses_excl_depreciation_lcu_m - bad_debt_expense_lcu_m + depreciation_amortisation_lcu_m + finance_costs_lcu_m)`
- **Données brutes** : `revenue_electricity_sales_lcu_m`, `other_operating_revenue_lcu_m`, `operating_expenses_excl_depreciation_lcu_m`, `bad_debt_expense_lcu_m`, `depreciation_amortisation_lcu_m`, `finance_costs_lcu_m`
- **Sources typiques** : audited financial statements (income statement and notes); utility annual report; regulator tariff review / cost-of-service study; World Bank / donor project appraisal documents
- **Disponibilité attendue** : moyenne. All four inputs appear on the face of, or in the notes to, a standard IFRS or SYSCOHADA income statement, and most MVP utilities publish audited accounts at least for some years. The main difficulty is separating tariff revenue from subsidies and compensation, which often requires the notes. [Review downgrade from high: 'High' assumes audited statements are published, but the GOV section itself says several state-owned utilities (especially in Central Africa) do not publish them. Removing tariff compensation from 'chiffre d'affaires' and splitting out bad-debt expense both need full notes, which public summaries often lack. Suggested: medium.]
- **Référence** (existence vérifiée, contenu non vérifié) : Conceptually aligned with the cost-recovery analysis in World Bank Policy Research Working Paper 7788 (Trimble, Kojima, Perez Arroyo, Mohammadzadeh, 2016), which uses a cash-cost and capital-cost basis per kWh; this platform uses an accounting (depreciation + finance cost) basis instead of replacement-cost capital charges. <https://econpapers.repec.org/paper/wbkwbrwps/7788.htm>
- **Pièges de comparaison** : (1) Depreciation depends on asset revaluation policy. Revalued assets (common under IFRS, e.g. Eskom, KPLC) inflate cost compared with historical-cost SYSCOHADA books, and assets financed by grants or owned by a state asset-holding company (e.g. patrimoine/société de patrimoine models) may sit off the operator's books. (2) Vertically integrated utilities include generation cost; distribution companies include bulk purchase cost from a single buyer, so the denominator scope differs. Always tag utility structure. (3) Fuel supplied in kind by the state or IPP costs paid directly by the Treasury make cost look artificially low. (4) Tariff compensation booked inside 'chiffre d'affaires' must be removed. (5) FX losses on debt may sit in finance costs and cause year-to-year swings, so report them separately where possible. (6) Bad-debt provisions inside opex differ widely between utilities.
- **Revue** : Review fix: other operating revenue added to the numerator (its costs sit in opex); bad-debt expense removed from the denominator so the KPI stays on a billed basis.
- **Revue** : Reference: only the RePEc abstract of World Bank WPS 7788 was read (OKR page returned 403); the paper exists, but method-level claims are not verified.

### `FIN_current_ratio` : Ratio de liquidité générale
*Current ratio (liquidity)* · palier **noyau MVP** · noté · plus haut = mieux · unité : ratio (dimensionless)

- **Définition** : Current assets divided by current liabilities at fiscal year-end. Gives a balance-sheet view of short-term liquidity. In African utilities it often reflects large unpaid power-purchase and fuel payables, together with receivables of doubtful quality (government and public entities), so read it together with the quick-ratio variant that excludes receivables from public entities when disclosed.
- **Formule** : `current_assets_lcu_m / current_liabilities_lcu_m ; optional stricter variant: (current_assets_lcu_m - receivables_public_sector_gross_lcu_m) / current_liabilities_lcu_m`
- **Données brutes** : `current_assets_lcu_m`, `current_liabilities_lcu_m`, `receivables_public_sector_gross_lcu_m`, `cash_and_equivalents_lcu_m`
- **Sources typiques** : audited financial statements (balance sheet / bilan); utility annual report
- **Disponibilité attendue** : moyenne. Reported in every balance sheet. SYSCOHADA presents 'actif circulant' and 'passif circulant' plus treasury lines ('trésorerie-actif/passif'), which need consistent mapping. Public-sector receivables are disclosed only sometimes. [Review downgrade from high: Computable only where a full balance sheet is public. SYSCOHADA treasury remapping is required. Suggested: medium.]
- **Référence** (aucune) : none (standard financial-analysis ratio)
- **Pièges de comparaison** : (1) A higher ratio can hide uncollectable government receivables that are not impaired, so a 'good' current ratio may be illusory. (2) Classification differs: SYSCOHADA separates 'trésorerie' from 'actif/passif circulant', so bank overdrafts must be added to current liabilities for consistency with IFRS. (3) Debt in covenant breach is reclassified as current under IFRS, which causes sudden drops. (4) Year-end timing of government settlements or securitisation can move the ratio sharply. Do not set fixed thresholds across structures (single buyers and distribution companies differ).

### `FIN_ebitda_margin` : Marge d'EBITDA (EBE / chiffre d'affaires)
*EBITDA margin* · palier **noyau MVP** · noté · plus haut = mieux · unité : % of operating revenue

- **Définition** : Earnings before interest, taxes, depreciation and amortisation, as a percentage of total operating revenue. Operating revenue includes tariff compensation and operating subsidies only when the utility books them as revenue. Store EBITDA both including and excluding government operating transfers, so that operating performance can be separated from subsidy support. The primary KPI uses EBITDA excluding transfers. In SYSCOHADA accounts, the closest published line is the 'Excédent brut d'exploitation (EBE)', which must be adjusted where it includes operating subsidies.
- **Formule** : `EBITDA_excl_transfers_lcu_m = revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m - operating_expenses_excl_depreciation_lcu_m ; FIN_ebitda_margin = 100 * EBITDA_excl_transfers_lcu_m / (revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m). Companion variant (stored, not ranked): 100 * (EBITDA_excl_transfers_lcu_m + tariff_compensation_revenue_lcu_m + operating_subsidies_received_lcu_m) / (revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m + tariff_compensation_revenue_lcu_m + operating_subsidies_received_lcu_m)`
- **Données brutes** : `revenue_electricity_sales_lcu_m`, `other_operating_revenue_lcu_m`, `tariff_compensation_revenue_lcu_m`, `operating_subsidies_received_lcu_m`, `operating_expenses_excl_depreciation_lcu_m`
- **Sources typiques** : audited financial statements (income statement, SYSCOHADA 'soldes intermédiaires de gestion'); utility annual report; bond / Eurobond prospectuses and rating agency reports where public
- **Disponibilité attendue** : moyenne. Calculable from any income statement. SYSCOHADA statements publish EBE directly. Isolating transfers needs note disclosure, which is usually available but sometimes vague. [Review downgrade from high: The ranked value requires EBITDA excluding transfers. Isolating 'subventions d'exploitation' or compensation booked as revenue needs notes, which public SYSCOHADA summaries often omit. Suggested: medium.]
- **Référence** (aucune) : none (EBITDA is a non-GAAP measure under IFRS; EBE is a SYSCOHADA intermediate balance; this platform defines its own computation)
- **Pièges de comparaison** : (1) EBITDA is not defined by IFRS, so utilities' self-reported EBITDA differs in its treatment of impairments, bad-debt provisions, FX gains/losses and fair-value movements. Always recompute from line items rather than using the reported figure. (2) Impairment of receivables (often very large for public-sector arrears) may sit in opex or below EBITDA, so flag which. (3) IFRS 16 (leases) moves rental-power or lease costs out of opex and into depreciation and interest, which raises IFRS EBITDA compared with SYSCOHADA accounts that do not apply IFRS 16. (4) Single-buyer entities have thin, regulated margins, which is structural rather than poor performance. (5) Negative or near-zero denominators are rare, but revenue can be restated after tariff disputes.

### `FIN_government_transfer_dependency` : Dépendance aux transferts publics d'exploitation
*Operating dependency on government transfers* · palier **noyau MVP** · noté · plus bas = mieux · unité : % of total operating resources

- **Définition** : Government operating transfers received or recognised in the year (explicit operating subsidies, tariff compensation for regulated below-cost tariffs, fuel or power purchase cost subsidies paid to or on behalf of the utility) as a share of total operating resources (sales revenue + other operating revenue + those transfers). Capital grants, debt assumption and arrears write-offs are recorded separately as context items, not in the core ratio.
- **Formule** : `100 * (tariff_compensation_revenue_lcu_m + operating_subsidies_received_lcu_m + govt_paid_fuel_or_ipp_costs_on_behalf_lcu_m) / (revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m + tariff_compensation_revenue_lcu_m + operating_subsidies_received_lcu_m + govt_paid_fuel_or_ipp_costs_on_behalf_lcu_m) ; context items stored: capital_grants_received_lcu_m, govt_debt_assumed_or_converted_lcu_m`
- **Données brutes** : `tariff_compensation_revenue_lcu_m`, `operating_subsidies_received_lcu_m`, `govt_paid_fuel_or_ipp_costs_on_behalf_lcu_m`, `revenue_electricity_sales_lcu_m`, `other_operating_revenue_lcu_m`, `capital_grants_received_lcu_m`, `govt_debt_assumed_or_converted_lcu_m`
- **Sources typiques** : audited financial statements (notes on subsidies, 'subventions d'exploitation', related-party transactions with the State); national budget laws / budget execution reports (subsidy lines for the power sector); IMF Article IV and programme reviews; regulator tariff decisions (tariff compensation mechanisms); World Bank / AfDB project appraisal documents
- **Disponibilité attendue** : faible. Explicit subsidies and tariff compensation are usually disclosed in the notes or in budget documents (e.g. compensation mechanisms in Senegal and Côte d'Ivoire, Nigeria's tariff shortfall funding). Transfers paid on the utility's behalf (fuel, IPP invoices paid by the Treasury) are often visible only in budget or IMF documents and are hard to attribute by year. [Review downgrade from medium: The govt_paid_fuel_or_ipp_costs_on_behalf component is rarely attributable by year, and without it the KPI is systematically understated. Suggested: low.]
- **Pièges de comparaison** : (1) Implicit support is far larger than explicit transfers in many countries: tolerated arrears, unpaid taxes and dividends, cheap fuel from a national oil company, debt servicing by the Treasury. A low value therefore does not prove financial independence. Pair it with FIN_quasi_fiscal_deficit_pct_gdp. (2) In single-buyer models, the subsidy may go to the single buyer or asset holder rather than to the distribution company being benchmarked. (3) Accrual (amount recognised) and cash (amount actually paid by the Treasury) diverge widely, so record which basis the source uses. (4) Some utilities net compensation against tax or dividend liabilities, which makes it invisible in revenue.

### `FIN_power_purchase_payables_days` : Délai de paiement des achats d’énergie et de combustible
*Power purchase & fuel payables days* · palier **noyau MVP** · noté · plus bas = mieux · unité : days

- **Définition** : Days of power-purchase and fuel cost outstanding in trade payables to IPPs, fuel and gas suppliers at year end. Overdue portion stored where disclosed. Main liquidity transmission channel and contingent fiscal liability.
- **Formule** : `(payables_power_purchase_and_fuel_lcu_m / (power_purchase_cost_lcu_m + fuel_cost_own_generation_lcu_m)) * days_in_period; companion: overdue_power_purchase_payables_lcu_m`
- **Données brutes** : `payables_power_purchase_and_fuel_lcu_m`, `overdue_power_purchase_payables_lcu_m`, `power_purchase_cost_lcu_m`, `fuel_cost_own_generation_lcu_m`, `days_in_period`
- **Sources typiques** : audited financial statements (payables note); IPP / single-buyer disclosures; IMF / World Bank country reports on sector arrears
- **Disponibilité attendue** : moyenne. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

### `FIN_controllable_opex_per_kwh_billed` : Charges contrôlables par kWh facturé
*Controllable opex per kWh billed* · palier **étendu** · noté · plus bas = mieux · unité : LCU/kWh

- **Définition** : Operating expenses excluding fuel, power purchases and bad-debt expense, per kWh billed: isolates costs management controls.
- **Formule** : `(operating_expenses_excl_depreciation_lcu_m - fuel_cost_own_generation_lcu_m - power_purchase_cost_lcu_m - bad_debt_expense_lcu_m) / energy_billed_gwh`
- **Données brutes** : `operating_expenses_excl_depreciation_lcu_m`, `fuel_cost_own_generation_lcu_m`, `power_purchase_cost_lcu_m`, `bad_debt_expense_lcu_m`, `energy_billed_gwh`
- **Sources typiques** : audited financial statements (expense notes)
- **Disponibilité attendue** : moyenne. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

### `FIN_debt_service_coverage_ratio` : Ratio de couverture du service de la dette
*Debt service coverage ratio (DSCR)* · palier **étendu** · noté · plus haut = mieux · unité : ratio (times)

- **Définition** : Cash available for debt service (EBITDA excluding government transfers; a variant includes transfers) divided by debt service actually paid in the year (interest paid plus scheduled principal repaid on borrowings and on-lent loans). Measures the ability to service debt from operations.
- **Formule** : `(cash_flow_from_operations_lcu_m + interest_paid_lcu_m) / (interest_paid_lcu_m + debt_principal_repaid_lcu_m + lease_principal_paid_lcu_m). Secondary (stored, not ranked): EBITDA_excl_transfers_lcu_m / same denominator.`
- **Données brutes** : `cash_flow_from_operations_lcu_m`, `interest_paid_lcu_m`, `debt_principal_repaid_lcu_m`, `lease_principal_paid_lcu_m`, `revenue_electricity_sales_lcu_m`, `other_operating_revenue_lcu_m`, `operating_expenses_excl_depreciation_lcu_m`
- **Sources typiques** : audited financial statements (cash flow statement, borrowings note); donor / DFI loan documents and project appraisal documents (covenant tests); Eurobond or bond prospectuses; rating agency reports where public
- **Disponibilité attendue** : moyenne. Interest and principal repaid appear in IFRS cash flow statements. Many SYSCOHADA utilities publish a 'tableau des flux de trésorerie' too, but publicly available versions are often summaries without the notes. Debt serviced directly by the Treasury on on-lent loans is often not visible.
- **Référence** (aucune) : none (lender-covenant convention; definitions vary by loan agreement)
- **Pièges de comparaison** : (1) Governments often service utility debt directly or convert it to equity or arrears, so low reported debt service can mean hidden support, not strength. (2) Grace periods on concessional loans inflate DSCR in early years. (3) Covenant definitions in DFI loans differ from this formula, so do not compare with covenant values reported by the utility. (4) FX-denominated debt service balloons after devaluations. (5) Unpaid IPP and fuel arrears are a form of debt not captured here.
- **Revue** : Review fix: accrual EBITDA overstates cash available when receivables balloon, so the ranked numerator is now operating cash flow before interest; lease principal is added to debt service.

### `FIN_equity_to_assets` : Fonds propres / actif total
*Equity to total assets* · palier **étendu** · noté · plus haut = mieux · unité : %

- **Définition** : Total equity divided by total assets at year end, with a negative-equity (technical insolvency) flag. Meaningful even when EBITDA is negative.
- **Formule** : `total_equity_lcu_m / total_assets_lcu_m * 100; negative_equity_flag = total_equity_lcu_m < 0`
- **Données brutes** : `total_equity_lcu_m`, `total_assets_lcu_m`
- **Sources typiques** : audited financial statements (balance sheet)
- **Disponibilité attendue** : moyenne. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

### `FIN_fx_debt_share` : Part de la dette en devises
*Foreign-currency debt share* · palier **étendu** · noté · plus bas = mieux · unité : %

- **Définition** : Share of interest-bearing borrowings denominated in foreign currency at year end (devaluation exposure).
- **Formule** : `borrowings_foreign_currency_lcu_m / total_borrowings_lcu_m * 100`
- **Données brutes** : `borrowings_foreign_currency_lcu_m`, `total_borrowings_lcu_m`
- **Sources typiques** : audited financial statements (borrowings / financial risk note)
- **Disponibilité attendue** : moyenne. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

### `FIN_interest_coverage_ratio` : Couverture des intérêts
*Interest coverage ratio* · palier **étendu** · noté · plus haut = mieux · unité : times

- **Définition** : EBITDA excluding transfers divided by interest expense. Simpler and more widely available than DSCR.
- **Formule** : `EBITDA_excl_transfers_lcu_m / interest_expense_lcu_m`
- **Données brutes** : `revenue_electricity_sales_lcu_m`, `other_operating_revenue_lcu_m`, `operating_expenses_excl_depreciation_lcu_m`, `interest_expense_lcu_m`
- **Sources typiques** : audited financial statements
- **Disponibilité attendue** : moyenne. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

### `FIN_net_debt_to_ebitda` : Dette nette / EBITDA
*Net debt to EBITDA (leverage)* · palier **étendu** · noté · plus bas = mieux · unité : ratio (times EBITDA); companion as ratio

- **Définition** : Interest-bearing borrowings (including on-lent government loans and lease liabilities) less cash and equivalents, divided by EBITDA excluding government transfers. Reported as 'not meaningful' when EBITDA is zero or negative; in that case only the companion indicator, net debt to total assets, is shown.
- **Formule** : `Ranked (cross-framework): (total_borrowings_lcu_m - cash_and_equivalents_lcu_m) / EBITDA_excl_transfers_excl_ifrs16_lcu_m (undefined if EBITDA <= 0). IFRS-only variant: (total_borrowings_lcu_m + lease_liabilities_lcu_m - cash_and_equivalents_lcu_m) / EBITDA_excl_transfers_lcu_m. Companion: net debt / total_assets_lcu_m.`
- **Données brutes** : `total_borrowings_lcu_m`, `lease_liabilities_lcu_m`, `cash_and_equivalents_lcu_m`, `total_assets_lcu_m`, `revenue_electricity_sales_lcu_m`, `other_operating_revenue_lcu_m`, `operating_expenses_excl_depreciation_lcu_m`
- **Sources typiques** : audited financial statements (balance sheet, borrowings note); bond prospectuses / rating reports; IMF Article IV / debt sustainability analyses mentioning SOE debt
- **Disponibilité attendue** : moyenne. Borrowings and cash are on every balance sheet. Lease liabilities appear only under IFRS 16. For several MVP utilities, EBITDA excluding transfers is negative in some years, so the ratio is often not meaningful and the companion debt-to-assets ratio is needed.
- **Pièges de comparaison** : (1) Overdue payables to IPPs, fuel suppliers and gas suppliers are economically debt but excluded; store them separately (overdue_power_purchase_payables_lcu_m) where disclosed. (2) Debt assumed or cancelled by the state (common restructurings in 2019-2025) creates breaks in the series. (3) Asset revaluations change the companion ratio. (4) Sign instability around zero EBITDA makes trend charts misleading, so the platform must suppress values when EBITDA is near zero or negative.
- **Revue** : Review fix: SYSCOHADA (no IFRS 16) keeps lease costs in opex, so leases are excluded from the cross-framework ranked version.

### `FIN_quasi_fiscal_deficit_pct_gdp` : Déficit quasi-budgétaire du secteur électrique (% du PIB)
*Power sector quasi-fiscal deficit (% of GDP)* · palier **étendu** · noté · plus bas = mieux · unité : % of nominal GDP (component values in LCU millions also stored)

- **Définition** : The hidden cost of utility inefficiency and underpricing, expressed as a share of national GDP. It is the gap between what an efficiently operated utility would collect at cost-recovery prices and what the utility actually collects. It has three components. (a) Underpricing: unit cost of service minus average tariff, times energy billed. (b) Excess network losses: losses above a methodology-defined normative loss rate, valued at unit cost. (c) Collection shortfall: billed revenue not collected. It is calculated at utility level and aggregated to country level when all sector entities are covered. Methodology parameters (normative loss rate, cost basis) are set by the platform's methodology note and published with each value; this dictionary does not set numeric values for them.
- **Formule** : `QFD_lcu_m = (C - R) + collection_shortfall_lcu_m, where C = operating_expenses_excl_depreciation_lcu_m - bad_debt_expense_lcu_m + depreciation_amortisation_lcu_m + finance_costs_lcu_m, R = revenue_electricity_sales_lcu_m, collection_shortfall_lcu_m = revenue_billed_lcu_m - cash_collected_lcu_m (stored signed, not floored). FIN_quasi_fiscal_deficit_pct_gdp = 100 * QFD_lcu_m / nominal_gdp_lcu_m. Decomposition into underpricing vs excess losses (losses valued at cost per kWh SUPPLIED, against a documented normative loss rate) is a stored analytical view, not part of the headline.`
- **Données brutes** : `operating_expenses_excl_depreciation_lcu_m`, `depreciation_amortisation_lcu_m`, `finance_costs_lcu_m`, `revenue_electricity_sales_lcu_m`, `revenue_billed_lcu_m`, `cash_collected_lcu_m`, `energy_billed_gwh`, `energy_sent_out_gwh`, `energy_injected_distribution_gwh`, `normative_loss_rate_param`, `nominal_gdp_lcu_m`, `bad_debt_expense_lcu_m`
- **Sources typiques** : audited financial statements; utility annual report (energy balance, collection statistics); regulator annual reports; IMF World Economic Outlook / national statistics office (nominal GDP); World Bank studies and project documents on sector hidden costs
- **Disponibilité attendue** : faible. Requires a complete and consistent energy balance, cash collections and full cost data for the same year, plus a methodology parameter. Cash collections and sent-out energy are often missing or inconsistent. Country-level aggregation needs every sector entity (generation company, transmission company, distribution companies, single buyer), which is rarely possible in unbundled systems such as Nigeria or Ghana within the MVP.
- **Référence** (existence vérifiée, contenu non vérifié) : World Bank Policy Research Working Paper 7788, 'Financial Viability of Electricity Sectors in Sub-Saharan Africa: Quasi-Fiscal Deficits and Hidden Costs' (Trimble, Kojima, Perez Arroyo, Mohammadzadeh, 2016). This platform's accounting-cost variant is simplified and is not identical to that paper's method (which also uses benchmark cost scenarios); see open questions. <https://econpapers.repec.org/paper/wbkwbrwps/7788.htm>
- **Pièges de comparaison** : (1) Results are highly sensitive to the normative loss rate and the cost basis (accounting vs replacement cost), so never compare with values published by the World Bank or IMF unless the method matches. (2) For a single utility in an unbundled sector, upstream subsidies are excluded, which understates the sector QFD. (3) Collection shortfall overlaps with COM collection-efficiency KPIs; it is used here only as a component and is not ranked separately. (4) Prepaid customers have near-full collection by construction, so prepaid penetration drives part of the cross-utility difference. (5) GDP rebasing (e.g. Nigeria, Ghana) changes the denominator. (6) Avoid double counting where tariff compensation already closes part of the underpricing gap: report QFD before transfers and show transfers separately.
- **Revue** : Review fix: the draft double counted losses (underpricing per kWh billed already equals the whole C - R gap). Headline is now (C - R) + collection shortfall. The normative loss rate is a methodology decision still open; no value is set.
- **Revue** : Reference: only the RePEc abstract of World Bank WPS 7788 was read (OKR page returned 403); the paper exists, but method-level claims are not verified.

### `FIN_unit_cost_of_service_per_kwh_billed` : Coût unitaire du service par kWh facturé
*Unit cost of service per kWh billed* · palier **étendu** · noté · plus bas = mieux · unité : LCU/kWh (USD/kWh at the annual average FX rate for cross-country views)

- **Définition** : Full accounting cost of service (cash operating costs including fuel and power purchases, plus depreciation and finance costs) divided by energy billed. Expressed per kWh billed, not per kWh sent out, so that technical and commercial losses raise the unit cost borne by paying customers.
- **Formule** : `(operating_expenses_excl_depreciation_lcu_m - bad_debt_expense_lcu_m + depreciation_amortisation_lcu_m + finance_costs_lcu_m) / energy_billed_gwh   (LCU per kWh)`
- **Données brutes** : `operating_expenses_excl_depreciation_lcu_m`, `fuel_cost_own_generation_lcu_m`, `power_purchase_cost_lcu_m`, `depreciation_amortisation_lcu_m`, `finance_costs_lcu_m`, `energy_billed_gwh`, `fx_lcu_per_usd_avg`, `bad_debt_expense_lcu_m`
- **Sources typiques** : audited financial statements and notes (cost breakdown); regulator cost-of-service / tariff studies; utility annual report
- **Disponibilité attendue** : moyenne. Same inputs as the cost recovery ratio. The fuel and power purchase sub-lines (stored for diagnosis) are often but not always disclosed in the notes. [Review downgrade from high: It inherits the cost-recovery issues, and the stored fuel and power-purchase sub-lines are often aggregated. Suggested: medium.]
- **Pièges de comparaison** : Strongly driven by structure and generation mix rather than by management: hydro-dominated systems (DRC, Zambia, Congo) differ from thermal or emergency-diesel systems (Senegal before gas, Ghana with IPP take-or-pay capacity charges, rental power). Capacity payments for unused IPP capacity raise unit cost without raising GWh. Distribution companies buying from a single buyer reflect the bulk tariff, not the true generation cost. Also store the fuel and power purchase share to support diagnosis. Inherits the depreciation and revaluation pitfalls of FIN_cost_recovery_ratio.

**Questions ouvertes (FIN)**

- Cost basis for cost recovery and QFD: accounting cost (depreciation + finance costs, as used here) or a normative capital charge (replacement cost x WACC), as in some World Bank work? The accounting basis is source-traceable but distorted by revaluations and grant-funded assets.
- How should normative_loss_rate_param be set and governed (single regional value vs country- or structure-specific), given the rule against inventing thresholds? Needs a documented methodology decision, possibly taken from the referenced World Bank paper after full-text review (the paper's landing page on openknowledge.worldbank.org returned 403; only the abstract on RePEc was verified).
- Treatment of SYSCOHADA vs IFRS statements: should the platform maintain an explicit line-item mapping table (e.g. EBE, 'subventions d'exploitation', 'trésorerie-passif') and, for IFRS 16 adopters, back out lease effects so EBITDA is comparable with non-IFRS 16 SYSCOHADA utilities?
- Unbundled and single-buyer systems (Nigeria GenCos/DisCos/NBET, Ghana ECG/VRA/GRIDCo, Kenya KPLC/KenGen, Côte d'Ivoire CIE/CI-Energies concession): benchmark at entity level only, or also build a 'sector consolidated' virtual entity for QFD and transfer dependency?
- Accrual vs cash basis for government transfers: record both when available, and which one drives the ranked KPI?
- Should overdue payables to IPPs, fuel and gas suppliers (take-or-pay arrears) be added as a separate FIN KPI or folded into net debt? This needs coordination with the COM dimension, which owns receivables.
- FX and inflation handling for per-kWh KPIs across 2019-2025 devaluations (Nigeria, Ghana, Zambia, partly Kenya): average-year FX, PPP, or real LCU indexed to a base year?
- Fiscal-year alignment (e.g. Kenya and South Africa June/March year-ends vs calendar years elsewhere): convention for mapping to the 2019-2025 'year' axis.
- Which UPBEAT (World Bank) financial indicator definitions should be mirrored for interoperability? The UPBEAT pages fetched did not list indicator definitions, so they could not be verified.

## GEN : Production et offre

*In most Sub-Saharan African power systems the binding problem sits upstream: how much installed capacity actually runs, whether it covers peak demand, how much energy comes from expensive oil, diesel or emergency rental plant, and how dependent the utility is on IPPs and imports bought under take-or-pay contracts. These factors drive the utility's cost of supply, its financial gap (subsidies, tariff compensation, arrears to IPPs) and the reliability its customers get (load shedding). Utility annual reports, regulator reports and ministry energy statistics publish them more often than plant-level engineering metrics. This dimension therefore pairs simple, publicly computable capacity and energy-mix ratios (core) with standard plant-performance metrics (extended) that need unit-level data, which is rarely published. All energy flows are in GWh and all money in local currency millions (_lcu_m). The supply balance is: total_supply_gwh = energy_sent_out_gwh (own net generation) + energy_purchased_total_gwh (IPPs + imports + other utilities). Integrated, generation-only and distribution-only companies can then be put on the same footing. A distribution company in an unbundled market (single buyer) has energy_sent_out_gwh = 0, so the generation-capacity KPIs do not apply to it.*

### `GEN_avg_power_purchase_cost` : Coût moyen d'achat d'énergie par kWh acheté
*Average power purchase cost per kWh purchased* · palier **noyau MVP** · noté · plus bas = mieux · unité : LCU per kWh (also USD per kWh)

- **Définition** : Total cost of purchased power (energy charges, capacity/availability charges including take-or-pay payments for undispatched energy, fuel pass-through paid or supplied by the utility, and import charges) divided by energy purchased. Sub-ratios by supplier type (IPP, emergency/rental, imports) are recommended where data allow.
- **Formule** : `GEN_avg_power_purchase_cost = (power_purchase_cost_lcu_m + fuel_supplied_to_ipps_lcu_m) / energy_purchased_total_gwh  [LCU/kWh]. Optional decomposition: capacity_charges_lcu_m / energy_purchased_total_gwh and energy_charges_lcu_m / energy_purchased_total_gwh. USD view divides by fx_lcu_per_usd_avg.`
- **Données brutes** : `power_purchase_cost_lcu_m`, `fuel_supplied_to_ipps_lcu_m`, `energy_purchased_domestic_gwh`, `energy_imported_gwh`, `capacity_charges_lcu_m`, `energy_charges_lcu_m`, `fx_lcu_per_usd_avg`
- **Sources typiques** : audited financial statements (purchased power expense note); utility annual report; regulator tariff determinations / bulk supply tariff decisions; single-buyer annual reports; IMF / World Bank / AfDB sector reviews
- **Disponibilité attendue** : moyenne. Purchased power expense is almost always a separate line in the financial statements, and purchased volume is usually in the energy balance. The split between capacity and energy charges and fuel paid on behalf of IPPs is less often disclosed.
- **Pièges de comparaison** : (1) Take-or-pay capacity payments for energy not taken raise the unit cost without any GWh. This is a real economic cost, but it makes years with low offtake look expensive. (2) Accrued vs paid: unpaid IPP invoices (arrears) may or may not be accrued, and late-payment interest may sit in finance costs. (3) A government that pays IPPs directly or provides guarantees/subsidies can remove costs from the utility books. (4) Imports priced at power-pool or bilateral rates are not comparable with IPP contracts. (5) USD-indexed tariffs vary with exchange rates. (6) For distribution companies buying under a regulated bulk tariff, the KPI reflects the regulator's tariff more than procurement performance.

### `GEN_costly_thermal_share` : Part de l'énergie d'origine thermique coûteuse (fioul/diesel/location d'urgence)
*Share of costly liquid-fuel and emergency power in supply* · palier **noyau MVP** · noté · plus bas = mieux · unité : % of total supply (GWh basis)

- **Définition** : Share of total energy supplied into the system (own net generation plus purchases) that comes from liquid-fuel thermal plant (HFO, LFO, diesel, including isolated-grid diesel) and from emergency or rental power contracts, whatever their fuel. Gas, coal, hydro, other renewables and imports are excluded from the numerator but included in the denominator.
- **Formule** : `GEN_costly_thermal_share = (energy_sent_out_liquid_fuel_gwh + energy_purchased_liquid_fuel_ipp_gwh + energy_purchased_emergency_rental_gwh) / (energy_sent_out_gwh + energy_purchased_total_gwh) x 100. To avoid double counting, an emergency or rental contract that burns liquid fuel is counted only in energy_purchased_emergency_rental_gwh.`
- **Données brutes** : `energy_sent_out_liquid_fuel_gwh`, `energy_purchased_liquid_fuel_ipp_gwh`, `energy_purchased_emergency_rental_gwh`, `energy_sent_out_gwh`, `energy_purchased_domestic_gwh`, `energy_imported_gwh`
- **Sources typiques** : utility annual report (production by source table); regulator annual report; ministry of energy statistics / national energy balance; IMF Article IV or World Bank DPO documents (often discuss emergency power costs); IPP / rental contract disclosures in audited financial statements notes
- **Disponibilité attendue** : moyenne. A production-by-technology breakdown (hydro, thermal, solar, purchases) is commonly published. However, 'thermal' is often not split between gas and liquid fuel, and emergency rental purchases are often lumped with IPP purchases. A thermal-total proxy may be needed (lower confidence).
- **Pièges de comparaison** : (1) An undifferentiated 'thermal' category (gas plus oil) is a frequent source of error. A gas-fired thermal fleet (Cote d'Ivoire, Nigeria, Ghana) is structurally cheaper than an HFO or diesel fleet (Senegal historically, isolated grids). Record the proxy level used. (2) Powerships and rental units may run on HFO or LNG: classify by contract type (emergency/rental) rather than by fuel to stay consistent. (3) Drought years mechanically raise the thermal share in hydro systems (e.g. Zambia, Ghana). Interpret together with a hydrology flag. (4) Isolated mini-grid diesel may be reported separately or not at all. (5) Gross vs net generation: use net (sent-out) for own plant to stay consistent with purchases, which are metered at delivery.

### `GEN_purchased_energy_share` : Part de l'énergie achetée (IPP, importations) dans l'approvisionnement
*Share of purchased energy (IPPs and imports) in total supply* · palier **noyau MVP** · contexte · contexte (non noté) · unité : % of total supply (GWh basis)

- **Définition** : Share of total energy supply that the utility buys from third parties (independent power producers, emergency/rental providers, other national utilities and cross-border imports) rather than generating itself. Sub-shares for IPPs and imports should also be stored. For a distribution-only company buying from a single buyer or bulk supplier, the value is 100% by construction. Report it, but exclude it from peer comparison.
- **Formule** : `GEN_purchased_energy_share = energy_purchased_total_gwh / (energy_sent_out_gwh + energy_purchased_total_gwh) x 100, where energy_purchased_total_gwh = energy_purchased_ipp_gwh + energy_purchased_emergency_rental_gwh + energy_imported_gwh + energy_purchased_other_utility_gwh. Sub-shares: energy_purchased_ipp_gwh / (energy_sent_out_gwh + energy_purchased_total_gwh) x 100; energy_imported_gwh / (energy_sent_out_gwh + energy_purchased_total_gwh) x 100.`
- **Données brutes** : `energy_purchased_domestic_gwh`, `energy_imported_gwh`, `energy_purchased_ipp_gwh`, `energy_purchased_emergency_rental_gwh`, `energy_purchased_other_utility_gwh`, `energy_sent_out_gwh`
- **Sources typiques** : utility annual report (energy balance); audited financial statements (notes on purchases of electricity, sometimes with volumes); regulator annual report / tariff decisions; ministry energy balance; power pool trade statistics
- **Disponibilité attendue** : moyenne. Integrated utilities and regulators usually publish the energy balance with own generation vs purchases, often with imports separated, because purchased power is a major cost line and a recurring policy topic. [Review downgrade from high: The headline own vs purchased share is usually available, but the sub-shares (IPP vs emergency vs imports vs other utilities) and wheeling exclusions are not. Suggested: medium (headline high).]
- **Pièges de comparaison** : (1) This is a structural, not a performance, indicator. A high IPP share is not 'bad' in itself. Its meaning depends on contract terms (take-or-pay capacity charges, indexation to USD or EUR, fuel pass-through). Pair it with GEN_avg_power_purchase_cost. (2) Unbundled vs integrated structure dominates the value. Benchmark only within the same structure category. (3) Some state-owned generators are legally separate but under common control (a sister company), and may be reported as purchases or as own generation depending on consolidation. (4) Wheeling and transit flows (energy passing through to export) should be excluded. (5) Exports should not be netted against imports in this ratio. Store energy_exported_gwh separately.
- **Revue** : energy_purchased_total_gwh = energy_purchased_domestic_gwh (IPP + emergency + other utilities) + energy_imported_gwh; derived, never extracted directly.

### `GEN_available_capacity_ratio` : Taux de disponibilité de la capacité installée (puissance disponible / puissance installée)
*Available-to-installed capacity ratio* · palier **étendu** · noté · plus haut = mieux · unité : %

- **Définition** : Share of the utility's own installed generating capacity that is actually available (dependable, not out on forced or planned outage, derating or fuel shortage) at a stated reference point. The preferred reference point is the system peak hour; otherwise year-end. Covers own plant only. IPP and import capacity are tracked separately through GEN_reserve_margin.
- **Formule** : `GEN_available_capacity_ratio = available_capacity_own_mw / installed_capacity_own_mw x 100, both at the same reference point (capacity_reference_point = 'peak' | 'year_end' | 'annual_average')`
- **Données brutes** : `installed_capacity_own_mw`, `available_capacity_own_mw`, `capacity_reference_point`
- **Sources typiques** : utility annual report (technical / production section); regulator annual report or market monitoring report; ministry of energy statistical yearbook / energy balance; donor project appraisal documents (World Bank PAD, AfDB appraisal report) diagnostic annexes; power pool reports (WAPP, SAPP, EAPP, CAPP)
- **Disponibilité attendue** : faible. Installed capacity is almost always published. 'Available' or 'dependable' capacity is reported regularly by some utilities and regulators and occasionally by others, often only in narrative form (e.g. a number of units out of service) or only in donor diagnostics. The reference point (peak vs year-end) and the meaning of 'available' (dependable, effective, guaranteed) are often not stated. [Review downgrade from medium: Available capacity at a stated reference point is rarely published as a number. Narrative unit-outage counts cannot be converted to MW reliably. Suggested: low.]
- **Référence** (aucune) : none (operational ratio; no single international standard for public reporting at system level)
- **Pièges de comparaison** : (1) 'Installed' may be nameplate gross MW or net MW, and may or may not include mothballed, decommissioned-but-not-retired or rehabilitation-pending units. Some utilities keep derelict plant on the books for decades. (2) Hydro-heavy systems (DRC, Zambia, Congo, Cameroon, Ghana) can be technically available yet energy-constrained by drought or low reservoir levels. Record a hydrology flag. (3) Thermal plant can be available but idle for lack of fuel or gas supply (e.g. gas constraints in Nigeria and Ghana). Decide whether fuel-constrained capacity counts as available and record the choice. (4) Not meaningful for distribution-only companies. (5) Peak and year-end values can differ a lot. Never mix reference points across utilities.
- **Revue** : Review: equality of capacity_reference_point must be a hard comparison filter in the platform, not only a stored flag.

### `GEN_equivalent_availability_factor` : Facteur de disponibilité équivalente (EAF) du parc propre
*Equivalent Availability Factor (EAF) of own fleet* · palier **étendu** · noté · plus haut = mieux · unité : %

- **Définition** : Percentage of period hours that a generating unit (or capacity-weighted fleet) was available, adjusted for deratings, following the NERC GADS / IEEE 762 approach: available hours minus equivalent derated hours, over period hours. For the platform, record the fleet-level value only when the source states that it is EAF (or equivalent) computed on a GADS / IEEE 762 basis. Simple 'availability' percentages without derating adjustment go in a separate field.
- **Formule** : `Per unit: GEN_equivalent_availability_factor = (available_hours - (equivalent_unplanned_derated_hours + equivalent_planned_derated_hours + equivalent_seasonal_derated_hours)) / period_hours x 100. Fleet: weighted by net_maximum_capacity_mw following NERC GADS weighted EAF (WEAF). If only the published value exists: store reported_eaf_pct with eaf_method_stated flag.`
- **Données brutes** : `available_hours`, `equivalent_unplanned_derated_hours`, `equivalent_planned_derated_hours`, `equivalent_seasonal_derated_hours`, `period_hours`, `net_maximum_capacity_mw`, `reported_eaf_pct`, `eaf_method_stated`
- **Sources typiques** : utility integrated / annual report (where generation KPIs are reported, e.g. large integrated utilities); generation company annual reports; regulator generation performance reports; lender technical due-diligence reports (rarely public)
- **Disponibilité attendue** : faible. Unit-hour data are almost never public in the region. Few utilities publish a fleet EAF (or 'energy availability factor'), and most report only a simple 'availability' percentage or none at all.
- **Référence** (vérifiée (URL consultée)) : NERC Generating Availability Data System (GADS) Data Reporting Instructions, Appendix F (Equations), based on IEEE Standard 762 <https://www.nerc.com/pa/RAPA/gads/DataReportingInstructions/Appendix_F_Equations_2023_DRI.pdf>
- **Pièges de comparaison** : (1) Utilities may publish an 'energy availability factor' or plain availability that differs from GADS EAF (e.g. treatment of outside-management-control outages, which NERC handles with separate 'XEAF' variants). (2) Unweighted vs capacity-weighted fleet averages give different results. (3) Hydro units constrained by water are 'available' under EAF but produce little. Pair with GEN_net_capacity_factor. (4) Fleet composition (old coal vs new gas vs hydro) dominates the level.

### `GEN_fuel_cost_per_kwh_thermal` : Coût du combustible par kWh produit (parc thermique propre)
*Fuel cost per kWh of own thermal generation* · palier **étendu** · noté · plus bas = mieux · unité : LCU per kWh (also USD per kWh at average annual exchange rate)

- **Définition** : Fuel expense of the utility's own thermal fleet divided by the net energy sent out by that fleet. Measures exposure to fuel prices, fuel efficiency (heat rate) and fuel mix. Fuel bought by the utility and supplied to IPPs or rental plant under tolling or fuel pass-through arrangements is excluded from the numerator, but is captured as an add-on in GEN_avg_power_purchase_cost.
- **Formule** : `GEN_fuel_cost_per_kwh_thermal = fuel_cost_own_generation_lcu_m / energy_sent_out_thermal_gwh  [LCU m / GWh = LCU/kWh]. USD view: (fuel_cost_own_generation_lcu_m / fx_lcu_per_usd_avg) / energy_sent_out_thermal_gwh.`
- **Données brutes** : `fuel_cost_own_generation_lcu_m`, `energy_sent_out_thermal_gwh`, `fx_lcu_per_usd_avg`
- **Sources typiques** : audited financial statements (operating expenses note: fuel and lubricants / combustibles); utility annual report; regulator tariff review or cost-of-service study; IMF / World Bank reports on energy subsidies
- **Disponibilité attendue** : faible. Fuel expense is normally a separate line or note in audited statements (IFRS, or SYSCOHADA purchase accounts for francophone utilities). Thermal net generation is less consistently published separately from total generation, and fuel bought for IPPs can be mixed into the same line. [Review downgrade from medium: It needs net thermal sent-out and fuel cost net of fuel supplied to IPPs. Both are seldom separable. Suggested: low.]
- **Pièges de comparaison** : (1) Fuel subsidies or state-supplied fuel (fuel provided in kind, or at regulated below-market prices by a national oil company) make fuel cost understate the economic cost. Flag explicitly. (2) Under SYSCOHADA, fuel may sit in 'achats de matières et fournitures' together with other consumables, and stock variation adjustments must be applied. Under IFRS it may be inside 'cost of sales'. (3) Fuel paid on behalf of IPPs in the same expense line inflates the ratio. (4) Fleet mix (gas vs HFO vs diesel) dominates the level, so compare against GEN_costly_thermal_share. (5) Currency effects: oil is priced in USD, so local-currency depreciation raises LCU values. Show USD as well, and keep the FX source explicit. (6) Gross vs net generation denominators must not be mixed.

### `GEN_net_capacity_factor` : Facteur de charge net (facteur d'utilisation) du parc propre
*Net capacity factor of own fleet* · palier **étendu** · contexte · contexte (non noté) · unité : %

- **Définition** : Net energy actually sent out by the utility's own generating fleet (or by one technology group) relative to the energy the fleet would have produced running at full net capacity for all period hours. A proxy for asset utilisation that can be computed from widely published annual data.
- **Formule** : `GEN_net_capacity_factor = energy_sent_out_gwh x 1000 / (installed_capacity_own_net_mw x period_hours) x 100. If only gross generation and gross capacity are published, compute the gross variant energy_generated_gross_gwh x 1000 / (installed_capacity_own_mw x period_hours) x 100 and flag basis = 'gross'. Compute by technology (hydro, thermal, solar) where breakdowns exist.`
- **Données brutes** : `energy_sent_out_gwh`, `energy_generated_gross_gwh`, `installed_capacity_own_net_mw`, `installed_capacity_own_mw`, `period_hours`
- **Sources typiques** : utility annual report (installed capacity and production tables); ministry energy statistics / energy balance; regulator annual report; IRENA / national renewable statistics for technology-level checks
- **Disponibilité attendue** : moyenne. Installed capacity and annual production are among the most consistently published utility figures. A gross-basis computation is almost always possible, while a net basis depends on disclosure of station auxiliary consumption. [Review downgrade from high: Only the gross variant is broadly computable. Net generation depends on auxiliary-consumption disclosure. Suggested: medium (gross variant high).]
- **Référence** (vérifiée (URL consultée)) : NERC GADS Data Reporting Instructions, Appendix F (Net Capacity Factor), based on IEEE Standard 762 <https://www.nerc.com/pa/RAPA/gads/DataReportingInstructions/Appendix_F_Equations_2023_DRI.pdf>
- **Pièges de comparaison** : (1) Technology mix dominates: hydro, solar and peaking diesel have structurally different factors. Compare by technology, not fleet-wide. (2) A low factor can mean unavailability, fuel or water shortage, or deliberate merit-order back-down when cheaper IPP energy is taken under take-or-pay, so interpret it with GEN_available_capacity_ratio and GEN_purchased_energy_share. (3) Capacity commissioned or retired mid-year distorts the denominator. Use a time-weighted average capacity if dates are known. (4) Gross vs net basis must be flagged and not mixed. (5) Derelict units kept in installed capacity depress the factor.
- **Revue** : Review: per NERC GADS, net capacity factor can be negative for units shut down all year (auxiliary consumption); handle explicitly.

### `GEN_reserve_margin` : Marge de réserve de capacité par rapport à la pointe
*Capacity reserve margin over peak demand* · palier **étendu** · noté · plage cible · unité : %

- **Définition** : Surplus (or deficit, if negative) of available capacity over peak demand served or estimated, in % of peak demand. Available capacity includes own available plant plus contracted firm IPP capacity and firm imports, because these are the resources that serve the peak. Negative values indicate structural load shedding.
- **Formule** : `GEN_reserve_margin = (available_capacity_own_mw + available_capacity_ipp_mw + firm_import_capacity_mw - peak_demand_mw) / peak_demand_mw x 100. peak_demand_mw should be the reported peak demand. Flag peak_demand_basis = 'served' | 'estimated_unconstrained'.`
- **Données brutes** : `available_capacity_own_mw`, `available_capacity_ipp_mw`, `firm_import_capacity_mw`, `peak_demand_mw`, `peak_demand_basis`
- **Sources typiques** : utility annual report; regulator annual report / system operator report; national least-cost generation expansion plan / integrated resource plan; power pool annual reports; donor project documents
- **Disponibilité attendue** : faible. Peak demand (MW) is very widely published. Available IPP capacity and firm import capacity are less often disclosed in a usable form, so a contracted-capacity proxy may be needed (record it as such with lower confidence). Many reports already quote a reserve margin, but with an undisclosed formula. [Review downgrade from medium: It needs available IPP MW and firm import MW, which are rarely disclosed. A contracted-capacity proxy changes the meaning. Suggested: low.]
- **Référence** (aucune) : none (system-planning concept; definitions vary between planning reports and regulators)
- **Pièges de comparaison** : (1) In supply-constrained systems, recorded peak is suppressed demand (what could be served). This inflates the reserve margin. Prefer the estimated unconstrained peak when published, and always store the basis. (2) Using installed rather than available capacity in the numerator makes systems with large derelict fleets look comfortable. (3) The direction is a target range: a very high margin can mean expensive idle capacity under take-or-pay. Do not publish numeric targets. (4) Interconnected systems relying on pool imports (e.g. through SAPP or WAPP) need firm and non-firm imports separated. (5) Integrated utility vs national system: in unbundled markets (Nigeria, Ghana, Kenya), compute at the system or single-buyer level and attribute it carefully.

**Questions ouvertes (GEN)**

- Should GEN KPIs be computed at the utility-entity level only, or also at the national-system level (single buyer + IPPs + system operator) for unbundled markets (Nigeria, Ghana, Kenya, South Africa)? This affects how distribution companies are scored on reserve margin and costly thermal share.
- How should fuel supplied in kind or subsidised by the state or a national oil company (and IPP fuel paid directly by the Treasury) be recorded? As a separate 'off-book cost' raw item, or only as a qualitative flag?
- Is a hydrology/drought flag per country-year (e.g. from the utility or ministry narrative) acceptable as a contextual field, given that it strongly drives the thermal share, capacity factor and unserved energy in hydro-dominated systems?
- Which exchange-rate source should be the single reference for USD conversions (e.g. IMF IFS annual average vs central bank), so that GEN_fuel_cost_per_kwh_thermal and GEN_avg_power_purchase_cost are comparable across currencies?
- For reserve margin, when only contracted IPP capacity (not available capacity) is published, is a lower-confidence proxy acceptable, or should the KPI be left blank?
- How should powerships and long-running 'emergency' rental contracts be classified (emergency vs IPP) when contracts have been extended for many years?
- Should unserved energy cover only generation/supply-shortfall load shedding (as defined here), with network-fault END left to the reliability (SAIDI/SAIFI) dimension? This must be coordinated with the network/quality dimension to avoid double counting.

## NET : Réseau : pertes et fiabilité

*Network losses and supply reliability are the operational KPIs that matter most for African utilities' finances and service quality. Every kWh lost between injection and the meter is energy that was already paid for. In single-buyer systems that cost includes IPP take-or-pay energy, and sometimes diesel or emergency power, but it earns no revenue. That raises the tariff-cost gap and the need for subsidies or tariff compensation. Loss figures (total, transmission, distribution) appear fairly often in annual reports, regulator reports and ministry energy statistics. They are often the only quantified operational indicator a utility discloses. SAIDI and SAIFI are disclosed less consistently, but regulators (e.g. in Kenya, Ghana, Nigeria and South Africa) and donor results frameworks increasingly require them. Network size metrics (km of line, number of transformers, customers) are mostly context variables. They are needed to normalise O&M spend and to explain differences in losses and reliability between utilities. Commercial billing efficiency, collection rates and ATC&C collection components belong to the COM dimension and are not covered here. This section only measures energy that physically and commercially goes missing between injection and billing.*

### `NET_distribution_losses_pct` : Pertes de distribution
*Distribution losses* · palier **noyau MVP** · noté · plus bas = mieux · unité : % of energy injected into distribution

- **Définition** : Energy lost within the MV/LV distribution network (technical plus non-technical), as a share of energy injected into the distribution network at transmission/distribution interface points (bulk supply points / primary substations).
- **Formule** : `100 * (energy_injected_distribution_gwh - energy_billed_distribution_gwh) / energy_injected_distribution_gwh, where energy_billed_distribution_gwh = energy_billed_gwh - energy_billed_hv_direct_gwh - energy_exported_billed_gwh`
- **Données brutes** : `energy_injected_distribution_gwh`, `energy_billed_gwh`, `energy_billed_hv_direct_gwh`, `energy_exported_billed_gwh`, `reported_distribution_losses_pct`
- **Sources typiques** : distribution company annual report; regulator performance reports (e.g. NERC quarterly reports for Nigerian DisCos); multi-year tariff order / tariff review documents; donor project documents (loss-reduction programmes)
- **Disponibilité attendue** : moyenne. Distribution companies and regulators of unbundled markets usually publish this figure, because it drives tariff loss allowances. Integrated utilities often report only total losses, or a T/D split without the underlying energy flows.
- **Référence** (de mémoire, non vérifiée) : none
- **Pièges de comparaison** : Interface metering at bulk supply points is often missing or faulty, so injected energy may be estimated. Some regulators (e.g. Nigeria) publish ATC&C, which mixes losses with collection; only the technical-plus-commercial part belongs here. Collection efficiency is COM. Inclusion of HV/MV direct customers in the billed figure is inconsistent. Prepaid meter rollout and meter bypass affect non-technical losses. Rural electrification extensions (long LV lines, low load density) structurally raise technical losses. Control for customers per km and the urban/rural mix.
- **Revue** : Review fix: single canonical energy_billed_distribution_gwh shared with COM, so billing efficiency = 100 - distribution losses holds exactly.

### `NET_saidi_hours` : Durée moyenne d'interruption par client (SAIDI)
*System Average Interruption Duration Index (SAIDI)* · palier **noyau MVP** · noté · plus bas = mieux · unité : hours per customer per year

- **Définition** : Average total duration of sustained interruptions per customer served during the year. Numerator: the sum over all sustained interruption events of customers interrupted multiplied by interruption duration. Denominator: total number of customers served. Record separately whether planned outages, load shedding (generation-deficit rationing) and major event days are included.
- **Formule** : `customer_interruption_duration_hours / customers_total_count, where customer_interruption_duration_hours = sum over sustained events of (customers_interrupted_in_event * event_duration_hours); store flags reliability_includes_planned_flag, reliability_includes_load_shedding_flag, reliability_excludes_major_events_flag, and reported_saidi_hours as published.`
- **Données brutes** : `customer_interruption_duration_hours`, `customers_total_count`, `reported_saidi_hours`, `reliability_includes_planned_flag`, `reliability_includes_load_shedding_flag`, `reliability_excludes_major_events_flag`
- **Sources typiques** : regulator quality-of-service / performance reports; utility annual report or integrated report (sustainability section); donor results frameworks (PAD indicators, completion reports); World Bank Doing Business 'Getting Electricity' reliability data (historical, discontinued)
- **Disponibilité attendue** : faible. Reported by utilities under regulator quality-of-service regimes (typically anglophone markets and some francophone utilities with performance contracts). Many smaller utilities do not publish it, or publish a feeder-based or non-standard outage-time measure instead. [Review downgrade from medium: Outside a few anglophone regulators, customer-weighted SAIDI with disclosed inclusion flags is rarely published. Without the flags the value cannot be compared. Suggested: low-medium (flag-complete values low).]
- **Référence** (existence vérifiée, contenu non vérifié) : IEEE 1366 (IEEE Guide for Electric Power Distribution Reliability Indices) <https://www.standards.nimonik.com/products/ieee/ieee-1366/>
- **Pièges de comparaison** : The biggest risk is treating load shedding as equivalent. Load shedding in South Africa, Zambia and Ghana in some years can dominate interruption time and is excluded by some reporters and included by others. Momentary interruption thresholds differ (IEEE uses longer than 5 minutes for sustained), and major-event-day normalisation is rarely applied. Many African utilities lack OMS/SCADA down to LV, so durations are estimated at feeder or MV level and ignore LV faults. Francophone utilities often report 'temps moyen de coupure' or 'energie non distribuee', which are not equivalent. Nigerian DisCo reporting may be feeder-hours, not customer-weighted. Customer counts may include inactive or disconnected accounts. Compare only within the same definition flags.
- **Revue** : Reference: the fetched URL is a third-party standards reseller, not IEEE. Cite IEEE Std 1366 by edition via the IEEE site and record the edition assumed.

### `NET_total_system_losses_pct` : Pertes totales du système (transport + distribution)
*Total system (T&D) losses* · palier **noyau MVP** · noté · plus bas = mieux · unité : % of net energy available for the domestic system

- **Définition** : Energy lost between the points where energy enters the utility's network (own generation sent out, purchases from IPPs or other utilities, imports) and the domestic customers' meters, as a share of net energy available for the domestic system. Includes technical and non-technical (commercial) losses. Excludes station auxiliary consumption, because sent-out energy is net of auxiliaries.
- **Formule** : `100 * ((energy_sent_out_gwh + energy_purchased_total_gwh - energy_exported_gwh) - energy_billed_gwh) / (energy_sent_out_gwh + energy_purchased_total_gwh - energy_exported_gwh); energy_billed_gwh = domestic customer billing only (excluding export sales). If the utility reports its own losses figure, also store reported_total_losses_pct and flag any difference.`
- **Données brutes** : `energy_sent_out_gwh`, `energy_purchased_domestic_gwh`, `energy_imported_gwh`, `energy_exported_gwh`, `energy_billed_gwh`, `reported_total_losses_pct`
- **Sources typiques** : utility annual report (operational highlights / energy balance); regulator annual report or tariff review; ministry of energy statistical yearbook / energy balance; World Bank / AfDB project appraisal documents (PAD) and results frameworks; SIE (Systeme d'Information Energetique) reports in francophone countries
- **Disponibilité attendue** : élevée. Most vertically integrated utilities publish an energy balance or at least a headline loss rate, and regulators track it for tariff setting. Exact energy volumes in the numerator and denominator are less often published than the headline percentage, so the recomputed value may only be available for part of the sample.
- **Référence** (de mémoire, non vérifiée) : none (no single binding standard; follows common utility energy-balance practice; the World Bank UPBEAT platform tracks loss indicators, but its exact definition was not checked)
- **Pièges de comparaison** : Utilities use different denominators: generation gross vs sent-out, inclusion of purchases and imports, and exports netted or not. Some report losses against energy injected into distribution only. Some count 'energy sold' including unbilled own use or public lighting that is not billed. Prepaid vending changes the timing of what counts as billed (energy vended vs consumed). Estimated billing of unmetered customers can hide non-technical losses. Unbundled structures (Nigeria TCN + DisCos; Ghana GRIDCo + ECG/NEDCo; Kenya KETRACO/KPLC) need consolidation across entities, or the KPI is not comparable with integrated utilities. Control for network length, share of HV bulk sales (mining loads in DRC/Zambia lower the loss ratio), rural share and load shedding (less energy injected changes the ratio). Fiscal year vs calendar year varies by utility.

### `NET_customers_per_network_km` : Densité de clients par km de réseau de distribution
*Customer density per km of distribution network* · palier **étendu** · contexte · contexte (non noté) · unité : customers per km (companion: customers per transformer)

- **Définition** : Number of customers served per km of MV+LV distribution line. A context variable used to normalise losses, reliability and O&M cost comparisons. A companion metric, customers per distribution transformer, indicates LV network structure and theft exposure.
- **Formule** : `customers_total_count / distribution_line_length_km; companion: customers_total_count / distribution_transformer_count`
- **Données brutes** : `customers_total_count`, `distribution_line_length_km`, `distribution_transformer_count`
- **Sources typiques** : utility annual report technical statistics; regulator annual report; ministry energy statistics; donor project appraisal documents (network baseline data)
- **Disponibilité attendue** : moyenne. Customer counts are widely published. Distribution line length and transformer counts appear in many annual reports and regulator statistics, though they may not be updated every year.
- **Référence** (de mémoire, non vérifiée) : none
- **Pièges de comparaison** : Customer counts may be accounts, not connections, and may include inactive or disconnected accounts. Shared connections or informal sub-connections (common in peri-urban areas) understate real users. Rapid electrification programmes add customers faster than network length is updated in the statistics. Mixing route km and circuit km, and including or excluding LV, changes the result. Utilities whose sales are dominated by mining or industry (e.g. DRC, Zambia) have low customer density without that meaning poor performance.

### `NET_energy_not_supplied_pct` : Énergie non distribuée (END) en % de la demande servie
*Energy not supplied (ENS) as share of energy delivered* · palier **étendu** · noté · plus bas = mieux · unité : % of potential energy delivered

- **Définition** : Estimated energy that customers would have consumed but did not receive because of network interruptions and/or load shedding, as a share of energy that would have been delivered (energy delivered plus energy not supplied). Commonly reported by francophone utilities and system operators as 'energie non distribuee' (END). State whether generation-deficit shedding is included.
- **Formule** : `100 * (energy_not_supplied_supply_shortfall_gwh + energy_not_supplied_network_gwh) / (energy_sent_out_gwh + energy_purchased_total_gwh - energy_exported_gwh + energy_not_supplied_supply_shortfall_gwh + energy_not_supplied_network_gwh); the two cause components are stored separately; fallback field (never mixed): load_shedding_hours_count.`
- **Données brutes** : `energy_not_supplied_supply_shortfall_gwh`, `energy_not_supplied_network_gwh`, `energy_sent_out_gwh`, `energy_purchased_domestic_gwh`, `energy_imported_gwh`, `energy_exported_gwh`, `reported_energy_not_supplied_gwh`, `load_shedding_hours_count`
- **Sources typiques** : utility annual report (francophone utilities' 'rapport d'activites'); national system operator / dispatching annual statistics; regulator annual report; ministry energy statistics (SIE)
- **Disponibilité attendue** : faible. Reported by some utilities and system operators, especially francophone ones and those under performance contracts with the state. Many others do not publish it. It may be the only reliability measure available where SAIDI is not published.
- **Référence** (de mémoire, non vérifiée) : none
- **Pièges de comparaison** : ENS is an estimate (based on load before the interruption or on typical load curves), and estimation methods are rarely disclosed. Scope differs: network faults only vs including generation shortfalls and load shedding. Not interchangeable with SAIDI. Use it for trend analysis within one utility, and use the scope flag before comparing across utilities.
- **Revue** : Merged with the former GEN_unserved_energy_ratio: one ENS record, one denominator, cause split (supply shortfall vs network faults).

### `NET_hours_of_supply_per_day` : Heures de fourniture par jour
*Hours of supply per day* · palier **étendu** · noté · plus haut = mieux · unité : hours per day

- **Définition** : Average daily hours of supply delivered to customers or feeders, as reported, with the weighting basis flagged. Used where SAIDI is absent.
- **Formule** : `as reported: avg_supply_hours_per_day (feeder- or customer-weighted, flag supply_hours_weighting_basis)`
- **Données brutes** : `avg_supply_hours_per_day`, `supply_hours_weighting_basis`
- **Sources typiques** : regulator quarterly / annual reports; band-based tariff reports
- **Disponibilité attendue** : faible. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

### `NET_non_technical_losses_pct` : Pertes non techniques (commerciales)
*Non-technical (commercial) losses* · palier **étendu** · noté · plus bas = mieux · unité : % of net energy available for the domestic system

- **Définition** : Estimated losses due to theft, fraud, meter tampering or bypass, metering errors, unmetered or unbilled consumption and billing errors, as a share of the same denominator used for total system losses. Technical losses equal total losses minus non-technical losses. Only populated when the utility, regulator or a loss study discloses the split.
- **Formule** : `100 * non_technical_losses_gwh / (energy_sent_out_gwh + energy_purchased_total_gwh - energy_exported_gwh); companion value technical_loss_share_pct = 100 * technical_losses_gwh / (technical_losses_gwh + non_technical_losses_gwh); if only percentages are disclosed, store reported_technical_losses_pct and reported_non_technical_losses_pct with their stated denominator.`
- **Données brutes** : `non_technical_losses_gwh`, `technical_losses_gwh`, `energy_sent_out_gwh`, `energy_purchased_domestic_gwh`, `energy_imported_gwh`, `energy_exported_gwh`, `reported_technical_losses_pct`, `reported_non_technical_losses_pct`, `loss_split_method_text`
- **Sources typiques** : technical loss studies commissioned by utility or donors; regulator tariff determinations (loss allowances); World Bank / AfDB / MCC project documents (loss-reduction components); utility annual report narrative sections
- **Disponibilité attendue** : faible. The split depends on load-flow studies and estimates. It is published irregularly, often only in donor or tariff documents, and rarely as an annual series.
- **Référence** (de mémoire, non vérifiée) : none
- **Pièges de comparaison** : Technical losses are usually modelled and non-technical losses taken as the residual, so the split depends on the method and the study year. Store the method text and confidence. Policy reclassification (e.g. regularising illegal connections, revising public-sector or estimated-billing volumes) can shift volumes between categories without any physical change. Do not interpolate between study years.

### `NET_om_cost_per_network_km` : Coût d'exploitation et de maintenance du réseau par km de ligne
*Network O&M expenditure per km of line* · palier **étendu** · contexte · contexte (non noté) · unité : LCU thousand per km per year (USD thousand per km when converted)

- **Définition** : Annual operating and maintenance expenditure on transmission and distribution assets (excluding depreciation, energy purchases and capitalised maintenance), divided by total circuit length of transmission and distribution lines. Can also be computed separately for transmission and distribution when the cost split is disclosed.
- **Formule** : `1000 * network_om_expense_lcu_m / (transmission_line_length_km + distribution_line_length_km)  [LCU thousand per km]; USD view: 1000 * (network_om_expense_lcu_m / fx_lcu_per_usd_avg) / (transmission_line_length_km + distribution_line_length_km)  [USD thousand per km]`
- **Données brutes** : `network_om_expense_lcu_m`, `transmission_line_length_km`, `distribution_line_length_km`, `fx_lcu_per_usd_avg`
- **Sources typiques** : audited financial statements (notes on operating expenses by nature or function); segment reporting in annual report (transmission / distribution segments); regulator tariff review (allowed O&M opex); utility annual report technical statistics (network length)
- **Disponibilité attendue** : faible. Network length is often published. A clean network O&M cost line is rare: integrated utilities usually report costs by nature (personnel, materials, external services), not by network function, especially under SYSCOHADA.
- **Référence** (de mémoire, non vérifiée) : none
- **Pièges de comparaison** : SYSCOHADA (by nature) vs IFRS (by function or segment) presentation makes isolating network O&M difficult. Capitalisation policies for maintenance differ. Donor-financed rehabilitation may be off the utility's books. Line length may be route km vs circuit km, and LV may be excluded. Currency depreciation and high inflation (Nigeria, Ghana, Zambia, DRC) distort time series; compare in real terms or USD. Low O&M spend can be a sign of underinvestment that shows up later as higher SAIDI or losses, so it is not 'lower is better'.
- **Revue** : Review fix: the draft USD conversion dropped the per-km division.

### `NET_saifi_count` : Fréquence moyenne d'interruption par client (SAIFI)
*System Average Interruption Frequency Index (SAIFI)* · palier **étendu** · noté · plus bas = mieux · unité : interruptions per customer per year

- **Définition** : Average number of sustained interruptions experienced per customer served during the year: total customer interruptions divided by total customers served. Use the same inclusion flags as SAIDI.
- **Formule** : `customers_interrupted_count / customers_total_count, where customers_interrupted_count = sum over sustained events of customers interrupted in the event; store reported_saifi_count and inclusion flags (planned, load shedding, major events).`
- **Données brutes** : `customers_interrupted_count`, `customers_total_count`, `reported_saifi_count`, `reliability_includes_planned_flag`, `reliability_includes_load_shedding_flag`, `reliability_excludes_major_events_flag`
- **Sources typiques** : regulator quality-of-service / performance reports; utility annual or integrated report; donor results frameworks
- **Disponibilité attendue** : moyenne. Usually published alongside SAIDI where SAIDI exists. Slightly less often published on its own.
- **Référence** (existence vérifiée, contenu non vérifié) : IEEE 1366 (IEEE Guide for Electric Power Distribution Reliability Indices) <https://www.standards.nimonik.com/products/ieee/ieee-1366/>
- **Pièges de comparaison** : Same issues as SAIDI: load shedding inclusion, the threshold for counting a sustained interruption, LV visibility and feeder vs customer weighting. Rotational load shedding can produce a very high SAIFI while the reported SAIDI looks moderate if durations are capped or estimated. Use SAIDI/SAIFI (CAIDI) only when both share the same flags.
- **Revue** : Reference: the fetched URL is a third-party standards reseller, not IEEE. Cite IEEE Std 1366 by edition via the IEEE site and record the edition assumed.

### `NET_transmission_losses_pct` : Pertes de transport
*Transmission losses* · palier **étendu** · noté · plus bas = mieux · unité : % of energy injected into transmission

- **Définition** : Energy lost on the HV transmission network between injection points (generation sent-out, purchases and imports at HV) and offtake points (bulk supply points to distribution, HV direct customers, export points), as a share of energy injected into the transmission network.
- **Formule** : `100 * (energy_injected_transmission_gwh - energy_delivered_transmission_offtake_gwh) / energy_injected_transmission_gwh; energy_delivered_transmission_offtake_gwh = energy_injected_distribution_gwh + energy_billed_hv_direct_gwh + energy_exported_gwh (when the components are disclosed).`
- **Données brutes** : `energy_injected_transmission_gwh`, `energy_delivered_transmission_offtake_gwh`, `energy_injected_distribution_gwh`, `energy_billed_hv_direct_gwh`, `energy_exported_gwh`, `reported_transmission_losses_pct`
- **Sources typiques** : transmission company annual report (e.g. TSO / grid company); system operator / national control centre annual statistics; regulator annual report; power pool reports (SAPP, WAPP, EAPP, CAPP) for interconnection data
- **Disponibilité attendue** : moyenne. Unbundled transmission companies and system operators usually report it. Integrated utilities may report it inside an energy balance or not at all, and smaller francophone utilities often give only a combined loss figure.
- **Référence** (de mémoire, non vérifiée) : none
- **Pièges de comparaison** : Strongly affected by network geography: long radial lines from remote hydro (e.g. Inga-Kolwezi, Kafue/Kariba) and voltage level. Wheeling and transit flows for regional power pools inflate injected energy. Utilities differ on whether step-up transformer losses at power stations are counted in generation or transmission. Not meaningful for distribution-only entities. Treat it as a context-heavy metric and compare mainly over time within one utility.

**Questions ouvertes (NET)**

- Default loss denominator: should the platform standardise on net energy available for the domestic system (sent-out + purchases + imports - exports) and recompute from volumes, or store each utility's reported percentage with its stated denominator as the primary value?
- How should unbundled systems (Nigeria TCN + DisCos, Ghana GRIDCo + ECG/NEDCo, Kenya KETRACO/KPLC) be shown: system-level consolidated losses, entity-level only, or both?
- SAIDI/SAIFI handling of load shedding: report a headline value including all interruptions plus a network-only variant, or only accept values whose inclusion flags are explicitly disclosed?
- Should Nigerian ATC&C (and similar regulator composites) be split, with the technical/commercial part kept in NET and collection moved to COM, or stored as a separate cross-dimension KPI?
- Is a free proxy for reliability acceptable when SAIDI is absent (e.g. ENS, number of hours of supply per day reported by regulators for Nigerian feeder bands)? If so, how should the proxy status be shown in the UI?
- For energy_billed_gwh with prepaid customers: use energy vended (token sales) or estimated consumption, and how should the vending-vs-consumption timing difference be flagged?
- Should network length be stored as route km or circuit km by default, and should LV be mandatory for the density and O&M-per-km KPIs?
- The World Bank UPBEAT platform tracks loss and reliability indicators for many of the same utilities. Should its exact definitions be fetched and aligned with, to allow cross-checking (definitions were not verified in this pass)?

## COM : Performance commerciale

*Commercial performance covers the chain from energy delivered into the distribution network, to energy billed, to cash collected. In Sub-Saharan Africa this chain is often where most utility value is lost: unbilled energy (theft, unmetered or flat-rate customers, faulty meters), unpaid bills (especially public-sector arrears from ministries, state companies and municipalities), and tariffs that do not cover cost. These KPIs show whether a utility turns physical supply into cash, which drives its ability to pay IPPs and fuel suppliers (take-or-pay, diesel or emergency power), to service debt, and to depend less on state subsidies or tariff compensation. The cash recovery index links COM to the NET (network losses) dimension. Billing efficiency, measured on energy injected into distribution, is the complement of the NET distribution loss rate measured on the same basis. Multiplying billing efficiency by the collection rate gives the share of injected energy that is actually paid for, which is the inverse of an ATC&C-type loss measure. Data come from three sources: annual reports and regulator reports (energy billed and injected, customer, meter and prepaid counts), audited financial statements under IFRS or SYSCOHADA (revenue, receivables and their notes), and regulator or donor monitoring (collection rates, public-sector arrears). Collection and segment-receivables data are published less often than energy and revenue data.*

### `COM_cash_recovery_index` : Indice de recouvrement de trésorerie (CRI)
*Cash recovery index (CRI)* · palier **noyau MVP** · noté · plus haut = mieux · unité : % of energy injected into distribution (value-weighted)

- **Définition** : Share of energy injected into the distribution network that is converted into cash, combining the physical side (billing efficiency, the complement of NET distribution losses) and the financial side (collection rate). This is the bridge KPI between the NET and COM dimensions. (1 - CRI) corresponds to an aggregate technical, commercial and collection (ATC&C) loss rate measured on the same denominator.
- **Formule** : `COM_cash_recovery_index (%) = (energy_billed_distribution_gwh / energy_injected_distribution_gwh) * min(1, cash_collected_lcu_m / revenue_billed_lcu_m) * 100. Uncapped value and 3-year average stored. ATC&C loss (%) = 100 - COM_cash_recovery_index.`
- **Données brutes** : `energy_billed_distribution_gwh`, `energy_injected_distribution_gwh`, `cash_collected_lcu_m`, `revenue_billed_lcu_m`
- **Sources typiques** : derived from utility annual report and regulator data; World Bank / AfDB utility performance assessments and project documents; regulator performance reports (some publish ATC&C directly)
- **Disponibilité attendue** : faible. Computable wherever both billing efficiency and the collection rate are available. Its availability is therefore capped by the collection rate. Some regulators (e.g. Nigeria) publish ATC&C losses directly, so CRI can also be derived from that figure. [Review downgrade from medium: Its availability is capped by both the injected-distribution denominator and the collection rate. The product of two medium-availability items is lower. Suggested: low-medium.]
- **Référence** (de mémoire, non vérifiée) : Aggregate Technical, Commercial and Collection (ATC&C) loss concept used in Indian and Nigerian regulatory practice and in World Bank/USAID utility-performance work; exact CRI naming not confirmed in a fetched source
- **Pièges de comparaison** : It inherits every pitfall of its two components. (1) It must use the same denominator as the NET distribution loss KPI. If NET uses sent-out energy, the bridge breaks. (2) It multiplies a volume ratio by a value ratio, which assumes uncollected amounts are spread evenly across tariff classes. In practice, high-tariff commercial customers and low-tariff or lifeline households, or public entities, differ. (3) Collection rates above 100% from arrears recovery can inflate CRI in a single year, so report a multi-year average alongside. (4) A tariff that is below cost does not show here; read CRI together with COM_revenue_per_kwh_billed and the FIN cost-recovery KPIs. Control for: structure, prepaid share, public-sector share.
- **Revue** : Review fix: collection can exceed 100% in arrears-recovery years; capped in the ranked value.

### `COM_collection_rate` : Taux de recouvrement
*Collection rate (collection efficiency)* · palier **noyau MVP** · noté · plus haut = mieux · unité : % of amount billed

- **Définition** : Cash collected from electricity customers during the period as a share of the amount billed to them in the same period, with both figures on the same tax basis (both including or both excluding VAT and levies). Includes prepaid vending receipts in both numerator and denominator. Can exceed 100% when old arrears are recovered.
- **Formule** : `COM_collection_rate (%) = (cash_collected_lcu_m / revenue_billed_lcu_m) * 100, where revenue_billed_lcu_m includes prepaid sales, and both are on the same VAT/levy basis.`
- **Données brutes** : `cash_collected_lcu_m`, `revenue_billed_lcu_m`
- **Sources typiques** : utility annual report (commercial performance section); regulator monthly/quarterly market reports (e.g. DisCo remittance and collection data); World Bank / IMF program documents and sector financial recovery plans; audited financial statements (cash flow statement: cash receipts from customers, as a proxy)
- **Disponibilité attendue** : moyenne. Regulators often publish collection rates for unbundled DisCos, and some integrated utilities report a 'taux de recouvrement'. Many audited statements do not, so a proxy may be needed: cash receipts from customers (direct-method cash flow) divided by revenue adjusted for VAT. This proxy is less reliable and must be flagged as derived.
- **Référence** (de mémoire, non vérifiée) : Common utility/regulator practice; collection-efficiency component of ATC&C methodology
- **Pièges de comparaison** : (1) Same-period vs cohort basis: collections in the period may include arrears from earlier years, so values above 100% occur and do not mean sustained performance. (2) VAT/levy inconsistency between billing (often excluding VAT) and cash (including VAT). (3) Non-cash settlements: offsets of government arrears against taxes, subsidies or tariff compensation, and cross-debt netting between state entities, may or may not be counted as collections. (4) Prepaid sales are effectively fully collected, so prepaid-heavy utilities show higher rates mechanically. (5) Some reports cover only private or low-voltage customers and exclude the public sector. Control for: prepaid share, public-sector share of billing, treatment of non-cash settlements.

### `COM_receivables_days` : Délai moyen de recouvrement des créances clients (DSO)
*Trade receivables days (DSO), all customers* · palier **noyau MVP** · noté · plus bas = mieux · unité : days

- **Définition** : Average number of days of electricity sales outstanding in trade receivables at year end. Uses net receivables after impairment (expected credit loss) as the primary basis. A gross variant is also computed where disclosed, because large impairments of public or old arrears can make net DSO look artificially healthy.
- **Formule** : `((trade_receivables_electricity_gross_lcu_m - tariff_compensation_receivable_lcu_m) / revenue_billed_lcu_m) * days_in_period, with revenue_billed_lcu_m on the same VAT basis as receivables (revenue_billed_vat_basis_code). Net-of-impairment variant stored.`
- **Données brutes** : `trade_receivables_electricity_gross_lcu_m`, `trade_receivables_electricity_net_lcu_m`, `tariff_compensation_receivable_lcu_m`, `revenue_billed_lcu_m`, `revenue_billed_vat_basis_code`, `days_in_period`
- **Sources typiques** : audited financial statements (balance sheet and trade receivables note: gross, impairment, ageing); utility annual report; IMF Article IV / program reports and World Bank documents on SOE arrears
- **Disponibilité attendue** : moyenne. Trade receivables and revenue are in every set of audited financial statements, under both IFRS and SYSCOHADA. Gross receivables and impairment are usually in the notes, though less consistently. The main constraint is whether financial statements are published at all, as some national utilities publish them late or not at all. [Review downgrade from high: Electricity-only, VAT-adjusted receivables excluding State compensation receivables need notes. Publication gaps also apply. Suggested: medium.]
- **Référence** (de mémoire, non vérifiée) : Standard financial-analysis ratio (days sales outstanding); receivable impairment under IFRS 9 expected credit loss model or SYSCOHADA provisions for doubtful receivables
- **Pièges de comparaison** : (1) Net vs gross: aggressive or lax impairment (IFRS 9 ECL vs SYSCOHADA 'provisions pour créances douteuses') changes net DSO a lot. (2) Receivables usually include VAT while revenue excludes it, which inflates DSO by the VAT rate; flag it or adjust. (3) Receivables may include non-electricity items (connection fees, government subsidy or tariff-compensation receivables, receivables from related state entities), which must be excluded where the note allows. (4) Prepaid-heavy utilities have mechanically lower DSO. (5) Single buyers and bulk sellers (e.g. a transmission company selling to DisCos) have intercompany receivables that are structurally different from retail. (6) Write-offs or debt-for-equity and arrears-clearance agreements with the state cause one-off drops. (7) Hyperinflation or devaluation distorts year-end balances against flow revenue. Control for: prepaid share, public-sector share, retail vs bulk structure.
- **Revue** : Review fix: VAT basis aligned; State tariff-compensation receivables excluded; gross basis is the comparison basis (as for the public-sector variant).

### `COM_bad_debt_expense_pct_revenue` : Dotations pour créances douteuses / chiffre d’affaires
*Bad-debt expense as % of revenue* · palier **étendu** · noté · plus bas = mieux · unité : %

- **Définition** : Impairment / bad-debt expense on trade receivables as a share of electricity sales revenue (accrual measure of collection failure).
- **Formule** : `bad_debt_expense_lcu_m / revenue_electricity_sales_lcu_m * 100`
- **Données brutes** : `bad_debt_expense_lcu_m`, `revenue_electricity_sales_lcu_m`
- **Sources typiques** : audited financial statements (income statement notes)
- **Disponibilité attendue** : moyenne. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

### `COM_billing_efficiency` : Taux de facturation (efficacité de facturation)
*Billing efficiency* · palier **étendu** · dérivé, affiché seulement · plus haut = mieux · unité : % of energy injected into distribution

- **Définition** : Share of energy injected into the distribution network that is billed to final customers in the same period. For a vertically integrated utility the denominator is the energy entering the distribution network (after transmission). Any export or high-voltage direct sales billed outside distribution must be excluded from both numerator and denominator. Measured on the same basis, this KPI is the complement of the NET distribution loss rate (technical plus non-technical).
- **Formule** : `COM_billing_efficiency = 100 - NET_distribution_losses_pct = 100 * energy_billed_distribution_gwh / energy_injected_distribution_gwh`
- **Données brutes** : `energy_billed_gwh`, `energy_billed_distribution_gwh`, `energy_billed_hv_direct_gwh`, `energy_exported_billed_gwh`, `energy_injected_distribution_gwh`
- **Sources typiques** : utility annual report (technical/commercial statistics section); regulator annual or quarterly sector report; ministry energy statistics yearbook; World Bank / AfDB project appraisal documents and implementation reports
- **Disponibilité attendue** : moyenne. Most utilities and regulators publish energy billed and energy injected, sent out or purchased, or a loss rate from which these can be derived. Nigeria's regulator publishes DisCo billing efficiency regularly. The weak point is the exact denominator: many reports give energy sent out or available rather than energy injected into distribution, so many values will need a basis flag. [Review downgrade from high: Energy injected into distribution is rarely published by integrated utilities. COM's own rationale admits that many values will need a basis flag. Suggested: medium.]
- **Référence** (de mémoire, non vérifiée) : Common utility/regulator practice; consistent with the billing-efficiency component of ATC&C loss methodology (used e.g. in Indian and Nigerian regulatory reporting)
- **Pièges de comparaison** : (1) Denominator basis: injected-into-distribution vs sent-out from generation vs total energy available (including imports). Mixing them shifts results by the amount of transmission losses. (2) Estimated billing: unmetered or flat-rate customers (forfait) and estimated bills inflate billed kWh without any metering behind them. (3) Unbundled DisCos (e.g. Nigeria) report energy received from the transmission operator, while integrated utilities (SNEL, E2C, ENEO) often report only network-wide losses. (4) Treatment of bulk customers, exports and auxiliary consumption. (5) Period mismatch between meter-reading cycles and the fiscal year. (6) Prepaid energy may be counted on vending (tokens sold), not on consumption. Control for: structure (integrated vs DisCo), share of HV/MV customers, share of unmetered customers.
- **Revue** : Not scored separately (exact complement of NET_distribution_losses_pct); displayed only.
- **Revue** : Reference: ATC&C attribution to Indian/Nigerian regulatory practice is from memory; no document fetched.

### `COM_metering_coverage` : Taux de comptage des clients
*Metering coverage* · palier **étendu** · noté · plus haut = mieux · unité : % of customers

- **Définition** : Share of customers (service connections) with a meter installed, prepaid or postpaid, as opposed to unmetered or flat-rate (forfait) supply, measured at year end. Where the utility discloses it, a stricter 'functional meter' variant counts only meters that are working and read.
- **Formule** : `COM_metering_coverage (%) = (customers_metered_count / customers_total_count) * 100. Strict variant: (customers_with_functional_meter_count / customers_total_count) * 100.`
- **Données brutes** : `customers_metered_count`, `customers_with_functional_meter_count`, `customers_total_count`
- **Sources typiques** : utility annual report (customer statistics); regulator annual report; World Bank / AfDB metering project documents (baseline and results frameworks); national metering programme reports (e.g. Nigeria's mass metering programmes)
- **Disponibilité attendue** : moyenne. Customer counts are widely published. The number of metered customers is published where metering is a policy issue (e.g. Nigeria, DRC, Congo, Cameroon), often in donor documents rather than annual reports. Functional-meter data are rare.
- **Pièges de comparaison** : (1) Customer vs connection vs meter counts: one meter may serve several households, and shared or collective meters are common in some countries. (2) Installed vs functional meters: defunct meters still counted. (3) Estimated billing on metered customers hides poor meter reading. (4) Coverage by count can be high while large energy volumes are unmetered, or the reverse; an energy-weighted variant is better but rarely available. (5) Informal or illegal connections are not in customers_total_count. Control for: urban/rural customer mix, recent mass-metering programmes.

### `COM_prepaid_share` : Part des clients prépayés
*Prepaid customer share* · palier **étendu** · contexte · contexte (non noté) · unité : % of customers

- **Définition** : Share of customers on prepaid metering (e.g. STS-standard token meters or smart prepaid meters) at year end. This is a structural indicator: it explains part of the differences in collection rates and receivable days, but a higher share is not automatically better. Prepaid suits low-voltage residential and small commercial customers, much less large industrial or MV customers.
- **Formule** : `COM_prepaid_share (%) = (customers_prepaid_count / customers_total_count) * 100. Optional energy variant: (energy_billed_prepaid_gwh / energy_billed_gwh) * 100.`
- **Données brutes** : `customers_prepaid_count`, `customers_total_count`, `energy_billed_prepaid_gwh`, `energy_billed_gwh`
- **Sources typiques** : utility annual report (customer statistics); regulator reports; donor project documents on prepaid metering rollout
- **Disponibilité attendue** : moyenne. Prepaid customer counts are often published by utilities where prepaid is widespread (e.g. Kenya, Zambia, Ghana, Senegal, South Africa). They are less often published, or are only partial, for utilities with limited rollout. The energy-weighted variant is rare.
- **Pièges de comparaison** : (1) Count share overstates prepaid's weight in revenue, because prepaid customers are mostly small residential users; prefer the energy share when available. (2) Prepaid does not remove non-technical losses (meter bypass, tampering, illegal vending) and may only shift them into billing efficiency. (3) Vending-based (tokens sold) vs consumption-based billing. (4) In municipal-distribution systems (South Africa) part of prepaid is run by municipalities, not the utility. (5) Public-sector prepaid policies (some governments mandate prepaid for state buildings) affect the public-sector comparison. Control for: customer mix, urbanisation.

### `COM_public_sector_receivables_share` : Part des créances publiques
*Public-sector receivables share* · palier **étendu** · noté · plus bas = mieux · unité : %

- **Définition** : Public-sector gross receivables as a share of total gross electricity trade receivables at year end; fallback when public-sector billing is not disclosed.
- **Formule** : `receivables_public_sector_gross_lcu_m / trade_receivables_electricity_gross_lcu_m * 100`
- **Données brutes** : `receivables_public_sector_gross_lcu_m`, `trade_receivables_electricity_gross_lcu_m`
- **Sources typiques** : audited financial statements (receivables note)
- **Disponibilité attendue** : moyenne. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

### `COM_receivables_days_public_sector` : Délai de recouvrement des créances sur le secteur public (administrations, entreprises publiques, collectivités)
*Public-sector receivables days* · palier **étendu** · noté · plus bas = mieux · unité : days

- **Définition** : Days of public-sector electricity sales outstanding in public-sector receivables at year end. Public sector covers central government ministries and agencies, state-owned enterprises (e.g. water utilities), and municipalities and local authorities, as defined in the utility's segment disclosure. Public-sector arrears are a recurring cause of utility liquidity crises in SSA and are often settled by offsets rather than cash. The private-customer counterpart can be derived as (total receivables - public receivables) / (total revenue - public revenue) * days_in_period when both splits are disclosed.
- **Formule** : `COM_receivables_days_public_sector (days) = (receivables_public_sector_gross_lcu_m / revenue_billed_public_sector_lcu_m) * days_in_period. Private counterpart: ((trade_receivables_electricity_gross_lcu_m - receivables_public_sector_gross_lcu_m) / (revenue_electricity_sales_lcu_m - revenue_billed_public_sector_lcu_m)) * days_in_period.`
- **Données brutes** : `receivables_public_sector_gross_lcu_m`, `revenue_billed_public_sector_lcu_m`, `trade_receivables_electricity_gross_lcu_m`, `revenue_electricity_sales_lcu_m`, `days_in_period`
- **Sources typiques** : audited financial statements (receivables note by customer category; related-party note); utility annual report (commercial section: 'créances sur l'Etat / administrations'); IMF program reports and public debt / SOE arrears audits; World Bank / AfDB project documents and arrears clearance plans; regulator reports
- **Disponibilité attendue** : faible. Many utilities disclose the public-sector receivables balance, often because it is large and contested. Fewer disclose public-sector billing for the same year, which is needed for the days computation. When only the balance is available, a fallback share KPI (public receivables / total receivables) can be stored, but it is not this KPI.
- **Pièges de comparaison** : (1) 'Public sector' definitions vary: some include SOEs and municipalities, others only central government. Store the definition used. (2) Government arrears are often offset against taxes, dividends, subsidies or tariff compensation owed to or by the state, and a single offset can cut the balance sharply. (3) Disputed or unrecognised amounts may sit off balance sheet. (4) Municipalities that resell electricity (e.g. South Africa) are wholesale customers, not end users. (5) Gross vs net of impairment, since some utilities do not impair state receivables. Control for: definition of public sector, presence of offset or arrears-clearance agreements in the year.

### `COM_revenue_per_customer` : Revenu moyen par client
*Average revenue per customer* · palier **étendu** · contexte · contexte (non noté) · unité : LCU per customer per year (USD for display)

- **Définition** : Annual electricity sales revenue per average retail customer. Reflects consumption intensity and tariff level together. Applicable only to entities selling to final customers, not to generation-only, transmission-only or single-buyer entities. The customer count is averaged over opening and closing balances.
- **Formule** : `COM_revenue_per_customer (LCU per customer per year) = (revenue_electricity_sales_lcu_m * 1000000) / ((customers_total_count[t-1] + customers_total_count[t]) / 2).`
- **Données brutes** : `revenue_electricity_sales_lcu_m`, `customers_total_count`, `fx_lcu_per_usd_avg`
- **Sources typiques** : audited financial statements; utility annual report (customer statistics); regulator reports
- **Disponibilité attendue** : élevée. Revenue and year-end customer counts are widely published. If the opening count is missing, the prior year's closing count can be used, so a two-year series makes the KPI computable.
- **Pièges de comparaison** : (1) Dominated by customer mix: a few large industrial or mining customers inflate the average, so a residential-only variant is preferable where segment data exist. (2) Fast electrification (many new low-consumption rural or prepaid customers) lowers the average while access improves, which is not a deterioration. (3) Customer definition: accounts, connections, or meters. (4) Same revenue perimeter and subsidy issues as COM_revenue_per_kwh_billed. (5) Exchange-rate effects. Control for: customer mix, electrification rate growth.

**Questions ouvertes (COM)**

- Denominator convention for the NET/COM bridge: confirm that NET's distribution loss KPI uses energy_injected_distribution_gwh, so that COM_billing_efficiency = 100 - NET distribution loss %. For integrated utilities that publish only total network losses on sent-out energy, decide whether to store a flagged variant or leave CRI blank.
- Collection-rate proxy: is a cash-flow-statement proxy (cash receipts from customers / VAT-adjusted revenue) acceptable when no reported collection rate exists? If so, which confidence level and flag should it carry?
- Non-cash settlements of public-sector arrears (offsets against taxes, dividends, subsidies, tariff compensation): should they count as collections? This needs one platform-wide rule, coordinated with FIN.
- Gross vs net receivables as the primary DSO basis: IFRS 9 ECL and SYSCOHADA provisioning practices differ, and some utilities do not impair state receivables at all.
- Treatment of tariff compensation and subsidies in revenue: should COM use sales revenue only, with subsidies kept in FIN, or carry both variants as separate KPIs?
- None of the reference definitions (ATC&C, collection efficiency, CRI naming) could be verified by fetch in this pass (fetch attempts returned 503/404). A follow-up lookup should target a regulator methodology document, e.g. NERC Nigeria ATC&C methodology or an ESMAP/World Bank utility performance framework, before marking any as verified.
- Should a public-sector receivables share KPI (balance-only, no billing split) be added as a fallback, given low availability of public-sector billing figures?
- Exchange-rate convention for USD display (annual average vs year-end) must be fixed platform-wide.

## OPS : Efficacité opérationnelle

*Labour productivity, absent from all drafted sections (critic gap). Placeholder dimension for opex/staff efficiency.*

### `OPS_customers_per_employee` : Clients par employé
*Customers per employee* · palier **noyau MVP** · noté · plus haut = mieux · unité : customers per employee

- **Définition** : Year-end customers divided by year-end permanent employees; contract/outsourced staff recorded separately. Standard labour-productivity benchmark.
- **Formule** : `customers_total_count / employees_permanent_count; companion: customers_total_count / (employees_permanent_count + employees_contract_count)`
- **Données brutes** : `customers_total_count`, `employees_permanent_count`, `employees_contract_count`
- **Sources typiques** : utility annual report (HR section); regulator annual report
- **Disponibilité attendue** : moyenne. Added at review stage; availability is a reviewer estimate, not yet checked against documents.
- **Pièges de comparaison** : To be completed during the document audit (step 1).
- **Revue** : Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.

## GOV : Gouvernance, transparence et régulation

*In Sub-Saharan Africa, how a utility is governed and how it reports drives everything else: whether tariffs get indexed, whether the state pays its arrears and tariff compensation, whether DFIs and IPPs extend credit, and whether the reported operating and financial figures can be trusted at all. On a source-first platform, this dimension also works as a meta-indicator of data quality: a disclaimer of opinion or a three-year publication lag tells the user how much weight to put on every other KPI for that utility-year. All KPIs below can be coded objectively from public documents (auditor's report, annual report, statutes and regulator decisions, ministry and SOE oversight reports, procurement portals). Each rubric scores only what can be seen in a citable document, so no subjective judgement is needed. Every rubric item scores 0 when no public evidence is found, and the evidence-search date is recorded. The goal is to avoid rewarding opacity while keeping 'not found' separate from 'confirmed absent' through a flag. Some KPIs are utility-year KPIs (publication lag, audit opinion, disclosure, board, procurement, performance contract). The regulatory framework KPIs are country-year KPIs attached to every utility in that jurisdiction.*

### `GOV_annual_reporting_disclosure_score` : Score de divulgation du rapport annuel
*Annual reporting disclosure score* · palier **noyau MVP** · noté · plus haut = mieux · unité : score 0-8 (or % of 8)

- **Définition** : Checklist score (0-8) measuring whether the utility publicly discloses, for the given financial year, the core information a benchmarking user needs. One point per item, scored only when evidence is available in a public document. (1) Annual report or activity report published. (2) Full audited financial statements published, including notes (not just summary figures). (3) Auditor's report published. (4) Operational statistics published: at least energy generated/purchased, energy billed and customer numbers. (5) Network loss figure or energy balance published. (6) Receivables/collection information published, including amounts owed by public-sector customers or the state. (7) Governance information published: board composition and management. (8) Related-party or state transactions disclosed: subsidies, tariff compensation and on-lent loans. The search date is recorded for each item.
- **Formule** : `GOV_annual_reporting_disclosure_score = disc_annual_report_published_flag + disc_full_audited_fs_with_notes_flag + disc_auditor_report_published_flag + disc_operational_stats_flag + disc_losses_or_energy_balance_flag + disc_receivables_public_sector_flag + disc_board_composition_flag + disc_state_transactions_flag (each 0/1). Optional normalised version: score / 8 x 100.`
- **Données brutes** : `disc_annual_report_published_flag`, `disc_full_audited_fs_with_notes_flag`, `disc_auditor_report_published_flag`, `disc_operational_stats_flag`, `disc_losses_or_energy_balance_flag`, `disc_receivables_public_sector_flag`, `disc_board_composition_flag`, `disc_state_transactions_flag`, `disclosure_search_date`
- **Sources typiques** : utility annual / sustainability / integrated reports; audited financial statements; utility website; regulator annual reports and statistical bulletins (for cross-checking only; points are given only for the utility's own disclosure)
- **Disponibilité attendue** : élevée. This KPI is produced by the platform's own document search, so it can be coded for every utility-year, including non-publishers, which score 0. The effort is in collecting documents systematically, not in finding the data.
- **Référence** (de mémoire, non vérifiée) : none (platform-defined checklist; conceptually aligned with utility transparency items in the World Bank RISE electricity access pillar, from memory)
- **Pièges de comparaison** : Listed utilities (e.g. on Nairobi, Lagos, Abidjan exchanges) face listing-disclosure rules that state-owned utilities do not. In unbundled structures, some items (energy balance, losses) may legitimately belong to a single buyer or TSO rather than the benchmarked entity; record 'not applicable' and normalise over the applicable items only. Documents may exist only in print, at the regulator, or in French, Portuguese or English. Score public online availability consistently, and archive the evidence because websites change. Do not let a later year's report back-fill disclosure for an earlier year unless it actually covers that year.
- **Revue** : Reference: Alignment with RISE indicators is unverified (rise.esmap.org returned 403); claim dropped until checked.

### `GOV_audit_opinion_code` : Type d'opinion d'audit (code ordinal)
*External audit opinion type (ordinal code)* · palier **noyau MVP** · noté · plus haut = mieux · unité : ordinal code 0-5

- **Définition** : Ordinal coding of the external auditor's opinion on the annual (statutory) financial statements, following the ISA 700/705/706/570 categories. Codes: 5 = unmodified opinion with no emphasis of matter and no material uncertainty related to going concern; 4 = unmodified opinion with an emphasis-of-matter paragraph and/or a material uncertainty related to going concern; 3 = qualified opinion ('except for'); 2 = adverse opinion; 1 = disclaimer of opinion; 0 = no audited statements publicly available (missing, as distinct from N/A). For OHADA/SYSCOHADA auditors (commissaires aux comptes): 'certification sans réserve' maps to 5 or 4 depending on 'observations'; 'certification avec réserve(s)' maps to 3; 'refus de certifier' maps to 2 when the basis is disagreement or material misstatement and to 1 when it is impossibility to obtain evidence (limitation of scope). The number of distinct qualification or disclaimer bases is captured as a companion field.
- **Formule** : `GOV_audit_opinion_code = lookup(audit_opinion_category, {unmodified_clean:5, unmodified_with_emphasis_or_going_concern:4, qualified:3, adverse:2, disclaimer:1}); not published / not available = NULL (separate state, not ranked; non-publication is captured by GOV_audited_fs_publication_lag_months). unmodified_with_emphasis_or_going_concern applies if emphasis_of_matter_flag = 1 OR going_concern_material_uncertainty_flag = 1.`
- **Données brutes** : `audit_opinion_category`, `emphasis_of_matter_flag`, `going_concern_material_uncertainty_flag`, `audit_modification_basis_count`, `auditor_name`, `auditor_type_code`, `auditing_standards_framework`, `accounting_framework_code`
- **Sources typiques** : independent auditor's report / rapport général du commissaire aux comptes in the audited financial statements; Auditor-General / Cour des comptes reports on state-owned enterprises; annual reports; DFI project appraisal documents (financial management assessments)
- **Disponibilité attendue** : moyenne. Where statements are published, the auditor's report is almost always attached, so coding is straightforward and objective. Availability is limited by non-publication among several state-owned utilities in francophone and Central Africa. In some cases only the opinion is reported second-hand in DFI documents, which the platform should flag with lower confidence.
- **Référence** (vérifiée (URL consultée)) : IAASB ISA 705 (Revised) Modifications to the Opinion in the Independent Auditor's Report (qualified / adverse / disclaimer); ISA 706 (emphasis of matter) and ISA 570 (going concern) used for code 4 <https://www.irba.co.za/upload/ISA-705-Revised.pdf>
- **Pièges de comparaison** : Qualifications at African utilities often reflect recurring structural issues (unreconciled government receivables and payables, fixed asset registers, tariff-compensation subsidy receivables, IPP take-or-pay provisions, pension obligations) rather than one-off problems. Read the basis text, not only the code. Going-concern material uncertainty is common for utilities that depend on state support and is not equivalent to a qualification. Auditor type matters (Big Four firm vs local firm vs supreme audit institution), as do national auditing standards that are not fully ISA-converged. The SYSCOHADA 'refus de certifier' must be split into adverse vs disclaimer using the stated basis. Consolidated vs company-only statements may carry different opinions; code the statements of the entity being benchmarked and record which one.
- **Revue** : Review fix: code 0 removed from the ordinal scale. The mapping of SYSCOHADA/OHADA "refus de certifier" to adverse vs disclaimer is a platform interpretation to validate with an OHADA audit specialist.

### `GOV_audited_fs_publication_lag_months` : Délai de publication des états financiers audités
*Audited financial statements publication lag* · palier **noyau MVP** · noté · plus bas = mieux · unité : months

- **Définition** : Number of months between the end of the financial year and the earliest date on which the audited financial statements for that year are verifiably available to the public. Public availability means posted on the utility, regulator, ministry, supreme audit institution or stock exchange website, or included in a published annual report or gazette. The audit report signing date is captured separately as a secondary measure. It is used as a lower bound if the public release date cannot be established, and a flag records this. If the statements are still not public at the platform's observation cut-off date, the value is right-censored: lag = months from year-end to cut-off, with flag not_published_at_cutoff = 1.
- **Formule** : `IF audited_fs_public_release_date known: GOV_audited_fs_publication_lag_months = months_between(fiscal_year_end_date, audited_fs_public_release_date). ELSE IF audited_fs_published_flag = 0: value = months_between(fiscal_year_end_date, observation_cutoff_date) with not_published_at_cutoff_flag = 1. Secondary: audit_signing_lag_months = months_between(fiscal_year_end_date, audit_report_signing_date). Months are computed as days/30.44, rounded to one decimal.`
- **Données brutes** : `fiscal_year_end_date`, `audit_report_signing_date`, `audited_fs_public_release_date`, `audited_fs_published_flag`, `observation_cutoff_date`, `release_date_evidence_type`
- **Sources typiques** : audited financial statements (auditor's report date); utility annual report; utility website publication metadata / archive snapshots; stock exchange or bond-listing disclosures (e.g. listed utilities, Eurobond issuers); supreme audit institution reports (Auditor-General / Cour des comptes); regulator annual reports reproducing utility accounts
- **Disponibilité attendue** : moyenne. The audit report signing date is usually printed in the statements whenever they are published, so it is highly available for utilities that publish. The true public release date is harder to pin down: PDFs often carry no posting date, and archive snapshots or press releases may be needed. Many state-owned utilities, especially in Central Africa, do not publish their statements at all. For them the KPI is still codable as right-censored, which is informative in itself.
- **Référence** (aucune) : none (platform-defined; dates per ISA 700 auditor's report date convention)
- **Pièges de comparaison** : Legal deadlines and approval cycles differ. OHADA/SYSCOHADA companies have accounts approved by the general assembly or board, and state-owned utilities may need ministerial or supervisory sign-off before release. Anglophone utilities may be audited by the Auditor-General with statutory tabling in Parliament before publication. Fiscal year-ends differ (calendar year vs 30 June vs 31 March for Eskom), so compare lags, never calendar dates. A late or missing release date may mean the document exists but was never posted online; keep the evidence type (signing date proxy vs observed posting) and never mix the two silently. Restated or re-issued statements: use the first publication of the audited version.

### `GOV_regulatory_framework_score` : Score du cadre de régulation et de tarification
*Regulatory and tariff-setting framework score* · palier **noyau MVP** · noté · plus haut = mieux · unité : score 0-7

- **Définition** : Country-year checklist score (0-7) describing the formal regulatory framework that applies to the utility. One point per item, each backed by a cited legal text, regulator decision or publication. (1) A sector regulator exists, established by law as a legal entity separate from the line ministry and the utility. (2) The regulator has legal authority to approve or set retail tariffs, not merely advise the minister. (3) A tariff methodology, formula or tariff code is published. (4) Tariff decisions, including current tariff schedules, are published by the regulator or in an official gazette. (5) The framework provides for periodic or multi-year tariff reviews and/or automatic indexation (fuel, FX, inflation). (6) Tariff decisions involve a public consultation or hearing step documented in published material. (7) The regulator published an annual report or activity report covering the year. A companion flag records whether a tariff adjustment provided for by the framework was actually applied in the year.
- **Formule** : `GOV_regulatory_framework_score = reg_separate_regulator_flag + reg_tariff_approval_authority_flag + reg_tariff_methodology_published_flag + reg_tariff_decisions_published_flag + reg_periodic_review_or_indexation_flag + reg_public_consultation_flag + reg_regulator_annual_report_flag (each 0/1). Companion: reg_scheduled_tariff_adjustment_applied_flag (1 = an adjustment due under the methodology was applied in the year; 0 = due but not applied/frozen; NA = none due).`
- **Données brutes** : `country_code`, `reg_separate_regulator_flag`, `reg_tariff_approval_authority_flag`, `reg_tariff_methodology_published_flag`, `reg_tariff_decisions_published_flag`, `reg_periodic_review_or_indexation_flag`, `reg_public_consultation_flag`, `reg_regulator_annual_report_flag`, `reg_scheduled_tariff_adjustment_applied_flag`, `regulator_name`
- **Sources typiques** : electricity act / code de l'électricité and regulator founding law; regulator websites, tariff decisions, tariff orders, official gazettes; regulator annual reports; World Bank RISE country scorecards (cross-check); AFUR / regional regulator association publications (e.g. ERERA for ECOWAS, RERA for SADC); DFI programme documents describing tariff reforms
- **Disponibilité attendue** : moyenne. Laws and regulator websites are mostly public, and the 10 MVP countries all have identifiable sector laws. The weakest items are the consultation step and the 'adjustment applied' companion, which require reading tariff orders and press releases year by year. [Review downgrade from high: The consultation item, the 'regulator annual report for the year' item and the companion 'adjustment applied' flag require year-by-year reading of tariff orders, and several regulators' archives are incomplete online. Suggested: medium.]
- **Référence** (de mémoire, non vérifiée) : none (platform-defined; overlaps with regulatory indicators in World Bank/ESMAP RISE and the AfDB Electricity Regulatory Index, from memory)
- **Pièges de comparaison** : De jure is not de facto. A country can score high while tariffs are frozen politically, and the 'adjustment applied' companion and the FIN tariff-shortfall KPIs must be read alongside the score. Some countries share a regulator across sectors or have sub-national regulators (e.g. Nigeria state regulators after the 2023 Electricity Act), so record which regulator governs the benchmarked utility. Regulators may set tariffs for distribution companies while generation tariffs are set by bilateral PPAs with a single buyer. Tariff compensation by the state (subsidy paid to the utility) is not captured here; see FIN dimension. Score changes mid-year: code status at fiscal year-end.
- **Revue** : Reference: AfDB Electricity Regulatory Index and RISE overlaps cited from memory; indicator structure not verified.

### `GOV_board_independence_ratio` : Taux d'administrateurs indépendants
*Board independence ratio* · palier **étendu** · noté · plus haut = mieux · unité : %

- **Définition** : Share of seats on the utility's board of directors (conseil d'administration) held by directors who are explicitly designated as independent in a public document, at financial year-end. Coding rule: a director counts as independent only if the annual report, governance statement or statutes label them independent (or 'administrateur indépendant'). Representatives of ministries, the state shareholder agency, the utility's management, staff representatives and strategic shareholders are coded non-independent even if described as 'non-executive'. Also captured: whether the chair is independent and whether the CEO and chair roles are separated.
- **Formule** : `GOV_board_independence_ratio = board_independent_directors_count / board_total_seats_filled_count x 100. Companion flags: board_chair_independent_flag, ceo_chair_separated_flag.`
- **Données brutes** : `board_total_seats_filled_count`, `board_independent_directors_count`, `board_state_representatives_count`, `board_executive_directors_count`, `board_chair_independent_flag`, `ceo_chair_separated_flag`, `board_composition_reference_date`
- **Sources typiques** : annual / integrated report corporate governance section; statutes / articles of association, decree establishing the SOE; stock exchange filings (listed utilities); SOE oversight agency or state portfolio reports
- **Disponibilité attendue** : faible. Listed or bond-issuing utilities (e.g. Kenya Power, Eskom, CIE) usually publish board composition with independence labels. Many state-owned utilities publish only names, or nothing, and their boards are by decree made up of ministry representatives. Ratios will therefore often be 0, or missing because of non-disclosure; the two cases must be distinguished.
- **Référence** (de mémoire, non vérifiée) : none (platform rule; independence concept as in national corporate governance codes such as King IV in South Africa, from memory)
- **Pièges de comparaison** : The concept of independence differs between national codes, and many SOE statutes do not use the term at all. The strict 'explicitly labelled' rule favours comparability over completeness. Boards dissolved or suspended (e.g. under state administration or a management contract) should be coded with a flag rather than as 0. Utilities under a private concession or management contract (e.g. CIE in Cote d'Ivoire, past arrangements elsewhere) have a different principal-agent structure. Board size changes during the year: use the year-end composition.

### `GOV_performance_contract_score` : Score du contrat de performance avec l'État
*State performance contract score* · palier **étendu** · noté · plus haut = mieux · unité : score 0-5

- **Définition** : Checklist score (0-5) for the formal performance agreement between the utility and the state (contrat de performance / contrat-plan / performance contract / shareholder compact), in force during the year. (1) A performance contract or equivalent is in force covering the year, evidenced by a public reference. (2) It contains quantified utility targets, such as losses, collection and supply quality. (3) It contains reciprocal state obligations, such as tariff compensation, settlement of public-sector bills and arrears, or investment funding. (4) The text or a substantive summary is publicly available. (5) A monitoring or evaluation report on achievement for the year is publicly available, from the utility, the ministry, the SOE oversight body or a DFI.
- **Formule** : `GOV_performance_contract_score = pc_in_force_flag + pc_quantified_utility_targets_flag + pc_state_reciprocal_obligations_flag + pc_text_public_flag + pc_annual_evaluation_public_flag (each 0/1; items 2-5 can only be 1 if item 1 = 1).`
- **Données brutes** : `pc_in_force_flag`, `pc_quantified_utility_targets_flag`, `pc_state_reciprocal_obligations_flag`, `pc_text_public_flag`, `pc_annual_evaluation_public_flag`, `pc_document_type`, `pc_start_year`, `pc_end_year`
- **Sources typiques** : performance contract / contrat-plan texts (ministry or SOE oversight portals); Kenya-style SOE performance contracting evaluation reports; utility annual reports (sections on state relations); IMF programme documents and World Bank / AfDB project appraisal documents (often summarise contract targets and arrears clearing)
- **Disponibilité attendue** : faible. Several francophone and anglophone countries use performance contracts, but texts are rarely published. Evidence often comes second-hand from IMF or DFI documents, so item 1 is often codable while items 4-5 are mostly 0. The KPI is useful as a structural descriptor, not yet as a robust ranking metric.
- **Référence** (aucune) : none (platform-defined)
- **Pièges de comparaison** : Equivalent instruments carry different names and legal force: contract, compact, shareholder letter of expectations, or regulatory license conditions. In privatised distribution companies (e.g. Nigerian DisCos) the relevant instrument is the licence or the performance agreement with the asset-holding agency, not a state contract. Concession or affermage arrangements need their own coding. A high score does not mean the state honoured its obligations; cross-check against FIN government arrears and tariff-compensation KPIs.

### `GOV_procurement_transparency_score` : Score de transparence des achats et contrats
*Procurement and contract transparency score* · palier **étendu** · noté · plus haut = mieux · unité : score 0-6 (companion: %)

- **Définition** : Checklist score (0-6) for public transparency of the utility's procurement and major power-purchase contracting during the year. (1) The procurement rules or policy applicable to the utility are published, whether national public procurement law or the utility's own manual. (2) An annual procurement plan is published. (3) Tender notices are published on a public portal or the utility website. (4) Contract award notices are published, including supplier name and value. (5) New IPP or emergency-power contracts (PPAs, rental or diesel emergency power agreements) signed in the year are disclosed at least in summary: counterparty, capacity, tenor and procurement method. Score 1 if none were signed and this is verifiable. (6) PPAs were procured competitively (auction or tender), or this was disclosed as direct negotiation with a published justification.
- **Formule** : `GOV_procurement_transparency_score = proc_rules_published_flag + proc_annual_plan_published_flag + proc_tender_notices_published_flag + proc_award_notices_published_flag + proc_ppa_emergency_contracts_disclosed_flag + proc_ppa_competitive_or_justified_flag (each 0/1). Optional extended companion: proc_competitive_award_share_pct = contracts_awarded_open_competition_value_lcu_m / contracts_awarded_total_value_lcu_m x 100, computed only where both are disclosed.`
- **Données brutes** : `proc_rules_published_flag`, `proc_annual_plan_published_flag`, `proc_tender_notices_published_flag`, `proc_award_notices_published_flag`, `proc_ppa_emergency_contracts_disclosed_flag`, `proc_ppa_competitive_or_justified_flag`, `contracts_awarded_open_competition_value_lcu_m`, `contracts_awarded_total_value_lcu_m`, `procurement_evidence_search_date`
- **Sources typiques** : national e-procurement portals and public procurement authority reports; utility website tender pages; regulator PPA approval decisions and IPP registers; Auditor-General / Cour des comptes reports on procurement; DFI procurement plans and contract award notices for donor-funded projects
- **Disponibilité attendue** : moyenne. Items 1 and 3 are often observable, and donor-financed procurement is systematically published by DFIs. Annual plans, award values for own-funded procurement and emergency-power contracts are frequently undisclosed. The value-share companion will rarely be computable.
- **Référence** (de mémoire, non vérifiée) : none (platform-defined; contract disclosure concept aligned with open contracting practice, from memory)
- **Pièges de comparaison** : Donor-financed procurement follows DFI rules and is published on DFI portals. Do not credit the utility's own transparency for it unless it publishes the information itself, and record the source. In single-buyer models, PPAs may be signed by the state, a single buyer or an asset-holding company rather than the benchmarked utility; attribute them to the contracting entity. Emergency or rental power is often procured under urgency exemptions, which item 6 handles via 'justified'. National procurement laws may exempt SOEs or certain contract types.

### `GOV_regulatory_reporting_compliance_code` : Conformité aux obligations de reporting réglementaire
*Regulatory reporting compliance* · palier **étendu** · noté · plus haut = mieux · unité : ordinal code 0-3

- **Définition** : Ordinal code (0-3) for whether the regulator publicly reports on the utility's compliance with its regulatory reporting or licence-performance obligations for the year. 3 = regulator publishes a utility-specific performance or compliance report or dataset for the year (e.g. technical/commercial performance tables per licensee). 2 = regulator publishes aggregate sector statistics that include the utility's figures, but no compliance assessment. 1 = regulator mentions the utility's reporting or performance only qualitatively, or notes non-submission of data. 0 = no regulator publication covering the utility for the year. A companion flag records whether the regulator documented sanctions or penalties against the utility for the year.
- **Formule** : `GOV_regulatory_reporting_compliance_code = lookup(regulator_utility_reporting_level, {utility_specific_compliance_report:3, aggregate_stats_including_utility:2, qualitative_mention_only:1, none:0}). Companion: regulator_sanction_documented_flag (0/1).`
- **Données brutes** : `regulator_utility_reporting_level`, `regulator_sanction_documented_flag`, `regulator_publication_year_covered`
- **Sources typiques** : regulator annual reports and quarterly performance reports per licensee; regulator statistical bulletins; regulator enforcement / sanction decisions
- **Disponibilité attendue** : moyenne. Some regulators in the MVP set publish licensee-level performance tables; others publish only sector aggregates or nothing recent. The KPI is coded entirely from regulator outputs, which are easier to collect than utility-internal data.
- **Référence** (aucune) : none (platform-defined)
- **Pièges de comparaison** : This KPI partly measures the regulator's transparency rather than the utility's. Interpret it at country level together with GOV_regulatory_framework_score. Vertically integrated utilities without competitors may be covered only in aggregate by default. Publication delays mean the year covered must be recorded explicitly, not the publication year.

**Questions ouvertes (GOV)**

- Observation cut-off date for right-censoring GOV_audited_fs_publication_lag_months: should it be a fixed platform snapshot date per release, or the date of each extraction run?
- Should the 'not found' score of 0 in checklist KPIs be shown separately from 'verified absent' in the UI, so that utilities are not penalised for documents the platform failed to locate (e.g. print-only or French-only reports)?
- The SYSCOHADA 'refus de certifier' must be mapped to adverse or disclaimer from its stated basis. Should a reviewer with OHADA audit experience validate this mapping rule?
- For unbundled or single-buyer structures (e.g. Ghana ECG/GRIDCo/VRA, Nigeria DisCos/TCN/NBET, Kenya KPLC/KenGen/KETRACO), are country-level governance KPIs attached to every entity, and how are 'not applicable' items normalised in the disclosure score?
- The World Bank/ESMAP RISE and AfDB Electricity Regulatory Index references could not be verified by fetch (rise.esmap.org returned 403). Before citing them as cross-check sources, confirm the current indicator structure and the latest edition covering 2019-2025.
- Should a composite GOV index be published, or only the separate coded components? A composite adds weighting choices that are hard to justify objectively.
- Should Big Four vs local firm vs supreme audit institution auditor type be a reportable breakdown or only a context field, given sensitivities around comparing audit quality?

## INV : Investissement et efficacité du capital

*Sub-Saharan African utilities have large backlogs in generation, transmission, distribution and access, but limited ability to fund them on their own. This dimension measures how much a utility invests, how well it delivers that investment against plan, whether its assets are being renewed or left to run down, how much of the investment depends on donors or the state, and roughly how much each new connection costs. Measuring this from public data is hard. Capex often sits partly off the utility's books: assets are financed by the State, donors or rural electrification agencies and then transferred in, or donor projects are run by separate project implementation units (PIUs). Under SYSCOHADA, cash-flow tables (TAFIRE, or the newer 'tableau des flux de tresorerie') and fixed-asset notes are laid out differently from IFRS. Capex budgets and implementation rates usually appear only in regulator reports, performance contracts (contrats de performance / contrats-plans) or donor project documents (World Bank ISRs/ICRs, AfDB PCRs), not in the financial statements. The KPIs below therefore lean on cash-flow-statement and PP&E-note items, which are audited and common to both frameworks. Execution and commissioning KPIs are extended, opportunistic metrics.*

### `INV_capex_to_depreciation` : Ratio de renouvellement des actifs (Capex / dotations aux amortissements)
*Asset renewal ratio (capex to depreciation)* · palier **noyau MVP** · contexte · contexte (non noté) · unité : ratio (x)

- **Définition** : Gross capex, divided by the depreciation and amortisation charge on PP&E and intangibles for the same year. A ratio persistently below 1 suggests the asset base is not being renewed and is wearing out. The ratio does not separate renewal capex from expansion capex.
- **Formule** : `capex_cash_lcu_m / depreciation_amortisation_lcu_m ; variant_accrual = ppe_intangible_additions_lcu_m / depreciation_amortisation_lcu_m`
- **Données brutes** : `capex_cash_lcu_m`, `ppe_intangible_additions_lcu_m`, `depreciation_amortisation_lcu_m`
- **Sources typiques** : audited financial statements (income statement, PP&E note, cash flow statement); SYSCOHADA etats financiers (dotations aux amortissements)
- **Disponibilité attendue** : moyenne. Depreciation and capex are both standard lines in IFRS and SYSCOHADA statements. [Review downgrade from high: Same publication and off-book issues. Depreciation on grant-funded assets is often neutralised. Suggested: medium.]
- **Référence** (vérifiée (URL consultée)) : IFRS IAS 16 (depreciation of PP&E); IAS 7 for cash capex <https://www.ifrs.org/issued-standards/list-of-standards/ias-16-property-plant-and-equipment/>
- **Pièges de comparaison** : Depreciation depends on accounting choices. Revaluation models (e.g. some anglophone utilities revalue network assets) inflate depreciation compared with historical-cost SYSCOHADA books. Useful-life assumptions differ, and so does the treatment of donor-funded or State-transferred assets: they may be booked with an offsetting deferred grant, so depreciation is neutralised in profit and loss but still appears gross. Fully depreciated but still operating assets (common in old hydro and networks) shrink depreciation and overstate the ratio. In high-inflation economies, historical-cost depreciation understates the true replacement need. Read alongside INV_asset_base_growth.

### `INV_asset_base_growth` : Croissance de la base d'actifs (immobilisations corporelles nettes)
*Asset base growth (net PP&E)* · palier **étendu** · contexte · contexte (non noté) · unité : % per year

- **Définition** : Year-on-year percentage change in the net carrying amount of property, plant and equipment, including construction work in progress (CWIP) and electricity-related intangible assets. Revaluation surpluses and impairments are flagged, and where disclosed a variant excluding revaluations is computed.
- **Formule** : `(net_ppe_end_lcu_m - net_ppe_start_lcu_m) / net_ppe_start_lcu_m * 100 ; variant_ex_reval = (net_ppe_end_lcu_m - ppe_revaluation_lcu_m + ppe_impairment_lcu_m - net_ppe_start_lcu_m) / net_ppe_start_lcu_m * 100`
- **Données brutes** : `net_ppe_start_lcu_m`, `net_ppe_end_lcu_m`, `ppe_revaluation_lcu_m`, `ppe_impairment_lcu_m`, `cwip_end_lcu_m`
- **Sources typiques** : audited financial statements (balance sheet, PP&E movement note); annual report
- **Disponibilité attendue** : élevée. Net PP&E appears on every balance sheet, and the movement note usually separates additions, depreciation, revaluations and transfers.
- **Référence** (vérifiée (URL consultée)) : IFRS IAS 16 (carrying amount, revaluation model) <https://www.ifrs.org/issued-standards/list-of-standards/ias-16-property-plant-and-equipment/>
- **Pièges de comparaison** : Revaluations can create large jumps that do not reflect any investment. Transfers in of State or donor assets, restructuring or unbundling (assets moved to a separate transmission company or asset-holding company) and IFRS first-time adoption also create jumps. Local-currency inflation and devaluation (especially for imported equipment in Nigeria, Ghana, Zambia, DRC) push nominal growth up. Use real or constant-currency growth for cross-country views.

### `INV_capex_execution_rate` : Taux d'execution du budget d'investissement
*Capex budget execution rate* · palier **étendu** · noté · plage cible · unité : %

- **Définition** : Actual capital expenditure realised in the year, divided by the capex budgeted or planned for the same year in the approved budget, business plan, regulator-approved investment plan or performance contract. The plan source must be recorded, because each one implies a different benchmark.
- **Formule** : `capex_cash_lcu_m / capex_budget_lcu_m * 100`
- **Données brutes** : `capex_cash_lcu_m`, `capex_budget_lcu_m`, `capex_budget_source_type`
- **Sources typiques** : regulator annual report / tariff review documents; performance contract (contrat de performance / contrat-plan) monitoring reports; annual report (management discussion); ministry budget execution reports; donor project documents (disbursement vs plan)
- **Disponibilité attendue** : faible. Budgets are rarely disclosed alongside actuals in audited statements. They appear in some regulator tariff reviews (e.g. multi-year tariff frameworks), in some state-owned enterprise performance-contract reviews, and occasionally in annual reports.
- **Pièges de comparaison** : Budgets may be aspirational, set on a ministry or donor wish list, or revised mid-year, so a high execution rate can just reflect a low budget. Actual and budget may differ in scope (cash versus commitments, utility-funded only versus including donor or State funding). Both under-execution, which signals capacity or procurement constraints, and large over-execution, which signals emergency spending such as rental or diesel power, call for comment. That is why the direction is target_range, with no numeric threshold.

### `INV_capex_per_new_connection` : Capex de distribution par nouveau raccordement
*Distribution capex per new connection* · palier **étendu** · contexte · contexte (non noté) · unité : LCU per connection (convert to USD at average annual rate for cross-country views)

- **Définition** : Distribution and access capex, including last-mile and metering capex where it is disclosed separately, divided by the net number of new customer connections made during the year. This is a rough unit-cost indicator, not a full engineering cost per connection. Where only total capex is available, the variant that uses total capex must be flagged as such.
- **Formule** : `capex_distribution_access_lcu_m * 1e6 / new_connections_count (gross connections only; suppressed when new_connections_count <= 0). Label: distribution capex per gross connection (upper bound).`
- **Données brutes** : `capex_distribution_access_lcu_m`, `new_connections_count`, `fx_lcu_per_usd_avg`
- **Sources typiques** : annual report (operational review); regulator annual report; donor project documents (World Bank ISR/ICR, AfDB PCR) for electrification programs; rural electrification agency reports
- **Disponibilité attendue** : faible. Customer counts are widely published. Capex broken down by segment is rare, and many connections are financed and built by rural electrification agencies or donor programmes (sometimes with subsidised or free connection fees), outside the utility's capex.
- **Pièges de comparaison** : The numerator and denominator often come from different perimeters: connections may be funded by agencies or donors while the utility reports them. Densification (low cost per connection) is mixed with grid extension (high cost). The net customer change is understated where the customer database is being cleaned up, and where post-paid customers are migrated to prepaid meters and re-registered. Capitalised connection fees paid by customers are sometimes netted against capex. Exchange-rate swings (e.g. Nigeria, Ghana, Zambia) distort USD comparisons. Use only as context, never as a ranking.
- **Revue** : Review fix: net customer change removed as denominator (can be zero or negative after database clean-ups).

### `INV_capex_to_revenue` : Intensite d'investissement (Capex / chiffre d'affaires)
*Capex intensity (capex to revenue)* · palier **étendu** · contexte · contexte (non noté) · unité : %

- **Définition** : Gross capital expenditure on property, plant and equipment and intangible assets during the year, divided by operating revenue from electricity sales and related services. The default basis is cash capex from the cash flow statement (investing activities). The accrual basis (additions to PP&E from the fixed-asset note) is stored as a variant. Revenue excludes government subsidies and tariff compensation, which are stored separately, so that the ratio is not distorted by how a subsidy happens to be booked.
- **Formule** : `capex_cash_lcu_m / (revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m) * 100 ; variant_accrual = ppe_intangible_additions_lcu_m / (revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m) * 100`
- **Données brutes** : `capex_cash_lcu_m`, `ppe_intangible_additions_lcu_m`, `revenue_electricity_sales_lcu_m`, `other_operating_revenue_lcu_m`, `tariff_compensation_revenue_lcu_m`
- **Sources typiques** : audited financial statements (cash flow statement, PP&E/intangibles note); annual report; SYSCOHADA TAFIRE / tableau des flux de tresorerie; regulator annual report
- **Disponibilité attendue** : moyenne. Most audited statements include a cash flow statement and a fixed-asset movement table, and both IFRS and SYSCOHADA report investment outflows. Gaps arise where statements are published late or not at all (several state-owned utilities), and where large assets are financed and held by the State, agencies or PIUs and never pass through the utility's cash flow. [Review downgrade from high: SYSCOHADA cash-flow tables published in summary form often lack a clear split of investing flows, and off-book State/PIU capex is common. Suggested: medium.]
- **Référence** (vérifiée (URL consultée)) : IFRS IAS 7 (investing activities: acquisition of long-term assets); IAS 16 for PP&E additions <https://www.ifrs.org/issued-standards/list-of-standards/ias-7-statement-of-cash-flows/>
- **Pièges de comparaison** : Comparisons are distorted by: off-balance-sheet investment (State, rural electrification agency or donor PIU assets transferred later at a lump-sum value, or never transferred); concession or affermage models where the asset owner (State or asset-holding company) invests and the operator does not; unbundled versus integrated structure (a transmission company's capex/revenue differs structurally from a distribution company's); tariff level, since a low regulated tariff raises the ratio; one-off mega-projects such as hydro dams that make the ratio lumpy (use a 3-year rolling average); capex cash outflows recorded net of capital grants in some statements; and lease or IPP arrangements, which move generation capex off the utility's books.

### `INV_commissioning_delay` : Retard de mise en service des projets majeurs
*Commissioning delay of major projects* · palier **étendu** · noté · plus bas = mieux · unité : months

- **Définition** : For each major capital project disclosed (generation plant, transmission line or substation, large distribution programme), the delay in months between the commissioning date planned at approval or financial close and the actual (or latest forecast) commercial operation date. Aggregated per utility-year as the median delay across disclosed projects, with the project count.
- **Formule** : `per project: delay_months = months_between(commissioning_date_planned_original, commissioning_date_actual_or_forecast) ; utility-year: median(delay_months) over projects_disclosed_count`
- **Données brutes** : `project_id`, `commissioning_date_planned_original`, `commissioning_date_actual_or_forecast`, `project_capacity_mw`, `project_cost_planned_lcu_m`, `project_cost_actual_or_forecast_lcu_m`, `projects_disclosed_count`
- **Sources typiques** : donor project documents (World Bank ISR/ICR, AfDB PAR/PCR); annual report (projects review); regulator reports; ministry of energy statistics / sector reviews; IPP/PPP procurement announcements
- **Disponibilité attendue** : faible. Original planned dates are best documented in donor appraisal and completion reports. Utility reports usually state only current target dates, and selective disclosure is common.
- **Pièges de comparaison** : The sample of projects is self-selected and small, and donor projects are over-represented. Baseline dates may be re-baselined after restructuring. Causes differ widely (financing close, land acquisition, conflict, contractor default, COVID-19 in 2020-2021), and IPP projects are not utility capex. Avoid ranking utilities on this metric; present it as case-level evidence, optionally with a cost overrun ratio = project_cost_actual_or_forecast_lcu_m / project_cost_planned_lcu_m.

### `INV_cwip_to_gross_ppe` : Part des immobilisations en cours
*Construction work in progress share of gross PP&E* · palier **étendu** · noté · plus bas = mieux · unité : %

- **Définition** : Construction work in progress (assets under construction / immobilisations en cours) at year end, divided by the gross carrying amount of PP&E at year end. A high or rising share suggests capital is tied up in projects that have not yet been commissioned. It is a proxy signal for commissioning delays.
- **Formule** : `cwip_end_lcu_m / gross_ppe_incl_cwip_end_lcu_m * 100`
- **Données brutes** : `cwip_end_lcu_m`, `gross_ppe_incl_cwip_end_lcu_m`
- **Sources typiques** : audited financial statements (PP&E movement note); SYSCOHADA etats financiers (immobilisations en cours)
- **Disponibilité attendue** : moyenne. CWIP is a standard line in PP&E notes under both IFRS and SYSCOHADA. [Review downgrade from high: It needs the full PP&E movement note with gross values, which is often missing from published summary statements. Suggested: medium.]
- **Référence** (vérifiée (URL consultée)) : IFRS IAS 16 (assets under construction as a PP&E class, not depreciated until available for use) <https://www.ifrs.org/issued-standards/list-of-standards/ias-16-property-plant-and-equipment/>
- **Pièges de comparaison** : A large greenfield project such as a hydro plant legitimately raises CWIP for years, so lower is not always better at the level of a single project. Some utilities are slow to capitalise completed assets (an accounting backlog rather than a physical delay). Stalled or abandoned projects may stay in CWIP without being impaired. Revaluations of in-service assets change the denominator. Interpret alongside INV_commissioning_delay where it is available.

### `INV_external_financing_share` : Part du financement concessionnel / bailleurs dans l'investissement
*Donor / concessional and State financing share of capex* · palier **étendu** · contexte · contexte (non noté) · unité : %

- **Définition** : Share of the year's capex financed by donor or concessional loans and grants (multilateral development banks, bilateral agencies, climate funds) and by State capital transfers or on-lent funds, as opposed to internally generated cash and commercial debt. The share is reported separately for donor/concessional and State funding where possible.
- **Formule** : `(capex_funded_donor_concessional_lcu_m + capex_funded_state_lcu_m) / capex_total_all_sources_lcu_m * 100 ; sub_donor = capex_funded_donor_concessional_lcu_m / capex_total_all_sources_lcu_m * 100`
- **Données brutes** : `capex_funded_donor_concessional_lcu_m`, `capex_funded_state_lcu_m`, `capex_funded_internal_lcu_m`, `capex_funded_commercial_debt_lcu_m`, `capex_total_all_sources_lcu_m`, `capital_grants_received_lcu_m`, `concessional_loan_drawdowns_lcu_m`
- **Sources typiques** : annual report (financing of investment programme); audited financial statements (notes on borrowings, capital grants / subventions d'investissement, on-lent loans); donor project documents (disbursement data); ministry of finance / debt office reports; regulator reports
- **Disponibilité attendue** : faible. An explicit funding-source breakdown is uncommon. A proxy can be built from cash-flow and notes data, using capital grants received and drawdowns of concessional or on-lent loans relative to capex, but loans are not always labelled as concessional. Donor documents give project-level disbursements, which often bypass the utility's accounts. [Review downgrade from medium: An explicit split of funding sources is rare and the proxy method is weak. 'Medium' is optimistic. Suggested: low.]
- **Référence** (de mémoire, non vérifiée) : OECD DAC concept of concessional finance (for labelling loans), applied loosely
- **Pièges de comparaison** : Donor-funded assets built by PIUs or rural electrification agencies may never appear in utility capex, so the measured share understates dependence. Loans on-lent by the Ministry of Finance hide their concessional origin. Capital grants are booked as deferred income (IFRS) or as subventions d'investissement in equity (SYSCOHADA), which changes where they show up. Proxy and explicit values are not directly comparable, so record the method used (explicit versus proxy).
- **Revue** : Capital transfers count only in INV; operating transfers only in FIN_government_transfer_dependency (no double counting in composites).

**Questions ouvertes (INV)**

- Perimeter: should the platform try to rebuild sector-wide capex (utility + State + rural electrification agency + donor PIUs) for each country, or strictly measure utility-reported capex and flag off-book investment qualitatively?
- Default capex basis: cash capex (IAS 7 / TAFIRE investing outflows) or accrual additions from the PP&E note. These diverge when there are large unpaid contractor balances or assets transferred in kind.
- How to treat revaluation-model utilities against historical-cost SYSCOHADA utilities for INV_capex_to_depreciation and INV_asset_base_growth: require the excluding-revaluation variants for cross-country views?
- Should IPP-delivered generation capacity, which is utility-backed through PPAs and take-or-pay, be tracked as an 'off-balance-sheet investment' context metric linked to the IPP/offtaker dimension?
- FX and inflation conversion policy for cross-country unit costs (INV_capex_per_new_connection): average-year market rate, official rate (relevant for Nigeria and the DRC), or PPP?
- Which public sources are reliable for capex budgets per country (performance contracts, multi-year tariff orders, finance ministry budget execution reports), and is it worth the extraction effort for MVP?
- Labelling rule for 'concessional' loans when notes give only the lender name and rate: apply a lender-type list (MDB/bilateral = concessional) or require an explicit disclosure?

## ACC : Clients, accès et qualité de service

*This dimension covers how large the utility's customer base is, how quickly it grows, who the customers are (residential versus commercial/industrial/public), how much each customer consumes, and the service experience (connection delays, complaints, social tariff coverage). It also places each utility in its national context using the access rate. In Sub-Saharan Africa, access expansion is often the main policy mandate given to utilities and donors (connection programmes, last-mile subsidies, prepaid meter rollouts), so customer-side metrics are needed to read financial and operational KPIs correctly. For example, falling consumption per customer can come from a successful mass-connection programme of low-consumption households, not from poor performance. Customer counts and connections are widely published in annual reports and regulator reports. Service-quality metrics (complaints, connection time) are less often published and are defined differently from one source to another, so they are mostly extended-tier.*

### `ACC_consumption_per_customer` : Consommation moyenne par client
*Average consumption per customer* · palier **noyau MVP** · contexte · contexte (non noté) · unité : kWh per customer per year

- **Définition** : Energy billed (or sold, including prepaid vending) during the year divided by the average number of active customers. Compute in total and, where possible, for residential customers only.
- **Formule** : `ACC_consumption_per_customer = energy_billed_gwh * 1,000,000 / ((customers_total_count[t] + customers_total_count[t-1]) / 2) [kWh per customer per year]. Residential variant: energy_billed_residential_gwh * 1,000,000 / average(customers_residential_count[t], customers_residential_count[t-1]). If only a year-end count exists, use customers_total_count[t] and flag it.`
- **Données brutes** : `energy_billed_gwh`, `energy_billed_residential_gwh`, `customers_total_count`, `customers_residential_count`
- **Sources typiques** : utility annual report (sales by tariff class); audited financial statements notes (revenue by category, for cross-checks); regulator annual report
- **Disponibilité attendue** : élevée. Both inputs (GWh billed or sold and customer count) are among the most commonly published utility figures. The residential split is less available.
- **Pièges de comparaison** : This is heavily driven by customer mix: a few large HV/MV industrial or mining customers (e.g. Zambia, DRC Katanga, South Africa) dominate the average, so prefer the residential variant for comparisons. Mass connection of low-income households lowers the average, which is not deterioration. Bulk sales to other utilities or exports must be excluded from energy_billed_gwh for this KPI. Billed energy for unmetered or estimated-billing customers is uncertain. Suppressed demand from load-shedding and rationing (e.g. South Africa, Zambia drought years, Ghana 'dumsor') lowers consumption without reflecting demand. Prepaid vending is recorded as energy sold when tokens are purchased, not when the energy is consumed.

### `ACC_new_connections` : Nouveaux raccordements réalisés dans l'année
*New connections completed per year* · palier **noyau MVP** · noté · plus haut = mieux · unité : count per year

- **Définition** : Number of new customer connections energised during the fiscal year, gross of disconnections and terminations. Where available, split into residential versus non-residential and into programme-funded (donor, government, 'branchements sociaux') versus customer-funded connections.
- **Formule** : `ACC_new_connections = new_connections_count. Optional share funded by programmes: new_connections_programme_funded_count / new_connections_count * 100. Optional consistency check: customers_total_count[t] - customers_total_count[t-1] + disconnections_terminations_count, compared with new_connections_count`
- **Données brutes** : `new_connections_count`, `new_connections_residential_count`, `new_connections_programme_funded_count`, `disconnections_terminations_count`, `customers_total_count`
- **Sources typiques** : utility annual report; regulator annual report; rural electrification agency reports; donor project documents (results frameworks, implementation status reports)
- **Disponibilité attendue** : moyenne. Often reported because access is a political priority, and donor results frameworks track connections. However, it can be reported as 'branchements' (service drops), meters installed or households connected, and sometimes only for a specific programme.
- **Pièges de comparaison** : Gross connections differ from net change in customer count. Programme counts (donor results) may double-count with the utility's count, or include connections made by a separate rural electrification agency or mini-grid operators that are not utility customers. Meter replacements under prepaid migration must not be counted as new connections. Scale by the customer base, or compare with the country's unconnected population, before ranking utilities.

### `ACC_complaints_per_1000_customers` : Taux de réclamations pour 1 000 clients
*Customer complaints per 1,000 customers* · palier **étendu** · noté · plus bas = mieux · unité : complaints per 1,000 customers per year

- **Définition** : Number of customer complaints registered during the year (by the utility's customer service and/or the regulator's complaint desk) per 1,000 average active customers. Optionally also report the resolution rate within the year.
- **Formule** : `ACC_complaints_per_1000_customers = complaints_received_count / ((customers_total_count[t] + customers_total_count[t-1]) / 2) * 1000. Optional resolution rate: complaints_resolved_count / complaints_received_count * 100`
- **Données brutes** : `complaints_received_count`, `complaints_resolved_count`, `complaints_received_regulator_count`, `customers_total_count`
- **Sources typiques** : regulator annual report (consumer protection section); utility annual or sustainability report; regulator customer service standards compliance reports
- **Disponibilité attendue** : faible. Published by some regulators (often those with formal consumer-protection mandates in anglophone markets) and in some utility sustainability reports. It is rarely published in francophone central African utility reports. Definitions of a 'complaint' versus an inquiry or fault call differ widely.
- **Pièges de comparaison** : Recording practices dominate the figure: better call centres and digital channels raise registered complaints. Complaints logged by the utility and complaints escalated to the regulator are different populations, so store them separately. Estimated-billing disputes and prepaid token issues can drive volume. A low value may mean little capacity to log complaints, not good service.

### `ACC_connection_time_days` : Délai moyen de raccordement
*Average new connection lead time* · palier **étendu** · noté · plus bas = mieux · unité : days

- **Définition** : Average (or median, as stated by the source) number of days from a complete application (or payment of connection fees) to energisation of a new connection. Record the customer segment (low-voltage residential versus business/MV) and which start event is used. Context alternate: the World Bank Doing Business 'Getting Electricity' time measure for a standardised business connection in the largest business city, available up to the 2020 edition (Doing Business was discontinued in 2021), and any successor B-READY measure.
- **Formule** : `ACC_connection_time_days = sum(connection_lead_time_days over connections completed) / new_connections_count, or as published: connection_time_avg_days. Context alternate: wb_getting_electricity_time_days`
- **Données brutes** : `connection_time_avg_days`, `connection_lead_time_days_sum`, `new_connections_count`, `connection_backlog_pending_count`, `wb_getting_electricity_time_days`
- **Sources typiques** : regulator service standards reports; utility annual report or customer charter compliance; World Bank Doing Business historical data (Getting Electricity); donor project documents
- **Disponibilité attendue** : faible. Utility-published connection delays are rare and use inconsistent start points. Pending application backlogs (e.g. due to meter shortages) are sometimes reported instead. Doing Business data covers a standardised commercial case rather than the utility's average customer, and stops after the 2020 edition.
- **Référence** (de mémoire, non vérifiée) : World Bank Doing Business 'Getting Electricity' indicator (time in days to obtain a permanent connection for a standardised business case); utility-reported delays have no common standard
- **Pièges de comparaison** : Start events differ (application, technical survey, payment, meter availability). Meter or material stock-outs and customer-funded network extensions can dominate delays. Average versus median and residential versus business segments are not comparable. Doing Business figures are for one city and one standardised business case, and must not be presented as utility-wide performance. A backlog of pending applications can hide long delays that are not captured in an average over completed connections only.
- **Revue** : Reference: Doing Business discontinuation is correct; the B-READY successor measure is unverified.

### `ACC_customer_growth_rate` : Taux de croissance annuel du nombre de clients
*Customer base growth rate* · palier **étendu** · contexte · contexte (non noté) · unité : % per year

- **Définition** : Year-on-year percentage change in total active customers at year end.
- **Formule** : `ACC_customer_growth_rate = (customers_total_count[t] / customers_total_count[t-1] - 1) * 100`
- **Données brutes** : `customers_total_count`
- **Sources typiques** : utility annual reports (consecutive years); regulator annual reports
- **Disponibilité attendue** : élevée. Computed from two consecutive year-end counts, which are widely available. Breaks in the series occur when the counting definition changes or when customer databases are cleaned up.
- **Pièges de comparaison** : Database clean-ups (removing dormant accounts, migrating to a new billing or prepaid system) can produce negative or artificially large changes. Restatements in later reports should be captured as new values with their own source. Growth is naturally higher from a low base, so read it together with the national access rate and population growth. Mergers, concession transfers and unbundling events create breaks in the series.

### `ACC_lifeline_tariff_coverage` : Couverture du tarif social (tranche sociale)
*Lifeline / social tariff coverage* · palier **étendu** · contexte · contexte (non noté) · unité : % of residential customers (or % of residential GWh)

- **Définition** : Share of residential customers billed under a lifeline or social tariff (e.g. 'tranche sociale', free basic electricity, first-block subsidised band), and optionally the share of residential energy billed under it. Record the eligibility rule (consumption threshold, subscribed capacity, means test).
- **Formule** : `ACC_lifeline_tariff_coverage = customers_lifeline_tariff_count / customers_residential_count * 100. Optional energy variant: energy_billed_lifeline_gwh / energy_billed_residential_gwh * 100. Optional fiscal link: lifeline_subsidy_amount_lcu_m (government compensation or cross-subsidy, as disclosed)`
- **Données brutes** : `customers_lifeline_tariff_count`, `customers_residential_count`, `energy_billed_lifeline_gwh`, `energy_billed_residential_gwh`, `lifeline_subsidy_amount_lcu_m`
- **Sources typiques** : regulator tariff decisions and tariff study reports; utility annual report (sales by tariff band); ministry of finance subsidy or tariff compensation reports; IMF Article IV or donor public-expenditure reviews
- **Disponibilité attendue** : faible. The existence and design of lifeline tariffs are usually public in tariff schedules. Counts of customers actually billed under them are published only occasionally, in tariff studies or regulator reports. The subsidy amount may appear in the government budget or as a tariff compensation line in financial statements (under IFRS or SYSCOHADA).
- **Pièges de comparaison** : Eligibility rules differ (kWh block for all customers versus a separate social class versus means-tested), so the same coverage percentage can mean very different policies. Under increasing-block tariffs every customer's first block is subsidised, so coverage should be defined as customers whose consumption falls only within the lifeline band, and the source's definition should be stated. Prepaid customers may be automatically placed in the social band. Higher coverage is a social-policy choice, not good or bad performance, so it is context_only. Link it to tariff-compensation receivables and government arrears in the financial dimension.

### `ACC_residential_share` : Part des clients résidentiels
*Residential customer share* · palier **étendu** · contexte · contexte (non noté) · unité : % of customers (or % of GWh billed)

- **Définition** : Share of residential (domestic) customers in total active customers at year end. Optionally also compute the residential share of energy billed.
- **Formule** : `ACC_residential_share = customers_residential_count / customers_total_count * 100. Optional energy variant: energy_billed_residential_gwh / energy_billed_gwh * 100`
- **Données brutes** : `customers_residential_count`, `customers_total_count`, `energy_billed_residential_gwh`, `energy_billed_gwh`
- **Sources typiques** : utility annual report (sales by tariff class); regulator tariff or market reports; tariff review filings
- **Disponibilité attendue** : moyenne. Many annual reports break customers and sales down by tariff category. Category definitions vary: 'domestique', 'social', 'BT professionnel' and small commercial may be grouped differently.
- **Pièges de comparaison** : Tariff class boundaries are utility-specific (e.g. low-voltage professional customers may be in or out of the residential group; social tranches may be a separate class). The customer-count share is typically very high, while the energy share is much lower, so always state which variant is used. This is a structural driver of revenue mix and collection risk: residential prepaid customers versus public-sector postpaid accounts with arrears.

**Questions ouvertes (ACC)**

- Customer count basis: should the platform standardise on 'active accounts' (prepaid accounts with a purchase in the last 12 months, plus postpaid billed accounts) and store the registered count as an alternate, or accept whatever each source publishes with a definition flag?
- In unbundled markets with many distribution companies (Nigeria, Ghana ECG/NEDCo, South Africa Eskom plus municipalities), should ACC KPIs for the national single buyer or transmission company be set to not applicable, and should national totals be built by aggregating distribution companies?
- Can the platform add a service-territory population denominator (e.g. 'utility-level access' = residential customers × average household size / territory population)? This would need household size from census or DHS data and territory boundaries, which bring assumptions that may conflict with the source-first principle.
- Should donor-programme connections (from results frameworks) be stored as separate raw items, so they are not double-counted against utility-reported connections?
- Connection time: the World Bank Doing Business 'Getting Electricity' series ended with the 2020 edition, and a B-READY successor measure needs to be confirmed by a fetch before it is referenced. Should the platform keep only the historical values for context?
- Should SAIDI/SAIFI and load-shedding hours be placed in this dimension (service quality from the customer's view) or in an operations/reliability dimension? Decide this to avoid overlap across the dictionary.
- For consumption per customer, should bulk/HV mining or export customers be systematically excluded (a 'residential + LV' variant as the default), given their dominance in Zambia, DRC and South Africa?

## CTX : Variables de contexte / groupes de pairs (non notées)

*African utilities operate under very different structural conditions: integrated versus unbundled sector design, state versus private or concession ownership, very different system sizes, hydro-dominated versus thermal or diesel-dependent supply, CFA-franc peg versus floating currencies, SYSCOHADA versus IFRS reporting, and fragile or conflict settings. If raw KPIs such as losses, collection rate, cost recovery or SAIDI are compared across these settings without adjustment, the platform mostly measures context rather than management performance. The CTX variables are never scored (direction=context_only). They have three uses: (1) build peer groups; (2) feed a Peer-Adjusted Performance Score, for example by comparing within a peer group or using residuals from a simple regression on context; (3) tell users when a comparison is structurally not like-for-like, for example comparing a distribution-only company's margin with a vertically integrated utility's. The variables are chosen because they can be recorded from public sources: sector law and regulator reports, utility annual reports, and World Bank WDI and FCV lists. Each value carries a source, page and confidence level, the same as the scored KPIs. Categorical variables are stored per utility-year because structure and ownership change over time (for example unbundling, privatisation, or the end of a concession).*

### `CTX_customer_base_size` : Taille du portefeuille clients
*Customer base size* · palier **noyau MVP** · contexte · contexte (non noté) · unité : count (customers); % prepaid

- **Définition** : Number of active billed customer accounts at year end, all voltage levels, split into postpaid and prepaid where disclosed. It is used both as a size variable for binning and as the denominator for per-customer KPIs.
- **Formule** : `customers_total_count (year-end, active accounts; class and prepaid/postpaid breakdowns as raw items); binning variable = log10(customers_total_count). Prepaid share: see COM_prepaid_share.`
- **Données brutes** : `customers_total_count`, `customers_postpaid_count`, `customers_prepaid_count`, `customers_mv_hv_count`
- **Sources typiques** : utility annual report (key figures); regulator annual report / market statistics; ministry energy statistics; donor project documents (baseline data)
- **Disponibilité attendue** : élevée. Almost every utility and regulator publishes customer numbers, though definitions vary (connections, meters or contracts) and the prepaid split is reported less consistently. Generation-only and transmission-only entities have no retail customers, so for them energy sent out is the size variable instead.
- **Pièges de comparaison** : Counts may mean contracts, meters or connections, and may include inactive or disconnected accounts. Year-end figures may be compared with averages. Shared or illegal connections hide the real population served. A high prepaid share mechanically lifts the collection rate. Size alone is a weak proxy for complexity: the same customer count over a dense capital city and over a vast rural territory are very different networks.

### `CTX_gdp_per_capita_usd` : PIB par habitant (USD courants)
*GDP per capita (current USD)* · palier **noyau MVP** · contexte · contexte (non noté) · unité : USD per person (current)

- **Définition** : Country GDP per capita in current US dollars from the World Bank WDI (NY.GDP.PCAP.CD). It approximates customers' ability to pay and the overall economic environment.
- **Formule** : `CTX_gdp_per_capita_usd = gdp_per_capita_current_usd (WDI NY.GDP.PCAP.CD, same year)`
- **Données brutes** : `gdp_per_capita_current_usd`
- **Sources typiques** : World Bank WDI; IMF World Economic Outlook database (cross-check)
- **Disponibilité attendue** : élevée. An open series available annually for all MVP countries.
- **Référence** (vérifiée (URL consultée)) : World Bank WDI indicator NY.GDP.PCAP.CD 'GDP per capita (current US$)' <https://data.worldbank.org/indicator/NY.GDP.PCAP.CD>
- **Pièges de comparaison** : Current-USD values swing with exchange rates (Nigeria, Ghana, Zambia and Kenya devalued during 2019-2025), so peer bins can change because of FX rather than real income. A PPP or a multi-year average variant should be considered. National averages hide inequality and the gap between the utility's franchise area and the rest of the country. Oil-rich economies (Congo-Brazzaville, Nigeria) can show GDP per capita well above household ability to pay.

### `CTX_market_structure` : Structure de marché et périmètre d'activité de l'entité
*Market structure and entity value-chain scope* · palier **noyau MVP** · contexte · contexte (non noté) · unité : category (+ % for the derived IPP purchase share)

- **Définition** : A categorical classification at two levels, both recorded per utility-year. (a) Sector model of the country: vertically_integrated_monopoly / single_buyer_with_IPPs / partially_unbundled (separate transmission company and/or system operator) / fully_unbundled_with_wholesale_market. (b) Scope of the entity: integrated_GTD / generation_only / transmission_only (including single buyer) / distribution_only (including distribution-plus-retail) / private_concession_integrated / private_concession_distribution. Boolean flags record whether the entity is the designated single buyer, whether it buys power from IPPs under take-or-pay PPAs, and whether a separate asset-holding company (société de patrimoine) owns the network.
- **Formule** : `CTX_market_structure = categorical(sector_model_code, entity_scope_code) + flags(is_single_buyer_flag, has_ipp_take_or_pay_flag, asset_holding_company_separate_flag). Purchase share: reference GEN_purchased_energy_share (not recomputed here).`
- **Données brutes** : `sector_model_code`, `entity_scope_code`, `is_single_buyer_flag`, `has_ipp_take_or_pay_flag`, `asset_holding_company_separate_flag`
- **Sources typiques** : electricity sector law / code de l'électricité; regulator annual report (e.g. sector overview section); utility annual report (company presentation); concession / affermage contract summaries; World Bank / AfDB project appraisal documents (sector background)
- **Disponibilité attendue** : élevée. Sector structure is described in legislation, regulator reports and almost every donor project document. The entity's scope can be read from its own annual report. Judgement calls are needed for hybrid cases, for example Nigeria's unbundled DisCos alongside a TCN that is still state-owned, Côte d'Ivoire's private operator under a concession with a separate state asset company, or Kenya's KPLC as distribution/retail plus single buyer while KenGen generates separately. The classification rules must therefore be written down explicitly.
- **Référence** (de mémoire, non vérifiée) : Loosely follows the reform-stage typology used in World Bank power sector reform literature (vertical integration, single buyer, unbundling, wholesale competition); exact category labels are the platform's own
- **Pièges de comparaison** : This is the most important control. Losses, margins, the cost structure (a distribution company's power-purchase cost versus an integrated utility's fuel and depreciation) and even the meaning of 'energy sent out' all differ by entity scope, so ratios from different scopes must never be ranked together. The label 'single buyer' covers very different exposures to IPP take-or-pay. Structure can change in the middle of the 2019-2025 window, so time series must be broken or flagged when it does.

### `CTX_national_access_rate` : Taux d'accès national à l'électricité
*National electricity access rate* · palier **noyau MVP** · contexte · contexte (non noté) · unité : % of population

- **Définition** : Share of the national population with access to electricity, taken from the SDG 7.1.1 series published by the World Bank (WDI EG.ELC.ACCS.ZS). Urban and rural splits are stored where available. This is a country-level variable attached to every utility in the country.
- **Formule** : `CTX_national_access_rate = wdi_access_electricity_pct_population (WDI EG.ELC.ACCS.ZS, same year; if missing, latest prior year flagged as carried-forward)`
- **Données brutes** : `wdi_access_electricity_pct_population`, `wdi_access_electricity_urban_pct`, `wdi_access_electricity_rural_pct`
- **Sources typiques** : World Bank WDI / ESMAP SDG7.1.1 electrification dataset; Tracking SDG7 report; national ministry / rural electrification agency statistics (as cross-check)
- **Disponibilité attendue** : élevée. Published for all MVP countries in an open, harmonised series. The latest year usually lags by one to two years, so 2024-2025 will often need carry-forward with a flag.
- **Référence** (vérifiée (URL consultée)) : World Bank WDI indicator EG.ELC.ACCS.ZS 'Access to electricity (% of population)', sourced from the ESMAP SDG 7.1.1 dataset <https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS>
- **Pièges de comparaison** : The measure is national, not specific to the utility. It mixes grid and off-grid or solar-home-system access, and in countries with several distribution companies (Nigeria, South Africa's municipal distributors) it says little about a given company's franchise area. Modelled survey-based estimates can differ from national administrative figures, so the World Bank series should be the primary source and only one source used per comparison.

### `CTX_ownership_type` : Type d'actionnariat et de contrôle
*Ownership and control type* · palier **noyau MVP** · contexte · contexte (non noté) · unité : category (+ % state share)

- **Définition** : A categorical ownership class per utility-year based on the shareholding: state_100pct / state_majority / mixed_private_majority / private_concessionaire_on_state_assets / private_full. Flags record a stock-exchange listing, a strategic operator or management contract, and any donor-financed performance contract. The state share is also kept as a number.
- **Formule** : `state_share_pct = shares_held_by_state_and_public_entities_count / total_shares_outstanding_count * 100; CTX_ownership_type = bin(state_share_pct, private_operator_contract_type_code) + flags(is_listed_flag, management_contract_flag)`
- **Données brutes** : `shares_held_by_state_and_public_entities_count`, `total_shares_outstanding_count`, `private_operator_contract_type_code`, `is_listed_flag`, `management_contract_flag`
- **Sources typiques** : audited financial statements (share capital note / related parties); utility annual report (shareholding structure); stock exchange filings (e.g. listed utilities); privatisation or concession agreements as summarised by regulator or donors
- **Disponibilité attendue** : élevée. Share capital and principal shareholders are disclosed in audited statements and annual reports. Listed utilities publish shareholder lists. For concessions, the asset owner and the operator must be recorded separately.
- **Pièges de comparaison** : Formal ownership does not capture governance in practice. A listed company with a state majority can be politically managed, and a private concessionaire can depend on state tariff compensation. Indirect state holdings through pension funds or holding companies may be missed. State-owned utilities often carry public-sector arrears both as receivables and as payables, which distorts working-capital KPIs in ways linked to ownership.

### `CTX_average_tariff_usd` : Tarif moyen effectif (USD/kWh)
*Average effective tariff (USD per kWh)* · palier **étendu** · dérivé, affiché seulement · contexte (non noté) · unité : USD/kWh

- **Définition** : Average revenue per kWh billed from electricity sales to end customers, converted to US dollars at the period-average official exchange rate. It measures the realised tariff level, not the tariff schedule. Government tariff compensation or subsidies are kept separately and shown both excluded and included.
- **Formule** : `Derived view: FIN_average_revenue_per_kwh_billed / fx_lcu_per_usd_avg (no separate extraction).`
- **Données brutes** : `revenue_electricity_sales_lcu_m`, `tariff_compensation_revenue_lcu_m`, `energy_billed_gwh`, `fx_lcu_per_usd_avg`
- **Sources typiques** : audited financial statements (revenue note); utility annual report (sales statistics); regulator tariff decisions / annual report; World Bank WDI PA.NUS.FCRF or central bank for exchange rate
- **Disponibilité attendue** : moyenne. Sales revenue and billed energy are usually both published, but revenue lines may mix connection fees, export sales and VAT or levies, so the revenue note needs to be read carefully. Subsidies are disclosed inconsistently: sometimes as revenue, sometimes as an operating grant, sometimes netted off arrears. The exchange rate comes from a verified open series.
- **Référence** (vérifiée (URL consultée)) : Exchange rate: World Bank WDI PA.NUS.FCRF 'Official exchange rate (LCU per US$, period average)'; tariff computation is platform convention <https://data.worldbank.org/indicator/PA.NUS.FCRF>
- **Pièges de comparaison** : Large devaluations (Nigeria 2023-24, Ghana 2022, Zambia, Kenya) make USD tariffs fall even when local tariffs rise. Where parallel markets exist the official rate can misstate the real level. Bulk or export sales and large mining customers (Zambia, DRC) pull the average down. In a distribution company the tariff is a retail tariff while in a generation company it is a wholesale tariff, so it must only be used within the same entity scope. This is a context variable, not a performance score: a higher tariff is neither better nor worse.

### `CTX_currency_accounting_regime` : Régime de change et référentiel comptable
*Currency regime and accounting framework* · palier **étendu** · contexte · contexte (non noté) · unité : category

- **Définition** : Two categorical sub-variables per utility-year. (a) Currency regime of the country: cfa_franc_peg_euro (XAF for CEMAC, XOF for UEMOA) / other_hard_peg / managed_float / free_float. (b) Accounting framework of the audited statements: IFRS_full / SYSCOHADA_revised / national_GAAP_other / IPSAS. A supplementary flag records whether the auditor's opinion is qualified, adverse or a disclaimer.
- **Formule** : `CTX_currency_accounting_regime = categorical(currency_regime_code, accounting_framework_code). Audit modification is derived from GOV audit_opinion_category, not stored here.`
- **Données brutes** : `currency_regime_code`, `accounting_framework_code`
- **Sources typiques** : audited financial statements (basis of preparation note; auditor's report); IMF AREAER / IMF country reports (exchange arrangement); central bank publications (BEAC, BCEAO, national central banks)
- **Disponibilité attendue** : élevée. The basis of preparation and the audit opinion appear on the first pages of any audited statements, and the currency regime is public. Availability is limited only where audited statements themselves are not published, which is common for some state-owned utilities.
- **Référence** (de mémoire, non vérifiée) : Exchange-arrangement classes loosely follow the IMF AREAER de facto classification; accounting framework labels follow IFRS / OHADA SYSCOHADA revised (2017) naming
- **Pièges de comparaison** : SYSCOHADA and IFRS treat several items differently: lease and concession accounting (IFRS 16 / IFRIC 12), revaluation, the presentation of subsidies and 'hors activités ordinaires' items, and provisions. Margins, EBITDA and asset bases are therefore not strictly comparable without restatement. CFA-peg utilities have no FX translation shocks against the euro but remain exposed to the USD (fuel, USD-denominated IPP PPAs). Utilities in floating-currency countries can show large FX losses on USD debt and PPAs that hide operating performance. A modified audit opinion should lower the confidence weight on all financial KPIs.

### `CTX_fcv_status` : Statut de fragilité, conflit et violence (FCV)
*Fragility, conflict and violence (FCV) status* · palier **étendu** · contexte · contexte (non noté) · unité : category

- **Définition** : Whether the country appears on the World Bank Group's annual fragility lists for the fiscal year that matches the data year. Up to FY2026 this is the Harmonized List of Fragile and Conflict-affected Situations (FCS), with classes such as conflict versus institutional/social fragility. From FY2027 the World Bank publishes two separate lists: a Public FCV List and an Institutional Fragility List. Stored as a categorical value with list-vintage metadata.
- **Formule** : `CTX_fcv_status = categorical(fcv_list_class_code) where fcv_list_class_code in {not_listed, institutional_fragility, conflict_or_violence} mapped from wb_fcs_fcv_list_fiscal_year matching data year (WB fiscal year FYt covers July t-1 to June t; mapping rule documented)`
- **Données brutes** : `fcv_list_class_code`, `wb_fcs_fcv_list_fiscal_year`
- **Sources typiques** : World Bank FCS/FCV classification page and historical lists; donor project documents (country context sections)
- **Disponibilité attendue** : élevée. Published annually by the World Bank with historical lists archived. The method changed for FY2027, so the 2019-2025 data years fall under the older FCS method and a crosswalk will be needed for later years.
- **Référence** (vérifiée (URL consultée)) : World Bank Group classification of Fragile and Conflict-affected Situations (FCS lists FY2006-FY2026) and FCV lists from FY2027 <https://www.worldbank.org/en/topic/fragilityconflictviolence/brief/classification-of-fragile-and-conflict-affected-situations>
- **Pièges de comparaison** : Status is national, while conflict is often regional (eastern DRC, northern Nigeria, north-west and south-west Cameroon), so the utility's core franchise area may be unaffected while its remote networks are. The method break at FY2027 means classes are not continuous over time. A binary flag hides intensity. Conflict affects vandalism, losses, collection and reliability, so FCV utilities should be compared with each other or adjusted rather than penalised directly.

### `CTX_supply_mix` : Mix d'approvisionnement (production propre, achats, importations)
*Supply mix (own generation by technology, purchases, imports)* · palier **étendu** · contexte · contexte (non noté) · unité : % of energy available (GWh basis)

- **Définition** : Shares of total energy available to the entity coming from each source: own hydro, own gas, own oil/diesel (including rented emergency power), own coal, own solar/wind/other renewables, IPP purchases, and cross-border imports. The denominator is total energy available before network losses: own gross generation plus purchases plus imports. A derived flag marks systems that depend on hydro or on liquid fuels.
- **Formule** : `energy_available_gwh = energy_sent_out_gwh + energy_purchased_total_gwh (net basis, same denominator as GEN). Shares (sum to 100%): own hydro, own gas, own coal, own liquid fuel (energy_sent_out_liquid_fuel_gwh), own solar/wind/other, IPP purchases excluding emergency, emergency rental (counted only here, as liquid fuel), imports, other utilities. Liquid-fuel exposure: reference GEN_costly_thermal_share.`
- **Données brutes** : `energy_generated_gross_gwh`, `energy_generated_hydro_gwh`, `energy_generated_gas_gwh`, `energy_sent_out_liquid_fuel_gwh`, `energy_generated_coal_gwh`, `energy_generated_solar_wind_other_gwh`, `energy_purchased_domestic_gwh`, `energy_imported_gwh`, `energy_purchased_emergency_rental_gwh`
- **Sources typiques** : utility annual report (energy balance / production statistics); regulator annual report (national energy balance); system operator / transmission company reports; ministry energy statistics / national energy balance; IEA or IRENA country statistics (national-level fallback)
- **Disponibilité attendue** : moyenne. Integrated utilities and single buyers usually publish an energy balance by source. Splits by technology for IPP purchases and for emergency rental power are less consistent. For distribution-only companies the mix belongs to the upstream system, so a national mix from the regulator or system operator has to be attached, with a flag.
- **Référence** (aucune) : none (platform energy-balance convention; denominator = own gross generation + purchases + imports)
- **Pièges de comparaison** : Hydro-heavy systems (DRC, Zambia, Congo-Brazzaville partly, Cameroon, Ghana partly) have low fuel costs but are exposed to drought, as in Zambia's 2024 drought. Year-to-year changes in the mix can therefore drive cost and reliability KPIs, so the mix should be compared per year and not only as an average. Mixing gross and net generation, or counting IPP energy both as generation and as purchases, inflates the denominator. Emergency diesel rentals are often reported under opaque 'other purchases'.
- **Revue** : Review fix: gross/net mixing and >100% double count (emergency rental in two shares) removed.

**Questions ouvertes (CTX)**

- Proposed peer-group method (MVP, about 15-25 utilities). Use a two-stage approach because the sample is too small for full cross-classification. Stage 1 is a hard filter on CTX_market_structure.entity_scope, collapsed into three groups: (i) integrated GTD and integrated concessions, (ii) distribution/retail, including single-buyer distribution companies like KPLC and Nigerian DisCos, (iii) generation-only or transmission-only. Ratios are never ranked across these groups. Stage 2, within each scope group, bins three variables into two or three classes each: (a) system size, as log10(CTX_customer_base_size) split at the sample tertiles (for generation and transmission companies, energy_sent_out_gwh tertiles instead); (b) economic environment, as CTX_gdp_per_capita_usd using a 3-year average to dampen FX swings, split into two classes at the sample median or at the World Bank income-group boundary (low versus lower-middle-and-above), with the World Bank boundaries preferred because they are external and reproducible; (c) supply-cost exposure, as a binary hydro-dominant versus thermal/import-dominant flag from CTX_supply_mix, with the cut at the majority source of energy available. CTX_fcv_status and CTX_currency_accounting_regime are not used for binning. They are adjustment flags: they appear as caveats, and SYSCOHADA versus IFRS is a restatement warning on financial KPIs. Peer-Adjusted Performance Score: compute the percentile within the stage-1 group and show it next to a 'context-expected' value from a parsimonious regression of each KPI on the stage-2 variables plus the FCV flag. Report the residual only when the group has at least about 6 observations (utility-years can be pooled over 2019-2025 with year effects).
- Weaknesses of this method: (1) Small n. With about 20 utilities, many stage-2 cells will hold one or two utilities, so bins have to be collapsed or the platform falls back to nearest-neighbour peers (for example Gower distance on the CTX variables), which is harder to explain. (2) Endogeneity. The average tariff, the access rate and even customer numbers partly reflect utility performance, so adjusting for them can explain away genuine under-performance. For that reason CTX_average_tariff_usd is deliberately left out of binning. (3) National variables (access, GDP per capita, FCV) are poor proxies for a single distribution company's franchise area in multi-company countries (Nigeria, South Africa). (4) Structural breaks within 2019-2025 (privatisations, concession changes, the FY2027 FCV method change) move utilities between groups over time. (5) Cut-points based on sample tertiles change whenever new utilities are added, so peer groups are unstable across releases. Fixed external cut-points are more stable but may leave cells empty. (6) A binary hydro/thermal flag ignores drought years and the take-or-pay exposure that comes with IPP-heavy supply.
- Should urbanization (WDI SP.URB.TOTL.IN.ZS, which exists as an open series) and a network-density proxy (customers_total_count / network_length_km, or customers per km2 of the franchise area) be added as CTX variables? Network density is arguably a better driver of losses and reliability than national urbanization, but network length and franchise area are published inconsistently. The decision is whether to collect them as extended raw items.
- For distribution-only entities and concessions, which supply mix should be attached: the national system mix (from the regulator or system operator) or the entity's own purchase mix by supplier? This affects the hydro/thermal flag used in peer binning.
- How should multi-entity countries (Nigeria's 11 DisCos, South African municipal distributors, Ghana's ECG versus NEDCo) be handled when national-level CTX variables are identical across them? One option is to add sub-national variables (state or regional GDP, population density) where public sources exist, accepting lower availability.
- GDP per capita in current USD versus PPP versus a 3-year average: which version drives binning? Current USD is the most transparent but is unstable after large devaluations (Nigeria, Ghana, Zambia).
- Should the auditor's opinion (qualified, adverse, disclaimer) stay as a sub-flag of CTX_currency_accounting_regime, or move into a separate data-quality / governance dimension that modulates confidence weights on all financial KPIs?
- Ownership and structure categories need written classification rules and worked examples for hybrid cases before extraction starts: Côte d'Ivoire's concession model with a separate state asset company, Senegal's integrated state utility buying from IPPs, Cameroon's structure after the end of the private concession, Kenya's split between KenGen, KPLC and KETRACO, and Nigeria's post-2013 DisCos alongside a state-owned TCN. Without these rules, coder disagreement will undermine the peer groups.

## Doublons supprimés

- `COM_revenue_per_kwh_billed` : Duplicate of FIN_average_revenue_per_kwh_billed.
- `ACC_national_access_rate` : Duplicate of CTX_national_access_rate (same WDI series EG.ELC.ACCS.ZS).
- `ACC_customers_total` : Duplicate of CTX_customer_base_size (same year-end count; class breakdown kept as raw items).
- `GEN_unserved_energy_ratio` : Merged into NET_energy_not_supplied_pct (single ENS record with cause split).

## Avis global du critique

The draft is detailed, but it was clearly assembled in silos.

1. **Duplicates.** At least five KPIs are duplicated outright or nearly so: average tariff three times, the access rate twice, the customer count twice, the prepaid share twice, and the IPP/purchase share three times with different denominators.

2. **Energy flow names are inconsistent.** The core energy-flow raw items are not reconciled. energy_purchased_gwh includes imports in GEN but excludes them in CTX. NET adds imports on top of it, which double-counts them. CTX mixes gross generation with net purchases. As a result, the advertised NET/COM bridge (billing efficiency = 100 - distribution losses) breaks, because the two use different HV/export exclusion items. A canonical energy-balance schema has to be fixed before any extraction starts.

3. **Formula errors.** The most serious is FIN_quasi_fiscal_deficit_pct_gdp. Because unit cost is defined per kWh billed, the underpricing term already equals the full cost-revenue gap, so adding excess losses double-counts them. DSCR mixes accrual EBITDA with cash debt service and omits lease principal. Net debt/EBITDA is biased between IFRS 16 and SYSCOHADA utilities. The USD conversion for O&M per km is dimensionally wrong.

4. **Availability ratings are too optimistic.** Ratings are optimistic for financial-statement KPIs, which are rated 'high' even though the GOV section concedes that several state-owned utilities do not publish audited statements. They are also optimistic for SAIDI, reserve margin, fuel cost per kWh and the funding-source split.

5. **Reference status overstated.** Two 'verified_by_fetch' tags (World Bank WPS 7788) rest on an abstract only. The IEEE 1366 citation points to a reseller. I spot-checked the NERC GADS and World Bank FCV references, and both are correct.

6. **Missing KPIs.** Arrears and payables to IPPs and fuel suppliers have no owner despite being central to SSA utility finance. Staff productivity (customers per employee) is entirely absent. Also missing: interest coverage, FX-debt exposure, equity/negative-equity, controllable opex per kWh and bad-debt expense.

7. **Core set.** The draft's 'core_mvp' set is too large (about 35) and includes context-only items as core.

**Recommended core set.** The 28 ids in core_mvp_recommendation: 23 scored KPIs plus 5 unscored CTX peer-group variables. It drops several draft-core items:
- the draft's COM_billing_efficiency, COM_revenue_per_kwh_billed, ACC_customers_total and ACC_national_access_rate (duplicates);
- GEN_available_capacity_ratio and GEN_reserve_margin (low data availability);
- INV_cwip_to_gross_ppe, INV_external_financing_share and INV_capex_to_revenue (weak signal or context-only).

It adds two of the proposed missing KPIs, FIN_power_purchase_payables_days and OPS_customers_per_employee, which have no definition in the draft yet. The rest of the set is draft ids.

Before extraction starts:
- Publish a canonical raw-item glossary.
- Correct the QFD formula.
- Separate the data-quality and missing state (code 0) from the audit opinion ordinal.
- Set one FX and fiscal-year convention for the whole platform.

## Décisions à prendre avant l’extraction

1. **Base du dénominateur des pertes** : recalculer à partir des volumes (énergie nette disponible) ou retenir la valeur publiée avec son dénominateur déclaré ? Proposition : stocker les deux, et classer sur la valeur recalculée seulement quand les volumes sont complets.
2. **Base de coût** : coût comptable (amortissement + frais financiers) ou charge normative du capital (valeur de remplacement × WACC) ? Le coût comptable est traçable, mais faussé par les réévaluations et les actifs financés par dons.
3. **Taux de pertes normatif** pour la décomposition du QFD : il faut une décision documentée, sans valeur inventée.
4. **Marchés dégroupés** (Nigeria, Ghana, Kenya, Afrique du Sud) : mesurer au niveau de l’entité, du système, ou des deux ?
5. **Date de coupure** des observations (pour le délai de publication des comptes) et distinction entre « non trouvé » et « absence vérifiée » dans les scores de gouvernance.
6. **Méthode des groupes de pairs** : filtre strict sur le périmètre, puis 3 variables en classes (taille, revenu, mix). Voir les questions ouvertes de CTX : le petit nombre d’utilities et l’endogénéité sont les deux faiblesses majeures.
7. **Validation experte** de la correspondance SYSCOHADA/OHADA pour les opinions d’audit (« refus de certifier »).
