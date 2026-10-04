"""BEAC (CEMAC regional central bank): government-securities auction notices.

Official page (checked 2026-10-04):
  https://www.beac.int/m-des-titres-publics/annonces-et-communiques/
One static HTML table (`#documents_contenu_cpt`, columns Titre du document | Taille | Pays | Année,
newest first, no server pagination) lists ~992 PDFs, 2019 → Sep 2026: auction announcements
("Communiqué d'annonce", "Announcement issuance", "Aviso de comunicado"), auction results
("Communiqué des résultats", "Auction results communique", "Comunicado de resultados"), weekly
market reports ("Rapport hebdomadaire", "Tableau de bord/hebdomadaire") and a few others
(calendars, financial-inclusion indicators, yield curves, a buyback notice).

File names and upload folders are inconsistent (many 2024–2026 files sit in /2016/11/), and the
"Pays" column is unreliable (misspelt, sometimes wrong): neither is used as data. The country of a
staged row comes from the issue code printed in the notice (checked against the printed text).
The listing date (from the title, else 1 January of the "Année" column) only selects documents
for --since/--until; it is never stored as a fact.

Every notice is a scanned image: documents are OCRed twice (app.ingest.beac_ocr), parsed by
app.ingest.beac_extract into UNVERIFIED staging rows, and promoted only by the strict checker
app.ingest.beac_check.

Use: free publication with attribution, under the written authorisation BEAC gave the owner
(no resale). Every staged and promoted row carries the source URL, the document SHA-256 and the
attribution line ATTRIBUTION.

Run:
    python -m app.ingest.beac --kind result --since 2019-01-01        # download + OCR + stage
    python -m app.ingest.beac --kind announcement                      # settlement dates
    python -m app.ingest.beac --kind all --no-extract                  # only download
    python -m app.ingest.beac --reextract                              # re-parse stored docs
"""

import argparse
import html as htmllib
import re
import time
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingest.umoa import Fetched, save_document
from app.models import Source, SourceDocument
from app.models.enums import SourceCategory, SourceStatus

SOURCE_NAME = "BEAC — marché des titres publics"
INSTITUTION = "Banque des États de l'Afrique Centrale (BEAC)"
LISTING_URL = "https://www.beac.int/m-des-titres-publics/annonces-et-communiques/"
TABLE_ID = "documents_contenu_cpt"
USER_AGENT = "CartoucheIngest/1.0 (https://cartouche-africa.netlify.app)"
REQUEST_PAUSE_SECONDS = 1.0  # at least one second between two requests to beac.int
ATTRIBUTION = ("Source : BEAC — marché des titres publics de la CEMAC (www.beac.int), publié avec "
               "l'autorisation écrite de la BEAC pour une diffusion gratuite (pas de revente).")

KINDS = ("result", "announcement", "weekly_report", "other")
DOCUMENT_TYPES = {"result": "auction_result", "announcement": "auction_announcement",
                  "weekly_report": "weekly_market_report", "other": "other"}


def fold(text: str) -> str:
    text = htmllib.unescape(text).replace("’", "'").replace("\xa0", " ")
    text = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return " ".join(text.split()).lower()


# --------------------------------------------------------------------------- listing


@dataclass
class ListingEntry:
    url: str
    title: str
    size: str
    country_label: str  # the listing's "Pays" column, as printed (unreliable; informational)
    year: int | None  # the listing's "Année" column
    kind: str
    language: str  # fr | en | es

    @property
    def listing_date(self) -> date | None:
        """Date for selection only: from the title, else 1 January of the Année column."""
        return title_date(self.title) or (date(self.year, 1, 1) if self.year else None)


class _ListingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.rows: list[tuple[list[str], list[str]]] = []
        self._cells: list[str] | None = None
        self._links: list[str] = []
        self._cell: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            if self.depth:
                self.depth += 1
            elif a.get("id") == TABLE_ID:
                self.depth = 1
        if not self.depth:
            return
        if tag == "tr":
            self._cells, self._links = [], []
        elif tag == "td" and self._cells is not None:
            self._cell = []
        elif tag == "a" and self._cells is not None and a.get("href"):
            self._links.append(a["href"])

    def handle_endtag(self, tag):
        if not self.depth:
            return
        if tag == "td" and self._cell is not None and self._cells is not None:
            self._cells.append(" ".join("".join(self._cell).split()))
            self._cell = None
        elif tag == "tr" and self._cells is not None:
            if self._cells:
                self.rows.append((self._cells, self._links))
            self._cells = None
        elif tag == "table":
            self.depth -= 1

    def handle_data(self, data):
        if self.depth and self._cell is not None:
            self._cell.append(data)


