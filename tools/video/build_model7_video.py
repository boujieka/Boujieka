"""Video guide to MODEL 7: "How to use MODEL 7, step by step" (1920 x 1080, narrated).

Run: python3 tools/video/build_model7_video.py
Needs: Kokoro-82M (pip install kokoro; voices af_heart in English, ff_siwis in French) or piper-tts (TTS_ENGINE=piper), ffmpeg, playwright with Chromium, and the scenario copies
(drought, offtaker, offtaker without backstop) recalculated from the master workbook (built automatically).

Every image is a render of the workbook itself: cell values, number formats, fonts and fills come from the calculated
file, so the numbers on screen are the model's numbers. Stress scenes show copies recalculated with the stress on.
Output: course/video/MODEL7_Video_Guide.mp4 (H.264 + AAC, chapters, soft English subtitles) and .srt.
VIDEO_LANG=fr builds the French version (MODEL7_Video_Guide_FR.mp4, .fr.srt) from course/video/script_fr.md with the
fr_FR-siwis-medium voice: narration, title cards, headers and captions in French; the workbook itself stays in English.
"""
import base64
import html
import json
import os
import re
import shutil
import subprocess
import sys

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter as L
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
WORK = os.environ.get("VIDEO_WORK", "/tmp/model7_video")
LANG = os.environ.get("VIDEO_LANG", "en")  # "en" or "fr"
ENGINE = os.environ.get("TTS_ENGINE", "kokoro")  # "kokoro" (default, more natural) or "piper"
KOKORO_VOICE = os.environ.get("KOKORO_VOICE", "ff_siwis" if LANG == "fr" else "af_heart")
KOKORO_SPEED = float(os.environ.get("KOKORO_SPEED", "0.94"))
VOICE_DIR = "/tmp/claude-0/-home-user-Boujieka/92f87389-f945-55f4-b28c-902b8d98c6ca/scratchpad/voice"
VOICE = os.environ.get("PIPER_VOICE", f"{VOICE_DIR}/" + ("fr_FR-siwis-medium.onnx" if LANG == "fr" else "en_GB-cori-high.onnx"))
RECALC = os.environ.get("RECALC", "/root/.claude/skills/synced/595554f7-3334-4cb8-90b6-40da4dcb6b84_e238fe12-8a4b-4490-8c46-5bf1323948af/xlsx/scripts/recalc.py")
MODEL = "model/Bankable_Hydro_Model_FR.xlsx" if LANG == "fr" else "model/Bankable_Hydro_Model.xlsx"  # the French video shows the French workbook
OUT_DIR = "course/video"
GREEN, GOLD, GOLDL, CREAM = "#0B3020", "#B07C0F", "#E0B44A", "#F7F3E8"
os.makedirs(WORK, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- scenario copies
SCEN = {"base": {}, "drought": {"C15": 1}, "offtaker": {"C19": 1}, "offtaker_nobs": {"C19": 1, "C12": 0}}
BOOKS = {}
for name, sets in SCEN.items():
    f = os.path.join(WORK, f"{name}.xlsx")
    if not os.path.exists(f):
        wb = load_workbook(MODEL)
        for c, v in sets.items():
            wb["01_CONTROL_PANEL"][c].value = v
        wb.save(f)
        res = json.loads(subprocess.run([sys.executable, RECALC, f, "300"], capture_output=True, text=True).stdout)
        assert res["status"] == "success", (name, res)
    BOOKS[name] = load_workbook(f, data_only=True)


# ---------------------------------------------------------------- cell rendering
def fmt(v, nf):
    if v is None:
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int, float)):
        nf = nf or "General"
        dec = 0
        m = re.search(r"0\.(0+)", nf)
        if m:
            dec = len(m.group(1))
        if "%" in nf:
            return f"{v * 100:,.{dec}f}%".replace("-", "−")
        if '"x"' in nf or nf.endswith("x"):
            return f"{v:,.{dec or 2}f}x".replace("-", "−")
        if nf == "General":
            if isinstance(v, int) or float(v).is_integer():
                return f"{int(v)}"
            return f"{v:,.2f}".replace("-", "−")
        if "#,##0" in nf or "0" in nf:
            s = f"{v:,.{dec}f}" if "," in nf else f"{v:.{dec}f}"
            return s.replace("-", "−")
        return str(v)
    return str(v)


def colour(c, default=None):
    try:
        rgb = c.rgb if c is not None else None
        if isinstance(rgb, str) and len(rgb) >= 6 and rgb not in ("00000000",):
            return "#" + rgb[-6:]
    except Exception:
        pass
    return default


