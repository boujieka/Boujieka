"""Generate the Senelec decision brief (artifact HTML) from brief_data.json. Every number comes from the data file."""
import json, sys, html
S, OUT = sys.argv[1], sys.argv[2]
B = json.load(open(f'{S}/brief_data.json'))
D, C = B['series'], B['computed']
ver = json.load(open(f'{S}/verified.json'))['summary']

URL = {
 'ar2019': 'https://www.senelec.sn/media/rapports/pdf/ras2019.pdf',
 'ar2020': 'https://www.senelec.sn/media/rapports/pdf/rapport-annuel-senelec-2020-ok1693835980.pdf',
 'ar2021': 'https://www.senelec.sn/media/rapports/pdf/ras2021.pdf',
 'ar2022': 'https://www.senelec.sn/media/rapports/pdf/rapport-annuel-senelec-2022-compressed1693835195.pdf',
 'ar2023': 'https://www.senelec.sn/media/rapports/pdf/rapport-annuel-senelec-2023-vf-ok1745314522.pdf',
 'ar2024': 'https://www.senelec.sn/media/rapports/pdf/rapport-annuel-senelec-20241760024319_1.pdf',
 'crse2020_21': 'https://www.crse.sn/wp-content/uploads/2026/03/RAPPORT-ANNUEL-CRSE-2020-2021.PDF.pdf',
 'crse2022_23': 'https://www.crse.sn/wp-content/uploads/2026/03/RAPPORT-ACTIVITES-CRSE-2022-2023_COMPRESSED-2.PDF.pdf',
 'crse2024': 'https://www.crse.sn/wp-content/uploads/2026/03/RAPPORT-ANNUEL-2024-CRSE-VF.pdf',
 'crse2025': 'https://www.crse.sn/wp-content/uploads/2026/09/Rapport-CRSE-2025_Digital.pdf',
}
LABEL = {'ar2019': 'RA 2019', 'ar2020': 'RA 2020', 'ar2021': 'RA 2021', 'ar2022': 'RA 2022', 'ar2023': 'RA 2023', 'ar2024': 'RA 2024',
         'crse2020_21': 'CRSE 2020-21', 'crse2022_23': 'CRSE 2022-23', 'crse2024': 'CRSE 2024', 'crse2025': 'CRSE 2025'}

# map 'crse pNN' sources to the right CRSE file using the verified records
VV = json.load(open(f'{S}/verified.json'))['values']
def file_for(item_quote):
    for v in VV:
        if v['quote'] == item_quote and v['verified']:
            return v['file'].replace('.txt', '')
    return None

def ref(series, year):
    r = D[series][str(year)]
    doc, page = r['src'].split(' p.')
    key = doc if doc != 'crse' else file_for(r['quote'])
    return f'<a class="ref" href="{URL[key]}" title="{html.escape(r["quote"].strip())}" target="_blank" rel="noopener">{LABEL[key]} p.{page}</a>'

def sref(key, page, quote=''):
    return f'<a class="ref" href="{URL[key]}" title="{html.escape(quote)}" target="_blank" rel="noopener">{LABEL[key]} p.{page}</a>'

def v(series, year): return D[series][str(year)]['v']
def bn(x, d=1):  # MFCFA -> milliards FCFA, French format
    s = f'{x/1000:,.{d}f}'.replace(',', ' ').replace('.', ',')
    return s
def num(x, d=1):
    return f'{x:,.{d}f}'.replace(',', ' ').replace('.', ',')

tag = lambda t: {'f': '<span class="tag f">fait sourcé</span>', 'c': '<span class="tag c">calcul</span>', 'i': '<span class="tag i">interprétation</span>'}[t]

# ---------- chart 1: RMA = tariff revenue + gap, 2020-2025 ----------
yrs = [2020, 2021, 2022, 2023, 2024, 2025]
W, H, L, R, T, Bm = 640, 300, 56, 16, 20, 40
maxv = 1000000
sx = lambda i: L + i * (W - L - R) / len(yrs) + 14
bw = (W - L - R) / len(yrs) - 28
sy = lambda val: T + (H - T - Bm) * (1 - val / maxv)
g1 = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Revenu maximum autorisé de Senelec, part couverte par les tarifs et écart compensé par l’État, 2020 à 2025">']
for t in range(0, 1000001, 250000):
    y = sy(t)
    g1.append(f'<line class="grid" x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}"/><text class="axis" x="{L-8}" y="{y+4:.1f}" text-anchor="end">{t//1000:,}</text>'.replace(',', ' '))
for i, y in enumerate(yrs):
    tr, gap = C['tariff_revenue'][str(y)] if isinstance(list(C['tariff_revenue'].keys())[0], str) else C['tariff_revenue'][y], v('gap', y)
    x = sx(i)
    g1.append(f'<rect class="b-tariff" x="{x:.1f}" y="{sy(tr):.1f}" width="{bw:.1f}" height="{sy(0)-sy(tr):.1f}"/>')
    g1.append(f'<rect class="b-gap" x="{x:.1f}" y="{sy(tr+gap):.1f}" width="{bw:.1f}" height="{sy(tr)-sy(tr+gap):.1f}"/>')
    cov = C['coverage'][str(y)] if isinstance(list(C['coverage'].keys())[0], str) else C['coverage'][y]
    g1.append(f'<text class="lbl" x="{x+bw/2:.1f}" y="{sy(tr+gap)-6:.1f}" text-anchor="middle">{num(cov,0)} %</text>')
    g1.append(f'<text class="axis" x="{x+bw/2:.1f}" y="{H-Bm+18}" text-anchor="middle">{y}</text>')
