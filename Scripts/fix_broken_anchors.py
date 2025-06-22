import os
import re
import unicodedata

DOCS_DIR = 'docs'

# Regex pattern to find [text](#anchor) format links
BROKEN_ANCHOR_PATTERN = re.compile(r'\[([^\]]+)\]\(#[-️]*([^)]+)\)')

def slugify(text):
    # Normalize and remove control chars, accents, emoji, etc.
    text = unicodedata.normalize("NFKD", text)
    text = ''.join(c for c in text if not unicodedata.category(c).startswith('C'))
    text = text.encode('ascii', 'ignore').decode()
    return text.strip().lower().replace(' ', '-').replace('–', '-').replace('.', '').replace(',', '').replace('/', '-')

def patch_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    changed = False
    new_lines = []

    for line in lines:
        original = line
        matches = BROKEN_ANCHOR_PATTERN.findall(line)
        for text, raw_anchor in matches:
            clean_anchor = slugify(raw_anchor)
            broken_link = f'[{text}](#{raw_anchor})'
            fixed_link = f'[{text}](#{clean_anchor})'
            line = line.replace(broken_link, fixed_link)
        if line != original:
            changed = True
        new_lines.append(line)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"✅ Patched: {filepath}")

def fix_all():
    print("🔧 Scanning for broken anchor links...\n")
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                patch_file(os.path.join(root, file))
    print("\n🏁 Anchor patch complete.")

if __name__ == '__main__':
    fix_all()
