"""Schémas Pydantic des requêtes."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.models import GRID_STATUSES, JUSTIFICATION_TYPES, LAND_STATUSES, RULE_KINDS, TECHNOLOGIES

Technology = Literal[TECHNOLOGIES]  # type: ignore[valid-type]
RuleKind = Literal[RULE_KINDS]  # type: ignore[valid-type]
JustificationType = Literal[JUSTIFICATION_TYPES]  # type: ignore[valid-type]
LandStatus = Literal[LAND_STATUSES]  # type: ignore[valid-type]
GridStatus = Literal[GRID_STATUSES]  # type: ignore[valid-type]


class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    country_iso3: str = Field(min_length=3, max_length=3, pattern=r"^[A-Za-z]{3}$")
    technology: Technology
    description: str = ""
    is_fictional: bool = False

    @field_validator("country_iso3")
    @classmethod
    def _upper(cls, v: str) -> str:
        return v.upper()


class ProjectPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    technology: Technology | None = None


class SiteIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    geometry: dict[str, Any]
    boundary_source: str = Field(default="Tracé manuel dans l'interface", max_length=300)
    boundary_accuracy_m: float | None = Field(default=None, ge=0)
    repair: bool = False


class SitePatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    geometry: dict[str, Any] | None = None
    boundary_source: str | None = Field(default=None, max_length=300)
    boundary_accuracy_m: float | None = Field(default=None, ge=0)
    land_status: LandStatus | None = None
    land_evidence_dataset_id: int | None = None
    grid_status: GridStatus | None = None
    grid_evidence_dataset_id: int | None = None


class RuleIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    dataset_id: int
    kind: RuleKind
    buffer_m: float = Field(default=0.0, ge=0, le=100_000)
    justification_type: JustificationType = "aucun_buffer"
    justification: str = ""
    weight: float | None = Field(default=None, ge=0, le=1)
    active: bool = True


class RulePatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    kind: RuleKind | None = None
    buffer_m: float | None = Field(default=None, ge=0, le=100_000)
    justification_type: JustificationType | None = None
    justification: str | None = None
    weight: float | None = Field(default=None, ge=0, le=1)
    active: bool | None = None


class AnalysisIn(BaseModel):
    setback_m: float = Field(default=0.0, ge=0, le=10_000)
    setback_justification: str = ""
    rule_ids: list[int] | None = None
    density_mwp_dc_per_ha: float | None = Field(default=None, gt=0, le=5)
    density_justification: str = ""
    force: bool = False
