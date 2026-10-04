"""Original tenor of a security, from official evidence only.

A UMOA-Titres result report prints, per line, a "Durée" and an "Adjudication n°". Both describe
the line *as offered at that operation*: on the original issue they give the security's original
tenor, but on a reopening ("émission simultanée", later re-issue) or a buyback ("RA-…") the Durée
is the REMAINING maturity ("7 jours" for a 364-day bill bought back a week before maturity), and
the auction-number code is often re-labelled to the remaining bucket too (Côte d'Ivoire reopens
1-year bills as "BAT11M", "BAT6M", "BAT2M"; old bonds come back as "OAT9M", "OAT0M").
`security.tenor_days` is the ORIGINAL tenor (it keys the engine's series, the heat grid and the
yield curve), so it is decided here, in this order:

(a) original issue — the earliest known operation of the ISIN is a primary auction whose printed
    Durée is the security's full life, proven by the same document:
      days   "n jours", n in {28, 91, 182, 364} (UMOA-Titres' 4/13/26/52-week terms), and
             maturity − value date = n − 1 or n (the report's own day count);
      bonds  "n ans" (whole n), value date + n calendar years = maturity date exactly, and no
             accrued coupon ("Taux coupon couru" is printed only when the line is reopened).
    Days: as printed for bills; n × 365 for years (the platform's 365-day-year bucket
    convention, same as umoa_extract._tenor_days).
(b) auction-number code — otherwise, the tenor code in the issuance auction numbers of the ISIN
    ("ADJ-TG0000003193-BAT1A-2025", "ADJ-ML0000003854-BT1A-28-2025", "OT5A"), when all usable
    codes agree (disagreeing codes → (c)):
      A = years, M = months (no day code exists in the data). Mapping, verified against the
      Durée printed on original issues carrying the same code:
        bills BAT/BT 1A or 12M → 364, 6M → 182, 3M → 91, 1M → 28 days;
        bonds OAT/OT nA → n × 365 days.
      Not used (they do not determine an original tenor): other bill month codes (2M, 4M, 5M,
      7M–11M: odd terms whose printed Durée varies, mostly residual labels of reopened 1-year
      bills); bond month codes (OATnM: residual labels of old bonds, e.g. OAT0M on a 3-day
      buyback); a code whose instrument family differs from the line; and a code shorter than
      the life already observed (maturity − earliest known value date > code tenor + 3 days),
      which can only be a residual label. Buyback numbers ("RA-…-BAT1A-2024") are not used:
      where the original issue is known they contradicted it (RA-BF0000002824-BAT1A-2024 and
      RA-CI0000007217-BAT1A-2024 on bills issued at "182 jours").
(c) otherwise the original tenor is not available: tenor_days NULL, field_status
    "not_available", with a note. Nothing is guessed.

Limits, measured on the securities whose original issue is known: judged on its own, an issuance
code gives the original tenor for 361 of 383 later auctions; the misses are residual labels that
coincide with a standard term (a 1-year bill reopened at 175 days as "BAT6M"). Rule (a) shares
that blind spot when the original report is missing (a 6-month bill reopened at exactly 91 days is
printed "91 jours", "BAT3M"). Every note therefore names the rule and the document used.
"""

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

ORIGINAL_ISSUE = "original_issue"
AUCTION_CODE = "auction_code"
NOT_AVAILABLE = "not_available"

BILL_FULL_LIFE_DAYS = frozenset({28, 91, 182, 364})
BILL_CODE_DAYS = {("A", 1): 364, ("M", 12): 364, ("M", 6): 182, ("M", 3): 91, ("M", 1): 28}
DAYS_PER_YEAR = 365
CODE_RE = re.compile(r"(?<![A-Z0-9])(BAT|BT|OAT|OT)\s*(\d{1,2})\s*([AM])(?![A-Z0-9])")
FAMILY = {"BAT": "BAT", "BT": "BAT", "OAT": "OAT", "OT": "OAT"}
SLACK_DAYS = 3


