"""API keys: generation, hashing, lookup and an operator CLI.

Keys are random 256-bit tokens. Only their SHA-256 hex digest is stored: a
database leak does not reveal usable keys. A fast hash is appropriate here
because the input is high-entropy (no dictionary to brute-force).

    python -m app.security.keys create --name "ops laptop" --role admin
    python -m app.security.keys list
    python -m app.security.keys revoke --id 3
"""

import argparse
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ApiKey
from app.models.base import utcnow
from app.models.enums import Role

KEY_PREFIX = "cart_"  # Makes leaked keys easy to spot in secret scanners and logs.
# last_used_at is a hint, not an audit trail: avoid a write on every request.
LAST_USED_RESOLUTION = timedelta(minutes=1)
KEY_ROLES = (Role.ANALYST, Role.ADMIN)


def hash_key(plaintext: str) -> str:
    return hashlib.sha256(plaintext.encode("utf-8")).hexdigest()


def generate_key() -> str:
    return KEY_PREFIX + secrets.token_urlsafe(32)


def create_key(session: Session, name: str, role: Role) -> tuple[ApiKey, str]:
    """Persist a new key and return it with its plaintext (the only time it exists)."""
    if role not in KEY_ROLES:
        raise ValueError(f"role must be one of {[r.value for r in KEY_ROLES]}")
    plaintext = generate_key()
    key = ApiKey(name=name, key_hash=hash_key(plaintext), role=role)
    session.add(key)
    session.flush()
    return key, plaintext


def revoke_key(session: Session, key_id: int) -> ApiKey | None:
    key = session.get(ApiKey, key_id)
    if key is not None and key.revoked_at is None:
        key.revoked_at = utcnow()
    return key


def _aware(dt: datetime) -> datetime:
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=timezone.utc)  # SQLite drops tz


def authenticate(session: Session, plaintext: str) -> ApiKey | None:
    """Return the active key matching `plaintext`, or None. Updates last_used_at."""
    if not plaintext or len(plaintext) > 256:
        return None
    digest = hash_key(plaintext)
    key = session.scalar(select(ApiKey).where(ApiKey.key_hash == digest))
    # The indexed lookup finds the candidate; the final check is constant-time.
    if key is None or not hmac.compare_digest(key.key_hash, digest) or key.revoked_at is not None:
        return None
    now = utcnow()
    if key.last_used_at is None or now - _aware(key.last_used_at) > LAST_USED_RESOLUTION:
        key.last_used_at = now
        session.commit()
    return key


def _fmt(dt: datetime | None) -> str:
    return dt.strftime("%Y-%m-%d %H:%M") if dt else "-"


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m app.security.keys", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    create = sub.add_parser("create", help="Create a key and print it once")
    create.add_argument("--name", required=True)
    create.add_argument("--role", required=True, choices=[r.value for r in KEY_ROLES])
    revoke = sub.add_parser("revoke", help="Revoke a key by id")
    revoke.add_argument("--id", type=int, required=True)
    sub.add_parser("list", help="List keys (never shows keys or hashes)")
    args = parser.parse_args(argv)

    from app.db import SessionLocal

    with SessionLocal() as session:
        if args.cmd == "create":
            key, plaintext = create_key(session, args.name, Role(args.role))
            session.commit()
            print(f"Created key id={key.id} name={key.name!r} role={key.role.value}")
            print("Store it now in a secret manager; it cannot be shown again:")
            print(plaintext)
        elif args.cmd == "revoke":
            key = revoke_key(session, args.id)
            if key is None:
                parser.exit(1, f"No key with id {args.id}\n")
            session.commit()
            print(f"Revoked key id={key.id} name={key.name!r} at {_fmt(key.revoked_at)}")
        else:
            print(f"{'id':>4}  {'role':<8} {'created':<16} {'last used':<16} {'revoked':<16} name")
            for k in session.scalars(select(ApiKey).order_by(ApiKey.id)):
                print(
                    f"{k.id:>4}  {k.role.value:<8} {_fmt(k.created_at):<16} "
                    f"{_fmt(k.last_used_at):<16} {_fmt(k.revoked_at):<16} {k.name}"
                )


if __name__ == "__main__":
    main()
