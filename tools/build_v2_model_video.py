"""Build the Book 2 model tutorial video: MODEL 2, the PAYGo Company Financial and Investment Model, in twelve steps.

Run: python tools/build_v2_model_video.py
Visuals are renders of the real workbook (layout, formats, fills and evaluated values) with highlights and captions;
narration uses the shared neural voice; assembly with ffmpeg (gentle camera moves, crossfades, chapters, subtitles).
Outputs to volumes/02-solar-home-systems/video-course/: the MP4, its SRT subtitles and the Module 17 script.
"""
import base64
import html
import json
import pickle
import re
import shutil
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).parent))
import av_common as A  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCR = Path("/tmp/claude-0/-home-user-Boujieka/5b078838-abd3-5f75-bf1a-e73c18413f2f/scratchpad")
WORK = SCR / "video_m17"
OUTD = ROOT / "volumes/02-solar-home-systems/video-course"
MODEL = ROOT / "volumes/02-solar-home-systems/model/AEF_SHS_PAYGo_Model_v0.8-dev.xlsx"
CASE = ROOT / "volumes/02-solar-home-systems/case-study/SolaraPay_Case_Model_v0.8-dev.xlsx"
# evaluated values: full recalculations of the same workbooks saved with their values
VALS = {"model": (MODEL, SCR / "lo/s5out/fm.xlsx"), "case": (CASE, SCR / "lo/s5out/fc.xlsx")}
W, H = 1920, 1080
GREEN, GOLD = "#0B3020", "#B07C0F"


# ------------------------------------------------------------------ number formats
def excel_date(x):
    return date(1899, 12, 30) + timedelta(days=float(x))


def fmt(v, nf):
    if v is None or v == "":
        return ""
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (datetime, date)):
        d = v.date() if isinstance(v, datetime) else v
        return d.strftime("%b-%y") if nf and "mmm" in nf else d.strftime("%d/%m/%Y")
    if isinstance(v, str):
        return v
    x = float(v)
    nf = nf or "General"
    if "mmm" in nf or "yy" in nf:
        try:
            return excel_date(x).strftime("%b-%y")
        except (OverflowError, ValueError):
            return str(v)
    if nf in ("General",):
        if abs(x - round(x)) < 1e-9 and abs(x) < 1e15:
            return f"{int(round(x))}"
        return f"{x:.6g}"
    if nf == "@":
        return str(v)
    secs = nf.split(";")
    if x < 0 and len(secs) > 1:
        sec, neg = secs[1], True
    elif x == 0 and len(secs) > 2:
        sec, neg = secs[2], False
    else:
        sec, neg = secs[0], False
    lit = re.fullmatch(r'"(.*)"', sec)
    if lit:
        return lit.group(1)
    pct = "%" in sec
    m = re.search(r"0\.(0+)", sec)
    dec = len(m.group(1)) if m else 0
    core = re.sub(r'"[^"]*"', "", sec)
    scale = len(re.search(r"[0#](,*)\W*$", core).group(1)) if re.search(r"[0#](,*)\W*$", core) else 0
    x = x / 1000 ** scale  # trailing commas after the last digit placeholder scale by a thousand each
    thou = "," in core.rstrip(",)") if scale else "," in sec
    suffix = "x" if '"x"' in sec else ""
    val = abs(x) * (100 if pct else 1) if (neg or "(" in sec) else x * (100 if pct else 1)
    s = f"{val:,.{dec}f}" if thou else f"{val:.{dec}f}"
    s += ("%" if pct else "") + suffix
    if "(" in sec and neg:
        s = f"({s})"
    elif x < 0 and len(secs) == 1:
        s = s if s.startswith("-") else s
    return s


def rgb(c):
    try:
        if c is not None and c.type == "rgb" and isinstance(c.rgb, str) and len(c.rgb) == 8 and c.rgb != "00000000":
            return "#" + c.rgb[2:]
    except Exception:  # noqa: BLE001
        pass
    return None


# ------------------------------------------------------------------ renderer
class Book:
    def __init__(self, key):
        path, recalc = VALS[key]
        self.key, self.path = key, path
        self.wb = openpyxl.load_workbook(path)
        self.vals = openpyxl.load_workbook(recalc, data_only=True)

    def value(self, ws, cell):
        v = cell.value
        if isinstance(v, str) and v.startswith("="):
            x = self.vals[ws.title][cell.coordinate].value
            return "" if x is None else x
        return v


def col_px(ws, c):
    d = ws.column_dimensions.get(get_column_letter(c))
    w = d.width if d is not None and d.width else 8.43
    return int(w * 7 + 5)


def row_px(ws, r):
    d = ws.row_dimensions.get(r)
    h = d.height if d is not None and d.height else 15
    return int(h * 96 / 72)


def parse_rng(rng):
    a, b = (rng.split(":") + [rng])[:2]
    m1, m2 = re.fullmatch(r"([A-Z]+)(\d+)", a), re.fullmatch(r"([A-Z]+)(\d+)", b)
    return column_index_from_string(m1.group(1)), int(m1.group(2)), column_index_from_string(m2.group(1)), int(m2.group(2))


