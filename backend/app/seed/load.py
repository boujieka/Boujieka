"""Idempotent seed loader. Re-running it never duplicates rows.

    python -m app.seed.load                 # reference data only
    python -m app.seed.load --synthetic     # + clearly labelled synthetic market data
"""

import argparse
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Auction, Country, Issuer, Security, Source
from app.models.enums import (
    DataNature,
    IssuerType,
    SourceCategory,
    SourceStatus,
    VerificationStatus,
)
from app.seed import reference, source_candidates, synthetic
from app.seed.africa import BY_ISO3

SYNTHETIC_SOURCE_NAME = "Synthetic seed generator"


def load_reference(session: Session) -> dict[str, Country]:
    countries: dict[str, Country] = {}
    for row in reference.COUNTRIES:
        country = session.scalar(select(Country).where(Country.iso3 == row["iso3"]))
        if country is None:
            country = Country(
                **row,
                data_nature=DataNature.FACT,
                verification_status=VerificationStatus.UNVERIFIED,
                confidence_score=None,
                provenance_notes=reference.UNVERIFIED_NOTE,
            )
            session.add(country)
        # Identity fields from the 54-country table; safe to refresh on every run.
        country.name_fr = BY_ISO3[row["iso3"]].name_fr
        country.region = BY_ISO3[row["iso3"]].region
        countries[row["iso3"]] = country
    session.flush()

    for iso3, country in countries.items():
        name = f"Government of {country.name}"
        if session.scalar(select(Issuer).where(Issuer.name == name)) is None:
            session.add(
                Issuer(
                    country_id=country.country_id,
                    name=name,
                    issuer_type=IssuerType.SOVEREIGN,
                    debt_management_entity=country.debt_management_office,
                )
            )

    for name, institution, category, iso3 in reference.SOURCES:
        source = session.scalar(select(Source).where(Source.name == name))
        if source is None:
            source = Source(
                name=name,
                institution=institution,
                category=category,
                country_id=countries[iso3].country_id if iso3 else None,
                base_url=None,
                status=SourceStatus.PENDING_CONFIGURATION,
                notes="Official URL not yet confirmed by an operator; crawler inactive.",
                crawl_config={},
            )
            session.add(source)
        # Proposals only: base_url is set by an operator, never by the seed.
        candidates = source_candidates.CANDIDATES.get(name, [])
        source.crawl_config = {
            **(source.crawl_config or {}),
            "candidates": candidates,
            "candidates_checked_on": source_candidates.CHECKED_ON if candidates else None,
        }
    session.flush()
    load_subscription_routes(session, countries)
    return countries


def load_subscription_routes(session: Session, countries: dict[str, Country]) -> int:
    """Upsert buyer-access routes (official, quoted) for every country they apply to."""
    from datetime import date as _date

    from app.models import SubscriptionRoute
    from app.seed import subscription_routes as sr

    rows: list[tuple[Country, dict]] = []
    for route in sr.ZONE_ROUTES:
        rows += [(c, route) for c in countries.values() if c.monetary_zone == route["zone"]]
    rows += [(countries[r["iso3"]], r) for r in sr.COUNTRY_ROUTES]

    existing = {
        (r.country_id, r.instrument_type, r.investor_type): r
        for r in session.scalars(select(SubscriptionRoute))
    }
    for country, route in rows:
        key = (country.country_id, route["instrument_type"], route["investor_type"])
        row = existing.get(key) or SubscriptionRoute(
            country_id=country.country_id,
            instrument_type=route["instrument_type"],
            investor_type=route["investor_type"],
        )
        for field in ("eligibility", "primary_dealer", "account_requirement", "submission_method",
                      "settlement_method", "instrument_notes", "quotes"):
            setattr(row, field, route.get(field))
        row.official_source_url = route["source_url"]
        row.last_verified = _date.fromisoformat(sr.VERIFIED_ON)
        session.add(row)
    session.flush()
    return len(rows)


def load_synthetic(session: Session, countries: dict[str, Country], reference_date: date) -> int:
    source = session.scalar(select(Source).where(Source.name == SYNTHETIC_SOURCE_NAME))
    if source is None:
        source = Source(
            name=SYNTHETIC_SOURCE_NAME,
            institution="African Bond Intelligence (development)",
            category=SourceCategory.SYNTHETIC,
            status=SourceStatus.ACTIVE,
            is_synthetic=True,
            notes=synthetic.SYNTHETIC_NOTE,
        )
        session.add(source)
        session.flush()

    # Preload existing synthetic rows so the upsert below costs no per-row queries.
    securities = {
        s.local_code: s for s in session.scalars(select(Security).where(Security.is_synthetic))
    }
    existing = {
        (a.security_id, a.auction_date, a.auction_type): a
        for a in session.scalars(select(Auction).where(Auction.is_synthetic))
    }
    issuers = {i.country_id: i for i in session.scalars(select(Issuer))}

    created = updated = 0
    for iso3, series in synthetic.generate(reference_date).items():
        country = countries[iso3]
        issuer = issuers[country.country_id]
        for sec in series:
            auctions = sec.pop("auctions")
            security = securities.get(sec["local_code"])
            if security is None:
                security = Security(
                    **sec,
                    **synthetic.SYNTHETIC_PROVENANCE,
                    issuer_id=issuer.issuer_id,
                    country_id=country.country_id,
                    currency=country.currency,
                    source_id=source.source_id,
                    field_status={"isin": "not_available"},
                )
                session.add(security)
                session.flush()
                securities[security.local_code] = security
            for a in auctions:
                row = existing.get((security.security_id, a["auction_date"], a["auction_type"]))
                if row is None:
                    session.add(
                        Auction(
                            **a,
                            **synthetic.SYNTHETIC_PROVENANCE,
                            security_id=security.security_id,
                            source_id=source.source_id,
                        )
                    )
                    created += 1
                elif row.status != a["status"]:
                    # Rolling generator: an announced auction gets its synthetic result once held.
                    for key, value in a.items():
                        setattr(row, key, value)
                    updated += 1
    session.flush()
    return created


def reset_synthetic(session: Session) -> int:
    """Delete all synthetic market data and derived signals (used when the generator changes)."""
    from sqlalchemy import delete

    from app.models import Opportunity

    session.execute(delete(Opportunity).where(Opportunity.is_synthetic))
    n = session.execute(delete(Auction).where(Auction.is_synthetic)).rowcount
    session.execute(delete(Security).where(Security.is_synthetic))
    session.flush()
    return n


def main() -> None:
    from app.db import SessionLocal

    parser = argparse.ArgumentParser()
    parser.add_argument("--synthetic", action="store_true", help="also load synthetic data")
    parser.add_argument("--reference-date", type=date.fromisoformat, default=date.today())
    parser.add_argument(
        "--reset-synthetic", action="store_true", help="delete synthetic data before loading"
    )
    args = parser.parse_args()

    with SessionLocal() as session:
        countries = load_reference(session)
        created = 0
        if args.reset_synthetic:
            print(f"Removed {reset_synthetic(session)} synthetic auctions.")
        if args.synthetic:
            created = load_synthetic(session, countries, args.reference_date)
            session.flush()
            from app.engine.opportunities import run as run_engine

            print("Opportunity Engine:", run_engine(session, args.reference_date))
        session.commit()
    print(f"Reference data loaded for {len(countries)} countries; {created} synthetic auctions added.")


if __name__ == "__main__":
    main()
