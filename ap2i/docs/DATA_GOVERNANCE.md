# AP²I — Data governance

## 1. Kinds of information (always labelled separately)
| Label (`data_nature`) | Meaning | Example |
|---|---|---|
| `officially_reported` | Published by the source; stored as published; not independently checked | World Bank `totalamt` |
| `verified` | Checked by an AP²I Data Reviewer against the source document (`verification_status=verified`) | Reviewer-approved record |
| `calculated` | Derived by AP²I with a published formula | Disbursement rate, USD equivalent |
| `estimated` | An estimate with its method stated (reserved; none produced automatically) | — |
| `ai_generated` | Text produced by an AI model; never a fact | Assistant narrative |
| `missing` | Explicitly not available; never replaced by zero | Operational status unknown |
| `synthetic` | Test fixtures only; refused in production (DB CHECK + pipeline guard) | `tests/fixtures/*` |

## 2. Provenance
Every source record is stored verbatim (JSON or original IATI XML) with SHA-256, source URL, the source's own
update date and the retrieval time. Every value written to a master project is also written as a
`source_observation` (field, source field, value, currency, reporting date, extraction date). Financial
transactions keep their source transaction key; agreements keep the source field their amount comes from
(`amount_label`, `reported_cumulative_label`).

## 3. Mapping rules (documented, deterministic)
* **Sectors**: World Bank first listed major sector name → AP²I sector; IATI DAC purpose codes (5-digit
  refinements, else 3-digit category; highest percentage wins) → AP²I sector (table in
  `app/reference/catalog.py`). Unmapped → no sector + validation note; the source label is always kept.
* **Statuses**: World Bank Active/Closed/Dropped/Pipeline; IATI 1–6 → pipeline/active/completed/closed/
  cancelled/suspended. Original wording kept as an observation.
* **Instruments**: World Bank lending instrument; IATI finance type (110 grant, 4xx loans, 5xx equity, 1100
  guarantee).
* **Additional Financing**: an official parent link (World Bank `parentprojid`, IATI `related-activity type=1`)
  makes the record a financing agreement of the parent master project.
* **Zero amounts**: a published `0` on a dropped/pipeline World Bank operation means "no commitment" and is
  stored as `NULL` with a note; elsewhere a published zero is kept.

## 4. Counting rules (no double counting)
* One master project per underlying project; financings from several partners are agreements of that project.
* Two sources reporting the same commitment: one is counted (`is_counted=true`), the other is kept with a
  `counting_note`. Precedence: uploaded official document > IATI transactions > API aggregate.
* Multi-country IATI activities: only transactions that name the country are attributed; no pro-rating.
* Annual portfolios count a project once per category and year; flows by transaction value date.
* Cumulative "disbursed to date" figures are never spread across years.

## 5. Currency and conversion
Original currency always kept. USD equivalents use the annual average rate of the transaction year (WDI
PA.NUS.FCRF; IMF ER for SDR). Missing rate → no conversion and an explicit "incomplete" flag. Constant-price
values are not produced (no deflator series has been integrated).

## 6. Entity resolution and review
Deterministic matches are applied automatically and recorded (`project_source_links.match_rule`).
Probabilistic matches (title similarity with bilingual normalisation, date proximity, sector, agency) are only
**candidates** for a Data Reviewer. Accepted merges are recorded with everything they moved and can be
reversed by an authorised reviewer.

## 7. Corrections
Source records are never edited: a changed source creates a new version. Reviewer corrections are new
observations that point to the observation they supersede. Annual snapshots are superseded, not overwritten.

## 8. Alerts and AI
Alerts are signals for verification and say so; they never assert fraud or corruption. The assistant answers
from database records only; optional AI narration must pass a numeric grounding check, and imported text is
fenced as untrusted data. Project Rescue never states causes that are not documented: it writes
"Further investigation required."

## 9. Coverage statement (shown in the product)
AP²I coverage is limited to the connected sources and uploaded official documents. It is not the complete
public investment portfolio of any country. Countries without imported records show "no data", never zeros.

## 10. Roles in the data lifecycle
Data Contributor (uploads; private until reviewed) → Data Reviewer (verifies records, resolves validation
issues, decides match candidates, reverses merges, reviews alerts) → AP²I Super Administrator (connectors,
schedules, thresholds, users). Every decision is written to `audit_logs`.
