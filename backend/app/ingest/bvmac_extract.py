"""BVMAC Bulletin officiel de la cote (BOC): deterministic parser for the bond tables.

Parser version EXTRACTOR = "bvmac_boc/1" reads the layout used since late 2023 (bond quote table
with a "Code ISIN" column and "Seuil Haut / Seuil Bas" columns). Per listed BOND (equities are
ignored) it reads:

  * the quote table ("MARCHE DES OBLIGATIONS", sub-tables OBLIGATIONS DES ETATS / REGIONALES /
    PRIVEES), one line per bond: issuer, bond name, ISIN, mnemo, then 17 columns —
        previous price date, previous price (% of nominal), previous price (FCFA),
        nominal (j+3, FCFA), accrued coupon (j+3, FCFA), volume demanded, volume offered,
        volume traded (number of bonds), value traded (FCFA), number of trades,
        status (NC = not quoted), opening price (%), closing price (%), upper limit (%),
        lower limit (%), variation (%), reference price for the next session (FCFA);
  * the section "Total" lines (volume traded, value traded, number of trades) and the
    front-page market summary line "OBLIGATIONS <volume> <value> <trades> <lines>";
  * the characteristics table ("MARCHE DES OBLIGATIONS : N LIGNES OBLIGATAIRES"): coupon
    ("Taux facial"), first listing date, amount raised, number of securities, current nominal,
    price, maturity in years, amortisation, payment periodicity, previous / next payment
    dates, outstanding amount ("Encours"), printed "Rend net/brut", turnover.

The 2019–2022 layout (bond code like "ECMR.05-18/23", no ISIN column) is NOT parsed: those
lines cannot be tied to an ISIN from the document itself (`layout="unsupported"`).

Numbers are printed French-style: thousands separated by spaces, decimal comma — and columns are
also separated by spaces, so "500 500 500 5 003 835 1" has several readings. The parser
enumerates EVERY reading compatible with the number grammar and the column order, keeps those
that satisfy the order-book identities (whole numbers of bonds and trades, traded <= demanded,
traded <= offered, 1 <= trades <= traded, nothing traded <=> no value and no trade), and accepts
a field only when all remaining readings give the same value; otherwise the field is left out
and the row is incomplete (never guessed). When a traded line still has several readings
(order-book numbers separated by single spaces, e.g. "500 000 500 000 500 000 5 198 260 000 1"),
the readings satisfying the printed value identity are shown in staging with a note, but the
checker HOLDS such a line: an ambiguous split is never resolved by arithmetic.

Two independent readings of the same PDF are supported:
  * mode="layout" (`pdftotext -layout`): one table row per text line; a run of two or more spaces
    is a column boundary;
  * mode="raw" (`pdftotext -raw`): content-stream order, single spaces everywhere, and a line
    break may fall inside a token ("GA000002031⏎3", "EGA1⏎0"). Each line break inside a record is
    tried both as a separator and as a join; a record must end at a line end.
The checker (app.ingest.bvmac_check) requires both readings to agree on every value.

Every value carries its raw text and a locator: layout "p<page>:L<line> t<i>-<j>" (page, line,
token range on that line), raw "raw:p<page>:L<line>" (line of the ISIN).
"""

import itertools
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation

EXTRACTOR = "bvmac_boc/1"
MAX_READINGS = 500  # enumeration cap per record; more readings than this => ambiguous
MAX_RAW_BREAKS = 6  # line breaks tried both ways in one raw record
RAW_TAIL_LINES = 5  # a raw record spans at most this many lines after its ISIN

# CEMAC ISIN prefixes (ISO 3166-1 alpha-2 -> ISO alpha-3).
ISIN_COUNTRY = {"CM": "CMR", "GA": "GAB", "TD": "TCD", "CG": "COG", "GQ": "GNQ", "CF": "CAF"}
STATE_NAMES = {  # as printed after "ETAT DU", folded, without spaces
    "CAMEROUN": "CMR", "GABON": "GAB", "TCHAD": "TCD", "CONGO": "COG",
    "GUINEEEQUATORIALE": "GNQ", "CENTRAFRIQUE": "CAF", "REPUBLIQUECENTRAFRICAINE": "CAF",
}
SECTIONS = {"ETATS": "sovereign", "DESETATS": "sovereign", "REGIONALES": "regional", "PRIVEES": "private"}

