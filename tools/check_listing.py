"""Check Etsy title/tag limits (title <= 140 chars, max 13 tags of <= 20 chars) in a listings file.

Usage: python tools/check_listing.py [marketing/LISTINGS.md]
Finds each "**Title**"/"**Titre Etsy**" code block and the "**Tags**"/"**Tags Etsy**" block that follows it.
"""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "marketing/LISTINGS.md"
text = open(path, encoding="utf-8").read()
pattern = re.compile(r"\*\*(?:Title|Titre Etsy)\*\*[^\n]*\n\s*```\n(.*?)```\s*\*\*(?:Tags|Tags Etsy)\*\*[^\n]*\n\s*```\n(.*?)```", re.S)
found = pattern.findall(text)
ok = bool(found)
if not found:
    print("ERROR: no title/tags blocks found")
for title, tag_block in found:
    title = title.strip()
    tags = [t.strip() for t in tag_block.strip().splitlines() if t.strip()]
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
