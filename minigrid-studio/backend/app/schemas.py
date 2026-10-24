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


class InvitationIn(BaseModel):
    email: EmailStr
    role: RoleName


class InvitationOut(BaseModel):
    id: str
    email: str
    role: RoleName
    expires_at: dt.datetime
    accepted_at: dt.datetime | None = None
    token: str | None = None   # returned once, at creation; deliver it to the invitee out of band


class AcceptInvitationIn(BaseModel):
    token: str = Field(min_length=20, max_length=200)
    name: str | None = Field(default=None, max_length=200)
    password: str | None = Field(default=None, min_length=12, max_length=200)


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


SCENARIO_PATTERN = r"^[A-Za-z0-9_\- ]{1,100}$"


class VersionIn(BaseModel):
    scenario: str = Field(default="base", min_length=1, max_length=100, pattern=SCENARIO_PATTERN)
    template: Literal["demo_fictitious", "crossboundary_reference"] | None = "demo_fictitious"
    assumptions: dict[str, Any] | None = None   # full assumption set instead of a template
    changes: dict[str, Any] = Field(default={}, max_length=200)  # dotted path or workbook cell -> value
    options: dict[str, bool] = {}
    solver_method: Literal["excel_macros", "exact"] = "excel_macros"
    note: str = Field(default="", max_length=5000)


class ReviseIn(BaseModel):
    changes: dict[str, Any] = Field(default={}, max_length=200)
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
    submitted_by: str | None = None
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
