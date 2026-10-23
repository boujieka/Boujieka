"""Static inventory of the CrossBoundary workbook (Phase 0, steps A-C).

Reads formulas and cached values with openpyxl; never calculates and never runs
VBA. Produces:
  docs/variable_dictionary.csv   one line per input cell, pasted value,
                                 calculated row and key output
  work/inventory.json            statistics used to write the audit documents
  work/row_graph.json            row-level dependency graph (sheet!row -> sheet!row)

Usage: python tools/phase0/inventory.py WORKBOOK.xlsm OUT_ROOT
"""
import collections
import csv
import datetime
import json
import os
import re
import sys

import networkx as nx
import openpyxl
from openpyxl.formula.tokenizer import Token, Tokenizer
from openpyxl.formula.translate import Translator
from openpyxl.utils import column_index_from_string as CI
from openpyxl.utils import get_column_letter as L
from openpyxl.utils import range_boundaries

FIRST_T, LAST_T = 10, 78  # timeline columns J..BZ on Model/Debt/FinStat/Graph sheet
TIME_SHEETS = {"Model", "Debt", "FinStat", "Graph sheet"}
INPUT_SHEETS = {"Currency", "Portfolio", "Inputs", "Names"}
# Cells the VBA macros overwrite with pasted values (circularity breaks).
PASTED = {"Inputs!G292": "Funding_paste (Debt_Sizing)", "Inputs!G300": "DSCR_paste (Debt_Sizing)",
          "Inputs!G344": "Refi_Paste (Refi_Debt_Sizing)", "Inputs!E372": "DSRA_Paste (DSRA_resize_3)"}
OFFSET = re.compile(r"(\$?[A-Z]{1,3}\$?\d+:)?OFFSET\((\$?[A-Z]{1,3}\$?\d+),([^,()]*),([^,()]*)(?:,([^,()]*),([^,()]*))?\)")
EPOCH = datetime.datetime(1899, 12, 30)


def ftext(v):
    return "=" + str(v.text) if hasattr(v, "text") else v


def is_formula(v):
    return isinstance(v, str) and v.startswith("=")


