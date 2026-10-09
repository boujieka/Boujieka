"""Build the Courant platform (static site + protected files for the download function).

Inputs: catalog.json, docs/utility-intelligence/audit_matrix.json, courant/data/<slug>/{brief.html, brief.json, verified.json, docs.json, turnaround.json}
Outputs: courant/platform/dist/ (public) and courant/platform/protected/ (served only by the download function).
Usage: build_site.py   (env SUPABASE_URL / SUPABASE_ANON_KEY written to dist/assets/config.js if set)
"""
import json, os, re, html, csv, io, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, '..', '..'))
DATA = os.path.join(REPO, 'courant', 'data')
DIST, PROT = os.path.join(ROOT, 'dist'), os.path.join(ROOT, 'protected')
for d in (DIST, PROT):
    shutil.rmtree(d, ignore_errors=True)
os.makedirs(os.path.join(DIST, 'assets')); os.makedirs(os.path.join(DIST, 'pays')); os.makedirs(os.path.join(DIST, 'u')); os.makedirs(PROT)

CAT = json.load(open(os.path.join(ROOT, 'catalog.json')))
AUD = {u['name']: u for a in json.load(open(os.path.join(REPO, 'docs', 'utility-intelligence', 'audit_matrix.json')))['audits'] for u in a['utilities']}
REG = {}
for a in json.load(open(os.path.join(REPO, 'docs', 'utility-intelligence', 'audit_matrix.json')))['audits']:
    for r in a['regulators']:
        REG.setdefault(r['country'], []).append(r)

E = html.escape
VIA = {'strong': 'Élevée', 'usable': 'Moyenne', 'weak': 'Limitée', 'not_viable': 'Insuffisante'}
SCOPE = {'integrated': 'Intégrée', 'distribution': 'Distribution', 'transmission': 'Transport', 'generation': 'Production', 'other': 'Concession / patrimoine', 'single_buyer': 'Acheteur unique'}
AR = {'found_fetched': ('●', 'yes', 'consulté'), 'found_link_not_fetched': ('◐', 'part', 'lien trouvé'), 'referenced_only': ('○', 'part', 'cité ailleurs'), 'not_found': ('·', 'no', 'non trouvé'), 'not_checked': ('?', 'no', 'non vérifié')}
FS = {'full_with_notes': ('●', 'yes', 'complets'), 'summary_or_extract': ('◐', 'part', 'résumé'), 'unaudited_only': ('u', 'part', 'non audités'), 'not_found': ('·', 'no', 'non trouvés'), 'not_checked': ('?', 'no', 'non vérifié')}
OPINION = {'unmodified': 'sans réserve', 'unmodified_with_emphasis': 'sans réserve, avec observation', 'qualified': 'avec réserve', 'adverse': 'défavorable', 'disclaimer': 'impossibilité', 'not_visible': '—'}
TIER = {'public': 'Public', 'registered': 'Inscrit', 'institutional': 'Institutionnel'}

logo = open(os.path.join(REPO, 'brand', 'courant', 'courant-logo.svg')).read()
logo = re.sub(r'<title>.*?</title>', '', logo).replace('#14211f', 'currentColor').replace('#e3a90b', 'var(--accent)')
logo = logo.replace('<svg ', '<svg aria-hidden="true" ', 1)

