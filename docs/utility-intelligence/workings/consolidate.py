"""Consolidate the 8 drafted KPI sections + critic review into one dictionary (JSON + Markdown)."""
import json, re, copy, os, sys

SRC = os.path.join(os.path.dirname(__file__), 'kpi_raw.json')
OUT_DIR = sys.argv[1]
raw = json.load(open(SRC))
drafts, crit = raw['drafts'], raw['critique']

# ---------------------------------------------------------------- canonical raw-item names
RENAME = {
    'electricity_sales_revenue_lcu_m': 'revenue_electricity_sales_lcu_m',
    'fx_rate_lcu_per_usd_avg': 'fx_lcu_per_usd_avg',
    'fx_avg_lcu_per_usd': 'fx_lcu_per_usd_avg',
    'tariff_compensation_subsidy_lcu_m': 'tariff_compensation_revenue_lcu_m',
    'subsidy_tariff_compensation_lcu_m': 'tariff_compensation_revenue_lcu_m',
    'cash_collected_from_customers_lcu_m': 'cash_collected_lcu_m',
    'revenue_billed_incl_vat_lcu_m': 'revenue_billed_lcu_m',
    'trade_receivables_public_sector_lcu_m': 'receivables_public_sector_gross_lcu_m',
    'customers_served_count': 'customers_total_count',
    'customers_count_start': 'customers_total_count[t-1]',
    'customers_count_end': 'customers_total_count[t]',
    'customers_total_count_opening': 'customers_total_count[t-1]',
    'customers_total_count_closing': 'customers_total_count[t]',
    'energy_billed_hv_gwh': 'energy_billed_hv_direct_gwh',
    'energy_generated_gwh': 'energy_generated_gross_gwh',
    'energy_generated_oil_diesel_gwh': 'energy_sent_out_liquid_fuel_gwh',
    'fuel_costs_lcu_m': 'fuel_cost_own_generation_lcu_m',
    'power_purchase_costs_lcu_m': 'power_purchase_cost_lcu_m',
    'energy_unserved_supply_shortfall_gwh': 'energy_not_supplied_supply_shortfall_gwh',
    'saidi_includes_planned_flag': 'reliability_includes_planned_flag',
    'saidi_includes_load_shedding_flag': 'reliability_includes_load_shedding_flag',
    'saidi_excludes_major_events_flag': 'reliability_excludes_major_events_flag',
    'access_electricity_pct_population': 'wdi_access_electricity_pct_population',
    'access_electricity_urban_pct': 'wdi_access_electricity_urban_pct',
    'access_electricity_rural_pct': 'wdi_access_electricity_rural_pct',
    'capex_actual_lcu_m': 'capex_cash_lcu_m',
    'revenue_operating_excl_subsidy_lcu_m': '(revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m)',
}
# list-level expansions for raw item arrays
RAW_EXPAND = {
    'energy_billed_hv_direct_and_export_gwh': ['energy_billed_hv_direct_gwh', 'energy_exported_billed_gwh'],
    'energy_purchased_gwh': ['energy_purchased_domestic_gwh', 'energy_imported_gwh'],
    'revenue_operating_excl_subsidy_lcu_m': ['revenue_electricity_sales_lcu_m', 'other_operating_revenue_lcu_m'],
    'audit_opinion_modified_flag': [],
    'customers_count_start': ['customers_total_count'], 'customers_count_end': ['customers_total_count'],
    'customers_total_count_opening': ['customers_total_count'], 'customers_total_count_closing': ['customers_total_count'],
}


def rename_text(s):
    # imports were double counted where GEN's purchase definition (incl. imports) met NET's "+ imports"
    s = s.replace('energy_purchased_gwh + energy_imported_gwh', 'energy_purchased_total_gwh')
    s = re.sub(r'\benergy_purchased_gwh\b', 'energy_purchased_total_gwh', s)
    s = re.sub(r'\benergy_billed_hv_direct_and_export_gwh\b', '(energy_billed_hv_direct_gwh + energy_exported_billed_gwh)', s)
    for a, b in sorted(RENAME.items(), key=lambda kv: -len(kv[0])):
        s = re.sub(r'\b' + re.escape(a) + r'\b', b, s)
    return s


def rename_raw(items):
    out = []
    for it in items:
        if it in RAW_EXPAND:
            out += RAW_EXPAND[it]
        else:
            out.append(RENAME.get(it, it))
    seen, res = set(), []
    for it in out:
        if it not in seen:
            seen.add(it); res.append(it)
    return res


DIM_FR = {
    'FIN': 'Soutenabilité financière', 'GEN': 'Production et offre', 'NET': 'Réseau : pertes et fiabilité',
    'COM': 'Performance commerciale', 'OPS': 'Efficacité opérationnelle', 'GOV': 'Gouvernance, transparence et régulation',
    'INV': 'Investissement et efficacité du capital', 'ACC': 'Clients, accès et qualité de service',
    'CTX': 'Variables de contexte / groupes de pairs (non notées)',
}