MNEMO = ("mnemo", "mnemo")
QUOTE_FIELDS = [
    ("previous_price_date", "date"), ("previous_price_pct", "num"), ("previous_price_fcfa", "num"),
    ("nominal", "num"), ("accrued_coupon", "num"), ("volume_demanded", "num"),
    ("volume_offered", "num"), ("volume_traded", "num"), ("value_traded", "num"), ("trades", "num"),
    ("status", "word"), ("open_price_pct", "num"), ("close_price_pct", "num"),
    ("upper_limit_pct", "num"), ("lower_limit_pct", "num"), ("variation_pct", "pct"),
    ("next_reference_price_fcfa", "num"),
]
# Order-book sizes are only used to choose between readings (every kept reading satisfies
# traded <= demanded and traded <= offered); when they stay ambiguous they are left out (noted),
# and nothing else on the line depends on them.
OPTIONAL_QUOTE_FIELDS = {"volume_demanded", "volume_offered"}
REQUIRED_QUOTE_FIELDS = ["mnemo"] + [n for n, _ in QUOTE_FIELDS if n not in OPTIONAL_QUOTE_FIELDS]
CHAR_FIELDS = [
    ("coupon_rate", "num"), ("first_listing_date", "date"), ("amount_raised", "num"),
    ("securities_listed", "num"), ("current_nominal", "num"), ("price_pct", "num"),
    ("maturity_years", "num"), ("amortization", "amort"), ("periodicity", "word"),
    ("previous_payment_date", "date"), ("next_payment_date", "date"), ("outstanding_amount", "num"),
    ("printed_return", "num"), ("turnover_rate", "num"),
]

ISIN_RE = re.compile(r"([A-Z]{2}) ?(\d{10})(?!\d)")
ISIN_BROKEN_RE = re.compile(r"([A-Z]{2}) ?\n?((?:\d\n?){9}\d)(?!\d)")  # raw: a line break may cut it
DATE_RE = re.compile(r"^(\d{2})/(\d{2})/(\d{4})$")
# "… N° 2607 DU 01/10/2026"; also printed "DU 2/08/2024" and "DU 1er/10/2025".
HEADER_RE = re.compile(r"BULLETIN\s*OFFICIEL\s*DE\s*LA\s*COTE\s*N\s*°\s*(\d+)\s*DU\s*(\d{1,2})\s*(?:ER)?\s*/\s*(\d{2})/(\d{4})")


# --------------------------------------------------------------------------- helpers


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.replace("’", "'"))
    return "".join(c for c in s if not unicodedata.combining(c)).upper()


def nospace(s: str) -> str:
    return re.sub(r"\s+", "", fold(s))


def isin_valid(isin: str) -> bool:
    """ISO 6166 check digit: letters -> numbers (A=10 … Z=35), then Luhn on the digit string."""
    if not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}\d", isin or ""):
        return False
    digits = "".join(str(int(c, 36)) for c in isin[:-1])
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2 == 0:  # the rightmost payload digit is doubled
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - total % 10) % 10 == int(isin[-1])


def to_decimal(raw: str) -> Decimal:
    return Decimal(raw.replace(" ", "").replace("%", "").replace(",", "."))


def to_date(raw: str) -> date | None:
    m = DATE_RE.match(raw)
    if not m:
        return None
    try:
        return date(int(m[3]), int(m[2]), int(m[1]))
    except ValueError:
        return None


@dataclass
class Tok:
    text: str
    gap: int  # spaces before the token (layout); 1 in raw mode
    index: int  # token index on its line (layout) / in the record (raw)
    line_end: bool = False  # raw: last token of a source line


def tokens(line: str, start: int = 0) -> list[Tok]:
    out, prev_end = [], None
    for i, m in enumerate(re.finditer(r"\S+", line[start:])):
        out.append(Tok(m.group(), 0 if prev_end is None else m.start() - prev_end, i))
        prev_end = m.end()
    return out


