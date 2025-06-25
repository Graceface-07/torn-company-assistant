import os
import yaml
from pathlib import Path
import shutil

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"
NEW_YML = ROOT / "mkdocs.nav.yml"
TRASH = ROOT / ".trash"

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
        elif isinstance(n, str):
            links.add(n)
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
    print(f"🧩 Stub created: {rel_path}")

def patch_nav(nav, doc_files):
    def walk(item):
        if isinstance(item, dict):
            patched = {}
            for k, v in item.items():
                sub = walk(v)
                if sub:
                    patched[k] = sub
            return patched if patched else None
        elif isinstance(item, list):
            patched = [walk(i) for i in item]
            return [x for x in patched if x]
        elif isinstance(item, str):
            if item in doc_files:
                return item
            else:
                ans = input(f"❓ Missing file in nav: {item} → Create stub? (y/N): ")
                if ans.lower() == "y":
                    stub_file(item)
                    return item
                else:
                    print(f"🧼 Removed from nav: {item}")
                    return None
    return walk(nav)

def ensure_index_md(doc_files):
    folders = {os.path.dirname(f) for f in doc_files if "/" in f}
    for folder in folders:
        index = f"{folder}/index.md"
        if index not in doc_files:
            ans = input(f"➕ Add missing {index}? (y/N): ")
            if ans.lower() == "y":
                stub_file(index)

def run():
    ensure_dir(TRASH)
    if not MKDOCS_YML.exists():
        print("❌ mkdocs.yml not found.")
        return

    all_md = collect_all_md()

    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    nav = config.get("nav", [])
    nav_links = flatten_nav(nav)

    # Archive orphans
    orphaned = all_md - nav_links
    for orphan in sorted(orphaned):
        ans = input(f"📄 Orphaned: {orphan} → Archive? (y/N): ")
        if ans.lower() == "y":
            archive_file(orphan)
            all_md.discard(orphan)

    ensure_index_md(all_md)

    # Patch nav
    print("\n⚙️ Rebuilding nav tree...")
    fixed_nav = patch_nav(nav, all_md)

    config["nav"] = fixed_nav
    with open(NEW_YML, "w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"\n✅ Done. Preview the patched config here:\n  {NEW_YML}")
    print("🔧 When ready, replace your existing mkdocs.yml with mkdocs.nav.yml.")

if __name__ == "__main__":
    print("🧙‍♂️ Torn Assistant Nav Healer\n" + "-" * 35)
    run()
