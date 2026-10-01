"""Join fr_01..fr_17 (each chunk separated by a blank line), harmonise terms, fix French spacing."""
import re
parts = [open(f"fr_{i:02d}.md", encoding="utf-8").read().strip("\n") for i in range(1, 18)]
t = "\n\n".join(parts) + "\n"
t = t.replace("test du souverain", "test souverain").replace("Test du souverain", "Test souverain").replace("tests du souverain", "tests souverains")
out, inref = [], False
for l in t.split("\n"):
    if l.startswith("#"):
        inref = bool(re.match(r"#+ Références", l))
    if not inref and not l.startswith(":::") and not l.startswith("|--"):
        l = re.sub(r"(?<=[\w»\)\*]) ([;:?!])(?=[\s\*]|$)", " \\1", l)
        l = l.replace("« ", "« ").replace(" »", " »")
    out.append(l)
open("fr_full.md", "w", encoding="utf-8").write("\n".join(out))