def render(book, sheet, rng, highlights, caption, step, select=None):
    ws = book.wb[sheet]
    c0, r0, c1, r1 = parse_rng(rng)
    xs, x = {}, 0
    for c in range(c0, c1 + 2):
        xs[c] = x
        if c <= c1:
            x += col_px(ws, c)
    ys, y = {}, 0
    for r in range(r0, r1 + 2):
        ys[r] = y
        if r <= r1:
            y += row_px(ws, r)
    gw, gh = xs[c1 + 1], ys[r1 + 1]
    merged = {}
    covered = set()
    for mr in ws.merged_cells.ranges:
        if mr.min_row > r1 or mr.max_row < r0 or mr.min_col > c1 or mr.max_col < c0:
            continue
        merged[(mr.min_row, mr.min_col)] = (min(mr.max_row, r1), min(mr.max_col, c1))
        for rr in range(mr.min_row, mr.max_row + 1):
            for cc in range(mr.min_col, mr.max_col + 1):
                if (rr, cc) != (mr.min_row, mr.min_col):
                    covered.add((rr, cc))
    grid = ws.sheet_view.showGridLines is not False
    cells = []
    vals = {}
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if (r, c) not in covered:
                vals[(r, c)] = book.value(ws, ws.cell(r, c))
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if (r, c) in covered:
                continue
            cell = ws.cell(r, c)
            rr, cc = merged.get((r, c), (r, c))
            left, top = xs[c], ys[r]
            width, height = xs[cc + 1] - left, ys[rr + 1] - top
            v = vals[(r, c)]
            txt = fmt(v, cell.number_format)
            f = cell.font
            box = [f"left:{left}px", f"top:{top}px", f"width:{width}px", f"height:{height}px"]
            bg = rgb(cell.fill.fgColor) if cell.fill is not None and cell.fill.fill_type == "solid" else None
            if bg:
                box.append(f"background:{bg}")
            elif grid:
                box.append("border-right:1px solid #e3e3e3;border-bottom:1px solid #e3e3e3")
            b = cell.border
            for side, nm in ((b.left, "left"), (b.right, "right"), (b.top, "top"), (b.bottom, "bottom")):
                if side is not None and side.style:
                    bc = rgb(side.color) or "#9a9a9a"
                    wpx = 2 if side.style in ("medium", "thick") else 1
                    box.append(f"border-{nm}:{wpx}px solid {bc}")
            cells.append(f'<div class="b" style="{";".join(box)}"></div>')
            if txt == "":
                continue
            al = cell.alignment.horizontal if cell.alignment is not None else None
            numeric = isinstance(v, (int, float)) and not isinstance(v, bool)
            wrap = cell.alignment is not None and cell.alignment.wrap_text
            tw = width
            if not numeric and not wrap and al in (None, "left", "general") and (r, c) not in merged:
                k = cc + 1
                while k <= c1 and (r, k) not in covered and vals.get((r, k)) in (None, "") and (r, k) not in merged:
                    tw += xs[k + 1] - xs[k]
                    k += 1
            ts = [f"left:{left}px", f"top:{top}px", f"width:{tw}px", f"height:{height}px"]
            col = rgb(f.color) if f is not None and f.color is not None else None
            if col:
                ts.append(f"color:{col}")
            if f is not None and f.b:
                ts.append("font-weight:700")
            if f is not None and f.i:
                ts.append("font-style:italic")
            if f is not None and f.sz:
                ts.append(f"font-size:{float(f.sz) * 96 / 72:.1f}px")
            if al in ("right",) or (al is None and numeric):
                ts.append("justify-content:flex-end")
            elif al in ("center", "centerContinuous"):
                ts.append("justify-content:center")
            if wrap:
                va = cell.alignment.vertical if cell.alignment is not None else None
                # Excel's default vertical alignment is bottom
                ts.append("white-space:normal;line-height:1.15;align-items:" + {"center": "center", "top": "flex-start"}.get(va, "flex-end"))
            cells.append(f'<div class="c" style="{";".join(ts)}">{html.escape(txt)}</div>')
    # images anchored in the range (logo on the cover)
    for img in getattr(ws, "_images", []):
        try:
            fr = img.anchor._from
            ic, ir = fr.col + 1, fr.row + 1
            if c0 <= ic <= c1 and r0 <= ir <= r1:
                data = img._data()
                b64 = base64.b64encode(data).decode()
                cells.append(f'<img style="position:absolute;left:{xs[ic] + fr.colOff / 9525:.0f}px;top:{ys[ir] + fr.rowOff / 9525:.0f}px;'
                             f'width:{img.width}px;height:{img.height}px" src="data:image/png;base64,{b64}">')
        except Exception:  # noqa: BLE001
            pass
    hl = []
    boxes = []
    for i, (hr, label) in enumerate(highlights):
        hc0, hr0, hc1, hr1 = parse_rng(hr)
        hx, hy = xs[max(hc0, c0)], ys[max(hr0, r0)]
        hw, hh = xs[min(hc1, c1) + 1] - hx, ys[min(hr1, r1) + 1] - hy
        boxes.append((hx, hy, hw, hh))
        hl.append((hx, hy, hw, hh, i + 1, label))
    # layout and scale
    top_ui, bottom_ui, rowhdr, colhdr = 74, 34, 46, 24
    labels = [(k, lab) for (_, _, _, _, k, lab) in hl if lab]
    cap_h = 152 if labels else 118
    avail_w, avail_h = W - rowhdr - 8, H - top_ui - bottom_ui - colhdr - cap_h - 8
    z = min(avail_w / gw, avail_h / gh, 1.9)
    # each box is numbered in the row number gutter beside its first row, and the numbers are explained in the caption
    # panel, so no marker covers a cell
    marks, gutter = [], []
    for hx, hy, hw, hh, k, lab in hl:
        marks.append(f'<div class="hl" style="left:{hx - 3}px;top:{hy - 3}px;width:{hw}px;height:{hh}px;border-width:{4 / z:.2f}px"></div>')
        if lab:
            r_first = next(r for r in range(r0, r1 + 1) if ys[r] >= hy - 0.5)
            cy = top_ui + colhdr + (ys[r_first] + (ys[r_first + 1] - ys[r_first]) / 2) * z
            gutter.append(f'<div class="mk" style="left:{(rowhdr - 30) / 2:.0f}px;top:{cy - 15:.0f}px">{k}</div>')
    legend = "".join(f'<span class="lg"><span class="lk">{k}</span>{html.escape(lab)}</span>' for k, lab in labels)
    colhdrs = "".join(f'<div class="ch" style="left:{xs[c] * z:.1f}px;width:{(xs[c + 1] - xs[c]) * z:.1f}px">{get_column_letter(c)}</div>' for c in range(c0, c1 + 1))
    rowhdrs = "".join(f'<div class="rh" style="top:{ys[r] * z:.1f}px;height:{(ys[r + 1] - ys[r]) * z:.1f}px">{r}</div>' for r in range(r0, r1 + 1))
    sel = select or (highlights[0][0].split(":")[0] if highlights else f"{get_column_letter(c0)}{r0}")
    scell = ws[sel]
    ftxt = scell.value if isinstance(scell.value, str) and scell.value.startswith("=") else fmt(book.value(ws, scell), scell.number_format)
    tabs_all = book.wb.sheetnames
    i0 = tabs_all.index(sheet)
    window = tabs_all[max(0, i0 - 5): i0 + 7]
    tabs = "".join(f'<div class="tab{" on" if t == sheet else ""}">{html.escape(t)}</div>' for t in window)
    fname = book.path.name
    page = f"""<html><head><meta charset="utf-8"><style>
body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;font-family:'Liberation Sans',Arial,sans-serif;background:#fff}}
.title{{position:absolute;left:0;top:0;width:{W}px;height:40px;background:{GREEN};color:#fff;font-size:17px;display:flex;align-items:center;padding-left:18px;box-sizing:border-box}}
.title b{{color:#E3C27A;margin-right:14px;letter-spacing:1px}}
.fbar{{position:absolute;left:0;top:40px;width:{W}px;height:34px;background:#f3f3f3;border-bottom:1px solid #d0d0d0;display:flex;align-items:center;font-size:15px}}
.nbox{{width:110px;height:24px;margin-left:8px;border:1px solid #c8c8c8;background:#fff;display:flex;align-items:center;padding-left:6px}}
.fx{{margin:0 10px;color:#777;font-style:italic}}
.ftext{{flex:1;height:24px;border:1px solid #c8c8c8;background:#fff;display:flex;align-items:center;padding-left:8px;margin-right:8px;overflow:hidden;white-space:nowrap;font-family:'Liberation Mono',monospace;font-size:14px}}
.colhdr{{position:absolute;left:{rowhdr}px;top:{top_ui}px;height:{colhdr}px;width:{W - rowhdr}px;background:#efefef;border-bottom:1px solid #c8c8c8;overflow:hidden}}
.ch{{position:absolute;top:0;height:{colhdr}px;border-right:1px solid #d6d6d6;font-size:13px;color:#555;display:flex;align-items:center;justify-content:center;box-sizing:border-box}}
.rowhdr{{position:absolute;left:0;top:{top_ui + colhdr}px;width:{rowhdr}px;height:{H - top_ui - colhdr - bottom_ui}px;background:#efefef;border-right:1px solid #c8c8c8;overflow:hidden}}
.rh{{position:absolute;left:0;width:{rowhdr}px;border-bottom:1px solid #d6d6d6;font-size:12px;color:#555;display:flex;align-items:center;justify-content:center;box-sizing:border-box}}
.gridwrap{{position:absolute;left:{rowhdr}px;top:{top_ui + colhdr}px;width:{W - rowhdr}px;height:{H - top_ui - colhdr - bottom_ui}px;overflow:hidden}}
.grid{{position:absolute;left:0;top:0;width:{gw}px;height:{gh}px;transform:scale({z:.4f});transform-origin:0 0;
}}
.b{{position:absolute;box-sizing:border-box}}
.c{{position:absolute;box-sizing:border-box;display:flex;align-items:center;padding:0 3px;font-size:13.3px;white-space:nowrap;overflow:hidden;color:#000;z-index:2}}
.hl{{z-index:3}}
.hl{{position:absolute;border:4px solid {GOLD};background:rgba(176,124,15,0.10);box-sizing:content-box;border-radius:3px;box-shadow:0 0 0 2000px rgba(0,0,0,0.0)}}
.mk{{position:absolute;z-index:6;width:30px;height:30px;font-size:16px;background:{GOLD};color:#fff;font-weight:700;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,0.35)}}
.lgs{{margin-top:8px;font-size:17px;color:#F1E4C3}}
.lg{{margin-right:26px;white-space:nowrap}}
.lk{{display:inline-flex;width:24px;height:24px;border-radius:50%;background:{GOLD};color:#fff;font-weight:700;font-size:14px;align-items:center;justify-content:center;margin-right:8px;vertical-align:1px}}
.tabs{{position:absolute;left:0;bottom:0;width:{W}px;height:{bottom_ui}px;background:#f3f3f3;border-top:1px solid #c8c8c8;display:flex;align-items:stretch;padding-left:30px;font-size:14px}}
.tab{{padding:0 16px;display:flex;align-items:center;color:#444;border-right:1px solid #d0d0d0}}
.tab.on{{background:#fff;color:{GREEN};font-weight:700;border-bottom:3px solid {GREEN}}}
.cap{{position:absolute;left:70px;right:70px;bottom:{bottom_ui + 16}px;min-height:{cap_h - 30}px;background:rgba(11,48,32,0.94);color:#fff;border-left:6px solid {GOLD};
  border-radius:4px;padding:14px 22px;box-sizing:border-box;font-size:25px;line-height:1.3;display:flex;flex-direction:column;justify-content:center}}
.cap .st{{color:#E3C27A;font-size:16px;font-weight:700;letter-spacing:1.5px;margin-bottom:4px}}
</style></head><body>
<div class="title"><b>AFRICA ENERGY FINANCE</b>{html.escape(fname)}&nbsp;&nbsp;|&nbsp;&nbsp;{html.escape(sheet)}</div>
<div class="fbar"><div class="nbox">{html.escape(sel)}</div><div class="fx">fx</div><div class="ftext">{html.escape(str(ftxt)[:160])}</div></div>
<div class="colhdr">{colhdrs}</div><div class="rowhdr">{rowhdrs}</div>
<div class="gridwrap"><div class="grid">{''.join(cells)}{''.join(marks)}</div></div>
{''.join(gutter)}
<div class="tabs">{tabs}</div>
<div class="cap"><div class="st">{html.escape(step.upper())}</div>{html.escape(caption)}{f'<div class="lgs">{legend}</div>' if legend else ''}</div>
</body></html>"""
    # focus point for the camera: centre of the first highlight, in screen pixels
    if boxes:
        bx, by, bw, bh = boxes[0]
        fx, fy = rowhdr + (bx + bw / 2) * z, top_ui + colhdr + (by + bh / 2) * z
    else:
        fx, fy = W / 2, H / 2
    return page, (fx, fy)


