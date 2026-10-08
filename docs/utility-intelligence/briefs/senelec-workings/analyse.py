"""Build the curated, sourced dataset and derived indicators for the Senelec decision brief."""
import json, sys
S = sys.argv[1]
V = [v for v in json.load(open(f'{S}/verified.json'))['values'] if v['verified']]

def pick(item, year, doc=None, approx=None):
    c = [v for v in V if v['item'] == item and v['fiscal_year'] == year and (doc is None or v['doc'] == doc)]
    if approx is not None:
        c = [v for v in c if abs(v['value'] - approx) <= max(1e-6, abs(approx) * 0.002)]
    assert c, (item, year, doc, approx)
    v = c[0]
    return {'v': v['value'], 'src': f"{v['doc']} p.{v['found_page']}", 'quote': v['quote']}

Y = [2019, 2020, 2021, 2022, 2023, 2024]
D = {}
def series(name, spec):
    D[name] = {str(y): pick(*s) for y, s in spec.items()}

series('ca_total', {2019: ('turnover_total_mfcfa', 2019, 'ar2019', 509686.15), 2020: ('turnover_total_mfcfa', 2020, 'ar2020'), 2021: ('turnover_total_mfcfa', 2021, 'ar2021'),
                    2022: ('turnover_total_mfcfa', 2022, 'ar2022'), 2023: ('turnover_total_mfcfa', 2023, 'ar2023'), 2024: ('turnover_total_mfcfa', 2024, 'ar2024', 1015180)})
series('ecart_rma_booked', {y: ('tariff_compensation_mfcfa', y, f'ar{y}') for y in Y})
series('ebe', {y: ('ebe_mfcfa', y, f'ar{y}') for y in Y})
series('net_result', {y: ('net_result_mfcfa', y, f'ar{y}') for y in Y})
series('operating_result', {y: ('operating_result_mfcfa', y, f'ar{y}') for y in Y})
series('rma', {y: ('rma_mfcfa', y, 'crse', a) for y, a in {2020: 501620, 2021: 622890, 2022: 833696, 2023: 909637, 2024: 923777, 2025: 923712}.items()})
series('gap', {y: ('revenue_gap_mfcfa', y, 'crse', a) for y, a in {2020: 62748, 2021: 155283, 2022: 298463, 2023: 249280, 2024: 214721, 2025: 160338}.items()})
series('sales_rma_gwh', {y: ('energy_billed_gwh', y, 'crse', a) for y, a in {2020: 3861.25, 2022: 4821.96, 2024: 5455.40, 2025: 5867.53}.items()})
series('compensation_decided', {y: ('tariff_compensation_mfcfa', y, 'crse', a) for y, a in {2020: 41525, 2021: 166173, 2022: 298463, 2023: 249280, 2024: 222629, 2025: 181527}.items()})
series('energy_available', {2019: ('energy_total_available_gwh', 2019, 'ar2019', 4454), 2020: ('energy_total_available_gwh', 2020, 'ar2020', 4814.54), 2021: ('energy_total_available_gwh', 2021, 'ar2021', 5167.47),
                            2022: ('energy_total_available_gwh', 2022, 'ar2022', 5908.32), 2023: ('energy_total_available_gwh', 2023, 'ar2023', 6654.02), 2024: ('energy_total_available_gwh', 2024, 'ar2024', 7465.86)})
series('energy_billed', {2019: ('energy_billed_gwh', 2019, 'ar2019'), 2020: ('energy_billed_gwh', 2020, 'ar2020', 3895.36), 2021: ('energy_billed_gwh', 2021, 'ar2021'),
                         2022: ('energy_billed_gwh', 2022, 'ar2022'), 2023: ('energy_billed_gwh', 2023, 'ar2023'), 2024: ('energy_billed_gwh', 2024, 'ar2024')})