kpis = {}
dim_meta = {}
for s in drafts:
    code = s['kpis'][0]['id'].split('_')[0]
    dim_meta[code] = {'name_en': s['dimension'], 'rationale_en': rename_text(s['dimension_rationale']), 'open_questions_en': s['open_questions']}
    for k in s['kpis']:
        k = copy.deepcopy(k)
        k['dimension'] = code
        k['formula'] = rename_text(k['formula'])
        k['raw_data_items'] = rename_raw(k['raw_data_items'])
        k['review_notes'] = []
        k['status'] = 'scored' if k['direction'] != 'context_only' else 'context'
        kpis[k['id']] = k

# ---------------------------------------------------------------- dedup (critic)
REMOVED = {
    'COM_revenue_per_kwh_billed': 'Duplicate of FIN_average_revenue_per_kwh_billed.',
    'ACC_national_access_rate': 'Duplicate of CTX_national_access_rate (same WDI series EG.ELC.ACCS.ZS).',
    'ACC_customers_total': 'Duplicate of CTX_customer_base_size (same year-end count; class breakdown kept as raw items).',
    'GEN_unserved_energy_ratio': 'Merged into NET_energy_not_supplied_pct (single ENS record with cause split).',
}
for r in REMOVED:
    kpis.pop(r)


def note(i, txt):
    kpis[i]['review_notes'].append(txt)


def patch(i, **kw):
    kpis[i].update(kw)

# ---------------------------------------------------------------- formula fixes (critic, checked against drafts)
patch('FIN_cost_recovery_ratio',
      formula='(revenue_electricity_sales_lcu_m + other_operating_revenue_lcu_m) / (operating_expenses_excl_depreciation_lcu_m - bad_debt_expense_lcu_m + depreciation_amortisation_lcu_m + finance_costs_lcu_m)',
      raw_data_items=['revenue_electricity_sales_lcu_m', 'other_operating_revenue_lcu_m', 'operating_expenses_excl_depreciation_lcu_m', 'bad_debt_expense_lcu_m', 'depreciation_amortisation_lcu_m', 'finance_costs_lcu_m'])
note('FIN_cost_recovery_ratio', 'Review fix: other operating revenue added to the numerator (its costs sit in opex); bad-debt expense removed from the denominator so the KPI stays on a billed basis.')
patch('FIN_unit_cost_of_service_per_kwh_billed',
      formula='(operating_expenses_excl_depreciation_lcu_m - bad_debt_expense_lcu_m + depreciation_amortisation_lcu_m + finance_costs_lcu_m) / energy_billed_gwh   (LCU per kWh)')
kpis['FIN_unit_cost_of_service_per_kwh_billed']['raw_data_items'].append('bad_debt_expense_lcu_m')
patch('FIN_debt_service_coverage_ratio',
      formula='(cash_flow_from_operations_lcu_m + interest_paid_lcu_m) / (interest_paid_lcu_m + debt_principal_repaid_lcu_m + lease_principal_paid_lcu_m). Secondary (stored, not ranked): EBITDA_excl_transfers_lcu_m / same denominator.',
      raw_data_items=['cash_flow_from_operations_lcu_m', 'interest_paid_lcu_m', 'debt_principal_repaid_lcu_m', 'lease_principal_paid_lcu_m', 'revenue_electricity_sales_lcu_m', 'other_operating_revenue_lcu_m', 'operating_expenses_excl_depreciation_lcu_m'])
note('FIN_debt_service_coverage_ratio', 'Review fix: accrual EBITDA overstates cash available when receivables balloon, so the ranked numerator is now operating cash flow before interest; lease principal is added to debt service.')
patch('FIN_net_debt_to_ebitda',
      formula='Ranked (cross-framework): (total_borrowings_lcu_m - cash_and_equivalents_lcu_m) / EBITDA_excl_transfers_excl_ifrs16_lcu_m (undefined if EBITDA <= 0). IFRS-only variant: (total_borrowings_lcu_m + lease_liabilities_lcu_m - cash_and_equivalents_lcu_m) / EBITDA_excl_transfers_lcu_m. Companion: net debt / total_assets_lcu_m.')
note('FIN_net_debt_to_ebitda', 'Review fix: SYSCOHADA (no IFRS 16) keeps lease costs in opex, so leases are excluded from the cross-framework ranked version.')
patch('FIN_quasi_fiscal_deficit_pct_gdp',
      formula='QFD_lcu_m = (C - R) + collection_shortfall_lcu_m, where C = operating_expenses_excl_depreciation_lcu_m - bad_debt_expense_lcu_m + depreciation_amortisation_lcu_m + finance_costs_lcu_m, R = revenue_electricity_sales_lcu_m, collection_shortfall_lcu_m = revenue_billed_lcu_m - cash_collected_lcu_m (stored signed, not floored). FIN_quasi_fiscal_deficit_pct_gdp = 100 * QFD_lcu_m / nominal_gdp_lcu_m. Decomposition into underpricing vs excess losses (losses valued at cost per kWh SUPPLIED, against a documented normative loss rate) is a stored analytical view, not part of the headline.',
      tier='extended')
