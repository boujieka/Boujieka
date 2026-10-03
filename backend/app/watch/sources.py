"""Daily watch of official source pages (real network checks, FACT-level observations).

For every proposed or confirmed source URL, the watcher records:
  * whether the page answered (HTTP status, final URL after redirects, page title);
  * a SHA-256 of the page's visible text (scripts and styles removed), to flag pages that changed;
  * the document links on the page (PDF, Word, Excel), to flag newly published documents.

Comparison is against the previous run's state, which the caller passes in (the daily job keeps
it in the published site's veille.json, because containers are ephemeral). On the first run
there is nothing to compare against: the run records a baseline and reports no "new" items.

This module only observes pages. It does not extract auction figures (Phase 2), and a new
document link is a lead to review, not a verified market event.
"""

import hashlib
import re
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import httpx

USER_AGENT = "Mozilla/5.0 (compatible; CartoucheWatch/1.0; +https://cartouche-africa.netlify.app)"
DOC_PATTERN = re.compile(r"\.(pdf|docx?|xlsx?)($|[?#])", re.IGNORECASE)
MAX_LINKS_KEPT = 20_000  # per page, in state (as 12-hex ids); far above any page seen so far
# Anti-bot / redirect interstitials answer HTTP 200 but are not the real page. Treating them as
# a successful check would wipe the page's known links and make every link "new" next time.
INTERSTITIAL_MARKERS = (
    "you are being redirected", "just a moment", "checking your browser", "enable javascript and cookies",
    "attention required", "verify you are human", "ddos protection",
)
MIN_TEXT_CHARS = 200  # visible text below this is treated as an interstitial or empty shell
MAX_NEW_PER_PAGE = 25  # cap reported new documents per page (a redesign can expose hundreds)


def link_id(url: str) -> str:
    """Compact, stable id for a document URL, used in persisted state (keeps veille.json small)."""
    return hashlib.sha1(url.encode()).hexdigest()[:12]


def _known_ids(prev: dict | None) -> list[str]:
    if not prev:
        return []
    # Older state stored full URLs under "links"; convert transparently.
    return prev.get("link_ids") or [link_id(u) for u in prev.get("links", [])]


@dataclass
class Target:
    url: str
    source_name: str
    institution: str
    purpose: str


@dataclass
class FetchResult:
    status: int | None
    final_url: str | None
    body: bytes
    error: str | None


@dataclass
class PageReport:
    url: str
    source_name: str
    institution: str
    purpose: str
    checked_at: str
    reachable: bool
    http_status: int | None
    final_url: str | None
    title: str | None
    text_sha256: str | None
    document_count: int
    changed: bool  # visible text differs from previous run (False on baseline)
    new_documents: list[dict] = field(default_factory=list)
    error: str | None = None


class _PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._in_title = False
        self._skip = 0
        self._href: str | None = None
        self._link_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self._skip += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "a":
            self._href = dict(attrs).get("href")
            self._link_text = []

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self._skip:
            self._skip -= 1
        elif tag == "title":
            self._in_title = False
        elif tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join("".join(self._link_text).split())))
            self._href = None

    def handle_data(self, data):
        if self._skip:
            return
        if self._in_title:
            self.title_parts.append(data)
        self.text_parts.append(data)
        if self._href is not None:
            self._link_text.append(data)


def is_interstitial(html: str) -> bool:
    p = _PageParser()
    try:
        p.feed(html)
    except Exception:
        pass
    text = " ".join(" ".join(p.text_parts).split()).lower()
    return len(text) < MIN_TEXT_CHARS or any(m in text[:2000] for m in INTERSTITIAL_MARKERS)


