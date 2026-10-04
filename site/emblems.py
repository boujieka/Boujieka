"""Fetch the national flags and coats of arms used by the quarterly report, with their licences.

    python site/emblems.py            # downloads into brand/emblems/ and writes emblems.json

Files come from Wikimedia Commons only. For each one the manifest keeps the Commons page, the
licence and author as Commons states them, the SHA-1 that Commons publishes and the SHA-256 of the
downloaded bytes. A file whose SHA-1 differs from Commons' is rejected. SVGs that carry scripts
or external references are rejected too (they are shown with <img>, but they must stay inert).
The file names are chosen by hand below: the current national version, as categorised on Commons
on the date of the fetch. Recheck them when a country changes its emblem (Burkina Faso, 2025).
"""

import hashlib
import json
import re
import subprocess
import time
from datetime import date
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "brand" / "emblems"
UA = "CartoucheReportBot/1.0 (https://cartouche-africa.netlify.app)"
API = "https://commons.wikimedia.org/w/api.php"

FILES = {
    "BEN": ("Flag of Benin.svg", "Coat of arms of Benin.svg"),
    "BFA": ("Flag of Burkina Faso.svg", "Coat of arms of Burkina Faso (2025-present).svg"),
    "CIV": ("Flag of Côte d'Ivoire.svg", "Coat of arms of Ivory Coast.svg"),
    "GNB": ("Flag of Guinea-Bissau.svg", "Emblem of Guinea-Bissau.svg"),
    "MLI": ("Flag of Mali.svg", "Coat of arms of Mali.svg"),
    "NER": ("Flag of Niger.svg", "Coat of arms of Niger.svg"),
    "SEN": ("Flag of Senegal.svg", "Coat of arms of Senegal.svg"),
    "TGO": ("Flag of Togo.svg", "Armoiries du Togo.svg"),
}


def _get(args: list[str]) -> bytes:
    """curl with a descriptive User-Agent and patient retries (Commons rate-limits)."""
    for i in range(8):
        r = subprocess.run(["curl", "-sSfL", "-A", UA, *args], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout
        time.sleep(15 * (i + 1))
    raise SystemExit(f"download failed: {args[-1]}")


def _api(title: str) -> dict:
    out = json.loads(_get(["-G", API, "--data-urlencode", "action=query", "--data-urlencode", "format=json",
                           "--data-urlencode", "redirects=1", "--data-urlencode", "prop=imageinfo",
                           "--data-urlencode", "iiprop=url|sha1|extmetadata",
                           "--data-urlencode", f"titles=File:{title}"]))
    page = next(iter(out["query"]["pages"].values()))
    if "imageinfo" not in page:
        raise SystemExit(f"not on Commons: {title}")
    return page


def _text(html: str | None) -> str | None:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", html))).strip() if html else None


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {"fetched": date.today().isoformat(), "source": "Wikimedia Commons", "countries": {}}
    for iso3, pair in FILES.items():
        entry = {}
        for kind, title in zip(("flag", "arms"), pair):
            page = _api(title)
            ii, meta = page["imageinfo"][0], page["imageinfo"][0]["extmetadata"]
            g = lambda k: (meta.get(k) or {}).get("value")  # noqa: E731
            name = f"{iso3.lower()}-{kind}.svg"
            cached = OUT / name
            body = cached.read_bytes() if cached.exists() else b""
            if hashlib.sha1(body).hexdigest() != ii["sha1"]:  # resumable: only fetch what is missing
                body = _get([ii["url"]])
                time.sleep(10)
            if hashlib.sha1(body).hexdigest() != ii["sha1"]:
                raise SystemExit(f"SHA-1 differs from Commons for {title}")
            if re.search(rb"<script|javascript:|xlink:href=\"(?!#)|href=\"http|<foreignObject", body, re.I):
                raise SystemExit(f"active or external content in {title}")
            (OUT / name).write_bytes(body)
            entry[kind] = {
                "file": name, "commons_title": page["title"], "requested": f"File:{title}",
                "page": ii["descriptionurl"], "url": ii["url"], "sha256": hashlib.sha256(body).hexdigest(),
                "license": g("LicenseShortName"), "license_url": g("LicenseUrl"),
                "author": _text(g("Artist")), "credit": _text(g("Credit")),
                "restrictions": g("Restrictions"),
            }
            time.sleep(3)
        manifest["countries"][iso3] = entry
        print(iso3, entry["flag"]["license"], "|", entry["arms"]["license"], entry["arms"]["commons_title"])
        # Written after each country, so an interrupted run (rate limits) leaves a valid manifest.
        (OUT / "emblems.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
