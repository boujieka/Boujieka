"""Compare a French translation with its English source: protected markup must survive unchanged.

python3 tools/fr/check_translation.py book7/src/ch01.md book7/src_fr/ch01.md
Checks: model fields {{...}} (same multiset), source keys [..] (same multiset), %% markers, figures, headings by level,
tables (count and columns per table), code fences; reports English words left in the text and banned dashes.
Exit status 1 if any check fails.
"""
import re
import sys
from collections import Counter

SRC_KEY = r"\[((?:[A-Z][A-Z0-9]{1,2}(?::S\d+[a-z]?|-\d{2}|:BENCH)|CI)(?:;\s*(?:[A-Z][A-Z0-9]{1,2}(?::S\d+[a-z]?|-\d{2}|:BENCH)|CI))*)\]"
EN_WORDS = {"the", "and", "with", "which", "this", "that", "from", "would", "should", "their", "there", "these", "where", "when",
            "into", "than", "between", "against", "because", "however", "without", "through"}


def strip_code(t):
    return re.sub(r"```.*?```", "", t, flags=re.S)


def tables(t):
    out, cur = [], None
    for line in t.split("\n"):
        if line.startswith("|"):
            if cur is None:
                cur = line.count("|") - 1
                out.append(cur)
        else:
            cur = None
    return out


def keys(t):
    ks = []
    for m in re.finditer(SRC_KEY, t):
        ks += [k.strip() for k in m.group(1).split(";")]
    return Counter(ks)


def main(en_path, fr_path):
    en, fr = open(en_path, encoding="utf8").read(), open(fr_path, encoding="utf8").read()
    fails = []

    def cmp(name, a, b):
        if a != b:
            fails.append(f"{name}: EN {a} / FR {b}")

    cmp("model fields", Counter(re.findall(r"\{\{[^}]+\}\}", en)), Counter(re.findall(r"\{\{[^}]+\}\}", fr)))
    cmp("source keys", keys(en), keys(fr))
    cmp("%% markers", re.findall(r"%%\w+", en), re.findall(r"%%\w+", fr))
    cmp("figures", re.findall(r"\]\((figures/[^)]+)\)", en), re.findall(r"\]\((figures/[^)]+)\)", fr))
    cmp("headings by level", [len(h) for h in re.findall(r"^(#+) ", strip_code(en), re.M)],
        [len(h) for h in re.findall(r"^(#+) ", strip_code(fr), re.M)])
    cmp("tables (columns)", tables(strip_code(en)), tables(strip_code(fr)))
    cmp("code fences", en.count("```"), fr.count("```"))
    cmp("'Table: ' captions", len(re.findall(r"^Table: ", en, re.M)), len(re.findall(r"^Table: ", fr, re.M)))
    cmp("'Note: ' lines", len(re.findall(r"^Note: ", en, re.M)), len(re.findall(r"^Note: ", fr, re.M)))
    body = strip_code(fr)
    body = re.sub(r"`[^`]*`", "", body)
    words = re.findall(r"[A-Za-z']+", body.lower())
    en_hits = Counter(w for w in words if w in EN_WORDS)
    if sum(en_hits.values()) > 3:
        fails.append(f"English words left (check they are titles or protected terms): {dict(en_hits.most_common(8))}")
    for ch, name in (("—", "em dash"), ("–", "en dash")):
        if ch in fr:
            fails.append(f"{name}: {fr.count(ch)}")
    ratio = len(re.findall(r"\w+", strip_code(fr))) / max(1, len(re.findall(r"\w+", strip_code(en))))
    if not 1.0 <= ratio <= 1.45:
        fails.append(f"length ratio FR/EN {ratio:.2f} (French usually runs 1.1 to 1.3 times longer; check for omissions or additions)")
    print(fr_path, "OK" if not fails else "")
    for f in fails:
        print("  -", f)
    return not fails


if __name__ == "__main__":
    ok = main(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