class Workbook:
    def __init__(self, path):
        self.wb = openpyxl.load_workbook(path)
        self.wv = openpyxl.load_workbook(path, data_only=True)
        self.names = {n: d.attr_text for n, d in self.wb.defined_names.items()}
        self.names_l = {n.lower(): n for n in self.names}
        self.maxc = {ws.title: ws.max_column for ws in self.wb.worksheets}
        self.maxr = {ws.title: ws.max_row for ws in self.wb.worksheets}
        self.funcs = collections.Counter()
        self.offset_cells = []

    # -- references -------------------------------------------------------
    def expand(self, sh, rng):
        c1, r1, c2, r2 = range_boundaries(rng)
        c1, r1 = c1 or 1, r1 or 1
        c2, r2 = c2 or self.maxc[sh], r2 or self.maxr[sh]
        return [(sh, r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]

    def split(self, ref, cur):
        ref = ref.replace("$", "")
        if "!" in ref:
            sh, rng = ref.rsplit("!", 1)
            return sh.strip("'"), rng
        return cur, ref

    def rewrite_offset(self, formula, cur):
        """Replace each OFFSET by the widest range it can reach: look-back
        windows (negative width) span the elapsed timeline up to the base
        column; look-forward windows span the base column to the last column."""
        def rep(m):
            pre, base, _ro, _co, h, w = m.groups()
            bc, br = re.match(r"\$?([A-Z]+)\$?(\d+)", base).groups()
            br, bci = int(br), CI(bc)
            height = int(h) if h and h.strip().isdigit() else 1
            if (w or "").strip().startswith("-"):
                c1, c2 = min(FIRST_T, bci), bci
            else:
                c1, c2 = bci, self.maxc[cur]
            if pre:
                c1 = min(c1, CI(re.match(r"\$?([A-Z]+)", pre).group(1)))
            return f"{L(c1)}{br}:{L(c2)}{br + height - 1}"
        new = OFFSET.sub(rep, formula)
        if "OFFSET(" in new.upper():
            raise ValueError("unhandled OFFSET form: " + formula)
        return new

    def refs(self, formula, cur, depth=0):
        if "OFFSET(" in formula.upper():
            for m in OFFSET.finditer(formula):
                self.funcs["OFFSET"] += 1
            formula = self.rewrite_offset(formula, cur)
        out = []
        for t in Tokenizer(formula).items:
            if t.type == Token.FUNC and t.subtype == Token.OPEN:
                self.funcs[t.value[:-1].upper()] += 1
            if t.type == Token.OPERAND and t.subtype == Token.RANGE:
                key = t.value.replace("$", "")
                if key.lower() in self.names_l and depth < 3:
                    txt = self.names[self.names_l[key.lower()]]
                    if re.match(r"^'?[^!]+'?!\$?[A-Z]+\$?\d+(:\$?[A-Z]+\$?\d+)?$", txt):
                        out += self.expand(*self.split(txt, cur))
                    else:  # a named formula (Baseline_consumption)
                        out += self.refs("=" + txt, cur, depth + 1)
                    continue
                out += self.expand(*self.split(t.value, cur))
        return out

    # -- graph --------------------------------------------------------------
    def graph(self):
        G = nx.DiGraph()
        for ws in self.wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    v = ftext(c.value)
                    if is_formula(v):
                        node = (ws.title, c.row, c.column)
                        G.add_node(node, formula=True)
                        if "OFFSET(" in v.upper():
                            self.offset_cells.append(node)
                        for r in self.refs(v, ws.title):
                            G.add_edge(r, node)
        return G

    # -- labelling ----------------------------------------------------------
    def label(self, sh, r):
        ws = self.wb[sh]
        for c in (3, 2, 4):
            v = ftext(ws.cell(r, c).value)
            if is_formula(v):
                v = self.wv[sh].cell(r, c).value
            if isinstance(v, str) and v.strip():
                return v.strip()
        return ""

    def unit(self, sh, r):
        v = ftext(self.wb[sh].cell(r, 4).value)
        if is_formula(v):
            v = self.wv[sh].cell(r, 4).value
        return v.strip() if isinstance(v, str) else ""

    def sections(self, sh):
        """Section header for each row: the closest row above whose only content
        is a text label in column C (the workbook's Header styles)."""
        ws = self.wb[sh]
        cur, out = "", {}
        for r in range(1, ws.max_row + 1):
            vals = [ws.cell(r, c).value for c in range(1, min(ws.max_column, 80) + 1)]
            nonempty = [(i, v) for i, v in enumerate(vals, 1) if v not in (None, "")]
            if len(nonempty) == 1 and nonempty[0][0] == 3 and isinstance(nonempty[0][1], str) \
                    and not nonempty[0][1].startswith("="):
                cur = nonempty[0][1].strip()
            out[r] = cur
        return out


def style_name(c):
    """Named cell style (the workbook's legend: Assumption, Technical_Input, ...)."""
    try:
        return c.style
    except IndexError:  # style index missing from the named-style table
        return ""


def value_repr(v):
    if isinstance(v, datetime.datetime):
        return v.date().isoformat()
    if isinstance(v, float):
        return repr(round(v, 10))
    return "" if v is None else str(v)


def validations(wb):
    out = {}
    for ws in wb.worksheets:
        for dv in ws.data_validations.dataValidation:
            for rng in str(dv.sqref).split():
                for (_sh, r, c) in [(ws.title, r, c) for r in range(range_boundaries(rng)[1], range_boundaries(rng)[3] + 1)
                                    for c in range(range_boundaries(rng)[0], range_boundaries(rng)[2] + 1)]:
                    out[f"{ws.title}!{L(c)}{r}"] = dv.formula1
    return out


def main():
    src, root = sys.argv[1:3]
    os.makedirs(os.path.join(root, "work"), exist_ok=True)
    W = Workbook(src)
    G = W.graph()
    dv = validations(W.wb)
    named_cell = {}
    for n, t in W.names.items():
        m = re.match(r"^'?([^!']+)'?!\$?([A-Z]+)\$?(\d+)$", t)
        if m:
            named_cell.setdefault(f"{m.group(1)}!{m.group(2)}{m.group(3)}", []).append(n)

    # cycles: static SCCs, then the subset that only exists through row-total cells
    sccs = [sorted(s) for s in nx.strongly_connected_components(G) if len(s) > 1]
    cond = [(u, v) for u, v in G.edges() if v in set(W.offset_cells) and u[2] == FIRST_T - 1
            and v[2] == FIRST_T and W.wb[u[0]].cell(u[1], u[2]).value is not None]
    H = G.copy()
    H.remove_edges_from(cond)
    acyclic_without_cond = nx.is_directed_acyclic_graph(H)

    rows = []
    # 1) constants that feed at least one formula = inputs
    for ws in W.wb.worksheets:
        secs = W.sections(ws.title)
        for row in ws.iter_rows():
            for c in row:
                v = ftext(c.value)
                if v is None or is_formula(v):
                    continue
                node = (ws.title, c.row, c.column)
                ref = f"{ws.title}!{c.coordinate}"
                if node not in G or (G.out_degree(node) == 0 and ref not in PASTED):
                    continue
                # text constants are labels/units picked up by label formulas, except
                # option values typed in the input sheets (e.g. "Gearing", "Fixed")
                if isinstance(v, str) and not (ws.title in INPUT_SHEETS and c.column >= 5):
                    continue
                users = {s for (s, _r, _c) in G.successors(node)}
                if ref in PASTED:
                    kind = "pasted_value"
                elif ws.title in TIME_SHEETS and c.column >= FIRST_T:
                    kind = "hardcode_in_calculation"
                elif ref in dv:
                    kind = "switch"
                elif style_name(c) in ("Technical_Input",):
                    kind = "technical_input"
                elif ws.title in INPUT_SHEETS:
                    kind = "input"
                else:
                    kind = "hardcode_in_calculation"
                rows.append({
                    "id": ref, "sheet": ws.title, "cell": c.coordinate,
                    "named_range": ";".join(named_cell.get(ref, [])),
                    "section": secs.get(c.row, ""), "label": W.label(ws.title, c.row),
                    "unit": W.unit(ws.title, c.row), "kind": kind,
                    "cell_style": style_name(c), "value_published": value_repr(v),
                    "allowed_values": dv.get(ref, ""), "used_by_cells": G.out_degree(node),
                    "used_by_sheets": ";".join(sorted(users)), "notes": PASTED.get(ref, ""),
                })
    # 2) calculated rows on timeline sheets, and calculated single cells elsewhere
    for ws in W.wb.worksheets:
        secs = W.sections(ws.title)
        by_row = collections.defaultdict(list)
        for row in ws.iter_rows():
            for c in row:
                v = ftext(c.value)
                if is_formula(v):
                    by_row[c.row].append((c, v))
        for r, cells in sorted(by_row.items()):
            if ws.title in TIME_SHEETS:
                tl = [(c, v) for c, v in cells if c.column >= FIRST_T]
                pats = collections.OrderedDict()
                for c, v in tl:
                    try:
                        base = Translator(v, origin=c.coordinate).translate_formula(f"{L(FIRST_T)}{r}")
                    except Exception:
                        base = v
                    pats.setdefault(base, 0)
                    pats[base] += 1
                first = next(iter(pats)) if pats else (cells[0][1] if cells else "")
                users = {s for c, _ in cells for (s, _r, _c) in G.successors((ws.title, r, c.column))}
                rows.append({
                    "id": f"{ws.title}!{r}", "sheet": ws.title, "cell": f"row {r}",
                    "named_range": "", "section": secs.get(r, ""), "label": W.label(ws.title, r),
                    "unit": W.unit(ws.title, r), "kind": "calculated_row",
                    "cell_style": style_name(cells[0][0]), "value_published": "",
                    "allowed_values": "", "used_by_cells": sum(G.out_degree((ws.title, r, c.column)) for c, _ in cells),
                    "used_by_sheets": ";".join(sorted(users)),
                    "notes": (f"{len(tl)} timeline cells; {len(pats)} distinct formula pattern(s); "
                              f"pattern in J: {first[:180]}") if tl else f"summary cells only: {cells[0][1][:180]}",
                })
            else:
                for c, v in cells:
                    ref = f"{ws.title}!{c.coordinate}"
                    kind = "output" if ws.title == "Dashboard" else "calculated_cell"
                    rows.append({
                        "id": ref, "sheet": ws.title, "cell": c.coordinate,
                        "named_range": ";".join(named_cell.get(ref, [])),
                        "section": secs.get(c.row, ""), "label": W.label(ws.title, c.row),
                        "unit": W.unit(ws.title, c.row), "kind": kind, "cell_style": style_name(c),
                        "value_published": value_repr(W.wv[ws.title][c.coordinate].value),
                        "allowed_values": "", "used_by_cells": G.out_degree((ws.title, c.row, c.column)),
                        "used_by_sheets": ";".join(sorted({s for (s, _r, _c) in G.successors((ws.title, c.row, c.column))})),
                        "notes": f"formula: {v[:200]}",
                    })
    order = {"switch": 0, "input": 1, "technical_input": 2, "pasted_value": 3, "hardcode_in_calculation": 4,
             "calculated_cell": 5, "calculated_row": 6, "output": 7}
    sheet_order = {s: i for i, s in enumerate(W.wb.sheetnames)}
    rows.sort(key=lambda d: (order[d["kind"]], sheet_order[d["sheet"]],
                             int(re.sub(r"\D", "", d["cell"]) or 0), d["cell"]))
    with open(os.path.join(root, "docs", "variable_dictionary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # row-level graph
    RG = collections.defaultdict(set)
    for (u, v) in G.edges():
        a, b = f"{u[0]}!{u[1]}", f"{v[0]}!{v[1]}"
        if a != b:
            RG[b].add(a)
    sheet_edges = collections.Counter((u[0], v[0]) for u, v in G.edges() if u[0] != v[0])
    json.dump({k: sorted(v) for k, v in RG.items()}, open(os.path.join(root, "work", "row_graph.json"), "w"))
    # row-level precedents for every row that holds formulas
    dependents = collections.Counter(a for b, prec in RG.items() for a in prec)
    formula_rows = sorted({(n[0], n[1]) for n, d in G.nodes(data=True) if d.get("formula")},
                          key=lambda t: (sheet_order[t[0]], t[1]))
    with open(os.path.join(root, "docs", "row_dependencies.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["row_id", "sheet", "row", "label", "unit", "precedent_rows", "dependent_rows"])
        for sh, r in formula_rows:
            rid = f"{sh}!{r}"
            prec = sorted(RG.get(rid, ()), key=lambda x: (sheet_order[x.split("!")[0]], int(x.split("!")[1])))
            w.writerow([rid, sh, r, W.label(sh, r), W.unit(sh, r),
                        ";".join(f"{p} [{W.label(*p.split('!')[:1], int(p.split('!')[1]))[:40]}]" for p in prec),
                        dependents.get(rid, 0)])
    stats = {
        "formula_cells": sum(1 for n, d in G.nodes(data=True) if d.get("formula")),
        "edges": G.number_of_edges(),
        "functions": W.funcs.most_common(),
        "offset_cells": len(W.offset_cells),
        "static_sccs": [len(s) for s in sccs],
        "conditional_edges_through_row_totals": [(f"{u[0]}!{L(u[2])}{u[1]}", f"{v[0]}!{L(v[2])}{v[1]}") for u, v in cond],
        "acyclic_without_conditional_edges": acyclic_without_cond,
        "longest_chain_cells": nx.dag_longest_path_length(H) if acyclic_without_cond else None,
        "sheet_edges": [[a, b, n] for (a, b), n in sheet_edges.most_common()],
        "dictionary_counts": collections.Counter(r["kind"] for r in rows),
        "defined_names": W.names,
    }
    json.dump(stats, open(os.path.join(root, "work", "inventory.json"), "w"), indent=1, default=list)
    print(json.dumps({k: stats[k] for k in ("formula_cells", "edges", "offset_cells", "static_sccs",
                                            "acyclic_without_conditional_edges", "dictionary_counts")}, default=list))


if __name__ == "__main__":
    main()
