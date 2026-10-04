"""Label-anchored parsers for OCRed BEAC notices (parser "beac_resultat/1", "beac_annonce/1").

Input: the two OCR passes of app.ingest.beac_ocr (words with boxes). Each pass is parsed on its
own, by the same rules; the two readings are then put side by side in one staging row per
security ("Code Emission" block). A field's `value` is set only when both passes produced exactly
the same normalised value; otherwise `value` is NULL and field_status says why. Nothing is
corrected, completed or inferred: a value is either read identically twice from the printed page
or left empty.

Layout: words are grouped into printed lines by geometry; a label is any line matching one of
the label patterns below; values are the numeric runs at the right end of lines, in the value
column (right of 55 % of the page width). Each value run goes to the label line vertically nearest
to it (assign_values), never to two labels; a run equidistant from two labels, two runs for one
label, or non-numeric text where the value should be ("6)" read for a "0") leave the field
unreadable.

Result notice ("Communiqué des résultats des adjudications"), per security block:

  label (fr / en)                                          field
  Code Emission / Issuance Code   <ISIN> <BTA|OTA>-<n> [ANS] [coupon %] <maturity>
                                                           isin, instrument_printed, tenor,
                                                           coupon_rate (OTA), maturity_date
  Nombre de SVT du réseau / … of the network                network_size
  Nombre de SVT soumissionnaires|souscripteurs / … bidders number_of_participants
  Montant (total) annoncé / Total amount announced          amount_offered
  Montant total des soumissions|souscriptions / … of bids   amount_submitted
  Montant total servi / Total amount served                 amount_allocated
  Taux|Prix minimum proposé / Minimum rate proposed         minimum_bid
  Taux|Prix maximum proposé                                 maximum_bid
  Taux|Prix limite / Ceiling rate                           marginal_rate (BTA) | marginal_price (OTA)
  Taux|Prix (d'intérêt) moyen pondéré / Weighted average …  weighted_average_yield (BTA) |
                                                           weighted_average_price (OTA)
  Taux de rendement / Weighted average rate of return       printed_yield_rate (kept, not promoted)
  Taux de couverture … (not "… soumissions retenues")       coverage_pct
  Taux de couverture … par les soumissions retenues         coverage_retained_pct (RCA; served/submitted)
  "Séance du <date>" / "<date> session"                     auction_date (document level)

Amounts are printed in millions of FCFA. They are stored in FCFA: the printed decimal number
multiplied by 10^6, exactly (Decimal arithmetic, no rounding: "27 550,19" → 27550190000). The
printed text is kept as `raw`. A number whose separators are ambiguous ("3.400": a dot followed by
three digits may be a thousands separator or a decimal point) is NOT interpreted: NULL with status
`ambiguous_number`. Rates and prices are stored in percent as printed ("7,00%" → 7.00; prices are
per 100 of face value).

Announcement notice ("Communiqué d'annonce"): Code Emission, auction date ("Date limite de
souscription" / "date de l'adjudication"), "Date de règlement" and "Date de valeur", read with the
same two-pass rule. They are used only to fill the settlement date of a result with the same
ISIN and auction date (app.ingest.beac_check).
"""

import re
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingest.beac_ocr import DocumentOcr, Line, PageOcr, Word, cached_ocr
from app.models import AuctionExtraction, SourceDocument
from app.models.enums import DataNature, FieldStatus, VerificationStatus

EXTRACTOR = "beac_resultat/1"
ANNOUNCEMENT_PARSER = "beac_annonce/1"
MILLION = Decimal(1_000_000)
ISIN_PREFIX_COUNTRY = {"CM": "CMR", "CF": "CAF", "TD": "TCD", "CG": "COG", "GQ": "GNQ", "GA": "GAB"}
COUNTRY_WORDS = {  # folded text printed in the notice (letterhead, body, place of signature) → ISO3
    "CMR": ("cameroun", "cameroon", "yaounde"),
    "CAF": ("centrafricaine", "centrafrique", "central african", "bangui"),
    "TCD": ("tchad", "chad", "n'djamena", "ndjamena"),
    "COG": ("republique du congo", "republic of congo", "congo", "brazzaville"),
    "GNQ": ("guinee equatoriale", "guinee equatorial", "guinea ecuatorial", "equatorial guinea", "malabo"),
    "GAB": ("gabon", "gabonaise", "libreville"),
}

# --------------------------------------------------------------------------- text helpers


