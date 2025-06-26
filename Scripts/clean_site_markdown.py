import os
import re

def fix_encoding(text):
    # Replace garbled emoji characters with correct ones
    replacements = {
        'ðŸ§±': '🧠',
        'ðŸ‘¤': '👤',
        'ðŸ‘‰': '👉',
        'ðŸ“‰': '📘',
        'ðŸ‘Š': '👊',
        'ðŸ¤‘': '🤱',
        'âœ…': '✅',
        'â‚¬': '€',
        'â€”': '—',
        'â€˜': "'",
        'â€™': "'",
        'â€œ': '"',
        'â€�': '"',
        'â€¦': '…'
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def clean_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    cleaned = []
    blank_count = 0
    for line in lines:
        line = fix_encoding(line.rstrip())

        # Reduce multiple blank lines
        if line.strip() == '':
            blank_count += 1
            if blank_count < 2:
                cleaned.append('')
            continue
        else:
            blank_count = 0

        # Compress wizard heading
        m = re.match(r'#\s?💸 Profit Wizard: Step (\d+) of \d+', line)
        if m:
            cleaned.append(f'## 💸 Step {m.group(1)}')
            continue

        # Clean "Your Answers So Far"
        if line.strip().startswith('**Your Answers So Far'):
            line = '🧠 ' + line.strip()

        # Normalize smart quotes
        line = line.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")

        cleaned.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned) + '\n')

    print(f'✅ Cleaned: {filepath}')


def scan_all_markdown(root='docs'):
    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith('.md'):
                clean_markdown_file(os.path.join(subdir, file))

if __name__ == '__main__':
    scan_all_markdown()
