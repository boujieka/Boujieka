# Project risk register (product and delivery)

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | A financial calculation error reaches an investment document | Medium | High | Deterministic engine, 16 kinds of integrity check plus fault injection, status rules (never VALIDATED without a named review), run stamps on every document, independent review before commercial launch | Engine lead |
| R2 | Synthetic demo data mistaken for real data | Medium | High | `is_demo` flags on organisations, projects, runs and datasets; badges in every view; demo and real never aggregated; demo points placed at sea | Product |
| R3 | Cross-tenant data leak | Low | Very high | API membership checks plus PostgreSQL RLS (forced), tests at both layers, non-owner app role | Security |
| R4 | Third-party geospatial data used without a licence | Medium | High | Mandatory licence and source fields; nothing bundled until licences are cleared | Data |
| R5 | Users read the optimizer as a least-cost plan | Medium | Medium | Method note on every result; technical gates; infeasible options never ranked | Product |
| R6 | Regulatory treatment (grid arrival, tariffs) applied without a source | Medium | High | Missing citation keeps the model at INCOMPLETE INPUTS | Engine lead |
| R7 | Marketplace read as a regulated offering | Low (not built) | High | Information and introduction service only; legal review before Phase 3 | Legal |
| R8 | Implied endorsement by governments or DFIs | Low | High | No partner names or logos; independent company statement | Management |
| R9 | AI Copilot invents figures | n/a (not built) | High | Phase 4 design: retrieval only from approved data, schema-validated outputs, citations, human review, no write access without approval | AI lead |
| R10 | Payment and subscription compliance | n/a (not built) | Medium | Provider chosen only after the jurisdiction and eligibility checks | Finance |
| R11 | Key-person dependency on the engine | Medium | Medium | Specification document, tests, readable code | Management |
| R12 | Scaling limits (synchronous runs, local storage, in-memory rate limit) | Low now | Medium | Documented in ADR 0001; Redis, workers and object storage planned | DevOps |
