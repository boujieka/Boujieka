"""Authentication: registration, email verification, login (+MFA), password reset, API keys."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import ApiKey, Organization, RoleDef, User, UserRole, UserToken
from app.security.core import (
    create_access_token,
    create_mfa_challenge,
    decode_token,
    hash_password,
    new_api_key,
    new_one_time_token,
    new_totp_secret,
    password_problems,
    sha256,
    totp_uri,
    verify_password,
    verify_totp,
)
from app.security.deps import Principal, audit, auth_rate_limit, require_feature, require_user
from app.security.email import send_email

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)
    full_name: str = Field(min_length=2, max_length=200)
    organization_name: str | None = Field(None, max_length=250)
    locale: str = Field("fr", pattern="^(fr|en)$")


class LoginIn(BaseModel):
    # Plain string: login must match stored accounts (incl. internal domains) without deliverability rules.
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(max_length=200)


class MfaIn(BaseModel):
    challenge: str
    code: str = Field(min_length=6, max_length=8)


class TokenIn(BaseModel):
    token: str


class ResetIn(BaseModel):
    token: str
    new_password: str


class EmailIn(BaseModel):
    email: str = Field(min_length=3, max_length=254)


class CodeIn(BaseModel):
    code: str


def _issue_token(db: Session, user: User, purpose: str, hours: int) -> str:
    raw, h = new_one_time_token()
    db.add(UserToken(user_id=user.id, purpose=purpose, token_hash=h,
                     expires_at=datetime.now(timezone.utc) + timedelta(hours=hours)))
    return raw


def _consume(db: Session, raw: str, purpose: str) -> User:
    t = db.scalar(select(UserToken).where(UserToken.token_hash == sha256(raw), UserToken.purpose == purpose))
    now = datetime.now(timezone.utc)
    if t is None or t.used_at is not None or _aware(t.expires_at) < now:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid or expired token")
    t.used_at = now
    return db.get(User, t.user_id)


def _aware(d: datetime) -> datetime:
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def user_out(db: Session, u: User, principal: Principal | None = None) -> dict:
    org = db.get(Organization, u.organization_id) if u.organization_id else None
    return {
        "id": u.id, "email": u.email, "full_name": u.full_name, "locale": u.locale,
        "email_verified": u.email_verified_at is not None, "mfa_enabled": u.mfa_enabled,
        "organization": {"id": org.id, "name": org.name} if org else None,
        "roles": sorted(principal.roles) if principal else [r.role.code for r in u.roles],
        "permissions": sorted(principal.permissions) if principal else None,
        "features": sorted(principal.features) if principal else None,
    }


@router.post("/register", status_code=201, dependencies=[Depends(auth_rate_limit)])
def register(body: RegisterIn, request: Request, db: Session = Depends(get_db)):
    email = body.email.lower()
    problems = password_problems(body.password, email)
    if problems:
        raise HTTPException(422, {"password": problems})
    if db.scalar(select(User).where(User.email == email)):
        # Do not reveal account existence: same response, no new account.
        return {"status": "verification_sent"}
    org_id = None
    if body.organization_name:
        org = Organization(name=body.organization_name.strip(), org_type="pending_verification", is_tenant=False)
        db.add(org)
        db.flush()
        org_id = org.id
    u = User(email=email, password_hash=hash_password(body.password), full_name=body.full_name.strip(),
             organization_id=org_id, locale=body.locale)
    db.add(u)
    db.flush()
    role = db.scalar(select(RoleDef).where(RoleDef.code == "registered_user"))
    db.add(UserRole(user_id=u.id, role_id=role.id))
    raw = _issue_token(db, u, "verify_email", 48)
    audit(db, request, "auth.register", user_id=u.id, entity_type="user", entity_id=u.id)
    db.commit()
    link = f"{get_settings().public_app_url}/verify-email?token={raw}"
    send_email(email, "AP²I — vérifiez votre adresse / verify your email", f"{link}\n")
    return {"status": "verification_sent"}


@router.post("/verify-email")
def verify_email(body: TokenIn, request: Request, db: Session = Depends(get_db)):
    u = _consume(db, body.token, "verify_email")
    u.email_verified_at = datetime.now(timezone.utc)
    audit(db, request, "auth.verify_email", user_id=u.id)
    db.commit()
    return {"status": "verified"}


@router.post("/login", dependencies=[Depends(auth_rate_limit)])
def login(body: LoginIn, request: Request, db: Session = Depends(get_db)):
    s = get_settings()
    u = db.scalar(select(User).where(User.email == body.email.lower()))
    now = datetime.now(timezone.utc)
    if u is not None and u.locked_until and _aware(u.locked_until) > now:
        raise HTTPException(status.HTTP_423_LOCKED, "Account temporarily locked")
    if u is None or not verify_password(body.password, u.password_hash) or not u.is_active:
        if u is not None:
            u.failed_logins += 1
            if u.failed_logins >= s.max_failed_logins:
                u.locked_until = now + timedelta(minutes=s.lockout_minutes)
                u.failed_logins = 0
            audit(db, request, "auth.login_failed", user_id=u.id, status_code=401)
            db.commit()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    if u.email_verified_at is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Email not verified")
    u.failed_logins = 0
    if u.mfa_enabled:
        db.commit()
        return {"mfa_required": True, "challenge": create_mfa_challenge(u.id)}
    u.last_login_at = now
    audit(db, request, "auth.login", user_id=u.id)
    db.commit()
    return {"access_token": create_access_token(u.id, u.token_version, mfa=False), "token_type": "bearer",
            "expires_in": s.access_token_minutes * 60}


@router.post("/login/mfa", dependencies=[Depends(auth_rate_limit)])
def login_mfa(body: MfaIn, request: Request, db: Session = Depends(get_db)):
    try:
        payload = decode_token(body.challenge, "mfa_challenge")
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid or expired challenge") from None
    u = db.get(User, int(payload["sub"]))
    if u is None or not u.mfa_enabled or not verify_totp(u.mfa_secret or "", body.code):
        if u:
            audit(db, request, "auth.mfa_failed", user_id=u.id, status_code=401)
            db.commit()
        raise HTTPException(401, "Invalid code")
    u.last_login_at = datetime.now(timezone.utc)
    audit(db, request, "auth.login", user_id=u.id, detail={"mfa": True})
    db.commit()
    return {"access_token": create_access_token(u.id, u.token_version, mfa=True), "token_type": "bearer",
            "expires_in": get_settings().access_token_minutes * 60}


@router.get("/me")
def me(principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    return user_out(db, principal.user, principal)


@router.post("/logout")
def logout(request: Request, principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    principal.user.token_version += 1  # revokes every issued token
    audit(db, request, "auth.logout", principal)
    db.commit()
    return {"status": "logged_out"}


@router.post("/mfa/setup")
def mfa_setup(principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    u = principal.user
    if u.mfa_enabled:
        raise HTTPException(400, "MFA already enabled")
    u.mfa_secret = new_totp_secret()
    db.commit()
    return {"secret": u.mfa_secret, "otpauth_uri": totp_uri(u.mfa_secret, u.email)}


@router.post("/mfa/enable")
def mfa_enable(body: CodeIn, request: Request, principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    u = principal.user
    if not u.mfa_secret or not verify_totp(u.mfa_secret, body.code):
        raise HTTPException(400, "Invalid code")
    u.mfa_enabled = True
    u.token_version += 1
    audit(db, request, "auth.mfa_enabled", principal)
    db.commit()
    return {"status": "mfa_enabled", "note": "Sign in again."}


@router.post("/mfa/disable")
def mfa_disable(body: CodeIn, request: Request, principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    u = principal.user
    if not u.mfa_enabled or not verify_totp(u.mfa_secret or "", body.code):
        raise HTTPException(400, "Invalid code")
    u.mfa_enabled, u.mfa_secret = False, None
    u.token_version += 1
    audit(db, request, "auth.mfa_disabled", principal)
    db.commit()
    return {"status": "mfa_disabled"}


@router.post("/password/forgot", dependencies=[Depends(auth_rate_limit)])
def forgot(body: EmailIn, request: Request, db: Session = Depends(get_db)):
    u = db.scalar(select(User).where(User.email == body.email.lower()))
    if u is not None and u.is_active:
        raw = _issue_token(db, u, "reset_password", 1)
        audit(db, request, "auth.password_reset_requested", user_id=u.id)
        db.commit()
        send_email(u.email, "AP²I — réinitialisation du mot de passe / password reset",
                   f"{get_settings().public_app_url}/reset-password?token={raw}\n")
    return {"status": "if_the_account_exists_an_email_was_sent"}


@router.post("/password/reset", dependencies=[Depends(auth_rate_limit)])
def reset(body: ResetIn, request: Request, db: Session = Depends(get_db)):
    u = _consume(db, body.token, "reset_password")
    problems = password_problems(body.new_password, u.email)
    if problems:
        db.rollback()
        raise HTTPException(422, {"password": problems})
    u.password_hash = hash_password(body.new_password)
    u.token_version += 1
    u.failed_logins, u.locked_until = 0, None
    audit(db, request, "auth.password_reset", user_id=u.id)
    db.commit()
    return {"status": "password_changed"}


class ApiKeyIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)


@router.post("/api-keys", status_code=201)
def create_api_key(body: ApiKeyIn, request: Request, principal: Principal = Depends(require_feature("api_access")),
                   db: Session = Depends(get_db)):
    raw, prefix, h = new_api_key()
    k = ApiKey(user_id=principal.user.id, name=body.name, prefix=prefix, key_hash=h)
    db.add(k)
    audit(db, request, "auth.api_key_created", principal, "api_key", prefix)
    db.commit()
    return {"id": k.id, "name": k.name, "prefix": prefix, "key": raw, "note": "Shown once; store it securely."}


@router.get("/api-keys")
def list_api_keys(principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    return [{"id": k.id, "name": k.name, "prefix": k.prefix, "created_at": k.created_at, "revoked_at": k.revoked_at,
             "last_used_at": k.last_used_at} for k in db.scalars(select(ApiKey).where(ApiKey.user_id == principal.user.id))]


@router.delete("/api-keys/{key_id}")
def revoke_api_key(key_id: int, request: Request, principal: Principal = Depends(require_user), db: Session = Depends(get_db)):
    k = db.get(ApiKey, key_id)
    if k is None or k.user_id != principal.user.id:
        raise HTTPException(404, "Not found")
    k.revoked_at = datetime.now(timezone.utc)
    audit(db, request, "auth.api_key_revoked", principal, "api_key", k.prefix)
    db.commit()
    return {"status": "revoked"}