def page(title, body, depth=0, active=''):
    up = '../' * depth
    nav = [('index.html', 'Pays', 'pays'), ('methode.html', 'Méthode', 'methode'), ('a-propos.html', 'À propos', 'apropos')]
    links = ''.join(f'<a href="{up}{h}"{" aria-current=page" if k == active else ""}>{t}</a>' for h, t, k in nav)
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="Courant · diagnostic sourcé des sociétés d’électricité africaines.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112..125,500..800&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="{up}assets/site.css"></head><body>
<header class="top"><div class="wrap"><a class="brand" href="{up}index.html" aria-label="Courant, accueil">{logo}<span class="brand-tag">Africa Utility Intelligence</span></a>
<nav class="links" aria-label="Navigation">{links}<a class="acct" id="acct" href="{up}compte.html">Se connecter</a></nav></div></header>
<main class="wrap">{body}</main>
<footer class="wrap"><span>Courant · Africa Utility Intelligence. Information et analyse uniquement, sans valeur de notation ni d’avis d’investissement.</span>
<span>Les noms des sociétés citées appartiennent à leurs détenteurs ; leur mention ne vaut pas partenariat. Une utility peut demander la correction de sa fiche en transmettant ses publications.</span></footer>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js"></script>
<script src="{up}assets/config.js"></script><script src="{up}assets/site.js"></script></body></html>'''

# ---------------- protected files and per-utility availability
manifest = {}
def protect(slug, name, content, tier, mode='w'):
    os.makedirs(os.path.join(PROT, slug), exist_ok=True)
    with open(os.path.join(PROT, slug, name), mode) as f:
        f.write(content)
    manifest[f'{slug}/{name}'] = tier

avail = {}
for u in CAT['utilities']:
    s = u['slug']; ud = os.path.join(DATA, s); a = []
    if os.path.exists(os.path.join(ud, 'brief.html')):
        b = open(os.path.join(ud, 'brief.html')).read()
        full = b if b.lstrip().lower().startswith('<!doctype') else '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + b + '</body></html>'
        protect(s, f'note-decision-{s}.html', full, 'registered')
        a.append(('registered', f'note-decision-{s}.html', 'Note de décision', 'Analyse sourcée : chaque chiffre renvoie à la page du document officiel. HTML, à ouvrir dans un navigateur.'))
    if os.path.exists(os.path.join(ud, 'verified.json')):
        v = json.load(open(os.path.join(ud, 'verified.json')))
        docs = json.load(open(os.path.join(ud, 'docs.json'))) if os.path.exists(os.path.join(ud, 'docs.json')) else {}
        buf = io.StringIO(); w = csv.writer(buf)
        w.writerow(['indicateur', 'exercice', 'valeur', 'unite_publiee', 'document', 'page', 'citation_exacte', 'note_definition', 'url_document'])
        n = 0
        for r in v['values']:
            if not r['verified']: continue
            k = (r.get('file') or r['doc']).replace('.txt', '')
            w.writerow([r['item'], r['fiscal_year'], r['value'], r['unit_as_printed'], docs.get(k, {}).get('title', k), r['found_page'], r['quote'].strip(), r['definition_note'], docs.get(k, {}).get('url', '')]); n += 1
        protect(s, f'donnees-verifiees-{s}.csv', buf.getvalue(), 'institutional')
        a.append(('institutional', f'donnees-verifiees-{s}.csv', 'Données vérifiées', f'{n} valeurs extraites des documents officiels, avec page et citation exacte. CSV.'))
    tp = os.path.join(ud, 'turnaround.json')
    if os.path.exists(tp):
        t = json.load(open(tp))
        if t.get('status') == 'approved' and os.path.exists(os.path.join(ud, 'turnaround.html')):
            protect(s, f'orientations-{s}.html', open(os.path.join(ud, 'turnaround.html')).read(), 'institutional')
            a.append(('institutional', f'orientations-{s}.html', 'Orientations de redressement', 'Leviers stratégiques et séquencement proposés aux décideurs, relus par un expert.'))
    teaser = None
    if os.path.exists(os.path.join(ud, 'brief.json')):
        bj = json.load(open(os.path.join(ud, 'brief.json'))); teaser = (bj.get('headline'), bj.get('decision_question'))
    elif os.path.exists(os.path.join(ud, 'brief.html')):
        m = re.search(r'<h1>(.*?)</h1>', open(os.path.join(ud, 'brief.html')).read(), re.S)
        q = re.search(r'Question posée</span>\s*<p><strong>(.*?)</strong>', open(os.path.join(ud, 'brief.html')).read(), re.S)
        teaser = (html.unescape(m.group(1)) if m else None, html.unescape(q.group(1)) if q else None)
    avail[s] = (a, teaser)
json.dump(manifest, open(os.path.join(PROT, 'manifest.json'), 'w'), indent=1)

# ---------------- utility pages
def years_table(au):
    rows = []
    for y in au['years']:
        ar, fs = AR.get(y['annual_report'], AR['not_checked']), FS.get(y['audited_fs'], FS['not_checked'])
        op = y['audit_opinion'].split('.')[0].split(',')[0].strip().lower()
        opk = next((k for k in OPINION if op.startswith(k)), None)
        link = f'<a href="{E(y["best_url"])}" rel="noopener" target="_blank">document</a>' if y['best_url'].startswith('http') else '—'
        rows.append(f'<tr><td class="mono">{E(y["fiscal_year"])}</td><td class="{ar[1]}">{ar[0]} {ar[2]}</td><td class="{fs[1]}">{fs[0]} {fs[2]}</td><td>{OPINION[opk] if opk else "—"}</td><td>{link}</td></tr>')
    return '<div class="tablewrap"><table><thead><tr><th>Exercice</th><th>Rapport annuel</th><th>États financiers audités</th><th>Opinion d’audit relevée</th><th>Source</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'

STATUS_KPI = {'computable': 'calculable', 'partially_computable': 'partiel', 'reported_value_only': 'valeur publiée seule', 'not_in_documents_read': 'absent des documents lus', 'not_applicable': 'non applicable'}
def kpi_cov(au):
    from collections import Counter
    c = Counter(k['status'] for k in au['kpi_coverage'])
    return '<div class="cov">' + ''.join(f'<span><strong class="mono">{c[k]}</strong> {v}</span>' for k, v in STATUS_KPI.items() if c[k]) + '</div>'

for u in CAT['utilities']:
    s = u['slug']; au = AUD[u['audit_name']]; cc = CAT['countries'][u['country']]
    legal = re.split(r' \(|, ', au['legal_name_confirmed'])[0][:120]
    a, teaser = avail[s]
    dls = [f'''<div class="dl"><div class="what"><strong>Fiche de transparence</strong><span>Documents publiés par exercice, opinions d’audit relevées, couverture des indicateurs. C’est cette page.</span></div><span class="tier public">Public</span></div>''']
    for tier, name, label, desc in a:
        dls.append(f'''<div class="dl"><div class="what"><strong>{E(label)} <span class="tier {tier}">{TIER[tier]}</span></strong><span>{E(desc)}</span></div>
