"""Audit-log writes and request-scoped DB access for the security middleware."""

import ipaddress
import logging
from collections.abc import Iterator
from contextlib import contextmanager

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import AuditLog
from app.security.principal import Principal

log = logging.getLogger("abi.audit")


@contextmanager
def app_session(app: FastAPI) -> Iterator[Session]:
    """A session from the app's `get_session` dependency, honouring test overrides."""
    gen = app.dependency_overrides.get(get_session, get_session)()
    try:
        yield next(gen)
    finally:
        gen.close()


def truncate_ip(host: str | None) -> str | None:
    """Keep the network, drop the host part: IPv4 /24, IPv6 /48. Non-IP peers are kept as-is."""
    if not host:
        return None
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return host[:64]  # e.g. "testclient"
    prefix = 24 if ip.version == 4 else 48
    return str(ipaddress.ip_network(f"{ip}/{prefix}", strict=False))


def write_audit(
    app: FastAPI,
    principal: Principal,
    method: str,
    path: str,
    status_code: int,
    client_host: str | None,
    request_id: str,
) -> None:
    """Best effort: an audit failure is logged but never turns a response into a 500."""
    row = AuditLog(
        api_key_id=principal.key_id,
        role=principal.role,
        method=method[:10],
        path=path[:512],  # Path only: the query string may carry secrets and is never stored.
        status_code=status_code,
        client_ip=truncate_ip(client_host),
        request_id=request_id,
    )
    try:
        with app_session(app) as session:
            session.add(row)
            session.commit()
    except SQLAlchemyError as exc:
        log.warning("audit write failed for %s %s (%s): %s", method, path, status_code, type(exc).__name__)
