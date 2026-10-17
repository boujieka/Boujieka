"""Contrôle indépendant des valeurs collectées par les agents de recherche.

Pour chaque enregistrement : retélécharge l'URL (HTML ou PDF), normalise le texte et vérifie
1. que la citation figure dans le document (correspondance exacte, sinon 85 % des mots de la citation),
2. que la valeur numérique enregistrée apparaît dans la citation (formats 1 093 / 1,093 / 0.074 / 7,4…).

    python verify_citations.py recherche/brut/*.json --out recherche/verification.json

Pour un tableau PDF (cellules réassemblées), la citation est acceptée si ≥ 90 % de ses mots
figurent à moins de 400 caractères d'une occurrence de la valeur (statut citation_partielle).

Statuts : confirmé, citation_partielle, qualitatif_citation_ok, citation_absente,
valeur_absente_de_citation (valeur dérivée, additionnée ou non citée), inaccessible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
# SEC EDGAR refuse les navigateurs anonymes et exige un agent déclaré (sec.gov/os/accessing-edgar-data).
UA_SEC = "EtudeSolaireAfrique research contact@example.org"


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    text = re.sub(r"[‘’“”'\"`]", "", text)
    text = re.sub(r"[‐-―-]", "-", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch_text(url: str, cache: dict[str, str | None]) -> str | None:
    if url in cache:
        return cache[url]
    text = None
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "doc"
        ua = UA_SEC if "sec.gov" in url else UA
        r = subprocess.run(["curl", "-sSL", "--fail", "--max-time", "60", "-A", ua, "-o", str(raw), url],
                           capture_output=True)
        if r.returncode == 0 and raw.exists() and raw.stat().st_size > 0:
            data = raw.read_bytes()
            if data[:5] == b"%PDF-":
                out = Path(tmp) / "doc.txt"
                subprocess.run(["pdftotext", "-layout", str(raw), str(out)], capture_output=True)
                text = out.read_text(errors="ignore") if out.exists() else None
            else:
                html = data.decode("utf-8", errors="ignore")
                html = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
                text = re.sub(r"<[^>]+>", " ", html)
                import html as h
                text = h.unescape(text)
    cache[url] = text
    return text


def number_variants(v: float) -> set[str]:
    """Écritures possibles d'une valeur : unités converties (x100 pour %, k/M) et séparateurs FR/EN."""
    out = set()
    for x in {v, v * 100, v * 1000, v * 1e6, v * 1e9, v / 1000, v / 1e6, v / 1e9}:
        for d in range(0, 7):
            if abs(round(x, d) - x) > 1e-9 * max(1, abs(x)):
                continue
            ip, _, dp = f"{x:.{d}f}".partition(".")
            if ip in ("0", "-0") and not dp:
                continue
            for sep in (",", " ", "\u202f", ""):
                grouped = f"{int(ip):,}".replace(",", sep)
                for dec in (".", ","):
                    if sep == dec:
                        continue
                    out.add(grouped + (dec + dp if dp else ""))
    return {normalize(s) for s in out}


def value_in_quote(value, quote_n: str) -> bool:
    if not isinstance(value, (int, float)):
        return normalize(str(value)) in quote_n
    return any(re.search(r"(?<![\d.,])" + re.escape(v) + r"(?![\d])", quote_n)
               for v in number_variants(float(value)))


def near_value(value: float, quote_n: str, doc_n: str, radius: int = 400) -> bool:
    """Vrai si ≥ 90 % des mots de la citation figurent à moins de `radius` caractères d'une
    occurrence de la valeur dans le document."""
    words = {w for w in re.findall(r"[a-z0-9]+", quote_n) if len(w) > 2}
    if not words:
        return False
    for v in number_variants(float(value)):
        for m in re.finditer(r"(?<![\d.,])" + re.escape(v) + r"(?![\d])", doc_n):
            window = doc_n[max(0, m.start() - radius): m.end() + radius]
            if sum(w in window for w in words) / len(words) >= 0.9:
                return True
    return False


def check(rec: dict, cache) -> dict:
    url, quote = rec.get("url", ""), rec.get("citation", "")
    text = fetch_text(url, cache) if url.startswith("http") else None
    res = {"url_sha1": hashlib.sha1(url.encode()).hexdigest()[:10]}
    if not text or len(text) < 200:
        res["statut"] = "inaccessible"
        return res
    doc_n, quote_n = normalize(text), normalize(quote)
    # Les citations élidées (« [...] », « ... ») sont vérifiées fragment par fragment.
    fragments = [f.strip(" ,;") for f in re.split(r"\[\.\.\.\]|\.\.\.|…", quote_n) if f.strip(" ,;")]
    if fragments and all(f in doc_n for f in fragments):
        found = "exacte"
    else:
        words = [w for w in re.findall(r"[a-z0-9.,%]+", quote_n) if len(w) > 2]
        hit = sum(1 for w in words if w in doc_n) / max(1, len(words))
        found = "partielle" if hit >= 0.85 else "absente"
        res["mots_trouves"] = round(hit, 2)
    if found == "absente" and isinstance(rec.get("valeur"), (int, float)) and near_value(rec["valeur"], quote_n, doc_n):
        # Cellules de tableau PDF réassemblées : mots de la citation regroupés autour de la valeur.
        found = "tableau"
        res["mode"] = "proximite_tableau"
    if found == "absente":
        res["statut"] = "citation_absente"
    elif not isinstance(rec.get("valeur"), (int, float)):
        # Valeur qualitative reformulée (procédure, financeurs…) : seule la citation est vérifiable.
        res["statut"] = "qualitatif_citation_ok"
    elif not value_in_quote(rec.get("valeur"), quote_n):
        res["statut"] = "valeur_absente_de_citation"
    else:
        res["statut"] = "confirmé" if found == "exacte" else "citation_partielle"
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cache: dict[str, str | None] = {}
    results = []
    for f in a.files:
        data = json.loads(Path(f).read_text())
        for i, rec in enumerate(data.get("records", [])):
            results.append({"fichier": Path(f).name, "index": i, **check(rec, cache)})
    Path(a.out).write_text(json.dumps(results, ensure_ascii=False, indent=1))
    from collections import Counter
    print(Counter(r["statut"] for r in results))


if __name__ == "__main__":
    main()