def fold(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'").replace("\xa0", " ")
    text = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return " ".join(text.split()).lower()


MONTHS = {
    "janvier": 1, "janv": 1, "jan": 1, "january": 1, "enero": 1, "ener": 1,
    "fevrier": 2, "fevr": 2, "fev": 2, "february": 2, "febuary": 2, "feb": 2, "febrero": 2,
    "mars": 3, "march": 3, "marzo": 3, "marz": 3,
    "avril": 4, "avri": 4, "avr": 4, "april": 4, "abril": 4,
    "mai": 5, "may": 5, "mayo": 5,
    "juin": 6, "june": 6, "junio": 6, "jun": 6,
    "juillet": 7, "juil": 7, "july": 7, "julio": 7,
    "aout": 8, "august": 8, "agosto": 8,
    "septembre": 9, "sept": 9, "september": 9, "septiembre": 9,
    "octobre": 10, "octob": 10, "octo": 10, "oct": 10, "october": 10, "octubre": 10,
    "novembre": 11, "nove": 11, "nov": 11, "november": 11, "noviembre": 11,
    "decembre": 12, "dece": 12, "dec": 12, "december": 12, "diciembre": 12,
}
MONTH_RE = "|".join(sorted(MONTHS, key=len, reverse=True))
# "18-MARS-2027", "08- JANV -2021", "16 septembre — 2028", "21-août-2028", "24 DECE 2026"
DATE_RE = re.compile(rf"\b(\d{{1,2}})(?:er)?\s*[-–—.]?\s*(?:de\s+)?({MONTH_RE})\.?\s*[-–—.,]?\s*(?:del?\s+)?(\d{{4}})(?!\d)")
NUM_DATE_RE = re.compile(r"\b(\d{2})/(\d{2})/(\d{4})\b")
# English: "15th January 2020", "January 15th, 2020"
EN_DATE_RE = re.compile(rf"\b({MONTH_RE})\s+(\d{{1,2}})(?:st|nd|rd|th)?,?\s+(\d{{4}})\b")
EN_DATE_RE2 = re.compile(rf"\b(\d{{1,2}})\s*(?:st|nd|rd|th|\")?\s*(?:of\s+)?({MONTH_RE})\s*,?\s*(\d{{4}})(?!\d)")


def parse_date(text: str) -> tuple[date | None, str | None]:
    """First date in folded text → (date, matched text). Day/month/year must be a real date."""
    t = fold(text)
    for rx, order in ((DATE_RE, "dmy"), (EN_DATE_RE2, "dmy"), (EN_DATE_RE, "mdy")):
        m = rx.search(t)
        if m:
            try:
                if order == "dmy":
                    return date(int(m[3]), MONTHS[m[2]], int(m[1])), m[0]
                return date(int(m[3]), MONTHS[m[1]], int(m[2])), m[0]
            except (ValueError, KeyError):
                return None, m[0]
    m = NUM_DATE_RE.search(t)
    if m:
        try:
            return date(int(m[3]), int(m[2]), int(m[1])), m[0]
        except ValueError:
            return None, m[0]
    return None, None


AMOUNT_RE = re.compile(r"^(\d{1,3}(?: \d{3})+|\d+)(?:,(\d+))?$")
AMBIGUOUS_DOT_RE = re.compile(r"^\d{1,3}(?:\.\d{3})+$")  # "3.400": thousands or decimals?
DECIMAL_DOT_RE = re.compile(r"^(\d+)\.(\d{1,2}|\d{4})$")  # "100.00", "6.25", "7.1667": decimal point
PCT_RE = re.compile(r"^(\d{1,3})(?:[,.](\d{1,4}))?$")


@dataclass
class Number:
    value: Decimal | None
    status: str | None = None  # None, "ambiguous_number", "unreadable"


def parse_amount(raw: str) -> Number:
    """French number as printed (space thousands, comma decimals). No guessing."""
    s = raw.replace(" ", " ").strip()
    s = re.sub(r"\s+", " ", s)
    if AMBIGUOUS_DOT_RE.match(s):
        return Number(None, "ambiguous_number")
    if m := DECIMAL_DOT_RE.match(s):
        return Number(Decimal(f"{m[1]}.{m[2]}"))
    m = AMOUNT_RE.match(s)
    if not m:
        return Number(None, "unreadable")
    whole = m[1].replace(" ", "")
    return Number(Decimal(f"{whole}.{m[2]}") if m[2] else Decimal(whole))


def parse_percent(raw: str) -> Number:
    """'7,00%', '6,0000 %', '96,00', '100.00%' → Decimal in percent. Spaces inside are refused."""
    s = raw.strip().rstrip("%").strip()
    m = PCT_RE.match(s)
    if not m:
        return Number(None, "unreadable")
    return Number(Decimal(f"{m[1]}.{m[2]}") if m[2] else Decimal(m[1]))


# --------------------------------------------------------------------------- line geometry


def build_lines(page: PageOcr) -> list[Line]:
    """Merge tesseract's line segments that sit on the same printed line.

    Tesseract may cut a label and its right-hand value into separate segments (psm 4 usually
    does not, sparse modes always do). Segments are merged when they overlap vertically by at
    least half of the smaller height and do not overlap horizontally."""
    segs = page.lines()
    merged: list[list[Word]] = []
    boxes: list[list[int]] = []
    for seg in sorted(segs, key=lambda s: s.box[0]):
        x0, y0, x1, y1 = seg.box
        best = None
        for i, (bx0, by0, bx1, by1) in enumerate(boxes):
            ov = min(y1, by1) - max(y0, by0)
            if ov >= 0.5 * min(y1 - y0, by1 - by0) and (x0 >= bx1 - 5 or x1 <= bx0 + 5):
                if best is None or ov > best[1]:
                    best = (i, ov)
        if best is None:
            merged.append(list(seg.words))
            boxes.append([x0, y0, x1, y1])
        else:
            i = best[0]
            merged[i].extend(seg.words)
            b = boxes[i]
            boxes[i] = [min(b[0], x0), min(b[1], y0), max(b[2], x1), max(b[3], y1)]
    order = sorted(range(len(merged)), key=lambda i: (boxes[i][1] + boxes[i][3]) / 2)
    return [Line(page.page, n, sorted(merged[i], key=lambda w: w.left)) for n, i in enumerate(order)]


# --------------------------------------------------------------------------- labels

LABELS: list[tuple[str, re.Pattern]] = [
    ("code", re.compile(r"code (d'?)?emission|issuance code|issue code|codigo de (la )?emision")),
    ("network_size", re.compile(r"nombre (de |des )?svt (du|de la) (reseau|red)|primary dealers (of|in) the network")),
    ("number_of_participants", re.compile(
        r"nombre (de |des )?svt (soumissionnaires|souscripteurs|participants|ayant soumissionne)"
        r"|primary dealers as bidders|number of bidders")),
    ("amount_offered", re.compile(r"montant (total )?annonce|amount announced|montant mis en adjudication par le tresor")),
    ("amount_submitted", re.compile(r"montant total des (soumissions|souscriptions)|total amount of bids")),
    ("amount_allocated", re.compile(r"montant total servi|total amount (served|allotted)")),
    ("minimum_bid", re.compile(r"(taux|prix) minimum propose|minimum (rate|price) proposed")),
    ("maximum_bid", re.compile(r"(taux|prix) maximum propose|maximum (rate|price) proposed")),
    ("limit", re.compile(r"(taux|prix) limite|ceiling (rate|price)|marginal (rate|price)")),
    ("weighted_average", re.compile(
        r"(taux|prix) (d'interet |d'interets |d interet )?moyen pondere"
        r"|weighted average (interest )?(rate|price)(?! of return)")),
    ("printed_yield_rate", re.compile(r"taux de rendement|rate of return")),
    ("coverage_retained_pct", re.compile(r"taux de couverture.*retenue")),  # served / submitted (RCA)
    ("coverage_pct", re.compile(r"taux de couverture|coverage rate")),
]
EXCLUDE = {"coverage_pct": re.compile(r"retenue")}
PRICE_LABEL = re.compile(r"\bprix\b|\bprice\b")
# A value token: digits with French/English separators and an optional "%", possibly glued to
# a separator the scan shows next to it (":", "|", quotes, "=", "_", "~"). Letters are never part
# of a value ("6,007o", "ls 000" stay unreadable).
LEAD = r":;|'‘’\"“”=_~"
TRAILING_TOKEN = re.compile(rf"^[{LEAD}]*\d[\d.,]*%?[|.;:'’]*$|^%$")
SEPARATOR_TOKEN = re.compile(r"^[|=+_—–\-.:;'‘’\"“”~]+$")  # table rules, leaders, stray marks


def match_label(text: str) -> tuple[str, re.Match] | None:
    t = fold(text)
    for name, rx in LABELS:
        m = rx.search(t)
        if m and not (name in EXCLUDE and EXCLUDE[name].search(t)):
            return name, m
    return None


def trailing_value(line: Line, min_x: int = 0) -> tuple[str, list[Word]] | None:
    """The run of numeric tokens at the right end of a line (right of `min_x`); separator marks
    after it (a table rule "|") are skipped."""
    words: list[Word] = []
    rev = list(reversed(line.words))
    while rev and SEPARATOR_TOKEN.match(rev[0].text) and rev[0].left >= min_x:
        rev.pop(0)
    for w in rev:
        if w.left < min_x:
            break
        if TRAILING_TOKEN.match(w.text):
            words.insert(0, w)
        else:
            break
    if not words:
        return None
    raw = " ".join(w.text for w in words)
    raw = re.sub(rf"^[{LEAD}]+", "", raw)
    raw = re.sub(r"[|.;:'’]+$", "", raw).strip()
    raw = re.sub(r"\s*%$", "%", raw)
    if not re.search(r"\d", raw):
        return None
    return raw, words


@dataclass
class Reading:
    """One field as read by one OCR pass."""

    raw: str | None
    value: str | None  # normalised (str of Decimal / ISO date / text)
    status: str | None  # why value is None: missing_label, unreadable, ambiguous_number, …
    page: int | None = None
    line: int | None = None
    label: str | None = None
    box: list[int] | None = None  # value tokens, pixels of that pass's raster
    conf: float | None = None  # minimum word confidence of the value tokens
    unit: str | None = None
    note: str | None = None

    def as_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}


