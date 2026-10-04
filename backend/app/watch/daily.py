"""Daily update ("veille") pipeline. Idempotent for a given date.

    python -m app.watch.daily --as-of 2026-10-04 \\
        --previous https://cartouche-africa.netlify.app/veille.json --out ../site/dist

Steps:
  1. Reference data for the 54 countries (upsert).
  2. Verified real market data loaded from the repository (app/seed/data, see app.seed.verified).
     The labelled synthetic generator runs only with --synthetic, or while no verified file exists.
  3. Opportunity Engine re-run for the as-of date.
  4. REAL watch of official source pages: reachability, changed pages, new documents.
  5. Writes veille.json (report + state + history) and rebuilds the static site.

State between runs lives in the previously published veille.json, so the job needs no
persistent disk. If the previous file cannot be read, the run records a fresh baseline.
"""

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import httpx
from sqlalchemy import select

from app.db import SessionLocal
from app.engine.opportunities import run as run_engine
from app.models import Source
from app.seed import verified
from app.seed.load import load_reference, load_synthetic
from app.watch.sources import Target, check, summarize, to_json

HISTORY_KEPT = 60  # daily summaries
FEED_KEPT = 150  # most recent new-document detections

REPO = Path(__file__).resolve().parents[3]


def targets_from_sources(sources: list[Source]) -> list[Target]:
    out: list[Target] = []
    seen: set[str] = set()
    for s in sources:
        if s.is_synthetic:
            continue
        urls = ([(s.base_url, "Confirmed source URL")] if s.base_url else []) + [
            (c["url"], c.get("purpose", "")) for c in s.candidates
        ]
        for url, purpose in urls:
            if url not in seen:
                seen.add(url)
                out.append(Target(url=url, source_name=s.name, institution=s.institution, purpose=purpose))
    return out


def load_previous(src: str | None) -> dict | None:
    """Previous veille.json from a URL or a file path; None if unavailable."""
    if not src:
        return None
    try:
        if src.startswith(("http://", "https://")):
            r = httpx.get(src, timeout=30, follow_redirects=True)
            if r.status_code != 200:
                return None
            return r.json()
        path = Path(src)
        return json.loads(path.read_text()) if path.exists() else None
    except (httpx.HTTPError, ValueError, OSError):
        return None


def build_veille(as_of: date, previous: dict | None, reports, state: dict, now: datetime) -> dict:
    baseline = state.get("baseline", False)
    summary = summarize(reports, baseline)
    new_docs = [
        {**d, "institution": r.institution, "source_name": r.source_name, "page": r.url,
         "detected_at": now.isoformat()}
        for r in reports
        for d in r.new_documents
    ]
    history = ((previous or {}).get("history") or [])
    history = [h for h in history if h.get("as_of") != as_of.isoformat()]  # same-day rerun replaces
    history = (history + [{"as_of": as_of.isoformat(), "run_at": now.isoformat(), **summary}])[-HISTORY_KEPT:]
    feed = [f for f in ((previous or {}).get("feed") or []) if f["url"] not in {d["url"] for d in new_docs}]
    feed = (new_docs + feed)[:FEED_KEPT]
    return {
        "as_of": as_of.isoformat(),
        "run_at": now.isoformat(),
        "summary": summary,
        "pages": to_json(reports),
        "new_documents": new_docs,
        "feed": feed,
        "history": history,
        "state": state,
        "note": "Real checks of official pages. A new document link is a lead to review, not a "
        "verified market event.",
    }


AUTO_REVIEWER = "Claude - routine quotidienne, controles automatiques stricts (instruction du proprietaire, 2026-10-04)"
AUTO_NOTE = ("Daily run: strict autocheck (re-download + SHA-256, independent pdftotext, column placement, unit "
             "re-derivation, whole-number tenor, no number fragments, consistency checks). Not a human review.")
LOOKBACK_DAYS = 45  # re-scan the recent past: late publications and corrected reports


def ingest_and_approve(session, as_of: date) -> dict:
    """Collect recent UMOA-Titres result reports, approve rows that pass every strict check, and
    export the verified dataset. Rows that fail stay UNVERIFIED in this run's queue (not exported)."""
    from datetime import timedelta

    from sqlalchemy import func

    from app.ingest import autocheck, umoa
    from app.models import Auction

    last = session.scalar(select(func.max(Auction.auction_date)).where(Auction.is_synthetic.is_(False)))
    since = (last or as_of) - timedelta(days=LOOKBACK_DAYS)
    stats = umoa.run(session, since=since)
    session.commit()
    report = autocheck.run(session, True, AUTO_REVIEWER, AUTO_NOTE)
    exported = verified.export(session)
    return {"since": since.isoformat(), "documents_new": stats.get("documents_new"),
            "extractions": stats.get("extractions"), "fetch_errors": stats.get("fetch_errors"),
            "approved": report["approved"], "held": len(report["held"]),
            "approval_errors": len(report["approve_errors"]), "exported": exported}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--previous", help="URL or path of the previous veille.json")
    parser.add_argument("--out", type=Path, default=REPO / "site" / "dist")
    parser.add_argument("--skip-watch", action="store_true", help="skip network checks (offline runs)")
    parser.add_argument("--ingest", action="store_true",
                        help="collect new UMOA-Titres results, approve those passing the strict checker, "
                             "and export the verified dataset (owner's instruction of 2026-10-04)")
    parser.add_argument("--synthetic", action="store_true",
                        help="development only: also roll the labelled synthetic generator forward")
    args = parser.parse_args()
    now = datetime.now(timezone.utc)

    with SessionLocal() as session:
        countries = load_reference(session)
        real = verified.load(session)  # verified real data versioned in the repo (app/seed/data)
        if args.ingest:
            session.commit()
            print("Ingestion:", ingest_and_approve(session, args.as_of))
        # Until a verified dataset is committed, keep the labelled synthetic data so the site is not empty.
        use_synthetic = args.synthetic or not verified.DATA_FILE.exists()
        added = load_synthetic(session, countries, args.as_of) if use_synthetic else 0
        session.flush()
        engine = run_engine(session, args.as_of)
        print(f"Verified data loaded {real}; synthetic auctions added: {added}; engine {engine}")

        previous = load_previous(args.previous)
        sources = list(session.scalars(select(Source)))
        targets = targets_from_sources(sources)
        if args.skip_watch:
            reports, state = [], (previous or {}).get("state") or {"pages": {}, "baseline": previous is None}
        else:
            reports, state = check(targets, (previous or {}).get("state"), now=now)
            by_source: dict[str, list] = {}
            for r in reports:
                by_source.setdefault(r.source_name, []).append(r)
            for s in sources:
                rs = by_source.get(s.name)
                if rs:
                    s.last_checked_at = now
                    failures = [r.error for r in rs if not r.reachable]
                    s.last_error = "; ".join(f for f in failures if f)[:1000] if len(failures) == len(rs) else None
        session.commit()

    veille = build_veille(args.as_of, previous, reports, state, now)
    args.out.mkdir(parents=True, exist_ok=True)
    veille_path = args.out / "veille.json"
    veille_path.write_text(json.dumps(veille, ensure_ascii=False, separators=(",", ":")))
    print(f"Veille: {veille['summary']} -> {veille_path}")

    subprocess.run(
        [sys.executable, str(REPO / "site" / "build.py"), "--as-of", args.as_of.isoformat(),
         "--veille", str(veille_path)],
        check=True,
    )


if __name__ == "__main__":
    main()