# --------------------------------------------------------------------------- number grammar

_SINGLE = re.compile(r"^(0|[1-9]\d*)(,\d+)?$")
_HEAD = re.compile(r"^[1-9]\d{0,2}$")
_MID = re.compile(r"^\d{3}$")
_LAST = re.compile(r"^\d{3}(,\d+)?$")
_PCT = re.compile(r"^[+-]?\d+(,\d+)?%$")
_WORD = re.compile(r"^[A-Za-z]+$")
_MNEMO1 = re.compile(r"^[A-Z][A-Z0-9]*$")
_MNEMO2 = re.compile(r"^[A-Z0-9]{1,3}$")


def _num_spans(toks: list[Tok], i: int, joinable) -> list[int]:
    """End indexes (exclusive) j such that toks[i:j] reads as one printed number."""
    out = []
    t = toks[i].text
    if _SINGLE.match(t):
        out.append(i + 1)
    if _HEAD.match(t):
        j = i + 1
        while j < len(toks) and joinable(toks[j]):
            if _LAST.match(toks[j].text):
                out.append(j + 1)
            if not _MID.match(toks[j].text):
                break
            j += 1
    return out


def _spans(kind: str, toks: list[Tok], i: int, joinable) -> list[int]:
    if i >= len(toks):
        return []
    t = toks[i].text
    nxt = toks[i + 1] if i + 1 < len(toks) else None
    if kind == "num":
        return _num_spans(toks, i, joinable)
    if kind == "date":
        return [i + 1] if DATE_RE.match(t) else []
    if kind == "word":
        return [i + 1] if _WORD.match(t) else []
    if kind == "pct":
        if _PCT.match(t):
            return [i + 1]
        if t in ("-", "+") and nxt and joinable(nxt) and _PCT.match(t + nxt.text):
            return [i + 2]
        return []
    if kind == "amort":  # one or two upper-case words ("CONSTANT", "IN FINE")
        if not re.match(r"^[A-Z]+$", t):
            return []
        return [i + 1] + ([i + 2] if nxt and joinable(nxt) and re.match(r"^[A-Z]+$", nxt.text) else [])
    if kind == "mnemo":  # "ECMR6", sometimes printed "ECM R6" / "ECM 10"
        if not _MNEMO1.match(t):
            return []
        return [i + 1] + ([i + 2] if nxt and joinable(nxt) and _MNEMO2.match(nxt.text) else [])
    raise ValueError(kind)


def readings(toks: list[Tok], spec: list[tuple[str, str]], mode: str) -> tuple[list[list[tuple[int, int]]], bool]:
    """Every way to cut `toks` into the fields of `spec`. Layout: all tokens consumed, a gap of 2+
    spaces is a column boundary. Raw: the reading must end at a source line end (what follows is
    the next record). Returns (readings, truncated)."""
    if mode == "layout":
        joinable = lambda tk: tk.gap == 1  # noqa: E731
        can_end = lambda i: i == len(toks)  # noqa: E731
    else:
        joinable = lambda tk: True  # noqa: E731
        can_end = lambda i: i > 0 and toks[i - 1].line_end  # noqa: E731
    out: list[list[tuple[int, int]]] = []
    truncated = False

    def rec(i: int, k: int, acc: list[tuple[int, int]]) -> None:
        nonlocal truncated
        if len(out) >= MAX_READINGS:
            truncated = True
            return
        if k == len(spec):
            if can_end(i):
                out.append(list(acc))
            return
        if len(toks) - i < len(spec) - k:
            return
        for j in _spans(spec[k][1], toks, i, joinable):
            acc.append((i, j))
            rec(j, k + 1, acc)
            acc.pop()

    rec(0, 0, [])
    return out, truncated


# --------------------------------------------------------------------------- results


@dataclass
class Value:
    value: object  # str for text, Decimal for numbers, date for dates
    raw: str
    locator: str

    def as_dict(self) -> dict:
        v = self.value
        v = v.isoformat() if isinstance(v, date) else (str(v) if isinstance(v, Decimal) else v)
        return {"value": v, "raw": self.raw, "locator": self.locator}