g1.append(f'<text class="axis" x="{L}" y="{H-6}">Mds FCFA · étiquette = part du RMA couverte par les tarifs</text></svg>')
chart1 = ''.join(g1)

# ---------- chart 2: EBE reported vs EBE excluding compensation ----------
Y6 = [2019, 2020, 2021, 2022, 2023, 2024]
W2, H2, L2 = 640, 300, 56
lo, hi = -250000, 150000
sy2 = lambda val: T + (H2 - T - Bm) * (hi - val) / (hi - lo)
step = (W2 - L2 - R) / len(Y6)
g2 = [f'<svg class="chart" viewBox="0 0 {W2} {H2}" role="img" aria-label="Excédent brut d’exploitation publié et hors compensation tarifaire, 2019 à 2024">']
for t in range(-250000, 150001, 50000):
    y = sy2(t)
    g2.append(f'<line class="{"zero" if t == 0 else "grid"}" x1="{L2}" x2="{W2-R}" y1="{y:.1f}" y2="{y:.1f}"/><text class="axis" x="{L2-8}" y="{y+4:.1f}" text-anchor="end">{t//1000}</text>')
cw = step / 2 - 10
for i, y in enumerate(Y6):
    x0 = L2 + i * step + 8
    e, ex = v('ebe', y), C['ebe_excl_comp'][str(y)] if isinstance(list(C['ebe_excl_comp'].keys())[0], str) else C['ebe_excl_comp'][y]
    for j, (val, cls) in enumerate(((e, 'b-ebe'), (ex, 'b-ex'))):
        top, bot = (sy2(val), sy2(0)) if val >= 0 else (sy2(0), sy2(val))
        g2.append(f'<rect class="{cls}" x="{x0 + j*(cw+4):.1f}" y="{top:.1f}" width="{cw:.1f}" height="{bot-top:.1f}"/>')
    g2.append(f'<text class="lbl" x="{x0 + cw + 4 + cw/2:.1f}" y="{(sy2(ex)+14) if ex < 0 else (sy2(ex)-6):.1f}" text-anchor="middle">{num(ex/1000,0)}</text>')
    g2.append(f'<text class="axis" x="{x0 + cw + 2:.1f}" y="{H2-Bm+18}" text-anchor="middle">{y}</text>')
g2.append(f'<text class="axis" x="{L2}" y="{H2-6}">Mds FCFA</text></svg>')
chart2 = ''.join(g2)

# ---------- chart 3: public-administration receivables (Dec) ----------
W3, H3, L3 = 640, 240, 56
mx = 175000
sy3 = lambda val: T + (H3 - T - Bm) * (1 - val / mx)
st3 = (W3 - L3 - R) / len(Y6)
g3 = [f'<svg class="chart" viewBox="0 0 {W3} {H3}" role="img" aria-label="Créances de Senelec sur l’Administration en fin d’année, 2019 à 2024">']
for t in range(0, 175001, 50000):
    y = sy3(t)
    g3.append(f'<line class="grid" x1="{L3}" x2="{W3-R}" y1="{y:.1f}" y2="{y:.1f}"/><text class="axis" x="{L3-8}" y="{y+4:.1f}" text-anchor="end">{t//1000}</text>')
for i, y in enumerate(Y6):
    x = L3 + i * st3 + 14; w = st3 - 28; val = v('recv_admin', y)
    g3.append(f'<rect class="{"b-alert" if y == 2024 else "b-tariff"}" x="{x:.1f}" y="{sy3(val):.1f}" width="{w:.1f}" height="{sy3(0)-sy3(val):.1f}"/>')
    g3.append(f'<text class="lbl" x="{x+w/2:.1f}" y="{sy3(val)-6:.1f}" text-anchor="middle">{num(val/1000,1)}</text>')
    g3.append(f'<text class="axis" x="{x+w/2:.1f}" y="{H3-Bm+18}" text-anchor="middle">déc. {y}</text>')
g3.append(f'<text class="axis" x="{L3}" y="{H3-6}">Mds FCFA · créances commerciales sur l’Administration (hors compensation due)</text></svg>')
chart3 = ''.join(g3)

def cget(k, y):
    d = C[k]; return d[str(y)] if str(y) in d else d[y]