def card(kicker, title, subtitle, foot=""):
    logo = base64.b64encode((ROOT / "brand/aef_logo.png").read_bytes()).decode()
    return f"""<html><head><meta charset="utf-8"><style>
body{{margin:0;width:{W}px;height:{H}px;background:#FBF8F0;font-family:'Liberation Sans',Arial,sans-serif;overflow:hidden}}
.logo{{position:absolute;left:120px;top:90px;width:560px}}
.panel{{position:absolute;left:0;right:0;top:400px;height:430px;background:{GREEN};border-top:6px solid {GOLD};border-bottom:6px solid {GOLD};color:#fff;padding:60px 120px;box-sizing:border-box}}
.k{{color:#E3C27A;font-size:28px;font-weight:700;letter-spacing:3px}}
.t{{font-size:68px;font-weight:700;margin:24px 0 18px 0;line-height:1.1}}
.s{{font-size:32px;color:#e8e8e8}}
.f{{position:absolute;left:120px;bottom:70px;font-size:22px;color:#555}}
</style></head><body><img class="logo" src="data:image/png;base64,{logo}">
<div class="panel"><div class="k">{html.escape(kicker)}</div><div class="t">{html.escape(title)}</div><div class="s">{html.escape(subtitle)}</div></div>
<div class="f">{html.escape(foot)}</div></body></html>"""