def table_html(book, sheet, r1, r2, c1, c2, hl=(), overrides=None, wrap_cols=(), maxw=None, setw=None):
    """HTML table of a sheet range; hl = list of (r1, c1, r2, c2) cell blocks to highlight; others dimmed."""
    ws = BOOKS[book][sheet]
    overrides = overrides or {}
    widths = []
    for c in range(c1, c2 + 1):
        w = ws.column_dimensions[L(c)].width or 9
        w = min(w, maxw.get(c, 999)) if maxw else w
        w = setw.get(c, w) if setw else w
        widths.append(int(w * 7.4 + 8))
    def inhl(r, c):
        return any(a <= r <= b and x <= c <= y for a, x, b, y in hl)
    rows = []
    for r in range(r1, r2 + 1):
        tds, skip = [f'<td class="rn">{r}</td>'], set()
        for c in range(c1, c2 + 1):
            cell = ws.cell(r, c)
            v = overrides.get(f"{L(c)}{r}", cell.value)
            txt = html.escape(fmt(v, cell.number_format))
            st = []
            fill = cell.fill
            if fill is not None and fill.fill_type == "solid":
                bg = colour(fill.fgColor)
                if bg:
                    st.append(f"background:{bg}")
            fnt = cell.font
            if fnt is not None:
                fc = colour(fnt.color)
                if fc:
                    st.append(f"color:{fc}")
                if fnt.b:
                    st.append("font-weight:700")
                if fnt.i:
                    st.append("font-style:italic")
                if fnt.sz and fnt.sz >= 13:
                    st.append(f"font-size:{min(fnt.sz, 22) * 1.15:.0f}px")
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                st.append("text-align:right")
            cls = []
            if hl:
                cls.append("hl" if inhl(r, c) else "dim")
            if f"{L(c)}{r}" in overrides:
                cls.append("ovr")
            if c in wrap_cols:
                cls.append("wrap")
            if c in skip:
                continue
            span = ""
            if isinstance(v, str) and c < c2 and txt:
                # Excel lets text run on over empty neighbours: span the free cells, so no grid line crosses the text
                k = c + 1
                while k <= c2 and ws.cell(r, k).value in (None, "") and f"{L(k)}{r}" not in overrides:
                    skip.add(k)
                    k += 1
                if k > c + 1:
                    span = f' colspan="{k - c}"'
            tds.append(f'<td{span} class="{" ".join(cls)}" style="{";".join(st)}">{txt}</td>')
        rows.append("<tr>" + "".join(tds) + "</tr>")
    head = '<tr><th class="rn"></th>' + "".join(f"<th>{L(c)}</th>" for c in range(c1, c2 + 1)) + "</tr>"
    cols = '<col style="width:34px">' + "".join(f'<col style="width:{w}px">' for w in widths)
    tw = 34 + sum(widths)  # fixed layout needs an explicit width, or long texts would widen the columns
    return f'<div class="sheet" style="width:{tw}px"><div class="tab">{html.escape(sheet)}</div><table style="width:{tw}px"><colgroup>{cols}</colgroup>{head}{"".join(rows)}</table></div>'


CSS = f"""
body {{ margin:0; width:1920px; height:1080px; background:{CREAM}; font-family:'Liberation Sans', Arial, sans-serif; overflow:hidden; }}
.top {{ height:86px; background:{GREEN}; color:white; display:flex; align-items:center; justify-content:space-between; padding:0 48px; border-bottom:5px solid {GOLD}; }}
.top .brand {{ font-size:22px; font-weight:700; letter-spacing:1px; color:{GOLDL}; }}
.top .brand span {{ color:white; font-weight:400; letter-spacing:0; margin-left:14px; }}
.top .chap {{ font-size:26px; font-weight:700; }}
.stage {{ position:absolute; top:91px; left:0; right:0; bottom:52px; display:flex; align-items:center; justify-content:center; gap:36px; padding:24px 40px; box-sizing:border-box; }}
.fit {{ transform-origin:center center; display:flex; gap:36px; align-items:flex-start; }}
.sheet {{ background:white; box-shadow:0 6px 24px rgba(0,0,0,.18); border:1px solid #c9c4b6; }}
.tab {{ background:#E9E4D6; color:{GREEN}; font-weight:700; font-size:15px; padding:6px 12px; border-bottom:2px solid {GOLD}; }}
table {{ border-collapse:collapse; table-layout:fixed; font-size:14px; }}
th {{ background:#F0F0F0; color:#555; font-weight:400; font-size:12px; border:1px solid #d8d8d8; height:20px; }}
td {{ border:1px solid #e3e3e3; padding:2px 6px; height:22px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:#111; }}
td.wrap {{ white-space:normal; height:auto; }}
td.rn {{ background:#F0F0F0; color:#777; font-size:11px; text-align:center; padding:0; }}
td.dim {{ opacity:.38; }}
td.hl {{ box-shadow: inset 0 0 0 9999px rgba(224,180,74,.18); outline:2px solid {GOLD}; outline-offset:-2px; }}
td.ovr {{ box-shadow: inset 0 0 0 9999px rgba(224,180,74,.55) !important; font-weight:700; outline:3px solid #A8432A; outline-offset:-3px; }}
.foot {{ position:absolute; left:0; right:0; bottom:0; height:52px; background:{GREEN}; color:#d9d9d9; display:flex; align-items:center; justify-content:space-between; padding:0 48px; font-size:16px; }}
.foot b {{ color:{GOLDL}; }}
.card {{ position:absolute; top:91px; left:0; right:0; bottom:52px; background:{GREEN}; color:white; padding:110px 140px; box-sizing:border-box; }}
.card .k {{ color:{GOLDL}; font-weight:700; font-size:26px; letter-spacing:2px; }}
.card h1 {{ font-size:72px; margin:26px 0 10px 0; line-height:1.08; }}
.card h1 em {{ color:{GOLDL}; font-style:normal; }}
.card h2 {{ font-size:34px; font-weight:400; margin:10px 0 34px 0; }}
.card p, .card li {{ font-size:30px; line-height:1.5; }}
.card ol {{ margin:10px 0 0 0; padding-left:40px; }}
.card .rule {{ width:220px; height:5px; background:{GOLD}; margin:24px 0; }}
.card .qr {{ position:absolute; right:140px; bottom:120px; background:white; padding:14px; text-align:center; color:{GREEN}; font-size:18px; }}
"""


