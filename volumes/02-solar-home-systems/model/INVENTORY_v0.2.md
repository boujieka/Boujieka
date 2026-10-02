# SHS model v0.2: pre-migration inventory

Source: `volumes/02-solar-home-systems/model/AEF_SHS_PAYGo_Model_v0.2.xlsx` (backup in `model/archive/`, git tag `shs-model-v0.2`).

| Sheet | Formulas | Hard-coded numeric inputs (blue) | Sheets referenced | Charts | Data validations |
|---|---|---|---|---|---|
| Cover | 1 | 0 | Checks | 0 | 0 |
| Investment_Summary | 120 | 0 | Checks, Financing, Inputs, KPIs, Scenarios, Sensitivity, Unit_Economics, Valuation | 0 | 0 |
| Inputs | 1 | 45 |  | 0 | 1 |
| Products | 65 | 95 | Inputs, Products, Scenarios | 0 | 0 |
| Scenarios | 6 | 15 | Inputs | 0 | 0 |
| Dashboard | 2 | 0 | Checks, Scenarios | 4 | 0 |
| KPIs | 195 | 0 | Covenants, FS, Financing, Inputs, Ops, Timeline | 0 | 0 |
| Valuation | 72 | 0 | Costs, FS, Inputs, Timeline | 0 | 0 |
| Covenants | 790 | 0 | FS, Financing, Inputs, Ops, Timeline | 0 | 0 |
| Unit_Economics | 100 | 0 | Curves, Inputs, Products | 0 | 0 |
| Sensitivity | 0 | 0 |  | 1 | 0 |
| Annual | 240 | 0 | FS, Timeline | 0 | 0 |
| FS | 3,411 | 0 | Costs, Financing, Inputs, Ops, Timeline | 0 | 0 |
| Ops | 8,844 | 0 | Cohort_T1, Cohort_T2, Cohort_T3, Cohort_T4, Cohort_T5, Curves, Inputs, Products, Scenarios, Timeline | 0 | 0 |
| Costs | 1,217 | 0 | Inputs, Ops, Timeline | 0 | 0 |
| Financing | 1,156 | 0 | FS, Inputs, Ops, Timeline | 0 | 0 |
| Curves | 3,380 | 0 | Curves, Inputs, Products | 0 | 0 |
| Cohort_T1 | 7,740 | 0 | Curves, Ops, Timeline | 0 | 0 |
| Cohort_T2 | 7,740 | 0 | Curves, Ops, Timeline | 0 | 0 |
| Cohort_T3 | 7,740 | 0 | Curves, Ops, Timeline | 0 | 0 |
| Cohort_T4 | 7,740 | 0 | Curves, Ops, Timeline | 0 | 0 |
| Cohort_T5 | 7,740 | 0 | Curves, Ops, Timeline | 0 | 0 |
| Timeline | 362 | 0 | Inputs, Scenarios | 0 | 0 |
| Glossary | 0 | 0 |  | 0 | 0 |
| Checks | 13 | 0 | FS, Financing, Inputs, Products | 0 | 0 |

Total formulas: 58,675. Defined names: 0 (the generator uses row-key registration instead of named ranges).
Excel errors: none (0 errors in the formulas-engine evaluation of Base and Severe, 2026-10-02).
Circularity: none by design (interest on opening balances; cash sweep uses cash before facility).
Hard-coded inputs live only on Inputs, Products and Scenarios (blue font). Every other number is a formula.