# ------------------------------------------------------------------ scenes
S = []


def scene(step, sheet, rng, highlights, caption, narration, book="model", select=None):
    S.append(dict(kind="sheet", step=step, sheet=sheet, rng=rng, hl=highlights, caption=caption, text=narration, book=book, select=select))


def title(kicker, t, sub, narration, foot=""):
    S.append(dict(kind="card", step="", kicker=kicker, title=t, sub=sub, text=narration, foot=foot))


title("BOOK 2  |  VIDEO COURSE  |  MODULE 17", "Using MODEL 2, step by step", "PAYGo Company Financial and Investment Model, in twelve steps",
      "This tutorial walks you through MODEL 2, the PAYGo Company Financial and Investment Model, in twelve steps, in the order "
      "an analyst should work. Every screen you will see is the real workbook, version 0.8, a development build, with its default inputs. Those inputs describe a fictional "
      "company in a fictional market. They are there to make the mechanics visible, not to describe any real business. "
      "Keep the user manual open beside you. It follows the same twelve steps.",
      foot="Author and ideation: Emmanuel Boujieka Kamga")

S1 = "Step 1 of 12  |  Start here"
scene(S1, "Cover", "B16:J44", [("E35:H35", "Master check"), ("E36:H36", ""), ("E37:H37", "")],
      "Open the workbook, let it recalculate, and read the status panel before anything else.",
      "Open the workbook in Excel 2016 or later and let it recalculate fully. The cover carries a live status panel. "
      "First, the master check. It must read OK before you rely on any output. Below it, the readiness line: three of "
      "twenty three gates are met at default inputs, and the decision reads STOP, because the evidence is incomplete. The "
      "model never rates a company. Then the active case, the illustrative model assumptions in the Base scenario, and the "
      "credit data mode, Proxy, which means the credit figures come from the model's curves. "
      "Before you change anything, save a copy under a new name and keep the original as your reference.")
scene(S1, "Start", "A1:D40", [("A4:D7", "Status"), ("A9:D18", "What to input"), ("A29:D34", "Read before quoting")],
      "One page: what to input, what the model calculates, what the results mean and what an investor should look at.",
      "Next, the Start sheet. It sets out on one page what to input, what the model calculates, what the results mean, and "
      "what an investor should look at, in that order. Every input carries a provenance label: model assumption, company "
      "data, external evidence, calibrated assumption or unverified. Read the third block before you quote any number. "
      "Revenue is not cash. The operational collection rate is not a PAYGo PERFORM KPI. The credit loss figures are "
      "analytical proxies. And the readiness decision measures the evidence file, not the business.")
scene(S1, "Checks", "A1:C54", [("A44:C44", "Master check"), ("A46:C54", "Readiness flags")],
      "Thirty eight integrity tests roll up into the master check. Readiness flags sit apart.",
      "The Checks sheet runs thirty eight integrity tests. The balance sheet balances, cash reconciles every month, the DPD "
      "buckets reconcile to gross receivables, and receivables, the loss allowance, debt and equity roll forward from month "
      "to month. Limits are respected and inputs are valid. Each test returns zero when it passes, and together they drive "
      "the master check. Below them sit seven readiness flags, such as affordability assumptions not yet "
      "reviewed. They are kept outside the master check on purpose. They tell you how mature the analysis is, not whether the "
      "arithmetic is right.")
scene(S1, "Inputs", "A1:E14", [("C5:C5", "Scenario"), ("C6:C7", ""), ("E5:E14", "Provenance")],
      "Blue cells are inputs, each with a provenance label. Set the scenario selector, the first model month and the currency label.",
      "All hard coded assumptions live on a handful of sheets, and the colour code tells you where. Blue font is an input, "
      "the only kind of cell you should change. Black font is a formula. Never overwrite it. On the Inputs sheet, start "
      "with three settings. The first is the scenario selector, where one is Base, two is Downside and three is Severe. "
      "Then come the first model month and the local currency label. The last column gives each input's provenance. At "
      "default inputs every one reads model assumption, because the defaults describe a fictional market.")

S2 = "Step 2 of 12  |  Define the business"
scene(S2, "Products", "A4:G16", [("A6:G11", "Product specification"), ("A13:G16", "Price plan")],
      "Five tiers, labelled by the capacity attribute of the Multi Tier Framework. Replace them with your own catalogue.",
      "The Products sheet holds one column per tier. Tier one is a pico solar kit on a twelve month plan. Tier five is a "
      "three kilowatt peak inverter system on a forty eight month plan. Replace the names, sizes, loads and segments with your "
      "own catalogue. Keep all five columns. If you sell fewer tiers, set the sales mix of the unused tier to zero. The tier "
      "label refers to capacity only, so check it against the product's real specification.")