def page(chap, inner, sheet_note=""):
    return (f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>"
            f"<div class='top'><div class='brand'>MODEL 7<span>{t_('Hydropower Development and Finance Model')}</span></div><div class='chap'>{html.escape(chap)}</div></div>"
            f"{inner}<div class='foot'><div>{t_('Africa Energy Finance  |  Book 7 companion  |  v1.0 RC1')}</div><div>{t_(sheet_note)}</div></div></body></html>")


def sheets_inner(panels):
    return f"<div class='stage'><div class='fit' id='fit'>{''.join(panels)}</div></div>"


def card(kicker, title, sub="", body="", qr=False):
    q = ""
    if qr:
        b64 = base64.b64encode(open("book7/src/figures/qr_companion.png", "rb").read()).decode()
        q = f"<div class='qr'><img src='data:image/png;base64,{b64}' width='230'><div>{t_('Companion materials')}</div></div>"
    if LANG == "fr":
        kicker, title, sub = t_(kicker), t_(title), t_(sub)
        body = OWN_PROJECT_FR if body.startswith("<ol><li>02 ") else "".join(t_(x) for x in re.split(r"(?<=</li>)(?=<li>Record)", body))
    return f"<div class='card'><div class='k'>{kicker}</div><h1>{title}</h1><div class='rule'></div><h2>{sub}</h2>{body}{q}</div>"


