"""Geographical and classification reference data (Master prompt §6, §18, §30)."""

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, Timestamped


class Country(Base, Timestamped):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    iso2: Mapped[str] = mapped_column(String(2), unique=True)
    iso3: Mapped[str] = mapped_column(String(3), unique=True, index=True)
    iso_numeric: Mapped[str | None] = mapped_column(String(3))
    name_en: Mapped[str] = mapped_column(String(120))
    name_fr: Mapped[str] = mapped_column(String(120))
    region: Mapped[str] = mapped_column(String(40))  # African Union region
    subregion: Mapped[str] = mapped_column(String(40))  # UN M49 sub-region
    currency: Mapped[str] = mapped_column(String(3))
    official_languages: Mapped[list] = mapped_column(JSON, default=list)
    # Activation is configuration (AP2I_ACTIVE_COUNTRIES) mirrored here for queries.
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    reporting_config: Mapped[dict] = mapped_column(JSON, default=dict)
    reference_status: Mapped[str] = mapped_column(String(20), default="unverified")
    reference_note: Mapped[str | None] = mapped_column(Text)

    regions: Mapped[list["AdminRegion"]] = relationship(back_populates="country")


class AdminRegion(Base):
    """Administrative divisions (table `regions`). Level 1 = first-level division."""

    __tablename__ = "regions"
    __table_args__ = (UniqueConstraint("country_id", "code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("regions.id"))
    level: Mapped[int] = mapped_column(Integer, default=1)
    code: Mapped[str] = mapped_column(String(20))
    name_en: Mapped[str] = mapped_column(String(120))
    name_fr: Mapped[str] = mapped_column(String(120))
    division_type: Mapped[str] = mapped_column(String(40), default="region")

    country: Mapped[Country] = relationship(back_populates="regions")


class CountryDataSource(Base, Timestamped):
    """Country-specific official sources (ministries, budget, procurement, audit)."""

    __tablename__ = "country_data_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("countries.id"), index=True)
    name: Mapped[str] = mapped_column(String(250))
    institution: Mapped[str] = mapped_column(String(250))
    category: Mapped[str] = mapped_column(String(60))  # budget | finance_law | procurement | audit | ministry | statistics
    url: Mapped[str | None] = mapped_column(Text)
    access_method: Mapped[str] = mapped_column(String(40), default="manual_document_import")
    reachability: Mapped[str] = mapped_column(String(20), default="not_checked")
    last_checked_at: Mapped[str | None] = mapped_column(String(40))
    notes: Mapped[str | None] = mapped_column(Text)


class Sector(Base):
    __tablename__ = "sectors"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True)
    name_en: Mapped[str] = mapped_column(String(80))
    name_fr: Mapped[str] = mapped_column(String(80))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    subsectors: Mapped[list["Subsector"]] = relationship(back_populates="sector")
    indicators: Mapped[list["SectorIndicator"]] = relationship(back_populates="sector")


class Subsector(Base):
    __tablename__ = "subsectors"
    __table_args__ = (UniqueConstraint("sector_id", "code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    sector_id: Mapped[int] = mapped_column(ForeignKey("sectors.id"), index=True)
    code: Mapped[str] = mapped_column(String(40))
    name_en: Mapped[str] = mapped_column(String(120))
    name_fr: Mapped[str] = mapped_column(String(120))

    sector: Mapped[Sector] = relationship(back_populates="subsectors")


class SectorIndicator(Base):
    """Configurable sector indicators (Master prompt §18). Projects do not share one indicator set."""

    __tablename__ = "sector_indicators"
    __table_args__ = (UniqueConstraint("sector_id", "code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    sector_id: Mapped[int] = mapped_column(ForeignKey("sectors.id"), index=True)
    code: Mapped[str] = mapped_column(String(60))
    name_en: Mapped[str] = mapped_column(String(160))
    name_fr: Mapped[str] = mapped_column(String(160))
    unit: Mapped[str] = mapped_column(String(40))
    kind: Mapped[str] = mapped_column(String(20), default="output")  # output | outcome | operational

    sector: Mapped[Sector] = relationship(back_populates="indicators")


class FinancingInstrument(Base):
    __tablename__ = "financing_instruments"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True)
    name_en: Mapped[str] = mapped_column(String(120))
    name_fr: Mapped[str] = mapped_column(String(120))


class Organization(Base, Timestamped):
    """Any institution: government bodies, DFIs, donors, contractors, and AP²I tenants."""

    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250))
    short_name: Mapped[str | None] = mapped_column(String(60))
    org_type: Mapped[str] = mapped_column(String(40), default="other")
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    iati_ref: Mapped[str | None] = mapped_column(String(80), index=True)
    is_tenant: Mapped[bool] = mapped_column(Boolean, default=False)
    website: Mapped[str | None] = mapped_column(Text)


class FinancingPartner(Base, Timestamped):
    """The extensible donor registry (Master prompt §8). Adding a donor = a row + a connector plugin."""

    __tablename__ = "financing_partners"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True)
    name: Mapped[str] = mapped_column(String(250))
    short_name: Mapped[str] = mapped_column(String(40))
    partner_type: Mapped[str] = mapped_column(String(40))  # multilateral | bilateral | un_agency | fund | government
    tier: Mapped[int] = mapped_column(Integer)
    organization_id: Mapped[int | None] = mapped_column(ForeignKey("organizations.id"))
    iati_org_refs: Mapped[list] = mapped_column(JSON, default=list)  # only refs observed in real IATI data
    connector_key: Mapped[str | None] = mapped_column(String(60))
    website: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
