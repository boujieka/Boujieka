"""Shared pieces for the "MoU Trap" training series (Chapter 1 of Bankable Is Not Enough).

Real cases (Nigeria, Qua Iboe, Ghana, Nachtigal) appear only as sourced data
cards, with the chapter's own caveats. The cartoon characters are fictional and
play generic roles; they never portray a real person.
"""
from v2cards import *  # noqa: F401,F403
from v2cards import esc, part, screen, badge
from lang import ui, LANG

ROLES = {
    "KERBU": ("MINISTER KERBU", "Government · signs the MoU"),
    "ENILEC": ("ENILEC MOK", "Ministry of Finance · the backstop"),
    "PAUL": ("PAUL AHMAK", "Utility · the buyer who must pay"),
    "EMSON": ("EMSON ANAHCT", "Developer · holds the option"),
    "TIDIANIE": ("TIDIANIE EUGOM", "Lender · arrives last"),
    "BELPAU": ("BELPAU", "Analyst · asks the questions"),
    "RESIDENT": ("RESIDENT", "Consumer"),
}


ROLES_FR = {
    "KERBU": ("MINISTRE KERBU", "Gouvernement · signe le MoU"),
    "ENILEC": ("ENILEC MOK", "Ministère des Finances · le dernier rempart"),
    "PAUL": ("PAUL AHMAK", "Compagnie d'électricité · l'acheteur qui paie"),
    "EMSON": ("EMSON ANAHCT", "Développeur · détient l'option"),
    "TIDIANIE": ("TIDIANIE EUGOM", "Prêteur · arrive en dernier"),
    "BELPAU": ("BELPAU", "Analyste · pose les questions"),
    "RESIDENT": ("RÉSIDENT", "Consommateur"),
}
if LANG == "fr":
    ROLES = ROLES_FR


def logo_intro(hold=3.6):
    """Opening card with the Courant Continental logo; visible from the very first frame."""
    s = screen("logo", [part('<img class="brand" src="assets/art/courant-continental.png" alt="Courant Continental"/>', [], hold)],
               None, "theme", "act", tail=0.6)
    s["first_visible"] = True
    return s


def stat(value, label, source, spoken, code="fact", hold=0.8, music=None, sting=None):
    return screen("big", [part(badge(code)),
                          part(f'<div class="stat">{value}</div><div class="stat-l">{label}</div>', spoken, hold),
                          part(f'<div class="src">{ui("source")} {esc(source)}</div>', [], 0.3)],
                  code, music or ("drone" if code == "red" else "bed"), sting)


def quote(text, source, spoken, code="fact", hold=1.0):
    return screen("big", [part(badge(code)),
                          part(f'<div class="big-text">&ldquo;{esc(text)}&rdquo;</div>', spoken, hold),
                          part(f'<div class="src">{esc(source)}</div>', [], 0.3)],
                  code, "drone" if code == "red" else "tension")


def fact(text, spoken, source=None, code="fact", sub=None, hold=0.8, music=None, sting=None):
    parts = [part(badge(code))] if code else []
    parts.append(part(f'<div class="big-text">{text}</div>', spoken, hold))
    if sub:
        parts.append(part(f'<div class="big-sub">{sub[0]}</div>', sub[1], 0.6))
    if source:
        parts.append(part(f'<div class="src">{ui("source")} {esc(source)}</div>', [], 0.3))
    return screen("big", parts, code, music or ("drone" if code == "red" else "bed"), sting)


def table(title, head, rows, spoken_rows, intro=(), source="author (Chapter 1)", code="fact", cols=None):
    """Grid table whose rows appear one by one (columns stay aligned)."""
    cols = cols or " ".join(["1fr"] * len(head))
    hdr = "".join(f"<div>{esc(h)}</div>" for h in head)
    parts = [part(badge(code)), part(f'<div class="dn-q">{esc(title)}</div>', intro, 0.2),
             part(f'<div class="trow th" style="grid-template-columns:{cols}">{hdr}</div>', [], 0.2)]
    for r, sp in zip(rows, spoken_rows):
        cells = "".join(f"<div>{esc(c)}</div>" for c in r)
        parts.append(part(f'<div class="trow" style="grid-template-columns:{cols}">{cells}</div>', sp, 0.3))
    parts.append(part(f'<div class="src">{ui("source")} {esc(source)}</div>', [], 0.8))
    return screen("table", parts, code, "bed")


