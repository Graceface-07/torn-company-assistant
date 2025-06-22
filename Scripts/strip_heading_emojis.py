import os
import re

DOCS_DIR = 'docs'

HEADING_PATTERN = re.compile(r'^(\s{0,3})(#{1,6})\s+(.+)')

# Emoji pattern using Unicode ranges — this covers most emoji blocks
EMOJI_PATTERN = re.compile(r'[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U000024C2-\U0001F251]+', flags=re.UNICODE)

def remove_emoji(text):
    return EMOJI_PATTERN.sub('', text).strip()

def clean_heading(line):
    m = HEADING_PATTERN.match(line)
    if not m:
        return line
    indent, hashes, text = m.groups()
    cleaned_text = remove_emoji(text)
    return f'{indent}{hashes} {cleaned_text}\n'

def process_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    changed = False
    new_lines = []

    for line in lines:
        new_line = clean_heading(line)
        if new_line != line:
            changed = True
        new_lines.append(new_line)

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"🧼 Cleaned emojis in: {filepath}")

def clean_all():
    print("🧽 Stripping emojis from Markdown headings...\n")
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                process_file(os.path.join(root, file))
    print("\n✅ All done!")

if __name__ == '__main__':
    clean_all()
