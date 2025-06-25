import yaml
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).parent.parent
MKDOCS_YML = ROOT / "mkdocs.yml"
DOCS = ROOT / "docs"
BACKUP = ROOT / "mkdocs.bak.yml"

def ensure_index_md(folder_path):
    index = folder_path / "index.md"
    if not index.exists():
        title = folder_path.name.replace("_", " ").title()
        index.write_text(f"# {title}\n\n_This is the landing page._\n", encoding="utf-8")
        print(f"🧱 Added: {index.relative_to(DOCS)}")

def auto_group_nav():
    all_files = list(DOCS.rglob("*.md"))
    by_folder = {}
    for f in all_files:
        rel = f.relative_to(DOCS).as_posix()
        if rel.startswith("_") or rel.startswith("."): continue
        folder = f.parent.relative_to(DOCS).as_posix()
        by_folder.setdefault(folder, []).append(f)

    nav = []
    for folder, files in sorted(by_folder.items()):
        if folder in ["", ".", "docs"]:  # top-level
            for f in sorted(files):
                rel = f.relative_to(DOCS).as_posix()
                name = f.stem.replace("_", " ").title()
                nav.append({name: rel})
        else:
            section = []
            for f in sorted(files):
                rel = f.relative_to(DOCS).as_posix()
                name = f.stem.replace("_", " ").title()
                section.append({name: rel})
            folder_name = folder.split("/")[-1].replace("_", " ").title()
            nav.append({folder_name: section})

    return nav

def optimize_mkdocs():
    if not MKDOCS_YML.exists():
        print("❌ mkdocs.yml not found.")
        return

    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    print("🧪 Scanning folders and generating grouped nav...")
    nav = auto_group_nav()

    print("🧱 Ensuring index.md for each folder...")
    for entry in nav:
        if isinstance(entry, dict):
            for group, items in entry.items():
                if isinstance(items, list):
                    folder = items[0][list(items[0].keys())[0]].split("/")[0]
                    ensure_index_md(DOCS / folder)

    config["nav"] = nav
    config["theme"] = config.get("theme", {})
    features = config["theme"].get("features", [])
    if "navigation.sections" not in features:
        features.append("navigation.sections")
    if "navigation.expand" not in features:
        features.append("navigation.expand")
    config["theme"]["features"] = features

    shutil.copy(MKDOCS_YML, BACKUP)
    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False)

    print(f"\n✅ Collapsible sidebar applied.")
    print(f"🛟 Backup saved as: {BACKUP}")

if __name__ == "__main__":
    print("📚 Auto-Optimizing mkdocs.yml for Collapsible Nav")
    optimize_mkdocs()