scene(S2, "Consumer_Risk", "A1:G15", [("A8:G8", "Illustrative incomes"), ("A10:G10", "Payment burden"), ("A13:G13", "Flag")],
      "Affordability is a credit risk. Replace the illustrative incomes with surveyed incomes.",
      "Consumer Risk sets each tier's instalment against the household income of its target segment. The incomes shown are "
      "illustrative placeholders and must be replaced with survey or customer data. With the defaults, three tiers sit above "
      "the model's ten per cent policy threshold for payment burden: Tier 2 at 13.0 per cent, Tier 3 at 13.2 per cent and Tier 4 at 11.3 per "
      "cent. A high burden predicts higher default, so treat these flags as credit warnings, not only as social ones.")

S3 = "Step 3 of 12  |  Market assumptions"
scene(S3, "Inputs", "A9:D14", [("C10:C14", "Macro")],
      "FX, inflation, tax, the price increase on new contracts and FX pass through.",
      "The macro block sets the opening exchange rate, 130 local currency units per dollar, local inflation of six per cent, "
      "a tax rate of thirty per cent, an annual price increase of five per cent on new contracts, and a pass through of fifty "
      "per cent of currency depreciation into new contract prices. Do not set depreciation to zero because the currency has "
      "been stable. A PAYGo company buys hardware and borrows in dollars while it collects in local currency.")
scene(S3, "Scenarios", "A4:E12", [("A6:E10", "Scenario levers")],
      "Downside and Severe move credit, collections, volume, hardware cost and the currency together.",
      "The Scenarios sheet scales five levers. The Downside raises the default hazard by thirty per cent, trims collections "
      "and volume, raises hardware cost and sets depreciation at twelve per cent a year. The Severe case goes further, with a "
      "hazard 1.75 times Base and twenty five per cent depreciation. Real stress moves several variables at once, and so do "
      "these scenarios.")

S4 = "Step 4 of 12  |  Build demand"
scene(S4, "Inputs", "A16:D21", [("C17:C21", "Units by year")],
      "Total units sold for Years 1 to 5 across all tiers.",
      "Enter the total units sold in each of the five years. The defaults run from twelve thousand units in Year 1 to fifty "
      "thousand in Year 5. The model divides each year by twelve, applies the scenario volume multiplier and splits the sales "
      "by tier. Version 0.8 does not model seasonality, so read monthly results as averages.")
scene(S4, "Products", "A4:G23", [("A23:G23", "Sales mix")],
      "The sales mix must total 100 per cent. A check enforces it.",
      "The sales mix sits on Products, and it must total one hundred per cent. A check enforces it. Be careful when you shift "
      "the mix towards Tiers 4 and 5. It raises value sharply, but those tiers usually have the least repayment history "
      "behind them.")

S5 = "Step 5 of 12  |  Build revenue"
scene(S5, "Products", "A12:G39", [("A13:G16", "Inputs"), ("A33:G35", "Derived"), ("A39:G39", "Implied APR")],
      "Cash price, deposit, daily rate and tenor; the model derives the instalment, the premium and the implied APR.",
      "Each price plan has four inputs: cash price, deposit, daily rate and tenor. Take Tier 2. A cash price of 39,000, a "
      "deposit of 4,000 and a daily rate of 77 over 24 months give a monthly instalment of 2,342 and a total contract value "
      "of 60,210. The PAYGo premium over the cash price is 21,210, and the implied annual rate is about fifty per cent. That "
      "rate is the figure a regulator or a journalist will compute, so know it first. Hardware revenue is booked at the cash "
      "price at sale, and the premium is earned as financing income over the tenor.")
scene(S5, "Inputs", "A30:D39", [("C34:C34", "RBF design"), ("C39:C39", "Evidence switch")],
      "Four RBF designs. Ownership linked RBF pays nothing until validated ownership data exist.",
      "Results based financing has four designs: sales based, repayment linked, ownership linked and hybrid. Ownership "
      "linked RBF pays zero by design until validated ownership data have been loaded and this evidence switch is set to "
      "one. The model will not manufacture that outcome from proxy curves.")

S6 = "Step 6 of 12  |  Hardware and capital costs"
scene(S6, "Products", "A17:G46", [("A18:G19", "Cost inputs"), ("A43:G44", "Landed cost and CAC")],
      "Hardware FOB cost in US dollars; landed cost includes freight and duty at the month's exchange rate.",
      "Hardware is entered as the dollar FOB cost per unit. The model adds freight and duty, converts at the exchange rate "
      "of the month and applies the scenario hardware cost lever. For Tier 2, a cost of 150 dollars becomes a landed cost of "
      "23,400 at the opening rate. Installation, warranty and the acquisition cost are set per tier. Do not enter a local "
      "price already converted at today's rate. That would count depreciation twice.")

S7 = "Step 7 of 12  |  Operating costs"
scene(S7, "Inputs", "A23:D28", [("C24:C27", "Operating costs")],
      "Payment fees, servicing per active account, staff and general and administrative costs.",
      "Operating costs follow their drivers. Payment fees are two per cent of cash collected. Customer service and "
      "collections cost 150 per active account per month. Staff and general costs are fixed monthly amounts, indexed to "
      "inflation. Size the central costs for the volume plan. A book of seventy thousand active accounts needs a collections "
      "team, a call centre and a data function.")

S8 = "Step 8 of 12  |  Financing"
scene(S8, "Inputs", "A48:D57", [("C49:C49", "Equity"), ("C50:C54", "USD term loan"), ("C55:C57", "Facility")],
      "Initial equity, a dollar term loan and a local currency receivables facility, with an automatic equity top up.",
      "Four sources fund the plan: initial equity, a dollar term loan revalued every month, a local currency receivables "
      "facility, and an automatic equity top up whenever cash would fall below the minimum. The facility is drawn only to "
      "hold the minimum cash balance, up to the lower of its limit and the borrowing base. The cumulative top up is your "
      "funding requirement. It is equity you must raise, not free money.")
