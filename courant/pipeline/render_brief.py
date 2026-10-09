"""Render a decision brief from brief.json + verified.json + docs.json.

brief.json is written by the brief-writer agent. Text fields may contain:
  [[V12]]          source chip for verified value #12 (index in verified.json "values")
  [[S7]]           source chip for verified signal #7
  [[C:id]]         formatted result of computation `id`
Computations: {"id", "expr" (Python arithmetic over V<n> names), "decimals", "unit", "scale"}.
Every reference must exist and be verified, or rendering fails: no chip can point to an unverified source.

Usage: render_brief.py <utility_dir> <out.html>
"""
import json, re, sys, html, math

UD, OUT = sys.argv[1], sys.argv[2]
brief = json.load(open(f'{UD}/brief.json'))
ver = json.load(open(f'{UD}/verified.json'))
docs = json.load(open(f'{UD}/docs.json'))
VAL, SIG = ver['values'], ver['signals']

errors = []

def V(i):
    i = int(i)
    if i >= len(VAL) or not VAL[i]['verified']:
        errors.append(f'V{i} missing or unverified')
        return None
    return VAL[i]

def S(i):
    i = int(i)
    if i >= len(SIG) or not SIG[i]['verified']:
        errors.append(f'S{i} missing or unverified')
        return None
    return SIG[i]

def doc_key(rec):
    return rec['file'].replace('.txt', '') if rec.get('file') else rec['doc']

def chip(rec):
    k = doc_key(rec)
    d = docs.get(k, {'label': k, 'url': ''})
    q = html.escape(rec['quote'].strip())
    href = f' href="{d["url"]}" target="_blank" rel="noopener"' if d.get('url') else ''
    return f'<a class="ref"{href} title="{q}">{html.escape(d["label"])} p.{rec["found_page"]}</a>'

def fnum(x, dec=1):
    s = f'{x:,.{dec}f}'
    return s.replace(',', ' ').replace('.', ',')

# ---- computations
COMP = {}
for c in brief.get('computations', []):
    names = {f'V{m}': (V(m) or {'value': math.nan})['value'] for m in re.findall(r'V(\d+)', c['expr'])}
    names.update({k: v for k, v in COMP.items()})
    try:
        val = eval(c['expr'], {'__builtins__': {}, 'abs': abs, 'min': min, 'max': max}, names)
    except Exception as e:
        errors.append(f'computation {c["id"]}: {e}')
        val = math.nan
    COMP[c['id']] = val * c.get('scale', 1)
CFMT = {c['id']: c for c in brief.get('computations', [])}

def fmt_comp(cid):
    c = CFMT.get(cid)
    if c is None:
        errors.append(f'C:{cid} undefined'); return '?'
    s = fnum(COMP[cid], c.get('decimals', 1))
    u = c.get('unit', '')
    return f'{s}{(" " + u) if u else ""}'

TAGS = {'fact': '<span class="tag f">fait sourcé</span>', 'calc': '<span class="tag c">calcul</span>', 'interp': '<span class="tag i">interprétation</span>'}

def rich(t):
    t = html.escape(t, quote=False)
    # bold first, so ** inside chip titles (source quotes) is never converted
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\[\[V(\d+)\]\]', lambda m: chip(V(m.group(1))) if V(m.group(1)) else '[?]', t)
    t = re.sub(r'\[\[S(\d+)\]\]', lambda m: chip(S(m.group(1))) if S(m.group(1)) else '[?]', t)
    t = re.sub(r'\[\[C:([\w-]+)\]\]', lambda m: fmt_comp(m.group(1)), t)
    return t

def tagged(p):
    tg = TAGS.get(p.get('tag', ''), '')
    return f'{tg} {rich(p["text"])}' if tg else rich(p['text'])

def series_value(ref):
    if isinstance(ref, (int, float)): return ref
    if ref.startswith('V'): r = V(ref[1:]); return r['value'] if r else math.nan
    if ref.startswith('C:'): return COMP.get(ref[2:], math.nan)
    return math.nan

