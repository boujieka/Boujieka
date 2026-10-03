### Why we attacked our own model

A model that supports a policy argument should be tested by someone who wants it to fail. Before publication we commissioned an adversarial review of the companion workbook, written from the position of a development-bank model auditor and an examiner in energy economics. The reviewer re-ran the model on separate copies, traced formulas cell by cell and reported thirty findings: three critical, ten high, ten medium and seven low. The workbook passed every one of its own integrity checks while several of these defects were present. That alone justified the exercise.

This chapter reports what the review found, what we changed, and what we did not change. All results elsewhere in this book come from the corrected model.

### Critical findings

**An uncapped guarantee.** The first version let a sovereign PPA payment guarantee pay every dollar of the utility's shortfall, every year, for thirty years. Under the offtaker stress the state ended up paying about 98 percent of all the utility's PPA bills, and the scenario "no budget backstop, guarantee called" produced exactly the same numbers as the scenario with a backstop. Real payment guarantees are capped, usually at a number of months of billing, and are reimbursed when the utility recovers. The corrected model limits calls to the available guarantee amount, tracks calls outstanding and credits the utility's reimbursements back to the Treasury. A shortfall beyond the cap now becomes arrears to the project. The consequence is stark: without a budget backstop, the offtaker stress drives the IPP into default, with a minimum DSCR of {{offtaker_nobs.kpi_min_dscr|x2}}.

**Supply that did not exist.** The utility model billed the whole of national demand and bought whatever it needed from "other supply" at a fixed cost, with no volume limit, even though the demand sheet showed that committed supply covered only part of that demand. By the end of the horizon the utility was buying several times more energy than existed. This flattered its payment capacity. The corrected model caps other supply at the amount available, so demand above it goes unserved, and treats the mining load served directly by the project as outside the utility's sales.

**A fiscal perimeter that stopped at the Treasury.** The first fiscal NPV counted only central-government cash. Losses that the state-owned utility absorbed, such as deemed-energy payments for power it could not receive or the extra cost of a PPA priced above its retail realisation, were invisible unless they surfaced as a payment gap. This is why a transmission delay appeared to improve public finances. The corrected model adds a no-project counterfactual for the utility and reports a consolidated fiscal NPV for government and utility together. The difference is material. In the base case, central-government fiscal NPV is about USD {{base_sized.fis_npv|n0}} million while the consolidated figure is about USD {{base_sized.fis_npv_cons|n0}} million, because each megawatt-hour the utility buys from Lumora costs it more than it collects when it resells it.

### High-severity findings

The review found that the debt service reserve was never drawn. Shortfalls went straight to guarantors and sponsors while the reserve sat idle, and reserve top-ups were themselves paid out of guarantee calls. The corrected waterfall draws the reserve first, releases only the excess over target, and tops up only from available cash.

"Locked" debt was not locked. In stress runs the first version switched the commercial loan from a sculpted to an annuity profile and let the concessional loan, grants and government equity grow with cost. Stress results therefore mixed the effect of the stress with the effect of refinancing. The corrected model locks every tranche amount and the commercial principal schedule at their base-case values, lets interest float only on the unhedged share, and lets equity absorb the difference, which is what a sponsor faces after financial close.

The low-demand stress did not propagate, because the base-year demand used to scale system peak and utility costs was itself scaled by the stress. A transmission delay was modelled as a rescheduled line, which made it cheaper in present-value terms; it is now a late line with a cost penalty, built to the original plan. Project-funded transmission spent after commercial operation dropped out of the funding and cash-flow accounts; it now reduces cash flow available for debt service, and a new check reconciles it.

The original financing gap was largely an artefact. Interest during construction, fees and the reserve were funded by equity while the gearing limit applied only to capital cost, so effective gearing on total uses was about 65 percent rather than 75. The corrected model funds IDC and fees with debt through a closed-form factor that avoids circularity, and the gap in the base case disappears.

Gate metrics could be text or blank. A failed internal rate of return calculation scored as ready, and a utility with no exposure scored as a critical gap. Both are fixed with explicit fallbacks.

The closed-form structure comparison omitted IDC and tax and so understated the tariff an IPP needs. The corrected screen grosses equity returns up for tax and includes IDC, and the book now reports tariffs solved by the full engine alongside it. The reviewer also pointed out that the result "gross public exposure barely changes across structures" holds by construction, because every dollar of capital is either public or protected by a termination payment. We kept the result but now present it as an identity, which is how it should be read.

Contingent exposures mixed stocks and flows, and the termination amount collapsed to the outstanding debt once equity had been repaid. The corrected model treats foreign exchange cover inside the maximum, values equity at termination as the larger of unrecovered equity with a premium and the present value of remaining distributions, and lets the state recover debt-guarantee calls from later project cash ahead of dividends.

Finally, the stress magnitudes did not match the model's own evidence base. The source database recommends the reference-class median for an expected outcome and the mean for a stress, but the model used the median as its stress. We kept the median as the default overrun stress and added a run at the reference-class mean of 96 percent. We also deepened the drought stress to 55 percent of normal flow, in line with the cut in Kariba's 2024 water allocation.

### Medium and low findings

We fixed several smaller items. The LLCR now covers every tranche over the longest loan life at the weighted interest rate. One regulatory item at critical gap now makes Gate 6 critical. Gate 8 now tests on-budget debt and the consolidated fiscal NPV. Tax losses are no longer consumed during the tax holiday. Royalties are charged only on energy delivered. The on-budget screening measure adds components in the same year rather than adding peaks from different years. Three new integrity checks cover the debt balloon, the reserve balance and project-funded transmission.

### What we did not change

Some limitations remain, and readers should weigh the results with them in mind.

- The lender case still applies a one-year P90 to every year. A ten-year P90 would be closer to P50, so the lender case is conservative on average and silent on runs of dry years. Debt sizing is set by the gearing cap rather than by coverage in most structures, so this matters less than it might.
- Annual periodicity and proportional curtailment remain. A plant with storage would do better than the model suggests when the line is constrained.
- The currency step is permanent in real terms, with no pass-through to local prices. This is severe but not unprecedented.
- Debt is drawn in proportion to spending rather than after equity, which slightly flatters the equity return.
- The utility model has no balance sheet and does not revalue receivables for currency moves.
- Call probabilities for expected loss remain user judgements.
- Only one project is assessed. The portfolio question raised in Chapter 19 is not modelled.

The review also flagged claims in the earlier draft that the model did not support, including figures for debt capacity, the LLCR and the effect of a transmission delay on public finances. Those passages have been rewritten, and every figure in this edition is generated from the corrected model.
