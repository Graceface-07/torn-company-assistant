import os
import re
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

MD_LINK = re.compile(r'\[([^\]]+)\]\((?!http)([^)#]+)(#[^\)]*)?\)')

def all_md_files():
    return {
        f.relative_to(DOCS).as_posix(): f
        for f in DOCS.rglob("*.md")
        if f.is_file()
    }

def flatten_nav(nav):
    results = set()
    def walk(n):
        if isinstance(n, list):
            for item in n: walk(item)
        elif isinstance(n, dict):
            for v in n.values(): walk(v)
        elif isinstance(n, str):
            results.add(n)
    walk(nav)
    return results

def scan_links():
    links = set()
    for path in DOCS.rglob("*.md"):
        rel = path.relative_to(DOCS)
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                for match in MD_LINK.findall(line):
                    target = match[1].strip().split("#")[0]
                    if target.endswith(".md"):
                        full = (path.parent / target).resolve()
                        try:
                            rel_path = full.relative_to(DOCS).as_posix()
                            links.add((str(rel), rel_path))
                        except ValueError:
                            pass
    return links

def check_index_md(md_files):
    folders = {}
    for rel_path in md_files:
        parent = os.path.dirname(rel_path)
        if parent and parent not in folders:
            folders[parent] = []
        if parent:
            folders[parent].append(rel_path)
    missing = []
    for folder, files in folders.items():
        if f"{folder}/index.md" not in files:
            missing.append(folder)
    return missing

def run():
    print("🧪 Running Full Site Audit...\n")

    if not MKDOCS.exists():
        print("❌ mkdocs.yml not found.")
        return

    with open(MKDOCS, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav_files = flatten_nav(config.get("nav", []))
    md_files = all_md_files()
    md_keys = set(md_files.keys())

    # Orphans and missing
    orphans = md_keys - nav_files
    missing_nav = nav_files - md_keys

    print("📄 Files not in nav:")
    for o in sorted(orphans):
        print(f"  - {o}")
    if not orphans: print("  ✅ None")

    print("\⚠️ Nav entries missing from disk:")
    for m in sorted(missing_nav):
        print(f"  - {m}")
    if not missing_nav: print("  ✅ None")

    # Link scan
    link_refs = scan_links()
    broken_links = [target for src, target in link_refs if target not in md_keys]

    print("\n🔗 Broken internal Markdown links:")
    for src, target in sorted(link_refs):
        if target not in md_keys:
            print(f"  - {src} ➜ {target}")
    if not broken_links: print("  ✅ All internal links are valid")

    # Index check
    missing_index = check_index_md(md_keys)

    print("\n📁 Folders missing index.md:")
    for folder in sorted(missing_index):
        print(f"  - {folder}/")
    if not missing_index: print("  ✅ All folders have index.md")

    print("\n✅ Audit complete.")

if __name__ == "__main__":
    run()
