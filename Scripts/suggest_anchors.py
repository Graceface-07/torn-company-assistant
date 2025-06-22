import os
import re
import difflib

DOCS_DIR = 'docs'
TARGET_FILE = 'company_profiles.md'

HEADING_PATTERN = re.compile(r'^\s{0,3}(#{1,6})\s+(.*)')
LINK_PATTERN = re.compile(r'\[.*?\]\((#.*?)\)')

def slugify(text):
    return text.strip().lower().replace(' ', '-').replace('–', '-').replace('.', '').replace(',', '')

def extract_headings(lines):
    slugs = []
    for line in lines:
        m = HEADING_PATTERN.match(line)
        if m:
            slugs.append(slugify(m.group(2)))
    return slugs

def extract_links(lines):
    return [link[1:] for line in lines for link in LINK_PATTERN.findall(line) if link.startswith('#')]

def suggest_fixes(broken_links, valid_anchors):
    for link in broken_links:
        suggestions = difflib.get_close_matches(link.lstrip('-️'), valid_anchors, n=1, cutoff=0.6)
        if suggestions:
            print(f"❌ #{link} → did you mean: #{suggestions[0]}")
        else:
            print(f"❌ #{link} → no close match found")

def run_suggestion():
    path = os.path.join(DOCS_DIR, TARGET_FILE)
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    anchors = extract_headings(lines)
    links = extract_links(lines)

    broken = [link for link in links if slugify(link) not in anchors]

    print(f"\n📘 Scanning: {path}")
    print(f"\n🔍 Found {len(anchors)} headings and {len(links)} anchor links")

    if broken:
        print(f"\n❌ {len(broken)} broken anchor links with suggestions:")
        suggest_fixes(broken, anchors)
    else:
        print("\n✅ All anchors look good!")

if __name__ == '__main__':
    run_suggestion()