kpis['FIN_quasi_fiscal_deficit_pct_gdp']['raw_data_items'] = rename_raw(kpis['FIN_quasi_fiscal_deficit_pct_gdp']['raw_data_items'] + ['bad_debt_expense_lcu_m'])
note('FIN_quasi_fiscal_deficit_pct_gdp', 'Review fix: the draft double counted losses (underpricing per kWh billed already equals the whole C - R gap). Headline is now (C - R) + collection shortfall. The normative loss rate is a methodology decision still open; no value is set.')
patch('NET_om_cost_per_network_km',
      formula='1000 * network_om_expense_lcu_m / (transmission_line_length_km + distribution_line_length_km)  [LCU thousand per km]; USD view: 1000 * (network_om_expense_lcu_m / fx_lcu_per_usd_avg) / (transmission_line_length_km + distribution_line_length_km)  [USD thousand per km]')
note('NET_om_cost_per_network_km', 'Review fix: the draft USD conversion dropped the per-km division.')
patch('NET_distribution_losses_pct',
      formula='100 * (energy_injected_distribution_gwh - energy_billed_distribution_gwh) / energy_injected_distribution_gwh, where energy_billed_distribution_gwh = energy_billed_gwh - energy_billed_hv_direct_gwh - energy_exported_billed_gwh',
      raw_data_items=['energy_injected_distribution_gwh', 'energy_billed_gwh', 'energy_billed_hv_direct_gwh', 'energy_exported_billed_gwh', 'reported_distribution_losses_pct'])
note('NET_distribution_losses_pct', 'Review fix: single canonical energy_billed_distribution_gwh shared with COM, so billing efficiency = 100 - distribution losses holds exactly.')
patch('COM_billing_efficiency', status='derived_display',
      formula='COM_billing_efficiency = 100 - NET_distribution_losses_pct = 100 * energy_billed_distribution_gwh / energy_injected_distribution_gwh')
note('COM_billing_efficiency', 'Not scored separately (exact complement of NET_distribution_losses_pct); displayed only.')
patch('COM_cash_recovery_index',
      formula='COM_cash_recovery_index (%) = (energy_billed_distribution_gwh / energy_injected_distribution_gwh) * min(1, cash_collected_lcu_m / revenue_billed_lcu_m) * 100. Uncapped value and 3-year average stored. ATC&C loss (%) = 100 - COM_cash_recovery_index.')
note('COM_cash_recovery_index', 'Review fix: collection can exceed 100% in arrears-recovery years; capped in the ranked value.')
patch('COM_receivables_days',
      formula='((trade_receivables_electricity_gross_lcu_m - tariff_compensation_receivable_lcu_m) / revenue_billed_lcu_m) * days_in_period, with revenue_billed_lcu_m on the same VAT basis as receivables (revenue_billed_vat_basis_code). Net-of-impairment variant stored.',
      raw_data_items=['trade_receivables_electricity_gross_lcu_m', 'trade_receivables_electricity_net_lcu_m', 'tariff_compensation_receivable_lcu_m', 'revenue_billed_lcu_m', 'revenue_billed_vat_basis_code', 'days_in_period'])
note('COM_receivables_days', 'Review fix: VAT basis aligned; State tariff-compensation receivables excluded; gross basis is the comparison basis (as for the public-sector variant).')
patch('INV_capex_per_new_connection',
      formula='capex_distribution_access_lcu_m * 1e6 / new_connections_count (gross connections only; suppressed when new_connections_count <= 0). Label: distribution capex per gross connection (upper bound).',
      raw_data_items=['capex_distribution_access_lcu_m', 'new_connections_count', 'fx_lcu_per_usd_avg'])
note('INV_capex_per_new_connection', 'Review fix: net customer change removed as denominator (can be zero or negative after database clean-ups).')
patch('INV_cwip_to_gross_ppe', formula='cwip_end_lcu_m / gross_ppe_incl_cwip_end_lcu_m * 100', raw_data_items=['cwip_end_lcu_m', 'gross_ppe_incl_cwip_end_lcu_m'])
patch('GOV_audit_opinion_code',
      formula='GOV_audit_opinion_code = lookup(audit_opinion_category, {unmodified_clean:5, unmodified_with_emphasis_or_going_concern:4, qualified:3, adverse:2, disclaimer:1}); not published / not available = NULL (separate state, not ranked; non-publication is captured by GOV_audited_fs_publication_lag_months). unmodified_with_emphasis_or_going_concern applies if emphasis_of_matter_flag = 1 OR going_concern_material_uncertainty_flag = 1.')
note('GOV_audit_opinion_code', 'Review fix: code 0 removed from the ordinal scale. The mapping of SYSCOHADA/OHADA "refus de certifier" to adverse vs disclaimer is a platform interpretation to validate with an OHADA audit specialist.')
k = kpis.pop('GOV_regulatory_reporting_compliance_flag'); k['id'] = 'GOV_regulatory_reporting_compliance_code'
k['formula'] = k['formula'].replace('GOV_regulatory_reporting_compliance_flag', 'GOV_regulatory_reporting_compliance_code'); kpis[k['id']] = k
note('GEN_available_capacity_ratio', 'Review: equality of capacity_reference_point must be a hard comparison filter in the platform, not only a stored flag.')
note('GEN_net_capacity_factor', 'Review: per NERC GADS, net capacity factor can be negative for units shut down all year (auxiliary consumption); handle explicitly.')
patch('NET_energy_not_supplied_pct',
      formula='100 * (energy_not_supplied_supply_shortfall_gwh + energy_not_supplied_network_gwh) / (energy_sent_out_gwh + energy_purchased_total_gwh - energy_exported_gwh + energy_not_supplied_supply_shortfall_gwh + energy_not_supplied_network_gwh); the two cause components are stored separately; fallback field (never mixed): load_shedding_hours_count.',
      raw_data_items=['energy_not_supplied_supply_shortfall_gwh', 'energy_not_supplied_network_gwh', 'energy_sent_out_gwh', 'energy_purchased_domestic_gwh', 'energy_imported_gwh', 'energy_exported_gwh', 'reported_energy_not_supplied_gwh', 'load_shedding_hours_count'])
