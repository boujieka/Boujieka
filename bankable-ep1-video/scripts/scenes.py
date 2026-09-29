"""Cartoon scene backgrounds and props (1920x1080 SVG), in the book's flat style.

Scenes let the puppets act out situations that have no page in the book:
a signing ceremony, a cabinet table with empty chairs, an office, a dark city.
"""
from lang import ui

INK = "#1d2230"


def _office(flag=True):
    return (f'<rect width="1920" height="1080" fill="#e6ede8"/>'
            f'<rect x="220" y="150" width="520" height="400" fill="#bfe0f2" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M 480 150 V 550 M 220 350 H 740" stroke="{INK}" stroke-width="8"/>'
            f'<circle cx="640" cy="240" r="46" fill="#fbf1c2"/>'
            + (f'<path d="M 1640 120 V 560" stroke="#8a6a3a" stroke-width="10"/><circle cx="1640" cy="116" r="12" fill="#f0b429"/>'
               f'<rect x="1646" y="130" width="100" height="130" fill="#13615f" stroke="{INK}" stroke-width="5"/>'
               f'<rect x="1746" y="130" width="120" height="130" fill="#f0b429" stroke="{INK}" stroke-width="5"/>'
               f'<circle cx="1806" cy="195" r="26" fill="#fff"/>' if flag else "") +
            f'<rect y="760" width="1920" height="320" fill="#c9b08a"/><path d="M 0 760 H 1920" stroke="{INK}" stroke-width="6"/>')


def _ceremony(banner="ceremony"):
    lights = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity="0.9"/>'
                     for x, y, r in [(200, 170, 16), (1720, 210, 20), (1560, 120, 12), (380, 280, 10), (1320, 90, 14)])
    crowd = "".join(f'<circle cx="{60 + i * 120}" cy="1000" r="70" fill="{c}"/>'
                    for i, c in enumerate(["#2c3e66", "#7a3b4a", "#3b6b5a", "#6a4a2f"] * 4))
    return (f'<rect width="1920" height="1080" fill="#8a2130"/>'
            f'<rect x="0" y="0" width="1920" height="1080" fill="url(#spot)"/>'
            f'<rect x="460" y="70" width="1000" height="130" rx="14" fill="#13615f" stroke="{INK}" stroke-width="8"/>'
            f'<text x="960" y="160" text-anchor="middle" font-family="Bangers" font-size="84" fill="#fff">{ui(banner)}</text>'
            + lights +
            f'<rect x="300" y="690" width="1320" height="60" fill="#6b4a2c" stroke="{INK}" stroke-width="6"/>'
            f'<rect x="330" y="750" width="1260" height="200" fill="#7c5634" stroke="{INK}" stroke-width="6"/>' + crowd)


def _cabinet():
    return (f'<rect width="1920" height="1080" fill="#e9e2d2"/>'
            f'<rect x="700" y="120" width="520" height="300" fill="#bfe0f2" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M 960 120 V 420 M 700 270 H 1220" stroke="{INK}" stroke-width="8"/>'
            f'<rect y="820" width="1920" height="260" fill="#c9b08a"/>')


def _city():
    b = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{1080 - y}" fill="#1c2748" stroke="#0b1022" stroke-width="4"/>'
                for x, y, w in [(0, 520, 220), (230, 420, 180), (420, 600, 200), (640, 380, 240), (900, 500, 200),
                                (1120, 340, 220), (1360, 560, 180), (1560, 450, 200), (1770, 520, 150)])
    wins = "".join(f'<rect x="{x}" y="{y}" width="22" height="30" fill="#f6c945"/>'
                   for x, y in [(60, 600), (280, 520), (700, 460), (760, 700), (950, 640), (1180, 420), (1420, 660), (1600, 560), (1820, 640)])
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#fff"/>' for x, y in [(120, 90), (430, 160), (820, 70), (1260, 140), (1650, 90), (1500, 250)])
    return f'<rect width="1920" height="1080" fill="#0f1733"/>{stars}{b}{wins}'


BACKGROUNDS = {"office": _office, "ceremony": _ceremony, "closing": lambda: _ceremony("closing"), "cabinet": _cabinet, "city": _city}

DEFS = ('<defs><radialGradient id="spot" cx="50%" cy="30%" r="70%"><stop offset="0" stop-color="#ffd27a" stop-opacity="0.35"/>'
        '<stop offset="1" stop-color="#000" stop-opacity="0.25"/></radialGradient></defs>')


def background(name):
    return f'<svg class="bg" viewBox="0 0 1920 1080" width="1920" height="1080">{DEFS}{BACKGROUNDS[name]()}</svg>'


def prop(kind, x, y, label="", s=1.0):
    """Positioned SVG props (stage pixels)."""
    if kind == "chair":  # an empty chair with a name card: the absent risk bearer
        body = (f'<rect x="-90" y="-170" width="180" height="200" rx="18" fill="#6b4a2c" stroke="{INK}" stroke-width="7"/>'
                f'<rect x="-110" y="20" width="220" height="40" rx="10" fill="#7c5634" stroke="{INK}" stroke-width="7"/>'
                f'<rect x="-100" y="60" width="16" height="120" fill="#5a3d23"/><rect x="84" y="60" width="16" height="120" fill="#5a3d23"/>'
                f'<rect x="-120" y="-250" width="240" height="64" rx="8" fill="#fff" stroke="{INK}" stroke-width="5"/>'
                f'<text x="0" y="-206" text-anchor="middle" font-family="Poppins" font-weight="700" font-size="{30 if len(label) <= 11 else 22}" fill="{INK}">{label}</text>')
        return f'<svg class="prop" style="left:{x - 150 * s}px;top:{y - 280 * s}px" width="{300 * s}" height="{480 * s}" viewBox="-150 -280 300 480">{body}</svg>'
    if kind == "table":
        return (f'<svg class="prop" style="left:{x}px;top:{y}px" width="{label or 1400}" height="120" viewBox="0 0 {label or 1400} 120">'
                f'<rect x="0" y="0" width="{label or 1400}" height="44" fill="#6b4a2c" stroke="{INK}" stroke-width="6"/>'
                f'<rect x="20" y="44" width="{(label or 1400) - 40}" height="76" fill="#7c5634" stroke="{INK}" stroke-width="6"/></svg>')
    if kind == "doc":  # a signed document with a pen
        return (f'<svg class="prop" style="left:{x}px;top:{y}px" width="{220 * s}" height="{150 * s}" viewBox="0 0 220 150">'
                f'<rect x="10" y="10" width="170" height="130" fill="#fff" stroke="{INK}" stroke-width="5" transform="rotate(-6 95 75)"/>'
                f'<path d="M 40 50 H 150 M 40 75 H 150 M 40 100 Q 70 90 100 104 T 150 96" stroke="#9aa3b5" stroke-width="5" fill="none" transform="rotate(-6 95 75)"/>'
                f'<rect x="150" y="30" width="14" height="110" rx="6" fill="#13615f" stroke="{INK}" stroke-width="4" transform="rotate(35 157 85)"/></svg>')
    if kind == "sign":  # a hanging sign / placard
        return (f'<div class="placard" style="left:{x}px;top:{y}px;transform:scale({s})">{label}</div>')
    raise ValueError(kind)
