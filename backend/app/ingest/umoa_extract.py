"""Field extraction from UMOA-Titres "Compte rendu d'adjudication" (auction result report).

UMOA-Titres publishes one result report (PDF, generated from Excel) per auction operation. Two
layouts exist, both read from `pdftotext -layout` output:

* single tranche (2014 → today for one-security operations): "Label : value" pairs, sometimes
  two per line ("Taux marginal : 5,1900%   Taux moyen pondéré : 4,9648%").
* multi tranche ("émission simultanée", ~2023 → today): a header block with one column per
  security (ISIN, name, tenor, maturity…), global totals, then a results table whose columns
  are headed "OAT - 2 ans", "BAT - 364 jours"… Columns are matched to the ISIN columns in
  order and cross-checked on instrument and tenor. Variants handled: headings without dash or
  misspelt ("BAT 182 jours", "BAT 107 jous"), fractional residual tenors ("OAT - 2,85 ans"),
  buyback tables headed by the ISIN codes (matched by code), units printed in their own cell
  ("182   jours"), header rows continued on the next line, and one buyback printed over
  several pages (one operation for the sum checks).

A PDF may hold several reports (issue + buyback). A report is a buyback when its heading says
"rachat" or its auction numbers start with "RA-". Consistency checks are attached to the
tranches they involve only, so one inconsistent tranche does not hold its siblings.

Every extracted value is a `Field` with the raw text, a locator (page, line, label, column)
and a deterministic confidence. Values are normalised only by unit conversion (French number
format, "millions de FCFA" → FCFA); nothing is estimated. When a value cannot be read the field
is left empty with a FieldStatus and the reason is recorded.

Confidence (per field, 0–1): 0.95 single labelled value; 0.90 column assigned by matching the
number of values to the number of columns; 0.80 column assigned by text position or value
read from a multi-line block; 0.75 ratio published without "%" and converted; ×0.6 when the
column mapping or a consistency check is doubtful.
"""

import re
import unicodedata
from dataclasses import asdict, dataclass, field, replace
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from app.models.enums import FieldStatus

EXTRACTOR = "umoa_compte_rendu/2"

ISIN_RE = re.compile(r"\b[A-Z]{2}[A-Z0-9]{9}\d\b")
DATE_RE = re.compile(r"(\d{2})/(\d{2})/(\d{4})")
NUM_RE = re.compile(r"-?\d{1,3}(?: \d{3})+(?:,\d+)?|-?\d+(?:,\d+)?")
# Results-table column heading: "OAT - 2 ans", "BAT - 364 jours"; early-2024 reports print it
# without the dash ("BAT 182 jours") and sometimes misspelt ("BAT 107 jous"); reopened lines
# show a fractional residual tenor ("OAT - 2,85 ans").
TENOR_UNITS = r"(jours|jour|jous|ans|an|mois|semaines)"
TRANCHE_RE = re.compile(r"\b(BAT|OAT)\s*-?\s*(\d+(?:,\d+)?)\s*" + TENOR_UNITS + r"\b", re.IGNORECASE)
UNIT_NAMES = {"jour": "jours", "jous": "jours", "an": "ans"}
# A cell holding only a unit, printed apart from its number ("182   jours", "1 000 000   FCFA").
UNIT_ONLY_RE = re.compile(r"(?:jours?|jous|ans?|mois|semaines|f ?cfa)", re.IGNORECASE)
TOKEN_RE = re.compile(r"\S+(?: \S+)*")  # runs of text separated by 2+ spaces
NULL_TOKENS = {"", "-", "--", "nd", "n/a", "na"}
MILLION = Decimal(1_000_000)

# WAEMU issuers as printed after "Emetteur :" (accents stripped, upper case) and ISIN prefixes.
ISSUERS = {
    "BENIN": "BEN", "BURKINA": "BFA", "COTE D'IVOIRE": "CIV", "GUINEE-BISSAU": "GNB",
    "GUINEE BISSAU": "GNB", "MALI": "MLI", "NIGER": "NER", "SENEGAL": "SEN", "TOGO": "TGO",
}
ISIN_PREFIX = {
    "BJ": "BEN", "BF": "BFA", "CI": "CIV", "GW": "GNB", "ML": "MLI", "NE": "NER", "SN": "SEN",
    "TG": "TGO",
}
MONTHS = [("jan", 1), ("fev", 2), ("mar", 3), ("avr", 4), ("mai", 5), ("juin", 6), ("juil", 7),
          ("aou", 8), ("sep", 9), ("oct", 10), ("nov", 11), ("dec", 12)]

# Fields every result tranche is expected to carry, by instrument. A missing one makes the
# extraction "partial" unless the document visibly leaves it blank ("-", "ND": not disclosed).
COMMON_EXPECTED = (
    "isin", "instrument", "auction_date", "settlement_date", "maturity_date", "tenor",
    "face_value", "number_of_participants", "number_of_bids", "amount_submitted",
    "amount_allocated", "amount_rejected", "weighted_average_yield",
)
EXPECTED = {
    "BAT": COMMON_EXPECTED + ("marginal_rate", "weighted_average_rate"),
    "OAT": COMMON_EXPECTED + ("coupon_rate", "marginal_price", "weighted_average_price"),
}


# --------------------------------------------------------------------------- data classes


@dataclass
class Field:
    value: str | None  # normalised: Decimal as string, ISO date, int, or text
    raw: str
    locator: str
    confidence: float
    unit: str | None = None
    note: str | None = None

    def as_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None or k == "value"}


@dataclass
class Tranche:
    index: int
    fields: dict[str, Field] = field(default_factory=dict)
    field_status: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    kind: str = "issue"  # "issue" | "buyback" (from the section heading)
    # Facts of the operation (report section) this tranche belongs to.
    operation: dict[str, Field] = field(default_factory=dict)
    operation_tranches: int = 1
    # Consistency checks that involve this tranche (its own, and its operation's sum checks),
    # so a failed check in one tranche or section does not hold its siblings.
    checks: list[dict] = field(default_factory=list)
    # Remarks on how a value was read (not errors): e.g. a blank cell in a tranche with no bids.
    notes: list[str] = field(default_factory=list)

    def value(self, name: str) -> str | None:
        f = self.fields.get(name)
        return f.value if f else None

    @property
    def tranche_key(self) -> str:
        key = self.value("isin") or f"col-{self.index + 1}"
        return f"{key}/buyback" if self.kind == "buyback" else key

    @property
    def parse_status(self) -> str:
        expected = EXPECTED.get(self.value("instrument") or "", COMMON_EXPECTED)
        missing = [f for f in expected if self.value(f) is None
                   and self.field_status.get(f) != FieldStatus.NOT_DISCLOSED.value]
        return "partial" if missing or self.errors else "complete"

    @property
    def confidence(self) -> float:
        key = [f.confidence for n, f in self.fields.items() if n in COMMON_EXPECTED and f.value]
        return round(min(key), 3) if key else 0.0


