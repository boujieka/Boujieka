"""Pre-deploy guard for site/dist: refuse to publish a partial, mixed or empty build.

    python3 scripts/check_dist.py [--as-of YYYY-MM-DD]

Checks: the pages and files exist and are not empty; the platform's embedded data, the home page
and veille.json carry the same as_of (and the expected one when given); the verified dataset is not
empty. Exit code 1 with the reasons otherwise.
"""

import argparse
import json
import re
import sys
from pathlib import Path

DIST = Path(__file__).resolve().parents[1] / "site" / "dist"


def embedded(path: Path, script_id: str) -> dict:
    m = re.search(rf'<script (?=[^>]*id="{script_id}")[^>]*type="application/json"[^>]*>(.*?)</script>', path.read_text(), re.S)
    if not m:
        raise ValueError(f"{path.name}: no embedded data")
    return json.loads(m.group(1))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--as-of")
    p.add_argument("--dist", type=Path, default=DIST)
    a = p.parse_args()
    d, errors = a.dist, []
    for f in ("index.html", "plateforme.html", "veille.json", "simcalc.js", "netlify.toml", "donnees/auctions.csv"):
        if not (d / f).is_file() or (d / f).stat().st_size == 0:
            errors.append(f"missing or empty: {f}")
    if errors:
        print("\n".join(errors))
        return 1
    try:
        plat = embedded(d / "plateforme.html", "data")
        home = embedded(d / "index.html", "home-data")
        veille = json.loads((d / "veille.json").read_text())
    except ValueError as e:
        print(f"unreadable build: {e}")
        return 1
    dates = {"plateforme.html": plat.get("as_of"), "index.html": home.get("as_of"), "veille.json": veille.get("as_of")}
    if len(set(dates.values())) != 1:
        errors.append(f"as_of differ: {dates}")
    if a.as_of and plat.get("as_of") != a.as_of:
        errors.append(f"as_of is {plat.get('as_of')}, expected {a.as_of}")
    if not (plat.get("data") or {}).get("real_auctions"):
        errors.append("no verified auction in the build")
    print("\n".join(errors) if errors else f"site/dist OK: as_of {plat.get('as_of')}, {plat['data']['real_auctions']} verified auctions")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