note('NET_energy_not_supplied_pct', 'Merged with the former GEN_unserved_energy_ratio: one ENS record, one denominator, cause split (supply shortfall vs network faults).')
patch('CTX_market_structure', formula='CTX_market_structure = categorical(sector_model_code, entity_scope_code) + flags(is_single_buyer_flag, has_ipp_take_or_pay_flag, asset_holding_company_separate_flag). Purchase share: reference GEN_purchased_energy_share (not recomputed here).',
      raw_data_items=['sector_model_code', 'entity_scope_code', 'is_single_buyer_flag', 'has_ipp_take_or_pay_flag', 'asset_holding_company_separate_flag'])
patch('CTX_customer_base_size', formula='customers_total_count (year-end, active accounts; class and prepaid/postpaid breakdowns as raw items); binning variable = log10(customers_total_count). Prepaid share: see COM_prepaid_share.')
patch('CTX_supply_mix',
      formula='energy_available_gwh = energy_sent_out_gwh + energy_purchased_total_gwh (net basis, same denominator as GEN). Shares (sum to 100%): own hydro, own gas, own coal, own liquid fuel (energy_sent_out_liquid_fuel_gwh), own solar/wind/other, IPP purchases excluding emergency, emergency rental (counted only here, as liquid fuel), imports, other utilities. Liquid-fuel exposure: reference GEN_costly_thermal_share.')
note('CTX_supply_mix', 'Review fix: gross/net mixing and >100% double count (emergency rental in two shares) removed.')
patch('CTX_average_tariff_usd', status='derived_display',
      formula='Derived view: FIN_average_revenue_per_kwh_billed / fx_lcu_per_usd_avg (no separate extraction).', expected_availability='medium')
patch('CTX_currency_accounting_regime', formula='CTX_currency_accounting_regime = categorical(currency_regime_code, accounting_framework_code). Audit modification is derived from GOV audit_opinion_category, not stored here.')
note('INV_external_financing_share', 'Capital transfers count only in INV; operating transfers only in FIN_government_transfer_dependency (no double counting in composites).')
note('GEN_purchased_energy_share', 'energy_purchased_total_gwh = energy_purchased_domestic_gwh (IPP + emergency + other utilities) + energy_imported_gwh; derived, never extracted directly.')

# ---------------------------------------------------------------- availability downgrades (critic)
AVAIL = {
    'FIN_cost_recovery_ratio': 'medium', 'FIN_average_revenue_per_kwh_billed': 'medium', 'FIN_unit_cost_of_service_per_kwh_billed': 'medium',
    'FIN_ebitda_margin': 'medium', 'FIN_current_ratio': 'medium', 'FIN_government_transfer_dependency': 'low',
    'GEN_purchased_energy_share': 'medium', 'GEN_available_capacity_ratio': 'low', 'GEN_reserve_margin': 'low',
    'GEN_fuel_cost_per_kwh_thermal': 'low', 'GEN_net_capacity_factor': 'medium', 'NET_saidi_hours': 'low',
    'NET_saifi_count': 'low', 'COM_billing_efficiency': 'medium', 'COM_receivables_days': 'medium', 'COM_cash_recovery_index': 'low',
    'INV_capex_to_revenue': 'medium', 'INV_capex_to_depreciation': 'medium', 'INV_cwip_to_gross_ppe': 'medium',
    'INV_external_financing_share': 'low', 'GOV_regulatory_framework_score': 'medium',
}
for c in crit['availability_too_optimistic']:
    i = c['id']
    if i in kpis and i in AVAIL and kpis[i]['expected_availability'] != AVAIL[i]:
        kpis[i]['availability_rationale'] += f" [Review downgrade from {kpis[i]['expected_availability']}: {c['reason']} Suggested: {c['suggested']}.]"
        kpis[i]['expected_availability'] = AVAIL[i]

# ---------------------------------------------------------------- reference status corrections (critic)
for i in ('FIN_cost_recovery_ratio', 'FIN_quasi_fiscal_deficit_pct_gdp'):
    patch(i, reference_status='verified_existence_only')
    note(i, 'Reference: only the RePEc abstract of World Bank WPS 7788 was read (OKR page returned 403); the paper exists, but method-level claims are not verified.')
for i in ('NET_saidi_hours', 'NET_saifi_count'):
    patch(i, reference_status='verified_existence_only')
    note(i, 'Reference: the fetched URL is a third-party standards reseller, not IEEE. Cite IEEE Std 1366 by edition via the IEEE site and record the edition assumed.')
