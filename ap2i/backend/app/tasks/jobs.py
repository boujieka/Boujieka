"""Background jobs (Master prompt §31). Usable with Celery or synchronously (CLI, tests).

Scheduling: `dispatch_due_syncs` runs every few minutes (Celery beat). For each ENABLED connector
with a cron schedule it checks whether a scheduled time has passed since the last scheduled run and,
if so, runs the sync. A per-connector PostgreSQL advisory lock makes runs idempotent (no two runs
of one connector at once). A daily schedule does not assume the source publishes daily: unchanged
records are detected by hash and skipped.
"""

from __future__ import annotations

import logging
import zlib
from datetime import datetime, timezone

from sqlalchemy import select, text

from app.config import get_settings
from app.db import SessionLocal
from app.models import Country, Notification, SourceConnector
from app.tasks import cron

log = logging.getLogger("ap2i.jobs")


def _lock(db, key: str) -> bool:
    if db.bind.dialect.name != "postgresql":
        return True
    return bool(db.execute(text("SELECT pg_try_advisory_lock(:k)"), {"k": zlib.crc32(key.encode())}).scalar())


def _unlock(db, key: str) -> None:
    if db.bind.dialect.name == "postgresql":
        db.execute(text("SELECT pg_advisory_unlock(:k)"), {"k": zlib.crc32(key.encode())})


def sync_connector(key: str, trigger: str = "manual") -> dict:
    from app.ingestion.pipeline import run_sync

    with SessionLocal() as db:
        if not _lock(db, f"sync:{key}"):
            return {"connector": key, "status": "skipped", "reason": "another run is in progress"}
        try:
            run = run_sync(db, key, trigger=trigger, force=trigger != "scheduled")
            result = {"connector": key, "run_id": run.id, "status": run.status, "imported": run.records_imported,
                      "retrieved": run.records_retrieved, "failed": run.records_failed}
        finally:
            _unlock(db, f"sync:{key}")
    if result["status"] in ("success", "partial") and result["imported"]:
        post_sync()
    return result


def post_sync(country_iso3s: list[str] | None = None) -> dict:
    """After validated imports: recompute alerts, data quality and annual portfolio snapshots."""
    from app.finance.portfolio import snapshot_portfolio
    from app.performance.alerts import run_alerts
    from app.performance.quality import assess_all

    s = get_settings()
    out = {}
    with SessionLocal() as db:
        for iso3 in country_iso3s or s.active_countries:
            c = db.scalar(select(Country).where(Country.iso3 == iso3))
            if c is None:
                continue
            out[iso3] = {
                "alerts": run_alerts(db, c.id),
                "quality_assessed": assess_all(db, c.id),
                "snapshots": len(snapshot_portfolio(db, iso3, s.portfolio_first_year, s.portfolio_last_year, note="post-sync")),
            }
    return out


def dispatch_due_syncs(now: datetime | None = None, runner=None) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    runner = runner or sync_connector
    results = []
    with SessionLocal() as db:
        due = []
        for c in db.scalars(select(SourceConnector).where(SourceConnector.enabled.is_(True), SourceConnector.schedule_cron.is_not(None))):
            try:
                last = cron.last_due(c.schedule_cron, now)
            except ValueError as exc:
                db.add(Notification(kind="config_error", title=f"Invalid schedule for {c.key}", body=str(exc)))
                continue
            done = (c.cursor or {}).get("last_scheduled_for")
            if last and (done is None or datetime.fromisoformat(done) < last):
                cur = dict(c.cursor or {})
                cur["last_scheduled_for"] = last.isoformat()
                c.cursor = cur
                due.append(c.key)
        db.commit()
    for key in due:
        try:
            results.append(runner(key, "scheduled"))
        except Exception as exc:  # noqa: BLE001 — logged on the run; keep dispatching others
            log.exception("scheduled sync failed: %s", key)
            results.append({"connector": key, "status": "failed", "error": str(exc)})
    return results
