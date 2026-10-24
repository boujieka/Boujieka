"""Fill a user-supplied workbook in the CrossBoundary Access Open Source Model 1.0
format with the assumptions of a scenario version and the pasted values found
by the engine.

The workbook is edited at the XML level: only the input cells and the four
macro-pasted cells are rewritten, so every formula, chart, style and the VBA
project of the original are kept byte for byte. Excel recalculates the file
when it is opened (``fullCalcOnLoad``). No macro is run here, and the template
is never stored: it is uploaded with the request and returned filled in.

The fill refuses (``TemplateMismatch``) rather than guesses when the scenario
cannot be written without changing formulas, e.g. a monetary input typed in USD
in the template but contracted in local currency in the scenario.
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import io
import posixpath
import re
import zipfile
from xml.sax.saxutils import escape

import openpyxl

from ..engine import assumptions as A
from ..engine.loader import CURRENCY_ROWS, load_assumptions

PASTED_CELLS = {"funding": "Inputs!G292", "dscr_limit": "Inputs!G300", "refi_limit": "Inputs!G344",
                "dsra_initial": "Inputs!E372"}
EXCEL_EPOCH = dt.date(1899, 12, 30)


class TemplateMismatch(ValueError):
    def __init__(self, problems: list[str]):
        super().__init__("; ".join(problems))
        self.problems = problems


# ------------------------------------------------------------------ cell values
def _cells_for(a: A.Assumptions, template: A.Assumptions) -> tuple[dict[str, object], list[str]]:
    """Map 'Sheet!A1' -> value to write, and list the problems that block the fill."""
    out: dict[str, object] = {}
    problems: list[str] = []
    for g in dataclasses.fields(A.Assumptions):
        if g.name in ("lots", "pasted"):
            continue
        cls = getattr(A, g.type) if isinstance(g.type, str) else g.type
        obj, tobj = getattr(a, g.name), getattr(template, g.name)
        for f in dataclasses.fields(cls):
            cell, val = f.metadata["cell"], getattr(obj, f.name)
            if g.name == "currency" and f.name in CURRENCY_ROWS:
                _money(out, problems, f.name, CURRENCY_ROWS[f.name], val, getattr(tobj, f.name))
                continue
            if f.default is None and val is None:
                continue
            if ":" in cell:
                sheet, rng = cell.split("!")
                refs = [f"{sheet}!{c.coordinate}" for row in openpyxl.Workbook().active[rng] for c in row]
                if len(refs) != len(val):
                    problems.append(f"{g.name}.{f.name}: {len(val)} values for {len(refs)} cells ({cell})")
                    continue
                out.update(zip(refs, val))
            else:
                out[cell] = val
    if len(a.lots) > len(A.LOT_COLUMNS):
        problems.append(f"{len(a.lots)} lots: the workbook format has {len(A.LOT_COLUMNS)} lot columns (E to J)")
    for i, col in enumerate(A.LOT_COLUMNS):
        lot = a.lots[i] if i < len(a.lots) else None
        tlot = template.lots[i]
        for name, row in A.LOT_ROWS.items():
            ref = f"Portfolio!{col}{row}"
            if lot is None:
                if name == "included":
                    out[ref] = 0          # unused column: switched off, other cells left as in the template
                continue
            val = getattr(lot, name)
            if val is None:
                if getattr(tlot, name) is not None:
                    problems.append(f"lots.{i}.{name}: inherits the portfolio value, but {ref} holds a typed "
                                    "value in the template (restore its formula first)")
                continue
            out[ref] = val
    return out, problems


def _money(out, problems, name, row, m: A.MoneyInput, t: A.MoneyInput) -> None:
    if m.basis != t.basis or m.vat != t.vat:
        problems.append(f"currency.{name} (Currency row {row}): scenario basis {m.basis}/{m.vat}, "
                        f"template {t.basis}/{t.vat}; change it in the template first")
        return
    if m.basis == "lcy_contracted":
        out[f"Currency!K{row}"] = m.value
    else:
        out[f"Currency!H{row}"] = m.value
        if m.basis == "usd_and_lcy":
            out[f"Currency!I{row}"] = m.lcy_value


# ------------------------------------------------------------------ XML editing
def _sheet_paths(z: zipfile.ZipFile) -> dict[str, str]:
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    targets = {m.group(1): m.group(2) for m in re.finditer(r'<Relationship\b[^>]*?Id="([^"]+)"[^>]*?Target="([^"]+)"', rels)}
    targets.update({m.group(2): m.group(1) for m in re.finditer(r'<Relationship\b[^>]*?Target="([^"]+)"[^>]*?Id="([^"]+)"', rels)})
    out = {}
    for m in re.finditer(r"<sheet\b[^>]*>", wb):
        tag = m.group(0)
        name = re.search(r'name="([^"]+)"', tag).group(1)
        rid = re.search(r'r:id="([^"]+)"', tag).group(1)
        target = targets[rid]
        out[_unescape(name)] = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
    return out


def _unescape(s: str) -> str:
    return s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&apos;", "'")


def _cell_xml(attrs: str, value) -> str:
    attrs = re.sub(r'\s+t="[^"]*"', "", attrs)
    if value is None:
        return f"<c{attrs}/>"
    if isinstance(value, bool):
        return f'<c{attrs} t="b"><v>{int(value)}</v></c>'
    if isinstance(value, dt.datetime):
        value = value.date()
    if isinstance(value, dt.date):
        return f"<c{attrs}><v>{(value - EXCEL_EPOCH).days}</v></c>"
    if isinstance(value, (int, float)):
        return f"<c{attrs}><v>{repr(float(value)) if isinstance(value, float) else value}</v></c>"
    return f'<c{attrs} t="inlineStr"><is><t xml:space="preserve">{escape(str(value))}</t></is></c>'


def _patch_sheet(xml: str, cells: dict[str, object], sheet: str, problems: list[str]) -> str:
    for addr, value in cells.items():
        m = re.search(r'<c\b((?:(?!/?>)[^>])*?\br="%s"(?:(?!/?>)[^>])*)(/?)>' % addr, xml)
        if m is None:
            problems.append(f"{sheet}!{addr}: cell not found in the template")
            continue
        start, attrs = m.start(), m.group(1)
        end = m.end() if m.group(2) else xml.index("</c>", m.end()) + 4
        inner = xml[m.end():end]
        if re.search(r'<f\b[^>]*\bt="shared"[^>]*\bref="', inner):
            problems.append(f"{sheet}!{addr}: holds the master of a shared formula; type the value in Excel instead")
            continue
        xml = xml[:start] + _cell_xml(attrs, value) + xml[end:]
    return xml


def fill_template(template: bytes, a: A.Assumptions, pasted: dict[str, float | None]) -> bytes:
    """Return the template with the scenario written in; raise TemplateMismatch if impossible."""
    with zipfile.ZipFile(io.BytesIO(template)) as z:
        tmp = io.BytesIO(template)
        try:
            tpl = load_assumptions(tmp)
        except Exception as exc:  # noqa: BLE001
            raise TemplateMismatch([f"not a CrossBoundary-format workbook: {type(exc).__name__}: {exc}"]) from exc
        cells, problems = _cells_for(a, tpl)
        for key, ref in PASTED_CELLS.items():
            if pasted.get(key) is not None:
                cells[ref] = pasted[key]
        by_sheet: dict[str, dict[str, object]] = {}
        for ref, v in cells.items():
            sh, addr = ref.split("!")
            by_sheet.setdefault(sh, {})[addr] = v
        paths = _sheet_paths(z)
        patched = {}
        for sh, cs in by_sheet.items():
            if sh not in paths:
                problems.append(f"sheet {sh} not found")
                continue
            patched[paths[sh]] = _patch_sheet(z.read(paths[sh]).decode("utf-8"), cs, sh, problems)
        if problems:
            raise TemplateMismatch(problems)
        wb = z.read("xl/workbook.xml").decode("utf-8")
        if "<calcPr" in wb:
            wb = re.sub(r"<calcPr\b([^>]*?)/?>", lambda m: "<calcPr" + re.sub(r'\s+fullCalcOnLoad="[^"]*"', "", m.group(1))
                        + ' fullCalcOnLoad="1"/>', wb, count=1)
        else:
            wb = wb.replace("</workbook>", '<calcPr fullCalcOnLoad="1"/></workbook>')
        patched["xl/workbook.xml"] = wb
        # the calculation chain lists formula cells; drop it so Excel rebuilds it
        drop = {"xl/calcChain.xml"}
        patched["xl/_rels/workbook.xml.rels"] = re.sub(
            r'<Relationship\b[^>]*calcChain[^>]*/>', "", z.read("xl/_rels/workbook.xml.rels").decode("utf-8"))
        patched["[Content_Types].xml"] = re.sub(
            r'<Override\b[^>]*calcChain[^>]*/>', "", z.read("[Content_Types].xml").decode("utf-8"))
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as w:
            for info in z.infolist():
                if info.filename in drop:
                    continue
                data = patched[info.filename].encode("utf-8") if info.filename in patched else z.read(info.filename)
                w.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)
        return out.getvalue()
