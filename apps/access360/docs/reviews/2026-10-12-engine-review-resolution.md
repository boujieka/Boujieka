# Resolution of the engine review of 12 October 2026

The review is in `2026-10-12-engine-review.md`. It was an independent AI review, not a human expert review. Status after the fixes: 77 backend tests pass.

| Finding | Severity | Resolution | Regression test |
|---|---|---|---|
| F01 Tax on tariff support in pre-subsidy flows | Critical | Fixed: separate unlevered taxes before and after subsidy | test_f01_pre_subsidy_metrics_do_not_depend_on_tariff_support |
| F02 Solver false "infeasible" | Critical | Fixed: zero first, grid scan, bisection, monotonicity flag; non-computable IRR with no equity input passes | test_f02_solver_finds_zero_and_interior_answers_with_irr_targets |
| F03 Short-life items never replaced | Major | Fixed: per-item replacement rule; storage life tied to battery life | test_f03_short_life_items_are_replaced_and_depreciated_over_their_life |
| F04 Construction tax missing from S&U | Major | Fixed in S&U; taxing of unrealised FX listed as L24 | test_f04_construction_tax_is_in_sources_and_uses |
| F05 Milestones dropped silently | Major | Fixed: inputs validated against the horizon; undisbursed grant reported with warning W_GRANT | test_f05_and_f14_invalid_timings_are_rejected, test_f05_grant_lost_to_closure_is_reported |
| F06 Checks blind to consistent formula errors | Major | Fixed: 12 kinds of independent recomputation check (`R_` codes); mutation test with 13 planted errors, all caught | tests/engine/test_mutations.py |
| F07 Closure-year DSCR of 0 | Major | Fixed: whole balance prepaid at closure, closure quarter excluded from scheduled debt service; closure cover reported (W_CLOSE) | test_f07_closure_quarter_is_not_scheduled_debt_service |
| F08 SHS recommended while leaving demand unserved | Major | Fixed: options above the unserved share limit fail their gate | test_partial_service_options_are_gated |
| F09 Affordability tariff mis-specified | Major | Fixed: revenue by class tariff on served energy; affordability caps the household tariff only | test_revenue_uses_class_tariffs_and_affordability_cap |
| F10 DSRA never drawn | Minor | Documented as L21 | |
| F11 Minimum cash first funded at COD | Minor | Fixed: funded before COD | test_f11_minimum_cash_is_funded_before_cod |
| F12 Deferred grant not released at residual disposal | Minor | Fixed | test_f12_residual_disposal_releases_the_deferred_grant |
| F13 Unlevered tax omits disposal gain and taxable grant | Minor | Fixed with F01 | covered by R_PCF check |
| F14 Tenor and grace not validated | Minor | Fixed | test_f05_and_f14_invalid_timings_are_rejected |
| F15 Battery life under 0.125 years | Minor | Fixed (minimum 0.25 years) | same |
| F16 Optimizer crash on zero cost | Minor | Fixed: missing values score worst | test_zero_cost_option_does_not_crash |
| F17 D and F asymmetric | Minor | Fixed: daytime anchor credit applied to every mini grid option; F documented as L26 | test_anchor_option_needs_an_anchor_and_costs_like_d |
| F18 Grid options serve all demand | Design | Documented as L25 | |
| F19 Compensation base includes finance costs | Design | Documented as L22 and in the specification | |
| F20 No salvage on late replacement | Design | Documented as L23 | |
| F21 MRR and LLCR definitions | Design | Definitions stated in the specification | |
