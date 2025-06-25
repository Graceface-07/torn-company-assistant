import os
import re
import sys
from difflib import get_close_matches

DOCS_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs"))
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((?!http)([^)#]+)(#[^\)]*)?\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s*(.+)$")

def collect_all_files():
    file_map = {}
    for root, _, files in os.walk(DOCS_ROOT):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), DOCS_ROOT).replace("\\", "/")
                file_map[file] = rel_path
    return file_map

def extract_anchors(md_path):
    anchors = set()
    full_path = os.path.join(DOCS_ROOT, md_path)
    if not os.path.exists(full_path):
        return anchors
    with open(full_path, "r", encoding="utf-8") as f:
        for line in f:
            m = HEADING_PATTERN.match(line)
            if m:
                title = m.group(2).strip()
                anchor = re.sub(r"[^\w\s-]", "", title).lower().replace(" ", "-")
                anchors.add(anchor)
    return anchors

def fix_links(md_file, files, fix=False):
    full_path = os.path.join(DOCS_ROOT, md_file)
    changed = False
    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for i, line in enumerate(lines, 1):
        original = line
        for match in LINK_PATTERN.finditer(line):
            text, file_part, anchor = match.groups()
            fixed_path = file_part
            fixed_anchor = anchor or ""

            # Fix path
            if not os.path.isfile(os.path.join(os.path.dirname(full_path), file_part)):
                suggestion = get_close_matches(os.path.basename(file_part), files.keys(), n=1)
                if suggestion:
                    fixed_path = files[suggestion[0]]
                    print(f"🔁 [{md_file}:{i}] Fix path: `{file_part}` → `{fixed_path}`")

            # Fix anchor
            if anchor:
                anchors = extract_anchors(fixed_path)
                anchor_clean = anchor[1:]
                if anchor_clean not in anchors:
                    close = get_close_matches(anchor_clean, anchors, n=1)
                    if close:
                        fixed_anchor = f"#{close[0]}"
                        print(f"🔁 [{md_file}:{i}] Fix anchor: `{anchor}` → `{fixed_anchor}`")

            new_link = f"[{text}]({fixed_path}{fixed_anchor})"
            line = line.replace(match.group(0), new_link)

        if line != original:
            changed = True
        new_lines.append(line)

    if changed and fix:
        with open(full_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"✅ Updated: {md_file}")
    elif changed:
        print(f"🔍 Would update: {md_file}")

def run(mode="check"):
    files = collect_all_files()
    for root, _, fns in os.walk(DOCS_ROOT):
        for fn in fns:
            if fn.endswith(".md"):
                rel = os.path.relpath(os.path.join(root, fn), DOCS_ROOT).replace("\\", "/")
                fix_links(rel, files, fix=(mode == "fix"))

if __name__ == "__main__":
    if "--fix" in sys.argv:
        run(mode="fix")
        print("\n🎉 All fixes applied.")
    else:
        run(mode="check")
        print("\n🔍 Dry run complete. Use --fix to apply changes.")