def classify(title: str) -> str:
    """result / announcement / weekly_report / other, from the listing title only."""
    t = fold(title)
    if re.search(r"rapport hebdo|tableau (de bord|hebdo)|weekly", t):
        return "weekly_report"
    if re.search(r"rachat|buyback|recompra", t):
        return "other"  # buyback notices and results: another layout, not parsed
    if re.search(r"resultat|results?\b|resultad", t):
        return "result"
    if re.search(r"annon|annou|anouncement|aviso|avis d'appel|avis d appel|appel d'offres", t):
        return "announcement"
    return "other"


def language(title: str) -> str:
    t = fold(title)
    if re.search(r"\b(comunicado|aviso|resultad|sesion|emision|republica)\b", t):
        return "es"
    if re.search(r"\b(announcement|annoucement|anouncement|auctions?|results|issuance|session|republic)\b", t):
        return "en"
    return "fr"


def parse_listing(html: str) -> list[ListingEntry]:
    p = _ListingParser()
    p.feed(html)
    out = []
    for cells, links in p.rows:
        if len(cells) < 4 or not links:
            continue
        url = links[0]
        if not url.lower().endswith(".pdf"):
            continue
        title = cells[0]
        year = int(cells[3]) if cells[3].strip().isdigit() else None
        out.append(ListingEntry(url=url, title=title, size=cells[1], country_label=cells[2], year=year,
                                kind=classify(title), language=language(title)))
    return out


MONTHS = {
    "janvier": 1, "janv": 1, "jan": 1, "january": 1, "enero": 1,
    "fevrier": 2, "fevr": 2, "fev": 2, "february": 2, "febuary": 2, "feb": 2, "febrero": 2,
    "mars": 3, "march": 3, "mar": 3, "marzo": 3,
    "avril": 4, "avr": 4, "april": 4, "apr": 4, "abril": 4,
    "mai": 5, "may": 5, "mayo": 5,
    "juin": 6, "june": 6, "jun": 6, "junio": 6,
    "juillet": 7, "juil": 7, "july": 7, "jul": 7, "julio": 7,
    "aout": 8, "august": 8, "aug": 8, "agosto": 8,
    "septembre": 9, "sept": 9, "sep": 9, "september": 9, "septiembre": 9,
    "octobre": 10, "oct": 10, "octo": 10, "october": 10, "octubre": 10,
    "novembre": 11, "nov": 11, "november": 11, "noviembre": 11,
    "decembre": 12, "dec": 12, "dece": 12, "december": 12, "diciembre": 12,
}
_MONTH_RE = "|".join(sorted(MONTHS, key=len, reverse=True))
_TITLE_DATE_RES = (
    re.compile(rf"\b(\d{{1,2}})(?:er|st|nd|rd|th)?(?: of)?[\s-]+({_MONTH_RE})\.?[\s-]+(?:de[l]? )?(\d{{4}})\b"),
    re.compile(rf"\b({_MONTH_RE})\.?\s+(\d{{1,2}})(?:er|st|nd|rd|th)?,?\s+(\d{{4}})\b"),
    re.compile(r"\b(\d{2})[-/.](\d{2})[-/.](\d{4})\b"),
)


def title_date(title: str) -> date | None:
    t = fold(title)
    for i, rx in enumerate(_TITLE_DATE_RES):
        m = rx.search(t)
        if not m:
            continue
        try:
            if i == 0:
                return date(int(m[3]), MONTHS[m[2]], int(m[1]))
            if i == 1:
                return date(int(m[3]), MONTHS[m[1]], int(m[2]))
            return date(int(m[3]), int(m[2]), int(m[1]))
        except (ValueError, KeyError):
            continue
    return None


# --------------------------------------------------------------------------- network


_last_request = [0.0]


def http_get(url: str, timeout: float = 90, retries: int = 3, pause: float = REQUEST_PAUSE_SECONDS) -> Fetched:
    """Polite GET: identifies itself, waits at least `pause` seconds between requests."""
    last = None
    for attempt in range(retries):
        wait = _last_request[0] + pause - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        try:
            r = httpx.get(url, timeout=timeout, follow_redirects=True, headers={"User-Agent": USER_AGENT})
            _last_request[0] = time.monotonic()
            if r.status_code >= 500:
                last = f"HTTP {r.status_code}"
                time.sleep(3 * (attempt + 1))
                continue
            return Fetched(r.status_code, str(r.url), r.content, r.headers.get("content-type"))
        except httpx.HTTPError as e:
            _last_request[0] = time.monotonic()
            last = f"{type(e).__name__}: {e}"[:300]
            time.sleep(3 * (attempt + 1))
    return Fetched(None, url, b"", None, last)


Fetcher = Callable[[str], Fetched]


# --------------------------------------------------------------------------- storage


