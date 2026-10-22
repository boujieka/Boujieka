"""Command line: python -m app.cli <command>

  seed                      load reference data (54 countries, sectors, donors, connectors, roles, plans)
  sync <connector> [...]    run connectors now (real sources); --reprocess re-applies mappings to unchanged records
  post-sync                 recompute alerts, data quality and portfolio snapshots
  rates                     refresh historical exchange rates (World Bank WDI, IMF)
  dispatch                  run due scheduled syncs once (what Celery beat does)
  create-admin <email>      create an AP²I super administrator (password prompted or AP2I_ADMIN_PASSWORD)
  activate-countries        mirror AP2I_ACTIVE_COUNTRIES into the database
  check-country-sources     check reachability of country-specific official sources
  connector-report          print the connector status report (markdown)
  migrate-mvp <db_url>      migrate an AP²I MVP v0.1 database (SQLite/PostgreSQL URL) and print the report
  export-public-snapshot <outdir> [ISO3 ...]
                            write the public read-only data snapshot used by the static portal
"""

from __future__ import annotations

import getpass
import os
import sys
from datetime import datetime, timezone

from sqlalchemy import select

from app.config import get_settings
from app.db import SessionLocal


def main(argv: list[str]) -> int:
    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    for noisy in ("httpx", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, args = argv[0], argv[1:]
    with SessionLocal() as db:
        if cmd == "seed":
            from app.reference.seed import seed_reference
            print(seed_reference(db))
        elif cmd == "sync":
            from app.tasks.jobs import sync_connector
            reprocess = "--reprocess" in args
            for key in [a for a in args if not a.startswith("--")]:
                print(sync_connector(key, "manual", reprocess=reprocess))
        elif cmd == "post-sync":
            from app.tasks.jobs import post_sync
            print(post_sync())
        elif cmd == "rates":
            from app.connectors.fx import refresh_rates
            print(refresh_rates(db, get_settings().active_countries, 2000, get_settings().portfolio_last_year))
        elif cmd == "dispatch":
            from app.tasks.jobs import dispatch_due_syncs
            print(dispatch_due_syncs())
        elif cmd == "create-admin":
            from app.models import RoleDef, User, UserRole
            from app.security.core import hash_password, password_problems
            email = args[0].lower()
            pw = os.environ.get("AP2I_ADMIN_PASSWORD") or getpass.getpass("Password: ")
            problems = password_problems(pw, email)
            if problems:
                print("Weak password:", problems)
                return 1
            u = db.scalar(select(User).where(User.email == email)) or User(email=email, full_name="AP²I administrator")
            u.password_hash = hash_password(pw)
            u.email_verified_at = u.email_verified_at or datetime.now(timezone.utc)
            db.add(u)
            db.flush()
            role = db.scalar(select(RoleDef).where(RoleDef.code == "ap2i_super_admin"))
            if not any(r.role_id == role.id for r in u.roles):
                db.add(UserRole(user_id=u.id, role_id=role.id))
            db.commit()
            print(f"Super administrator ready: {email}")
        elif cmd == "export-public-snapshot":
            # offline, in-process API calls: the per-client request limit does not apply to this export
            os.environ["AP2I_RATE_LIMIT_PER_MINUTE"] = "1000000"
            get_settings.cache_clear()
            from app.publish.snapshot import export_public_snapshot
            print(export_public_snapshot(db, args[0], args[1:] or None))
        elif cmd == "activate-countries":
            from app.reference.seed import sync_active_countries
            print(sync_active_countries(db))
        elif cmd == "check-country-sources":
            import httpx
            from app.models import CountryDataSource
            for s in db.scalars(select(CountryDataSource)):
                if not s.url:
                    s.reachability = "no_url"
                    continue
                try:
                    r = httpx.get(s.url, timeout=20, follow_redirects=True)
                    s.reachability = f"http_{r.status_code}"
                except httpx.HTTPError as exc:
                    s.reachability = f"error:{type(exc).__name__}"
                s.last_checked_at = datetime.now(timezone.utc).isoformat()
                print(s.institution, s.url, s.reachability)
            db.commit()
        elif cmd == "connector-report":
            from app.models import SourceConnector, SourceRecord
            from sqlalchemy import func
            print("| Connector | Tier | Status | Enabled | Records stored | Last success | Evidence / blocker |\n|---|---|---|---|---|---|---|")
            for c in db.scalars(select(SourceConnector).order_by(SourceConnector.tier, SourceConnector.key)):
                n = db.scalar(select(func.count(SourceRecord.id)).where(SourceRecord.connector_id == c.id, SourceRecord.is_latest.is_(True)))
                ev = (c.status_evidence or c.last_error or "").replace("|", "/")[:220]
                print(f"| `{c.key}` | {c.tier} | {c.status} | {c.enabled} | {n} | {c.last_success_at:%Y-%m-%d} | {ev} |" if c.last_success_at
                      else f"| `{c.key}` | {c.tier} | {c.status} | {c.enabled} | {n} | — | {ev} |")
        elif cmd == "migrate-mvp":
            import json
            from app.migration.mvp import migrate
            print(json.dumps(migrate(args[0], db), indent=2, ensure_ascii=False))
        else:
            print(__doc__)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
