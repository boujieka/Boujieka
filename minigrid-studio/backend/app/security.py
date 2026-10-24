"""Authentication (argon2 passwords, opaque bearer tokens stored as SHA-256)
and authorisation (role per organisation, optional per-project restriction)."""
from __future__ import annotations

import datetime as dt
import hashlib
import secrets
import time
from collections import defaultdict, deque
from dataclasses import dataclass

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import get_settings
from .db import get_db
from .models import Membership, Project, ProjectMember, Role, SessionToken, User

_ph = PasswordHasher()

# what each role may do
CAN = {
    "read": {Role.admin, Role.analyst, Role.reviewer, Role.investor},
    "read_drafts": {Role.admin, Role.analyst, Role.reviewer},
    "edit": {Role.admin, Role.analyst},
    "review": {Role.admin, Role.reviewer},
    "manage": {Role.admin},
}


def hash_password(pw: str) -> str:
    if len(pw) < 12:
        raise HTTPException(422, "password must have at least 12 characters")
    return _ph.hash(pw)


def verify_password(pw: str, h: str) -> bool:
    try:
        return _ph.verify(h, pw)
    except (VerifyMismatchError, InvalidHashError):
        return False


def _digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def issue_token(db: Session, user: User) -> tuple[str, dt.datetime]:
    token = secrets.token_urlsafe(32)
    exp = dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=get_settings().token_ttl_hours)
    db.add(SessionToken(user_id=user.id, token_hash=_digest(token), expires_at=exp))
    return token, exp


def revoke_token(db: Session, token: str) -> None:
    row = db.scalar(select(SessionToken).where(SessionToken.token_hash == _digest(token)))
    if row:
        row.revoked = True


class LoginLimiter:
    """In-memory, per-process limiter for login attempts (per e-mail and IP)."""
    def __init__(self):
        self.hits: dict[str, deque] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.monotonic()
        q = self.hits[key]
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= get_settings().login_attempts_per_minute:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "too many login attempts, retry in a minute")
        q.append(now)


login_limiter = LoginLimiter()


@dataclass
class Caller:
    user: User
    token: str
    roles: dict[str, Role]  # org_id -> role

    def role_in(self, org_id: str) -> Role | None:
        return self.roles.get(org_id)

    def require(self, org_id: str, capability: str) -> Role:
        role = self.role_in(org_id)
        if role is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")  # do not reveal other tenants
        if role not in CAN[capability]:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"role '{role.value}' may not {capability}")
        return role


def current_caller(request: Request, db: Session = Depends(get_db)) -> Caller:
    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing bearer token",
                            headers={"WWW-Authenticate": "Bearer"})
    token = auth[7:].strip()
    row = db.scalar(select(SessionToken).where(SessionToken.token_hash == _digest(token)))
    now = dt.datetime.now(dt.timezone.utc)
    if row is None or row.revoked or row.expires_at < now:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid or expired token",
                            headers={"WWW-Authenticate": "Bearer"})
    user = db.get(User, row.user_id)
    if user is None or not user.active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "inactive user")
    roles = {m.org_id: m.role for m in db.scalars(select(Membership).where(Membership.user_id == user.id))}
    return Caller(user=user, token=token, roles=roles)


def project_for(db: Session, caller: Caller, project_id: str, capability: str = "read") -> tuple[Project, Role]:
    """Load a project the caller may access with ``capability``; 404 otherwise
    (also for projects of other organisations, so their existence is not leaked)."""
    p = db.get(Project, project_id)
    if p is None or caller.role_in(p.org_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    role = caller.require(p.org_id, capability)
    if p.restricted and role != Role.admin:
        member = db.scalar(select(ProjectMember).where(ProjectMember.project_id == p.id,
                                                       ProjectMember.user_id == caller.user.id))
        if member is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    return p, role
