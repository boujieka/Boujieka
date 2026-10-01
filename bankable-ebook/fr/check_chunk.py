"""Structural check of a French chunk against its English source.

usage: python3 check_chunk.py en_XX.md fr_XX.md   -> prints OK or the list of problems (exit 1)
"""
import re
import sys

en, fr = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
problems = []


def lines(t):
    return [l for l in t.split("\n") if l.strip()]


le, lf = lines(en), lines(fr)
if len(le) != len(lf):
    problems.append(f"non-empty line count differs: en {len(le)} vs fr {len(lf)} (one paragraph per line, nothing added or dropped)")

attr = lambda t: re.findall(r"(?m)^(#{1,6}) .*?(\{[^}]*\})\s*$", t)
if attr(en) != attr(fr):
    ae, af = attr(en), attr(fr)
    problems.append(f"heading levels/attribute blocks differ (en {len(ae)}, fr {len(af)}); first mismatch: "
                    + str(next(((a, b) for a, b in zip(ae, af) if a != b), (ae[len(af):len(af) + 1], af[len(ae):len(ae) + 1]))))

divs = lambda t: re.findall(r"(?m)^:::.*$", t)
if divs(en) != divs(fr):
    problems.append("fenced div lines (:::) differ")

refs = lambda t: re.findall(r"\[\^(\d+)\](?!:)", t)
defs = lambda t: re.findall(r"(?m)^\[\^(\d+)\]:", t)
if sorted(refs(en)) != sorted(refs(fr)):
    problems.append(f"footnote references differ: en {refs(en)} fr {refs(fr)}")
if sorted(defs(en)) != sorted(defs(fr)):
    problems.append(f"footnote definitions differ: en {defs(en)} fr {defs(fr)}")

tab = lambda t: [len(re.findall(r"(?<!\\)\|", l)) for l in t.split("\n") if l.startswith("|")]
if tab(en) != tab(fr):
    te, tf = tab(en), tab(fr)
    problems.append(f"table rows/columns differ: en {len(te)} rows vs fr {len(tf)} rows"
                    + (f"; first differing row index {next(i for i, (a, b) in enumerate(zip(te, tf)) if a != b)}" if any(a != b for a, b in zip(te, tf)) else ""))

urls = lambda t: sorted(re.findall(r"https?://[^\s)>\]]+", t))
if urls(en) != urls(fr):
    missing = set(urls(en)) - set(urls(fr))
    problems.append(f"URLs differ; missing or changed: {sorted(missing)[:5]}")

eng = [l[:60] for l in fr.split("\n")
       if re.match(r"^(#{1,6} (Part|Appendix|Chapter)\b|Chapter \d|\*?Sources?: |\*?Note: )", l)]
if eng:
    problems.append(f"English labels left in French text: {eng}")

print("OK" if not problems else "PROBLEMS:\n- " + "\n- ".join(problems))
sys.exit(1 if problems else 0)