scene(S8, "Credit_Assumptions", "A4:E24", [("C5:C5", "Data mode"), ("C8:C11", "Definitions"), ("C20:C24", "Proxy DPD split")],
      "Default at 180 DPD, staging thresholds, borrowing base eligibility, recovery cost and the proxy DPD distribution.",
      "Credit Assumptions holds the definitions. Default at 180 days past due. Stage 2 from thirty days and Stage 3 from "
      "ninety days for the indicative expected credit loss. Borrowing base eligibility up to thirty days past due. A "
      "recovery cost of fifteen per cent of resale proceeds. The binding constraint on the facility is usually the borrowing "
      "base, not the limit, and it shrinks when credit quality deteriorates.")

S9 = "Step 9 of 12  |  Financial statements"
scene(S9, "Annual", "A5:I28", [("E12:I12", "Total revenue"), ("E17:I17", "ECL at origination"), ("E19:I19", "EBITDA")],
      "Read the revenue mix, credit losses charged at origination, and EBITDA year by year.",
      "The Annual sheet sums the monthly statements by year. Check the revenue mix between hardware, financing income and "
      "other revenue. Expected credit losses are charged when each contract is originated, so a growing book carries the "
      "full lifetime loss of its newest cohorts. In the default Base case, EBITDA turns positive in month 21.")
scene(S9, "Annual", "A30:I62", [("E46:I46", "Balance check"), ("E55:I55", "Operating cash flow"), ("E60:I60", "Cash before top up")],
      "Profit arrives before cash. The balance check must read zero; the cash flow shows the true funding gap.",
      "Now the balance sheet and cash flow. The balance check must read zero in every period. Operating cash flow stays "
      "negative while the receivables book grows. In the default case it stays positive only from month 51, thirty months "
      "after EBITDA. A PAYGo company can report a profit and still run out of cash. The cash flow statement and the funding "
      "requirement are the figures to trust.")

S10 = "Step 10 of 12  |  Scenarios"
scene(S10, "Sensitivity", "A5:I24", [("A6:I8", "Scenarios"), ("A13:I14", "Currency and pricing"), ("A23:I24", "Live row")],
      "Fifteen dated cases computed at default inputs, and a live row for the active case. Currency and pricing move value more than volume.",
      "Switch the selector between Base, Downside and Severe and read the investment summary each time. The Sensitivity "
      "sheet holds a static table of fifteen cases, dated and computed at default inputs, and below it a live row that "
      "follows the active case. The Base investor IRR is 46.4 per cent. In the Downside the IRR is "
      "minus 22.9 per cent, and the Severe case is a total loss. Look at the currency rows. Twenty per cent depreciation a "
      "year takes the Base IRR to minus sixteen per cent, and freezing prices on new contracts cuts it to 7.9 per cent. Remember to "
      "reset the selector to Base before you save.")

S11 = "Step 11 of 12  |  Lender case"
scene(S11, "Credit_Portfolio", "A4:L31", [("A10:L16", "DPD buckets"), ("A20:L20", "Collection ratio"), ("A25:L28", "Borrowing base")],
      "Gross receivables by DPD bucket, the collection ratio, indicative ECL and the borrowing base with its headroom.",
      "Credit Portfolio consolidates the five tiers month by month: gross receivables by DPD bucket, the collection ratio, "
      "PD and LGD proxies, the indicative stage based ECL, and the borrowing base with its headroom against the facility. The "
      "buckets reconcile exactly to gross receivables. This is the view a lender reads first.")
scene(S11, "Covenants", "A4:L26", [("A8:L9", "Collection covenant"), ("A26:L26", "Any breach")],
      "Each covenant is tested monthly. Headroom matters as much as compliance.",
      "Covenants tests each threshold every month and flags breaches. In the default Base case the lowest trailing three "
      "month collection rate is 72.9 per cent against a minimum of seventy, and no month breaches. Look at the headroom, not "
      "only at the pass or fail flag. The annual DSCR sits on the KPIs sheet, and it is a poor test for a growing book.")
scene(S11, "Credit_Input", "A6:L25", [("A7:L7", "One block per tier"), ("D8:I25", "Month end DPD buckets")],
      "Paste the company's own history, then switch the credit data mode to Actual. Shown here: the fictional SolaraPay case.",
      "Now load the company's own data. Credit Input takes one block per tier and up to sixty months: month end balances and "
      "DPD buckets, and monthly flows such as originations, collections and write offs. The screen shows the SolaraPay case "
      "workbook, whose history is synthetic teaching data. The buckets must add up to gross receivables. Then set the credit "
      "data mode to Actual. Reporting switches to the company's history, while projections stay on the curves.", book="case")
scene(S11, "Vintage_Dashboard", "A1:I20", [("A9:I12", "Observed cohorts at M12"), ("A17:I18", "Portfolio curve")],
      "Compare observed cohorts with the proxy curves, then recalibrate the hazards and collection rates on Products.",
      "Vintage Dashboard sets the observed cohorts against the plan curves. In the SolaraPay case, every tier with history "
      "repays below plan at month 12. When the curves diverge, recalibrate the default hazard and collection rates on the "
      "Products sheet. Lenders lend against data, and twelve or more months of clean cohort history is the fastest route to "
      "better terms.", book="case")

S12 = "Step 12 of 12  |  Investment memo"
scene(S12, "Valuation", "A22:D40", [("C27:C28", "DCF enterprise value"), ("C36:C36", "Exit equity"), ("C39:C40", "IRR and multiple")],
      "DCF on normalised free cash flow, exit value, and investor returns in US dollars.",
      "Valuation holds three views. The DCF of free cash flow gives an enterprise value of about 15.6 million dollars, with "
      "a terminal value larger than the whole value, which is normal for a growing PAYGo book. The exit value at six times "
      "EBITDA gives an equity value of about 80.6 million dollars at the end of Year 5. The investor's stake of one third then "
      "returns an IRR of 46.4 per cent and 6.7 times the money, in dollars. Present the DCF and the exit value side by side "
      "and explain the gap.")
