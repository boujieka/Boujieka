"""Shot helpers for the v2 (training + short) storyboards.

A shot is a dict. Panel shots frame the book art (with talking puppets);
screen shots are designed "one idea" screens made of parts that appear one
after another, each with the lines spoken while it is on screen.

Visual codes (constant across the series):
  FACT      blue    documented information
  DECISION  yellow  what the decision-maker must examine
  RED TEAM  red     what could make the deal fail
"""
import html as _h

N, B, E, T, K, M, P = "NARRATOR", "BELPAU", "ENILEC", "TIDIANIE", "KERBU", "EMSON", "PAUL"
esc = _h.escape

ROLES = {  # each character is a voice of risk
    "KERBU": ("MINISTER KERBU", "Political commitment"),
    "ENILEC": ("ENILEC MOK", "Fiscal risk · Public Debt"),
    "PAUL": ("PAUL AHMAK", "Offtaker risk · KivoElec"),
    "EMSON": ("EMSON ANAHCT", "Project bankability · Developer"),
    "TIDIANIE": ("TIDIANIE EUGOM", "Debt service · Lender"),
    "BELPAU": ("BELPAU", "Due diligence · Analyst"),
    "RESIDENT": ("RESIDENT", "Kivona"),
}


def panel(page, idx, lines, cut=False, music="bed"):
    return {"kind": "panel", "page": page, "panel": idx, "lines": lines, "cut": cut, "music": music}


def pan(page, a, b, lines, music="tension"):
    return {"kind": "pan", "page": page, "a": a, "b": b, "lines": lines, "cut": False, "music": music}


def part(html, lines=(), hold=0.0, cls="", countdown=0):
    return {"html": html, "lines": list(lines), "hold": hold, "cls": cls, "countdown": countdown}


def screen(layout, parts, code=None, music="bed", sting=None, chapter=None, tail=0.9):
    return {"kind": "screen", "layout": layout, "parts": parts, "code": code, "music": music,
            "sting": sting, "chapter": chapter, "tail": tail}


def badge(code):
    label = {"fact": "FACT", "decision": "DECISION", "red": "RED TEAM"}.get(code)
    return f'<div class="badge {code}">{label}</div>' if label else ""


# ------------------------------------------------------------------ screens
def big(text, lines=(), code=None, sub=None, hold=0.7, music=None, sting=None):
    parts = [part(badge(code) if code else "", ())] if code else []
    parts.append(part(f'<div class="big-text">{text}</div>', lines, hold))
    if sub:
        parts.append(part(f'<div class="big-sub">{sub[0]}</div>', sub[1] if len(sub) > 1 else (), 0.6))
    return screen("big", parts, code, music or ("drone" if code == "red" else "bed"), sting)


def act(label, title, lines, chapter, music="bed"):
    return screen("act", [part(f'<div class="act-label">{esc(label)}</div>'),
                          part(f'<div class="act-title">{title}</div>', lines, 0.9)],
                  None, music, "act", chapter)


def stop(role, facts, question, options, silence=4, after=None):
    parts = [part('<div class="stop-sign">STOP</div>', [(N, "Stop.")], 0.2),
             part(f'<div class="stop-role">{esc(role[0])}</div>', [(N, role[1])], 0.2)]
    for txt, spoken in facts:
        parts.append(part(f'<div class="stop-fact">{esc(txt)}</div>', [(N, spoken)], 0.1))
    parts.append(part(f'<div class="stop-q">{esc(question)}</div>', [(N, question)], 0.3))
    opts = "".join(f'<div class="opt"><b>{k}</b>{esc(v)}</div>' for k, v in options)
    parts.append(part(f'<div class="stop-opts">{opts}</div>', [], 0.3))
    parts.append(part('<div class="stop-pause">Pause the video and answer before continuing.</div>',
                      [], silence, countdown=silence))
    if after:
        parts.append(part(f'<div class="stop-after">{esc(after[0])}</div>', [(N, after[1])], 0.4))
    s = screen("stop", parts, "decision", "silence")
    s["cues"] = [("drone", 0), ("silence", len(parts) - (2 if after else 1))]  # silence from options on
    return s


def decision(question, evidence, verdict, lines_q, lines_e, lines_d, extra=None):
    parts = [part(badge("decision")),
             part(f'<div class="dn-h">THE QUESTION</div><div class="dn-q">{esc(question)}</div>', lines_q, 0.3),
             part('<div class="dn-h">THE EVIDENCE</div>', [], 0)]
    for i, ev in enumerate(evidence):
        parts.append(part(f'<div class="dn-ev">{esc(ev)}</div>', lines_e[i] if i < len(lines_e) else [], 0.15))
    parts.append(part(f'<div class="dn-h">THE DECISION</div><div class="dn-d">{esc(verdict)}</div>', lines_d, 0.9))
    if extra:
        parts.append(part(f'<div class="dn-x">{esc(extra[0])}</div>', extra[1], 0.8))
    return screen("decision", parts, "decision", "bed")


