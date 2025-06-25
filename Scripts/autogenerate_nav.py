import os
import yaml

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
MKDOCS_YML = os.path.join(ROOT_DIR, "mkdocs.yml")


def format_title(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    name = name.replace("_", " ").replace("-", " ")
    return name.title()


def group_files_by_folder():
    grouped = {}
    for root, _, files in os.walk(DOCS_DIR):
        md_files = [f for f in files if f.endswith(".md")]
        if not md_files:
            continue

        rel_dir = os.path.relpath(root, DOCS_DIR).replace("\\", "/")
        for md in sorted(md_files):
            rel_path = os.path.normpath(os.path.join(rel_dir, md)).replace("\\", "/")
            if rel_dir == ".":
                grouped.setdefault("_root", []).append(rel_path)
            else:
                grouped.setdefault(rel_dir, []).append(rel_path)
    return grouped


def build_nav_structure(grouped):
    nav = []

    # Optional fixed order for top folders
    folder_titles = {
        "_root": "Home",
        "decision_flow": "Decision Flow",
        "company_profiles": "Company Profiles",
        "output": "Outputs",
    }

    for folder, files in sorted(grouped.items()):
        entries = []
        for file_path in files:
            entries.append({format_title(file_path): file_path})
        section_title = folder_titles.get(folder, format_title(folder))
        if folder == "_root":
            nav.extend(entries)
        else:
            nav.append({section_title: entries})
    return nav


def inject_nav_into_yaml(nav):
    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    config["nav"] = nav

    with open(MKDOCS_YML, "w", encoding="utf-8") as f:
        yaml.dump(config, f, sort_keys=False)

    print("✅ mkdocs.yml successfully updated with automated nav.")


if __name__ == "__main__":
    grouped_files = group_files_by_folder()
    nav_structure = build_nav_structure(grouped_files)

    print("🔧 Generated Navigation:\n")
    print(yaml.dump({"nav": nav_structure}, sort_keys=False))

    choice = input("\n👉 Overwrite mkdocs.yml with this nav? (y/n): ").lower()
    if choice == "y":
        inject_nav_into_yaml(nav_structure)
    else:
        print("🛑 Nav not written to file — preview only.")