for i, msg in [('GOV_annual_reporting_disclosure_score', 'Alignment with RISE indicators is unverified (rise.esmap.org returned 403); claim dropped until checked.'),
               ('GOV_regulatory_framework_score', 'AfDB Electricity Regulatory Index and RISE overlaps cited from memory; indicator structure not verified.'),
               ('ACC_connection_time_days', 'Doing Business discontinuation is correct; the B-READY successor measure is unverified.'),
               ('COM_billing_efficiency', 'ATC&C attribution to Indian/Nigerian regulatory practice is from memory; no document fetched.')]:
    note(i, 'Reference: ' + msg)

# ---------------------------------------------------------------- KPIs added by the critic (short form)
ADDED = [
    dict(id='FIN_power_purchase_payables_days', dimension='FIN', name_fr='Délai de paiement des achats d’énergie et de combustible', name_en='Power purchase & fuel payables days',
         definition='Days of power-purchase and fuel cost outstanding in trade payables to IPPs, fuel and gas suppliers at year end. Overdue portion stored where disclosed. Main liquidity transmission channel and contingent fiscal liability.',
         formula='(payables_power_purchase_and_fuel_lcu_m / (power_purchase_cost_lcu_m + fuel_cost_own_generation_lcu_m)) * days_in_period; companion: overdue_power_purchase_payables_lcu_m',
         unit='days', direction='lower_better', raw_data_items=['payables_power_purchase_and_fuel_lcu_m', 'overdue_power_purchase_payables_lcu_m', 'power_purchase_cost_lcu_m', 'fuel_cost_own_generation_lcu_m', 'days_in_period'],
         typical_sources=['audited financial statements (payables note)', 'IPP / single-buyer disclosures', 'IMF / World Bank country reports on sector arrears'], expected_availability='medium', tier='core_mvp'),
    dict(id='FIN_interest_coverage_ratio', dimension='FIN', name_fr='Couverture des intérêts', name_en='Interest coverage ratio',
         definition='EBITDA excluding transfers divided by interest expense. Simpler and more widely available than DSCR.', formula='EBITDA_excl_transfers_lcu_m / interest_expense_lcu_m',
         unit='times', direction='higher_better', raw_data_items=['revenue_electricity_sales_lcu_m', 'other_operating_revenue_lcu_m', 'operating_expenses_excl_depreciation_lcu_m', 'interest_expense_lcu_m'],
         typical_sources=['audited financial statements'], expected_availability='medium', tier='extended'),
    dict(id='FIN_fx_debt_share', dimension='FIN', name_fr='Part de la dette en devises', name_en='Foreign-currency debt share',
         definition='Share of interest-bearing borrowings denominated in foreign currency at year end (devaluation exposure).', formula='borrowings_foreign_currency_lcu_m / total_borrowings_lcu_m * 100',
         unit='%', direction='lower_better', raw_data_items=['borrowings_foreign_currency_lcu_m', 'total_borrowings_lcu_m'],
         typical_sources=['audited financial statements (borrowings / financial risk note)'], expected_availability='medium', tier='extended'),
    dict(id='FIN_equity_to_assets', dimension='FIN', name_fr='Fonds propres / actif total', name_en='Equity to total assets',
         definition='Total equity divided by total assets at year end, with a negative-equity (technical insolvency) flag. Meaningful even when EBITDA is negative.', formula='total_equity_lcu_m / total_assets_lcu_m * 100; negative_equity_flag = total_equity_lcu_m < 0',
         unit='%', direction='higher_better', raw_data_items=['total_equity_lcu_m', 'total_assets_lcu_m'],
         typical_sources=['audited financial statements (balance sheet)'], expected_availability='medium', tier='extended'),
    dict(id='FIN_controllable_opex_per_kwh_billed', dimension='FIN', name_fr='Charges contrôlables par kWh facturé', name_en='Controllable opex per kWh billed',
         definition='Operating expenses excluding fuel, power purchases and bad-debt expense, per kWh billed: isolates costs management controls.',
         formula='(operating_expenses_excl_depreciation_lcu_m - fuel_cost_own_generation_lcu_m - power_purchase_cost_lcu_m - bad_debt_expense_lcu_m) / energy_billed_gwh',
         unit='LCU/kWh', direction='lower_better', raw_data_items=['operating_expenses_excl_depreciation_lcu_m', 'fuel_cost_own_generation_lcu_m', 'power_purchase_cost_lcu_m', 'bad_debt_expense_lcu_m', 'energy_billed_gwh'],
         typical_sources=['audited financial statements (expense notes)'], expected_availability='medium', tier='extended'),
    dict(id='OPS_customers_per_employee', dimension='OPS', name_fr='Clients par employé', name_en='Customers per employee',
         definition='Year-end customers divided by year-end permanent employees; contract/outsourced staff recorded separately. Standard labour-productivity benchmark.',
         formula='customers_total_count / employees_permanent_count; companion: customers_total_count / (employees_permanent_count + employees_contract_count)',
         unit='customers per employee', direction='higher_better', raw_data_items=['customers_total_count', 'employees_permanent_count', 'employees_contract_count'],
         typical_sources=['utility annual report (HR section)', 'regulator annual report'], expected_availability='medium', tier='core_mvp'),
    dict(id='COM_public_sector_receivables_share', dimension='COM', name_fr='Part des créances publiques', name_en='Public-sector receivables share',
         definition='Public-sector gross receivables as a share of total gross electricity trade receivables at year end; fallback when public-sector billing is not disclosed.',
         formula='receivables_public_sector_gross_lcu_m / trade_receivables_electricity_gross_lcu_m * 100',
         unit='%', direction='lower_better', raw_data_items=['receivables_public_sector_gross_lcu_m', 'trade_receivables_electricity_gross_lcu_m'],
         typical_sources=['audited financial statements (receivables note)'], expected_availability='medium', tier='extended'),
    dict(id='COM_bad_debt_expense_pct_revenue', dimension='COM', name_fr='Dotations pour créances douteuses / chiffre d’affaires', name_en='Bad-debt expense as % of revenue',
         definition='Impairment / bad-debt expense on trade receivables as a share of electricity sales revenue (accrual measure of collection failure).',
         formula='bad_debt_expense_lcu_m / revenue_electricity_sales_lcu_m * 100',
         unit='%', direction='lower_better', raw_data_items=['bad_debt_expense_lcu_m', 'revenue_electricity_sales_lcu_m'],
         typical_sources=['audited financial statements (income statement notes)'], expected_availability='medium', tier='extended'),
    dict(id='NET_hours_of_supply_per_day', dimension='NET', name_fr='Heures de fourniture par jour', name_en='Hours of supply per day',
         definition='Average daily hours of supply delivered to customers or feeders, as reported, with the weighting basis flagged. Used where SAIDI is absent.',
         formula='as reported: avg_supply_hours_per_day (feeder- or customer-weighted, flag supply_hours_weighting_basis)',
         unit='hours per day', direction='higher_better', raw_data_items=['avg_supply_hours_per_day', 'supply_hours_weighting_basis'],
         typical_sources=['regulator quarterly / annual reports', 'band-based tariff reports'], expected_availability='low', tier='extended'),
]
for a in ADDED:
    a.update(availability_rationale='Added at review stage; availability is a reviewer estimate, not yet checked against documents.',
             reference_definition='none', reference_status='none', reference_url='',
             comparability_pitfalls='To be completed during the document audit (step 1).',
             review_notes=['Added by the cross-dimension critic (gap in the drafts). Short-form entry, to be expanded.'],
             status='scored')
    kpis[a['id']] = a
