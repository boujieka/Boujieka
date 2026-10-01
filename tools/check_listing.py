"""Check Etsy title/tag lengths in marketing/LISTINGS.md (title <= 140 chars, 13 tags <= 20 chars)."""
import re
import sys

text = open("marketing/LISTINGS.md", encoding="utf-8").read()
blocks = re.findall(r"```\n(.*?)```", text, re.S)
title = blocks[0].strip()
tags = [t.strip() for t in blocks[1].strip().splitlines() if t.strip()]
ok = True
print(f"Title: {len(title)} chars")
if len(title) > 140:
    ok = False
    print("  ERROR: title over 140 characters")
print(f"Tags: {len(tags)}")
if len(tags) > 13:
    ok = False
    print("  ERROR: more than 13 tags")
for t in tags:
    if len(t) > 20:
        ok = False
        print(f"  ERROR: tag over 20 chars: {t!r} ({len(t)})")
sys.exit(0 if ok else 1)
