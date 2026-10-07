"""Inline the logo SVGs into sheet.src.html -> brand-sheet.html (artifact page)."""
import re, os
here = os.path.dirname(os.path.abspath(__file__))
def svg(name, style='height:100%;width:auto;max-width:100%;display:block'):
    s = open(os.path.join(here, name)).read().strip()
    s = re.sub(r'<title>.*?</title>', '', s)
    return s.replace('<svg ', f'<svg style="{style}" ', 1)
src = open(os.path.join(here, 'sheet.src.html')).read()
for k in ['logo-tagline', 'logo-tagline-dark', 'logo', 'logo-dark', 'mark', 'mark-dark']:
    src = src.replace('{{' + k + '}}', svg(f'courant-{k}.svg'))
for px in (64, 32, 16):
    src = src.replace('{{fav-%d}}' % px, svg('favicon.svg', f'width:{px}px;height:{px}px;display:block'))
assert '{{' not in src
open(os.path.join(here, 'brand-sheet.html'), 'w').write(src)
print('ok')