dim_meta['OPS'] = {'name_en': 'Operational efficiency', 'rationale_en': 'Labour productivity, absent from all drafted sections (critic gap). Placeholder dimension for opex/staff efficiency.', 'open_questions_en': []}

# ---------------------------------------------------------------- core set (critic recommendation)
CORE = set(crit['core_mvp_recommendation'])
for i, k in kpis.items():
    k['tier'] = 'core_mvp' if i in CORE else 'extended'
missing_core = CORE - set(kpis)
assert not missing_core, missing_core

# ---------------------------------------------------------------- output
ORDER = ['FIN', 'GEN', 'NET', 'COM', 'OPS', 'GOV', 'INV', 'ACC', 'CTX']
by_dim = {d: sorted([k for k in kpis.values() if k['dimension'] == d], key=lambda k: (k['tier'] != 'core_mvp', k['id'])) for d in ORDER}

raw_items = {}
for k in kpis.values():
    for r in k['raw_data_items']:
        raw_items.setdefault(r, []).append(k['id'])

FIELDS = ['id', 'dimension', 'name_fr', 'name_en', 'status', 'tier', 'definition', 'formula', 'unit', 'direction', 'raw_data_items',
          'typical_sources', 'expected_availability', 'availability_rationale', 'reference_definition', 'reference_status', 'reference_url',
          'comparability_pitfalls', 'review_notes']