@dataclass
class BondRow:
    isin: str
    table: str  # quote | characteristics
    section: str | None  # sovereign | regional | private (layout only)
    page: int
    line_no: int
    line: str  # the printed line (layout) / the record text (raw)
    issuer: str | None = None
    name: str | None = None
    country_iso3: str | None = None  # from "ETAT DU …" (sovereign lines)
    prefix_compact: str | None = None  # raw: text before the ISIN, without spaces
    fields: dict[str, Value] = field(default_factory=dict)
    readings_total: int = 0  # readings allowed by the number grammar
    readings_kept: int = 0  # readings that also satisfy the order-book identities
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def v(self, name: str):
        f = self.fields.get(name)
        return f.value if f else None


@dataclass
class SectionTotal:
    section: str
    page: int
    line_no: int
    line: str
    digits: str  # every digit printed after "Total", in order


@dataclass
class ParsedBoc:
    mode: str
    layout: str = "unsupported"  # EXTRACTOR | "unsupported"
    boc_number: str | None = None
    session_date: date | None = None
    header_dates: set = field(default_factory=set)  # (page, BOC number, ISO date) of every page header
    quotes: dict[str, BondRow] = field(default_factory=dict)
    characteristics: dict[str, BondRow] = field(default_factory=dict)
    totals: dict[str, SectionTotal] = field(default_factory=dict)
    summary_digits: str | None = None  # front-page "OBLIGATIONS <vol> <value> <trades> <lines>"
    declared_lines: int | None = None  # "MARCHE DES OBLIGATIONS : N LIGNES OBLIGATAIRES"
    warnings: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------- record reading


def _whole(d: Decimal) -> bool:
    return d == d.to_integral_value()


def quote_constraints(vals: dict) -> bool:
    vd, vo, vt = vals["volume_demanded"], vals["volume_offered"], vals["volume_traded"]
    val, n = vals["value_traded"], vals["trades"]
    if not all(_whole(x) for x in (vd, vo, vt, n)):
        return False
    if vt == 0:
        return val == 0 and n == 0
    return vt <= vd and vt <= vo and 1 <= n <= vt and val > 0


def value_identity(vals: dict) -> bool:
    """Value traded == traded x (closing % x nominal / 100 + accrued coupon), within rounding."""
    vt, val = vals["volume_traded"], vals["value_traded"]
    expected = vt * (vals["close_price_pct"] * vals["nominal"] / 100 + vals["accrued_coupon"])
    return abs(val - expected) <= vt * Decimal("0.005") + 1


def char_constraints(vals: dict) -> bool:
    mat, price = vals["maturity_years"], vals["price_pct"]
    raised, count = vals["amount_raised"], vals["securities_listed"]
    if not _whole(mat) or not (0 < mat <= 50) or not (0 < price <= 200):
        return False
    return _whole(count) and count > 0 and raised >= count


def _convert(kind: str, raw: str):
    if kind in ("num", "pct"):
        return to_decimal(raw)
    if kind == "date":
        d = to_date(raw)
        if d is None:
            raise ValueError(raw)
        return d
    if kind == "mnemo":
        return raw.replace(" ", "")
    return raw


def decode(toks: list[Tok], spec, mode: str, constraints) -> tuple[list[dict], int, bool]:
    """Readings of `toks` as `spec`, decoded, filtered by `constraints`.
    Returns (decoded readings {field: (value, raw, i, j)}, grammar-valid count, truncated)."""
    rds, truncated = readings(toks, spec, mode)
    out = []
    for rd in rds:
        vals = {}
        try:
            for (name, kind), (i, j) in zip(spec, rd):
                raw = " ".join(t.text for t in toks[i:j])
                vals[name] = (_convert(kind, raw), raw, i, j)
        except (InvalidOperation, ValueError):
            continue
        if constraints({k: v[0] for k, v in vals.items()}):
            out.append(vals)
    return out, len(rds), truncated


TIE_BREAK_NOTE = "several readings of the order-book columns; one kept by the printed value identity"


