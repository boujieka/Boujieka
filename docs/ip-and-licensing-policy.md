# IP & licensing policy

## What we can do

1. **Benchmark** any public or purchased tool: list its features, structure and gaps, and record this in `benchmarks/*.md`.
2. **Build our own models from scratch** (clean-room), implementing standard finance mechanics. DSCR, cohort analysis, waterfalls and similar mechanics are general knowledge.
3. **Interoperate.** Provide import tabs that accept outputs from free tools (HOMER, PVGIS, the AFUR tariff tool, the CCA unit-economics toolkit) and explain how to use them alongside ours.
4. **Cite public data** with attribution, under the licence of each document. World Bank works are often CC BY 3.0 IGO, which allows commercial reuse with attribution. Confirm this on each document.
5. **Use standard KPI definitions**, such as PAYGo PERFORM, with citation.

## What we must not do

1. Resell, repackage or modify a third-party model, paid or free, unless its licence explicitly allows commercial derivative works.
2. Copy formulas, sheet layouts, text or charts from purchased templates.
3. Commit third-party files to any public repository. This repository is private, and `benchmarks/` stays private.
4. Use confidential client data, even anonymised, where it is covered by an NDA or engagement letter.

## Before release (per volume)

- [ ] Every default value is either labelled illustrative or listed as Verified in `sources/source-register.md`
- [ ] No third-party content was copied (author's self-check)
- [ ] Disclaimer present on the Cover and in the manual
- [ ] Case study is fictional, or the data owner has consented in writing
