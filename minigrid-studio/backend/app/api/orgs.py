from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
import datetime as dt
import hashlib
import secrets

from ..config import get_settings
from ..models import AuditEvent, Invitation, Membership, Project, ProjectMember, Role, User
from ..schemas import AuditOut, InvitationIn, InvitationOut, MemberOut, RoleIn
from ..security import Caller, current_caller, revoke_all_tokens
from ..services import audit

router = APIRouter(prefix="/orgs", tags=["organisations"])


@router.get("/{org_id}/members", response_model=list[MemberOut])
def members(org_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    caller.require(org_id, "read_drafts")
    rows = db.execute(select(Membership, User).join(User).where(Membership.org_id == org_id)).all()
    return [MemberOut(user_id=u.id, email=u.email, name=u.name, role=m.role.value) for m, u in rows]


@router.post("/{org_id}/invitations", response_model=InvitationOut, status_code=201)
def invite(org_id: str, body: InvitationIn, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    """Create a single-use invitation. No account is created and no password is
    set by the admin; existing accounts are never attached without their consent."""
    caller.require(org_id, "manage")
    token = secrets.token_urlsafe(32)
    inv = Invitation(org_id=org_id, email=body.email.lower(), role=Role(body.role), invited_by=caller.user.id,
                     token_hash=hashlib.sha256(token.encode()).hexdigest(),
                     expires_at=dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=get_settings().invitation_ttl_days))
    db.add(inv)
    db.flush()
    audit.record(db, org_id=org_id, user_id=caller.user.id, action="invitation.create", entity_type="invitation",
                 entity_id=inv.id, payload={"email": inv.email, "role": body.role})
    return InvitationOut(id=inv.id, email=inv.email, role=body.role, expires_at=inv.expires_at, token=token)


@router.get("/{org_id}/invitations", response_model=list[InvitationOut])
def invitations(org_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    caller.require(org_id, "manage")
    rows = db.scalars(select(Invitation).where(Invitation.org_id == org_id, Invitation.revoked.is_(False))
                      .order_by(Invitation.created_at)).all()
    return [InvitationOut(id=i.id, email=i.email, role=i.role.value, expires_at=i.expires_at,
                          accepted_at=i.accepted_at) for i in rows]


@router.delete("/{org_id}/members/{user_id}", status_code=204)
def remove_member(org_id: str, user_id: str, caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    """Remove a member; their project memberships in this organisation go too and
    all their sessions are revoked."""
    caller.require(org_id, "manage")
    m = db.scalar(select(Membership).where(Membership.user_id == user_id, Membership.org_id == org_id))
    if m is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not found")
    if m.role == Role.admin and len(db.scalars(select(Membership).where(
            Membership.org_id == org_id, Membership.role == Role.admin)).all()) == 1:
        raise HTTPException(status.HTTP_409_CONFLICT, "an organisation keeps at least one admin")
    project_ids = select(Project.id).where(Project.org_id == org_id)
    for pm in db.scalars(select(ProjectMember).where(ProjectMember.user_id == user_id,
                                                     ProjectMember.project_id.in_(project_ids))):
        db.delete(pm)
    db.delete(m)
    revoke_all_tokens(db, user_id)
    audit.record(db, org_id=org_id, user_id=caller.user.id, action="member.remove", entity_type="user",
                 entity_id=user_id)


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
