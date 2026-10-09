"""Verify extracted values against the source text: quote must appear on the stated page; number must appear in quote.
Then reconcile the same item/year reported by several documents. Usage: verify.py extraction.json paged_dir out.json"""
import json, re, sys, collections

ext_path, paged_dir, out_path = sys.argv[1:4]
docs = json.load(open(ext_path))

def pages_of(fname):
    txt = open(f'{paged_dir}/{fname}', encoding='utf-8', errors='replace').read()
    parts = re.split(r'\n=== PAGE (\d+) ===\n', txt)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}

ws = lambda s: re.sub(r'\s+', ' ', s).strip()
digits = lambda s: re.sub(r'[^\d]', '', s)

rows, sigs = [], []
for d in docs:
    pg = {f: pages_of(f) for f in d['files']}
    def locate(quote, page):
        """exact on page > whitespace-normalised on page > anywhere (wrong page)."""
        for f, P in pg.items():
            t = P.get(page, '')
            if quote in t: return 'exact', f, page
        for f, P in pg.items():
            if ws(quote) and ws(quote) in ws(P.get(page, '')): return 'ws_normalised', f, page
        for f, P in pg.items():
            for p, t in P.items():
                if ws(quote) and ws(quote) in ws(t): return 'other_page', f, p
        return 'not_found', None, None
    for v in d['values']:
        status, f, p = locate(v['quote'], v['page'])
        num_ok = bool(digits(v['value_raw'])) and digits(v['value_raw']) in digits(v['quote'])
        rows.append({**v, 'doc': d['key'], 'file': f, 'found_page': p, 'quote_check': status, 'number_in_quote': num_ok,
                     'verified': status in ('exact', 'ws_normalised', 'other_page') and num_ok})
    for s in d['signals']:
        status, f, p = locate(s['quote'], s['page'])
        sigs.append({**s, 'doc': d['key'], 'file': f, 'found_page': p, 'quote_check': status, 'verified': status != 'not_found'})

# reconciliation: same item + fiscal_year from different docs (verified values only)
by = collections.defaultdict(list)
for r in rows:
    if r['verified']:
        by[(r['item'], r['fiscal_year'])].append(r)
recon = []
for (item, fy), rs in sorted(by.items()):
    vals = sorted({round(r['value'], 3) for r in rs})
    docs_ = sorted({r['doc'] for r in rs})
    if len(docs_) > 1:
        spread = (max(vals) - min(vals)) / abs(max(vals)) if max(vals) else 0
        recon.append({'item': item, 'fiscal_year': fy, 'docs': docs_, 'values': vals, 'relative_spread': round(spread, 4)})

c = collections.Counter((r['quote_check'], r['number_in_quote']) for r in rows)
summary = {'values': len(rows), 'verified': sum(r['verified'] for r in rows), 'checks': {f'{k[0]}|num={k[1]}': n for k, n in c.items()},
           'signals': len(sigs), 'signals_verified': sum(s['verified'] for s in sigs),
           'reconciled_pairs': len(recon), 'disagreements_gt_1pct': sum(1 for r in recon if r['relative_spread'] > 0.01)}
json.dump({'summary': summary, 'values': rows, 'signals': sigs, 'reconciliation': recon}, open(out_path, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(summary, indent=1))
