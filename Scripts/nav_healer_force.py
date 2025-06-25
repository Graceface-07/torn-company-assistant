import os
import yaml
from pathlib import Path
import shutil

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"
TRASH = ROOT / ".trash"
BACKUP = ROOT / "mkdocs.bak.yml"

def ensure_dir(p): p.mkdir(parents=True, exist_ok=True)

def collect_all_md():
    return {
        f.relative_to(DOCS).as_posix()
        for f in DOCS.rglob("*.md")
        if not f.name.startswith("_")
    }

def flatten_nav(nav):
    links = set()
    def walk(n):
        if isinstance(n, dict):
            for v in n.values(): walk(v)
        elif isinstance(n, list):
            for i in n: walk(i)
        elif isinstance(n, str): links.add(n)
    walk(nav)
    return links

def archive_file(rel_path):
    src = DOCS / rel_path
    dest = TRASH / rel_path
    ensure_dir(dest.parent)
    shutil.move(src, dest)
    print(f"🗃️ Archived: {rel_path}")

def stub_file(rel_path):
    path = DOCS / rel_path
    ensure_dir(path.parent)
    title = path.stem.replace("_", " ").title()
    path.write_text(f"# {title}\n\n_This is a stub page._\n", encoding="utf-8")
    print(f"🧩 Stubbed: {rel_path}")

def patch_nav(nav, doc_files):
    def walk(item):
        if isinstance(item, dict):
            patched = {}
            for k, v in item.items():
                sub = walk(v)
                if sub: patched[k] = sub
            return patched or None
        elif isinstance(item, list):
            patched = [walk(i) for i in item]
            return [x for x in patched if x]
        elif isinstance(item, str):
            if item not in doc_files:
                stub_file(item)
                doc_files.add(item)
            return item
    return walk(nav)

def add_index_to_folders(doc_files):
    folders = {os.path.dirname(f) for f in doc_files if "/" in f}
    for folder in folders:
        index = f"{folder}/index.md"
        if index not in doc_files:
            stub_file(index)
            doc_files.add(index)

def run():
    ensure_dir(TRASH)
    all_md = collect_all_md()

    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    nav_links = flatten_nav(nav)

    # Archive unused
    unused = all_md - nav_links
    for f in unused:
        archive_file(f)
        all_md.remove(f)

    # Patch
    add_index_to_folders(all_md)
    patched_nav = patch_nav(nav, all_md)
    config["nav"] = patched_nav

    shutil.copy(MKDOCS_YML, BACKUP)
    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"\n✅ Healed mkdocs.yml written.")
    print(f"🛟 Original backed up as: {BACKUP}")

if __name__ == "__main__":
    print("🧠 Running nav_healer_force.py (No Prompts)")
    run()
