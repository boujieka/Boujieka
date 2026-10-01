"""Language layer for the workbook builders.

The builders write English strings. When a language other than English is selected, this module
patches openpyxl so that, at build time:
- plain cell text is translated through a dictionary (exact match);
- string literals inside formulas are translated the same way, and sheet names referenced in
  formulas are renamed;
- worksheet titles and conditional-formatting formulas are translated.
Separately, TEXT(x,"fmt") calls are always rewritten to FIXED(), because TEXT format codes are
locale-dependent (a "#,##0" code breaks in French-locale Excel) while FIXED uses the user's locale.

Usage in a builder:
    import i18n
    LANG, OUT_ARG = i18n.setup(sys.argv)
    T = i18n.T            # translate a Python-side string (chart titles, validation messages)
    USD = i18n.money(...) # drops the "$" sign in non-English versions (currency is a label input)
    ...
    i18n.report()          # at the end: lists untranslated strings
"""
import re
import sys

LANG = "en"
DICT = {}
MISSING = set()
SHEETS = {}
SUFFIXES = {}

_LIT = re.compile(r'"((?:[^"]|"")*)"')


def T(s):
    """Translate a plain string (exact match, with known suffix rules)."""
    if LANG == "en" or not isinstance(s, str):
        return s
    if s in DICT:
        return DICT[s]
    for suf_en, suf_tr in SUFFIXES.items():
        if s.endswith(suf_en) and s[: -len(suf_en)] in DICT:
            return DICT[s[: -len(suf_en)]] + suf_tr
    if re.search(r"[A-Za-z]{2,}", s):
        MISSING.add(s)
    return s


def money(fmt):
    return fmt if LANG == "en" else fmt.replace("$", "")


def _split_args(inner):
    """Split a function's argument string at top-level commas (respecting quotes and parentheses)."""
    args, depth, q, cur = [], 0, False, ""
    for ch in inner:
        if ch == '"':
            q = not q
        elif not q and ch == "(":
            depth += 1
        elif not q and ch == ")":
            depth -= 1
        elif not q and ch == "," and depth == 0:
            args.append(cur)
            cur = ""
            continue
        cur += ch
    args.append(cur)
    return args


FIXED_MAP = {
    "#,##0": lambda x: f"FIXED({x},0)",
    "#,##0;(#,##0)": lambda x: f"FIXED({x},0)",
    "$#,##0": lambda x: f"FIXED({x},0)",
    "$#,##0.00": lambda x: f"FIXED({x},2)",
    "0.00": lambda x: f"FIXED({x},2)",
    "0.0%": lambda x: f'FIXED(({x})*100,1)&"%"',
    "0%": lambda x: f'FIXED(({x})*100,0)&"%"',
}


def text_to_fixed(f):
    """Rewrite TEXT(x,"fmt") calls into locale-independent FIXED() expressions."""
    out, i = "", 0
    while True:
        j = f.find("TEXT(", i)
        if j < 0 or (j > 0 and (f[j - 1].isalnum() or f[j - 1] == "_")):
            if j < 0:
                return out + f[i:]
            out += f[i:j + 5]
            i = j + 5
            continue
        # find matching parenthesis
        depth, q, k = 0, False, j + 4
        while k < len(f):
            ch = f[k]
            if ch == '"':
                q = not q
            elif not q and ch == "(":
                depth += 1
            elif not q and ch == ")":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        inner = f[j + 5:k]
        args = _split_args(inner)
        fmt = args[-1].strip().strip('"') if len(args) == 2 else None
        if fmt in FIXED_MAP:
            out += f[i:j] + FIXED_MAP[fmt](text_to_fixed(args[0]))
        else:
            out += f[i:k + 1]
        i = k + 1


def F(formula):
    """Translate a formula: sheet names, then string literals."""
    if not isinstance(formula, str):
        return formula
    formula = text_to_fixed(formula)
    if LANG == "en":
        return formula
    for en, tr in SHEETS.items():
        formula = formula.replace(f"'{en}'!", f"'{tr}'!")

    def lit(m):
        s = m.group(1)
        if s.replace('""', '"') not in DICT and (not re.search(r"[A-Za-z]{2,}", s) or s.startswith(("#", "$", "0"))):
            return m.group(0)
        return '"' + T(s.replace('""', '"')).replace('"', '""') + '"'

    return _LIT.sub(lit, formula)


def setup(argv):
    """Parse --lang and patch openpyxl. Returns (lang, output path or None)."""
    global LANG
    args = [a for a in argv[1:]]
    out = None
    if "--lang" in args:
        k = args.index("--lang")
        LANG = args[k + 1]
        del args[k:k + 2]
    if args:
        out = args[0]
    if LANG != "en":
        mod = __import__(f"i18n_{LANG}")
        DICT.update(mod.DICT)
        SHEETS.update(mod.SHEETS)
        SUFFIXES.update(mod.SUFFIXES)
        DICT.update(mod.SHEETS)
    _patch()
    return LANG, out


def _patch():
    from openpyxl.cell.cell import Cell
    from openpyxl.formatting.formatting import ConditionalFormattingList
    from openpyxl.workbook.child import _WorkbookChild

    orig_bind = Cell._bind_value

    def bind(self, value):
        if isinstance(value, str):
            value = F(value) if value.startswith("=") else T(value)
        return orig_bind(self, value)

    Cell._bind_value = bind

    if LANG != "en":
        prop = _WorkbookChild.title

        def set_title(self, value):
            prop.fset(self, SHEETS.get(value, value))

        _WorkbookChild.title = property(prop.fget, set_title)

        orig_add = ConditionalFormattingList.add

        def add(self, rng, rule):
            if getattr(rule, "formula", None):
                rule.formula = [F(x) for x in rule.formula]
            return orig_add(self, rng, rule)

        ConditionalFormattingList.add = add


def report():
    if LANG != "en" and MISSING:
        print(f"[i18n] {len(MISSING)} untranslated strings:", file=sys.stderr)
        for s in sorted(MISSING):
            print("   ", repr(s), file=sys.stderr)