@dataclass(frozen=True)
class TenorEvidence:
    """One verified operation of a security, as printed in its official report."""

    extraction_id: int | None
    instrument: str | None  # "BAT" / "OAT"
    auction_date: date | None
    settlement_date: date | None
    maturity_date: date | None
    buyback: bool
    tenor: str | None = None  # normalised by the parser: "364 jours", "3 ans", "2.85 ans"
    tenor_raw: str | None = None
    tenor_locator: str | None = None
    auction_number: str | None = None
    accrued_coupon: Decimal | None = None
    document: str | None = None  # title or URL of the official report

    @property
    def when(self) -> date | None:
        return self.settlement_date or self.auction_date

    def cite(self) -> str:
        bits = [f"auction {self.auction_number or '(no number)'} of {self.auction_date}"]
        if self.document:
            bits.append(f"in '{self.document}'")
        if self.extraction_id is not None:
            bits.append(f"(staging row {self.extraction_id})")
        return " ".join(bits)

    @classmethod
    def from_extraction(cls, ext) -> "TenorEvidence":
        f = ext.fields or {}

        def val(name):
            return (f.get(name) or {}).get("value")

        def day(name):
            v = val(name)
            return date.fromisoformat(v) if v else None

        number = val("auction_number")
        accrued = None
        if val("accrued_coupon_rate") is not None:
            try:
                accrued = Decimal(val("accrued_coupon_rate"))
            except InvalidOperation:
                accrued = None
        doc = getattr(ext, "document", None)
        return cls(
            extraction_id=ext.extraction_id,
            instrument=ext.instrument,
            auction_date=ext.auction_date,
            settlement_date=day("settlement_date"),
            maturity_date=day("maturity_date"),
            buyback=(ext.operation or {}).get("operation_kind") == "buyback"
            or (number or "").strip().upper().startswith("RA-"),
            tenor=val("tenor"),
            tenor_raw=(f.get("tenor") or {}).get("raw"),
            tenor_locator=(f.get("tenor") or {}).get("locator"),
            auction_number=number,
            accrued_coupon=accrued,
            document=(doc.title if doc is not None else None) or ext.source_url,
        )


@dataclass(frozen=True)
class TenorDecision:
    days: int | None
    rule: str  # ORIGINAL_ISSUE / AUCTION_CODE / NOT_AVAILABLE
    note: str
    evidence: TenorEvidence | None = None
    code_days: int | None = None  # what rule (b) gives, when a usable code exists
    conflict: str | None = None  # (a) and (b) disagree


def _add_years(d: date, n: int) -> date:
    try:
        return d.replace(year=d.year + n)
    except ValueError:  # 29 February
        return d.replace(year=d.year + n, day=28)