def redteam(question, answers, closing):
    parts = [part(badge("red")),
             part(f'<div class="rt-q">{esc(question[0])}</div>', question[1], 0.5)]
    for i, (txt, spoken) in enumerate(answers, 1):
        parts.append(part(f'<div class="rt-a"><b>{i}</b>{esc(txt)}</div>', spoken, 0.25))
    parts.append(part(f'<div class="rt-c">{closing[0]}</div>', closing[1], 1.2))
    return screen("redteam", parts, "red", "drone", "risk")


def ladder(steps, neq, final):
    parts = []
    for i, (word, desc, spoken, ok) in enumerate(steps):
        mark = "&#10003;" if ok else "?"
        parts.append(part(f'<div class="step {"ok" if ok else "q"}"><span class="n">{i + 1}</span>'
                          f'<b>{esc(word)}</b><i>{esc(desc)}</i><span class="m">{mark}</span></div>', spoken, 0.3))
    parts.append(part(f'<div class="neq">{neq[0]}</div>', neq[1], 0.9))
    parts.append(part(f'<div class="ladder-final">{final[0]}</div>', final[1], 1.4))
    return screen("ladder", parts, None, "theme")


def checklist(title, qs, closing):
    parts = [part(f'<div class="ck-title">{esc(title[0])}</div>', title[1], 0.3)]
    for i, (txt, spoken) in enumerate(qs, 1):
        parts.append(part(f'<div class="ck-q"><b>{i:02d}</b>{esc(txt)}</div>', spoken, 0.5))
    parts.append(part(f'<div class="ck-c">{esc(closing[0])}</div>', closing[1], 1.5))
    return screen("checklist", parts, "decision", "bed")


def flow(steps, lines_each, code="fact"):
    parts = [part(badge(code))]
    for i, s in enumerate(steps):
        arrow = '<div class="arrow">&#8595;</div>' if i else ""
        parts.append(part(f'{arrow}<div class="flow-box">{esc(s)}</div>', lines_each[i], 0.35))
    return screen("flow", parts, code, "tension")


def roles(intro, items, table=None):
    """items: [(WHO, spoken)] -> puppet lineup, each labelled with its role."""
    table = table or ROLES
    parts = [part(f'<div class="roles-title">{esc(intro[0])}</div>', intro[1], 0.3)]
    for who, spoken in items:
        name, role = table[who]
        parts.append(part(f'<div class="role" data-who="{who}"><div class="pup" data-who="{who}"></div>'
                          f'<b>{esc(name)}</b><i>{esc(role)}</i></div>', spoken, 0.15, cls="role-part"))
    return screen("roles", parts, None, "bed")


def legend(lines_intro, rows):
    parts = [part('<div class="lg-title">THREE SIGNALS</div>', lines_intro, 0.2)]
    for code, desc, spoken in rows:
        parts.append(part(f'<div class="lg-row">{badge(code)}<span>{esc(desc)}</span></div>', spoken, 0.3))
    return screen("legend", parts, None, "bed")


def title_card(lines, sub="EPISODE 1: THE SIGNING"):
    return screen("title", [part('<div class="kicker">A CAPACITY BUILDING SERIES ON AFRICA\'S POWER DEALS</div>'),
                            part('<div class="t1">BANKABLE</div><div class="t2">IS NOT ENOUGH</div>', lines, 0.4),
                            part(f'<div class="ep">{esc(sub)}</div><div class="lineup"></div>'
                                 '<div class="author">EMMANUEL BOUJIEKA KAMGA</div>', [], 1.2)],
                  None, "theme", "act")


def lesson(lines1, lines2, lines3):
    return screen("lesson", [part('<div class="ls1">BANKABLE IS NOT ENOUGH.</div>', lines1, 0.6),
                             part('<div class="ls2">Before you sign, test the deal.</div>', lines2, 0.8),
                             part('<div class="ls3">Bankability is the beginning. Not the end.</div>', lines3, 2.0)],
                  None, "theme", "act")


def credits(extra=""):
    return screen("credits", [part('<div class="cr-t">BANKABLE IS NOT ENOUGH</div><div class="cr-s">EPISODE 1: THE SIGNING</div>'),
                              part('<p>Story, text and illustrations &copy; 2026 Emmanuel Boujieka Kamga. All rights reserved.</p>'
                                   '<p>Kivona, KivoElec, SunRiver Power and all characters are invented. All figures are illustrative.</p>'
                                   '<p>For education and capacity building. Not legal, financial or investment advice.</p>'
                                   f'{extra}<p class="dim">Voices are synthetic (Kokoro-82M). Music is procedurally generated.</p>', [], 5.5)],
                  None, "theme")


def actor(who, x, y, size=110, look=0, mood="neutral", arm=False):
    """A puppet on a cartoon stage: face centre (x, y) in stage px, head radius `size` px."""
    return {"who": who, "x": x, "y": y, "size": size, "look": look, "mood": mood, "arm": arm}


def scene(bg, cast, lines, props=(), cut=False, music="bed", chapter=None):
    """A cartoon scene: drawn background, puppets that talk (speech bubbles, lip-sync),
    narration boxes for the narrator's lines."""
    return {"kind": "scene", "bg": bg, "cast": list(cast), "lines": lines, "props": list(props),
            "cut": cut, "music": music, "chapter": chapter}
