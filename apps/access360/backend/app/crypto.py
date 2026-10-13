"""Application-level field encryption (Fernet / MultiFernet) for secrets stored in the database.

STATUS: prepared but NOT yet wired to `users.mfa_secret` (limitation L13). A Fernet token for a 32 character TOTP
secret is 140 characters, and the column is VARCHAR(64), so a migration widening it (to at least 255) must land
first. Once it has, the wiring is:

* `/mfa/setup`: store `encrypt(secret)`;
* every TOTP check: `plain, rewrap = decrypt(stored)`; verify with `plain`; if the code is valid and `rewrap` is
  true, store `encrypt(plain)` (migrates legacy plaintext and re-encrypts under the newest key after a rotation);
* call `cipher()` at application start-up so production refuses to start without A360_DATA_KEY.

Keys: A360_DATA_KEY is the current key (urlsafe base64 32 bytes, `Fernet.generate_key()`); A360_DATA_KEYS_OLD
is a comma-separated list of previous keys still accepted for decryption.
"""
from __future__ import annotations

import re
import warnings

from cryptography.fernet import Fernet, InvalidToken, MultiFernet

from .config import get_settings

_LEGACY_TOTP = re.compile(r"^[A-Z2-7]{16,64}=*$")  # plaintext base32 TOTP secret as stored before encryption
_dev_key: bytes | None = None


def cipher() -> MultiFernet:
    global _dev_key
    st = get_settings()
    key = st.data_key.strip()
    if not key:
        if st.env == "production":
            raise RuntimeError("A360_DATA_KEY must be set in production")
        if _dev_key is None:
            warnings.warn("A360_DATA_KEY not set: using a random per-process data key (encrypted values become "
                          "unreadable on restart)")
            _dev_key = Fernet.generate_key()
        key = _dev_key.decode()
    olds = [k.strip() for k in st.data_keys_old.split(",") if k.strip()]
    return MultiFernet([Fernet(key.encode())] + [Fernet(k.encode()) for k in olds])


def is_legacy_plaintext(stored: str) -> bool:
    return bool(_LEGACY_TOTP.match(stored))


def encrypt(plain: str) -> str:
    return cipher().encrypt(plain.encode()).decode()


def decrypt(stored: str) -> tuple[str, bool]:
    """Returns (plaintext, needs_rewrap). needs_rewrap is true for a legacy plaintext value or a value encrypted with
    an old key. Raises InvalidToken if no configured key can decrypt the value."""
    if is_legacy_plaintext(stored):
        return stored, True
    mf = cipher()
    plain = mf.decrypt(stored.encode()).decode()
    current = Fernet(get_settings().data_key.strip().encode()) if get_settings().data_key.strip() else None
    if current is None:
        return plain, False
    try:
        current.decrypt(stored.encode())
        return plain, False
    except InvalidToken:
        return plain, True
