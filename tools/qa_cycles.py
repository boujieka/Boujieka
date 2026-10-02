"""QA: static circular-reference detector (cell level, like Excel's own check).

Excel flags a circular reference from the formula precedents alone, whatever IF() branches evaluate to.
This script parses every formula, expands ranges into cells, and runs an iterative Tarjan SCC search.

Run: python tools/qa_cycles.py <file.xlsx>
"""
import re
import sys

import openpyxl
from openpyxl.utils import column_index_from_string as ci
from openpyxl.utils import get_column_letter as gcl

REF = re.compile(r"(?:(?:'([^']+)'|([A-Za-z_][A-Za-z0-9_.]*))!)?\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?")
STR = re.compile(r'"[^"]*"')

path = sys.argv[1]
wb = openpyxl.load_workbook(path)
ids, graph = {}, []


def nid(key):
    if key not in ids:
        ids[key] = len(graph)
        graph.append([])
    return ids[key]


sheetnames = set(wb.sheetnames)
n_formulas = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if not (isinstance(v, str) and v.startswith("=")):
                continue
            n_formulas += 1
            src = nid((ws.title, c.column, c.row))
            body = STR.sub('""', v)
            for m in REF.finditer(body):
                sh = m.group(1) or m.group(2) or ws.title
                if sh not in sheetnames:
                    continue  # function names like EOMONTH( never match; unknown prefixes ignored
                c1, r1 = ci(m.group(3)), int(m.group(4))
                c2, r2 = (ci(m.group(5)), int(m.group(6))) if m.group(5) else (c1, r1)
                for cc in range(min(c1, c2), max(c1, c2) + 1):
                    for rr in range(min(r1, r2), max(r1, r2) + 1):
                        graph[src].append(nid((sh, cc, rr)))

# iterative Tarjan
index, low, onstack, stack, sccs = {}, {}, set(), [], []
counter = 0
for start in range(len(graph)):
    if start in index:
        continue
    work = [(start, 0)]
    while work:
        v, pi = work.pop()
        if pi == 0:
            index[v] = low[v] = counter; counter += 1
            stack.append(v); onstack.add(v)
        recurse = False
        for i in range(pi, len(graph[v])):
            w = graph[v][i]
            if w not in index:
                work.append((v, i + 1)); work.append((w, 0)); recurse = True
                break
            if w in onstack:
                low[v] = min(low[v], index[w])
        if recurse:
            continue
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop(); onstack.discard(w); comp.append(w)
                if w == v:
                    break
            if len(comp) > 1 or v in graph[v]:
                sccs.append(comp)
        if work:
            u = work[-1][0]
            low[u] = min(low[u], low[v])

inv = {v: k for k, v in ids.items()}
print(f"formulas: {n_formulas:,}  nodes: {len(graph):,}  edges: {sum(map(len, graph)):,}")
print(f"circular groups: {len(sccs)}")
for comp in sccs[:10]:
    cells = sorted(f"{inv[x][0]}!{gcl(inv[x][1])}{inv[x][2]}" for x in comp)
    print(len(cells), cells[:12])
sys.exit(1 if sccs else 0)