P = {}
P['gap22'], P['gap25'] = bn(v('gap', 2022)), bn(v('gap', 2025))
P['cov22'], P['cov25'] = num(cget('coverage', 2022), 0), num(cget('coverage', 2025), 0)
P['gpk22'], P['gpk25'] = num(cget('gap_per_kwh', 2022)), num(cget('gap_per_kwh', 2025))
P['rpk22'], P['rpk25'] = num(cget('rma_per_kwh', 2022)), num(cget('rma_per_kwh', 2025))
P['tpk22'], P['tpk25'] = num(cget('tariff_per_kwh', 2022)), num(cget('tariff_per_kwh', 2025))
P['gapshare25'] = num(C['gap_vs_tariff_rev_2025'], 0)
P['ebex22'], P['ebex24'] = bn(cget('ebe_excl_comp', 2022), 0), bn(cget('ebe_excl_comp', 2024), 0)
P['comp22'], P['comp24'] = num(cget('comp_share_ca', 2022), 0), num(cget('comp_share_ca', 2024), 0)
P['adm23'], P['adm24'] = bn(84436.48), bn(v('recv_admin', 2024))
P['admg'] = num(C['admin_recv_growth_2024'], 0)
P['cr19'], P['cr24'] = num(cget('current_ratio', 2019), 2), num(cget('current_ratio', 2024), 2)
P['rd22'], P['rd24'] = num(cget('recv_days_ca', 2022), 0), num(cget('recv_days_ca', 2024), 0)
P['loss_pt_gwh'] = num(C['loss_point_gwh_2024'], 0)
P['loss_pt_bn'] = bn(C['loss_point_value_2024'], 1)
P['loss_pt_share'] = num(C['loss_point_share_gap_2024'], 1)
P['cpe'] = num(C['cust_per_employee_2024'], 0)