# ---- charts (bars, grouped or stacked), drawn to one scale
def chart(ch):
    years = ch['years']
    series = ch['series']
    vals = [[series_value(s['values'].get(str(y))) * ch.get('scale', 1) if s['values'].get(str(y)) is not None else math.nan for y in years] for s in series]
    stacked = ch.get('kind') == 'stacked'
    flat = [v for row in vals for v in row if not math.isnan(v)]
    if stacked:
        tops = [sum(row[i] for row in vals if not math.isnan(row[i])) for i in range(len(years))]
        hi, lo = max(tops + [0]), 0
    else:
        hi, lo = max(flat + [0]), min(flat + [0])
    span = hi - lo or 1
    step = 10 ** math.floor(math.log10(span / 4)) if span > 0 else 1
    for m in (1, 2, 2.5, 5, 10):
        if span / (step * m) <= 6: step *= m; break
    hi_t = math.ceil(hi / step) * step; lo_t = math.floor(lo / step) * step
    W, H, L, R, T, B = 640, 290, 60, 16, 22, 40
    sy = lambda v: T + (H - T - B) * (hi_t - v) / (hi_t - lo_t or 1)
    out = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(ch["title"])}">']
    t = lo_t
    while t <= hi_t + 1e-9:
        y = sy(t)
        out.append(f'<line class="{"zero" if abs(t) < 1e-9 and lo_t < 0 else "grid"}" x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}"/><text class="axis" x="{L-8}" y="{y+4:.1f}" text-anchor="end">{fnum(t, 0 if step >= 1 else 1)}</text>')
        t += step
    slot = (W - L - R) / len(years)
    n = 1 if stacked else len(series)
    bw = (slot - 20) / n
    for i, y in enumerate(years):
        x0 = L + i * slot + 10
        base = 0
        for j, s in enumerate(series):
            v = vals[j][i]
            if math.isnan(v): continue
            cls = f'b{j}'
            if stacked:
                top, bot = sy(base + v), sy(base); base += v; x = x0
            else:
                top, bot = (sy(v), sy(0)) if v >= 0 else (sy(0), sy(v)); x = x0 + j * bw
            out.append(f'<rect class="{cls}" x="{x:.1f}" y="{top:.1f}" width="{bw-2:.1f}" height="{max(bot-top,0.5):.1f}"/>')
            if not stacked and (ch.get('label_series') is None or ch.get('label_series') == j):
                ly = top - 5 if v >= 0 else bot + 13
                out.append(f'<text class="lbl" x="{x+(bw-2)/2:.1f}" y="{ly:.1f}" text-anchor="middle">{fnum(v, ch.get("decimals", 0))}</text>')
        if stacked and ch.get('top_labels'):
            lab = series_value(ch['top_labels'].get(str(y))) if ch['top_labels'].get(str(y)) else None
            if lab is not None and not math.isnan(lab):
                out.append(f'<text class="lbl" x="{x0+bw/2:.1f}" y="{sy(base)-6:.1f}" text-anchor="middle">{fnum(lab, 0)}{ch.get("top_label_unit","")}</text>')
        out.append(f'<text class="axis" x="{x0 + (bw*n)/2:.1f}" y="{H-B+18}" text-anchor="middle">{html.escape(str(ch.get("year_labels", {}).get(str(y), y)))}</text>')
    out.append(f'<text class="axis" x="{L}" y="{H-6}">{html.escape(ch.get("unit_label",""))}</text></svg>')
    legend = ''.join(f'<span style="--sw: var(--s{j})">{html.escape(s["label"])}</span>' for j, s in enumerate(series))
    return f'<figure>{"".join(out)}<div class="legend">{legend}</div><figcaption>{rich(ch.get("caption",""))}</figcaption></figure>'

