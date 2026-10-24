from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import AuditEvent, Membership, Role, User
from ..schemas import AuditOut, MemberIn, MemberOut, RoleIn
from ..security import Caller, current_caller, hash_password
from ..services import audit

router = APIRouter(prefix="/orgs", tags=["organisations"])


@router.get("/{org_id}/members", response_model=list[MemberOut])
def members(org_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    caller.require(org_id, "read_drafts")
    rows = db.execute(select(Membership, User).join(User).where(Membership.org_id == org_id)).all()
    return [MemberOut(user_id=u.id, email=u.email, name=u.name, role=m.role.value) for m, u in rows]


@router.post("/{org_id}/members", response_model=MemberOut, status_code=201)
def add_member(org_id: str, body: MemberIn, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    caller.require(org_id, "manage")
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    if user is None:
        user = User(email=body.email.lower(), name=body.name, password_hash=hash_password(body.password))
        db.add(user)
        db.flush()
    elif db.scalar(select(Membership).where(Membership.user_id == user.id, Membership.org_id == org_id)):
        raise HTTPException(status.HTTP_409_CONFLICT, "already a member")
    db.add(Membership(user_id=user.id, org_id=org_id, role=Role(body.role)))
    audit.record(db, org_id=org_id, user_id=caller.user.id, action="member.add", entity_type="user",
                 entity_id=user.id, payload={"email": user.email, "role": body.role})
    return MemberOut(user_id=user.id, email=user.email, name=user.name, role=body.role)


@router.put("/{org_id}/members/{user_id}", response_model=MemberOut)
def set_role(org_id: str, user_id: str, body: RoleIn, caller: Caller = Depends(current_caller),
             db: Session = Depends(get_db)):
    caller.require(org_id, "manage")
    m = db.scalar(select(Membership).where(Membership.user_id == user_id, Membership.org_id == org_id))
    if m is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    if m.role == Role.admin and body.role != "admin":
        admins = db.scalars(select(Membership).where(Membership.org_id == org_id, Membership.role == Role.admin)).all()
        if len(admins) == 1:
            raise HTTPException(status.HTTP_409_CONFLICT, "an organisation keeps at least one admin")
    old = m.role.value
    m.role = Role(body.role)
    audit.record(db, org_id=org_id, user_id=caller.user.id, action="member.role", entity_type="user",
                 entity_id=user_id, payload={"from": old, "to": body.role})
    u = db.get(User, user_id)
    return MemberOut(user_id=u.id, email=u.email, name=u.name, role=body.role)


@router.get("/{org_id}/audit", response_model=list[AuditOut])
def audit_log(org_id: str, limit: int = Query(100, ge=1, le=1000), caller: Caller = Depends(current_caller),
              db: Session = Depends(get_db)):
    caller.require(org_id, "manage")
    return db.scalars(select(AuditEvent).where(AuditEvent.org_id == org_id)
                      .order_by(AuditEvent.id.desc()).limit(limit)).all()