def layers(title, items, intro=(), code="decision", music="bed", closing=None):
    """items: [(name, text, sub, spoken)] stacked cards revealed one by one."""
    parts = [part(badge(code)), part(f'<div class="dn-q">{esc(title)}</div>', intro, 0.2)]
    for name, text, sub, spoken in items:
        parts.append(part(f'<div class="layer"><b>{esc(name)}</b><span>{esc(text)}'
                          f'{f"<em>{esc(sub)}</em>" if sub else ""}</span></div>', spoken, 0.25))
    if closing:
        parts.append(part(f'<div class="dn-x">{esc(closing[0])}</div>', closing[1], 0.9))
    return screen("layers", parts, code, music)


def timeline(title, events, intro, source, code="fact"):
    parts = [part(badge(code)), part(f'<div class="dn-q">{esc(title)}</div>', intro, 0.2)]
    row = []
    for year, text, spoken in events:
        row.append(part(f'<div class="tl-i"><b>{esc(year)}</b><span>{esc(text)}</span></div>', spoken, 0.25))
    parts += row
    parts.append(part(f'<div class="src">{ui("source")} {esc(source)}</div>', [], 0.8))
    return screen("timeline", parts, code, "tension")


def trap_title(kicker, line1, line2, sub, spoken):
    return screen("title", [part(f'<div class="kicker">{esc(kicker)}</div>'),
                            part(f'<div class="t1">{line1}</div><div class="t2">{line2}</div>', spoken, 0.4),
                            part(f'<div class="ep">{esc(sub)}</div><div class="lineup"></div>'
                                 '<div class="author">EMMANUEL BOUJIEKA KAMGA</div>', [], 1.2)],
                  None, "theme", "act")


def trap_lesson(l1, l2, l3):
    return screen("lesson", [part(f'<div class="ls1">{l1[0]}</div>', l1[1], 0.6),
                             part(f'<div class="ls2">{l2[0]}</div>', l2[1], 0.8),
                             part(f'<div class="ls3">{l3[0]}</div>', l3[1], 2.0)],
                  None, "theme", "act")


def trap_credits():
    if LANG == "fr":
        head = '<div class="cr-t">LE PIÈGE DU MoU</div><div class="cr-s">BANCABLE NE SUFFIT PAS · PARTIE I · CHAPITRE 1</div>'
        body = ('<p>D&rsquo;après &laquo; The MoU trap &raquo;, chapitre 1 de <i>Bankable Is Not Enough</i>, d&rsquo;Emmanuel Boujieka Kamga.</p>'
                '<p>Les chiffres des cas proviennent des sources citées à l&rsquo;écran, avec les réserves du chapitre. '
                'La liste complète des références figure dans le chapitre.</p>'
                '<p>Les personnages sont fictifs et jouent des rôles génériques. Ils ne représentent aucune personne ni institution réelle.</p>'
                '<p>À des fins de formation et de renforcement des capacités. Ne constitue pas un conseil juridique, financier ou d&rsquo;investissement.</p>'
                '<p class="dim">Voix de synthèse (Kokoro-82M). Musique générée de façon procédurale.</p>')
    else:
        head = '<div class="cr-t">THE MoU TRAP</div><div class="cr-s">BANKABLE IS NOT ENOUGH · PART I · CHAPTER 1</div>'
        body = ('<p>Based on &ldquo;The MoU trap&rdquo;, Chapter 1 of <i>Bankable Is Not Enough</i>, by Emmanuel Boujieka Kamga.</p>'
                '<p>Case figures are taken from the sources cited on screen, with the chapter&rsquo;s caveats. '
                'The full reference list is in the chapter.</p>'
                '<p>The cartoon characters are fictional and play generic roles. They do not represent any real person or institution.</p>'
                '<p>For education and capacity building. Not legal, financial or investment advice.</p>'
                '<p class="dim">Voices are synthetic (Kokoro-82M). Music is procedurally generated.</p>')
    return screen("credits", [part(head), part(body, [], 6.0)], None, "theme")


def brief_title(audience, hook, spoken):
    return screen("act", [part(f'<div class="act-label">BRIEFING · {esc(audience)}</div>'),
                          part(f'<div class="act-title">{hook}</div>', spoken, 1.0),
                          part('<div class="src" style="color:#cfe3df">' + ("Le piège du MoU · Bancable ne suffit pas, chapitre 1" if LANG == "fr"
                  else "The MoU Trap · Bankable Is Not Enough, Chapter 1") + '</div>', [], 0.4)],
                  None, "theme", "act", 0)