def _tie_break(row: BondRow, decoded: list[dict]) -> list[dict]:
    """When several readings remain (numbers of the order book separated by single spaces, e.g.
    "500 000 500 000 500 000 5 198 260 000"), keep the readings that satisfy the printed value
    identity, and NOTE it. This only makes the candidate values visible in staging: the checker
    holds every line carrying this note (an ambiguous split is never resolved by arithmetic)."""
    variants = {tuple(v[0] for v in d.values()) for d in decoded}
    if len(variants) <= 1:
        return decoded
    kept = [d for d in decoded if value_identity({k: v[0] for k, v in d.items()})]
    if kept and len({tuple(v[0] for v in d.values()) for d in kept}) < len(variants):
        row.notes.append(TIE_BREAK_NOTE)
        return kept
    return decoded


def _settle(row: BondRow, decoded: list[dict], spec, locate, require_all: bool) -> None:
    """Keep the fields on which every remaining reading agrees."""
    row.readings_kept = len(decoded)
    if not decoded:
        row.errors.append("no reading of the line fits the expected columns")
        return
    for name, _ in spec:
        variants = {d[name][0] for d in decoded}
        if len(variants) == 1:
            # Same value; the printed text can differ only by where a raw line break fell.
            first = min((d[name] for d in decoded), key=lambda v: (v[1].count(" "), v[1]))
            row.fields[name] = Value(first[0], first[1], locate(first))
        elif require_all and name in OPTIONAL_QUOTE_FIELDS:
            row.notes.append(f"{name} not read: {len(variants)} possible readings "
                             f"{sorted({d[name][1] for d in decoded})}")
        elif require_all:
            row.errors.append(f"{name}: {len(variants)} possible readings "
                              f"{sorted({d[name][1] for d in decoded})}")


def split_issuer(prefix: str, section: str | None) -> tuple[str | None, str | None, str | None, str | None]:
    """(issuer, bond name, country from 'ETAT DU …', error) from the layout text before the ISIN."""
    text = prefix.strip()
    if not text:
        return None, None, None, "issuer and bond name are not on the ISIN line"
    if section == "sovereign":
        m = re.match(r"^E\s*T\s*A\s*T\s*D\s*U\s*", fold(text))
        if not m:
            return None, None, None, f"sovereign line without 'ETAT DU …': {text!r}"
        flat = nospace(fold(text)[m.end():])
        for state, iso3 in sorted(STATE_NAMES.items(), key=lambda kv: -len(kv[0])):
            if flat.startswith(state):
                pos, seen = m.end(), 0  # cut the printed text right after the state name
                while seen < len(state) and pos < len(text):
                    if not text[pos].isspace():
                        seen += 1
                    pos += 1
                issuer, name = " ".join(text[:pos].split()), " ".join(text[pos:].split())
                return issuer, name or None, iso3, None if name else "bond name missing"
        return None, None, None, f"unknown state in {text!r}"
    parts = [p for p in re.split(r"\s{2,}", text) if p]
    if len(parts) >= 2:
        return " ".join(parts[0].split()), " ".join(" ".join(parts[1:]).split()), None, None
    return None, " ".join(text.split()), None, "issuer and bond name are not separated by a column gap"


# --------------------------------------------------------------------------- document parsing


def _region_walk(pages: list[str], out: ParsedBoc):
    """Yield (page, line_no, line, region, section) for every line, tracking table headers."""
    region = section = None
    for p_i, page in enumerate(pages, start=1):
        for l_i, line in enumerate(page.split("\n"), start=1):
            flat = nospace(line)
            if flat.startswith("MARCHEDESACTIONS"):
                region, section = "equity", None
                yield p_i, l_i, line, "header", None
                continue
            if flat.startswith("MARCHEDESOBLIGATIONS"):
                m = re.match(r"MARCHEDESOBLIGATIONS:?(\d+)LIGNESOBLIGATAIRES", flat)
                if m:
                    region, section = "bond_characteristics", None
                    out.declared_lines = int(m[1])
                else:
                    region, section = ("bond_quotes" if flat == "MARCHEDESOBLIGATIONS" else None), None
                yield p_i, l_i, line, "header", None
                continue
            if region and region.startswith("bond") and flat.startswith("OBLIGATIONS") and flat[11:] in SECTIONS:
                section = SECTIONS[flat[11:]]
                yield p_i, l_i, line, "header", section
                continue
            if flat.startswith("TOTALDESENCOURS"):
                region = section = None
                yield p_i, l_i, line, "header", None
                continue
            if region is None and out.summary_digits is None and re.match(r"^OBLIGATIONS\d", flat):
                out.summary_digits = re.sub(r"\D", "", flat)
                continue
            yield p_i, l_i, line, region, section


