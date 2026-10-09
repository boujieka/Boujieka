export const meta = {
  name: 'courant-extract',
  description: 'Extract sourced financial, energy and governance data from a utility\'s official documents, one agent per document, with page and verbatim quote for every value',
  phases: [{ title: 'Extract', detail: 'one agent per document' }],
}
// args: { dir, utility, context, docs: [{key, file, desc}] }
const A = args
const ITEMS = `
Monetary items are in LOCAL CURRENCY MILLIONS (suffix _lcu_m). Convert from thousands (/1000), units (/1e6) or billions (x1000) and say so in definition_note; state the currency in unit_as_printed.
ENERGY (GWh): energy_generated_gross_gwh, energy_sent_out_gwh (net own generation), energy_purchased_gwh (total; note scope), energy_purchased_ipp_gwh, energy_imported_gwh, energy_exported_gwh, energy_transmitted_gwh (transmission companies: energy received/delivered), energy_available_gwh (total system input), energy_sold_gwh (billed, total; note whether exports included), energy_sold_domestic_gwh, losses_total_pct_reported, losses_transmission_pct_reported, losses_distribution_pct_reported, losses_allowed_pct (regulator benchmark), atcc_losses_pct (aggregate technical, commercial & collection), availability_pct (plant or network availability), capacity_factor_pct, installed_capacity_mw, available_capacity_mw, peak_demand_mw, load_shedding_hours_or_days, unserved_energy_gwh.
COMMERCIAL: customers_total_count, customers_prepaid_count, metered_customers_count, new_connections_count, employees_count, collection_rate_pct_reported (state scope), billing_efficiency_pct, revenue_billed_lcu_m, cash_collected_lcu_m, average_tariff_lcu_per_kwh, saidi_hours, saifi.
FINANCIAL: revenue_total_lcu_m, revenue_electricity_sales_lcu_m, pass_through_revenue_lcu_m (fuel / FX / other pass-through), government_subsidy_or_compensation_lcu_m (tariff shortfall subsidy, compensation, grants recognised as income; say where booked), other_income_lcu_m, power_purchase_costs_lcu_m, fuel_costs_lcu_m, primary_energy_costs_lcu_m, staff_costs_lcu_m, maintenance_costs_lcu_m, depreciation_lcu_m, impairment_receivables_lcu_m, finance_costs_lcu_m, fx_losses_lcu_m, ebitda_lcu_m (as reported), operating_profit_lcu_m, profit_before_tax_lcu_m, net_profit_lcu_m, total_assets_lcu_m, equity_lcu_m, borrowings_total_lcu_m, borrowings_foreign_currency_lcu_m, government_guaranteed_debt_lcu_m, trade_payables_lcu_m, payables_energy_suppliers_lcu_m (IPPs, gencos, fuel, market operator), current_assets_lcu_m, current_liabilities_lcu_m, cash_lcu_m, overdraft_short_term_debt_lcu_m, capex_lcu_m, dividends_paid_lcu_m, trade_receivables_gross_lcu_m, trade_receivables_net_lcu_m, receivables_government_lcu_m (ministries, agencies, municipalities, state-owned customers), receivables_related_utilities_lcu_m (amounts due from other state utilities), government_equity_injection_or_debt_relief_lcu_m, cash_from_operations_lcu_m, debt_service_lcu_m.
REGULATORY: tariff_events (decision, date, % change), allowed_revenue_lcu_m (regulatory revenue requirement), revenue_gap_lcu_m.`

const RULES = `
You extract data for a sourced decision brief on ${A.utility}. ${A.context}
Work ONLY from the local text file given (pdftotext or OCR output of the official PDF; "=== PAGE n ===" markers = PDF page numbers). Do not use the web. Use grep/sed/Read; search keywords. OCR text may misread digits/symbols.
Rules (strict):
- Every value: page (PDF page from the nearest preceding marker) and quote = an EXACT verbatim substring of the text containing the number (25-200 chars, copy spacing and any OCR errors exactly; verified by string match).
- value_raw = number exactly as printed; value = numeric in target unit (fix OCR misreads only when certain; say so).
- fiscal_year = the year the value refers to. State the fiscal-year convention in document_notes (e.g. FY ends 31 March 2025 = fiscal_year 2025). Extract BOTH current and prior year, and every year of multi-year summary tables.
- Never compute or infer an unprinted value; omit missing items (list in not_found); record conflicting figures separately with notes.
- definition_note: scope (company vs group, restated, includes/excludes pass-through or subsidy, units converted).
Items (use these ids exactly; add an item with a clear snake_case id only if decision-critical and not listed):
${ITEMS}
SIGNALS (each with page + exact quote): audit opinion type and every qualification basis, emphasis of matter, going-concern material uncertainty, key audit matters, irregular/fruitless expenditure, PFMA/lawfulness findings; government arrears and support (bailouts, debt relief, guarantees, equity); disputes; restructuring/unbundling; tariff decisions; load shedding/blackouts; governance changes (CEO, board); strategic targets.`

const SCHEMA = {
  type: 'object',
  properties: {
    document: { type: 'string' },
    values: { type: 'array', items: { type: 'object', properties: {
      item: { type: 'string' }, fiscal_year: { type: 'integer' }, value: { type: 'number' }, value_raw: { type: 'string' },
      unit_as_printed: { type: 'string' }, page: { type: 'integer' }, quote: { type: 'string' }, definition_note: { type: 'string' },
    }, required: ['item', 'fiscal_year', 'value', 'value_raw', 'unit_as_printed', 'page', 'quote', 'definition_note'] } },
    signals: { type: 'array', items: { type: 'object', properties: {
      fiscal_year: { type: 'integer' }, category: { type: 'string', enum: ['audit', 'state_arrears', 'government_support', 'financing', 'dispute', 'tariff', 'load_shedding', 'governance', 'strategy', 'other'] },
      summary: { type: 'string' }, page: { type: 'integer' }, quote: { type: 'string' },
    }, required: ['fiscal_year', 'category', 'summary', 'page', 'quote'] } },
    not_found: { type: 'array', items: { type: 'string' } },
    document_notes: { type: 'string' },
  },
  required: ['document', 'values', 'signals', 'not_found', 'document_notes'],
}

phase('Extract')
const out = await parallel(A.docs.map(d => () =>
  agent(`${RULES}\n\nDocument: ${d.desc}\nFile: ${A.dir}/${d.file}`, { label: `extract:${d.key}`, phase: 'Extract', schema: SCHEMA })
    .then(r => r ? { key: d.key, files: [d.file], ...r } : null)))
const ok = out.filter(Boolean)
log(`${ok.length}/${A.docs.length} documents; ${ok.reduce((n, r) => n + r.values.length, 0)} values, ${ok.reduce((n, r) => n + r.signals.length, 0)} signals`)
return ok