page = f'''<title>Note Senelec 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112..125,500..800&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: one 820px reading column (decision memo); charts full column width; sources as mono chips after each figure. Courant tokens. */
:root {{
  --bg: #eef0ec; --surface: #f8f9f6; --plate: #e2e6df; --fg: #14211f; --muted: #4d5b57; --line: #c7cec7;
  --accent: #e3a90b; --accent-ink: #8a5a00; --copper: #a84d24; --good: #2f7a4f; --bad: #a83a2a; --gap: #d9a514;
  --display: "Archivo", "Arial Narrow", Arial, sans-serif; --body: "Public Sans", "Segoe UI", system-ui, sans-serif; --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg: #0f1615; --surface: #151e1c; --plate: #1c2725; --fg: #e4e9e5; --muted: #a2afaa; --line: #2c3a37; --accent: #f2c230; --accent-ink: #f2c230; --copper: #e08a5b; --good: #6cc391; --bad: #ec7b68; --gap: #f2c230; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --bg: #0f1615; --surface: #151e1c; --plate: #1c2725; --fg: #e4e9e5; --muted: #a2afaa; --line: #2c3a37; --accent: #f2c230; --accent-ink: #f2c230; --copper: #e08a5b; --good: #6cc391; --bad: #ec7b68; --gap: #f2c230; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--fg); font: 16px/1.65 var(--body); padding-inline: 20px; padding-block: 28px 72px; }}
.wrap {{ max-width: 820px; margin-inline: auto; display: grid; gap: 44px; }}
h1, h2, h3 {{ font-family: var(--display); font-stretch: 118%; margin: 0; line-height: 1.12; text-wrap: balance; }}
h1 {{ font-size: clamp(1.9rem, 4.6vw, 2.8rem); font-weight: 800; }}
h2 {{ font-size: 1.45rem; font-weight: 750; }}
h3 {{ font-size: 1.02rem; font-weight: 700; font-stretch: 112%; }}
p {{ margin: 0; }}
a {{ color: inherit; }}
:focus-visible {{ outline: 3px solid var(--accent); outline-offset: 2px; }}
.eyebrow {{ font-family: var(--mono); font-size: .76rem; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}
.top {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; padding-bottom: 14px; border-bottom: 1px solid var(--line); }}
.top svg {{ height: 22px; width: auto; }}
.proto {{ font-family: var(--mono); font-size: .72rem; padding: 3px 8px; border: 1px dashed var(--muted); color: var(--muted); border-radius: 2px; }}
header.intro {{ display: grid; gap: 14px; }}
.meta {{ color: var(--muted); font-size: .95rem; }}
.question {{ background: var(--surface); border: 1px solid var(--line); border-left: 4px solid var(--accent); padding: 18px 20px; border-radius: 3px; display: grid; gap: 6px; }}
.keys {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 0; border-top: 1px solid var(--line); }}
.keys li {{ display: grid; grid-template-columns: 9.5rem minmax(0, 1fr); gap: 18px; padding-block: 14px; border-bottom: 1px solid var(--line); }}
.keys .k {{ font-family: var(--display); font-stretch: 125%; font-weight: 800; font-size: 1.5rem; line-height: 1.1; font-variant-numeric: tabular-nums; }}
.keys .k small {{ display: block; font-family: var(--mono); font-size: .7rem; font-weight: 400; color: var(--muted); letter-spacing: .04em; margin-top: 4px; }}
@media (max-width: 560px) {{ .keys li {{ grid-template-columns: 1fr; gap: 4px; }} }}
section {{ display: grid; gap: 16px; }}
section > p, section li {{ max-width: 68ch; }}
.ref {{ font-family: var(--mono); font-size: .72rem; color: var(--muted); text-decoration: none; border-bottom: 1px dotted var(--muted); white-space: nowrap; }}
.ref:hover {{ color: var(--fg); }}
.tag {{ font-family: var(--mono); font-size: .66rem; letter-spacing: .05em; text-transform: uppercase; padding: 1px 6px; border-radius: 2px; vertical-align: 2px; white-space: nowrap; }}
.tag.f {{ background: var(--plate); color: var(--fg); }}
.tag.c {{ border: 1px solid var(--muted); color: var(--muted); }}
.tag.i {{ border: 1px dashed var(--copper); color: var(--copper); }}
figure {{ margin: 0; background: var(--surface); border: 1px solid var(--line); border-radius: 4px; padding: 16px 16px 12px; display: grid; gap: 8px; min-width: 0; }}
figcaption {{ font-size: .88rem; color: var(--muted); }}
.chart {{ width: 100%; height: auto; display: block; }}
.chart text {{ font-family: var(--mono); fill: var(--muted); font-size: 11px; }}
.chart .lbl {{ fill: var(--fg); font-size: 12px; }}
.chart .grid {{ stroke: var(--line); stroke-width: 1; }}
.chart .zero {{ stroke: var(--fg); stroke-width: 1.2; }}
.chart .b-tariff {{ fill: var(--fg); }}
.chart .b-gap {{ fill: var(--gap); }}
.chart .b-ebe {{ fill: var(--fg); }}
.chart .b-ex {{ fill: var(--copper); }}
.chart .b-alert {{ fill: var(--copper); }}
.legend {{ display: flex; flex-wrap: wrap; gap: 14px; font-size: .82rem; color: var(--muted); }}
.legend span::before {{ content: ""; display: inline-block; width: 10px; height: 10px; margin-right: 6px; vertical-align: -1px; background: var(--sw); }}
table {{ border-collapse: collapse; width: 100%; font-size: .9rem; font-variant-numeric: tabular-nums; }}
th, td {{ text-align: right; padding: 7px 8px; border-bottom: 1px solid var(--line); white-space: nowrap; }}
th:first-child, td:first-child {{ text-align: left; white-space: normal; }}
th {{ font-weight: 600; font-size: .8rem; color: var(--muted); }}
.tablewrap {{ overflow-x: auto; }}
.options {{ display: grid; gap: 12px; }}
.opt {{ background: var(--surface); border: 1px solid var(--line); border-radius: 4px; padding: 16px 18px; display: grid; gap: 6px; }}
.opt .what {{ font-size: .92rem; color: var(--muted); }}
ul {{ margin: 0; padding-left: 20px; display: grid; gap: 6px; }}
.limits {{ font-size: .92rem; }}
.limits li {{ color: var(--muted); }}
footer {{ font-size: .82rem; color: var(--muted); border-top: 1px solid var(--line); padding-top: 16px; display: grid; gap: 6px; }}
</style>

<div class="wrap">
  <div class="top">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -700 5630 740" role="img" aria-label="Courant"><rect x="0" y="-660" width="640" height="160" fill="currentColor"/><rect x="0" y="-410" width="461" height="160" fill="currentColor"/><rect x="479" y="-410" width="161" height="160" fill="var(--accent)"/><rect x="0" y="-160" width="390" height="160" fill="currentColor"/><path transform="translate(860 0)" fill="currentColor" d="M387.9 12Q283 12 206.1 -18.5Q129.3 -49 87.6 -110.3Q45.9 -171.6 45.9 -264Q45.9 -356.4 87.6 -417.6Q129.3 -478.8 206.1 -509.1Q283 -539.4 387.9 -539.4Q455.4 -539.4 514.5 -525.7Q573.7 -512 618.7 -484.1Q663.7 -456.2 688.8 -414.8Q713.8 -373.5 713.8 -318.7H538.5Q538.5 -349.7 518.2 -372.2Q498 -394.6 464.1 -406.5Q430.2 -418.4 387.9 -418.4Q334.8 -418.4 298.4 -400.8Q262 -383.2 243.6 -350.9Q225.2 -318.6 225.2 -274V-254Q225.2 -210 244.1 -177.4Q263 -144.8 300.8 -126.9Q338.6 -109 394.5 -109Q436.3 -109 470.4 -122.1Q504.5 -135.2 524.8 -158.2Q545.1 -181.1 545.1 -209.7H713.8Q713.8 -153.5 688.5 -111.7Q663.1 -69.8 618.6 -42.4Q574.1 -15 514.7 -1.5Q455.4 12 387.9 12Z M1136.2 12Q1031.9 12 955.1 -18.8Q878.2 -49.6 836.2 -110.9Q794.2 -172.2 794.2 -264Q794.2 -356.4 836.2 -417.6Q878.2 -478.8 955.1 -509.1Q1031.9 -539.4 1136.2 -539.4Q1240.5 -539.4 1317.4 -509.1Q1394.2 -478.8 1436.2 -417.6Q1478.2 -356.4 1478.2 -264Q1478.2 -172.2 1436.2 -110.9Q1394.2 -49.6 1317.4 -18.8Q1240.5 12 1136.2 12ZM1136.2 -109Q1189.3 -109 1225.7 -126.9Q1262.1 -144.8 1280.5 -177.4Q1298.9 -210 1298.9 -254V-274Q1298.9 -318.6 1280.5 -350.9Q1262.1 -383.2 1225.7 -400.8Q1189.3 -418.4 1136.2 -418.4Q1083.1 -418.4 1046.7 -400.8Q1010.4 -383.2 992 -350.9Q973.6 -318.6 973.6 -274V-254Q973.6 -210 992 -177.4Q1010.4 -144.8 1046.7 -126.9Q1083.1 -109 1136.2 -109Z M1804.5 12Q1691.2 12 1633.4 -42.5Q1575.7 -97 1575.7 -207.2V-527.4H1749.2V-232.4Q1749.2 -203.8 1757.3 -182.4Q1765.3 -160.9 1780.6 -147.3Q1795.8 -133.8 1818 -127.1Q1840.2 -120.5 1868.2 -120.5Q1908.9 -120.5 1942.8 -137.1Q1976.8 -153.6 1997.3 -183.2Q2017.8 -212.7 2017.8 -251.1V-527.4H2191.3V0H2051L2038.9 -88.3H2029.9Q2002.3 -51 1965.2 -29.2Q1928.1 -7.4 1886.9 2.3Q1845.7 12 1804.5 12Z M2314.5 0V-527.4H2454.8L2466.8 -437.3H2475.3Q2489.6 -468.2 2513 -491.4Q2536.5 -514.5 2567.8 -527.2Q2599.1 -539.8 2635.4 -539.8Q2655 -539.8 2673 -537.1Q2690.9 -534.4 2706.5 -528.6V-389H2623.5Q2587.2 -389 2561.6 -377.2Q2535.9 -365.3 2519.7 -345Q2503.6 -324.7 2495.8 -299.2Q2488 -273.8 2488 -245.6V0Z M2978 12Q2929.3 12 2887.4 4.7Q2845.5 -2.6 2814.1 -20.1Q2782.8 -37.6 2765.4 -67.8Q2748 -98 2748 -144.2Q2748 -207.8 2782.4 -244Q2816.7 -280.2 2879.9 -296.9Q2943.1 -313.5 3028.6 -317.9Q3114.1 -322.3 3216.2 -322.3V-339.8Q3216.2 -370.9 3200.7 -389.4Q3185.2 -408 3154.4 -416.1Q3123.7 -424.2 3076.3 -424.2Q3041.2 -424.2 3010.5 -419.2Q2979.8 -414.2 2960.8 -403.3Q2941.8 -392.3 2941.8 -373.9V-365.2H2766.7Q2765.7 -369.2 2765.4 -372.6Q2765.1 -375.9 2765.1 -380.5Q2765.1 -427.5 2801.4 -463.3Q2837.6 -499.2 2909.2 -519.3Q2980.7 -539.4 3086.5 -539.4Q3184.5 -539.4 3252.1 -522.2Q3319.7 -505 3354.7 -466.4Q3389.7 -427.8 3389.7 -362.7V-148Q3389.7 -130.3 3397.4 -119.7Q3405.1 -109 3422.8 -109H3475.5V-6.2Q3462.2 -1 3432.4 5.5Q3402.6 12 3368.1 12Q3320 12 3291.6 1.6Q3263.1 -8.8 3249.5 -26.5Q3235.9 -44.3 3230.3 -65.6H3222.3Q3193.9 -41.7 3156.3 -23.9Q3118.8 -6.2 3074 2.9Q3029.2 12 2978 12ZM3025.6 -102.8Q3050.6 -102.8 3082.8 -108.4Q3114.9 -114 3145.7 -125.6Q3176.4 -137.2 3196.3 -155.5Q3216.2 -173.7 3216.2 -199.5V-228.9Q3114.5 -228.9 3048.8 -221Q2983.2 -213.1 2951.7 -196.3Q2920.3 -179.6 2920.3 -151.5Q2920.3 -130.8 2935.7 -120.4Q2951.1 -110 2975.5 -106.4Q2999.9 -102.8 3025.6 -102.8Z M3531.5 0V-527.4H3671.8L3683.8 -439.1H3692.8Q3721 -476.4 3757.8 -498.2Q3794.6 -520 3836.1 -529.7Q3877.6 -539.4 3918.3 -539.4Q3994.3 -539.4 4045.1 -515.4Q4095.8 -491.3 4121.4 -442.7Q4147 -394 4147 -320.2V0H3973.5V-295Q3973.5 -323.6 3965.5 -345Q3957.4 -366.5 3942.2 -380.1Q3927 -393.7 3904.9 -400.3Q3882.9 -406.9 3854.6 -406.9Q3813.9 -406.9 3779.9 -390.3Q3746 -373.8 3725.5 -344.5Q3705 -315.2 3705 -276.3V0Z M4519.8 12Q4456 12 4413.4 -3.2Q4370.8 -18.3 4349.6 -55.4Q4328.3 -92.5 4328.3 -158.3V-406.4H4225.7V-527.4H4334.4L4369 -683.9H4501.8V-527.4H4648.1V-406.4H4501.8V-186.5Q4501.8 -148.7 4517.2 -128.9Q4532.5 -109 4581.6 -109H4648.1V-5.8Q4634.1 -0.8 4610.4 3.4Q4586.6 7.6 4562.1 9.8Q4537.6 12 4519.8 12Z"/></svg>
    <span class="proto">Prototype · note générée à partir des documents publics</span>
  </div>

  <header class="intro">
    <span class="eyebrow">Note de décision · Senelec (Sénégal) · données 2019-2025 · octobre 2026</span>
    <h1>L’écart tarifaire de Senelec se réduit. Le risque se déplace vers les impayés publics.</h1>
    <p class="meta">Destinataires : Ministère des Finances et du Budget, Ministère de l’Énergie, CRSE, bailleurs. Sources : six rapports annuels de Senelec (2019 à 2024) et quatre rapports de la CRSE (2020-21 à 2025). Chaque chiffre renvoie au document et à la page. Survolez une référence pour lire la citation exacte.</p>
    <div class="question">
      <span class="eyebrow">Question posée</span>
      <p><strong>Comment financer l’écart restant entre le revenu autorisé de Senelec et ses recettes tarifaires, et à quel rythme le résorber, sans recréer une crise de trésorerie ?</strong></p>
    </div>
  </header>

  <section aria-labelledby="h-keys">
    <h2 id="h-keys">En bref</h2>
    <ul class="keys">
      <li><span class="k">{P["gap25"]} Mds<small>écart 2025</small></span><p>L’écart entre le revenu maximum autorisé (RMA) et les recettes au tarif est passé de {P["gap22"]} Mds FCFA en 2022 {ref("gap",2022)} à {P["gap25"]} Mds en 2025 {ref("gap",2025)}. Les tarifs couvrent désormais {P["cov25"]} % du RMA, contre {P["cov22"]} % en 2022. {tag("c")}</p></li>
      <li><span class="k">{P["ebex24"]} Mds<small>EBE 2024 hors compensation</small></span><p>Sans la compensation de l’État, l’excédent brut d’exploitation aurait été négatif cinq années sur six, jusqu’à {P["ebex22"]} Mds en 2022. La compensation représentait encore {P["comp24"]} % du chiffre d’affaires en 2024. {tag("c")}</p></li>
      <li><span class="k">+{P["admg"]} %<small>créances Administration 2024</small></span><p>Les factures impayées de l’Administration sont passées de {P["adm23"]} Mds en janvier 2024 à {P["adm24"]} Mds en décembre 2024 {ref("recv_admin",2024)}. Le taux de couverture des encaissements est tombé à {num(v("tccae",2024),2)} % {ref("tccae",2024)}. {tag("f")}</p></li>
      <li><span class="k">≈ 19 %<small>pertes, stables depuis 2019</small></span><p>Le rendement global reste autour de 81 % de 2019 à 2024 {ref("rendement_brut",2024)}. Chaque point de pertes représente environ {P["loss_pt_gwh"]} GWh, soit {P["loss_pt_bn"]} Mds FCFA par an au prix moyen 2024. {tag("c")}</p></li>
      <li><span class="k">2 ans<small>concession expirée</small></span><p>La concession de Senelec a expiré le 31 mars 2024. Elle est prolongée d’année en année par avis de la CRSE en attendant un nouveau contrat {sref("crse2025",29,"Avis n°07/2025")}. Les comptes 2021 et 2022 ont reçu une opinion avec réserve {sref("ar2022",64)}. {tag("f")}</p></li>
    </ul>
  </section>

  <section aria-labelledby="h-gap">
    <h2 id="h-gap">1. L’écart tarifaire se résorbe depuis 2023</h2>
    <p>Le régulateur fixe chaque année un revenu maximum autorisé (RMA) qui couvre les coûts de Senelec. L’État compense la différence entre ce revenu et les recettes au tarif en vigueur. Cet écart a culminé en 2022, année de hausse des prix du pétrole et de gel des tarifs. La CRSE attribue la baisse depuis 2023 à la hausse tarifaire de janvier 2023 (+16,72 % en moyenne) et à la baisse des prix des combustibles {sref("crse2022_23",22)} {sref("crse2025",38)}.</p>
    <figure>
      {chart1}
      <div class="legend"><span style="--sw: var(--fg)">Recettes au tarif</span><span style="--sw: var(--gap)">Écart compensé par l’État</span></div>
      <figcaption>Hauteur totale = RMA définitif. Sources : CRSE, rapports 2020-21 à 2025 {ref("rma",2020)} {ref("rma",2022)} {ref("rma",2024)} {ref("rma",2025)}. Recettes au tarif = RMA − écart. {tag("c")}</figcaption>
    </figure>
    <div class="tablewrap"><table>
      <thead><tr><th>FCFA par kWh vendu</th><th>2020</th><th>2022</th><th>2024</th><th>2025</th></tr></thead>
      <tbody>
        <tr><td>Revenu autorisé (RMA / ventes)</td>{''.join(f"<td>{num(cget('rma_per_kwh',y))}</td>" for y in (2020,2022,2024,2025))}</tr>
        <tr><td>Recette au tarif</td>{''.join(f"<td>{num(cget('tariff_per_kwh',y))}</td>" for y in (2020,2022,2024,2025))}</tr>
        <tr><td><strong>Écart par kWh</strong></td>{''.join(f"<td><strong>{num(cget('gap_per_kwh',y))}</strong></td>" for y in (2020,2022,2024,2025))}</tr>
      </tbody></table></div>
    <p>{tag("c")} Le coût autorisé par kWh a baissé de {P["rpk22"]} FCFA en 2022 à {P["rpk25"]} FCFA en 2025, tandis que la recette au tarif passait de {P["tpk22"]} à {P["tpk25"]} FCFA. Pour combler l’écart 2025 par le seul tarif, il faudrait relever les recettes tarifaires d’environ {P["gapshare25"]} % (écart 2025 / recettes au tarif 2025). Ventes retenues : volumes du RMA, hors exportations {ref("sales_rma_gwh",2025)}.</p>
  </section>

  <section aria-labelledby="h-ebe">
    <h2 id="h-ebe">2. La rentabilité affichée repose sur la compensation</h2>
    <p>Senelec comptabilise la compensation dans son chiffre d’affaires (« Écart sur RMA ») {ref("ecart_rma_booked",2024)}. Son excédent brut d’exploitation publié est donc positif chaque année. Une fois la compensation retirée, l’exploitation est déficitaire, sauf en 2020, année de prix bas des combustibles.</p>
    <figure>
      {chart2}
      <div class="legend"><span style="--sw: var(--fg)">EBE publié</span><span style="--sw: var(--copper)">EBE hors compensation (étiqueté)</span></div>
      <figcaption>EBE publié {ref("ebe",2019)} … {ref("ebe",2024)} ; compensation comptabilisée {ref("ecart_rma_booked",2019)} … {ref("ecart_rma_booked",2024)}. {tag("c")}</figcaption>
    </figure>
    <p>Le résultat net reste positif (34,76 Mds en 2024 {ref("net_result",2024)}), mais il inclut entre 18,6 et 19,1 Mds de résultat hors activités ordinaires (HAO) dans chaque rapport qui le détaille (2019, 2020, 2021, 2023, 2024) {sref("ar2019",42)} {sref("ar2024",44)}. {tag("i")} Un résultat HAO aussi régulier mérite d’être expliqué : il gonfle la rentabilité apparente.</p>
  </section>

  <section aria-labelledby="h-cash">
    <h2 id="h-cash">3. Le risque se déplace vers l’encaissement et la trésorerie</h2>
    <figure>
      {chart3}
      <figcaption>Créances commerciales sur l’Administration au 31 décembre {ref("recv_admin",2019)} … {ref("recv_admin",2024)}. Elles excluent la compensation encore due par l’État, qui atteignait 135,8 Mds fin 2022 {sref("ar2022",52)}.</figcaption>
    </figure>
    <ul>
      <li>{tag("f")} En 2024, la Délégation Grands Comptes (63 % du chiffre d’affaires encaissable) n’a encaissé que 82,14 % de ses factures {sref("ar2024",42)}. Senelec cite les créances « sensibles » : forages, foyers religieux, hôpitaux et postes de santé {sref("ar2024",43)}.</li>
      <li>{tag("c")} Créances clients au bilan : {P["rd22"]} jours de chiffre d’affaires en 2022, {P["rd24"]} jours en 2024 {ref("recv_balance",2024)}.</li>
      <li>{tag("c")} Actif circulant / passif circulant (hors trésorerie) : {P["cr19"]} en 2019, {P["cr24"]} en 2024 {ref("current_liab",2024)}. Le passif circulant a augmenté de 189,85 Mds en 2024, surtout du fait des fournisseurs d’exploitation {sref("ar2024",47)}.</li>
      <li>{tag("f")} Les dettes envers les fournisseurs de combustible ont plus que doublé en 2022, de 145,0 à 328,1 Mds {sref("ar2022",55)}. La trésorerie passive a atteint 202,6 Mds fin 2023, puis 134,5 Mds fin 2024 {sref("ar2024",47)}.</li>
      <li>{tag("i")} Lecture : la compensation est désormais versée, mais les factures publiques impayées recréent un besoin de trésorerie. Senelec le reporte sur ses fournisseurs (producteurs indépendants, combustible). C’est un cycle d’arriérés à surveiller plus que le niveau de l’écart lui-même.</li>
    </ul>
  </section>

  <section aria-labelledby="h-loss">
    <h2 id="h-loss">4. Les pertes ne baissent pas</h2>
    <p>{tag("f")} Rendement brut (énergie vendue / énergie disponible) : {", ".join(f"{num(v('rendement_brut',y),2)} % en {y}" for y in Y6)} {ref("rendement_brut",2019)} {ref("rendement_brut",2024)}. Le rapport ne publie pas la part technique et la part commerciale des pertes.</p>
    <p>{tag("c")} En 2024, l’énergie disponible était de {num(v("energy_available",2024),0)} GWh {ref("energy_available",2024)}. Un point de pertes en moins représente donc environ {P["loss_pt_gwh"]} GWh vendus en plus, soit {P["loss_pt_bn"]} Mds FCFA au prix moyen de {num(v("avg_price",2024),2)} FCFA/kWh {ref("avg_price",2024)}, environ {P["loss_pt_share"]} % de l’écart 2024. Ce calcul suppose que l’énergie récupérée serait facturée et payée au prix moyen.</p>
  </section>

  <section aria-labelledby="h-risk">
    <h2 id="h-risk">5. Points de vigilance</h2>
    <ul>
      <li>{tag("f")} <strong>Statut juridique.</strong> La concession (1999, 25 ans) a expiré le 31 mars 2024 {sref("crse2024",45)}. Les conditions préalables, à savoir un nouveau contrat avec accès des tiers et la restructuration de Senelec, n’étaient pas remplies à la fin de la période transitoire {sref("crse2025",29)}.</li>
      <li>{tag("f")} <strong>Audit.</strong> Opinion avec réserve sur 2021 et 2022 : les actifs dont la propriété a été transférée à l’État figurent toujours au bilan de Senelec {sref("ar2021",48)} {sref("ar2022",65)}. Les rapports 2023 et 2024 ne reproduisent pas l’opinion des commissaires aux comptes {sref("ar2024",6)}.</li>
      <li>{tag("f")} <strong>Approvisionnement.</strong> La fin du contrat de location Karpowership (335 MW) pourrait créer un déficit d’environ 300 MW selon la CRSE {sref("crse2025",29)}. Achats d’énergie (combustible des producteurs indépendants et primes fixes compris) : {bn(v("energy_purchases",2024))} Mds en 2024, contre {bn(v("energy_purchases",2021))} Mds en 2021 {ref("energy_purchases",2024)}.</li>
      <li>{tag("f")} <strong>Qualité de service.</strong> SAIDI de {num(v("saidi",2024),2)} h en 2024 selon Senelec {ref("saidi",2024)}. La norme CRSE de 1 h 30 n’est pas respectée {sref("crse2024",35)}. Le rapport CRSE 2025 indique pourtant 33 minutes pour 2024 {sref("crse2025",45)}, sans expliquer l’écart.</li>
    </ul>
  </section>

  <section aria-labelledby="h-opt">
    <h2 id="h-opt">Options à instruire</h2>
    <p>Ces options sont des pistes à évaluer, pas des recommandations. Leur coût social et leur faisabilité politique ne sont pas couverts par cette note. {tag("i")}</p>
    <div class="options">
      <div class="opt"><h3>A. Apurer les factures de l’Administration et instaurer un paiement à date fixe</h3><p class="what">Effet direct sur la trésorerie : jusqu’à {P["adm24"]} Mds d’encours fin 2024. Cela rompt le cycle d’arriérés vers les producteurs indépendants. À instruire : budgétisation des consommations publiques, compteurs à prépaiement pour les entités publiques.</p></div>
      <div class="opt"><h3>B. Poursuivre la convergence tarifaire, avec protection de la première tranche</h3><p class="what">L’écart 2025 équivaut à environ {P["gapshare25"]} % des recettes tarifaires. Étalé sur plusieurs années, il pourrait suivre la méthode de 2023 (hausse ciblée, première tranche domestique protégée {sref("crse2022_23",10)}). Le mécanisme de correction des coûts de production (déclenché au-delà de ±5 %) existe déjà {sref("crse2022_23",20)}.</p></div>
      <div class="opt"><h3>C. Programme de réduction des pertes avec objectifs publiés</h3><p class="what">Environ {P["loss_pt_bn"]} Mds par point et par an. Préalable : publier la décomposition entre pertes techniques et pertes commerciales, sans laquelle l’investissement ne peut pas être ciblé.</p></div>
      <div class="opt"><h3>D. Régulariser le cadre : nouveau contrat de concession et régime des actifs</h3><p class="what">Lève la réserve d’audit récurrente et sécurise les financements à long terme. Publier l’opinion d’audit complète chaque année.</p></div>
    </div>
  </section>

  <section aria-labelledby="h-watch">
    <h2 id="h-watch">Indicateurs à suivre chaque trimestre</h2>
    <ul>
      <li>Écart RMA trimestriel et compensation effectivement versée (CRSE)</li>
      <li>Créances sur l’Administration et taux d’encaissement des grands comptes</li>
      <li>Dettes envers les fournisseurs de combustible et les producteurs indépendants</li>
      <li>Rendement global, avec la part technique et la part commerciale</li>
      <li>Capacité disponible face à la pointe, notamment à l’échéance Karpowership</li>
    </ul>
  </section>

  <section aria-labelledby="h-lim" class="limits">
    <h2 id="h-lim">Fiabilité de cette note</h2>
    <ul>
      <li>{ver["values"]} valeurs extraites de 10 documents ; {ver["verified"]} ont été vérifiées automatiquement : citation exacte retrouvée dans le texte et nombre présent dans la citation. {ver["signals_verified"]} faits qualitatifs vérifiés de la même façon.</li>
      <li>Les rapports annuels ne sont pas des états financiers complets. Les définitions varient d’une année à l’autre : le périmètre des achats d’énergie change à partir de 2021, et le taux de couverture des encaissements n’est pas cohérent avec les montants publiés à côté.</li>
      <li>Incohérences relevées dans les sources : nombre de clients 2023 (2 410 431 dans le RA 2023, 2 261 996 dans le RA 2024) ; SAIDI 2024 (6 h 40 contre 33 min) ; couverture du RMA 2023 calculée à 72,6 % contre 73,25 % imprimés par la CRSE.</li>
      <li>Les comptes 2025 de Senelec n’étaient pas publiés à la date de la note. Les données 2025 viennent de la CRSE.</li>
      <li>Les interprétations et les options demandent la relecture d’un expert du secteur avant tout usage externe.</li>
    </ul>
  </section>

  <footer>
    <span>Courant · Africa Utility Intelligence · prototype. Information et analyse uniquement, sans valeur de notation ni d’avis d’investissement.</span>
    <span>Chiffres en milliards de FCFA (Mds) sauf mention contraire. Les années sont des exercices calendaires.</span>
  </footer>
</div>
'''
open(OUT, 'w').write(page)
print('ok', len(page))