@dataclass
class ParsedDocument:
    layout: str  # "multi_tranche" | "single_tranche" | "unknown"
    operation: dict[str, Field] = field(default_factory=dict)
    tranches: list[Tranche] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: list[dict] = field(default_factory=list)
    publication_date: date | None = None
    operation_status: dict[str, str] = field(default_factory=dict)

    def value(self, name: str) -> str | None:
        f = self.operation.get(name)
        return f.value if f else None


# --------------------------------------------------------------------------- text helpers


def _fold(text: str) -> str:
    """Lower-case, accents stripped, typographic apostrophes unified. Keeps string length,
    so column positions found in the folded text are valid in the original."""
    out = []
    for ch in text:
        if ch in "’‘`´":
            out.append("'")
            continue
        if ch in "\xa0  ":
            out.append(" ")
            continue
        base = unicodedata.normalize("NFKD", ch)
        kept = [c for c in base if not unicodedata.combining(c)]
        out.append(kept[0] if len(kept) == 1 else ch)
    return "".join(out).lower()


@dataclass
class Line:
    page: int
    number: int  # 1-based within the page
    text: str
    folded: str

    def loc(self, label: str, col: int | None = None, ncols: int | None = None) -> str:
        where = f"p{self.page}:L{self.number} '{label}'"
        return where + (f" col {col + 1}/{ncols}" if col is not None else "")


# Header labels printed without a colon (multi-tranche layout).
BARE_LABELS = ("taux d'interet fixe annonce", "taux coupon couru")


def _is_bare_label(folded: str) -> bool:
    """A label with nothing after it: 'Date de valeur   :' or 'Taux coupon couru'."""
    f = folded.strip()
    return (f.endswith(":") and f.count(":") == 1) or f in BARE_LABELS


def _clean(raw: str) -> str:
    return raw.replace("\xa0", " ").replace("\u202f", " ")


def to_lines(text: str) -> list[Line]:
    """Non-blank lines with page/line numbers. Some templates (2026) print each header value
    on the line below its label; such a value line is overlaid onto the label line, keeping
    the label's locator and the value's column positions."""
    lines: list[Line] = []
    for p, page in enumerate(text.split("\f"), start=1):
        raw_lines = [(n, _clean(r)) for n, r in enumerate(page.splitlines(), start=1) if r.strip()]
        k = 0
        while k < len(raw_lines):
            n, clean = raw_lines[k]
            folded = _fold(clean)
            if _is_bare_label(folded) and k + 1 < len(raw_lines) and raw_lines[k + 1][0] == n + 1:
                nxt = raw_lines[k + 1][1]
                width = len(clean.rstrip())
                is_table_head = bool(TRANCHE_RE.search(nxt)) and not TRANCHE_RE.sub("", nxt).strip()
                if not nxt[:width].strip() and not _is_bare_label(_fold(nxt)) and not is_table_head:
                    clean = clean.rstrip() + nxt[width:]
                    folded = _fold(clean)
                    k += 1
            lines.append(Line(p, n, clean, folded))
            k += 1
    return lines


def is_null(token: str | None) -> bool:
    return token is None or token.strip().strip(":").strip().lower() in NULL_TOKENS


def parse_number(token: str) -> Decimal | None:
    m = NUM_RE.search(token.replace("\xa0", " ").replace(" ", " "))
    if not m:
        return None
    try:
        return Decimal(m.group().replace(" ", "").replace(",", "."))
    except InvalidOperation:
        return None


def parse_date(token: str) -> date | None:
    m = DATE_RE.search(token)
    if not m:
        return None
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


def parse_french_date(text: str) -> date | None:
    """'Dakar le 01 octobre 2026', 'Dakar, le 08 septembre 2016', 'Dakar le 02.sept.26'."""
    m = re.search(r"dakar,?\s+le\s+(\d{1,2})[\s.]+([a-z]+)\.?[\s.]*(\d{2,4})", _fold(text))
    if not m:
        return None
    month = next((n for prefix, n in MONTHS if m.group(2).startswith(prefix)), None)
    year = int(m.group(3))
    year += 2000 if year < 100 else 0
    try:
        return date(year, month, int(m.group(1))) if month else None
    except ValueError:
        return None


def tokens_after(line: Line, start: int) -> list[tuple[int, str]]:
    """Text runs (separated by 2+ spaces) from `start`, with their column positions."""
    rest = line.text[start:]
    lead = len(rest) - len(rest.lstrip(" :°º"))
    out = []
    for m in TOKEN_RE.finditer(rest[lead:]):
        tok = m.group().lstrip(": ").rstrip()
        if tok:
            out.append((start + lead + m.start(), tok))
    return out


