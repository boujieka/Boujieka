# Test fixtures — SYNTHETIC

Every file in this folder is **synthetic test data** built to exercise parsers and rules. Titles start
with "SYNTHETIC", identifiers use reserved test prefixes (`P9xxxxx`, `TEST-`), and amounts are invented.
They are used only by the automated tests (served through `httpx.MockTransport`) and are never loaded
into a production database. The structure mirrors the real World Bank Projects API JSON and IATI 2.03 XML.