def _union(words: list[Word]) -> list[int]:
    return [min(w.left for w in words), min(w.top for w in words),
            max(w.right for w in words), max(w.bottom for w in words)]


# --------------------------------------------------------------------------- code line

CODE_RE = re.compile(
    # The code may be printed (or read) with a space after the country letters ("TD 1200001147")
    # and glued to punctuation ("_GA2K00000017", "GA2J00000127.OTA"): the code is the 12
    # characters without that space; the ISIN check digit (beac_check) guards the reading.
    r"(?<![a-z0-9])([a-z]{2} ?[0-9][0-9a-z]{9})(?![a-z0-9])\s*[-–—:.]?\s*(bta|ota)\s*[-–—]?\s*(\d{1,2})\s*"
    r"(ans|an|years|year|semaines|sem|weeks|s)?\b\s*[-–—]?\s*(?:(\d{1,2}[,.]\d{1,4})\s*%)?\s*[-–—,]?\s*(.*)$")
ISIN_RE = re.compile(r"(?<![A-Za-z0-9])([A-Z]{2} ?[0-9][0-9A-Z]{9})(?![A-Za-z0-9])")


def parse_code_line(text: str) -> dict:
    """'CG1200002133 BTA-26 18-MARS-2027' → parts (all as printed). Empty dict if no match."""
    t = fold(text)
    m = CODE_RE.search(t)
    if not m:
        return {}
    isin = m[1].replace(" ", "").upper()
    instrument = m[2].upper()
    n = int(m[3])
    unit = m[4] or ""
    maturity, maturity_raw = parse_date(m[6] or "")
    out = {"isin": isin, "instrument_printed": instrument, "tenor_n": n, "tenor_unit_raw": unit,
           "maturity_date": maturity.isoformat() if maturity else None, "maturity_raw": maturity_raw}
    if instrument == "BTA":
        out["tenor"] = f"{n} semaines"
    elif unit.startswith(("an", "year")):
        out["tenor"] = f"{n} ans"
    if m[5]:
        out["coupon_rate"] = str(Decimal(m[5].replace(",", ".")))
        out["coupon_raw"] = m[5] + "%"
    return out


# --------------------------------------------------------------------------- one pass


@dataclass
class Block:
    """One security as read by one pass."""

    index: int
    code_text: str
    code: dict
    code_page: int
    code_box: list[int]
    code_conf: float
    readings: dict[str, Reading] = field(default_factory=dict)
    repeats: list[str] = field(default_factory=list)  # code lines of merged copies
    conflicts: set[str] = field(default_factory=set)  # code parts the copies read differently


@dataclass
class PassParse:
    pass_name: str
    auction_date: Reading
    blocks: list[Block]
    text: str
    has_millions: bool
    countries_in_text: list[str]
    operation_words: list[str] = field(default_factory=list)


