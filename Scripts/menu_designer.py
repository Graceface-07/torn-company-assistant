import os
import yaml
from pathlib import Path
from prompt_toolkit.shortcuts import checkboxlist_dialog, input_dialog, yes_no_dialog

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MKDOCS_YML = ROOT / "mkdocs.yml"

def scan_markdown_files():
    files = []
    for path in DOCS.rglob("*.md"):
        if "main_menu.md" in path.name.lower():
            continue
        rel_path = path.relative_to(DOCS).as_posix()
        full_path = DOCS / rel_path
        desc = extract_description(full_path)
        label = f"{rel_path} — {desc}" if desc else rel_path
        files.append((rel_path, label))
    return sorted(files, key=lambda x: x[0])

def extract_description(filepath):
    try:
        lines = filepath.read_text(encoding="utf-8").splitlines()
        for line in lines[:5]:
            line = line.strip()
            if line.lower().startswith("<!-- description:"):
                return line.strip("<!-->").replace("description:", "", 1).strip()
    except Exception:
        pass
    return None

def group_sections(choices):
    sections = []
    used = set()

    while True:
        label = input_dialog(
            title="🗂 New Section",
            text="Section name (blank to finish):"
        ).run()
        if not label:
            break

        available = [(k, v) for k, v in choices if k not in used]
        if not available:
            break

        selected = checkboxlist_dialog(
            title=f"☑️ Files for '{label}'",
            text="Tick the pages to include:",
            values=available
        ).run()
        if not selected:
            continue

        collapse = yes_no_dialog(
            title="Collapse Section?",
            text=f"Should '{label}' be collapsible (requires index.md)?"
        ).run()

        sections.append({"title": label, "collapse": collapse, "files": selected})
        used.update(selected)

    return sections

def build_nav_structure(sections):
    nav = []
    for section in sections:
        title = section["title"]
        children = []
        for path in section["files"]:
            name = Path(path).stem.replace("_", " ").title()
            children.append({name: path})
        nav.append({title: children})
    return nav

def write_nav(nav):
    if not MKDOCS_YML.exists():
        print("❌ mkdocs.yml not found.")
        return

    with MKDOCS_YML.open("r", encoding="utf-8") as f:
        yml = yaml.safe_load(f)

    yml["nav"] = nav

    with MKDOCS_YML.open("w", encoding="utf-8") as f:
        yaml.dump(yml, f, sort_keys=False, allow_unicode=True)

    print("✅ Navigation updated in mkdocs.yml")

def run():
    print("📘 Launching Smart Sidebar Builder...\n")
    choices = scan_markdown_files()
    if not choices:
        print("No Markdown files found.")
        return

    sections = group_sections(choices)
    if not sections:
        print("No sections created — exiting.")
        return

    nav = build_nav_structure(sections)

    print("\n🔍 Final Navigation Preview:\n")
    for sec in nav:
        label = list(sec.keys())[0]
        print(f"  {label}")
        for item in sec[label]:
            name = list(item.keys())[0]
            print(f"    - {name}: {item[name]}")

    confirm = yes_no_dialog(
        title="Apply Navigation?",
        text="Save this structure to mkdocs.yml?"
    ).run()

    if confirm:
        write_nav(nav)
    else:
        print("❌ Changes discarded.")

if __name__ == "__main__":
    run()
