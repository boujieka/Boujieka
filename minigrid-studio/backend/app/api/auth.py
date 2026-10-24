from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
from ..models import Membership, Organization, Role, User
from ..schemas import LoginIn, MembershipOut, MeOut, SignupIn, TokenOut
from ..security import Caller, current_caller, hash_password, issue_token, login_limiter, revoke_token, verify_password
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
    ip = request.client.host if request.client else "?"
    login_limiter.check(f"{body.email.lower()}|{ip}")
    user = db.scalar(select(User).where(User.email == body.email.lower()))
    if user is None or not user.active or not verify_password(body.password, user.password_hash):
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