<button class="btn" data-need="{tier}" data-path="{s}/{name}" data-name="{name}">Télécharger</button><p class="msg" role="status"></p></div>''')
    if not any(x[2] == 'Note de décision' for x in a):
        msg = {0: 'Les documents publics de cette utility ne permettent pas encore une note de décision. La fiche de transparence reste disponible.', 2: 'Note de décision prévue dans la deuxième vague.', 1: 'Note de décision en cours de vérification.'}[u['wave']]
        dls.append(f'<div class="dl"><div class="what"><strong>Note de décision</strong><span>{msg}</span></div><span class="tier registered">Inscrit</span></div>')
    tz = ''
    if teaser and teaser[0]:
        tz = (f'<div class="teaser"><span class="eyebrow">Note de décision · question traitée</span><p><strong>{E(teaser[1])}</strong></p><p class="lede" style="font-size:.95rem">Les constats sont réservés aux comptes inscrits.</p></div>' if teaser[1] else '')
    regs = ''.join(f'<li><strong>{E(r["name"])}</strong> · <a href="{E(r["best_url"] or r["website"])}" target="_blank" rel="noopener">source</a></li>' for r in REG.get(au['country'], []))
    body = f'''<section class="first"><div class="uhead"><span class="eyebrow"><a href="../pays/{u["country"]}.html">{E(cc["name"])}</a> · {E(SCOPE.get(au["entity_scope"], au["entity_scope"]))}</span>
<h1>{E(u["short"])}</h1><p class="lede">{E(legal)}</p>
<p><span class="chip {au["mvp_viability"]}">Documentation publique : {VIA[au["mvp_viability"]]}</span></p>
<dl class="facts"><div><dt>Périmètre</dt><dd>{E(SCOPE.get(au["entity_scope"], au["entity_scope"]))}</dd></div><div><dt>Cadre comptable</dt><dd>{E(au["reporting_currency_and_framework"].split(";")[0][:90])}</dd></div>
<div><dt>Clôture</dt><dd>{E(au["fiscal_year_end"][:60])}</dd></div><div><dt>Site officiel</dt><dd><a href="{E(au["website"])}" target="_blank" rel="noopener">{E(au["website"].replace("https://", "")[:40])}</a></dd></div></dl>{tz}</div></section>
<section><div class="head"><h2>Téléchargements</h2><p class="lede">Ce que vous pouvez obtenir dépend de votre niveau d’accès. <a href="../compte.html">Créer un compte ou se connecter</a>.</p></div><div class="downloads">{"".join(dls)}</div></section>
<section><div class="head"><h2>Fiche de transparence</h2><p class="lede">Ce que l’utility publie réellement pour les exercices 2019 à 2025, d’après l’audit documentaire d’octobre 2026. « Non trouvé » ne veut pas dire « inexistant » : certains sites bloquent l’accès automatisé.</p></div>
{years_table(au)}<h3 style="margin-top:24px">Indicateurs du noyau calculables à partir des documents lus</h3>{kpi_cov(au)}</section>
<section><div class="head"><h2>Autres sources</h2></div><ul>{regs}</ul></section>'''
    open(os.path.join(DIST, 'u', f'{s}.html'), 'w').write(page(f'{u["short"]} · Courant', body, 1))

# ---------------- country pages
for cc, c in CAT['countries'].items():
    us = [u for u in CAT['utilities'] if u['country'] == cc]
    cards = ''.join(f'''<a class="country" href="../u/{u["slug"]}.html"><span class="cname">{E(u["short"])}</span><span class="eyebrow">{E(SCOPE.get(AUD[u["audit_name"]]["entity_scope"], ""))}</span>
