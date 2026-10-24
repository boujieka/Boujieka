"""Assemble the static assets of the in-browser demo into frontend/demo-public/:

  pyodide/             Pyodide 0.29.4 core (from frontend/node_modules/pyodide, MPL-2.0)
  py/mgs.zip           the engine, labels, comparison, Studio export and the browser entry module,
                       the fictitious template only, plus openpyxl and et_xmlfile (MIT) for the .xlsx export

Run from minigrid-studio/backend with its venv (openpyxl is taken from there):
    .venv/bin/python ../tools/web_demo/build_assets.py
No CrossBoundary file or value is included: the reference template stays out of the demo.
"""
import importlib.util
import io
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
OUT = ROOT / "frontend" / "demo-public"
PYODIDE = ROOT / "frontend" / "node_modules" / "pyodide"
PYODIDE_FILES = ["pyodide.mjs", "pyodide.asm.js", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]
APP_FILES = [
    "app/__init__.py",
    *(f"app/engine/{n}.py" for n in ("__init__", "assumptions", "changes", "excel", "model", "options", "prepare",
                                     "results", "solver", "validation")),
    *(f"app/exports/{n}.py" for n in ("__init__", "labels", "compare", "xlsx_studio")),
    "app/demo/__init__.py", "app/demo/browser.py", "app/demo/templates/demo_fictitious.json",
]


def package_dir(name: str) -> Path:
    spec = importlib.util.find_spec(name)
    if spec is None or spec.origin is None:
        sys.exit(f"{name} not installed in this interpreter")
    return Path(spec.origin).parent


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "pyodide").mkdir(parents=True)
    (OUT / "py").mkdir()
    for f in PYODIDE_FILES:
        shutil.copy2(PYODIDE / f, OUT / "pyodide" / f)
    shutil.copy2(PYODIDE / "package.json", OUT / "pyodide" / "package.json")   # version and licence (MPL-2.0)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in APP_FILES:
            z.write(BACKEND / rel, rel)
        for pkg in ("openpyxl", "et_xmlfile"):
            base = package_dir(pkg)
            for p in sorted(base.rglob("*")):
                if p.is_file() and "__pycache__" not in p.parts and p.suffix in (".py", ".typed", ""):
                    z.write(p, f"{pkg}/{p.relative_to(base)}")
            dist = next(base.parent.glob(f"{pkg}-*.dist-info"), None)
            if dist:
                for lic in dist.rglob("LICEN*"):
                    z.write(lic, f"{pkg}/{lic.name}")
    (OUT / "py" / "mgs.zip").write_bytes(buf.getvalue())
    shutil.copy2(BACKEND / "app/demo/templates/demo_fictitious.json", OUT / "py" / "template.json")
    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"demo assets in {OUT} ({total / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
