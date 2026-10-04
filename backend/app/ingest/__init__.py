"""Phase 2: verified ingestion of official documents.

Pipeline: fetch (official listing → document bytes → SourceDocument, deduplicated by SHA-256)
→ extract (deterministic text parsing, every value with a locator and a confidence)
→ staging (`auction_extraction`, UNVERIFIED) → human review (`python -m app.ingest.review`)
→ promotion of approved rows to `security` / `auction` as VERIFIED facts.

Nothing in this package calls an LLM. A value that cannot be read from the document is left
empty with a FieldStatus; it is never inferred.
"""
