"""Request principal, RBAC, tenant isolation, rate limiting and audit helpers."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone

import jwt
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import or_, select, true
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import ApiKey, AuditLog, Plan, Project, Subscription, User, UserRole
from app.reference.catalog import P_ADMIN_ALL, P_READ_PUBLIC
from app.security.core import decode_token, sha256


@dataclass
class Principal:
    user: User | None = None
    roles: set[str] = field(default_factory=set)
    permissions: set[str] = field(default_factory=lambda: {P_READ_PUBLIC})
    organization_id: int | None = None
    features: set[str] = field(default_factory=lambda: {"basic_search", "country_summaries", "public_dashboards"})
    via_api_key: bool = False

    @property
    def is_authenticated(self) -> bool:
        return self.user is not None

    @property
    def is_super_admin(self) -> bool:
        return P_ADMIN_ALL in self.permissions

    def can(self, perm: str) -> bool:
        return perm in self.permissions or self.is_super_admin

    def has_feature(self, feature: str) -> bool:
        return feature in self.features or self.is_super_admin


def _load_principal(db: Session, user: User, via_api_key: bool = False) -> Principal:
    p = Principal(user=user, organization_id=user.organization_id, via_api_key=via_api_key)
    rows = db.scalars(select(UserRole).where(UserRole.user_id == user.id)).all()
    perms = {P_READ_PUBLIC}
    for ur in rows:
        p.roles.add(ur.role.code)
        perms.update(ur.role.permissions or [])
    p.permissions = perms
    feats = set(p.features)
    subs = db.scalars(select(Subscription).where(
        or_(Subscription.user_id == user.id, Subscription.organization_id == user.organization_id) if user.organization_id
        else Subscription.user_id == user.id, Subscription.status.in_(("active", "trial")))).all()
    for s in subs:
        plan = db.get(Plan, s.plan_id)
        if plan:
            feats.update(plan.features or [])
    p.features = feats
    return p


def get_principal(request: Request, db: Session = Depends(get_db)) -> Principal:
    auth = request.headers.get("authorization", "")
    api_key = request.headers.get("x-api-key")
    principal = Principal()
    if api_key:
        row = db.scalar(select(ApiKey).where(ApiKey.key_hash == sha256(api_key), ApiKey.revoked_at.is_(None)))
        if row is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API key")
        user = db.get(User, row.user_id)
        if user is None or not user.is_active:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Inactive account")
        principal = _load_principal(db, user, via_api_key=True)
        if not principal.has_feature("api_access"):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "API access requires an Enterprise subscription")
        row.last_used_at = datetime.now(timezone.utc)
        db.commit()
    elif auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
        try:
            payload = decode_token(token)
        except jwt.PyJWTError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token") from None
        user = db.get(User, int(payload["sub"]))
        if user is None or not user.is_active or user.token_version != payload.get("tv"):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session revoked")
        if user.mfa_enabled and not payload.get("mfa"):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "MFA required")
        principal = _load_principal(db, user)
    request.state.principal = principal
    return principal


def require_user(principal: Principal = Depends(get_principal)) -> Principal:
    if not principal.is_authenticated:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Authentication required")
    return principal


def require(permission: str):
    def dep(principal: Principal = Depends(require_user)) -> Principal:
        if not principal.can(permission):
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Missing permission: {permission}")
        return principal
    return dep


def require_feature(feature: str):
    def dep(principal: Principal = Depends(require_user)) -> Principal:
        if not principal.has_feature(feature):
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Your plan does not include: {feature}")
        return principal
    return dep


def tenant_filter(model, principal: Principal):
    """SQL condition implementing tenant isolation for any model with a tenant_id column.

    Public rows (tenant_id NULL) are visible to everyone; private rows only to members of the owning
    organization holding tenant:read, and to AP²I super administrators.
    """
    if principal.is_super_admin:
        return true()
    if principal.organization_id and principal.can("tenant:read"):
        return or_(model.tenant_id.is_(None), model.tenant_id == principal.organization_id)
    return model.tenant_id.is_(None)


def visible_project_or_404(db: Session, project_ref: str, principal: Principal) -> Project:
    q = select(Project).where(Project.merged_into_id.is_(None))
    if project_ref.isdigit():
        q = q.where(Project.id == int(project_ref))
    else:
        q = q.where(Project.ap2i_id == project_ref)
    q = q.where(tenant_filter(Project, principal))
    p = db.scalar(q)
    if p is None:
        # Same response for "missing" and "not yours": no information leak across tenants.
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    return p


# --- rate limiting (in-process sliding window; use Redis for multi-instance deployments) -----------
class RateLimiter:
    def __init__(self):
        self.hits: dict[str, deque] = defaultdict(deque)

    def check(self, key: str, limit: int, window: float = 60.0) -> float | None:
        now = time.monotonic()
        q = self.hits[key]
        while q and now - q[0] > window:
            q.popleft()
        if len(q) >= limit:
            return window - (now - q[0])
        q.append(now)
        return None

    def reset(self) -> None:
        self.hits.clear()


limiter = RateLimiter()


def client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def truncate_ip(ip: str) -> str:
    if ":" in ip:
        return ":".join(ip.split(":")[:3]) + "::/48"
    parts = ip.split(".")
    return ".".join(parts[:3]) + ".0/24" if len(parts) == 4 else ip


def auth_rate_limit(request: Request) -> None:
    retry = limiter.check(f"auth:{client_ip(request)}", get_settings().auth_rate_limit_per_minute)
    if retry is not None:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many attempts", headers={"Retry-After": str(int(retry) + 1)})


def audit(db: Session, request: Request | None, action: str, principal: Principal | None = None, entity_type: str | None = None,
          entity_id: str | int | None = None, detail: dict | None = None, status_code: int | None = None,
          user_id: int | None = None) -> None:
    db.add(AuditLog(
        user_id=user_id or (principal.user.id if principal and principal.user else None),
        organization_id=principal.organization_id if principal else None, action=action, entity_type=entity_type,
        entity_id=str(entity_id) if entity_id is not None else None,
        method=request.method if request else None, path=str(request.url.path)[:300] if request else None,
        status_code=status_code, ip_truncated=truncate_ip(client_ip(request)) if request else None, detail=detail or {},
    ))