def parse_page(html: str, base_url: str) -> tuple[str | None, str, list[dict]]:
    """Return (title, sha256 of visible text, document links [{url, text}])."""
    p = _PageParser()
    try:
        p.feed(html)
    except Exception:  # malformed HTML: keep what was parsed
        pass
    title = " ".join("".join(p.title_parts).split()) or None
    text = " ".join(" ".join(p.text_parts).split())
    seen: set[str] = set()
    docs: list[dict] = []
    for href, label in p.links:
        if not href or href.startswith(("mailto:", "javascript:", "#")):
            continue
        absolute = urljoin(base_url, href.strip())
        if urlparse(absolute).scheme not in ("http", "https") or not DOC_PATTERN.search(absolute):
            continue
        if absolute not in seen:
            seen.add(absolute)
            docs.append({"url": absolute, "text": label[:200]})
    return title, hashlib.sha256(text.encode()).hexdigest(), docs


def http_fetch(url: str, timeout: float = 30, retries: int = 3) -> FetchResult:
    """GET with retries for transient network errors. Honours proxy env vars."""
    last_error = None
    for attempt in range(retries):
        try:
            r = httpx.get(url, timeout=timeout, follow_redirects=True, headers={"User-Agent": USER_AGENT})
            return FetchResult(r.status_code, str(r.url), r.content, None)
        except httpx.HTTPError as e:
            last_error = f"{type(e).__name__}: {e}"[:300]
            time.sleep(2 * (attempt + 1))
    return FetchResult(None, None, b"", last_error)


def check(
    targets: list[Target],
    previous: dict | None,
    fetch: Callable[[str], FetchResult] = http_fetch,
    now: datetime | None = None,
) -> tuple[list[PageReport], dict]:
    """Check every target; return reports and the new state to persist for the next run."""
    now = now or datetime.now(timezone.utc)
    prev_pages: dict = (previous or {}).get("pages", {})
    baseline = previous is None
    reports: list[PageReport] = []
    state: dict = {"pages": {}, "updated_at": now.isoformat()}

    for t in targets:
        prev = prev_pages.get(t.url)
        res = fetch(t.url)
        ok = res.status is not None and 200 <= res.status < 400 and bool(res.body)
        title = sha = None
        docs: list[dict] = []
        interstitial = False
        if ok:
            html = res.body.decode("utf-8", errors="replace")
            interstitial = is_interstitial(html)
            ok = not interstitial
        if ok:
            title, sha, docs = parse_page(html, res.final_url or t.url)

        new_docs: list[dict] = []
        changed = False
        if ok and prev is not None:
            known = set(_known_ids(prev))
            new_docs = [d for d in docs if link_id(d["url"]) not in known][:MAX_NEW_PER_PAGE]
            changed = prev.get("sha") is not None and prev.get("sha") != sha

        reports.append(PageReport(
            url=t.url, source_name=t.source_name, institution=t.institution, purpose=t.purpose,
            checked_at=now.isoformat(), reachable=ok, http_status=res.status, final_url=res.final_url,
            title=title, text_sha256=sha, document_count=len(docs), changed=changed,
            new_documents=new_docs,
            error=res.error or (None if ok else (
                "Interstitial or anti-bot page instead of content" if interstitial
                else "Empty response body" if res.status and res.status < 400
                else f"HTTP {res.status}"
            )),
        ))

        if ok:
            current = [link_id(d["url"]) for d in docs]
            seen_now = set(current)
            # Keep links that disappeared too, so a link that comes back is not reported as new.
            ids = current + [i for i in _known_ids(prev) if i not in seen_now]
            state["pages"][t.url] = {"sha": sha, "title": title, "link_ids": ids[:MAX_LINKS_KEPT], "last_ok": now.isoformat()}
        elif prev is not None:
            # Keep the last good state so a transient failure does not reset the baseline.
            state["pages"][t.url] = prev

    state["baseline"] = baseline
    return reports, state


def summarize(reports: list[PageReport], baseline: bool) -> dict:
    return {
        "pages_checked": len(reports),
        "reachable": sum(r.reachable for r in reports),
        "failing": sum(not r.reachable for r in reports),
        "changed": sum(r.changed for r in reports),
        "new_documents": sum(len(r.new_documents) for r in reports),
        "documents_listed": sum(r.document_count for r in reports),
        "baseline": baseline,
    }


def to_json(reports: list[PageReport]) -> list[dict]:
    return [asdict(r) for r in reports]