scene(S12, "Unit_Economics", "A4:G24", [("A11:G11", "Expected loss"), ("A20:G23", "Contribution, LTV to CAC, payback, unit IRR")],
      "Per tier: expected loss, contribution, LTV to CAC, cash payback and unit IRR.",
      "Unit Economics answers whether each sale creates value. For Tier 2 at default inputs, the expected loss is about 35.6 "
      "per cent of scheduled instalments, LTV to CAC is 4.8 times, and the cash payback is fifteen months. Read the ratio with "
      "the payback and the unit IRR. A strong ratio on a product with no repayment history is a hypothesis, not a result.")
scene(S12, "Calibration", "A5:F12", [("A6:F7", "References suspended"), ("A10:F10", "Operational collection rate")],
      "Diagnostics use verified references only. Suspended or conflicting references are shown, never used as targets.",
      "Calibration turns benchmarks into questions, and it compares the model only with references whose source is "
      "verified. At this edition, every reference on the sheet is suspended or absent. The M-KOPA group figures conflict "
      "between sources, so that comparison is withdrawn until the group's consolidated accounts are read. The ESMAP sector "
      "collection rate is pending its primary document, and it is context for the model's operational collection rate, "
      "not a PERFORM repayment rate. The sheet asks you to justify the cost and credit assumptions on the company's own "
      "data. It never changes an input on its own.")
scene(S12, "Investment_Readiness", "A4:G36", [("B5:G5", "Readiness banner"), ("A31:D36", "Decision rule")],
      "Twenty three gates, thirteen critical. The decision rule reads evidence only: STOP, CONDITIONAL GO or GO.",
      "Finally, Investment Readiness. Twenty three gates, automatic where the model can test them and manual where they need "
      "outside evidence, such as legal review or the auditor's view of the ECL approach. A manual gate counts only when the "
      "sheet records where the evidence is held and who signed it off. Thirteen gates are critical, and the decision rule "
      "uses the evidence and nothing else. It reads STOP when a test fails, GO only when all twenty three gates are met, and "
      "CONDITIONAL GO when every critical gate is met. Otherwise it reads STOP, because the evidence is incomplete. At default "
      "inputs three gates are met and the decision is STOP, with ten of the thirteen critical gates open. A STOP on "
      "incomplete evidence is not a verdict on the business, and a GO is not an investment recommendation. Every gate not "
      "yet met should become a condition precedent, a covenant or an accepted risk in the investment memo.")
scene(S12, "Investment_Summary", "A4:G35", [("B9:F19", "Trajectory"), ("B22:B27", "Funding"), ("B30:B35", "Returns")],
      "The one page summary for the investment committee, live for the active scenario.",
      "The Investment Summary brings it together on one page for the active scenario: the operating trajectory, the funding "
      "requirement, valuation and returns, the lender view and unit economics by tier. Build the memo from this page and the "
      "sheets behind it, using Template T01, and check every figure you quote against its source sheet.")
scene(S12, "Dashboard", "A5:H50", [("A22:H23", "Collection rate and PERFORM"), ("A29:H29", "Cash conversion"),
                                     ("A47:H48", "FX: USD debt share and FX effect"), ("A49:H50", "Readiness")],
      "Thirty nine labelled metrics by year, rounded for reading, each with its unit and its source sheet.",
      "Behind the summary sits the Dashboard: a table of thirty nine labelled metrics by year, rounded for reading, each "
      "with its unit and its source sheet. Single values, such as returns, peaks, timing and readiness, sit under Year 1. "
      "Three readings teach the most. First, revenue is not cash. Cash conversion, operating cash flow over EBITDA, reads "
      "not applicable in Years 1 and 2, while EBITDA is negative. It is then minus 1.32 times in Year 3, minus 0.08 times "
      "in Year 4 and 0.25 times in Year 5, because the growing receivables book absorbs the cash. Second, the operational "
      "collection rate falls from 84.5 per cent in Year 1 to 73.3 per cent in Year 5. It is labelled not a PERFORM KPI, and "
      "the PERFORM repayment line below it reads not provided, because only company results can fill it. Third, the net FX "
      "transaction effect on costs and RBF, before price pass through, is a cost that grows from about twenty five million "
      "local currency units in Year 1 to about nine hundred and twenty eight million in Year 5. The last lines repeat the "
      "readiness result: three of twenty three gates met, and a decision of STOP, on incomplete evidence.")

title("BOOK 2  |  VIDEO COURSE", "Twelve steps, one discipline", "Load the company's data before you trust the projections",
      "That completes the twelve steps. Three habits matter most. Never use an output while the master check reads error. "
      "Load the company's own history before you trust any projection. And read the Downside as carefully as the Base. The "
      "user manual, the case study, the templates and the decision tools take each step further. Thank you for watching.",
      foot="Africa Energy Finance  |  Business & Financial Models  |  Decision support material; not investment advice.")


