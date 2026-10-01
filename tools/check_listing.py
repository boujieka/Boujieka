"""Check Etsy title/tag lengths in marketing/LISTINGS.md (title <= 140 chars, 13 tags <= 20 chars) for each product listing."""
import re
import sys

text = open("marketing/LISTINGS.md", encoding="utf-8").read()
blocks = re.findall(r"```\n(.*?)```", text, re.S)
ok = True
# Etsy listings: title block followed by tags block, at block index 0 (P1) and 4 (P2)
for start in (0, 4):
    title = blocks[start].strip()
    tags = [t.strip() for t in blocks[start + 1].strip().splitlines() if t.strip()]
    print(f"Title: {len(title)} chars | Tags: {len(tags)}")
    if len(title) > 140:
        ok = False
        print("  ERROR: title over 140 characters")
    if len(tags) > 13:
        ok = False
        print("  ERROR: more than 13 tags")
    for t in tags:
        if len(t) > 20:
            ok = False
            print(f"  ERROR: tag over 20 chars: {t!r} ({len(t)})")
sys.exit(0 if ok else 1)