# ---------------------------------------------------------------- French on-screen text
FR = {
    "Hydropower Development and Finance Model": "Modèle de développement et de financement hydroélectrique",
    "Africa Energy Finance  |  Book 7 companion  |  v1.0 RC1": "Africa Energy Finance  |  Compagnon du Livre 7  |  v1.0 RC1",
    "Companion materials": "Ressources du livre",
    "VIDEO GUIDE": "GUIDE VIDÉO", "How to use <em>MODEL 7</em>,<br>step by step": "Utiliser <em>MODEL 7</em>,<br>pas à pas",
    "Hydropower Development and Finance Model  |  Companion to Book 7": "Modèle de développement et de financement hydroélectrique  |  Compagnon du Livre 7",
    "THE ROUTE": "LE PARCOURS", "From the cover<br>to your own project": "De la feuille de garde<br>à votre propre projet",
    "Kasiri River Hydro: 60 MW run-of-river, fictional Republic of Navaria": "Kasiri River Hydro : 60 MW au fil de l'eau, République fictive de Navaria",
    "<ol><li>Cover and checks</li><li>Dashboard and the close decision</li><li>Developer view and stresses</li><li>Your own project</li></ol>":
        "<ol><li>Feuille de garde et contrôles</li><li>Tableau de bord et décision de bouclage</li><li>Point de vue du développeur et stress</li><li>Votre propre projet</li></ol>",
    "BEFORE YOU START": "AVANT DE COMMENCER", "Open the workbook": "Ouvrez le classeur",
    "<p>Keep it open next to the video. Pause whenever you want to try a step.</p>": "<p>Gardez-le ouvert à côté de la vidéo. Mettez en pause pour essayer chaque étape.</p>",
    "Sheet: COVER": "Feuille : COVER", "Sheet: COVER, live status": "Feuille : COVER, live status", "Sheet: COVER, start here": "Feuille : COVER, start here",
    "Sheet: 00_README": "Feuille : 00_README", "Sheet: 00_README, colour code": "Feuille : 00_README, code couleur",
    "Sheet: 00_README, units and timeline": "Feuille : 00_README, unités et chronologie", "Sheet: 00_README, two levels of gates": "Feuille : 00_README, deux niveaux de portes",
    "Sheet: 01_CONTROL_PANEL": "Feuille : 01_CONTROL_PANEL", "Section A: case and generation": "Section A : cas et production",
    "Section B: transaction structure": "Section B : structure de la transaction", "Sections C and D: stresses and flexes": "Sections C et D : stress et sensibilités",
    "Section E: active scenario read-out": "Section E : résultats du scénario actif", "Sheet: 33_CHECKS": "Feuille : 33_CHECKS", "Sheet: 35_BOOK_CHECK": "Feuille : 35_BOOK_CHECK",
    "Rule: ALL OK before reading any result": "Règle : ALL OK avant de lire un résultat", "Sheet: 32_DASHBOARD": "Feuille : 32_DASHBOARD",
    "Project block": "Bloc projet", "Financial block": "Bloc financier", "Developer block": "Bloc développeur",
    "Utility and public finance blocks": "Blocs compagnie d'électricité et finances publiques", "Sheet: 30A_CLOSE_READINESS": "Feuille : 30A_CLOSE_READINESS",
    "The decision ladder": "L'échelle de décision", "The seven critical gates not met": "Les sept portes critiques non franchies",
    "Framework summary and 34_FRAMEWORK_MAP": "Synthèse du cadre et 34_FRAMEWORK_MAP", "Sheet: 01A_DEVELOPMENT, stages": "Feuille : 01A_DEVELOPMENT, étapes",
    "Returns and value of the position by stage": "Rendements et valeur de la position par étape", "Try a change: stage probabilities": "Essayez : probabilités des étapes",
    "Drought on: minimum DSCR": "Sécheresse activée : DSCR minimum", "Drought (left) against the base case (right)": "Sécheresse (à gauche) contre cas de base (à droite)",
    "Offtaker stress with the budget backstop": "Stress acheteur avec garantie budgétaire", "Offtaker stress, no backstop": "Stress acheteur, sans garantie budgétaire",
    "Sheet: 17A_STRUCTURES, full-engine runs": "Feuille : 17A_STRUCTURES, calculs complets", "Sheet: 05A_CONTRACTING": "Feuille : 05A_CONTRACTING",
    "YOUR OWN PROJECT": "VOTRE PROPRE PROJET", "Replace the blue inputs,<br>in this order": "Remplacez les données bleues,<br>dans cet ordre",
    "AFTER EVERY CHANGE": "APRÈS CHAQUE MODIFICATION", "Check, then read": "Vérifier, puis lire",
    "<ol><li>33_CHECKS must read ALL OK</li><li>35_BOOK_CHECK will show CHECK lines: expected</li>": "<ol><li>33_CHECKS doit indiquer ALL OK</li><li>35_BOOK_CHECK affichera des lignes CHECK : c'est normal</li>",
    "<li>Record each assumption and its source</li></ol>": "<li>Notez chaque hypothèse et sa source</li></ol>",
    "THE WHOLE ROUTE": "TOUT LE PARCOURS", "Cover, checks, dashboard,<br>close decision, stresses": "Garde, contrôles, tableau de bord,<br>décision, stress",
    "MANUAL 7 gives every formula; Book 7 explains the reasoning": "MANUAL 7 détaille chaque formule ; le Livre 7 explique le raisonnement",
    "Decision support,<br>not investment advice": "Aide à la décision,<br>pas un conseil en investissement",
    "All default inputs are illustrative  |  Emmanuel Boujieka Kamga  |  Africa Energy Finance": "Toutes les valeurs par défaut sont illustratives  |  Emmanuel Boujieka Kamga  |  Africa Energy Finance",
}
OWN_PROJECT_FR = ("<ol><li>02 Données du projet et 03 Hydrologie</li><li>05 Coût d'investissement de la centrale</li><li>01A Étapes, budgets et probabilités</li>"
                  "<li>14 Contrat d'achat ; 11 et 12 l'acheteur</li><li>Conditions de financement : 17A et 18</li><li>Statuts de preuve des 23 portes : 30A</li></ol>")


def t_(x):
    return FR.get(x, x) if LANG == "fr" else x


# ---------------------------------------------------------------- narration
script = open("course/video/script_fr.md" if LANG == "fr" else "course/audio/model7_walkthrough/script.md", encoding="utf8").read()
CH = {}
for num, title, body in re.findall(r"^## (\d+)\. (.+?)\n(.*?)(?=^## |\Z)", script, re.S | re.M):
    paras = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
    CH[int(num)] = (title, paras)