# ------------------------------------------------------------------ build
def build():
    WORK.mkdir(parents=True, exist_ok=True)
    for f in WORK.iterdir():  # keep narration (wav and its text key) so unchanged scenes are not re-voiced
        if f.is_file() and f.suffix not in (".wav", ".txt"):
            f.unlink()
    OUTD.mkdir(parents=True, exist_ok=True)
    books = {k: Book(k) for k in ("model", "case")}
    focus = []
    with sync_playwright() as p:
        import glob
        exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
        br = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(S):
            if s["kind"] == "card":
                page, fxy = card(s["kicker"], s["title"], s["sub"], s.get("foot", "")), (W / 2, H / 2)
            else:
                page, fxy = render(books[s["book"]], s["sheet"], s["rng"], s["hl"], s["caption"], s["step"], s.get("select"))
            pg.set_content(page, wait_until="load")
            pg.screenshot(path=str(WORK / f"s{i:02d}.png"))
            focus.append(fxy)
        br.close()
    print("frames rendered", len(S))
    # narration
    durs = []
    for i, s in enumerate(S):
        wav, txt = WORK / f"s{i:02d}.wav", WORK / f"s{i:02d}.txt"
        if wav.exists() and txt.exists() and txt.read_text() == A.speakable(s["text"]):
            d = A.duration(wav)  # narration unchanged since the last build
        else:
            d = A.tts(s["text"], wav, lead=0.6, tail=0.9)
            txt.write_text(A.speakable(s["text"]))
        durs.append(d)
    print("narration seconds", round(sum(durs)))
    # clips: a gentle push towards the focus point over the first three seconds, then a still hold that keeps text sharp
    fps = 25
    for i, s in enumerate(S):
        d = durs[i]
        n = int(d * fps)
        fx, fy = focus[i]
        zmax = 1.0  # still frames: every marker and edge column stays in view, and text stays sharp
        ramp = 3 * fps
        zexpr = f"1+({zmax}-1)*(3*pow(min(on/{ramp},1),2)-2*pow(min(on/{ramp},1),3))"
        vf = (f"scale={W * 2}:{H * 2}:flags=lanczos,zoompan=z='{zexpr}':x='({fx * 2})-({fx * 2})/zoom':y='({fy * 2})-({fy * 2})/zoom':d={n}:s={W}x{H}:fps={fps},"
              f"fade=t=in:st=0:d=0.4,fade=t=out:st={d - 0.4:.2f}:d=0.4,format=yuv420p")
        A.run(["ffmpeg", "-y", "-loop", "1", "-i", str(WORK / f"s{i:02d}.png"), "-i", str(WORK / f"s{i:02d}.wav"),
               "-vf", vf, "-t", f"{d:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-tune", "stillimage", "-x264-params", "keyint=250",
               "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-af", f"afade=t=in:st=0:d=0.2,afade=t=out:st={d - 0.3:.2f}:d=0.3",
               "-shortest", str(WORK / f"c{i:02d}.mp4")])
    lst = WORK / "list.txt"
    lst.write_text("".join(f"file '{WORK / f'c{i:02d}.mp4'}'\n" for i in range(len(S))))
    A.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(WORK / "joined.mp4")])
    # subtitles, chapters, metadata
    srt, t, k = [], 0.0, 1
    chapters, last_step, ch_start = [], None, 0.0
    for i, s in enumerate(S):
        for a, b, line in A.srt_blocks(s["text"], t, durs[i], lead=0.6, tail=0.9):
            srt.append(f"{k}\n{A.srt_time(a)} --> {A.srt_time(b)}\n{line}\n")
            k += 1
        step = s["step"] or (s.get("title") or "")
        if step != last_step:
            if last_step is not None:
                chapters.append((ch_start, t, last_step))
            last_step, ch_start = step, t
        t += durs[i]
    chapters.append((ch_start, t, last_step))
    (WORK / "subs.srt").write_text("\n".join(srt))
    meta = [";FFMETADATA1", "title=Using MODEL 2, the PAYGo Company Financial and Investment Model: a step by step guide", f"artist={A.AUTHOR}",
            "album=Africa Energy Finance, Book 2 video course", "comment=Module 17. Decision support material; not investment advice.",
            f"date={date.today().year}"]
    for a, b, name in chapters:
        meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(a * 1000)}", f"END={int(b * 1000)}", f"title={name}"]
    (WORK / "meta.txt").write_text("\n".join(meta) + "\n")
    out = OUTD / "AEF_V2_Module17_Model_Walkthrough.mp4"
    A.run(["ffmpeg", "-y", "-i", str(WORK / "joined.mp4"), "-i", str(WORK / "subs.srt"), "-i", str(WORK / "meta.txt"),
           "-map", "0:v", "-map", "0:a", "-map", "1:0", "-map_metadata", "2", "-map_chapters", "2",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:s", "mov_text",
           "-metadata:s:s:0", "language=eng", "-metadata:s:a:0", "language=eng", "-fflags", "+bitexact", "-flags:v", "+bitexact",
           "-flags:a", "+bitexact", "-movflags", "+faststart", str(out)])
    shutil.copy(WORK / "subs.srt", OUTD / "AEF_V2_Module17_Model_Walkthrough.srt")
    # module 17 script, generated from the same scenes
    md = ["# Module 17. Using MODEL 2, step by step", "",
          f"Duration: about {round(t / 60)} minutes. Book: Chapters 1 to 16. Model: MODEL 2, version 0.8 (development build), file AEF_SHS_PAYGo_Model_v0.8-dev.xlsx. User manual: Steps 1 to 12.", "",
          "## Learning objectives", "1. Work through the model in the order an analyst should.",
          "2. Know which sheet holds each input and which sheet answers each question.",
          "3. Read the integrity checks, the readiness gates and the investment summary correctly.", ""]
    for i, s in enumerate(S, 1):
        head = s["title"] if s["kind"] == "card" else f"{s['step'].split('|')[1].strip()}: {s['sheet']}"
        md += [f"## Scene {i}. {head}", f"On screen: {s.get('caption') or s.get('sub')}" + (f" Sheet {s['sheet']}, range {s['rng']}." if s["kind"] == "sheet" else ""), "", s["text"], ""]
    (OUTD / "scripts").mkdir(exist_ok=True)
    (OUTD / "scripts" / "module_17.md").write_text("\n".join(md))
    json.dump([dict(i=i, step=s["step"], sheet=s.get("sheet"), seconds=round(durs[i], 1)) for i, s in enumerate(S)],
              open(WORK / "timeline.json", "w"), indent=1)
    print(out, round(A.duration(out) / 60, 1), "minutes")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        books = {k: Book(k) for k in ("model", "case")}
        WORK.mkdir(parents=True, exist_ok=True)
        import glob
        with sync_playwright() as p:
            exe = (glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome") or [None])[0]
            br = p.chromium.launch(executable_path=exe)
            pg = br.new_page(viewport={"width": W, "height": H})
            for i, s in enumerate(S):
                page = card(s["kicker"], s["title"], s["sub"], s.get("foot", "")) if s["kind"] == "card" else \
                    render(books[s["book"]], s["sheet"], s["rng"], s["hl"], s["caption"], s["step"], s.get("select"))[0]
                pg.set_content(page, wait_until="load")
                pg.screenshot(path=str(WORK / f"s{i:02d}.png"))
            br.close()
        print("frames", len(S))
    else:
        build()
