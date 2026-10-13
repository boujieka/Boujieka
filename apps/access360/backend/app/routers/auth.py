from __future__ import annotations

import uuid
from typing import Literal

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_session
from ..deps import COOKIE, Ctx, current_user
from ..models import Membership, Organization, User
from ..security import (hash_password, limiter, make_reset_token, make_token, new_totp_secret, password_problems,
                        read_reset_token, reset_token_matches, revocations, totp_ok, totp_uri, verify_password)
from ..services import email as mailer
from cryptography.fernet import InvalidToken

from ..crypto import decrypt, encrypt
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


class ForgotIn(BaseModel):
    email: EmailStr


class ResetIn(BaseModel):
    token: str = Field(min_length=10, max_length=2000)
    new_password: str = Field(min_length=1, max_length=200)


class ChangeIn(BaseModel):
    current_password: str = Field(min_length=1, max_length=200)
    new_password: str = Field(min_length=1, max_length=200)


def _ip(request: Request) -> str:
    """Client address for per-IP limits. Behind N trusted proxies that each append to X-Forwarded-For
    (A360_TRUSTED_PROXY_HOPS=N), the client is the N-th entry from the right; entries further left can be forged by
    the client and are ignored. Too few entries means the request did not come through the proxy chain: use the
    TCP peer."""
    peer = request.client.host if request.client else "x"
    hops = get_settings().trusted_proxy_hops
    if hops <= 0:
        return peer
    chain = [p.strip() for p in request.headers.get("x-forwarded-for", "").split(",") if p.strip()]
    return chain[-hops] if len(chain) >= hops else peer


def _limit(key: str, per_minute: int) -> None:
    if not limiter().allow(key, per_minute):
        raise HTTPException(429, "Too many attempts, try again in a minute")


def _check_policy(pw: str) -> None:
    probs = password_problems(pw)
    if probs:
        raise HTTPException(400, "Password needs " + ", ".join(probs))


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
def register(body: RegisterIn, request: Request, resp: Response, s: Session = Depends(get_session)):
    _limit(f"register:{_ip(request)}", get_settings().register_rate_per_minute)
    if not body.accept_terms:
        raise HTTPException(400, "The terms and privacy notice must be accepted")
    _check_policy(body.password)
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
    _set_cookie(resp, make_token(u.id, mfa=False, password_hash=u.password_hash))
    return user_out(s, u)


def _check_totp(u: User, code: str) -> bool:
    """Verify a TOTP code against the encrypted secret; re-encrypt legacy plaintext or old-key ciphertext on success."""
    if not u.mfa_secret:
        return False
    try:
        plain, rewrap = decrypt(u.mfa_secret)
    except InvalidToken:
        return False  # no configured data key can read it (key lost or not rotated correctly)
    if not totp_ok(plain, code):
        return False
    if rewrap:
        u.mfa_secret = encrypt(plain)
    return True


@router.post("/login")
def login(body: LoginIn, request: Request, resp: Response, s: Session = Depends(get_session)):
    _limit(f"login:{_ip(request)}:{body.email.lower()}", get_settings().login_rate_per_minute)
    u = s.execute(select(User).where(User.email == body.email.lower())).scalar_one_or_none()
    if not u or not verify_password(body.password, u.password_hash):
        raise HTTPException(401, "Email or password not recognised")
    mfa = False
    if u.mfa_enabled:
        if not body.totp:
            raise HTTPException(401, "MFA code required", headers={"X-MFA-Required": "1"})
        if not _check_totp(u, body.totp):
            raise HTTPException(401, "MFA code not valid")
        mfa = True
    tok = make_token(u.id, mfa=mfa, password_hash=u.password_hash)
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
    secret = new_totp_secret()
    ctx.user.mfa_secret = encrypt(secret)  # stored encrypted at rest (limitation L13)
    return {"secret": secret, "otpauth_uri": totp_uri(secret, ctx.user.email)}


@router.post("/mfa/verify")
def mfa_verify(body: TotpIn, resp: Response, ctx: Ctx = Depends(current_user)):
    _limit(f"mfa:{ctx.user.id}", get_settings().mfa_rate_per_minute)
    if not ctx.user.mfa_secret or not _check_totp(ctx.user, body.code):
        raise HTTPException(400, "Code not valid")
    ctx.user.mfa_enabled = True
    audit(ctx.session, "mfa_enabled", "user", ctx.user.id, user_id=ctx.user.id)
    tok = make_token(ctx.user.id, mfa=True, password_hash=ctx.user.password_hash)
    _set_cookie(resp, tok)
    return {"mfa_enabled": True}


