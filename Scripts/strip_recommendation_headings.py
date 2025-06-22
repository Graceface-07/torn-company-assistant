import os
import re

RECOMMENDATION_DIR = 'docs/decision_flow'
HEADING_PATTERN = re.compile(r'^(\s{0,3}#{1,6})\s+(.*?)\s+Recommendation\s*$', re.IGNORECASE)

def strip_recommendation_heading(filepath):
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    changed = False
    for i, line in enumerate(lines):
        m = HEADING_PATTERN.match(line)
        if m:
            prefix, title = m.groups()
            lines[i] = f'{prefix} {title.strip()}\n'
            changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"🧹 Cleaned heading in: {filepath}")

def run_cleanup():
    print(f"🧼 Scanning: {RECOMMENDATION_DIR}\n")
    for file in os.listdir(RECOMMENDATION_DIR):
        if file.startswith("rec_") and file.endswith(".md"):
            strip_recommendation_heading(os.path.join(RECOMMENDATION_DIR, file))
    print("\n✅ Heading cleanup complete!")

if __name__ == '__main__':
    run_cleanup()