out = {
    'version': '0.1-draft',
    'status': 'Draft for expert review. Not validated against documents (step 1 audit pending). No benchmark values by design.',
    'dimensions': {d: {'name_fr': DIM_FR[d], **dim_meta[d]} for d in ORDER},
    'kpis': [{f: k.get(f) for f in FIELDS} for d in ORDER for k in by_dim[d]],
    'removed_as_duplicates': REMOVED,
    'raw_data_items': {r: sorted(v) for r, v in sorted(raw_items.items())},
    'critic': {k: crit[k] for k in ('overall_assessment', 'missing_kpis', 'suspicious_references', 'core_mvp_recommendation')},
}
json.dump(out, open(os.path.join(OUT_DIR, 'kpi_dictionary.json'), 'w'), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- markdown
AV = {'high': 'élevée', 'medium': 'moyenne', 'low': 'faible'}
DIR = {'higher_better': 'plus haut = mieux', 'lower_better': 'plus bas = mieux', 'target_range': 'plage cible', 'context_only': 'contexte (non noté)'}
REF = {'verified_by_fetch': 'vérifiée (URL consultée)', 'verified_existence_only': 'existence vérifiée, contenu non vérifié', 'from_memory_unverified': 'de mémoire, non vérifiée', 'none': 'aucune'}
STAT = {'scored': 'noté', 'context': 'contexte', 'derived_display': 'dérivé, affiché seulement'}

n_total = len(kpis)
n_scored = sum(1 for k in kpis.values() if k['status'] == 'scored')
n_core = sum(1 for k in kpis.values() if k['tier'] == 'core_mvp')
n_core_scored = sum(1 for k in kpis.values() if k['tier'] == 'core_mvp' and k['status'] == 'scored')
n_core_ctx = sum(1 for k in kpis.values() if k['tier'] == 'core_mvp' and k['dimension'] == 'CTX')
avail = {a: sum(1 for k in kpis.values() if k['tier'] == 'core_mvp' and k['status'] == 'scored' and k['expected_availability'] == a) for a in ('high', 'medium', 'low')}

L = []
w = L.append
w('# Dictionnaire de KPI : Africa Utility Intelligence (v0.1, brouillon)\n')
w('> **Statut : brouillon de travail destiné à une revue experte.** Les KPI n’ont pas encore été confrontés aux documents réellement publiés : c’est l’objet de l’étape 1 (audit de disponibilité). '
  'Le dictionnaire ne contient **aucune valeur de référence ni aucun seuil**, par choix : les benchmarks viendront des données extraites, pas d’hypothèses.\n')
w('## Résumé\n')
w(f'- **{n_total} entrées** : {n_scored} KPI notés, {sum(1 for k in kpis.values() if k["status"]=="context")} indicateurs de contexte ou descriptifs (non notés) et {sum(1 for k in kpis.values() if k["status"]=="derived_display")} indicateurs dérivés affichés seulement.')
w(f'- **Noyau MVP : {n_core} entrées**, soit {n_core_scored} KPI notés, {n_core - n_core_scored - n_core_ctx} indicateurs descriptifs (affichés, non notés) et {n_core_ctx} variables de contexte pour les groupes de pairs. '
  f'Disponibilité attendue des KPI notés du noyau : {avail["high"]} élevée, {avail["medium"]} moyenne, {avail["low"]} faible. '
  'Ces niveaux sont une estimation d’experts, pas un constat.')
w('- Les autres entrées forment le palier **étendu** : elles seront collectées quand elles sont disponibles, mais ne sont pas requises pour le score MVP.')
w(f'- {len(REMOVED)} doublons ont été supprimés et environ 20 noms de données brutes harmonisés. Les erreurs de formule relevées en revue ont été corrigées (voir « Méthode et corrections »).\n')
w('## Méthode et corrections\n')
w('Le dictionnaire a été produit en trois temps :\n')
w('1. **Rédaction** : 8 agents spécialisés, un par dimension, ont rédigé chacun une section. Consigne : aucune statistique, aucun seuil, aucune URL inventés ; une référence n’est marquée « vérifiée » que si l’URL a réellement été consultée.')
w('2. **Revue adversariale** : un agent critique a relu l’ensemble pour relever doublons, erreurs de formule, noms incohérents, disponibilités trop optimistes, KPI manquants et références douteuses.')
w('3. **Consolidation** : les corrections du critique ont été vérifiées contre les formules brutes, puis appliquées.\n')
w('**Corrections principales :**\n')
w('- **Quasi-fiscal deficit** : la formule comptait les pertes deux fois. Le coût unitaire étant calculé par kWh facturé, l’écart de tarif représente déjà la totalité de l’écart coût–recette. Le titre est désormais (Coût − Recette) + défaut de recouvrement.')
w('- **Bilan énergétique** : les importations étaient comptées deux fois (incluses dans les achats côté GEN, puis rajoutées côté NET). Les achats sont désormais scindés en `energy_purchased_domestic_gwh` + `energy_imported_gwh`, et `energy_purchased_total_gwh` n’est que leur somme dérivée.')
w('- **Pont NET/COM** : une donnée canonique unique, `energy_billed_distribution_gwh`, garantit que « efficacité de facturation = 100 − pertes de distribution ». Seules les pertes sont notées ; l’efficacité de facturation est seulement affichée.')
w('- **Couverture du service de la dette (DSCR)** : le numérateur est désormais le flux de trésorerie d’exploitation avant intérêts (l’EBITDA surestime la trésorerie quand les créances gonflent), et le principal des loyers est ajouté au service de la dette.')
w('- **Dette nette / EBITDA** : la version classée exclut les loyers, pour ne pas biaiser la comparaison entre IFRS 16 et SYSCOHADA.')
w('- **Coût O&M par km** : la conversion en USD a été corrigée (la division par km manquait).')
w('- **Opinion d’audit** : « non publié » sort de l’échelle ordinale. La non-publication est déjà mesurée par le délai de publication.')
w('- **Taux de recouvrement** : il est plafonné à 100 % dans l’indice de recouvrement de trésorerie classé (au-delà, il s’agit de récupération d’arriérés).')
w('- **Références** : 4 références marquées « vérifiées » ont été rétrogradées (lecture d’un résumé seulement, ou site revendeur au lieu de l’éditeur de la norme).\n')
w('Les **fiches détaillées** ci-dessous gardent les définitions techniques en anglais, telles que rédigées, avec un nom en français pour chaque KPI. '
  'La version lisible par machine est `kpi_dictionary.json`, qui contient aussi le glossaire complet des données brutes.\n')

w('## Vue d’ensemble : noyau MVP\n')
w('| ID | KPI | Dimension | Sens | Disponibilité attendue | Statut |')
w('|---|---|---|---|---|---|')
for d in ORDER:
    for k in by_dim[d]:
        if k['tier'] == 'core_mvp':
            w(f"| `{k['id']}` | {k['name_fr']} | {d} | {DIR[k['direction']]} | {AV[k['expected_availability']]} | {STAT[k['status']]} |")
w('')
w('## Vue d’ensemble : palier étendu\n')
w('| ID | KPI | Dimension | Disponibilité attendue | Statut |')
w('|---|---|---|---|---|')
for d in ORDER:
    for k in by_dim[d]:
        if k['tier'] != 'core_mvp':
            w(f"| `{k['id']}` | {k['name_fr']} | {d} | {AV[k['expected_availability']]} | {STAT[k['status']]} |")
w('')

w('## Règles transversales\n')
w('- **Unités** : énergie en GWh ; montants en millions de monnaie locale (`_lcu_m`) de l’exercice ; LCU m / GWh = LCU/kWh. Conversion en USD au cours moyen annuel (`fx_lcu_per_usd_avg`), en montrant aussi la série en LCU (les dévaluations de 2019-2025 au Nigeria, au Ghana et en Zambie dominent sinon les tendances).')
w('- **Valeurs absentes** : *Non publié* (la source ne donne pas l’information), *Non disponible* (aucune source trouvée), *Non trouvé*. Une valeur absente n’est jamais déduite.')
w('- **Variantes** : chaque KPI garde la valeur publiée par l’utility (`reported_*`) à côté de la valeur recalculée, avec son dénominateur déclaré.')
w('- **Comparabilité** : on ne classe jamais ensemble des utilities de périmètres différents (intégrée, distribution, production ou transport seuls).')
w('- **Transferts** : les transferts d’investissement ne comptent que dans INV, les transferts d’exploitation que dans FIN.')
w('- **Comptabilité** : SYSCOHADA et IFRS demandent une table de correspondance explicite des postes (EBE, subventions d’exploitation, trésorerie-passif, IFRS 16).\n')

for d in ORDER:
    m = out['dimensions'][d]
    w(f"## {d} : {DIM_FR[d]}\n")
    w(f"*{m['rationale_en']}*\n")
    for k in by_dim[d]:
        w(f"### `{k['id']}` : {k['name_fr']}")
        w(f"*{k['name_en']}* · palier **{'noyau MVP' if k['tier']=='core_mvp' else 'étendu'}** · {STAT[k['status']]} · {DIR[k['direction']]} · unité : {k['unit']}\n")
        w(f"- **Définition** : {k['definition']}")
        w(f"- **Formule** : `{k['formula']}`")
        w(f"- **Données brutes** : {', '.join('`'+r+'`' for r in k['raw_data_items'])}")
        w(f"- **Sources typiques** : {'; '.join(k['typical_sources'])}")
        w(f"- **Disponibilité attendue** : {AV[k['expected_availability']]}. {k['availability_rationale']}")
        ref = k['reference_definition']
        if k['reference_status'] != 'none' or (ref and ref != 'none'):
            url = f" <{k['reference_url']}>" if k.get('reference_url') else ''
            w(f"- **Référence** ({REF[k['reference_status']]}) : {ref}{url}")
        w(f"- **Pièges de comparaison** : {k['comparability_pitfalls']}")
        for n in k['review_notes']:
            w(f"- **Revue** : {n}")
        w('')
    if m['open_questions_en']:
        w(f"**Questions ouvertes ({d})**\n")
        for q in m['open_questions_en']:
            w(f"- {q}")
        w('')

w('## Doublons supprimés\n')
for i, r in REMOVED.items():
    w(f"- `{i}` : {r}")
w('\n## Avis global du critique\n')
w(crit['overall_assessment'] + '\n')
w('## Décisions à prendre avant l’extraction\n')
w('1. **Base du dénominateur des pertes** : recalculer à partir des volumes (énergie nette disponible) ou retenir la valeur publiée avec son dénominateur déclaré ? Proposition : stocker les deux, et classer sur la valeur recalculée seulement quand les volumes sont complets.')
w('2. **Base de coût** : coût comptable (amortissement + frais financiers) ou charge normative du capital (valeur de remplacement × WACC) ? Le coût comptable est traçable, mais faussé par les réévaluations et les actifs financés par dons.')
w('3. **Taux de pertes normatif** pour la décomposition du QFD : il faut une décision documentée, sans valeur inventée.')
w('4. **Marchés dégroupés** (Nigeria, Ghana, Kenya, Afrique du Sud) : mesurer au niveau de l’entité, du système, ou des deux ?')
w('5. **Date de coupure** des observations (pour le délai de publication des comptes) et distinction entre « non trouvé » et « absence vérifiée » dans les scores de gouvernance.')
w('6. **Méthode des groupes de pairs** : filtre strict sur le périmètre, puis 3 variables en classes (taille, revenu, mix). Voir les questions ouvertes de CTX : le petit nombre d’utilities et l’endogénéité sont les deux faiblesses majeures.')
w('7. **Validation experte** de la correspondance SYSCOHADA/OHADA pour les opinions d’audit (« refus de certifier »).')
w('')
open(os.path.join(OUT_DIR, 'KPI_DICTIONARY.md'), 'w').write('\n'.join(L))
print(f'total={n_total} scored={n_scored} core={n_core} core_scored={n_core_scored} avail={avail} raw_items={len(raw_items)}')
