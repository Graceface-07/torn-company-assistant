import os
import re

DOCS_DIR = 'docs'
TARGET_FILE = 'company_profiles.md'

HEADING_PATTERN = re.compile(r'^\s{0,3}(#{1,6})\s+(.*)')
LINK_PATTERN = re.compile(r'\[.*?\]\((#.*?)\)')

def slugify(text):
    return text.strip().lower().replace(' ', '-').replace('–', '-').replace('.', '').replace(',', '')

def extract_headings(lines):
    slugs = []
    for line in lines:
        match = HEADING_PATTERN.match(line)
        if match:
            text = match.group(2)
            slugs.append(slugify(text))
    return set(slugs)

def extract_links(lines):
    return [link[1:] for line in lines for link in LINK_PATTERN.findall(line) if link.startswith('#')]

def debug_file(path):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    headings = extract_headings(lines)
    links = extract_links(lines)

    print(f"\n📘 Scanning: {path}")
    print(f"\n🔹 Headings found ({len(headings)}):")
    for h in sorted(headings):
        print(f"  - #{h}")

    print(f"\n🔹 Anchor links found ({len(links)}):")
    for link in sorted(set(links)):
        print(f"  - #{link}")

    print(f"\n❌ Broken anchor links:")
    for link in links:
        if link not in headings:
            print(f"  - #{link} (no matching heading)")

if __name__ == '__main__':
    path = os.path.join(DOCS_DIR, TARGET_FILE)
    debug_file(path)
