import os
import argparse
import yaml

DOCS_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs"))
MKDOCS_YML = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "mkdocs.yml"))

def build_nav(flat=False):
    nav = []
    for root, _, files in os.walk(DOCS_ROOT):
        rel_root = os.path.relpath(root, DOCS_ROOT).replace("\\", "/")
        md_links = []
        for f in sorted(files):
            if f.endswith(".md") and not f.startswith("_"):
                title = os.path.splitext(f)[0].replace("_", " ").title()
                rel_path = os.path.join(rel_root, f).replace("\\", "/") if rel_root != "." else f
                md_links.append({title: rel_path})

        if md_links:
            if flat or rel_root == ".":
                nav.extend(md_links)
            else:
                folder_title = os.path.basename(rel_root).replace("_", " ").title()
                nav.append({folder_title: md_links})
    return nav

def inject_nav(new_nav):
    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["nav"] = new_nav

    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False)

    print("✅ Injected nav into mkdocs.yml")

def display_nav(nav):
    print(yaml.dump({"nav": nav}, sort_keys=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build nav for mkdocs.yml")
    parser.add_argument("--flat", action="store_true", help="Generate flat nav")
    parser.add_argument("--inject", action="store_true", help="Inject into mkdocs.yml")

    args = parser.parse_args()

    nav = build_nav(flat=args.flat)

    if args.inject:
        inject_nav(nav)
    else:
        display_nav(nav)
