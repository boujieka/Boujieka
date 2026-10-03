# Africa Energy Finance — Business & Financial Models

*From business model to bankability.* A collection of professional financial models, manuals, case studies and investment tools for energy businesses in African markets.

> **Private repository.** It contains work-in-progress products and third-party benchmark files that must not be redistributed (see `benchmarks/README.md`).

## Collection

| # | Volume | Central question | Status |
|---|--------|------------------|--------|
| 2 | **Solar Home Systems (PAYGo)**: Book 2, *PAYGo Solar Finance* | Can PAYGo solar become profitable and financeable? | **Book first edition v0.2 (pre-publication); model v0.8 in development** |
| 3 | Clean Cooking | Can clean cooking scale as a commercial business? | Planned |
| 1 | Mini-Grids | Can this mini-grid become a sustainable business? | Planned |
| 4 | C&I Solar + BESS | Should the customer invest, sign a PPA or use an ESCO? | Planned |
| 5 | Energy Access Fund | Can a fund mobilise capital and generate sustainable returns? | Planned |
| 6 | Power Utilities | Can the utility become financially sustainable? | Planned |

Volume numbers follow the editorial plan. Production order follows market gaps (SHS first, English first).

## Repository layout

```
engine/          Shared engine specification (mechanics reused by every model)
tools/           Python generators that build every Excel model (reproducible, diff-able)
volumes/NN-*/    model/ manual/ book/ case-study/ templates/ per volume
master-library/  Templates shared across volumes (IC memo, due diligence, risk matrix ...)
benchmarks/      Third-party tools for analysis only (never redistributed)
sources/         Source and licence register
docs/            Conventions, production plan
```

## Building a model

```bash
pip install openpyxl
python tools/build_shs_model.py      # -> volumes/02-solar-home-systems/model/*.xlsx
```

The `.xlsx` is generated. Edit the generator, not the workbook, so that every change is reviewed in git.

## Ground rules

1. **No copying of third-party models.** We benchmark existing tools, then build our own from scratch. See `docs/ip-and-licensing-policy.md`.
2. **Every number has a source or is labelled illustrative.** See `sources/source-register.md`.
3. **Every model passes its integrity checks** (master check = OK) before release.