series('rendement_brut', {y: ('network_efficiency_pct_reported', y, f'ar{y}', a) for y, a in {2019: 81.14, 2020: 80.91, 2021: 81.11, 2022: 82.30, 2023: 81.22, 2024: 81.18}.items()})
series('avg_price', {y: ('average_tariff_fcfa_per_kwh', y, f'ar{y}', a) for y, a in {2019: 107.36, 2020: 114.66, 2021: 111.73, 2022: 110.18, 2023: 128.72, 2024: 127.23}.items()})
series('tccae', {y: ('collection_rate_pct_reported', y, f'ar{y}', a) for y, a in {2019: 92.71, 2020: 97.42, 2021: 107.75, 2022: 98.79, 2023: 94.65, 2024: 88.08}.items()})
series('recv_admin', {y: ('receivables_state_mfcfa', y, f'ar{y}', a) for y, a in {2019: 76802.74, 2020: 86614.70, 2021: 57480.29, 2022: 63092.82, 2023: 79146.03, 2024: 153543.88}.items()})
series('recv_commercial', {y: ('receivables_total_mfcfa', y, f'ar{y}', a) for y, a in {2019: 132119.12, 2020: 171290.57, 2021: 138060.78, 2022: 148775.72, 2023: 194865.08, 2024: 283640.68}.items()})
series('recv_balance', {y: ('receivables_total_mfcfa', y, f'ar{y}', a) for y, a in {2019: 185250, 2020: 194310, 2021: 137559, 2022: 189401.38, 2023: 236580, 2024: 324200}.items()})
series('current_assets', {y: ('current_assets_mfcfa', y, f'ar{y}') for y in Y})
series('current_liab', {y: ('current_liabilities_mfcfa', y, f'ar{y}') for y in Y})
series('st_bank_debt', {2019: ('financial_debt_mfcfa', 2019, 'ar2019'), 2021: ('financial_debt_mfcfa', 2021, 'ar2021', 105467)})
series('energy_purchases', {2021: ('energy_purchases_mfcfa', 2021, 'ar2022'), 2022: ('energy_purchases_mfcfa', 2022, 'ar2022'), 2023: ('energy_purchases_mfcfa', 2023, 'ar2023'), 2024: ('energy_purchases_mfcfa', 2024, 'ar2024')})
series('saidi', {y: ('saidi_or_tmc_hours', y, f'ar{y}', a) for y, a in {2019: 10.09, 2020: 4.84, 2021: 7.59, 2022: 14.34, 2023: 7.32, 2024: 6.67}.items()})
series('customers', {2019: ('customers_total_count', 2019, 'ar2019'), 2020: ('customers_total_count', 2020, 'ar2020'), 2021: ('customers_total_count', 2021, 'ar2021'),
                     2022: ('customers_total_count', 2022, 'ar2022'), 2024: ('customers_total_count', 2024, 'ar2024')})
series('employees', {2019: ('employees_count', 2019, 'ar2019', 3138), 2020: ('employees_count', 2020, 'ar2020'), 2021: ('employees_count', 2021, 'ar2021'),
                     2022: ('employees_count', 2022, 'ar2022'), 2023: ('employees_count', 2023, 'ar2023'), 2024: ('employees_count', 2024, 'ar2024')})
series('cash_active', {y: ('cash_mfcfa', y, f'ar{y}') for y in Y})

g = lambda n, y: D[n][str(y)]['v']
C = {}
C['ebe_excl_comp'] = {y: g('ebe', y) - g('ecart_rma_booked', y) for y in Y}
C['comp_share_ca'] = {y: 100 * g('ecart_rma_booked', y) / g('ca_total', y) for y in Y}
C['tariff_revenue'] = {y: g('rma', y) - g('gap', y) for y in range(2020, 2026)}
C['coverage'] = {y: 100 * C['tariff_revenue'][y] / g('rma', y) for y in range(2020, 2026)}
C['rma_per_kwh'] = {y: g('rma', y) / g('sales_rma_gwh', y) for y in (2020, 2022, 2024, 2025)}
C['tariff_per_kwh'] = {y: C['tariff_revenue'][y] / g('sales_rma_gwh', y) for y in (2020, 2022, 2024, 2025)}
C['gap_per_kwh'] = {y: g('gap', y) / g('sales_rma_gwh', y) for y in (2020, 2022, 2024, 2025)}
C['gap_vs_tariff_rev_2025'] = 100 * g('gap', 2025) / C['tariff_revenue'][2025]
C['losses_implied'] = {y: 100 - g('rendement_brut', y) for y in Y}
C['loss_point_gwh_2024'] = g('energy_available', 2024) / 100
C['loss_point_value_2024'] = C['loss_point_gwh_2024'] * g('avg_price', 2024)  # GWh * FCFA/kWh = MFCFA
C['loss_point_share_gap_2024'] = 100 * C['loss_point_value_2024'] / g('gap', 2024)
C['current_ratio'] = {y: g('current_assets', y) / g('current_liab', y) for y in Y}
C['recv_days_ca'] = {y: 365 * g('recv_balance', y) / g('ca_total', y) for y in Y}
C['admin_recv_growth_2024'] = 100 * (153543.88 / 84436.48 - 1)
C['cust_per_employee_2024'] = g('customers', 2024) / g('employees', 2024)
json.dump({'series': D, 'computed': C}, open(f'{S}/brief_data.json', 'w'), ensure_ascii=False, indent=1)
for k, v in C.items():
    print(k, {a: round(b, 1) for a, b in v.items()} if isinstance(v, dict) else round(v, 2))
