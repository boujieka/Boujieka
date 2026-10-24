"""Apply edits to an assumption set (pure: used by the API and by the in-browser demo).

Changes are keyed by dotted path ("debt.sizing_method") or workbook cell ("Inputs!E302");
"lots" replaces the whole lot table. Errors raise ChangeError with a user-facing message.
"""
from __future__ import annotations

import dataclasses
import math
import re

from .assumptions import LOT_COLUMNS, Lot, cell_paths, from_dict, set_path, to_dict

CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")


class ChangeError(ValueError):
    pass


def apply_changes(base: dict, changes: dict) -> dict:
    if "lots" in changes:   # whole lot table replaced (add, remove or reorder lots)
        base = {**base, "lots": parse_lots(changes["lots"])}
        changes = {k: v for k, v in changes.items() if k != "lots"}
    a = from_dict(base)
    paths = cell_paths()
    for key, value in changes.items():
        path = paths.get(key, key)
        try:
            set_path(a, path, value)
        except (AttributeError, IndexError, ValueError, TypeError) as exc:
            raise ChangeError(f"cannot set {key!r}: {exc}") from exc
    return to_dict(a)


def parse_lots(lots) -> list[dict]:
    if not isinstance(lots, list) or not 1 <= len(lots) <= len(LOT_COLUMNS):
        raise ChangeError(f"lots must be a list of 1 to {len(LOT_COLUMNS)} lots")
    fields = {f.name: f for f in dataclasses.fields(Lot)}
    out = []
    for i, lot in enumerate(lots):
        if not isinstance(lot, dict) or set(lot) - set(fields):
            raise ChangeError(f"lots.{i}: unknown fields {sorted(set(lot) - set(fields)) if isinstance(lot, dict) else ''}")
        clean = {}
        for name, f in fields.items():
            v = lot.get(name)
            required = f.default is dataclasses.MISSING
            if v is None:
                if required:
                    raise ChangeError(f"lots.{i}.{name} is required")
                clean[name] = None
            elif name in ("name", "country"):
                if not isinstance(v, str) or len(v) > 100 or CONTROL_CHARS.search(v):
                    raise ChangeError(f"lots.{i}.{name} must be text (100 characters at most, no control characters)")
                clean[name] = v
            elif isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise ChangeError(f"lots.{i}.{name} must be a finite number")
            else:
                clean[name] = v
        out.append(clean)
    return out
