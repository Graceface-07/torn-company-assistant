import os
import re

DOCS_DIR = 'docs'
VALID_ANCHORS = set()

def build_anchor_from_name(name):
    return name.lower().strip().replace(' ', '-')

# Step 1: Index all anchors from company_profiles
def extract_profile_anchors():
    path = os.path.join(DOCS_DIR, 'company_profiles', 'index.md')
    if not os.path.exists(path):
        print("⚠️  index.md not found.")
        return set()

    anchors = set()
    with open(path, encoding='utf-8') as f:
        for line in f:
            match = re.match(r'<h3 id="([^"]+)">', line)
            if match:
                anchors.add(match.group(1))
    return anchors

# Step 2: Patch other files
def patch_links(anchors):
    pattern = re.compile(r'\(#([^)]+)\)')
    total_fixed = 0

    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if not file.endswith('.md'):
                continue
            full_path = os.path.join(root, file)
            with open(full_path, encoding='utf-8') as f:
                content = f.read()

            matches = pattern.findall(content)
            fixed = 0
            for match in matches:
                clean = match.lower().replace(' ', '-').replace('–', '-')
                if clean not in anchors:
                    continue
                content = content.replace(f'(#${match})', f'({f"#{clean}"})')
                fixed += 1

            if fixed > 0:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"🔧 Patched {file}: {fixed} links")
                total_fixed += fixed

    print(f"\n✅ Done. {total_fixed} total links patched.")

if __name__ == '__main__':
    VALID_ANCHORS = extract_profile_anchors()
    if VALID_ANCHORS:
        patch_links(VALID_ANCHORS)
