import yaml
from pathlib import Path

ROOT = Path("C:/Users/farsi/Documents/Torn Assistant/torn-assistant")
MKDOCS_YML = ROOT / "mkdocs.yml"
DOCS = ROOT / "docs"

def extract_md_paths(nav_section):
    """Recursively pull all .md paths from the nav section"""
    paths = []

    def walk(node):
        if isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            for val in node.values():
                walk(val)
        elif isinstance(node, str) and node.endswith(".md"):
            paths.append(node)

    walk(nav_section)
    return paths

def load_mkdocs_paths():
    with MKDOCS_YML.open(encoding="utf-8") as f:
        yml = yaml.safe_load(f)
    return extract_md_paths(yml.get("nav", []))

def suggest_description(text):
    lines = text.strip().splitlines()
    joined = " ".join(line.strip() for line in lines if line.strip())
    if "job" in joined.lower():
        return "Provides guidance on job selection and stats."
    elif "profit" in joined.lower() or "$" in joined:
        return "Helps analyze profit-oriented decisions or strategies."
    elif "refill" in joined.lower():
        return "Calculates optimal refill value or timing."
    elif "stat" in joined.lower():
        return "Analyzes player statistics for strategic planning."
    elif "company" in joined.lower():
        return "Details aspects of company management or evaluation."
    elif "respec" in joined.lower():
        return "Tool to reset or rebuild your character's stats."
    elif "goal" in joined.lower():
        return "Assists in choosing gameplay goals or outcomes."
    elif "flow" in joined.lower():
        return "Describes flow-based decision making or logic trees."
    elif "link" in joined.lower():
        return "Checks and manages internal documentation links."
    elif "nav" in joined.lower():
        return "Helps design and optimize your MkDocs navigation."
    return "This guide supports decision making in Torn Assistant."

def insert_description(md_path, description):
    full_path = DOCS / md_path
    if not full_path.exists():
        print(f"❌ Missing: {md_path}")
        return

    lines = full_path.read_text(encoding="utf-8").splitlines()

    already_exists = any("<!-- description:" in line.lower() for line in lines[:5])
    if already_exists:
        print(f"📝 Skipped (existing): {md_path}")
        return

    lines.insert(0, f"<!-- description: {description} -->")
    full_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Added: {md_path}")

def run():
    print("🔍 Scanning mkdocs.yml for all referenced docs...\n")
    paths = load_mkdocs_paths()
    for md in paths:
        full_path = DOCS / md
        if not full_path.exists():
            print(f"⚠️  Not found: {md}")
            continue
        content = full_path.read_text(encoding="utf-8")
        desc = suggest_description(content)
        insert_description(md, desc)

if __name__ == "__main__":
    run()
