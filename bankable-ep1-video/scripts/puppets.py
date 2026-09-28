"""SVG puppets of the six characters, drawn in the book's flat outline style,
wearing formal West/Central African attire.

Puppet space: head radius 100, face centre at (0, 0). The body extends down to
y=460 and is clipped by the panel. Animated parts carry ids:
  {pid}-head   head group (rotation / nod, pivot at the neck)
  {pid}-mouth  mouth group (scaleY 0.14 closed .. 1 open, pivot y=46)
  {pid}-lids   eyelids (scaleY 0 open .. 1 closed, pivot y=-24)
  {pid}-body   torso (breathing)
"""

INK = "#1d2230"
SW = 4.2  # outline width in puppet units

SKIN = {
    "BELPAU": "#6b4027", "ENILEC": "#5a3322", "KERBU": "#4f2e1f",
    "EMSON": "#5c3624", "TIDIANIE": "#b07a52", "PAUL": "#5a3423",
}


def _eyes(pid, skin, look, glasses=False):
    lx = 5 * look
    s = []
    for ex in (-38, 38):
        s.append(f'<circle cx="{ex}" cy="-6" r="17" fill="#fff" stroke="{INK}" stroke-width="{SW * 0.8}"/>')
        s.append(f'<circle cx="{ex + lx}" cy="-5" r="8.5" fill="{INK}"/>')
        s.append(f'<circle cx="{ex + lx + 3}" cy="-8" r="2.6" fill="#fff"/>')
    # eyelids: skin discs clipped to each eye, collapsed by default
    lids = "".join(
        f'<clipPath id="{pid}-ec{i}"><circle cx="{ex}" cy="-6" r="17.5"/></clipPath>'
        f'<rect clip-path="url(#{pid}-ec{i})" x="{ex - 19}" y="-25" width="38" height="38" fill="{skin}"/>'
        for i, ex in enumerate((-38, 38)))
    s.append(f'<g id="{pid}-lids" transform="matrix(1 0 0 0.001 0 -23.98)">{lids}'
             f'<path d="M -56 -6 L -20 -6 M 20 -6 L 56 -6" stroke="{INK}" stroke-width="3" opacity="0"/></g>')
    if glasses:
        s.append(f'<rect x="-64" y="-30" width="52" height="46" rx="14" fill="none" stroke="{INK}" stroke-width="6"/>'
                 f'<rect x="12" y="-30" width="52" height="46" rx="14" fill="none" stroke="{INK}" stroke-width="6"/>'
                 f'<path d="M -12 -12 Q 0 -18 12 -12" fill="none" stroke="{INK}" stroke-width="5"/>')
    return "".join(s)


def _brows(mood, color):
    # (inner y, outer y) per mood; inner end is nearest the nose
    iy, oy = {"neutral": (-44, -46), "angry": (-36, -50), "worried": (-50, -40), "happy": (-48, -44)}[mood]
    return (f'<path d="M -22 {iy} L -58 {oy}" stroke="{color}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M 22 {iy} L 58 {oy}" stroke="{color}" stroke-width="9" stroke-linecap="round"/>')


def _mouth(pid):
    return (f'<g id="{pid}-mouth" transform="matrix(1 0 0 0.14 0 39.56)">'
            f'<path d="M -21 46 Q 0 44 21 46 Q 20 74 0 76 Q -20 74 -21 46 Z" fill="#5a1717" stroke="{INK}" stroke-width="3.5"/>'
            f'<path d="M -11 68 Q 0 60 11 68 Q 0 75 -11 68 Z" fill="#e2707a"/></g>')


def _face(pid, who, skin, look, mood, extra_front="", hair_back="", hair_front="", brow="#241510", glasses=False, beard=""):
    return (hair_back +
            f'<circle cx="-99" cy="6" r="17" fill="{skin}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<circle cx="99" cy="6" r="17" fill="{skin}" stroke="{INK}" stroke-width="{SW}"/>'
            f'<circle cx="0" cy="0" r="100" fill="{skin}" stroke="{INK}" stroke-width="{SW}"/>'
            + hair_front +
            f'<ellipse cx="-50" cy="30" rx="17" ry="10" fill="#c2534a" opacity="0.45"/>'
            f'<ellipse cx="50" cy="30" rx="17" ry="10" fill="#c2534a" opacity="0.45"/>'
            + _brows(mood, brow) + _eyes(pid, skin, look, glasses) +
            f'<path d="M -3 8 Q 9 22 -5 30" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/>'
            + beard + _mouth(pid) + extra_front)


def _neck(skin):
    return (f'<path d="M -26 80 L -26 150 L 26 150 L 26 80" fill="{skin}" stroke="{INK}" stroke-width="{SW}"/>')


