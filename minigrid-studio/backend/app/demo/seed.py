"""Create a demonstration organisation with the FICTITIOUS portfolio.

The admin credentials must be provided (no default password):
    MGS_DEMO_ADMIN_EMAIL=... MGS_DEMO_ADMIN_PASSWORD=... python -m app.demo.seed
"""
import os
import sys

from sqlalchemy import select

from ..db import engine, get_db
from ..models import Membership, Organization, Project, Role, User
from ..security import hash_password
from ..services import audit
from ..services import scenarios as svc


def main() -> int:
    email = os.environ.get("MGS_DEMO_ADMIN_EMAIL")
    password = os.environ.get("MGS_DEMO_ADMIN_PASSWORD")
    if not email or not password:
        print("set MGS_DEMO_ADMIN_EMAIL and MGS_DEMO_ADMIN_PASSWORD", file=sys.stderr)
        return 2
    engine()
    gen = get_db()
    db = next(gen)
    if db.scalar(select(Organization).where(Organization.name == "Demo (fictitious)")):
        print("demo organisation already exists")
        return 0
    org = Organization(name="Demo (fictitious)")
    user = db.scalar(select(User).where(User.email == email.lower())) or \
        User(email=email.lower(), name="Demo admin", password_hash=hash_password(password))
    db.add_all([org, user])
    db.flush()
    db.add(Membership(user_id=user.id, org_id=org.id, role=Role.admin))
    p = Project(org_id=org.id, name="Fictitia portfolio (demo)", country="Fictitia",
                description="Invented data for demonstration only.", created_by=user.id)
    db.add(p)
    db.flush()
    v = svc.create_version(db, project=p, scenario="base", assumptions=svc.apply_changes(svc.load_template("demo_fictitious"), {}),
                           options={}, solver_method="excel_macros", user=user,
                           provenance={"source": "template", "template": "demo_fictitious"})
    run = svc.run_version(db, v, user, per_lot=True)
    audit.record(db, org_id=org.id, user_id=user.id, action="demo.seed", entity_type="project", entity_id=p.id)
    try:
        next(gen)
    except StopIteration:
        pass
    print(f"demo project {p.id}, run {run.id} ({run.status})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
