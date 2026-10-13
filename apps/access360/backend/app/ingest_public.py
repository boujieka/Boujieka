"""Load the bundled public reference data into the database.

    python -m app.ingest_public            (uses A360_DATABASE_OWNER_URL)

Runs as the owner role, like the migrations: platform datasets have org_id NULL, which the app role cannot insert
under row level security, and reference_sources / country_profiles are read only for the app role.

The command is idempotent: each platform dataset is matched by its `source_key` and updated in place (its id is
kept), reference sources and country profiles are upserted by key. Every derived file is checked against the
SHA-256 recorded in app/public_data/manifest.json before anything is written; a mismatch aborts the run.
"""
from __future__ import annotations

import json
import sys
from datetime import date

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from .config import get_settings
from .models import CountryProfile, Dataset, ReferenceSource, now
from .reference import AFRICA, DATA_DIR, country_indicators, manifest, read_csv, sha256, source


class ChecksumError(RuntimeError):
    pass


def verify(man: dict) -> None:
    for s in man["sources"]:
        for d in s["derived"]:
            got = sha256(DATA_DIR / d["file"])
            if got != d["sha256"]:
                raise ChecksumError(f"{d['file']}: SHA-256 {got} does not match the manifest ({d['sha256']})")


def _bbox(geom: dict) -> list[float]:
    xs: list[float] = []
    ys: list[float] = []

    def walk(c):
        if isinstance(c[0], (int, float)):
            xs.append(c[0])
            ys.append(c[1])
        else:
            for x in c:
                walk(x)
    walk(geom["coordinates"])
    return [min(xs), min(ys), max(xs), max(ys)]


def _upsert_dataset(s: Session, src: dict) -> Dataset:
    fc = json.loads((DATA_DIR / src["file"]).read_text(encoding="utf-8"))
    raw = src["raw"][0]
    fields = dict(title=src["title"], layer_type=src["layer_type"], source_institution=src["source_institution"],
                  publication_date=src["publication_date"], geographic_coverage=src["geographic_coverage"],
                  resolution=src["resolution"], licence=src["licence"], retrieval_date=date.fromisoformat(src["retrieval_date"]),
                  quality=src["quality"], limitations=src["limitations"], feature_count=len(fc["features"]), geojson=fc,
                  is_demo=False, source_url=raw.get("pinned_url") or raw["url"], source_version=src["version"][:300],
                  attribution=src["attribution"])
    d = s.execute(select(Dataset).where(Dataset.source_key == src["key"], Dataset.org_id.is_(None))).scalar_one_or_none()
    if d is None:
        d = Dataset(org_id=None, source_key=src["key"], **fields)
        s.add(d)
    else:
        for k, v in fields.items():
            if getattr(d, k) != v:
                setattr(d, k, v)
    return d


def _upsert_source(s: Session, src: dict) -> None:
    fields = dict(kind=src["kind"], title=src["title"], source_institution=src["source_institution"], licence=src["licence"],
                  attribution=src["attribution"], quality=src["quality"],
                  retrieval_date=date.fromisoformat(src["retrieval_date"]), record=src)
    r = s.get(ReferenceSource, src["key"])
    if r is None:
        s.add(ReferenceSource(key=src["key"], ingested_at=now(), **fields))
    elif any(getattr(r, k) != v for k, v in fields.items()):
        for k, v in fields.items():
            setattr(r, k, v)
        r.ingested_at = now()


def ingest(owner_url: str | None = None) -> dict:
    man = manifest()
    verify(man)
    eng = create_engine(owner_url or get_settings().database_owner_url, future=True)
    counts = {"datasets": 0, "sources": 0, "profiles": 0}
    try:
        with Session(eng) as s, s.begin():
            for src in man["sources"]:
                _upsert_source(s, src)
                counts["sources"] += 1
                if src["kind"] == "dataset":
                    _upsert_dataset(s, src)
                    counts["datasets"] += 1
            admin0 = json.loads((DATA_DIR / source("ne_admin0_africa", man)["file"]).read_text(encoding="utf-8"))["features"]
            admin1 = json.loads((DATA_DIR / source("ne_admin1_africa", man)["file"]).read_text(encoding="utf-8"))["features"]
            places = json.loads((DATA_DIR / source("ne_populated_places_africa", man)["file"]).read_text(encoding="utf-8"))["features"]
            owid_rows = read_csv(source("owid_energy", man)["file"])
            wdi_rows = read_csv(source("wdi_eg_elc_accs_zs", man)["file"])
            for iso3, name in AFRICA:
                b = next((f for f in admin0 if f["properties"]["iso3"] == iso3), None)
                fields = dict(name=name, bbox=_bbox(b["geometry"]) if b else None,
                              indicators=country_indicators(iso3, man, owid_rows, wdi_rows),
                              admin1_count=sum(1 for f in admin1 if f["properties"]["iso3"] == iso3),
                              places_count=sum(1 for f in places if f["properties"]["iso3"] == iso3))
                p = s.get(CountryProfile, iso3)
                if p is None:
                    s.add(CountryProfile(iso3=iso3, ingested_at=now(), **fields))
                elif any(getattr(p, k) != v for k, v in fields.items()):
                    for k, v in fields.items():
                        setattr(p, k, v)
                    p.ingested_at = now()
                counts["profiles"] += 1
    finally:
        eng.dispose()
    return counts


def main() -> None:
    try:
        counts = ingest()
    except ChecksumError as e:
        print(f"Aborted: {e}", file=sys.stderr)
        raise SystemExit(2) from e
    print(f"Public reference data loaded: {counts['datasets']} platform datasets, {counts['sources']} sources, "
          f"{counts['profiles']} country profiles")


if __name__ == "__main__":
    main()
