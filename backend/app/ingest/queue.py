"""Verification queue: list, approve (promote to core tables as VERIFIED) and reject.

Approval is the only path from a staging row to `security`/`auction`. It records who approved
and when (on the row and in the append-only `extraction_review_event` table). Promotion maps
staged fields onto core columns without inventing anything:

  amount_offered          single-security operation: the published amount offered.
                          Multi-security operation: NULL, `not_disclosed` (UMOA-Titres
                          publishes one global amount for all securities together).
  amount_submitted        "Montant global des soumissions" (tranche)
  amount_allocated        "Soumissions retenues" (tranche)
  cutoff_yield            bills (BAT): "Taux marginal". Bonds (OAT): NULL, `not_disclosed`
                          (a marginal *price* is published instead; kept in the staging row).
  weighted_average_yield  "Rendement moyen pondéré"
  average_price           bonds: "Prix moyen pondéré" per 100 of nominal (converted from FCFA
                          per unit when published that way, with a note)
  reported_bid_to_cover   single-security operation: "Taux de couverture … par les soumissions"
                          / 100. Multi-security: NULL, `not_disclosed` (global ratio only).
  number_of_bidders       "Nombre de participants"

When nothing was allotted, the published 0,00 % rates are not market yields: the yield and
price columns stay NULL (`not_disclosed`) and a note says why.
"""

from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ingest.tenor import (
    ORIGINAL_ISSUE,
    TenorEvidence,
    apply_decision,
    original_tenor,
    security_evidence,
)
from app.models import Auction, AuctionExtraction, Country, ExtractionReviewEvent, Issuer, Security
from app.models.enums import (
    AuctionStatus,
    AuctionType,
    DataNature,
    FieldStatus,
    InstrumentType,
    VerificationStatus,
)

INSTRUMENTS = {"BAT": InstrumentType.TREASURY_BILL, "OAT": InstrumentType.TREASURY_BOND}
YIELD_CONVENTION = "UMOA-Titres: rendement moyen pondéré, as published"
ND = FieldStatus.NOT_DISCLOSED.value


class ReviewError(Exception):
    """The requested review action is not allowed (wrong state, missing or conflicting data)."""


@dataclass
class QueuePage:
    items: list[AuctionExtraction]
    total: int


