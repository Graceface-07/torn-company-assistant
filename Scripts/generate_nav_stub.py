import os

def get_markdown_files(base_path="docs"):
    pages = []
    for root, _, files in os.walk(base_path):
        for file in sorted(files):
            if file.endswith(".md"):
                rel_dir = os.path.relpath(root, base_path).replace("\\", "/")
                rel_file = f"{rel_dir}/{file}" if rel_dir != "." else file
                pages.append(rel_file)
    return pages

def format_nav(files):
    nav_lines = ["nav:"]
    for file in files:
        title = os.path.splitext(os.path.basename(file))[0].replace("_", " ").title()
        nav_lines.append(f"  - {title}: {file}")
    return "\n".join(nav_lines)

if __name__ == "__main__":
    markdown_files = get_markdown_files()
    nav_block = format_nav(markdown_files)
    print("🔧 Suggested mkdocs.yml nav block:\n")
    print(nav_block)