def _countries(text: str) -> list[str]:
    t = fold(text)
    out = []
    for iso3, words in COUNTRY_WORDS.items():
        if any(w in t for w in words):
            out.append(iso3)
    # "congo" alone also appears in "République démocratique du Congo"? not on BEAC notices.
    return out


SEANCE_RE = re.compile(r"(seance|session|sesion)\b")


def _auction_date(lines: list[Line]) -> Reading:
    """'Séance du 15 septembre 2026' / '15th January 2020 session' (first page only)."""
    for ln in lines:
        if ln.page != 1:
            continue
        t = fold(ln.text)
        if SEANCE_RE.search(t) and not re.search(r"date (de|d')", t):
            d, raw = parse_date(t)
            if raw:
                toks = set(raw.split())
                words = [w for w in ln.words if fold(w.text).strip(".,-–—()") in toks] or ln.words
                return Reading(raw, d.isoformat() if d else None, None if d else "unreadable",
                               ln.page, ln.index, "seance", _union(words), min(w.conf for w in words))
    return Reading(None, None, "missing_label")


VALUE_COLUMN = 0.55  # values are printed right of 55 % of the page width (labels left of it)
NAME_LIKE = re.compile(r"^[A-Za-zÀ-ÿ'’()\-]+[.:]?$")


def _center(words: list[Word]) -> float:
    return sum((w.top + w.bottom) / 2 for w in words) / len(words)


@dataclass
class ValueSlot:
    """What the layout gives a label line: the numeric runs nearest to it, or why none."""

    runs: list[tuple[str, list[Word], int]] = field(default_factory=list)  # (raw, words, line index)
    ambiguous: bool = False


