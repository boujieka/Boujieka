"""Resolution of the four loops the workbook breaks with pasted values.

``excel_macros`` (default, faithful): replays the audited VBA macros
Module1.Debt_Sizing, Module2.Refi_Debt_Sizing and Module7.DSRA_resize_3 in
the order the workbook prescribes, starting from the pasted values stored in
the assumptions. Results match Excel, including the macros' one-sided
tolerance of ROUND(x, -5) (audit section 4).

``exact`` (improvement, flagged): solves the same fixed point to a tight
tolerance. Results differ from Excel by up to the macros' tolerance.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .assumptions import Assumptions
from .model import Ledger, run_model
from .options import FAITHFUL, EngineOptions
from .prepare import prepare

MAX_LOOP = 500
MAX_ROUNDS = 25


class SolverError(RuntimeError):
    pass


@dataclass
class SolveLog:
    method: str
    converged: bool = False
    rounds: int = 0
    runs: int = 0
    steps: list = field(default_factory=list)


def evaluate(a: Assumptions, options: EngineOptions = FAITHFUL) -> Ledger:
    return run_model(a, prepare(a, options), options)


def _sizing_ok(L: Ledger) -> bool:
    S = L.s
    return all(S[k] == 0 for k in ("Inputs!N292", "Inputs!N300", "Inputs!N344", "Inputs!E373"))


def solve_excel_macros(a: Assumptions, options: EngineOptions = FAITHFUL) -> tuple[Assumptions, Ledger, SolveLog]:
    a = a.replace()
    log = SolveLog("excel_macros")
    L = evaluate(a, options); log.runs += 1
    for rnd in range(1, MAX_ROUNDS + 1):
        if _sizing_ok(L):
            log.converged, log.rounds = True, rnd - 1
            return a, L, log
        # Debt_Sizing: Do Until DSCR_Delta = 0 And Funding_Delta = 0
        n = 0
        while not (L.s["Inputs!J300"] == 0 and L.s["Inputs!J292"] == 0):
            if n >= MAX_LOOP:
                raise SolverError("Debt_Sizing did not converge (the VBA loop would run forever)")
            a.pasted.dscr_limit = L.s["Inputs!I300"]       # DSCR_Copy -> DSCR_Paste
            L = evaluate(a, options); log.runs += 1
            a.pasted.funding = L.s["Inputs!I292"]          # Funding_Copy -> Funding_Paste
            L = evaluate(a, options); log.runs += 1
            n += 1
        log.steps.append({"macro": "Debt_Sizing", "iterations": n})
        if a.refi.on == 1:
            n = 0
            while L.s["Inputs!J344"] != 0:
                if n >= MAX_LOOP:
                    raise SolverError("Refi_Debt_Sizing did not converge")
                a.pasted.refi_limit = L.s["Inputs!I344"]
                L = evaluate(a, options); log.runs += 1
                n += 1
            log.steps.append({"macro": "Refi_Debt_Sizing", "iterations": n})
        a.pasted.dsra_initial = L.s["Inputs!E371"]          # DSRA_Copy -> DSRA_Paste
        L = evaluate(a, options); log.runs += 1
        log.steps.append({"macro": "DSRA_resize_3"})
    log.converged, log.rounds = _sizing_ok(L), MAX_ROUNDS
    if not log.converged:
        raise SolverError("sizing checks still non-zero after 25 rounds")
    return a, L, log


def solve_exact(a: Assumptions, options: EngineOptions = FAITHFUL, tol: float = 1e-6) -> tuple[Assumptions, Ledger, SolveLog]:
    """Fixed point: pasted funding = calculated funding, pasted DSCR limit =
    DSCR capacity, pasted refi limit = refi capacity, pasted DSRA = DSRA target."""
    a = a.replace()
    log = SolveLog("exact")
    L = evaluate(a, options); log.runs += 1
    for it in range(1, 1000):
        new = {
            "dscr_limit": L.s["Inputs!E300"],
            "refi_limit": L.s["Inputs!E344"] if a.refi.on == 1 else a.pasted.refi_limit,
            "dsra_initial": L.s["Inputs!E371"],
        }
        moved = 0.0
        for k, val in new.items():
            old = getattr(a.pasted, k)
            # damping on the DSCR capacity, as the workbook's trial value does
            step = 0.5 * (val - old) if k == "dscr_limit" else val - old
            setattr(a.pasted, k, old + step)
            moved = max(moved, abs(val - old))
        L = evaluate(a, options); log.runs += 1
        a.pasted.funding = L.s["Inputs!E292"]
        L = evaluate(a, options); log.runs += 1
        moved = max(moved, abs(L.s["Inputs!E292"] - a.pasted.funding))
        if moved < tol:
            log.converged, log.rounds = True, it
            return a, L, log
    raise SolverError("exact solver did not converge")


def solve(a: Assumptions, method: str = "excel_macros", options: EngineOptions = FAITHFUL):
    if method == "excel_macros":
        return solve_excel_macros(a, options)
    if method == "exact":
        return solve_exact(a, options)
    raise ValueError(f"unknown solver method {method!r}")
