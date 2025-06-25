import os
import re
import sys
from difflib import get_close_matches

DOCS_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs"))
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((?!http)([^)#]+)(#[^\)]*)?\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s*(.+)$")

def collect_all_files():
    md_paths = {}
    for root, _, files in os.walk(DOCS_ROOT):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), DOCS_ROOT).replace("\\", "/")
                md_paths[os.path.basename(file)] = rel_path
    return md_paths

def extract_anchors(md_path):
    anchors = set()
    with open(os.path.join(DOCS_ROOT, md_path), "r", encoding="utf-8") as f:
        for line in f:
            match = HEADING_PATTERN.match(line)
            if match:
                heading = match.group(2).strip()
                anchor = re.sub(r"[^\w\s-]", "", heading).lower().replace(" ", "-")
                anchors.add(anchor)
    return anchors

def resolve_path(src, target):
    return os.path.normpath(os.path.join(os.path.dirname(src), target))

def fix_links_in_file(filepath, all_files, dry_run=True):
    full_path = os.path.join(DOCS_ROOT, filepath)
    changed = False
    output_lines = []

    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        original = line
        for match in LINK_PATTERN.finditer(line):
            text, file_part, anchor = match.groups()
            fixed_path = file_part

            # Fix incorrect paths
            if not os.path.isfile(os.path.join(os.path.dirname(full_path), file_part)):
                match_file = get_close_matches(os.path.basename(file_part), all_files.keys(), n=1)
                if match_file:
                    fixed_path = all_files[match_file[0]]
                    print(f"🔁 {filepath}: fixed path `{file_part}` → `{fixed_path}`")

            # Fix anchors
            if anchor and os.path.isfile(os.path.join(DOCS_ROOT, fixed_path)):
                target_anchors = extract_anchors(fixed_path)
                clean_anchor = anchor[1:].strip()
                if clean_anchor not in target_anchors:
                    suggestion = get_close_matches(clean_anchor, target_anchors, n=1)
                    if suggestion:
                        new_anchor = "#" + suggestion[0]
                        print(f"🔁 {filepath}: fixed anchor `{anchor}` → `#{suggestion[0]}`")
                        anchor = new_anchor

            new_link = f"[{text}]({fixed_path}{anchor or ''})"
            line = line.replace(match.group(0), new_link)

        output_lines.append(line)
        if line != original:
            changed = True

    if changed:
        if dry_run:
            print(f"🔍 {filepath} would be updated.")
        else:
            with open(full_path, "w", encoding="utf-8") as f:
                f.writelines(output_lines)
            print(f"✅ Updated: {filepath}")

def run(dry=True):
    all_files = collect_all_files()
    for root, _, files in os.walk(DOCS_ROOT):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), DOCS_ROOT).replace("\\", "/")
                fix_links_in_file(rel_path, all_files, dry_run=dry)

