"""Le projet de démonstration se charge, reste marqué fictif et se recharge sans doublon."""

from sqlalchemy import func, select
from sqlalchemy.orm import sessionmaker

from app import demo
from app.db import make_engine
from app.models import Dataset, Project


def test_demo_load_is_idempotent_and_fictional(db_url, monkeypatch, client):
    engine = make_engine(db_url)
    monkeypatch.setattr(demo, "SessionLocal", sessionmaker(bind=engine, expire_on_commit=False))
    demo.load()
    demo.load()
    with demo.SessionLocal() as db:
        assert db.scalar(select(func.count()).select_from(Project)) == 1
        p = db.execute(select(Project)).scalar_one()
        assert p.is_fictional and len(p.sites) == 2 and len(p.rules) == 3
        assert all(d.is_synthetic for d in db.execute(select(Dataset)).scalars())
        site_id = p.sites[0].id
    run = client.post(f"/api/v1/sites/{site_id}/analyses", json={}).json()
    assert run["results"]["donnees_fictives"] is True
    ind = run["results"]["indicateurs"]
    assert 0 < ind["surface_nette"]["valeur_m2"] < ind["surface_brute"]["valeur_m2"]
    assert ind["chevauchement_non_double_compte"]["valeur_m2"] > 0  # zones humides qui se chevauchent
    assert all(c["ok"] for c in run["results"]["controles"])
    engine.dispose()
