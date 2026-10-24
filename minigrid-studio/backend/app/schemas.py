from __future__ import annotations

import datetime as dt
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

RoleName = Literal["admin", "analyst", "reviewer", "investor"]


class SignupIn(BaseModel):
    organization: str = Field(min_length=2, max_length=200)
    email: EmailStr
    name: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=12, max_length=200)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: dt.datetime


class MembershipOut(BaseModel):
    org_id: str
    organization: str
    role: RoleName


class MeOut(BaseModel):
    id: str
    email: str
    name: str
    memberships: list[MembershipOut]


class MemberIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=12, max_length=200)
    role: RoleName


class MemberOut(BaseModel):
    user_id: str
    email: str
    name: str
    role: RoleName


class RoleIn(BaseModel):
    role: RoleName


class ProjectIn(BaseModel):
    org_id: str
    name: str = Field(min_length=1, max_length=200)
    country: str = Field(default="", max_length=100)
    description: str = Field(default="", max_length=5000)
    restricted: bool = False


class ProjectPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    country: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    restricted: bool | None = None
    archived: bool | None = None


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    org_id: str
    name: str
    country: str
    description: str
    restricted: bool
    archived: bool
    created_at: dt.datetime


class VersionIn(BaseModel):
    scenario: str = Field(default="base", min_length=1, max_length=100, pattern=r"^[A-Za-z0-9_\- ]+$")
    template: Literal["demo_fictitious", "crossboundary_reference"] | None = "demo_fictitious"
    assumptions: dict[str, Any] | None = None   # full assumption set instead of a template
    changes: dict[str, Any] = {}                # dotted path or workbook cell -> value
    options: dict[str, bool] = {}
    solver_method: Literal["excel_macros", "exact"] = "excel_macros"
    note: str = Field(default="", max_length=5000)


class ReviseIn(BaseModel):
    changes: dict[str, Any] = {}
    options: dict[str, bool] | None = None
    solver_method: Literal["excel_macros", "exact"] | None = None
    note: str = Field(default="", max_length=5000)


class ReviewIn(BaseModel):
    decision: Literal["approve", "reject"]
    comment: str = Field(default="", max_length=5000)


class VersionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    project_id: str
    scenario: str
    version: int
    parent_id: str | None
    options: dict
    solver_method: str
    changes: dict
    provenance: dict
    note: str
    content_hash: str
    status: str
    created_by: str
    created_at: dt.datetime
    reviewed_by: str | None
    reviewed_at: dt.datetime | None
    review_comment: str


class VersionDetail(VersionOut):
    assumptions: dict


class RunIn(BaseModel):
    per_lot: bool = False


class RunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    version_id: str
    engine_version: str
    status: str
    inputs_hash: str
    error: str
    duration_ms: int
    created_at: dt.datetime
    result: dict


class AuditOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    org_id: str | None
    user_id: str | None
    action: str
    entity_type: str
    entity_id: str
    payload: dict
    created_at: dt.datetime
