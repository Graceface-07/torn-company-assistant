import os
import yaml
from pathlib import Path
import shutil

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"
TRASH = ROOT / ".trash"

def flatten_nav(nav):
    links = set()

    def walk(node):
        if isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for i in node:
                walk(i)
        elif isinstance(node, str):
            links.add(node)

    walk(nav)
    return links

def collect_md_files():
    return {
        f.relative_to(DOCS).as_posix()
        for f in DOCS.rglob("*.md")
        if not f.name.startswith("_")
    }

def collect_folders(files):
    return sorted({os.path.dirname(f) for f in files if "/" in f})

def ensure_folder(path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

def archive_file(rel_path):
    src = DOCS / rel_path
    dest = TRASH / rel_path
    ensure_folder(dest.parent)
    shutil.move(src, dest)
    print(f"🗑️  Archived: {rel_path} → .trash/{rel_path}")

def write_blank_index(folder):
    path = DOCS / folder / "index.md"
    path.write_text(f"# {folder.title()}\n", encoding="utf-8")
    print(f"📄 Created: {folder}/index.md")

def clean_nav():
    if not MKDOCS_YML.exists():
        print("❌ mkdocs.yml not found.")
        return

    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    nav_files = flatten_nav(nav)
    all_md = collect_md_files()

    unused = all_md - nav_files
    if unused:
        print(f"\n📄 Unused Markdown files ({len(unused)}):")
        for f in sorted(unused):
            ans = input(f"  - {f} → Archive? (y/N): ")
            if ans.lower() == "y":
                archive_file(f)

    folders = collect_folders(all_md)
    print("\n📁 Checking folders for missing index.md...")
    for folder in folders:
        index = f"{folder}/index.md"
        if index not in all_md:
            ans = input(f"  - {folder}/ (missing index.md) → Create? (y/N): ")
            if ans.lower() == "y":
                write_blank_index(folder)

if __name__ == "__main__":
    print("🧹 Torn Assistant Folder Cleanup")
    print("-" * 35)
    ensure_folder(TRASH)
    clean_nav()
    print("\n✅ Cleanup complete.")