def _parse_layout(pages: list[str], out: ParsedBoc) -> None:
    for p_i, l_i, line, region, section in _region_walk(pages, out):
        if region not in ("bond_quotes", "bond_characteristics"):
            continue
        flat = nospace(line)
        if region == "bond_quotes" and section and flat.startswith("TOTAL"):
            after = fold(line)[fold(line).index("TOTAL") + 5:]
            out.totals.setdefault(section, SectionTotal(section, p_i, l_i, line, re.sub(r"\D", "", after)))
            continue
        m = ISIN_RE.search(line)
        if not m:
            continue
        isin = m[1] + m[2]
        quote = region == "bond_quotes"
        row = BondRow(isin, "quote" if quote else "characteristics", section, p_i, l_i, line)
        if section is None:
            row.errors.append("bond line outside a known section")
        toks = tokens(line, m.end())
        spec = [MNEMO] + (QUOTE_FIELDS if quote else CHAR_FIELDS)
        if quote:
            row.issuer, row.name, row.country_iso3, err = split_issuer(line[:m.start()], section)
            if err:
                row.errors.append(err)
        decoded, row.readings_total, truncated = decode(toks, spec, "layout",
                                                        quote_constraints if quote else char_constraints)
        if quote:
            decoded = _tie_break(row, decoded)
        if truncated:
            row.errors.append(f"more than {MAX_READINGS} readings: ambiguous")
        else:
            def locate(v, toks=toks, p=p_i, l_=l_i):
                return f"p{p}:L{l_} t{toks[v[2]].index}-{toks[v[3] - 1].index}"
            _settle(row, decoded, spec, locate, require_all=quote)
        _store(out, row)


def _parse_raw(pages: list[str], out: ParsedBoc) -> None:
    blocks: list[tuple[str, list[tuple[int, int, str]]]] = []
    current = None  # contiguous run of lines inside one bond table
    for p_i, l_i, line, region, _ in _region_walk(pages, out):
        if region not in ("bond_quotes", "bond_characteristics"):
            current = None
            continue
        if current is None or current[0] != region:
            current = (region, [])
            blocks.append(current)
        current[1].append((p_i, l_i, line))
    for region, lines in blocks:
        text = "\n".join(ln for _, _, ln in lines)
        starts, pos = [], 0
        for _, _, ln in lines:
            starts.append(pos)
            pos += len(ln) + 1
        matches = list(ISIN_BROKEN_RE.finditer(text))
        for k, m in enumerate(matches):
            isin = m[1] + m[2].replace("\n", "")
            line_ix = max(i for i, s in enumerate(starts) if s <= m.start())
            p_i, l_i, _ = lines[line_ix]
            end = matches[k + 1].start() if k + 1 < len(matches) else len(text)
            tail_lines = text[m.end():end].split("\n")[:RAW_TAIL_LINES + 1]
            quote = region == "bond_quotes"
            row = BondRow(isin, "quote" if quote else "characteristics", None, p_i, l_i,
                          (m.group() + "\n".join(tail_lines)).replace("\n", "⏎"))
            row.prefix_compact = nospace(text[max(0, m.start() - 400):m.start()])
            spec = [MNEMO] + (QUOTE_FIELDS if quote else CHAR_FIELDS)
            decoded, total, truncated = [], 0, False
            for toks in _raw_variants(tail_lines):
                d, n, t = decode(toks, spec, "raw", quote_constraints if quote else char_constraints)
                decoded += d
                total += n
                truncated |= t
            if quote:
                decoded = _tie_break(row, decoded)
            row.readings_total = total
            if truncated:
                row.errors.append(f"more than {MAX_READINGS} readings: ambiguous")
            else:
                _settle(row, decoded, spec, lambda v, p=p_i, l_=l_i: f"raw:p{p}:L{l_}", require_all=quote)
            _store(out, row)


