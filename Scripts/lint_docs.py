import os
import re
import requests
import argparse

DOCS_DIR = 'docs'

# 🔍 Regex patterns
LINK_PATTERN = re.compile(r'\[.*?\]\((.*?)\)')
HEADING_PATTERN = re.compile(r'^\s{0,3}(#{1,6})\s+(.*)')
HTML_ANCHOR_PATTERN = re.compile(r'<h\d+\s+id="([^"]+)"')
BROKEN_ANCHOR_PATTERN = re.compile(r'\[([^\]]+)\]\(#[-️]*([^)]+)\)')

# 🧼 Anchor slugifier
def slugify(text):
    return text.strip().lower().replace(' ', '-').replace('–', '-').replace('.', '').replace(',', '')

def collect_anchors(content):
    anchors = set()
    for line in content.splitlines():
        m = HEADING_PATTERN.match(line)
        if m:
            anchors.add(slugify(m.group(2)))
        anchors.update(slugify(a) for a in HTML_ANCHOR_PATTERN.findall(line))
    return anchors

def patch_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    changed = False
    new_lines = []

    for line in lines:
        original = line
        matches = BROKEN_ANCHOR_PATTERN.findall(line)
        for text, raw_anchor in matches:
            clean = slugify(raw_anchor)
            broken = f'[{text}](#{raw_anchor})'
            fixed = f'[{text}](#{clean})'
            line = line.replace(broken, fixed)
        if line != original:
            changed = True
        new_lines.append(line)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"✅ Patched: {filepath}")

def fix_all():
    print("🔧 Fixing broken anchors...")
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                patch_file(os.path.join(root, file))
    print("✅ Anchor fixing done.\n")

def validate_links():
    print("🔍 Validating links...")
    broken = []
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue
            full_path = os.path.join(root, file)
            with open(full_path, encoding='utf-8') as f:
                content = f.read()
            anchors = collect_anchors(content)
            links = LINK_PATTERN.findall(content)
            for link in links:
                if link.startswith('#'):
                    anchor = slugify(link[1:])
                    if anchor not in anchors:
                        broken.append((full_path, f'#{anchor} (on this page)'))
                elif not link.startswith(('http://', 'https://')):
                    file_part = link.split('#')[0]
                    anchor_part = link.split('#')[1:] if '#' in link else []
                    target_path = os.path.normpath(os.path.join(root, file_part))
                    if not os.path.isfile(target_path):
                        broken.append((full_path, link))
                    elif anchor_part:
                        with open(target_path, encoding='utf-8') as tf:
                            tanchors = collect_anchors(tf.read())
                            if slugify(anchor_part[0]) not in tanchors:
                                broken.append((full_path, link))
                else:
                    try:
                        r = requests.head(link, allow_redirects=True, timeout=5)
                        if r.status_code >= 400:
                            broken.append((full_path, link))
                    except Exception:
                        broken.append((full_path, link))
    if broken:
        print("\n❌ Broken links or anchors found:")
        for f, l in broken:
            print(f"- {f} → {l}")
    else:
        print("✅ All links and anchors are valid.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Lint Markdown docs: fix + validate anchors")
    parser.add_argument('--fix', action='store_true', help='Automatically patch broken anchor links')
    args = parser.parse_args()

    if args.fix:
        fix_all()
    validate_links()
