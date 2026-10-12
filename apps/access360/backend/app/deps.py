"""Request dependencies: current user, organisation membership, roles and the tenant database context."""
from __future__ import annotations

import uuid
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import get_session, set_tenant
from .models import Membership, Organization, User
from .security import read_token

COOKIE = "a360_session"
ROLE_RANK = {"viewer": 0, "analyst": 1, "admin": 2, "owner": 3}
CSRF_HEADER = "x-requested-with"
CSRF_VALUE = "access360"


@dataclass
class Ctx:
    user: User
    mfa: bool
    session: Session


def current_user(request: Request, s: Session = Depends(get_session)) -> Ctx:
    tok = request.cookies.get(COOKIE)
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        tok = auth[7:]
    elif tok and request.method not in ("GET", "HEAD", "OPTIONS"):
        # cookie sessions must send the custom header on state changing requests (CSRF mitigation)
        if request.headers.get(CSRF_HEADER) != CSRF_VALUE:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Missing CSRF header")
    if not tok:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated")
    claims = read_token(tok)
    if not claims:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session expired or invalid")
    user = s.get(User, uuid.UUID(claims["sub"]))
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unknown user")
    return Ctx(user=user, mfa=bool(claims.get("mfa")), session=s)


@dataclass
class OrgCtx(Ctx):
    org: Organization
    role: str


def org_ctx(min_role: str = "viewer", privileged: bool = False):
    """Membership check (API layer) then tenant context for row level security (database layer).
    `privileged` routes (member and settings administration) also require a session established with MFA."""

    def dep(org_id: uuid.UUID, ctx: Ctx = Depends(current_user)) -> OrgCtx:
        s = ctx.session
        m = s.execute(select(Membership).where(Membership.user_id == ctx.user.id, Membership.org_id == org_id)).scalar_one_or_none()
        if m is None:
            # same answer as a missing organisation: do not reveal that it exists
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Organisation not found")
        if ROLE_RANK[m.role] < ROLE_RANK[min_role]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Requires role {min_role} or above")
        if privileged and not (ctx.user.mfa_enabled and ctx.mfa):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Multi factor authentication required for this action")
        org = s.get(Organization, org_id)
        set_tenant(s, org_id)
        return OrgCtx(user=ctx.user, mfa=ctx.mfa, session=s, org=org, role=m.role)

    return dep


def superadmin(ctx: Ctx = Depends(current_user)) -> Ctx:
    if not ctx.user.is_superadmin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Platform administrator only")
    if not (ctx.user.mfa_enabled and ctx.mfa):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Multi factor authentication required for this action")
    return ctx
