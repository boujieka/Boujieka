"""Seed commands. Demo points are placed at sea in the Gulf of Guinea on purpose, so that no synthetic project can be
mistaken for a real settlement.

    python -m app.seed demo          creates the demo workspace with clearly labelled synthetic projects
    python -m app.seed superadmin    creates a platform administrator from A360_ADMIN_EMAIL / A360_ADMIN_PASSWORD

No password is hard coded. The demo password comes from A360_DEMO_PASSWORD or is generated and printed once.
"""
from __future__ import annotations

import os
import secrets
import sys
from datetime import date, timedelta

from sqlalchemy import select

from .db import engine, get_session, set_tenant
from .engine.demo import demo_inputs
from .engine.inputs import GridArrival
from .models import Dataset, Membership, Milestone, ModelRun, Organization, Project, User
from .security import hash_password
from .services.runs import execute

DEMO_ORG = "Demo workspace (synthetic data)"
DEMO_EMAIL = "demo@access360.example"


def _session():
    engine()
    return next(get_session())


def seed_demo() -> None:
    s = _session()
    if s.execute(select(Organization).where(Organization.name == DEMO_ORG)).scalar_one_or_none():
        print("Demo workspace already exists")
        return
    pw = os.environ.get("A360_DEMO_PASSWORD") or secrets.token_urlsafe(12) + "A1"
    u = s.execute(select(User).where(User.email == DEMO_EMAIL)).scalar_one_or_none()
    if u is None:
        u = User(email=DEMO_EMAIL, password_hash=hash_password(pw), full_name="Demo user")
        s.add(u)
    o = Organization(name=DEMO_ORG, kind="developer", is_demo=True, plan="developer_pro")
    s.add(o)
    s.flush()
    s.add(Membership(user_id=u.id, org_id=o.id, role="owner"))
    s.flush()
    set_tenant(s, o.id)
    variants = [
        ("Demo site batch A (synthetic)", 0.60, 2.40, "financing", None),
        ("Demo site B, grid arrives year 9 (synthetic)", 0.35, 2.10, "feasibility",
         GridArrival(enabled=True, operating_year=9, treatment="asset_transfer", compensation_pct_nbv=0.5,
                     regulatory_source="SYNTHETIC: illustrative treatment, no country rule")),
        ("Demo site C, lower tariff (synthetic)", 0.85, 2.75, "screening", "low_tariff"),
    ]
    for name, lat, lon, stage, variant in variants:
        pin = demo_inputs()
        pin.project_name = name
        if isinstance(variant, GridArrival):
            pin.grid_arrival = variant
        elif variant == "low_tariff":
            for c in pin.customers:
                c.tariff_per_kwh *= 0.8
        p = Project(org_id=o.id, name=name, country="Demo country (fictional)", stage=stage, latitude=lat, longitude=lon,
                    inputs=pin.model_dump(mode="json"), inputs_version=1, is_demo=True, created_by=u.id)
        s.add(p)
        s.flush()
        out = execute(pin)
        s.add(ModelRun(org_id=o.id, project_id=p.id, inputs_version=1, inputs_snapshot=p.inputs, is_demo=True, created_by=u.id,
                       **{k: out[k] for k in ("engine_version", "status", "metrics", "checks", "warnings", "missing_inputs",
                                              "annual", "sources_uses", "quarterly", "inputs_sha256")}))
        for i, (t, cat) in enumerate([("Feasibility study signed off", "feasibility"), ("Environmental and social screening", "esia"),
                                      ("Tariff application filed", "tariff"), ("Term sheet with lender", "financing")]):
            s.add(Milestone(org_id=o.id, project_id=p.id, title=t, category=cat, due_date=date.today() + timedelta(days=30 * (i + 1) - 45),
                            status="done" if i == 0 else "open", owner_name="Demo team"))
    feats = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]},
              "properties": {"name": f"Synthetic settlement {i + 1}", "households": hh}}
             for i, (lat, lon, hh) in enumerate([(0.60, 2.40, 600), (0.35, 2.10, 420), (0.85, 2.75, 350), (0.20, 2.60, 280)])]
    s.add(Dataset(org_id=o.id, title="Synthetic demo settlements", layer_type="settlements", source_institution="ACCESS360 demo generator",
                  publication_date=str(date.today()), geographic_coverage="Demo points placed at sea in the Gulf of Guinea on purpose", resolution="Point",
                  licence="Demo only", retrieval_date=date.today(), quality="synthetic_demo",
                  limitations="SYNTHETIC: locations are arbitrary and do not represent real settlements, populations or electrification status.",
                  feature_count=len(feats), geojson={"type": "FeatureCollection", "features": feats}, is_demo=True))
    s.commit()
    print(f"Demo workspace created. Login: {DEMO_EMAIL}")
    if not os.environ.get("A360_DEMO_PASSWORD"):
        print(f"Generated demo password (shown once): {pw}")


def seed_superadmin() -> None:
    email, pw = os.environ.get("A360_ADMIN_EMAIL"), os.environ.get("A360_ADMIN_PASSWORD")
    if not email or not pw:
        sys.exit("Set A360_ADMIN_EMAIL and A360_ADMIN_PASSWORD")
    s = _session()
    u = s.execute(select(User).where(User.email == email.lower())).scalar_one_or_none()
    if u is None:
        u = User(email=email.lower(), password_hash=hash_password(pw), full_name="Platform administrator")
        s.add(u)
    u.is_superadmin = True
    s.commit()
    print(f"Platform administrator ready: {email}. Enable MFA at first login; admin actions require it.")


if __name__ == "__main__":
    {"demo": seed_demo, "superadmin": seed_superadmin}[sys.argv[1]]()
