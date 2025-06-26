import os
import re

def fix_encoding(text):
    bad_to_good = {
        'ðŸ§±': '🧠', 'ðŸ‘¤': '👤', 'ðŸ“‰': '📘', 'ðŸ’¸': '💸', 'ðŸ“„': '📄',
        'âœ…': '✅', 'â€“': '–', 'â€”': '—', 'â€˜': "'", 'â€™': "'", 'â€œ': '"', 'â€�': '"', 'â€¦': '…',
        'Â': '', 'Ã©': 'é', 'Ã ': 'à'
    }
    for bad, good in bad_to_good.items():
        text = text.replace(bad, good)
    return text

def clean_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    output = []
    prev_blank = False

    for i, line in enumerate(lines):
        line = line.rstrip()
        line = fix_encoding(line)
        line = line.replace('“', '"').replace('”', '"').replace("‘", "'").replace("’", "'")

        # Fix common wizard heading
        m = re.match(r'#\s?💸 Profit Wizard: Step (\d+) of \d+', line)
        if m:
            output.append(f'## 💸 Step {m.group(1)}')
            prev_blank = False
            continue

        # Collapse "Your Answers So Far"
        if line.startswith("**Your Answers So Far"):
            output.append("🧠 " + line)
            prev_blank = False
            continue

        # Remove >1 blank line
        if line.strip() == "":
            if not prev_blank:
                output.append("")
                prev_blank = True
            continue

        # Clean visible links if accidentally pasted as raw
        line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f"[{m.group(1)}]({m.group(2)})", line)

        output.append(line)
        prev_blank = False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output) + '\n')

    print(f"✅ Cleaned: {filepath}")

def clean_all_docs(root='docs'):
    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith('.md'):
                clean_markdown(os.path.join(subdir, file))

if __name__ == '__main__':
    clean_all_docs()