# ------------------------------------------------------------------ outfits
def _ankara(pid, name, base, c1, c2, scale=1.0):
    s = 34 * scale
    return (f'<pattern id="{pid}-{name}" width="{s}" height="{s}" patternUnits="userSpaceOnUse">'
            f'<rect width="{s}" height="{s}" fill="{base}"/>'
            f'<circle cx="{s / 2}" cy="{s / 2}" r="{s * 0.28}" fill="{c1}"/>'
            f'<circle cx="{s / 2}" cy="{s / 2}" r="{s * 0.12}" fill="{c2}"/>'
            f'<circle cx="0" cy="0" r="{s * 0.1}" fill="{c2}"/><circle cx="{s}" cy="{s}" r="{s * 0.1}" fill="{c2}"/></pattern>')


def body_kerbu(pid, skin):
    # Grand agbada in royal navy with gold embroidery.
    gold = "#e2b13c"
    return (f'<path d="M -270 470 C -262 280 -190 170 -70 142 L 70 142 C 190 170 262 280 270 470 Z" fill="#23386e" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M -150 470 C -140 330 -110 250 -60 205 M 150 470 C 140 330 110 250 60 205" fill="none" stroke="#1a2a55" stroke-width="5"/>'
            + _neck(skin) +
            f'<path d="M -54 140 Q 0 215 54 140" fill="#23386e" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M -64 144 Q 0 232 64 144" fill="none" stroke="{gold}" stroke-width="11"/>'
            f'<path d="M -64 144 Q 0 232 64 144" fill="none" stroke="#fff3c4" stroke-width="3" stroke-dasharray="4 10"/>'
            f'<rect x="-20" y="196" width="40" height="150" rx="8" fill="none" stroke="{gold}" stroke-width="7"/>'
            f'<circle cx="0" cy="228" r="9" fill="{gold}"/><circle cx="0" cy="264" r="9" fill="{gold}"/><circle cx="0" cy="300" r="9" fill="{gold}"/>')


def head_kerbu(pid, skin, look, mood):
    gold = "#e2b13c"
    hair = (f'<path d="M -97 -18 Q -104 -46 -86 -58 L -80 -30 Z" fill="#a7a7a7" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M 97 -18 Q 104 -46 86 -58 L 80 -30 Z" fill="#a7a7a7" stroke="{INK}" stroke-width="3"/>')
    cap = (f'<path d="M -84 -52 Q -90 -128 0 -134 Q 90 -128 84 -52 Q 0 -70 -84 -52 Z" fill="#23386e" stroke="{INK}" stroke-width="{SW}"/>'
           f'<path d="M -84 -56 Q 0 -74 84 -56" fill="none" stroke="{gold}" stroke-width="10"/>'
           f'<path d="M -60 -100 Q 0 -112 60 -100" fill="none" stroke="{gold}" stroke-width="4" stroke-dasharray="3 9"/>')
    return _face(pid, "KERBU", skin, look, mood, hair_front=hair + cap, brow="#8a8a8a")


def body_enilec(pid, skin):
    # Buba blouse in blue ankara with coral beads.
    return ('<defs>' + _ankara(pid, "ank", "#2360a8", "#3d80c9", "#f0b429", 1.7) + '</defs>'
            f'<path d="M -240 470 C -236 300 -200 190 -120 160 Q -60 140 -40 142 L 40 142 Q 60 140 120 160 C 200 190 236 300 240 470 Z" fill="url(#{pid}-ank)" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M -200 250 Q -150 200 -120 162 M 200 250 Q 150 200 120 162" fill="none" stroke="{INK}" stroke-width="3"/>'
            + _neck(skin) +
            f'<path d="M -46 142 Q 0 196 46 142" fill="{skin}" stroke="{INK}" stroke-width="{SW}"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="7.5" fill="#d9442f" stroke="{INK}" stroke-width="1.6"/>'
                      for x, y in [(-40, 150), (-30, 164), (-18, 174), (-6, 179), (6, 179), (18, 174), (30, 164), (40, 150)]))