def table(tb):
    head = ''.join(f'<th>{html.escape(str(c))}</th>' for c in tb['columns'])
    rows = []
    for r in tb['rows']:
        cells = [f'<td>{rich(r["label"])}</td>']
        for c in r['cells']:
            if isinstance(c, str) and (c.startswith('V') or c.startswith('C:')) and re.fullmatch(r'(V\d+|C:[\w-]+)', c):
                v = series_value(c) * r.get('scale', 1)
                cells.append(f'<td>{fnum(v, r.get("decimals", 1))}{r.get("suffix","")}</td>')
            else:
                cells.append(f'<td>{rich(str(c))}</td>')
        rows.append('<tr>' + ''.join(cells) + '</tr>')
    return f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>' + (f'<p class="note">{rich(tb["note"])}</p>' if tb.get('note') else '')

b = brief
parts = []
parts.append(f'''<header class="intro"><span class="eyebrow">{html.escape(b["eyebrow"])}</span><h1>{html.escape(b["headline"])}</h1>
<p class="meta">{rich(b["audience_and_sources"])}</p>
<div class="question"><span class="eyebrow">Question posée</span><p><strong>{html.escape(b["decision_question"])}</strong></p></div></header>''')
keys = ''.join(f'<li><span class="k">{rich(k["figure"])}<small>{html.escape(k["figure_label"])}</small></span><p>{tagged(k)}</p></li>' for k in b['key_messages'])
parts.append(f'<section><h2>En bref</h2><ul class="keys">{keys}</ul></section>')
for i, s in enumerate(b['sections'], 1):
    body = []
    for blk in s['blocks']:
        if blk['type'] == 'p': body.append(f'<p>{tagged(blk)}</p>')
        elif blk['type'] == 'list': body.append('<ul>' + ''.join(f'<li>{tagged(x)}</li>' for x in blk['items']) + '</ul>')
        elif blk['type'] == 'chart': body.append(chart(blk))
        elif blk['type'] == 'table': body.append(table(blk))
    parts.append(f'<section><h2>{i}. {html.escape(s["heading"])}</h2>{"".join(body)}</section>')
opts = ''.join(f'<div class="opt"><h3>{html.escape(o["title"])}</h3><p class="what">{rich(o["text"])}</p></div>' for o in b['options'])
parts.append(f'<section><h2>Options à instruire</h2><p>{TAGS["interp"]} Ces options sont des pistes à évaluer, pas des recommandations. Leur coût social et leur faisabilité politique ne sont pas couverts par cette note.</p><div class="options">{opts}</div></section>')
parts.append('<section><h2>Indicateurs à suivre</h2><ul>' + ''.join(f'<li>{rich(w)}</li>' for w in b['watch']) + '</ul></section>')
s = ver['summary']
lim = [f'{s["values"]} valeurs extraites ; {s["verified"]} vérifiées automatiquement (citation exacte retrouvée dans le texte à la page indiquée, nombre présent dans la citation). {s["signals_verified"]} faits qualitatifs vérifiés de la même façon.',
       f'Sur {s["reconciled_pairs"]} couples (même indicateur, même année) publiés dans plusieurs documents, {s["disagreements_gt_1pct"]} diffèrent de plus de 1 %, le plus souvent du fait de définitions différentes.'] + b['limits']
parts.append('<section class="limits"><h2>Fiabilité de cette note</h2><ul>' + ''.join(f'<li>{rich(x)}</li>' for x in lim) + '</ul></section>')

if errors:
    sys.exit('RENDER ERRORS:\n' + '\n'.join(sorted(set(errors))))

css = open(__file__.replace('render_brief.py', 'brief.css')).read()
logo = open(__file__.replace('pipeline/render_brief.py', '../brand/courant/courant-logo.svg')).read()
logo = re.sub(r'<title>.*?</title>', '', logo).replace('#14211f', 'currentColor').replace('#e3a90b', 'var(--accent)')
page = f'''<title>{html.escape(b["title"])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112..125,500..800&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style>
<div class="wrap"><div class="top">{logo}<span class="proto">Prototype · note générée à partir des documents publics</span></div>
{"".join(parts)}
<footer><span>Courant · Africa Utility Intelligence · prototype. Information et analyse uniquement, sans valeur de notation ni d’avis d’investissement.</span><span>{html.escape(b.get("footer_units",""))}</span></footer></div>'''
open(OUT, 'w').write(page)
print('rendered', OUT, len(page), 'bytes;', len(COMP), 'computations')
