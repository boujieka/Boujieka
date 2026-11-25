"""Generates the DiaspoSwap mark and logo SVGs from exact geometry (run: python3 generate.py)."""
import math

PETROL, EMERALD, GOLD, IVORY, ANTHRACITE = '#082F35', '#087F6D', '#C9A44C', '#FAF8F2', '#182525'
C, R, SW = 64.0, 47.0, 7.0

def pt(theta, r=R):
    t = math.radians(theta)
    return C + r * math.cos(t), C + r * math.sin(t)

def arc_with_arrow(a0, a1, color):
    # arc from a0 to a1 (clockwise in screen coords), arrowhead at a1
    stop = a1 - 7  # leave room for the head
    x0, y0 = pt(a0); x1, y1 = pt(stop)
    large = 1 if (stop - a0) % 360 > 180 else 0
    path = f'<path d="M{x0:.2f} {y0:.2f} A{R} {R} 0 {large} 1 {x1:.2f} {y1:.2f}" fill="none" stroke="{color}" stroke-width="{SW}" stroke-linecap="round"/>'
    # arrowhead: base centred on the arc at `stop`, tip further along the circle
    tip = pt(a1 + 4)
    bo, bi = pt(stop, R + 7.5), pt(stop, R - 7.5)
    head = f'<path d="M{bo[0]:.2f} {bo[1]:.2f} L{tip[0]:.2f} {tip[1]:.2f} L{bi[0]:.2f} {bi[1]:.2f} Z" fill="{color}" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>'
    return path + head

def wings(color):
    out = []
    for y, L, tilt in [(53, 29, 5), (63.5, 23, 3), (74, 16, 1.5)]:
        for s in (1, -1):
            x0 = C + s * 7.5
            xt = C + s * (7.5 + L)
            pts = [(x0, y - 3.2), (xt, y - 3.2 - tilt), (xt - s * 5, y + 3.2 - tilt), (x0, y + 3.2)]
            out.append('<path d="M' + ' L'.join(f'{x:.2f} {yy:.2f}' for x, yy in pts) + f' Z" fill="{color}"/>')
    return ''.join(out)

def axis(color):
    # Maat balance axis: slender lozenge with a feather-like rounded crown
    return (f'<path d="M64 33 C67.5 37 68.6 41 68.4 46 L66.2 82 L64 88 L61.8 82 L59.6 46 C59.4 41 60.5 37 64 33 Z" fill="{color}"/>')

def mark(top, bottom, wing, ax, bg=None, size=128):
    body = arc_with_arrow(195, 345, top) + arc_with_arrow(15, 165, bottom) + wings(wing) + axis(ax)
    rect = f'<rect width="128" height="128" rx="28" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="{size}" height="{size}" role="img" aria-label="DiaspoSwap">'
            f'<title>DiaspoSwap</title>{rect}{body}</svg>\n')

def inner(top, bottom, wing, ax):
    return arc_with_arrow(195, 345, top) + arc_with_arrow(15, 165, bottom) + wings(wing) + axis(ax)

FONT = "font-family=\"'Plus Jakarta Sans','Inter','Segoe UI',Arial,sans-serif\" font-weight=\"700\""

def horizontal(dark=False):
    word1 = IVORY if dark else PETROL
    m = inner(GOLD, IVORY if dark else EMERALD, IVORY if dark else PETROL, GOLD)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 128" width="520" height="128" role="img" aria-label="DiaspoSwap">'
            f'<title>DiaspoSwap</title>{m}'
            f'<text x="140" y="82" {FONT} font-size="54" letter-spacing="-1"><tspan fill="{word1}">Diaspo</tspan><tspan fill="{GOLD}">Swap</tspan></text></svg>\n')

def stacked():
    m = inner(GOLD, EMERALD, PETROL, GOLD)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 205" width="320" height="205" role="img" aria-label="DiaspoSwap">'
            f'<title>DiaspoSwap</title><g transform="translate(96 0)">{m}</g>'
            f'<text x="160" y="168" text-anchor="middle" {FONT} font-size="44" letter-spacing="-1"><tspan fill="{PETROL}">Diaspo</tspan><tspan fill="{GOLD}">Swap</tspan></text>'
            f'<text x="160" y="196" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" fill="{ANTHRACITE}">L’argent circule localement. La valeur voyage.</text></svg>\n')

files = {
    'mark-light.svg': mark(GOLD, EMERALD, PETROL, GOLD),
    'mark-dark.svg': mark(GOLD, IVORY, IVORY, GOLD),
    'mark-mono-dark.svg': mark(PETROL, PETROL, PETROL, PETROL),
    'mark-mono-light.svg': mark(IVORY, IVORY, IVORY, IVORY),
    'app-icon.svg': mark(GOLD, IVORY, IVORY, GOLD, bg=PETROL),
    'icon-square.svg': mark(GOLD, IVORY, IVORY, GOLD, bg=PETROL).replace('rx="28"', 'rx="0"'),
    'adaptive-foreground.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -40 208 208" width="208" height="208">' + inner(GOLD, IVORY, IVORY, GOLD) + '</svg>\n',
    'adaptive-monochrome.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -40 208 208" width="208" height="208">' + inner('#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF') + '</svg>\n',
    'logo-horizontal-light.svg': horizontal(False),
    'logo-horizontal-dark.svg': horizontal(True),
    'logo-stacked.svg': stacked(),
}
for name, svg in files.items():
    open(name, 'w').write(svg)
print('\n'.join(files))
