"""Stockage des géométries : aller-retour exact (condition de la reproductibilité)."""

import shapely
from sqlalchemy.orm import Session

from app.db import make_engine
from app.models import Project, Site
from tests.helpers import site_1km


def test_geometry_roundtrip_is_bit_exact(db_url):
    engine = make_engine(db_url)
    geom = site_1km()
    with Session(engine) as s:
        p = Project(name="rt", country_iso3="ZAF", technology="pv")
        s.add(Site(project=p, name="x", boundary=geom))
        s.commit()
        site_id = p.sites[0].id
    with Session(engine) as s:
        back = s.get(Site, site_id).boundary
    engine.dispose()
    assert isinstance(back, shapely.Geometry)
    assert shapely.to_wkb(back) == shapely.to_wkb(geom)
