# AP²I — Known limitations (2026-10-22)

## Data coverage
* Only donor-reported financing for Cameroon is loaded (World Bank, AfDB, AFD, EIB, EU INTPA, IFAD). No
  national budget (government-funded) data: no machine-readable Cameroon source was found; the import workflow
  exists but nothing has been imported. **AP²I does not show the complete public investment portfolio.**
* No other African country has project data yet (geographical reference only).
* Physical progress, operational status, contracts, contract amendments and beneficiaries are not published by
  the connected sources: these fields are empty for imported projects (they can be filled through the upload
  workflow from official reports). Alerts that need them do not fire.
* World Bank supervision reports: results-table values of the post-2024 ISR layout are not in the text
  rendition and are not extracted (PDF table extraction not implemented). Ratings, dates, narrative and the
  disbursement table are extracted. ISRs before 2011 are catalogued but not parsed (configurable).
* Physical progress comes only from reviewer-validated candidates (narrative percentages) or uploaded official
  documents; it is empty until a reviewer acts.
* World Bank disbursements are cumulative to date (US$ millions, 2 decimals); they are not split by year.
  Annual disbursements for World Bank projects come only from the 46 activities in the World Bank IATI file.
* AfDB amounts are in SDR (XDR); USD equivalents depend on IMF annual averages; 2026 rates (EUR, XDR) are not
  yet published, so 2026 USD totals are flagged incomplete.
* Sector mapping uses the first major sector published by the World Bank, which is not always the largest
  share; DAC codes for IATI. Some projects (≈5 %) have no mappable sector.
* Results indicators are imported from IATI where published but are not yet linked to the configurable sector
  indicators (linking requires review).
* IATI data was retrieved via the Code for IATI mirror; the official IATI Datastore path needs a subscription
  key and is untested.
* Direct AfDB portal and AFD open-data API were unreachable from the build environment (blocked).
* AfDB documents on www.afdb.org (incl. EER/IPR supervision reports) are behind an anti-bot challenge that AP²I
  does not circumvent: 988 of 1,030 AfDB document links are catalogued only. Only the 31 PDFs on evrd.afdb.org are
  parsed automatically; other AfDB reports must be attached manually (PDF upload). There is no EER/IPR parser.
* Tier-2/3 donors without IATI publication for Cameroon (IsDB, KfW, JICA, GEF, GCF, BADEA, SFD, Kuwait Fund,
  ADFD) have no automated connector.

## Product
* Document processing: World Bank ISR/ICR texts are downloaded and parsed (plain-text renditions). AfDB
  completion reports and IDEV review notes from evrd.afdb.org are parsed (PDF text layer); uploaded PDFs are stored
  as text. AFD documents are stored as links only. RAG/semantic search over
  documents is not implemented; the assistant uses structured database retrieval only.
* The assistant understands a fixed set of question types (list, low disbursement, compare commitments,
  completed-not-operational, annual commitments, recovery plan). Other questions fall back to a project list.
* No LLM is configured by default; the optional narrative has only been tested with stub providers.
* Constant-price values are not produced (no deflator series integrated).
* Payment processing is intentionally inactive; plan prices are "on request".
* Email is logged to the console unless SMTP is configured.
* S3-compatible storage is configured by variables but the code writes reports to the local document store.
* Rate limiting is in-process (per API instance).
* Probabilistic matching uses simple token similarity; it found 3 cross-donor candidates in the Cameroon data,
  none reviewed yet.

## Engineering
* `docker compose up` was not run end-to-end in the build environment because Docker Hub rate-limited image
  pulls (HTTP 429); the API, Celery worker and beat images were built (via a registry mirror) and run against
  PostGIS and Redis containers, including real syncs and scheduled dispatch. The frontend image build is
  reported separately.
* No external penetration test; no production TLS/reverse-proxy configuration; backups are documented, not
  automated (see SECURITY.md).
* GitHub Actions workflow is written but has not run on GitHub yet.
* Country reference data (names, regions, languages) is compiled and unverified except ISO codes, which are
  cross-checked live against the World Bank API.
