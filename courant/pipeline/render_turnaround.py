"""Render turnaround orientations from turnaround.json (+ verified.json, docs.json). Same citation markup as render_brief.py:
[[V<n>]], [[S<n>]] source chips; **bold**. Fails if a citation is missing or unverified.
Usage: render_turnaround.py <utility_dir> <out.html>"""
import json, re, sys, html

UD, OUT = sys.argv[1], sys.argv[2]
T = json.load(open(f'{UD}/turnaround.json'))
ver = json.load(open(f'{UD}/verified.json')); docs = json.load(open(f'{UD}/docs.json'))
VAL, SIG = ver['values'], ver['signals']
errors = []

def rec(kind, i):
    L = VAL if kind == 'V' else SIG
    i = int(i)
    if i >= len(L) or not L[i]['verified']:
        errors.append(f'{kind}{i} missing or unverified'); return None
    return L[i]

def chip(r):
    k = (r.get('file') or r['doc']).replace('.txt', '')
    d = docs.get(k, {'label': k, 'url': ''})
    href = f' href="{d["url"]}" target="_blank" rel="noopener"' if d.get('url') else ''
    return f'<a class="ref"{href} title="{html.escape(r["quote"].strip())}">{html.escape(d["label"])} p.{r["found_page"]}</a>'

def rich(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\[\[([VS])(\d+)\]\]', lambda m: (chip(r) if (r := rec(m.group(1), m.group(2))) else '[?]'), t)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)

H = {'0-6': '0 à 6 mois', '6-24': '6 à 24 mois', '24-60': '2 à 5 ans'}
parts = [f'''<header class="intro"><span class="eyebrow">Orientations de redressement · {html.escape(T["utility"])} · {"BROUILLON, NON RELU" if T.get("status") != "approved" else "relu et approuvé"}</span>
<h1>{html.escape(T["headline"])}</h1><p class="meta">{rich(T["scope_note"])}</p></header>''']
if T.get('priorities'):
    rows = ''.join(f'<tr><td>{i}</td><td>{html.escape(p["lever"])}<br><span class="ws">{html.escape(p.get("workstream", ""))}</span></td><td>{rich(p["magnitude"])}</td><td>{html.escape(p["owner"])}</td><td>{html.escape(p["deadline"])}</td></tr>' for i, p in enumerate(T['priorities'], 1))
    parts.append(f'<section><h2>Priorités classées par enjeu</h2><div class="tscroll"><table class="prio"><thead><tr><th>#</th><th>Levier</th><th>Ordre de grandeur ({html.escape(T.get("currency", "KES"))})</th><th>Décideur</th><th>Échéance</th></tr></thead><tbody>{rows}</tbody></table></div></section>')
parts.append('<section><h2>Diagnostic en une page</h2><ul class="keys">' + ''.join(f'<li><span class="k">{html.escape(d["label"])}</span><p>{rich(d["text"])}</p></li>' for d in T['diagnosis']) + '</ul></section>')
parts.append('<section><h2>Enchaînement des causes</h2><ol class="chain">' + ''.join(f'<li>{rich(c)}</li>' for c in T['causal_chain']) + '</ol></section>')
for h in ('0-6', '6-24', '24-60'):
    levers = [l for l in T['levers'] if l['horizon'] == h]
    if not levers: continue
    cards = ''.join(f'''<div class="opt"><h3>{html.escape(l["title"])}</h3><p>{rich(l["why"])}</p>
<dl class="lv"><dt>Porteur</dt><dd>{html.escape(l["owner"])}</dd><dt>Indicateur de suivi</dt><dd>{rich(l["kpi"])}</dd><dt>Préalables</dt><dd>{rich(l["preconditions"])}</dd><dt>Risques</dt><dd>{rich(l["risks"])}</dd></dl></div>''' for l in levers)
    parts.append(f'<section><h2>{H[h]}</h2><div class="options">{cards}</div></section>')
parts.append('<section><h2>Ce qu’il ne faut pas faire</h2><ul>' + ''.join(f'<li>{rich(x)}</li>' for x in T['avoid']) + '</ul></section>')
parts.append('<section class="limits"><h2>Limites</h2><ul>' + ''.join(f'<li>{rich(x)}</li>' for x in T['limits']) + '</ul></section>')
if errors:
    sys.exit('RENDER ERRORS:\n' + '\n'.join(sorted(set(errors))))
css = open(__file__.replace('render_turnaround.py', 'brief.css')).read() + '\n.chain{display:grid;gap:8px;padding-left:22px;max-width:70ch}.lv{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:4px 14px;margin:6px 0 0;font-size:.9rem}.lv dt{color:var(--muted);font-family:var(--mono);font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;padding-top:2px}.lv dd{margin:0}.tscroll{overflow-x:auto}.prio{border-collapse:collapse;width:100%;font-size:.88rem}.prio th,.prio td{text-align:left;vertical-align:top;padding:6px 8px;border-bottom:1px solid var(--line)}.prio th{font-family:var(--mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}.prio .ws{color:var(--muted);font-size:.8rem}\n'
logo = open(__file__.replace('pipeline/render_turnaround.py', '../brand/courant/courant-logo.svg')).read()
logo = re.sub(r'<title>.*?</title>', '', logo).replace('#14211f', 'currentColor').replace('#e3a90b', 'var(--accent)')
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(T["title"])}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112..125,500..800&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap"><style>{css}</style></head><body>
<div class="wrap"><div class="top">{logo}<span class="proto">{"Brouillon · relecture experte requise avant diffusion" if T.get("status") != "approved" else "Relu par un expert"}</span></div>{"".join(parts)}
<footer><span>Courant · orientations stratégiques à instruire, sans valeur de recommandation d’investissement. Fondées sur les documents publics cités.</span></footer></div></body></html>'''
open(OUT, 'w').write(page)
print('rendered', OUT)