def list_queue(
    session: Session,
    status: VerificationStatus | None = VerificationStatus.UNVERIFIED,
    country: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> QueuePage:
    stmt = select(AuctionExtraction)
    if status is not None:
        stmt = stmt.where(AuctionExtraction.verification_status == status)
    if country:
        stmt = stmt.where(AuctionExtraction.country_iso3 == country.upper())
    total = session.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = session.scalars(
        stmt.order_by(AuctionExtraction.auction_date.desc(), AuctionExtraction.extraction_id)
        .limit(limit)
        .offset(offset)
    ).all()
    return QueuePage(list(items), total)


def _value(ext: AuctionExtraction, name: str) -> str | None:
    f = (ext.fields or {}).get(name)
    return f.get("value") if f else None


def _dec(ext: AuctionExtraction, name: str) -> Decimal | None:
    v = _value(ext, name)
    return Decimal(v) if v is not None else None


def _get_pending(session: Session, extraction_id: int) -> AuctionExtraction:
    ext = session.get(AuctionExtraction, extraction_id)
    if ext is None:
        raise ReviewError(f"extraction {extraction_id} not found")
    if ext.verification_status != VerificationStatus.UNVERIFIED:
        raise ReviewError(
            f"extraction {extraction_id} is already {ext.verification_status.value} "
            f"(by {ext.reviewed_by} at {ext.reviewed_at})"
        )
    return ext


def _record(session: Session, ext: AuctionExtraction, action: str, reviewer: str,
            reason: str | None, details: dict) -> None:
    now = datetime.now(timezone.utc)
    ext.reviewed_by, ext.reviewed_at, ext.review_reason = reviewer, now, reason
    session.add(ExtractionReviewEvent(extraction_id=ext.extraction_id, action=action, reviewer=reviewer,
                                      reason=reason, at=now, details=details))


def reject(session: Session, extraction_id: int, reviewer: str, reason: str) -> AuctionExtraction:
    if not reviewer or not reviewer.strip():
        raise ReviewError("a reviewer name is required")
    if not reason or not reason.strip():
        raise ReviewError("a reason is required to reject an extraction")
    ext = _get_pending(session, extraction_id)
    ext.verification_status = VerificationStatus.REJECTED
    _record(session, ext, "rejected", reviewer.strip(), reason.strip(), {})
    session.flush()
    return ext


def _provenance(ext: AuctionExtraction, reviewer: str, notes: list[str]) -> dict:
    doc = ext.document
    return {
        "source_id": ext.source_id,
        "source_document_id": ext.source_document_id,
        "source_url": ext.source_url,
        "publication_date": doc.publication_date if doc else ext.publication_date,
        "extracted_at": ext.extracted_at,
        "verification_status": VerificationStatus.VERIFIED,
        "data_nature": DataNature.FACT,
        "confidence_score": ext.confidence_score,
        "is_synthetic": False,
        "provenance_notes": " ".join(
            [f"Extracted by {ext.extractor} from '{doc.title if doc else ext.source_url}' "
             f"(staging row {ext.extraction_id}); verified against the document by {reviewer} "
             f"on {datetime.now(timezone.utc).date().isoformat()}."] + notes
        ),
    }


def _security(session: Session, ext: AuctionExtraction, country: Country, reviewer: str) -> Security:
    isin = ext.isin
    instrument = INSTRUMENTS[ext.instrument or ""]
    maturity = _value(ext, "maturity_date")
    maturity_date = date.fromisoformat(maturity) if maturity else None
    existing = session.scalar(select(Security).where(Security.isin == isin))
    if existing is not None:
        if existing.is_synthetic:
            raise ReviewError(f"ISIN {isin} belongs to a synthetic security; refusing to mix")
        conflicts = [
            name for name, ours, theirs in (
                ("country", country.country_id, existing.country_id),
                ("instrument_type", instrument, existing.instrument_type),
                ("maturity_date", maturity_date, existing.maturity_date),
            ) if ours is not None and theirs is not None and ours != theirs
        ]
        if conflicts:
            raise ReviewError(f"ISIN {isin} already exists with different {', '.join(conflicts)}; "
                              "reject this extraction or correct the existing security first")
        _refresh_tenor(session, existing, ext)
        return existing

    issuer = session.scalar(
        select(Issuer).where(Issuer.country_id == country.country_id, Issuer.name == f"Government of {country.name}")
    )
    if issuer is None:
        raise ReviewError(f"no sovereign issuer for {country.iso3}: run `python -m app.seed.load` first")
    # The printed Durée of a reopening or buyback is the remaining maturity: tenor_days is the
    # original tenor, decided from all verified operations of this ISIN (app.ingest.tenor).
    decision = original_tenor(*_tenor_inputs(session, isin, ext))
    notes = [f"tenor_days: {decision.note}."]
    security = Security(
        issuer_id=issuer.issuer_id,
        country_id=country.country_id,
        instrument_type=instrument,
        security_name=_value(ext, "security_name") or isin,
        isin=isin,
        currency=country.currency,
        face_value=_dec(ext, "face_value"),
        coupon_rate=_dec(ext, "coupon_rate") if instrument == InstrumentType.TREASURY_BOND else None,
        maturity_date=maturity_date,
        tenor_days=decision.days,
        # A result report does not state these; the notice (Avis d'appel d'offres) does.
        field_status={f: ND for f in ("issue_date", "coupon_frequency", "amortization", "indexation",
                                      "green_social_sustainability_flag", "listing_status",
                                      "minimum_denomination")},
        **_provenance(ext, reviewer, notes),
    )
    if instrument == InstrumentType.TREASURY_BILL:
        security.field_status["coupon_rate"] = ND  # discount instrument
    if decision.days is None:
        security.field_status["tenor_days"] = FieldStatus.NOT_AVAILABLE.value
    session.add(security)
    session.flush()
    return security


def _tenor_inputs(session: Session, isin: str, ext: AuctionExtraction):
    """Evidence for the original tenor: verified staging rows of the ISIN plus the row being approved."""
    rows = list(session.scalars(select(AuctionExtraction).where(
        AuctionExtraction.isin == isin, AuctionExtraction.verification_status == VerificationStatus.VERIFIED)))
    rows = [r for r in rows if r.extraction_id != ext.extraction_id] + [ext]
    return [TenorEvidence.from_extraction(r) for r in rows], []


def _refresh_tenor(session: Session, security: Security, ext: AuctionExtraction) -> None:
    """Re-decide an existing security's original tenor now that `ext` is being approved.

    With every promoted auction's staging row at hand the full rule applies (an earlier original
    issue replaces a value taken from a reopening). In a database rebuilt from the versioned export
    (no staging rows for older auctions) the evidence is partial: only an original issue may
    replace a value, and the dates of the known auctions still count when deciding which
    operation came first."""
    evidence, known, complete = security_evidence(session, security, extra=ext)
    decision = original_tenor(evidence, known)
    partial_ok = decision.rule == ORIGINAL_ISSUE or (security.tenor_days is None and decision.days is not None)
    if complete or partial_ok:
        apply_decision(security, decision, datetime.now(timezone.utc).date(), verb="updated")


def approve(session: Session, extraction_id: int, reviewer: str, note: str | None = None) -> Auction:
    if not reviewer or not reviewer.strip():
        raise ReviewError("a reviewer name is required")
    reviewer = reviewer.strip()
    ext = _get_pending(session, extraction_id)
    missing = [n for n, v in (("isin", ext.isin), ("instrument", ext.instrument),
                              ("auction_date", ext.auction_date), ("country", ext.country_iso3)) if not v]
    if missing:
        raise ReviewError(f"cannot promote: missing {', '.join(missing)} (reject, or fix the parser)")
    if ext.instrument not in INSTRUMENTS:
        raise ReviewError(f"unknown instrument {ext.instrument!r}")
    country = session.scalar(select(Country).where(Country.iso3 == ext.country_iso3))
    if country is None:
        raise ReviewError(f"country {ext.country_iso3} not in the reference table")

    security = _security(session, ext, country, reviewer)
    number = _value(ext, "auction_number") or ""
    buyback = (ext.operation or {}).get("operation_kind") == "buyback" or number.upper().startswith("RA-")
    auction_type = AuctionType.BUYBACK if buyback else AuctionType.PRIMARY_AUCTION
    if session.scalar(select(Auction).where(Auction.security_id == security.security_id,
                                            Auction.auction_date == ext.auction_date,
                                            Auction.auction_type == auction_type)) is not None:
        raise ReviewError(f"an auction for {ext.isin} on {ext.auction_date} ({auction_type.value}) "
                          "already exists; reject this duplicate extraction")

    single = (ext.operation or {}).get("tranche_count") == 1
    is_bond = ext.instrument == "OAT"
    allocated = _dec(ext, "amount_allocated")
    notes: list[str] = []
    status = {k: v for k, v in (ext.field_status or {}).items()}
    out_status: dict[str, str] = {}

    cutoff = None if is_bond else _dec(ext, "marginal_rate")
    if is_bond:
        out_status["cutoff_yield"] = ND
        notes.append("Bond auction: a marginal price is published, not a marginal yield.")
    average_price = None
    if is_bond:
        p = ext.fields.get("weighted_average_price")
        if p and p.get("value") is not None:
            average_price = Decimal(p["value"])
            if p.get("unit") == "XOF_per_unit":
                face = _dec(ext, "face_value")
                if not face:
                    raise ReviewError("price published in FCFA per unit but face value unknown")
                average_price = average_price / face * 100
                notes.append(f"average_price converted from {p['value']} FCFA per {face} nominal to per 100.")
    else:
        out_status["average_price"] = ND
    wa_yield = _dec(ext, "weighted_average_yield")
    if allocated is not None and allocated == 0:
        cutoff = wa_yield = average_price = None
        for f in ("cutoff_yield", "weighted_average_yield", "average_price"):
            out_status[f] = ND
        notes.append("Nothing was allotted: the published 0,00% rates are not market yields and are not stored.")

    coverage = (ext.operation or {}).get("coverage_bids_pct", {}).get("value")
    reported_btc = Decimal(coverage) / 100 if single and coverage is not None else None
    if not single:
        out_status["amount_offered"] = ND
        out_status["reported_bid_to_cover"] = ND
        notes.append("Multi-security operation: amount offered and coverage are published only for "
                     "all securities together (kept in the staging row).")
    elif coverage is None:
        out_status["reported_bid_to_cover"] = ND
    else:
        notes.append("reported_bid_to_cover = published 'taux de couverture' / 100.")
    for f in ("minimum_bid", "maximum_bid", "number_of_successful_bidders"):
        out_status[f] = ND
    for src, dst in (("amount_submitted", "amount_submitted"), ("amount_allocated", "amount_allocated"),
                     ("weighted_average_yield", "weighted_average_yield"),
                     ("number_of_participants", "number_of_bidders")):
        if src in status:
            out_status.setdefault(dst, status[src])
    if not is_bond and "marginal_rate" in status:
        out_status.setdefault("cutoff_yield", status["marginal_rate"])
    if note:
        notes.append(f"Reviewer note: {note}")

    participants = _value(ext, "number_of_participants")
    auction = Auction(
        security_id=security.security_id,
        auction_date=ext.auction_date,
        settlement_date=date.fromisoformat(v) if (v := _value(ext, "settlement_date")) else None,
        auction_type=auction_type,
        status=AuctionStatus.COMPLETED,
        amount_offered=_dec(ext, "amount_offered") if single else None,
        amount_submitted=_dec(ext, "amount_submitted"),
        amount_allocated=allocated,
        cutoff_yield=cutoff,
        weighted_average_yield=wa_yield,
        average_price=average_price,
        reported_bid_to_cover=reported_btc,
        number_of_bidders=int(participants) if participants else None,
        yield_convention=YIELD_CONVENTION,
        field_status=out_status,
        **_provenance(ext, reviewer, notes),
    )
    session.add(auction)
    session.flush()
    ext.verification_status = VerificationStatus.VERIFIED
    ext.promoted_auction_id = auction.auction_id
    _record(session, ext, "approved", reviewer, note,
            {"auction_id": auction.auction_id, "security_id": security.security_id})
    session.flush()
    return auction
