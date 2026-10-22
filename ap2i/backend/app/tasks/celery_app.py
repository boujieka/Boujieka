"""Celery application: worker + beat.

    celery -A app.tasks.celery_app worker -l info
    celery -A app.tasks.celery_app beat -l info
"""

from __future__ import annotations

from celery import Celery

from app.config import get_settings

settings = get_settings()
celery = Celery("ap2i", broker=settings.redis_url, backend=settings.redis_url)
celery.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_default_rate_limit="10/m",
    timezone="UTC",
    beat_schedule={
        "dispatch-due-syncs": {"task": "ap2i.dispatch_due_syncs", "schedule": 300.0},
        "refresh-exchange-rates": {"task": "ap2i.refresh_rates", "schedule": 7 * 24 * 3600.0},
    },
)


@celery.task(name="ap2i.sync_connector", bind=True, autoretry_for=(ConnectionError, TimeoutError),
             retry_backoff=True, retry_kwargs={"max_retries": 3})
def sync_connector_task(self, key: str, trigger: str = "manual"):
    from app.tasks.jobs import sync_connector

    return sync_connector(key, trigger)


@celery.task(name="ap2i.dispatch_due_syncs")
def dispatch_task():
    from app.tasks.jobs import dispatch_due_syncs

    # Each due connector is queued as its own task (retries and rate limits apply per connector).
    return dispatch_due_syncs(runner=lambda key, trig: {"connector": key, "queued": sync_connector_task.delay(key, trig).id})


@celery.task(name="ap2i.post_sync")
def post_sync_task():
    from app.tasks.jobs import post_sync

    return post_sync()


@celery.task(name="ap2i.refresh_rates")
def refresh_rates_task():
    from app.connectors.fx import refresh_rates
    from app.db import SessionLocal

    with SessionLocal() as db:
        return refresh_rates(db, settings.active_countries, 2000, settings.portfolio_last_year)