def head_enilec(pid, skin, look, mood):
    # Sculpted gele (headtie) in her blue-and-gold colours.
    # Sculpted gele: pleats fanning up from a band that hugs the head.
    petal = 'M -46 -70 Q -78 -178 0 -238 Q 78 -178 46 -70 Z'
    pleats = "".join(
        f'<g transform="rotate({a} 0 -70)"><path d="{petal}" fill="#2c6fbf" stroke="{INK}" stroke-width="{SW}"/>'
        f'<path d="M 0 -84 Q -10 -170 0 -224" fill="none" stroke="#f0b429" stroke-width="7" stroke-linecap="round"/></g>'
        for a in (-62, 62, -32, 32, 0))
    band = (f'<path d="M -106 -26 Q -114 -112 0 -120 Q 114 -112 106 -26 Q 0 -64 -106 -26 Z" fill="#2c6fbf" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M -104 -40 Q 0 -80 104 -40" fill="none" stroke="#f0b429" stroke-width="9"/>'
            f'<path d="M -98 -60 Q 0 -98 98 -60" fill="none" stroke="#153e73" stroke-width="4"/>')
    gele = pleats + band
    ear = f'<circle cx="-100" cy="30" r="8" fill="#f0b429" stroke="{INK}" stroke-width="2"/><circle cx="100" cy="30" r="8" fill="#f0b429" stroke="{INK}" stroke-width="2"/>'
    return _face(pid, "ENILEC", skin, look, mood, hair_front=gele, extra_front=ear)


def body_paul(pid, skin):
    # Senator-style kaftan in brown with embroidered placket.
    trim = "#caa165"
    return (f'<path d="M -236 470 C -232 290 -196 186 -96 156 L 96 156 C 196 186 232 290 236 470 Z" fill="#76502f" stroke="{INK}" stroke-width="{SW}"/>'
            + _neck(skin) +
            f'<path d="M -42 138 L -42 170 L 42 170 L 42 138" fill="#76502f" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M -42 168 L 42 168" stroke="{trim}" stroke-width="5"/>'
            f'<path d="M -16 170 L -16 380 M 16 170 L 16 380" stroke="{trim}" stroke-width="5"/>'
            f'<path d="M -16 170 L -16 380 M 16 170 L 16 380" stroke="#fff0cf" stroke-width="1.6" stroke-dasharray="3 7"/>'
            + "".join(f'<circle cx="0" cy="{y}" r="6" fill="{trim}" stroke="{INK}" stroke-width="1.5"/>' for y in (200, 240, 280, 320))
            + f'<path d="M 120 250 L 185 250 L 180 300 L 124 300 Z" fill="none" stroke="{trim}" stroke-width="4"/>')


def head_paul(pid, skin, look, mood):
    hair = (f'<path d="M -98 -12 Q -106 -70 -60 -88 Q 0 -104 60 -88 Q 106 -70 98 -12 Q 90 -48 60 -62 Q 0 -80 -60 -62 Q -90 -48 -98 -12 Z" fill="#a9a9a9" stroke="{INK}" stroke-width="3"/>')
    stache = f'<path d="M -30 44 Q -14 34 0 42 Q 14 34 30 44 Q 14 50 0 46 Q -14 50 -30 44 Z" fill="#2b2b2b" stroke="{INK}" stroke-width="2"/>'
    return _face(pid, "PAUL", skin, look, mood, hair_front=hair, extra_front=stache, brow="#8e8e8e")


def body_belpau(pid, skin):
    # Tailored navy blazer with ankara lapels over her signature yellow.
    return ('<defs>' + _ankara(pid, "lap", "#e8553f", "#f0b429", "#7a1f16", 0.7) + '</defs>'
            f'<path d="M -228 470 C -224 300 -190 190 -100 160 L 100 160 C 190 190 224 300 228 470 Z" fill="#1f3a5f" stroke="{INK}" stroke-width="{SW}"/>'
            + _neck(skin) +
            f'<path d="M -56 150 L 0 260 L 56 150 Z" fill="#f0b429" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M -84 158 L -56 150 L 0 262 L -22 470 L -44 470 L -30 300 L -96 214 Z" fill="url(#{pid}-lap)" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M 84 158 L 56 150 L 0 262 L 22 470 L 44 470 L 30 300 L 96 214 Z" fill="url(#{pid}-lap)" stroke="{INK}" stroke-width="{SW}"/>'
            f'<circle cx="0" cy="330" r="8" fill="#e2b13c" stroke="{INK}" stroke-width="2"/>')


def head_belpau(pid, skin, look, mood):
    back = "".join(f'<rect x="{x}" y="-40" width="24" height="{h}" rx="12" fill="#23150e" stroke="{INK}" stroke-width="3"/>'
                   for x, h in [(-128, 210), (-106, 225), (82, 225), (104, 210)])
    top = (f'<path d="M -100 -4 Q -108 -104 0 -110 Q 108 -104 100 -4 Q 96 -60 50 -74 Q 0 -60 -50 -74 Q -96 -60 -100 -4 Z" fill="#23150e" stroke="{INK}" stroke-width="3"/>')
    ear = f'<circle cx="-100" cy="30" r="6" fill="#1b8f8a" stroke="{INK}" stroke-width="2"/><circle cx="100" cy="30" r="6" fill="#1b8f8a" stroke="{INK}" stroke-width="2"/>'
    return _face(pid, "BELPAU", skin, look, mood, hair_back=back, hair_front=top, extra_front=ear, glasses=True)