<span class="chip {AUD[u["audit_name"]]["mvp_viability"]}">Documentation : {VIA[AUD[u["audit_name"]]["mvp_viability"]]}</span><span class="mono" style="font-size:.8rem">{"Note de décision disponible" if any(x[2] == "Note de décision" for x in avail[u["slug"]][0]) else "Fiche de transparence"}</span></a>''' for u in us)
    body = f'<section class="first"><div class="head"><span class="eyebrow">{E(c["region"])}</span><h1>{E(c["name"])}</h1><p class="lede">{len(us)} société{"s" if len(us) > 1 else ""} suivie{"s" if len(us) > 1 else ""}.</p></div><div class="countries">{cards}</div></section>'
    open(os.path.join(DIST, 'pays', f'{cc}.html'), 'w').write(page(f'{c["name"]} · Courant', body, 1))

# ---------------- home
regions = {}
for cc, c in CAT['countries'].items():
    regions.setdefault(c['region'], []).append(cc)
blocks = []
for rg, ccs in regions.items():
    cards = []
    for cc in ccs:
        us = [u for u in CAT['utilities'] if u['country'] == cc]
        lis = ''.join(f'<li><span>{E(u["short"])}</span><span class="chip {AUD[u["audit_name"]]["mvp_viability"]}">{"note" if any(x[2] == "Note de décision" for x in avail[u["slug"]][0]) else "fiche"}</span></li>' for u in us)
        cards.append(f'<a class="country" href="pays/{cc}.html"><span class="cname">{E(CAT["countries"][cc]["name"])}</span><ul>{lis}</ul></a>')
    blocks.append(f'<div class="region"><span class="eyebrow">{E(rg)}</span><div class="countries">{"".join(cards)}</div></div>')
n_notes = sum(1 for v in avail.values() if any(x[2] == 'Note de décision' for x in v[0]))
home = f'''<section class="first"><div class="head"><span class="eyebrow">Plateforme · version pilote</span><h1>Choisissez un pays.</h1>
<p class="lede">{len(CAT["utilities"])} sociétés d’électricité dans {len(CAT["countries"])} pays. Pour chacune, une fiche de transparence publique ; pour {n_notes} d’entre elles, une note de décision sourcée, chaque chiffre relié à la page du document officiel.</p><div class="legend-docs"><span>Couleur = documentation publique disponible :</span><span class="chip strong">élevée</span><span class="chip usable">moyenne</span><span class="chip weak">limitée</span><span class="chip not_viable">insuffisante</span></div></div>{"".join(blocks)}</section>
<section><div class="head"><h2>Trois niveaux d’accès</h2></div><div class="tiers">
<div><span class="tier public">Public</span><h3>Sans compte</h3><ul><li>Fiches de transparence des 19 utilities</li><li>Liens vers les documents officiels</li><li>Méthode</li></ul></div>
<div><span class="tier registered">Inscrit</span><h3>Compte gratuit</h3><ul><li>Notes de décision complètes</li><li>Références cliquables vers chaque page source</li></ul></div>
<div><span class="tier institutional">Institutionnel</span><h3>Sur validation</h3><ul><li>Données vérifiées (CSV, avec citations)</li><li>Orientations de redressement relues par un expert</li><li>Pour ministères, régulateurs, bailleurs, utilities</li></ul></div>
</div><p style="margin-top:18px"><a class="btn primary" href="compte.html">Créer un compte</a></p></section>'''
open(os.path.join(DIST, 'index.html'), 'w').write(page('Courant · Africa Utility Intelligence', home, 0, 'pays'))

# ---------------- account, method, about
acct = '''<section class="first"><div class="head"><span class="eyebrow">Compte</span><h1>Accéder aux notes</h1><p class="lede">Connexion sans mot de passe : saisissez votre adresse, vous recevez un lien. Un compte donne le niveau Inscrit. Le niveau Institutionnel est accordé après vérification de votre organisation.</p></div>
<div id="signed-out"><form class="card" id="login-form" novalidate><div class="field"><label for="email">Adresse e-mail professionnelle</label><input id="email" type="email" autocomplete="email" required></div>
<div class="field"><label for="org">Organisation</label><input id="org" autocomplete="organization"></div><button class="btn primary" type="submit">Recevoir le lien de connexion</button><p class="status" id="login-status" role="status" hidden></p></form></div>
<div id="signed-in" hidden><div class="card"><p id="who"></p><p>Pour le niveau Institutionnel, écrivez-nous en précisant votre fonction et votre organisation, depuis cette adresse.</p><button class="btn" id="logout" type="button">Se déconnecter</button></div></div></section>'''
open(os.path.join(DIST, 'compte.html'), 'w').write(page('Compte · Courant', acct, 0))
meth = '''<section class="first"><div class="head"><span class="eyebrow">Méthode</span><h1>Comment une note est produite</h1></div><ol style="display:grid;gap:12px;max-width:70ch">
<li><strong>Collecte</strong> des rapports annuels, états financiers audités et rapports des régulateurs. Chaque PDF est archivé avec son empreinte SHA-256.</li>
<li><strong>Extraction</strong> par agents : chaque valeur est relevée avec sa page et une citation exacte du document.</li>
<li><strong>Vérification automatique</strong> : la citation doit se retrouver telle quelle à la page indiquée, et le nombre doit y figurer. Une valeur qui échoue est écartée.</li>
<li><strong>Calculs par script</strong> : aucun chiffre dérivé n’est saisi à la main.</li>
<li><strong>Rédaction</strong> de la note, chaque phrase étiquetée fait sourcé, calcul ou interprétation.</li>
<li><strong>Contre-vérification</strong> par un agent indépendant chargé de trouver des erreurs, puis correction.</li>
<li><strong>Relecture experte</strong> avant toute diffusion des orientations de redressement.</li></ol></section>'''
open(os.path.join(DIST, 'methode.html'), 'w').write(page('Méthode · Courant', meth, 0, 'methode'))
landing = open(os.path.join(REPO, 'utility-site', 'landing.html')).read()
lb = landing[landing.index('<main'):landing.index('</main>') + 7] if '<main' in landing else ''
ls = re.search(r'<style>(.*?)</style>', landing, re.S).group(1)
about = f'<style>{ls} header.top{{display:none}}</style>' + lb.replace('<main class="wrap" id="top">', '<div>').replace('</main>', '</div>')
about = about.replace('window.AUI_FORM_LIVE', 'window.AUI_FORM_LIVE')
open(os.path.join(DIST, 'a-propos.html'), 'w').write(page('À propos · Courant', about, 0, 'apropos').replace('</body>', landing[landing.index('<script>'):landing.index('</script>') + 9] + '<script>window.AUI_FORM_LIVE=true</script></body>') if '<script>' in landing else page('À propos · Courant', about, 0, 'apropos'))

# ---------------- assets
shutil.copy(os.path.join(ROOT, 'site.css'), os.path.join(DIST, 'assets', 'site.css'))
shutil.copy(os.path.join(ROOT, 'site.js'), os.path.join(DIST, 'assets', 'site.js'))
shutil.copy(os.path.join(REPO, 'brand', 'courant', 'favicon.svg'), os.path.join(DIST, 'favicon.svg'))
cfg = {'supabaseUrl': os.environ.get('SUPABASE_URL', ''), 'supabaseAnonKey': os.environ.get('SUPABASE_ANON_KEY', '')}
open(os.path.join(DIST, 'assets', 'config.js'), 'w').write('window.COURANT = ' + json.dumps(cfg) + ';\n')
print('built', len(os.listdir(os.path.join(DIST, 'u'))), 'utility pages;', len(manifest), 'protected files;', n_notes, 'notes')
