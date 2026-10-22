"""Generate docs/DATABASE_SCHEMA.md tables section from the ORM metadata: python scripts/gen_schema_doc.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app.models as m  # noqa: E402

out = []
for t in m.Base.metadata.sorted_tables:
    out.append(f"### `{t.name}`\n")
    if t.comment:
        out.append(t.comment + "\n")
    out.append("| Column | Type | Null | Key / reference |\n|---|---|---|---|")
    for c in t.columns:
        keys = []
        if c.primary_key:
            keys.append("PK")
        for fk in c.foreign_keys:
            keys.append(f"FK → `{fk.target_fullname}`")
        if c.unique:
            keys.append("unique")
        if c.index:
            keys.append("indexed")
        out.append(f"| `{c.name}` | {c.type} | {'yes' if c.nullable else 'no'} | {', '.join(keys)} |")
    uqs = [", ".join(col.name for col in con.columns) for con in t.constraints if con.__class__.__name__ == "UniqueConstraint" and len(con.columns) > 1]
    cks = [str(con.sqltext) for con in t.constraints if con.__class__.__name__ == "CheckConstraint"]
    if uqs:
        out.append("\nUnique together: " + "; ".join(f"({u})" for u in uqs))
    if cks:
        out.append("\nChecks: " + "; ".join(f"`{c}`" for c in cks))
    out.append("")
print("\n".join(out))