def merge_unit_cells(tokens: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Join a unit printed in its own cell to the number before it: "182   jours" → "182 jours",
    "1 000 000   FCFA" → "1 000 000 FCFA". Only a unit-only cell right after a bare number is
    joined; anything else is left as printed."""
    out: list[tuple[int, str]] = []
    for pos, tok in tokens:
        if out and UNIT_ONLY_RE.fullmatch(tok) and re.fullmatch(r"\d[\d ]*(?:,\d+)?", out[-1][1]):
            out[-1] = (out[-1][0], f"{out[-1][1]} {tok}")
        else:
            out.append((pos, tok))
    return out


# One amount cell of the results table: "66 462,40 millions de F CFA[, dont ONC :0]". The
# number is matched leftmost; a valid French-format amount never starts with "0" followed by
# a digit, which separates cells printed with no space at all ("… ONC :05 484,13 millions").
# Some reports print a stray space around the decimal comma ("20 208, 7 millions",
# "6 622 ,4millions"); the cell is kept as printed and read by `_amount_millions`.
AMOUNT_CELL_RE = re.compile(
    r"(?:0|[1-9]\d{0,2}(?: \d{3})*|[1-9]\d*)(?: ?, ?\d+)?\s*millions[^,\d]*", re.IGNORECASE)
SPACED_DECIMAL_RE = re.compile(r"(\d) ?, ?(\d+\s*millions)", re.IGNORECASE)


def amount_tokens(line: Line, start: int) -> list[tuple[int, str]]:
    """Like tokens_after, but amount cells are cut on their own pattern, because some reports
    separate them by one space, or by none."""
    rest = line.text[start:]
    if "millions" not in rest.lower():
        return tokens_after(line, start)
    return [(start + m.start(), m.group().strip()) for m in AMOUNT_CELL_RE.finditer(rest)]


def assign_columns(
    tokens: list[tuple[int, str]], col_starts: list[int]
) -> tuple[dict[int, tuple[int, str]], float, str | None]:
    """Map value tokens to columns. Same count → in order; else by nearest position."""
    if not tokens:
        return {}, 0.0, None
    if len(tokens) == len(col_starts):
        return {i: t for i, t in enumerate(tokens)}, 0.90, None
    out: dict[int, tuple[int, str]] = {}
    for pos, tok in tokens:
        col = min(range(len(col_starts)), key=lambda i: abs(col_starts[i] - pos))
        if col in out:
            return out, 0.5, f"two values fall in column {col + 1}"
        out[col] = (pos, tok)
    return out, 0.80, None


def find_line(lines: list[Line], label: str, start: int = 0, end: int | None = None,
              anywhere: bool = False) -> tuple[int, int] | None:
    """(line index, column after the label) of the first line holding `label` (folded)."""
    end = len(lines) if end is None else end
    for i in range(start, min(end, len(lines))):
        f = lines[i].folded
        if anywhere:
            pos = f.find(label)
        else:
            pos = 0 if f.lstrip().startswith(label) else -1
            pos = f.find(label) if pos == 0 else -1
        if pos >= 0:
            return i, pos + len(label)
    return None


def single_value(line: Line, after: int) -> str:
    """The value right after a label in a 'Label : value    Next label : …' line."""
    toks = tokens_after(line, after)
    return toks[0][1] if toks else ""


def single_amount(line: Line, after: int) -> str:
    """An amount after its label, with its unit when the unit is printed in the next cell
    ("9 050,000        millions de FCFA, dont en ONC : 0" → "9 050,000 millions de FCFA"): the
    scale is part of the printed evidence."""
    toks = tokens_after(line, after)
    if not toks:
        return ""
    raw = toks[0][1]
    if len(toks) > 1 and "millions" not in raw.lower() and re.fullmatch(r"\d[\d ]*(?:,\d+)?", raw):
        unit = re.match(r"millions(?: de)?(?: f ?cfa)?", toks[1][1], re.IGNORECASE)
        if unit:
            raw = f"{raw} {unit.group()}"
    return raw


# --------------------------------------------------------------------------- field builders


def _amount_millions(raw: str, loc: str, conf: float) -> tuple[Field | None, str | None]:
    if is_null(raw):
        return None, FieldStatus.NOT_DISCLOSED.value
    note = "published in millions of FCFA; converted to FCFA"
    joined = SPACED_DECIMAL_RE.sub(r"\1,\2", raw, count=1)
    if joined != raw:
        note += "; printed with a space around the decimal comma, read as " + repr(
            joined.split("millions")[0].strip())
    n = parse_number(joined)
    if n is None:
        return None, FieldStatus.NOT_AVAILABLE.value
    return Field(str((n * MILLION).normalize().quantize(Decimal(1))), raw, loc, conf, "XOF", note), None


def _percent(raw: str, loc: str, conf: float, allow_ratio: bool = False) -> tuple[Field | None, str | None]:
    if is_null(raw):
        return None, FieldStatus.NOT_DISCLOSED.value
    n = parse_number(raw)
    if n is None:
        return None, FieldStatus.NOT_AVAILABLE.value
    if "%" in raw:
        return Field(str(n), raw, loc, conf, "percent"), None
    if allow_ratio and n <= Decimal("1.5"):
        return Field(str(n * 100), raw, loc, min(conf, 0.75), "percent",
                     "published as a ratio without '%'; multiplied by 100"), None
    return None, FieldStatus.NOT_AVAILABLE.value


def _price(raw: str, loc: str, conf: float) -> tuple[Field | None, str | None]:
    if is_null(raw):
        return None, FieldStatus.NOT_DISCLOSED.value
    n = parse_number(raw)
    if n is None:
        return None, FieldStatus.NOT_AVAILABLE.value
    unit = "percent_of_nominal" if "%" in raw else "XOF_per_unit"
    return Field(str(n), raw, loc, conf, unit), None


def _integer(raw: str, loc: str, conf: float) -> tuple[Field | None, str | None]:
    if is_null(raw):
        return None, FieldStatus.NOT_DISCLOSED.value
    n = parse_number(raw)
    if n is None or n != n.to_integral_value():
        return None, FieldStatus.NOT_AVAILABLE.value
    return Field(str(int(n)), raw, loc, conf), None


def _date(raw: str, loc: str, conf: float) -> tuple[Field | None, str | None]:
    if is_null(raw):
        return None, FieldStatus.NOT_DISCLOSED.value
    d = parse_date(raw)
    if d is None:
        return None, FieldStatus.NOT_AVAILABLE.value
    return Field(d.isoformat(), raw, loc, conf), None


def _text(raw: str, loc: str, conf: float) -> tuple[Field | None, str | None]:
    if is_null(raw):
        return None, FieldStatus.NOT_DISCLOSED.value
    return Field(raw.strip(), raw, loc, conf), None


def tenor_text(number: str, unit: str) -> str:
    """Normalised tenor: '182 jours', '3 ans'; a fractional residual tenor keeps its decimals
    ('2,85 ans' → '2.85 ans')."""
    return f"{number.replace(',', '.')} {UNIT_NAMES.get(unit.lower(), unit.lower())}"


def _tenor(raw: str, loc: str, conf: float) -> tuple[Field | None, str | None]:
    if is_null(raw):
        return None, FieldStatus.NOT_DISCLOSED.value
    m = re.search(r"(\d+(?:,\d+)?)\s*" + TENOR_UNITS + r"\b", _fold(raw))
    if not m:
        return None, FieldStatus.NOT_AVAILABLE.value
    return Field(tenor_text(m.group(1), m.group(2)), raw, loc, conf), None


def _put(target_fields: dict, target_status: dict, errors: list, name: str,
         result: tuple[Field | None, str | None], label_found: bool = True) -> None:
    f, status = result
    if f is not None:
        target_fields[name] = f
        target_status.pop(name, None)
        return
    if not label_found:
        target_status.setdefault(name, FieldStatus.NOT_DISCLOSED.value)
        return
    target_status[name] = status or FieldStatus.NOT_AVAILABLE.value
    if status == FieldStatus.NOT_AVAILABLE.value:
        errors.append(f"{name}: value present but could not be read")


# --------------------------------------------------------------------------- layouts

# label (folded) → (field name, builder)
HEADER_LABELS = [
    ("denomination de l'emission", "security_name", _text),
    ("adjudication n", "auction_number", _text),
    ("duree", "tenor", _tenor),
    ("date d'echeance", "maturity_date", _date),
    ("valeur nominale unitaire", "face_value", None),  # number, FCFA
    ("taux d'interet fixe annonce", "coupon_rate", lambda r, l, c: _percent(r, l, c, allow_ratio=True)),
    ("taux coupon couru", "accrued_coupon_rate", lambda r, l, c: _percent(r, l, c, allow_ratio=True)),
]
RESULT_LABELS = [
    ("nombre de participants", "number_of_participants", _integer),
    ("nombre de soumissions", "number_of_bids", _integer),
    ("montant global des soumissions", "amount_submitted", _amount_millions),
    ("soumissions retenues", "amount_allocated", _amount_millions),
    ("soumissions rejetees", "amount_rejected", _amount_millions),
    ("taux d'absorption", "absorption_rate", None),  # percent or ratio
    ("taux/prix marginal", "marginal", None),  # rate (BAT) or price (OAT)
    ("taux/prix moyen pondere", "weighted_average", None),
    ("rendement moyen pondere", "weighted_average_yield", _percent),
]


def _face_value(raw: str, loc: str, conf: float) -> tuple[Field | None, str | None]:
    if is_null(raw):
        return None, FieldStatus.NOT_DISCLOSED.value
    n = parse_number(raw)
    return (Field(str(n), raw, loc, conf, "XOF"), None) if n is not None else (
        None, FieldStatus.NOT_AVAILABLE.value)


def _operation_fields(lines: list[Line], doc: ParsedDocument, end: int) -> None:
    op, status, errs = doc.operation, doc.operation_status, doc.warnings

    hit = find_line(lines, "emetteur", anywhere=True)
    if hit:
        i, after = hit
        _put(op, status, errs, "issuer", _text(single_value(lines[i], after), lines[i].loc("Emetteur"), 0.95))
    hit = find_line(lines, "nature des titres")
    if hit:
        i, after = hit
        _put(op, status, errs, "security_type", _text(single_value(lines[i], after),
                                                       lines[i].loc("Nature des titres"), 0.95))
    for label in ("montant global mis en adjudication", "montant mis en adjudication"):
        hit = find_line(lines, label, end=end)
        if hit:
            i, after = hit
            _put(op, status, errs, "total_amount_offered",
                 _amount_millions(single_amount(lines[i], after), lines[i].loc(label), 0.95))
            onc = re.search(r"dont (?:en )?onc\s*:\s*(.*?)\s*$", lines[i].folded)
            raw_onc = lines[i].text[onc.start(1):onc.end(1)] if onc else ""
            _put(op, status, errs, "total_onc_offered",
                 _amount_millions(raw_onc, lines[i].loc("dont ONC"), 0.9), label_found=bool(onc))
            break
    hit = find_line(lines, "date d'adjudication", end=end)
    if hit:
        i, after = hit
        _put(op, status, errs, "auction_date",
             _date(single_value(lines[i], after), lines[i].loc("Date d'adjudication"), 0.95))
    else:  # single layout: "Adjudication N° : … du : 02/09/2026"
        for i, ln in enumerate(lines[:end]):
            m = re.search(r"\b(du\s*:)\s*(\d{2}/\d{2}/\d{4})", ln.folded)
            if m and "adjudication" in ln.folded:
                # The date's own label is the printed "du :" of the "Adjudication N°" line.
                label = ln.text[m.start(1):m.end(1)]
                _put(op, status, errs, "auction_date", _date(ln.text[m.start(2):m.end(2)], ln.loc(label), 0.95))
                break
    hit = find_line(lines, "date de valeur", end=end)
    if hit:
        i, after = hit
        _put(op, status, errs, "settlement_date",
             _date(single_value(lines[i], after), lines[i].loc("Date de valeur"), 0.95))
    for label, name in (("montant global des soumissions", "total_amount_submitted"),
                        ("soumissions retenues", "total_amount_allocated"),
                        ("soumissions rejetees", "total_amount_rejected")):
        hit = find_line(lines, label, end=end)
        if hit and ":" in lines[hit[0]].text[hit[1]:hit[1] + 20]:
            i, after = hit
            _put(op, status, errs, name, _amount_millions(single_amount(lines[i], after), lines[i].loc(label), 0.95))

    # "Taux de couverture …" spans 2–3 lines; the two percentages appear in reading order:
    # coverage by bids, then coverage by accepted bids.
    hit = find_line(lines, "taux de couverture", end=end)
    if hit:
        i = hit[0]
        stop = find_line(lines, "taux d'absorption", start=i, end=end)
        block = lines[i:(stop[0] if stop else i + 4)]
        found = [(ln, m) for ln in block for m in re.finditer(r"\d[\d ]*,\d+\s*%", ln.text)]
        for (ln, m), name in zip(found, ("coverage_bids_pct", "coverage_accepted_pct")):
            _put(op, status, errs, name, _percent(m.group(), ln.loc("Taux de couverture"), 0.80))
        if len(found) < 2:
            doc.warnings.append("coverage ratios: fewer than two percentages found")
    hit = find_line(lines, "taux d'absorption", end=end)
    if hit:
        i, after = hit
        _put(op, status, errs, "absorption_rate",
             _absorption(single_value(lines[i], after), lines[i].loc("Taux d'absorption"), 0.95))
    for ln in reversed(lines):
        d = parse_french_date(ln.text)
        if d:
            doc.publication_date = d
            op["publication_date"] = Field(d.isoformat(), ln.text.strip(), ln.loc("Dakar le"), 0.9)
            break


def _instrument_from(text: str | None) -> str | None:
    if not text:
        return None
    m = re.search(r"-(BAT|OAT)-", text.upper())
    return m.group(1) if m else None


def find_results_head(lines: list[Line], isin_idx: int, isins: list[str]) -> tuple[int | None, list[tuple]]:
    """The results-table header: the first line after the ISIN line made only of column
    headings, either "OAT - 2 ans" / "BAT 182 jours" or (buyback reports) the ISIN codes of the
    section. Returns (line index, [(column start, kind, label)]) where kind is "BAT"/"OAT" with
    a normalised tenor label, or "ISIN" with the code."""
    for j in range(isin_idx + 1, len(lines)):
        text = lines[j].text
        if TRANCHE_RE.search(text) and not TRANCHE_RE.sub("", text).strip():
            return j, [(m.start(), m.group(1).upper(), tenor_text(m.group(2), m.group(3)))
                       for m in TRANCHE_RE.finditer(text)]
        codes = ISIN_RE.findall(text)
        if codes and not ISIN_RE.sub("", text).strip() and set(codes) <= set(isins):
            return j, [(m.start(), "ISIN", m.group()) for m in ISIN_RE.finditer(text)]
    return None, []


def _continuation(lines: list[Line], i: int, tokens: list[tuple[int, str]],
                  starts: list[int]) -> list[tuple[int, str, Line]] | None:
    """Header cells printed over two lines: the label line holds the first column(s) and the
    next, unlabelled line the remaining ones ("Dénomination de l'émission : CI…-BAT-05-2024" /
    "      CI…-OAT-06-2024   CI…-BAT-04-2024 …"). Returns the cells of both lines when together
    they fill every column exactly once, each cell nearest to its own column; else None."""
    n = len(starts)
    if not tokens or len(tokens) >= n or i + 1 >= len(lines):
        return None
    nxt = lines[i + 1]
    if nxt.page != lines[i].page or nxt.number != lines[i].number + 1:
        return None
    if nxt.text[:starts[0]].strip() or ":" in nxt.text:
        return None  # a label, or text left of the value columns: not a continuation
    more = merge_unit_cells(tokens_after(nxt, 0))
    cells = [(p, t, lines[i]) for p, t in tokens] + [(p, t, nxt) for p, t in more]
    if len(cells) != n:
        return None
    for c, (pos, _, _) in enumerate(cells):
        if min(range(n), key=lambda k: abs(starts[k] - pos)) != c:
            return None
    return cells


def _parse_multi(lines: list[Line], isin_idx: int, doc: ParsedDocument) -> None:
    isin_line = lines[isin_idx]
    after = isin_line.folded.find("code isin") + len("code isin")
    cols = [(m.start(), m.group()) for m in ISIN_RE.finditer(isin_line.text, after)]
    starts = [c[0] for c in cols]
    n = len(cols)
    tranches = [Tranche(i) for i in range(n)]
    for i, (_, isin) in enumerate(cols):
        tranches[i].fields["isin"] = Field(isin, isin, isin_line.loc("Code ISIN", i, n), 0.95)

    # Results table header ("OAT - 2 ans   BAT - 364 jours", or the ISIN codes), first after
    # the ISIN line.
    head_idx, heads = find_results_head(lines, isin_idx, [c[1] for c in cols])
    table_end = find_line(lines, "lieu de soumission", start=isin_idx) or find_line(
        lines, "montant propose", start=isin_idx)
    end = table_end[0] if table_end else len(lines)

    # Header block: one column per ISIN.
    for label, name, builder in HEADER_LABELS:
        hit = find_line(lines, label, start=isin_idx + 1, end=head_idx or end)
        if not hit:
            for t in tranches:
                t.field_status.setdefault(name, FieldStatus.NOT_DISCLOSED.value)
            if name == "coupon_rate":
                _unlabelled_coupon(lines, isin_idx, head_idx or end, tranches)
            continue
        i, after_label = hit
        tokens = merge_unit_cells(tokens_after(lines[i], after_label))
        build = builder or _face_value
        cells = _continuation(lines, i, tokens, starts)
        if cells:
            doc.warnings.append(f"{name}: values printed over two lines; merged by column position")
            for c, t in enumerate(tranches):
                pos, raw, ln = cells[c]
                _put(t.fields, t.field_status, t.errors, name,
                     build(_header_raw(name, raw), ln.loc(label, c, n), 0.80))
            continue
        assigned, conf, problem = assign_columns(tokens, starts)
        if problem:
            # The cells could not be told apart: none of them is reliable, and a printed value
            # must never be reported as "not disclosed".
            doc.warnings.append(f"{name}: {problem}")
            for c, t in enumerate(tranches):
                t.field_status[name] = FieldStatus.NOT_AVAILABLE.value
                t.errors.append(f"{name}: cells of {lines[i].loc(label)} could not be assigned to columns ({problem})")
            continue
        for c, t in enumerate(tranches):
            raw = assigned.get(c, (0, ""))[1]
            loc = lines[i].loc(label, c, n)
            _put(t.fields, t.field_status, t.errors, name, build(_header_raw(name, raw), loc, conf or 0.9))
    for t in tranches:
        instr = _instrument_from(t.value("security_name"))
        if instr:
            t.fields["instrument"] = Field(instr, t.fields["security_name"].raw,
                                           t.fields["security_name"].locator, 0.95)

    if head_idx is None:
        doc.warnings.append("results table header (e.g. 'OAT - 2 ans') not found")
        for t in tranches:
            t.errors.append("results table not found")
        doc.tranches = tranches
        return

    # Map results columns to ISIN columns.
    order = list(range(len(heads)))
    mapping_conf = 1.0
    got = [(h[1], h[2]) for h in heads]
    if heads and heads[0][1] == "ISIN":
        # Columns headed by ISIN codes: matched by exact code.
        codes = [h[2] for h in heads]
        perm = [codes.index(t.value("isin")) if codes.count(t.value("isin")) == 1 else -1 for t in tranches]
        if -1 in perm:
            mapping_conf = 0.6
            doc.warnings.append(f"results columns {codes} do not match ISIN columns; mapped by position")
            for t in tranches:
                t.errors.append("column mapping between ISIN block and results table is doubtful")
        else:
            order = perm
    else:
        # In order when instrument and tenor agree.
        expected = [(t.value("instrument"), t.value("tenor")) for t in tranches]
        if len(heads) != n or any(e[0] and e != g for e, g in zip(expected, got)):
            perm = []
            for e in expected:
                matches = [k for k, g in enumerate(got) if g == e and k not in perm]
                perm.append(matches[0] if len(matches) == 1 else -1)
            if -1 not in perm and len(heads) == n:
                order = perm
                doc.warnings.append("results columns reordered to match instrument/tenor of ISIN columns")
            else:
                mapping_conf = 0.6
                doc.warnings.append(
                    f"results columns {got} do not match ISIN columns {expected}; mapped by position"
                )
                for t in tranches:
                    t.errors.append("column mapping between ISIN block and results table is doubtful")
    head_starts = [h[0] for h in heads]

    for label, name, builder in RESULT_LABELS:
        hit = find_line(lines, label, start=head_idx + 1, end=end)
        if not hit:
            # Every row of the results table is part of the template: a missing row means the
            # text was not read as expected, not that the source withheld the value.
            for t in tranches:
                t.field_status[name] = FieldStatus.NOT_AVAILABLE.value
                t.errors.append(f"{name}: row '{label}' not found in the results table")
            continue
        i, after_label = hit
        assigned, conf, problem = assign_columns(amount_tokens(lines[i], after_label), head_starts)
        if problem:
            doc.warnings.append(f"{name}: {problem}")
        for c, t in enumerate(tranches):
            k = order[c] if c < len(order) else c
            raw = assigned.get(k, (0, ""))[1]
            loc = lines[i].loc(label, k, len(heads))
            if not raw:
                if name == "absorption_rate" and t.value("amount_submitted") == "0" \
                        and t.value("amount_allocated") == "0":
                    # A tranche that received no bid: the document prints 0 amounts and leaves
                    # the absorption cell blank (absorption is undefined without bids).
                    t.field_status[name] = FieldStatus.NOT_DISCLOSED.value
                    t.notes.append(f"{name}: cell blank in the source at {loc}; the tranche received "
                                   "no bids (amount submitted 0), so no absorption rate is published")
                    continue
                # Every results column carries a value ("-" when nothing applies): an empty
                # cell means the row was not split correctly. Never treat it as "not disclosed".
                t.field_status[name] = FieldStatus.NOT_AVAILABLE.value
                t.errors.append(f"{name}: no value found in column {k + 1} at {loc}")
                continue
            cf = round((conf or 0.9) * mapping_conf, 3)
            _put_result(t, name, builder, raw, loc, cf)
    doc.tranches = tranches


def _header_raw(name: str, raw: str) -> str:
    """The face value is stored in FCFA as printed; a unit printed in its own cell ("FCFA") is
    dropped from the raw number (the field's unit says XOF). Tenor keeps its unit."""
    if name == "face_value":
        return re.sub(r"\s+f ?cfa$", "", raw, flags=re.IGNORECASE)
    return raw


def _unlabelled_coupon(lines: list[Line], start: int, end: int, tranches: list[Tranche]) -> None:
    """Some 2024 reports print the bond coupon on a line with no label (e.g. "5,70%" under the
    face value, sometimes right above "Taux coupon couru"). It is not read automatically (which
    field it belongs to is an inference), but the bond tranches must not claim the coupon is
    undisclosed either: NOT_AVAILABLE with an error, for a person to confirm."""
    stop = find_line(lines, "montant global des soumissions", start=start, end=end)
    for ln in lines[start + 1:stop[0] if stop else end]:
        if "%" in ln.text and not re.search(r"[a-z]", ln.folded):
            for t in tranches:
                if _instrument_from(t.value("security_name")) == "OAT":
                    t.field_status["coupon_rate"] = FieldStatus.NOT_AVAILABLE.value
                    t.errors.append(f"coupon_rate: a percentage is printed without a label at "
                                    f"{ln.loc('(no label)')}; not read automatically")
            return


def _absorption(raw: str, loc: str, conf: float) -> tuple[Field | None, str | None]:
    """Absorption rate (allotted / submitted): a percentage between 0 and 100. A reading outside
    that range is not a value of this field (e.g. a stray digit glued to the cell)."""
    f, status = _percent(raw, loc, conf, allow_ratio=True)
    if f is not None and not (Decimal(0) <= Decimal(f.value) <= Decimal(100)):
        return None, FieldStatus.NOT_AVAILABLE.value
    return f, status


def _put_result(t: Tranche, name: str, builder, raw: str, loc: str, conf: float) -> None:
    instr = t.value("instrument")
    if name == "absorption_rate":
        f, status = _absorption(raw, loc, conf)
        if f is None and status == FieldStatus.NOT_AVAILABLE.value and parse_number(raw) is not None:
            t.errors.append(f"absorption_rate: '{raw}' at {loc} does not read as a percentage between 0 and 100")
        _put(t.fields, t.field_status, t.errors, name, (f, status))
    elif name in ("marginal", "weighted_average"):
        # "Taux/Prix": a rate for bills (BAT), a price in % of nominal for bonds (OAT).
        if instr == "BAT":
            _put(t.fields, t.field_status, t.errors, f"{name}_rate", _percent(raw, loc, conf))
        elif instr == "OAT":
            _put(t.fields, t.field_status, t.errors, f"{name}_price", _price(raw, loc, conf))
        else:
            t.errors.append(f"{name}: instrument unknown, cannot tell rate from price")
    else:
        _put(t.fields, t.field_status, t.errors, name, builder(raw, loc, conf))


def _parse_single(lines: list[Line], isin_idx: int, doc: ParsedDocument) -> None:
    t = Tranche(0)
    ln = lines[isin_idx]
    m = ISIN_RE.search(ln.text, ln.folded.find("code isin"))
    if m:
        t.fields["isin"] = Field(m.group(), m.group(), ln.loc("Code ISIN"), 0.95)

    def labelled(label: str, name: str, builder, anywhere: bool = True) -> None:
        hit = find_line(lines, label, anywhere=anywhere)
        if not hit:
            t.field_status.setdefault(name, FieldStatus.NOT_DISCLOSED.value)
            return
        i, after = hit
        value = single_amount if builder is _amount_millions else single_value
        _put(t.fields, t.field_status, t.errors, name,
             builder(value(lines[i], after), lines[i].loc(label), 0.95))

    labelled("denomination de l'emission", "security_name", _text)
    hit = find_line(lines, "adjudication n")
    if hit:
        i, after = hit
        raw = single_value(lines[i], after)
        raw = re.sub(r"^[°º]?\s*:?\s*", "", raw)
        _put(t.fields, t.field_status, t.errors, "auction_number", _text(raw, lines[i].loc("Adjudication N°"), 0.95))
    hit = find_line(lines, "duree")
    if hit:
        i, after = hit
        # The tenor cell, with its unit when printed in the next cell ("182      jours").
        cells = merge_unit_cells(tokens_after(lines[i], after))
        _put(t.fields, t.field_status, t.errors, "tenor",
             _tenor(cells[0][1] if cells else "", lines[i].loc("Durée"), 0.95))
    labelled("date d'echeance", "maturity_date", _date)
    labelled("valeur nominale unitaire", "face_value", _face_value)
    labelled("taux d'interet fixe annonce", "coupon_rate", lambda r, l, c: _percent(r, l, c, allow_ratio=True))
    labelled("taux coupon couru", "accrued_coupon_rate", lambda r, l, c: _percent(r, l, c, allow_ratio=True))
    labelled("nombre de participants", "number_of_participants", _integer)
    labelled("nombre de soumissions", "number_of_bids", _integer)
    labelled("montant global des soumissions", "amount_submitted", _amount_millions)
    labelled("soumissions retenues", "amount_allocated", _amount_millions)
    labelled("soumissions rejetees", "amount_rejected", _amount_millions)
    labelled("rendement moyen pondere", "weighted_average_yield", _percent)
    instr = _instrument_from(t.value("security_name"))
    if instr is None:
        nature = _fold(doc.value("security_type") or "")
        instr = "BAT" if "bons" in nature else "OAT" if "obligations" in nature else None
    if instr:
        src = t.fields.get("security_name")
        t.fields["instrument"] = Field(instr, src.raw if src else "", src.locator if src else "", 0.9)
    if instr == "BAT":
        labelled("taux marginal", "marginal_rate", _percent)
        labelled("taux moyen pondere", "weighted_average_rate", _percent)
    elif instr == "OAT":
        labelled("prix marginal", "marginal_price", _price)
        labelled("prix moyen pondere", "weighted_average_price", _price)
    # Absorption is a tranche value as well when the operation has a single security.
    if "absorption_rate" in doc.operation:
        t.fields["absorption_rate"] = replace(doc.operation["absorption_rate"])
    doc.tranches = [t]


# --------------------------------------------------------------------------- checks


def _check(doc: ParsedDocument, name: str, ok: bool, detail: str, tranches: list[Tranche]) -> None:
    """Record a check on the document and on each tranche it involves (only those)."""
    check = {"check": name, "ok": ok, "detail": detail, "data_nature": "CALCULATION"}
    doc.checks.append(check)
    for t in tranches:
        t.checks.append(dict(check))
    if not ok:
        doc.warnings.append(f"check failed: {name} ({detail})")
        for t in tranches:
            for f in t.fields.values():
                f.confidence = round(min(f.confidence, 0.6), 3)


def _tolerance(*fields: Field | None) -> Decimal:
    """Rounding tolerance from the printed precision: amounts printed in millions with
    decimals are exact to 0.005 million; amounts printed as whole millions to 0.5 million."""
    def exact(f: Field | None) -> bool:
        m = NUM_RE.search(f.raw) if f else None
        return bool(m and "," in m.group())

    return sum((Decimal(5_000) if exact(f) else Decimal(500_000) for f in fields), Decimal(0))


def _run_checks(doc: ParsedDocument, operation: dict[str, Field], tranches: list[Tranche]) -> None:
    """Consistency checks (CALCULATION, for the reviewer) of one operation: its published totals
    against its tranches, and each tranche on its own. A failed check lowers confidence; it
    never changes a value, since the document itself may be inconsistent."""

    def dec(v):
        return Decimal(v) if v is not None else None

    def op_value(name):
        f = operation.get(name)
        return f.value if f else None

    if len(tranches) > 1:
        for total, part in (("total_amount_submitted", "amount_submitted"),
                            ("total_amount_allocated", "amount_allocated")):
            tot = dec(op_value(total))
            parts = [dec(t.value(part)) for t in tranches]
            if tot is not None and None not in parts:
                s = sum(parts, Decimal(0))
                tol = _tolerance(operation.get(total), *(t.fields.get(part) for t in tranches))
                _check(doc, f"sum_{part}", abs(s - tot) <= tol,
                       f"sum of tranches {s} vs published total {tot}", tranches)
    for t in tranches:
        names = ("amount_submitted", "amount_allocated", "amount_rejected")
        sub, alloc, rej = (dec(t.value(f)) for f in names)
        if None not in (sub, alloc, rej):
            _check(doc, f"{t.tranche_key}: submitted = allocated + rejected",
                   abs(sub - alloc - rej) <= _tolerance(*(t.fields.get(f) for f in names)),
                   f"{sub} vs {alloc} + {rej}", [t])
        country = (t.operation or operation).get("country_iso3")
        isin, iso3 = t.value("isin"), country.value if country else None
        if isin and iso3:
            _check(doc, f"{t.tranche_key}: ISIN prefix matches issuer",
                   ISIN_PREFIX.get(isin[:2]) == iso3, f"{isin[:2]} vs {iso3}", [t])
        ad, sd, md = t.value("auction_date"), t.value("settlement_date"), t.value("maturity_date")
        if ad and sd and md:
            # "<=": a buyback can settle on the maturity date of the security bought back.
            _check(doc, f"{t.tranche_key}: auction <= settlement <= maturity", ad <= sd <= md,
                   f"{ad} / {sd} / {md}", [t])
        if alloc is not None and alloc == 0:
            doc.warnings.append(
                f"{t.tranche_key}: nothing allotted; published rates/yields are not market yields")


# --------------------------------------------------------------------------- entry point


def _is_buyback(heading: Line | None, d: ParsedDocument) -> bool:
    """A buyback ("rachat") report: by its heading, or by its auction numbers, which UMOA-Titres
    prefixes "RA-" for buybacks ("ADJ-" for issues) — this also covers a misspelt heading
    ("COMPTE RENDU DE RACAHT …") and single reports printed without a heading."""
    if heading is not None and "rachat" in heading.folded:
        return True
    numbers = [t.value("auction_number") for t in d.tranches]
    return bool(numbers) and all(n and n.upper().startswith("RA-") for n in numbers)


def _continues(prev: ParsedDocument, d: ParsedDocument) -> bool:
    """True when buyback section `d` is the next page of the operation reported by `prev`: one
    operation of many securities printed over several pages, each repeating the operation
    header (same auction date and amount offered) while only the first prints the totals."""
    same = all(d.value(k) is not None and d.value(k) == prev.value(k)
               for k in ("auction_date", "total_amount_offered"))
    own_totals = any(d.value(k) is not None for k in ("total_amount_submitted", "total_amount_allocated"))
    return same and not own_totals


def parse_compte_rendu(text: str) -> ParsedDocument:
    """Parse a result report. A PDF may hold several reports (e.g. "EC": an issue report
    followed by a buyback report); each section starting with a "COMPTE RENDU …" heading is
    parsed on its own and the tranches are combined, each keeping its section's facts. A
    buyback printed over several pages (one section per page) is one operation: its sum checks
    run over all its pages. Checks are recorded on the tranches they involve."""
    lines = to_lines(text)
    heads = [i for i, ln in enumerate(lines) if "compte rendu d" in ln.folded]
    bounds = sorted({0, *heads, len(lines)})
    sections: list[tuple[str, ParsedDocument]] = []
    groups: list[list[ParsedDocument]] = []  # sections forming one operation
    for a, b in zip(bounds, bounds[1:]):
        sec = lines[a:b]
        if not any("code isin" in ln.folded for ln in sec):
            continue
        d = _parse_section(sec)
        kind = "buyback" if _is_buyback(sec[0] if a in heads else None, d) else "issue"
        if kind == "buyback" and a in heads and "rachat" not in sec[0].folded:
            d.warnings.append(f"heading {sec[0].text.strip()!r} read as a buyback: auction numbers start with 'RA-'")
        for t in d.tranches:
            t.kind, t.operation = kind, d.operation
        if kind == "buyback" and sections and sections[-1][0] == "buyback" and _continues(groups[-1][0], d):
            groups[-1].append(d)
            d.warnings.append("continuation page of the previous buyback operation (same date and "
                              "amount offered, no totals of its own); checked together with it")
        else:
            groups.append([d])
        sections.append((kind, d))
    if not sections:
        doc = ParsedDocument(layout="unknown")
        doc.warnings.append("no 'Code ISIN' line: not a recognised UMOA-Titres result report")
        return doc
    for group in groups:
        tranches = [t for d in group for t in d.tranches]
        for t in tranches:
            t.operation_tranches = len(tranches)
        _run_checks(group[0], group[0].operation, tranches)
    main = sections[0][1]
    for kind, d in sections[1:]:
        main.layout = f"{main.layout}+{kind}:{d.layout}"
        main.tranches += d.tranches
        main.warnings += [f"[{kind} section] {w}" for w in d.warnings]
        main.checks += d.checks
        main.publication_date = main.publication_date or d.publication_date
    if len(sections) > 1:
        main.warnings.append(f"document holds {len(sections)} reports: " + ", ".join(k for k, _ in sections))
    return main


def _parse_section(lines: list[Line]) -> ParsedDocument:
    doc = ParsedDocument(layout="unknown")
    isin_hit = find_line(lines, "code isin", anywhere=True)
    if isin_hit is None:
        doc.warnings.append("no 'Code ISIN' line: not a recognised UMOA-Titres result report")
        return doc
    isin_idx = isin_hit[0]
    n_isins = len(ISIN_RE.findall(lines[isin_idx].text))
    has_table = any(TRANCHE_RE.search(ln.text) for ln in lines[isin_idx + 1:]) and find_line(
        lines, "taux/prix", anywhere=True) is not None
    doc.layout = "multi_tranche" if (n_isins > 1 or has_table) else "single_tranche"
    # Global block ends where the per-tranche table starts (multi) or at the regional table.
    end_hit = (find_line(lines, "nombre de participants", start=isin_idx) if doc.layout == "multi_tranche"
               else find_line(lines, "resultat global", start=isin_idx))
    end = end_hit[0] if end_hit else len(lines)
    if doc.layout == "multi_tranche":
        head, _ = find_results_head(lines, isin_idx, ISIN_RE.findall(lines[isin_idx].text))
        end = head if head is not None else end
    _operation_fields(lines, doc, end)

    issuer = _fold(doc.value("issuer") or "").upper().replace("ETAT DU ", "").replace(
        "ETAT DE LA ", "").replace("ETAT DE ", "").replace("ETAT D'", "").strip()
    iso3 = next((code for name, code in ISSUERS.items() if issuer.startswith(name)), None)
    if iso3:
        src = doc.operation["issuer"]
        doc.operation["country_iso3"] = Field(iso3, src.raw, src.locator, 0.95, note="mapped from issuer name")
    else:
        doc.warnings.append(f"issuer {doc.value('issuer')!r} not mapped to a WAEMU country")

    if doc.layout == "multi_tranche":
        _parse_multi(lines, isin_idx, doc)
    else:
        _parse_single(lines, isin_idx, doc)

    total_offered = doc.operation.get("total_amount_offered")
    for t in doc.tranches:
        for name in ("auction_date", "settlement_date"):
            if name in doc.operation:
                t.fields[name] = replace(doc.operation[name])
            else:
                t.field_status[name] = doc.operation_status.get(name, FieldStatus.NOT_AVAILABLE.value)
        if len(doc.tranches) == 1 and total_offered:
            t.fields["amount_offered"] = replace(total_offered)
        else:
            t.field_status["amount_offered"] = FieldStatus.NOT_DISCLOSED.value
        if t.value("tenor"):
            _tenor_days(t)
    return doc


def _tenor_days(t: Tranche) -> None:
    src = t.fields["tenor"]
    num, unit = src.value.split()
    n = Decimal(num)
    factor = {"jours": 1, "ans": 365, "semaines": 7}.get(unit)
    if factor is None:
        return
    exact = n * factor
    days = int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP))
    if unit == "jours" and exact == days:
        note = None
    elif n == n.to_integral_value():
        note = f"stated as '{num} {unit}'; stored as days with the platform's 365-day-year bucket convention"
    else:
        # A reopened line printed with its residual tenor ("2,85 ans").
        note = (f"stated as a fractional tenor '{src.raw.strip()}'; converted to days as "
                f"round({num} x {factor}) = {days} (365-day year); not a whole number of {unit}")
    t.fields["tenor_days"] = Field(str(days), src.raw, src.locator, src.confidence, "days", note)
