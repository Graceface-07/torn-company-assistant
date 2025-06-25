import os
import re

DOCS_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs"))
LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?!http)([^)#]+\.md)(#[^\)]+)?\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s*(.+)$")

def find_md_files(base):
    for root, _, files in os.walk(base):
        for file in files:
            if file.endswith(".md"):
                yield os.path.join(root, file)

def extract_anchors(md_path):
    anchors = set()
    with open(md_path, "r", encoding="utf-8") as f:
        for line in f:
            match = HEADING_PATTERN.match(line)
            if match:
                title = match.group(2).strip()
                # MkDocs-style anchor: lowercase, dash-separated, remove symbols
                anchor = re.sub(r"[^\w\s\-]", "", title).strip().lower().replace(" ", "-")
                anchors.add(anchor)
    return anchors

def resolve_path(src, target):
    return os.path.normpath(os.path.join(os.path.dirname(src), target))

def validate():
    errors = []

    for src_file in find_md_files(DOCS_ROOT):
        rel_src = os.path.relpath(src_file, DOCS_ROOT)
        with open(src_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            for match in LINK_PATTERN.finditer(line):
                file_ref = match.group(1)
                anchor = match.group(2)[1:] if match.group(2) else None
                target_path = resolve_path(src_file, file_ref)

                if not os.path.isfile(target_path):
                    errors.append(f"❌ [{rel_src}:{i}] File not found → `{file_ref}`")
                    continue

                if anchor:
                    anchors = extract_anchors(target_path)
                    if anchor not in anchors:
                        suggest = f" (Hint: available anchors: {', '.join(list(anchors)[:3])}...)" if anchors else ""
                        errors.append(f"⚠️ [{rel_src}:{i}] Anchor `#{anchor}` not found in `{file_ref}`{suggest}")

    return errors

if __name__ == "__main__":
    issues = validate()
    if issues:
        print("🔍 Internal Link Issues Found:\n")
        for issue in issues:
            print(issue)
    else:
        print("✅ All file links and anchors resolved successfully!")