VIDEO_EDITS = [("Welcome to the audio guide to MODEL 7", "Welcome to the video guide to MODEL 7"),
               ("keep it next to you as you listen", "keep it next to you as you watch"),
               ("Pause the recording", "Pause the video")] if LANG == "en" else []


def para(ch, i):
    t = CH[ch][1][i]
    for a, b in VIDEO_EDITS:
        t = t.replace(a, b)
    return t


def chap_label(ch):
    return f"{'Partie' if LANG == 'fr' else 'Part'} {ch}. {CH[ch][0]}"


W = {}  # width caps for long text columns
CP = ("base", "01_CONTROL_PANEL", 1, 41, 1, 3)
DASH = ("base", "32_DASHBOARD", 3, 34, 1, 8)
G30A = ("base", "30A_CLOSE_READINESS", 4, 27, 1, 9)


def T(spec, hl=(), overrides=None, wrap=(), maxw=None, book=None, setw=None):
    b, s, r1, r2, c1, c2 = spec
    return table_html(book or b, s, r1, r2, c1, c2, hl=hl, overrides=overrides, wrap_cols=wrap, maxw=maxw, setw=setw)


cover_rows = ("base", "COVER", 8, 44, 2, 6)
readme = ("base", "00_README", 1, 21, 1, 2)
logo = base64.b64encode(open("brand/aef_logo_cover.png", "rb").read()).decode()
LOGO = f"<img src='data:image/png;base64,{logo}' style='width:300px;display:block;margin:0 0 14px 0'>"
w30a = {2: 46, 7: 30, 8: 26, 9: 20}

