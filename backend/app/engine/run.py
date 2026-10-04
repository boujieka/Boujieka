"""Run the Opportunity Engine.

    python -m app.engine.run                       # as of today
    python -m app.engine.run --as-of 2026-10-03
"""

import argparse
from datetime import date

from app.db import SessionLocal
from app.engine.opportunities import run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    with SessionLocal() as session:
        stats = run(session, args.as_of)
        session.commit()
    print(f"Opportunity Engine as of {args.as_of}: {stats}")


if __name__ == "__main__":
    main()
