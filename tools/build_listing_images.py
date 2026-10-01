"""Build Etsy/Gumroad listing images from real renders of the workbooks.

Usage: python tools/build_listing_images.py [--lang en|fr|all] [--product p1|p2|p3|all] [--gumroad-only]

Steps per product and language:
1. rebuild the workbook into a temp folder with print areas set (tools/print_areas.py), one page per sheet;
2. recalculate with LibreOffice, export to PDF, rasterise the pages of interest and crop the margins;
3. compose 2400 x 1800 px (4:3) listing images: headline band, screenshot card, honesty footer.
Screens are never edited: every number shown is the workbook's own output.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
TMP = Path(os.environ.get("SHOT_TMP", "/tmp/claude-0/shots"))
OUT = ROOT / "marketing" / "images"
RECALC = os.environ.get("RECALC", "/root/.claude/skills/synced/595554f7-3334-4cb8-90b6-40da4dcb6b84_e238fe12-8a4b-4490-8c46-5bf1323948af/xlsx/scripts/recalc.py")
LO_PROFILE = "file:///tmp/claude-0/lo_profile"
W, H = 2400, 1800
NAVY, TEAL, BG = (31, 58, 95), (27, 127, 121), (244, 247, 250)
F_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

sys.path.insert(0, str(ROOT / "tools"))
import i18n_fr  # noqa: E402

PRODUCTS = {
    "p1": {"builder": "build_entry_calculator.py", "sheets": ["Start Here", "Inputs", "Dashboard", "Cash Flow", "Checks"]},
    "p2": {"builder": "build_developer_edition.py",
           "sheets": ["Start Here", "Inputs", "Load Profile", "Productive Use", "Dashboard", "Funding Gap & RBF", "Sensitivity",
                      "Impact & MRV", "Financing Request", "Cash Flow", "Checks"]},
    "p3": {"builder": "build_fund_manager.py",
           "sheets": ["Start Here", "Fund Parameters", "Pipeline", "Eligibility & Scoring", "Allocation", "Disbursements",
                      "MRV Tracker", "Portfolio Dashboard", "Checks"]},
}

# views: key -> (sheet, range). Views on the same sheet go to different passes automatically.
VIEWS = {
    "p1": {
        "dash_kpi": ("Dashboard", "B1:F25"),
        "dash_charts": ("Dashboard", "B27:F63"),
        "inputs_demand": ("Inputs", "A1:F39"),
        "inputs_tech": ("Inputs", "A40:E77"),
        "cashflow": ("Cash Flow", "A1:I44"),
    },
    "p2": {
        "dash_kpi": ("Dashboard", "B1:F27"),
        "dash_charts": ("Dashboard", "B28:F62"),
        "gap": ("Funding Gap & RBF", "B1:E30"),
        "sens": ("Sensitivity", "B1:O33"),
        "finreq": ("Financing Request", "B1:F21"),
        "load": ("Load Profile", "A1:S34"),
        "segments": ("Inputs", "A33:K50"),
        "impact": ("Impact & MRV", "A1:L40"),
    },
    "p3": {
        "dash_kpi": ("Portfolio Dashboard", "B1:F41"),
        "dash_charts": ("Portfolio Dashboard", "B42:K64"),
        "alloc": ("Allocation", "A1:K15"),
        "elig": ("Eligibility & Scoring", "A5:P20"),
        "params": ("Fund Parameters", "A1:F37"),
        "mrv": ("MRV Tracker", "A1:K20"),
    },
}

# listing images: (file stem, view key or special, headline, subline) per language
CAPTIONS = {
    "p1": [
        ("01_hero", "dash_kpi",
         {"en": ("Mini-grid feasibility in 10 minutes", "IRR, NPV, LCOE, DSCR and the viability gap: the subsidy your project needs"),
          "fr": ("La faisabilité d'un mini-réseau en 10 minutes", "TRI, VAN, LCOE, DSCR et déficit de viabilité : la subvention dont votre projet a besoin")}),
        ("02_charts", "dash_charts",
         {"en": ("20-year cash flows at a glance", "Revenue, OPEX, CFADS against debt service, and the solar and diesel generation mix"),
          "fr": ("20 ans de flux en un coup d'œil", "Recettes, OPEX, CFADS face au service de la dette, et mix de production solaire et diesel")}),
        ("03_inputs", "inputs_demand",
         {"en": ("Clear, colour-coded inputs", "Customer segments, connection ramp-up, collection rate and scenario levers"),
          "fr": ("Des hypothèses claires et codées par couleur", "Segments de clientèle, montée en charge, taux de recouvrement et leviers de scénario")}),
        ("04_sizing", "inputs_tech",
         {"en": ("Automatic PV, battery and diesel sizing", "With battery round-trip losses, manual override, CAPEX per connection and battery replacement"),
          "fr": ("Dimensionnement automatique PV, batterie et diesel", "Pertes de stockage incluses, forçage manuel, CAPEX par raccordement, remplacement des batteries")}),
        ("05_engine", "cashflow",
         {"en": ("A transparent annual engine", "Every line is a readable formula: connections, energy, revenue, costs, tax, debt"),
          "fr": ("Un moteur annuel transparent", "Chaque ligne est une formule lisible : raccordements, énergie, recettes, charges, impôt, dette")}),
        ("06_manual", "manual", {"en": ("15-page PDF user manual included", "Method, formulas, worked example, checks and limits of use, in English and French"),
                                 "fr": ("Manuel d'utilisation PDF de 15 pages inclus", "Méthode, formules, exemple commenté, contrôles et limites d'emploi, en français et en anglais")}),
    ],
    "p2": [
        ("01_hero", "gap",
         {"en": ("How much grant or RBF does your mini-grid need?", "Viability gap, grant needed, RBF per connection and debt capacity, solved exactly"),
          "fr": ("Quelle subvention ou quel RBF pour votre mini-réseau ?", "Déficit de viabilité, subvention nécessaire, RBF par raccordement et capacité d'endettement, calculés exactement")}),
        ("02_dashboard", "dash_kpi",
         {"en": ("Bankability at a glance", "Project and equity returns, DSCR, LCOE, verdicts and affordability by segment"),
          "fr": ("La bancabilité en un coup d'œil", "Rentabilité projet et fonds propres, DSCR, LCOE, verdicts et capacité de paiement par segment")}),
        ("03_sensitivity", "sens",
         {"en": ("Live tornado sensitivity", "Tariff, demand, CAPEX, OPEX, collection, diesel price and interest rates, recalculated instantly"),
          "fr": ("Tornado de sensibilité dynamique", "Tarif, demande, CAPEX, OPEX, recouvrement, prix du diesel et taux d'intérêt, recalculés instantanément")}),
        ("04_financing_request", "finreq",
         {"en": ("Your financing note, written by the model", "Project summary, funding request, bankability, impact, sources and uses"),
          "fr": ("Votre note de financement, rédigée par le modèle", "Résumé du projet, demande de financement, bancabilité, impact, emplois et ressources")}),
        ("05_load_profile", "load",
         {"en": ("Hourly load profile drives the sizing", "Night-time share sizes the battery, the peak ratio sizes the generator"),
          "fr": ("La courbe de charge horaire pilote le dimensionnement", "La part nocturne dimensionne la batterie, le ratio de pointe le groupe diesel")}),
        ("06_segments", "segments",
         {"en": ("Five customer segments, each with its own RBF", "Tariff, connection fee, RBF per connection and an affordability test"),
          "fr": ("Cinq segments, chacun avec son RBF", "Tarif, frais de raccordement, RBF par raccordement et test de capacité de paiement")}),
        ("07_impact", "impact",
         {"en": ("Impact and MRV indicators", "Verified connections, people with access, jobs, MWh, CO2 avoided, RBF disbursed"),
          "fr": ("Indicateurs d'impact et de MRV", "Raccordements vérifiés, personnes desservies, emplois, MWh, CO2 évité, RBF décaissé")}),
        ("08_manual", "manual", {"en": ("16-page PDF user manual included", "Method, exact RBF calibration, worked example, checks and limits, in English and French"),
                                 "fr": ("Manuel d'utilisation PDF de 16 pages inclus", "Méthode, calibrage exact du RBF, exemple commenté, contrôles et limites, en français et en anglais")}),
    ],
    "p3": [
        ("01_hero", "dash_kpi",
         {"en": ("Allocate RBF and grants across your pipeline", "Commitments, impact bought, leverage, concentration and portfolio verdicts"),
          "fr": ("Allouez le RBF et les subventions sur votre pipeline", "Engagements, impact financé, effet de levier, concentration et verdicts sur le portefeuille")}),
        ("02_allocation", "alloc",
         {"en": ("Rank-order allocation with live limits", "Envelope and country ceilings applied in order, with the binding constraint shown"),
          "fr": ("Allocation par rang avec limites dynamiques", "Enveloppe et plafonds par pays appliqués dans l'ordre, contrainte limitante affichée")}),
        ("03_eligibility", "elig",
         {"en": ("Eligibility screening with reasons", "Eight switchable criteria and the rejection reason for every applicant"),
          "fr": ("Éligibilité motivée", "Huit critères activables et le motif de rejet de chaque candidat")}),
        ("04_parameters", "params",
         {"en": ("Your fund's rules, in one sheet", "Envelope, over-commitment, support profiles, RBF tranches and concentration limits"),
          "fr": ("Les règles de votre fonds, sur un seul onglet", "Enveloppe, surengagement, profils de soutien, tranches RBF et limites de concentration")}),
        ("05_mrv", "mrv",
         {"en": ("MRV tracker for the life of the fund", "Verified connections against targets, RBF earned and outstanding, project status"),
          "fr": ("Suivi MRV sur toute la vie du fonds", "Raccordements vérifiés vs cibles, RBF acquis et restant dû, statut par projet")}),
        ("06_charts", "dash_charts",
         {"en": ("Portfolio charts", "Allocation by project, expected disbursements by year and allocation by country"),
          "fr": ("Graphiques du portefeuille", "Allocation par projet, décaissements attendus par année et allocation par pays")}),
        ("07_manual", "manual", {"en": ("15-page PDF user manual included", "Method, scoring, allocation rules, worked example and limits, in English and French"),
                                 "fr": ("Manuel d'utilisation PDF de 15 pages inclus", "Méthode, notation, règles d'allocation, exemple commenté et limites, en français et en anglais")}),
    ],
}

FOOTER = {
    "en": "Unedited screenshot of the workbook. Example values are illustrative, not market benchmarks.",
    "fr": "Capture non retouchée du classeur. Les valeurs d'exemple sont illustratives et ne sont pas des références de marché.",
}
FOOTER_MANUAL = {"en": "Actual pages of the manual supplied with the workbook.", "fr": "Pages réelles du manuel fourni avec le classeur."}
KICKER = "ENERGY ACCESS FINANCE TOOLKIT  |  EMMANUEL BOUJIEKA KAMGA"
MANUALS = {
    ("p1", "en"): "product/01-entry-calculator/Manual_MiniGrid_Feasibility_Calculator_EN.pdf",
    ("p1", "fr"): "product/01-entry-calculator/Manuel_Calculateur_Faisabilite_MiniReseau_FR.pdf",
    ("p2", "en"): "product/02-developer-edition/Manual_Developer_Edition_EN.pdf",
    ("p2", "fr"): "product/02-developer-edition/Manuel_Modele_Financier_Developpeur_FR.pdf",
    ("p3", "en"): "product/03-fund-manager/Manual_Fund_Manager_Edition_EN.pdf",
    ("p3", "fr"): "product/03-fund-manager/Manuel_Modele_Gestionnaire_Fonds_FR.pdf",
}


def tr_sheet(name, lang):
    return i18n_fr.SHEETS.get(name, name) if lang == "fr" else name


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[:3]} failed: {r.stderr[-800:]}")
    return r.stdout


def passes(product):
    """Split views so that each pass has at most one view per sheet."""
    out = []
    for key, (sheet, rng) in VIEWS[product].items():
        for p in out:
            if sheet not in {s for s, _ in p.values()}:
                p[key] = (sheet, rng)
                break
        else:
            out.append({key: (sheet, rng)})
    return out


def crop(img, pad=18):
    bg = Image.new(img.mode, img.size, (255, 255, 255))
    bbox = ImageChops.difference(img, bg).convert("L").point(lambda v: 255 if v > 12 else 0).getbbox()
    if not bbox:
        return img
    l, t, r, b = bbox
    return img.crop((max(0, l - pad), max(0, t - pad), min(img.width, r + pad), min(img.height, b + pad)))


def render_views(product, lang):
    spec = PRODUCTS[product]
    shots = {}
    for i, views in enumerate(passes(product)):
        work = TMP / f"{product}_{lang}_{i}"
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        areas = {tr_sheet(s, lang): "ZZ1000:ZZ1000" for s in spec["sheets"]}  # empty range: sheet not printed
        for key, (sheet, rng) in views.items():
            areas[tr_sheet(sheet, lang)] = rng
        xlsx = work / "m.xlsx"
        env = dict(os.environ, PRINT_AREAS=json.dumps(areas))
        run([sys.executable, str(ROOT / "tools" / spec["builder"]), str(xlsx), "--lang", lang], env=env, cwd=ROOT)
        res = json.loads(run([sys.executable, RECALC, str(xlsx), "300"]))
        if res.get("total_errors", 1) != 0:
            raise RuntimeError(f"recalc errors in {product} {lang}: {res}")
        run(["soffice", "--headless", f"-env:UserInstallation={LO_PROFILE}", "--convert-to", "pdf", "--outdir", str(work), str(xlsx)])
        pdf = work / "m.pdf"
        pages = int([l for l in run(["pdfinfo", str(pdf)]).splitlines() if l.startswith("Pages")][0].split()[-1])
        order = sorted(views, key=lambda k: spec["sheets"].index(views[k][0]))
        if pages != len(order):
            raise RuntimeError(f"{product} {lang}: expected {len(order)} pages, got {pages}")
        for key in views:
            page = order.index(key) + 1
            run(["pdftoppm", "-png", "-r", "220", "-f", str(page), "-l", str(page), "-singlefile", str(pdf), str(work / key)])
            shots[key] = crop(Image.open(work / f"{key}.png").convert("RGB"))
    return shots


def manual_strip(product, lang):
    pdf = ROOT / MANUALS[(product, lang)]
    work = TMP / f"{product}_{lang}_manual"
    work.mkdir(parents=True, exist_ok=True)
    # cover plus the two densest content pages (tables, method, example)
    pages = int([l for l in run(["pdfinfo", str(pdf)]).splitlines() if l.startswith("Pages")][0].split()[-1])
    density = {n: len(run(["pdftotext", "-f", str(n), "-l", str(n), str(pdf), "-"])) for n in range(4, pages)}
    chosen = [1] + sorted(sorted(density, key=density.get, reverse=True)[:2])
    imgs = []
    for n in chosen:
        run(["pdftoppm", "-png", "-r", "110", "-f", str(n), "-l", str(n), "-singlefile", str(pdf), str(work / f"p{n}")])
        imgs.append(Image.open(work / f"p{n}.png").convert("RGB"))
    return imgs


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def card(canvas, img, box):
    """Paste img scaled into box (x0, y0, x1, y1) on a white card with a soft shadow."""
    x0, y0, x1, y1 = box
    scale = min((x1 - x0) / img.width, (y1 - y0) / img.height)
    w, h = int(img.width * scale), int(img.height * scale)
    img = img.resize((w, h), Image.LANCZOS)
    x, y = x0 + ((x1 - x0) - w) // 2, y0 + ((y1 - y0) - h) // 2
    shadow = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((30, 34, w + 30, h + 34), fill=(20, 40, 70, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    canvas.paste(shadow, (x - 30, y - 30), shadow)
    canvas.paste(img, (x, y))
    ImageDraw.Draw(canvas).rectangle((x, y, x + w - 1, y + h - 1), outline=(205, 214, 224), width=2)


def compose(headline, subline, footer, content):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 330), fill=NAVY)
    d.text((110, 62), KICKER, font=fit_font(d, KICKER, F_REG, 30, W - 220), fill=(201, 214, 227))
    f_head = ImageFont.truetype(F_BOLD, 74)
    while d.textlength(headline, font=f_head) > W - 220 and f_head.size > 50:
        f_head = ImageFont.truetype(F_BOLD, f_head.size - 2)
    d.text((110, 112), headline, font=f_head, fill="white")
    f_sub = ImageFont.truetype(F_REG, 38)
    for k, line in enumerate(wrap(d, subline, f_sub, W - 220)[:2]):
        d.text((110, 208 + k * 48), line, font=f_sub, fill=(170, 222, 216))
    if isinstance(content, list):  # manual pages side by side
        n = len(content)
        gap = 60
        slot = (W - 220 - gap * (n - 1)) // n
        for k, page in enumerate(content):
            x0 = 110 + k * (slot + gap)
            card(im, page, (x0, 400, x0 + slot, H - 140))
    else:
        card(im, content, (110, 400, W - 110, H - 140))
    d.text((110, H - 92), footer, font=ImageFont.truetype(F_REG, 28), fill=(100, 112, 128))
    return im


# ---------------------------------------------------------------- Gumroad thumbnail and cover
GUMROAD = {
    "p1": {"accent": (27, 127, 121), "view": "dash_kpi",
           "name": {"en": "Mini-Grid Feasibility Calculator", "fr": "Calculateur de faisabilité de mini-réseau"},
           "tag": {"en": "IRR, NPV, LCOE, DSCR and the viability gap", "fr": "TRI, VAN, LCOE, DSCR et déficit de viabilité"},
           "points": {"en": ["The subsidy your project needs, as a viability gap", "Automatic PV, battery and diesel sizing", "15-page PDF manual in English and French"],
                      "fr": ["La subvention nécessaire, chiffrée en déficit de viabilité", "Dimensionnement automatique PV, batterie et diesel", "Manuel PDF de 15 pages en français et en anglais"]}},
    "p2": {"accent": (200, 129, 26), "view": "gap",
           "name": {"en": "Energy Access Financial Model", "fr": "Modèle financier d'accès à l'énergie"},
           "edition": {"en": "Developer Edition", "fr": "Édition Développeur"},
           "tag": {"en": "Grant, RBF and debt sized exactly", "fr": "Subvention, RBF et dette calculés exactement"},
           "points": {"en": ["Viability gap and RBF per connection, solved exactly", "Debt capacity at your minimum DSCR", "Live tornado, impact and MRV, financing note"],
                      "fr": ["Déficit de viabilité et RBF par raccordement, calcul exact", "Capacité d'endettement au DSCR minimum", "Tornado dynamique, impact et MRV, note de financement"]}},
    "p3": {"accent": (107, 79, 160), "view": "dash_kpi",
           "name": {"en": "Energy Access Fund Manager Model", "fr": "Modèle du gestionnaire de fonds d'accès à l'énergie"},
           "edition": {"en": "RBF & Portfolio Edition", "fr": "Édition RBF & Portefeuille"},
           "tag": {"en": "Screen, score and allocate RBF and grants", "fr": "Sélectionner, noter et allouer RBF et subventions"},
           "points": {"en": ["Eligibility screening and weighted scoring", "Allocation within envelope and country limits", "Disbursements, fund cash position, MRV tracker"],
                      "fr": ["Éligibilité motivée et notation pondérée", "Allocation dans l'enveloppe et les limites par pays", "Décaissements, trésorerie du fonds, suivi MRV"]}},
}
AUTHOR_NAME = "Emmanuel Boujieka Kamga"
BADGE = {"en": "EXCEL  |  ENGLISH + FRENCH  |  PDF MANUAL", "fr": "EXCEL  |  FRANÇAIS + ANGLAIS  |  MANUEL PDF"}
SHOT_NOTE = {"en": "Unedited screenshot. Example values are illustrative.", "fr": "Capture non retouchée. Valeurs d'exemple illustratives."}


def fit_font(draw, text, path, size, width, min_size=28):
    f = ImageFont.truetype(path, size)
    while draw.textlength(text, font=f) > width and f.size > min_size:
        f = ImageFont.truetype(path, f.size - 2)
    return f


def fit_lines(draw, text, path, size, width, max_lines):
    """Largest font (from size down) whose wrapped text fits in max_lines; never truncates."""
    f = ImageFont.truetype(path, size)
    while len(wrap(draw, text, f, width)) > max_lines and f.size > 20:
        f = ImageFont.truetype(path, f.size - 2)
    return f, wrap(draw, text, f, width)


def draw_lines(draw, xy, lines, font, fill, gap):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + gap
    return y


def gumroad_thumbnail(p, lg, shot):
    g = GUMROAD[p]
    S = 1200
    im = Image.new("RGB", (S, S), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, S, 22), fill=g["accent"])
    d.text((80, 80), "ENERGY ACCESS FINANCE TOOLKIT", font=ImageFont.truetype(F_REG, 30), fill=(201, 214, 227))
    f_name, lines = fit_lines(d, g["name"][lg], F_BOLD, 84, S - 160, 3)
    y = draw_lines(d, (80, 140), lines, f_name, "white", 10)
    if "edition" in g:
        f_ed = ImageFont.truetype(F_BOLD, 50)
        y = draw_lines(d, (80, y + 6), [g["edition"][lg]], f_ed, tuple(min(255, c + 70) for c in g["accent"]), 0)
    f_tag, lines = fit_lines(d, g["tag"][lg], F_REG, 40, S - 160, 2)
    y = draw_lines(d, (80, y + 22), lines, f_tag, (170, 222, 216), 8)
    # author, large
    by = {"en": "by ", "fr": "par "}[lg]
    f_by = ImageFont.truetype(F_REG, 44)
    f_au = fit_font(d, AUTHOR_NAME, F_BOLD, 60, S - 160 - d.textlength(by, font=f_by), 36)
    y += 34
    d.text((80, y + (f_au.size - f_by.size) * 0.8), by, font=f_by, fill=(201, 214, 227))
    d.text((80 + d.textlength(by, font=f_by), y), AUTHOR_NAME, font=f_au, fill="white")
    y += f_au.size + 6
    d.rectangle((80, y + 8, 80 + 140, y + 14), fill=g["accent"])
    y += 14
    # screenshot crop (top-left of the real view) as a card at the bottom
    crop_box = (0, 0, int(shot.width * 0.78), int(shot.height * 0.36))
    part = shot.crop(crop_box)
    top = max(y + 46, 700)
    card(im, part, (80, top, S - 80, S - 130))
    f_b = fit_font(d, BADGE[lg], F_BOLD, 30, S - 160)
    d.text((80, S - 92), BADGE[lg], font=f_b, fill="white")
    return im


def gumroad_cover(p, lg, shot):
    g = GUMROAD[p]
    W2, H2 = 1920, 1080
    im = Image.new("RGB", (W2, H2), BG)
    d = ImageDraw.Draw(im)
    panel = 760
    d.rectangle((0, 0, panel, H2), fill=NAVY)
    d.rectangle((0, 0, panel, 14), fill=g["accent"])
    d.text((70, 70), KICKER, font=fit_font(d, KICKER, F_REG, 24, panel - 140, 16), fill=(201, 214, 227))
    f_name, lines = fit_lines(d, g["name"][lg], F_BOLD, 60, panel - 140, 3)
    y = draw_lines(d, (70, 120), lines, f_name, "white", 8)
    if "edition" in g:
        f_ed = ImageFont.truetype(F_BOLD, 38)
        y = draw_lines(d, (70, y + 4), [g["edition"][lg]], f_ed, tuple(min(255, c + 70) for c in g["accent"]), 0)
    f_tag, lines = fit_lines(d, g["tag"][lg], F_REG, 32, panel - 140, 2)
    y = draw_lines(d, (70, y + 18), lines, f_tag, (170, 222, 216), 6)
    f_pt = ImageFont.truetype(F_REG, 28)
    y += 40
    for pt in g["points"][lg]:
        d.rectangle((70, y + 11, 82, y + 23), fill=g["accent"])
        y = draw_lines(d, (104, y), wrap(d, pt, f_pt, panel - 180), f_pt, "white", 6) + 18
    f_b = fit_font(d, BADGE[lg], F_BOLD, 24, panel - 140)
    d.text((70, H2 - 80), BADGE[lg], font=f_b, fill="white")
    card(im, shot, (panel + 60, 90, W2 - 60, H2 - 110))
    d.text((panel + 60, H2 - 62), SHOT_NOTE[lg], font=ImageFont.truetype(F_REG, 22), fill=(100, 112, 128))
    return im


def build_gumroad(p, lg, shots):
    outdir = OUT / "gumroad"
    outdir.mkdir(parents=True, exist_ok=True)
    shot = shots[GUMROAD[p]["view"]]
    t = gumroad_thumbnail(p, lg, shot)
    t.save(outdir / f"{p}_thumbnail_{lg}.png", dpi=(72, 72), optimize=True)
    c = gumroad_cover(p, lg, shot)
    c.save(outdir / f"{p}_cover_{lg}.jpg", dpi=(72, 72), quality=92, optimize=True)
    print("wrote", outdir / f"{p}_thumbnail_{lg}.png", "and cover")


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "all"
    prod = args[args.index("--product") + 1] if "--product" in args else "all"
    langs = ["en", "fr"] if lang == "all" else [lang]
    prods = list(PRODUCTS) if prod == "all" else [prod]
    for p in prods:
        for lg in langs:
            shots = render_views(p, lg)
            build_gumroad(p, lg, shots)
            if "--gumroad-only" in args:
                continue
            outdir = OUT / f"{p}_{lg}"
            outdir.mkdir(parents=True, exist_ok=True)
            for stem, view, caps in CAPTIONS[p]:
                head, sub = caps[lg]
                if view == "manual":
                    img = compose(head, sub, FOOTER_MANUAL[lg], manual_strip(p, lg))
                else:
                    img = compose(head, sub, FOOTER[lg], shots[view])
                img.save(outdir / f"{stem}.jpg", quality=90, optimize=True)
                print("wrote", outdir / f"{stem}.jpg")


if __name__ == "__main__":
    main()