SCENES = [
    # (chapter, paragraph index, html-inner, footer note)
    (1, 0, card("VIDEO GUIDE", "How to use <em>MODEL 7</em>,<br>step by step", "Hydropower Development and Finance Model  |  Companion to Book 7"), ""),
    (1, 1, card("THE ROUTE", "From the cover<br>to your own project", "Kasiri River Hydro: 60 MW run-of-river, fictional Republic of Navaria",
                "<ol><li>Cover and checks</li><li>Dashboard and the close decision</li><li>Developer view and stresses</li><li>Your own project</li></ol>"), ""),
    (1, 2, card("BEFORE YOU START", "Open the workbook", "MODEL7_Modele_financier_hydro_v1.0RC1_FR.xlsx" if LANG == "fr" else "MODEL7_Bankable_Hydro_Model_v1.0RC1.xlsx",
                "<p>Keep it open next to the video. Pause whenever you want to try a step.</p>"), ""),
    (2, 0, sheets_inner([LOGO + T(("base", "COVER", 8, 22, 2, 6), hl=[(10, 2, 19, 6)], maxw={2: 64})]), "Sheet: COVER"),
    (2, 1, sheets_inner([T(("base", "COVER", 23, 31, 2, 6), hl=[(24, 2, 30, 6)], maxw={2: 64, 4: 40})]), "Sheet: COVER, live status"),
    (2, 2, sheets_inner([T(("base", "COVER", 32, 40, 2, 6), hl=[(32, 2, 38, 6)], maxw={2: 40, 3: 60})]), "Sheet: COVER, start here"),
    (3, 0, sheets_inner([T(readme, hl=[(4, 1, 8, 2)], maxw={2: 150})]), "Sheet: 00_README"),
    (3, 1, sheets_inner([T(readme, hl=[(9, 1, 9, 2)], maxw={2: 150})]), "Sheet: 00_README, colour code"),
    (3, 2, sheets_inner([T(readme, hl=[(10, 1, 11, 2)], maxw={2: 150})]), "Sheet: 00_README, units and timeline"),
    (3, 3, sheets_inner([T(readme, hl=[(15, 1, 15, 2)], maxw={2: 150})]), "Sheet: 00_README, two levels of gates"),
    (4, 0, sheets_inner([T(CP)]), "Sheet: 01_CONTROL_PANEL"),
    (4, 1, sheets_inner([T(("base", "01_CONTROL_PANEL", 1, 13, 1, 3), hl=[(4, 1, 7, 3)], maxw={1: 70})]), "Section A: case and generation"),
    (4, 2, sheets_inner([T(("base", "01_CONTROL_PANEL", 1, 13, 1, 3), hl=[(8, 1, 13, 3)], maxw={1: 70})]), "Section B: transaction structure"),
    (4, 3, sheets_inner([T(("base", "01_CONTROL_PANEL", 14, 29, 1, 3), hl=[(14, 1, 29, 3)], maxw={1: 70})]), "Sections C and D: stresses and flexes"),
    (4, 4, sheets_inner([T(("base", "01_CONTROL_PANEL", 30, 41, 1, 3), hl=[(30, 1, 41, 3)], maxw={1: 70})]), "Section E: active scenario read-out"),
    (5, 0, sheets_inner([T(("base", "33_CHECKS", 1, 19, 1, 3), hl=[(4, 1, 19, 3)])]), "Sheet: 33_CHECKS"),
    (5, 1, sheets_inner([T(("base", "35_BOOK_CHECK", 4, 33, 1, 6), hl=[(5, 5, 31, 5), (33, 1, 33, 5)])]), "Sheet: 35_BOOK_CHECK"),
    (5, 2, sheets_inner([T(("base", "33_CHECKS", 1, 19, 1, 3), hl=[(19, 1, 19, 3)])]), "Rule: ALL OK before reading any result"),
    (6, 0, sheets_inner([T(DASH, hl=[(3, 1, 4, 8)], maxw={1: 36, 4: 36, 7: 36})]), "Sheet: 32_DASHBOARD"),
    (6, 1, sheets_inner([T(("base", "32_DASHBOARD", 6, 15, 1, 2), hl=[(7, 1, 10, 2)], maxw={1: 40})]), "Project block"),
    (6, 2, sheets_inner([T(("base", "32_DASHBOARD", 6, 15, 4, 5), hl=[(8, 4, 8, 5), (10, 4, 10, 5), (14, 4, 15, 5)], maxw={4: 40})]), "Financial block"),
    (6, 3, sheets_inner([T(("base", "32_DASHBOARD", 6, 15, 7, 8), hl=[(7, 7, 11, 8)], maxw={7: 44})]), "Developer block"),
    (6, 4, sheets_inner([T(("base", "32_DASHBOARD", 17, 23, 4, 5), hl=[(21, 4, 21, 5)], maxw={4: 40}),
                         T(("base", "32_DASHBOARD", 25, 33, 1, 2), hl=[(30, 1, 30, 2)], maxw={1: 44})]), "Utility and public finance blocks"),
    (7, 0, sheets_inner([T(G30A, hl=[(5, 5, 27, 6)], maxw=w30a)]), "Sheet: 30A_CLOSE_READINESS"),
    (7, 1, sheets_inner([T(("base", "30A_CLOSE_READINESS", 28, 35, 1, 3), hl=[(29, 1, 34, 3)], setw={1: 46, 2: 6, 3: 34})]), "The decision ladder"),
    (7, 2, sheets_inner([T(G30A, hl=[(5, 1, 5, 9), (7, 1, 7, 9), (9, 1, 9, 9), (12, 1, 12, 9), (19, 1, 19, 9), (21, 1, 21, 9), (23, 1, 23, 9)], maxw=w30a)]), "The seven critical gates not met"),
    (7, 3, sheets_inner(["<div style='display:flex;flex-direction:column;gap:22px;align-items:flex-start'>"
                         + T(("base", "30A_CLOSE_READINESS", 39, 47, 2, 6), hl=[(40, 2, 47, 6)], maxw={2: 30})
                         + T(("base", "34_FRAMEWORK_MAP", 4, 12, 2, 6), maxw={2: 52, 3: 24, 4: 18, 6: 22}) + "</div>"]), "Framework summary and 34_FRAMEWORK_MAP"),
    (8, 0, sheets_inner([T(("base", "01A_DEVELOPMENT", 4, 15, 1, 5), hl=[(5, 1, 11, 5)], maxw={1: 44, 2: 30})]), "Sheet: 01A_DEVELOPMENT, stages"),
    (8, 1, sheets_inner([T(("base", "01A_DEVELOPMENT", 36, 56, 1, 5), hl=[(44, 1, 47, 3), (54, 1, 54, 5)], maxw={1: 52})]), "Returns and value of the position by stage"),
    (8, 2, sheets_inner([T(("base", "01A_DEVELOPMENT", 4, 15, 1, 5), hl=[(6, 5, 11, 5)], maxw={1: 44, 2: 30})]), "Try a change: stage probabilities"),
    (9, 0, sheets_inner([T(("drought", "01_CONTROL_PANEL", 14, 23, 1, 3), overrides={"C15": 1}),
                         T(("drought", "32_DASHBOARD", 6, 15, 4, 5), hl=[(10, 4, 10, 5)], maxw={4: 34})]), "Drought on: minimum DSCR"),
    (9, 1, sheets_inner([T(("drought", "32_DASHBOARD", 6, 15, 4, 5), hl=[(10, 4, 11, 5)], maxw={4: 34}),
                         T(("base", "32_DASHBOARD", 6, 15, 4, 5), maxw={4: 34})]), "Drought (left) against the base case (right)"),
    (10, 0, sheets_inner([T(("offtaker", "01_CONTROL_PANEL", 11, 23, 1, 3), overrides={"C19": 1}),
                          T(("offtaker", "32_DASHBOARD", 17, 33, 1, 5), hl=[(21, 4, 21, 5), (30, 1, 30, 2)], maxw={1: 34, 4: 34})]), "Offtaker stress with the budget backstop"),
    (10, 1, sheets_inner([T(("offtaker_nobs", "01_CONTROL_PANEL", 11, 23, 1, 3), overrides={"C12": 0, "C19": 1}),
                          T(("offtaker_nobs", "32_DASHBOARD", 6, 23, 4, 5), hl=[(10, 4, 10, 5), (23, 4, 23, 5)], maxw={4: 34})]), "Offtaker stress, no backstop"),
    (11, 0, sheets_inner([T(("base", "17A_STRUCTURES", 53, 59, 1, 8), hl=[(55, 1, 59, 3)], maxw={1: 20}),
                          ]), "Sheet: 17A_STRUCTURES, full-engine runs"),
    (11, 1, sheets_inner([T(("base", "05A_CONTRACTING", 4, 10, 1, 7), hl=[(6, 5, 10, 7)], maxw={1: 50})]), "Sheet: 05A_CONTRACTING"),
    (12, 0, card("YOUR OWN PROJECT", "Replace the blue inputs,<br>in this order", "",
                 "<ol><li>02 Project inputs and 03 Hydrology</li><li>05 Plant capital cost</li><li>01A Development stages, budgets, odds</li>"
                 "<li>14 PPA, 11 and 12 the buyer</li><li>Financing terms: 17A and 18</li><li>Evidence statuses of the 23 gates: 30A</li></ol>"), ""),
    (12, 1, card("AFTER EVERY CHANGE", "Check, then read", "", "<ol><li>33_CHECKS must read ALL OK</li><li>35_BOOK_CHECK will show CHECK lines: expected</li>"
                 "<li>Record each assumption and its source</li></ol>"), ""),
    (13, 0, card("THE WHOLE ROUTE", "Cover, checks, dashboard,<br>close decision, stresses", "MANUAL 7 gives every formula; Book 7 explains the reasoning", qr=True), ""),
    (13, 1, card("MODEL 7", "Decision support,<br>not investment advice", "All default inputs are illustrative  |  Emmanuel Boujieka Kamga  |  Africa Energy Finance", qr=True), ""),
]