def body_emson(pid, skin):
    # Charcoal business suit, white shirt, gold tie (SunRiver colour).
    return (f'<path d="M -232 470 C -228 300 -194 188 -100 158 L 100 158 C 194 188 228 300 232 470 Z" fill="#3a404d" stroke="{INK}" stroke-width="{SW}"/>'
            + _neck(skin) +
            f'<path d="M -56 148 L 0 270 L 56 148 Z" fill="#fff" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M -12 160 L 12 160 L 18 180 L 8 330 L 0 345 L -8 330 L -18 180 Z" fill="#e0a526" stroke="{INK}" stroke-width="3"/>'
            f'<path d="M -100 158 L -56 148 L 0 272 L -24 470 M 100 158 L 56 148 L 0 272 L 24 470" fill="none" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M 120 240 L 180 240 L 172 262 L 126 262 Z" fill="#fff" stroke="{INK}" stroke-width="2.5"/>')


def head_emson(pid, skin, look, mood):
    return _face(pid, "EMSON", skin, look, mood)


def body_tidianie(pid, skin):
    # Maroon tailored blazer, ivory blouse, pearls.
    return (f'<path d="M -226 470 C -222 300 -188 190 -98 160 L 98 160 C 188 190 222 300 226 470 Z" fill="#8c2a42" stroke="{INK}" stroke-width="{SW}"/>'
            + _neck(skin) +
            f'<path d="M -54 150 L 0 250 L 54 150 Z" fill="#f6ead8" stroke="{INK}" stroke-width="{SW}"/>'
            f'<path d="M -98 160 L -54 150 L 0 252 L -20 470 M 98 160 L 54 150 L 0 252 L 20 470" fill="none" stroke="{INK}" stroke-width="{SW}"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="5.5" fill="#fbf7ee" stroke="#b8b0a0" stroke-width="1.2"/>'
                      for x, y in [(-30, 150), (-21, 162), (-11, 170), (0, 173), (11, 170), (21, 162), (30, 150)]))


def head_tidianie(pid, skin, look, mood):
    top = (f'<circle cx="0" cy="-116" r="34" fill="#2a1a12" stroke="{INK}" stroke-width="3"/>'
           f'<path d="M -100 -4 Q -106 -102 0 -106 Q 106 -102 100 -4 Q 94 -62 0 -72 Q -94 -62 -100 -4 Z" fill="#2a1a12" stroke="{INK}" stroke-width="3"/>')
    ear = f'<circle cx="-100" cy="30" r="6" fill="#fbf7ee" stroke="#8d8577" stroke-width="2"/><circle cx="100" cy="30" r="6" fill="#fbf7ee" stroke="#8d8577" stroke-width="2"/>'
    return _face(pid, "TIDIANIE", skin, look, mood, hair_front=top, extra_front=ear)


BUILD = {
    "KERBU": (body_kerbu, head_kerbu), "ENILEC": (body_enilec, head_enilec),
    "PAUL": (body_paul, head_paul), "BELPAU": (body_belpau, head_belpau),
    "EMSON": (body_emson, head_emson), "TIDIANIE": (body_tidianie, head_tidianie),
}


SLEEVE = {"BELPAU": "#1f3a5f", "ENILEC": "#2360a8", "KERBU": "#23386e", "EMSON": "#3a404d",
          "TIDIANIE": "#8c2a42", "PAUL": "#76502f"}


def raised_arm(pid, who, skin):
    """Hand raised beside the body (covers the book's raised-hand pose)."""
    col = SLEEVE[who]
    return (f'<g id="{pid}-arm">'
            f'<path d="M 110 262 L 232 92" stroke="{INK}" stroke-width="80" stroke-linecap="round"/>'
            f'<path d="M 110 262 L 232 92" stroke="{col}" stroke-width="70" stroke-linecap="round"/>'
            f'<path d="M 206 60 Q 200 22 214 18 L 222 40 L 226 8 Q 238 2 242 12 L 244 38 L 252 12 Q 264 10 266 22 L 262 46 L 272 30 Q 284 32 280 46 L 266 88 Q 248 110 222 100 Q 202 88 206 60 Z" '
            f'fill="{skin}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round"/></g>')


def puppet_svg(pid, who, look=0.0, mood="neutral", arm=False):
    """Return the inner SVG markup for one puppet (no <svg> wrapper)."""
    skin = SKIN[who]
    body, head = BUILD[who]
    return (f'<g id="{pid}-body">{body(pid, skin)}</g>'
            + (raised_arm(pid, who, skin) if arm else "") +
            f'<g id="{pid}-head">{head(pid, skin, look, mood)}</g>')