def get_or_create_source(session: Session) -> Source:
    source = session.scalar(select(Source).where(Source.name == SOURCE_NAME))
    if source is None:
        source = Source(
            name=SOURCE_NAME,
            institution=INSTITUTION,
            category=SourceCategory.CENTRAL_BANK,
            country_id=None,  # regional: the six CEMAC states
            base_url=LISTING_URL,
            status=SourceStatus.ACTIVE,
            crawl_config={"listing_url": LISTING_URL, "table_id": TABLE_ID, "user_agent": USER_AGENT,
                          "pause_seconds": REQUEST_PAUSE_SECONDS},
            notes=("Regional (CEMAC: CMR, CAF, TCD, COG, GNQ, GAB). Scanned notices, OCRed twice and "
                   "checked by app.ingest.beac_check. " + ATTRIBUTION),
        )
        session.add(source)
        session.flush()
    return source


def document_title(entry: ListingEntry) -> str:
    return f"BEAC — {entry.title} ({entry.country_label}, {entry.year})"


# --------------------------------------------------------------------------- orchestration


def select_entries(entries: list[ListingEntry], kinds: set[str], since: date | None, until: date | None,
                   limit: int | None) -> list[ListingEntry]:
    out = [e for e in entries if e.kind in kinds
           and (since is None or (e.listing_date or date.max) >= since)
           and (until is None or (e.listing_date or date.min) <= until)]
    return out[:limit] if limit else out


def run(session: Session, kinds: set[str], since: date | None = None, until: date | None = None,
        limit: int | None = None, refresh: bool = False, extract: bool = True,
        fetch: Fetcher = http_get, log: Callable[[str], None] = lambda _: None) -> dict:
    source = get_or_create_source(session)
    stats: dict = {"listed": 0, "listed_by_kind": {}, "selected": 0, "skipped_known_url": 0,
                   "downloaded": 0, "new_documents": 0, "fetch_errors": 0, "staged_rows": 0, "errors": []}
    now = datetime.now(timezone.utc)
    source.last_checked_at = now
    res = fetch(LISTING_URL)
    if res.status != 200 or not res.content:
        source.last_error = f"listing: {res.error or f'HTTP {res.status}'}"
        stats["errors"].append(source.last_error)
        return stats
    entries = parse_listing(res.content.decode("utf-8", errors="replace"))
    stats["listed"] = len(entries)
    for e in entries:
        stats["listed_by_kind"][e.kind] = stats["listed_by_kind"].get(e.kind, 0) + 1
    chosen = select_entries(entries, kinds, since, until, limit)
    stats["selected"] = len(chosen)
    for e in chosen:
        known = session.scalar(select(SourceDocument).where(SourceDocument.url == e.url))
        if known is not None and not refresh:
            stats["skipped_known_url"] += 1
            continue
        got = fetch(e.url)
        if got.status != 200 or not got.content or got.content[:5] != b"%PDF-":
            stats["fetch_errors"] += 1
            stats["errors"].append(f"{e.url}: {got.error or f'HTTP {got.status}'}")
            continue
        stats["downloaded"] += 1
        doc, created = save_document(session, source, e.url, got.content, got.content_type,
                                     document_title(e), DOCUMENT_TYPES[e.kind])
        stats["new_documents"] += int(created)
        session.commit()
        log(f"{e.kind:13s} {e.year} {e.title[:90]} {'new' if created else 'same bytes'}")
    if extract:
        from app.ingest.beac_extract import extract_stored

        st = extract_stored(session, kinds & {"result", "announcement"}, log=log)
        stats["staged_rows"] = st.get("staged_rows", 0)
        stats["extraction"] = st
    source.last_success_at = now
    source.last_error = None
    session.flush()
    return stats


def main() -> None:
    from app.db import SessionLocal

    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--since", type=date.fromisoformat)
    parser.add_argument("--until", type=date.fromisoformat)
    parser.add_argument("--limit", type=int, help="first N selected listing entries (newest first)")
    parser.add_argument("--kind", default="result", choices=[*KINDS, "all", "result+announcement"])
    parser.add_argument("--refresh", action="store_true", help="re-download URLs already stored")
    parser.add_argument("--no-extract", action="store_true", help="download only (no OCR)")
    parser.add_argument("--reextract", action="store_true", help="OCR/parse stored documents only (no network)")
    parser.add_argument("--workers", type=int, default=4, help="parallel OCR processes")
    args = parser.parse_args()
    kinds = set(KINDS) if args.kind == "all" else (
        {"result", "announcement"} if args.kind == "result+announcement" else {args.kind})
    with SessionLocal() as session:
        if args.reextract:
            from app.ingest.beac_extract import extract_stored

            stats = extract_stored(session, kinds, workers=args.workers, log=print)
        else:
            stats = run(session, kinds, args.since, args.until, args.limit, args.refresh,
                        extract=not args.no_extract, log=print)
        session.commit()
    errors = stats.pop("errors", []) if isinstance(stats, dict) else []
    for k, v in stats.items():
        print(f"{k}: {v}")
    for e in errors[:30]:
        print("error:", e)


if __name__ == "__main__":
    main()