def _raw_variants(lines: list[str]):
    """Token lists for every way of reading the line breaks in a raw record (separator or join)."""
    lines = [ln for ln in lines]
    while lines and not lines[-1].strip():
        lines.pop()
    breaks = [i for i in range(len(lines) - 1)
              if lines[i] and lines[i + 1] and not lines[i][-1].isspace() and not lines[i + 1][0].isspace()]
    breaks = breaks[:MAX_RAW_BREAKS]
    for mask in itertools.product((False, True), repeat=len(breaks)):
        joins = {b for b, j in zip(breaks, mask) if j}
        toks: list[Tok] = []
        glue = False
        for i, ln in enumerate(lines):
            words = ln.split()
            for w_i, w in enumerate(words):
                if glue and w_i == 0 and toks:
                    toks[-1] = Tok(toks[-1].text + w, 1, toks[-1].index, False)
                else:
                    toks.append(Tok(w, 1, len(toks), False))
            if toks and words:
                toks[-1].line_end = i not in joins
            glue = i in joins
        if toks:
            toks[-1].line_end = True
        yield toks


def _store(out: ParsedBoc, row: BondRow) -> None:
    target = out.quotes if row.table == "quote" else out.characteristics
    if row.isin in target:
        target[row.isin].errors.append(f"ISIN printed twice in the {row.table} table")
        out.warnings.append(f"{row.table} {row.isin} printed twice")
        return
    if not isin_valid(row.isin):
        row.errors.append(f"ISIN {row.isin} fails its check digit")
    target[row.isin] = row


def parse(text: str, mode: str = "layout") -> ParsedBoc:
    """Parse one BOC from `pdftotext -layout` text (mode="layout") or `pdftotext -raw` text."""
    out = ParsedBoc(mode=mode)
    pages = text.split("\f")
    (_parse_layout if mode == "layout" else _parse_raw)(pages, out)
    for p_i, page in enumerate(pages, start=1):  # whole page: raw text may break a header line
        for m in HEADER_RE.finditer(fold(page)):
            out.header_dates.add((p_i, m[1], f"{m[4]}-{m[3]}-{int(m[2]):02d}"))
    # The session is the one printed on the front page and on every page that carries a bond
    # table read here; those headers must all agree. (Some BOCs repeat the previous session's
    # header on later pages — funds, company sheets — which is recorded as a warning only.)
    pages_used = {1} | {r.page for r in [*out.quotes.values(), *out.characteristics.values()]} \
        | {t.page for t in out.totals.values()}
    used = {(n, d) for p, n, d in out.header_dates if p in pages_used}
    missing = sorted(p for p in pages_used if p != 1 and not any(h[0] == p for h in out.header_dates))
    if used:
        if len(used) == 1 and not missing:
            out.boc_number, iso = used.pop()
            out.session_date = date.fromisoformat(iso)
        else:
            out.warnings.append(f"inconsistent or missing BOC headers on the bond pages: {sorted(used)}, "
                                f"pages without header {missing}")
        others = {(n, d) for _, n, d in out.header_dates} - {(out.boc_number, str(out.session_date))}
        if out.session_date and others:
            out.warnings.append(f"other pages carry another BOC header: {sorted(others)}")
    else:
        out.warnings.append("no 'BULLETIN OFFICIEL DE LA COTE N° … DU dd/mm/yyyy' header")
    flat_all = nospace(text)
    if out.quotes and "CODEISIN" in flat_all and "SEUIL" in flat_all:
        out.layout = EXTRACTOR
    elif out.quotes:
        out.warnings.append("bond rows found but the 'Code ISIN' / 'Seuil' column headers are missing")
    return out


def coupon_in_name(name: str | None) -> Decimal | None:
    """The coupon printed inside a bond name, e.g. 'EOG 6,25% NET 2019-2024' -> 6.25."""
    if not name:
        return None
    found = re.findall(r"(\d+(?:[.,]\d+)?)\s*%", name)
    if len(found) != 1:
        return None
    return Decimal(found[0].replace(",", "."))
