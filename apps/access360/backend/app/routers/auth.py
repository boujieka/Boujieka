from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_session
from ..deps import COOKIE, Ctx, current_user
from ..models import Membership, Organization, User
from ..security import (hash_password, login_limiter, make_token, new_totp_secret, password_problems, totp_ok, totp_uri,
                        verify_password)
from ..services.audit import audit

router = APIRouter(prefix="/api/auth", tags=["auth"])

OrgKind = Literal["individual", "developer", "investor", "government", "accredited"]


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=200)
    full_name: str = Field(min_length=1, max_length=200)
    org_name: str = Field(min_length=1, max_length=200)
    org_kind: OrgKind
    locale: Literal["en", "fr"] = "en"
    accept_terms: bool


class LoginIn(BaseModel):
    email: EmailStr
    password: str
    totp: str | None = None


class TotpIn(BaseModel):
    code: str = Field(min_length=6, max_length=8)


def user_out(s: Session, u: User) -> dict:
    rows = s.execute(select(Membership, Organization).join(Organization, Organization.id == Membership.org_id)
                     .where(Membership.user_id == u.id)).all()
    return {"id": str(u.id), "email": u.email, "full_name": u.full_name, "locale": u.locale, "mfa_enabled": u.mfa_enabled,
            "is_superadmin": u.is_superadmin,
            "organizations": [{"id": str(o.id), "name": o.name, "kind": o.kind, "role": m.role, "plan": o.plan,
                               "accreditation_status": o.accreditation_status, "is_demo": o.is_demo} for m, o in rows]}


def _set_cookie(resp: Response, tok: str) -> None:
    st = get_settings()
    resp.set_cookie(COOKIE, tok, httponly=True, secure=st.cookie_secure, samesite="lax", max_age=st.jwt_minutes * 60, path="/")


@router.post("/register", status_code=201)
def register(body: RegisterIn, resp: Response, s: Session = Depends(get_session)):
    if not body.accept_terms:
        raise HTTPException(400, "The terms and privacy notice must be accepted")
    probs = password_problems(body.password)
    if probs:
        raise HTTPException(400, "Password needs " + ", ".join(probs))
    email = body.email.lower()
    if s.execute(select(User).where(User.email == email)).scalar_one_or_none():
        raise HTTPException(409, "An account with this email already exists")
    u = User(email=email, password_hash=hash_password(body.password), full_name=body.full_name, locale=body.locale)
    # accredited status is never granted by registration: it waits for administrator verification
    o = Organization(name=body.org_name, kind=body.org_kind,
                     accreditation_status="pending" if body.org_kind == "accredited" else "not_applicable")
    s.add_all([u, o])
    s.flush()
    s.add(Membership(user_id=u.id, org_id=o.id, role="owner"))
    audit(s, "register", "user", u.id, user_id=u.id)
    s.flush()
    _set_cookie(resp, make_token(u.id, mfa=False))
    return user_out(s, u)


@router.post("/login")
def login(body: LoginIn, request: Request, resp: Response, s: Session = Depends(get_session)):
    key = f"{request.client.host if request.client else 'x'}:{body.email.lower()}"
    if not login_limiter.allow(key, get_settings().login_rate_per_minute):
        raise HTTPException(429, "Too many attempts, try again in a minute")
    u = s.execute(select(User).where(User.email == body.email.lower())).scalar_one_or_none()
    if not u or not verify_password(body.password, u.password_hash):
        raise HTTPException(401, "Email or password not recognised")
    mfa = False
    if u.mfa_enabled:
        if not body.totp:
            raise HTTPException(401, "MFA code required", headers={"X-MFA-Required": "1"})
        if not totp_ok(u.mfa_secret or "", body.totp):
            raise HTTPException(401, "MFA code not valid")
        mfa = True
    tok = make_token(u.id, mfa=mfa)
    _set_cookie(resp, tok)
    audit(s, "login", "user", u.id, user_id=u.id, mfa=mfa)
    return {**user_out(s, u), "session_mfa": mfa}


@router.post("/logout")
def logout(resp: Response):
    resp.delete_cookie(COOKIE, path="/")
    return {"ok": True}


@router.get("/me")
def me(ctx: Ctx = Depends(current_user)):
    return {**user_out(ctx.session, ctx.user), "session_mfa": ctx.mfa}


@router.post("/mfa/setup")
def mfa_setup(ctx: Ctx = Depends(current_user)):
    if ctx.user.mfa_enabled:
        raise HTTPException(400, "MFA already enabled")
    ctx.user.mfa_secret = new_totp_secret()
    return {"secret": ctx.user.mfa_secret, "otpauth_uri": totp_uri(ctx.user.mfa_secret, ctx.user.email)}


@router.post("/mfa/verify")
def mfa_verify(body: TotpIn, resp: Response, ctx: Ctx = Depends(current_user)):
    if not ctx.user.mfa_secret or not totp_ok(ctx.user.mfa_secret, body.code):
        raise HTTPException(400, "Code not valid")
    ctx.user.mfa_enabled = True
    audit(ctx.session, "mfa_enabled", "user", ctx.user.id, user_id=ctx.user.id)
    tok = make_token(ctx.user.id, mfa=True)
    _set_cookie(resp, tok)
    return {"mfa_enabled": True}