def assign_values(lines: list[Line], widths: dict[int, int]) -> dict[int, ValueSlot]:
    """Give every numeric run of the value column to the label line nearest to it vertically.

    Anchors are the lines carrying a label (or an issue code). Each run (the numbers at the right
    end of a line, right of VALUE_COLUMN) goes to the anchor whose label words are vertically
    nearest, if within 2.5 word heights; a run almost equidistant from two anchors (difference
    under 0.3 word height) is given to neither, and both are marked ambiguous. A run therefore
    serves at most one label, and a value printed slightly above or below its label (two-line
    labels, skewed scans) still finds it, without ever borrowing the neighbouring label's value."""
    heights = sorted(w.height for ln in lines for w in ln.words) or [40]
    h = heights[len(heights) // 2]
    anchors = [i for i, ln in enumerate(lines) if match_label(ln.text) or ISIN_RE.search(ln.text)]
    slots = {i: ValueSlot() for i in anchors}

    def label_center(i: int) -> float:
        ln = lines[i]
        col = int(widths.get(ln.page, 2500) * VALUE_COLUMN)
        left = [w for w in ln.words if w.right <= col] or ln.words
        return _center(left)

    centers = {i: label_center(i) for i in anchors}
    for i, ln in enumerate(lines):
        got = trailing_value(ln, min_x=int(widths.get(ln.page, 2500) * VALUE_COLUMN))
        if got is None:
            continue
        raw, words = got
        yc = _center(words)
        near = sorted((abs(centers[a] - yc), a) for a in anchors if lines[a].page == ln.page)
        if not near or near[0][0] > 2.5 * h:
            continue
        if len(near) > 1 and near[1][0] - near[0][0] < 0.3 * h:
            slots[near[0][1]].ambiguous = slots[near[1][1]].ambiguous = True
            continue
        slots[near[0][1]].runs.append((raw, words, i))
    return slots


def _read_value(lines: list[Line], i: int, name: str, page_width: int, slots: dict[int, ValueSlot]) -> Reading:
    """Value of the label on line i, from assign_values. Never guessed: unreadable when the layout
    gives the label no run, several runs, or a run equidistant from two labels, or when the label
    line ends, in the value column, with something that is not a number ("6)" read for a "0")."""
    ln = lines[i]
    label_text = ln.text
    col = int(page_width * VALUE_COLUMN)
    slot = slots.get(i, ValueSlot())
    tail = [w for w in ln.words if not SEPARATOR_TOKEN.match(w.text)] or ln.words
    last = tail[-1]
    if (last.left >= col and not TRAILING_TOKEN.match(last.text) and not NAME_LIKE.match(last.text)):
        return Reading(None, None, "unreadable", ln.page, ln.index, label_text,
                       note=f"non-numeric text {last.text!r} in the value column")
    if slot.ambiguous:
        return Reading(None, None, "unreadable", ln.page, ln.index, label_text,
                       note="a value is as close to another label")
    if len(slot.runs) != 1:
        return Reading(None, None, "unreadable", ln.page, ln.index, label_text,
                       note=f"{len(slot.runs)} values near the label" if slot.runs else None)
    raw, words, j = slot.runs[0]
    got = (raw, words)
    raw, words = got
    # Confidence of the characters that make the value: pure punctuation tokens ("%", ":") are
    # left out (tesseract scores an isolated "%" low even when the digits are sharp).
    conf = min((w.conf for w in words if re.search(r"\d", w.text)), default=0.0)
    unit = None
    note = None
    if name in ("amount_offered", "amount_submitted", "amount_allocated"):
        num = parse_amount(raw.rstrip("%"))
        if raw.endswith("%"):
            num = Number(None, "unreadable")
        value = str(num.value * MILLION) if num.value is not None else None
        unit = "XAF"
        note = "printed in millions of FCFA; stored = printed number x 10^6 (exact)"
    elif name in ("network_size", "number_of_participants"):
        num = parse_amount(raw) if re.fullmatch(r"\d{1,3}", raw) else Number(None, "unreadable")
        value = str(int(num.value)) if num.value is not None else None
    else:
        num = parse_percent(raw)
        value = str(num.value) if num.value is not None else None
        unit = "percent"
    return Reading(raw, value, num.status, ln.page, lines[j].index, label_text, _union(words), conf, unit, note)


def parse_pass(ocr_pages: list[PageOcr], pass_name: str) -> PassParse:
    lines: list[Line] = []
    widths = {}
    for p in ocr_pages:
        lines += build_lines(p)
        widths[p.page] = p.width
    text = "\n".join(ln.text for ln in lines)
    blocks: list[Block] = []
    first_code = next((i for i, ln in enumerate(lines) if parse_code_line(ln.text)), len(lines))
    intro = "\n".join(ln.text for ln in lines[:first_code])
    slots = assign_values(lines, widths)
    current: Block | None = None
    for i, ln in enumerate(lines):
        m = match_label(ln.text)
        # A code printed without its label (in a box on its own line) must start the line.
        bare_code = m is None and re.match(r"^\W{0,3}[A-Z]{2} ?[0-9A-Z]{10}\s*[-–—:.]?\s*(BTA|OTA)\b", ln.text, re.I)
        if (m and m[0] == "code") or bare_code:
            code = parse_code_line(ln.text)
            if bare_code and not code:
                continue
            # Confidence of the code itself: the word carrying the ISIN (the other parts of the
            # code line are guarded by the consistency checks (e) of beac_check).
            start = next((k for k, w in enumerate(ln.words) if code.get("isin") and code["isin"] in w.text.upper()), 0)
            conf = ln.words[start].conf if code.get("isin") else 0.0
            if not code and current is not None and current.code and not current.readings:
                # "Code Emission" label read just below its value line (value printed level with
                # the label): the label belongs to the block that value line opened.
                continue
            if bare_code and current is not None and not current.code and not current.readings:
                # "Code Emission :" alone on the line above: this line is its value.
                current.code, current.code_text, current.code_box, current.code_conf = code, ln.text, list(ln.box), conf
                continue
            current = Block(len(blocks), ln.text, code, ln.page, list(ln.box), conf)
            blocks.append(current)
            continue
        if m is None or current is None:
            continue
        name = m[0]
        if name in current.readings and current.readings[name].value is not None:
            continue  # first reading of a label in a block wins; a repeat is recorded as a warning
        r = _read_value(lines, i, name, widths.get(ln.page, 2500), slots)
        r.note = (r.note + "; " if r.note else "") + ("price" if PRICE_LABEL.search(fold(ln.text)) else "rate") \
            if name in ("minimum_bid", "maximum_bid", "limit", "weighted_average") else r.note
        current.readings[name] = r
    return PassParse(pass_name, _auction_date(lines), consolidate(blocks), text,
                     "million" in fold(text), _countries(text), _operation_words(intro))


OPERATION_WORDS = re.compile(r"syndi?y?cation|syndication|rachat|buyback|recompra|echange|switch")


def _operation_words(text: str) -> list[str]:
    """Words saying the operation is not a plain auction (syndication, buyback, exchange), in the
    title and opening sentence (the text before the first issue code)."""
    return sorted({m[0] for m in OPERATION_WORDS.finditer(fold(text))})


def _same_security(first: "Block", blk: "Block") -> bool:
    """An ISIN-less block is a repeat (other-language copy) of `first` only if at least three of
    its values were read and every one equals the value read in `first`."""
    common = [k for k, r in blk.readings.items() if r.value is not None
              and first.readings.get(k) is not None and first.readings[k].value is not None]
    return len(common) >= 3 and all(first.readings[k].value == blk.readings[k].value for k in common)


def consolidate(blocks: list[Block]) -> list[Block]:
    """Merge blocks of one pass that describe the same security (bilingual notices print the
    results twice, in French then in English): same ISIN, or no readable ISIN and identical
    values (see _same_security). A field read differently in two copies becomes unreadable
    ("repeat_disagreement"); a field missing in one copy keeps the other's reading. Merging can
    only remove values, never add one that a copy did not print."""
    out: list[Block] = []
    by_isin: dict[str, Block] = {}
    for blk in blocks:
        isin = blk.code.get("isin")
        first = by_isin.get(isin) if isin else None
        if first is None and not isin:
            first = next((b for b in reversed(out) if _same_security(b, blk)), None)
        if first is None:
            blk.index = len(out)
            out.append(blk)
            if isin:
                by_isin[isin] = blk
            continue
        first.repeats.append(blk.code_text)
        if isin:
            for k in ("maturity_date", "coupon_rate", "tenor", "instrument_printed"):
                if k in first.conflicts or blk.code.get(k) is None:
                    continue
                if first.code.get(k) is None:
                    first.code[k] = blk.code[k]  # unreadable in the first copy, read in this one
                elif first.code[k] != blk.code[k]:
                    first.code[k] = None  # the copies disagree: unreadable for good
                    first.conflicts.add(k)
        for name, r in blk.readings.items():
            mine = first.readings.get(name)
            if mine is None or (mine.value is None and r.value is not None and mine.status != "repeat_disagreement"):
                first.readings[name] = r
            elif r.value is not None and mine.value is not None and r.value != mine.value:
                first.readings[name] = Reading(mine.raw, None, "repeat_disagreement", mine.page, mine.line,
                                               mine.label, mine.box, mine.conf, mine.unit,
                                               f"copies read {mine.raw!r} and {r.raw!r}")
    return out


# --------------------------------------------------------------------------- both passes → rows


@dataclass
class StagedField:
    value: str | None
    status: str | None
    readings: dict[str, dict]
    unit: str | None = None
    note: str | None = None

    def as_dict(self) -> dict:
        a = self.readings.get("A", {})
        d = {"value": self.value, "raw": a.get("raw"), "locator": _locator(a), "confidence": _conf(self),
             "ocr": self.readings}
        if self.unit:
            d["unit"] = self.unit
        if self.note:
            d["note"] = self.note
        if self.status:
            d["status"] = self.status
        return d


def _locator(r: dict) -> str | None:
    if not r or r.get("page") is None:
        return None
    return f"p{r['page']}:L{r.get('line')} '{r.get('label') or ''}' box={r.get('box')} (pass A, {300} dpi)"


def _conf(f: StagedField) -> float | None:
    cs = [r.get("conf") for r in f.readings.values() if r.get("conf") is not None]
    return round(min(cs) / 100, 3) if cs else None


def combine(name: str, a: Reading | None, b: Reading | None) -> StagedField:
    ra = a.as_dict() if a else {"status": "missing_label"}
    rb = b.as_dict() if b else {"status": "missing_label"}
    readings = {"A": ra, "B": rb}
    va, vb = (a.value if a else None), (b.value if b else None)
    unit = (a or b).unit if (a or b) else None
    note = (a or b).note if (a or b) else None
    if va is not None and va == vb:
        return StagedField(va, None, readings, unit, note)
    if va is None and vb is None:
        sa, sb = ra.get("status"), rb.get("status")
        status = "not_printed" if sa == sb == "missing_label" else (sa if sa == sb else f"{sa}/{sb}")
        return StagedField(None, status, readings, unit, note)
    return StagedField(None, "ocr_disagreement", readings, unit, note)


@dataclass
class StagedRow:
    tranche_key: str
    fields: dict[str, StagedField]
    operation: dict
    warnings: list[str]


def _code_reading(block: Block | None, key: str) -> Reading | None:
    if block is None:
        return None
    v = block.code.get(key)
    raw = block.code_text
    if v is None and key == "coupon_rate" and block.code.get("instrument_printed") == "BTA":
        return Reading(None, None, "missing_label")  # bills carry no coupon
    return Reading(raw, None if v is None else str(v), None if v is not None else "unreadable",
                   block.code_page, None, "code", block.code_box, block.code_conf if key == "isin" else None)


def rows_from_passes(pa: PassParse, pb: PassParse) -> list[StagedRow]:
    """Pair the blocks of the two passes (by ISIN when both read one, else by order when both
    passes found the same number of blocks) and combine every field."""
    rows: list[StagedRow] = []
    warnings: list[str] = []
    pairs: list[tuple[Block | None, Block | None]] = []
    b_by_isin = {blk.code.get("isin"): blk for blk in pb.blocks if blk.code.get("isin")}
    used_b: set[int] = set()
    for blk in pa.blocks:
        other = b_by_isin.get(blk.code.get("isin"))
        if other is None and len(pa.blocks) == len(pb.blocks):
            other = pb.blocks[blk.index]
        if other is not None and other.index in used_b:
            other = None
        if other is not None:
            used_b.add(other.index)
        pairs.append((blk, other))
    pairs += [(None, blk) for blk in pb.blocks if blk.index not in used_b]
    if len(pa.blocks) != len(pb.blocks):
        warnings.append(f"pass A found {len(pa.blocks)} security block(s), pass B {len(pb.blocks)}")

    date_f = combine("auction_date", pa.auction_date, pb.auction_date)
    for n, (ba, bb) in enumerate(pairs):
        fields: dict[str, StagedField] = {}
        for key in ("isin", "instrument_printed", "tenor", "maturity_date", "coupon_rate"):
            fields[key] = combine(key, _code_reading(ba, key), _code_reading(bb, key))
        names = ("network_size", "number_of_participants", "amount_offered", "amount_submitted",
                 "amount_allocated", "minimum_bid", "maximum_bid", "limit", "weighted_average",
                 "printed_yield_rate", "coverage_pct", "coverage_retained_pct")
        for key in names:
            fields[key] = combine(key, ba.readings.get(key) if ba else None, bb.readings.get(key) if bb else None)
        fields["auction_date"] = date_f
        isin = fields["isin"].value
        key = isin or f"block-{n + 1}"
        op = {"layout": "beac_communique_resultats", "securities_in_notice": len(pairs), "block_index": n,
              "has_millions_label": {"A": pa.has_millions, "B": pb.has_millions},
              "countries_in_text": {"A": pa.countries_in_text, "B": pb.countries_in_text},
              "operation_words": {"A": pa.operation_words, "B": pb.operation_words},
              "code_line": {"A": ba.code_text if ba else None, "B": bb.code_text if bb else None}}
        rows.append(StagedRow(key, fields, op, list(warnings)))
    return rows


# --------------------------------------------------------------------------- announcements

ANN_LABELS = [
    ("code", re.compile(r"code (d'?)?emission|issuance code|codigo")),
    ("auction_date", re.compile(r"date (limite )?de (souscription|soumission|l'adjudication|adjudication)|date de la seance"
                                r"|auction date|subscription deadline|date of (the )?auction")),
    ("settlement_date", re.compile(r"date de reglement|settlement date|fecha de (pago|liquidacion)")),
    ("value_date", re.compile(r"date de valeur|value date|fecha valor")),
]


@dataclass
class AnnouncementBlock:
    isin: str | None
    dates: dict[str, Reading]


INTRO_RE = re.compile(r"procedera,?\s+(le\s+)?|will (proceed|issue),? on\s+|procedera el\s+")


def _date_reading(ln: Line, text_after: str, label: str) -> Reading:
    d, raw = parse_date(text_after)
    return Reading(raw, d.isoformat() if d else None, None if d else ("unreadable" if raw else "missing_value"),
                   ln.page, ln.index, label, list(ln.box), min(w.conf for w in ln.words))


def parse_announcement_pass(ocr_pages: list[PageOcr]) -> list[AnnouncementBlock]:
    """Code blocks of an announcement, each with its dates. Dates printed after a run of several
    codes (a multi-line issue) apply to every code of the run; a code printed twice (French and
    English copies) is one block whose dates must agree. When no "date limite de souscription"
    line is found, the auction date is the one of the opening sentence ("Le Trésor … procèdera le
    lundi 25 août 2025 à l'émission …"), if printed before the first code."""
    lines: list[Line] = []
    for p in ocr_pages:
        lines += build_lines(p)
    blocks: list[AnnouncementBlock] = []
    group: list[AnnouncementBlock] = []
    group_closed = False
    intro: Reading | None = None
    for ln in lines:
        t = fold(ln.text)
        if not blocks and intro is None and (m := INTRO_RE.search(t)):
            r = _date_reading(ln, t[m.end():], "intro sentence")
            if r.value:
                intro = r
        for name, rx in ANN_LABELS:
            if not rx.search(t):
                continue
            if name == "code":
                code = parse_code_line(ln.text)
                m = ISIN_RE.search(ln.text)
                blk = AnnouncementBlock(code.get("isin") or (m[1].replace(" ", "") if m else None), {})
                blocks.append(blk)
                if group_closed:
                    group, group_closed = [], False
                group.append(blk)
            elif group:
                r = _date_reading(ln, t[rx.search(t).end():], ln.text)
                for blk in group:
                    blk.dates.setdefault(name, r)
                group_closed = True
            break
    if intro is not None:
        for blk in blocks:
            if blk.dates.get("auction_date") is None or blk.dates["auction_date"].value is None:
                blk.dates["auction_date"] = intro
    merged: dict[str | None, AnnouncementBlock] = {}
    out: list[AnnouncementBlock] = []
    for blk in blocks:
        first = merged.get(blk.isin) if blk.isin else None
        if first is None:
            out.append(blk)
            if blk.isin:
                merged[blk.isin] = blk
            continue
        for name, r in blk.dates.items():
            mine = first.dates.get(name)
            if mine is None or (mine.value is None and r.value is not None and mine.status != "repeat_disagreement"):
                first.dates[name] = r
            elif r.value is not None and mine.value is not None and r.value != mine.value:
                first.dates[name] = Reading(mine.raw, None, "repeat_disagreement", mine.page, mine.line, mine.label)
    return out


def parse_announcement(ocr: DocumentOcr) -> list[dict]:
    """[{isin, auction_date, settlement_date, value_date}] agreed by both passes (values NULL
    where the passes disagree), with both readings."""
    pa = parse_announcement_pass(ocr.passes["A"].pages)
    pb = parse_announcement_pass(ocr.passes["B"].pages)
    out = []
    b_by = {b.isin: b for b in pb if b.isin}
    for a in pa:
        b = b_by.get(a.isin)
        rec = {"isin": a.isin if b is not None else None, "isin_readings": {"A": a.isin, "B": b.isin if b else None}}
        for name in ("auction_date", "settlement_date", "value_date"):
            f = combine(name, a.dates.get(name), b.dates.get(name) if b else None)
            rec[name] = f.value
            rec[f"{name}_detail"] = f.as_dict()
        out.append(rec)
    return out


# --------------------------------------------------------------------------- staging


def _instrument_for_queue(printed: str | None) -> str | None:
    # app.ingest.queue.approve knows the UMOA codes: BAT = treasury bill, OAT = treasury bond.
    # BEAC's BTA (Bons du Trésor Assimilables) and OTA (Obligations du Trésor Assimilables) are the
    # same two instrument types; the printed code is kept in fields["instrument_printed"].
    return {"BTA": "BAT", "OTA": "OAT"}.get(printed or "")


def queue_fields(row: StagedRow) -> tuple[dict, dict]:
    """Staged fields, plus the names app.ingest.queue.approve reads, and field_status.

    approve() reads `marginal_rate` (bills) and `weighted_average_yield` / `weighted_average_price`;
    they are copies of BEAC's "limite" and "moyen pondéré" readings under those names."""
    f = row.fields
    instrument = f["instrument_printed"].value
    is_bond = instrument == "OTA"
    out: dict[str, dict] = {k: v.as_dict() for k, v in f.items()}
    status: dict[str, str] = {}
    for k, v in f.items():
        if v.value is None and v.status:
            status[k] = (FieldStatus.NOT_DISCLOSED.value if v.status == "not_printed"
                         else FieldStatus.NOT_AVAILABLE.value)
    if instrument == "BTA":
        out.pop("coupon_rate", None)
        status.pop("coupon_rate", None)
    if instrument:
        avg, lim = ("weighted_average_price", "marginal_price") if is_bond else ("weighted_average_yield", "marginal_rate")
        out[avg] = f["weighted_average"].as_dict()
        out[lim] = f["limit"].as_dict()
        for alias, src in ((avg, "weighted_average"), (lim, "limit")):
            if src in status:
                status[alias] = status[src]
    if is_bond:
        status["weighted_average_yield"] = FieldStatus.NOT_DISCLOSED.value  # a price is published
    # Settlement date: only from a matching announcement (app.ingest.beac_check).
    status["settlement_date"] = FieldStatus.NOT_AVAILABLE.value
    return out, status


def stage_rows(session: Session, doc: SourceDocument, rows: list[StagedRow], ocr_signature: str) -> list[AuctionExtraction]:
    from app.ingest.beac import ATTRIBUTION

    staged = []
    for row in rows:
        ext = session.scalar(select(AuctionExtraction).where(
            AuctionExtraction.source_document_id == doc.document_id,
            AuctionExtraction.tranche_key == row.tranche_key))
        if ext is not None and ext.verification_status != VerificationStatus.UNVERIFIED:
            continue  # already decided: never touched again
        if ext is None:
            ext = AuctionExtraction(source_document_id=doc.document_id, tranche_key=row.tranche_key)
            session.add(ext)
        fields, status = queue_fields(row)
        printed = row.fields["instrument_printed"].value
        isin = row.fields["isin"].value
        prefix_country = ISIN_PREFIX_COUNTRY.get((isin or "")[:2])
        ad = row.fields["auction_date"].value
        ext.extractor = EXTRACTOR
        required = ("isin", "instrument_printed", "auction_date", "amount_offered", "amount_submitted",
                    "amount_allocated", "coverage_pct")
        ext.parse_status = "complete" if all(row.fields[k].value is not None for k in required) else "partial"
        ext.country_iso3 = prefix_country
        ext.isin = isin
        ext.instrument = _instrument_for_queue(printed)
        ext.auction_date = date.fromisoformat(ad) if ad else None
        ext.fields = fields
        ext.field_status = status
        cov = row.fields["coverage_pct"]
        ext.operation = {**row.operation, "operation_kind": "issue",
                         # Each BEAC security block prints its own announced amount and coverage:
                         # the amount offered and the coverage ratio belong to this security alone.
                         "tranche_count": 1,
                         "coverage_bids_pct": cov.as_dict(),
                         "ocr_signature": ocr_signature,
                         "attribution": ATTRIBUTION,
                         "document_sha256": doc.content_sha256}
        ext.warnings = list(row.warnings)
        ext.checks = []
        ext.source_id = doc.source_id
        ext.source_url = doc.url
        ext.publication_date = doc.publication_date
        ext.extracted_at = datetime.now(timezone.utc)
        ext.data_nature = DataNature.FACT
        ext.verification_status = VerificationStatus.UNVERIFIED
        ext.is_synthetic = False
        confs = [v.get("confidence") for v in fields.values() if isinstance(v, dict) and v.get("confidence") is not None]
        ext.confidence_score = Decimal(str(min(confs))) if confs else None
        ext.provenance_notes = (f"Extracted by {EXTRACTOR} (double OCR) from '{doc.title}' "
                                f"(SHA-256 {doc.content_sha256}). UNVERIFIED until app.ingest.beac_check. "
                                + ATTRIBUTION)
        staged.append(ext)
    session.flush()
    return staged


def ocr_document(doc: SourceDocument) -> DocumentOcr:
    return cached_ocr(Path(doc.storage_path or ""))


def extract_result(session: Session, doc: SourceDocument, ocr: DocumentOcr) -> list[AuctionExtraction]:
    pa = parse_pass(ocr.passes["A"].pages, "A")
    pb = parse_pass(ocr.passes["B"].pages, "B")
    rows = rows_from_passes(pa, pb)
    keys = {r.tranche_key for r in rows}
    for stale in session.scalars(select(AuctionExtraction).where(
            AuctionExtraction.source_document_id == doc.document_id,
            AuctionExtraction.verification_status == VerificationStatus.UNVERIFIED)):
        if stale.tranche_key not in keys:
            session.delete(stale)  # an unreviewed row a previous parser version made; reviewed rows stay
    if not rows:
        doc.extraction_status = "failed"
        return []
    staged = stage_rows(session, doc, rows, ocr.signature)
    doc.extraction_status = "complete" if all(r.parse_status == "complete" for r in staged) else "partial"
    return staged


# Pages OCRed per document type: results run to 1-2 pages (bilingual and multi-security notices
# use 2-3); the dates of an announcement are on its first page (page 2+ lists the dealers).
MAX_PAGES = {"auction_result": 3, "auction_announcement": 1}


def _ocr_job(job: tuple[str, int]) -> tuple[str, str | None]:
    path, max_pages = job
    try:
        cached_ocr(Path(path), max_pages=max_pages)
        return path, None
    except Exception as e:  # noqa: BLE001 - reported, never fatal for the run
        return path, f"{type(e).__name__}: {e}"[:300]


def extract_stored(session: Session, kinds: set[str], workers: int = 4,
                   log: Callable[[str], None] = lambda _: None, run_ocr: bool = True) -> dict:
    """OCR (cached) every stored BEAC result/announcement document, then stage result rows."""
    from concurrent.futures import ProcessPoolExecutor

    from app.ingest.beac import DOCUMENT_TYPES, get_or_create_source

    source = get_or_create_source(session)
    types = [DOCUMENT_TYPES[k] for k in kinds if k in ("result", "announcement")]
    docs = list(session.scalars(select(SourceDocument).where(
        SourceDocument.source_id == source.source_id, SourceDocument.document_type.in_(types))
        .order_by(SourceDocument.document_id)))
    stats = {"documents": len(docs), "ocr_errors": 0, "staged_rows": 0, "missing_file": 0, "errors": []}
    paths = [(d.storage_path, MAX_PAGES.get(d.document_type, 3)) for d in docs
             if d.storage_path and Path(d.storage_path).is_file()]
    stats["missing_file"] = len(docs) - len(paths)
    with ProcessPoolExecutor(max(1, workers)) as ex:
        for n, (path, err) in enumerate(ex.map(_ocr_job, paths if run_ocr else [], chunksize=1), start=1):
            if err:
                stats["ocr_errors"] += 1
                stats["errors"].append(f"{path}: {err}")
            if n % 25 == 0:
                log(f"OCR {n}/{len(paths)}")
    for doc in docs:
        if doc.document_type != DOCUMENT_TYPES["result"] or not doc.storage_path:
            if doc.document_type == DOCUMENT_TYPES["announcement"]:
                doc.extraction_status = "ocr_cached"
            continue
        if re.search(r"rachat|buyback|recompra", fold(doc.title)):
            doc.extraction_status = "unsupported_buyback"  # buyback results: another layout, not parsed
            for stale in session.scalars(select(AuctionExtraction).where(
                    AuctionExtraction.source_document_id == doc.document_id,
                    AuctionExtraction.verification_status == VerificationStatus.UNVERIFIED)):
                session.delete(stale)  # unreviewed rows an earlier parser version made from it
            continue
        cache = Path(doc.storage_path).with_suffix(".ocr.json")
        if not cache.is_file():
            doc.extraction_status = "failed"
            continue
        try:
            with session.begin_nested():
                staged = extract_result(session, doc, DocumentOcr.from_json(cache.read_text(encoding="utf-8")))
        except Exception as e:  # noqa: BLE001
            doc.extraction_status = "failed"
            stats["errors"].append(f"{doc.url}: {type(e).__name__}: {e}"[:300])
            continue
        stats["staged_rows"] += len(staged)
        log(f"{doc.title[:100]}: {doc.extraction_status}, {len(staged)} row(s)")
    session.flush()
    return stats
