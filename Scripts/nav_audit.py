import os
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"

def find_md_files():
    return {
        f.relative_to(DOCS).as_posix()
        for f in DOCS.rglob("*.md")
        if not f.name.startswith("_")
    }

def flatten_nav(nav):
    links = set()

    def walk(item):
        if isinstance(item, dict):
            for v in item.values():
                walk(v)
        elif isinstance(item, list):
            for x in item:
                walk(x)
        elif isinstance(item, str):
            links.add(item)

    walk(nav)
    return links

def audit():
    if not MKDOCS_YML.exists():
        print("❌ mkdocs.yml not found.")
        return

    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    nav_files = flatten_nav(nav)
    doc_files = find_md_files()

    print("\n🔍 Navigation Audit Report")
    print("-" * 40)

    unused = doc_files - nav_files
    missing = nav_files - doc_files

    if unused:
        print(f"📄 Files not in nav ({len(unused)}):")
        for f in sorted(unused):
            print(f"  - {f}")
    else:
        print("✅ All Markdown files are included in nav.")

    if missing:
        print(f"\n⚠️ Nav entries missing from disk ({len(missing)}):")
        for f in sorted(missing):
            print(f"  - {f}")
    else:
        print("✅ All nav entries point to valid files.")

    print("\n📁 Folders missing index.md:")
    folders = {os.path.dirname(path) for path in doc_files if "/" in path}
    for folder in sorted(folders):
        if f"{folder}/index.md" not in doc_files:
            print(f"  - {folder}/ (no index.md)")

if __name__ == "__main__":
    audit()
