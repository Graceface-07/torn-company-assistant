import os
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"
OUTPUT = DOCS / "main_menu.md"

EXCLUDE = {"index.md", "main_menu.md", "README.md"}

def load_nav_order():
    with MKDOCS.open("r", encoding="utf-8") as f:
        yml = yaml.safe_load(f)
        return yml.get("nav", [])

def flatten_nav(nav):
    paths = []

    def walk(item, label=""):
        if isinstance(item, list):
            for i in item: walk(i)
        elif isinstance(item, dict):
            for k, v in item.items():
                walk(v, k)
        elif isinstance(item, str):
            paths.append((label, item))
    walk(nav)
    return paths

def get_section(md_path):
    parent = md_path.parent.relative_to(DOCS)
    return str(parent) if parent != Path('.') else "Home"

def generate():
    print("📘 Generating main_menu.md...")

    nav = flatten_nav(load_nav_order())
    sections = {}

    for label, rel_path in nav:
        if rel_path in EXCLUDE: continue
        full = DOCS / rel_path
        if not full.exists(): continue
        section = get_section(full)
        sections.setdefault(section, []).append((label, rel_path))

    with OUTPUT.open("w", encoding="utf-8") as f:
        f.write("# Main Menu\n\nWelcome to the Torn Assistant. Choose a section below to explore:\n\n---\n")
        for section in sorted(sections):
            emoji = "📁"
            if "decision_flow" in section:
                emoji = "🎯"
            elif "company_profiles" in section:
                emoji = "🏢"
            elif "features" in section:
                emoji = "⚙️"
            elif "utils" in section or "tools" in section:
                emoji = "🛠️"
            elif "output" in section:
                emoji = "📦"
            elif "changelog" in section:
                emoji = "📜"
            elif section == "Home":
                continue

            section_title = section.replace("_", " ").title()
            f.write(f"\n## {emoji} {section_title}\n\n")
            for label, path in sorted(sections[section]):
                f.write(f"- [{label}]({path})\n")

    print("✅ main_menu.md updated.")

if __name__ == "__main__":
    generate()
