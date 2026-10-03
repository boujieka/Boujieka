"""Source watch tests. No network: pages are served by a fake fetcher."""

from datetime import date, datetime, timezone

from app.watch.daily import build_veille, targets_from_sources
from app.watch.sources import FetchResult, Target, check, parse_page, summarize

NOW = datetime(2026, 10, 4, 5, 0, tzinfo=timezone.utc)
URL = "https://cb.example/results/"
T = [Target(url=URL, source_name="CB results", institution="Central Bank", purpose="Results")]


def page(*docs: str, extra: str = "") -> bytes:
    links = "".join(f'<li><a href="{d}">Result {i}</a></li>' for i, d in enumerate(docs))
    return (
        "<html><head><title> Treasury  Bills | CB </title><script>var t = Date.now();</script>"
        f"</head><body><h1>Results</h1><ul>{links}</ul>{extra}"
        '<a href="/about">About</a><a href="mailto:x@cb.example">Mail</a></body></html>'
    ).encode()


def fake(pages: dict[str, FetchResult]):
    return lambda url: pages[url]


def ok(body: bytes) -> FetchResult:
    return FetchResult(200, URL, body, None)


class TestParsePage:
    def test_title_and_document_links(self):
        title, sha, docs = parse_page(page("/u/a.pdf", "b.PDF?v=2", "/u/c.xlsx", "/not-a-doc").decode(), URL)
        assert title == "Treasury Bills | CB"
        assert [d["url"] for d in docs] == [
            "https://cb.example/u/a.pdf",
            "https://cb.example/results/b.PDF?v=2",
            "https://cb.example/u/c.xlsx",
        ]
        assert docs[0]["text"] == "Result 0"
        assert len(sha) == 64

    def test_script_content_does_not_change_hash(self):
        a = parse_page(page("/a.pdf").decode(), URL)[1]
        b = parse_page(page("/a.pdf").decode().replace("Date.now()", "12345"), URL)[1]
        assert a == b

    def test_duplicate_links_collapsed(self):
        _, _, docs = parse_page(page("/a.pdf", "/a.pdf").decode(), URL)
        assert len(docs) == 1


class TestCheck:
    def test_first_run_is_a_baseline(self):
        reports, state = check(T, None, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        assert state["baseline"] is True
        assert reports[0].reachable and reports[0].new_documents == [] and not reports[0].changed
        from app.watch.sources import link_id

        assert state["pages"][URL]["link_ids"] == [link_id("https://cb.example/a.pdf")]

    def test_new_document_detected_on_next_run(self):
        _, s1 = check(T, None, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        reports, s2 = check(T, s1, fake({URL: ok(page("/a.pdf", "/b.pdf"))}), now=NOW)
        assert [d["url"] for d in reports[0].new_documents] == ["https://cb.example/b.pdf"]
        assert reports[0].changed is True
        assert s2["baseline"] is False

    def test_same_page_twice_reports_nothing_new(self):
        _, s1 = check(T, None, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        reports, _ = check(T, s1, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        assert reports[0].new_documents == [] and reports[0].changed is False

    def test_removed_then_restored_link_is_not_new(self):
        _, s1 = check(T, None, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        _, s2 = check(T, s1, fake({URL: ok(page())}), now=NOW)
        reports, _ = check(T, s2, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        assert reports[0].new_documents == []

    def test_failure_keeps_previous_state(self):
        _, s1 = check(T, None, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        reports, s2 = check(T, s1, fake({URL: FetchResult(None, None, b"", "ConnectError: boom")}), now=NOW)
        assert reports[0].reachable is False and "ConnectError" in reports[0].error
        assert s2["pages"][URL] == s1["pages"][URL]
        reports, _ = check(T, s2, fake({URL: ok(page("/a.pdf", "/b.pdf"))}), now=NOW)
        assert [d["url"] for d in reports[0].new_documents] == ["https://cb.example/b.pdf"]

    def test_large_page_has_no_false_new_documents(self):
        """Regression: pages with ~1,000 document links (BEAC, CBK) must not re-report old links."""
        many = [f"/docs/{i}.pdf" for i in range(1200)]
        _, s1 = check(T, None, fake({URL: ok(page(*many))}), now=NOW)
        reports, _ = check(T, s1, fake({URL: ok(page(*many))}), now=NOW)
        assert reports[0].document_count == 1200 and reports[0].new_documents == []

    def test_legacy_state_with_full_urls_is_understood(self):
        legacy = {"pages": {URL: {"sha": "x", "links": ["https://cb.example/a.pdf"]}}}
        reports, state = check(T, legacy, fake({URL: ok(page("/a.pdf", "/b.pdf"))}), now=NOW)
        assert [d["url"] for d in reports[0].new_documents] == ["https://cb.example/b.pdf"]
        assert "link_ids" in state["pages"][URL]

    def test_empty_body_is_reported_clearly(self):
        reports, _ = check(T, None, fake({URL: FetchResult(200, URL, b"", None)}), now=NOW)
        assert reports[0].reachable is False and reports[0].error == "Empty response body"

    def test_http_error_is_unreachable(self):
        reports, _ = check(T, None, fake({URL: FetchResult(403, URL, b"denied", None)}), now=NOW)
        assert reports[0].reachable is False and reports[0].error == "HTTP 403"

    def test_summary(self):
        reports, state = check(T, None, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        assert summarize(reports, state["baseline"]) == {
            "pages_checked": 1, "reachable": 1, "failing": 0, "changed": 0,
            "new_documents": 0, "documents_listed": 1, "baseline": True,
        }


class TestVeille:
    def test_history_and_feed(self):
        _, s1 = check(T, None, fake({URL: ok(page("/a.pdf"))}), now=NOW)
        r2, s2 = check(T, s1, fake({URL: ok(page("/a.pdf", "/b.pdf"))}), now=NOW)
        v1 = build_veille(date(2026, 10, 4), None, [], s1, NOW)
        v2 = build_veille(date(2026, 10, 5), v1, r2, s2, NOW)
        assert [h["as_of"] for h in v2["history"]] == ["2026-10-04", "2026-10-05"]
        assert v2["feed"][0]["url"] == "https://cb.example/b.pdf"
        assert v2["feed"][0]["institution"] == "Central Bank"
        # A same-day rerun replaces that day's history entry instead of duplicating it.
        v3 = build_veille(date(2026, 10, 5), v2, r2, s2, NOW)
        assert [h["as_of"] for h in v3["history"]] == ["2026-10-04", "2026-10-05"]
        assert len(v3["feed"]) == 1

    def test_targets_from_registered_sources(self, db):
        from sqlalchemy import select

        from app.models import Source

        targets = targets_from_sources(list(db.scalars(select(Source))))
        urls = [t.url for t in targets]
        assert len(urls) == len(set(urls)) == 31
        assert all(u.startswith("https://") for u in urls)
