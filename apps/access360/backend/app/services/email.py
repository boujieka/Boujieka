"""Outgoing e-mail behind a small backend abstraction.

* `console` (default outside production): logs the message, including links, to the application log.
* `smtp` (default in production): sends through A360_SMTP_HOST / PORT / USER / PASSWORD, STARTTLS by default.
* `memory`: keeps messages in `OUTBOX` (tests only).
"""
from __future__ import annotations

import json
import logging
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage

from ..config import get_settings

log = logging.getLogger("access360.email")


@dataclass
class Mail:
    to: str
    subject: str
    body: str


OUTBOX: list[Mail] = []


class ConsoleBackend:
    def send(self, mail: Mail) -> None:
        log.info(json.dumps({"email_console": True, "to": mail.to, "subject": mail.subject, "body": mail.body}))


class MemoryBackend:
    def send(self, mail: Mail) -> None:
        OUTBOX.append(mail)


class SmtpBackend:
    def send(self, mail: Mail) -> None:
        st = get_settings()
        if not st.smtp_host:
            raise RuntimeError("A360_SMTP_HOST is not set")
        msg = EmailMessage()
        msg["From"] = st.smtp_from
        msg["To"] = mail.to
        msg["Subject"] = mail.subject
        msg.set_content(mail.body)
        ctx = ssl.create_default_context()
        if st.smtp_ssl:
            server: smtplib.SMTP = smtplib.SMTP_SSL(st.smtp_host, st.smtp_port, timeout=15, context=ctx)
        else:
            server = smtplib.SMTP(st.smtp_host, st.smtp_port, timeout=15)
        with server:
            if st.smtp_starttls and not st.smtp_ssl:
                server.starttls(context=ctx)
            if st.smtp_user:
                server.login(st.smtp_user, st.smtp_password)
            server.send_message(msg)


BACKENDS = {"console": ConsoleBackend, "smtp": SmtpBackend, "memory": MemoryBackend}


def backend():
    name = get_settings().email_backend_name()
    if name not in BACKENDS:
        raise RuntimeError(f"Unknown A360_EMAIL_BACKEND {name!r}")
    return BACKENDS[name]()


def send(mail: Mail) -> None:
    """Never raises: called from background tasks, and a delivery failure must not change the HTTP answer
    (that would reveal whether the account exists). Failures are logged without the message body."""
    try:
        backend().send(mail)
    except Exception as exc:
        log.error(json.dumps({"email_failed": type(exc).__name__, "subject": mail.subject}))
