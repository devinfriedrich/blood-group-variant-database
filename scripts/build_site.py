"""
Assembles the deployable site into _site/.

The repository root is not safe to publish directly: it holds
data/variants_raw.json, which contains every compiled record including the
systems that are deliberately not published (see SCOPE_SYSTEMS in
normalize_data.py). Publishing the root would make those fetchable by URL.
So only the files a visitor actually needs are copied.

Run from anywhere: python3 scripts/build_site.py
Output: _site/ (gitignored)
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

PAGES = [
    "index.html", "stats.html", "methods.html", "download-cite.html",
    "about.html", "changelog.html", "feedback.html",
]
ASSETS = ["assets/style.css", "assets/app.js", "assets/data.js"]
# The two generated, in-scope data files the Download page links to.
DATA = ["data/variants.json", "data/variants.csv"]
EXTRAS = ["CITATION.cff"]

# Anything matching these must never reach the publish directory.
FORBIDDEN = ["variants_raw.json"]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    copied = []
    for rel in PAGES + ASSETS + DATA + EXTRAS:
        src = ROOT / rel
        if not src.exists():
            sys.exit(f"ERROR: expected file is missing: {rel}")
        dst = OUT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copied.append(rel)

    # Fail the build rather than publish a file that should stay private.
    for path in OUT.rglob("*"):
        if path.is_file() and any(bad in path.name for bad in FORBIDDEN):
            sys.exit(f"ERROR: refusing to publish {path.relative_to(OUT)}")

    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"Assembled {len(copied)} files into {OUT} ({total:,} bytes)")
    for rel in copied:
        print(f"  {rel}")


if __name__ == "__main__":
    main()