def _add_months(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    year, month = d.year + y, m + 1
    for day in (d.day, 30, 29, 28):
        try:
            return date(year, month, day)
        except ValueError:
            continue
    raise ValueError(d)


def full_life_days(ev: TenorEvidence) -> int | None:
    """Days of the printed Durée when the same report proves it is the full life of the line."""
    if ev.buyback or not ev.tenor or not ev.settlement_date or not ev.maturity_date:
        return None
    try:
        num, unit = ev.tenor.split()
        n = Decimal(num)
    except (ValueError, InvalidOperation):
        return None
    if n != n.to_integral_value() or n <= 0:
        return None  # "2,85 ans": a residual
    n = int(n)
    life = (ev.maturity_date - ev.settlement_date).days
    if unit in ("jours", "semaines"):
        days = n * (7 if unit == "semaines" else 1)
        if days in BILL_FULL_LIFE_DAYS and days - life in (0, 1):
            return days
        return None
    if unit == "ans":
        if ev.instrument != "OAT" or ev.accrued_coupon:
            return None
        if _add_years(ev.settlement_date, n) == ev.maturity_date:
            return n * DAYS_PER_YEAR
    return None


@dataclass(frozen=True)
class CodeReading:
    code: str
    days: int | None
    reason: str | None  # why it cannot be used (days is None)


def read_code(ev: TenorEvidence, first: date | None) -> CodeReading | None:
    """Rule (b) for one operation: None when its auction number carries no tenor code."""
    m = CODE_RE.search((ev.auction_number or "").upper())
    if not m:
        return None
    prefix, n, unit = m.group(1), int(m.group(2)), m.group(3)
    code = f"{prefix}{n}{unit}"
    family = FAMILY[prefix]
    if ev.buyback:
        return CodeReading(code, None, f"buyback number code {code} is not used (buyback codes contradict "
                                       "the original issue's printed Durée in some reports)")
    if ev.instrument and family != ev.instrument:
        return CodeReading(code, None, f"code {code} does not match the instrument {ev.instrument}")
    if family == "BAT":
        days = BILL_CODE_DAYS.get((unit, n))
        if days is None:
            return CodeReading(code, None, f"bill code {code} has no fixed day count "
                                           "(odd-term or residual label)")
        span = timedelta(days=days)
        issue = ev.maturity_date - span if ev.maturity_date else None
    else:
        if unit == "M":
            return CodeReading(code, None, f"bond code {code} in months is a residual-maturity label")
        days = n * DAYS_PER_YEAR
        issue = _add_years(ev.maturity_date, -n) if ev.maturity_date else None
    if issue is not None and first is not None and issue > first + timedelta(days=SLACK_DAYS):
        return CodeReading(code, None, f"code {code} is shorter than the life already observed "
                                       f"(maturity {ev.maturity_date}, first known operation {first}): "
                                       "a residual label")
    return CodeReading(code, days, None)


def original_tenor(evidence: Iterable[TenorEvidence], known_dates: Iterable[date | None] = ()) -> TenorDecision:
    """Apply rules (a) → (b) → (c). `known_dates` are dates of other known operations of the
    security (e.g. promoted auctions whose staging rows are not available)."""
    evs = sorted((e for e in evidence if e.when is not None), key=lambda e: (e.when, e.extraction_id or 0))
    dates = [e.when for e in evs] + [d for d in known_dates if d is not None]
    if not evs:
        return TenorDecision(None, NOT_AVAILABLE, "no dated operation of this security is available")
    first = min(dates)

    readings = [(e, r) for e in evs if (r := read_code(e, first)) is not None]
    usable = [(e, r) for e, r in readings if r.days is not None]
    distinct = sorted({r.days for _, r in usable})
    code_ev, code = (usable or readings or [(None, None)])[0]
    code_days = distinct[0] if len(distinct) == 1 else None

    original = next(((e, d) for e in evs if e.when == first and (d := full_life_days(e)) is not None), None)
    if original is not None:
        e, days = original
        note = (f"original tenor from the original issue: Durée '{(e.tenor_raw or e.tenor or '').strip()}' "
                f"({e.tenor_locator}) printed for {e.cite()}")
        if (e.tenor or "").endswith("ans"):
            note += f"; {days} days = years x 365 (platform convention)"
        conflict = None
        disagree = [(ce, r) for ce, r in usable if r.days != days]
        if disagree:
            ce, r = disagree[0]
            conflict = (f"auction-number code {r.code} ({ce.auction_number}) gives {r.days} days; "
                        f"the original issue's printed Durée ({days} days) is kept")
            note += f"; note: {conflict}"
        return TenorDecision(days, ORIGINAL_ISSUE, note, e, code_days, conflict)

    if code_days is not None:
        note = (f"original tenor from the auction-number code {code.code} ({code.days} days) in "
                f"{code_ev.cite()}; the original issue is not among the known operations")
        ignored = [(ce, r) for ce, r in readings if r.days is None]
        if ignored:
            note += f" (code {ignored[0][1].code} of {ignored[0][0].auction_number} ignored: {ignored[0][1].reason})"
        return TenorDecision(code_days, AUCTION_CODE, note, code_ev, code_days)

    why = "no known operation is the original issue"
    if len(distinct) > 1:
        codes = ", ".join(f"{r.code} ({ce.auction_number})" for ce, r in usable)
        why += f" and the auction-number codes disagree: {codes}"
        return TenorDecision(None, NOT_AVAILABLE, f"original tenor not available: {why}", code_ev, None,
                             f"codes disagree: {codes}")
    why += f" and {code.reason} ({code_ev.auction_number})" if code is not None else \
        " and no auction number carries a tenor code"
    return TenorDecision(None, NOT_AVAILABLE, f"original tenor not available: {why}", code_ev, None)


# --------------------------------------------------------------------------- database helpers


def security_evidence(session, security, extra=None) -> tuple[list[TenorEvidence], list[date | None], bool]:
    """Verified staging rows of the security's ISIN (plus `extra`, the row being approved), the
    dates of its promoted auctions, and whether every promoted auction has its staging row here
    (False in a database rebuilt from the versioned export, which keeps no staging rows)."""
    from sqlalchemy import select

    from app.models import Auction, AuctionExtraction
    from app.models.enums import VerificationStatus

    rows = list(session.scalars(select(AuctionExtraction).where(
        AuctionExtraction.isin == security.isin,
        AuctionExtraction.verification_status == VerificationStatus.VERIFIED)))
    if extra is not None and all(r.extraction_id != extra.extraction_id for r in rows):
        rows.append(extra)
    auctions = [] if security.security_id is None else list(session.scalars(
        select(Auction).where(Auction.security_id == security.security_id)))
    promoted = {r.promoted_auction_id for r in rows}
    complete = all(a.auction_id in promoted for a in auctions)
    return ([TenorEvidence.from_extraction(r) for r in rows],
            [a.settlement_date or a.auction_date for a in auctions], complete)


def _fmt(days: int | None) -> str:
    return "NULL" if days is None else str(days)


def apply_decision(security, decision: TenorDecision, when: date, verb: str = "corrected") -> bool:
    """Write the decision on the security; on a change, append a dated provenance note.
    Returns True when tenor_days or its status changed."""
    status = dict(security.field_status or {})
    want_status = NOT_AVAILABLE if decision.days is None else None
    if security.tenor_days == decision.days and status.get("tenor_days") == want_status:
        return False
    before = security.tenor_days
    security.tenor_days = decision.days
    if want_status:
        status["tenor_days"] = want_status
    else:
        status.pop("tenor_days", None)
    security.field_status = status  # plain JSON column: reassign so the change is flushed
    line = (f"tenor_days {verb} from {_fmt(before)} to {_fmt(decision.days)} on {when.isoformat()}: "
            f"{decision.note}.")
    security.provenance_notes = f"{security.provenance_notes} {line}" if security.provenance_notes else line
    return True