# ------------------------------------------------------------------ password lifecycle and session revocation

FORGOT_ANSWER = {"detail": "If an account exists for this address, a password reset link has been sent to it."}


@router.post("/password/forgot", status_code=202)
def password_forgot(body: ForgotIn, request: Request, tasks: BackgroundTasks, s: Session = Depends(get_session)):
    """Same status and body whether or not the account exists; the e-mail is sent after the response."""
    st = get_settings()
    email = body.email.lower()
    _limit(f"pwforgot:ip:{_ip(request)}", st.password_rate_per_minute)
    _limit(f"pwforgot:email:{email}", st.password_rate_per_minute)
    u = s.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if u is not None:
        tok = make_reset_token(u.id, u.password_hash)
        link = f"{st.public_base_url.rstrip('/')}/reset-password?token={tok}"
        fr = u.locale == "fr"
        subject = "ACCESS360 AFRICA : réinitialisation du mot de passe" if fr else "ACCESS360 AFRICA password reset"
        body_txt = (
            f"Pour choisir un nouveau mot de passe, ouvrez ce lien (valable {st.reset_token_minutes} minutes, une seule fois) :\n\n"
            f"{link}\n\nSi vous n'êtes pas à l'origine de cette demande, ignorez ce message." if fr else
            f"To choose a new password, open this link (valid for {st.reset_token_minutes} minutes, once):\n\n"
            f"{link}\n\nIf you did not ask for this, ignore this message; your password is unchanged.")
        tasks.add_task(mailer.send, mailer.Mail(to=u.email, subject=subject, body=body_txt))
        audit(s, "password_reset_requested", "user", u.id, user_id=u.id)
    return FORGOT_ANSWER


@router.post("/password/reset")
def password_reset(body: ResetIn, request: Request, s: Session = Depends(get_session)):
    _limit(f"pwreset:{_ip(request)}", get_settings().password_rate_per_minute)
    bad = HTTPException(400, "This reset link is invalid, expired or already used")
    claims = read_reset_token(body.token)
    if not claims:
        raise bad
    try:
        u = s.get(User, uuid.UUID(claims["sub"]))
    except ValueError:
        u = None
    # the token is bound to the password hash it was issued for, so it dies once the password changes
    if u is None or not reset_token_matches(claims, u.password_hash):
        raise bad
    _check_policy(body.new_password)
    u.password_hash = hash_password(body.new_password)  # also invalidates every existing session
    audit(s, "password_reset", "user", u.id, user_id=u.id)
    return {"ok": True}


@router.post("/password/change")
def password_change(body: ChangeIn, resp: Response, ctx: Ctx = Depends(current_user)):
    _limit(f"pwchange:{ctx.user.id}", get_settings().password_rate_per_minute)
    if not verify_password(body.current_password, ctx.user.password_hash):
        raise HTTPException(400, "Current password not recognised")
    _check_policy(body.new_password)
    if verify_password(body.new_password, ctx.user.password_hash):
        raise HTTPException(400, "The new password must differ from the current one")
    ctx.user.password_hash = hash_password(body.new_password)  # other sessions end: their version no longer matches
    audit(ctx.session, "password_changed", "user", ctx.user.id, user_id=ctx.user.id)
    _set_cookie(resp, make_token(ctx.user.id, mfa=ctx.mfa, password_hash=ctx.user.password_hash))
    return {"ok": True}


@router.post("/logout-all")
def logout_all(resp: Response, ctx: Ctx = Depends(current_user)):
    """Ends every session of this user, on every device, including this one."""
    try:
        revocations().revoke_all(str(ctx.user.id), get_settings().jwt_minutes * 60 + 60)
    except Exception:
        raise HTTPException(503, "Session revocation store unavailable, try again")
    audit(ctx.session, "logout_all", "user", ctx.user.id, user_id=ctx.user.id)
    resp.delete_cookie(COOKIE, path="/")
    return {"ok": True}

