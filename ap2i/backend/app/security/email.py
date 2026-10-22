"""Outgoing email. The console backend logs messages (development/test); SMTP sends them."""

from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from app.config import get_settings

log = logging.getLogger("ap2i.email")
OUTBOX: list[dict] = []  # console backend keeps the last messages (used by tests and local development)


def send_email(to: str, subject: str, body: str) -> None:
    s = get_settings()
    if s.email_backend == "smtp":
        if not s.smtp_host:
            raise RuntimeError("AP2I_SMTP_HOST is not configured")
        msg = EmailMessage()
        msg["From"], msg["To"], msg["Subject"] = s.email_from, to, subject
        msg.set_content(body)
        with smtplib.SMTP(s.smtp_host, s.smtp_port, timeout=20) as smtp:
            smtp.starttls()
            if s.smtp_user:
                smtp.login(s.smtp_user, s.smtp_password or "")
            smtp.send_message(msg)
        return
    OUTBOX.append({"to": to, "subject": subject, "body": body})
    del OUTBOX[:-50]
    log.info("EMAIL (console backend) to=%s subject=%s", to, subject)
