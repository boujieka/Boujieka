"""Ingestion verification queue (admin-oriented, read-only).

Lists staged extractions for reviewers. These rows are deliberately kept out of every public
market-data endpoint and of the Opportunity Engine until a human approves them
(`python -m app.ingest.review approve <id>`), which promotes them to VERIFIED facts.
"""

from typing import Annotated, Literal

from fastapi import APIRouter, Query

from app.api.deps import SessionDep
from app.ingest.queue import list_queue
from app.models.enums import VerificationStatus
from app.schemas import ExtractionDocument, ExtractionOut, Page

# TODO(auth): protect this router with `require_role("analyst")` when the auth module lands
# (e.g. `APIRouter(..., dependencies=[Depends(require_role("analyst"))])`). Until then it must
# not be exposed outside a trusted network: it shows unreviewed extractions.
router = APIRouter(prefix="/ingest", tags=["ingest (admin)"])

STATUS = {"unverified": VerificationStatus.UNVERIFIED, "verified": VerificationStatus.VERIFIED,
          "rejected": VerificationStatus.REJECTED, "all": None}
NOTICE = {
    VerificationStatus.UNVERIFIED: "UNVERIFIED extraction: not a verified fact; awaiting human review.",
    VerificationStatus.VERIFIED: "Approved by a reviewer and promoted to the auction table.",
    VerificationStatus.REJECTED: "Rejected by a reviewer; kept for audit only.",
}


@router.get("/queue", response_model=Page[ExtractionOut])
def ingest_queue(
    session: SessionDep,
    status: Literal["unverified", "verified", "rejected", "all"] = "unverified",
    country: Annotated[str | None, Query(description="ISO3 code")] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Page[ExtractionOut]:
    page = list_queue(session, STATUS[status], country, limit, offset)
    items = [
        ExtractionOut(
            extraction_id=e.extraction_id,
            verification_status=e.verification_status,
            data_nature=e.data_nature,
            notice=NOTICE.get(e.verification_status, ""),
            parse_status=e.parse_status,
            confidence_score=e.confidence_score,
            extractor=e.extractor,
            tranche_key=e.tranche_key,
            country_iso3=e.country_iso3,
            isin=e.isin,
            instrument=e.instrument,
            auction_date=e.auction_date,
            fields=e.fields or {},
            field_status=e.field_status or {},
            operation=e.operation or {},
            warnings=e.warnings or [],
            checks=e.checks or [],
            document=ExtractionDocument.model_validate(e.document) if e.document else None,
            extracted_at=e.extracted_at,
            reviewed_by=e.reviewed_by,
            reviewed_at=e.reviewed_at,
            review_reason=e.review_reason,
            promoted_auction_id=e.promoted_auction_id,
        )
        for e in page.items
    ]
    return Page[ExtractionOut](items=items, total=page.total, limit=limit, offset=offset)
