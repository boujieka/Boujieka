"""ARVI — Africa Resource Value Intelligence (pilot).

Compares what African countries declare as natural-resource exports with what their trading
partners declare as imports from them (UN Comtrade "mirror" statistics), then computes the
indicators that need no modelled parameter: ARVI-1 (trade gap), ARVI-2 (unit-value gap versus
the mirror) and ARVI-3 (export structure along the processing chain), each with a rule-based
confidence score.

ARVI-4 (fiscal), ARVI-5 (local value addition) and ARVI-6 (investment equivalents) need sourced
fiscal, cost and price parameters that are not collected yet; they are reported as not published.

See docs/arvi/ARVI_MASTER_BLUEPRINT_v1.0.md.
"""
