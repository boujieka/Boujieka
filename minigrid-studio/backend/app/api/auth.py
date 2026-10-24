from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
import datetime as dt
import hashlib

from ..models import Invitation, Membership, Organization, Role, SessionToken, User
from ..schemas import AcceptInvitationIn, LoginIn, MembershipOut, MeOut, SignupIn, TokenOut
from ..security import Caller, current_caller, hash_password, issue_token, revoke_token, verify_or_dummy
from ..security_limits import throttle_ip, throttle_login
from ..services import audit

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenOut, status_code=201)
def signup(body: SignupIn, db: Session = Depends(get_db)):
    """Create an organisation and its first administrator (disabled unless MGS_ALLOW_SIGNUP=true)."""
    if not get_settings().allow_signup:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "self-service signup is disabled")
    if db.scalar(select(User).where(User.email == body.email.lower())):
        raise HTTPException(status.HTTP_409_CONFLICT, "e-mail already registered")
    if db.scalar(select(Organization).where(Organization.name == body.organization)):
        raise HTTPException(status.HTTP_409_CONFLICT, "organisation name already taken")
    org = Organization(name=body.organization)
    user = User(email=body.email.lower(), name=body.name, password_hash=hash_password(body.password))
    db.add_all([org, user])
    db.flush()
    db.add(Membership(user_id=user.id, org_id=org.id, role=Role.admin))
    audit.record(db, org_id=org.id, user_id=user.id, action="organization.create", entity_type="organization",
                 entity_id=org.id, payload={"name": org.name})
    token, exp = issue_token(db, user)
    return TokenOut(access_token=token, expires_at=exp)


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, request: Request, db: Session = Depends(get_db)):
    ip = throttle_login(request, body.email)
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    ok = verify_or_dummy(body.password, user.password_hash if user else None)
    if user is None or not user.active or not ok:
        audit.record(db, org_id=None, user_id=user.id if user else None, action="auth.login_failed",
                     entity_type="user", entity_id=user.id if user else "", payload={"ip": ip})
        db.commit()  # keep the failed attempt even though the request fails
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid credentials")
    token, exp = issue_token(db, user)
    audit.record(db, org_id=None, user_id=user.id, action="auth.login", entity_type="user", entity_id=user.id,
                 payload={"ip": ip})
    return TokenOut(access_token=token, expires_at=exp)


@router.post("/logout", status_code=204)
def logout(caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    revoke_token(db, caller.token)
    audit.record(db, org_id=None, user_id=caller.user.id, action="auth.logout", entity_type="user",
                 entity_id=caller.user.id)


@router.get("/me", response_model=MeOut)
def me(caller: Caller = Depends(current_caller), db: Session = Depends(get_db)):
    orgs = {o.id: o.name for o in db.scalars(select(Organization).where(Organization.id.in_(list(caller.roles))))}
    return MeOut(id=caller.user.id, email=caller.user.email, name=caller.user.name,
                 memberships=[MembershipOut(org_id=k, organization=orgs.get(k, ""), role=v.value)
                              for k, v in caller.roles.items()])


@router.post("/accept-invitation", response_model=TokenOut)
def accept_invitation(body: AcceptInvitationIn, request: Request, db: Session = Depends(get_db)):
    """New users set their own password here. Existing users must call this
    endpoint while signed in as the invited account (bearer token)."""
    throttle_ip(request)
    inv = db.scalar(select(Invitation).where(Invitation.token_hash == hashlib.sha256(body.token.encode()).hexdigest()))
    now = dt.datetime.now(dt.timezone.utc)
    if inv is None or inv.revoked or inv.accepted_at is not None or inv.expires_at < now:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid or expired invitation")
    user = db.scalar(select(User).where(User.email == inv.email))
    if user is not None:
        auth = request.headers.get("authorization", "")
        tok = auth[7:].strip() if auth.lower().startswith("bearer ") else ""
        row = db.scalar(select(SessionToken).where(
            SessionToken.token_hash == hashlib.sha256(tok.encode()).hexdigest())) if tok else None
        if row is None or row.revoked or row.expires_at < now or row.user_id != user.id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                "this e-mail already has an account: sign in as that account to accept")
    else:
        if not body.password or not body.name:
            raise HTTPException(422, "name and password are required to create the account")
        user = User(email=inv.email, name=body.name, password_hash=hash_password(body.password))
        db.add(user)
        db.flush()
    if db.scalar(select(Membership).where(Membership.user_id == user.id, Membership.org_id == inv.org_id)) is None:
        db.add(Membership(user_id=user.id, org_id=inv.org_id, role=inv.role))
    inv.accepted_at = now
    audit.record(db, org_id=inv.org_id, user_id=user.id, action="invitation.accept", entity_type="invitation",
                 entity_id=inv.id, payload={"role": inv.role.value})
    token, exp = issue_token(db, user)
    return TokenOut(access_token=token, expires_at=exp)