# ---------------------------------------------------------------- build
def render_images():
    with sync_playwright() as p:
        exe = (sorted(__import__("glob").glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")) or [None])[0]
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        for k, (ch, pi, inner, note) in enumerate(SCENES):
            pg.set_content(page(chap_label(ch), inner, note), wait_until="load")
            pg.evaluate("""() => { const f = document.getElementById('fit'); if (!f) return;
                const st = f.parentElement; const sw = st.clientWidth - 80, sh = st.clientHeight - 48;
                const s = Math.min(sw / f.scrollWidth, sh / f.scrollHeight, 2.1); f.style.transform = `scale(${s})`; }""")
            pg.screenshot(path=f"{WORK}/scene_{k:02d}.png")
        b.close()


# How the French voice should say English names (respellings checked by transcribing the synthesised audio)
SAY_FR = [("Hydropower Development and Finance, From River to Financial Close",
           "Haïdropaweur Dévelopmeunt ènde Faïnance, Frome Riveur tou Faïnancheul Clôze"),
          ("Hydro Readiness Framework", "Haïdro Rédinesse Framework"), ("Kasiri River Hydro", "Kasiri Riveur Haïdro"),
          ("Read me", "Rîd mî"), ("Start here", "Start hir"), ("Close readiness", "Clôze rédinesse"),
          ("Development", "Dévelopmeunt"), ("Contracting", "Contractinng"), ("Book check", "Bouk tchèk"),
          ("lignes check", "lignes tchèk"), ("MODEL 7", "Modèle 7"), ("MANUAL 7", "Manuel 7")]


def tts():
    for k, (ch, pi, _, _) in enumerate(SCENES):
        out = f"{WORK}/scene_{k:02d}.wav"
        if os.environ.get("REUSE_TTS") and os.path.exists(out):  # regenerate only the scenes whose wav was deleted
            continue
        text = (f"{chap_label(ch)}.\n\n" if pi == 0 and ch > 1 else "") + para(ch, pi)
        for x, y in (SAY_FR if LANG == "fr" else [("Read me", "Read-me")]):
            text = text.replace(x, y)
        if ENGINE == "piper":
            subprocess.run([sys.executable, "-m", "piper", "-m", VOICE, "-f", out, "--length-scale", "1.06", "--sentence-silence", "0.45"],
                           input=text.encode(), check=True, capture_output=True)
        else:
            kokoro_say(text, out)


_KP = {}


def kokoro_say(text, out):
    """Kokoro-82M (Apache-2.0): one pass per sentence, joined with short pauses, so the pacing stays calm and even."""
    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline
    lang = "f" if LANG == "fr" else "a"
    if lang not in _KP:
        _KP[lang] = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
    sr, parts = 24000, []
    blocks = [x for x in text.split("\n\n") if x.strip()]
    for bi, block in enumerate(blocks):
        for sent in re.split(r"(?<=[.!?;:])\s+", block.strip()):
            audio = [a.numpy() if hasattr(a, "numpy") else a for _, _, a in _KP[lang](sent, voice=KOKORO_VOICE, speed=KOKORO_SPEED)]
            if audio:
                parts += [np.concatenate(audio), np.zeros(int(sr * (0.32 if sent[-1] in ".!?" else 0.18)))]
        if bi + 1 < len(blocks):
            parts.append(np.zeros(int(sr * 0.45)))  # after the "Part N" announcement
    sf.write(out, np.concatenate(parts), sr)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


def srt_time(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    s = t - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def assemble():
    clips, t, subs, chapters = [], 0.0, [], []
    for k, (ch, pi, _, _) in enumerate(SCENES):
        wav = f"{WORK}/scene_{k:02d}.wav"
        lead, tail = 0.4, (1.1 if k + 1 == len(SCENES) or SCENES[k + 1][0] != ch else 0.5)
        d = lead + dur(wav) + tail
        clip = f"{WORK}/clip_{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "30", "-i", f"{WORK}/scene_{k:02d}.png",
                        "-i", wav, "-filter_complex",
                        f"[0:v]fade=t=in:st=0:d=0.35,fade=t=out:st={d - 0.35:.3f}:d=0.35,format=yuv420p[v];"
                        f"[1:a]adelay={int(lead * 1000)},apad,aformat=sample_rates=48000:channel_layouts=mono[a]",
                        "-map", "[v]", "-map", "[a]", "-t", f"{d:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "16",
                        "-tune", "stillimage", "-r", "30", "-c:a", "pcm_s16le", clip.replace(".mp4", ".mkv")], check=True)
        clips.append(clip.replace(".mp4", ".mkv"))
        if pi == 0:
            chapters.append((t, f"{ch}. {CH[ch][0]}"))
        text = para(ch, pi)
        sents = re.split(r"(?<=[.!?])\s+", text)
        speak = dur(wav)
        total = sum(len(s) for s in sents) or 1
        st = t + lead
        for s_ in sents:
            dt = speak * len(s_) / total
            subs.append((st, st + dt, s_))
            st += dt
        t += d
    with open(f"{WORK}/list.txt", "w") as fh:
        for c in clips:
            fh.write(f"file '{c}'\n")
    meta = [";FFMETADATA1", "title=" + ("Utiliser MODEL 7, pas à pas" if LANG == "fr" else "How to use MODEL 7, step by step"), "artist=Emmanuel Boujieka Kamga",
            "album=Africa Energy Finance: Book 7 companion", "comment=Video guide to MODEL 7 v1.0 RC1. Narration: synthetic voice."]
    for i, (st, name) in enumerate(chapters):
        end = chapters[i + 1][0] if i + 1 < len(chapters) else t
        meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(st * 1000)}", f"END={int(end * 1000)}", f"title={name}"]
    open(f"{WORK}/chapters.txt", "w").write("\n".join(meta) + "\n")
    srt = f"{OUT_DIR}/MODEL7_Video_Guide" + ("_FR.fr.srt" if LANG == "fr" else ".en.srt")
    with open(srt, "w", encoding="utf8") as fh:
        for i, (a, b, s_) in enumerate(subs, 1):
            fh.write(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{s_}\n\n")
    joined = f"{WORK}/joined.mkv"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/list.txt", "-c", "copy", joined], check=True)
    out = f"{OUT_DIR}/MODEL7_Video_Guide" + ("_FR.mp4" if LANG == "fr" else ".mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", joined, "-i", srt, "-i", f"{WORK}/chapters.txt",
                    "-map", "0:v", "-map", "0:a", "-map", "1:s", "-map_metadata", "2", "-map_chapters", "2",
                    "-c:v", "copy", "-af", "highpass=f=60,loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-c:s", "mov_text", "-metadata:s:s:0", "language=" + ("fre" if LANG == "fr" else "eng"), "-movflags", "+faststart", out], check=True)
    print(out, f"{t / 60:.1f} min, {len(SCENES)} scenes, {len(chapters)} chapters")


if __name__ == "__main__":
    render_images()
    tts()
    assemble()
