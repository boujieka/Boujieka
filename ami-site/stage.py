"""Prepare a deployable copy of the site in a staging directory (outside git).

Usage: python ami-site/stage.py <staging_dir> <password_file>
Copies netlify.toml, the edge function and dist/ (run build.py first), and writes
netlify/lib/password-hash.ts with the SHA-256 of the password read from <password_file>.
Deploy from <staging_dir> (dist/ and the hash are git-ignored in the repo).
"""
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    stage, password_file = Path(sys.argv[1]), Path(sys.argv[2])
    password = password_file.read_text(encoding="utf-8").strip()
    if len(password) < 16:
        sys.exit("password too short")
    if not (HERE / "dist" / "index.html").exists():
        sys.exit("run build.py first")
    if stage.exists():
        shutil.rmtree(stage)
    shutil.copytree(HERE / "dist", stage / "dist")
    shutil.copytree(HERE / "netlify" / "edge-functions", stage / "netlify" / "edge-functions")
    shutil.copy(HERE / "netlify.toml", stage / "netlify.toml")
    (stage / "netlify" / "lib").mkdir(parents=True)
    digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
    (stage / "netlify" / "lib" / "password-hash.ts").write_text(
        f'export const PASSWORD_SHA256 = "{digest}";\n', encoding="utf-8")
    print(f"Staged in {stage}")


if __name__ == "__main__":
    main()
